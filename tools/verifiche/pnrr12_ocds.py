"""#43 Misura 1.2: aggiudicatari dei CIG collegati presi dall'OCDS bulk ANAC (archivio), dove il dataset aggiudicatari manca.

Ingresso: report/metodo/pnrr-contratti-v3.csv (CIG 1.2) e archivio/.../ocds/filesystem/bulk/<anno>/<mese>.json.
Uscita: lavoro/pnrr12/ocds-1.2.jsonl, una riga per CIG (= id del lotto OCDS) trovato: cig, file, suppliers degli award
con relatedLots = CIG (id, name), status degli award, tender (title, lotto). Idempotente: riscrive il file.
Uso (server): nice python tools/verifiche/pnrr12_ocds.py"""
import csv, glob, json, os
from pathlib import Path
import ijson

R = Path(__file__).resolve().parents[2]
B = R / "archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/ocds/filesystem/bulk"


def main():
    csv.field_size_limit(10 ** 8)
    cigs = {r["cig"] for r in csv.DictReader(open(R / "report/metodo/pnrr-contratti-v3.csv", encoding="utf-8")) if r["misura"] == "1.2"}
    os.makedirs(R / "lavoro/pnrr12", exist_ok=True)
    trovati = {}
    for f in sorted(glob.glob(str(B / "*/*.json"))):
        with open(f, "rb") as fh:
            for rel in ijson.items(fh, "releases.item", use_float=True):
                t = rel.get("tender") or {}
                lotti = {l.get("id") for l in t.get("lots", [])} | {x for a in rel.get("awards", []) for x in a.get("relatedLots", [])}
                hit = lotti & cigs
                if not hit: continue
                for c in hit:
                    x = trovati.setdefault(c, {"cig": c, "file": [], "suppliers": [], "status": [], "tender": None})
                    fr = os.path.relpath(f, R)
                    if fr not in x["file"]: x["file"].append(fr)
                    for a in rel.get("awards", []):
                        if c in a.get("relatedLots", []):
                            x["status"].append(a.get("status"))
                            x["suppliers"] += [{"id": s_.get("id"), "name": s_.get("name")} for s_ in a.get("suppliers", [])
                                               if {"id": s_.get("id"), "name": s_.get("name")} not in x["suppliers"]]
                    lot = next((l for l in t.get("lots", []) if l.get("id") == c), {})
                    x["tender"] = x["tender"] or {"title": t.get("title"), "lot": (lot.get("title") or lot.get("description") or "")[:500],
                                                  "description": (t.get("description") or "")[:500]}
        print(f, len(trovati), flush=True)
    with open(R / "lavoro/pnrr12/ocds-1.2.jsonl", "w", encoding="utf-8") as o:
        for x in trovati.values(): o.write(json.dumps(x, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
