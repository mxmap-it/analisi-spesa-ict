"""Prove su un ente: robots.txt, pagina AT con UA da bot dichiarato e da browser identificato,
meta robots / X-Robots-Tag, challenge anti-bot, TLS, piattaforma. Nessun UA di Googlebot.

Evidenze nell'archivio content-addressed: robots.txt sempre; corpo delle risposte solo se
l'esito non è «accessibile» (per gli accessibili si registra solo lo sha256 del corpo,
per non riempire il disco del server condiviso).
"""
from __future__ import annotations

import re
import time
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit

import requests
import urllib3

import piattaforme
import robots
from comune import UA_BOT, UA_BROWSER, salva_blob

urllib3.disable_warnings()
MAX_CORPO = 3_000_000
TIMEOUT = (10, 25)
MOTORI = {"*": "*", "Googlebot": "Googlebot", "Bingbot": "bingbot"}

# Firme di challenge/WAF riconoscibili: (nome, dove, regex)
FIRME = [
    ("Cloudflare challenge", "intest", r"cf-mitigated:\s*challenge"),
    ("Cloudflare challenge", "corpo", r"challenge-platform|cf-chl-|Just a moment\.\.\.|Attention Required! \| Cloudflare"),
    ("Imperva/Incapsula", "corpo", r"_Incapsula_Resource|Incapsula incident|Request unsuccessful\. Incapsula"),
    ("Imperva/Incapsula", "intest", r"x-iinfo:|x-cdn:\s*imperva"),
    ("Akamai", "corpo", r"Access Denied.{0,400}Reference&#32;#|errors\.edgesuite\.net"),
    ("Azure Application Gateway/Front Door", "corpo", r"Microsoft-Azure-Application-Gateway|The request is blocked\.|azurefd\.net/.{0,40}blocked"),
    ("F5 BIG-IP ASM", "corpo", r"The requested URL was rejected\. Please consult with your administrator"),
    ("Sucuri", "corpo", r"Sucuri WebSite Firewall"),
    ("AWS WAF", "corpo", r"awswaf|aws-waf-token"),
    ("Radware/ShieldSquare", "corpo", r"shieldsquare|perfdrive\.com|radware"),
    ("DDoS-Guard", "corpo", r"ddos-guard"),
    ("JS-challenge generica", "corpo", r"(?s)^.{0,3000}(enable javascript|abilita(re)? javascript).{0,2000}(challenge|verif|captcha)"),
    ("CAPTCHA", "corpo", r"g-recaptcha|hcaptcha\.com|turnstile|captcha-delivery"),
]


class _Link(HTMLParser):
    def __init__(self):
        super().__init__()
        self.link, self._href, self._txt = [], None, []

    def handle_starttag(self, tag, a):
        if tag == "a":
            self._href, self._txt = dict(a).get("href"), []

    def handle_data(self, d):
        if self._href is not None:
            self._txt.append(d)

    def handle_endtag(self, tag):
        if tag == "a" and self._href is not None:
            self.link.append((self._href, " ".join(self._txt).strip()))
            self._href = None


def link_at(html: str, base: str) -> str:
    p = _Link()
    try:
        p.feed(html or "")
    except Exception:
        pass
    # testo del link: «Amministrazione / Società / Ente / Azienda trasparente»; poi l'href; poi «Trasparenza» da solo
    cand = [h for h, t in p.link if h and re.search(r"(amministrazione|societ[aà]|ente|azienda)\s+trasparente", t, re.I)]
    cand += [h for h, t in p.link if h and re.search(r"(amministrazione|societa)[-_]?trasparente|/trasparenza(/|$|\?|\.)", h, re.I)]
    cand += [h for h, t in p.link if h and re.fullmatch(r"\s*trasparenza\s*", t, re.I)]
    for h in cand:
        u = urljoin(base, h.strip())
        if u.startswith("http"):
            return u
    return ""


def firme(r_status, intest: dict, corpo: str) -> list[str]:
    it = "\n".join(f"{k.lower()}: {v}" for k, v in intest.items())
    out = []
    for nome, dove, rx in FIRME:
        if re.search(rx, it if dove == "intest" else corpo[:200_000], re.I) and nome not in out:
            out.append(nome)
    # una pagina normale può includere reCAPTCHA in un modulo: conta solo se la risposta è un blocco
    if "CAPTCHA" in out and r_status == 200 and len(corpo) > 20_000:
        out.remove("CAPTCHA")
    if "JS-challenge generica" in out and len(corpo) > 30_000:
        out.remove("JS-challenge generica")
    return out


