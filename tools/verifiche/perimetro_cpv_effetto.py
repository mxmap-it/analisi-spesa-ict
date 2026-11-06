"""#44 Decisione di Fabio del 7/11/2026: effetto delle modifiche al perimetro, calcolato A PARTE (senza rigenerare ict.csv).

A. Review di 79342 (marketing) e 3224 (telecamere/TV): campione stratificato per importo (tutti i CIG >= 1 M€ e 40 per
   strato 100 k-1 M, 10-100 k, < 10 k), report/cpv/review-79342-3224/{campione,etichette}.csv. Stima pesata degli ICT veri
   (N_h / n_h) con Wilson per strato; quanti ICT veri e dubbi il nuovo RX_ICT recupera dal testo.
B. RX_ICT 0.3.3 (aggiunti «sw» e «connettività»): CIG dal 2024 oggi in S1 (assenti da ict.csv, importo >= 500) che il
   nuovo RX_ICT porta nel residuo S6 «cpv-non-ict-testo-ict», per gruppo dell'imbuto; 40 esempi casuali da rileggere.
C. 79342 fuori da CPV_ICT: CIG dal 2024 di ict.csv con quel CPV e strato S3-S6 (passati per il classificatore) che
   restano (testo ICT) o scendono in S1.
Base: lavoro/imbuto/ict.csv (imbuto 0.3.2) e lavoro/cig_completo. duckdb 6 GB, 2 thread.
Uso (server): SPESAICT_BASE=~/analisi-spesa-ict nice python tools/verifiche/perimetro_cpv_effetto.py -> esiti/<oggi>/cpv/perimetro-effetto.json"""
import csv, json, os, re, sys, math, datetime, collections, hashlib
from pathlib import Path
import duckdb

R = Path(__file__).resolve().parents[2]
BASE = Path(os.environ.get("SPESAICT_BASE", R))
sys.path.insert(0, str(R / "tools/analisi"))
import imbuto  # noqa: E402

NUOVO = imbuto.RX_ICT
VECCHIO = re.compile(NUOVO.pattern.replace("|sw|connettivit\\w*)", ")"), re.I)
assert VECCHIO.pattern != NUOVO.pattern
SEME = 20261107


def wilson(k, n, z=1.96):
    if not n: return None
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(p, 4), round(c - h, 4), round(c + h, 4)]


def strato_imp(x):
    return "a>=1M" if x >= 1e6 else "b100k-1M" if x >= 1e5 else "c10k-100k" if x >= 1e4 else "d<10k"


