"""Confronto della prova a secco imbuto 0.3.4 (#71, #66): legge le quattro varianti di imbuto_prova_034.py e scrive
esiti/<data>/imbuto-prova/{confronto.json, g1-nuovi.csv, via6-cambi.csv}. Non tocca lavoro/imbuto/ict.csv.

  - strati S0-S6 e gruppi G1-G4 (CIG, euro dichiarati) dal 2024 e dal 2020, per variante e per la base 0.3.1;
  - S3-S6 dal 2024 al netto dei tetti (stesso metodo del rendiconto: euro_netti di esiti/2026-11-06/imbuto/tetti-cig-v2.csv
    per i CIG >= 50 M€, una riga per CIG) contro 58,2 (0.3.1), 55,3 (base 0.11) e la stima 55,7 (0.12);
  - CIG ripetuti in ict.csv (devono essere 0 nella variante A);
  - effetti separati: R53 = A-B, perimetro = B-C, lente = C-D;
  - G1 nuovi per il perimetro: CIG S6/G1 in B che in C non sono nell imbuto ICT (attesi 29, connettività/ASI);
  - via 6: CIG di report/metodo/llm/imbuto-g1g3/lotti (G1, G3) il cui strato/gruppo in A non è più quello della selezione.
duckdb con memory_limit 4GB, threads 2, temp su disco in lavoro/. Uso (sul server): .venv/bin/python
tools/verifiche/imbuto_prova_034_confronto.py [data]   (default: oggi)
"""
import csv, glob, json, os, sys, time

RADICE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
PROVA = os.path.join(RADICE, "lavoro/imbuto-prova-0.3.4")
VAR = {"A": f"{PROVA}/A", "B": f"{PROVA}/B", "C": f"{PROVA}/C", "D": f"{PROVA}/D", "base-0.3.1": f"{RADICE}/lavoro/imbuto"}
TETTI = f"{RADICE}/esiti/2026-11-06/imbuto/tetti-cig-v2.csv"
S36 = ("S3-convenzione-lotto", "S4-marchio", "S5-ict-non-cloud", "S6-residuo")
mld = lambda x: round(x / 1e9, 3)


def strati(v):
    R = json.load(open(f"{VAR[v]}/riepilogo.json", encoding="utf-8"))
    T = {}
    for r in R["righe"]:
        for per in ("dal-2020", "dal-2024") if int(r["anno"]) >= 2024 else ("dal-2020",):
            k = f"{per}|{r['strato']}" + (f"|{r['gruppo']}" if r["gruppo"] else "")
            x = T.setdefault(k, [0, 0]); x[0] += r["cig"]; x[1] += r["euro"]
            if r["gruppo"]:
                x = T.setdefault(f"{per}|{r['strato']}", [0, 0]); x[0] += r["cig"]; x[1] += r["euro"]
    return R["versione"], T


