#!/usr/bin/env python3
"""Servizio di annotazione per volontari: stato condiviso fra più persone (SQLite), solo libreria standard.

La pagina (tools/annotazioni/pagina.html) è pubblicata su analisi-spesa-ict.mxmap.it/annotazioni/ (copia in sito/static); il servizio è esposto in HTTPS da Caddy su annotazioni.51-158-36-151.sslip.io (nessun DNS da gestire) e chiama questo
servizio; il servizio la serve anche direttamente su "/". Ogni contratto del campione riceve fino a
ANNOTAZIONI_PER_CIG annotazioni indipendenti (alla cieca: chi annota non vede le altre né le proposte).

    .venv/bin/python tools/annotazioni/server.py --porta 8790
Endpoint: GET /api/prossimo?nome=..  POST /api/annota  GET /api/stato  GET /api/esporta?chiave=..
Dati: stato/annotazioni.sqlite (append-only: ogni annotazione è una riga, le correzioni sono righe nuove).

Cruscotto dei contratti (#53, M13, decisione di Fabio del 19/11/2026): sola lettura sull'indice
lavoro/cruscotto/contratti.sqlite (tools/cruscotto/indice_contratti.py), pagina tools/cruscotto/pagina.html su "/contratti".
  GET /api/cerca?q=..&strato=..&anno_da=..&anno_a=..&giurisdizione=..&gruppo=..&livello=..&esito=..&ordina=..&pagina=..[&formato=csv]
  GET /api/contratto?cig=..     scheda: dati, esiti di ogni livello, atti archiviati, annotazioni (senza nomi)
  GET /api/totali?anno_da=..&anno_a=..   strato x giurisdizione e livello x esito, per il drilldown
  POST /api/annota con "modo": "cruscotto": annotazione libera di qualunque CIG dell'indice (a supporto e controllo).
Le annotazioni del campione alla cieca (modo «cieco», /api/prossimo) restano separate: il cruscotto mostra le nostre
classificazioni, quindi le sue annotazioni non contano come letture indipendenti.
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
DB = R / os.environ.get("ANNOTAZIONI_DB", "stato/annotazioni.sqlite")  # altro file solo per le prove
CAMPIONE = R / "report/metodo/campione-misura-v3-cieco.csv"
PAGINA = Path(__file__).with_name("pagina.html")
ANNOTAZIONI_PER_CIG = 2
ORIGINI = {"https://analisi-spesa-ict.mxmap.it", "http://localhost:1313", "http://localhost:8790"}
CHIAVE_EXPORT = os.environ.get("ANNOTAZIONI_CHIAVE", "")
SERVIZI = {"cloud", "licenza", "servizi-professionali", "psn", "in-house", "telefonia", "connettivita", "hardware", "altro", "non-so"}
DOCUMENTI = {"no", "determina", "piano-fabbisogni-psn", "contratto-ordine", "convenzione", "scheda-prodotto", "altro"}
GIUR = {"IT", "UE", "EXTRA-UE", "non-determinabile", "ignota"}
INDICE = R / "lavoro/cruscotto/contratti.sqlite"
PAGINA_CRUSCOTTO = R / "tools/cruscotto/pagina.html"
SI_NO = {"s", "n", "non-so"}
PER_PAGINA = 50
MAX_CSV = 10000
lock = threading.Lock()
cache_totali: dict = {}
limiti: dict[str, list[float]] = {}


def db():
    c = sqlite3.connect(DB, timeout=30)
    c.execute("""CREATE TABLE IF NOT EXISTS annotazioni (id INTEGER PRIMARY KEY, cig TEXT, annotatore TEXT, e_cloud TEXT,
                 servizio TEXT, provider TEXT, giurisdizione TEXT, confidenza TEXT, note TEXT, secondi INTEGER,
                 quando TEXT, ip_hash TEXT)""")
    if "documento" not in [r[1] for r in c.execute("PRAGMA table_info(annotazioni)")]:
        c.execute("ALTER TABLE annotazioni ADD COLUMN documento TEXT")
    col = [r[1] for r in c.execute("PRAGMA table_info(annotazioni)")]
    if "modo" not in col:  # 19/11/2026: «cieco» (campione, /api/prossimo) o «cruscotto» (annotazione libera, #53)
        c.execute("ALTER TABLE annotazioni ADD COLUMN modo TEXT")
    if "ict" not in col:
        c.execute("ALTER TABLE annotazioni ADD COLUMN ict TEXT")
    return c


CIECO = "coalesce(modo, 'cieco') = 'cieco'"


def indice():
    """connessione in sola lettura all'indice dei contratti (None se non ancora costruito)"""
    if not INDICE.exists():
        return None
    c = sqlite3.connect(f"file:{INDICE}?mode=ro", uri=True, timeout=30)
    c.row_factory = sqlite3.Row
    return c


