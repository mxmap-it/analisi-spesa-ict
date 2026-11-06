"""#43 Controvalidazione della catena PNRR (CUP -> CIG) con il campo FLAG_PNRR_PNC dei CIG ANAC.

Seconda via indipendente: il flag lo dichiara la stazione appaltante all'acquisizione del CIG, la catena v3 nasce
dalle candidature PA Digitale 2026 e dal dataset ANAC cup. Si conta, per i CIG di ciascuna catena (1.2 e 1.1 v3 da
report/metodo/pnrr-contratti-v3.csv; 1.1 dai decreti da esiti/2026-11-06/pnrr11/pnrr11-prodotto.csv in esiti/<oggi>/pnrr),
quanti hanno FLAG_PNRR_PNC valorizzato come PNRR, e quanto pesano in euro.
Ingresso ANAC: lavoro/cig_completo/cig_csv_*.csv (file mensili) + lavoro/cig_delta/*.csv (2026), letti con DuckDB su
disco (memory_limit 6GB, 2 thread). Gira sul server.

Uso (server): nice .venv/bin/python tools/verifiche/pnrr_flag.py -> esiti/<oggi>/pnrr/pnrr-flag.json"""
import csv, json, os, datetime, glob, collections
from pathlib import Path
import duckdb

R = Path(__file__).resolve().parents[2]


def main():
    csv.field_size_limit(10 ** 8)
    catene = collections.defaultdict(dict)
    for r in csv.DictReader(open(R / "report/metodo/pnrr-contratti-v3.csv", encoding="utf-8")):
        catene["v3-" + r["misura"]][r["cig"]] = (float(r["importo_lotto"] or 0), r["provider"])
    p11 = sorted(glob.glob(str(R / "esiti/*/pnrr/pnrr11-prodotto.csv")))[-1]
    for r in csv.DictReader(open(p11, encoding="utf-8")):
        catene["decreti-1.1"][r["cig"]] = (float(r["importo_cig"] or 0), r["provider"])
    tutti = sorted({c for d in catene.values() for c in d})
    os.makedirs(R / "lavoro/pnrr-flag", exist_ok=True)
    con = duckdb.connect(str(R / "lavoro/pnrr-flag/flag.duckdb"))
    con.execute("SET memory_limit='6GB'; SET threads=2; SET temp_directory='lavoro/pnrr-flag/tmp'")
    con.execute("CREATE OR REPLACE TABLE c (cig VARCHAR)")
    con.executemany("INSERT INTO c VALUES (?)", [(x,) for x in tutti])
    files = sorted(glob.glob(str(R / "lavoro/cig_completo/cig_csv_*.csv"))) + sorted(glob.glob(str(R / "lavoro/cig_delta/*.csv")))
    con.execute(f"""CREATE OR REPLACE TABLE f AS SELECT cig, string_agg(DISTINCT coalesce(flag_pnrr_pnc,''), '|') flag
        FROM read_csv({files!r}, delim=';', header=true, all_varchar=true, union_by_name=true, ignore_errors=true)
        WHERE cig IN (SELECT cig FROM c) GROUP BY cig""")
    flag = dict(con.execute("SELECT cig, flag FROM f").fetchall())
    valori = collections.Counter(v for v in flag.values())
    out = {"ingresso_anac": f"{len(files)} file cig mensili/delta", "valori_flag": valori.most_common(20), "catene": {}}
    for nome, d in sorted(catene.items()):
        n = collections.Counter(); e = collections.Counter()
        for cig, (imp, prov) in d.items():
            v = flag.get(cig)
            k = "assente_nei_file_cig" if v is None else ("pnrr" if any(x.strip().upper() in ("1", "S", "SI", "PNRR", "PNRR-PNC", "PNRR_PNC", "TRUE") or "PNRR" in x.upper() for x in v.split("|")) else "non_pnrr_o_vuoto")
            n[k] += 1; e[k] += imp
        out["catene"][nome] = {"cig": len(d), **{k: {"cig": n[k], "importo": round(e[k])} for k in n},
                               "quota_cig_flag_pnrr": round(n["pnrr"] / len(d), 3) if d else None}
    o = R / f"esiti/{datetime.date.today().isoformat()}/pnrr"; os.makedirs(o, exist_ok=True)
    json.dump(out, open(o / "pnrr-flag.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
