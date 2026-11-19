#!/usr/bin/env python3
"""BDAP (#25): lista delle risorse da specchiare, dai metadati CKAN archiviati (lavoro/bdap-pagine, bdap_metadati.sh).

Perimetro (sito/content/progetto/perimetro-fonti.md, «le entrate non entrano»; sito/content/progetto/bdap.md § Mirror):
- dentro: CSV (datastore/dump), PDF e XLS dei metadati, per i dataset di spesa, bilancio, CE/SP SSN, opere pubbliche, anagrafi;
- fuori, per regola sul titolo: entrate, disponibilità liquide, dipendenti pubblici, mutui e prestiti
  (non sono spesa, tanto meno spesa ICT);
- fuori per formato: le viste OData XML (/ODataProxy/...), stessi dati del CSV in XML, dimensione non dichiarata.
Gli URL http:// si riscrivono in https:// (la porta 80 non risponde, bdap.md).

    bdap_lista.py [--pagine DIR] [--out DIR]
Scrive OUT/bdap-dentro.txt (URL, i CSV piccoli prima), OUT/bdap-fuori.csv, OUT/bdap-risorse.csv e stampa i totali.
"""
import argparse, csv, glob, json, re, sys
from pathlib import Path

FUORI = [(r"entrat", "entrate"), (r"disponibilit", "disponibilità liquide"), (r"dipendenti pubblici", "dipendenti pubblici"),
         (r"\bmutui\b", "mutui"), (r"prestiti obbligazionari", "prestiti")]

def tipo(u):
    if "/datastore/dump/" in u: return "csv"
    if "ODataProxy" in u: return "odata-xml"
    if u.lower().endswith(".pdf"): return "pdf"
    if re.search(r"\.xlsx?$", u.lower()): return "xls"
    return "altro"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pagine", default="lavoro/bdap-pagine")
    ap.add_argument("--out", type=Path, default=Path("lavoro/mirror-completamento"))
    a = ap.parse_args()
    ds = {}
    for f in sorted(glob.glob(f"{a.pagine}/start-*.json")):
        for p in json.load(open(f, encoding="utf-8"))["result"]["results"]:
            ds[p["name"]] = p
    righe = {}
    for p in ds.values():
        motivo = next((m for rx, m in FUORI if re.search(rx, p["title"], re.I)), "")
        for r in p["resources"]:
            u = re.sub(r"^http://", "https://", r["url"])
            t = tipo(u)
            m = motivo or ("formato OData XML (stessi dati del CSV)" if t == "odata-xml" else "")
            try: z = int(r.get("size") or 0)
            except ValueError: z = 0
            # un PDF di metadati può servire più dataset: resta dentro se almeno uno è dentro
            if u in righe and not righe[u]["motivo"]: continue
            righe[u] = dict(url=u, dataset=p["name"], titolo=p["title"], tipo=t, dimensione=z, motivo=m)
    a.out.mkdir(parents=True, exist_ok=True)
    with open(a.out / "bdap-risorse.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(next(iter(righe.values()))))
        w.writeheader(); w.writerows(righe.values())
    dentro = sorted((r for r in righe.values() if not r["motivo"]), key=lambda r: r["dimensione"])
    (a.out / "bdap-dentro.txt").write_text("".join(r["url"] + "\n" for r in dentro), encoding="utf-8")
    with open(a.out / "bdap-fuori.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(dentro[0])); w.writeheader()
        w.writerows(r for r in righe.values() if r["motivo"])
    tot = {}
    for r in righe.values():
        k = r["motivo"] or "dentro"; n, s = tot.get(k, (0, 0)); tot[k] = (n + 1, s + r["dimensione"])
    print(f"dataset {len(ds)}, risorse {len(righe)}")
    for k, (n, s) in sorted(tot.items()): print(f"  {k}: {n} risorse, {s/1e9:.2f} GB dichiarati")

if __name__ == "__main__":
    sys.exit(main())
