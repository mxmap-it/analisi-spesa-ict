"""Verifica «Imbuto: CIG contati due volte» (#66, R53, rendiconto 0.6).

imbuto.py (imbuto-0.3.1) salta nei file annuali solo i CIG presenti negli aggiornamenti mensili (delta): un CIG che
compare in due file annuali (es. cig-2024 e cig-2025), o due volte nello stesso file, è contato due volte, in numero
e in euro. Questa verifica ricostruisce le righe che imbuto.py conta (stesse fonti, stesso filtro sull'anno, stesso
salto dei CIG del delta), trova i CIG ripetuti e calcola le righe e gli euro in eccesso per periodo e strato; poi
corregge gli strati del riepilogo e controlla che i conti tornino (righe - eccesso = CIG distinti).

Non riscrive lavoro/imbuto/ict.csv (lo usa la via 6 in corso): la correzione è applicata ai totali.
Si tiene, per ogni CIG ripetuto, l'ultima riga letta (stesso ordine di imbuto.py); l'eccesso in euro è la somma degli
importi delle altre righe.

Uso:
  python tools/verifiche/imbuto_doppioni.py             # da un clone: legge esiti/2026-11-06/imbuto/doppioni.json
  python tools/verifiche/imbuto_doppioni.py --rigenera  # SUL SERVER (nice): stream del mirror + DuckDB su disco
"""
import csv, glob, json, os, sys

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.normpath(os.path.join(QUI, "..", ".."))
OUT = os.path.join(RADICE, "esiti/2026-11-06/imbuto/doppioni.json")
LISTA = os.path.join(RADICE, "esiti/2026-11-06/imbuto/doppioni-ict.csv")
RIEP = os.path.join(RADICE, "esiti/2026-11-03/imbuto/riepilogo-0.3.1.json")
W = os.path.join(RADICE, "lavoro/imbuto/dup")
periodo = lambda a: "2020-2023" if int(a) <= 2023 else "dal-2024"