def noindex(intest: dict, corpo: str) -> list[str]:
    out = []
    for k, v in intest.items():
        if k.lower() == "x-robots-tag" and re.search(r"noindex|none", v, re.I):
            out.append(f"X-Robots-Tag: {v}")
    for m in re.finditer(r"<meta[^>]+>", corpo[:300_000], re.I):
        t = m.group(0)
        if re.search(r"name=[\"']?(robots|googlebot|bingbot)", t, re.I) and re.search(r"noindex|\bnone\b", t, re.I):
            out.append(t[:200])
    return out


def richiesta(sess, ritmo, url: str, ua: str, verify=True) -> dict:
    host = urlsplit(url).netloc.lower()
    t0 = time.monotonic()
    with ritmo(host):
        try:
            r = sess.get(url, headers={"User-Agent": ua, "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
                                       "Accept-Language": "it-IT,it;q=0.9"},
                         timeout=TIMEOUT, allow_redirects=True, stream=True, verify=verify)
            corpo = b""
            for ch in r.iter_content(65536):
                corpo += ch
                if len(corpo) > MAX_CORPO:
                    break
            r.close()
            # Redirect verso altri host: rispettano comunque il ritmo dell'host di partenza;
            # il successivo accesso all'host finale passa dal suo turno.
            return {"url": url, "ua": "bot" if ua == UA_BOT else "browser", "status": r.status_code,
                    "finale": r.url, "redirect": [h.headers.get("location", "") for h in r.history][:10],
                    "intest": dict(r.headers), "corpo": corpo, "secondi": round(time.monotonic() - t0, 2), "errore": ""}
        except requests.exceptions.SSLError as e:
            err = "tls: " + str(e)[:200]
        except requests.exceptions.ConnectionError as e:
            err = ("dns: " if "resolve" in str(e).lower() or "name or service" in str(e).lower() else "connessione: ") + str(e)[:200]
        except requests.exceptions.Timeout as e:
            err = "timeout: " + str(e)[:120]
        except Exception as e:  # noqa: BLE001
            err = f"{type(e).__name__}: {str(e)[:200]}"
        return {"url": url, "ua": "bot" if ua == UA_BOT else "browser", "status": None, "finale": "", "redirect": [],
                "intest": {}, "corpo": b"", "secondi": round(time.monotonic() - t0, 2), "errore": err}


def testo(r) -> str:
    return r["corpo"].decode("utf-8", "replace") if r["corpo"] else ""


def bloccata(r) -> bool:
    return r["status"] is None or r["status"] >= 400


def leggi_robots(sess, ritmo, base: str) -> dict:
    u = base.rstrip("/") + "/robots.txt"
    r = richiesta(sess, ritmo, u, UA_BOT)
    if r["errore"].startswith("tls"):
        r = richiesta(sess, ritmo, u, UA_BOT, verify=False)
    out = {"url": u, "status": r["status"], "errore": r["errore"], "sha256": "", "byte": len(r["corpo"])}
    if r["corpo"]:
        out["sha256"] = salva_blob(r["corpo"])
    if r["status"] and r["status"] < 300 and r["corpo"] and "html" not in r["intest"].get("Content-Type", "").lower():
        out["gruppi"] = robots.analizza(testo(r))
        out["stato"] = "presente"
    elif r["status"] and 400 <= r["status"] < 500:
        out["gruppi"], out["stato"] = {}, "assente (4xx: tutto consentito)"
    elif r["status"] and r["status"] < 400:
        out["gruppi"], out["stato"] = {}, "non valido (HTML o vuoto: tutto consentito)"
    else:
        out["gruppi"], out["stato"] = None, "irraggiungibile (5xx/errore: per RFC 9309 tutto vietato)"
    return out


