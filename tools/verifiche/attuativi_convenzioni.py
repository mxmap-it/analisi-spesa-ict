"""Attuativi in BDNCP delle convenzioni con dossier (report/convenzioni/, #55).
Streaming riga per riga (righe_cig): in memoria solo le righe che riguardano i CIG padre in esame.
Per ogni CIG vale l'ultima versione (file annuali, poi delta mensile).
Uso (sul server, da ~/analisi-spesa-ict): nice -n 19 .venv/bin/python tools/verifiche/attuativi_convenzioni.py
Esito: lavoro/convenzioni-55/attuativi.csv, lavoro/convenzioni-55/riepilogo.json"""
import collections, csv, json, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "analisi"))
from attribuisci_provider import righe_cig  # noqa: E402

PADRI = {
    "9066973ECE": "psn",
    "55187486EA": "spc-cloud-l1",
    "55193442C1": "spc-cloud-l3",
    "5519376D26": "spc-cloud-l4",
    "7991036B82": "trenitalia-ict",
    "7963682E45": "fs-2019-candidato",
}
# righe senza legame al padre ma con l'iniziativa nell'oggetto (legame mancante: altro indicatore di qualità)
RX_ORFANI = {
    "psn": re.compile(r"polo\s+strategico|\bPSN\b|secure\s+public\s+cloud|psn\s+managed", re.I),
    "spc-cloud-l1": re.compile(r"spc\s*cloud.{0,40}lotto\s*1\b", re.I),
    "spc-cloud-l3": re.compile(r"spc\s*cloud.{0,40}lotto\s*3\b", re.I),
    "spc-cloud-l4": re.compile(r"spc\s*cloud.{0,40}lotto\s*4\b", re.I),
}
CLASSI = {
    "secure_public_cloud": r"secure\s+public\s+cloud",
    "psn_managed": r"psn\s+managed|managed",
    "hybrid": r"hybrid|ibrid",
    "azure_microsoft": r"azure|microsoft",
    "google": r"google",
    "aws_amazon": r"\baws\b|amazon",
    "oracle": r"oracle",
    "housing": r"housing",
    "hosting": r"hosting",
    "iaas_paas_saas": r"\biaas\b|\bpaas\b|\bsaas\b",
    "migrazione": r"migraz|trasferiment|lift|shift|rehost|replatform|re-?architect",
    "cloud": r"cloud",
    "sviluppo_manutenzione": r"svilupp|realizzazion|manutenzion|evoluti|portale|sito\s+web|applicativ",
    "interoperabilita": r"interoperabil|cooperazione\s+applicativa|\bapi\b|\bpdnd\b",
    "servizi_professionali": r"supporto|consulenz|assistenza|servizi\s+professional|data\s*(analysis|analytics)|big\s+data",
    "sicurezza": r"sicurezza|security",
}
CLASSI = {k: re.compile(v, re.I) for k, v in CLASSI.items()}
ANNI = list(range(2007, 2026)) + ["delta"]


def euro(s):
    try:
        return float((s or "0").replace(",", "."))
    except ValueError:
        return 0.0


def main():
    os.makedirs("lavoro/convenzioni-55", exist_ok=True)
    righe = {}  # cig -> (iniziativa, legame, riga): solo le righe rilevanti
    for anno in ANNI:
        for r in righe_cig(anno):
            aq, cig = (r.get("cig_accordo_quadro") or "").strip().upper(), (r.get("cig") or "").strip().upper()
            if cig in PADRI:
                righe[cig] = (PADRI[cig], "padre", r)
            elif aq in PADRI:
                righe[cig] = (PADRI[aq], "attuativo", r)
            else:
                testo = f"{r.get('oggetto_gara', '')} {r.get('oggetto_lotto', '')}"
                for ini, rx in RX_ORFANI.items():
                    if rx.search(testo):
                        righe[cig] = (ini, "orfano", r)
                        break
        print(anno, len(righe), flush=True)
    rip = collections.defaultdict(lambda: {"n": 0, "euro": 0.0, "per_anno": collections.Counter(),
                                           "euro_per_anno": collections.Counter(), "classi_n": collections.Counter(),
                                           "classi_euro": collections.Counter(), "anomali": [], "top": []})
    with open("lavoro/convenzioni-55/attuativi.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["iniziativa", "legame", "cig", "cig_accordo_quadro", "anno", "importo_lotto", "stazione_appaltante",
                    "cpv", "classi", "oggetto_gara", "oggetto_lotto"])
        for cig, (ini, leg, r) in sorted(righe.items()):
            testo = f"{r.get('oggetto_gara', '')} {r.get('oggetto_lotto', '')}"
            cl = [k for k, rx in CLASSI.items() if rx.search(testo)]
            imp = euro(r.get("importo_lotto"))
            anno = r.get("anno_pubblicazione", "")
            w.writerow([ini, leg, cig, r.get("cig_accordo_quadro"), anno, imp, r.get("denominazione_amministrazione_appaltante"),
                        r.get("cod_cpv"), "|".join(cl), (r.get("oggetto_gara") or "")[:300], (r.get("oggetto_lotto") or "")[:300]])
            k = f"{ini}/{leg}"
            s = rip[k]
            s["n"] += 1
            s["euro"] += imp
            s["per_anno"][anno] += 1
            s["euro_per_anno"][anno] += imp
            for c in cl or ["nessuna"]:
                s["classi_n"][c] += 1
                s["classi_euro"][c] += imp
            if leg != "padre" and imp >= 20e6:
                s["anomali"].append([cig, anno, imp, r.get("denominazione_amministrazione_appaltante"), (r.get("oggetto_lotto") or "")[:160]])
            s["top"].append([imp, cig, anno, r.get("denominazione_amministrazione_appaltante"), (r.get("oggetto_lotto") or "")[:160]])
    for s in rip.values():
        s["top"] = sorted(s["top"], reverse=True)[:15]
        s["euro"] = round(s["euro"])
        s["euro_per_anno"] = {a: round(v) for a, v in sorted(s["euro_per_anno"].items())}
        s["classi_euro"] = {a: round(v) for a, v in s["classi_euro"].most_common()}
        s["per_anno"] = dict(sorted(s["per_anno"].items()))
        s["classi_n"] = dict(s["classi_n"].most_common())
    with open("lavoro/convenzioni-55/riepilogo.json", "w", encoding="utf-8") as f:
        json.dump(rip, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
