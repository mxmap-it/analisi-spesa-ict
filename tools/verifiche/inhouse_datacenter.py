"""#52 In-house e datacenter propri: primo inquadramento con numeri (punto APERTO, nessuna conclusione).

Dal 2024, su lavoro/imbuto/ict.csv (imbuto 0.3.x, CIG distinti; importi = importo del lotto, quindi anche tetti):
  1. in-house pubblico (servizio «in-house» del classificatore): per società in-house (aggiudicatario) e per ente;
  2. segnali di infrastruttura propria: sottoclassi hardware-infrastruttura, consulenza-infrastruttura-in-house,
     software-infrastruttura (VMware, Nutanix…), più testo «data center / CED / sala macchine» e CPV infrastrutturali
     (30211 elaboratori/server, 30233 memorie/storage, 48820 server, 3242 apparecchiature di rete, 72514 gestione impianti
     informatici, 72510 gestione informatica, 45314 impianti di telecomunicazione);
  3. stati di avanzamento (dataset ANAC stati-avanzamento, ultimo zip archiviato) sui CIG in-house: quanti hanno SAL e somma.
Uso (server): SPESAICT_BASE=~/analisi-spesa-ict nice python tools/verifiche/inhouse_datacenter.py -> esiti/<oggi>/inhouse/inquadramento.json"""
import csv, glob, io, json, os, re, zipfile, datetime, collections
from pathlib import Path
import duckdb

R = Path(__file__).resolve().parents[2]
BASE = Path(os.environ.get("SPESAICT_BASE", R))
CPV_INFRA = ["30211", "30233", "48820", "3242", "72514", "72510", "45314"]
RX_DC = r"(?i)data\s*cent(er|re)|\bced\b|sala\s+(server|macchine)|\bserver\b|storage|virtualizzazion"


def f(x):
    try: return float((x or "0").replace(",", "."))
    except ValueError: return 0.0


def main():
    c = duckdb.connect(); c.execute("set memory_limit='6GB'; set threads=2")
    c.execute(f"""create temp table t as select cig, any_value(servizio) servizio, any_value(sottoclasse) sottoclasse,
        any_value(replace(cod_cpv,'-','')) cpv, max(try_cast(importo as double)) imp, any_value(stazione_appaltante) ente,
        any_value(aggiudicatari) agg, any_value(testo) testo, any_value(strato) strato
        from read_csv('{BASE}/lavoro/imbuto/ict.csv', all_varchar=true) where anno >= '2024' group by cig""")
    m = lambda q: [list(r[:-1]) + [round(r[-1] or 0, 1)] for r in c.execute(q).fetchall()]
    out = {"generato": str(datetime.date.today()), "base": "lavoro/imbuto/ict.csv dal 2024 (CIG distinti)"}
    ih = "servizio = 'in-house'"
    out["inhouse"] = {"totale": m(f"select count(*), sum(imp)/1e6 from t where {ih}")[0],
                      "per_societa": m(f"select agg, count(*), sum(imp)/1e6 from t where {ih} group by 1 order by 3 desc limit 20"),
                      "per_ente": m(f"select ente, count(*), sum(imp)/1e6 from t where {ih} group by 1 order by 3 desc limit 20"),
                      "enti_distinti": c.execute(f"select count(distinct ente) from t where {ih}").fetchone()[0]}
    casi = " ".join(f"when cpv like '{p}%' then '{p}'" for p in CPV_INFRA)
    out["infrastruttura_propria"] = {
        "per_sottoclasse": m("""select sottoclasse, count(*), sum(imp)/1e6 from t where sottoclasse in
            ('hardware-infrastruttura','consulenza-infrastruttura-in-house','software-infrastruttura') group by 1 order by 3 desc"""),
        "testo_datacenter": m(f"select count(*), sum(imp)/1e6 from t where regexp_matches(testo, '{RX_DC}')")[0],
        "testo_datacenter_per_strato": m(f"select strato, count(*), sum(imp)/1e6 from t where regexp_matches(testo, '{RX_DC}') group by 1 order by 3 desc"),
        "cpv_infrastrutturali": m(f"select p, count(*), sum(imp)/1e6 from (select case {casi} end p, imp from t) where p is not null group by 1 order by 3 desc"),
        "software_infrastruttura_per_marchio": m("""select regexp_extract(lower(testo), '(vmware|nutanix|openshift|red\\s*hat|proxmox|openstack|citrix|hyper-v|veeam)') mk,
            count(*), sum(imp)/1e6 from t where sottoclasse='software-infrastruttura' or servizio='software-infrastruttura' group by 1 order by 3 desc""")}
    cig_ih = {r[0] for r in c.execute(f"select cig from t where {ih}").fetchall()}
    D = BASE / "archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/stati-avanzamento/filesystem"
    zs = sorted(glob.glob(str(D / "*csv*.zip")))
    sal = collections.defaultdict(float)
    if zs:
        zf = zipfile.ZipFile(zs[-1]); nm = [n for n in zf.namelist() if n.endswith(".csv")][0]
        for r in csv.DictReader(io.TextIOWrapper(zf.open(nm), encoding="utf-8-sig", errors="replace"), delimiter=";"):
            if r["cig"] in cig_ih: sal[r["cig"]] += f(r.get("importo_sal"))
    out["inhouse"]["sal"] = {"fonte": Path(zs[-1]).name if zs else None, "cig_con_sal": len(sal), "su_cig_inhouse": len(cig_ih),
                             "somma_sal_meur": round(sum(sal.values()) / 1e6, 1)}
    o = R / "esiti" / str(datetime.date.today()) / "inhouse"; o.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(o / "inquadramento.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(out, ensure_ascii=False, indent=0)[:6000])


if __name__ == "__main__":
    main()
