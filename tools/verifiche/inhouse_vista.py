#!/usr/bin/env python3
"""Vista per società ICT in-house: che cosa comprano e che cosa ricevono dagli enti (#52). Versione 0.1 (20/11/2026).

Richiesta di Fabio del 20/11/2026: misurare espressamente che cosa fanno le società in-house, con tutte le loro spese
cloud e infrastrutturali.

Ingressi:
  config/societa_inhouse_ict.yaml        elenco (soci Assinter Italia + Sogei, CINECA, PagoPA) con espressioni sul nome;
  lavoro/imbuto/ict.csv                  CIG ICT dell'imbuto (stazione appaltante, aggiudicatari);
  lavoro/imbuto/stati-finali.csv.gz      stato di ogni CIG dopo i livelli (scritto da tools/verifiche/imbuto_spostamenti.py).
Due lenti:
  come acquirente:  CIG in cui la società è stazione appaltante, per stato finale (cloud esterno per giurisdizione,
                    cloud in proprio per famiglia, ICT non cloud, incerti, fuori misura);
  come fornitrice:  CIG in cui la società è aggiudicataria (affidamenti degli enti), con il numero di enti.
Gli importi sono al netto dei massimali (tetti v2), come nella tabella unica. Il riconoscimento è sul nome (0.1):
l'uscita elenca, per ogni società, le denominazioni trovate, da controllare a mano (passaggio al codice fiscale: 0.2).

Uso: python3 tools/verifiche/inhouse_vista.py [AAAA-MM-GG]   (dopo imbuto_spostamenti.py)
Uscite: esiti/<data>/inhouse/vista/{vista.json, vista.md}
"""
import collections
import csv
import gzip
import json
import os
import re
import sys
from datetime import date

import yaml

VERSIONE = "0.1"
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GIORNO = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
OUT = os.path.join(R, "esiti", GIORNO, "inhouse", "vista")
csv.field_size_limit(10**9)
SOC = yaml.safe_load(open(os.path.join(R, "config/societa_inhouse_ict.yaml"), encoding="utf-8"))["societa"]
RX = {k: re.compile(v["regex"]) for k, v in SOC.items()}
VOCI = ["cloud-esterno-EXTRA-UE", "cloud-esterno-UE", "cloud-esterno-IT", "cloud-esterno-non-determinata",
        "dc-proprio", "inhouse-certo", "ict-non-cloud", "incerto", "escluso-non-ict", "fuori-misura"]


def chi(nome):
    n = (nome or "").upper().strip()
    return [k for k, rx in RX.items() if rx.search(n)]


def voce(st):
    s = st["stato"]
    if s == "cloud-certo":
        return "cloud-esterno-" + (st["giurisdizione"] or "non-determinata").replace("non determinata", "non-determinata")
    if s.startswith("incerto"):
        return "incerto"
    return s


def main():
    stati = {r["cig"]: r for r in csv.DictReader(gzip.open(os.path.join(R, "lavoro/imbuto/stati-finali.csv.gz"), "rt", encoding="utf-8"))}
    nuovo = lambda: collections.defaultdict(lambda: [0, 0.0])
    acq = collections.defaultdict(nuovo)        # (soc, periodo) -> voce -> [cig, euro]
    acq_fam = collections.defaultdict(nuovo)    # (soc, periodo) -> famiglia dc -> [cig, euro]
    forn = collections.defaultdict(nuovo)       # (soc, periodo) -> voce -> [cig, euro]
    forn_enti = collections.defaultdict(set)
    nomi = collections.defaultdict(collections.Counter)
    visti = set()
    for r in csv.DictReader(open(os.path.join(R, "lavoro/imbuto/ict.csv"), encoding="utf-8", newline="")):
        cig = r["cig"].strip().upper()
        if cig in visti or cig not in stati:
            continue
        visti.add(cig)
        st = stati[cig]
        per = "2020-2023" if int(r["anno"] or 0) <= 2023 else "dal-2024"
        e = float(st["euro_netti"] or 0)
        v = voce(st)
        for k in chi(r["stazione_appaltante"]):
            nomi[k]["SA: " + r["stazione_appaltante"].upper().strip()] += 1
            a = acq[(k, per)][v]; a[0] += 1; a[1] += e
            if v == "dc-proprio":
                f = acq_fam[(k, per)][st["famiglia_dc"] or "?"]; f[0] += 1; f[1] += e
        ks = set()
        for ag in re.split(r"\s*[|;]\s*", r["aggiudicatari"] or ""):
            for k in chi(ag):
                ks.add(k); nomi[k]["AGG: " + ag.upper().strip()] += 1
        for k in ks:
            if chi(r["stazione_appaltante"]) == [k]:
                continue   # affidamento a sé stessa (es. ordine interno): non è un ente che affida
            a = forn[(k, per)][v]; a[0] += 1; a[1] += e
            forn_enti[(k, per)].add(r["stazione_appaltante"].upper().strip())
    conv = lambda d: {v: {"cig": d[v][0], "meur": round(d[v][1] / 1e6, 2)} for v in VOCI + sorted(set(d) - set(VOCI)) if v in d}
    out = {"versione": VERSIONE, "data": GIORNO, "strumento": "tools/verifiche/inhouse_vista.py",
           "nota": "M€ al netto dei massimali (tetti v2); stato dopo i livelli della tabella unica; riconoscimento sul nome",
           "societa": {}}
    for k, s in SOC.items():
        x = {"nome": s["nome"], "fonte": s["fonte"]}
        for per in ("2020-2023", "dal-2024"):
            x[per] = {"come_acquirente": conv(acq[(k, per)]), "cloud_in_proprio_per_famiglia": conv(acq_fam[(k, per)]),
                      "come_fornitrice": conv(forn[(k, per)]), "enti_che_affidano": len(forn_enti[(k, per)])}
        x["denominazioni_trovate"] = nomi[k].most_common(12)
        out["societa"][k] = x
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(os.path.join(OUT, "vista.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    it = lambda x: f"{x:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
    L = [f"# Società ICT in-house: che cosa comprano e che cosa ricevono — {GIORNO}", "",
         f"Strumento `{out['strumento']}` {VERSIONE}. Dal 2024, M€ al netto dei massimali.", "",
         "| società | cloud esterno extra-UE | cloud esterno UE | cloud esterno IT | cloud in proprio | ICT non cloud | incerto | ricevuto dagli enti (affidamenti) | enti |",
         "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    g = lambda d, v: d.get(v, {}).get("meur", 0)
    for k, x in sorted(out["societa"].items(), key=lambda a: -sum(v["meur"] for v in a[1]["dal-2024"]["come_acquirente"].values())):
        a, f = x["dal-2024"]["come_acquirente"], x["dal-2024"]["come_fornitrice"]
        L.append(f"| {x['nome']} | {it(g(a, 'cloud-esterno-EXTRA-UE'))} | {it(g(a, 'cloud-esterno-UE'))} | {it(g(a, 'cloud-esterno-IT'))} | "
                 f"{it(g(a, 'dc-proprio'))} | {it(g(a, 'ict-non-cloud'))} | {it(g(a, 'incerto'))} | {it(sum(v['meur'] for v in f.values()))} | {x['dal-2024']['enti_che_affidano']} |")
    open(os.path.join(OUT, "vista.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
