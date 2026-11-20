#!/usr/bin/env python3
"""Codici fiscali di stazione appaltante e aggiudicatari per i CIG ICT dell'imbuto (#82). Versione 0.2 (20/11/2026).

Serve a riconoscere le società ICT pubbliche nei CIG per codice fiscale (dati/inhouse/societa-ict-pa.csv) invece che
con espressioni sul nome. Legge, con DuckDB su disco (memory_limit 6 GB, 2 thread: un solo job pesante alla volta):
  lavoro/imbuto/ict.csv                          CIG ICT dell'imbuto;
  lavoro/cig_completo/*.csv                      CIG ANAC (cf_amministrazione_appaltante), annuali e delta;
  aggiudicatari ANAC (codice_fiscale per CIG): tutti gli zip CSV del mirror
  (archivio/mirror/dati.anticorruzione.it/.../aggiudicatari/filesystem/*_csv.zip, annuale e mensili; 0.2: il file in
  lavoro/aggiudicatari era fermo al 26/10 e non copriva i CIG recenti).
Uso: nice python3 tools/verifiche/inhouse_cf.py
Uscita: lavoro/inhouse/cig-cf.csv.gz (cig, cf_sa, cf_aggiudicatari separati da «|»), sha256 stampato.
"""
import csv
import glob
import hashlib
import io
import os
import zipfile

import duckdb

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(R, "lavoro/inhouse/cig-cf.csv.gz")


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmp = os.path.join(R, "lavoro/inhouse/duck")
    os.makedirs(tmp, exist_ok=True)
    con = duckdb.connect()
    con.execute(f"SET memory_limit='6GB'; SET threads=2; SET temp_directory='{tmp}'; SET preserve_insertion_order=false")
    con.execute(f"""CREATE TABLE ict AS SELECT DISTINCT upper(trim(cig)) cig
                    FROM read_csv('{R}/lavoro/imbuto/ict.csv', header=true, all_varchar=true)""")
    con.execute(f"""CREATE TABLE sa AS SELECT upper(trim(c.cig)) cig, max(trim(c.cf_amministrazione_appaltante)) cf_sa
                    FROM read_csv('{R}/lavoro/cig_completo/*.csv', delim=';', header=true, all_varchar=true,
                                  union_by_name=true, ignore_errors=true, quote='"') c
                    JOIN ict ON ict.cig = upper(trim(c.cig)) GROUP BY 1""")
    ict = {r[0] for r in con.execute("SELECT cig FROM ict").fetchall()}
    ag = {}
    zips = sorted(glob.glob(f"{R}/archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/aggiudicatari/filesystem/*_csv.zip"))
    for z in zips:
        zf = zipfile.ZipFile(z)
        m = next(i for i in zf.namelist() if i.endswith(".csv"))
        for r in csv.DictReader(io.TextIOWrapper(zf.open(m), encoding="utf-8-sig", errors="replace"), delimiter=";"):
            c = (r.get("cig") or "").strip().upper()
            if c in ict and (r.get("codice_fiscale") or "").strip():
                ag.setdefault(c, set()).add(r["codice_fiscale"].strip())
    print("zip aggiudicatari letti:", len(zips))
    tab = os.path.join(tmp, "ag.csv")
    with open(tab, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["cig", "cf_agg"])
        for c, v in ag.items():
            w.writerow([c, "|".join(sorted(v))])
    con.execute(f"CREATE TABLE ag AS SELECT * FROM read_csv('{tab}', header=true, all_varchar=true)")
    con.execute(f"""COPY (SELECT ict.cig, coalesce(sa.cf_sa, '') cf_sa, coalesce(ag.cf_agg, '') cf_aggiudicatari
                          FROM ict LEFT JOIN sa USING (cig) LEFT JOIN ag USING (cig) ORDER BY ict.cig)
                    TO '{OUT}' (HEADER, DELIMITER ',', COMPRESSION gzip)""")
    n = con.execute("SELECT count(*), count(*) FILTER (WHERE cf_sa<>''), count(*) FILTER (WHERE cf_agg IS NOT NULL) FROM ict LEFT JOIN sa USING (cig) LEFT JOIN ag USING (cig)").fetchone()
    print(f"CIG {n[0]}, con cf stazione appaltante {n[1]}, con aggiudicatari {n[2]}")
    print("sha256", hashlib.sha256(open(OUT, "rb").read()).hexdigest())


if __name__ == "__main__":
    main()
