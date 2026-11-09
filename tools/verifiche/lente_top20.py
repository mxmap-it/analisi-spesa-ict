"""#40/#41 Misura della lente prodotto sul campione casuale dei primi 20 rivenditori (60 CIG, seme 20261109).

Ingresso: esiti/2026-11-09/rivenditori/campione-top20-v4.1.csv (estrazione, congelata), etichette a mano
report/metodo/rivenditori-v4/etichette-top20.csv (prodotto_corretto si/no rispetto al provider della v4.1) e i testi
di lavoro/attribuzione/[0-9]*.csv. Riclassifica ogni CIG con le regole CORRENTI e conta:
  tenuti_giusti = etichetta si e stesso provider; persi = etichetta si e provider cambiato/assente (regressione);
  errori_restanti = etichetta no e stesso provider; errori_tolti = etichetta no e provider cambiato.
Uso: python tools/verifiche/lente_top20.py [etichetta] -> esiti/<oggi>/rivenditori/lente-top20-<etichetta>.json"""
import csv, glob, json, os, sys, datetime, collections
from pathlib import Path
R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/analisi"))
from classifica import Classificatore  # noqa: E402


def main():
    c = Classificatore(); nome = sys.argv[1] if len(sys.argv) > 1 else "corrente"
    camp = list(csv.DictReader(open(R / "esiti/2026-11-09/rivenditori/campione-top20-v4.1.csv", encoding="utf-8")))
    et = {r["cig"]: r["prodotto_corretto"] for r in csv.DictReader(open(R / "report/metodo/rivenditori-v4/etichette-top20.csv", encoding="utf-8"))}
    voluti = {r["cig"] for r in camp}; righe = {}
    for f in sorted(glob.glob(str(R / "lavoro/attribuzione/[0-9]*.csv"))):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            if r["cig"] in voluti: righe[r["cig"]] = r
    n = collections.Counter(); eur = collections.Counter(); det = []
    for x in camp:
        r = righe[x["cig"]]; ag = [a.strip() for a in r["aggiudicatari"].split(";") if a.strip()]
        k = c.classifica(r["testo"], r["cig_accordo_quadro"], ag, r["cod_cpv"]) or {"provider": "", "servizio": ""}
        stesso = k["provider"] == x["provider"] and k["servizio"] not in ("servizi-professionali", "in-house", "software-infrastruttura")
        e = et[x["cig"]]
        cls = {("si", True): "tenuti_giusti", ("si", False): "persi", ("no", True): "errori_restanti", ("no", False): "errori_tolti"}[(e, stesso)]
        n[cls] += 1; eur[cls] += float(x["eur"]); det.append({"cig": x["cig"], "v4.1": x["provider"], "ora": k["provider"], "servizio": k["servizio"], "etichetta": e, "esito": cls})
    tp, fp = n["tenuti_giusti"], n["errori_restanti"]
    out = {"regole": nome, "conteggi": dict(n), "euro": {k: round(v) for k, v in eur.items()},
           "precisione": round(tp / (tp + fp), 3) if tp + fp else None,
           "precisione_eur": round(eur["tenuti_giusti"] / (eur["tenuti_giusti"] + eur["errori_restanti"]), 3) if tp + fp else None,
           "richiamo_relativo": round(tp / (tp + n["persi"]), 3), "dettaglio_cambiati": [d for d in det if d["esito"] != "tenuti_giusti"]}
    o = R / f"esiti/{datetime.date.today().isoformat()}/rivenditori"; os.makedirs(o, exist_ok=True)
    json.dump(out, open(o / f"lente-top20-{nome}.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
