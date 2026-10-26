#!/usr/bin/env python3
"""Quale periodo contiene davvero un file OCDS bulk di ANAC.

ANAC pubblica l'OCDS come un file per mese, `bulk/{anno}/{mese}.json`. Questo
script legge il file in streaming e conta le release per mese, così da
verificare se il contenuto corrisponde al mese dichiarato nel percorso.

Serve a rispondere a una domanda precisa: se un mese manca, il mese vicino lo
contiene?

    ocds_periodo.py percorso/al/03.json
"""
from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

import ijson


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", type=Path)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()

    per_mese_release = collections.Counter()
    per_mese_aggiudicazione = collections.Counter()
    ocid = set()
    n = 0
    intestazione = {}

    with a.file.open("rb") as f:
        # L'intestazione del pacchetto sta prima di "releases".
        for k in ("version", "uri", "publishedDate", "license"):
            pass
        f.seek(0)
        testa = f.read(4096).decode("utf-8", "replace")
        for campo in ("uri", "publishedDate"):
            i = testa.find(f'"{campo}"')
            if i >= 0:
                intestazione[campo] = testa[i:testa.find("\n", i)].strip().rstrip(",")

        f.seek(0)
        for rel in ijson.items(f, "releases.item", use_float=True):
            n += 1
            if rel.get("ocid"):
                ocid.add(rel["ocid"])
            d = (rel.get("date") or "")[:7]
            if len(d) == 7:
                per_mese_release[d] += 1
            for aw in rel.get("awards") or []:
                ad = (aw.get("date") or "")[:7]
                if len(ad) == 7:
                    per_mese_aggiudicazione[ad] += 1
            if n % 200000 == 0:
                print(f"  ...{n:,} release lette", flush=True)

    print(f"\nfile: {a.file}")
    for k, v in intestazione.items():
        print(f"  {v}")
    print(f"  release: {n:,}   ocid distinti: {len(ocid):,}")

    print("\n### release per mese (campo `date` della release)")
    for m, c in sorted(per_mese_release.items()):
        print(f"  {m}  {c:>9,}  {'#' * min(60, c * 60 // max(per_mese_release.values()))}")

    print("\n### aggiudicazioni per mese (campo `date` dell'award)")
    for m, c in sorted(per_mese_aggiudicazione.items())[-24:]:
        print(f"  {m}  {c:>9,}")

    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(json.dumps({
            "file": str(a.file), "intestazione": intestazione, "release": n,
            "ocid_distinti": len(ocid),
            "release_per_mese": dict(sorted(per_mese_release.items())),
            "aggiudicazioni_per_mese": dict(sorted(per_mese_aggiudicazione.items())),
        }, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\nscritto {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
