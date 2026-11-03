#!/usr/bin/env python3
"""Censimento dell'accessibilità di «Amministrazione trasparente» (art. 9 c.1 d.lgs. 33/2013), #61.

Un comando, idempotente e ripartibile (stato in lavoro/trasparenza/stato.sqlite):

    censimento.py tutto   [--run AAAA-MM] [--campione N] [--paralleli 24]
    censimento.py fonti                  # registro ANAC L.190 + IndicePA -> tabella enti
    censimento.py sonda   [--run ...] [--campione N] [--paralleli 24]
    censimento.py browser [--run ...]    # seconda prova con Chromium headless sui bloccati
    censimento.py esporta [--run ...] [--forza]  # open data: sito/static/dati/trasparenza/giri/AAAA-MM-GG/
    censimento.py indici                 # indice.json, storico.json, ultimo/, invii.json
    censimento.py pec-prepara --giro AAAA-MM-GG   # testi + allegati, NESSUN INVIO
    censimento.py pec-registra --cf CF --giro G --destinatario ente|anac --evento invio|...

Il «run» identifica la rilevazione (default: mese corrente); rilanciare lo stesso run riprende
da dove si era fermato. Un ente è un'unità di lavoro; gli enti sono raggruppati per host e ogni
host è servito da un solo filo, con almeno 5 s fra due richieste.
"""
from __future__ import annotations

import argparse
import calendar
import json
import random
import sys
import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))

import requests  # noqa: E402

from comune import Ritmo, adesso, connetti, jdump  # noqa: E402


def campione_stratificato(righe: list[dict], n: int, seme: int = 20261103) -> list[dict]:
    """Giro a turno sugli strati (tipologia/categoria x regione), casuale con seme fisso."""
    rnd = random.Random(seme)
    strati = defaultdict(list)
    for r in righe:
        strati[(r["categoria"] or r["tipologia"], r["regione"])].append(r)
    for v in strati.values():
        rnd.shuffle(v)
    chiavi = sorted(strati, key=lambda k: -len(strati[k]))
    out = []
    while len(out) < n and any(strati.values()):
        for k in chiavi:
            if strati[k] and len(out) < n:
                out.append(strati[k].pop())
    return out


def host_di(r: dict) -> str:
    for u in (r.get("at_url"), r.get("url_l190"), r.get("sito_ipa")):
        if u and "://" in u:
            return urlsplit(u.strip()).netloc.lower()
    return "?"


def cmd_sonda(a) -> int:
    import sonda
    c = connetti()
    c.row_factory = __import__("sqlite3").Row
    tutti = [dict(r) for r in c.execute("SELECT * FROM enti")]
    if a.campione:
        tutti = campione_stratificato(tutti, a.campione)
        Path(c.execute("PRAGMA database_list").fetchone()[2]).with_name(f"campione-{a.run}.json").write_text(
            jdump([r["cf"] for r in tutti]), encoding="utf-8")
    fatti = {r[0] for r in c.execute("SELECT cf FROM esiti WHERE run=?", (a.run,))}
    da_fare = [r for r in tutti if r["cf"] not in fatti]
    per_host = defaultdict(list)
    for r in da_fare:
        per_host[host_di(r)].append(r)
    gruppi = sorted(per_host.values(), key=len, reverse=True)  # gli host grossi partono per primi
    print(f"{adesso()} run={a.run} enti={len(tutti)} già fatti={len(fatti)} da fare={len(da_fare)} host={len(gruppi)}", flush=True)
    ritmo, lk, cont = Ritmo(), threading.Lock(), [0]
    t0 = time.monotonic()

    def lavora(gruppo):
        sess = requests.Session()
        sess.max_redirects = 10
        for e in gruppo:
            try:
                d = sonda.prova_ente(sess, ritmo, e)
            except Exception as ex:  # noqa: BLE001
                d = {"esito": "errore dello strumento", "dettaglio_esito": f"{type(ex).__name__}: {ex}"[:300]}
            with lk:
                c.execute("INSERT OR REPLACE INTO esiti VALUES(?,?,?,?,?)", (a.run, e["cf"], adesso(), d["esito"], jdump(d)))
                c.commit()
                cont[0] += 1
                if cont[0] % 50 == 0:
                    v = cont[0] / (time.monotonic() - t0)
                    print(f"{adesso()} {cont[0]}/{len(da_fare)} ({v*3600:.0f}/h, mancano ~{(len(da_fare)-cont[0])/v/3600:.1f} h)", flush=True)

    with ThreadPoolExecutor(a.paralleli) as ex:
        list(ex.map(lavora, gruppi))
    print(f"{adesso()} fine run={a.run} sondati={cont[0]}", flush=True)
    return 0


