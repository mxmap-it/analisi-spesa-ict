"""Verifica «Imbuto: dove siamo» (#55, consegna 12/11/2026): dimensione di ogni strato dell'imbuto in numero
di CIG ed euro, per periodo (2020-2023 / dal 2024) e per i due assi (A: è cloud? B: giurisdizione), più la
distribuzione degli importi per proporre la soglia.

Ingressi versionati (riproducibile da un clone pulito, nessun dato grezzo):
  esiti/2026-11-03/imbuto/riepilogo-0.3.1.json   (tools/analisi/imbuto.py, imbuto-0.3.1, regole v3.1)
  esiti/2026-11-06/imbuto/distribuzione.json     (prodotto da questo script con --rigenera, sul server)

Uso:
  python tools/verifiche/imbuto_strati.py              # stampa le tabelle e controlla la coerenza
  python tools/verifiche/imbuto_strati.py --json OUT   # scrive anche le tabelle in JSON (per il rendiconto)
  python tools/verifiche/imbuto_strati.py --rigenera   # SUL SERVER: rilegge lavoro/imbuto/ict.csv con DuckDB su disco
                                                       # (memory_limit 6GB, 2 thread) e riscrive distribuzione.json
Per rigenerare anche ict.csv e il riepilogo dal mirror ANAC: python tools/analisi/imbuto.py 2020 (sul server).
"""
import json, os, sys, collections, hashlib

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.normpath(os.path.join(QUI, "..", ".."))
RIEP = os.path.join(RADICE, "esiti/2026-11-03/imbuto/riepilogo-0.3.1.json")
DISTR = os.path.join(RADICE, "esiti/2026-11-06/imbuto/distribuzione.json")
ICT = os.path.join(RADICE, "lavoro/imbuto/ict.csv")
CLASSI = [0, 500, 1000, 5000, 40000, 140000, 1e6, 5e6, 50e6, float("inf")]


def periodo(anno):
    return "2020-2023" if int(anno) <= 2023 else "dal-2024"


# Asse A (è cloud o infrastruttura?) per strato/sottoclasse. Regole del rendiconto, non nuove classificazioni.
def asse_a(strato, sotto):
    if strato == "S0-padre-aq": return "fuori-misura (padre AQ, contato negli attuativi)"
    if strato == "S1-escluso-non-ict": return "escluso certo (non ICT)"
    if strato == "S2-sotto-soglia": return "sotto soglia (contato, fuori misura)"
    if strato in ("S3-convenzione-lotto", "S4-marchio") and sotto == "cloud": return "incluso certo (cloud)"
    if strato == "S4-marchio" and sotto == "in-house": return "incluso certo (infrastruttura in-house)"
    if strato == "S5-ict-non-cloud": return "ICT non cloud (S5, voce infrastrutture interne da ripartire)"
    if strato == "S6-residuo": return "incerto (residuo S6)"
    return "incerto (marchio/lotto noto, cloud da accertare: licenze, software, servizi, PSN)"


