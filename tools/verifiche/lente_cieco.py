"""#40 Lente prodotto su un campione NUOVO a cieco (senza la circolarità del campione v3).

Disegno: report/metodo/lente-cieco/disegno.json (universo lavoro/imbuto/ict.csv dal 2024, esclusi i 611 del v3,
40 CIG casuali per strato, seme 20261106). Etichette: report/metodo/lente-cieco/etichette.csv, date leggendo il solo
testo dell'oggetto (atti non aperti), senza vedere l'uscita della lente: il riferimento misura «quale prodotto nomina
il testo», cioè la lente stessa, non il prodotto effettivamente comprato.
Misura: per strato, TP/FP/FN del primo marchio (Classificatore.marchio) contro l'etichetta, per big tech USA e per tutti
i provider del dizionario; stima pesata sull'universo con i pesi di strato (N_h / n_h).

Uso: python tools/verifiche/lente_cieco.py -> esiti/<oggi>/lente-prodotto/lente-cieco.json"""
import csv, json, os, sys, math, datetime, collections
from pathlib import Path

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/analisi")); sys.path.insert(0, str(R / "tools/verifiche"))
from classifica import Classificatore, NOME_CANONICO  # noqa: E402
from lente_prodotto import BIGTECH_USA, wilson  # noqa: E402

D = R / (sys.argv[1] if len(sys.argv) > 1 else "report/metodo/lente-cieco")


def main():
    cl = Classificatore()
    diz = {NOME_CANONICO.get(m["provider"], m["provider"]) for m in cl.marchi}
    dis = json.load(open(D / "disegno.json", encoding="utf-8"))
    testi = {r["cig"]: r for r in csv.DictReader(open(D / "campione-cieco.csv", encoding="utf-8"))}
    et = list(csv.DictReader(open(D / "etichette.csv", encoding="utf-8")))
    per = collections.defaultdict(collections.Counter); err = []
    for e in et:
        m, _ = cl.marchio(testi[e["cig"]]["testo"])
        p = NOME_CANONICO.get(m["provider"], m["provider"]) if m else ""
        y = e["etichetta_prodotto"]; s = e["strato"]; c = per[s]; c["n"] += 1
        for nome, ins in (("bt", BIGTECH_USA), ("diz", diz)):
            c[nome + "_tp"] += p in ins and p == y
            c[nome + "_fp"] += p in ins and p != y
            c[nome + "_fn"] += y in ins and p != y
        if p != y and (p or y in diz): err.append({"cig": e["cig"], "strato": s, "lente": p, "etichetta": y, "testo": testi[e["cig"]]["testo"][:200]})
    N = dis["dimensione_strati"]
    out = {"disegno": dis, "per_strato": {s: dict(c) for s, c in sorted(per.items())}}
    for nome in ("bt", "diz"):
        tp = sum(c[nome + "_tp"] for c in per.values()); fp = sum(c[nome + "_fp"] for c in per.values()); fn = sum(c[nome + "_fn"] for c in per.values())
        w = {s: N[s] / per[s]["n"] for s in per}
        tpw = sum(per[s][nome + "_tp"] * w[s] for s in per); fpw = sum(per[s][nome + "_fp"] * w[s] for s in per); fnw = sum(per[s][nome + "_fn"] * w[s] for s in per)
        out["bigtech_usa" if nome == "bt" else "tutti_i_provider"] = {
            "campione": {"tp": tp, "fp": fp, "fn": fn, "precisione": round(tp / (tp + fp), 3) if tp + fp else None, "precisione_w95": wilson(tp, tp + fp),
                         "richiamo": round(tp / (tp + fn), 3) if tp + fn else None, "richiamo_w95": wilson(tp, tp + fn)},
            "pesato_universo": {"precisione": round(tpw / (tpw + fpw), 3) if tpw + fpw else None, "richiamo": round(tpw / (tpw + fnw), 3) if tpw + fnw else None,
                                "cig_stimati_veri_positivi": round(tpw), "cig_stimati_falsi_positivi": round(fpw), "cig_stimati_mancati": round(fnw)}}
    out["errori"] = err
    out["nota"] = "riferimento = lettura umana del solo oggetto; negli strati S0/S5 (314 mila CIG) 0 menzioni su 80: il richiamo pesato ha incertezza alta"
    o = R / f"esiti/{datetime.date.today().isoformat()}/lente-prodotto"; os.makedirs(o, exist_ok=True)
    json.dump(out, open(o / (D.name + ".json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in out.items() if k != "disegno"}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
