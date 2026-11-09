"""#50 (P15) terza misura: cig_accordo_quadro per anno e per TIPO di adesione, validità del CIG padre, impatto sull'imbuto.

Dopo tools/verifiche/cig_aq_modalita.py (6/11, per modalità). Qui:
  1. per anno (2016+) i CIG con modalità «discendente da AQ/convenzione»: campo valorizzato, padre esistente nella base
     CIG 2007-oggi, padre assente; il tipo di adesione è il tipo di soggetto della stazione appaltante del CIG padre
     (regole di config/tipi_soggetto.yaml: consip, psn, aggregatore-regionale, consorzio-unione, altro);
  2. padre puntato che non è a sua volta un AQ/convenzione (modalità del padre), come controllo di coerenza;
  2bis. (ex lavoro/aq_pmod.py, regola #47) per anno: modalità dei padri esistenti (quanti «contratto d'appalto»
     invece di AQ/convenzione) e forma dei padri inesistenti (primo carattere e lunghezza del CIG puntato);
  3. imbuto (lavoro/imbuto/ict.csv): spesa ICT dei CIG discendenti per strato, collegata a un padre esistente oppure
     non collegabile (campo vuoto o padre inesistente), quindi senza il prodotto dell'AQ da ereditare.
Base: lavoro/cig_completo (file ANAC archiviati). duckdb memory_limit 6 GB, 2 thread, temp su disco in lavoro/.
Uso (server): SPESAICT_BASE=~/analisi-spesa-ict nice python tools/verifiche/cig_aq_tipo.py -> esiti/<oggi>/cig-aq/tipo.json"""
import json, os, datetime, collections
from pathlib import Path
import duckdb, yaml

R = Path(__file__).resolve().parents[2]
BASE = Path(os.environ.get("SPESAICT_BASE", R))


def caso_tipo(col):
    rr = yaml.safe_load(open(R / "config/tipi_soggetto.yaml", encoding="utf-8"))["regole"]
    q = lambda s: s.replace("'", "''")
    return "case " + " ".join(f"when regexp_matches({col}, '{q(r['rx'])}') then '{r['tipo']}'" for r in rr) + " else 'altro' end"


