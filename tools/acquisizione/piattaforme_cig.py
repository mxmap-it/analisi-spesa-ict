#!/usr/bin/env python3
"""Ricerca di un CIG dentro le piattaforme di e-procurement, da anonimo (#66, rendiconto 0.8).

Perché: il link PVL ai documenti di gara (`documenti_di_gara_link`) spesso punta alla home o a un elenco della
piattaforma, non all'atto. Questo strumento prova a raggiungere, senza login, la pagina della procedura e i
documenti pubblici, con un adattatore per famiglia di piattaforma. Ogni pagina e documento scaricato finisce
nell'archivio content-addressed (tools/archivia.py --da-file), con sha256.

Regole (AGENTS.md §3): User-Agent da browser con l'URL del progetto, >= 6 s fra richieste allo stesso host, mai
login, registrazione, CAPTCHA o aree riservate: se la piattaforma chiede il login o mostra una verifica anti-bot, il
CIG si chiude con esito «blocco» e la riga va in report/convenzioni/blocchi-accesso.csv.

Famiglie (riconosciute dall'URL o dal contenuto):
  portaleappalti  Maggioli/Eldasoft «PortaleAppalti» (…/PortaleAppalti/…, ppgare_*.wp): la pagina procedura
                  (openProcedura / codice=Gxxxxx) ha «Altri atti e documenti» (viewAttiDocumenti.action) con i
                  link pubblici downloadDocumentoPubblico.action: si scaricano tutti
  esop            Jaggaer/BravoSolution «esop» (…/esop/…-host/…): elenco pubblico delle opportunità
                  (opportunityListFiltered.jsp); si cerca il CIG nell'elenco e nelle pagine di dettaglio pubbliche;
                  se l'URL porta a login.html è un blocco «login»
  generico        qualunque altra pagina: si cerca il CIG nella pagina e nei link della stessa sezione (max 15)
Uso (server): nice .venv/bin/python tools/acquisizione/piattaforme_cig.py INGRESSO.csv USCITA_DIR  (env: PAUSA_HOST=5, HOST_PARALLELI=10, GUARDIA_GB=15)
  INGRESSO.csv: colonne cig, link [priorita, importo, stazione_appaltante]. Un thread per host (max 10 host insieme). Ripartibile: i CIG già in USCITA_DIR/esiti.jsonl si saltano.
Uscita: USCITA_DIR/esiti.jsonl (una riga per CIG: famiglia, esito, pagine, documenti con sha256); i documenti che citano
  il CIG vanno anche in dati/atti/atti-server.jsonl (spesaict.atto/1, livello L3) con il testo in dati/atti/testi/.
"""
import csv, hashlib, html, json, os, re, subprocess, sys, time
from pathlib import Path
from urllib.parse import urljoin, urlsplit

import requests

RADICE = Path(__file__).resolve().parent.parent.parent
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36 "
      "analisi-spesa-ict (+https://github.com/mxmap-it/analisi-spesa-ict)")
PAUSA = float(os.environ.get("PAUSA_HOST", "5"))
ULTIMO = {}
SEGNI_BLOCCO = re.compile(r"captcha|recaptcha|hcaptcha|turnstile|just a moment|checking your browser|access denied|radware|imperva", re.I)


def attendi(u):
    h = urlsplit(u).netloc; t = ULTIMO.get(h, 0) + PAUSA - time.time()
    if t > 0: time.sleep(t)
    ULTIMO[h] = time.time()


def archivia(dati, url, out):
    h = hashlib.sha256(dati).hexdigest(); p = out / "file" / h
    p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(dati)
    subprocess.run([sys.executable, str(RADICE / "tools/archivia.py"), "--da-file", str(p), "--url", url,
                    "--data", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "--nota", "piattaforme_cig.py #66"],
                   capture_output=True, cwd=RADICE)
    p.unlink()  # la copia resta nell'archivio (blob); niente doppioni su disco
    return h


def prendi(s, u, out):
    attendi(u); r = s.get(u, timeout=60, allow_redirects=True)
    h = archivia(r.content, r.url, out)
    testo = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", r.text))) if "html" in r.headers.get("content-type", "") else ""
    return r, h, testo


