"""Verifica «CIG ripetuti con strati diversi» (R53, #66, #58).

Causa (misurata qui): nei file annuali ANAC 2024 e 2025 un CIG ha una riga per ogni CPV (più qualche riga identica
ripetuta). imbuto-0.3.1 (che ha prodotto lavoro/imbuto/ict.csv il 3/11) le conta tutte; 0.3.2 tiene la PRIMA letta,
imbuto_doppioni.py (base del 55,3 mld S3-S6 dal 2024) toglie l'eccesso tenendo l'ULTIMA. In entrambi i casi la
classificazione dipende dal CPV della riga tenuta, cioè dall'ordine del file: un CIG con un CPV ICT e uno non ICT
può finire in S5 (CPV ICT), in S6 «cpv-non-ict-testo-ict» o perfino in S1 (fuori dall'imbuto).

Regola proposta (imbuto 0.3.4, DEDUP_CPV in tools/analisi/imbuto.py, applicata alla prossima rigenerazione):
una riga per CIG e per fonte; se il CIG ha almeno un CPV ICT si classifica con il più basso dei suoi CPV ICT,
altrimenti con la prima riga. Non dipende dall'ordine del file, e un CIG con un CPV ICT resta nel perimetro ICT.

Questa verifica non tocca ict.csv:
 (A) misura i CIG ripetuti in ict.csv, righe ed euro in eccesso, la causa (CPV diversi o righe identiche) e i totali
     per strato dal 2024 con quattro regole: tutte le righe (0.3.1), prima riga (0.3.2), ultima riga (base del 55,3),
     CPV ICT (0.3.4). La 0.3.4 si stima scegliendo fra le righe di ict.csv quella con cpv_ict=1 e CPV minimo.
 (B) con --mirror (SUL SERVER, nice, ~20 min): rilegge 2024 e 2025 dal mirror, conta i CIG con più righe e con CPV
     ICT e non ICT insieme, e stima quanti CIG oggi in S3-S6 la regola 0.3.2 (prima riga) porterebbe in S1
     (prima riga del file con CPV non ICT e testo senza RX_ICT).
Uscita: esiti/2026-11-09/imbuto/cig-ripetuti.json e cig-ripetuti.csv (un CIG ripetuto per riga, con lo strato 0.3.4).
Uso: nice .venv/bin/python tools/verifiche/imbuto_cig_ripetuti.py [--mirror]
"""
import csv, json, os, sys

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.normpath(os.path.join(QUI, "..", ".."))
OUT = os.path.join(RADICE, "esiti/2026-11-09/imbuto")
W = os.path.join(RADICE, "lavoro/imbuto/ripetuti")
ICT = os.path.join(RADICE, "lavoro/imbuto/ict.csv")
S36 = ("S3-convenzione-lotto", "S4-marchio", "S5-ict-non-cloud", "S6-residuo")
REGOLE = (("tutte-le-righe-0.3.1", None), ("prima-riga-0.3.2", "prima"), ("ultima-riga-base-55.3", "ultima"),
          ("cpv-ict-0.3.4", "regola034"))


def connetti():
    import duckdb
    os.makedirs(os.path.join(W, "tmp"), exist_ok=True)
    c = duckdb.connect()
    c.execute(f"SET memory_limit='6GB'; SET threads=2; SET temp_directory='{W}/tmp'")
    c.execute(f"""CREATE TABLE t AS SELECT row_number() OVER () rn, cig, anno, strato, coalesce(sottoclasse,'') sottoclasse,
        coalesce(gruppo,'') gruppo, coalesce(via,'') via, coalesce(cod_cpv,'') cod_cpv, cpv_ict::INT cpv_ict,
        importo::DOUBLE importo, testo FROM read_csv('{ICT}', header=true, all_varchar=true)""")
    return c


