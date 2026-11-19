#!/usr/bin/env python3
"""Stato del mirror per ticket (#11 #12 #13 #25 #26 #27 #28 #29 #17), misurato dal manifest reale.

Per ogni fonte conta gli URL con almeno un'acquisizione riuscita (sha256 nel manifest), i byte dell'ultima
versione, gli URL il cui ultimo tentativo è fallito e, dove esiste un elenco atteso (BDAP dai metadati CKAN,
Consip dal catalogo HTML, IndicePA dal CKAN), i mancanti rispetto all'elenco.

    mirror_fonti.py [--out esiti/AAAA-MM-GG/mirror/stato-fonti.json]

Elenchi attesi (generati, in lavoro/mirror-completamento/):
- bdap-risorse.csv   da tools/acquisizione/bdap_lista.py (metadati CKAN archiviati)
- consip/html-elenco.tsv, indicepa/elenco.txt
Se un elenco manca, la fonte riporta solo i conteggi dal manifest.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
from collections import defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

BASE = Path(__file__).resolve().parent.parent.parent
ROOT = Path(os.environ.get("ARCHIVIO_ROOT", BASE / "archivio"))
LAV = BASE / "lavoro" / "mirror-completamento"
OK = ("nuovo", "invariato")

# fonte -> (ticket, filtro sull'URL)
FONTI = {
    "anac": (None, lambda u, h: h == "dati.anticorruzione.it" and "/opendata/download/" in u),
    "consip": (11, lambda u, h: h == "dati.consip.it" and "/download/" in u),
    "siope": (12, lambda u, h: h == "www.siope.it" and "/open/" in u),
    "indicepa": (13, lambda u, h: h == "indicepa.gov.it" and "/ipa-dati/" in u),
    "padigitale2026": (13, lambda u, h: "padigitale2026-opendata" in u),
    "bdap": (25, lambda u, h: h == "bdap-opendata.rgs.mef.gov.it"),
    "opencup": (26, lambda u, h: h == "www.opencup.gov.it" and "/documents/" in u),
    "opencoesione": (26, lambda u, h: h == "opencoesione.gov.it" and ("/opendata/" in u)),
    "openpnrr": (26, lambda u, h: h == "openpnrr.s3.amazonaws.com" or (h == "openpnrr.it" and "/csv/" in u)),
    "ted": (27, lambda u, h: h == "api.ted.europa.eu"),
    "fts": (27, lambda u, h: "financial-transparency-system" in u),
    "gleif": (28, lambda u, h: h == "goldencopy.gleif.org" and "golden-copy-files" in u),
    "cpt": (29, lambda u, h: h == "politichecoesione.governo.it"),
    "eurostat-cofog": (29, lambda u, h: "gov_10a_exp" in u),
}


def leggi_manifest():
    ultimo, ok = {}, {}
    with (ROOT / "manifest.jsonl").open(encoding="utf-8") as f:
        for riga in f:
            r = json.loads(riga)
            ultimo[r["url"]] = r
            if r.get("esito") in OK:
                ok[r["url"]] = r
    return ultimo, ok


def attesi():
    e = {}
    p = LAV / "bdap-risorse.csv"
    if p.exists():
        righe = list(csv.DictReader(p.open(encoding="utf-8")))
        e["bdap"] = {r["url"]: r for r in righe}
    p = LAV / "consip" / "html-elenco.tsv"
    if p.exists():
        e["consip"] = {l.split("\t")[1].strip(): {} for l in p.open(encoding="utf-8") if "\t" in l}
    p = LAV / "indicepa" / "elenco.txt"
    if p.exists():
        e["indicepa"] = {l.strip(): {} for l in p.open(encoding="utf-8") if l.strip()}
    return e


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=BASE / "esiti" / date.today().isoformat() / "mirror" / "stato-fonti.json")
    a = ap.parse_args()
    ultimo, ok = leggi_manifest()
    att = attesi()
    esito = {"data": date.today().isoformat(), "manifest_righe": sum(1 for _ in (ROOT / "manifest.jsonl").open()), "fonti": {}}
    for nome, (ticket, filtro) in FONTI.items():
        urls = [u for u in ultimo if filtro(u, urlsplit(u).netloc)]
        riusciti = [u for u in urls if u in ok]
        falliti = [u for u in urls if ultimo[u].get("esito") not in OK]
        d = {"ticket": ticket, "url_tentati": len(urls), "url_con_sha256": len(riusciti),
             "gb_ultima_versione": round(sum(ok[u].get("dimensione") or 0 for u in riusciti) / 1e9, 3),
             "ultimo_tentativo_fallito": len(falliti),
             "ultima_acquisizione": max((ok[u]["acquisito"] for u in riusciti), default=None)}
        if nome in att:
            el = att[nome]
            if nome == "bdap":
                gruppi = defaultdict(lambda: {"risorse": 0, "con_sha256": 0, "gb_dichiarati": 0.0, "gb_archiviati": 0.0})
                for u, r in el.items():
                    k = (r["motivo"] or "dentro") + " / " + r["tipo"]
                    g = gruppi[k]; g["risorse"] += 1; g["gb_dichiarati"] += int(r["dimensione"] or 0) / 1e9
                    if u in ok:
                        g["con_sha256"] += 1; g["gb_archiviati"] += (ok[u].get("dimensione") or 0) / 1e9
                d["elenco_atteso"] = {k: {**v, "gb_dichiarati": round(v["gb_dichiarati"], 2), "gb_archiviati": round(v["gb_archiviati"], 2)}
                                      for k, v in sorted(gruppi.items())}
            else:
                manc = [u for u in el if u not in ok]
                d["elenco_atteso"] = {"risorse": len(el), "con_sha256": len(el) - len(manc), "mancanti": manc}
        esito["fonti"][nome] = d
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(esito, ensure_ascii=False, indent=1), encoding="utf-8")
    for n, d in esito["fonti"].items():
        print(f"#{d['ticket'] or '-':>3} {n:16} url {d['url_con_sha256']:5}/{d['url_tentati']:<5} {d['gb_ultima_versione']:8.2f} GB  falliti {d['ultimo_tentativo_fallito']}")
        if isinstance(d.get("elenco_atteso"), dict) and n == "bdap":
            for k, v in d["elenco_atteso"].items():
                print(f"      {k:55} {v['con_sha256']:5}/{v['risorse']:<5} {v['gb_archiviati']:6.2f}/{v['gb_dichiarati']:.2f} GB")
        elif d.get("elenco_atteso"):
            e = d["elenco_atteso"]; print(f"      elenco atteso: {e['con_sha256']}/{e['risorse']}")
    print(f"scritto {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
