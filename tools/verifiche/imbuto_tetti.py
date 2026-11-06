"""Verifica «Imbuto: tetti o spesa?» (#66, top-5 punto 2): classifica ogni CIG dal 2024 con importo >= 50 M€
(«importo da verificare» di imbuto-0.3.1, esclusi i padri S0) come TETTO (massimale di accordo quadro/convenzione,
valore di concessione copiato), SPESA EFFETTIVA (valore contrattuale aggiudicato di un appalto singolo), ANNULLATO
o INCERTO, registrando per ciascuno la via che lo ha deciso; poi ricalcola strati ed euro al netto.

Vie, in ordine (la prima che scatta decide):
  T1-padre-copiato   CIG derivato (cig_accordo_quadro) con importo uguale (±1 %) a quello del CIG padre        -> tetto
  T2-oltre-ordinato  CIG derivato di un'iniziativa Consip con importo > ordinato Consip 2024-2026 dell'intera
                     iniziativa (open data dati.consip.it, report/convenzioni/database/iniziative.json)          -> tetto
  T3-ripetuto        stesso importo (all'euro) in >= 3 CIG di stazioni appaltanti diverse                        -> tetto
  T4-modalita        modalita_realizzazione ANAC = «ACCORDO QUADRO» o contratto di concessione (non discendente):
                     il valore è un massimale o il valore pluriennale della concessione, non spesa della PA   -> tetto
  A1-cancellato      CIG con motivo di cancellazione ANAC                                                         -> annullato
  E1-aggiudicato     contratto d'appalto senza AQ, esito aggiudicata, importo di aggiudicazione > 0              -> spesa
                     effettiva (euro = importo di aggiudicazione; è un impegno contrattuale, non un pagamento)
  I*                 tutto il resto -> incerto (I1 derivato di AQ (campo o modalità) senza riscontro, I2 testo con AQ/convenzione/
                     massimale, I3 senza aggiudicazione)

Uso:
  python tools/verifiche/imbuto_tetti.py            # da un clone: legge esiti/2026-11-06/imbuto/tetti-cig.csv, stampa e controlla
  python tools/verifiche/imbuto_tetti.py --rigenera # SUL SERVER (nice): rilegge il mirror ANAC e ict.csv, riscrive tetti-cig.csv
  ... --json OUT                                     # tabelle in JSON per il rendiconto
"""
import csv, collections, glob, hashlib, io, json, os, re, sys, zipfile

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.normpath(os.path.join(QUI, "..", ".."))
ESITI = os.path.join(RADICE, "esiti/2026-11-06/imbuto")
OUT = os.path.join(ESITI, "tetti-cig.csv")
ICT = os.path.join(RADICE, "lavoro/imbuto/ict.csv")
INIZ = os.path.join(RADICE, "report/convenzioni/database/iniziative.json")
YAML_INIZ = os.path.join(RADICE, "config/iniziative_ict.yaml")
RIEP = os.path.join(RADICE, "esiti/2026-11-03/imbuto/riepilogo-0.3.1.json")
SOGLIA = 50e6
RX_TESTO = re.compile(r"accordo\s+quadro|convenzion|massimal|concession|\bpsn\b|polo\s+strategico", re.I)
CAMPI = ["cig", "anno", "strato", "sottoclasse", "gruppo", "importo", "classe", "via", "euro_netti", "cig_accordo_quadro",
         "importo_padre", "importo_aggiudicazione", "modalita_realizzazione", "tipo_scelta_contraente", "esito",
         "stazione_appaltante", "oggetto"]


