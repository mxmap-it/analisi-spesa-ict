"""Attribuzione del cloud provider ai contratti ANAC (metodo: sito/content/progetto/metodo-cloud-provider.md).
Vie implementate: 1 lotto di AQ/convenzione, 2 lotto dichiarato nel testo, 3 marchio, 5 fornitore = provider, 7 indeterminato.
Le vie 4 (PSN voce per voce) e 6 (modello linguistico) non sono ancora implementate: il PSN è solo marcato come canale.
Uso: python tools/analisi/attribuisci_provider.py 2024 2025 delta  -> lavoro/attribuzione/<anno>.csv e riepilogo.json"""
import csv, glob, io, json, os, re, sys, zipfile, collections
import yaml

D = "archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/"
CPV_ICT = re.compile(r"^(48|72|302|3223|3224|3225|3226|50312|50320|51611|64216|64222|79342)")
MARCHI = yaml.safe_load(open("config/marchi_cloud.yaml", encoding="utf-8"))
for m in MARCHI:
    m["rx"] = [re.compile(r, re.I) for r in m["regex"]]
    m["ex"] = [re.compile(r, re.I) for r in m.get("escludi", [])]
    m["fx"] = [re.compile(r, re.I) for r in m.get("fornitori", [])]
LOTTI = {}
for ini in yaml.safe_load(open("config/lotti_cloud.yaml", encoding="utf-8")):
    for l in ini["lotti"]:
        LOTTI[l["cig"]] = dict(l, iniziativa=ini["iniziativa"])
GIUR = {m["provider"]: m["giurisdizione"] for m in MARCHI}
# via 2: "IaaS e PaaS 2" / "2746" + "lotto N" nel testo
RX_AQ2746 = re.compile(r"2746|iaas\s*(e|/|-)?\s*paas\s*2|cloud\s+iaas\s+e\s+paas", re.I)
RX_LOTTO = re.compile(r"\blott?o\s*n?\.?\s*(\d)\b", re.I)
LOTTO_N = {str(l.get("lotto")): l for l in LOTTI.values() if l.get("lotto")}
RX_CLOUD = re.compile(r"\bcloud\b|\bsaas\b|\biaas\b|\bpaas\b|\bhosting\b", re.I)
# "servizi applicativi in ottica cloud" (AQ Consip) è sviluppo applicativo, non servizio cloud
RX_NON_CLOUD = re.compile(r"ins+otticas+cloud|clouds+natives+development", re.I)
# AQ non ancora richiamati da nessun attuativo: massimale presunto
RX_AQ = re.compile(r"accordos+quadro|convenzione", re.I)

def marchio(testo):
    for m in MARCHI:
        if any(r.search(testo) for r in m["rx"]) and not any(e.search(testo) for e in m["ex"]):
            return m
    return None

def righe_cig(anno):
    if anno == "delta":  # aggiornamenti mensili ANAC (es. 2026, non ancora nei file annuali): ultima versione di ogni CIG
        ultimo = {}
        for z in sorted(glob.glob(D + "cig/filesystem/*-cig_csv.zip")):
            zf = zipfile.ZipFile(z)
            m = next(i for i in zf.namelist() if i.endswith(".csv"))
            for r in csv.DictReader(io.TextIOWrapper(zf.open(m), encoding="utf-8-sig", errors="replace"), delimiter=";"):
                ultimo[r["cig"]] = r
        yield from ultimo.values()
        return
    for z in sorted(glob.glob(D + f"cig-{anno}/filesystem/cig_csv_*.zip")):
        zf = zipfile.ZipFile(z)
        yield from csv.DictReader(io.TextIOWrapper(zf.open(zf.namelist()[0]), encoding="utf-8-sig", errors="replace"), delimiter=";")

