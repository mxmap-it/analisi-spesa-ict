"""Verifica «Imbuto: via 6 su G1 e sui primi 1.000 G3» (#55 #66, decisione di Fabio del 7/11/2026).

Ingressi versionati (riproducibile da un clone, nessun dato grezzo):
  report/metodo/llm/imbuto-g1g3/selezione.json, lotti/, verificati.jsonl   (tools/llm/imbuto_lotti.py, verifica_imbuto.py)
  dati/classificazioni/campione-v3.jsonl                                   (riferimento del campione 611, per la precisione)
  stato/claude-consumi.jsonl                                               (consumo per etichetta imbuto-g1/g3/ctl)
Stampa e scrive (--json OUT) per gruppo: CIG ed euro per stato degli assi A e B, euro spostati di strato (PROPOSTE da revisionare),
precisione sul campione di controllo (Wilson 95 %), consumo reale contro la stima (360 USD-eq per 1.000 G3).
Uso: python tools/verifiche/imbuto_via6.py [--json esiti/<data>/imbuto/via6-g1g3.json]
"""
import collections, json, math, sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]
B = R / "report/metodo/llm/imbuto-g1g3"


def wilson(k, n, z=1.96):
    if not n: return None
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - m, 3), round(c + m, 3)]


def jl(p):
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


