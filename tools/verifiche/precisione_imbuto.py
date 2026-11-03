"""Precisione degli strati dell'imbuto sul campione v3 (611 CIG classificati con la via 6 e revisione).

Riferimento: esito del campione (dati/classificazioni/campione-v3.jsonl). Non è una verità assoluta: è la
classificazione più approfondita che abbiamo (modello + atti, revisione); le righe con fonte primaria si contano a parte.
Per ogni strato: quanti CIG del campione vi cadono, quanti sono d'accordo sull'asse A (è cloud?) e, per gli inclusi,
sull'asse B (giurisdizione), con intervallo di Wilson al 95%. I CIG del campione assenti da ict.csv sono stati
esclusi in S1 o sotto soglia: si controlla che il riferimento non li dica cloud (falsi esclusi).

Uso: python tools/verifiche/precisione_imbuto.py [lavoro/imbuto/ict.csv] -> esiti/<oggi>/imbuto/precisione.json"""
import csv, json, math, os, sys, collections, datetime


def wilson(k, n, z=1.96):
    if not n: return None
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - m, 3), round(c + m, 3)]


def main(ict="lavoro/imbuto/ict.csv"):
    rif = {}
    for l in open("dati/classificazioni/campione-v3.jsonl", encoding="utf-8"):
        d = json.loads(l); rif[d["cig"]] = d["esito"]
    imb = {}
    csv.field_size_limit(10 ** 7)
    for r in csv.DictReader(open(ict, encoding="utf-8")):
        if r["cig"] in rif: imb[r["cig"]] = r
    stat = collections.defaultdict(lambda: collections.Counter())
    for cig, e in rif.items():
        r = imb.get(cig)
        s = r["strato"] if r else "S1/S2-escluso"
        c = stat[s]; c["n"] += 1; c["primaria"] += bool(e.get("fonte_primaria"))
        cloud = e.get("e_cloud") == "s"
        if s.startswith(("S3", "S4")):
            c["a_ok"] += cloud or e.get("servizio") in ("licenza", "in-house", "software-infrastruttura")
            if e.get("giurisdizione") in ("IT", "UE", "EXTRA-UE"):
                c["b_n"] += 1; c["b_ok"] += e["giurisdizione"] == r["giurisdizione"]
        elif s.startswith(("S1", "S2", "S5")):
            c["a_ok"] += not cloud
        else:
            c["cloud_rif"] += cloud
    out = {}
    for s, c in sorted(stat.items()):
        o = {"n": c["n"], "con_fonte_primaria": c["primaria"]}
        if not s.startswith("S6"):
            o["asse_a_accordo"] = c["a_ok"]; o["asse_a_wilson95"] = wilson(c["a_ok"], c["n"])
        if c["b_n"]:
            o["asse_b_n"] = c["b_n"]; o["asse_b_accordo"] = c["b_ok"]; o["asse_b_wilson95"] = wilson(c["b_ok"], c["b_n"])
        if s.startswith("S6"): o["cloud_secondo_riferimento"] = c["cloud_rif"]
        out[s] = o
    oggi = datetime.date.today().isoformat()
    os.makedirs(f"esiti/{oggi}/imbuto", exist_ok=True)
    res = {"riferimento": "dati/classificazioni/campione-v3.jsonl", "imbuto": ict, "strati": out,
           "nota": "campione stratificato v3, non casuale sull'universo: la precisione vale per strato, non si riporta all'universo senza pesi"}
    json.dump(res, open(f"esiti/{oggi}/imbuto/precisione.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(*sys.argv[1:])
