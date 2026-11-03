"""Dossier convenzioni (#55): attuativi in BDNCP dei CIG padre indicati, in streaming (mai tutti i CIG in memoria).
Per ogni padre: numero di attuativi, euro per anno, distribuzione per fascia d'importo (i massimali), attuativi più grandi,
classi di oggetto per parole chiave (migrazione, cloud, sviluppo, manutenzione, PMO, prodotti), aggiudicatari.
Uso: nice python tools/analisi/attuativi_convenzioni.py CIG [CIG ...] -> lavoro/dossier-convenzioni/attuativi.csv, riepilogo.json"""
import csv, glob, io, json, os, re, sys, zipfile, collections
sys.path.insert(0, os.path.dirname(__file__))
from attribuisci_provider import righe_cig, D  # noqa: E402

CLASSI = {
    "migrazione": r"migraz|trasfer\w* (su|in|al) cloud|re-?host|lift|cloud.?enabl|modernizzaz",
    "cloud": r"cloud|\bpsn\b|polo strategico|iaas|paas|saas|azure|aws|amazon web|google cloud|oracle cloud",
    "sviluppo": r"svilupp|realizzaz|evoluti|reingegneri|nuove funzionalit|digitalizzaz",
    "manutenzione": r"manutenz|\bmac\b|\bmev\b|correttiv|adeguativ|gestione applicat|conduzione",
    "pmo_demand": r"\bpmo\b|project management|demand|governance|supporto (al|alla) (rup|direzione)",
    "pnrr": r"pnrr|pnc\b|m1c1|misura 1\.",
    "prodotti": r"sap\b|oracle|microsoft|salesforce|servicenow|ibm\b|red ?hat|vmware|google|amazon|aws\b|azure|sas\b",
}
RX = {k: re.compile(v, re.I) for k, v in CLASSI.items()}
FASCE = [(0, 1e5), (1e5, 1e6), (1e6, 1e7), (1e7, 5e7), (5e7, 1e15)]


def fascia(x):
    for a, b in FASCE:
        if a <= x < b: return f"{a:.0e}-{b:.0e}"
    return "?"


def main(padri):
    padri = set(padri); os.makedirs("lavoro/dossier-convenzioni", exist_ok=True)

    # streaming puro: righe_cig("delta") tiene in memoria tutto il delta (~10 GB misurati il 3/11/2026); qui si filtra subito
    def delta():
        for z in sorted(glob.glob(D + "cig/filesystem/*-cig_csv.zip")):
            zf = zipfile.ZipFile(z); m = next(i for i in zf.namelist() if i.endswith(".csv"))
            yield from csv.DictReader(io.TextIOWrapper(zf.open(m), encoding="utf-8-sig", errors="replace"), delimiter=";")
    # limite: un CIG presente nel delta ma non più legato ai padri resta contato dalla versione annuale
    delta_cig = {r["cig"] for r in delta() if r["cig"] in padri or r.get("cig_accordo_quadro") in padri}
    fonti = sorted(p[-4:] for p in glob.glob(D + "cig-20*")) + ["delta"]
    att = {}; info_padre = {}
    for fonte in fonti:
        for r in (delta() if fonte == "delta" else righe_cig(fonte)):
            if fonte != "delta" and r["cig"] in delta_cig: continue
            if r["cig"] in padri:
                info_padre[r["cig"]] = {k: r.get(k, "") for k in ("cig", "anno_pubblicazione", "data_pubblicazione", "denominazione_amministrazione_appaltante", "oggetto_gara", "oggetto_lotto", "importo_lotto", "importo_complessivo_gara", "cod_cpv", "durata_prevista", "numero_gara", "stato")}
            if r.get("cig_accordo_quadro") in padri:
                att[r["cig"]] = {"padre": r["cig_accordo_quadro"], "cig": r["cig"], "anno": r.get("anno_pubblicazione", ""),
                                 "ente": r.get("denominazione_amministrazione_appaltante", ""), "cf_ente": r.get("cf_amministrazione_appaltante", ""),
                                 "importo": r.get("importo_lotto", ""), "oggetto": ((r.get("oggetto_gara") or "") + " | " + (r.get("oggetto_lotto") or ""))[:400],
                                 "cpv": r.get("cod_cpv", ""), "stato": r.get("stato", "")}
    agg = collections.defaultdict(set)
    for z in sorted(glob.glob(D + "aggiudicatari/filesystem/*_csv.zip")):
        zf = zipfile.ZipFile(z); m = next(i for i in zf.namelist() if i.endswith(".csv"))
        for r in csv.DictReader(io.TextIOWrapper(zf.open(m), encoding="utf-8-sig", errors="replace"), delimiter=";"):
            if r["cig"] in padri or r["cig"] in att: agg[r["cig"]].add((r.get("denominazione") or "").strip())
    with open("lavoro/dossier-convenzioni/attuativi.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["padre", "cig", "anno", "ente", "cf_ente", "importo", "aggiudicatari", "classi", "cpv", "oggetto"])
        for a in att.values():
            cl = [k for k, rx in RX.items() if rx.search(a["oggetto"])]; a["classi"] = cl
            w.writerow([a["padre"], a["cig"], a["anno"], a["ente"], a["cf_ente"], a["importo"], "; ".join(sorted(agg.get(a["cig"], ()))), ",".join(cl), a["cpv"], a["oggetto"]])
    rie = {}
    for p in sorted(padri):
        L = [a for a in att.values() if a["padre"] == p]
        imp = lambda a: float((a["importo"] or "0").replace(",", ".") or 0)
        per_anno = collections.defaultdict(lambda: [0, 0.0]); per_fascia = collections.defaultdict(lambda: [0, 0.0])
        classi = collections.defaultdict(lambda: [0, 0.0]); fornitori = collections.defaultdict(lambda: [0, 0.0])
        for a in L:
            x = imp(a); per_anno[a["anno"]][0] += 1; per_anno[a["anno"]][1] += x
            per_fascia[fascia(x)][0] += 1; per_fascia[fascia(x)][1] += x
            for c in a["classi"] or ["nessuna"]: classi[c][0] += 1; classi[c][1] += x
            for g in agg.get(a["cig"], {"(non indicato)"}): fornitori[g][0] += 1; fornitori[g][1] += x
        tot = sum(imp(a) for a in L); med = sorted(imp(a) for a in L)
        rie[p] = {"padre": info_padre.get(p), "aggiudicatari_padre": sorted(agg.get(p, ())), "n": len(L), "euro": round(tot),
                  "mediana": med[len(med)//2] if med else 0, "per_anno": {k: [v[0], round(v[1])] for k, v in sorted(per_anno.items())},
                  "per_fascia": {k: [v[0], round(v[1])] for k, v in sorted(per_fascia.items())},
                  "classi": {k: [v[0], round(v[1])] for k, v in sorted(classi.items(), key=lambda x: -x[1][1])},
                  "fornitori": {k: [v[0], round(v[1])] for k, v in sorted(fornitori.items(), key=lambda x: -x[1][1])[:12]},
                  "top": [[a["cig"], a["anno"], a["ente"][:60], round(imp(a)), a["oggetto"][:160]] for a in sorted(L, key=imp, reverse=True)[:12]]}
    json.dump(rie, open("lavoro/dossier-convenzioni/riepilogo.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print({p: (v["n"], v["euro"]) for p, v in rie.items()})


if __name__ == "__main__":
    main(sys.argv[1:])
