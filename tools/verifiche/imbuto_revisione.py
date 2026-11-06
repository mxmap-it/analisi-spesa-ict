"""Verifica «Imbuto: revisione dei tetti» (#66, rendiconto 0.3): misura la precisione delle regole T3 e T4 di
imbuto_tetti.py su un campione stratificato giudicato sugli atti, poi applica le regole v2 e ricalcola gli strati.

Ingressi versionati (esiti/2026-11-06/imbuto/):
  tetti-cig.csv                 classi v1 (imbuto_tetti.py)
  campione-tetti.csv            campione stratificato, 15 per strato, seme 20261106 (T3 tondo / T3 non tondo /
                                T4 accordo quadro / T4 concessione); estratto con --campione
  campione-tetti-giudizi.csv    giudizio sugli atti: oggetto ANAC + avviso PVL (campo accordo_quadro, descrizione,
                                valore aggiudicato). «si» = l'importo dichiarato non è spesa della PA per quel CIG
  pvl-percig.csv                dagli avvisi PVL (API ANAC, scaricati il 4/11) per ognuno dei 2.130 CIG: schede,
                                campo accordo_quadro, valore stimato, valore dell'offerta vincente, valore di affidamento
  revisione-incerti-ict.csv     revisione una per una dei CIG ICT incerti: errori d'importo evidenti e lotti ripetuti

Regole v2 (a valle del campione):
  T3 vale solo se l'importo non è tondo (non è un multiplo di 100.000 €) oppure se la modalità è «discendente da
     AQ/convenzione»: tondo e non discendente -> incerto (I5). Nel campione i CIG tondi confermati sono tutti adesioni.
  T5-pvl-aq       incerto con PVL «Accordo quadro» -> tetto
  E2-pvl          incerto con PVL accordo_quadro «Nulla» e offerta vincente/affidamento > 0 e < importo dichiarato
                  -> spesa effettiva, euro = valore PVL
  T6-revisione    tetto dalla revisione a mano (lotto ripetuto, valore di convenzione)
  X1-errore       errore d'importo evidente dalla revisione a mano -> fuori dai totali (né spesa né tetto)
Uso:  python tools/verifiche/imbuto_revisione.py [--json OUT]
      python tools/verifiche/imbuto_revisione.py --campione   # SUL SERVER: rifà l'estrazione del campione
"""
import csv, collections, json, math, os, random, sys

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.normpath(os.path.join(QUI, "..", ".."))
E = os.path.join(RADICE, "esiti/2026-11-06/imbuto")
RIEP = os.path.join(RADICE, "esiti/2026-11-03/imbuto/riepilogo-0.3.1.json")
RX_PA_PAGA = __import__("re").compile(r"energ|termic|efficient|trigenera|cogenera|calore|illuminazion|trasporto pubblico|\btpl\b|infrastruttura tecnologica|centro (unico )?di cottura", __import__("re").I)
leggi = lambda n: list(csv.DictReader(open(os.path.join(E, n), encoding="utf-8")))


def strato_c(r):
    if r["via"] == "T3-ripetuto": return "T3-tondo" if round(float(r["importo"])) % 100000 == 0 else "T3-non-tondo"
    if r["via"] == "T4-modalita": return "T4-concessione" if "CONCESSIONE" in r["modalita_realizzazione"] else "T4-accordo-quadro"


def wilson(k, n, z=1.96):
    if not n: return None, None
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return round(c - h, 3), round(c + h, 3)


