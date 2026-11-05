"""Strato S3 dell'imbuto, passo 1: quali accordi quadro e convenzioni (CIG padre) generano la spesa ICT dal 2020.
Per ogni cig_accordo_quadro richiamato da contratti attuativi ICT (CPV ICT) conta attuativi ed euro, e riporta
l'oggetto, la stazione appaltante e l'anno del CIG padre. È la lista di lavoro per la base di conoscenza delle
iniziative (config/lotti_cloud.yaml, report/metodo/llm/conoscenza-iniziative.yaml): si decifrano per primi i padri
che pesano di più. Deterministico, streaming, due passate (mai tutti i CIG in memoria).

Uso: python tools/analisi/padri_ict.py [anno_iniziale] [anno_finale] [uscita.csv] -> default report/metodo/conoscenza/padri-ict.csv
(#62: tools/analisi/padri_ict.py 2024 2025 report/convenzioni/database/padri-ict-2024-2025.csv)"""
import csv, glob, os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from classifica import CPV_ICT  # noqa: E402
from attribuisci_provider import righe_cig, D  # noqa: E402


def main(anno0=2020, anno1=2026, uscita="report/metodo/conoscenza/padri-ict.csv"):
    anni = {str(a) for a in range(anno0, anno1 + 1)}
    fonti = sorted(p[-4:] for p in glob.glob(D + "cig-20*")) + ["delta"]
    delta_cig = {r["cig"] for r in righe_cig("delta")}
    n = collections.Counter(); eur = collections.Counter(); anni_att = collections.defaultdict(set)
    for fonte in fonti:
        for r in righe_cig(fonte):
            if fonte != "delta" and r["cig"] in delta_cig: continue
            aq = r["cig_accordo_quadro"]
            if not aq or (r.get("anno_pubblicazione") or "").strip() not in anni: continue
            if not CPV_ICT.match(r["cod_cpv"] or ""): continue
            try: imp = float(r["importo_lotto"] or 0)
            except ValueError: imp = 0.0
            n[aq] += 1; eur[aq] += imp; anni_att[aq].add(r["anno_pubblicazione"])
    info = {}
    for fonte in fonti:
        for r in righe_cig(fonte):
            if r["cig"] in n: info[r["cig"]] = (r.get("anno_pubblicazione", ""), r.get("denominazione_amministrazione_appaltante", ""),
                                                ((r.get("oggetto_gara") or "") + " | " + (r.get("oggetto_lotto") or ""))[:300], r.get("cod_cpv", ""))
    os.makedirs(os.path.dirname(uscita), exist_ok=True)
    with open(uscita, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["cig_padre", "attuativi_ict", "euro_attuativi", "anni_attuativi", "anno_padre", "stazione_appaltante_padre", "oggetto_padre", "cpv_padre"])
        for aq, _ in sorted(eur.items(), key=lambda x: -x[1]):
            w.writerow([aq, n[aq], round(eur[aq]), ",".join(sorted(anni_att[aq])), *info.get(aq, ("", "", "", ""))])
    print(len(n), "padri ICT")


if __name__ == "__main__":
    a = sys.argv[1:]
    main(int(a[0]) if a else 2020, int(a[1]) if len(a) > 1 else 2026, a[2] if len(a) > 2 else "report/metodo/conoscenza/padri-ict.csv")
