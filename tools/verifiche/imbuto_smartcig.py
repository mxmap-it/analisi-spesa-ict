"""SmartCIG nell'imbuto (#76, mancanza M6): profilo per fattispecie e anno e imbuto degli SmartCIG dal 2024.

Fonti (mirror ANAC): smartcig-YYYY (file mensili annuali, solo CSV) e smartcig/ (aggiornamenti, ultima versione
di ogni CIG: il file più recente vince, come righe_cig("delta") dell'imbuto). Gli SmartCIG NON hanno CPV e NON hanno
aggiudicatari negli open data (verificato il 19/11/2026: 0 su 20.000 SmartCIG di marzo 2024 nel dataset aggiudicatari
e nel dataset CIG), quindi l'imbuto si applica solo sul testo dell'oggetto:
  S2  importo < 500 €  (ict / non-ict come nell'imbuto)
  S4  marchio di un provider nel testo (classifica.py, via 3; la via 5 richiede gli aggiudicatari e qui non scatta)
  S6  parola «cloud»/SaaS ecc. senza marchio (via 7) -> residuo
  S5  testo ICT (RX_ICT dell'imbuto 0.3.4) senza segnali cloud -> ICT non cloud, con le sottoclassi dell'imbuto
  S1  nessun segnale ICT nel testo -> escluso
Stesse regole e stesse funzioni di tools/analisi/imbuto.py (strato, sottoclasse_s5, RX_ICT, RX_PSN) e classifica.py.

Uso (dalla radice, sul server):
  flock lavoro/pesante.lock nice -n 15 .venv/bin/python tools/verifiche/imbuto_smartcig.py
     -> esiti/2026-11-19/imbuto/smartcig/{profilo.json, imbuto.json, sa.csv, marchi.csv, campione-cieco.csv}
        lavoro/smartcig/ict.csv (righe ICT, git-ignorato)
  python tools/verifiche/imbuto_smartcig.py riepilogo  -> esiti/.../riepilogo.json (cloud per giurisdizione, provider, enti)
  python tools/verifiche/imbuto_smartcig.py misura  -> precisione del campione a cieco (report/metodo/imbuto/smartcig-campione-cieco.csv)
"""
import collections, csv, glob, hashlib, io, json, math, os, sys, zipfile

RADICE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "tools/analisi"))
ESITI = os.path.join(RADICE, os.environ.get("SMARTCIG_ESITI", "esiti/2026-11-19/imbuto/smartcig"))
LAVORO = os.path.join(RADICE, "lavoro/smartcig")
ANNOT = os.path.join(RADICE, "report/metodo/imbuto/smartcig-campione-cieco.csv")
D = os.path.join(RADICE, "archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/")
ANNI_PROFILO = [str(a) for a in range(2020, 2026)]
SEME = "spesaict-smartcig-2026-11-19"


def righe(z):
    zf = zipfile.ZipFile(z); m = next(i for i in zf.namelist() if i.endswith(".csv"))
    yield from csv.DictReader(io.TextIOWrapper(zf.open(m), encoding="utf-8-sig", errors="replace"), delimiter=";")


def num(x):
    try: return float(x or 0)
    except ValueError: return 0.0


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


