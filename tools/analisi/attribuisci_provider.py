"""Attribuzione del cloud provider ai contratti ANAC (metodo: sito/content/progetto/metodo-cloud-provider.md).
Le regole stanno in classifica.py (funzione pura, testata in tests/test_classifica.py); qui solo lettura dei dati ANAC,
esclusione dei padri di accordo quadro e scrittura dei risultati.
Uso: python tools/analisi/attribuisci_provider.py 2024 2025 2026  -> lavoro/attribuzione/<anno>.csv e riepilogo.json (anno di pubblicazione)"""
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
    """anni: anni di pubblicazione da misurare (es. 2024 2025 2026). Per ogni CIG vale l'ultima versione pubblicata:
    i file annuali e poi gli aggiornamenti mensili (delta), che vincono. Il delta contiene CIG di ogni anno: senza questa
    deduplica un contratto 2024 aggiornato nel 2026 si conterebbe due volte (errore trovato il 28/10/2026)."""
    os.makedirs("lavoro/attribuzione", exist_ok=True)
    c = Classificatore()
    agg = aggiudicatari()
    # un CIG è padre (massimale, non spesa) se un qualunque contratto, di qualunque anno, lo indica come accordo quadro
    padri = set()
    for a in [p[-4:] for p in glob.glob(D + "cig-20*")] + ["delta"]:
        padri |= {r["cig_accordo_quadro"] for r in righe_cig(a) if r["cig_accordo_quadro"]}
    ultimi = {}  # cig -> riga di output (solo contratti nel perimetro), l'ultima fonte vince
    fonti = [a for a in anni if glob.glob(D + f"cig-{a}/filesystem/cig_csv_*.zip")] + ["delta"]
    for fonte in fonti:
        for r in righe_cig(fonte):
            anno = (r.get("anno_pubblicazione") or "").strip()
            if anno not in anni:
                ultimi.pop(r["cig"], None)
                continue
            testo = (r["oggetto_lotto"] or "") + " | " + (r["oggetto_gara"] or "")
            aq = r["cig_accordo_quadro"]
            nomi = sorted(agg.get(r["cig"], set()))
            e = c.classifica(testo, aq, nomi, r["cod_cpv"] or "")
            if e is None:
                ultimi.pop(r["cig"], None)
                continue
            padre = r["cig"] in padri or (not aq and bool(RX_AQ.search(testo)) and r.get("tipo_scelta_contraente", "").upper().startswith("PROCEDURA"))
            try: imp = float(r["importo_lotto"] or 0)
            except ValueError: imp = 0.0
            ultimi[r["cig"]] = [anno, fonte, r["cig"], aq, int(padre), r["cod_cpv"], imp, r["denominazione_amministrazione_appaltante"], " ; ".join(nomi), testo[:500],
                                e["via"], e["provider"], e["giurisdizione"], e["servizio"], int(bool(CPV_ICT.match(r["cod_cpv"] or ""))), e["canale"], e["regola"]]
    # Importi da verificare: in molte adesioni importo_lotto è il massimale della convenzione, non la spesa dell'ente
    # (es. 430,0 milioni identici per Banca d'Italia e Infocamere su Microsoft EA). Regola trasparente, non correzione:
    # >= SOGLIA_GRANDE, oppure stesso importo (>= SOGLIA_RIPETUTO) presso stazioni appaltanti diverse. Si pubblicano i totali con e senza.
    SOGLIA_GRANDE, SOGLIA_RIPETUTO = 50e6, 5e6
    enti_per_importo = collections.defaultdict(set)
    for riga in ultimi.values():
        if riga[6] >= SOGLIA_RIPETUTO and riga[11]: enti_per_importo[round(riga[6])].add(riga[7])
    def da_verificare(riga):
        if riga[6] >= SOGLIA_GRANDE: return "grande importo (>= 50 milioni)"
        if riga[11] and len(enti_per_importo.get(round(riga[6]), ())) > 1: return "importo identico presso enti diversi"
        return ""
    riepilogo = {"regole": VERSIONE, "fonti": fonti, "soglie_importi_da_verificare": {"grande": SOGLIA_GRANDE, "ripetuto": SOGLIA_RIPETUTO}}
    with open("lavoro/attribuzione/importi-da-verificare.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["anno", "cig", "importo_lotto", "motivo", "stazione_appaltante", "aggiudicatari", "provider", "servizio", "e_padre", "testo"])
        for riga in sorted(ultimi.values(), key=lambda x: -x[6]):
            if riga[11] and (m := da_verificare(riga)):
                w.writerow([riga[0], riga[2], riga[6], m, riga[7], riga[8], riga[11], riga[13], riga[4], riga[9][:300]])
    for anno in anni:
        conta = collections.Counter(); somma = collections.Counter(); somma_netta = collections.Counter()
        with open(f"lavoro/attribuzione/{anno}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["cig", "cig_accordo_quadro", "e_padre", "cod_cpv", "importo_lotto", "stazione_appaltante", "aggiudicatari", "testo",
                        "via", "provider", "giurisdizione", "servizio", "cpv_ict", "canale", "regola", "fonte", "importo_da_verificare"])
            for riga in ultimi.values():
                if riga[0] != anno: continue
                _, fonte, cig, aq, padre, cpv, imp, sa, nomi, testo, via, prov, giur, serv, ict, canale, regola = riga
                dv = da_verificare(riga) if prov else ""
                w.writerow([cig, aq, padre, cpv, imp, sa, nomi, testo, via, prov, giur, serv, ict, canale, regola, fonte, dv])
                k = (via, prov, serv if ict else serv + "-fuori-cpv-ict")
                conta[k] += 1
                if not padre:
                    somma[k] += imp
                    if not dv: somma_netta[k] += imp
        riepilogo[anno] = [{"via": v, "provider": p, "servizio": s, "giurisdizione": c.giur.get(p, ""), "cig": n, "importo_esclusi_padri": round(somma[(v, p, s)]),
                            "importo_esclusi_padri_e_da_verificare": round(somma_netta[(v, p, s)])} for (v, p, s), n in sorted(conta.items())]
    json.dump(riepilogo, open("lavoro/attribuzione/riepilogo.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps(riepilogo, indent=1, ensure_ascii=False))

if __name__ == "__main__":
    main(sys.argv[1:] or ["2024", "2025", "2026"])
