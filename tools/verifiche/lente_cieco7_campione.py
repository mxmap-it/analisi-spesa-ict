"""#40 #72 #78 Settimo campione a cieco della lente prodotto, regole v4.5 (commit 02830f51): l'unico previsto, prima del
rendiconto finale. Copia di lente_cieco6_campione.py con seme 20261119, esclusi anche i CIG del cieco 6 e di
esiti/*/regole-v4.5. Quote: M tutti, P 40, F 30, R 40, E 40, N 60. Uscite in report/metodo/lente-cieco-7/.
Criterio delle etichette: «prodotto comprato» (metodo-cloud-provider.md).
Uso: nice python tools/verifiche/lente_cieco7_campione.py -> report/metodo/lente-cieco-7/{campione-cieco,strati}.csv, disegno.json"""
import csv, glob, json, random, re, sys, collections
from pathlib import Path

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/analisi")); sys.path.insert(0, str(R / "tools/verifiche"))
from classifica import Classificatore, RX_MULTILOTTO  # noqa: E402
from lente_cieco4_campione import atti  # noqa: E402

D = R / "report/metodo/lente-cieco-7"
SEME, QUOTE = 20261119, {"M": 10**6, "P": 40, "F": 30, "R": 40, "E": 40, "N": 60}
RX_CIG = re.compile(r"\b[0-9A-Z]{10}\b")
RX_PIATTAFORMA = re.compile(r"consulenz|manutenzion|migrazion|sviluppo|system\s*integrat|servizi\s+professional|application\s+(management|maintenance)", re.I)
RX_ACCESSORIO = re.compile(r"formazion|\bcors[oi]\b|docenz|support|assistenz|help\s*desk|sistemist|backup|connettivit|\bfibra\b|collegament|\blinea\b", re.I)
csv.field_size_limit(10**8)


def gia_visti():
    v = set()
    fs = glob.glob(str(R / "report/metodo/**/*.csv"), recursive=True) + sum((glob.glob(str(R / g)) for g in ("esiti/*/rivenditori/campione-*.csv", "esiti/*/lente-cieco-*/*.csv", "esiti/*/regole-v4.3/*.csv", "esiti/*/regole-v4.4/*.csv", "esiti/*/regole-v4.5/*.csv")), [])
    for f in fs:
        if "lente-cieco-7" in f: continue
        try:
            for r in csv.DictReader(open(f, encoding="utf-8")):
                if r.get("cig"): v.add(r["cig"].strip())
        except (UnicodeDecodeError, csv.Error): pass
    v |= set(RX_CIG.findall(open(R / "tests/casi_classifica.yaml", encoding="utf-8").read()))
    return v


def main():
    c = Classificatore(); esclusi = gia_visti(); at = atti()
    strati = collections.defaultdict(list); visti = set()
    for f in sorted(glob.glob(str(R / "lavoro/attribuzione/202[4-6].csv"))):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            cig = r["cig"]
            if cig in visti or cig in esclusi: continue
            visti.add(cig)
            ag = [a.strip() for a in r["aggiudicatari"].split(";") if a.strip()]
            k = c.classifica(r["testo"], r["cig_accordo_quadro"], ag, r["cod_cpv"])
            if k is None: continue
            mar = c._marchio(r["testo"])[0]
            if RX_MULTILOTTO.search(r["testo"]) and mar: s = "M"
            elif mar and RX_PIATTAFORMA.search(r["testo"]): s = "P"
            elif mar and RX_ACCESSORIO.search(r["testo"]): s = "F"
            elif k["giurisdizione"] == "EXTRA-UE": s = "R" if k["canale"] == "rivenditore" else "E"
            elif not k["provider"]: s = "N"
            else: continue
            strati[s].append({"cig": cig, "importo": r["importo_lotto"], "stazione_appaltante": r["stazione_appaltante"],
                              "aggiudicatari": r["aggiudicatari"], "cig_accordo_quadro": r["cig_accordo_quadro"], "cod_cpv": r["cod_cpv"],
                              "atti_testo_sha256": ";".join(at.get(cig, [])), "testo": r["testo"]})
    rnd = random.Random(SEME); camp = []; strato_di = {}
    for s in sorted(QUOTE):
        pool = sorted(strati[s], key=lambda x: x["cig"])
        for x in rnd.sample(pool, min(QUOTE[s], len(pool))): camp.append(x); strato_di[x["cig"]] = s
    rnd.shuffle(camp)
    D.mkdir(parents=True, exist_ok=True)
    with open(D / "campione-cieco.csv", "w", encoding="utf-8", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=["n"] + list(camp[0])); w.writeheader()
        for i, x in enumerate(camp, 1): w.writerow({"n": i, **x})
    with open(D / "strati.csv", "w", encoding="utf-8", newline="") as fo:
        w = csv.writer(fo); w.writerow(["cig", "strato"]); [w.writerow([x["cig"], strato_di[x["cig"]]]) for x in camp]
    json.dump({"universo": "lavoro/attribuzione/2024-2026.csv, CIG distinti, regole v4.5 (02830f51)", "seme": SEME,
               "quote": {k: ("tutti" if v == 10**6 else v) for k, v in QUOTE.items()}, "esclusi_gia_visti": len(esclusi),
               "dimensione_strati": {s: len(strati[s]) for s in sorted(strati)}},
              open(D / "disegno.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("campione:", len(camp), "con atto:", sum(1 for x in camp if x["atti_testo_sha256"]))


if __name__ == "__main__":
    main()
