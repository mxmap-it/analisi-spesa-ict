#!/usr/bin/env python3
"""Tabella unica degli spostamenti per CIG fra i livelli di raffinamento dell'imbuto (#71, #78).

Versione 0.1 (19/11/2026).

Perché: ogni livello di raffinamento (L2 regole, B1-B2 dataset BDNCP, L3 Opus sul testo,
L4 Opus con gli atti, revisione della via 6, regole delle licenze, verifiche manuali) produce
una tabella sua. Sommarle conta due volte un contratto toccato da due livelli. Qui:

1. si legge lo stato di partenza di ogni CIG dall'imbuto (`lavoro/imbuto/ict.csv`, asse A come
   in `imbuto_strati.py`);
2. si raccolgono tutti gli spostamenti proposti dai livelli, uno per riga (CIG x livello);
3. per ogni CIG vince il livello con la prova più forte (ordine PRIORITA sotto); i disaccordi
   fra livelli si contano e si pubblicano;
4. si ricalcolano i totali dell'asse A e la giurisdizione degli inclusi certi, lordi e al netto
   dei massimali (`tetti-cig-v2.csv`), prima e dopo.

Nessun livello modifica `ict.csv`: questo è uno strato sopra, rieseguibile da zero.

Uso: python3 tools/verifiche/imbuto_spostamenti.py [AAAA-MM-GG]
Uscite: esiti/<data>/imbuto/spostamenti/{spostamenti.csv.gz, finale.csv.gz, riepilogo.json, riepilogo.md}
"""
import collections
import csv
import glob
import gzip
import io
import hashlib
import json
import os
import re
import sys
from datetime import date

import yaml

VERSIONE = "0.2.0"
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GIORNO = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
ICT = os.environ.get("IMBUTO_ICT", os.path.join(R, "lavoro/imbuto/ict.csv"))
OUT = os.environ.get("IMBUTO_ESITI_OUT", os.path.join(R, "esiti", GIORNO, "imbuto", "spostamenti"))
csv.field_size_limit(10**9)



def gz_scrivi(path):
    """gzip di testo senza data (mtime=0; nell'intestazione solo il nome del file, costante): stessi byte a ogni esecuzione (#81, prova da clone pulito)."""
    return io.TextIOWrapper(gzip.GzipFile(path, mode="wb", mtime=0), encoding="utf-8", newline="")

def p(*a):
    return os.path.join(R, *a)


def ultimo(pattern):
    fs = sorted(glob.glob(p(pattern)))
    return fs[-1] if fs else None


# Ingressi: l'ultimo esito disponibile di ogni livello.
INGRESSI = {
    "tetti": ultimo("esiti/*/imbuto/tetti-cig-v2.csv"),
    "L2": ultimo("esiti/*/imbuto/raffinamento-l2.csv"),
    "L3": ultimo("esiti/*/imbuto/raffinamento-l3.csv"),
    # B: l'ultima versione del livello B (le versioni nuove stanno in sottocartelle vX.Y, che si ordinano dopo).
    "B": ultimo("esiti/*/imbuto/bdncp/v*/segnali.csv*") or ultimo("esiti/*/imbuto/bdncp/segnali.csv*"),
    "LIC": ultimo("esiti/*/imbuto/licenze-cig.csv"),
    "V6R": p("dati/classificazioni/imbuto-revisione.jsonl"),
    "L4": p("report/metodo/llm/raffinamento-l4/esiti"),
    # DC: datacenter propri («cloud in proprio», #52), regole di tools/verifiche/datacenter_proprio.py.
    "DC": ultimo("esiti/*/imbuto/datacenter/datacenter-cig.csv.gz"),
}
# Stato per CIG dopo i livelli, per le viste a valle (società in-house): dato di lavoro, non in git.
STATI_FINALI = os.environ.get("IMBUTO_STATI_FINALI", os.path.join(R, "lavoro/imbuto/stati-finali.csv.gz"))
DC_CFG = yaml.safe_load(open(p("config/datacenter_proprio.yaml"), encoding="utf-8"))
# Verifiche manuali o di altri filoni: qualunque esiti/*/imbuto/*/spostamenti-*.csv con colonne
# cig, a (stato finale), motivo, fonte; facoltative giurisdizione, importo (importo corretto).
# In L4 la «nota_quota» («X EUR su Y EUR») diventa una frazione dell'importo (codificata negativa).
# Di ogni file (sottocartella + nome) vale solo l'esito più recente: una verifica rieseguita sostituisce la precedente.
MANUALI = sorted({os.path.relpath(f, p("esiti")).split(os.sep, 1)[1]: f
                  for f in sorted(glob.glob(p("esiti/*/imbuto/*/spostamenti-*.csv")))}.values())