def parte_a(c):
    q = lambda s: c.execute(s).fetchall()
    c.execute("CREATE TABLE d AS SELECT * FROM t WHERE cig IN (SELECT cig FROM t GROUP BY 1 HAVING count(*)>1)")
    righe, distinti = q("SELECT count(*), count(DISTINCT cig) FROM t")[0]
    dr, dc = q("SELECT count(*), count(DISTINCT cig) FROM d")[0]
    causa = dict(q("""SELECT CASE WHEN ncpv>1 THEN 'cpv-diversi' ELSE 'righe-identiche' END, count(*) FROM
        (SELECT cig, count(DISTINCT cod_cpv) ncpv FROM d GROUP BY 1) GROUP BY 1"""))
    diversi = {k: q(f"SELECT count(*) FROM (SELECT cig FROM d GROUP BY 1 HAVING count(DISTINCT {k})>1)")[0][0]
               for k in ("anno", "importo", "testo", "cod_cpv", "via", "strato", "sottoclasse", "gruppo")}
    misti = dict(q("""SELECT s, count(*) FROM (SELECT cig, string_agg(DISTINCT strato, '+' ORDER BY strato) s FROM d
        GROUP BY 1 HAVING count(DISTINCT strato)>1) GROUP BY 1"""))
    c.execute("""CREATE TABLE scelte AS SELECT cig, min(rn) prima, max(rn) ultima,
        arg_min(rn, (1-cpv_ict)::VARCHAR || '|' || cod_cpv || '|' || lpad(rn::VARCHAR, 9, '0')) regola034 FROM t GROUP BY cig""")
    tot = {}
    for nome, col in REGOLE:
        sql = "SELECT strato, count(*), sum(importo) FROM t WHERE anno>='2024' " + \
              (f"AND rn IN (SELECT {col} FROM scelte) " if col else "") + "GROUP BY 1 ORDER BY 1"
        v = {s: {"cig": n, "euro": round(e or 0)} for s, n, e in q(sql)}
        v["S3-S6"] = {"cig": sum(x["cig"] for k, x in v.items() if k in S36), "euro": sum(x["euro"] for k, x in v.items() if k in S36)}
        tot[nome] = v
    base = tot["tutte-le-righe-0.3.1"]
    ecc = {s: {"righe": base[s]["cig"] - tot["cpv-ict-0.3.4"].get(s, {"cig": 0})["cig"],
               "euro": base[s]["euro"] - tot["cpv-ict-0.3.4"].get(s, {"euro": 0})["euro"]} for s in base}

    def spost(col):
        return [dict(zip(["da", "a", "cig", "euro"], x)) for x in q(f"""SELECT u.strato||'/'||u.sottoclasse, n.strato||'/'||n.sottoclasse,
            count(*), round(sum(n.importo)) FROM scelte s JOIN t u ON u.rn=s.{col} JOIN t n ON n.rn=s.regola034
            WHERE u.strato||u.sottoclasse <> n.strato||n.sottoclasse GROUP BY 1,2 ORDER BY 4 DESC""")]
    os.makedirs(OUT, exist_ok=True)
    c.execute(f"""COPY (SELECT d.cig, any_value(d.anno) anno, count(*) righe, count(DISTINCT d.cod_cpv) cpv_distinti,
        string_agg(DISTINCT d.strato||'/'||d.sottoclasse, ' + ') strati, max(d.importo) importo,
        (count(*)-1)*max(d.importo) euro_eccesso, any_value(n.strato) strato_034, any_value(n.sottoclasse) sottoclasse_034,
        any_value(n.gruppo) gruppo_034, any_value(n.cod_cpv) cpv_034
        FROM d JOIN scelte s USING (cig) JOIN t n ON n.rn=s.regola034 GROUP BY d.cig ORDER BY euro_eccesso DESC, d.cig)
        TO '{OUT}/cig-ripetuti.csv' (HEADER)""")
    return {"ict_csv": {"righe": righe, "cig_distinti": distinti, "righe_in_eccesso": righe - distinti},
            "cig_ripetuti": dc, "righe_dei_cig_ripetuti": dr,
            "righe_per_cig": {str(k): v for k, v in q("SELECT n, count(*) FROM (SELECT count(*) n FROM d GROUP BY cig) GROUP BY 1 ORDER BY 1")},
            "anni": dict(q("SELECT anno, count(DISTINCT cig) FROM d GROUP BY 1 ORDER BY 1")),
            "causa": causa, "cig_con_campo_diverso_fra_le_righe": diversi, "strati_misti": misti,
            "eccesso_dal_2024_per_strato": ecc, "totali_dal_2024_per_regola": tot,
            "spostamenti_ultima_riga_vs_0.3.4": spost("ultima"), "spostamenti_prima_riga_0.3.2_vs_0.3.4": spost("prima")}


