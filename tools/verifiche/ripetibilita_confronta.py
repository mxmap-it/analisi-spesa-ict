#!/usr/bin/env python3
"""Confronto della prova di ripetibilità (tools/verifiche/ripetibilita.sh, #71 #74) con gli esiti pubblicati.

Per ogni coppia (pubblicato, rifatto): sha256 dei due file; se diversi, confronto del contenuto con tolleranza zero:
JSON campo per campo (dopo aver riportato ai nomi pubblicati i percorsi della cartella di prova), CSV riga per riga
(multinsieme delle righe, somme delle colonne numeriche). Registra anche gli ingressi (sha256 dei file del mirror ANAC
letti, del codice e della configurazione) e gli ingressi che NON stanno nell'archivio né in git.

Uso: .venv/bin/python tools/verifiche/ripetibilita_confronta.py lavoro/ripetibilita/<data> esiti/<data>/ripetibilita
  -> esito.json, esito.md"""
import collections, csv, glob, gzip, hashlib, io, json, os, subprocess, sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]
os.chdir(R)
csv.field_size_limit(1 << 30)
D, OUT = sys.argv[1].rstrip("/"), Path(sys.argv[2])
P18, P19 = "esiti/2026-11-18/imbuto", "esiti/2026-11-19/imbuto/bdncp"
E = f"{D}/esiti"

COPPIE = [  # passo, pubblicato, rifatto
    ("a", "lavoro/imbuto/ict.csv", f"{D}/prova/A/ict.csv"),
    ("a", f"{P18}/riepilogo-0.3.4.json", f"{D}/prova/A/riepilogo.json"),
] + [("b", f"{P18}/{n}", f"{E}/{n}") for n in (
    "distribuzione.json", "strati.json", "tetti-cig.csv", "tetti-fonti.json", "tetti.json", "tetti-cig-v2.csv",
    "revisione.json", "licenze-cig.csv", "licenze.json", "cig-ripetuti.json", "cig-ripetuti.csv")
] + [("c", f"{P19}/{n}", f"{E}/bdncp/{n}") for n in ("riepilogo.json", "campione-b1-esce-lavori.csv", "campione-b2-non-sa.csv")
] + [("c", f"{P19}/segnali.csv", f"{E}/bdncp/segnali.csv.gz")
] + [("d", f"{P18}/{n}", f"{E}/{n}") for n in (
    "raffinamento-l2.csv", "raffinamento-l2.json", "raffinamento-l2-campione.csv", "raffinamento-l3.csv", "raffinamento-l3.json")]

# percorsi della prova riportati ai nomi pubblicati prima del confronto del contenuto
ALIAS = [(f"{D}/prova/A/ict.csv", "lavoro/imbuto/ict.csv"), (f"{D}/prova/A/riepilogo.json", f"{P18}/riepilogo-0.3.4.json"),
         (f"{E}/bdncp", P19), (E, P18)]


