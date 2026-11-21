"""Copertura dei dati per trimestre (#83 voce A): CIG pubblicati per trimestre nel mirror ANAC e CIG ICT classificati.

Mostra fin dove arrivano i dati rispetto al trimestre corrente (gli ultimi trimestri sono incompleti: i CIG arrivano
con i delta mensili). Ingressi: lavoro/cig_completo/*.csv (dal mirror ANAC), lavoro/imbuto/stati-finali.csv.gz.
Uscita: esiti/<giorno>/statistiche/copertura-trimestri.{csv,json}
Uso: python tools/verifiche/copertura_trimestri.py [giorno]   (duckdb su disco, 6 GB, 2 thread)
"""
import json, os, sys
import duckdb
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
G = sys.argv[1] if len(sys.argv) > 1 else "2026-11-21"
OUT = os.path.join(R, "esiti", G, "statistiche"); os.makedirs(OUT, exist_ok=True)
c = duckdb.connect(os.path.join(R, "lavoro", "copertura.duckdb"))
c.sql("SET memory_limit='6GB'; SET threads=2; SET preserve_insertion_order=false")
c.sql(f"""CREATE OR REPLACE TABLE pub AS SELECT DISTINCT cig, try_cast(anno_pubblicazione AS INT) a, try_cast(mese_pubblicazione AS INT) m
  FROM read_csv('{R}/lavoro/cig_completo/*.csv', delim=';', header=true, all_varchar=true, union_by_name=true, ignore_errors=true)""")
c.sql(f"CREATE OR REPLACE TABLE sf AS SELECT cig, stato FROM read_csv('{R}/lavoro/imbuto/stati-finali.csv.gz', all_varchar=true)")
q = c.sql("""SELECT a AS anno, (m-1)//3+1 AS trimestre, count(DISTINCT p.cig) AS cig_pubblicati,
  count(DISTINCT sf.cig) FILTER (WHERE sf.stato NOT IN ('escluso-non-ict','fuori-misura')) AS cig_ict
  FROM pub p LEFT JOIN sf USING (cig) WHERE a BETWEEN 2020 AND 2026 AND m BETWEEN 1 AND 12 GROUP BY 1,2 ORDER BY 1,2""")
q.write_csv(os.path.join(OUT, "copertura-trimestri.csv"))
righe = [dict(zip(q.columns, r)) for r in q.fetchall()]
json.dump({"versione": "0.1", "strumento": "tools/verifiche/copertura_trimestri.py", "giorno": G, "trimestri": righe},
          open(os.path.join(OUT, "copertura-trimestri.json"), "w"), indent=1)
for r in righe: print(r)
c.close(); os.remove(os.path.join(R, "lavoro", "copertura.duckdb"))