def fts(q):
    """testo libero -> espressione FTS5 sicura: ogni parola tra virgolette, con prefisso, in AND"""
    parole = re.findall(r"[\w']+", q.lower())[:12]
    return " AND ".join('"' + p.replace('"', '') + '"*' for p in parole if p.strip("'"))


def filtri(q):
    """parametri della ricerca -> (where, argomenti); tutti facoltativi"""
    w, a = [], []
    if q.get("q"):
        t = q["q"].strip()
        if re.fullmatch(r"[0-9A-Za-z]{10}", t):
            w.append("(c.cig = ? OR c.rowid IN (SELECT rowid FROM contratti_fts WHERE contratti_fts MATCH ?))"); a += [t.upper(), fts(t)]
        elif fts(t):
            w.append("c.rowid IN (SELECT rowid FROM contratti_fts WHERE contratti_fts MATCH ?)"); a.append(fts(t))
    for k, col in (("strato", "c.strato"), ("gruppo", "c.gruppo"), ("sottoclasse", "c.sottoclasse")):
        if q.get(k) == "-":
            w.append(f"{col} = ''")
        elif q.get(k):
            w.append(f"{col} LIKE ?"); a.append(q[k] + "%")
    if "giurisdizione" in q:
        w.append("c.giurisdizione = ?"); a.append(q["giurisdizione"] if q["giurisdizione"] != "-" else "")
    if q.get("provider"):
        w.append("c.provider LIKE ?"); a.append("%" + q["provider"] + "%")
    for k, op in (("anno_da", ">="), ("anno_a", "<=")):
        if q.get(k, "").isdigit():
            w.append(f"c.anno {op} ?"); a.append(int(q[k]))
    if q.get("importo_min"):
        try: w.append("c.importo >= ?"); a.append(float(q["importo_min"]))
        except ValueError: w.pop()
    if q.get("da_verificare") in ("0", "1"):
        w.append("c.importo_da_verificare = ?"); a.append(int(q["da_verificare"]))
    if q.get("livello"):
        if q.get("esito"):
            w.append("c.cig IN (SELECT cig FROM esiti WHERE livello = ? AND esito = ?)"); a += [q["livello"], q["esito"]]
        elif q["livello"] == "-":
            w.append("c.livelli = ''")
        else:
            w.append("c.cig IN (SELECT cig FROM esiti WHERE livello = ?)"); a.append(q["livello"])
    if q.get("atti") == "1":
        w.append("c.n_atti > 0")
    return (" WHERE " + " AND ".join(w)) if w else "", a


COLONNE = ["cig", "anno", "strato", "sottoclasse", "gruppo", "giurisdizione", "provider", "servizio", "via", "cpv", "importo",
           "importo_da_verificare", "ente", "aggiudicatari", "livelli", "n_atti", "testo"]