def sha(p):
    h = hashlib.sha256()
    op = gzip.open if str(p).endswith(".gz") else open
    with op(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def testo(p):
    op = gzip.open if str(p).endswith(".gz") else open
    with op(p, "rt", encoding="utf-8", newline="") as f:
        s = f.read()
    for a, b in ALIAS:
        s = s.replace(a, b)
    return s


def diff_json(a, b, via="", out=None):
    out = [] if out is None else out
    if type(a) != type(b):
        out.append((via, a, b))
    elif isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append((f"{via}.{k}", a.get(k, "<assente>"), b.get(k, "<assente>")))
            else:
                diff_json(a[k], b[k], f"{via}.{k}", out)
    elif isinstance(a, list):
        if len(a) != len(b):
            out.append((f"{via}[len]", len(a), len(b)))
        for i, (x, y) in enumerate(zip(a, b)):
            diff_json(x, y, f"{via}[{i}]", out)
    elif a != b:
        out.append((via, a, b))
    return out


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def diff_csv(sp, sr):
    rp, rr = list(csv.reader(io.StringIO(sp))), list(csv.reader(io.StringIO(sr)))
    r = {"intestazione_uguale": rp[:1] == rr[:1], "righe_pubblicato": len(rp) - 1, "righe_rifatto": len(rr) - 1}
    cp, cr = collections.Counter(map(tuple, rp[1:])), collections.Counter(map(tuple, rr[1:]))
    sol_p, sol_r = cp - cr, cr - cp
    r["righe_solo_pubblicato"], r["righe_solo_rifatto"] = sum(sol_p.values()), sum(sol_r.values())
    r["esempi_solo_pubblicato"] = [list(x)[:6] for x in list(sol_p)[:5]]
    r["esempi_solo_rifatto"] = [list(x)[:6] for x in list(sol_r)[:5]]
    if rp[:1] == rr[:1] and rp:
        somme = {}
        for j, c in enumerate(rp[0]):
            a = [num(x[j]) for x in rp[1:] if j < len(x)]
            b = [num(x[j]) for x in rr[1:] if j < len(x)]
            if a and sum(v is not None for v in a) > 0.9 * len(a):
                sa, sb = sum(v or 0 for v in a), sum(v or 0 for v in b)
                if round(sa, 2) != round(sb, 2):
                    somme[c] = {"pubblicato": round(sa, 2), "rifatto": round(sb, 2)}
        r["somme_diverse"] = somme
    r["ordine_diverso_stesso_contenuto"] = not sol_p and not sol_r and rp != rr
    if r["ordine_diverso_stesso_contenuto"]:  # sha256 canonico: intestazione + righe ordinate, uguale se il contenuto è uguale
        can = lambda rows: hashlib.sha256("\n".join([",".join(rows[0])] + sorted(",".join(x) for x in rows[1:])).encode()).hexdigest()
        r["sha256_canonico_pubblicato"], r["sha256_canonico_rifatto"] = can(rp), can(rr)
    return r


SHA_ICT_PUBBLICATO = "9604940172cd6f80b52617cf302fcaa7c7002fd06a1162ea93c782c9f8a2fd5c"


def classifica(d, sha_ict_rifatto):
    """tipo di ogni differenza JSON: virgola mobile (|Δ| < 0,01), sha256 di ict.csv (ordine delle righe), altro."""
    t = collections.Counter(); mx = 0.0
    for c, a, b in d:
        if isinstance(a, float) and isinstance(b, (int, float)) and abs(a - b) < 0.01:
            t["virgola-mobile"] += 1; mx = max(mx, abs(a - b))
        elif a == SHA_ICT_PUBBLICATO and b == sha_ict_rifatto:
            t["sha256-ict-ordine-righe"] += 1
        else:
            t["altro"] += 1
    return dict(t), mx


def confronta(passo, pub, rif):
    x = {"passo": passo, "pubblicato": pub, "rifatto": rif}
    if not os.path.exists(rif):
        x["esito"] = "MANCANTE (il passo non ha prodotto il file)"; return x
    if not os.path.exists(pub):
        x["esito"] = "pubblicato assente"; return x
    x["sha256_pubblicato"], x["sha256_rifatto"] = sha(pub), sha(rif)
    if x["sha256_pubblicato"] == x["sha256_rifatto"]:
        x["esito"] = "uguale (sha256)"; return x
    sp, sr = testo(pub), testo(rif)
    if sp == sr:
        x["esito"] = "uguale dopo aver riportato i percorsi della prova ai nomi pubblicati"; return x
    if pub.endswith(".json"):
        d = diff_json(json.loads(sp), json.loads(sr))
        x["differenze"] = len(d)
        x["dettaglio"] = [{"campo": c, "pubblicato": a, "rifatto": b} for c, a, b in d[:40]]
        tipi, mx = classifica(d, sha(f"{D}/prova/A/ict.csv"))
        x["tipi_differenze"], x["max_delta_virgola_mobile"] = tipi, mx
        x["esito"] = (f"uguale nei numeri: {len(d)} campi diversi solo per " + ", ".join(f"{k} {v}" for k, v in tipi.items())
                      + (f" (Δ massimo {mx:.1e} €)" if mx else "")) if "altro" not in tipi else f"DIVERSO: {len(d)} campi ({tipi})"
    else:
        x["csv"] = diff_csv(sp, sr)
        c = x["csv"]
        x["esito"] = ("uguale nel contenuto, ordine delle righe diverso (sha256 canonico " + ("uguale" if c.get("sha256_canonico_pubblicato") == c.get("sha256_canonico_rifatto") else "DIVERSO") + ")"
                      if c["ordine_diverso_stesso_contenuto"] else
                      f"DIVERSO: {c['righe_solo_pubblicato']} righe solo nel pubblicato, {c['righe_solo_rifatto']} solo nel rifatto")
    return x


def ingressi():
    A = "archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/"
    zips = sorted(glob.glob(A + "cig-20*/filesystem/cig_csv_*.zip") + glob.glob(A + "cig/filesystem/*-cig_csv.zip") +
                  glob.glob(A + "aggiudicatari/filesystem/*_csv.zip"))
    mir = {p: sha(p) for p in zips}
    codice = ["tools/analisi/imbuto.py", "tools/analisi/classifica.py", "tools/analisi/attribuisci_provider.py",
              "tools/verifiche/imbuto_prova_034.py", "tools/verifiche/imbuto_strati.py", "tools/verifiche/imbuto_tetti.py",
              "tools/verifiche/imbuto_revisione.py", "tools/verifiche/imbuto_licenze.py", "tools/verifiche/imbuto_cig_ripetuti.py",
              "tools/verifiche/imbuto_bdncp.py", "tools/llm/raffinamento.py"] + sorted(glob.glob("config/*.yaml"))
    versionati = set(subprocess.run(["git", "ls-files"], capture_output=True, text=True).stdout.split())
    fuori = {}
    for p in ["lavoro/pvl/cig_link.csv", "lavoro/convenzioni/attuativi.csv"]:
        fuori[p] = {"sha256": sha(p) if os.path.exists(p) else None, "in_git": p in versionati,
                    "usato_da": "imbuto_strati (link PVL per strato)" if "pvl" in p else "imbuto_licenze (attuativi delle convenzioni)"}
    pac = sorted(glob.glob("lavoro/raffinamento/pacchetti/d*.jsonl"))
    h = hashlib.sha256()
    for p in pac:
        h.update(open(p, "rb").read())
    fuori["lavoro/raffinamento/pacchetti/d*.jsonl"] = {"file": len(pac), "sha256_concatenati": h.hexdigest(), "in_git": False,
                                                       "usato_da": "raffinamento.py esito (ingresso di L3: importo e oggetto)"}
    if os.path.exists("config/ingressi-lavoro.yaml"):  # M12: registro degli ingressi conservati in git o nell'archivio
        import yaml
        for e in yaml.safe_load(open("config/ingressi-lavoro.yaml", encoding="utf-8"))["ingressi"]:
            k = e["percorso"] + ("/d*.jsonl" if e["via"] == "git-tar" else "")
            if k in fuori:
                fuori[k]["conservato"] = e["via"] + ": " + (e.get("copia") or e.get("blob") or "")
                fuori[k]["sha256_registro"] = e.get("sha256") or e.get("sha256_concatenati")
    return {"commit": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
            "mirror_anac_letti_dal_passo_a": {"file": len(mir), "byte": sum(os.path.getsize(p) for p in mir), "sha256": mir},
            "codice_e_configurazione": {p: sha(p) for p in codice if os.path.exists(p)},
            "fuori_archivio": fuori}


def tempi():
    t = []
    p = Path(D) / "tempi.tsv"
    if p.exists():
        for l in p.read_text(encoding="utf-8").splitlines():
            n, a, b, c, cmd = l.split("\t", 4)
            t.append({"passo": n, "secondi": int(b) - int(a), "codice": int(c), "comando": cmd})
    return t


NOTE = [
    "**Ordine delle righe** (ict.csv, licenze-cig.csv, raffinamento-l2.csv): imbuto_prova_034.py legge il delta da duckdb con "
    "`preserve_insertion_order=false` e 2 thread, quindi l'ordine delle righe di ict.csv cambia da un'esecuzione all'altra; "
    "chi legge ict.csv in sequenza eredita l'ordine. Il contenuto è identico (sha256 canonico, righe ordinate, uguale). "
    "Per questo lo sha256 di ict.csv registrato da tetti-fonti.json, bdncp/riepilogo.json e raffinamento-l2.json è diverso. "
    "Correzione proposta: scrivere ict.csv ordinato per (anno, cig) e registrare lo sha256 canonico. "
    "**Corretto il 19/11 (M12):** imbuto.py scrive ict.csv ordinato per CIG (ordina_ict; prova tools/verifiche/ripetibilita_ordina_ict.py).",
    "**Virgola mobile** (distribuzione.json, strati.json, solo i campi `euro` e `euro_link` non arrotondati del link PVL): "
    "somme parallele di duckdb in ordine diverso, differenza massima sotto 0,001 €. Correzione proposta: arrotondare al centesimo. "
    "**Corretto il 19/11 (M12):** imbuto_strati.py somma in centesimi interi (CENT).",
    "**Deviazione della prova**: «prepara» è andata in Out of Memory con 8 GB di memoria virtuale (ulimit -v) mentre il 9/11 "
    "era riuscita; rifatta con 12 GB (memory_limit di duckdb invariato a 4 GB). La variante A ha girato con 8 GB come l'originale.",
    "**Ingressi fuori dall'archivio content-addressed e fuori da git**: lavoro/pvl/cig_link.csv (scaricamento API PVL del 4/11), "
    "lavoro/convenzioni/attuativi.csv, lavoro/raffinamento/pacchetti/ (ingressi di L3). Oggi sono sul server e la prova li ha "
    "riletti; da un clone pulito mancherebbero. Correzione proposta: versionarli o archiviarli con sha256. "
    "**Corretto il 19/11 (M12):** registro config/ingressi-lavoro.yaml, copie in dati/ingressi/ (git) e cig_link.csv come blob "
    "nell'archivio; tools/ingressi_lavoro.py verifica | ripristina.",
    "**Esiti del modello linguistico**: L3, L4 e via 6 non si rigenerano: si rileggono gli esiti versionati in git.",
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    risultati = [confronta(*c) for c in COPPIE]
    T = tempi()
    J = {"versione": "ripetibilita 0.1", "cartella_prova": D, "tempi": T, "durata_totale_min": round(sum(x["secondi"] for x in T) / 60, 1),
         "confronti": risultati, "ingressi": ingressi(), "note": NOTE,
         "non_ripetibili_per_natura": {
             "L3": "Claude Opus legge il testo (report/metodo/llm/raffinamento/esiti/, versionati): si rilegge, non si rigenera",
             "L4": "Claude Opus cerca e legge gli atti (report/metodo/llm/raffinamento-l4/esiti/, versionati; atti con sha256 in dati/atti/)",
             "via6_revisione": "letture del modello (report/metodo/llm/imbuto-g1g3, imbuto-revisione): ingressi versionati di imbuto_revisione"}}
    json.dump(J, open(OUT / "esito.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    righe = ["# Prova di ripetibilità dell'imbuto, " + os.path.basename(D), "",
             f"Rifatto da zero in `{D}` con `tools/verifiche/ripetibilita.sh`, confronto con `tools/verifiche/ripetibilita_confronta.py`. "
             f"Commit {J['ingressi']['commit'][:8]}. Durata dei passi: {J['durata_totale_min']} minuti.", "",
             "| passo | durata | codice |", "|---|---:|---:|"]
    righe += [f"| {t['passo']} | {t['secondi'] // 60} min {t['secondi'] % 60} s | {t['codice']} |" for t in T]
    righe += ["", "| passo | file pubblicato | esito |", "|---|---|---|"]
    righe += [f"| {x['passo']} | `{x['pubblicato']}` | {x['esito']} |" for x in risultati]
    diversi = [x for x in risultati if x["esito"].startswith(("DIVERSO", "MANCANTE"))]
    if diversi:
        righe += ["", "## Differenze", ""]
        for x in diversi:
            righe.append(f"- `{x['pubblicato']}`: {x['esito']}")
            for d in x.get("dettaglio", [])[:10]:
                righe.append(f"  - `{d['campo']}`: pubblicato {str(d['pubblicato'])[:80]} / rifatto {str(d['rifatto'])[:80]}")
            if "csv" in x:
                c = x["csv"]
                righe.append(f"  - righe {c['righe_pubblicato']} / {c['righe_rifatto']}; somme diverse: {json.dumps(c.get('somme_diverse', {}), ensure_ascii=False)[:300]}")
                for e in c["esempi_solo_pubblicato"][:3]:
                    righe.append(f"  - solo pubblicato: {e}")
                for e in c["esempi_solo_rifatto"][:3]:
                    righe.append(f"  - solo rifatto: {e}")
    righe += ["", "## Ingressi", "",
              f"- Mirror ANAC letto dal passo a: {J['ingressi']['mirror_anac_letti_dal_passo_a']['file']} file zip, "
              f"{J['ingressi']['mirror_anac_letti_dal_passo_a']['byte'] / 1e9:.1f} GB (sha256 in esito.json).",
              "- Codice e configurazione: sha256 in esito.json.", "- Ingressi fuori dall'archivio e fuori da git:"]
    for p, v in J["ingressi"]["fuori_archivio"].items():
        righe.append(f"  - `{p}` ({v['usato_da']}): in git = {v['in_git']}")
    righe += ["", "## Cause delle differenze e deviazioni", ""] + [f"- {n}" for n in NOTE]
    righe += ["", "## Non ripetibili per natura", ""] + [f"- **{k}**: {v}" for k, v in J["non_ripetibili_per_natura"].items()]
    (OUT / "esito.md").write_text("\n".join(righe) + "\n", encoding="utf-8")
    print("\n".join(righe))


if __name__ == "__main__":
    main()
