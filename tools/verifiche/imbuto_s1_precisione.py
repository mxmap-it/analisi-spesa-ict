"""Precisione dell'esclusione non ICT (strato S1 dell'imbuto 0.3.4, CIG pubblicati dal 2024) — #77, mancanza M5.

S1 = CIG con anno di pubblicazione >= 2024, importo >= 500 €, che l'imbuto non ha scritto in lavoro/imbuto/ict.csv
(ict.csv contiene tutti i CIG non esclusi in S1 o S2-non-ICT: S0 padri AQ, S2-ict, S3-S6). Si ricostruisce leggendo
le stesse fonti dell'imbuto (file annuali cig-2024, cig-2025 e aggiornamenti mensili, ultima versione di ogni CIG da
lavoro/imbuto-prova-0.3.4/base.duckdb, tabella delta), senza rifare la classificazione. Controllo: il conteggio deve
coincidere con il riepilogo 0.3.4 (3.209.583 CIG).

Campione (seme fisso SEME): strati per classe d'importo; dentro ogni classe si prendono i CIG con la chiave
sha256(SEME|cig) più piccola (campione casuale semplice senza reinserimento, riproducibile e in streaming).
Allocazione dei 400 casi: metà proporzionale al numero di CIG della classe, metà proporzionale agli euro
(sovracampionamento pesato per importo), minimo 20 per classe. Le stime usano i pesi N_h/n_h (per conteggio) e il
rapporto euro ICT/euro del campione per classe (per euro); l'intervallo è di Wilson con la dimensione efficace di Kish.

Uso (dalla radice):
  flock lavoro/pesante.lock nice -n 15 .venv/bin/python tools/verifiche/imbuto_s1_precisione.py estrai   # SUL SERVER
      -> esiti/2026-11-19/imbuto/s1-precisione/{popolazione.json, campione.csv}
  python tools/verifiche/imbuto_s1_precisione.py misura      # da un clone pulito: legge popolazione.json e
      report/metodo/imbuto/s1-campione-misura.csv (annotazioni a cieco di Claude) -> esiti/.../misura.json
  flock lavoro/pesante.lock nice -n 15 .venv/bin/python tools/verifiche/imbuto_s1_precisione.py classi    # SUL SERVER
      -> esiti/.../proposte.json: peso in S1 delle correzioni proposte (non applicate)
"""
import csv, collections, glob, hashlib, heapq, io, json, math, os, sys, zipfile

RADICE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
ESITI = os.path.join(RADICE, os.environ.get("S1_ESITI", "esiti/2026-11-19/imbuto/s1-precisione"))
ANNOT = os.path.join(RADICE, "report/metodo/imbuto/s1-campione-misura.csv")
D = os.path.join(RADICE, "archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/")
ICT = os.path.join(RADICE, "lavoro/imbuto/ict.csv")
BASE = os.path.join(RADICE, "lavoro/imbuto-prova-0.3.4/base.duckdb")
SEME = "spesaict-s1-2026-11-19"
N_TOT, N_MIN = 400, 20
CLASSI = [(500, 5e3), (5e3, 40e3), (40e3, 140e3), (140e3, 1e6), (1e6, 5e6), (5e6, float("inf"))]
ATTESO = 3209583  # CIG S1 dal 2024 nel riepilogo 0.3.4 (esiti/2026-11-18/imbuto/riepilogo-0.3.4.json)


def classe(imp):
    return next(i for i, (a, b) in enumerate(CLASSI) if a <= imp < b)


def chiave(cig):
    return hashlib.sha256(f"{SEME}|{cig}".encode()).hexdigest()


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