def main():
    c = duckdb.connect(); c.execute("set memory_limit='6GB'; set threads=2; set preserve_insertion_order=false")
    os.makedirs(BASE / "lavoro/duck/tmp", exist_ok=True); c.execute(f"set temp_directory='{BASE}/lavoro/duck/tmp'")
    ict = f"read_csv('{BASE}/lavoro/imbuto/ict.csv', all_varchar=true)"
    out = {"generato": str(datetime.date.today()), "versione_imbuto": imbuto.VERSIONE_IMBUTO}
    # A. review
    D = R / "report/cpv/review-79342-3224"
    testi = {r["cig"]: r for r in csv.DictReader(open(D / "campione.csv", encoding="utf-8"))}
    et = list(csv.DictReader(open(D / "etichette.csv", encoding="utf-8")))
    dim = {}
    for p in ("79342", "3224"):
        for s, n, e in c.execute(f"""select st, count(*), sum(imp)/1e6 from (select cig, max(try_cast(importo as double)) imp,
                case when max(try_cast(importo as double))>=1e6 then 'a>=1M' when max(try_cast(importo as double))>=1e5 then 'b100k-1M'
                when max(try_cast(importo as double))>=1e4 then 'c10k-100k' else 'd<10k' end st
                from {ict} where anno>='2024' and replace(cod_cpv,'-','') like '{p}%' group by cig) group by 1""").fetchall():
            dim[(p, s)] = (n, round(e or 0, 1))
    rev = {}
    for p in ("79342", "3224"):
        per = collections.defaultdict(collections.Counter); stima = collections.Counter(); recup = collections.Counter()
        for e in et:
            if e["prefisso"] != p: continue
            per[e["strato"]][e["ict"]] += 1
            if e["ict"] in ("s", "dubbio"):
                recup[e["ict"] + ("_recuperato" if NUOVO.search(testi[e["cig"]]["testo"]) else "_perso")] += 1
        for s, cnt in per.items():
            n = sum(cnt.values()); N = dim[(p, s)][0]
            for k, v in cnt.items(): stima[k] += v * N / n
        rev[p] = {"strati": {s: {"universo": dim[(p, s)], "campione": dict(v), "ict_veri": wilson(v["s"], sum(v.values()))} for s, v in sorted(per.items())},
                  "stima_pesata_cig": {k: round(v) for k, v in stima.items()}, "universo_cig": sum(dim[(p, s)][0] for s in per),
                  "recupero_testo_nuovo_rx": dict(recup)}
    out["review"] = rev
    big = c.execute(f"""select cig, max(try_cast(importo as double)), any_value(stazione_appaltante), any_value(testo) from {ict}
        where anno>='2024' and replace(cod_cpv,'-','') like '3224%' group by cig order by 2 desc limit 1""").fetchone()
    out["review"]["3224"]["importo_massimo"] = {"cig": big[0], "importo": big[1], "ente": big[2], "testo": big[3][:150]}
    # B. nuovi ingressi da S1
    fs = sorted(str(p) for p in (BASE / "lavoro/cig_completo").glob("*cig_csv*.csv"))
    cur = c.execute(f"""select distinct on (cig) cig, try_cast(replace(importo_lotto,',','.') as double) imp,
        coalesce(oggetto_gara,'') || ' | ' || coalesce(oggetto_lotto,'') testo
        from read_csv({fs}, delim=';', header=true, all_varchar=true, ignore_errors=true, union_by_name=true)
        where anno_pubblicazione >= '2024' and try_cast(replace(importo_lotto,',','.') as double) >= {imbuto.SOGLIA_MIN}
          and cig not in (select cig from {ict})""")
    g = collections.Counter(); ge = collections.Counter(); per_termine = collections.Counter(); es = []
    n_s1 = 0
    while True:
        rows = cur.fetchmany(100000)
        if not rows: break
        for cig, imp, testo in rows:
            n_s1 += 1
            if NUOVO.search(testo) and not VECCHIO.search(testo):
                gr = imbuto.gruppo(imp, testo); g[gr] += 1; ge[gr] += imp
                m = NUOVO.search(testo).group(1).lower(); per_termine["sw" if m == "sw" else "connettivit*"] += 1
                es.append((cig, imp, testo))
    es.sort(key=lambda x: hashlib.sha256((x[0] + str(SEME)).encode()).hexdigest())
    out["nuovo_rx_da_s1"] = {"s1_dal_2024_in_base": n_s1, "cig_nuovi_nel_residuo": sum(g.values()), "importo_meur": round(sum(ge.values()) / 1e6, 1),
                             "per_gruppo": {k: [v, round(ge[k] / 1e6, 1)] for k, v in g.most_common()}, "per_termine": dict(per_termine),
                             "g1_elenco": [[a, round(b / 1e6, 1), t[:160]] for a, b, t in sorted(es, key=lambda x: -x[1]) if imbuto.gruppo(b, t).startswith("G1")]}
    with open(R / "report/cpv/review-79342-3224/nuovo-rx-esempi.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["cig", "importo", "testo"]); w.writerows([[a, b, t[:300]] for a, b, t in es[:40]])
    # C. 79342 fuori lista
    rr = c.execute(f"""select cig, any_value(strato), max(try_cast(importo as double)), any_value(testo) from {ict}
        where anno>='2024' and replace(cod_cpv,'-','') like '79342%' group by cig""").fetchall()
    cc = collections.Counter(); ce = collections.Counter()
    for cig, st, imp, testo in rr:
        k = (st, "resta (testo ICT)" if NUOVO.search(testo) else "va in S1"); cc[k] += 1; ce[k] += imp or 0
    out["togliere_79342"] = {" | ".join(k): [v, round(ce[k] / 1e6, 1)] for k, v in sorted(cc.items())}
    o = R / "esiti" / str(datetime.date.today()) / "cpv"; o.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(o / "perimetro-effetto.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(out, ensure_ascii=False, indent=0)[:6000])


if __name__ == "__main__":
    main()
