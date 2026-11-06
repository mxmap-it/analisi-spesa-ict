"""Verifica «Censimento EA Microsoft e licenze Oracle» (#66, rendiconto 0.7).

1. Microsoft: atti di adesione agli EA Consip con il dettaglio dei prodotti (esiti/2026-11-06/imbuto/ea-campione.csv,
   un atto per riga, con URL e sha256 del PDF archiviato e il metodo con cui è calcolata la quota cloud). Confine
   R-S5 (report/convenzioni/ea-quota-cloud-elaborazione.md): cloud = abbonamento a un servizio erogato da Microsoft
   (M365/O365, Dynamics 365, EMS, Copilot, Azure); licenze perpetue, SA, Windows/SQL Server, CAL = on premises.
   Il campione NON è casuale: sono gli atti che la ricerca ha trovato (soprattutto enti piccoli), più MAECI fra i
   primi 50 EA per importo. Si calcolano la quota per atto, la quota pesata e la quota di atti a prevalenza cloud
   (intervallo di Wilson), e la forbice che ne deriva sul residuo Microsoft di imbuto_licenze.py.
2. Oracle: primi 20 incerti per importo, decisione sull'oggetto (supporto, rinnovo, manutenzione, Exadata, ULA =
   prodotti installati; «cloud», OCI = cloud). Non è certo: nessun atto letto.
Uso: python tools/verifiche/ea_censimento.py [--json OUT]
"""
import csv, json, math, os, re, sys

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.normpath(os.path.join(QUI, "..", ".."))
E = os.path.join(RADICE, "esiti/2026-11-06/imbuto")
leggi = lambda n: list(csv.DictReader(open(os.path.join(E, n), encoding="utf-8")))


def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return round(c - h, 3), round(c + h, 3)


def main():
    A = leggi("ea-campione.csv"); L = leggi("licenze-cig.csv")
    q = [float(a["quota_cloud"]) for a in A]
    pes = [(float(a["euro_atto"]), float(a["quota_cloud"])) for a in A if a["euro_atto"]]
    k = sum(x >= 0.5 for x in q)
    ms = sorted([r for r in L if r["provider"] == "Microsoft" and r["asse_a"] in ("incerto", "misto")], key=lambda r: -float(r["euro_netti"]))
    eur = sum(float(r["euro_netti"]) for r in ms)
    lo, hi = wilson(k, len(q))
    trovati = [a for a in A if a["cig_imbuto"]]
    T = {"microsoft": {"atti_letti": len(A), "fra_i_primi_50": len(trovati), "euro_primi_50_coperti": round(sum(float(r["euro_netti"]) for r in ms[:50] if r["cig"] in {a["cig_imbuto"] for a in trovati})),
                       "quota_media_per_atto": round(sum(q) / len(q), 3), "quota_pesata": round(sum(e * x for e, x in pes) / sum(e for e, _ in pes), 3),
                       "atti_prevalenza_cloud": k, "wilson95": (lo, hi), "residuo_incerto_euro": round(eur),
                       "forbice_cloud_euro": (round(eur * lo), round(eur * hi)),
                       "nota": "campione non casuale; la forbice vale solo se gli atti trovati sono rappresentativi"}}
    ora = sorted([r for r in L if r["provider"] == "Oracle" and r["asse_a"] in ("incerto", "misto")], key=lambda r: -float(r["euro_netti"]))[:20]
    dec = []
    for r in ora:
        t = r["testo"]
        if re.search(r"\b(cloud|oci|saas)\b", t, re.I): d = "cloud (testo)"
        elif re.search(r"support|manutenz|rinnov|exadata|\bula\b|assistenz|licenz", t, re.I): d = "on premises probabile (testo: supporto/rinnovo/licenze)"
        else: d = "non determinabile dal testo"
        dec.append({"cig": r["cig"], "euro": round(float(r["euro_netti"])), "decisione": d, "testo": t[:120]})
    T["oracle_primi_20"] = {"euro": sum(x["euro"] for x in dec), "per_decisione": {d: sum(x["euro"] for x in dec if x["decisione"] == d) for d in {x["decisione"] for x in dec}}, "cig": dec}
    # 0.8: atti Oracle letti (oracle-campione.csv; uno dei primi 20, CINECA, da PortaleAppalti via piattaforme_cig.py)
    if os.path.exists(os.path.join(E, "oracle-campione.csv")):
        O = leggi("oracle-campione.csv"); c = sum(o["cloud"] == "si" for o in O)
        T["oracle_atti_letti"] = {"atti": len(O), "con_cloud": c, "wilson95_quota_atti_cloud": wilson(c, len(O)),
                                  "fra_i_primi_20": sum(1 for o in O if o["cig_imbuto"]), "cig": [o["cig_imbuto"] for o in O if o["cig_imbuto"]]}
    print(json.dumps(T, ensure_ascii=False, indent=1))
    if "--json" in sys.argv: json.dump(T, open(sys.argv[sys.argv.index("--json") + 1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
