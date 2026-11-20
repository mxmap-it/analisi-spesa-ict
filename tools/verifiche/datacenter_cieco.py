#!/usr/bin/env python3
"""Precisione delle regole del cloud in proprio su campione a cieco (#52). Versione 0.1 (20/11/2026).

Ogni campione sta in esiti/<data>/imbuto/datacenter/cieco<N>/: campione.csv (testi senza la nostra etichetta),
chiave.csv (CIG, gruppo di estrazione, famiglia, euro netti), etichette.csv (etichetta del valutatore cieco, un agente
Claude Sonnet senza accesso alla chiave). Gruppi: «dc-casuale» (estrazione semplice: precisione per numero di contratti),
«dc-pesato-euro» (estrazione con probabilità proporzionale agli euro: la quota di DC stima la precisione pesata in euro),
«misto-non-contato» (contratti lasciati incerti: quanta parte sarebbe DC, cioè cosa perdiamo), «servizio-inhouse».
Gli INDETERMINATO si tolgono dal denominatore. Intervallo di Wilson al 95 %.

Uso: python3 tools/verifiche/datacenter_cieco.py esiti/2026-11-20/imbuto/datacenter/cieco1 [...]
"""
import collections, csv, json, math, os, sys

GIUSTE = {"dc-casuale": {"DC"}, "dc-pesato-euro": {"DC"}, "misto-non-contato": {"DC"}, "servizio-inhouse": {"INHOUSE", "DC"}}


def wilson(x, n, z=1.96):
    if not n:
        return None
    p = x / n; d = 1 + z * z / n; m = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(100 * (m - h), 1), round(100 * (m + h), 1)]


def misura(cart):
    k = {r["id"]: r for r in csv.DictReader(open(os.path.join(cart, "chiave.csv"), encoding="utf-8"))}
    e = {r["id"]: r["etichetta"].strip() for r in csv.DictReader(open(os.path.join(cart, "etichette.csv"), encoding="utf-8"))}
    c = collections.defaultdict(collections.Counter)
    errori = collections.Counter()
    for i, r in k.items():
        c[r["gruppo"]][e[i]] += 1
        if r["gruppo"] != "misto-non-contato" and e[i] not in GIUSTE[r["gruppo"]] | {"INDETERMINATO"}:
            errori[(r["famiglia"], e[i])] += 1
    out = {"campione": cart, "gruppi": {}}
    for g, cc in c.items():
        det = sum(cc.values()) - cc["INDETERMINATO"]
        ok = sum(cc[x] for x in GIUSTE[g])
        out["gruppi"][g] = {"etichette": dict(cc), "giuste": ok, "determinati": det,
                            "quota_pct": round(100 * ok / det, 1) if det else None, "wilson95": wilson(ok, det)}
    out["errori_per_famiglia"] = [[f, l, n] for (f, l), n in errori.most_common()]
    return out


if __name__ == "__main__":
    print(json.dumps([misura(c) for c in sys.argv[1:]], ensure_ascii=False, indent=1))
