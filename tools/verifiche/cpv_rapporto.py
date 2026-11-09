"""#59 #44 Rapporto CPV: attendibilità del CPV dichiarato in ANAC per l'ICT, effetto del perimetro 0.3.3 (+R53, 0.3.4) rispetto a
0.3.2, sottoclasse videosorveglianza di 3224, tabella di riclassificazione.

A. Attendibilità (campioni con verità di riferimento, già versionati):
   - L  report/cpv/campione-lista-bianca (200 CIG con CPV in lista, etichetta sul solo oggetto) -> CPV ICT su oggetto non ICT;
   - S1 report/cpv/campione-s1 (200 CIG esclusi) e V3 campione 611 (via 6 con atti) -> oggetto ICT con CPV non ICT;
   per anno di pubblicazione e tipo di ente (regole TIPI sul nome della stazione appaltante, sotto). Wilson 95 %.
   Universo: in ict.csv dal 2024 i CIG fuori lista entrati per il testo (= oggetto ICT con CPV non ICT, lato testo).
B. Effetto perimetro: base ict.csv (imbuto 0.3.2, una riga per CPV) -> 0.3.2 con R53 (un CIG una volta) -> 0.3.3 con R53:
   escono i CIG con 79342 che non hanno altri CPV in lista né testo ICT (RX_ICT 0.3.3); entrano i CIG dal 2024 in S1
   (assenti da ict.csv, importo >= soglia) che il nuovo RX_ICT («sw», «connettività») porta nel residuo.
C. 3224: classi videosorveglianza / ICT stretto / altro con regole sul testo (RX_VIDEO, RX_ICT), controllate sulle
   etichette della review del 7/11 (report/cpv/review-79342-3224); importi con e senza l'errore B139F77033.
D. dati/classificazioni/cpv-riclassificazione.csv: per i 611 del V3, CPV dichiarato -> classe spesaict -> CPV proposto.
Uso (server): SPESAICT_BASE=~/analisi-spesa-ict nice python tools/verifiche/cpv_rapporto.py -> esiti/<oggi>/cpv/rapporto-cpv.json
duckdb 6 GB, 2 thread, temp in lavoro/duck/tmp."""
import csv, json, os, re, sys, math, datetime, collections
from pathlib import Path
import yaml, duckdb

R = Path(__file__).resolve().parents[2]
BASE = Path(os.environ.get("SPESAICT_BASE", R))
sys.path.insert(0, str(R / "tools/analisi"))
import imbuto  # noqa: E402

WL = yaml.safe_load(open(R / "config/perimetro_cpv.yaml", encoding="utf-8"))
PREF = sorted((str(x["prefisso"]) for x in WL["lista_bianca"]), key=len, reverse=True)   # 0.3.3: senza 79342
PREF_032 = PREF + ["79342"]
NUOVO = imbuto.RX_ICT
VECCHIO = re.compile(NUOVO.pattern.replace("|sw|connettivit\\w*)", ")"), re.I)
assert VECCHIO.pattern != NUOVO.pattern
OUTLIER = "B139F77033"   # Università di Perugia, «telecamera con accessori», 4.703.401.002 €: errore d'importo
RX_VIDEO = re.compile(r"videosorv|video.sorv|telecamer|\bztl\b|targh|fototrappol|\btvcc\b|\bcctv\b|varch|lettura\s+targ|"
                      r"sorveglianza|foto.?trapp|dash.?cam|body.?cam|bodycam|videocontrollo|video\s*control", re.I)
