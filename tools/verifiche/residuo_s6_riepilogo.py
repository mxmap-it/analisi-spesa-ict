#!/usr/bin/env python3
"""#57 Riepilogo finale dell'acquisizione documenti sul residuo S6 fuori dalla via 6: L3 (link PVL), MePA, L4 (AT),
L4-js (#73: ripasso con browser headless degli enti L4 «pagina-quasi-vuota-js», at_cig_js.py).

Rifà da zero i numeri pubblicati in sito/content/progetto/acquisizione-documenti.md §«Residuo S6: misure finali».
Ingressi (server, lavoro/residuo-s6/): ingresso.csv, out/esiti.jsonl (L3 e MePA, l'ultima riga per CIG vale),
l4/enti.jsonl e l4/esiti.jsonl (L4, at_cig.py), l4-js/enti.jsonl e l4-js/esiti.jsonl (L4-js),
dati/atti/atti-server.jsonl (atti spesaict.atto/1 registrati). L4-js è un livello separato: conta solo i CIG che non
hanno già una riga L4 (nessun doppio conteggio; le sovrapposizioni si contano in «l4js_sovrapposti_l4»).
I documenti L4 e L4-js passano per at_cig.filtra_documenti (#73): fogli di stile, script, font e immagini non contano;
quante righe cambiano è in «filtro_non_documenti».
Ogni CIG ha un solo livello: il primo che trova un documento che cita il CIG (L3 prima di L4); i conteggi «trovato»
e «con documento» sono per livello e possono sovrapporsi solo se lo stesso CIG ha link PVL e voce L4 (non accade:
L4 lavora solo sui CIG senza link).
Uscite: esiti/<DATA>/acquisizione/residuo-s6-riepilogo.json, residuo-s6-piattaforme.csv, residuo-s6-blocchi-tipo.csv;
        esiti/<DATA>/imbuto/residuo-s6-per-66.csv (input del ricalcolo dell'imbuto #66: NON lo ricalcola).
Uso (server): .venv/bin/python tools/verifiche/residuo_s6_riepilogo.py [DATA]
"""
import collections, csv, datetime, json, os, sys
from pathlib import Path
from urllib.parse import urlsplit

R = Path(__file__).resolve().parents[2]
D = R / "lavoro/residuo-s6"
csv.field_size_limit(10**9)
os.environ.setdefault("SPESAICT_BASE", str(R))
sys.path.insert(0, str(R / "tools/acquisizione"))
import at_cig  # noqa: E402  (filtra_documenti)
TROVATO = {"documenti", "cig-nella-pagina", "cig-in-sottopagina", "cig-nella-home", "cig-nell-elenco", "cig-con-ricerca",
           "nessun-documento", "mepa-cig-in-vetrina"}
STRATO = {"P1-incerti-ict": "S3-S6 incerti ICT", "P2-g3": "S6/G3", "P3-g2": "S6/G2", "P4-nuovi-rx": "S1->residuo (RX 0.3.3)",
          "P5-g4-campione": "S6/G4 campione"}


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if p.exists() else []


def host(u):
    try: return urlsplit(u).hostname or ""
    except ValueError: return ""