def main():
    c = duckdb.connect(); c.execute("set memory_limit='6GB'; set threads=2; set preserve_insertion_order=false")
    os.makedirs(BASE / "lavoro/duck/tmp", exist_ok=True); c.execute(f"set temp_directory='{BASE}/lavoro/duck/tmp'")
    fs = sorted(str(p) for p in (BASE / "lavoro/cig_completo").glob("*cig_csv*.csv"))
    c.execute(f"""create temp table t as select distinct on (cig) trim(cig) cig, anno_pubblicazione anno,
        coalesce(modalita_realizzazione,'') mod, coalesce(trim(cig_accordo_quadro),'') aq,
        upper(coalesce(denominazione_amministrazione_appaltante,'')) sa
        from read_csv({fs}, delim=';', header=true, all_varchar=true, ignore_errors=true, union_by_name=true) where cig is not null""")
    c.execute(f"create temp table p as select cig, mod pmod, {caso_tipo('sa')} ptipo from t")
    c.execute("""create temp table d as select t.cig, t.anno, t.aq, p.ptipo, p.pmod,
        case when t.aq='' then 'vuoto' when p.cig is null then 'padre-inesistente' else 'padre-esistente' end esito
        from t left join p on p.cig=t.aq where t.anno>='2016' and t.mod like '%DISCENDENTE%'""")
    per = collections.defaultdict(lambda: collections.defaultdict(dict))
    for a, e, tp, n in c.execute("select anno, esito, coalesce(ptipo,'-'), count(*) from d group by all order by all").fetchall():
        per[a][e][tp] = n
    sint = {}
    for a, n, v, ok, ino, ppn in c.execute("""select anno, count(*), count(*) filter (where esito='vuoto'),
            count(*) filter (where esito='padre-esistente'), count(*) filter (where esito='padre-inesistente'),
            count(*) filter (where esito='padre-esistente' and pmod not like '%ACCORDO QUADRO%' and pmod not like '%CONVENZIONE%')
            from d group by 1 order by 1""").fetchall():
        sint[a] = {"discendenti": n, "vuoto": v, "padre_esistente": ok, "padre_inesistente": ino,
                   "quota_collegabile": round(ok / n, 4), "padre_esistente_ma_non_AQ_conv": ppn}
    tipo_tot = {tp: {"n": n, "padre_inesistente": ino} for tp, n, ino in c.execute(
        "select coalesce(ptipo,'(vuoto o padre inesistente)'), count(*), 0 from d group by 1 order by 2 desc").fetchall()}
    pmod = collections.defaultdict(dict)
    for a, m, n in c.execute("select anno, coalesce(pmod,''), count(*) from d where esito='padre-esistente' group by all order by 1, 3 desc").fetchall():
        pmod[a][m or "(vuota)"] = n
    forme = collections.defaultdict(dict)
    for a, f, n in c.execute("""select anno, substr(aq,1,1)||':'||length(aq), count(*) from d where esito='padre-inesistente'
            group by all order by 1, 3 desc""").fetchall():
        forme[a][f] = n
    ict = BASE / "lavoro/imbuto/ict.csv"
    c.execute(f"""create temp table i as select distinct on (cig) cig, anno, strato, try_cast(importo as double) imp
        from read_csv('{ict}', header=true, all_varchar=true)""")
    imb = {}
    for s, e, tp, n, imp in c.execute("""select i.strato, coalesce(d.esito,'non-discendente'), coalesce(d.ptipo,'-'), count(*),
            round(sum(coalesce(i.imp,0))) from i left join d using (cig) group by all order by all""").fetchall():
        imb.setdefault(s, {}).setdefault(e, {})[tp] = {"cig": n, "importo": imp}
    imb_anno = {a: {"discendenti": n, "importo": i0, "non_collegabili": k, "importo_non_collegabile": i1}
                for a, n, i0, k, i1 in c.execute("""select i.anno, count(*), round(sum(coalesce(imp,0))),
            count(*) filter (where esito<>'padre-esistente'), round(sum(coalesce(imp,0)) filter (where esito<>'padre-esistente'))
            from i join d using (cig) group by 1 order by 1""").fetchall()}
    tot = c.execute("""select count(*), round(sum(coalesce(imp,0))), count(*) filter (where esito<>'padre-esistente'),
            round(sum(coalesce(imp,0)) filter (where esito<>'padre-esistente')) from i join d using (cig)""").fetchone()
    es = c.execute("""select anno, cig, esito, aq from d where esito<>'padre-esistente' and anno='2025'
            order by hash(cig||'20261109') limit 10""").fetchall()
    out = {"generato": str(datetime.date.today()), "file": len(fs), "cig_base": c.execute("select count(*) from t").fetchone()[0],
           "sintesi_per_anno": sint, "per_anno_esito_tipo": per, "tipo_padre_totale": tipo_tot,
           "modalita_padre_per_anno": pmod, "forma_padre_inesistente_per_anno": forme,
           "imbuto": {"file": str(ict.relative_to(BASE)), "ict_discendenti": tot[0], "importo": tot[1],
                      "non_collegabili": tot[2], "importo_non_collegabile": tot[3],
                      "quota_importo_non_collegabile": round(tot[3] / tot[1], 4) if tot[1] else None,
                      "per_anno": imb_anno, "per_strato": imb},
           "esempi_2025_non_collegabili": [dict(zip(("anno", "cig", "esito", "cig_accordo_quadro"), r)) for r in es]}
    o = R / "esiti" / str(datetime.date.today()) / "cig-aq"; o.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(o / "tipo.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({k: out[k] for k in ("cig_base", "sintesi_per_anno", "tipo_padre_totale")}, ensure_ascii=False))
    print(json.dumps({"modalita_padre_2025": dict(list(pmod.get("2025", {}).items())[:8]),
                      "forma_padre_inesistente_2025": dict(list(forme.get("2025", {}).items())[:6])}, ensure_ascii=False))
    print(json.dumps({k: v for k, v in out["imbuto"].items() if k != "per_strato"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