def main():
    T = leggi("tetti-cig.csv")
    if "--campione" in sys.argv:
        rnd = random.Random(20261106)
        for s in ("T3-tondo", "T3-non-tondo", "T4-accordo-quadro", "T4-concessione"):
            pop = sorted([r for r in T if strato_c(r) == s], key=lambda r: r["cig"])
            print(s, len(pop), [r["cig"] for r in rnd.sample(pop, min(15, len(pop)))])
        return
    G = leggi("campione-tetti-giudizi.csv"); P = {r["cig"]: r for r in leggi("pvl-percig.csv")}
    REV = {r["cig"]: r for r in leggi("revisione-incerti-ict.csv")}
    QE = {r["cig"]: r for r in leggi("anac-qe-sal.csv")}
    pop = collections.Counter(strato_c(r) for r in T if strato_c(r))
    prec = []
    for s in ("T3-tondo", "T3-non-tondo", "T4-accordo-quadro", "T4-concessione"):
        g = [x for x in G if x["strato_campione"] == s]; k = sum(x["importo_non_spesa_pa"] == "si" for x in g)
        prec.append({"strato": s, "popolazione": pop[s], "campione": len(g), "confermati": k, "precisione": round(k / len(g), 3), "wilson95": wilson(k, len(g))})
    # precisione di T4 concessione dopo la regola v3 (sui CIG del campione che la regola lascia tetti)
    ogg = {r["cig"]: r["oggetto"] for r in T}
    g = [x for x in G if x["strato_campione"] == "T4-concessione" and not RX_PA_PAGA.search(ogg.get(x["cig"], ""))]
    k = sum(x["importo_non_spesa_pa"] == "si" for x in g)
    prec.append({"strato": "T4-concessione dopo regola v3 (I6)", "campione": len(g), "confermati": k, "precisione": round(k / len(g), 3) if g else None, "wilson95": wilson(k, len(g))})
    # controllo esaustivo T4 accordo quadro sul campo PVL accordo_quadro (dove l'avviso c'è)
    t4 = [P[r["cig"]]["aq_pvl"] for r in T if strato_c(r) == "T4-accordo-quadro" and r["cig"] in P and P[r["cig"]]["aq_pvl"] not in ("", "none")]
    k = sum("ccordo quadro" in a or a.startswith("fa-") for a in t4)
    pvl_t4 = {"con_campo_pvl": len(t4), "accordo_quadro_pvl": k, "precisione": round(k / len(t4), 3) if t4 else None, "wilson95": wilson(k, len(t4))}
    # regole v2
    out = []
    for r in T:
        r = dict(r, sal_cumulato=""); imp = float(r["importo"]); p = P.get(r["cig"], {}); aq = p.get("aq_pvl", "")
        if r["via"] == "T3-ripetuto" and round(imp) % 100000 == 0 and "DISCENDENTE" not in r["modalita_realizzazione"].upper():
            r["classe"], r["via"], r["euro_netti"] = "incerto", "I5-tondo-non-confermato", imp
        # v3 (0.4): concessione con servizi energetici, impianti o TPL -> i canoni li paga di norma la PA: incerto
        if r["via"] == "T4-modalita" and "CONCESSIONE" in r["modalita_realizzazione"] and RX_PA_PAGA.search(r["oggetto"]):
            r["classe"], r["via"], r["euro_netti"] = "incerto", "I6-concessione-canoni-pa", imp
        if r["cig"] in REV:
            x = REV[r["cig"]]
            if x["tipo"] == "errore": r["classe"], r["via"], r["euro_netti"] = "errore-importo", "X1-errore", 0.0
            elif x["tipo"] == "spesa": r["classe"], r["via"], r["euro_netti"] = "spesa-effettiva", "E3-atto", float(x["euro_ordinativo"])
            elif x["tipo"] == "incerto": r["classe"], r["via"], r["euro_netti"] = "incerto", "I7-atto-non-risolutivo", imp
            else: r["classe"], r["via"], r["euro_netti"] = "tetto", "T6-revisione", 0.0
        elif r["classe"] == "incerto":
            v = max([float(p[c]) for c in ("vincente_max", "affidamento_max") if p.get(c)] or [0])
            if "ccordo quadro" in aq or aq.startswith("fa-"): r["classe"], r["via"], r["euro_netti"] = "tetto", "T5-pvl-aq", 0.0
            elif "Nulla" in aq and 0 < v < imp * 0.999: r["classe"], r["via"], r["euro_netti"] = "spesa-effettiva", "E2-pvl", v
        # v3 (0.4): quadro economico ANAC (seconda fonte ANAC, imbuto_qe_sal.py). Per un incerto o un errore d'importo
        # con QE > 0 e < metà dell'importo dichiarato vale il QE; il SAL cumulato si riporta come speso certificato
        q = QE.get(r["cig"])
        if q:
            qv = float(q["qe_ultimo_importo"] or 0); r["sal_cumulato"] = q["sal_cumulato"]
            if r["classe"] in ("incerto", "errore-importo") and 0 < qv < imp * 0.5:
                r["classe"], r["via"], r["euro_netti"] = "spesa-effettiva", ("E4-qe-corregge-errore" if r["classe"] == "errore-importo" else "E4-qe"), qv
        out.append(r)
    agg = lambda f: sorted(((k, v) for k, v in _agg(out, f).items()), key=lambda x: str(x[0]))
    Rj = {"precisione_campione": prec, "t4_accordo_quadro_su_pvl": pvl_t4}
    Rj["per_classe_v2"] = [{"chiave": k, "cig": v[0], "euro_dichiarati": round(v[1]), "euro_netti": round(v[2])} for k, v in agg(lambda r: r["classe"])]
    Rj["per_via_v2"] = [{"chiave": k, "cig": v[0], "euro_dichiarati": round(v[1]), "euro_netti": round(v[2])} for k, v in agg(lambda r: (r["classe"], r["via"]))]
    Rj["ict_per_classe_v2"] = [{"chiave": k, "cig": v[0], "euro_dichiarati": round(v[1]), "euro_netti": round(v[2])}
                               for k, v in agg(lambda r: r["classe"] if r["strato"] != "S1-escluso-non-ict" else None) if k]
    P0 = json.load(open(RIEP, encoding="utf-8")); st = collections.defaultdict(float)
    for r in P0["righe"]:
        if int(r["anno"]) >= 2024: st[r["strato"]] += r["euro"] or 0
    corr = collections.defaultdict(lambda: [0.0, 0.0, 0.0])
    for r in out:
        c = corr[r["strato"]]; c[0] += float(r["importo"]); c[1] += float(r["euro_netti"])
        if r["classe"] == "incerto": c[2] += float(r["importo"])
    Rj["strati_dal_2024_v2"] = [{"strato": s, "euro_prima": round(v), "euro_dopo": round(v - corr[s][0] + corr[s][1]), "di_cui_incerti_oltre_50M": round(corr[s][2])}
                                for s, v in sorted(st.items()) if s not in ("S0-padre-aq", "S2-sotto-soglia")]
    ict = [x for x in Rj["strati_dal_2024_v2"] if x["strato"] != "S1-escluso-non-ict"]
    Rj["sal_certificato"] = {"cig_con_sal": sum(1 for r in out if r["sal_cumulato"] and float(r["sal_cumulato"]) > 0),
                             "euro_sal": round(sum(float(r["sal_cumulato"] or 0) for r in out)),
                             "euro_sal_ict": round(sum(float(r["sal_cumulato"] or 0) for r in out if r["strato"] != "S1-escluso-non-ict"))}
    Rj["s3_s6"] ={k: sum(x[k] for x in ict) for k in ("euro_prima", "euro_dopo", "di_cui_incerti_oltre_50M")}
    with open(os.path.join(E, "tetti-cig-v2.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
    # precisione di E4 (0.5): campione casuale di 15 CIG E4 (seme 20261108) giudicato sul testo; e rapporti potenza di 10
    if os.path.exists(os.path.join(E, "campione-e4-giudizi.csv")):
        g = leggi("campione-e4-giudizi.csv"); e4 = [r for r in out if r["via"].startswith("E4")]
        a = sum(x["dichiarato_errato"] == "si" for x in g); b = sum(x["qe_plausibile"] == "si" for x in g)
        pw = sum(1 for r in e4 if float(r["euro_netti"]) > 0 and abs(math.log10(float(r["importo"]) / float(r["euro_netti"])) - round(math.log10(float(r["importo"]) / float(r["euro_netti"])))) < 0.005)
        Rj["precisione_e4"] = {"cig_e4": len(e4), "campione": len(g), "dichiarato_errato": a, "wilson95_dichiarato_errato": wilson(a, len(g)),
                               "qe_plausibile": b, "wilson95_qe_plausibile": wilson(b, len(g)), "rapporto_esatto_potenza_di_10": pw}
    print(json.dumps(Rj, ensure_ascii=False, indent=1, default=str))
    if "--json" in sys.argv: json.dump(Rj, open(sys.argv[sys.argv.index("--json") + 1], "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)


def _agg(out, f):
    a = collections.defaultdict(lambda: [0, 0.0, 0.0])
    for r in out:
        k = f(r)
        if isinstance(k, tuple): k = " / ".join(k)
        x = a[k]; x[0] += 1; x[1] += float(r["importo"]); x[2] += float(r["euro_netti"])
    return a


if __name__ == "__main__":
    main()
