#!/usr/bin/env python3
"""Copertura del link ai documenti di gara negli avvisi PVL (#57).

Legge in streaming il CSV prodotto da `pvl_avvisi.py estrai` e stampa: CIG
distinti, quota con `documenti_di_gara_link`, ripartizione per scheda e per
dominio di destinazione. Tiene in memoria solo gli insiemi di CIG (qualche
milione di stringhe da 10 caratteri: ~300 MB al massimo sull'universo 2024-26).

    pvl_copertura.py lavoro/pvl/link_cig.csv
"""
import collections
import csv
import sys
import urllib.parse as u


def dominio(l: str) -> str:
    l = l.split(" | ")[0].strip()
    try:
        h = u.urlsplit(l if "//" in l else "http://" + l).hostname or "?"
    except ValueError:
        return "?"
    return h.removeprefix("www.")


def main(p: str) -> None:
    cig, cig_link = set(), set()
    scheda, scheda_link, dom = collections.Counter(), collections.Counter(), collections.Counter()
    with open(p, encoding="utf-8", newline="") as f:
        for x in csv.DictReader(f):
            c = x["cig"]
            if not c:
                continue
            cig.add(c)
            scheda[x["codice_scheda"]] += 1
            if x["documenti_di_gara_link"]:
                cig_link.add(c)
                scheda_link[x["codice_scheda"]] += 1
                dom[dominio(x["documenti_di_gara_link"])] += 1
    print(f"CIG distinti {len(cig)}; con link {len(cig_link)} ({100*len(cig_link)/max(1,len(cig)):.1f} %)")
    print("righe (avviso,CIG) per scheda: totale / con link")
    for k, v in scheda.most_common():
        print(f"  {k:6} {v:9} {scheda_link[k]:9} {100*scheda_link[k]/v:5.1f} %")
    print(f"{len(dom)} domini; primi 40:")
    for h, c in dom.most_common(40):
        print(f"  {c:8} {h}")


if __name__ == "__main__":
    main(sys.argv[1])