def rigenera():
    os.chdir(RADICE); sys.path.insert(0, "tools/analisi")
    from attribuisci_provider import righe_cig, D
    import duckdb
    os.makedirs(W, exist_ok=True)
    anni = {str(a) for a in range(2020, 2027)}
    delta = set()
    with open(os.path.join(W, "righe.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["n", "cig", "fonte", "anno", "importo"]); n = 0
        for r in righe_cig("delta"):
            delta.add(r["cig"])
        fonti = sorted(a for a in anni if glob.glob(D + f"cig-{a}/filesystem/cig_csv_*.zip")) + ["delta"]
        for fo in fonti:
            for r in righe_cig(fo):
                if fo != "delta" and r["cig"] in delta: continue
                a = (r.get("anno_pubblicazione") or "").strip()
                if a not in anni: continue
                try: imp = float(r["importo_lotto"] or 0)
                except ValueError: imp = 0.0
                n += 1; w.writerow([n, r["cig"], fo, a, imp])
            print("letto", fo, n, flush=True)
    del delta
    con = duckdb.connect(os.path.join(W, "dup.duckdb"))
    con.execute(f"SET memory_limit='6GB'; SET threads=2; SET temp_directory='{W}/tmp'")
    con.execute(f"CREATE OR REPLACE TABLE r AS SELECT * FROM read_csv('{W}/righe.csv', header=true, types={{'cig':'VARCHAR','anno':'VARCHAR','importo':'DOUBLE','n':'BIGINT','fonte':'VARCHAR'}})")
    con.execute(f"""CREATE OR REPLACE TABLE s AS SELECT cig, strato, sottoclasse, gruppo FROM
        (SELECT *, row_number() OVER (PARTITION BY cig) k FROM read_csv('{RADICE}/lavoro/imbuto/ict.csv', header=true, all_varchar=true)) WHERE k=1""")
    # righe in eccesso: tutte tranne l'ultima letta per CIG
    con.execute("""CREATE OR REPLACE TABLE ecc AS SELECT r.*, row_number() OVER (PARTITION BY cig ORDER BY n DESC) k,
        count(*) OVER (PARTITION BY cig) c FROM r""")
    tot = con.execute("SELECT count(*), count(DISTINCT cig) FROM r").fetchone()
    q = """SELECT CASE WHEN CAST(e.anno AS INT)<=2023 THEN '2020-2023' ELSE 'dal-2024' END p,
             coalesce(s.strato, CASE WHEN e.importo < 500 THEN 'S2-sotto-soglia' ELSE 'S1-escluso-non-ict' END) st,
             coalesce(s.gruppo,'') g, count(*) righe, sum(e.importo) euro, sum(CASE WHEN e.importo>=50e6 THEN 1 ELSE 0 END) righe_oltre_50M
           FROM ecc e LEFT JOIN s USING (cig) WHERE e.k>1 GROUP BY ALL ORDER BY ALL"""
    ecc = [dict(zip(["periodo", "strato", "gruppo", "righe", "euro", "righe_oltre_50M"], x)) for x in con.execute(q).fetchall()]
    fonti_dup = [dict(zip(["fonti", "cig"], x)) for x in con.execute(
        "SELECT fonti, count(*) FROM (SELECT cig, string_agg(DISTINCT fonte, '+' ORDER BY fonte) fonti FROM ecc WHERE c>1 GROUP BY cig) GROUP BY ALL ORDER BY 2 DESC LIMIT 20").fetchall()]
    con.execute(f"""COPY (SELECT e.cig, e.anno, s.strato, s.gruppo, e.c volte, sum(e.importo) euro_eccesso FROM ecc e JOIN s USING (cig)
        WHERE e.k>1 GROUP BY ALL ORDER BY euro_eccesso DESC) TO '{LISTA}' (HEADER)""")
    json.dump({"righe_contate": tot[0], "cig_distinti": tot[1], "eccesso": ecc, "fonti_dei_doppioni": fonti_dup,
               "nota": "strato dei CIG fuori da ict.csv: S1 (o S2 se importo < 500 €)"}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
    con.close(); os.remove(os.path.join(W, "righe.csv")); os.remove(os.path.join(W, "dup.duckdb"))
    print("scritto", OUT)


def main():
    if "--rigenera" in sys.argv: return rigenera()
    X = json.load(open(OUT, encoding="utf-8")); P = json.load(open(RIEP, encoding="utf-8"))
    st = {}
    for r in P["righe"]:
        k = (periodo(r["anno"]), r["strato"]); v = st.setdefault(k, [0, 0.0]); v[0] += r["cig"]; v[1] += r["euro"] or 0
    ecc = {}
    for e in X["eccesso"]:
        k = (e["periodo"], e["strato"]); v = ecc.setdefault(k, [0, 0.0]); v[0] += e["righe"]; v[1] += e["euro"] or 0
    T = {"strati": [], "gruppi_eccesso": [e for e in X["eccesso"] if e["gruppo"]]}
    for k in sorted(st):
        e = ecc.get(k, [0, 0.0]); e1 = 0.0 if k[1] == "S0-padre-aq" else e[1]
        T["strati"].append({"periodo": k[0], "strato": k[1], "cig_prima": st[k][0], "cig_eccesso": e[0], "cig_dopo": st[k][0] - e[0],
                            "euro_prima": round(st[k][1]), "euro_eccesso": round(e1), "euro_dopo": round(st[k][1] - e1)})
    righe = sum(v[0] for v in st.values()); ecc_tot = sum(v[0] for v in ecc.values())
    T["coerenza"] = {"righe_riepilogo": righe, "righe_ricostruite": X["righe_contate"], "eccesso": ecc_tot,
                     "cig_distinti": X["cig_distinti"], "torna": righe == X["righe_contate"] and righe - ecc_tot == X["cig_distinti"]}
    T["fonti_dei_doppioni"] = X["fonti_dei_doppioni"]
    for s in T["strati"]: print(s)
    print("gruppi:", T["gruppi_eccesso"]); print("coerenza:", T["coerenza"]); print("fonti:", T["fonti_dei_doppioni"][:6])
    if "--json" in sys.argv: json.dump(T, open(sys.argv[sys.argv.index("--json") + 1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if not T["coerenza"]["torna"]: print("ATTENZIONE: i conti non tornano"); sys.exit(1)


if __name__ == "__main__":
    main()
