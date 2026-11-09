"""#40 Sesto campione a cieco della lente prodotto, DOPO le regole v4.4 (commit e3c0d197). Copia di lente_cieco5_campione.py
con seme 20261112, esclusi anche i CIG del cieco 5 e di esiti/*/regole-v4.4, e uno strato P «servizi su piattaforma»
(marchio del dizionario e consulenza/manutenzione/migrazione/sviluppo/system integration/servizi professionali), prima di F.
Quote: M tutti (vuoto: il cieco 5 li ha presi tutti), P 50, F 40, R 40, E 40, N 80. Uscite in report/metodo/lente-cieco-6/. Testo originale del cieco 5: Criterio delle etichette:
«prodotto che si compra», non «prodotto nominato» (metodo-cloud-provider.md, cieco 4 e v4.3).

Universo: lavoro/attribuzione/2024-2026.csv (CIG distinti), classificati con le regole CORRENTI di classifica.py;
esclusi tutti i CIG già comparsi in report/metodo/** (campioni v3, ciechi 1-4, rivenditori), esiti/*/** (*.csv:
campioni rivenditori, errori dei ciechi, regole-v4.3) e tests/casi_classifica.yaml.
Strati (disgiunti, in quest'ordine):
  M  multilotto: RX_MULTILOTTO in un punto qualunque del testo (oggetto del lotto o della gara; nel cieco 4 solo la gara,
     7 CIG) e un marchio del dizionario nel testo -> presi tutti
  F  marchio del dizionario nel testo e parole di servizio accessorio (formazione/corso/docenza, supporto/assistenza/
     help desk/sistemista, backup, connettività/fibra/collegamento/linea)
  R  marchio extra-UE attribuito, canale rivenditore
  E  marchio extra-UE attribuito, canale diretto o ignoto
  N  ICT (classifica non None) senza provider attribuito (per il richiamo)
Seme 20261111; quote M tutti, F 40, R 35, E 35, N 80. Il file per l'annotatore (campione-cieco.csv) è mescolato e NON
contiene strato né uscita del classificatore; lo strato sta in strati.csv, da aprire solo dopo aver fissato le etichette.
Uso: nice python tools/verifiche/lente_cieco5_campione.py -> report/metodo/lente-cieco-6/{campione-cieco,strati}.csv, disegno.json"""
import csv, glob, json, random, re, sys, collections
from pathlib import Path

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/analisi")); sys.path.insert(0, str(R / "tools/verifiche"))
from classifica import Classificatore, RX_MULTILOTTO  # noqa: E402
from lente_cieco4_campione import atti  # noqa: E402

D = R / "report/metodo/lente-cieco-6"
SEME, QUOTE = 20261112, {"M": 10**6, "P": 50, "F": 40, "R": 40, "E": 40, "N": 80}
RX_CIG = re.compile(r"\b[0-9A-Z]{10}\b")
RX_PIATTAFORMA = re.compile(r"consulenz|manutenzion|migrazion|sviluppo|system\s*integrat|servizi\s+professional|application\s+(management|maintenance)", re.I)
RX_ACCESSORIO = re.compile(r"formazion|\bcors[oi]\b|docenz|support|assistenz|help\s*desk|sistemist|backup|connettivit|\bfibra\b|collegament|\blinea\b", re.I)
csv.field_size_limit(10**8)


def gia_visti():
    v = set()
    fs = glob.glob(str(R / "report/metodo/**/*.csv"), recursive=True) + sum((glob.glob(str(R / g)) for g in ("esiti/*/rivenditori/campione-*.csv", "esiti/*/lente-cieco-*/*.csv", "esiti/*/regole-v4.3/*.csv", "esiti/*/regole-v4.4/*.csv")), [])
    for f in fs:
        if "lente-cieco-6" in f: continue
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
    json.dump({"universo": "lavoro/attribuzione/2024-2026.csv, CIG distinti, regole v4.4 (e3c0d197)", "seme": SEME,
               "quote": {k: ("tutti" if v == 10**6 else v) for k, v in QUOTE.items()}, "esclusi_gia_visti": len(esclusi),
               "dimensione_strati": {s: len(strati[s]) for s in sorted(strati)}},
              open(D / "disegno.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("campione:", len(camp), "con atto:", sum(1 for x in camp if x["atti_testo_sha256"]))


if __name__ == "__main__":
    main()
