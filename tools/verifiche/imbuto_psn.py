"""Verifica «Imbuto: PSN, impegni e spesa» (#66, top-5 punto 3).

Confronta gli impegni dichiarati in ANAC per i CIG PSN (sottoclasse psn-servizio-da-determinare di imbuto-0.3.1),
prima e dopo la separazione dei tetti (imbuto_tetti.py), con quanto PSN S.p.A. dichiara nei bilanci: ricavi
fatturati (spesa effettiva delle PA verso PSN, per competenza) e portafoglio ordini (impegni contrattuali). Riporta
la copertura dei piani dei fabbisogni pubblicati (report/convenzioni/psn-database/documenti-psn.csv).

Ingressi versionati:
  esiti/2026-11-03/imbuto/riepilogo-0.3.1.json, esiti/2026-11-06/imbuto/tetti-cig.csv,
  esiti/2026-11-06/psn/bilanci-psn.json (cifre [R] di PSN, con sha256 dei PDF archiviati),
  report/convenzioni/psn-database/documenti-psn.csv
Uso:
  python tools/verifiche/imbuto_psn.py [--json OUT]
  python tools/verifiche/imbuto_psn.py --rigenera   # SUL SERVER: ricontrolla sha256 e cifre nei PDF archiviati (pdftotext)
"""
import csv, collections, hashlib, json, os, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.normpath(os.path.join(QUI, "..", ".."))
RIEP = os.path.join(RADICE, "esiti/2026-11-03/imbuto/riepilogo-0.3.1.json")
TETTI = os.path.join(RADICE, "esiti/2026-11-06/imbuto/tetti-cig.csv")
BIL = os.path.join(RADICE, "esiti/2026-11-06/psn/bilanci-psn.json")
DOC = os.path.join(RADICE, "report/convenzioni/psn-database/documenti-psn.csv")
PSN = "psn-servizio-da-determinare"


def rigenera():
    B = json.load(open(BIL, encoding="utf-8")); ok = True
    for d in B["documenti"]:
        p = os.path.join(RADICE, "archivio/mirror", d["url"].split("://", 1)[1])
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        t = subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True).stdout
        mancano = [v for v in B["controlli_testo"][str(d["esercizio"])].values() if v not in t]
        print(d["esercizio"], "sha256", "ok" if h == d["sha256"] else "DIVERSO", "| cifre non trovate:", mancano or "nessuna")
        ok &= h == d["sha256"] and not mancano
    sys.exit(0 if ok else 1)


def main():
    if "--rigenera" in sys.argv: return rigenera()
    P = json.load(open(RIEP, encoding="utf-8")); B = json.load(open(BIL, encoding="utf-8"))
    anc = collections.defaultdict(lambda: [0, 0.0])
    for r in P["righe"]:
        if r["sottoclasse"] == PSN:
            k = "2020-2023" if int(r["anno"]) <= 2023 else "dal-2024"; anc[k][0] += r["cig"]; anc[k][1] += r["euro"] or 0
    tet = [r for r in csv.DictReader(open(TETTI, encoding="utf-8")) if r["sottoclasse"] == PSN]
    cl = collections.defaultdict(lambda: [0, 0.0, 0.0])
    for r in tet:
        x = cl[(r["classe"], r["via"])]; x[0] += 1; x[1] += float(r["importo"]); x[2] += float(r["euro_netti"])
    tolto = sum(float(r["importo"]) - float(r["euro_netti"]) for r in tet)
    inc = sum(float(r["importo"]) for r in tet if r["classe"] == "incerto")
    imp_tot = anc["2020-2023"][1] + anc["dal-2024"][1]
    ricavi = sum(B["ricavi"].values()); port = B["portafoglio_ordini"]["2025-12-31"]
    docs = list(csv.DictReader(open(DOC, encoding="utf-8")))
    T = {"anac_psn": {k: {"cig": v[0], "euro": round(v[1])} for k, v in anc.items()},
         "anac_psn_tetti_oltre_50M_dal_2024": [{"classe": k[0], "via": k[1], "cig": v[0], "euro_dichiarati": round(v[1]), "euro_netti": round(v[2])} for k, v in sorted(cl.items())],
         "anac_psn_impegni_2020_2026_prima": round(imp_tot), "anac_psn_impegni_2020_2026_dopo_tetti": round(imp_tot - tolto),
         "di_cui_incerti_oltre_50M": round(inc),
         "psn_ricavi_2023_2025_R": ricavi, "psn_portafoglio_ordini_2025_R": port,
         "rapporto_impegni_dopo_tetti_su_portafoglio": round((imp_tot - tolto) / port, 3),
         "rapporto_ricavi_su_portafoglio": round(ricavi / port, 3),
         "rapporto_ricavi_su_impegni_dopo_tetti": round(ricavi / (imp_tot - tolto), 3),
         "quota_servizi_professionali_ricavi_2025_R": round(B["ricavi_2025_composizione"]["servizi_professionali"] / B["ricavi"]["2025"], 3),
         "documenti_psn": {"righe": len(docs), "ppdf_pubblicati": sum(r["tipo"] == "P" for r in docs),
                           "enti_ppdf": len({r["ente"] for r in docs if r["tipo"] == "P"}),
                           "pa_contrattualizzate_R": B["pa_contrattualizzate_2025-12-31"]}}
    T["documenti_psn"]["quota_enti_con_ppdf"] = round(T["documenti_psn"]["enti_ppdf"] / B["pa_contrattualizzate_2025-12-31"], 3)
    print(json.dumps(T, ensure_ascii=False, indent=1))
    if "--json" in sys.argv:
        json.dump(T, open(sys.argv[sys.argv.index("--json") + 1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
