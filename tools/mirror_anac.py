#!/usr/bin/env python3
"""Specchia tutte le risorse ANAC censite, in ordine di priorità.

Legge `config/anac-risorse.jsonl` prodotto da `censisci_anac.py` e scarica con
la logica di `archivia.py`: append-only, indirizzamento per contenuto, manifest.

Priorità, perché se il lavoro si interrompe deve essersi salvato il salvabile:
  1. risorse deperibili (delta che spariscono) in CSV
  2. risorse deperibili negli altri formati
  3. tutto il resto in CSV
  4. tutto il resto negli altri formati
A parità, prima le più piccole: più risorse messe in salvo per minuto.

Ripartibile: `archivia.py` salta ciò che non è cambiato, quindi rilanciarlo
costa solo le richieste HEAD.

    mirror_anac.py                 # tutto
    mirror_anac.py --formati CSV   # un formato per volta
    mirror_anac.py --max-gb 5      # si ferma dopo 5 GB scaricati
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from archivia import archivia, scrivi_manifest  # noqa: E402

BASE = Path(__file__).resolve().parent.parent


def priorita(r: dict) -> tuple:
    csv = 0 if r.get("formato") == "CSV" else 1
    dep = 0 if r.get("deperibile") else 1
    return (dep, csv, r.get("dim_reale") or 0)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--elenco", type=Path, default=BASE / "config" / "anac-risorse.jsonl")
    ap.add_argument("--formati", nargs="*")
    ap.add_argument("--max-gb", type=float)
    a = ap.parse_args()

    righe = [json.loads(l) for l in a.elenco.read_text(encoding="utf-8").splitlines() if l.strip()]
    da_fare = [r for r in righe if r.get("http") == 200]
    if a.formati:
        f = {x.upper() for x in a.formati}
        da_fare = [r for r in da_fare if r.get("formato") in f]
    da_fare.sort(key=priorita)

    tot = sum(r.get("dim_reale") or 0 for r in da_fare)
    print(f"{len(da_fare)} risorse, {tot/1e9:.2f} GB dichiarati dal server\n", flush=True)

    sess = requests.Session()
    scaricati = 0
    conteggi = {"nuovo": 0, "invariato": 0, "errore": 0, "assente": 0}
    for i, r in enumerate(da_fare, 1):
        rec = archivia(sess, r["url"])
        rec["dataset"] = r.get("dataset")
        rec["formato"] = r.get("formato")
        scrivi_manifest(rec)
        conteggi[rec["esito"]] = conteggi.get(rec["esito"], 0) + 1
        if rec["esito"] == "nuovo":
            scaricati += rec.get("dimensione") or 0
        mb = (rec.get("dimensione") or 0) / 1e6
        print(f"[{i}/{len(da_fare)}] {rec['esito']:9s} {mb:9.1f} MB  "
              f"{r['dataset']}/{r['risorsa']} [{r['formato']}]", flush=True)
        if a.max_gb and scaricati / 1e9 >= a.max_gb:
            print(f"\nraggiunto il tetto di {a.max_gb} GB, mi fermo. "
                  f"Rilanciare per continuare: salta ciò che è già preso.")
            break

    print(f"\nscaricati {scaricati/1e9:.2f} GB in questa sessione")
    print("esiti:", {k: v for k, v in conteggi.items() if v})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
