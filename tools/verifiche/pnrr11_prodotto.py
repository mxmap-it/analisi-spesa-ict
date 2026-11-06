"""#43 Misura 1.1 dai decreti: i CIG dei 312 CUP finanziati (esiti/2026-11-06/pnrr11/cup-cig.csv, da pnrr11_cup_cig.py)
attribuiti per prodotto con la stessa attribuzione v3 (lavoro/attribuzione/[0-9]*.csv; per i CIG assenti, il
Classificatore sul testo di lavoro/imbuto/ict.csv). Quanto va a prodotti delle big tech USA, quanto al PSN, quanto è
padre di AQ o importo da verificare. Importi = importo del CIG, non il finanziamento.

Uso (server): nice .venv/bin/python tools/verifiche/pnrr11_prodotto.py -> esiti/<oggi>/pnrr/pnrr11-prodotto.{json,csv}"""
import csv, glob, json, os, sys, datetime, collections
from pathlib import Path

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/analisi"))
from classifica import Classificatore  # noqa: E402
BIGTECH = {"Microsoft", "Amazon Web Services", "Google", "Oracle", "IBM", "Salesforce", "ServiceNow", "Adobe", "Zoom",
           "Cisco Webex", "Cloudera", "VMware"}


def main(cupcig="esiti/2026-11-06/pnrr11/cup-cig.csv"):
    csv.field_size_limit(10 ** 8)
    righe = list(csv.DictReader(open(R / cupcig, encoding="utf-8")))
    cigs = {r["cig"] for r in righe if r["cig"]}
    att = {}
    for f in sorted(glob.glob(str(R / "lavoro/attribuzione/[0-9]*.csv"))):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            if r["cig"] in cigs: att[r["cig"]] = r
    cl = Classificatore(); imb = {}
    for r in csv.DictReader(open(R / "lavoro/imbuto/ict.csv", encoding="utf-8")):
        if r["cig"] in cigs and r["cig"] not in att: imb[r["cig"]] = r
    tot = collections.defaultdict(collections.Counter); fuori = collections.Counter(); visti = set(); out_r = []
    for r in righe:
        if not r["cig"] or r["cig"] in visti: continue
        visti.add(r["cig"]); imp = float(r["importo_cig"] or 0)
        if r["cig"] in att:
            a = att[r["cig"]]; prov, giu, serv, fonte = a["provider"], a["giurisdizione"], a["servizio"], "attribuzione-v3"
            padre, dav = a["e_padre"] == "1", bool(a.get("importo_da_verificare"))
        elif r["cig"] in imb:
            a = imb[r["cig"]]; k = cl.classifica(a["testo"], aggiudicatari=a["aggiudicatari"].split(";"), cpv=a["cod_cpv"]) or {}
            prov, giu, serv, fonte, padre, dav = k.get("provider", ""), k.get("giurisdizione", ""), k.get("servizio", ""), "classificatore-su-ict.csv", False, bool(a.get("importo_da_verificare"))
        else:
            prov = giu = serv = ""; fonte = "fuori-perimetro-ict"; padre = dav = False
        if fonte == "fuori-perimetro-ict": fuori["cig"] += 1; fuori["eur"] += imp; cat = "fuori-perimetro-ict"
        elif padre or dav: cat = "padre-o-da-verificare"
        elif prov in BIGTECH: cat = "bigtech_usa"
        elif prov == "Polo Strategico Nazionale": cat = "PSN"
        elif prov: cat = giu or "?"
        else: cat = "senza_provider"
        tot[cat]["cig"] += 1; tot[cat]["eur"] += imp
        out_r.append({"cup": r["cup"], "cig": r["cig"], "importo_cig": imp, "categoria": cat, "provider": prov, "servizio": serv, "fonte": fonte})
    contati = sum(v["eur"] for k, v in tot.items() if k not in ("fuori-perimetro-ict", "padre-o-da-verificare"))
    out = {"ingresso": cupcig, "cup": len({r["cup"] for r in righe}), "cup_con_cig": len({r["cup"] for r in righe if r["cig"]}),
           "cig_distinti": len(visti), "per_categoria": {k: {"cig": v["cig"], "importo": round(v["eur"])} for k, v in sorted(tot.items())},
           "importo_ict_contato": round(contati),
           "quota_bigtech_sul_contato": round(tot["bigtech_usa"]["eur"] / contati, 4) if contati else None,
           "quota_psn_sul_contato": round(tot["PSN"]["eur"] / contati, 4) if contati else None}
    o = R / f"esiti/{datetime.date.today().isoformat()}/pnrr"; os.makedirs(o, exist_ok=True)
    json.dump(out, open(o / "pnrr11-prodotto.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    with open(o / "pnrr11-prodotto.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_r[0])); w.writeheader(); w.writerows(out_r)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(*sys.argv[1:])
