#!/usr/bin/env python3
"""#57 Copertura e costo dell'acquisizione L3 sul residuo S6 non coperto dalla via 6, per priorità, famiglia ed esito.

Base: lavoro/residuo-s6/ingresso.csv e lavoro/residuo-s6/out/esiti.jsonl (tools/acquisizione/residuo_s6.sh).
Costo = richieste HTTP (pagine + documenti) e secondi di orologio per CIG (comprese le pause di 5 s per host); token: zero.
Uso (server): .venv/bin/python tools/verifiche/residuo_s6_copertura.py [DATA] -> esiti/<DATA>/acquisizione/residuo-s6.{json,csv}
"""
import collections, csv, datetime, json, sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]
D = R / "lavoro/residuo-s6"
csv.field_size_limit(10**9)
DOC = {"documenti"}
CIG_TROVATO = {"documenti", "cig-nella-pagina", "cig-in-sottopagina", "cig-nella-home", "cig-nell-elenco"}


def main():
    data = sys.argv[1] if len(sys.argv) > 1 else str(datetime.date.today())
    ing = {r["cig"]: r for r in csv.DictReader(open(D / "ingresso.csv", encoding="utf-8"))}
    es = {}
    for l in open(D / "out/esiti.jsonl", encoding="utf-8"):
        r = json.loads(l); es[r["cig"]] = r
    agg = collections.defaultdict(lambda: collections.Counter())
    for cig, r in es.items():
        p = ing.get(cig, {}).get("priorita", r.get("priorita", "?")); imp = float(ing.get(cig, {}).get("importo") or 0)
        cig_doc = sum(1 for d in r["documenti"] if d.get("cig_presente"))
        for k in ((p, r["famiglia"], r["esito"]), (p, "*", r["esito"]), ("*", r["famiglia"], r["esito"])):
            a = agg[k]; a["cig"] += 1; a["importo"] += imp; a["richieste"] += len(r["pagine"]) + len(r["documenti"])
            a["secondi"] += r.get("secondi", 0); a["documenti"] += len(r["documenti"]); a["documenti_con_cig"] += cig_doc
            a["cig_con_documento_che_cita"] += 1 if cig_doc else 0
    tot = collections.defaultdict(collections.Counter)
    for (p, f, e), a in agg.items():
        if f == "*":
            t = tot[p]; t["cig"] += a["cig"]; t["importo"] += a["importo"]
            if e in DOC: t["cig_con_documenti"] += a["cig"]; t["importo_con_documenti"] += a["importo"]
            if e in CIG_TROVATO: t["cig_trovato"] += a["cig"]
            t["cig_con_documento_che_cita"] += a["cig_con_documento_che_cita"]; t["richieste"] += a["richieste"]; t["secondi"] += a["secondi"]
    sintesi = {p: {**{k: round(v, 1) for k, v in t.items()}, "in_ingresso": sum(1 for x in ing.values() if x["priorita"] == p)}
               for p, t in sorted(tot.items()) if p != "*"}
    out = R / f"esiti/{data}/acquisizione"; out.mkdir(parents=True, exist_ok=True)
    json.dump({"generato": data, "ingresso": len(ing), "elaborati": len(es), "finito": (D / "out/FINITO.txt").exists(),
               "per_priorita": sintesi}, open(out / "residuo-s6.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(out / "residuo-s6.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["priorita", "famiglia", "esito", "cig", "importo", "richieste", "secondi", "documenti", "documenti_con_cig", "cig_con_documento_che_cita"])
        for (p, fa, e), a in sorted(agg.items()):
            w.writerow([p, fa, e, a["cig"], round(a["importo"], 2), a["richieste"], round(a["secondi"], 1), a["documenti"], a["documenti_con_cig"], a["cig_con_documento_che_cita"]])
    # registro dei blocchi di #57 (da validare nel monitoraggio PVL/AT prima di diventare evidenza): un host per riga
    bl = {}
    for r in es.values():
        if r["esito"] in ("blocco", "robots"):
            h = r["pagine"][0]["url"] if r["pagine"] else r["link"]
            k = h.split("/")[2] if "//" in h else h
            b = bl.setdefault(k, {"host": k, "tipo": r.get("blocco", "robots.txt"), "cig": 0, "esempio_url": h, "sha256": r["pagine"][0]["sha256"] if r["pagine"] else "", "data": r["data"]})
            b["cig"] += 1
    with open(out / "residuo-s6-blocchi.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, ["host", "tipo", "cig", "esempio_url", "sha256", "data"]); w.writeheader()
        w.writerows(sorted(bl.values(), key=lambda b: -b["cig"]))
    print(json.dumps(sintesi, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
