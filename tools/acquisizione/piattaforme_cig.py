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
# Monitoraggio PVL/AT (clone ~/visibilita-pa): blocchi, firme anti-bot, robots.txt e piattaforme AT si riusano da lì.
os.environ.setdefault("ARCHIVIO_ROOT", str(Path(os.environ.get("SPESAICT_BASE", Path(__file__).resolve().parents[2])) / "archivio"))
sys.path.insert(0, os.environ.get("VISIBILITA_PA", str(Path.home() / "visibilita-pa")))
from visibilita_pa.core import robots as VROBOTS, platforms as VPIATT  # noqa: E402
from visibilita_pa.core.probes import extended as VEXT  # noqa: E402

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
    attendi(u)
    try:
        r = s.get(u, timeout=60, allow_redirects=True)
    except requests.exceptions.ConnectionError:
        # es. ariaspa.it: la porta 80 non risponde, la 443 sì
        if not u.lower().startswith("http://"): raise
        u = "https://" + u[7:]; attendi(u); r = s.get(u, timeout=60, allow_redirects=True)
    h = archivia(r.content, r.url, out)
    testo = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", r.text))) if "html" in r.headers.get("content-type", "") else ""
    return r, h, testo


def blocco_v1(r, testo):
    """Regole proprie fino al 7/11/2026, tenute solo per il confronto (tools/verifiche/blocchi_vpa_confronto.py)."""
    if "login" in r.url.lower() and "public" not in r.url.lower(): return "login"
    if r.status_code in (401, 403, 429): return f"HTTP {r.status_code}"
    if re.search(r"login.html", r.text) and len(testo) < 1500: return "login"   # home che rimanda (anche via JS) al login
    # FriendlyCaptcha (frc-*) di PortaleAppalti protegge solo i moduli di accesso: non è un blocco se la pagina ha contenuto
    if SEGNI_BLOCCO.search(testo[:20000]) and not ("frc-" in r.text and len(testo) > 2000): return "anti-bot"
    return ""


def blocco(r, testo):
    """Login e HTTP come prima; anti-bot con visibilita_pa (extended.riconosci_blocco: firme dei vendor, CAPTCHA,
    challenge JS, con le stesse esclusioni per i moduli di accesso nelle pagine normali)."""
    if "login" in r.url.lower() and "public" not in r.url.lower(): return "login"
    if r.status_code in (401, 403, 429): return f"HTTP {r.status_code}"
    if re.search(r"login.html", r.text) and len(testo) < 1500: return "login"
    # pagina-cancello con CAPTCHA nell'URL (es. dati.anticorruzione.it/superset/recaptcha/): riconosci_blocco guarda solo
    # il corpo e la scarta perché è lunga; regola da proporre a visibilita-pa
    if re.search(r"/[^/?]*captcha", urlsplit(r.url).path, re.I): return "anti-bot"
    b = VEXT.riconosci_blocco(r.status_code, dict(r.headers), r.text, [])
    if b["vendor_blocco"] or b["challenge_js"]: return "anti-bot"
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


# Ricerca interna per CIG (adattatore trasversale ai software AT e ai portali): moduli GET con un solo campo di testo
# (ISWEB, Halley, PortaleAppalti, Traspare, trasparenza-pa.net, Drupal, WordPress…) e ricerche note per generatore.
RX_FORM = re.compile(r"<form\b([^>]*)>(.*?)</form>", re.I | re.S)
RX_INPUT = re.compile(r"<input\b([^>]*)>", re.I)


def _attr(a, n):
    m = re.search(rf"\b{n}\s*=\s*[\"']([^\"']*)[\"']", a, re.I)
    return html.unescape(m.group(1)) if m else ""


def modelli_ricerca(r):
    """URL modello (con {CIG}) dalle form GET con un solo campo di testo e dai generatori noti."""
    mod = []
    for fa, corpo in RX_FORM.findall(r.text):
        if _attr(fa, "method").lower() == "post": continue
        testo, nascosti = [], []
        for ia in RX_INPUT.findall(corpo):
            t = (_attr(ia, "type") or "text").lower(); n = _attr(ia, "name")
            if not n: continue
            if t in ("text", "search"): testo.append(n)
            elif t == "hidden": nascosti.append((n, _attr(ia, "value")))
        if len(testo) != 1: continue
        az = urljoin(r.url, _attr(fa, "action") or r.url)
        if "login" in az.lower(): continue
        q = "&".join(f"{n}={requests.utils.quote(v)}" for n, v in nascosti if n.lower() not in ("csrf", "_token"))
        mod.append(az.split("#")[0] + ("&" if "?" in az else "?") + (q + "&" if q else "") + f"{testo[0]}={{CIG}}")
    g = re.search(r"<meta[^>]+generator[^>]+content=[\"']([^\"']+)", r.text, re.I)
    base = f"{urlsplit(r.url).scheme}://{urlsplit(r.url).netloc}"
    if g and "wordpress" in g.group(1).lower(): mod.append(base + "/?s={CIG}")
    if g and "drupal" in g.group(1).lower(): mod.append(base + "/search/node?keys={CIG}")
    return list(dict.fromkeys(mod))[:2]