TIPI = [("comune", r"^COMUNE\b|\bCOMUNE DI\b|^CITTA'? DI\b|ROMA CAPITALE"),
        ("regione-provincia", r"^REGIONE\b|^PROVINCIA\b|PROVINCIA AUTONOMA|CITTA'? METROPOLITANA|GIUNTA REGIONALE|CONSIGLIO REGIONALE"),
        ("sanita", r"\bA\.?S\.?L\b|\bASL\b|AZIENDA SANITARIA|AZIENDA OSPEDALIER|OSPEDAL|\bASST\b|\bATS\b|\bAUSL\b|\bULSS\b|\bASP\b|IRCCS|AZIENDA U(NITA|SL)|\bESTAR\b|AZIENDA ZERO|SO\.?RE\.?SA"),
        ("universita-ricerca", r"UNIVERSIT|POLITECNICO|CONSIGLIO NAZIONALE DELLE RICERCHE|\bCNR\b|ISTITUTO NAZIONALE DI|\bINFN\b|\bINAF\b|\bINGV\b|\bENEA\b|SCUOLA NORMALE|\bSISSA\b|AGENZIA SPAZIALE"),
        ("scuola", r"ISTITUTO COMPRENSIVO|ISTITUTO DI ISTRUZIONE|LICEO|CIRCOLO DIDATTICO|SCUOLA (PRIMARIA|SECONDARIA|MEDIA)|ISTITUTO TECNICO|ISTITUTO PROFESSIONALE|CONSERVATORIO|ACCADEMIA DI BELLE"),
        ("stato-centrale", r"MINISTERO|PRESIDENZA DEL CONSIGLIO|AGENZIA (DELLE|DEL|PER)|COMANDO|\bINPS\b|\bINAIL\b|\bISTAT\b|\bCONSIP\b|CORTE DEI CONTI|PREFETTURA|QUESTURA|CARABINIERI|GUARDIA DI FINANZA|POLIZIA DI STATO|AERONAUTICA|ESERCITO|MARINA MILITARE|AVVOCATURA|SOGEI|DIFESA"),
        ("societa-partecipata", r"S\.?P\.?A\.?\b|S\.?R\.?L\.?\b|SOCIETA'|S\.?C\.?A\.?R\.?L|SPA$|SRL$"),
        ("altro", r".")]
TIPI = [(t, re.compile(x, re.I)) for t, x in TIPI]
SERV_CPV = {  # classe spesaict -> CPV 2008 più vicino (proposta; dove manca un codice adatto lo si dice)
    ("cloud", "s"): ("72416000 / 72415000", "nessun codice per IaaS, PaaS, SaaS: il più vicino è ASP (72416000) o hosting (72415000)"),
    ("psn", "s"): ("72510000 / 72415000", "PSN non distinguibile: gestione informatica o hosting"),
    ("in-house", "s"): ("72510000", "gestione informatica; in-house non distinguibile"),
    ("in-house", "n"): ("72510000", "gestione informatica; in-house non distinguibile"),
    ("licenza", "n"): ("48xxxxxx", "pacchetto software per funzione; licenza perpetua e abbonamento indistinti"),
    ("licenza", "s"): ("48xxxxxx / 72416000", "abbonamento SaaS: nessun codice proprio"),
    ("servizi-professionali", "n"): ("722xxxxx / 7259xxxx", "sviluppo, consulenza, servizi professionali informatici"),
    ("servizi-professionali", "s"): ("722xxxxx / 7259xxxx", "servizi professionali per il cloud: nessun codice proprio"),
    ("telefonia", "s"): ("64210000 / 3225xxxx", "telefonia: 642 è fuori lista, entra per testo"),
    ("telefonia", "n"): ("64210000 / 3225xxxx", "telefonia: 642 è fuori lista, entra per testo"),
    ("altro", "n"): ("(non ICT)", "oggetto non ICT: un CPV in lista è un errore di codifica"),
}


def wilson(k, n, z=1.96):
    if not n: return None
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [k, n, round(p, 4), round(max(0, c - h), 4), round(c + h, 4)]


def pulito(cpv): return (cpv or "").split("-")[0].strip()
def in_lista(cpv, pref=PREF): return any(pulito(cpv).startswith(p) for p in pref)
def generico(cpv): c = pulito(cpv); return len(c) == 8 and c[3:] == "00000"
def tipo(nome): return next((t for t, rx in TIPI if rx.search(nome or "")), "ignoto")


def conn():
    c = duckdb.connect(); c.execute("set memory_limit='6GB'; set threads=2; set preserve_insertion_order=false")
    os.makedirs(BASE / "lavoro/duck/tmp", exist_ok=True); c.execute(f"set temp_directory='{BASE}/lavoro/duck/tmp'")
    return c


def base():
    fs = sorted(str(p) for p in (BASE / "lavoro/cig_completo").glob("*cig_csv*.csv"))
    return f"read_csv({fs}, delim=';', header=true, all_varchar=true, ignore_errors=true, union_by_name=true)"


