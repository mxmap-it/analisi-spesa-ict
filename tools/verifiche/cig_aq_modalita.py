"""#50 (P15) cig_accordo_quadro: compilato per anno e per modalità di realizzazione, e denominatore validato a mano.

Seconda misura dopo tools/verifiche/cig_accordo_quadro.py (27/10, solo testo). Qui il denominatore è anche il campo
strutturato modalita_realizzazione («... DISCENDENTE DA ACCORDO QUADRO/CONVENZIONE ...»), dichiarato dalla stazione
appaltante quando chiede il CIG:
  1. per anno di pubblicazione e modalità: CIG distinti, con cig_accordo_quadro valorizzato;
  2. per anno: CIG che nel testo dichiarano un'adesione (stessa espressione del 27/10) ma con modalità non discendente;
  3. campione casuale (seme fisso) di 60 CIG 2025 «testo di adesione + CONTRATTO D'APPALTO + campo vuoto», scritto in
     report/anac/cig-aq/campione-2025.csv; le etichette a mano stanno in report/anac/cig-aq/etichette-2025.csv
     (adesione vera s/n/dubbio) e danno la precisione dell'espressione sul residuo.
Base: lavoro/cig_completo (file annuali e mensili ANAC già archiviati). duckdb con memory_limit 6 GB, 2 thread.
Uso (server): SPESAICT_BASE=~/analisi-spesa-ict nice python tools/verifiche/cig_aq_modalita.py -> esiti/<oggi>/cig-aq/modalita.json"""
import csv, json, os, math, datetime, collections
from pathlib import Path
import duckdb

R = Path(__file__).resolve().parents[2]
BASE = Path(os.environ.get("SPESAICT_BASE", R))
ADESIONE = (r"(?i)adesion\w*\s+(a(l|ll\W?)?\s*)?(accordo\s+quadro|\baq\b|convenzion)|\bin\s+adesione\b|ordinativo\s+di\s+fornitura|"
            r"contratto\s+(esecutivo|attuativo|applicativo)|appalto\s+specifico")
SEME = 20261111


def wilson(k, n, z=1.96):
    if not n: return None
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(p, 4), round(c - h, 4), round(c + h, 4)]


def main():
    c = duckdb.connect(); c.execute("set memory_limit='6GB'; set threads=2; set preserve_insertion_order=false")
    os.makedirs(BASE / "lavoro/duck/tmp", exist_ok=True); c.execute(f"set temp_directory='{BASE}/lavoro/duck/tmp'")
    fs = sorted(str(p) for p in (BASE / "lavoro/cig_completo").glob("*cig_csv*.csv"))
    c.execute(f"""create temp table b as select distinct on (cig) cig, anno_pubblicazione anno, coalesce(modalita_realizzazione,'') mod,
        coalesce(trim(cig_accordo_quadro),'') aq, coalesce(oggetto_lotto,'') || ' ' || coalesce(oggetto_gara,'') testo
        from read_csv({fs}, delim=';', header=true, all_varchar=true, ignore_errors=true, union_by_name=true) where anno_pubblicazione >= '2016'""")
    c.execute(f"alter table b add column ades boolean; update b set ades = regexp_matches(testo, '{ADESIONE.replace(chr(39), chr(39)*2)}')")
    disc = "mod like '%DISCENDENTE%'"
    per = collections.defaultdict(dict)
    for a, m, n, k, ad in c.execute("select anno, mod, count(*), count(*) filter (where aq<>''), count(*) filter (where ades) from b group by 1,2 order by 1,2").fetchall():
        per[a][m] = {"cig": n, "aq_valorizzato": k, "testo_adesione": ad}
    sint = {}
    for a, n, d, dk, nd_k, ad, ad_nd, ad_nd_vuoto in c.execute(f"""select anno, count(*), count(*) filter (where {disc}),
            count(*) filter (where {disc} and aq<>''), count(*) filter (where not {disc} and aq<>''), count(*) filter (where ades),
            count(*) filter (where ades and not {disc}), count(*) filter (where ades and aq='') from b group by 1 order by 1""").fetchall():
        sint[a] = {"cig": n, "modalita_discendente": d, "discendente_con_aq": [dk, wilson(dk, d)], "non_discendente_con_aq": nd_k,
                   "testo_adesione": ad, "testo_adesione_modalita_non_discendente": [ad_nd, wilson(ad_nd, ad)], "testo_adesione_aq_vuoto": ad_nd_vuoto}
    orf = c.execute("""select count(distinct aq), count(distinct aq) filter (where aq not in (select cig from b)) from b where aq<>''""").fetchone()
    camp = c.execute(f"""select cig, testo from b where anno='2025' and ades and aq='' and mod='CONTRATTO D''APPALTO'
        order by hash(cig || '{SEME}') limit 60""").fetchall()
    o = R / "report/anac/cig-aq"; o.mkdir(parents=True, exist_ok=True)
    with open(o / "campione-2025.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["cig", "testo"]); w.writerows([[a, t[:400]] for a, t in camp])
    out = {"generato": str(datetime.date.today()), "file": len(fs), "sintesi_per_anno": sint, "per_anno_modalita": per,
           "cig_padre_puntati_dal_2016": orf[0], "padre_non_presente_nella_base_dal_2016": orf[1]}
    et = o / "etichette-2025.csv"
    if et.exists():
        e = collections.Counter(r["adesione"] for r in csv.DictReader(open(et, encoding="utf-8")))
        n = sum(e.values()); out["campione_2025"] = {"n": n, "conteggi": dict(e), "precisione_espressione": wilson(e["s"], n),
            "stima_adesioni_vere_senza_collegamento": round(sint["2025"]["testo_adesione_aq_vuoto"] * e["s"] / n) if n else None}
    d = R / "esiti" / str(datetime.date.today()) / "cig-aq"; d.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(d / "modalita.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in out.items() if k != "per_anno_modalita"}, ensure_ascii=False, indent=0)[:5000])


if __name__ == "__main__":
    main()