# Stati dell'asse A (nomi brevi).
STATI = ["fuori-misura", "escluso-non-ict", "ict-non-cloud", "cloud-certo", "inhouse-certo", "dc-proprio",
         "incerto-marchio", "incerto-s6"]
CERTI = ("cloud-certo", "inhouse-certo", "dc-proprio")
NOMI = {
    "fuori-misura": "fuori misura (S0 padre AQ, S2 sotto soglia)",
    "escluso-non-ict": "escluso certo, non ICT",
    "ict-non-cloud": "ICT non cloud",
    "cloud-certo": "incluso certo: cloud",
    "inhouse-certo": "incluso certo: infrastruttura in-house",
    "dc-proprio": "incluso certo: cloud in proprio (datacenter dell'ente)",
    "incerto-marchio": "incerto: marchio o lotto noto, da attribuire",
    "incerto-s6": "incerto: residuo S6",
}
# Ordine di forza della prova: vince il primo. Le verifiche manuali (MAN) leggono gli atti uno per uno.
PRIORITA = ["MAN", "L4", "V6R", "B2", "B1", "L3", "LIC", "L2"]
DESCR = {
    "MAN": "verifica manuale sugli atti (un contratto alla volta)",
    "L4": "Claude Opus con gli atti di gara (fonte primaria)",
    "V6R": "via 6 con revisione C1-C4 controvalidata",
    "B2": "in-house: aggiudicatario confrontato con l'Indice PA (BDNCP)",
    "B1": "quadro economico BDNCP: lavori >= 80 %",
    "L3": "Claude Opus sul testo, solo certezza alta",
    "LIC": "regole delle licenze (rendiconto imbuto § 4.5)",
    "L2": "regole sul testo (stampanti, consumabili, cablaggio)",
    "DC": "regole del datacenter proprio con prevalenza e dei servizi delle in-house ICT (si applicano dopo gli altri livelli, mai sopra una verifica manuale)",
}


def stato_base(strato, sotto):
    if strato in ("S0-padre-aq", "S2-sotto-soglia"):
        return "fuori-misura"
    if strato == "S1-escluso-non-ict":
        return "escluso-non-ict"
    if strato in ("S3-convenzione-lotto", "S4-marchio") and sotto == "cloud":
        return "cloud-certo"
    if strato == "S4-marchio" and sotto == "in-house":
        return "inhouse-certo"
    if strato == "S5-ict-non-cloud":
        return "ict-non-cloud"
    if strato == "S6-residuo":
        return "incerto-s6"
    return "incerto-marchio"


def giur(g):
    g = (g or "").strip().upper().replace("EXTRA UE", "EXTRA-UE")
    return g if g in ("IT", "UE", "EXTRA-UE") else ""


def periodo(anno):
    return "2020-2023" if int(anno or 0) <= 2023 else "dal-2024"


def apri(f):
    return gzip.open(f, "rt", encoding="utf-8", newline="") if f.endswith(".gz") else open(f, encoding="utf-8", newline="")