def main():
    data = sys.argv[1] if len(sys.argv) > 1 else str(datetime.date.today())
    ing = {r["cig"]: r for r in csv.DictReader(open(D / "ingresso.csv", encoding="utf-8"))}
    l3 = {}
    for r in jl(D / "out/esiti.jsonl"): l3[r["cig"]] = r
    l4 = {r["cig"]: r for r in jl(D / "l4/esiti.jsonl")}
    enti = jl(D / "l4/enti.jsonl")
    l4js_tutti = {r["cig"]: r for r in jl(D / "l4-js/esiti.jsonl")}
    enti_js = jl(D / "l4-js/enti.jsonl")
    l4js = {c: r for c, r in l4js_tutti.items() if c not in l4}
    filtro = {}
    for nome, recs in (("L4", l4), ("L4-js", l4js)):
        f = collections.Counter()
        for r in recs.values():
            prima = r.get("documenti") or []
            r["documenti"], n = at_cig.filtra_documenti(prima)
            if n:
                f["righe_cambiate"] += 1; f["documenti_scartati"] += n
                if not r["documenti"]: f["righe_documento_diventano_senza_documento"] += 1
                if any(d.get("cig_presente") for d in prima) and not any(d.get("cig_presente") for d in r["documenti"]): f["righe_cita_cig_perse"] += 1
            if prima: f["righe_con_documento_prima"] += 1
            if r["documenti"]: f["righe_con_documento_dopo"] += 1
        filtro[nome] = dict(f)
    atti = collections.defaultdict(set)
    for a in jl(R / "dati/atti/atti-server.jsonl"):
        lv = (a.get("trovato_con") or {}).get("livello")
        if lv in ("L3", "L4", "L4-js") and a.get("pertinenza") == "cig-citato": atti[a["cig"]].add(lv)
    imp = lambda c: float(ing.get(c, {}).get("importo") or 0)

    def misura(nome, recs, trovato, cita):
        m = collections.Counter(); per = collections.defaultdict(collections.Counter)
        for c, r in recs.items():
            p = ing.get(c, {}).get("priorita", r.get("priorita", "?")); t = trovato(r); docs = r.get("documenti") or []
            k = cita(r)
            for a in (m, per[p]):
                a["cig"] += 1; a["euro"] += imp(c)
                if t: a["cig_trovati"] += 1; a["euro_trovati"] += imp(c)
                if docs: a["cig_con_documento"] += 1; a["euro_con_documento"] += imp(c); a["documenti"] += len(docs)
                if k: a["cig_documento_cita_cig"] += 1; a["euro_documento_cita_cig"] += imp(c)
                if k and c in atti: a["cig_con_atto_registrato"] += 1
        rnd = lambda x: {k: round(v, 2) for k, v in x.items()}
        return {"livello": nome, **rnd(m), "per_priorita": {p: rnd(v) for p, v in sorted(per.items())}}

    cita = lambda r: any(d.get("cig_presente") for d in r.get("documenti") or [])
    con_link = {c: r for c, r in l3.items() if r["esito"] != "senza-link" and r["famiglia"] != "mepa" and not r["esito"].startswith("mepa")}
    mepa = {c: r for c, r in l3.items() if r["esito"].startswith("mepa")}
    out = {"generato": data, "ingresso": len(ing), "righe_esiti_l3": sum(1 for _ in open(D / "out/esiti.jsonl", encoding="utf-8")),
           "cig_elaborati_l3": len(l3), "finito_l3": (D / "out/FINITO.txt").exists(), "finito_l4": (D / "l4/FINITO.txt").exists(),
           "finito_l4js_fase1": (D / "l4-js/FINITO-1-js.txt").exists(), "finito_l4js_difesa": (D / "l4-js/FINITO-2-difesa.txt").exists(),
           "l4js_sovrapposti_l4": len(l4js_tutti) - len(l4js), "filtro_non_documenti": filtro,
           "cig_senza_link": sum(1 for x in ing.values() if not x["link"]),
           "enti_senza_link": len({x["stazione_appaltante"] for x in ing.values() if not x["link"]}),
           "livelli": [misura("L3 link PVL", con_link, lambda r: r["esito"] in TROVATO, cita),
                       misura("MePA vetrina pubblica", mepa, lambda r: r["esito"] in TROVATO, cita),
                       misura("L4 sezione Bandi di gara e contratti", l4, lambda r: True, cita),
                       misura("L4-js pagine AT rese con browser headless", l4js, lambda r: True, cita)]}
    costi = {}
    for nome, recs in (("L3", con_link), ("MePA", mepa)):
        costi[nome] = {"richieste": sum(len(r["pagine"]) + len(r["documenti"]) + (r.get("ricerca") or {}).get("richieste", 0) for r in recs.values()),
                       "ore_orologio_somma_cig": round(sum(r.get("secondi", 0) for r in recs.values()) / 3600, 1)}
    costi["L4"] = {"enti_elaborati": len(enti), "richieste": sum(len(e["pagine"]) for e in enti),
                   "ore_orologio_somma_enti": round(sum(e["secondi"] for e in enti) / 3600, 1),
                   "esiti_enti": dict(collections.Counter(e["esito"] for e in enti).most_common())}
    costi["L4-js"] = {"enti_elaborati": len(enti_js), "richieste": sum(len(e["pagine"]) + (e.get("ricerca_browser") or {}).get("richieste", 0) for e in enti_js),
                      "ore_orologio_somma_enti": round(sum(e["secondi"] for e in enti_js) / 3600, 1),
                      "esiti_enti": dict(collections.Counter(e["esito"] for e in enti_js).most_common())}
    u = R / f"esiti/{data}/acquisizione/l4js-url-at.json"
    if u.exists(): out["l4js_url_at"] = json.load(open(u, encoding="utf-8"))
    costi["token"] = 0
    out["costi"] = costi
    out["esiti_l3"] = dict(collections.Counter(r["esito"] for r in l3.values()).most_common())
    # blocchi per tipo (L3) ed enti bloccati (L4)
    bt = collections.Counter(); bh = collections.defaultdict(set)
    for r in con_link.values():
        if r["esito"] in ("blocco", "robots"):
            t = r.get("blocco") or "robots.txt"; bt[t] += 1; bh[t].add(host(r["link"]))
    out["blocchi_l3"] = {t: {"cig": n, "host": len(bh[t])} for t, n in bt.most_common()}
    out["blocchi_l4_enti"] = sum(1 for e in enti if e["esito"] == "blocco")
    # per piattaforma: famiglia + host del link
    pf = collections.defaultdict(collections.Counter)
    for c, r in con_link.items():
        k = (r["famiglia"], host(r["link"]))
        a = pf[k]; a["cig"] += 1; a["euro"] += imp(c); a["trovati"] += r["esito"] in TROVATO; a["con_documento"] += bool(r["documenti"])
        a["documento_cita_cig"] += cita(r); a["blocco_o_robots"] += r["esito"] in ("blocco", "robots"); a["errore"] += r["esito"] == "errore"
    o = R / f"esiti/{data}/acquisizione"; o.mkdir(parents=True, exist_ok=True)
    with open(o / "residuo-s6-piattaforme.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); cols = ["cig", "euro", "trovati", "con_documento", "documento_cita_cig", "blocco_o_robots", "errore"]
        w.writerow(["famiglia", "host"] + cols)
        for (fa, h), a in sorted(pf.items(), key=lambda x: -x[1]["cig"]): w.writerow([fa, h] + [round(a[c], 2) for c in cols])
    fam = collections.defaultdict(collections.Counter)
    for (fa, h), a in pf.items():
        for c, v in a.items(): fam[fa][c] += v
        fam[fa]["host"] += 1
    out["per_famiglia_l3"] = {k: {c: round(v, 2) for c, v in a.items()} for k, a in sorted(fam.items(), key=lambda x: -x[1]["cig"])}
    out["piattaforme_top"] = [{"famiglia": fa, "host": h, **{c: round(v, 2) for c, v in a.items()}}
                              for (fa, h), a in sorted(pf.items(), key=lambda x: -x[1]["documento_cita_cig"])[:15]]
    # input per #66: un CIG per riga, con cosa abbiamo in mano
    imb = R / f"esiti/{data}/imbuto"; imb.mkdir(parents=True, exist_ok=True)
    q = collections.defaultdict(collections.Counter)
    with open(imb / "residuo-s6-per-66.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["cig", "priorita", "strato", "importo", "livello", "materiale", "documenti_che_citano", "atto_registrato"])
        for c, x in ing.items():
            r3, r4, rj = con_link.get(c), l4.get(c), l4js.get(c)
            if r3 and cita(r3): lv, mat, rr = "L3", "documento-cita-cig", r3
            elif r4 and cita(r4): lv, mat, rr = "L4", "documento-cita-cig", r4
            elif rj and cita(rj): lv, mat, rr = "L4-js", "documento-cita-cig", rj
            elif r3 and r3["documenti"]: lv, mat, rr = "L3", "documento-senza-cig", r3
            elif r4 and r4["documenti"]: lv, mat, rr = "L4", "documento-senza-cig", r4
            elif rj and rj["documenti"]: lv, mat, rr = "L4-js", "documento-senza-cig", rj
            elif r3 and r3["esito"] in TROVATO: lv, mat, rr = "L3", "solo-pagina-con-cig", r3
            elif r4: lv, mat, rr = "L4", "solo-pagina-con-cig", r4
            elif rj: lv, mat, rr = "L4-js", "solo-pagina-con-cig", rj
            else: lv, mat, rr = "", "nulla", None
            n = sum(1 for d in (rr or {}).get("documenti") or [] if d.get("cig_presente"))
            w.writerow([c, x["priorita"], STRATO.get(x["priorita"], ""), x["importo"], lv, mat, n, "sì" if c in atti else "no"])
            a = q[(x["priorita"], mat)]; a["cig"] += 1; a["euro"] += imp(c)
    out["per_66"] = {f"{p}|{m}": {"cig": a["cig"], "euro": round(a["euro"], 2)} for (p, m), a in sorted(q.items())}
    json.dump(out, open(o / "residuo-s6-riepilogo.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "piattaforme_top"}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
