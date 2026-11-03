"""Parti comuni del censimento «Amministrazione trasparente» (#61).

Percorsi, User-Agent dichiarati, archivio content-addressed, stato SQLite e
ritmo per host. Nessuna email negli User-Agent: c'è solo l'URL della pagina di
progetto, che ha i contatti.
"""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

RADICE = Path(os.environ.get("TRASPARENZA_RADICE", Path(__file__).resolve().parent.parent.parent))
ARCHIVIO = Path(os.environ.get("ARCHIVIO_ROOT", RADICE / "archivio"))
LAVORO = RADICE / "lavoro" / "trasparenza"
DB = Path(os.environ.get("TRASPARENZA_DB", LAVORO / "stato.sqlite"))

PAGINA_PROGETTO = "https://analisi-spesa-ict.mxmap.it/progetto/trasparenza-accessibilita/"
# Bot onesto: si dichiara come bot, con la pagina del progetto.
UA_BOT = f"analisi-spesa-ict-trasparenza/1.0 (+{PAGINA_PROGETTO})"
# Client da browser identificato (ammesso sulle sezioni obbligatorie, AGENTS.md §3).
# NON si usa mai uno User-Agent di Googlebot o Bingbot: non si impersonano i motori.
UA_BROWSER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
              f"Chrome/140.0 Safari/537.36 analisi-spesa-ict (+{PAGINA_PROGETTO})")
UA_ANAC = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
           "Chrome/140.0 Safari/537.36 analisi-spesa-ict (+https://github.com/mxmap-it/analisi-spesa-ict)")

INTERVALLO_HOST = float(os.environ.get("TRASPARENZA_INTERVALLO", "5"))


def adesso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def salva_blob(dati: bytes) -> str:
    """Scrive il contenuto nell'archivio (blobs/sha256/ab/cd/<hash>), mai sovrascritto."""
    sha = hashlib.sha256(dati).hexdigest()
    p = ARCHIVIO / "blobs" / "sha256" / sha[:2] / sha[2:4] / sha
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_name(f"{sha}.{os.getpid()}.{threading.get_ident()}.part")
        tmp.write_bytes(dati)
        os.replace(tmp, p)
    return sha


def connetti() -> sqlite3.Connection:
    DB.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB, timeout=60, check_same_thread=False)
    c.execute("PRAGMA journal_mode=WAL")
    c.executescript("""
    CREATE TABLE IF NOT EXISTS enti(
      cf TEXT PRIMARY KEY, ipa TEXT, denominazione TEXT, tipologia TEXT, categoria TEXT,
      regione TEXT, sito_ipa TEXT, pec_ipa TEXT, url_l190 TEXT, anno_l190 TEXT, esito_anac TEXT,
      at_url TEXT, at_provenienza TEXT, fonti TEXT);
    CREATE TABLE IF NOT EXISTS esiti(
      run TEXT, cf TEXT, ts TEXT, esito TEXT, dettaglio TEXT,
      PRIMARY KEY(run, cf));
    CREATE TABLE IF NOT EXISTS tentativi(
      run TEXT, cf TEXT, origine TEXT, ip TEXT, asn TEXT, ts TEXT, tipo TEXT, client TEXT,
      status INTEGER, grezzo_sha256 TEXT, dati TEXT,
      PRIMARY KEY(run, cf, origine, ts, tipo, client));
    CREATE TABLE IF NOT EXISTS caratteri(
      run TEXT, cf TEXT, ts TEXT, ricercabilita TEXT, coincidono INTEGER, dati TEXT,
      PRIMARY KEY(run, cf));
    CREATE TABLE IF NOT EXISTS cig_test(cf TEXT PRIMARY KEY, cig TEXT, data TEXT, oggetto TEXT, importo REAL);
    CREATE TABLE IF NOT EXISTS fonti_scaricate(
      url TEXT, ts TEXT, sha256 TEXT, byte INTEGER, nota TEXT);
    """)
    return c


class Ritmo:
    """Una richiesta alla volta per host e almeno INTERVALLO_HOST secondi fra due richieste."""

    def __init__(self, intervallo: float = INTERVALLO_HOST):
        self.intervallo = intervallo
        self._lock = threading.Lock()
        self._host: dict[str, tuple[threading.Lock, list[float]]] = {}

    def __call__(self, host: str):
        with self._lock:
            if host not in self._host:
                self._host[host] = (threading.Lock(), [0.0])
            lk, ultimo = self._host[host]
        return _Turno(lk, ultimo, self.intervallo)


class _Turno:
    def __init__(self, lk, ultimo, intervallo):
        self.lk, self.ultimo, self.intervallo = lk, ultimo, intervallo

    def __enter__(self):
        self.lk.acquire()
        attesa = self.ultimo[0] + self.intervallo - time.monotonic()
        if attesa > 0:
            time.sleep(attesa)

    def __exit__(self, *a):
        self.ultimo[0] = time.monotonic()
        self.lk.release()


def jdump(o) -> str:
    return json.dumps(o, ensure_ascii=False, separators=(",", ":"))

# Versione del metodo: si incrementa a ogni cambio di regole (registro in METODO.md).
VERSIONE_METODO = "1.1.0-beta"
DATI = Path(os.environ.get("TRASPARENZA_DATI", RADICE / "dati" / "trasparenza"))
