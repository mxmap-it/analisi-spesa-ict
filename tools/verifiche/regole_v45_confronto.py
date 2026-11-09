"""#40/#72 regole v4.5 (9/11/2026): fotografia prima/dopo delle regole del classificatore su TUTTI i campioni etichettati
della lente prodotto, come regole_v44_confronto.py (che riusa: fotografa i ciechi 1-5 e il top-20 allo stesso modo) piu il
sesto cieco, valutato come i ciechi 4-5 (classifica completa, la lente conta il provider salvo «servizi-professionali»).
Per i ciechi 4-6 calcola anche precisione e richiamo in euro (importo del lotto).
Alias delle etichette (senza toccare i file delle etichette): «altro:tim-spc-cloud» = «SPC Cloud lotto 1» (v4.4) e, nuovo
v4.5, le etichette col nome di una in-house pubblica del dizionario (altro:csi-piemonte, altro:lepida, ...) = «In-house
pubblico»: l'annotatore ha scritto il nome dell'ente, la lente il nome canonico; e lo stesso prodotto.
Uso: python tools/verifiche/regole_v45_confronto.py prima|dopo -> esiti/2026-11-09/regole-v4.5/<nome>.csv;
con entrambi i file presenti stampa P/R big tech e tutti i provider per campione e i CIG cambiati (riepilogo.json)."""
import csv, json, os, sys
from pathlib import Path
R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/analisi")); sys.path.insert(0, str(R / "tools/verifiche"))
import regole_v44_confronto as v44  # noqa: E402
from classifica import Classificatore, NOME_CANONICO  # noqa: E402
from lente_prodotto import BIGTECH_USA  # noqa: E402
O = R / "esiti/2026-11-09/regole-v4.5"
M = R / "report/metodo"
INHOUSE = ("csi-piemonte", "lepida", "cineca", "trentino-digitale", "liguria-digitale", "insiel", "sogei", "inva", "aria")
ALIAS = dict(v44.ALIAS, **{f"altro:{n}": "In-house pubblico" for n in INHOUSE})


def fotografa(nome):
    v44.O = O; v44.ALIAS = ALIAS
    v44.fotografa(nome)  # ciechi 1-5 e top-20, stessa logica della v4.4, alias estesi
    righe = list(csv.DictReader(open(O / f"{nome}.csv", encoding="utf-8")))
    imp = {}
    for d in ("lente-cieco-4", "lente-cieco-5"):
        imp.update({(d, r["cig"]): r["importo"] for r in csv.DictReader(open(M / d / "campione-cieco.csv", encoding="utf-8"))})
    for r in righe: r["importo"] = imp.get((r["campione"], r["cig"]), "")
    c = Classificatore(); d = "lente-cieco-6"
    camp = {r["cig"]: r for r in csv.DictReader(open(M / d / "campione-cieco.csv", encoding="utf-8"))}
    for e in csv.DictReader(open(M / d / "etichette.csv", encoding="utf-8")):
        r = camp[e["cig"]]; ag = [a.strip() for a in r["aggiudicatari"].split(";") if a.strip()]
        k = c.classifica(r["testo"], r["cig_accordo_quadro"], ag, r["cod_cpv"]) or {"provider": "", "servizio": ""}
        y = ALIAS.get(e["etichetta_prodotto"], e["etichetta_prodotto"])
        righe.append({"campione": d, "cig": e["cig"], "etichetta": y, "lente": k["provider"] if k["servizio"] not in v44.FUORI_LENTE else "",
                      "lente_grezza": k["provider"], "importo": r["importo"]})
    with open(O / f"{nome}.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(righe[0])); w.writeheader(); w.writerows(righe)


def euro(righe, ins):
    x = lambda r: float(r["importo"] or 0)
    tp = sum(x(r) for r in righe if r["lente"] in ins and r["lente"] == r["etichetta"])
    fp = sum(x(r) for r in righe if r["lente"] in ins and r["lente"] != r["etichetta"])
    fn = sum(x(r) for r in righe if r["etichetta"] in ins and r["lente"] != r["etichetta"])
    return {"tp": round(tp), "fp": round(fp), "fn": round(fn), "precisione": round(tp / (tp + fp), 4) if tp + fp else None,
            "richiamo": round(tp / (tp + fn), 4) if tp + fn else None}


def confronta():
    v44.O = O
    v44.confronta()
    out = json.load(open(O / "riepilogo.json", encoding="utf-8"))
    A = list(csv.DictReader(open(O / "prima.csv", encoding="utf-8"))); B = list(csv.DictReader(open(O / "dopo.csv", encoding="utf-8")))
    diz = {NOME_CANONICO.get(m["provider"], m["provider"]) for m in Classificatore().marchi}
    for s in ("lente-cieco-4", "lente-cieco-5", "lente-cieco-6"):
        a = [r for r in A if r["campione"] == s]; b = [r for r in B if r["campione"] == s]
        out["campioni"][s]["euro"] = {f"{f}_{n}": euro(x, ins) for f, x in (("prima_grezza", [dict(r, lente=r["lente_grezza"]) for r in a]), ("prima", a), ("dopo", b))
                                      for n, ins in (("bigtech", set(BIGTECH_USA)), ("tutti", diz))}
    json.dump(out, open(O / "riepilogo.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({s: v["euro"] for s, v in out["campioni"].items() if "euro" in v}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    os.makedirs(O, exist_ok=True)
    fotografa(sys.argv[1])
    if (O / "prima.csv").exists() and (O / "dopo.csv").exists(): confronta()
