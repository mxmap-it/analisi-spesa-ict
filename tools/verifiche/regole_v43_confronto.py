"""#40 regole v4.3 (9/11/2026): fotografia prima/dopo delle regole del classificatore su TUTTI i campioni etichettati
della lente prodotto: ciechi 1-3 (primo marchio, come lente_cieco.py), cieco 4 (classifica completa, come
lente_cieco4.py) e top-20 dei rivenditori (come lente_top20.py; etichetta si = provider della v4.1, no = nessuno).
Uso: python tools/verifiche/regole_v43_confronto.py prima|dopo -> esiti/2026-11-09/regole-v4.3/<nome>.csv;
con entrambi i file presenti stampa P/R big tech e tutti i provider per campione e i CIG cambiati (riepilogo.json)."""
import csv, glob, json, os, sys
from pathlib import Path
R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/analisi")); sys.path.insert(0, str(R / "tools/verifiche"))
from classifica import Classificatore, NOME_CANONICO  # noqa: E402
from lente_prodotto import BIGTECH_USA  # noqa: E402
O = R / "esiti/2026-11-09/regole-v4.3"
M = R / "report/metodo"


def fotografa(nome):
    c = Classificatore(); righe = []
    for d in ("lente-cieco", "lente-cieco-2", "lente-cieco-3"):
        t = {r["cig"]: r["testo"] for r in csv.DictReader(open(M / d / "campione-cieco.csv", encoding="utf-8"))}
        for e in csv.DictReader(open(M / d / "etichette.csv", encoding="utf-8")):
            m, _ = c.marchio(t[e["cig"]]); p = NOME_CANONICO.get(m["provider"], m["provider"]) if m else ""
            righe.append({"campione": d, "cig": e["cig"], "etichetta": e["etichetta_prodotto"], "lente": p})
    camp = {r["cig"]: r for r in csv.DictReader(open(M / "lente-cieco-4/campione-cieco.csv", encoding="utf-8"))}
    for e in csv.DictReader(open(M / "lente-cieco-4/etichette.csv", encoding="utf-8")):
        r = camp[e["cig"]]; ag = [a.strip() for a in r["aggiudicatari"].split(";") if a.strip()]
        k = c.classifica(r["testo"], r["cig_accordo_quadro"], ag, r["cod_cpv"]) or {"provider": ""}
        righe.append({"campione": "lente-cieco-4", "cig": e["cig"], "etichetta": e["etichetta_prodotto"], "lente": k["provider"]})
    camp = list(csv.DictReader(open(R / "esiti/2026-11-09/rivenditori/campione-top20-v4.1.csv", encoding="utf-8")))
    et = {r["cig"]: r["prodotto_corretto"] for r in csv.DictReader(open(M / "rivenditori-v4/etichette-top20.csv", encoding="utf-8"))}
    voluti = {r["cig"] for r in camp}; testi = {}
    for f in sorted(glob.glob(str(R / "lavoro/attribuzione/[0-9]*.csv"))):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            if r["cig"] in voluti: testi[r["cig"]] = r
    for x in camp:
        r = testi[x["cig"]]; ag = [a.strip() for a in r["aggiudicatari"].split(";") if a.strip()]
        k = c.classifica(r["testo"], r["cig_accordo_quadro"], ag, r["cod_cpv"]) or {"provider": "", "servizio": ""}
        p = k["provider"] if k["servizio"] not in ("servizi-professionali", "in-house", "software-infrastruttura") else ""
        righe.append({"campione": "top20", "cig": x["cig"], "etichetta": x["provider"] if et[x["cig"]] == "si" else "", "lente": p})
    os.makedirs(O, exist_ok=True)
    with open(O / f"{nome}.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(righe[0])); w.writeheader(); w.writerows(righe)


def metriche(righe, ins):
    tp = sum(r["lente"] in ins and r["lente"] == r["etichetta"] for r in righe)
    fp = sum(r["lente"] in ins and r["lente"] != r["etichetta"] for r in righe)
    fn = sum(r["etichetta"] in ins and r["lente"] != r["etichetta"] for r in righe)
    return {"tp": tp, "fp": fp, "fn": fn, "precisione": round(tp / (tp + fp), 3) if tp + fp else None, "richiamo": round(tp / (tp + fn), 3) if tp + fn else None}


def confronta():
    A = list(csv.DictReader(open(O / "prima.csv", encoding="utf-8"))); B = list(csv.DictReader(open(O / "dopo.csv", encoding="utf-8")))
    diz = {NOME_CANONICO.get(m["provider"], m["provider"]) for m in Classificatore().marchi}
    out = {"campioni": {}, "cambiati": []}
    for s in dict.fromkeys(r["campione"] for r in A):
        a = [r for r in A if r["campione"] == s]; b = [r for r in B if r["campione"] == s]
        out["campioni"][s] = {f"{f}_{n}": metriche(x, ins) for f, x in (("prima", a), ("dopo", b)) for n, ins in (("bigtech", set(BIGTECH_USA)), ("tutti", diz))}
    for a, b in zip(A, B):
        if a["lente"] != b["lente"]:
            ok = lambda x: x["lente"] == x["etichetta"] or (not x["lente"] and x["etichetta"] not in diz)  # «altro:x» = nessun provider del dizionario
            esito = "corretto" if ok(b) else ("regressione" if ok(a) else "cambiato-ancora-errato")
            out["cambiati"].append({"campione": a["campione"], "cig": a["cig"], "etichetta": a["etichetta"], "prima": a["lente"], "dopo": b["lente"], "esito": esito})
    json.dump(out, open(O / "riepilogo.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    fotografa(sys.argv[1])
    if (O / "prima.csv").exists() and (O / "dopo.csv").exists(): confronta()