def blocco(r, testo):
    if "login" in r.url.lower() and "public" not in r.url.lower(): return "login"
    if r.status_code in (401, 403, 429): return f"HTTP {r.status_code}"
    if re.search(r"login.html", r.text) and len(testo) < 1500: return "login"   # home che rimanda (anche via JS) al login
    # FriendlyCaptcha (frc-*) di PortaleAppalti protegge solo i moduli di accesso: non è un blocco se la pagina ha contenuto
    if SEGNI_BLOCCO.search(testo[:20000]) and not ("frc-" in r.text and len(testo) > 2000): return "anti-bot"
    return ""


def testo_pdf(dati):
    try:
        return subprocess.run(["pdftotext", "-layout", "-l", "40", "-", "-"], input=dati, capture_output=True, timeout=120).stdout.decode("utf-8", "replace")
    except Exception:
        return ""


# Famiglie aggiunte per il residuo S6 (#57, mappa esiti/pvl-link-cig/2026-11-04/sistemi.csv):
#   js    MePA/acquistinretepa: le schede sono in JavaScript; il browser reale lo decide Fabio: non si tenta
#   home  il link PVL è la sola home della piattaforma o dell'ente (START, Sintel, SATER, EmPULIA, Alto Adige…):
#         la home si scarica UNA volta per URL (cache) e si guarda solo se cita il CIG
#   generico (anche trasparenza-pa.net, halleyweb, ASMECOMM, STELLA, Traspare…): se la pagina o una sottopagina
#         cita il CIG, si scaricano i documenti collegati (PDF, p7m, allegati; max 12)
JS = ("acquistinretepa.it",)
HOME = re.compile(r"^/?(index\.(php|html?|jsp|aspx?)|home|it|portale|web|alboeproc/?[^/]*)?/?$", re.I)
RX_DOC = re.compile(r"\.(pdf|p7m|docx?|xlsx?|zip|odt)(\?|$)|download|scarica|allegat|documento|getfile|attachment", re.I)
CACHE = {}


def famiglia(u):
    p = urlsplit(u if "://" in u else "http://" + u); h = p.netloc.lower()
    if "PortaleAppalti" in u or "ppgare_" in u: return "portaleappalti"
    if "/esop/" in u: return "esop"
    if any(h.endswith(d) for d in JS): return "js"
    if HOME.match(p.path) and not p.query: return "home"
    return "generico"


def documenti_pagina(s, cig, r, out, rec, massimo=12):
    """Scarica i documenti collegati da una pagina che cita il CIG (stesso dominio)."""
    base = ".".join(urlsplit(r.url).netloc.split(".")[-2:]); visti = set()
    for href in re.findall(r"href=[\"']([^\"'#]+)[\"']", r.text):
        du = urljoin(r.url, html.unescape(href)).split(";jsessionid")[0]
        if du in visti or not RX_DOC.search(du) or not urlsplit(du).netloc.endswith(base): continue
        visti.add(du)
        if len(visti) > massimo: break
        try:
            attendi(du); d = s.get(du, timeout=120)
        except Exception:
            continue
        if d.status_code != 200 or len(d.content) < 200 or "html" in d.headers.get("content-type", ""): continue
        hd = archivia(d.content, du, out)
        tx = testo_pdf(d.content) if d.content[:4] == b"%PDF" else ""
        rec["documenti"].append({"url": du, "sha256": hd, "byte": len(d.content), "cig_presente": cig in tx, "testo": tx[:20000]})


def js(s, cig, u, out, rec):
    rec["esito"] = "non-tentato-js"


def home(s, cig, u, out, rec):
    if u not in CACHE:
        r, h, t = prendi(s, u, out); CACHE[u] = (r.url, h, t, blocco(r, t))
    url, h, t, b = CACHE[u]; rec["pagine"].append({"url": url, "sha256": h, "cig_presente": cig in t})
    rec["esito"] = ("blocco" if b else "cig-nella-home" if cig in t else "link-home")
    if b: rec["blocco"] = b