def rigenera():
    os.chdir(RADICE)
    sys.path.insert(0, os.path.join(RADICE, "tools/analisi"))
    from attribuisci_provider import righe_cig, D
    import yaml
    # 1) strato da ict.csv (chi non c'è è S1 o S2-non-ict)
    strato = {}
    with open(ICT, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if float(r["importo"] or 0) >= SOGLIA * 0.9 or r["strato"] == "S0-padre-aq":
                strato[r["cig"]] = (r["strato"], r["sottoclasse"], r["gruppo"])
    # 2) mirror ANAC: tutte le righe >= 45 M€ (candidati e possibili padri), ultima versione (delta vince)
    grandi = {}
    fonti = sorted({p.rstrip("/").split("cig-")[-1] for p in glob.glob(D + "cig-20*/")}) + ["delta"]
    for fo in fonti:
        if fo != "delta" and int(fo) < 2012: continue
        for r in righe_cig(fo):
            try: imp = float(r["importo_lotto"] or 0)
            except ValueError: continue
            if imp >= SOGLIA * 0.9: grandi[r["cig"]] = r
        print("letto", fo, len(grandi), flush=True)
    cand = {c: r for c, r in grandi.items() if (r.get("anno_pubblicazione") or "") >= "2024"
            and float(r["importo_lotto"]) >= SOGLIA and strato.get(c, ("",))[0] != "S0-padre-aq"}
    # 3) aggiudicazioni (mirror, ultimo file)
    agg = {}
    z = sorted(glob.glob(D + "aggiudicazioni/filesystem/*-aggiudicazioni_csv.zip"))[-1]
    zf = zipfile.ZipFile(z); m = next(i for i in zf.namelist() if i.endswith(".csv"))
    for r in csv.DictReader(io.TextIOWrapper(zf.open(m), encoding="utf-8-sig", errors="replace"), delimiter=";"):
        if r["cig"] in cand:
            try: agg[r["cig"]] = max(agg.get(r["cig"], 0.0), float(r["importo_aggiudicazione"] or 0))
            except ValueError: pass
    # 4) ordinato Consip per CIG padre
    ini = {i["nome"]: i for i in json.load(open(INIZ, encoding="utf-8"))}
    ordinato = {}
    for e in yaml.safe_load(open(YAML_INIZ, encoding="utf-8")):
        o = (ini.get(e["iniziativa"]) or {}).get("ordinato_consip") or {}
        tot = sum(v for k, v in o.items() if k.isdigit())
        if tot: ordinato[e["cig"]] = tot
    # 5) importi ripetuti fra stazioni appaltanti diverse
    sa_per_imp = collections.defaultdict(set)
    for c, r in cand.items(): sa_per_imp[round(float(r["importo_lotto"]))].add(r["cf_amministrazione_appaltante"])
    righe = []
    for c, r in sorted(cand.items()):
        imp = float(r["importo_lotto"]); aq = r["cig_accordo_quadro"]
        ip = float(grandi[aq]["importo_lotto"]) if aq in grandi else None
        mod = (r["modalita_realizzazione"] or "").upper(); ia = agg.get(c)
        testo = (r["oggetto_lotto"] or "") + " | " + (r["oggetto_gara"] or "")
        if aq and ip and abs(imp - ip) <= 0.01 * ip: k, v = "tetto", "T1-padre-copiato"
        elif aq and aq in ordinato and imp > ordinato[aq]: k, v = "tetto", "T2-oltre-ordinato"
        elif len(sa_per_imp[round(imp)]) >= 3: k, v = "tetto", "T3-ripetuto"
        elif "DISCENDENTE" not in mod and (mod == "ACCORDO QUADRO" or mod.startswith("CONTRATTO DI CONCESSIONE")): k, v = "tetto", "T4-modalita"
        elif r.get("COD_MOTIVO_CANCELLAZIONE"): k, v = "annullato", "A1-cancellato"
        elif not aq and "APPALTO" in mod and "AGGIUDICAT" in (r.get("ESITO") or "").upper() and ia: k, v = "spesa-effettiva", "E1-aggiudicato"
        elif aq or "DISCENDENTE" in mod: k, v = "incerto", "I1-derivato-senza-riscontro"
        elif RX_TESTO.search(testo): k, v = "incerto", "I2-testo-aq-convenzione"
        else: k, v = "incerto", "I3-senza-aggiudicazione"
        netti = 0.0 if k in ("tetto", "annullato") else (min(ia, imp) if k == "spesa-effettiva" else imp)
        s = strato.get(c, ("S1-escluso-non-ict", "", ""))
        righe.append([c, r["anno_pubblicazione"], *s, round(imp, 2), k, v, round(netti, 2), aq, ip or "", ia or "",
                      r["modalita_realizzazione"], r["tipo_scelta_contraente"], r.get("ESITO", ""),
                      r["denominazione_amministrazione_appaltante"], testo[:200]])
    os.makedirs(ESITI, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(CAMPI); w.writerows(righe)
    json.dump({"fonte_ict": "lavoro/imbuto/ict.csv", "sha256_ict": hashlib.sha256(open(ICT, "rb").read()).hexdigest(),
               "aggiudicazioni": os.path.relpath(z, RADICE), "candidati": len(righe)},
              open(os.path.join(ESITI, "tetti-fonti.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("scritto", OUT, len(righe))


def main():
    if "--rigenera" in sys.argv: return rigenera()
    R = list(csv.DictReader(open(OUT, encoding="utf-8")))
    fmt = lambda x: f"{x / 1e9:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    T = {"cig": len(R), "euro_dichiarati": round(sum(float(r["importo"]) for r in R)),
         "euro_netti": round(sum(float(r["euro_netti"]) for r in R))}
    for chiave, f in (("per_classe", lambda r: r["classe"]), ("per_via", lambda r: (r["classe"], r["via"])),
                      ("per_strato_classe", lambda r: (r["strato"], r["classe"]))):
        a = collections.defaultdict(lambda: [0, 0.0, 0.0])
        for r in R:
            x = a[f(r)]; x[0] += 1; x[1] += float(r["importo"]); x[2] += float(r["euro_netti"])
        T[chiave] = [{"chiave": k, "cig": v[0], "euro_dichiarati": round(v[1]), "euro_netti": round(v[2])} for k, v in sorted(a.items())]
    # ricalcolo degli strati dal 2024: euro dichiarati - (dichiarati dei 2.160) + netti
    P = json.load(open(RIEP, encoding="utf-8"))
    st = collections.defaultdict(lambda: [0, 0.0])
    for r in P["righe"]:
        if int(r["anno"]) >= 2024: st[r["strato"]][0] += r["cig"]; st[r["strato"]][1] += r["euro"] or 0
    corr = collections.defaultdict(lambda: [0.0, 0.0, 0.0])
    for r in R:
        c = corr[r["strato"]]; c[0] += float(r["importo"]); c[1] += float(r["euro_netti"])
        if r["classe"] == "incerto": c[2] += float(r["importo"])
    T["strati_dal_2024"] = [{"strato": s, "cig": v[0], "euro_prima": round(v[1]), "euro_dopo": round(v[1] - corr[s][0] + corr[s][1]),
                             "di_cui_incerti_oltre_50M": round(corr[s][2])} for s, v in sorted(st.items())]
    print(f"CIG da verificare: {T['cig']}  euro dichiarati {fmt(T['euro_dichiarati'])} mld -> netti {fmt(T['euro_netti'])} mld")
    for sez in ("per_classe", "per_via", "per_strato_classe"):
        print("\n##", sez)
        for x in T[sez]: print(x["chiave"], "|", x["cig"], "CIG |", fmt(x["euro_dichiarati"]), "->", fmt(x["euro_netti"]), "mld")
    print("\n## strati dal 2024 (mld): prima -> dopo (incerti > 50 M€ ancora dentro)")
    for x in T["strati_dal_2024"]: print(x["strato"], x["cig"], fmt(x["euro_prima"]), "->", fmt(x["euro_dopo"]), "| incerti", fmt(x["di_cui_incerti_oltre_50M"]))
    # coerenza con imbuto-0.3.1: 2.160 CIG da verificare dal 2024
    attesi = sum(r["cig"] for r in P["righe"] if int(r["anno"]) >= 2024 and r["importo_da_verificare"] and r["strato"] != "S0-padre-aq")
    # il riepilogo conta RIGHE: 30 righe sono CIG ripetuti nei file annuali ANAC (per la parte ict.csv: 167 righe = 162 CIG,
    # nessun CIG mancante, controllato il 6/11). Qui si contano CIG distinti.
    T["coerenza"] = {"righe_riepilogo": attesi, "cig_distinti": len(R), "righe_duplicate": attesi - len(R), "ok": 0 <= attesi - len(R) <= 30}
    print("\n## coerenza", T["coerenza"])
    if "--json" in sys.argv:
        json.dump(T, open(sys.argv[sys.argv.index("--json") + 1], "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)


if __name__ == "__main__":
    main()
