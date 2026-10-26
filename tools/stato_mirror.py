#!/usr/bin/env python3
"""Stato dell'archivio: avanzamento, spazio, e quanto risparmia la deduplicazione.

L'archivio è indirizzato per contenuto: due risorse con lo stesso `sha256`
occupano un solo blob. Dove una fonte pubblica lo stesso file sotto nomi
diversi — come i mesi duplicati dell'OCDS di ANAC — il risparmio misura
esattamente quella duplicazione.

    stato_mirror.py
    stato_mirror.py --json stato/mirror.json
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
ROOT = Path(os.environ.get("ARCHIVIO_ROOT", BASE / "archivio"))
MANIFEST = ROOT / "manifest.jsonl"
ELENCO = BASE / "config" / "anac-risorse.jsonl"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=Path)
    a = ap.parse_args()

    righe = [json.loads(l) for l in MANIFEST.read_text(encoding="utf-8").splitlines() if l.strip()]
    per_url: dict[str, dict] = {}
    for r in righe:
        if r["esito"] in ("nuovo", "invariato"):
            per_url[r["url"]] = r

    esiti = collections.Counter(r["esito"] for r in righe)
    byte_logici = sum(r.get("dimensione") or 0 for r in per_url.values())
    blob = {r["sha256"]: r.get("dimensione") or 0 for r in per_url.values() if r.get("sha256")}
    byte_fisici = sum(blob.values())

    # risorse che condividono il contenuto con un'altra
    per_sha = collections.defaultdict(list)
    for u, r in per_url.items():
        if r.get("sha256"):
            per_sha[r["sha256"]].append(u)
    gruppi = {s: u for s, u in per_sha.items() if len(u) > 1}

    atteso = 0
    if ELENCO.exists():
        atteso = sum(1 for l in ELENCO.read_text(encoding="utf-8").splitlines()
                     if l.strip() and json.loads(l).get("http") == 200)

    libero = shutil.disk_usage(ROOT if ROOT.exists() else BASE).free / 1e9
    su_disco = sum(f.stat().st_size for f in (ROOT / "blobs").rglob("*") if f.is_file()) / 1e9 \
        if (ROOT / "blobs").exists() else 0

    print(f"risorse in archivio : {len(per_url):,}" + (f" su {atteso:,} attese" if atteso else ""))
    print(f"tentativi registrati: {len(righe):,}  {dict(esiti)}")
    print(f"\nbyte logici (somma delle risorse) : {byte_logici/1e9:>8.2f} GB")
    print(f"byte fisici (blob distinti)       : {byte_fisici/1e9:>8.2f} GB")
    if byte_logici:
        print(f"risparmio da deduplicazione       : {(byte_logici-byte_fisici)/1e9:>8.2f} GB "
              f"({(1-byte_fisici/byte_logici)*100:.1f}%)")
    print(f"blob su disco                     : {su_disco:>8.2f} GB")
    print(f"spazio libero                     : {libero:>8.2f} GB")

    if gruppi:
        print(f"\ncontenuti identici pubblicati sotto piu nomi: {len(gruppi)} gruppi")
        ordinati = sorted(gruppi.items(), key=lambda x: -blob.get(x[0], 0) * (len(x[1]) - 1))
        for sha, urls in ordinati[:8]:
            dim = blob.get(sha, 0)
            print(f"  {len(urls)} copie x {dim/1e6:.0f} MB  (sprecati {dim*(len(urls)-1)/1e9:.2f} GB)")
            for u in sorted(urls)[:6]:
                print(f"     {u.split('/dataset/')[-1]}")
            if len(urls) > 6:
                print(f"     ...e altre {len(urls)-6}")

    if a.json:
        a.json.parent.mkdir(parents=True, exist_ok=True)
        a.json.write_text(json.dumps({
            "risorse": len(per_url), "attese": atteso, "esiti": dict(esiti),
            "byte_logici": byte_logici, "byte_fisici": byte_fisici,
            "blob_distinti": len(blob), "libero_gb": round(libero, 2),
            "gruppi_duplicati": {s: sorted(u) for s, u in gruppi.items()},
        }, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\nscritto {a.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
