#!/usr/bin/env python3
"""OCR del capitolo "Configuratore" dei Progetti del Piano dei Fabbisogni PSN (#55).

Legge lavoro/psn-db/estratti.jsonl; per ogni documento con il capitolo
Configuratore individua le pagine dal titolo "Configuratore" in poi (max 6 per
blocco, tutti i blocchi), le rasterizza a 300 dpi e le passa a tesseract (ita).
Scrive lavoro/psn-db/ocr/<sha>-p<n>.txt e, in lavoro/psn-db/tratti.jsonl, i tratti
ricalcolati sul testo normalizzato (clausola di confidenzialità, ecc.).
Idempotente: non ripete pagine già OCR-izzate.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
D = BASE / "lavoro" / "psn-db"
OCR = D / "ocr"
OCR.mkdir(exist_ok=True)


def blob(sha: str) -> Path:
    return BASE / "archivio" / "blobs" / "sha256" / sha[:2] / sha[2:4] / sha


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).lower()


out = []
visti = set()
for l in (D / "estratti.jsonl").open(encoding="utf-8"):
    d = json.loads(l)
    sha = d.get("sha256")
    if not sha or sha in visti or d.get("pagine") is None:
        continue
    visti.add(sha)
    p = blob(sha)
    pagine = []
    for i in range(1, d["pagine"] + 1):
        r = subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), "-layout", str(p), "-"], capture_output=True, text=True, errors="replace")
        pagine.append(r.stdout)
    tutto = norm("\n".join(pagine))
    tr = {
        "sha256": sha,
        "url": d["url"],
        "confidenziale": bool(re.search(r"confidenzial\w*\W{0,3} di propriet", tutto)),
        "non_pubblicabile": bool(re.search(r"non possono essere (pubblicat|divulgat|riprodott)", tutto)),
        "pagine_vuote": sum(1 for t in pagine if len(t.strip()) < 40),
        "pagine": d["pagine"],
    }
    # pagine del Configuratore: titolo di capitolo "Configuratore" (non nell'indice)
    conf = [i for i, t in enumerate(pagine, 1) if re.search(r"^\s*(\d+\s+)?CONFIGURATORE\s*$", t, re.I | re.M) and not re.search(r"\.{5,}", t)]
    tr["pagine_configuratore"] = conf
    ocrfiles = []
    for c in conf:
        for i in range(c, min(c + 4, d["pagine"]) + 1):
            o = OCR / f"{sha}-p{i}.txt"
            if not o.exists():
                png = OCR / f"{sha}-p{i}"
                subprocess.run(["nice", "pdftoppm", "-r", "300", "-f", str(i), "-l", str(i), "-png", "-singlefile", str(p), str(png)], check=False)
                subprocess.run(["nice", "tesseract", f"{png}.png", str(o)[:-4], "-l", "ita", "--psm", "6"], capture_output=True)
                Path(f"{png}.png").unlink(missing_ok=True)
            ocrfiles.append(o.name)
    tr["ocr"] = ocrfiles
    out.append(tr)
    print(tr["pagine"], conf, tr["confidenziale"], d["url"][:80], flush=True)

with (D / "tratti.jsonl").open("w", encoding="utf-8") as f:
    for t in out:
        f.write(json.dumps(t, ensure_ascii=False) + "\n")
