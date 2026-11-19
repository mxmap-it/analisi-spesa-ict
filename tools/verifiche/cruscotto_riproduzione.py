#!/usr/bin/env python3
"""Verifica «Cruscotto: i totali riproducono l'imbuto» (#53, M13).

Il cruscotto (tools/cruscotto/pagina.html, servito da tools/annotazioni/server.py) calcola i totali e il drilldown
dall'indice lavoro/cruscotto/contratti.sqlite (tools/cruscotto/indice_contratti.py). Questa verifica ricalcola dall'indice
CIG ed euro per (anno, strato, sottoclasse, gruppo, giurisdizione, importo anomalo) con la stessa regola dell'imbuto
(i padri di accordo quadro S0 contano 0 €) e li confronta, riga per riga, con il riepilogo pubblicato dell'imbuto.
S1 (non ICT) e S2 non ICT non sono nell'indice: si escludono dal confronto e si dichiarano.
Controlla anche che ogni CIG con esiti di un livello sia nell'indice e che nessun aggiudicatario dell'indice abbia un
codice fiscale (i nomi delle persone fisiche sono oscurati).

Uso: python tools/verifiche/cruscotto_riproduzione.py [--riepilogo esiti/2026-11-18/imbuto/riepilogo-0.3.4.json] [--json OUT]
"""
import argparse, collections, hashlib, json, re, sqlite3, sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]
CHIAVI = ("anno", "strato", "sottoclasse", "gruppo", "giurisdizione", "importo_da_verificare")


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--riepilogo", default="esiti/2026-11-18/imbuto/riepilogo-0.3.4.json")
    a.add_argument("--indice", default="lavoro/cruscotto/contratti.sqlite")
    a.add_argument("--json")
    x = a.parse_args()
    rp = R / x.riepilogo
    rif = {}
    fuori = collections.Counter()
    for r in json.loads(rp.read_text(encoding="utf-8"))["righe"]:
        if r["strato"].startswith("S1") or (r["strato"].startswith("S2") and r["sottoclasse"] == "non-ict"):
            fuori["cig"] += r["cig"]; fuori["euro"] += r["euro"]; continue
        rif[tuple(str(r[k]) for k in CHIAVI)] = (r["cig"], r["euro"])
    c = sqlite3.connect(f"file:{R / x.indice}?mode=ro", uri=True)
    ind = {tuple(str(v) for v in k): (n, round(e or 0)) for *k, n, e in c.execute(
        "SELECT anno, strato, sottoclasse, gruppo, giurisdizione, importo_da_verificare, count(*),"
        " sum(CASE WHEN strato LIKE 'S0%' THEN 0 ELSE importo END) FROM contratti GROUP BY 1,2,3,4,5,6")}
    diverse = [{"chiave": dict(zip(CHIAVI, k)), "riepilogo": rif.get(k), "indice": ind.get(k)}
               for k in sorted(set(rif) | set(ind)) if rif.get(k) != ind.get(k)
               and not (rif.get(k) and ind.get(k) and rif[k][0] == ind[k][0] and abs(rif[k][1] - ind[k][1]) <= 1)]
    orfani = c.execute("SELECT count(*) FROM esiti WHERE cig NOT IN (SELECT cig FROM contratti)").fetchone()[0]
    rx_cf = re.compile(r"\b[A-Z]{6}[0-9LMNPQRSTUV]{2}[A-Z][0-9LMNPQRSTUV]{2}[A-Z][0-9LMNPQRSTUV]{3}[A-Z]\b")
    # un codice fiscale ha almeno due cifre (le lettere dell'omocodia sono rare): così «PROVESUSTRUTTURE» non conta
    cf_in_aggiudicatari = sum(any(sum(ch.isdigit() for ch in m) >= 2 for m in rx_cf.findall(a or "")) for (a,) in c.execute("SELECT aggiudicatari FROM contratti"))
    meta = json.loads(c.execute("SELECT valore FROM meta WHERE chiave='riepilogo'").fetchone()[0])
    T = {"verifica": "cruscotto-riproduzione 0.1", "riepilogo": x.riepilogo,
         "riepilogo_sha256": hashlib.sha256(rp.read_bytes()).hexdigest(), "indice_data": meta["data"], "imbuto": meta["imbuto"],
         "righe_confrontate": len(set(rif) | set(ind)), "righe_uguali": len(set(rif) | set(ind)) - len(diverse), "righe_diverse": len(diverse),
         "diverse": diverse[:50], "fuori_dal_confronto_S1_S2_non_ict": dict(fuori),
         "totale_indice": {"cig": sum(v[0] for v in ind.values()), "euro": sum(v[1] for v in ind.values())},
         "totale_riepilogo": {"cig": sum(v[0] for v in rif.values()), "euro": sum(v[1] for v in rif.values())},
         "esiti_senza_contratto": orfani, "aggiudicatari_con_codice_fiscale": cf_in_aggiudicatari,
         "cig_con_persona_fisica_oscurata": meta["cig_con_persona_fisica_oscurata"],
         "esito": "riprodotto" if not diverse and not orfani and not cf_in_aggiudicatari else "DIFFERENZE"}
    print(json.dumps({k: v for k, v in T.items() if k != "diverse"}, ensure_ascii=False, indent=1))
    if diverse: print("prime differenze:", json.dumps(diverse[:5], ensure_ascii=False), file=sys.stderr)
    if x.json:
        p = R / x.json; p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(T, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0 if T["esito"] == "riprodotto" else 1


if __name__ == "__main__":
    sys.exit(main())