def rigenera():
    import duckdb
    os.makedirs(os.path.join(RADICE, "lavoro/imbuto/duck"), exist_ok=True)
    con = duckdb.connect(os.path.join(RADICE, "lavoro/imbuto/duck/distr.duckdb"))
    con.execute("SET memory_limit='6GB'; SET threads=2; SET temp_directory='%s'" % os.path.join(RADICE, "lavoro/imbuto/duck/tmp"))
    casi = " ".join(f"WHEN importo < {CLASSI[i+1]} THEN '{i:02d}'" for i in range(len(CLASSI) - 2)) + f" ELSE '{len(CLASSI)-2:02d}'"
    q = f"""SELECT CASE WHEN CAST(anno AS INT) <= 2023 THEN '2020-2023' ELSE 'dal-2024' END AS periodo, strato,
        CASE {casi} END AS classe, count(*) n, sum(importo) euro, sum(importo_da_verificare) n_da_verificare
        FROM read_csv('{ICT}', header=true, all_varchar=false, types={{'importo':'DOUBLE','cig':'VARCHAR'}})
        GROUP BY ALL ORDER BY ALL"""
    righe = [dict(zip(["periodo", "strato", "classe", "n", "euro", "n_da_verificare"], r)) for r in con.execute(q).fetchall()]
    # presenza del link ai documenti (API PVL, #57) per strato, solo dal 2024: riuso di lavoro/pvl/cig_link.csv (4/11)
    link = os.path.join(RADICE, "lavoro/pvl/cig_link.csv")
    q2 = f"""WITH l AS (SELECT DISTINCT cig FROM read_csv('{link}', header=true, all_varchar=true) WHERE coalesce(link,'') <> ''),
        i AS (SELECT cig, strato, gruppo, importo FROM read_csv('{ICT}', header=true, types={{'importo':'DOUBLE','cig':'VARCHAR'}})
              WHERE CAST(anno AS INT) >= 2024 AND strato NOT IN ('S0-padre-aq','S2-sotto-soglia'))
        SELECT strato, gruppo, count(*) n, count(l.cig) n_link, sum(importo) euro, sum(CASE WHEN l.cig IS NOT NULL THEN importo END) euro_link
        FROM i LEFT JOIN l USING (cig) GROUP BY ALL ORDER BY ALL"""
    link_strati = [dict(zip(["strato", "gruppo", "n", "n_link", "euro", "euro_link"], r)) for r in con.execute(q2).fetchall()]
    h = hashlib.sha256(open(ICT, "rb").read()).hexdigest()
    out = {"fonte": "lavoro/imbuto/ict.csv", "sha256": h, "versione_imbuto": "imbuto-0.3.1",
           "classi_euro": [c if c != float("inf") else None for c in CLASSI], "righe": righe,
           "link_pvl_per_strato_dal_2024": link_strati, "fonte_link": "lavoro/pvl/cig_link.csv (API PVL, scaricamento del 4/11/2026)",
           "nota": "solo i CIG non esclusi in S1/S2 (ict.csv); S1 è nel riepilogo, senza distribuzione"}
    os.makedirs(os.path.dirname(DISTR), exist_ok=True)
    json.dump(out, open(DISTR, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
    print("scritto", DISTR, len(righe), "righe")


def main():
    if "--rigenera" in sys.argv:
        return rigenera()
    R = json.load(open(RIEP, encoding="utf-8"))
    D = json.load(open(DISTR, encoding="utf-8"))
    T = {}
    agg = lambda: collections.defaultdict(lambda: [0, 0.0])
    strati, assea, asseb, gruppi, dav, tot = agg(), agg(), agg(), agg(), agg(), agg()
    for r in R["righe"]:
        p = periodo(r["anno"]); k = r["cig"]; e = r["euro"] or 0
        tot[p][0] += k; tot[p][1] += e
        strati[(p, r["strato"], r["sottoclasse"])][0] += k; strati[(p, r["strato"], r["sottoclasse"])][1] += e
        a = asse_a(r["strato"], r["sottoclasse"])
        assea[(p, a)][0] += k; assea[(p, a)][1] += e
        if a.startswith("incluso certo"):
            g = r["giurisdizione"] or "non determinata"
            asseb[(p, g)][0] += k; asseb[(p, g)][1] += e
        if r["gruppo"]:
            gruppi[(p, r["gruppo"], r["sottoclasse"])][0] += k; gruppi[(p, r["gruppo"], r["sottoclasse"])][1] += e
        if r["importo_da_verificare"]:
            dav[(p, r["strato"])][0] += k; dav[(p, r["strato"])][1] += e
    conv = lambda d: [{"chiave": list(k) if isinstance(k, tuple) else k, "cig": v[0], "euro": round(v[1])} for k, v in sorted(d.items())]
    T = {"versione_imbuto": R["versione"], "totale": conv(tot), "strati": conv(strati), "asse_a": conv(assea),
         "asse_b_inclusi_certi": conv(asseb), "gruppi_residuo": conv(gruppi), "importo_da_verificare": conv(dav)}
    # distribuzione degli importi (CIG non esclusi in S1/S2) e quota cumulata sotto ogni soglia
    dist = agg()
    for r in D["righe"]:
        if r["strato"] in ("S0-padre-aq", "S2-sotto-soglia"): continue
        dist[(r["periodo"], r["classe"])][0] += r["n"]; dist[(r["periodo"], r["classe"])][1] += r["euro"] or 0
    cum = []
    for p in ("2020-2023", "dal-2024"):
        nt = sum(v[0] for (pp, _), v in dist.items() if pp == p); et = sum(v[1] for (pp, _), v in dist.items() if pp == p)
        cn = ce = 0
        for i in range(len(D["classi_euro"]) - 1):
            v = dist.get((p, f"{i:02d}"), [0, 0]); cn += v[0]; ce += v[1]
            hi = D["classi_euro"][i + 1]
            cum.append({"periodo": p, "fino_a_euro": hi, "cig_classe": v[0], "euro_classe": round(v[1]),
                        "quota_cig_cumulata": round(cn / nt, 4) if nt else None, "quota_euro_cumulata": round(ce / et, 6) if et else None})
    T["distribuzione_importi"] = cum
    T["link_pvl_per_strato_dal_2024"] = [dict(r, pct_link=round(100 * r["n_link"] / r["n"], 1), pct_euro_link=round(100 * (r["euro_link"] or 0) / r["euro"], 1) if r["euro"] else None)
                                         for r in D.get("link_pvl_per_strato_dal_2024", [])]
    # coerenza: i CIG di ict.csv (strati S0,S3-S6 e S2-ict) devono coincidere con il riepilogo
    for p in ("2020-2023", "dal-2024"):
        n_r = sum(v[0] for (pp, s, so), v in strati.items() if pp == p and s not in ("S1-escluso-non-ict",) and not (s == "S2-sotto-soglia" and so == "non-ict"))
        n_d = sum(r["n"] for r in D["righe"] if r["periodo"] == p)
        T.setdefault("coerenza", []).append({"periodo": p, "cig_riepilogo_non_S1": n_r, "cig_ict_csv": n_d, "uguali": n_r == n_d})
    fmt = lambda x: f"{x:,.0f}".replace(",", ".")
    for sez in ("totale", "asse_a", "asse_b_inclusi_certi", "gruppi_residuo", "importo_da_verificare"):
        print("\n##", sez)
        for r in T[sez]: print(" | ".join(map(str, r["chiave"] if isinstance(r["chiave"], list) else [r["chiave"]])), "|", fmt(r["cig"]), "CIG |", fmt(r["euro"]), "€")
    print("\n## distribuzione_importi (CIG S3-S6)")
    for r in cum: print(r)
    print("\n## link PVL per strato (dal 2024)")
    for r in T["link_pvl_per_strato_dal_2024"]: print(r["strato"], r["gruppo"], r["n"], r["pct_link"], "% CIG,", r["pct_euro_link"], "% euro")
    print("\n## coerenza", T["coerenza"])
    if "--json" in sys.argv:
        json.dump(T, open(sys.argv[sys.argv.index("--json") + 1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if not all(c["uguali"] for c in T["coerenza"]):
        print("ATTENZIONE: riepilogo e distribuzione non coincidono"); sys.exit(1)


if __name__ == "__main__":
    main()