def portaleappalti(s, cig, u, out, rec):
    r, h, t = prendi(s, u, out); rec["pagine"].append({"url": r.url, "sha256": h, "cig_presente": cig in t})
    if (b := blocco(r, t)): rec["esito"] = "blocco"; rec["blocco"] = b; return
    m = re.search(r"codice=(G\d+)", r.url + r.text)
    if not m: rec["esito"] = "procedura-non-trovata"; return
    base = f"{urlsplit(r.url).scheme}://{urlsplit(r.url).netloc}/PortaleAppalti/it/ppgare_detail.wp"
    for azione in ("Esiti/viewAttiDocumenti", "Bandi/viewAttiDocumenti"):
        ua = f"{base}?actionPath=/ExtStr2/do/FrontEnd/{azione}.action&currentFrame=7&codice={m.group(1)}&ext="
        ra, ha, ta = prendi(s, ua, out); rec["pagine"].append({"url": ua, "sha256": ha})
        for href in re.findall(r'href="([^"]*downloadDocumentoPubblico[^"]*)"', ra.text):
            du = urljoin(ra.url, html.unescape(href))
            attendi(du); d = s.get(du, timeout=120)
            if d.status_code != 200 or len(d.content) < 200: continue
            hd = archivia(d.content, du.split(";jsessionid")[0], out)
            tx = testo_pdf(d.content) if d.content[:4] == b"%PDF" else ""
            rec["documenti"].append({"url": du.split(";jsessionid")[0], "sha256": hd, "byte": len(d.content), "cig_presente": cig in tx, "testo": tx[:20000]})
    rec["esito"] = "documenti" if rec["documenti"] else "nessun-documento"


def esop(s, cig, u, out, rec):
    r, h, t = prendi(s, u, out); rec["pagine"].append({"url": r.url, "sha256": h, "cig_presente": cig in t})
    if (b := blocco(r, t)): rec["esito"] = "blocco"; rec["blocco"] = b; return
    if cig in t: rec["esito"] = "cig-nell-elenco"; return
    rec["esito"] = "cig-non-trovato-nell-elenco-pubblico"


def generico(s, cig, u, out, rec):
    r, h, t = prendi(s, u, out); rec["pagine"].append({"url": r.url, "sha256": h, "cig_presente": cig in t})
    if (b := blocco(r, t)): rec["esito"] = "blocco"; rec["blocco"] = b; return
    if cig in t:
        documenti_pagina(s, cig, r, out, rec); rec["esito"] = "documenti" if rec["documenti"] else "cig-nella-pagina"; return
    base = urlsplit(r.url).netloc; visti = 0
    for href in re.findall(r'href="([^"#]+)"', r.text):
        v = urljoin(r.url, html.unescape(href))
        if urlsplit(v).netloc != base or not re.search(r"band|gar|contratt|esit|affidament|procedur|202[4-6]", v, re.I): continue
        visti += 1
        if visti > 15: break
        try: rr, hh, tt = prendi(s, v, out)
        except Exception: continue
        rec["pagine"].append({"url": rr.url, "sha256": hh, "cig_presente": cig in tt})
        if cig in tt:
            documenti_pagina(s, cig, rr, out, rec); rec["esito"] = "documenti" if rec["documenti"] else "cig-in-sottopagina"; return
    rec["esito"] = "cig-non-trovato"


