"""Snapshot dei file usati per il rendiconto: URL, percorso nel mirror, byte, sha256.

  python tools/verifiche/snapshot.py crea report/anac/snapshot-2026-10-27.tsv
      (dal manifest dell'archivio, ultima versione di ogni URL dei dataset usati dalle verifiche)
  python tools/verifiche/snapshot.py controlla report/anac/snapshot-2026-10-27.tsv
      (ricalcola lo sha256 dei file scaricati e dice quali coincidono con lo snapshot)
"""
import csv
import hashlib
import json
import os
import sys
from fnmatch import fnmatch
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
ROOT = Path(os.environ.get("ARCHIVIO_ROOT", BASE / "archivio"))
PREFISSO = "https://dati.anticorruzione.it/opendata/download/dataset/"
USATI = ["ocds/filesystem/bulk/*", "cig-20*/filesystem/cig_csv_*.zip", "cig/filesystem/*-cig_csv.zip",
         "aggiudicazioni/filesystem/*_csv.zip", "aggiudicatari/filesystem/*_csv.zip",
         "cup/filesystem/cup_csv.zip", "stazioni-appaltanti/filesystem/stazioni-appaltanti_csv.zip"]


def crea(out: Path) -> None:
    ultimo = {}
    for riga in (ROOT / "manifest.jsonl").read_text(encoding="utf-8").splitlines():
        d = json.loads(riga)
        if d.get("sha256") and d["url"].startswith(PREFISSO) and any(fnmatch(d["url"][len(PREFISSO):], m) for m in USATI):
            ultimo[d["url"]] = d
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["url", "byte", "sha256"])
        for url in sorted(ultimo):
            d = ultimo[url]
            w.writerow([url, d.get("byte") or d.get("dimensione") or "", d["sha256"]])
    print(f"{len(ultimo)} file in {out}")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def controlla(snap: Path) -> int:
    uguali = diversi = mancanti = 0
    for r in csv.DictReader(snap.open(encoding="utf-8"), delimiter="\t"):
        p = ROOT / "mirror" / r["url"].split("://", 1)[1]
        if not p.exists():
            mancanti += 1
            continue
        if sha256(p) == r["sha256"]:
            uguali += 1
        else:
            diversi += 1
            print(f"DIVERSO  {r['url']}  (ANAC ha cambiato il file dopo lo snapshot)")
    print(f"{uguali} file identici allo snapshot, {diversi} diversi, {mancanti} non scaricati")
    return 0


if __name__ == "__main__":
    cmd, path = sys.argv[1], Path(sys.argv[2])
    raise SystemExit(crea(path) if cmd == "crea" else controlla(path))
