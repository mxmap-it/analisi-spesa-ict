"""#44 #59 Perimetro ICT per CPV: lista bianca (config/perimetro_cpv.yaml) misurata sui campioni, e attendibilità del CPV.

Campioni e verità di riferimento:
  - L  report/cpv/campione-lista-bianca: 200 CIG casuali con CPV nella lista bianca (ict.csv dal 2024) -> precisione;
  - S1 report/cpv/campione-s1: 200 CIG casuali esclusi in S1 (CPV fuori lista e testo senza segnali ICT) -> falsi esclusi;
    entrambi etichettati ICT s/n/dubbio dall'agente sul solo oggetto, senza vedere il CPV;
  - V3 campione 611 (dati/classificazioni/campione-v3.jsonl, via 6 + atti): ICT = servizio != «altro», cloud = e_cloud;
  - cieco: campioni report/metodo/lente-cieco{,-2}: CIG con prodotto etichettato = ICT certo.
Misure: precisione della lista bianca (P(ICT | CPV in lista)) e per prefisso; falsi esclusi in S1; esiti del CPV sugli ICT
(fuori-lista / generico / specifico / mancante) e CPV fuori lista più frequenti (candidati); per i cloud del 611: CPV che
esprime un servizio erogato da terzi (hosting, ASP, storage, Internet) o no. Intervalli di Wilson al 95%.
Uso (server): SPESAICT_BASE=~/analisi-spesa-ict python tools/verifiche/perimetro_cpv.py -> esiti/<oggi>/cpv/perimetro-cpv.json"""
import csv, json, os, math, datetime, collections
from pathlib import Path
import yaml, duckdb

R = Path(__file__).resolve().parents[2]
BASE = Path(os.environ.get("SPESAICT_BASE", R))
WL = yaml.safe_load(open(R / "config/perimetro_cpv.yaml", encoding="utf-8"))
PREF = sorted((str(x["prefisso"]) for x in WL["lista_bianca"]), key=len, reverse=True)
EROG = [str(x) for x in WL["cpv_servizio_erogato"]]


def wilson(k, n, z=1.96):
    if not n: return None
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(p, 4), round(c - h, 4), round(c + h, 4)]


def pulito(cpv): return (cpv or "").split("-")[0].strip()
def pref(cpv): return next((p for p in PREF if pulito(cpv).startswith(p)), "")
def generico(cpv): c = pulito(cpv); return len(c) == 8 and c[3:] == "00000"   # 72000000, 48000000, 30200000
def erogato(cpv): return any(pulito(cpv).startswith(p) for p in EROG)


def cpv_di(cigs):
    c = duckdb.connect(); c.execute("set memory_limit='6GB'; set threads=2")
    c.execute("create table k(cig varchar)"); c.executemany("insert into k values (?)", [[x] for x in cigs])
    fs = sorted(str(p) for p in (BASE / "lavoro/cig_completo").glob("*cig_csv*.csv"))
    q = f"""select cig, any_value(cod_cpv), any_value(descrizione_cpv) from read_csv({fs}, delim=';', header=true,
            all_varchar=true, ignore_errors=true, union_by_name=true) where cig in (select cig from k) group by cig"""
    return {a: (b or "", d or "") for a, b, d in c.execute(q).fetchall()}


def universo():
    """CIG distinti e importo dal 2024 in ict.csv per prefisso della lista, più i codici segnaposto/generici nell'intera base."""
    c = duckdb.connect(); c.execute("set memory_limit='6GB'; set threads=2")
    ict = f"read_csv('{BASE}/lavoro/imbuto/ict.csv', all_varchar=true)"
    casi = " ".join(f"when replace(cod_cpv,'-','') like '{p}%' then '{p}'" for p in PREF)
    righe = c.execute(f"""select case {casi} else '(fuori lista, testo ICT)' end p, count(distinct cig), sum(try_cast(importo as double))/1e6
        from {ict} where anno >= '2024' group by 1 order by 2 desc""").fetchall()
    fs = sorted(str(p) for p in (BASE / "lavoro/cig_completo").glob("*cig_csv*.csv"))
    base = f"read_csv({fs}, delim=';', header=true, all_varchar=true, ignore_errors=true, union_by_name=true)"
    tot, seg, gen = c.execute(f"""select count(distinct cig), count(distinct cig) filter (where cod_cpv like '99999999%' or coalesce(cod_cpv,'')=''),
        count(distinct cig) filter (where len(split_part(cod_cpv,'-',1))=8 and substr(cod_cpv,4,5)='00000')
        from {base} where anno_pubblicazione >= '2024'""").fetchone()
    return {"ict_csv_per_prefisso": [[p, n, round(e or 0, 1)] for p, n, e in righe],
            "base_cig": {"cig": tot, "cpv_99999999_o_vuoto": [seg, round(seg / tot, 4)], "cpv_livello_gruppo_xxx00000": [gen, round(gen / tot, 4)]}}


