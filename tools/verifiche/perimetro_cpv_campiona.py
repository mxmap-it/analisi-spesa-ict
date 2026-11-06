"""#44 Campione casuale di S1 (escluso non ICT) dal 2024: CIG dei file annuali 2024-2025 con importo_lotto >= 500
assenti da lavoro/imbuto/ict.csv (che contiene tutto ciò che non è S1/S2 sotto soglia). Seme fisso.
Uso (server): python tools/verifiche/perimetro_cpv_campiona.py -> report/cpv/campione-s1/campione.csv (cig, testo) + disegno.json"""
import duckdb, json, os, csv
from pathlib import Path
R = Path(__file__).resolve().parents[2]
BASE = Path(os.environ.get("SPESAICT_BASE", R))
SEME, N = 20261109, 200
O = R / "report/cpv/campione-s1"; O.mkdir(parents=True, exist_ok=True)
os.makedirs(BASE / "lavoro/duck", exist_ok=True)
c = duckdb.connect(str(BASE / "lavoro/duck/perimetro_cpv.duckdb"))
c.execute("set memory_limit='6GB'; set threads=2; set preserve_insertion_order=false")
c.execute(f"set temp_directory='{BASE}/lavoro/duck/tmp'")
fs = sorted(str(p) for p in (BASE / "lavoro/cig_completo").glob("cig_csv_202[45]_*.csv"))
c.execute(f"""create or replace table s1 as
 select distinct on (cig) cig, oggetto_gara, oggetto_lotto, try_cast(replace(importo_lotto,',','.') as double) imp
 from read_csv({fs}, delim=';', header=true, all_varchar=true, ignore_errors=true)
 where try_cast(replace(importo_lotto,',','.') as double) >= 500
   and cig not in (select cig from read_csv('{BASE}/lavoro/imbuto/ict.csv', all_varchar=true))""")
n = c.execute("select count(*) from s1").fetchone()[0]
c.execute(f"select setseed({SEME/1e8})")
rows = c.execute(f"select cig, coalesce(oggetto_gara,'') || ' | ' || coalesce(oggetto_lotto,'') from s1 order by hash(cig || '{SEME}') limit {N}").fetchall()
with open(O / "campione.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["cig", "testo"]); w.writerows(rows)
json.dump({"universo": "cig_csv_2024_*/2025_* (importo_lotto>=500) meno lavoro/imbuto/ict.csv = S1 escluso non ICT", "file": [Path(x).name for x in fs],
           "seme": SEME, "n": N, "dimensione_universo": n, "ordine": "hash(cig||seme)"}, open(O / "disegno.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(n, len(rows))