def estrai():
    import duckdb
    os.makedirs(ESITI, exist_ok=True)
    ict = set()
    with open(ICT, encoding="utf-8") as f:
        for r in csv.DictReader(f): ict.add(r["cig"])
    c = duckdb.connect(BASE, read_only=True)
    c.execute("SET memory_limit='4GB'; SET threads=2")
    delta = {r[0] for r in c.execute("SELECT cig FROM delta").fetchall()}
    KMAX = N_TOT  # per classe se ne tengono abbastanza per qualunque allocazione
    heaps = [[] for _ in CLASSI]; N = [0] * len(CLASSI); E = [0.0] * len(CLASSI)
    per_anno = collections.Counter()
    campi = ["cig", "anno_pubblicazione", "importo_lotto", "cod_cpv", "descrizione_cpv", "oggetto_principale_contratto",
             "tipo_scelta_contraente", "denominazione_amministrazione_appaltante", "oggetto_lotto", "oggetto_gara"]

    def considera(r):
        anno = (r.get("anno_pubblicazione") or "").strip()
        if not anno.isdigit() or int(anno) < 2024 or anno > "2026": return
        if r["cig"] in ict: return
        try: imp = float(r["importo_lotto"] or 0)
        except ValueError: imp = 0.0
        if imp < 500: return
        h = classe(imp); N[h] += 1; E[h] += imp; per_anno[anno] += 1
        k = chiave(r["cig"])
        voce = (-int(k[:15], 16), r["cig"], {x: (r.get(x) or "") for x in campi})
        if len(heaps[h]) < KMAX: heapq.heappush(heaps[h], voce)
        elif voce[0] > heaps[h][0][0]: heapq.heapreplace(heaps[h], voce)

    fonti = []
    for anno in ("2024", "2025"):
        for z in sorted(glob.glob(D + f"cig-{anno}/filesystem/cig_csv_*.zip")):
            fonti.append(os.path.relpath(z, RADICE))
        visti = set()
        for z in sorted(glob.glob(D + f"cig-{anno}/filesystem/cig_csv_*.zip")):
            zf = zipfile.ZipFile(z)
            for r in csv.DictReader(io.TextIOWrapper(zf.open(zf.namelist()[0]), encoding="utf-8-sig", errors="replace"), delimiter=";"):
                if r["cig"] in delta or r["cig"] in visti: continue
                visti.add(r["cig"]); considera(r)
        print(anno, N, flush=True)
    q = c.execute("SELECT * FROM delta"); cols = [d[0] for d in q.description]
    for b in iter(lambda: q.fetchmany(50000), []):
        for t in b: considera({k: (x or "") for k, x in zip(cols, t)})
    print("delta", N, flush=True)
    # allocazione: metà per numero, metà per euro, minimo N_MIN
    nt, et = sum(N), sum(E)
    alloc = [max(N_MIN, round(N_TOT / 2 * N[h] / nt + N_TOT / 2 * E[h] / et)) for h in range(len(CLASSI))]
    while sum(alloc) > N_TOT:  # riporta a N_TOT togliendo dalla classe più grande
        alloc[alloc.index(max(alloc))] -= 1
    camp = []
    for h in range(len(CLASSI)):
        scelti = sorted(heaps[h], key=lambda v: -v[0])[:alloc[h]]  # chiavi più piccole
        for _, cig, r in scelti: camp.append(dict(r, classe=h))
    # aggiudicatari del campione (solo per l'annotazione)
    agg = dict(c.execute("SELECT cig, nomi FROM agg WHERE cig IN (SELECT unnest($1::VARCHAR[]))", [[x["cig"] for x in camp]]).fetchall())
    camp.sort(key=lambda x: chiave(x["cig"]))  # ordine casuale: l'annotatore non vede la classe in blocco
    with open(os.path.join(ESITI, "campione.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["cig", "anno", "classe", "importo", "cod_cpv", "descrizione_cpv", "tipo", "procedura", "stazione_appaltante",
                    "aggiudicatari", "oggetto_lotto", "oggetto_gara"])
        for x in camp:
            w.writerow([x["cig"], x["anno_pubblicazione"], x["classe"], x["importo_lotto"], x["cod_cpv"], x["descrizione_cpv"],
                        x["oggetto_principale_contratto"], x["tipo_scelta_contraente"], x["denominazione_amministrazione_appaltante"],
                        " ; ".join(sorted(n for n in agg.get(x["cig"], []) if n)), x["oggetto_lotto"][:500], x["oggetto_gara"][:500]])
    pop = {"seme": SEME, "classi_euro": [[a, b if b != float("inf") else None] for a, b in CLASSI],
           "N": N, "euro": [round(e) for e in E], "allocazione": alloc, "cig_totale": nt, "euro_totale": round(et),
           "per_anno": dict(per_anno), "atteso_riepilogo_034": ATTESO, "coerente": nt == ATTESO,
           "ict_csv_sha256": sha(ICT), "fonti": fonti + ["delta: lavoro/imbuto-prova-0.3.4/base.duckdb (tabella delta)"]}
    json.dump(pop, open(os.path.join(ESITI, "popolazione.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(pop, ensure_ascii=False, indent=1))


# Proposte di correzione emerse dal campione (#77): quanto pesano in S1. NON cambiano l'imbuto (si decide per livelli).
import re
PROPOSTE = {
    "P1-cpv-503-assistenza-pc-tlc": lambda cpv, t: cpv.startswith("503") and not cpv.startswith(("50312", "50320")),
    "P2-cpv-64221-interconnessione": lambda cpv, t: cpv.startswith("64221"),
    "P3-cpv-3255-centralini-telefonia": lambda cpv, t: cpv.startswith("3255"),
    "P4-testo-pc-postazioni": lambda cpv, t: bool(re.search(r"\bpc\b|\bportatil[ie]\b|postazion[ei]\s+(di\s+)?lavoro|fleet\s+management|\btablet\b", t, re.I)),
    "P5-testo-ot-iot": lambda cpv, t: bool(re.search(r"\biiot\b|\biot\b|\bscada\b|telecontroll\w*|telemetri\w*", t, re.I)),
    "X-cpv-642-telefonia (fuori perimetro per scelta)": lambda cpv, t: cpv.startswith("642") and not cpv.startswith(("64216", "64222")),
}


def righe_s1():
    """Stessa lettura di estrai(): (riga, importo) per ogni CIG di S1."""
    import duckdb
    ict = set()
    with open(ICT, encoding="utf-8") as f:
        for r in csv.DictReader(f): ict.add(r["cig"])
    c = duckdb.connect(BASE, read_only=True); c.execute("SET memory_limit='4GB'; SET threads=2")
    delta = {r[0] for r in c.execute("SELECT cig FROM delta").fetchall()}

    def filtro(r):
        anno = (r.get("anno_pubblicazione") or "").strip()
        if not anno.isdigit() or int(anno) < 2024 or anno > "2026" or r["cig"] in ict: return None
        try: imp = float(r["importo_lotto"] or 0)
        except ValueError: imp = 0.0
        return imp if imp >= 500 else None
    for anno in ("2024", "2025"):
        visti = set()
        for z in sorted(glob.glob(D + f"cig-{anno}/filesystem/cig_csv_*.zip")):
            zf = zipfile.ZipFile(z)
            for r in csv.DictReader(io.TextIOWrapper(zf.open(zf.namelist()[0]), encoding="utf-8-sig", errors="replace"), delimiter=";"):
                if r["cig"] in delta or r["cig"] in visti: continue
                visti.add(r["cig"])
                if (imp := filtro(r)) is not None: yield r, imp
    q = c.execute("SELECT * FROM delta"); cols = [d[0] for d in q.description]
    for b in iter(lambda: q.fetchmany(50000), []):
        for t in b:
            r = {k: (x or "") for k, x in zip(cols, t)}
            if (imp := filtro(r)) is not None: yield r, imp


def classi():
    tot = collections.defaultdict(lambda: [0, 0.0]); es = collections.defaultdict(list); n = 0
    for r, imp in righe_s1():
        n += 1
        cpv, t = r["cod_cpv"] or "", (r["oggetto_lotto"] or "") + " | " + (r["oggetto_gara"] or "")
        for k, f in PROPOSTE.items():
            if f(cpv, t):
                tot[k][0] += 1; tot[k][1] += imp
                kk = chiave(r["cig"])
                es[k].append((kk, r["cig"], cpv, round(imp), r["denominazione_amministrazione_appaltante"][:60], t[:200]))
                if len(es[k]) > 200: es[k] = sorted(es[k])[:20]
    out = {"cig_s1_letti": n, "nota": "conteggi su tutto S1 dal 2024; esempi = 20 CIG casuali (chiave sha256 col seme) per proposta",
           "proposte": {k: {"cig": v[0], "euro": round(v[1]), "esempi": [list(x[1:]) for x in sorted(es[k])[:20]]} for k, v in tot.items()}}
    json.dump(out, open(os.path.join(ESITI, "proposte.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v["cig"] for k, v in out["proposte"].items()}, ensure_ascii=False), n)


def wilson(p, n, z=1.96):
    if not n: return None
    d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(max(p * (1 - p), 0) / n + z * z / (4 * n * n)) / d
    return [max(0.0, c - h), min(1.0, c + h)]


def misura():
    pop = json.load(open(os.path.join(ESITI, "popolazione.json"), encoding="utf-8"))
    camp = {r["cig"]: r for r in csv.DictReader(open(os.path.join(ESITI, "campione.csv"), encoding="utf-8"))}
    ann = list(csv.DictReader(open(ANNOT, encoding="utf-8")))
    assert {a["cig"] for a in ann} == set(camp), "annotazioni e campione non coincidono"
    H = len(pop["N"])
    per = [collections.defaultdict(float) for _ in range(H)]
    classi_err = collections.Counter(); esempi = collections.defaultdict(list)
    for a in ann:
        h = int(camp[a["cig"]]["classe"]); imp = float(camp[a["cig"]]["importo"])
        g = a["giudizio"]; assert g in ("non-ict", "ict", "dubbio"), g
        per[h]["n"] += 1; per[h]["eur"] += imp
        per[h][g] += 1; per[h]["eur_" + g] += imp
        if g == "ict" and a.get("cloud_potenziale") == "si": per[h]["cloud"] += 1; per[h]["eur_cloud"] += imp
        if g != "non-ict":
            classi_err[(g, a.get("classe_errore") or "")] += 1
            esempi[a.get("classe_errore") or ""].append(a["cig"])
    W = [pop["N"][h] / sum(pop["N"]) for h in range(H)]

    def stima(chi):
        """Quota di CIG (pesata N_h) e di euro (rapporto per classe, pesata E_h) giudicati `chi`; Wilson con n efficace di Kish."""
        p = sum(W[h] * per[h][chi] / per[h]["n"] for h in range(H) if per[h]["n"])
        pesi = [pop["N"][h] / per[h]["n"] for h in range(H) if per[h]["n"]]
        ns = [per[h]["n"] for h in range(H) if per[h]["n"]]
        n_eff = sum(w * k for w, k in zip(pesi, ns)) ** 2 / sum(w * w * k for w, k in zip(pesi, ns))
        Et = sum(pop["euro"])
        pe = sum(pop["euro"][h] / Et * per[h]["eur_" + chi] / per[h]["eur"] for h in range(H) if per[h]["eur"])
        pesi_e = [pop["euro"][h] / per[h]["n"] for h in range(H) if per[h]["n"]]
        ne_eff = sum(w * k for w, k in zip(pesi_e, ns)) ** 2 / sum(w * w * k for w, k in zip(pesi_e, ns))
        wi, we = wilson(p, n_eff), wilson(pe, ne_eff)
        return {"quota_cig": round(p, 5), "wilson95_cig": [round(x, 5) for x in wi], "n_eff_cig": round(n_eff, 1),
                "cig_stimati": round(p * sum(pop["N"])), "cig_intervallo": [round(x * sum(pop["N"])) for x in wi],
                "quota_euro": round(pe, 5), "wilson95_euro": [round(x, 5) for x in we], "n_eff_euro": round(ne_eff, 1),
                "euro_stimati": round(pe * Et), "euro_intervallo": [round(x * Et) for x in we]}

    ris = {"popolazione": {k: pop[k] for k in ("cig_totale", "euro_totale", "N", "euro", "allocazione", "coerente", "seme")},
           "annotazioni": os.path.relpath(ANNOT, RADICE), "annotatore": "Claude (a cieco, decisione di Fabio del 19/11/2026)",
           "per_classe": [{"classe": pop["classi_euro"][h], **{k: round(v, 2) for k, v in per[h].items()}} for h in range(H)],
           "ict": stima("ict"), "dubbio": stima("dubbio"),
           "precisione_esclusione": None, "classi_errore": [{"giudizio": g, "classe": c, "n": n, "cig": esempi[c][:10]} for (g, c), n in classi_err.most_common()]}
    for h in range(H): per[h]["ict_o_dubbio"] = per[h]["ict"] + per[h]["dubbio"]; per[h]["eur_ict_o_dubbio"] = per[h]["eur_ict"] + per[h]["eur_dubbio"]
    ris["ict_o_dubbio"] = stima("ict_o_dubbio"); ris["cloud_potenziale"] = stima("cloud")
    # stimatore per espansione (Horvitz-Thompson stratificato) degli euro ICT persi: somma N_h * media del campione,
    # con intervallo normale al 95 % (varianza stratificata). Il rapporto per classe (sopra) pesa meno gli importi anomali.
    camp_imp = collections.defaultdict(list)
    for a in ann:
        h = int(camp[a["cig"]]["classe"]); imp = float(camp[a["cig"]]["importo"])
        camp_imp[h].append((imp if a["giudizio"] == "ict" else 0.0, imp if a["giudizio"] != "non-ict" else 0.0))
    for j, nome in ((0, "ict"), (1, "ict_o_dubbio")):
        tot = var = 0.0
        for h, xs in camp_imp.items():
            v = [x[j] for x in xs]; nh = len(v); Nh = pop["N"][h]; m = sum(v) / nh
            s2 = sum((x - m) ** 2 for x in v) / (nh - 1) if nh > 1 else 0.0
            tot += Nh * m; var += Nh * Nh * (1 - nh / Nh) * s2 / nh
        ris[nome]["euro_espansione"] = round(tot); ris[nome]["euro_espansione_ic95"] = [round(max(0.0, tot - 1.96 * var ** 0.5)), round(tot + 1.96 * var ** 0.5)]
    s = ris["ict"]
    ris["precisione_esclusione"] = {"cig": round(1 - s["quota_cig"], 5), "cig_wilson95": [round(1 - s["wilson95_cig"][1], 5), round(1 - s["wilson95_cig"][0], 5)],
                                     "euro": round(1 - s["quota_euro"], 5), "euro_wilson95": [round(1 - s["wilson95_euro"][1], 5), round(1 - s["wilson95_euro"][0], 5)],
                                     "nota": "precisione = quota di CIG (o euro) di S1 che sono davvero non ICT; i «dubbio» contati come non ICT qui, a parte in ict_o_dubbio"}
    json.dump(ris, open(os.path.join(ESITI, "misura.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(ris, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    {"estrai": estrai, "misura": misura, "classi": classi}[sys.argv[1]]()
