"""#50 (P15) quarta misura: chi sono i CIG derivati il cui padre è dichiarato «CONTRATTO D'APPALTO» (anomalia 2024-2025).

Dopo tools/verifiche/cig_aq_tipo.py (170.759 derivati 2025 con padre «contratto d'appalto», 22.595 nel 2024).
Per i derivati 2023-2026 con padre esistente e modalità del padre = contratto d'appalto conta: padri distinti,
stazione appaltante del padre (top), tipo di scelta del contraente del padre e del figlio, strumento di svolgimento
del padre (STRUMENTO_SVOLGIMENTO, es. sistema dinamico), modalità di indizione speciali del padre, anno del padre,
divisione CPV (2 cifre) del padre; più esempi deterministici. Base: lavoro/cig_completo, duckdb 6 GB, 2 thread.
Uso (server): nice .venv/bin/python tools/verifiche/cig_aq_padre_appalto.py -> esiti/<oggi>/cig-aq/padre-appalto.json"""
import json, os, datetime
from pathlib import Path
import duckdb

R = Path(__file__).resolve().parents[2]
BASE = Path(os.environ.get("SPESAICT_BASE", R))


def main():
    c = duckdb.connect(); c.execute("set memory_limit='6GB'; set threads=2; set preserve_insertion_order=false")
    os.makedirs(BASE / "lavoro/duck/tmp", exist_ok=True); c.execute(f"set temp_directory='{BASE}/lavoro/duck/tmp'")
    fs = sorted(str(p) for p in (BASE / "lavoro/cig_completo").glob("*cig_csv*.csv"))
    c.execute(f"""create temp table t as select distinct on (cig) trim(cig) cig, anno_pubblicazione anno,
        coalesce(modalita_realizzazione,'') mod, coalesce(trim(cig_accordo_quadro),'') aq,
        coalesce(denominazione_amministrazione_appaltante,'') sa, coalesce(tipo_scelta_contraente,'') scelta,
        coalesce(STRUMENTO_SVOLGIMENTO,'') strum, coalesce(MODALITA_INDIZIONE_SPECIALI,'') spec,
        substr(coalesce(cod_cpv,''),1,2) cpv2, coalesce(oggetto_lotto, oggetto_gara,'') ogg
        from read_csv({fs}, delim=';', header=true, all_varchar=true, ignore_errors=true, union_by_name=true) where cig is not null""")
    c.execute("""create temp table d as select f.anno, f.cig, f.scelta fscelta, f.strum fstrum, p.cig pcig, p.anno panno, p.sa psa,
        p.scelta pscelta, p.strum pstrum, p.spec pspec, p.cpv2 pcpv2, p.ogg pogg
        from t f join t p on p.cig=f.aq where f.anno between '2023' and '2026' and f.mod like '%DISCENDENTE%'
        and p.mod like '%CONTRATTO D%APPALTO%' and p.mod not like '%DISCENDENTE%'""")
    out = {"generato": str(datetime.date.today()), "file": len(fs)}
    def g(col, lim=15):
        r = {}
        for a, k, n in c.execute(f"""select anno, k, n from (select anno, {col} k, count(*) n,
                row_number() over (partition by anno order by count(*) desc) rn from d group by anno, {col}) where rn<={lim} order by anno, n desc""").fetchall():
            r.setdefault(a, {})[k or "(vuoto)"] = n
        return r
    out["totale"] = {a: {"derivati": n, "padri_distinti": p} for a, n, p in c.execute(
        "select anno, count(*), count(distinct pcig) from d group by 1 order by 1").fetchall()}
    for nome, col in [("sa_padre", "psa"), ("scelta_padre", "pscelta"), ("strumento_padre", "pstrum"),
                      ("indizione_speciale_padre", "pspec"), ("anno_padre", "panno"), ("cpv2_padre", "pcpv2"),
                      ("scelta_figlio", "fscelta"), ("strumento_figlio", "fstrum")]:
        out[nome] = g(col)
    out["padri_top_2025"] = [dict(zip(("cig_padre", "sa", "anno", "scelta", "strumento", "oggetto", "derivati"), r)) for r in c.execute(
        """select pcig, psa, panno, pscelta, pstrum, left(pogg,120), count(*) from d where anno='2025' group by 1,2,3,4,5,6
        order by 7 desc limit 15""").fetchall()]
    out["esempi_2025"] = [dict(zip(("cig", "cig_padre", "sa_padre", "scelta_padre", "strumento_padre"), r)) for r in c.execute(
        """select cig, pcig, psa, pscelta, pstrum from d where anno='2025' order by hash(cig||'20261109') limit 8""").fetchall()]
    # regime dei dati: modalità dei CIG non discendenti e STRUMENTO_SVOLGIMENTO vuoto per anno (scomparsa di «CONVENZIONE» dal 2024)
    out["modalita_non_discendenti_per_anno"] = {}
    for a, m, n in c.execute("""select anno, mod, count(*) from t where anno>='2020' and mod not like '%DISCENDENTE%'
            group by all having count(*)>=100 order by 1, 3 desc""").fetchall():
        out["modalita_non_discendenti_per_anno"].setdefault(a, {})[m or "(vuota)"] = n
    out["strumento_vuoto_per_anno"] = {a: {"cig": n, "strumento_vuoto": v} for a, n, v in c.execute(
        """select anno, count(*), count(*) filter (where strum='') from t where anno>='2020' group by 1 order by 1""").fetchall()}
    o = R / "esiti" / str(datetime.date.today()) / "cig-aq"; o.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(o / "padre-appalto.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(out, ensure_ascii=False, indent=1)[:9000])


if __name__ == "__main__":
    main()
