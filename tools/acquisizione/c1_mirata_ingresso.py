#!/usr/bin/env python3
"""Ingresso della ricerca mirata degli atti per i CIG della via 6 fermi al criterio C1 (#55 #66, 9/11/2026).

Selezione da esiti/AAAA-MM-GG/imbuto/revisione-via6.json (tools/verifiche/imbuto_via6_revisione.py esito):
  P1-concorde-c1     seconda lettura concorde, C2 ok, ma nessun atto archiviato che citi il CIG (C1 falso);
  P2-nonconf-alto    seconda lettura «non confermato», C1 falso, importo >= SOGLIA (1 M€).
Link dalla PVL (lavoro/pvl/link_cig.csv, il più specifico) e TED (link_eform_ted), come residuo_s6_ingresso.py.
Stesso formato di lavoro/residuo-s6/ingresso.csv: lo leggono piattaforme_cig.py (L3) e at_cig.py (L4) senza modifiche.
Uso (server): nice .venv/bin/python tools/acquisizione/c1_mirata_ingresso.py esiti/2026-11-09/imbuto/revisione-via6.json lavoro/c1-mirata/ingresso.csv
"""
import csv, glob, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from residuo_s6_ingresso import specificita  # noqa: E402

R = Path(__file__).resolve().parents[2]
SOGLIA = 1_000_000
csv.field_size_limit(10**9)


def main():
    rev, out = json.load(open(sys.argv[1], encoding="utf-8")), Path(sys.argv[2])
    out.parent.mkdir(parents=True, exist_ok=True)
    lotti = {}
    for f in glob.glob(str(R / "report/metodo/llm/imbuto-g1g3/lotti/*.jsonl")):
        for l in open(f, encoding="utf-8"):
            if l.strip():
                c = json.loads(l); lotti[c["cig"]] = c
    sel = {}
    for x in rev["righe"]:
        if x["C1_fonte_primaria"] or not x["C2_regole"]:
            continue
        if x["C4_seconda_lettura"] == "concorde":
            sel[x["cig"]] = "P1-concorde-c1"
        elif x["C4_seconda_lettura"] == "non-confermato" and x["importo"] >= SOGLIA:
            sel[x["cig"]] = "P2-nonconf-alto"
    link, ted = {}, {}
    for r in csv.DictReader(open(R / "lavoro/pvl/link_cig.csv", encoding="utf-8")):
        if r["cig"] in sel:
            u = r["documenti_di_gara_link"].strip()
            if u and specificita(u) > specificita(link.get(r["cig"], "")):
                link[r["cig"]] = u
            if r["link_eform_ted"]:
                ted[r["cig"]] = r["link_eform_ted"]
    righe = sorted(sel.items(), key=lambda kv: (kv[1], -lotti[kv[0]]["importo"]))
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["cig", "priorita", "importo", "anno", "stazione_appaltante", "link", "link_ted", "oggetto"])
        for cig, p in righe:
            c = lotti[cig]
            w.writerow([cig, p, c["importo"], c.get("anno", ""), c["ente"], link.get(cig, ""), ted.get(cig, ""), c["testo"][:200]])
    print(f"{len(righe)} CIG -> {out}; con link PVL {sum(1 for c, _ in righe if c in link)}, con TED {sum(1 for c, _ in righe if c in ted)}")


if __name__ == "__main__":
    main()