ORDINI = {"importo": "c.importo DESC", "importo_asc": "c.importo ASC", "anno": "c.anno DESC, c.importo DESC", "cig": "c.cig"}


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
                cont = dict(c.execute(f"SELECT cig, COUNT(DISTINCT annotatore) FROM annotazioni WHERE {CIECO} GROUP BY cig").fetchall())
                fatti = {r[0] for r in c.execute(f"SELECT cig FROM annotazioni WHERE annotatore=? AND {CIECO}", (nome,))}
            liberi = [g for g in CAMP if g not in fatti and cont.get(g, 0) < ANNOTAZIONI_PER_CIG]
            if not liberi:
                return self._json({"finito": True, "fatti": len(fatti)})
            minimo = min(cont.get(g, 0) for g in liberi)
            # prima i contratti con meno annotazioni, poi a caso (seme per nome: ordine stabile per la stessa persona)
            scelta = random.Random(nome + str(len(fatti))).choice([g for g in liberi if cont.get(g, 0) == minimo])
            return self._json({"contratto": CAMP[scelta], "fatti": len(fatti), "restanti": len(liberi)})
        if u.path == "/api/stato":
            with db() as c:
                n = c.execute(f"SELECT COUNT(*), COUNT(DISTINCT cig), COUNT(DISTINCT annotatore) FROM annotazioni WHERE {CIECO}").fetchone()
                completi = c.execute(f"SELECT COUNT(*) FROM (SELECT cig FROM annotazioni WHERE {CIECO} GROUP BY cig HAVING COUNT(DISTINCT annotatore)>=?)",
                                     (ANNOTAZIONI_PER_CIG,)).fetchone()[0]
                classifica = c.execute("SELECT annotatore, COUNT(*) FROM annotazioni GROUP BY annotatore ORDER BY 2 DESC LIMIT 20").fetchall()
                cr = c.execute("SELECT COUNT(*), COUNT(DISTINCT cig) FROM annotazioni WHERE modo = 'cruscotto'").fetchone()
            return self._json({"annotazioni": n[0], "contratti_toccati": n[1], "volontari": n[2], "contratti_completi": completi,
                               "totale_contratti": len(CAMP), "per_contratto": ANNOTAZIONI_PER_CIG, "classifica": classifica,
                               "cruscotto": {"annotazioni": cr[0], "contratti": cr[1]}})
        if u.path in ("/contratti", "/contratti/"):
            b = PAGINA_CRUSCOTTO.read_bytes()
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b); return
        if u.path in ("/api/cerca", "/api/contratto", "/api/totali", "/api/indice"):
            if self._troppe(120):
                return self._json({"errore": "troppe richieste, riprova fra un minuto"}, 429)
            ix = indice()
            if ix is None:
                return self._json({"errore": "indice dei contratti non ancora costruito"}, 503)
            try:
                with ix:
                    return getattr(self, "_" + u.path[5:])(ix, q)
            except sqlite3.OperationalError as e:
                return self._json({"errore": "ricerca non valida: " + str(e)[:120]}, 400)
            finally:
                ix.close()
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
        if self._troppe(30, "post"):
            return self._json({"errore": "troppe richieste, riprova fra un minuto"}, 429)
        ip = self._ip()
        try:
            d = json.loads(self.rfile.read(min(int(self.headers.get("Content-Length", 0)), 20000)))
        except (ValueError, json.JSONDecodeError):
            return self._json({"errore": "richiesta non valida"}, 400)
        rec = {"cig": pulisci(d.get("cig"), 10), "annotatore": pulisci(d.get("nome"), 60), "e_cloud": pulisci(d.get("e_cloud"), 8),
               "servizio": pulisci(d.get("servizio"), 30), "provider": pulisci(d.get("provider"), 120),
               "giurisdizione": pulisci(d.get("giurisdizione"), 20), "confidenza": pulisci(d.get("confidenza"), 6),
               "note": pulisci(d.get("note"), 1000), "documento": pulisci(d.get("documento"), 30),
               "modo": "cruscotto" if d.get("modo") == "cruscotto" else "cieco", "ict": pulisci(d.get("ict"), 8) or None}
        if rec["modo"] == "cruscotto":
            # annotazione libera dal cruscotto: qualunque CIG dell'indice; servizio e documento facoltativi
            rec["servizio"] = rec["servizio"] or "non-so"; rec["documento"] = rec["documento"] or "no"
            ix = indice()
            try:
                noto = ix is not None and ix.execute("SELECT 1 FROM contratti WHERE cig = ?", (rec["cig"],)).fetchone() is not None
            finally:
                if ix is not None: ix.close()
            if not noto or rec["ict"] not in SI_NO:
                return self._json({"errore": "CIG non nell'indice o campo «è ICT?» mancante"}, 400)
        elif rec["cig"] not in CAMP:
            return self._json({"errore": "campi mancanti o non validi"}, 400)
        if not rec["annotatore"] or rec["e_cloud"] not in ("s", "n", "non-so") \
                or rec["servizio"] not in SERVIZI or rec["giurisdizione"] not in GIUR or rec["confidenza"] not in ("alta", "media", "bassa") or rec["documento"] not in DOCUMENTI:
            return self._json({"errore": "campi mancanti o non validi"}, 400)
        try:
            sec = max(0, min(int(d.get("secondi") or 0), 36000))
        except (TypeError, ValueError):
            sec = 0
        with lock, db() as c:
            c.execute("INSERT INTO annotazioni (cig, annotatore, e_cloud, servizio, provider, giurisdizione, confidenza, note, documento, modo, ict, secondi, quando, ip_hash)"
                      " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,datetime('now'),?)",
                      (*rec.values(), sec, hashlib.sha256(("annotazioni" + ip).encode()).hexdigest()[:16]))
        return self._json({"ok": True})

    def _troppe(self, n, tipo="get"):
        """limite per IP: n richieste al minuto per tipo"""
        k = tipo + self._ip(); ora = time.time()
        with lock:
            t = [x for x in limiti.get(k, []) if ora - x < 60]
            limiti[k] = t + [ora]
            return len(t) >= n

    def _cerca(self, ix, q):
        w, a = filtri(q)
        ordine = ORDINI.get(q.get("ordina", ""), "c.importo DESC")
        sel = ", ".join("c." + k for k in COLONNE)
        if q.get("formato") == "csv":
            righe = ix.execute(f"SELECT {sel} FROM contratti c{w} ORDER BY {ordine} LIMIT {MAX_CSV}", a).fetchall()
            s = io.StringIO(); wr = csv.writer(s); wr.writerow(COLONNE); wr.writerows([tuple(r) for r in righe])
            b = s.getvalue().encode()
            self.send_response(200); self._cors(); self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Disposition", 'attachment; filename="contratti.csv"'); self.send_header("Content-Length", str(len(b)))
            self.end_headers(); self.wfile.write(b); return
        try: pag = max(0, min(int(q.get("pagina", 0)), 2000))
        except ValueError: pag = 0
        tot = ix.execute(f"SELECT count(*), sum(CASE WHEN c.strato LIKE 'S0%' THEN 0 ELSE c.importo END) FROM contratti c{w}", a).fetchone()
        righe = ix.execute(f"SELECT {sel} FROM contratti c{w} ORDER BY {ordine} LIMIT {PER_PAGINA} OFFSET {pag * PER_PAGINA}", a).fetchall()
        return self._json({"totale": tot[0], "euro": round(tot[1] or 0), "pagina": pag, "per_pagina": PER_PAGINA,
                           "righe": [{k: (r[k][:300] if k == "testo" else r[k]) for k in COLONNE} for r in righe]})

    def _contratto(self, ix, q):
        cig = (q.get("cig") or "").strip().upper()
        r = ix.execute("SELECT * FROM contratti WHERE cig = ?", (cig,)).fetchone()
        if r is None:
            return self._json({"errore": "CIG non nell'indice dell'imbuto"}, 404)
        d = {k: r[k] for k in r.keys()}
        d["esiti"] = [dict(x) for x in ix.execute("SELECT livello, esito, certezza, giurisdizione, provider, dettaglio, fonte FROM esiti WHERE cig = ? ORDER BY livello", (cig,))]
        b = ix.execute("SELECT * FROM bdncp WHERE cig = ?", (cig,)).fetchone()
        d["bdncp"] = {k: b[k] for k in b.keys()} if b else None
        d["atti"] = [dict(x) for x in ix.execute("SELECT url, sha256, tipo_atto, esito_recupero, recuperato_il FROM atti WHERE cig = ? ORDER BY recuperato_il", (cig,))]
        with db() as c:  # annotazioni senza il nome di chi annota (dato personale) né l'IP
            c.row_factory = sqlite3.Row
            d["annotazioni"] = [dict(x) for x in c.execute("SELECT coalesce(modo, 'cieco') AS modo, ict, e_cloud, servizio, provider, giurisdizione,"
                                                         " confidenza, documento, note, quando FROM annotazioni WHERE cig = ? ORDER BY id", (cig,))]
        d["campione_cieco"] = cig in CAMP
        return self._json(d)

    def _totali(self, ix, q):
        chiave = (q.get("anno_da", ""), q.get("anno_a", ""), q.get("da_verificare", ""), INDICE.stat().st_mtime)
        if chiave in cache_totali:
            return self._json(cache_totali[chiave])
        w, a = filtri({k: q[k] for k in ("anno_da", "anno_a", "da_verificare") if k in q})
        eur = "sum(CASE WHEN c.strato LIKE 'S0%' THEN 0 ELSE c.importo END)"
        T = {"filtri": dict(zip(("anno_da", "anno_a", "da_verificare"), chiave[:3])),
             "strato_giurisdizione": [list(x) for x in ix.execute(f"SELECT c.strato, c.giurisdizione, count(*), round({eur}) FROM contratti c{w} GROUP BY 1, 2 ORDER BY 1, 2", a)],
             "strato_gruppo": [list(x) for x in ix.execute(f"SELECT c.strato, c.gruppo, count(*), round({eur}) FROM contratti c{w} GROUP BY 1, 2 ORDER BY 1, 2", a)],
             "livello_esito": [list(x) for x in ix.execute(f"SELECT e.livello, e.esito, count(*), round({eur}) FROM esiti e JOIN contratti c ON c.cig = e.cig{w} GROUP BY 1, 2 ORDER BY 1, 3 DESC", a)],
             "indice": json.loads(ix.execute("SELECT valore FROM meta WHERE chiave = 'riepilogo'").fetchone()[0])}
        T["indice"].pop("ingressi_sha256", None)
        cache_totali[chiave] = T
        return self._json(T)

    def _indice(self, ix, q):
        return self._json(json.loads(ix.execute("SELECT valore FROM meta WHERE chiave = 'riepilogo'").fetchone()[0]))

    def log_message(self, fmt, *a):
        pass


if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("--porta", type=int, default=8790); a.add_argument("--host", default="127.0.0.1")
    x = a.parse_args()
    DB.parent.mkdir(parents=True, exist_ok=True); db().close()
    print(f"annotazioni su http://{x.host}:{x.porta}  ({len(CAMP)} contratti)", flush=True)
    ThreadingHTTPServer((x.host, x.porta), H).serve_forever()