def parte_a(c, out):
    et = {n: {r["cig"]: r["ict"] for r in csv.DictReader(open(R / f"report/cpv/{n}/etichette.csv", encoding="utf-8"))}
          for n in ("campione-lista-bianca", "campione-s1")}
    v3 = {}
    for l in open(R / "dati/classificazioni/campione-v3.jsonl", encoding="utf-8"):
        j = json.loads(l); e = j["esito"]
        v3[j["cig"]] = {"ict": "n" if e["servizio"] == "altro" else "s", "cloud": e["e_cloud"], "servizio": e["servizio"],
                        "cpv": j["ingresso"]["cpv"] or "", "ente": j["ingresso"].get("stazione_appaltante") or ""}
    cigs = set(et["campione-lista-bianca"]) | set(et["campione-s1"]) | set(v3)
    c.execute("create or replace table k(cig varchar)"); c.executemany("insert into k values (?)", [[x] for x in cigs])
    info = {}
    for cig, anno, ente, cpvs in c.execute(f"""select cig, min(anno_pubblicazione), any_value(denominazione_amministrazione_appaltante),
            list(distinct cod_cpv) from {base()} where cig in (select cig from k) group by cig""").fetchall():
        info[cig] = (anno, ente, [x for x in cpvs if x])
    righe = []   # (campione, cig, anno, tipo, cpv_in_lista, ict)
    for n, d in (("L", et["campione-lista-bianca"]), ("S1", et["campione-s1"])):
        for cig, e in d.items():
            a, ente, cpvs = info.get(cig, ("", "", []))
            righe.append((n, cig, a or "?", tipo(ente), any(in_lista(x) for x in cpvs), e))
    for cig, v in v3.items():
        a, ente, cpvs = info.get(cig, ("", v["ente"], [v["cpv"]]))
        righe.append(("V3", cig, a or "?", tipo(ente or v["ente"]), any(in_lista(x) for x in (cpvs or [v["cpv"]])), v["ict"]))
    res = {"n_righe": len(righe), "anni_campioni": dict(collections.Counter((r[0], r[2]) for r in righe).most_common()) and
           {f"{a}|{b}": n for (a, b), n in collections.Counter((r[0], r[2]) for r in righe).items()}}

    def tab(filtro, esito, chiave):
        d = collections.defaultdict(lambda: [0, 0])
        for r in righe:
            if not filtro(r): continue
            for k in ("tutti", chiave(r)):
                d[k][1] += 1; d[k][0] += esito(r)
        return {k: wilson(*v) for k, v in sorted(d.items())}
    anno_g = lambda r: r[2] if r[2] >= "2024" else ("2019-2023" if r[2] >= "2019" else "fino-2018")
    # 1) CPV ICT su oggetto non ICT: fra i CIG con CPV in lista (L e V3), quota non ICT (dubbi a parte)
    f1 = lambda r: r[4] and r[0] in ("L", "V3") and r[5] != "dubbio"
    res["cpv_ict_oggetto_non_ict"] = {"per_anno": tab(f1, lambda r: r[5] == "n", anno_g), "per_tipo": tab(f1, lambda r: r[5] == "n", lambda r: r[3]),
                                      "solo_L_per_anno": tab(lambda r: r[0] == "L" and r[5] != "dubbio", lambda r: r[5] == "n", anno_g)}
    # 2) Oggetto ICT con CPV non ICT: fra gli ICT veri del V3 (verità con atti), quota con nessun CPV in lista
    f2 = lambda r: r[0] == "V3" and r[5] == "s"
    res["oggetto_ict_cpv_non_ict"] = {"per_anno": tab(f2, lambda r: not r[4], anno_g), "per_tipo": tab(f2, lambda r: not r[4], lambda r: r[3])}
    # 3) S1: ICT veri fra gli esclusi (CPV fuori lista e testo senza segnali ICT), per anno e tipo
    f3 = lambda r: r[0] == "S1"
    res["s1_falsi_esclusi"] = {"per_tipo": tab(f3, lambda r: r[5] == "s", lambda r: r[3])}
    # universo: in ict.csv dal 2024, CIG fuori lista entrati per testo (CPV non ICT, oggetto ICT dal testo), per anno e tipo
    ict = f"read_csv('{BASE}/lavoro/imbuto/ict.csv', all_varchar=true)"
    u = collections.defaultdict(lambda: [0, 0, 0.0])
    for anno, ente, fuori, imp in c.execute(f"""select anno, any_value(stazione_appaltante), max(cpv_ict)='0' and min(cpv_ict)='0',
            max(try_cast(importo as double)) from {ict} where anno>='2024' group by cig, anno""").fetchall():
        for k in (anno, tipo(ente)):
            u[k][0] += 1; u[k][1] += fuori; u[k][2] += (imp or 0) if fuori else 0
    res["universo_ict_csv_dal_2024_fuori_lista_per_testo"] = {k: {"cig": v[0], "fuori_lista": v[1], "quota": round(v[1] / v[0], 4),
                                                                   "meur_fuori_lista": round(v[2] / 1e6, 1)} for k, v in sorted(u.items())}
    res["regole_tipo_ente"] = {t: rx.pattern for t, rx in TIPI}
    out["A_attendibilita"] = res
    return v3, info