def sha(f):
    h = hashlib.sha256()
    with open(f, "rb") as x:
        for b in iter(lambda: x.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def raccogli():
    """Ritorna lista di spostamenti: dict(cig, livello, a, giurisdizione, importo, motivo, fonte)."""
    S = []
    add = lambda cig, liv, a, motivo, fonte, g="", imp=None: S.append(
        {"cig": cig.strip().upper(), "livello": liv, "a": a, "giurisdizione": giur(g), "importo_corretto": imp,
         "motivo": (motivo or "")[:200], "fonte": fonte})
    # L2: escono dalla misura cloud come ICT non cloud.
    for r in csv.DictReader(apri(INGRESSI["L2"])):
        add(r["cig"], "L2", "ict-non-cloud", f"regola L2: {r['motivo']}", os.path.relpath(INGRESSI["L2"], R))
    # L3: esce solo con certezza alta; «resta-incerto-L4» non sposta.
    for r in csv.DictReader(apri(INGRESSI["L3"])):
        a = {"esce-ict-non-cloud": "ict-non-cloud", "esce-non-ict": "escluso-non-ict"}.get(r["esito_l3"])
        if a:
            add(r["cig"], "L3", a, f"L3 {r['categoria']} ({r['certezza']})", os.path.relpath(INGRESSI["L3"], R))
    # B1 e B2 dal file dei segnali BDNCP.
    for r in csv.DictReader(apri(INGRESSI["B"])):
        if r["b1"] == "esce-lavori":
            add(r["cig"], "B1", "escluso-non-ict", f"lavori {r['qe_quota_lavori']} del quadro economico", os.path.relpath(INGRESSI["B"], R))
        if r["b2"] in ("non-sa", "sa-non-ipa", "senza-aggiudicatario"):
            add(r["cig"], "B2", "incerto-marchio", f"in-house non confermato dall'Indice PA: {r['b2']}", os.path.relpath(INGRESSI["B"], R))
    # Regole delle licenze: cloud / non cloud; «incerto» e «misto» non spostano.
    for r in csv.DictReader(apri(INGRESSI["LIC"])):
        a = {"cloud": "cloud-certo", "non-cloud": "ict-non-cloud"}.get(r["asse_a"])
        if a:
            add(r["cig"], "LIC", a, f"licenze: {r['via']} {r['provider']}", os.path.relpath(INGRESSI["LIC"], R), r["giurisdizione_prodotto"])
    # Revisione della via 6: entrano solo i controvalidati (C1-C4).
    for l in open(INGRESSI["V6R"], encoding="utf-8"):
        x = json.loads(l)
        if (x.get("revisione") or {}).get("stato") != "controvalidato":
            continue
        e = x["esito"]
        if e.get("asse_a") == "incluso-certo" and e.get("e_cloud") == "s":
            a = "cloud-certo"
        elif e.get("asse_a") == "escluso-certo":
            a = "ict-non-cloud" if e.get("servizio") not in ("non-ict",) else "escluso-non-ict"
        else:
            continue
        add(x["cig"], "V6R", a, f"via 6 controvalidata: {e.get('servizio','')}", "dati/classificazioni/imbuto-revisione.jsonl", e.get("giurisdizione"))
    # L4: incluso-certo cloud, escluso-certo (ICT o non ICT); «incerto» non sposta.
    for f in sorted(glob.glob(os.path.join(INGRESSI["L4"], "*.jsonl"))):
        for l in open(f, encoding="utf-8"):
            x = json.loads(l)
            a_ = x["asse_a"]
            if a_.get("stato") == "incluso-certo" and a_.get("e_cloud") == "s":
                a = "cloud-certo"
            elif a_.get("stato") == "escluso-certo":
                a = "escluso-non-ict" if a_.get("ict") == "n" else "ict-non-cloud"
            else:
                continue
            imp = None
            m = re.search(r"([\d.]+) EUR su ([\d.]+) EUR", x.get("nota_quota") or "")
            if m:  # quota cloud dichiarata dall'atto: si applica come frazione dell'importo
                imp = -float(m.group(1).replace(".", "")) / float(m.group(2).replace(".", ""))
            add(x["cig"], "L4", a, ("L4 " + (x.get("motivazione") or ""))[:200], os.path.relpath(f, R), x["asse_b"].get("giurisdizione"), imp)
    for f in MANUALI:
        for r in csv.DictReader(apri(f)):
            if r.get("a") not in STATI:
                continue
            imp = r.get("importo")
            add(r["cig"], "MAN", r["a"], r.get("motivo", ""), r.get("fonte") or os.path.relpath(f, R), r.get("giurisdizione", ""),
                float(imp) if imp not in (None, "") else None)
    return S


def main():
    os.makedirs(OUT, exist_ok=True)
    S = raccogli()
    per_cig = collections.defaultdict(list)
    for s in S:
        per_cig[s["cig"]].append(s)
    tetti = {}
    for r in csv.DictReader(apri(INGRESSI["tetti"])):
        try:
            tetti[r["cig"]] = float(r["euro_netti"])
        except ValueError:
            pass

    dc = {}
    if INGRESSI["DC"]:
        for r in csv.DictReader(apri(INGRESSI["DC"])):
            if r["esito"] == "dc-proprio":
                dc[r["cig"]] = r["famiglia"]
            elif r["esito"] == "servizio-inhouse":
                dc[r["cig"]] = "servizio-inhouse"
    dc_stati, dc_escluse = set(DC_CFG["origini"]["stati"]), set(DC_CFG["origini"]["sottoclassi_escluse"])
    dc_fam = collections.defaultdict(lambda: [0, 0.0, 0.0])   # (periodo, famiglia)
    fs = gz_scrivi(STATI_FINALI)
    ws = csv.writer(fs)
    ws.writerow(["cig", "anno", "stato", "livello", "giurisdizione", "euro_lordi", "euro_netti", "famiglia_dc"])

    agg = lambda: collections.defaultdict(lambda: [0, 0.0, 0.0])
    prima, dopo, giur_prima, giur_dopo = agg(), agg(), agg(), agg()
    flussi = agg()               # (periodo, da, a, livello decisivo)
    marg = agg()                 # effetto di ogni livello da solo (lordo dei doppioni)
    conflitti = collections.Counter()
    finale = []
    visti = set()

    def somma(d, k, lordo, netto):
        d[k][0] += 1; d[k][1] += lordo; d[k][2] += netto

    with open(ICT, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            cig = r["cig"].strip().upper()
            per = periodo(r["anno"])
            st0 = stato_base(r["strato"], r["sottoclasse"])
            lordo = float(r["importo"] or 0)
            netto = tetti.get(cig, lordo)
            g0 = giur(r["giurisdizione"])
            somma(prima, (per, st0), lordo, netto)
            if st0 in ("cloud-certo", "inhouse-certo"):
                somma(giur_prima, (per, st0, g0 or "IT" if st0 == "inhouse-certo" else g0 or "non determinata"), lordo, netto)
            mv = per_cig.get(cig)
            st1, g1, liv, imp = st0, g0, "", None
            if mv:
                visti.add(cig)
                for m in mv:
                    if m["a"] != st0:
                        somma(marg, (per, m["livello"], st0, m["a"]), lordo, netto)
                mv = sorted(mv, key=lambda m: PRIORITA.index(m["livello"]))
                arrivi = {m["a"] for m in mv}
                if len(arrivi) > 1:
                    conflitti[(per, " vs ".join(sorted({f"{m['livello']}:{m['a']}" for m in mv})))] += 1
                d = mv[0]
                st1, liv = d["a"], d["livello"]
                g1 = d["giurisdizione"] or (g0 if st1 == "cloud-certo" else "")
                imp = d["importo_corretto"]
                if imp is not None and imp < 0:      # frazione (quota cloud da L4)
                    lordo, netto = lordo * -imp, netto * -imp
                elif imp is not None:                # importo corretto da verifica manuale
                    lordo = netto = imp
                if st1 != st0:
                    somma(flussi, (per, st0, st1, liv), lordo, netto)
                finale.append([cig, r["anno"], r["strato"], r["sottoclasse"], st0, st1, liv,
                               "|".join(sorted({m["livello"] for m in mv})), int(len(arrivi) > 1),
                               round(float(r["importo"] or 0), 2), round(netto, 2), g0, g1, d["motivo"]])
            fam = (dc.get(cig) or "verifica-manuale") if st1 == "dc-proprio" else ""
            if st1 == "dc-proprio":
                somma(dc_fam, (per, fam), lordo, netto)
            elif cig in dc and st1 in dc_stati and r["sottoclasse"] not in dc_escluse and liv != "MAN":
                # cloud in proprio: datacenter dell'ente, sovrano IT (decisione di Fabio 20/11/2026)
                fam = dc[cig]
                if not mv:
                    finale.append([cig, r["anno"], r["strato"], r["sottoclasse"], st0, "inhouse-certo" if fam == "servizio-inhouse" else "dc-proprio", "DC", "DC", 0,
                                   round(float(r["importo"] or 0), 2), round(netto, 2), g0, "IT", f"datacenter proprio: {fam}"])
                else:
                    finale[-1][5], finale[-1][6], finale[-1][12] = ("inhouse-certo" if fam == "servizio-inhouse" else "dc-proprio"), "DC", "IT"
                    finale[-1][13] = f"datacenter proprio: {fam} (dopo {liv or 'nessun livello'}: {st1})"
                if st1 != st0:   # il flusso già contato dal livello precedente si sposta su DC
                    flussi[(per, st0, st1, liv)][0] -= 1; flussi[(per, st0, st1, liv)][1] -= lordo; flussi[(per, st0, st1, liv)][2] -= netto
                st1, liv, g1 = ("inhouse-certo" if fam == "servizio-inhouse" else "dc-proprio"), "DC", "IT"
                if st1 != st0:
                    somma(flussi, (per, st0, st1, liv), lordo, netto)
                somma(dc_fam, (per, fam), lordo, netto)
            ws.writerow([cig, r["anno"], st1, liv, g1 if st1 in CERTI else "", round(lordo, 2), round(netto, 2), fam])
            somma(dopo, (per, st1), lordo, netto)
            if st1 in CERTI:
                somma(giur_dopo, (per, st1, g1 or ("IT" if st1 in ("inhouse-certo", "dc-proprio") else "non determinata")), lordo, netto)

    fs.close()
    fuori = sorted(set(per_cig) - visti)
    with gz_scrivi(os.path.join(OUT, "spostamenti.csv.gz")) as f:
        w = csv.writer(f)
        w.writerow(["cig", "livello", "a", "giurisdizione", "importo_corretto", "motivo", "fonte"])
        for s in sorted(S, key=lambda s: (s["cig"], PRIORITA.index(s["livello"]))):
            w.writerow([s["cig"], s["livello"], s["a"], s["giurisdizione"], s["importo_corretto"] if s["importo_corretto"] is not None else "", s["motivo"], s["fonte"]])
    with gz_scrivi(os.path.join(OUT, "finale.csv.gz")) as f:
        w = csv.writer(f)
        w.writerow(["cig", "anno", "strato", "sottoclasse", "stato_prima", "stato_dopo", "livello_decisivo", "livelli",
                    "disaccordo", "importo", "euro_netti", "giurisdizione_prima", "giurisdizione_dopo", "motivo"])
        for x in sorted(finale):
            w.writerow(x)

    conv = lambda d: [{"chiave": list(k), "cig": v[0], "euro_lordi": round(v[1], 2), "euro_netti_tetti": round(v[2], 2)} for k, v in sorted(d.items())]
    T = {
        "versione": VERSIONE, "data": GIORNO, "strumento": "tools/verifiche/imbuto_spostamenti.py",
        "ingressi": {k: {"file": os.path.relpath(v, R), "sha256": sha(v)} for k, v in INGRESSI.items() if v and os.path.isfile(v)}
        | {"L4": {"cartella": os.path.relpath(INGRESSI["L4"], R), "file": len(glob.glob(os.path.join(INGRESSI["L4"], "*.jsonl")))},
           "ict": {"file": os.path.relpath(ICT, R)}, "manuali": [os.path.relpath(f, R) for f in MANUALI]},
        "priorita": [{"livello": l, "descrizione": DESCR[l]} for l in PRIORITA],
        "stati": NOMI,
        "spostamenti_proposti": len(S), "cig_toccati": len(per_cig), "cig_non_in_imbuto": len(fuori),
        "cig_non_in_imbuto_esempi": fuori[:20],
        "prima": conv(prima), "dopo": conv(dopo),
        "giurisdizione_prima": conv(giur_prima), "giurisdizione_dopo": conv(giur_dopo),
        "flussi_netti": conv({k: v for k, v in flussi.items() if v[0]}), "datacenter_per_famiglia": conv(dc_fam), "effetto_per_livello_lordo_doppioni": conv(marg),
        "disaccordi": [{"chiave": list(k), "cig": v} for k, v in sorted(conflitti.items())],
    }
    json.dump(T, open(os.path.join(OUT, "riepilogo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    scrivi_md(T)
    print(json.dumps({"cig_toccati": len(per_cig), "non_in_imbuto": len(fuori)}, ensure_ascii=False))


def scrivi_md(T):
    it = lambda x, n=2: f"{x:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    n_ = lambda x: f"{x:,}".replace(",", ".")
    pick = lambda lst, per: {tuple(r["chiave"][1:]): r for r in lst if r["chiave"][0] == per}
    L = [f"# Tabella unica degli spostamenti — {T['data']}", "",
         f"Strumento `{T['strumento']}` {T['versione']}. Spostamenti proposti {n_(T['spostamenti_proposti'])}, CIG toccati {n_(T['cig_toccati'])} (fuori dall'imbuto: {T['cig_non_in_imbuto']}).", "",
         "Lo strato S1 (non ICT per CPV e testo) non è in `ict.csv` e non è contato qui: «escluso certo, non ICT» conta solo i CIG che i livelli tolgono dall'ICT.", "",
         "## Asse A dal 2024, prima e dopo i livelli", "",
         "| stato | CIG prima | CIG dopo | mld lordi prima | mld lordi dopo | mld netti tetti prima | mld netti tetti dopo |",
         "|---|---:|---:|---:|---:|---:|---:|"]
    a, b = pick(T["prima"], "dal-2024"), pick(T["dopo"], "dal-2024")
    for s in STATI:
        x, y = a.get((s,), {"cig": 0, "euro_lordi": 0, "euro_netti_tetti": 0}), b.get((s,), {"cig": 0, "euro_lordi": 0, "euro_netti_tetti": 0})
        L.append(f"| {NOMI[s]} | {n_(x['cig'])} | {n_(y['cig'])} | {it(x['euro_lordi']/1e9)} | {it(y['euro_lordi']/1e9)} | {it(x['euro_netti_tetti']/1e9)} | {it(y['euro_netti_tetti']/1e9)} |")
    L += ["", "## Flussi netti dal 2024 (livello decisivo)", "", "| da | a | livello | CIG | M€ netti tetti |", "|---|---|---|---:|---:|"]
    for r in T["flussi_netti"]:
        if r["chiave"][0] == "dal-2024":
            L.append(f"| {r['chiave'][1]} | {r['chiave'][2]} | {r['chiave'][3]} | {r['cig']} | {it(r['euro_netti_tetti']/1e6, 1)} |")
    L += ["", "## Giurisdizione degli inclusi certi dal 2024 (netti tetti)", "", "| stato | giurisdizione | M€ prima | M€ dopo |", "|---|---|---:|---:|"]
    gp, gd = pick(T["giurisdizione_prima"], "dal-2024"), pick(T["giurisdizione_dopo"], "dal-2024")
    for k in sorted(set(gp) | set(gd)):
        L.append(f"| {k[0]} | {k[1]} | {it(gp.get(k, {}).get('euro_netti_tetti', 0)/1e6, 1)} | {it(gd.get(k, {}).get('euro_netti_tetti', 0)/1e6, 1)} |")
    L += ["", "## Cloud in proprio dal 2024: datacenter dell'ente per famiglia (netti tetti)", "", "| famiglia | CIG | M€ lordi | M€ netti tetti |", "|---|---:|---:|---:|"]
    for r in T["datacenter_per_famiglia"]:
        if r["chiave"][0] == "dal-2024":
            L.append(f"| {r['chiave'][1]} | {n_(r['cig'])} | {it(r['euro_lordi']/1e6, 1)} | {it(r['euro_netti_tetti']/1e6, 1)} |")
    L += ["", "## Disaccordi fra livelli", ""] + [f"- {r['chiave'][0]}: {r['chiave'][1]} — {r['cig']} CIG" for r in T["disaccordi"]]
    open(os.path.join(OUT, "riepilogo.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
