"""#27 TED come fonte di esiti: per i CIG collegati a un avviso TED di aggiudicazione (esiti/*/mirror/ted-cig.csv) che in ANAC
non hanno aggiudicatari (aggiudicatari_csv.zip del mirror), quanti vincitori, P.IVA e valori porta TED.
Ingressi: lavoro/ted-v2/pagine (tools/acquisizione/ted_mirror.py), esiti/*/mirror/ted-cig.csv (tools/verifiche/ted_cig.py).
Gira sul server.

Uso: nice .venv/bin/python tools/verifiche/ted_esiti.py -> esiti/<oggi>/mirror/ted-esiti.{json,csv}"""
import csv, glob, io, json, os, re, zipfile, datetime, collections
from pathlib import Path

R = Path(__file__).resolve().parents[2]


def nome(v):
    if isinstance(v, dict): v = next(iter(v.values()), [])
    return " ; ".join(v) if isinstance(v, list) else str(v or "")


def main():
    avv = {}
    for f in sorted(glob.glob(str(R / "lavoro/ted-v2/pagine/*.json"))):
        for n in json.load(open(f, encoding="utf-8")).get("notices", []): avv[n["publication-number"]] = n
    tc = sorted(glob.glob(str(R / "esiti/*/mirror/ted-cig.csv")))[-1]
    righe = [r for r in csv.DictReader(open(tc, encoding="utf-8")) if r["tipo"].startswith("can")]
    cigs = {r["cig"] for r in righe}
    agg = set()
    z = zipfile.ZipFile(R / "archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/aggiudicatari/filesystem/aggiudicatari_csv.zip")
    for r in csv.DictReader(io.TextIOWrapper(z.open("aggiudicatari_csv.csv"), encoding="utf-8", errors="replace"), delimiter=";"):
        if r["cig"] in cigs: agg.add(r["cig"])
    out_r = []; c = collections.Counter()
    for r in righe:
        if r["cig"] in agg: c["cig_con_aggiudicatari_anac"] += 1; continue
        n = avv.get(r["avviso_ted"], {})
        w = nome(n.get("winner-name")); piva = " ; ".join(n.get("winner-identifier") or [])
        val = n.get("total-value")
        c["cig_senza_aggiudicatari_anac"] += 1; c["di_cui_con_vincitore_ted"] += bool(w); c["di_cui_con_piva_ted"] += bool(piva); c["di_cui_con_valore_ted"] += val is not None
        out_r.append({"cig": r["cig"], "avviso_ted": r["avviso_ted"], "vincitore_ted": w, "piva_ted": piva, "valore_ted": val,
                      "valuta": n.get("total-value-cur", "")})
    tot = sum(float(x["valore_ted"][0] if isinstance(x["valore_ted"], list) else x["valore_ted"] or 0) for x in out_r if x["valore_ted"] is not None)
    out = {"ingresso": tc, "cig_in_esiti_ted": len(cigs), **c, "valore_ted_totale_dei_cig_senza_aggiudicatari": round(tot)}
    o = R / f"esiti/{datetime.date.today().isoformat()}/mirror"; os.makedirs(o, exist_ok=True)
    json.dump(out, open(o / "ted-esiti.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    with open(o / "ted-esiti.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_r[0]) if out_r else ["cig"]); w.writeheader(); w.writerows(out_r)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