def parte_b(c, out):
    ict = f"read_csv('{BASE}/lavoro/imbuto/ict.csv', all_varchar=true)"
    righe, cig_d, e_righe, e_cig = c.execute(f"""select count(*), count(distinct cig), sum(try_cast(importo as double))/1e6,
        (select sum(m)/1e6 from (select max(try_cast(importo as double)) m from {ict} where anno>='2024' group by cig))
        from {ict} where anno>='2024'""").fetchone()
    res = {"0.3.2_righe": {"righe": righe, "meur": round(e_righe, 1)},
           "0.3.2_con_R53": {"cig": cig_d, "meur": round(e_cig, 1), "doppioni_tolti": righe - cig_d, "meur_tolti": round(e_righe - e_cig, 1)}}
    # uscite: CIG con almeno un CPV 79342 in ict.csv dal 2024
    c.execute(f"""create or replace table m as select cig, any_value(strato) strato, max(try_cast(importo as double)) imp,
        any_value(testo) testo from {ict} where anno>='2024' and cig in (select cig from {ict} where replace(cod_cpv,'-','') like '79342%') group by cig""")
    cpvs = {a: [x for x in b if x] for a, b in c.execute(f"select cig, list(distinct cod_cpv) from {base()} where cig in (select cig from m) group by cig").fetchall()}
    esce = collections.Counter(); esce_e = collections.Counter(); per_strato = collections.Counter()
    for cig, st, imp, testo in c.execute("select * from m").fetchall():
        altri = any(in_lista(x) for x in cpvs.get(cig, []))
        k = "resta: altro CPV in lista (R53)" if altri else "resta: testo ICT" if NUOVO.search(testo or "") else "esce in S1"
        esce[k] += 1; esce_e[k] += imp or 0
        if k == "esce in S1": per_strato[st] += 1
    res["79342_uscite"] = {k: [v, round(esce_e[k] / 1e6, 1)] for k, v in esce.items()}
    res["79342_uscite_per_strato"] = dict(per_strato)
    # entrate: CIG dal 2024 assenti da ict.csv che il nuovo RX_ICT porta nel residuo
    cur = c.execute(f"""select distinct on (cig) cig, try_cast(replace(importo_lotto,',','.') as double) imp,
        coalesce(oggetto_gara,'') || ' | ' || coalesce(oggetto_lotto,'') testo from {base()}
        where anno_pubblicazione >= '2024' and try_cast(replace(importo_lotto,',','.') as double) >= {imbuto.SOGLIA_MIN}
          and cig not in (select cig from {ict})""")
    g = collections.Counter(); ge = collections.Counter()
    while True:
        rows = cur.fetchmany(100000)
        if not rows: break
        for cig, imp, testo in rows:
            if NUOVO.search(testo) and not VECCHIO.search(testo):
                gr = imbuto.gruppo(imp, testo); g[gr] += 1; ge[gr] += imp
    res["rx_0.3.3_entrate"] = {"cig": sum(g.values()), "meur": round(sum(ge.values()) / 1e6, 1),
                               "per_gruppo": {k: [v, round(ge[k] / 1e6, 1)] for k, v in g.most_common()}}
    usc = esce["esce in S1"]; usc_e = esce_e["esce in S1"] / 1e6
    res["0.3.3_con_R53"] = {"cig": cig_d - usc + res["rx_0.3.3_entrate"]["cig"], "meur": round(e_cig - usc_e + res["rx_0.3.3_entrate"]["meur"], 1),
                            "saldo_cig": res["rx_0.3.3_entrate"]["cig"] - usc, "saldo_meur": round(res["rx_0.3.3_entrate"]["meur"] - usc_e, 1)}
    out["B_effetto_perimetro"] = res


