"""Attribuzione del cloud provider ai contratti ANAC (metodo: sito/content/progetto/metodo-cloud-provider.md).
Le regole stanno in classifica.py (funzione pura, testata in tests/test_classifica.py); qui solo lettura dei dati ANAC,
esclusione dei padri di accordo quadro e scrittura dei risultati.
Uso: python tools/analisi/attribuisci_provider.py 2024 2025 delta  -> lavoro/attribuzione/<anno>.csv e riepilogo.json"""
import csv, glob, io, json, os, re, sys, zipfile, collections
sys.path.insert(0, os.path.dirname(__file__))
from classifica import Classificatore, CPV_ICT, VERSIONE  # noqa: E402

D = "archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/"
# AQ non ancora richiamati da nessun attuativo: massimale presunto
RX_AQ = re.compile(r"\baccordo\s+quadro\b|\bconvenzione\b", re.I)

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
    c = Classificatore()
    agg = aggiudicatari()
    # un CIG è padre (massimale, non spesa) se un qualunque contratto, di qualunque anno, lo indica come accordo quadro
    padri = set()
    for a in [p[-4:] for p in glob.glob(D + "cig-20*")] + ["delta"]:
        padri |= {r["cig_accordo_quadro"] for r in righe_cig(a) if r["cig_accordo_quadro"]}
    riepilogo = {"regole": VERSIONE}
    for anno in anni:
        conta = collections.Counter(); somma = collections.Counter()
        with open(f"lavoro/attribuzione/{anno}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["cig", "cig_accordo_quadro", "e_padre", "cod_cpv", "importo_lotto", "stazione_appaltante", "aggiudicatari", "testo",
                        "via", "provider", "giurisdizione", "servizio", "cpv_ict", "canale", "regola"])
            for r in righe_cig(anno):
                testo = (r["oggetto_lotto"] or "") + " | " + (r["oggetto_gara"] or "")
                aq = r["cig_accordo_quadro"]
                nomi = sorted(agg.get(r["cig"], set()))
                e = c.classifica(testo, aq, nomi, r["cod_cpv"] or "")
                if e is None: continue
                ict = bool(CPV_ICT.match(r["cod_cpv"] or ""))
                padre = r["cig"] in padri or (not aq and bool(RX_AQ.search(testo)) and r.get("tipo_scelta_contraente", "").upper().startswith("PROCEDURA"))
                try: imp = float(r["importo_lotto"] or 0)
                except ValueError: imp = 0.0
                w.writerow([r["cig"], aq, int(padre), r["cod_cpv"], imp, r["denominazione_amministrazione_appaltante"], " ; ".join(nomi), testo[:500],
                            e["via"], e["provider"], e["giurisdizione"], e["servizio"], int(ict), e["canale"], e["regola"]])
                k = (e["via"], e["provider"], e["servizio"] if ict else e["servizio"] + "-fuori-cpv-ict")
                conta[k] += 1
                if not padre: somma[k] += imp
        riepilogo[anno] = [{"via": v, "provider": p, "servizio": s, "giurisdizione": c.giur.get(p, ""), "cig": n, "importo_esclusi_padri": round(somma[(v, p, s)])} for (v, p, s), n in sorted(conta.items())]
    json.dump(riepilogo, open("lavoro/attribuzione/riepilogo.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps(riepilogo, indent=1, ensure_ascii=False))

if __name__ == "__main__":
    main(sys.argv[1:] or ["2025"])