def registra_atto(cig, d, livello, ente):
    """spesaict.atto/1 (come tools/llm/atti.py) per i documenti che citano il CIG: la via 6 li trova per CIG."""
    TESTI = RADICE / "dati/atti/testi"; TESTI.mkdir(parents=True, exist_ok=True)
    (TESTI / f"{d['sha256']}.txt").write_text(d["testo"], encoding="utf-8")
    rec = {"schema": "spesaict.atto/1", "cig": cig, "url": d["url"],
           "trovato_con": {"livello": livello, "metodo": "link PVL documenti_di_gara_link, piattaforme_cig.py", "query": ""},
           "recuperato_il": time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime()), "http_status": 200, "mime": "application/pdf",
           "byte": d["byte"], "sha256": d["sha256"], "tipo_atto": "altro", "ente": ente,
           "estrazione": {"strumento": "pdftotext", "ocr": False, "testo_sha256": hashlib.sha256(d["testo"].encode()).hexdigest(), "caratteri": len(d["testo"])},
           "pertinenza": "cig-citato", "esito_recupero": "ok"}
    with LOCK, open(RADICE / "dati/atti/atti-server.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


import threading, shutil, urllib.robotparser
from concurrent.futures import ThreadPoolExecutor
LOCK = threading.Lock()
GUARDIA_GB = float(os.environ.get("GUARDIA_GB", "15"))   # Fabio 7/11: scaricamenti per l'analisi fino a 15 GB liberi
PARALLELO = int(os.environ.get("HOST_PARALLELI", "10"))
ROBOTS = {}


def robots_ok(u):
    p = urlsplit(u); k = f"{p.scheme}://{p.netloc}"
    if k not in ROBOTS:
        rp = urllib.robotparser.RobotFileParser()
        try:
            attendi(k + "/robots.txt"); r = requests.get(k + "/robots.txt", headers={"User-Agent": UA}, timeout=20)
            rp.parse(r.text.splitlines() if r.status_code == 200 else [])
        except Exception:
            rp.parse([])
        ROBOTS[k] = rp
    return ROBOTS[k].can_fetch(UA, u)


def normalizza(u):
    u = u.strip().strip('"').strip("'").strip()
    return u if re.match(r"https?://", u, re.I) else ("http://" + u if u else "")


def main():
    ing, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    fatti = {json.loads(l)["cig"] for l in open(out / "esiti.jsonl", encoding="utf-8")} if (out / "esiti.jsonl").exists() else set()
    per_host = {}
    for r in csv.DictReader(open(ing, encoding="utf-8")):
        u = normalizza(r.get("link", ""))
        if r["cig"] in fatti: continue
        per_host.setdefault(urlsplit(u).netloc.lower() if u else "", []).append((r, u))
    stop = threading.Event()

    def scrivi(rec):
        with LOCK, open(out / "esiti.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    def host(h):
        s = requests.Session(); s.headers["User-Agent"] = UA
        for r, u in per_host[h]:
            if stop.is_set(): return
            if shutil.disk_usage(RADICE).free / 1e9 < GUARDIA_GB:
                stop.set(); (out / "STOP-disco.txt").write_text(time.strftime("%FT%T ") + f"spazio libero sotto {GUARDIA_GB} GB\n"); return
            cig = r["cig"]
            rec = {"cig": cig, "priorita": r.get("priorita", ""), "importo": r.get("importo", ""), "link": u,
                   "famiglia": famiglia(u) if u else "senza-link", "pagine": [], "documenti": [], "esito": "",
                   "data": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
            t0 = time.time()
            try:
                if not u: rec["esito"] = "senza-link"
                elif rec["famiglia"] != "js" and not robots_ok(u): rec["esito"] = "robots"
                else:
                    {"portaleappalti": portaleappalti, "esop": esop, "generico": generico, "js": js, "home": home}[rec["famiglia"]](s, cig, u, out, rec)
            except Exception as e:
                rec["esito"] = "errore"; rec["errore"] = str(e)[:200]
            rec["secondi"] = round(time.time() - t0, 1)
            for d in rec["documenti"]:
                if d.get("cig_presente") and d.get("testo"): registra_atto(cig, d, "L3", r.get("stazione_appaltante", ""))
                d["testo"] = d.get("testo", "")[:500]   # il testo intero sta in dati/atti/testi (se cita il CIG) o si rigenera dal blob
            scrivi(rec)
            print(cig, h, rec["famiglia"], rec["esito"], len(rec["documenti"]), flush=True)

    # host grandi prima, così i 10 posti restano pieni
    with ThreadPoolExecutor(PARALLELO) as ex:
        list(ex.map(host, sorted(per_host, key=lambda h: -len(per_host[h]))))
    if not stop.is_set(): (out / "FINITO.txt").write_text(time.strftime("%FT%T\n"))


if __name__ == "__main__":
    main()
