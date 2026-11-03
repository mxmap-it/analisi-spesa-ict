"""Attuativi BDNCP delle iniziative S5 (system management, sicurezza da remoto, SPC2, reti locali, PC) — dossier #55.

Streaming sui file CIG ANAC del mirror: in memoria restano solo le righe dei padri bersaglio e dei loro figli
(mai tutti i CIG: incidente del 27/10/2026). Per ogni CIG vale l'ultima versione pubblicata (file annuali, poi
aggiornamenti mensili). Da lanciare sul server con nice:

    nice -n 19 ionice -c3 .venv/bin/python tools/verifiche/attuativi_s5.py

Scrive lavoro/convenzioni/attuativi_s5.csv (righe) e lavoro/convenzioni/attuativi_s5.json (riepilogo).
Regole del riepilogo (dichiarate nei dossier report/convenzioni/):
- «anomalo»: importo_lotto >= 25 % del massimale BDNCP del padre (di solito l'ente ha copiato il massimale
  o il valore del lotto); escluso dai totali «puliti»;
- «possibili doppioni»: stessa SA e stesso importo ripetuti (CIG duplicati per lo stesso ordine), solo segnalati;
- parole chiave cercate nel solo oggetto_lotto (l'oggetto_gara ripete il titolo dell'AQ: «...e Chromebook»).
"""
import collections
import csv
import glob
import io
import json
import os
import re
import statistics
import sys
import zipfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "analisi"))
from attribuisci_provider import D, righe_cig  # noqa: E402

PADRI = {"7260902DDE": "SM-1836", "893944468E": "SM-2275", "B2094754F1": "SM-2710",
         "88846293CA": "SIC-2296-L1", "8884642E81": "SIC-2296-L2", "5133642F61": "SPC2-1367",
         "9543706356": "RL8-2223-L2", "9158053868": "PC-2425-L1", "9158062FD3": "PC-2425-L2",
         "91580749BC": "PC-2425-L3", "9823936871": "PC-2631-L2"}
CAMPI = ("cig", "cig_accordo_quadro", "oggetto_lotto", "oggetto_gara", "importo_lotto", "data_pubblicazione",
         "anno_pubblicazione", "denominazione_amministrazione_appaltante", "cod_cpv", "descrizione_cpv",
         "DATA_CANCELLAZIONE", "ESITO", "DURATA_PREVISTA")
KW = {"cloud": r"cloud|hosting|iaas|paas|saas|housing|data ?cent|disaster|backup",
      "soc": r"\bsoc\b|security operation|siem|monitoraggio",
      "voip": r"voip|voce|telefon|centralin",
      "chromebook": r"chrome ?book|cromebook|chrombook",
      "google": r"google|workspace|g suite",
      "microsoft": r"office ?365|microsoft ?365|m365|azure"}
MARCHI = r"\b(lenovo|hp|hewlett|acer|asus|fujitsu|apple|microsoft|samsung|cisco|huawei|aruba|juniper|extreme|fortinet|zyxel|alcatel)\b"
OUT = "lavoro/convenzioni"


def eur(s):
    try:
        return float((s or "0").replace(",", "."))
    except ValueError:
        return 0.0


def raccogli():
    out = {}

    def scan(rows):
        for r in rows:
            if r.get("cig_accordo_quadro") in PADRI or r.get("cig") in PADRI:
                out[r["cig"]] = {k: r.get(k, "") for k in CAMPI}
    for d in sorted(glob.glob(D + "cig-20*")):
        scan(righe_cig(d[-4:]))
    for z in sorted(glob.glob(D + "cig/filesystem/*-cig_csv.zip")):  # delta mensili in streaming, l'ultimo vince
        zf = zipfile.ZipFile(z)
        m = next(i for i in zf.namelist() if i.endswith(".csv"))
        scan(csv.DictReader(io.TextIOWrapper(zf.open(m), encoding="utf-8-sig", errors="replace"), delimiter=";"))
    agg = collections.defaultdict(set)
    for z in sorted(glob.glob(D + "aggiudicatari/filesystem/*_csv.zip")):
        zf = zipfile.ZipFile(z)
        m = next(i for i in zf.namelist() if i.endswith(".csv"))
        for r in csv.DictReader(io.TextIOWrapper(zf.open(m), encoding="utf-8-sig", errors="replace"), delimiter=";"):
            if r["cig"] in out:
                agg[r["cig"]].add((r["denominazione"] or "").strip())
    for c, r in out.items():
        r["aggiudicatari"] = " | ".join(sorted(agg[c]))
        r["iniziativa"] = PADRI.get(r["cig_accordo_quadro"]) or "PADRE:" + PADRI.get(c, "")
    return out


