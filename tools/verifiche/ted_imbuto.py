"""#27 / #66 I vincitori TED dei CIG senza aggiudicatari ANAC (esiti/*/mirror/ted-esiti.csv, tools/verifiche/ted_esiti.py) nell'imbuto:
in quale strato/gruppo/via cadono (lavoro/imbuto/ict.csv), con quale importo, e che cosa cambia la P.IVA TED per la lente
fornitore (vincitore = produttore? rivenditore?). Non modifica l'imbuto: produce un esito da integrare (decide chi cura l'imbuto, #66).

Uso (server): nice .venv/bin/python tools/verifiche/ted_imbuto.py -> esiti/<oggi>/imbuto/ted-vincitori.{json,csv}"""
import csv, glob, json, os, datetime, collections
from pathlib import Path

R = Path(__file__).resolve().parents[2]


def main():
    csv.field_size_limit(10 ** 8)
    te = sorted(glob.glob(str(R / "esiti/*/mirror/ted-esiti.csv")))[-1]
    ted = {}
    for r in csv.DictReader(open(te, encoding="utf-8")):
        if r["vincitore_ted"]: ted.setdefault(r["cig"], r)
    imb = {}
    for r in csv.DictReader(open(R / "lavoro/imbuto/ict.csv", encoding="utf-8")):
        if r["cig"] in ted: imb[r["cig"]] = r
    st = collections.Counter(); eur = collections.Counter(); righe = []
    for cig, t in ted.items():
        r = imb.get(cig); s = (r["strato"] + "/" + (r.get("gruppo") or "")) if r else "fuori ict.csv (escluso S1 o anno < 2020)"
        imp = float(r["importo"] or 0) if r else 0.0
        st[s] += 1; eur[s] += imp
        righe.append({"cig": cig, "strato_gruppo": s, "via": r["via"] if r else "", "provider": r["provider"] if r else "",
                      "importo_anac": imp, "aggiudicatari_ict_csv": r["aggiudicatari"] if r else "",
                      "vincitore_ted": t["vincitore_ted"], "piva_ted": t["piva_ted"], "valore_ted": t["valore_ted"], "avviso_ted": t["avviso_ted"]})
    out = {"ingresso": [te, "lavoro/imbuto/ict.csv"], "cig_con_vincitore_ted": len(ted), "nell_imbuto": len(imb),
           "per_strato_gruppo": {k: {"cig": v, "importo_anac": round(eur[k])} for k, v in st.most_common()},
           "nota": "esito da integrare nell'imbuto (#66): il vincitore TED colma il campo aggiudicatari mancante in ANAC"}
    o = R / f"esiti/{datetime.date.today().isoformat()}/imbuto"; os.makedirs(o, exist_ok=True)
    json.dump(out, open(o / "ted-vincitori.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    with open(o / "ted-vincitori.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(righe[0])); w.writeheader(); w.writerows(righe)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