def main():
    lotti = {c["cig"]: c for f in sorted((B / "lotti").glob("*.jsonl")) for c in jl(f)}
    ver = {v["cig"]: v for v in jl(B / "verificati.jsonl")}
    sel = json.loads((B / "selezione.json").read_text(encoding="utf-8"))
    T = {"selezione": {k: sel[k] for k in ("g1", "g3", "ctl")}, "per_gruppo": {}, "spostamenti": {}}
    agg = lambda: collections.defaultdict(lambda: [0, 0.0])
    for g in ("G1", "G3", "CTL"):
        tot = [c for c in lotti.values() if c["gruppo"] == g]
        fatti = [c for c in tot if c["cig"] in ver]
        st, sp = agg(), agg()
        for c in fatti:
            v = ver[c["cig"]]; a, b = v["asse_a"]["stato"], v["asse_b"]["stato"]
            st[f"A:{a} | B:{b}"][0] += 1; st[f"A:{a} | B:{b}"][1] += c["importo"]
            if a == "escluso-certo": k = "escluso certo non ICT -> S1 (proposta via 6)" if v["asse_a"].get("ict") == "n" else "escluso certo dal cloud, ICT -> S5 (proposta via 6)"
            elif a == "incluso-certo" and b == "incluso-certo": k = f"incluso certo cloud, giurisdizione {v['asse_b'].get('giurisdizione')} (proposta via 6)"
            elif a == "incluso-certo": k = "incluso certo cloud, giurisdizione incerta (proposta via 6)"
            else: k = "resta incerto (S6)"
            sp[k][0] += 1; sp[k][1] += c["importo"]
        conf = collections.Counter(ver[c["cig"]]["confidenza"] for c in fatti)
        T["per_gruppo"][g] = {"cig_totali": len(tot), "euro_totali": round(sum(c["importo"] for c in tot)), "cig_classificati": len(fatti),
                              "euro_classificati": round(sum(c["importo"] for c in fatti)), "confidenza": dict(conf),
                              "fonte_primaria": sum(ver[c["cig"]]["fonte_primaria"] for c in fatti),
                              "con_documento_archiviato": sum(ver[c["cig"]]["verifica"]["documenti_archiviati"] > 0 for c in fatti),
                              "stati": {k: {"cig": v[0], "euro": round(v[1])} for k, v in sorted(st.items())}}
        T["spostamenti"][g] = {k: {"cig": v[0], "euro": round(v[1])} for k, v in sorted(sp.items())}
    # precisione sul campione di controllo (campione 611): asse A = è cloud?; asse B = giurisdizione, solo dove entrambe determinate
    rif = {d["cig"]: d["esito"] for d in jl(R / "dati/classificazioni/campione-v3.jsonl")}
    pa = pb = na = nb = 0; dis = []
    pac = nac = 0
    for cig, v in ver.items():
        if cig not in rif: continue
        e = rif[cig]; nuovo = v["asse_a"].get("e_cloud"); vecchio = e.get("e_cloud")
        if nuovo in ("s", "n") and vecchio in ("s", "n"):
            na += 1; pa += nuovo == vecchio
            if v["asse_a"]["stato"] != "incerto": nac += 1; pac += nuovo == vecchio
            if nuovo != vecchio: dis.append({"cig": cig, "asse": "A", "via6_p3": nuovo, "riferimento": vecchio})
        gn, gv = v["asse_b"].get("giurisdizione"), e.get("giurisdizione")
        if gn in ("IT", "UE", "EXTRA-UE") and gv in ("IT", "UE", "EXTRA-UE"):
            nb += 1; pb += gn == gv
            if gn != gv: dis.append({"cig": cig, "asse": "B", "via6_p3": gn, "riferimento": gv})
    T["precisione_controllo"] = {"riferimento": "dati/classificazioni/campione-v3.jsonl (via 6 p1/p2 + regole, non verità assoluta)",
                                 "asse_a": {"accordo": pa, "n": na, "wilson95": wilson(pa, na)},
                                 "asse_a_solo_stati_certi": {"accordo": pac, "n": nac, "wilson95": wilson(pac, nac)},
                                 "asse_b": {"accordo": pb, "n": nb, "wilson95": wilson(pb, nb)}, "disaccordi": dis}
    # ostacoli incontrati (per R51): tipo e dominio
    ost, dom = collections.Counter(), collections.Counter()
    for v in ver.values():
        for o in v.get("ostacoli") or []:
            if isinstance(o, dict):
                ost[o.get("tipo", "altro")] += 1; dom[(o.get("url") or "").split("/")[2] if (o.get("url") or "").count("/") >= 2 else ""] += 1
    T["ostacoli"] = {"cig_con_ostacoli": sum(bool(v.get("ostacoli")) for v in ver.values()), "per_tipo": dict(ost.most_common()), "domini_principali": dict(dom.most_common(15))}
    cons = collections.defaultdict(lambda: [0, 0.0])
    for r in jl(R / "stato/claude-consumi.jsonl"):
        if str(r.get("etichetta", "")).startswith(("imbuto-", "riproduzione-")):
            cons[r["etichetta"]][0] += 1; cons[r["etichetta"]][1] += r.get("costo_usd_equivalente") or 0
    n3 = T["per_gruppo"]["G3"]["cig_classificati"]
    T["consumo"] = {k: {"chiamate": v[0], "usd_eq": round(v[1], 2)} for k, v in sorted(cons.items())}
    T["consumo"]["g3_stima"] = {"stima_1000": 360, "limite_+20%": 432, "per_cig": round(cons["imbuto-g3"][1] / n3, 3) if n3 else None,
                               "proiezione_1000": round(cons["imbuto-g3"][1] / n3 * 1000, 1) if n3 else None}
    fmt = lambda x: f"{x:,.0f}".replace(",", ".")
    for g, d in T["per_gruppo"].items():
        print(f"\n## {g}: {d['cig_classificati']}/{d['cig_totali']} CIG, {fmt(d['euro_classificati'])}/{fmt(d['euro_totali'])} €; confidenza {d['confidenza']}; fonte primaria {d['fonte_primaria']}")
        for k, v in T["spostamenti"][g].items(): print(f"  {k}: {v['cig']} CIG, {fmt(v['euro'])} €")
    print("\n## precisione", {k: v for k, v in T["precisione_controllo"].items() if k != "disaccordi"})
    print("## ostacoli", T["ostacoli"]["per_tipo"])
    print("## consumo", T["consumo"])
    if "--json" in sys.argv:
        o = Path(sys.argv[sys.argv.index("--json") + 1]); o.parent.mkdir(parents=True, exist_ok=True)
        o.write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
