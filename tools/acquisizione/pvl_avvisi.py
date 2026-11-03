#!/usr/bin/env python3
"""Scaricatore degli avvisi della Pubblicità a valore legale (PVL) di ANAC (#57).

Perché: il link ai documenti di gara / pagina dell'ente che dettaglio-cig mostra
in fondo alla scheda (campo LINK_SITO_COMMITTENTE, API protetta da CAPTCHA
mosparo) non è nei dataset bulk. Lo stesso dato, come `documenti_di_gara_link`,
è negli avvisi PVL, esposti da un'API JSON pubblica senza CAPTCHA:

    GET https://pubblicitalegale.anticorruzione.it/api/v0/avvisi
        ?dataPubblicazioneStart=DD/MM/YYYY&dataPubblicazioneEnd=DD/MM/YYYY
        &page=N&size=1000&sortField=idAvviso&sortDirection=ASC

Metodo: un giorno di pubblicazione alla volta, pagine da 1000 ordinate per
idAvviso (ordine stabile). Ogni pagina grezza finisce in un blob indirizzato per
contenuto (stessa struttura di tools/archivia.py, ma gzip) e una riga in
`indice.jsonl`. Un giorno è «fatto» solo se gli idAvviso unici raccolti
coincidono con totalElements; altrimenti si registra la discrepanza.
Ripartibile: i giorni chiusi in `stato.jsonl` non si riscaricano.

    pvl_avvisi.py scarica --da 2024-01-01 --a 2026-11-03 [--pausa 2]
    pvl_avvisi.py estrai  > lavoro/pvl/link_cig.csv   (streaming dai blob)
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import os
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import requests

BASE = Path(__file__).resolve().parents[2]
ROOT = Path(os.environ.get("ARCHIVIO_ROOT", BASE / "archivio"))
LAVORO = Path(os.environ.get("PVL_LAVORO", BASE / "lavoro" / "pvl"))
API = "https://pubblicitalegale.anticorruzione.it/api/v0/avvisi"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/140.0 Safari/537.36 analisi-spesa-ict (+https://github.com/mxmap-it/analisi-spesa-ict)")
SIZE = 1000


def ora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def salva_blob(raw: bytes) -> str:
    h = hashlib.sha256(raw).hexdigest()
    p = ROOT / "blobs" / "sha256" / h[:2] / h[2:4] / f"{h}.json.gz"
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(".part")
        with gzip.open(tmp, "wb") as f:
            f.write(raw)
        tmp.replace(p)
    return h


def blob_path(h: str) -> Path:
    return ROOT / "blobs" / "sha256" / h[:2] / h[2:4] / f"{h}.json.gz"


def giorni_fatti() -> set[str]:
    s = LAVORO / "stato.jsonl"
    if not s.exists():
        return set()
    out = set()
    for r in s.open(encoding="utf-8"):
        try:
            d = json.loads(r)
        except ValueError:
            continue
        if d.get("esito") == "ok":
            out.add(d["giorno"])
    return out


def scrivi(nome: str, rec: dict) -> None:
    with (LAVORO / nome).open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def get(sess: requests.Session, params: dict, pausa: float) -> bytes:
    attesa = 30
    for tentativo in range(8):
        time.sleep(pausa)
        try:
            r = sess.get(API, params=params, timeout=120)
            if r.status_code == 200:
                return r.content
            errore = f"HTTP {r.status_code}"
        except requests.RequestException as e:
            errore = repr(e)
        print(f"{ora()} {params.get('dataPubblicazioneStart')} p{params.get('page')} "
              f"{errore}; riprovo fra {attesa}s", file=sys.stderr, flush=True)
        time.sleep(attesa)
        attesa = min(attesa * 2, 1800)
    raise RuntimeError(f"troppi errori: {params}")


def scarica(da: date, a: date, pausa: float) -> None:
    LAVORO.mkdir(parents=True, exist_ok=True)
    fatti = giorni_fatti()
    sess = requests.Session()
    sess.headers.update({"User-Agent": UA, "Accept": "application/json"})
    g = da
    while g <= a:
        k = g.isoformat()
        if k in fatti:
            g += timedelta(days=1)
            continue
        d = g.strftime("%d/%m/%Y")
        ids: set[str] = set()
        page, totale, pagine = 0, None, 0
        while True:
            params = {"dataPubblicazioneStart": d, "dataPubblicazioneEnd": d, "page": page,
                      "size": SIZE, "sortField": "idAvviso", "sortDirection": "ASC"}
            raw = get(sess, params, pausa)
            j = json.loads(raw)
            h = salva_blob(raw)
            totale = j.get("totalElements")
            n = len(j.get("content") or [])
            ids.update(x.get("idAvviso") for x in j.get("content") or [])
            scrivi("indice.jsonl", {"giorno": k, "page": page, "n": n, "totale": totale,
                                    "sha256": h, "bytes": len(raw), "ts": ora()})
            pagine += 1
            if j.get("last", True) or n == 0:
                break
            page += 1
        esito = "ok" if totale == len(ids) else "discrepanza"
        scrivi("stato.jsonl", {"giorno": k, "esito": esito, "totale": totale,
                               "unici": len(ids), "pagine": pagine, "ts": ora()})
        print(f"{ora()} {k} {esito} totale={totale} unici={len(ids)} pagine={pagine}", flush=True)
        g += timedelta(days=1)


def cammina(x, chiave_cig: list, chiave_link: list, sito: list) -> None:
    if isinstance(x, dict):
        for kk, v in x.items():
            if kk == "cig" and isinstance(v, str) and v:
                chiave_cig.append(v)
            elif kk == "indirizzo_internet_sa" and isinstance(v, str) and v.strip():
                sito.append(v.strip())
            elif kk == "documenti_di_gara_link" and isinstance(v, str) and v.strip():
                chiave_link.append(v.strip())
            else:
                cammina(v, chiave_cig, chiave_link, sito)
    elif isinstance(x, list):
        for v in x:
            cammina(v, chiave_cig, chiave_link, sito)


def estrai(out) -> None:
    """Una riga per (avviso, cig): streaming pagina per pagina, nessun CIG in memoria."""
    w = csv.writer(out)
    w.writerow(["cig", "id_avviso", "id_appalto", "codice_scheda", "tipologia",
                "data_pubblicazione", "cf_sa", "documenti_di_gara_link", "indirizzo_internet_sa", "link_eform_ted", "sha256_pagina"])
    visti: set[str] = set()
    for r in (LAVORO / "indice.jsonl").open(encoding="utf-8"):
        h = json.loads(r)["sha256"]
        if h in visti:
            continue
        visti.add(h)
        with gzip.open(blob_path(h), "rb") as f:
            j = json.load(f)
        for a in j.get("content") or []:
            cigs, links, siti, cf = [], [], [], ""
            ted = ""
            for t in a.get("templates") or []:
                tpl = t.get("template") or {}
                ted = ted or ((tpl.get("metadata") or {}).get("link_eform_ted") or "")
                cammina(tpl.get("sections"), cigs, links, siti)
                for s in tpl.get("sections") or []:
                    for sa in (s.get("fields") or {}).get("soggetti_sa") or []:
                        cf = cf or sa.get("codice_fiscale", "")
            link = " | ".join(dict.fromkeys(links))
            for c in dict.fromkeys(cigs) or [""]:
                w.writerow([c, a.get("idAvviso"), a.get("idAppalto"), a.get("codiceScheda"),
                            a.get("tipologia"), a.get("dataPubblicazione"), cf, link,
                            " | ".join(dict.fromkeys(siti)), ted, h])


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scarica")
    s.add_argument("--da", default="2024-01-01")
    s.add_argument("--a", default=date.today().isoformat())
    s.add_argument("--pausa", type=float, default=2.0)
    sub.add_parser("estrai")
    a = ap.parse_args()
    if a.cmd == "scarica":
        scarica(date.fromisoformat(a.da), date.fromisoformat(a.a), max(a.pausa, 1.0))
    else:
        estrai(sys.stdout)


if __name__ == "__main__":
    main()