def cmd_browser(a) -> int:
    """Seconda prova con un browser reale (Chromium headless di Playwright) sugli enti bloccati
    o irraggiungibili: distingue «blocca i bot» da «sito rotto». Nessun CAPTCHA risolto."""
    from playwright.sync_api import sync_playwright
    import sonda
    from comune import UA_BROWSER, salva_blob
    c = connetti()
    righe = c.execute("SELECT cf, dettaglio FROM esiti WHERE run=? AND esito IN ('bloccato da WAF/anti-bot','irraggiungibile')", (a.run,)).fetchall()
    with sync_playwright() as p:
        br = p.chromium.launch(headless=True)
        ctx = br.new_context(user_agent=UA_BROWSER, locale="it-IT")
        for cf, det in righe:
            d = json.loads(det)
            if "browser" in d or not d.get("at_url"):
                continue
            pg = ctx.new_page()
            r = {"ts": adesso()}
            try:
                resp = pg.goto(d["at_url"], timeout=45000, wait_until="domcontentloaded")
                pg.wait_for_timeout(8000)  # lascia completare una JS-challenge non interattiva
                html = pg.content()
                r |= {"status": resp.status if resp else None, "finale": pg.url, "titolo": pg.title()[:160],
                      "firme": sonda.firme(resp.status if resp else 0, {}, html), "sha256": salva_blob(html.encode())}
            except Exception as ex:  # noqa: BLE001
                r["errore"] = f"{type(ex).__name__}: {str(ex)[:200]}"
            pg.close()
            d["browser"] = r
            ok = r.get("status") and r["status"] < 400 and not r.get("firme")
            if d["esito"] == "irraggiungibile" and ok:
                d["esito"], d["dettaglio_esito"] = "bloccato da WAF/anti-bot", "accessibile solo con browser reale (JS)"
            elif d["esito"] == "bloccato da WAF/anti-bot" and d.get("da_confermare_con_browser") and (r.get("status") or 0) >= 500:
                d["esito"], d["dettaglio_esito"] = "irraggiungibile", f"errore del server anche con browser reale (HTTP {r['status']})"
                d["conferma_browser"] = "sito guasto, non blocco"
            elif d["esito"] == "bloccato da WAF/anti-bot":
                if r.get("firme"):
                    d["firme_browser"] = sorted(set(d.get("firme_browser", []) + r["firme"]))
                d["conferma_browser"] = "browser respinto: blocco o sito rotto" if not ok else "browser accettato: blocco selettivo dei client non-browser"
            c.execute("UPDATE esiti SET esito=?, dettaglio=? WHERE run=? AND cf=?", (d["esito"], jdump(d), a.run, cf))
            c.commit()
            time.sleep(5)
        br.close()
    return 0




DUBBI = ("bloccato da WAF/anti-bot", "bloccato da robots.txt", "noindex", "irraggiungibile", "tls invalido", "sezione non individuata")


def _enti_dubbi(c, run: str, campione: int = 0) -> list[dict]:
    c.row_factory = __import__("sqlite3").Row
    q = f"SELECT e.*, x.dettaglio, x.esito FROM esiti x JOIN enti e USING(cf) WHERE x.run=? AND x.esito IN ({','.join('?' * len(DUBBI))})"
    out = []
    for r in c.execute(q, (run, *DUBBI)):
        e = dict(r)
        d = json.loads(e.pop("dettaglio"))
        e["at_url_anac"] = e.get("at_url") or ""
        e["at_url"] = d.get("at_url") or e.get("at_url") or ""
        out.append(e)
    c.row_factory = None
    return campione_stratificato(out, campione) if campione else out


def salva_tentativi(c, run: str, righe: list[dict]):
    for t in righe:
        c.execute("INSERT OR REPLACE INTO tentativi VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                  (run, t["cf"], t["origine"], t["ip"], t["asn"], t["ts"], t["tipo"], t.get("client", ""),
                   t.get("status"), t.get("grezzo_sha256", ""), jdump(t)))
    c.commit()


