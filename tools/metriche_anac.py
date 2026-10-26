#!/usr/bin/env python3
"""Metriche di non ricorrenza per i problemi ANAC.

Ogni problema della sezione 5 del rapporto ANAC (I1-I9) ha un controllo
automatico: se il controllo passa, il problema non c'è; se fallisce, c'è, con la
prova. Rilanciato ogni giorno, dice se un problema è stato risolto e se torna.

Esito in stato/metriche/<data>.json, mai sovrascritto nel tempo: è lo storico che
alimenta la scheda dell'ente e la dashboard.

    metriche_anac.py [--oggi AAAA-MM-GG]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import date, datetime, timezone
from pathlib import Path

import time

import requests

BASE = Path(__file__).resolve().parent.parent
STATO = Path(os.environ.get("STATO_ROOT", BASE / "stato")) / "metriche"
ARCHIVIO = Path(os.environ.get("ARCHIVIO_ROOT", BASE / "archivio"))

PORTALE = "https://dati.anticorruzione.it/opendata"
DL = f"{PORTALE}/download/dataset"
API = f"{PORTALE}/api/3/action"
UA_BROWSER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/140.0 Safari/537.36 analisi-spesa-ict (+https://github.com/mxmap-it/analisi-spesa-ict)")
H = {"User-Agent": UA_BROWSER, "Accept": "*/*"}

s = requests.Session()
ERRORI: dict[str, str] = {}


def head(url: str) -> requests.Response | None:
    """Stato e intestazioni con un GET in streaming: alcuni host non gestiscono bene HEAD."""
    time.sleep(0.5)  # cortesia: il mirror sta già interrogando lo stesso server
    try:
        r = s.get(url, headers=H, timeout=60, allow_redirects=True, stream=True)
        r.close()
        return r
    except requests.RequestException as e:
        ERRORI[url] = type(e).__name__
        return None


def ckan(azione: str, **p) -> dict | None:
    try:
        r = s.get(f"{API}/{azione}", params=p, headers=H, timeout=90)
        return r.json()["result"] if r.status_code == 200 else None
    except (requests.RequestException, ValueError, KeyError):
        return None


def mesi_fino_a(oggi: date, da: tuple[int, int]):
    y, m = da
    while (y, m) < (oggi.year, oggi.month):
        yield y, m
        m += 1
        if m == 13:
            y, m = y + 1, 1


def esito(id_: str, ok: bool, controllo: str, prova: dict) -> dict:
    return {"id": id_, "esito": "rispettato" if ok else "violato", "controllo": controllo, "prova": prova}


# ---------------------------------------------------------------------------
def i1_ocds_mensile(oggi: date) -> dict:
    """Dopo il giorno 2 deve esistere il file OCDS del mese precedente."""
    y, m = (oggi.year, oggi.month - 1) if oggi.month > 1 else (oggi.year - 1, 12)
    url = f"{DL}/ocds/filesystem/bulk/{y}/{m:02d}.json"
    r = head(url)
    mancanti = [f"{a}/{b:02d}" for a, b in mesi_fino_a(oggi, (oggi.year, 1))
                if (h := head(f"{DL}/ocds/filesystem/bulk/{a}/{b:02d}.json")) is None or h.status_code != 200]
    ok = oggi.day <= 2 or (r is not None and r.status_code == 200)
    return esito("I1", ok, "file OCDS del mese precedente pubblicato dopo il giorno 2",
                 {"url": url, "http": r.status_code if r is not None else None, "mesi_mancanti_anno_corrente": mancanti})


def i2_api_rest() -> dict:
    """Gli endpoint documentati rispondono e lo swagger è JSON valido."""
    stati = {}
    for ep in ("version", "releases", "awards"):
        u = f"https://api.anticorruzione.it/opendata/ocds/api/v1/1.0.0/{ep}"
        r = head(u)
        stati[ep] = r.status_code if r is not None else f"errore: {ERRORI.get(u)}"
    try:
        sw = s.get(f"{PORTALE}/ocds/api/spec/swagger.json", headers=H, timeout=60)
        json.loads(sw.text)
        swagger_ok = True
    except (requests.RequestException, ValueError):
        swagger_ok = False
    ok = swagger_ok and all(isinstance(v, int) and v < 400 for v in stati.values())
    return esito("I2", ok, "endpoint dell'API REST OCDS raggiungibili e swagger valido",
                 {"endpoint": stati, "swagger_json_valido": swagger_ok})


def i3_licenza(oggi: date) -> dict:
    """La licenza del catalogo coincide con quella dichiarata nel file."""
    pkg = ckan("package_show", id=f"ocds-appalti-ordinari-{oggi.year}") or \
        ckan("package_show", id=f"ocds-appalti-ordinari-{oggi.year - 1}")
    lic_cat = (pkg or {}).get("license_title")
    lic_file = None
    for y, m in sorted(mesi_fino_a(oggi, (oggi.year - 1, 1)), reverse=True):
        try:
            r = s.get(f"{DL}/ocds/filesystem/bulk/{y}/{m:02d}.json",
                      headers={**H, "Range": "bytes=0-2047"}, timeout=60)
            if r.status_code in (200, 206):
                t = r.text
                i = t.find('"license"')
                if i >= 0:
                    lic_file = t[i:t.find("\n", i)].split('"')[3]
                    break
        except requests.RequestException:
            continue
    by_sa_cat = lic_cat and "share" in lic_cat.lower()
    by_sa_file = lic_file and "by-sa" in lic_file.lower()
    ok = lic_cat is not None and lic_file is not None and bool(by_sa_cat) == bool(by_sa_file)
    return esito("I3", ok, "licenza del catalogo uguale a quella nel file OCDS",
                 {"catalogo": lic_cat, "file": lic_file})


def i4_mesi_duplicati(oggi: date) -> dict:
    """Mesi OCDS diversi non devono servire lo stesso contenuto."""
    firme: dict[str, list[str]] = {}
    for y, m in mesi_fino_a(oggi, (oggi.year - 2, 1)):
        url = f"{DL}/ocds/filesystem/bulk/{y}/{m:02d}.json"
        r = head(url)
        if r is None or r.status_code != 200 or "Content-Length" not in r.headers:
            continue
        n = int(r.headers["Content-Length"])
        # firma: dimensione + un blocco a metà file, che salta l'intestazione con l'uri
        try:
            b = s.get(url, headers={**H, "Range": f"bytes={n // 2}-{n // 2 + 65535}"}, timeout=90).content
        except requests.RequestException:
            continue
        firma = f"{n}:{hashlib.sha256(b).hexdigest()[:16]}"
        firme.setdefault(firma, []).append(f"{y}/{m:02d}")
    gruppi = [v for v in firme.values() if len(v) > 1]
    return esito("I4", not gruppi, "nessun mese OCDS con contenuto identico a un altro",
                 {"mesi_esaminati": sum(len(v) for v in firme.values()),
                  "contenuti_distinti": len(firme), "gruppi_duplicati": gruppi})


def i5_continuita(oggi: date) -> dict:
    """Le serie mensili dei delta non hanno buchi dentro la finestra pubblicata."""
    buchi = {}
    for ds in ("cig", "smartcig", "aggiudicazioni", "aggiudicatari"):
        pkg = ckan("package_show", id=ds)
        if not pkg:
            buchi[ds] = "catalogo non leggibile"
            continue
        mesi = sorted({r["name"][:6] for r in pkg["resources"]
                       if r.get("name", "")[:8].isdigit() and r.get("format", "").upper() == "CSV"})
        if not mesi:
            continue
        attesi = [f"{y}{m:02d}" for y, m in mesi_fino_a(date(int(mesi[-1][:4]), int(mesi[-1][4:]), 28),
                                                         (int(mesi[0][:4]), int(mesi[0][4:])))] + [mesi[-1]]
        mancanti = [x for x in attesi if x not in mesi]
        if mancanti:
            buchi[ds] = mancanti
    return esito("I5", not buchi, "nessun mese mancante nelle serie di delta", {"buchi": buchi})


def i6_sparizioni() -> dict:
    """Ciò che abbiamo archiviato è ancora pubblicato."""
    man = ARCHIVIO / "manifest.jsonl"
    if not man.exists():
        return esito("I6", True, "risorse archiviate ancora pubblicate", {"nota": "manifest assente"})
    urls = set()
    for riga in man.read_text(encoding="utf-8").splitlines():
        r = json.loads(riga)
        if r.get("esito") in ("nuovo", "invariato") and "/filesystem/20" in r["url"]:
            urls.add(r["url"])
    sparite = [u for u in sorted(urls) if (h := head(u)) is not None and h.status_code == 404]
    return esito("I6", not sparite, "nessuna risorsa delta archiviata sparita dalla fonte",
                 {"controllate": len(urls), "sparite": [u.split("/dataset/")[1] for u in sparite]})


def i7_dimensioni() -> dict:
    """Il size del catalogo corrisponde al Content-Length servito (campione)."""
    pkg = ckan("package_show", id="cig") or {}
    scarti = []
    for r in pkg.get("resources", [])[:6]:
        dich = int(r["size"]) if str(r.get("size") or "").isdigit() else None
        h = head(r.get("url", ""))
        reale = int(h.headers["Content-Length"]) if h is not None and "Content-Length" in h.headers else None
        if dich and reale:
            scarti.append({"risorsa": r.get("name"), "dichiarato": dich, "servito": reale,
                           "rapporto": round(dich / reale, 2)})
    ok = bool(scarti) and all(abs(x["rapporto"] - 1) < 0.05 for x in scarti)
    return esito("I7", ok, "dimensione dichiarata entro il 5% di quella servita", {"campione": scarti})


def i8_elencate_inesistenti() -> dict:
    """Ogni risorsa elencata nel catalogo esiste: delta, annuali smartcig e OCDS."""
    rotte = []
    oggi = date.today()
    elenco = ["cig", "smartcig", "aggiudicazioni", "aggiudicatari", f"smartcig-{oggi.year - 1}"] + [f"ocds-appalti-ordinari-{y}" for y in (oggi.year - 1, oggi.year)]
    for ds in elenco:
        for r in (ckan("package_show", id=ds) or {}).get("resources", []):
            h = head(r.get("url", ""))
            if h is not None and h.status_code == 404:
                rotte.append(f"{ds}/{r.get('name')}")
    return esito("I8", not rotte, "nessuna risorsa elencata che risponda 404", {"rotte": rotte})


def i9_user_agent() -> dict:
    """Con un user-agent non da browser il server serve il file o un errore esplicito."""
    url = f"{DL}/stazioni-appaltanti/filesystem/stazioni-appaltanti_csv.zip"
    esiti = {}
    for ua in ("python-requests/2.32", "curl/8.5"):
        try:
            r = s.head(url, headers={"User-Agent": ua}, timeout=60, allow_redirects=True)
            esiti[ua] = {"http": r.status_code, "tipo": r.headers.get("Content-Type")}
        except requests.RequestException:
            esiti[ua] = {"http": None, "tipo": None}
    falsi_ok = [ua for ua, e in esiti.items() if e["http"] == 200 and "html" in (e["tipo"] or "")]
    return esito("I9", not falsi_ok, "nessuna pagina HTML servita come 200 al posto del file", esiti)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--oggi", default=date.today().isoformat())
    a = ap.parse_args()
    oggi = date.fromisoformat(a.oggi)
    risultati = []
    for f in (lambda: i1_ocds_mensile(oggi), i2_api_rest, lambda: i3_licenza(oggi),
              lambda: i4_mesi_duplicati(oggi), lambda: i5_continuita(oggi), i6_sparizioni,
              i7_dimensioni, i8_elencate_inesistenti, i9_user_agent):
        try:
            r = f()
        except Exception as e:  # una metrica rotta non deve fermare le altre
            r = {"id": "?", "esito": "errore", "controllo": str(f), "prova": {"errore": repr(e)}}
        risultati.append(r)
        print(f"{r['id']:3s} {r['esito']:10s} {r['controllo']}", flush=True)
    STATO.mkdir(parents=True, exist_ok=True)
    out = STATO / f"{oggi.isoformat()}.json"
    out.write_text(json.dumps({"ente": "ANAC", "istante": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                               "metriche": risultati}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nscritto {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
