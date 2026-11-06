#!/usr/bin/env python3
"""Ingresso dell'acquisizione L2-L4 per il residuo S6 che la via 6 non copre (#57, decisione di Fabio del 7/11/2026).

Priorità (colonna `priorita`, in quest'ordine; dentro ogni priorità per importo decrescente):
  P1-incerti-ict   gli 80 CIG ICT con importo incerto (esiti/2026-11-06/imbuto/tetti-cig-v2.csv, classe=incerto, S3-S6)
  P2-g3            G3 del residuo S6 oltre i lotti della via 6 (report/metodo/llm/imbuto-g1g3/lotti/*.jsonl)
  P3-g2            G2 (informazione mancante, comprese le adesioni PSN)
  P4-nuovi-rx      CIG dal 2024 che RX_ICT 0.3.3 («sw», «connettività») porta da S1 nel residuo (come perimetro_cpv_effetto.py B)
  P5-g4-campione   G4 a campione: 1.000 CIG estratti con sha256(cig+SEME)
Il link viene dalla PVL (lavoro/pvl/link_cig.csv, campo documenti_di_gara_link; più link per CIG: il più specifico,
cioè quello con il percorso più lungo) e, se c'è, dall'avviso TED (link_eform_ted, L2).
Uso (server): SPESAICT_BASE=~/analisi-spesa-ict nice .venv/bin/python tools/acquisizione/residuo_s6_ingresso.py lavoro/residuo-s6/ingresso.csv
"""
import csv, collections, glob, hashlib, json, os, sys
from pathlib import Path
from urllib.parse import urlsplit

R = Path(__file__).resolve().parents[2]
BASE = Path(os.environ.get("SPESAICT_BASE", R))
sys.path.insert(0, str(R / "tools/analisi"))
csv.field_size_limit(10**9)
SEME = 20261107
N_G4 = 1000


def num(x):
    try: return float(x or 0)
    except ValueError: return 0.0


def specificita(u):
    p = urlsplit(u if "://" in u else "http://" + u)
    return len(p.path.strip("/")) + len(p.query)


def main():
    out = Path(sys.argv[1]); out.parent.mkdir(parents=True, exist_ok=True)
    via6 = set()
    for f in glob.glob(str(R / "report/metodo/llm/imbuto-g1g3/lotti/*.jsonl")):
        via6 |= {json.loads(l)["cig"] for l in open(f, encoding="utf-8") if l.strip()}
    s6 = {}
    for r in csv.DictReader(open(BASE / "lavoro/imbuto/ict.csv", encoding="utf-8")):
        if r["strato"].startswith("S6") and r["cig"] not in via6:
            v = s6.get(r["cig"])
            if not v or num(r["importo"]) > v[1]:
                s6[r["cig"]] = (r["gruppo"], num(r["importo"]), r["anno"], r["stazione_appaltante"], r["testo"][:200])
    sel = {}
    for r in csv.DictReader(open(R / "esiti/2026-11-06/imbuto/tetti-cig-v2.csv", encoding="utf-8")):
        if r["classe"] == "incerto" and r["strato"][:2] in ("S3", "S4", "S5", "S6") and r["cig"] not in via6:
            sel[r["cig"]] = ("P1-incerti-ict", num(r["importo"]), r["anno"], r["stazione_appaltante"], r["oggetto"][:200])
    for cig, (g, imp, a, sa, t) in s6.items():
        if cig in sel: continue
        if g.startswith("G3"): sel[cig] = ("P2-g3", imp, a, sa, t)
        elif g.startswith("G2"): sel[cig] = ("P3-g2", imp, a, sa, t)
    # P4: nuovi ingressi RX_ICT 0.3.3 da S1 (stessa interrogazione di tools/verifiche/perimetro_cpv_effetto.py, parte B)
    import duckdb, imbuto
    import re
    vecchio = re.compile(imbuto.RX_ICT.pattern.replace("|sw|connettivit\\w*)", ")"), re.I)
    c = duckdb.connect(); c.execute("set memory_limit='6GB'; set threads=2; set preserve_insertion_order=false")
    os.makedirs(BASE / "lavoro/duck/tmp", exist_ok=True); c.execute(f"set temp_directory='{BASE}/lavoro/duck/tmp'")
    fs = sorted(str(p) for p in (BASE / "lavoro/cig_completo").glob("*cig_csv*.csv"))
    ict = f"read_csv('{BASE}/lavoro/imbuto/ict.csv', all_varchar=true)"
    cur = c.execute(f"""select distinct on (cig) cig, try_cast(replace(importo_lotto,',','.') as double) imp, anno_pubblicazione,
        coalesce(denominazione_amministrazione_appaltante,''), coalesce(oggetto_gara,'') || ' | ' || coalesce(oggetto_lotto,'') testo
        from read_csv({fs}, delim=';', header=true, all_varchar=true, ignore_errors=true, union_by_name=true)
        where anno_pubblicazione >= '2024' and try_cast(replace(importo_lotto,',','.') as double) >= {imbuto.SOGLIA_MIN}
          and cig not in (select cig from {ict})""")
    while rows := cur.fetchmany(100000):
        for cig, imp, a, sa, t in rows:
            if cig not in sel and cig not in via6 and imbuto.RX_ICT.search(t) and not vecchio.search(t):
                sel[cig] = ("P4-nuovi-rx", imp, a, sa, t[:200])
    g4 = sorted((hashlib.sha256((k + str(SEME)).encode()).hexdigest(), k) for k, v in s6.items() if v[0].startswith("G4"))
    for _, cig in g4[:N_G4]:
        g, imp, a, sa, t = s6[cig]; sel.setdefault(cig, ("P5-g4-campione", imp, a, sa, t))
    link = collections.defaultdict(set); ted = {}
    for r in csv.DictReader(open(BASE / "lavoro/pvl/link_cig.csv", encoding="utf-8")):
        if r["cig"] in sel:
            u = (r["documenti_di_gara_link"] or "").strip().strip('"')
            if u: link[r["cig"]].add(u)
            if r["link_eform_ted"]: ted[r["cig"]] = r["link_eform_ted"]
    righe = sorted(sel.items(), key=lambda kv: (kv[1][0], -kv[1][1]))
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["cig", "priorita", "importo", "anno", "stazione_appaltante", "link", "link_ted", "oggetto"])
        for cig, (p, imp, a, sa, t) in righe:
            ls = sorted(link.get(cig, ()), key=lambda u: -specificita(u))
            w.writerow([cig, p, imp, a, sa, ls[0] if ls else "", ted.get(cig, ""), t])
    cnt = collections.Counter((v[0], bool(link.get(k))) for k, v in sel.items())
    print(json.dumps({f"{p}|{'link' if l else 'senza-link'}": n for (p, l), n in sorted(cnt.items())}, indent=1))


if __name__ == "__main__":
    main()