def parte_b(c):
    sys.path.insert(0, os.path.join(RADICE, "tools/analisi")); os.chdir(RADICE)
    from attribuisci_provider import righe_cig
    from imbuto import RX_ICT
    from classifica import CPV_ICT
    delta = {r["cig"] for r in righe_cig("delta")}
    anni = {str(a) for a in range(2020, 2027)}
    p = os.path.join(W, "mirror.csv")
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["n", "cig", "fonte", "cpv", "cpv_ict"]); n = 0
        for fo in ("2024", "2025"):
            for r in righe_cig(fo):
                if r["cig"] in delta or (r.get("anno_pubblicazione") or "").strip() not in anni: continue
                n += 1; cpv = r["cod_cpv"] or ""; w.writerow([n, r["cig"], fo, cpv, int(bool(CPV_ICT.match(cpv)))])
            print("letto", fo, n, flush=True)
    del delta
    c.execute(f"CREATE TABLE m AS SELECT * FROM read_csv('{p}', header=true, types={{'cig':'VARCHAR','cpv':'VARCHAR'}})")
    c.execute("""CREATE TABLE mr AS SELECT cig, count(*) righe, count(DISTINCT fonte) fonti, max(cpv_ict) un_ict,
        min(cpv_ict) tutti_ict, arg_min(cpv_ict, n) prima_ict FROM m GROUP BY cig HAVING count(*)>1""")
    q = lambda s: c.execute(s).fetchall()
    tot = q("SELECT count(*), sum(righe), sum(CASE WHEN fonti>1 THEN 1 ELSE 0 END) FROM mr")[0]
    misti = q("SELECT count(*) FROM mr WHERE un_ict=1 AND tutti_ict=0")[0][0]
    rows = q("""SELECT DISTINCT t.cig, t.strato, t.importo, t.testo FROM mr JOIN t USING (cig)
        WHERE mr.un_ict=1 AND mr.tutti_ict=0 AND mr.prima_ict=0 AND t.cpv_ict=1 AND t.anno>='2024'""")
    persi = {}
    for cig, st, imp, testo in rows:
        if RX_ICT.search(testo or ""): continue
        v = persi.setdefault(st, [set(), 0.0])
        if cig not in v[0]: v[0].add(cig); v[1] += imp or 0
    os.remove(p)
    return {"mirror_2024_2025": {"cig_con_piu_righe": tot[0], "righe": tot[1], "cig_in_due_file_annuali": tot[2],
                                 "cig_con_cpv_ict_e_non_ict": misti},
            "stima_cig_che_0.3.2_porterebbe_in_S1": {s: {"cig": len(v[0]), "euro": round(v[1])} for s, v in sorted(persi.items())}}


def main():
    c = connetti(); x = parte_a(c)
    j = os.path.join(OUT, "cig-ripetuti.json")
    if "--mirror" in sys.argv: x["parte_b"] = parte_b(c)
    else:
        try: x["parte_b"] = json.load(open(j, encoding="utf-8")).get("parte_b")
        except (OSError, ValueError): x["parte_b"] = None
    json.dump(x, open(j, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print(json.dumps({k: x[k] for k in ("ict_csv", "cig_ripetuti", "righe_per_cig", "causa", "cig_con_campo_diverso_fra_le_righe",
                                        "strati_misti", "eccesso_dal_2024_per_strato")}, ensure_ascii=False, indent=1))
    for k, v in x["totali_dal_2024_per_regola"].items():
        print(k, "S3-S6 dal 2024:", v["S3-S6"]["cig"], "CIG", round(v["S3-S6"]["euro"] / 1e9, 3), "mld;",
              {s: round(e["euro"] / 1e9, 3) for s, e in v.items() if s in S36})
    print("ultima->0.3.4", x["spostamenti_ultima_riga_vs_0.3.4"])
    print("prima->0.3.4", x["spostamenti_prima_riga_0.3.2_vs_0.3.4"])
    print("parte B", x["parte_b"])


if __name__ == "__main__":
    main()
