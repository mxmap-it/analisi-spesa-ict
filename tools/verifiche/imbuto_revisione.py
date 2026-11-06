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
    pop = collections.Counter(strato_c(r) for r in T if strato_c(r))
    prec = []
    for s in ("T3-tondo", "T3-non-tondo", "T4-accordo-quadro", "T4-concessione"):
        g = [x for x in G if x["strato_campione"] == s]; k = sum(x["importo_non_spesa_pa"] == "si" for x in g)
        prec.append({"strato": s, "popolazione": pop[s], "campione": len(g), "confermati": k, "precisione": round(k / len(g), 3), "wilson95": wilson(k, len(g))})
    # controllo esaustivo T4 accordo quadro sul campo PVL accordo_quadro (dove l'avviso c'è)
    t4 = [P[r["cig"]]["aq_pvl"] for r in T if strato_c(r) == "T4-accordo-quadro" and r["cig"] in P and P[r["cig"]]["aq_pvl"] not in ("", "none")]
    k = sum("ccordo quadro" in a or a.startswith("fa-") for a in t4)
    pvl_t4 = {"con_campo_pvl": len(t4), "accordo_quadro_pvl": k, "precisione": round(k / len(t4), 3) if t4 else None, "wilson95": wilson(k, len(t4))}
    # regole v2
    out = []
    for r in T:
        r = dict(r); imp = float(r["importo"]); p = P.get(r["cig"], {}); aq = p.get("aq_pvl", "")
        if r["via"] == "T3-ripetuto" and round(imp) % 100000 == 0 and "DISCENDENTE" not in r["modalita_realizzazione"].upper():
            r["classe"], r["via"], r["euro_netti"] = "incerto", "I5-tondo-non-confermato", imp
        if r["cig"] in REV:
            x = REV[r["cig"]]
            if x["tipo"] == "errore": r["classe"], r["via"], r["euro_netti"] = "errore-importo", "X1-errore", 0.0
            else: r["classe"], r["via"], r["euro_netti"] = "tetto", "T6-revisione", 0.0
        elif r["classe"] == "incerto":
            v = max([float(p[c]) for c in ("vincente_max", "affidamento_max") if p.get(c)] or [0])
            if "ccordo quadro" in aq or aq.startswith("fa-"): r["classe"], r["via"], r["euro_netti"] = "tetto", "T5-pvl-aq", 0.0
            elif "Nulla" in aq and 0 < v < imp * 0.999: r["classe"], r["via"], r["euro_netti"] = "spesa-effettiva", "E2-pvl", v
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
    Rj["s3_s6"] = {k: sum(x[k] for x in ict) for k in ("euro_prima", "euro_dopo", "di_cui_incerti_oltre_50M")}
    with open(os.path.join(E, "tetti-cig-v2.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
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
