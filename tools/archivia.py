#!/usr/bin/env python3
"""Archivio append-only delle risorse pubbliche.

Ogni risorsa scaricata finisce in un blob indirizzato per contenuto
(`blobs/sha256/ab/cd/<hash>`) e mai sovrascritto. Una vista `mirror/` riproduce
i percorsi originali (`mirror/<host>/<path>`) con un hardlink alla versione più
recente: chi oggi scarica dalla fonte può puntare a noi cambiando solo l'URL di
base. Ogni tentativo, riuscito o no, è una riga di `manifest.jsonl`.

Idempotente: prima un HEAD; se dimensione e Last-Modified coincidono con l'ultima
acquisizione riuscita non si riscarica. Se si riscarica e l'hash è identico, non
si crea un nuovo blob. Ripartibile: un'interruzione lascia al più un file `.part`.

La radice dell'archivio viene da ARCHIVIO_ROOT, così l'archivio si sposta con un
rsync senza toccare il codice.

    archivia.py URL [URL ...]
    archivia.py --lista risorse.txt
    archivia.py --da-file FILE --url URL_ORIGINALE --data DATA_ISO [--nota TESTO]

Con --da-file si porta nell'archivio una copia già scaricata con altri mezzi
(Chrome headless, quando l'allegato è un POST JSF o un URL monouso): sha256, blob
se manca (copia; l'originale resta), vista e riga di manifest con
via="browser-headless" e la data originale dello scaricamento. Per non collidere
con la pagina, la vista sta in mirror/<host>/<path>__allegati/<query>/<frammento>.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

import requests

ROOT = Path(os.environ.get("ARCHIVIO_ROOT", Path(__file__).resolve().parent.parent / "archivio"))
MANIFEST = ROOT / "manifest.jsonl"

# ANAC respinge gli user-agent che non sembrano browser. Ci dichiariamo comunque,
# così chi amministra i portali può riconoscere il traffico e scriverci.
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/140.0 Safari/537.36 analisi-spesa-ict (+https://github.com/mxmap-it/analisi-spesa-ict)")
HEADERS = {"User-Agent": UA, "Accept": "*/*", "Accept-Language": "it-IT,it;q=0.9"}
PAUSA_S = 1.0  # una richiesta al secondo: i portali pubblici non dichiarano quote
CHUNK = 1 << 20


def adesso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def ultima_riuscita(url: str) -> dict | None:
    if not MANIFEST.exists():
        return None
    ultima = None
    with MANIFEST.open(encoding="utf-8") as f:
        for riga in f:
            r = json.loads(riga)
            if r["url"] == url and r["esito"] in ("nuovo", "invariato"):
                ultima = r
    return ultima


def scrivi_manifest(rec: dict) -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def percorso_blob(sha: str) -> Path:
    return ROOT / "blobs" / "sha256" / sha[:2] / sha[2:4] / sha


def percorso_mirror(url: str) -> Path:
    p = urlsplit(url)
    return ROOT / "mirror" / p.netloc / p.path.lstrip("/")


def aggiorna_vista(url: str, sha: str) -> None:
    dest = percorso_mirror(url)
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".link")
    if tmp.exists():
        tmp.unlink()
    os.link(percorso_blob(sha), tmp)
    os.replace(tmp, dest)


def archivia(sess: requests.Session, url: str, accetta_html: bool = False) -> dict:
    """accetta_html=True per pagine web vere (es. Amministrazione trasparente, tools/llm/atti.py)."""
    rec = {"acquisito": adesso(), "url": url}
    prec = ultima_riuscita(url)
    t0 = time.monotonic()
    try:
        h = sess.head(url, headers=HEADERS, timeout=60, allow_redirects=True)
        rec.update(http_head=h.status_code,
                   dimensione_dichiarata=int(h.headers["Content-Length"]) if "Content-Length" in h.headers else None,
                   last_modified=h.headers.get("Last-Modified"),
                   etag=h.headers.get("ETag"),
                   tipo=h.headers.get("Content-Type"))
        if h.status_code == 404:
            rec.update(esito="assente", secondi=round(time.monotonic() - t0, 2))
            return rec
        if (prec and h.status_code == 200 and rec["last_modified"]
                and rec["last_modified"] == prec.get("last_modified")
                and rec["dimensione_dichiarata"] == prec.get("dimensione")):
            rec.update(esito="invariato", sha256=prec["sha256"], dimensione=prec["dimensione"],
                       verifica="head", secondi=round(time.monotonic() - t0, 2))
            return rec

        time.sleep(PAUSA_S)
        part = ROOT / "tmp" / (hashlib.sha256(url.encode()).hexdigest() + ".part")
        part.parent.mkdir(parents=True, exist_ok=True)
        sha = hashlib.sha256()
        n = 0
        with sess.get(url, headers=HEADERS, timeout=(60, 900), stream=True) as r:
            rec["http"] = r.status_code
            if r.status_code != 200:
                rec.update(esito="errore", errore=f"HTTP {r.status_code}",
                           secondi=round(time.monotonic() - t0, 2))
                return rec
            # Il WAF di ANAC risponde 200 con una pagina HTML invece del file.
            ctype = r.headers.get("Content-Type", "")
            with part.open("wb") as f:
                for blocco in r.iter_content(CHUNK):
                    f.write(blocco)
                    sha.update(blocco)
                    n += len(blocco)
        digest = sha.hexdigest()
        if "text/html" in ctype and not accetta_html and not url.endswith((".html", ".htm")):
            part.unlink(missing_ok=True)
            rec.update(esito="errore", errore="risposta HTML al posto del file: probabile blocco WAF",
                       dimensione=n, secondi=round(time.monotonic() - t0, 2))
            return rec

        # Uno zip è valido solo se ha la firma PK e supera il test di integrità
        # (pratica ripresa da scripts/anac_archivio_mensile.sh di Cruscotto Italia).
        if url.lower().endswith(".zip"):
            import zipfile
            try:
                with zipfile.ZipFile(part) as zf:
                    rotto = zf.testzip()
            except zipfile.BadZipFile:
                rotto = "non è uno zip"
            if rotto:
                part.unlink(missing_ok=True)
                rec.update(esito="errore", errore=f"zip non valido: {rotto}",
                           dimensione=n, secondi=round(time.monotonic() - t0, 2))
                return rec

        blob = percorso_blob(digest)
        if blob.exists():
            part.unlink()
            esito = "invariato"
        else:
            blob.parent.mkdir(parents=True, exist_ok=True)
            os.replace(part, blob)
            esito = "nuovo"
        aggiorna_vista(url, digest)
        rec.update(esito=esito, sha256=digest, dimensione=n, verifica="hash",
                   secondi=round(time.monotonic() - t0, 2))
        return rec
    except requests.RequestException as e:
        rec.update(esito="errore", errore=f"{type(e).__name__}: {e}",
                   secondi=round(time.monotonic() - t0, 2))
        return rec


def percorso_mirror_file(url: str) -> Path:
    p = urlsplit(url)
    base = ROOT / "mirror" / p.netloc / p.path.lstrip("/")
    if not (p.query or p.fragment):
        return base
    dest = base.with_name(base.name + "__allegati")
    if p.query:
        dest = dest / p.query.replace("/", "_")
    return dest / (p.fragment.replace("/", "_") or "_")


def archivia_file(sorgente: Path, url: str, data: str, via: str = "browser-headless",
                  nota: str | None = None) -> dict:
    """Porta nell'archivio una copia locale già scaricata, senza toccare l'originale."""
    import shutil
    rec = {"acquisito": data, "archiviato": adesso(), "url": url, "via": via,
           "origine_locale": str(sorgente)}
    if nota:
        rec["nota"] = nota
    sha = hashlib.sha256()
    with sorgente.open("rb") as f:
        for blocco in iter(lambda: f.read(CHUNK), b""):
            sha.update(blocco)
    digest = sha.hexdigest()
    blob = percorso_blob(digest)
    if blob.exists():
        esito = "invariato"
    else:
        part = ROOT / "tmp" / (digest + ".part")
        part.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(sorgente, part)
        blob.parent.mkdir(parents=True, exist_ok=True)
        os.replace(part, blob)
        esito = "nuovo"
    dest = percorso_mirror_file(url)
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".link")
    if tmp.exists():
        tmp.unlink()
    os.link(blob, tmp)
    os.replace(tmp, dest)
    rec.update(esito=esito, sha256=digest, dimensione=blob.stat().st_size, verifica="hash",
               mirror=str(dest.relative_to(ROOT)))
    return rec


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url", nargs="*")
    ap.add_argument("--lista", type=Path, help="file con un URL per riga")
    ap.add_argument("--da-file", type=Path, help="copia locale già scaricata da archiviare")
    ap.add_argument("--url", help="con --da-file: URL originale (o pagina + #nome per URL monouso)")
    ap.add_argument("--data", help="con --da-file: data ISO dello scaricamento originale")
    ap.add_argument("--nota", help="con --da-file: annotazione nel manifest")
    a = ap.parse_args()
    if a.da_file:
        if not (a.url and a.data):
            ap.error("--da-file richiede --url e --data")
        rec = archivia_file(a.da_file, a.url, a.data, nota=a.nota)
        scrivi_manifest(rec)
        print(f"{rec['esito']:9s} {rec['sha256']}  {a.url}")
        return 0
    urls = list(a.url)
    if a.lista:
        urls += [u.strip() for u in a.lista.read_text(encoding="utf-8").splitlines()
                 if u.strip() and not u.startswith("#")]
    if not urls:
        ap.error("nessun URL")
    sess = requests.Session()
    errori = 0
    for url in urls:
        rec = archivia(sess, url)
        scrivi_manifest(rec)
        if rec["esito"] == "errore":
            errori += 1
        mb = (rec.get("dimensione") or 0) / 1e6
        print(f"{rec['esito']:9s} {mb:9.1f} MB  {url}", flush=True)
        time.sleep(PAUSA_S)
    return 1 if errori else 0


if __name__ == "__main__":
    sys.exit(main())
