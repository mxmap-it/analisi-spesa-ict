#!/usr/bin/env python3
"""Collega un CIG a un documento (determina, contratto, convenzione): lo archivia, ne estrae il testo, lo registra.

    atti.py CIG URL [--metodo "ricerca web" --query "..." --tipo determina --ente "..."]

1. scarica l'URL nell'archivio append-only content-addressed (tools/archivia.py, sha256);
2. estrae il testo: pdftotext; se il PDF non ha testo (scansione) OCR con tesseract (ita); HTML -> testo;
3. salva il testo in dati/atti/testi/<sha256>.txt e appende una riga spesaict.atto/1 a dati/atti/atti-server.jsonl;
4. stampa JSON con l'esito, la pertinenza (il CIG compare nel testo?) e i primi 3000 caratteri del testo.

Pensato per essere chiamato dall'agente che classifica (claude -p) al posto di WebFetch, che non legge i PDF.
Schema: schemi/atto.schema.json. Metodo: sito/content/progetto/formato-classificazione.md
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

RADICE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RADICE / "tools"))
import archivia  # noqa: E402

TESTI = RADICE / "dati/atti/testi"
REGISTRO = RADICE / "dati/atti/atti-server.jsonl"


def testo_pdf(blob: Path) -> tuple[str, bool]:
    t = subprocess.run(["pdftotext", "-layout", str(blob), "-"], capture_output=True, text=True, errors="replace").stdout
    if len(re.sub(r"\s", "", t)) > 200:
        return t, False
    # scansione: OCR pagina per pagina (massimo 30 pagine per non caricare il server condiviso)
    with tempfile.TemporaryDirectory(dir=RADICE / "lavoro") as d:
        subprocess.run(["pdftoppm", "-r", "200", "-l", "30", "-png", str(blob), f"{d}/p"], capture_output=True)
        parti = []
        for img in sorted(Path(d).glob("p*.png")):
            parti.append(subprocess.run(["nice", "tesseract", str(img), "-", "-l", "ita"], capture_output=True,
                                        text=True, errors="replace").stdout)
    return "\n".join(parti), True


def testo_html(blob: Path) -> str:
    h = blob.read_text(encoding="utf-8", errors="replace")
    h = re.sub(r"(?is)<(script|style).*?</\1>", " ", h)
    return re.sub(r"[ \t]+", " ", unescape(re.sub(r"<[^>]+>", " ", h)))


def main() -> int:
    a = argparse.ArgumentParser()
    a.add_argument("cig"); a.add_argument("url")
    a.add_argument("--metodo", default=""); a.add_argument("--query", default="")
    a.add_argument("--tipo", default="altro"); a.add_argument("--ente", default="")
    x = a.parse_args()
    sess = archivia.requests.Session()
    sess.headers["User-Agent"] = archivia.UA
    rec = archivia.archivia(sess, x.url)
    archivia.scrivi_manifest(rec)
    sha = rec.get("sha256") or (archivia.ultima_riuscita(x.url) or {}).get("sha256")
    out = {"schema": "spesaict.atto/1", "cig": x.cig, "url": x.url,
           "trovato_con": {"metodo": x.metodo, "query": x.query},
           "recuperato_il": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "http_status": rec.get("http"), "mime": rec.get("tipo", ""), "byte": rec.get("dimensione"),
           "sha256": sha or "", "tipo_atto": x.tipo, "ente": x.ente}
    if not sha:
        out.update(esito_recupero="bloccato" if rec.get("http") in (401, 403, 429) else "non-trovato", nota=str(rec.get("errore", "")))
        testo = ""
    else:
        blob = archivia.percorso_blob(sha)
        pdf = blob.read_bytes()[:5] == b"%PDF-"
        testo, ocr = testo_pdf(blob) if pdf else (testo_html(blob), False)
        tsha = hashlib.sha256(testo.encode()).hexdigest()
        TESTI.mkdir(parents=True, exist_ok=True)
        (TESTI / f"{sha}.txt").write_text(testo, encoding="utf-8")
        out["estrazione"] = {"strumento": "tesseract" if ocr else ("pdftotext" if pdf else "html"), "ocr": ocr,
                             "testo_sha256": tsha, "caratteri": len(testo)}
        out["pertinenza"] = "cig-citato" if x.cig.upper() in testo.upper() else "contesto"
        out["esito_recupero"] = "ok" if len(testo.strip()) > 100 else "illeggibile"
    REGISTRO.parent.mkdir(parents=True, exist_ok=True)
    with REGISTRO.open("a", encoding="utf-8") as f:
        f.write(json.dumps(out, ensure_ascii=False) + "\n")
    print(json.dumps({**out, "testo_estratto": testo[:3000]}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