def main():
    import imbuto
    from classifica import Classificatore
    os.makedirs(ESITI, exist_ok=True); os.makedirs(LAVORO, exist_ok=True)
    fonti = {}
    # 1) profilo per fattispecie, procedura e anno (file annuali, CIG distinti per anno)
    prof = collections.defaultdict(lambda: [0, 0.0])
    for a in ANNI_PROFILO:
        visti = set()
        for z in sorted(glob.glob(D + f"smartcig-{a}/filesystem/smartcig_csv_*.zip")):
            fonti[os.path.relpath(z, RADICE)] = sha(z)
            for r in righe(z):
                if r["cig"] in visti: continue
                visti.add(r["cig"])
                k = (a, r["tipo_fattispecie_contrattuale"].strip(), r["tipo_scelta_contraente"].strip().upper(), r["oggetto_principale_contratto"].strip())
                prof[k][0] += 1; prof[k][1] += num(r["importo_lotto"])
        print(a, len(visti), flush=True)
    profilo = [{"anno": k[0], "fattispecie": k[1], "procedura": k[2], "oggetto": k[3], "cig": v[0], "euro": round(v[1])}
               for k, v in sorted(prof.items(), key=lambda kv: (kv[0][0], -kv[1][1]))]
    # 2) imbuto dal 2024: delta (file più recente vince) + annuali 2024, 2025 non presenti nel delta
    c = Classificatore()
    agg = collections.defaultdict(lambda: [0, 0.0]); sa = collections.defaultdict(lambda: [0, 0.0, 0, 0.0])
    marchi = collections.defaultdict(lambda: [0, 0.0]); pool = []
    out = csv.writer(open(os.path.join(LAVORO, "ict.csv"), "w", newline="", encoding="utf-8"))
    out.writerow(["anno", "cig", "strato", "sottoclasse", "via", "provider", "giurisdizione", "servizio", "importo", "stazione_appaltante", "cf_sa", "testo"])
    visti = set()

    def tratta(r):
        anno = (r.get("anno_comunicazione") or "").strip()
        if anno < "2024": return
        testo = (r["oggetto_lotto"] or "") + " | " + (r["oggetto_gara"] or "")
        imp = num(r["importo_lotto"])
        e = c.classifica(testo, "", [], "")
        if e and e["via"][0] in "07" and not imbuto.RX_ICT.search(testo): e = None  # senza CPV: il testo decide
        s, sc, g = imbuto.strato({"cig_accordo_quadro": ""}, e, imp, False, testo, "")
        giur = "incerto-servizio-psn" if sc == "psn-servizio-da-determinare" else (e or {}).get("giurisdizione", "")
        agg[(anno, s, sc, giur)][0] += 1; agg[(anno, s, sc, giur)][1] += imp
        if s == "S1-escluso-non-ict" or (s == "S2-sotto-soglia" and sc == "non-ict"): return
        prov = (e or {}).get("provider", "")
        out.writerow([anno, r["cig"], s, sc, (e or {}).get("via", ""), prov, giur, (e or {}).get("servizio", ""), imp,
                      r["denominazione_amministrazione_appaltante"], r["cf_amministrazione_appaltante"], testo[:400]])
        cloud = s in ("S3-convenzione-lotto", "S4-marchio", "S6-residuo")
        k = (r["cf_amministrazione_appaltante"], r["denominazione_amministrazione_appaltante"])
        sa[k][0] += 1; sa[k][1] += imp
        if cloud: sa[k][2] += 1; sa[k][3] += imp
        if prov: marchi[(prov, giur, (e or {}).get("servizio", ""))][0] += 1; marchi[(prov, giur, (e or {}).get("servizio", ""))][1] += imp
        if cloud and s != "S2-sotto-soglia":
            pool.append((hashlib.sha256(f"{SEME}|{r['cig']}".encode()).hexdigest(), r["cig"], anno, s, sc, prov, imp,
                         r["denominazione_amministrazione_appaltante"], testo[:400]))

    for z in sorted(glob.glob(D + "smartcig/filesystem/*-smartcig_csv.zip"), reverse=True):
        fonti[os.path.relpath(z, RADICE)] = sha(z)
        ultimo = {}
        for r in righe(z): ultimo[r["cig"]] = r  # dentro il file vince l'ultima riga
        for cig, r in ultimo.items():
            if cig in visti: continue
            visti.add(cig); tratta(r)
        del ultimo
    n_delta = len(visti); print("delta", n_delta, flush=True)
    for a in ("2024", "2025"):
        for z in sorted(glob.glob(D + f"smartcig-{a}/filesystem/smartcig_csv_*.zip")):
            for r in righe(z):
                if r["cig"] in visti: continue
                visti.add(r["cig"]); tratta(r)
        print(a, len(visti), flush=True)
    imb = [{"anno": k[0], "strato": k[1], "sottoclasse": k[2], "giurisdizione": k[3], "cig": v[0], "euro": round(v[1])} for k, v in sorted(agg.items())]
    json.dump({"profilo": profilo, "fonti_sha256": fonti, "anni_profilo": ANNI_PROFILO,
               "nota": "profilo: CIG distinti per file annuale smartcig-YYYY (solo CSV); i mesi mancanti alla fonte (P09) non sono ricostruiti"},
              open(os.path.join(ESITI, "profilo.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump({"versione": "imbuto-0.3.4 su SmartCIG (solo testo)", "cig_letti_dal_delta": n_delta, "righe": imb},
              open(os.path.join(ESITI, "imbuto.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    with open(os.path.join(ESITI, "sa.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["cf_sa", "stazione_appaltante", "cig_ict", "euro_ict", "cig_cloud", "euro_cloud"])
        for k, v in sorted(sa.items(), key=lambda kv: -kv[1][3])[:500]: w.writerow([*k, v[0], round(v[1]), v[2], round(v[3])])
    with open(os.path.join(ESITI, "marchi.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["provider", "giurisdizione", "servizio", "cig", "euro"])
        for k, v in sorted(marchi.items(), key=lambda kv: -kv[1][1]): w.writerow([*k, v[0], round(v[1])])
    # campione a cieco: 40 fra i CIG inclusi come cloud (S4 marchio + S6 residuo), 25 S4 e 15 S6, chiave sha256 più piccola
    pool.sort()
    s4 = [p for p in pool if p[3] == "S4-marchio"][:25]; s6 = [p for p in pool if p[3] == "S6-residuo"][:40 - min(25, len([p for p in pool if p[3] == "S4-marchio"]))]
    with open(os.path.join(ESITI, "campione-cieco.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["cig", "anno", "strato", "sottoclasse", "provider", "importo", "stazione_appaltante", "testo"])
        for p in sorted(s4 + s6): w.writerow(p[1:])
    print("fatto", flush=True)


def riepilogo():
    """Dai CIG ICT di lavoro/smartcig/ict.csv (scritto da main): cloud >= 500 € per giurisdizione, provider, ente e anno."""
    tot = collections.defaultdict(lambda: [0, 0.0]); prov = collections.defaultdict(lambda: [0, 0.0])
    sa = collections.defaultdict(lambda: [0, 0.0]); anno = collections.defaultdict(lambda: [0, 0.0])
    for r in csv.DictReader(open(os.path.join(LAVORO, "ict.csv"), encoding="utf-8")):
        if r["strato"] == "S2-sotto-soglia": continue
        imp = float(r["importo"])
        if r["strato"] == "S4-marchio" and r["sottoclasse"] in ("cloud", "in-house"): k = "cloud certo (S4)"
        elif r["strato"] == "S6-residuo": k = "cloud incerto (S6)"
        else: continue
        tot[(k, r["giurisdizione"] or "da determinare")][0] += 1; tot[(k, r["giurisdizione"] or "da determinare")][1] += imp
        anno[(k, r["anno"])][0] += 1; anno[(k, r["anno"])][1] += imp
        if r["provider"]: prov[(r["provider"], r["giurisdizione"])][0] += 1; prov[(r["provider"], r["giurisdizione"])][1] += imp
        sa[(r["cf_sa"], r["stazione_appaltante"].strip())][0] += 1; sa[(r["cf_sa"], r["stazione_appaltante"].strip())][1] += imp
    f = lambda d, n=None: [{"chiave": list(k), "cig": v[0], "euro": round(v[1])} for k, v in sorted(d.items(), key=lambda kv: -kv[1][1])[:n]]
    out = {"fonte": "lavoro/smartcig/ict.csv (imbuto_smartcig.py)", "sha256": sha(os.path.join(LAVORO, "ict.csv")),
           "cloud_per_giurisdizione": f(tot), "cloud_per_anno": f(anno), "provider_cloud_certo": f(prov, 20), "enti_cloud_s4_s6": f(sa, 20),
           "nota": "solo CIG >= 500 € (S2 escluso); fornitori non disponibili: gli open data SmartCIG non hanno aggiudicatari"}
    json.dump(out, open(os.path.join(ESITI, "riepilogo.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({k: out[k] for k in ("cloud_per_giurisdizione", "cloud_per_anno")}, ensure_ascii=False, indent=0))
    print(json.dumps(out["provider_cloud_certo"][:10], ensure_ascii=False)); print(json.dumps(out["enti_cloud_s4_s6"][:10], ensure_ascii=False))


def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(p, 3), round(c - h, 3), round(c + h, 3)]


def misura():
    camp = {r["cig"]: r for r in csv.DictReader(open(os.path.join(ESITI, "campione-cieco.csv"), encoding="utf-8"))}
    ann = list(csv.DictReader(open(ANNOT, encoding="utf-8")))
    assert {a["cig"] for a in ann} == set(camp)
    # atteso dall'imbuto: cloud per S6 e per S4 con servizio cloud o in-house; non cloud per S4 licenza/software/servizi
    atteso = lambda r: "cloud" if r["strato"] == "S6-residuo" or r["sottoclasse"] in ("cloud", "in-house") else "non-cloud"
    ris = {}
    for nome, sel in (("S4 cloud/in-house", [a for a in ann if camp[a["cig"]]["strato"] == "S4-marchio" and atteso(camp[a["cig"]]) == "cloud"]),
                      ("S4 licenza/software", [a for a in ann if atteso(camp[a["cig"]]) == "non-cloud"]),
                      ("S6 residuo", [a for a in ann if camp[a["cig"]]["strato"] == "S6-residuo"]), ("tutti", ann)):
        if not sel: continue
        ok = sum(a["giudizio"] == atteso(camp[a["cig"]]) for a in sel)
        dub = sum(a["giudizio"] == "dubbio" for a in sel)
        ris[nome] = {"n": len(sel), "concordi": ok, "dubbi": dub, "precisione_wilson95": wilson(ok, len(sel)),
                     "precisione_senza_dubbi_wilson95": wilson(ok, len(sel) - dub) if len(sel) > dub else None,
                     "giudizi": dict(collections.Counter(a["giudizio"] for a in sel)),
                     "prodotto": dict(collections.Counter(a["prodotto_corretto"] for a in sel))}
    json.dump(ris, open(os.path.join(ESITI, "misura-cieco.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(ris, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    {"misura": misura, "riepilogo": riepilogo}.get((sys.argv[1:] or [""])[0], main)()