def cmd_diagnosi(a) -> int:
    """Diagnostica estesa sui dubbi del run, da questa origine, giro di conferma N (--giro-conferma).
    Un blocco si conferma solo con più giri a distanza di almeno --distanza minuti. --elenco per il desktop.
    Enti raggruppati per host: un filo per host, --paralleli host alla volta, ogni filo con il suo browser."""
    import diagnosi
    c = connetti()
    enti = json.loads(Path(a.elenco).read_text(encoding="utf-8")) if a.elenco else _enti_dubbi(c, a.run, a.campione)
    n = a.giro_conferma
    stato = {}
    for cf, g, ts in c.execute("SELECT cf, json_extract(dati,'$.giro_conferma'), max(ts) FROM tentativi "
                               "WHERE run=? AND origine=? GROUP BY cf, json_extract(dati,'$.giro_conferma')", (a.run, a.origine)):
        stato.setdefault(cf, {})[g or 1] = ts
    da_fare, attesa = [], 0
    for e in enti:
        s = stato.get(e["cf"], {})
        if n in s:
            continue
        if n > 1:
            prec = s.get(n - 1)
            if not prec:
                continue
            if time.time() - calendar.timegm(time.strptime(prec, "%Y-%m-%dT%H:%M:%SZ")) < a.distanza * 60:
                attesa += 1
                continue
        da_fare.append(e)
    print(f"{adesso()} diagnosi run={a.run} origine={a.origine} giro={n} enti={len(da_fare)} (in attesa della distanza: {attesa})", flush=True)
    pac = Path(a.pacchetto) if a.pacchetto else None
    per_host = defaultdict(list)
    for e in da_fare:
        per_host[host_di(e)].append(e)
    lk, cont = threading.Lock(), [0]

    def lavora(gruppo):
        pw_ctx = None
        if not a.senza_browser:
            from playwright.sync_api import sync_playwright
            pw_ctx = sync_playwright().start()
        try:
            for e in gruppo:
                try:
                    righe = diagnosi.diagnostica(e, a.origine, browser=pw_ctx is not None, headed=a.headed,
                                                 canale=a.canale, pw=pw_ctx, giro=n)
                except Exception as ex:  # noqa: BLE001
                    print(f"{adesso()} errore {e['cf']}: {type(ex).__name__}: {ex}", flush=True)
                    continue
                for t in righe:
                    t["run"] = a.run
                with lk:
                    salva_tentativi(c, a.run, righe)
                    if pac:
                        diagnosi.esporta_pacchetto(righe, pac)
                    cont[0] += 1
                    if cont[0] % 25 == 0:
                        print(f"{adesso()} {cont[0]}/{len(da_fare)}", flush=True)
        finally:
            if pw_ctx:
                pw_ctx.stop()

    with ThreadPoolExecutor(a.paralleli) as ex:
        list(ex.map(lavora, sorted(per_host.values(), key=len, reverse=True)))
    print(f"{adesso()} fine diagnosi giro={n} fatti={cont[0]}", flush=True)
    return 0