def parte_c(c, out):
    ict = f"read_csv('{BASE}/lavoro/imbuto/ict.csv', all_varchar=true)"
    rows = c.execute(f"""select cig, any_value(anno), any_value(strato), max(try_cast(importo as double)), any_value(stazione_appaltante), any_value(testo)
        from {ict} where anno>='2024' and replace(cod_cpv,'-','') like '3224%' group by cig""").fetchall()
    cl = lambda t: "videosorveglianza" if RX_VIDEO.search(t or "") else "ict-stretto" if NUOVO.search(t or "") else "altro"
    agg = collections.defaultdict(lambda: [0, 0.0, 0.0]); es = collections.defaultdict(list); st = collections.defaultdict(collections.Counter)
    tipi = collections.defaultdict(collections.Counter)
    for cig, anno, strato, imp, ente, testo in rows:
        k = cl(testo); agg[k][0] += 1; agg[k][1] += imp or 0; agg[k][2] += 0 if cig == OUTLIER else (imp or 0)
        st[k][strato] += 1; tipi[k][tipo(ente)] += 1; es[k].append((imp or 0, cig, ente, (testo or "")[:140]))
    res = {"universo_dal_2024": {k: {"cig": v[0], "meur": round(v[1] / 1e6, 1), "meur_senza_B139F77033": round(v[2] / 1e6, 1),
                                     "per_strato": dict(st[k]), "per_tipo_ente": dict(tipi[k].most_common())} for k, v in agg.items()},
           "esempi_maggiori": {k: [[round(a / 1e6, 2), b, e, t] for a, b, e, t in sorted(v, reverse=True)[:6] if b != OUTLIER] for k, v in es.items()},
           "regola_video": RX_VIDEO.pattern}
    testi = {r["cig"]: r["testo"] for r in csv.DictReader(open(R / "report/cpv/review-79342-3224/campione.csv", encoding="utf-8"))}
    m = collections.Counter()
    for e in csv.DictReader(open(R / "report/cpv/review-79342-3224/etichette.csv", encoding="utf-8")):
        if e["prefisso"] != "3224": continue
        m[(e["ict"], cl(testi.get(e["cig"], "")))] += 1
    vv = sum(v for (a, b), v in m.items() if b == "videosorveglianza")
    ok = m[("videosorveglianza", "videosorveglianza")]; tot_v = sum(v for (a, b), v in m.items() if a == "videosorveglianza")
    res["controllo_regola_su_review"] = {"matrice_etichetta_regola": {f"{a}->{b}": v for (a, b), v in sorted(m.items())},
                                         "precisione_regola": wilson(ok, vv), "richiamo_regola": wilson(ok, tot_v)}
    out["C_videosorveglianza_3224"] = res


def parte_d(v3, info, out):
    p = R / "dati/classificazioni/cpv-riclassificazione.csv"
    cnt = collections.Counter()
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["cig", "cpv_dichiarato", "esito_cpv", "servizio_spesaict", "e_cloud", "cpv_proposto", "coerente", "nota"])
        for cig, v in sorted(v3.items()):
            cpvs = info.get(cig, ("", "", []))[2] or [v["cpv"]]
            co = v["cpv"] or (cpvs[0] if cpvs else "")
            es = "mancante" if not co or pulito(co).startswith("99999999") else "fuori-lista" if not in_lista(co) else "generico" if generico(co) else "specifico"
            prop, nota = SERV_CPV.get((v["servizio"], v["cloud"]), ("?", ""))
            if v["ict"] == "n":
                coer = "s" if not in_lista(co) else "n"
            elif es in ("mancante", "fuori-lista"):
                coer = "n"
            else:
                coer = "s" if any(pulito(co).startswith(x.strip()[:2]) for x in prop.replace("xxxxxx", "").replace("xxxxx", "").replace("xxxx", "").split("/")) else "parziale"
            if v["servizio"] == "cloud" and coer == "s" and not any(pulito(co).startswith(x) for x in ("72416", "72415", "72317", "7241", "7240")): coer = "parziale"
            cnt[(v["servizio"], coer)] += 1
            w.writerow([cig, co, es, v["servizio"], v["cloud"], prop, coer, nota])
    out["D_riclassificazione"] = {"file": str(p.relative_to(R)), "per_servizio_coerenza": {f"{a}|{b}": n for (a, b), n in sorted(cnt.items())}}


def main():
    c = conn(); out = {"generato": str(datetime.date.today()), "versione_lista": WL["versione"], "versione_imbuto": imbuto.VERSIONE_IMBUTO}
    v3, info = parte_a(c, out); print("A ok", flush=True)
    parte_d(v3, info, out); print("D ok", flush=True)
    parte_c(c, out); print("C ok", flush=True)
    parte_b(c, out); print("B ok", flush=True)
    o = R / "esiti" / str(datetime.date.today()) / "cpv"; o.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(o / "rapporto-cpv.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(out, ensure_ascii=False)[:12000])


if __name__ == "__main__":
    main()
