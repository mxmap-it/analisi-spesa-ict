"""#40 Misura a cieco della lente prodotto DOPO le regole del 9/11/2026 (commit 9ba5ad88), quarto campione.

Ingressi (committati): report/metodo/lente-cieco-4/{campione-cieco.csv, strati.csv, disegno.json, etichette.csv,
etichette.csv.sha256}. Le etichette sono state fissate e committate (0818f6fb) prima di eseguire questo confronto;
lo script verifica lo sha256 e si ferma se non coincide.
Uscita del classificatore: classifica.py (Classificatore.classifica: vie 1, 2, 3, 5) con le regole CORRENTI.
Misure: precisione e richiamo, in numero di CIG e in euro (importo_lotto), con intervalli di Wilson al 95 %, per
strato e in totale, su tre insiemi: big tech USA, tutto l'extra-UE del dizionario, tutti i provider del dizionario;
stima pesata sull'universo (N_h / n_h). Errori elencati per classe (marchio sbagliato, marchio senza prodotto, mancato).
Uso: python tools/verifiche/lente_cieco4.py -> esiti/<oggi>/lente-cieco-4/misura.json, errori.csv"""
import csv, json, os, sys, hashlib, datetime, collections
from pathlib import Path

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/analisi")); sys.path.insert(0, str(R / "tools/verifiche"))
from classifica import Classificatore, NOME_CANONICO  # noqa: E402
from lente_prodotto import BIGTECH_USA, wilson  # noqa: E402

D = R / "report/metodo/lente-cieco-4"


def main():
    atteso = open(D / "etichette.csv.sha256").read().split()[0]
    if hashlib.sha256(open(D / "etichette.csv", "rb").read()).hexdigest() != atteso: sys.exit("sha256 delle etichette diverso")
    c = Classificatore()
    diz = {NOME_CANONICO.get(m["provider"], m["provider"]) for m in c.marchi}
    extra = {p for p in diz if c.giur.get(p) == "EXTRA-UE"}
    insiemi = {"bigtech_usa": set(BIGTECH_USA), "extra_ue": extra, "tutti_i_provider": diz}
    dis = json.load(open(D / "disegno.json", encoding="utf-8"))
    camp = {r["cig"]: r for r in csv.DictReader(open(D / "campione-cieco.csv", encoding="utf-8"))}
    strato = {r["cig"]: r["strato"] for r in csv.DictReader(open(D / "strati.csv", encoding="utf-8"))}
    cnt = {k: collections.defaultdict(collections.Counter) for k in insiemi}
    eur = {k: collections.defaultdict(collections.Counter) for k in insiemi}
    nh = collections.Counter(); err = []
    for e in csv.DictReader(open(D / "etichette.csv", encoding="utf-8")):
        r = camp[e["cig"]]; s = strato[e["cig"]]; nh[s] += 1
        ag = [a.strip() for a in r["aggiudicatari"].split(";") if a.strip()]
        k = c.classifica(r["testo"], r["cig_accordo_quadro"], ag, r["cod_cpv"]) or {"provider": "", "via": "fuori-perimetro"}
        p, y = k["provider"], e["etichetta_prodotto"]; x = float(r["importo"] or 0)
        for nome, ins in insiemi.items():
            for cl, v in (("tp", p in ins and p == y), ("fp", p in ins and p != y), ("fn", y in ins and p != y)):
                cnt[nome][s][cl] += v; eur[nome][s][cl] += x * v
        if p != y and (p in diz or y in diz):
            classe = "mancato" if not p else ("marchio sbagliato" if y in diz else "marchio senza prodotto del dizionario")
            err.append({"cig": e["cig"], "strato": s, "classe": classe, "lente": p, "via": k.get("via", ""), "regola": k.get("regola", ""),
                        "etichetta": y, "nota_etichetta": e["nota"], "importo": x, "testo": r["testo"][:300]})
    N = dis["dimensione_strati"]; out = {"disegno": dis, "etichette_sha256": atteso, "n_per_strato": dict(nh)}

    def misura(tp, fp, fn, dec=3):
        return {"tp": round(tp), "fp": round(fp), "fn": round(fn), "precisione": round(tp / (tp + fp), dec) if tp + fp else None,
                "richiamo": round(tp / (tp + fn), dec) if tp + fn else None}
    for nome in insiemi:
        o = {"per_strato": {}}
        for s in sorted(nh):
            m = misura(*(cnt[nome][s][k] for k in ("tp", "fp", "fn")))
            m["precisione_w95"] = wilson(m["tp"], m["tp"] + m["fp"]); m["richiamo_w95"] = wilson(m["tp"], m["tp"] + m["fn"])
            m["euro"] = misura(*(eur[nome][s][k] for k in ("tp", "fp", "fn"))); o["per_strato"][s] = m
        t = misura(*(sum(cnt[nome][s][k] for s in nh) for k in ("tp", "fp", "fn")))
        t["precisione_w95"] = wilson(t["tp"], t["tp"] + t["fp"]); t["richiamo_w95"] = wilson(t["tp"], t["tp"] + t["fn"])
        t["euro"] = misura(*(sum(eur[nome][s][k] for s in nh) for k in ("tp", "fp", "fn")))
        o["campione"] = t
        w = {s: N[s] / nh[s] for s in nh}
        o["pesato_universo"] = misura(*(sum(cnt[nome][s][k] * w[s] for s in nh) for k in ("tp", "fp", "fn")))
        o["pesato_universo"]["euro"] = misura(*(sum(eur[nome][s][k] * w[s] for s in nh) for k in ("tp", "fp", "fn")))
        out[nome] = o
    out["errori_per_classe"] = dict(collections.Counter(x["classe"] for x in err)); out["errori"] = err
    o = R / f"esiti/{datetime.date.today().isoformat()}/lente-cieco-4"; os.makedirs(o, exist_ok=True)
    json.dump(out, open(o / "misura.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    with open(o / "errori.csv", "w", encoding="utf-8", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(err[0]) if err else ["cig"]); wr.writeheader(); wr.writerows(err)
    print(json.dumps({k: v for k, v in out.items() if k not in ("disegno", "errori")}, indent=1, ensure_ascii=False))
    for x in err: print(x["cig"], x["strato"], x["classe"], x["lente"], "<>", x["etichetta"], x["via"], "|", x["testo"][:140])


if __name__ == "__main__":
    main()
