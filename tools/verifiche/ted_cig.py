"""#27 TED -> CIG: quanti avvisi TED italiani ICT (lavoro/ted-v2/pagine, tools/acquisizione/ted_mirror.py) si collegano a un CIG ANAC.
L'avviso TED non ha un campo CIG: le stazioni lo scrivono a volte negli identificativi interni o nei testi. Si estraggono i
candidati (10 caratteri: 7 cifre + 3 esadecimali, o A/B/Z + 9 esadecimali) e si tengono solo quelli che ESISTONO nei file CIG
ANAC (lavoro/cig_completo + lavoro/cig_delta, DuckDB su disco, 6 GB, 2 thread). Controprova: per gli avvisi di aggiudicazione
con P.IVA del vincitore, si confronta con gli aggiudicatari ANAC del CIG (aggiudicatari_csv.zip del mirror).

Uso (server): nice .venv/bin/python tools/verifiche/ted_cig.py -> esiti/<oggi>/mirror/ted-cig.{json,csv}"""
import csv, glob, io, json, os, re, zipfile, datetime, collections
from pathlib import Path
import duckdb

R = Path(__file__).resolve().parents[2]
RX = re.compile(r"(?<![0-9A-Z])(?:[0-9]{7}[0-9A-F]{3}|[ABZ][0-9A-F]{9})(?![0-9A-Z])")
CAMPI_TESTO = ["internal-identifier-lot", "internal-identifier-proc", "title-lot", "description-lot", "title-proc", "description-proc"]


def main():
    avvisi = {}
    for f in sorted(glob.glob(str(R / "lavoro/ted-v2/pagine/*.json"))):
        for n in json.load(open(f, encoding="utf-8")).get("notices", []):
            testo = json.dumps([n.get(k) for k in CAMPI_TESTO], ensure_ascii=False).upper()
            piva = {re.sub(r"\D", "", x)[-11:] for x in (n.get("winner-identifier") or []) if re.sub(r"\D", "", x)}
            avvisi[n["publication-number"]] = {"tipo": n.get("notice-type", ""), "cand": sorted(set(RX.findall(testo))), "piva": piva}
    cand = sorted({c for a in avvisi.values() for c in a["cand"]})
    os.makedirs(R / "lavoro/ted-cig/tmp", exist_ok=True)
    con = duckdb.connect(str(R / "lavoro/ted-cig/db.duckdb"))
    con.execute("SET memory_limit='6GB'; SET threads=2; SET temp_directory='lavoro/ted-cig/tmp'")
    con.execute("CREATE OR REPLACE TABLE c (cig VARCHAR)"); con.executemany("INSERT INTO c VALUES (?)", [(x,) for x in cand])
    files = sorted(glob.glob(str(R / "lavoro/cig_completo/cig_csv_*.csv"))) + sorted(glob.glob(str(R / "lavoro/cig_delta/*.csv")))
    esistono = {r[0] for r in con.execute(f"""SELECT DISTINCT cig FROM read_csv({files!r}, delim=';', header=true, all_varchar=true,
        union_by_name=true, ignore_errors=true) WHERE cig IN (SELECT cig FROM c)""").fetchall()}
    agg = collections.defaultdict(set)
    z = zipfile.ZipFile(R / "archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/aggiudicatari/filesystem/aggiudicatari_csv.zip")
    for r in csv.DictReader(io.TextIOWrapper(z.open("aggiudicatari_csv.csv"), encoding="utf-8", errors="replace"), delimiter=";"):
        if r["cig"] in esistono: agg[r["cig"]].add(re.sub(r"\D", "", r["codice_fiscale"]).zfill(11))
    tipi = collections.Counter(); coll = collections.Counter(); ctrl = collections.Counter(); righe = []
    for pn, a in avvisi.items():
        ok = [c for c in a["cand"] if c in esistono]
        tipi[a["tipo"]] += 1; coll[a["tipo"]] += bool(ok)
        if ok and a["piva"] and a["tipo"].startswith("can"):
            pa = set().union(*(agg[c] for c in ok))
            ctrl["con_piva_e_aggiudicatari_anac" if pa else "senza_aggiudicatari_anac"] += 1
            if pa: ctrl["piva_coincide"] += bool(a["piva"] & pa)
        for c in ok: righe.append({"avviso_ted": pn, "tipo": a["tipo"], "cig": c})
    out = {"avvisi": len(avvisi), "candidati": len(cand), "candidati_esistenti_in_anac": len(esistono),
           "avvisi_con_cig": sum(coll.values()), "quota": round(sum(coll.values()) / len(avvisi), 3),
           "per_tipo": {t: {"avvisi": n, "con_cig": coll[t]} for t, n in tipi.most_common()}, "controprova_piva": dict(ctrl)}
    o = R / f"esiti/{datetime.date.today().isoformat()}/mirror"; os.makedirs(o, exist_ok=True)
    json.dump(out, open(o / "ted-cig.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    with open(o / "ted-cig.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["avviso_ted", "tipo", "cig"]); w.writeheader(); w.writerows(righe)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
