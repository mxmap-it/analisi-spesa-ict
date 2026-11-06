"""#41 Rivenditori: codici fiscali e nazionalità dagli aggiudicatari ANAC, e riconciliazione dei totali della mappa v3.

Ingresso: lavoro/attribuzione/[0-9]*.csv (attribuisci_provider.py, regole v3; stessi filtri di tools/analisi/rivenditori.py)
e il dataset ANAC aggiudicatari del mirror (aggiudicatari_csv.zip, sha256 nel manifest). Gira sul server (zip da 800 MB
letto in streaming, si tengono solo i CIG attribuiti).

Riconciliazione (perché il file per rivenditore somma più del totale per canale):
  A = somma per canale come rivenditori.py (ogni riga dei file annuali, anche CIG ripetuti su più anni);
  B = somma per rivenditore come rivenditori.py (l'importo del CIG si somma a OGNI membro dell'RTI);
  C = A dopo dedup per CIG (si tiene l'anno più recente);
  D = C ripartito fra gli aggiudicatari ANAC del CIG: alla mandataria se indicata, altrimenti in parti uguali.
Nazionalità del rivenditore dal codice fiscale ANAC: 11 cifre o CF di persona fisica (16 caratteri) = IT; altro = non IT
o non valido (si riporta il tipo_soggetto). Giurisdizione del PRODOTTO da config/marchi_cloud.yaml.

Uso (server): nice .venv/bin/python tools/verifiche/rivenditori_cf.py -> esiti/<oggi>/rivenditori/rivenditori-cf.{json,csv}"""
import csv, glob, io, json, os, re, sys, zipfile, datetime, collections
from pathlib import Path

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/analisi"))
from classifica import Classificatore  # noqa: E402
from rivenditori import normalizza  # noqa: E402

ZIP = R / "archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/aggiudicatari/filesystem/aggiudicatari_csv.zip"
RX_IT = re.compile(r"^(\d{11}|[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z])$")


def main():
    csv.field_size_limit(10 ** 8)
    c = Classificatore()
    giur = dict(c.giur); giur.setdefault("VMware", "EXTRA-UE")
    A = collections.Counter(); B = collections.Counter(); righe = 0
    ultimo = {}
    for f in sorted(glob.glob(str(R / "lavoro/attribuzione/[0-9]*.csv"))):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            if r["e_padre"] == "1" or not r["provider"] or r["servizio"] in ("servizi-professionali", "in-house", "software-infrastruttura"): continue
            if r.get("importo_da_verificare"): continue
            imp = float(r["importo_lotto"] or 0)
            ag = [a.strip() for a in r["aggiudicatari"].split(";") if a.strip()]
            ch = c.canale(r["provider"], ag); g = giur.get(r["provider"], "?")
            A[(g, ch)] += imp; righe += 1
            if ch == "rivenditore":
                for _ in ag: B[g] += imp
            ultimo[r["cig"]] = (r["provider"], g, ch, imp, ag)  # file in ordine di anno: vince il più recente
    C = collections.Counter()
    for v in ultimo.values(): C[(v[1], v[2])] += v[3]
    cig_riv = {k for k, v in ultimo.items() if v[2] == "rivenditore"}
    ag_anac = collections.defaultdict(list)
    with zipfile.ZipFile(ZIP) as z, z.open("aggiudicatari_csv.csv") as fb:
        for r in csv.DictReader(io.TextIOWrapper(fb, encoding="utf-8", errors="replace"), delimiter=";"):
            if r["cig"] in cig_riv:
                ag_anac[r["cig"]].append((r["codice_fiscale"].strip().upper(), r["denominazione"].strip(), (r["ruolo"] or "").upper(), r["tipo_soggetto"]))
    D = collections.Counter(); naz = collections.defaultdict(collections.Counter); per_cf = {}
    senza_anac = collections.Counter(); tipi_non_it = collections.Counter()
    for cig in cig_riv:
        prov, g, ch, imp, ag = ultimo[cig]
        rows = list({x[0] or x[1]: x for x in ag_anac.get(cig, [])}.values())
        if not rows:
            senza_anac[g] += imp; continue
        mand = [x for x in rows if "MANDATARI" in x[2]]
        quote = [(x, imp) for x in mand[:1]] if mand else [(x, imp / len(rows)) for x in rows]
        for (cf, den, ruolo, tipo), q in quote:
            n = "IT" if RX_IT.match(cf) else "non-IT-o-non-valido"
            if n != "IT": tipi_non_it[(cf, den, tipo[:60])] += q
            D[g] += q; naz[g][n] += q
            p = per_cf.setdefault(cf or den, {"cf": cf, "denominazione": den, "nazionalita_cf": n, "importo": 0.0, "estero": 0.0, "cig": 0, "prodotti": collections.Counter()})
            p["importo"] += q; p["cig"] += 1; p["prodotti"][prov] += q
            if g == "EXTRA-UE": p["estero"] += q
    top = sorted(per_cf.values(), key=lambda x: -x["estero"])
    oggi = datetime.date.today().isoformat(); o = R / f"esiti/{oggi}/rivenditori"; os.makedirs(o, exist_ok=True)
    with open(o / "rivenditori-cf.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["cf", "denominazione", "nazionalita_cf", "cig", "importo_eur", "estero_extra_ue_eur", "prodotti"])
        for p in top:
            w.writerow([p["cf"], p["denominazione"], p["nazionalita_cf"], p["cig"], round(p["importo"]), round(p["estero"]),
                        " ; ".join(f"{k}={round(v)}" for k, v in p["prodotti"].most_common())])
    r2 = lambda cnt: {f"{k[0]}|{k[1]}" if isinstance(k, tuple) else k: round(v) for k, v in sorted(cnt.items())}
    out = {"ingresso": {"attribuzione": "lavoro/attribuzione/[0-9]*.csv (v3)", "aggiudicatari": str(ZIP.relative_to(R))},
           "righe_considerate": righe, "cig_distinti": len(ultimo), "cig_ripetuti_su_piu_anni": righe - len(ultimo),
           "A_per_canale_righe": r2(A), "B_per_rivenditore_somma_ogni_membro": r2(B),
           "C_per_canale_dedup_cig": r2(C), "D_rivenditore_ripartito_dedup": r2(D),
           "rivenditore_senza_aggiudicatari_anac": r2(senza_anac),
           "nazionalita_rivenditore_per_giurisdizione_prodotto": {g: {k: round(v) for k, v in c2.items()} for g, c2 in naz.items()},
           "quota_extra_ue_rivenduta_da_cf_italiani": round(naz["EXTRA-UE"]["IT"] / sum(naz["EXTRA-UE"].values()), 4) if naz["EXTRA-UE"] else None,
           "rivenditori_cf_distinti": len(per_cf),
           "non_it_o_non_validi_primi": [{"cf": k[0], "denominazione": k[1], "tipo_soggetto": k[2], "importo": round(v)} for k, v in tipi_non_it.most_common(15)],
           "primi_15_estero": [{"cf": p["cf"], "denominazione": p["denominazione"], "nazionalita_cf": p["nazionalita_cf"], "estero": round(p["estero"])} for p in top[:15]],
           "impresa_inesistente": [{"cf": p["cf"], "denominazione": p["denominazione"], "importo": round(p["importo"]), "cig": p["cig"]}
                                   for p in per_cf.values() if "INESISTENTE" in normalizza(p["denominazione"])]}
    json.dump(out, open(o / "rivenditori-cf.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in out.items() if k not in ("primi_15_estero",)}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