def prova_ente(sess, ritmo, ente: dict) -> dict:
    d: dict = {"at_url": ente.get("at_url") or "", "at_provenienza": ente.get("at_provenienza") or "", "richieste": []}
    ev: list[dict] = []

    def log(r):
        d["richieste"].append({k: r[k] for k in ("url", "ua", "status", "finale", "secondi", "errore")} |
                              {"intest": {k: v for k, v in r["intest"].items()
                                          if k.lower() in ("server", "content-type", "x-robots-tag", "cf-ray", "cf-mitigated",
                                                           "x-powered-by", "x-generator", "location", "retry-after", "x-iinfo", "x-cdn")},
                               "redirect": r["redirect"]})
        ev.append(r)

    # 1. scoperta dell'URL AT se il registro ANAC non lo dà
    if not d["at_url"]:
        visti = set()
        # prima il sito istituzionale (IndicePA), poi la radice dell'host del file L.190
        for base, prov in ((ente.get("sito_ipa"), "home-sito-indicepa"), (_root(ente.get("url_l190")), "home-host-l190")):
            if not base or base.rstrip("/").lower() in visti:
                continue
            visti.add(base.rstrip("/").lower())
            r = richiesta(sess, ritmo, base, UA_BROWSER)
            if r["errore"].startswith("tls"):
                r = richiesta(sess, ritmo, base, UA_BROWSER, verify=False)
            log(r)
            if r["status"] and r["status"] < 400:
                tt = testo(r)
                u = link_at(tt, r["finale"] or base)
                if not u and re.search(r"<title[^>]*>[^<]*trasparen", tt, re.I):
                    u = r["finale"] or base  # la home stessa è il portale della trasparenza
                if u:
                    d["at_url"], d["at_provenienza"] = u, prov
                    break
            d.setdefault("home_errori", []).append(r["errore"] or (f"HTTP {r['status']}" if bloccata(r) else "home letta, nessun link"))
    if not d["at_url"]:
        err = d.get("home_errori", [])
        if not err:
            d["esito"], d["dettaglio_esito"] = "url non valido", "nessun URL: né registro ANAC né sito IndicePA"
        elif any(e == "home letta, nessun link" for e in err):
            d["esito"], d["dettaglio_esito"] = "sezione non individuata", "home letta ma nessun link riconoscibile alla sezione (registro ANAC senza percorso AT)"
        elif all(e.startswith("tls") for e in err):
            d["esito"], d["dettaglio_esito"] = "tls invalido", err[0]
        elif all(e.startswith(("dns", "connessione", "timeout", "tls", "HTTP 5")) for e in err):
            d["esito"], d["dettaglio_esito"] = "irraggiungibile", "; ".join(err)[:300]
        else:
            d["esito"], d["dettaglio_esito"] = "url non valido", "; ".join(err)[:300]
        return _fine(d, ev, None)

    at = d["at_url"]
    p = urlsplit(at)
    # 2. robots.txt dell'host della sezione
    rb = robots_in_cache(sess, ritmo, f"{p.scheme}://{p.netloc}")
    d["robots"] = {k: v for k, v in rb.items() if k != "gruppi"}
    percorsi = [p.path or "/"]
    if ente.get("url_l190") and urlsplit(ente["url_l190"].strip()).netloc.lower() == p.netloc.lower():
        q = urlsplit(ente["url_l190"].strip())
        percorsi.append(q.path + (("?" + q.query) if q.query else ""))
    blocchi = []
    if rb["gruppi"] is None:
        d["robots"]["verdetto"] = "robots irraggiungibile"
    else:
        for nome, ua in MOTORI.items():
            for pa in percorsi:
                ok, regola = robots.consentito(rb["gruppi"], ua, pa)
                if not ok:
                    blocchi.append({"agente": nome, "percorso": pa, "regola": regola})
        tutto = [ua for ua in MOTORI.values() if not robots.consentito(rb["gruppi"], ua, "/")[0]]
        d["robots"]["blocchi"] = blocchi
        d["robots"]["vieta_tutto_il_sito"] = tutto

    # 3. pagina AT con bot dichiarato e con browser identificato
    rbot = richiesta(sess, ritmo, at, UA_BOT)
    log(rbot)
    tls_ko = rbot["errore"].startswith("tls")
    rbro = richiesta(sess, ritmo, at, UA_BROWSER, verify=not tls_ko)
    log(rbro)
    if rbot["errore"] and not rbot["errore"].startswith(("tls", "dns")) and not bloccata(rbro):
        # errore di rete solo sul bot: si ripete una volta prima di attribuirlo a un filtro
        rbot = richiesta(sess, ritmo, at, UA_BOT)
        log(rbot)
    d["tls_valido"] = not tls_ko
    princ = rbro if not bloccata(rbro) else rbot
    corpo = testo(princ)
    d["firme_bot"] = firme(rbot["status"], rbot["intest"], testo(rbot)) if rbot["status"] else []
    d["firme_browser"] = firme(rbro["status"], rbro["intest"], testo(rbro)) if rbro["status"] else []
    d["noindex"] = noindex(princ["intest"], corpo) if not bloccata(princ) else []
    d["status_bot"], d["status_browser"] = rbot["status"], rbro["status"]
    d["finale"] = princ["finale"]
    d["piattaforma"] = piattaforme.riconosci(urlsplit(princ["finale"] or at).netloc, corpo, princ["intest"])
    d["titolo"] = (re.search(r"<title[^>]*>(.*?)</title>", corpo, re.I | re.S) or [None, ""])[1].strip()[:160] if corpo else ""

    # 4. classificazione
    if rbot["errore"].startswith(("InvalidURL", "MissingSchema", "InvalidSchema", "LocationParseError")):
        d["esito"], d["dettaglio_esito"] = "url non valido", rbot["errore"]
    elif rbot["errore"] and rbro["errore"] and not tls_ko:
        d["esito"], d["dettaglio_esito"] = "irraggiungibile", rbro["errore"]
    elif tls_ko and bloccata(rbro):
        d["esito"], d["dettaglio_esito"] = "tls invalido", rbot["errore"]
    elif d["firme_browser"] or d["firme_bot"] or (bloccata(rbot) and not bloccata(rbro)) or (
            rbro["status"] in (401, 403, 405, 406, 428, 429, 503) and rbot["status"] in (401, 403, 405, 406, 428, 429, 503)):
        motivi = sorted(set(d["firme_bot"] + d["firme_browser"]))
        if bloccata(rbot) and not bloccata(rbro):
            motivi.append(f"bot dichiarato respinto ({('HTTP ' + str(rbot['status'])) if rbot['status'] else rbot['errore'][:80]}), browser accettato")
        if not motivi:
            motivi.append(f"HTTP {rbot['status']}/{rbro['status']} tipico di blocco")
        d["esito"], d["dettaglio_esito"] = "bloccato da WAF/anti-bot", "; ".join(motivi)
        # 403/503 su entrambi senza firma: non si può distinguere da un sito rotto senza browser reale
        d["da_confermare_con_browser"] = not d["firme_browser"] and not d["firme_bot"] and bloccata(rbro)
    elif rbro["status"] in (404, 410) or (bloccata(rbro) and bloccata(rbot)):
        d["esito"], d["dettaglio_esito"] = ("url non valido" if rbro["status"] in (404, 410) else "irraggiungibile"), f"HTTP {rbro['status']}"
    elif blocchi:
        d["esito"], d["dettaglio_esito"] = "bloccato da robots.txt", "; ".join(f"{b['agente']} {b['percorso']} <- {b['regola']}" for b in blocchi[:4])
    elif d["noindex"]:
        d["esito"], d["dettaglio_esito"] = "noindex", d["noindex"][0]
    elif tls_ko:
        d["esito"], d["dettaglio_esito"] = "tls invalido", rbot["errore"]
    else:
        d["esito"], d["dettaglio_esito"] = "accessibile", ""
    # segnali secondari (un ente può averne più d'uno)
    d["segnali"] = sorted({s for s, c in (("robots", bool(blocchi)), ("noindex", bool(d["noindex"])),
                                            ("waf", bool(d["firme_bot"] or d["firme_browser"] or (bloccata(rbot) and not bloccata(rbro)))),
                                            ("tls", tls_ko)) if c})
    return _fine(d, ev, princ)


def _fine(d, ev, princ):
    tieni = d["esito"] != "accessibile"
    for r, rec in zip(ev, d["richieste"]):
        if r["corpo"]:
            import hashlib
            rec["sha256"] = salva_blob(r["corpo"]) if tieni else hashlib.sha256(r["corpo"]).hexdigest()
            rec["archiviato"] = tieni
            rec["byte"] = len(r["corpo"])
    return d


def _root(url: str | None) -> str:
    if not url or not re.match(r"^\s*https?://", url, re.I):
        return ""
    p = urlsplit(url.strip())
    return f"{p.scheme}://{p.netloc}/"


_ROBOTS: dict[str, dict] = {}
_ROBOTS_LK = __import__("threading").Lock()


def robots_in_cache(sess, ritmo, base: str) -> dict:
    """Un solo robots.txt per host e per esecuzione (molti enti condividono l'host della piattaforma)."""
    chiave = base.lower()
    with _ROBOTS_LK:
        if chiave in _ROBOTS:
            return _ROBOTS[chiave]
    rb = leggi_robots(sess, ritmo, base)
    with _ROBOTS_LK:
        _ROBOTS[chiave] = rb
    return rb