def riepiloga(R):
    ris = {}
    for p, nome in PADRI.items():
        pr = R.get(p, {})
        mass = eur(pr.get("importo_lotto"))
        F = [r for r in R.values() if r["cig_accordo_quadro"] == p and r["cig"] != p]
        vivi = [r for r in F if not r["DATA_CANCELLAZIONE"].strip()]
        soglia = 0.25 * mass if mass else float("inf")
        anom = [r for r in vivi if eur(r["importo_lotto"]) >= soglia]
        pul = [r for r in vivi if eur(r["importo_lotto"]) < soglia]
        imp = [eur(r["importo_lotto"]) for r in pul]
        dup = collections.Counter((r["denominazione_amministrazione_appaltante"], r["importo_lotto"]) for r in pul)
        anni = collections.defaultdict(lambda: [0, 0.0])
        for r in pul:
            anni[r["anno_pubblicazione"]][0] += 1
            anni[r["anno_pubblicazione"]][1] += eur(r["importo_lotto"])
        kw = {}
        for k, rx in KW.items():
            hit = [r for r in pul if re.search(rx, r["oggetto_lotto"].lower())]
            kw[k] = {"n": len(hit), "euro": round(sum(eur(r["importo_lotto"]) for r in hit)),
                     "esempi": [(r["cig"], r["importo_lotto"], r["denominazione_amministrazione_appaltante"][:50],
                                 r["oggetto_lotto"][:150]) for r in hit[:10]]}
        marchi = collections.Counter(m.lower() for r in pul for m in set(re.findall(MARCHI, r["oggetto_lotto"], re.I)))
        ris[nome] = {
            "padre": p, "padre_oggetto": pr.get("oggetto_lotto"), "padre_data": pr.get("data_pubblicazione"),
            "padre_aggiudicatari": pr.get("aggiudicatari"), "massimale_bdncp": mass,
            "n_attuativi": len(F), "cancellati": len(F) - len(vivi),
            "anomali": [(r["cig"], r["importo_lotto"], r["anno_pubblicazione"],
                         r["denominazione_amministrazione_appaltante"][:50], r["oggetto_lotto"][:80]) for r in anom],
            "euro_anomali": round(sum(eur(r["importo_lotto"]) for r in anom)),
            "n_puliti": len(pul), "euro_puliti": round(sum(imp)),
            "puliti_su_massimale": round(sum(imp) / mass, 3) if mass else None,
            "mediana": round(statistics.median(imp)) if imp else 0,
            "p90": round(sorted(imp)[int(.9 * len(imp))]) if imp else 0,
            "sotto_500": sum(1 for x in imp if x < 500),
            "doppioni": [sum(c - 1 for c in dup.values() if c > 1),
                         round(sum((c - 1) * eur(k[1]) for k, c in dup.items() if c > 1))],
            "per_anno": {k: [v[0], round(v[1])] for k, v in sorted(anni.items())},
            "cpv": collections.Counter(r["descrizione_cpv"][:60] for r in pul).most_common(6),
            "aggiudicatari": collections.Counter(a for r in pul for a in r["aggiudicatari"].split(" | ") if a).most_common(8),
            "impresa_inesistente": sum(1 for r in pul if "INESISTENTE" in r["aggiudicatari"]),
            "parole_chiave": kw, "marchi_in_oggetto": marchi.most_common(10)}
    return ris


def main():
    os.makedirs(OUT, exist_ok=True)
    R = raccogli()
    with open(f"{OUT}/attuativi_s5.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(CAMPI) + ["aggiudicatari", "iniziativa"])
        w.writeheader()
        w.writerows(R.values())
    ris = riepiloga(R)
    with open(f"{OUT}/attuativi_s5.json", "w", encoding="utf-8") as f:
        json.dump(ris, f, ensure_ascii=False, indent=1)
    for k, v in ris.items():
        print(k, v["n_attuativi"], v["n_puliti"], v["euro_puliti"], v["puliti_su_massimale"], len(v["anomali"]))


if __name__ == "__main__":
    main()
