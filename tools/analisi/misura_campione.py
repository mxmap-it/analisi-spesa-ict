"""Misura della precisione del classificatore su un campione annotato alla cieca (metodo, "Verifica umana a campione").
Confronta l'esito automatico (campione-<nome>.csv) con una o due annotazioni umane (copie cieche compilate).
Uso: python tools/analisi/misura_campione.py report/metodo/campione-misura-v3.csv annotazione-A.csv [annotazione-B.csv]
Esce un JSON con: precisione per via (provider, giurisdizione, provider+tipo), richiamo (cloud sfuggito fra i non attribuiti),
accordo fra annotatori (kappa di Cohen sulla giurisdizione) e l'elenco dei disaccordi da risolvere."""
import collections, csv, json, sys

COL_SERV = "servizio (cloud/licenza/servizi-professionali/psn/in-house/altro)"
COL_GIUR = "giurisdizione (IT/UE/EXTRA-UE)"

def leggi(f):
    return {r["cig"]: r for r in csv.DictReader(open(f, encoding="utf-8"))}

def norm(s):
    return (s or "").strip().lower()

def kappa(a, b):
    n = len(a)
    if not n: return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = collections.Counter(a), collections.Counter(b)
    pe = sum(ca[k] * cb[k] for k in ca) / (n * n)
    return round((po - pe) / (1 - pe), 3) if pe < 1 else 1.0

def main(auto_f, *ann_f):
    auto = leggi(auto_f)
    anns = [leggi(f) for f in ann_f]
    a = anns[0]
    per_via = collections.defaultdict(collections.Counter)
    for cig, r in auto.items():
        h = a.get(cig)
        if not h or not norm(h["e_cloud (s/n)"]): continue  # non ancora annotata
        via = r["via"][:1]
        c = per_via[via]
        c["annotate"] += 1
        if via in "12345" and r["provider"]:
            c["attribuite"] += 1
            c["provider_ok"] += norm(h["provider_prodotto"]) == norm(r["provider"])
            c["giurisdizione_ok"] += norm(h[COL_GIUR]) == norm(r.get("giurisdizione", ""))
            c["provider_e_tipo_ok"] += norm(h["provider_prodotto"]) == norm(r["provider"]) and norm(h[COL_SERV]) == norm(r["servizio"])
        else:
            c["non_attribuite"] += 1
            c["cloud_sfuggito"] += norm(h["e_cloud (s/n)"]) == "s" and bool(norm(h["provider_prodotto"]))
    out = {"campione": auto_f, "annotazioni": list(ann_f), "per_via": {}}
    tot = collections.Counter()
    for via, c in sorted(per_via.items()):
        tot.update(c)
        d = dict(c)
        if c["attribuite"]:
            for k in ("provider_ok", "giurisdizione_ok", "provider_e_tipo_ok"):
                d["precisione_" + k[:-3]] = round(100 * c[k] / c["attribuite"], 1)
        out["per_via"][via] = d
    if tot["attribuite"]:
        out["precisione_provider"] = round(100 * tot["provider_ok"] / tot["attribuite"], 1)
        out["precisione_giurisdizione"] = round(100 * tot["giurisdizione_ok"] / tot["attribuite"], 1)
        out["precisione_provider_e_tipo"] = round(100 * tot["provider_e_tipo_ok"] / tot["attribuite"], 1)
    if tot["non_attribuite"]:
        out["quota_cloud_sfuggito"] = round(100 * tot["cloud_sfuggito"] / tot["non_attribuite"], 1)
    if len(anns) > 1:
        comuni = [c for c in anns[0] if c in anns[1] and norm(anns[0][c][COL_GIUR]) and norm(anns[1][c][COL_GIUR])]
        ga = [norm(anns[0][c][COL_GIUR]) for c in comuni]; gb = [norm(anns[1][c][COL_GIUR]) for c in comuni]
        out["doppia_annotazione"] = {"righe": len(comuni), "kappa_giurisdizione": kappa(ga, gb),
                                     "disaccordi": [c for c, x, y in zip(comuni, ga, gb) if x != y]}
    print(json.dumps(out, indent=1, ensure_ascii=False))

if __name__ == "__main__":
    main(*sys.argv[1:])
