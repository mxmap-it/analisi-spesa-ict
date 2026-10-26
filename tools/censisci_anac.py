#!/usr/bin/env python3
"""Censimento completo delle risorse ANAC, con le dimensioni vere.

Enumera i dataset dal catalogo CKAN, ne estrae tutte le risorse in tutti i
formati e per ciascuna chiede al server la dimensione effettiva con un HEAD:
il campo `size` del catalogo descrive il file scompattato e sbaglia di circa
4,5 volte.

Produce `config/anac-risorse.jsonl` (una riga per risorsa, con dimensione
dichiarata e reale) e un piano di scarico ordinato per priorità.

    censisci_anac.py                  # tutto
    censisci_anac.py --formati CSV    # solo un formato
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import requests

BASE = Path(__file__).resolve().parent.parent
API = "https://dati.anticorruzione.it/opendata/api/3/action"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/140.0 Safari/537.36 analisi-spesa-ict (+https://github.com/mxmap-it/analisi-spesa-ict)")
HEADERS = {"User-Agent": UA, "Accept": "application/json", "Accept-Language": "it-IT,it;q=0.9"}
PAUSA = 1.0

# Le risorse che servono prima: deperibili (spariscono) e nel perimetro ICT.
DEPERIBILI = {"cig", "smartcig", "aggiudicazioni", "aggiudicatari", "partecipanti",
              "subappalti", "quadro-economico", "stati-avanzamento", "avvio-contratto",
              "fine-contratto", "varianti", "collaudo", "fonti-finanziamento",
              "pubblicazioni", "cup", "stazioni-appaltanti", "centri-di-costo"}


def api(sess, azione: str, **p) -> dict:
    for tentativo in range(4):
        try:
            r = sess.get(f"{API}/{azione}", params=p, headers=HEADERS, timeout=120)
            if r.status_code == 200:
                return r.json()["result"]
            if r.status_code in (429, 500, 502, 503):
                time.sleep(5 * (tentativo + 1))
                continue
            r.raise_for_status()
        except (requests.RequestException, ValueError, KeyError):
            time.sleep(5 * (tentativo + 1))
    raise RuntimeError(f"{azione} {p} non risponde")


def dimensione_reale(sess, url: str) -> tuple[int | None, str | None, int | None]:
    """(byte, last-modified, stato http) dal server, non dal catalogo."""
    try:
        r = sess.head(url, headers={**HEADERS, "Accept": "*/*"}, timeout=90, allow_redirects=True)
        cl = r.headers.get("Content-Length")
        return (int(cl) if (cl or "").isdigit() else None,
                r.headers.get("Last-Modified"), r.status_code)
    except requests.RequestException:
        return None, None, None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--formati", nargs="*", help="es. CSV JSON TTL; default tutti")
    ap.add_argument("--out", type=Path, default=BASE / "config" / "anac-risorse.jsonl")
    a = ap.parse_args()
    formati = {f.upper() for f in a.formati} if a.formati else None

    sess = requests.Session()
    nomi = api(sess, "package_list")
    print(f"dataset nel catalogo: {len(nomi)}\n", flush=True)

    righe = []
    for i, nome in enumerate(sorted(nomi), 1):
        time.sleep(PAUSA)
        try:
            d = api(sess, "package_show", id=nome)
        except RuntimeError as e:
            print(f"[{i}/{len(nomi)}] {nome}: NON LEGGIBILE ({e})", flush=True)
            continue
        ris = d.get("resources", [])
        tenute = 0
        for r in ris:
            fmt = (r.get("format") or "").upper()
            if formati and fmt not in formati:
                continue
            url = r.get("url")
            if not url:
                continue
            time.sleep(PAUSA)
            reale, lm, http = dimensione_reale(sess, url)
            righe.append({
                "dataset": nome, "risorsa": r.get("name"), "formato": fmt, "url": url,
                "dim_dichiarata": int(r["size"]) if str(r.get("size") or "").isdigit() else None,
                "dim_reale": reale, "last_modified": lm, "http": http,
                "deperibile": nome in DEPERIBILI,
                "licenza": d.get("license_title"),
            })
            tenute += 1
        dich = sum(x["dim_dichiarata"] or 0 for x in righe if x["dataset"] == nome)
        vera = sum(x["dim_reale"] or 0 for x in righe if x["dataset"] == nome)
        print(f"[{i}/{len(nomi)}] {nome:28s} risorse {tenute:>3}  "
              f"dichiarato {dich/1e6:>8.0f} MB  reale {vera/1e6:>8.0f} MB", flush=True)

    a.out.parent.mkdir(parents=True, exist_ok=True)
    with a.out.open("w", encoding="utf-8") as f:
        for r in righe:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    ok = [r for r in righe if r["http"] == 200]
    rotte = [r for r in righe if r["http"] not in (200, None)]
    per_formato: dict[str, list[int]] = {}
    for r in ok:
        per_formato.setdefault(r["formato"], []).append(r["dim_reale"] or 0)

    print(f"\nrisorse censite: {len(righe)}   scaricabili: {len(ok)}   non scaricabili: {len(rotte)}")
    print("\nper formato (dimensione reale):")
    for fmt, v in sorted(per_formato.items(), key=lambda x: -sum(x[1])):
        print(f"  {fmt or '(vuoto)':8s} {len(v):>4} risorse  {sum(v)/1e9:>7.2f} GB")
    dich = sum(r["dim_dichiarata"] or 0 for r in ok)
    vera = sum(r["dim_reale"] or 0 for r in ok)
    print(f"\ntotale dichiarato dal catalogo: {dich/1e9:.2f} GB")
    print(f"totale reale servito:           {vera/1e9:.2f} GB")
    if vera:
        print(f"il catalogo sovrastima di {dich/vera:.1f} volte")
    if rotte:
        print(f"\nrisorse elencate nel catalogo ma non scaricabili: {len(rotte)}")
        for r in rotte[:15]:
            print(f"  {r['http']}  {r['dataset']}/{r['risorsa']} [{r['formato']}]")
    print(f"\nscritto {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
