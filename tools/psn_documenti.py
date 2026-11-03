#!/usr/bin/env python3
"""Censimento dei documenti PSN pubblicati (#55).

Per ogni URL di una lista: archivia (tools/archivia.py), ritrova il blob dal
manifest, estrae il testo con pdftotext e rileva i tratti distintivi (codici
PdF/PPdF, CIG, CUP, clausola di confidenzialità, capitolo Configuratore,
pagine-immagine). Scrive una riga JSON per documento in lavoro/psn-db/estratti.jsonl.
Idempotente: salta gli sha256 già estratti.

    psn_documenti.py lista.txt
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
MANIFEST = BASE / "archivio" / "manifest.jsonl"
OUT = BASE / "lavoro" / "psn-db"
OUT.mkdir(parents=True, exist_ok=True)
TXT = OUT / "txt"
TXT.mkdir(exist_ok=True)
EST = OUT / "estratti.jsonl"

RE = {
    "codici": re.compile(r"\b(20\d\d-\d{16}-P{1,2}dF-P\d+R\d+(?:M\d+)?)", re.I),
    "cig": re.compile(r"\bCIG[^A-Z0-9]{0,30}([A-Z0-9]{10})\b"),
    "cup": re.compile(r"\bCUP[^A-Z0-9]{0,20}([A-Z]\d{2}[A-Z]\d{11})\b"),
}
TRATTI = {
    "confidenziale": r"confidenzial\w+ di propriet",
    "configuratore": r"\bConfiguratore\b",
    "riepilogo_prezzi": r"riepilogo\s+prezzi",
    "titolo_ppdf": r"progetto\s+del\s+piano\s+dei\s+fabbisogni",
    "piano_fabbisogni_ente": r"template piano dei fabbisogni|piano dei fabbisogni\s*\n.*nell.ambito della concessione",
    "contratto_utenza": r"contratto\s+di\s+utenza",
    "secure_public_cloud": r"secure public cloud",
    "industry_standard": r"industry standard",
    "psn_managed": r"psn managed",
    "omissis": r"omissis|oscurat",
}


def ultimo(url: str) -> dict | None:
    r = None
    with MANIFEST.open(encoding="utf-8") as f:
        for line in f:
            if url in line:
                d = json.loads(line)
                if d.get("url") == url:
                    r = d
    return r


def blob(sha: str) -> Path:
    return BASE / "archivio" / "blobs" / "sha256" / sha[:2] / sha[2:4] / sha


def main(lista: str) -> None:
    fatti = set()
    if EST.exists():
        for l in EST.open(encoding="utf-8"):
            fatti.add(json.loads(l)["url"])
    urls = [u.strip() for u in Path(lista).read_text(encoding="utf-8").splitlines() if u.strip() and not u.startswith("#")]
    for url in urls:
        if url in fatti:
            continue
        subprocess.run([sys.executable, str(BASE / "tools" / "archivia.py"), url], capture_output=True, timeout=300)
        m = ultimo(url) or {}
        rec = {"url": url, "http": m.get("http"), "esito": m.get("esito"), "sha256": m.get("sha256"), "tipo": m.get("tipo")}
        sha = m.get("sha256")
        if sha and blob(sha).exists():
            p = blob(sha)
            t = TXT / f"{sha}.txt"
            if not t.exists():
                subprocess.run(["pdftotext", "-layout", str(p), str(t)], capture_output=True, timeout=300)
            testo = t.read_text(encoding="utf-8", errors="replace") if t.exists() else ""
            info = subprocess.run(["pdfinfo", str(p)], capture_output=True, text=True).stdout
            mp = re.search(r"Pages:\s+(\d+)", info)
            rec["pagine"] = int(mp.group(1)) if mp else None
            rec["caratteri"] = len(testo)
            for k, rx in RE.items():
                rec[k] = sorted(set(rx.findall(testo)))
            low = testo.lower()
            for k, rx in TRATTI.items():
                rec[k] = bool(re.search(rx, low if k != "configuratore" else testo, re.I))
        with EST.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(rec.get("http"), rec.get("pagine"), rec.get("codici"), url[:90], flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