def cerca_cig(s, cigs, pagine, out, massimo=25):
    """Prova la ricerca interna per i CIG (ordinati per priorità): {cig: risposta della pagina che lo cita}, richieste."""
    mod = []
    for r in pagine:
        mod += [m for m in modelli_ricerca(r) if m not in mod]
    trovati, n = {}, 0
    if not mod: return trovati, 0, []
    m0 = mod[0]
    for c in cigs[:massimo]:
        try:
            rr, hh, tt = prendi(s, m0.replace("{CIG}", c), out); n += 1
        except Exception:
            continue
        if blocco(rr, tt): break
        if c in tt: trovati[c] = rr
    return trovati, n, mod


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
    tr, n, mod = cerca_cig(s, [cig], [r], out, 1)
    if mod: rec["ricerca"] = {"modelli": mod, "richieste": n}
    if cig in tr:
        documenti_pagina(s, cig, tr[cig], out, rec); rec["esito"] = "documenti" if rec["documenti"] else "cig-con-ricerca"; return
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
    """robots.txt con il parser del monitoraggio AT (visibilita_pa.core.robots, RFC 9309); agente «analisi-spesa-ict»."""
    if k not in ROBOTS:
        try:
            attendi(k + "/robots.txt"); r = requests.get(k + "/robots.txt", headers={"User-Agent": UA}, timeout=20)
            ROBOTS[k] = VROBOTS.analizza(r.text if r.status_code == 200 else "")
        except Exception:
            ROBOTS[k] = VROBOTS.analizza("")
    return VROBOTS.consentito(ROBOTS[k], "analisi-spesa-ict", p.path + ("?" + p.query if p.query else "") or "/")[0]


def robots_ok_v1(u):
    """Parser della libreria standard, fino al 7/11/2026: solo per il confronto."""
    p = urlsplit(u); k = f"{p.scheme}://{p.netloc}"
    rp = urllib.robotparser.RobotFileParser()
    try:
        r = requests.get(k + "/robots.txt", headers={"User-Agent": UA}, timeout=20)
        rp.parse(r.text.splitlines() if r.status_code == 200 else [])
    except Exception:
        rp.parse([])
    return rp.can_fetch(UA, u)


# Eccezione AGENTS.md §3 (Fabio, 3/11/2026): per le sezioni «Amministrazione trasparente» e gli atti obbligatori robots.txt
# non vincola (art. 9 c. 1 d.lgs. 33/2013). Su questi host si scarica anche se robots.txt esclude, solo in orari di poco
# carico (ORE_AT, default 21-7), >= 5 s per host; robots.txt si archivia come evidenza di violazione.
AT_HOST = [l.split("#")[0].strip() for l in open(RADICE / "config/at_robots_esenti.txt", encoding="utf-8")
           if l.split("#")[0].strip()] if (RADICE / "config/at_robots_esenti.txt").exists() else []
ORE_AT = os.environ.get("ORE_AT", "21-7")
EVIDENZE = {}
SOLO_HOST = os.environ.get("SOLO_HOST", "")   # regex sugli host: limita un ripasso (es. RIPASSA=errore SOLO_HOST=ariaspa)


def at_esente(u):
    """Host di software AT: riconoscimento per host di visibilita_pa (platforms.riconosci); in più gli host che le sue
    regole non coprono ancora (config/at_robots_esenti.txt: cloud.urbi.it, sicopat2; proposta da portare là)."""
    h = urlsplit(u).netloc.lower()
    return VPIATT.riconosci(h, "", {}).get("prova") == "host" or any(h == d or h.endswith("." + d) for d in AT_HOST)


def ora_at():
    a, b = (int(x) for x in ORE_AT.split("-")); o = time.localtime().tm_hour
    return (o >= a or o < b) if a > b else (a <= o < b)


def robots_evidenza(u, out):
    p = urlsplit(u); k = f"{p.scheme}://{p.netloc}/robots.txt"
    attendi(k); r = requests.get(k, headers={"User-Agent": UA}, timeout=20)
    return {"url": k, "http": r.status_code, "sha256": archivia(r.content, k, out), "norma": "art. 9 c. 1 d.lgs. 33/2013"}


def normalizza(u):
    u = u.strip().strip('"').strip("'").strip()
    return u if re.match(r"https?://", u, re.I) else ("http://" + u if u else "")


def main():
    ing, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    # RIPASSA=robots,errore rifà i CIG il cui ULTIMO esito è fra quelli (le righe nuove si accodano: vale l'ultima)
    ripassa = set(filter(None, os.environ.get("RIPASSA", "").split(",")))
    ultimo = {}
    if (out / "esiti.jsonl").exists():
        for l in open(out / "esiti.jsonl", encoding="utf-8"):
            x = json.loads(l); ultimo[x["cig"]] = x["esito"]
    fatti = {c for c, e in ultimo.items() if e not in ripassa}
    per_host = {}
    for r in csv.DictReader(open(ing, encoding="utf-8")):
        u = normalizza(r.get("link", ""))
        if r["cig"] in fatti: continue
        if SOLO_HOST and not re.search(SOLO_HOST, urlsplit(u).netloc, re.I): continue
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
                elif rec["famiglia"] != "js" and not robots_ok(u) and not at_esente(u): rec["esito"] = "robots"
                elif rec["famiglia"] != "js" and not robots_ok(u) and not ora_at():
                    continue   # host AT escluso da robots.txt: si passa solo in orari di poco carico, al prossimo giro
                else:
                    if rec["famiglia"] != "js" and not robots_ok(u):
                        k = urlsplit(u).netloc
                        if k not in EVIDENZE: EVIDENZE[k] = robots_evidenza(u, out)
                        rec["robots_escluso_at"] = EVIDENZE[k]
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
    if not stop.is_set(): (out / os.environ.get("FINE_FILE", "FINITO.txt")).write_text(time.strftime("%FT%T\n"))


if __name__ == "__main__":
    main()
