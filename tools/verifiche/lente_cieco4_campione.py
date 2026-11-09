"""#40 Quarto campione a cieco della lente prodotto, DOPO le regole del 9/11/2026 (commit 9ba5ad88: marchio di altro
lotto, prodotti di terzi col nome del marchio, formazione AWS).

Universo: lavoro/attribuzione/2024-2026.csv (CIG distinti), riclassificati con le regole CORRENTI di classifica.py;
esclusi tutti i CIG già comparsi in report/metodo/** (campioni v3, cieco 1-3, rivenditori v3/v4), nei campioni
esiti/*/rivenditori/campione-*.csv e in tests/casi_classifica.yaml.
Strati (disgiunti, in quest'ordine):
  M  gara multilotto (RX_MULTILOTTO sull'oggetto di gara) e un marchio del dizionario compare in qualche punto del testo
  R  marchio extra-UE attribuito, canale rivenditore
  E  marchio extra-UE attribuito, canale diretto o ignoto
  N  ICT (classifica non None) senza provider attribuito (per il richiamo)
Seme 20261110; quote M 40 (lo strato ne ha solo 7: presi tutti), R 50, E 50, N 43 = 150 CIG. Il file per l'annotatore (campione-cieco.csv) è mescolato e NON contiene strato né
uscita del classificatore; lo strato sta in strati.csv, da aprire solo dopo aver fissato e firmato le etichette.
Uso: python tools/verifiche/lente_cieco4_campione.py -> report/metodo/lente-cieco-4/{campione-cieco,strati}.csv, disegno.json"""
import csv, glob, json, random, re, sys, collections
from pathlib import Path

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/analisi"))
from classifica import Classificatore, RX_MULTILOTTO  # noqa: E402

D = R / "report/metodo/lente-cieco-4"
SEME, QUOTE = 20261110, {"M": 40, "R": 50, "E": 50, "N": 43}
RX_CIG = re.compile(r"\b[0-9A-Z]{10}\b")
csv.field_size_limit(10**8)


def gia_visti():
    v = set()
    for f in list(glob.glob(str(R / "report/metodo/**/*.csv"), recursive=True)) + glob.glob(str(R / "esiti/*/rivenditori/campione-*.csv")):
        if "lente-cieco-4" in f: continue
        for r in csv.DictReader(open(f, encoding="utf-8")):
            if r.get("cig"): v.add(r["cig"].strip())
    v |= set(RX_CIG.findall(open(R / "tests/casi_classifica.yaml", encoding="utf-8").read()))
    return v


def atti():
    a = collections.defaultdict(list)
    for l in open(R / "dati/atti/atti-server.jsonl", encoding="utf-8"):
        x = json.loads(l); s = (x.get("estrazione") or {}).get("testo_sha256")
        if s and x.get("esito_recupero") == "ok" and (R / f"dati/atti/testi/{s}.txt").exists(): a[x["cig"]].append(s)
    return a


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
            parti = r["testo"].split(" | ", 1)
            if len(parti) == 2 and RX_MULTILOTTO.search(parti[1]) and c._marchio(r["testo"])[0]: s = "M"
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
    json.dump({"universo": "lavoro/attribuzione/2024-2026.csv, CIG distinti, regole correnti (dopo 9ba5ad88)", "seme": SEME,
               "quote": QUOTE, "esclusi_gia_visti": len(esclusi), "dimensione_strati": {s: len(strati[s]) for s in sorted(strati)}},
              open(D / "disegno.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print({s: len(strati[s]) for s in strati}, "campione:", len(camp), "con atto:", sum(1 for x in camp if x["atti_testo_sha256"]))


if __name__ == "__main__":
    main()
