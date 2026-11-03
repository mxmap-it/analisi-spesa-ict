#!/usr/bin/env python3
"""Verifica a campione dei link ai documenti per sistema (#57).

Per ogni dominio di `lavoro/pvl/sistemi.csv` (i primi --top per numero di CIG,
più --casuali presi a caso fra gli altri) apre `link_esempio` una volta:
codice HTTP, URL finale, tipo di contenuto, indizi di login, numero di link a
documenti scaricabili (.pdf .p7m .zip .doc .xls .odt .rar) nella pagina.
Il corpo va nell'archivio content-addressed (gzip). Una richiesta ogni >= 3 s,
nessun login, nessun CAPTCHA. Ripartibile: salta i domini già in uscita.

    pvl_verifica_link.py [--top 300] [--casuali 100]
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import os
import random
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

BASE = Path(__file__).resolve().parents[2]
ROOT = Path(os.environ.get("ARCHIVIO_ROOT", BASE / "archivio"))
P = BASE / "lavoro" / "pvl"
OUT = P / "verifica_link.csv"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/140.0 Safari/537.36 analisi-spesa-ict (+https://github.com/mxmap-it/analisi-spesa-ict)")
DOC = re.compile(rb"""href=["'][^"']+\.(pdf|p7m|zip|docx?|xlsx?|odt|rar)(\?[^"']*)?["']""", re.I)
LOGIN = re.compile(rb"""type=["']password["']|spid|/login|accedi\b|area riservata""", re.I)
CAMPI = ["dominio", "link", "http", "url_finale", "content_type", "bytes", "login", "n_link_documenti",
         "esito", "sha256", "ts"]


def blob(raw: bytes) -> str:
    h = hashlib.sha256(raw).hexdigest()
    p = ROOT / "blobs" / "sha256" / h[:2] / h[2:4] / f"{h}.gz"
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        with gzip.open(p.with_suffix(".part"), "wb") as f:
            f.write(raw)
        p.with_suffix(".part").replace(p)
    return h


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=300)
    ap.add_argument("--casuali", type=int, default=100)
    ap.add_argument("--pausa", type=float, default=3.0)
    a = ap.parse_args()
    righe = list(csv.DictReader((P / "sistemi.csv").open(encoding="utf-8")))
    scelti = righe[:a.top]
    resto = righe[a.top:]
    random.Random(57).shuffle(resto)
    scelti += resto[:a.casuali]
    fatti = set()
    if OUT.exists():
        fatti = {r["dominio"] for r in csv.DictReader(OUT.open(encoding="utf-8"))}
    nuovo = not OUT.exists()
    s = requests.Session()
    s.headers["User-Agent"] = UA
    with OUT.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, CAMPI)
        if nuovo:
            w.writeheader()
        for r in scelti:
            if r["dominio"] in fatti:
                continue
            link = r["link_esempio"].strip()
            url = link if "://" in link else "https://" + link
            rec = {"dominio": r["dominio"], "link": link, "ts": datetime.now(timezone.utc).isoformat(timespec="seconds")}
            try:
                x = s.get(url, timeout=40, allow_redirects=True, stream=True)
                raw = x.raw.read(5_000_000, decode_content=True)
                ct = x.headers.get("content-type", "")
                rec.update(http=x.status_code, url_finale=x.url, content_type=ct, bytes=len(raw), sha256=blob(raw),
                           login=bool(LOGIN.search(raw)), n_link_documenti=len(DOC.findall(raw)))
                if x.status_code >= 400:
                    rec["esito"] = "errore http"
                elif "html" not in ct.lower():
                    rec["esito"] = "documento diretto"
                elif rec["n_link_documenti"]:
                    rec["esito"] = "documenti scaricabili"
                elif rec["login"]:
                    rec["esito"] = "login o area riservata"
                else:
                    rec["esito"] = "pagina senza documenti visibili"
            except requests.RequestException as e:
                rec.update(esito="non risponde", content_type=type(e).__name__)
            w.writerow(rec)
            f.flush()
            print(rec["dominio"], rec.get("http"), rec["esito"], flush=True)
            time.sleep(a.pausa)


if __name__ == "__main__":
    main()
