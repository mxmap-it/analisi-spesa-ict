#!/usr/bin/env python3
"""Sonda di disponibilità su tutte le risorse del registry.

Per ogni risorsa una richiesta HEAD (con fallback a GET parziale quando il
server non gradisce HEAD) e una riga di esito in `stato/sonda/<data>.jsonl`,
mai sovrascritta: è lo storico da cui si calcolano continuità e persistenza.

I modelli temporali del registry vengono espansi in risorse concrete: una riga
per mese o per anno, così la sonda vede i buchi uno per uno.

Non scarica il contenuto e non consuma token: l'unico limite è la cortesia
verso i portali, una richiesta al secondo per autorità.

    sonda.py                      # tutte le risorse
    sonda.py --autorita anac      # una sola autorità
    sonda.py --solo-ict
"""
from __future__ import annotations

import argparse
import json
import os
import time
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

import requests
import yaml

BASE = Path(__file__).resolve().parent.parent
REGISTRY = BASE / "config" / "risorse.yaml"
STATO = Path(os.environ.get("STATO_ROOT", BASE / "stato")) / "sonda"

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/140.0 Safari/537.36 analisi-spesa-ict (+https://github.com/mxmap-it/analisi-spesa-ict)")
HEADERS = {"User-Agent": UA, "Accept": "*/*", "Accept-Language": "it-IT,it;q=0.9"}
PAUSA_S = 1.0


def mesi(da: str, a: str):
    """Sequenza AAAA-MM inclusiva."""
    y1, m1 = (int(x) for x in da.split("-"))
    y2, m2 = (int(x) for x in a.split("-"))
    while (y1, m1) <= (y2, m2):
        yield y1, m1
        m1 += 1
        if m1 == 13:
            y1, m1 = y1 + 1, 1


def espandi(r: dict, oggi: date) -> list[dict]:
    """Un modello temporale diventa una lista di risorse concrete."""
    modello = r.get("modello")
    if not modello:
        return [dict(r, periodo=None)]
    fine_mese = f"{oggi.year}-{oggi.month:02d}"
    out = []
    if modello == "mensile":
        for y, m in mesi(r.get("da", fine_mese), r.get("a", fine_mese)):
            out.append(dict(r, periodo=f"{y}-{m:02d}",
                            url=r["url"].replace("{AAAAMM}", f"{y}{m:02d}")))
    elif modello == "annuale":
        for y in range(int(r.get("da", oggi.year)), int(r.get("a", oggi.year)) + 1):
            out.append(dict(r, periodo=str(y), url=r["url"].replace("{AAAA}", str(y))))
    elif modello == "annuale-mensile":
        for y in range(int(r.get("da", oggi.year)), int(r.get("a", oggi.year)) + 1):
            ultimo = oggi.month if y == oggi.year else 12
            for m in range(1, ultimo + 1):
                out.append(dict(r, periodo=f"{y}-{m:02d}",
                                url=r["url"].replace("{AAAA}", str(y)).replace("{MM}", f"{m:02d}")))
    else:
        raise ValueError(f"modello sconosciuto: {modello}")
    return out


def sonda(sess: requests.Session, r: dict) -> dict:
    rec = {"istante": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "autorita": r["autorita"], "dataset": r["dataset"], "periodo": r.get("periodo"),
           "url": r["url"], "specchia": bool(r.get("specchia")), "ict": bool(r.get("ict"))}
    t0 = time.monotonic()
    try:
        resp = sess.head(r["url"], headers=HEADERS, timeout=60, allow_redirects=True)
        metodo = "HEAD"
        # Alcuni portali rifiutano o ignorano HEAD: si riprova con un GET minimo.
        if resp.status_code in (403, 405, 501) or (resp.status_code == 200 and "Content-Length" not in resp.headers):
            time.sleep(PAUSA_S)
            resp = sess.get(r["url"], headers={**HEADERS, "Range": "bytes=0-0"},
                            timeout=60, allow_redirects=True, stream=True)
            resp.close()
            metodo = "GET-range"
        dim = resp.headers.get("Content-Length")
        cr = resp.headers.get("Content-Range")
        if metodo == "GET-range" and cr and "/" in cr:
            dim = cr.rsplit("/", 1)[1]
        tipo = resp.headers.get("Content-Type", "")
        rec.update(metodo=metodo, http=resp.status_code,
                   dimensione=int(dim) if (dim or "").isdigit() else None,
                   last_modified=resp.headers.get("Last-Modified"),
                   etag=resp.headers.get("ETag"), tipo=tipo or None,
                   accept_ranges=resp.headers.get("Accept-Ranges"),
                   secondi=round(time.monotonic() - t0, 2))
        if resp.status_code == 200:
            # Risposta HTML su una risorsa che dovrebbe essere un file: tipico del WAF.
            atteso_html = r["url"].rstrip("/").endswith((".html", "/opendata", "opendata/"))
            rec["esito"] = "bloccato" if ("text/html" in tipo and not atteso_html) else "disponibile"
        elif resp.status_code == 404:
            rec["esito"] = "assente"
        elif resp.status_code in (401, 403):
            rec["esito"] = "negato"
        else:
            rec["esito"] = "errore"
        return rec
    except requests.RequestException as e:
        rec.update(esito="irraggiungibile", errore=f"{type(e).__name__}",
                   secondi=round(time.monotonic() - t0, 2))
        return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--autorita")
    ap.add_argument("--solo-ict", action="store_true")
    ap.add_argument("--oggi", default=date.today().isoformat())
    a = ap.parse_args()
    oggi = date.fromisoformat(a.oggi)

    reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    risorse: list[dict] = []
    for r in reg["risorse"]:
        if a.autorita and r["autorita"] != a.autorita:
            continue
        if a.solo_ict and not r.get("ict"):
            continue
        risorse += espandi(r, oggi)

    STATO.mkdir(parents=True, exist_ok=True)
    out = STATO / f"{oggi.isoformat()}.jsonl"
    conteggi: dict[str, int] = defaultdict(int)
    sess = requests.Session()
    ultima_per_autorita: dict[str, float] = {}

    print(f"{len(risorse)} risorse da sondare\n")
    with out.open("a", encoding="utf-8") as f:
        for r in risorse:
            attesa = PAUSA_S - (time.monotonic() - ultima_per_autorita.get(r["autorita"], 0))
            if attesa > 0:
                time.sleep(attesa)
            rec = sonda(sess, r)
            ultima_per_autorita[r["autorita"]] = time.monotonic()
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
            conteggi[rec["esito"]] += 1
            mb = f"{rec.get('dimensione')/1e6:8.1f} MB" if rec.get("dimensione") else "         —"
            per = f" {rec['periodo']}" if rec.get("periodo") else ""
            print(f"{rec['esito']:14s} {rec.get('http') or '---':>4} {mb}  "
                  f"{rec['autorita']}/{rec['dataset']}{per}", flush=True)

    print("\nriepilogo:", dict(sorted(conteggi.items(), key=lambda x: -x[1])))
    print(f"scritto {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
