#!/usr/bin/env python3
"""Servizio di annotazione per volontari: stato condiviso fra più persone (SQLite), solo libreria standard.

La pagina (tools/annotazioni/pagina.html) è pubblicata su analisi-spesa-ict.mxmap.it/annotazioni/ (GitHub Pages, copia in sito/static) e chiama questo
servizio; il servizio la serve anche direttamente su "/". Ogni contratto del campione riceve fino a
ANNOTAZIONI_PER_CIG annotazioni indipendenti (alla cieca: chi annota non vede le altre né le proposte).

    .venv/bin/python tools/annotazioni/server.py --porta 8790
Endpoint: GET /api/prossimo?nome=..  POST /api/annota  GET /api/stato  GET /api/esporta?chiave=..
Dati: stato/annotazioni.sqlite (append-only: ogni annotazione è una riga, le correzioni sono righe nuove).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import random
import re
import sqlite3
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

R = Path(__file__).resolve().parents[2]
DB = R / "stato/annotazioni.sqlite"
CAMPIONE = R / "report/metodo/campione-misura-v3-cieco.csv"
PAGINA = Path(__file__).with_name("pagina.html")
ANNOTAZIONI_PER_CIG = 2
ORIGINI = {"https://analisi-spesa-ict.mxmap.it", "http://localhost:1313", "http://localhost:8790"}
CHIAVE_EXPORT = os.environ.get("ANNOTAZIONI_CHIAVE", "")
SERVIZI = {"cloud", "licenza", "servizi-professionali", "psn", "in-house", "telefonia", "connettivita", "hardware", "altro", "non-so"}
GIUR = {"IT", "UE", "EXTRA-UE", "ignota"}
lock = threading.Lock()
limiti: dict[str, list[float]] = {}


def db():
    c = sqlite3.connect(DB, timeout=30)
    c.execute("""CREATE TABLE IF NOT EXISTS annotazioni (id INTEGER PRIMARY KEY, cig TEXT, annotatore TEXT, e_cloud TEXT,
                 servizio TEXT, provider TEXT, giurisdizione TEXT, confidenza TEXT, note TEXT, secondi INTEGER,
                 quando TEXT, ip_hash TEXT)""")
    return c


def campione():
    with CAMPIONE.open(encoding="utf-8") as f:
        return {r["cig"]: {"cig": r["cig"], "cpv": r["cod_cpv"], "importo": r["importo_lotto"], "ente": r["stazione_appaltante"],
                           "aggiudicatari": r["aggiudicatari"], "oggetto": r["testo"]} for r in csv.DictReader(f)}


CAMP = campione()


def pulisci(s, n=200):
    return re.sub(r"[\x00-\x1f]", " ", str(s or ""))[:n].strip()


class H(BaseHTTPRequestHandler):
    server_version = "annotazioni"

    def _cors(self):
        o = self.headers.get("Origin", "")
        if o in ORIGINI:
            self.send_header("Access-Control-Allow-Origin", o)
            self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, obj, code=200):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code); self._cors()
        self.send_header("Content-Type", "application/json; charset=utf-8"); self.send_header("Content-Length", str(len(b)))
        self.end_headers(); self.wfile.write(b)

    def _ip(self):
        return self.headers.get("X-Forwarded-For", self.client_address[0]).split(",")[0].strip()

    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()

    def do_GET(self):
        u = urlsplit(self.path); q = {k: v[0] for k, v in parse_qs(u.query).items()}
        if u.path in ("/", "/annotazioni", "/annotazioni/"):
            b = PAGINA.read_bytes()
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b); return
        if u.path == "/api/prossimo":
            nome = pulisci(q.get("nome"), 60)
            if not nome:
                return self._json({"errore": "nome mancante"}, 400)
            with lock, db() as c:
                cont = dict(c.execute("SELECT cig, COUNT(DISTINCT annotatore) FROM annotazioni GROUP BY cig").fetchall())
                fatti = {r[0] for r in c.execute("SELECT cig FROM annotazioni WHERE annotatore=?", (nome,))}
            liberi = [g for g in CAMP if g not in fatti and cont.get(g, 0) < ANNOTAZIONI_PER_CIG]
            if not liberi:
                return self._json({"finito": True, "fatti": len(fatti)})
            minimo = min(cont.get(g, 0) for g in liberi)
            # prima i contratti con meno annotazioni, poi a caso (seme per nome: ordine stabile per la stessa persona)
            scelta = random.Random(nome + str(len(fatti))).choice([g for g in liberi if cont.get(g, 0) == minimo])
            return self._json({"contratto": CAMP[scelta], "fatti": len(fatti), "restanti": len(liberi)})
        if u.path == "/api/stato":
            with db() as c:
                n = c.execute("SELECT COUNT(*), COUNT(DISTINCT cig), COUNT(DISTINCT annotatore) FROM annotazioni").fetchone()
                completi = c.execute("SELECT COUNT(*) FROM (SELECT cig FROM annotazioni GROUP BY cig HAVING COUNT(DISTINCT annotatore)>=?)",
                                     (ANNOTAZIONI_PER_CIG,)).fetchone()[0]
                classifica = c.execute("SELECT annotatore, COUNT(*) FROM annotazioni GROUP BY annotatore ORDER BY 2 DESC LIMIT 20").fetchall()
            return self._json({"annotazioni": n[0], "contratti_toccati": n[1], "volontari": n[2], "contratti_completi": completi,
                               "totale_contratti": len(CAMP), "per_contratto": ANNOTAZIONI_PER_CIG, "classifica": classifica})
        if u.path == "/api/esporta":
            if not CHIAVE_EXPORT or q.get("chiave") != CHIAVE_EXPORT:
                return self._json({"errore": "non autorizzato"}, 403)
            with db() as c:
                righe = c.execute("SELECT * FROM annotazioni ORDER BY id").fetchall()
                nomi = [d[0] for d in c.execute("SELECT * FROM annotazioni LIMIT 0").description]
            s = io.StringIO(); w = csv.writer(s); w.writerow(nomi); w.writerows(righe)
            b = s.getvalue().encode()
            self.send_response(200); self.send_header("Content-Type", "text/csv; charset=utf-8"); self.end_headers(); self.wfile.write(b); return
        self._json({"errore": "non trovato"}, 404)

    def do_POST(self):
        if urlsplit(self.path).path != "/api/annota":
            return self._json({"errore": "non trovato"}, 404)
        ip = self._ip(); ora = time.time()
        with lock:
            t = [x for x in limiti.get(ip, []) if ora - x < 60]
            if len(t) >= 30:
                return self._json({"errore": "troppe richieste, riprova fra un minuto"}, 429)
            limiti[ip] = t + [ora]
        try:
            d = json.loads(self.rfile.read(min(int(self.headers.get("Content-Length", 0)), 20000)))
        except (ValueError, json.JSONDecodeError):
            return self._json({"errore": "richiesta non valida"}, 400)
        rec = {"cig": pulisci(d.get("cig"), 10), "annotatore": pulisci(d.get("nome"), 60), "e_cloud": pulisci(d.get("e_cloud"), 8),
               "servizio": pulisci(d.get("servizio"), 30), "provider": pulisci(d.get("provider"), 120),
               "giurisdizione": pulisci(d.get("giurisdizione"), 10), "confidenza": pulisci(d.get("confidenza"), 6),
               "note": pulisci(d.get("note"), 1000)}
        if rec["cig"] not in CAMP or not rec["annotatore"] or rec["e_cloud"] not in ("s", "n", "non-so") \
                or rec["servizio"] not in SERVIZI or rec["giurisdizione"] not in GIUR or rec["confidenza"] not in ("alta", "media", "bassa"):
            return self._json({"errore": "campi mancanti o non validi"}, 400)
        try:
            sec = max(0, min(int(d.get("secondi") or 0), 36000))
        except (TypeError, ValueError):
            sec = 0
        with lock, db() as c:
            c.execute("INSERT INTO annotazioni (cig, annotatore, e_cloud, servizio, provider, giurisdizione, confidenza, note, secondi, quando, ip_hash)"
                      " VALUES (?,?,?,?,?,?,?,?,?,datetime('now'),?)",
                      (*rec.values(), sec, hashlib.sha256(("annotazioni" + ip).encode()).hexdigest()[:16]))
        return self._json({"ok": True})

    def log_message(self, fmt, *a):
        pass


if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("--porta", type=int, default=8790); a.add_argument("--host", default="127.0.0.1")
    x = a.parse_args()
    DB.parent.mkdir(parents=True, exist_ok=True); db().close()
    print(f"annotazioni su http://{x.host}:{x.porta}  ({len(CAMP)} contratti)", flush=True)
    ThreadingHTTPServer((x.host, x.porta), H).serve_forever()
