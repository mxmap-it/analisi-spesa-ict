"""#62, passo 3a: per ogni iniziativa del censimento trova la pagina del bando su consip.it e ne elenca i documenti.

Ricerca pubblica consip.it/imprese/bandi (testo libero = ID Sigef, o il CIG padre se manca l'ID); nessun login,
nessun CAPTCHA, una richiesta ogni 5 s, User-Agent del progetto. Ripartibile: salta le iniziative con esito gia' scritto.
Uscita (piccola, versionata): report/convenzioni/database/consip/<iniziativa>.json con URL della pagina, sha256 dell'HTML,
data, e l'elenco dei documenti linkati (URL, nome, tipo dedotto dal nome).
Uso: python tools/convenzioni/consip_pagine.py [--rifai]"""
import csv, hashlib, json, re, sys, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote
import requests

R = Path(__file__).resolve().parent.parent.parent
DB = R / "report/convenzioni/database"
OUT = DB / "consip"
UA = "Mozilla/5.0 (X11; Linux x86_64) analisi-spesa-ict (+https://github.com/mxmap-it/analisi-spesa-ict)"
BASE = "https://www.consip.it"
PAUSA = 5
# tipo di documento dedotto dal nome del file (ordine = priorita')
TIPI = [
    ("aggiudicazione", r"aggiudicaz|esito|graduatoria"),
    ("chiarimenti", r"chiariment"),
    ("determina", r"determina|decisione a contrarre"),
    ("commissione", r"nomina|commission|seggio|curricul"),
    ("listini", r"listin|prezzi|corrispettiv"),
    ("capitolato", r"capitolato"),
    ("schema_aq_convenzione", r"schema|accordo quadro|convenzione|contratto quadro"),
    ("disciplinare", r"disciplinare|cdo\b|condizioni|lettera d.invito"),
    ("bando", r"bando|guue|guri|avviso"),
    ("pacchetto_documentazione", r"doc(umentazione)?[ _%20-]*(non[ _%20-]*)?uff|\.zip$"),
    ("modulistica", r"modul|dichiaraz|dgue|allegato"),
]


def tipo(nome):
    n = nome.lower()
    for t, rx in TIPI:
        if re.search(rx, n):
            return t
    return "altro"


def get(s, url):
    time.sleep(PAUSA)
    return s.get(url, timeout=60)


def cerca(s, chiave):
    r = get(s, f"{BASE}/imprese/bandi?search_api_fulltext={chiave}")
    return sorted(set(re.findall(r'href="(/bandi/[^"?#]+)"', r.text)))


def main(rifai=False):
    OUT.mkdir(parents=True, exist_ok=True)
    s = requests.Session(); s.headers["User-Agent"] = UA
    viste = {}
    for r in csv.DictReader(open(DB / "censimento.csv", encoding="utf-8")):
        viste.setdefault(r["iniziativa"], r["cig_padre"])
    for ini, cig in viste.items():
        dest = OUT / f"{ini}.json"
        if dest.exists() and not rifai:
            continue
        m = re.match(r"consip-(\d{4})$", ini)
        chiave = m.group(1) if m else cig
        esito = {"iniziativa": ini, "chiave_ricerca": chiave, "data": datetime.now(timezone.utc).isoformat(timespec="seconds"), "pagine": []}
        try:
            cand = cerca(s, chiave)
            if m:  # con l'ID si tengono solo le pagine che lo citano nello slug (es. ...-id-2928)
                cand = [c for c in cand if re.search(rf"id-?{chiave}\b", c)] or cand[:3]
            for c in cand[:4]:
                p = get(s, BASE + c)
                html = p.text
                docs = []
                for h in sorted(set(re.findall(r'href="([^"]+\.(?:pdf|p7m|zip|xlsx?|docx?|odt|ods|rar))"', html, re.I))):
                    u = h if h.startswith("http") else BASE + h
                    if "cv-commissione" in u or "curricul" in u.lower():
                        continue  # dati personali non necessari all'analisi
                    nome = unquote(u.rsplit("/", 1)[-1])
                    docs.append({"url": u, "nome": nome, "tipo": tipo(nome)})
                cita = (chiave in html) or (cig in html)
                esito["pagine"].append({"url": BASE + c, "http": p.status_code, "sha256_html": hashlib.sha256(p.content).hexdigest(),
                                        "cita_chiave": cita, "titolo": (re.search(r"<title>([^<]*)", html) or [None, ""])[1].strip(),
                                        "documenti": docs})
            esito["esito"] = "trovata" if any(pg["cita_chiave"] for pg in esito["pagine"]) else "non-trovata"
        except requests.RequestException as e:
            esito["esito"] = "errore"; esito["errore"] = str(e)[:200]
        dest.write_text(json.dumps(esito, ensure_ascii=False, indent=1), encoding="utf-8")
        print(ini, esito["esito"], sum(len(p["documenti"]) for p in esito["pagine"]), flush=True)


if __name__ == "__main__":
    main("--rifai" in sys.argv)