def aggiudicatari():
    a = collections.defaultdict(set)
    for z in sorted(glob.glob(D + "aggiudicatari/filesystem/*_csv.zip")):
        zf = zipfile.ZipFile(z)
        m = next(i for i in zf.namelist() if i.endswith(".csv"))
        for r in csv.DictReader(io.TextIOWrapper(zf.open(m), encoding="utf-8-sig", errors="replace"), delimiter=";"):
            a[r["cig"]].add((r["denominazione"] or "").strip())
    return a

def main(anni):
    os.makedirs("lavoro/attribuzione", exist_ok=True)
    agg = aggiudicatari()
    # un CIG è padre (massimale, non spesa) se un qualunque contratto, di qualunque anno, lo indica come accordo quadro
    padri = set()
    for a in [p[-4:] for p in glob.glob(D + "cig-20*")] + ["delta"]:
        padri |= {r["cig_accordo_quadro"] for r in righe_cig(a) if r["cig_accordo_quadro"]}
    riepilogo = {}
    for anno in anni:
        righe = list(righe_cig(anno))
        conta = collections.Counter(); somma = collections.Counter()
        with open(f"lavoro/attribuzione/{anno}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["cig", "cig_accordo_quadro", "e_padre", "cod_cpv", "importo_lotto", "stazione_appaltante", "aggiudicatari", "testo", "via", "provider", "giurisdizione", "servizio"])
            for r in righe:
                testo = (r["oggetto_lotto"] or "") + " | " + (r["oggetto_gara"] or "")
                aq = r["cig_accordo_quadro"]
                ict = bool(CPV_ICT.match(r["cod_cpv"] or ""))
                via = prov = serv = ""
                if aq in LOTTI:
                    via, prov, serv = "1-lotto", LOTTI[aq]["provider"], "cloud"
                elif RX_AQ2746.search(testo) and (mm := RX_LOTTO.search(testo)) and mm.group(1) in LOTTO_N:
                    via, prov, serv = "2-lotto-nel-testo", LOTTO_N[mm.group(1)]["provider"], "cloud"
                elif (m := marchio(testo)):
                    via, prov, serv = "3-marchio", m["provider"], m["servizio"]
                else:
                    nomi = agg.get(r["cig"], set())
                    for m in MARCHI:
                        if m["servizio"] != "licenza" and any(fx.search(n) for fx in m["fx"] for n in nomi) and RX_CLOUD.search(testo):
                            via, prov, serv = "5-fornitore", m["provider"], m["servizio"]; break
                if not via:
                    if not ict: continue
                    via = "7-indeterminato-cloud" if RX_CLOUD.search(testo) and not RX_NON_CLOUD.search(testo) else "0-ict-non-cloud"
                prov = {"AWS": "Amazon Web Services", "Google Cloud": "Google", "Microsoft Azure": "Microsoft", "Oracle Cloud": "Oracle", "IBM Cloud": "IBM"}.get(prov, prov)
                padre = r["cig"] in padri or (not aq and bool(RX_AQ.search(testo)) and r.get("tipo_scelta_contraente", "").upper().startswith("PROCEDURA"))
                try: imp = float(r["importo_lotto"] or 0)
                except ValueError: imp = 0.0
                w.writerow([r["cig"], aq, int(padre), r["cod_cpv"], imp, r["denominazione_amministrazione_appaltante"], " ; ".join(sorted(agg.get(r["cig"], []))), testo[:500], via, prov, GIUR.get(prov, ""), serv])
                k = (via, prov, serv)
                conta[k] += 1
                if not padre: somma[k] += imp
        riepilogo[anno] = [{"via": v, "provider": p, "servizio": s, "giurisdizione": GIUR.get(p, ""), "cig": n, "importo_esclusi_padri": round(somma[(v, p, s)])} for (v, p, s), n in sorted(conta.items())]
    json.dump(riepilogo, open("lavoro/attribuzione/riepilogo.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps(riepilogo, indent=1, ensure_ascii=False))

if __name__ == "__main__":
    main(sys.argv[1:] or ["2025"])