def cmd_elenco(a) -> int:
    c = connetti()
    enti = _enti_dubbi(c, a.run, a.campione)
    campi = ("cf", "denominazione", "at_url", "at_url_anac", "sito_ipa", "url_l190", "esito")
    Path(a.elenco).write_text(json.dumps([{k: e.get(k) for k in campi} for e in enti], ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"{len(enti)} enti in {a.elenco}")
    return 0


def cmd_importa(a) -> int:
    """Importa un pacchetto (tentativi.jsonl + blobs/) prodotto da un'altra origine."""
    from comune import salva_blob
    c = connetti()
    pac = Path(a.pacchetto)
    righe = [json.loads(x) for x in (pac / "tentativi.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    for b in (pac / "blobs").glob("*"):
        assert salva_blob(b.read_bytes()) == b.name, f"sha256 non corrisponde: {b.name}"
    for t in righe:
        salva_tentativi(c, t.get("run") or a.run, [t])
    print(json.dumps({"importati": len(righe), "origini": sorted({t['origine'] for t in righe})}))
    return 0


def cmd_caratterizza(a) -> int:
    """Due vie (ANAC e home IndicePA) e ricercabilità con un CIG reale dell'ente."""
    import diagnosi
    from playwright.sync_api import sync_playwright
    c = connetti()
    c.row_factory = __import__("sqlite3").Row
    righe = [dict(r) for r in c.execute(
        "SELECT e.*, x.dettaglio, t.cig FROM esiti x JOIN enti e USING(cf) LEFT JOIN cig_test t USING(cf) "
        "WHERE x.run=? AND x.esito NOT IN ('url non valido','irraggiungibile','tls invalido')", (a.run,))]
    c.row_factory = None
    if a.campione:
        righe = campione_stratificato(righe, a.campione)
    fatti = {r[0] for r in c.execute("SELECT cf FROM caratteri WHERE run=?", (a.run,))}
    righe = [r for r in righe if r["cf"] not in fatti]
    print(f"{adesso()} caratterizza run={a.run} enti={len(righe)}", flush=True)
    with sync_playwright() as pw:
        for i, e in enumerate(righe, 1):
            d = json.loads(e.pop("dettaglio"))
            e["at_url_anac"] = e.get("at_url") or (d.get("at_url") if d.get("at_provenienza", "").startswith("anac") else "")
            k = diagnosi.caratterizza(pw, e, e.get("cig") or "", headed=a.headed)
            c.execute("INSERT OR REPLACE INTO caratteri VALUES(?,?,?,?,?,?)",
                      (a.run, e["cf"], k["ts"], k.get("ricercabilita"), int(bool(k.get("coincidono"))), jdump(k)))
            c.commit()
            if i % 10 == 0:
                print(f"{adesso()} {i}/{len(righe)}", flush=True)
            time.sleep(5)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("comando", choices=["tutto", "fonti", "sonda", "browser", "esporta", "indici", "pec-prepara", "pec-registra",
                                        "indice-cig", "diagnosi", "elenco", "importa", "caratterizza"])
    ap.add_argument("--run", default=date.today().strftime("%Y-%m"))
    ap.add_argument("--campione", type=int, default=0)
    ap.add_argument("--paralleli", type=int, default=24)
    ap.add_argument("--data", default="", help="cartella esiti (AAAA-MM-GG); default: data del primo esito del run")
    ap.add_argument("--forza", action="store_true")
    ap.add_argument("--giro", default="")
    ap.add_argument("--cf", action="append", default=[])
    ap.add_argument("--destinatario", choices=["ente", "anac"])
    ap.add_argument("--evento")
    ap.add_argument("--indirizzo", default="")
    ap.add_argument("--id-messaggio", default="")
    ap.add_argument("--file", default="")
    ap.add_argument("--nota", default="")
    ap.add_argument("--origine", default="server", choices=["server", "desktop"])
    ap.add_argument("--elenco", default="")
    ap.add_argument("--pacchetto", default="")
    ap.add_argument("--headed", action="store_true", help="browser con finestra (sul server: xvfb-run)")
    ap.add_argument("--canale", default=None, help="es. chrome: usa il Chrome installato")
    ap.add_argument("--senza-browser", action="store_true")
    ap.add_argument("--giro-conferma", type=int, default=1)
    ap.add_argument("--distanza", type=int, default=60, help="minuti minimi fra due giri di conferma")
    a = ap.parse_args()
    if a.comando in ("fonti", "tutto"):
        import fonti
        fonti.costruisci()
    if a.comando in ("sonda", "tutto"):
        cmd_sonda(a)
    if a.comando == "browser":
        cmd_browser(a)
    if a.comando in ("esporta", "tutto"):
        import esporta
        esporta.esporta(a.run, a.data, a.forza)
    if a.comando == "indici":
        import esporta
        esporta.aggiorna_indici()
    if a.comando == "pec-prepara":
        import pec
        pec.prepara(connetti(), a.run, a.giro or a.data, a.cf or None)
    if a.comando == "pec-registra":
        import pec
        print(jdump(pec.registra(a.cf[0], a.giro, a.destinatario, a.evento, a.indirizzo, a.id_messaggio, a.file, a.nota, a.data)))
    if a.comando == "indice-cig":
        import fonti
        fonti.indice_cig()
    for nome, f in (("diagnosi", cmd_diagnosi), ("elenco", cmd_elenco), ("importa", cmd_importa), ("caratterizza", cmd_caratterizza)):
        if a.comando == nome:
            f(a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