def main():
    import duckdb
    data = sys.argv[1] if len(sys.argv) > 1 else time.strftime("%Y-%m-%d")
    out = os.path.join(RADICE, f"esiti/{data}/imbuto-prova"); os.makedirs(out, exist_ok=True)
    os.makedirs(f"{PROVA}/tmp", exist_ok=True)
    c = duckdb.connect()
    c.execute(f"SET memory_limit='4GB'; SET threads=2; SET temp_directory='{PROVA}/tmp'")
    c.execute(f"CREATE TABLE tetti AS SELECT cig, any_value(euro_netti::DOUBLE) netti FROM read_csv('{TETTI}', all_varchar=true) GROUP BY cig")
    J = {"versioni": {}, "strati": {}, "ripetuti": {}, "s3s6_dal_2024": {}, "riferimenti_rendiconto": {
        "s3s6_dal_2024_0.3.1_dopo_tetti": 58.26, "base_0.11_dopo_doppioni": 55.3, "stima_0.12": 55.7}}
    for v in VAR:
        if not os.path.exists(f"{VAR[v]}/riepilogo.json"): print("manca", v); continue
        J["versioni"][v], J["strati"][v] = strati(v)
        c.execute(f"""CREATE OR REPLACE TABLE {('t' + v).replace('-', '_').replace('.', '_')} AS SELECT anno::INT anno, cig, strato,
                      coalesce(sottoclasse,'') sottoclasse, coalesce(gruppo,'') gruppo, importo::DOUBLE importo, coalesce(cod_cpv,'') cpv,
                      coalesce(stazione_appaltante,'') sa, coalesce(testo,'') testo
                      FROM read_csv('{VAR[v]}/ict.csv', all_varchar=true, header=true)""")
        t = ("t" + v).replace("-", "_").replace(".", "_")
        n, e = c.execute(f"SELECT count(*), coalesce(sum(n-1),0) FROM (SELECT cig, count(*) n FROM {t} GROUP BY cig HAVING n>1)").fetchone()
        J["ripetuti"][v] = {"cig_ripetuti": n, "righe_in_eccesso": int(e)}
        # S3-S6 dal 2024: dichiarati (tutte le righe) e al netto dei tetti, una riga per CIG (la prima scritta)
        r = c.execute(f"""WITH u AS (SELECT * FROM {t} WHERE anno >= 2024 AND strato IN {S36} QUALIFY row_number() OVER (PARTITION BY cig) = 1)
                          SELECT strato, count(*), sum(importo), sum(coalesce(netti, importo)) FROM u LEFT JOIN tetti USING (cig)
                          GROUP BY ALL ORDER BY 1""").fetchall()
        d = c.execute(f"SELECT sum(importo) FROM {t} WHERE anno >= 2024 AND strato IN {S36}").fetchone()[0]
        J["s3s6_dal_2024"][v] = {"per_strato": {s: {"cig": k, "euro_mld": mld(x), "netti_mld": mld(y)} for s, k, x, y in r},
                                 "dichiarati_tutte_le_righe_mld": mld(d), "cig": sum(x[1] for x in r),
                                 "dichiarati_una_riga_mld": mld(sum(x[2] for x in r)), "netti_tetti_mld": mld(sum(x[3] for x in r))}
    # effetti separati (dal 2024, per strato e gruppo, dai riepiloghi)
    J["effetti"] = {}
    for nome, a, b in (("R53 (A-B)", "A", "B"), ("perimetro 0.3.3 (B-C)", "B", "C"), ("lente v4.3 (C-D)", "C", "D"),
                       ("totale (A-D)", "A", "D"), ("D contro base 0.3.1", "D", "base-0.3.1")):
        if a in J["strati"] and b in J["strati"]:
            ks = sorted(set(J["strati"][a]) | set(J["strati"][b]))
            J["effetti"][nome] = {k: {"cig": J["strati"][a].get(k, [0, 0])[0] - J["strati"][b].get(k, [0, 0])[0],
                                      "euro_mld": mld(J["strati"][a].get(k, [0, 0])[1] - J["strati"][b].get(k, [0, 0])[1])}
                                  for k in ks if J["strati"][a].get(k) != J["strati"][b].get(k)}
            sa, sb = J["s3s6_dal_2024"][a], J["s3s6_dal_2024"][b]
            J["effetti"][nome]["S3-S6 dal 2024 netti tetti"] = {"cig": sa["cig"] - sb["cig"], "euro_mld": round(sa["netti_tetti_mld"] - sb["netti_tetti_mld"], 3)}
    # G1 nuovi per il perimetro: in B S6/G1, in C fuori dall imbuto ICT (S1)
    if "B" in J["strati"] and "C" in J["strati"]:
        q = c.execute(f"""SELECT b.anno, b.cig, b.importo, b.cpv, b.sa, b.testo FROM tB b
                          WHERE b.strato = 'S6-residuo' AND b.gruppo = 'G1-mega' AND b.cig NOT IN (SELECT cig FROM tC WHERE strato IN {S36})
                          ORDER BY b.importo DESC""").fetchall()
        with open(f"{out}/g1-nuovi.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["anno", "cig", "importo", "cod_cpv", "stazione_appaltante", "testo"]); w.writerows(q)
        J["g1_nuovi_perimetro"] = {"cig": len(q), "euro_mld": mld(sum(x[2] for x in q)), "dal_2024": sum(1 for x in q if x[0] >= 2024)}
    # via 6: strato/gruppo in A dei CIG selezionati (G1, G3) dalla base 0.3.1
    sel = [json.loads(l) for p in sorted(glob.glob(f"{RADICE}/report/metodo/llm/imbuto-g1g3/lotti/*.jsonl")) for l in open(p, encoding="utf-8") if l.strip()]
    sel = {s["cig"]: s for s in sel if s["gruppo"] in ("G1", "G3")}
    if "A" in J["strati"]:
        c.execute("CREATE TABLE sel (cig VARCHAR, gsel VARCHAR)"); c.executemany("INSERT INTO sel VALUES (?, ?)", [(k, s["gruppo"]) for k, s in sel.items()])
        q = c.execute("""SELECT s.cig, s.gsel, a.strato, a.sottoclasse, a.gruppo, a.importo, a.testo FROM sel s LEFT JOIN
                         (SELECT * FROM tA QUALIFY row_number() OVER (PARTITION BY cig) = 1) a USING (cig)
                         WHERE a.cig IS NULL OR a.strato <> 'S6-residuo' OR NOT starts_with(a.gruppo, s.gsel || '-') ORDER BY a.importo DESC NULLS FIRST""").fetchall()
        with open(f"{out}/via6-cambi.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["cig", "gruppo_via6", "strato_A", "sottoclasse_A", "gruppo_A", "importo", "testo"])
            w.writerows([(a, b, cc or "S1/assente", d, e, x, (t or "")[:200]) for a, b, cc, d, e, x, t in q])
        cnt = {}
        for _, g, s, _, gg, x, _ in q:
            k = f"{g} -> {s or 'S1/assente'}{'/' + gg if gg else ''}"; z = cnt.setdefault(k, [0, 0.0]); z[0] += 1; z[1] += x or 0
        J["via6_cambi"] = {"selezionati": len(sel), "cambiano": len(q), "per_passaggio": {k: {"cig": z[0], "euro_mld": mld(z[1])} for k, z in sorted(cnt.items())}}
    json.dump(J, open(f"{out}/confronto.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: J[k] for k in ("ripetuti", "s3s6_dal_2024", "g1_nuovi_perimetro", "via6_cambi") if k in J}, ensure_ascii=False, indent=1))
    if J["ripetuti"].get("A", {}).get("cig_ripetuti"): print("ATTENZIONE: CIG ripetuti nella variante A"); sys.exit(1)


if __name__ == "__main__":
    main()
