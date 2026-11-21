"""Tabellone big tech (#83 voce A): Google / Microsoft / Amazon / Oracle / altri x cloud / licenze-software / incerto, per anno.

Ingressi (sola lettura, registrati in config/ingressi-lavoro.yaml):
  lavoro/imbuto/stati-finali.csv.gz   stato finale di ogni CIG (cloud-certo, ict-non-cloud, incerto-marchio, ...), euro netti
  lavoro/imbuto/ict.csv               marchio (provider) riconosciuto dalla lente prodotto
Colonne:
  cloud      stato cloud-certo (servizio erogato dal produttore o per suo conto)
  licenze    stato ict-non-cloud con marchio (licenze, software installato presso l'ente, supporto)
  incerto    incerto-marchio (es. «licenze Microsoft» senza dettaglio: il carrello sta nell'atto)
Gli importi sono euro netti (al netto dei tetti degli accordi quadro e degli errori d'importo).
Uscita: esiti/<giorno>/statistiche/tabellone-bigtech.{csv,json}
Uso: python tools/verifiche/tabellone_bigtech.py [giorno]
"""
import csv, collections, gzip, json, os, sys

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GIORNO = sys.argv[1] if len(sys.argv) > 1 else "2026-11-21"
SF = os.environ.get("IMBUTO_STATI_FINALI", os.path.join(R, "lavoro/imbuto/stati-finali.csv.gz"))
ICT = os.environ.get("IMBUTO_ICT", os.path.join(R, "lavoro/imbuto/ict.csv"))
OUT = os.path.join(R, "esiti", GIORNO, "statistiche")
GRUPPI = [("Google", ("google",)), ("Microsoft", ("microsoft",)), ("Amazon", ("amazon", "aws")), ("Oracle", ("oracle",))]
COL = {"cloud-certo": "cloud", "ict-non-cloud": "licenze", "incerto-marchio": "incerto"}


def gruppo(p):
    q = p.lower()
    for g, chiavi in GRUPPI:
        if any(k in q for k in chiavi):
            return g
    return "altri"


csv.field_size_limit(10**9)
prov = {}
with open(ICT, newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["provider"]:
            prov[r["cig"]] = r["provider"]

T = collections.defaultdict(lambda: [0, 0.0])
with gzip.open(SF, "rt", newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        c = COL.get(r["stato"])
        p = prov.get(r["cig"])
        if not c or not p:
            continue
        g = gruppo(p)
        for chiave in ((g, c, r["anno"]), (g, c, "tutti")):
            T[chiave][0] += 1
            T[chiave][1] += float(r["euro_netti"] or 0)

os.makedirs(OUT, exist_ok=True)
righe = [{"gruppo": g, "colonna": c, "anno": a, "cig": n, "euro_netti": round(e, 2)} for (g, c, a), (n, e) in sorted(T.items())]
with open(os.path.join(OUT, "tabellone-bigtech.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(righe[0]))
    w.writeheader(); w.writerows(righe)
riep = {"versione": "0.1", "strumento": "tools/verifiche/tabellone_bigtech.py", "giorno": GIORNO,
        "ingressi": {"stati_finali": os.path.relpath(SF, R), "ict": os.path.relpath(ICT, R)},
        "tutti_gli_anni": {g: {c: {"cig": T[(g, c, "tutti")][0], "milioni": round(T[(g, c, "tutti")][1] / 1e6, 1)}
                                for c in ("cloud", "licenze", "incerto")} for g in [x for x, _ in GRUPPI] + ["altri"]}}
json.dump(riep, open(os.path.join(OUT, "tabellone-bigtech.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps(riep["tutti_gli_anni"], ensure_ascii=False, indent=1))