def main():
    et = {n: {r["cig"]: r["ict"] for r in csv.DictReader(open(R / f"report/cpv/{n}/etichette.csv", encoding="utf-8"))}
          for n in ("campione-lista-bianca", "campione-s1")}
    L, S = et["campione-lista-bianca"], et["campione-s1"]
    v3 = {}
    for l in open(R / "dati/classificazioni/campione-v3.jsonl", encoding="utf-8"):
        j = json.loads(l); e = j["esito"]
        v3[j["cig"]] = {"ict": "n" if e["servizio"] == "altro" else "s", "cloud": e["e_cloud"], "servizio": e["servizio"], "cpv": j["ingresso"]["cpv"] or ""}
    cieco = [r["cig"] for d in ("lente-cieco", "lente-cieco-2")
             for r in csv.DictReader(open(R / f"report/metodo/{d}/etichette.csv", encoding="utf-8")) if r["etichetta_prodotto"]]
    cpv = cpv_di(set(L) | set(S) | set(cieco))
    for k, v in v3.items(): cpv.setdefault(k, (v["cpv"], ""))
    g = lambda k: cpv.get(k, ("", ""))
    import re, sys; sys.path.insert(0, str(R / "tools/analisi"))
    from classifica import CPV_ICT  # noqa: E402
    cod = set(re.match(r"\^\((.*)\)", CPV_ICT.pattern).group(1).split("|"))
    out = {"versione_lista": WL["versione"], "generato": str(datetime.date.today()), "prefissi": PREF,
           "allineata_a_classifica_CPV_ICT": cod == set(PREF), "solo_in_classifica": sorted(cod - set(PREF)), "solo_in_lista": sorted(set(PREF) - cod)}
    out["universo_dal_2024"] = universo()
    c = collections.Counter(L.values())
    out["precisione_lista"] = {"n": len(L), "conteggi": dict(c), "stretta": wilson(c["s"], len(L)), "dubbi_come_ict": wilson(c["s"] + c["dubbio"], len(L))}
    pp = collections.defaultdict(collections.Counter)
    for k, e in L.items(): pp[pref(g(k)[0]) or "(fuori: testo ICT)"][e] += 1
    out["precisione_per_prefisso"] = {p: dict(v) for p, v in sorted(pp.items())}
    out["lista_non_ict"] = [{"cig": k, "cpv": g(k)[0], "descr": g(k)[1], "etichetta": e} for k, e in L.items() if e != "s"]
    c = collections.Counter(S.values())
    out["s1"] = {"n": len(S), "conteggi": dict(c), "falsi_esclusi": wilson(c["s"], len(S)), "con_dubbi": wilson(c["s"] + c["dubbio"], len(S)),
                 "casi": [{"cig": k, "etichetta": e, "cpv": g(k)[0], "descr": g(k)[1]} for k, e in S.items() if e != "n"]}
    gruppi = {"V3-611-ict": [(k, v["servizio"]) for k, v in v3.items() if v["ict"] == "s"],
              "cieco-prodotto": [(k, "") for k in cieco],
              "lista-bianca-ict": [(k, "") for k, e in L.items() if e == "s"]}
    out["esiti_cpv"] = {}
    for nome, xs in gruppi.items():
        c = collections.Counter(); fl = collections.Counter(); sv = collections.defaultdict(collections.Counter)
        for k, s in xs:
            co = g(k)[0]
            e = "mancante" if not co else "fuori-lista" if not pref(co) else "generico" if generico(co) else "specifico"
            c[e] += 1; sv[s or "-"][e] += 1
            if e == "fuori-lista": fl[pulito(co)[:5] + " " + g(k)[1][:40]] += 1
        n = len(xs)
        out["esiti_cpv"][nome] = {"n": n, **{e: [c[e], wilson(c[e], n)] for e in ("specifico", "generico", "fuori-lista", "mancante")},
                                  "fuori_lista": fl.most_common(20), "per_servizio": {k: dict(v) for k, v in sv.items()}}
    nc = [k for k, v in v3.items() if v["cloud"] == "s"]
    nn = [k for k, v in v3.items() if v["cloud"] == "n" and v["ict"] == "s"]
    a = sum(erogato(g(k)[0]) for k in nc); b = sum(erogato(g(k)[0]) for k in nn)
    out["cloud_v3"] = {"cloud": len(nc), "cloud_con_cpv_erogato": [a, wilson(a, len(nc))],
                       "ict_non_cloud": len(nn), "non_cloud_con_cpv_erogato": [b, wilson(b, len(nn))],
                       "cpv_dei_cloud": collections.Counter(pulito(g(k)[0]) for k in nc).most_common(15)}
    o = R / "esiti" / str(datetime.date.today()) / "cpv"; o.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(o / "perimetro-cpv.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({k: out[k] for k in ("precisione_lista", "s1", "cloud_v3", "precisione_per_prefisso")}, ensure_ascii=False))
    for nome, v in out["esiti_cpv"].items():
        print(nome, {e: v[e] for e in ("n", "specifico", "generico", "fuori-lista", "mancante")}); print("  ", v["fuori_lista"][:12])
    for x in out["lista_non_ict"]: print(x)


if __name__ == "__main__":
    main()
