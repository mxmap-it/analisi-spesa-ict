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
Uso (server): nice .venv/bin/python tools/acquisizione/piattaforme_cig.py INGRESSO.csv USCITA_DIR
  INGRESSO.csv: colonne cig, link (altre ignorate). Ripartibile: i CIG già in USCITA_DIR/esiti.jsonl si saltano.
Uscita: USCITA_DIR/esiti.jsonl (una riga per CIG: famiglia, esito, pagine, documenti con sha256 e testo estratto).
"""
import csv, hashlib, html, json, os, re, subprocess, sys, time
from pathlib import Path
from urllib.parse import urljoin, urlsplit

import requests

RADICE = Path(__file__).resolve().parent.parent.parent
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36 "
      "analisi-spesa-ict (+https://github.com/mxmap-it/analisi-spesa-ict)")
PAUSA = 6.0
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


def famiglia(u):
    if "PortaleAppalti" in u or "ppgare_" in u: return "portaleappalti"
    if "/esop/" in u: return "esop"
    return "generico"


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
    if cig in t: rec["esito"] = "cig-nella-pagina"; return
    base = urlsplit(r.url).netloc; visti = 0
    for href in re.findall(r'href="([^"#]+)"', r.text):
        v = urljoin(r.url, html.unescape(href))
        if urlsplit(v).netloc != base or not re.search(r"band|gar|contratt|esit|affidament|procedur|202[4-6]", v, re.I): continue
        visti += 1
        if visti > 15: break
        try: rr, hh, tt = prendi(s, v, out)
        except Exception: continue
        rec["pagine"].append({"url": rr.url, "sha256": hh, "cig_presente": cig in tt})
        if cig in tt: rec["esito"] = "cig-in-sottopagina"; return
    rec["esito"] = "cig-non-trovato"


def main():
    ing, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    fatti = {json.loads(l)["cig"] for l in open(out / "esiti.jsonl", encoding="utf-8")} if (out / "esiti.jsonl").exists() else set()
    s = requests.Session(); s.headers["User-Agent"] = UA
    for r in csv.DictReader(open(ing, encoding="utf-8")):
        cig, u = r["cig"], r.get("link", "")
        if not u or cig in fatti: continue
        rec = {"cig": cig, "link": u, "famiglia": famiglia(u), "pagine": [], "documenti": [], "esito": "", "data": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        try:
            {"portaleappalti": portaleappalti, "esop": esop, "generico": generico}[rec["famiglia"]](s, cig, u, out, rec)
        except Exception as e:
            rec["esito"] = "errore"; rec["errore"] = str(e)[:200]
        with open(out / "esiti.jsonl", "a", encoding="utf-8") as f: f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(cig, rec["famiglia"], rec["esito"], len(rec["documenti"]), flush=True)


if __name__ == "__main__":
    main()
