"""Diagnostica estesa e caratterizzazione delle sezioni (fase 2, metodo 1.1.0, #61).

Due punti di osservazione, stesso codice:
- origine «server» (datacenter): sul server del progetto;
- origine «desktop» (residenziale): sul portatile di Fabio, `--origine desktop`.
Ogni tentativo registra origine, IP pubblico e ASN (api.ipify.org + RIPEstat), data e ora UTC, client e versione,
User-Agent, DNS (A/AAAA/alias CNAME dal resolver di sistema), TLS (versione, certificato, emittente, scadenza,
errore), catena dei redirect con intestazioni complete, dimensione/hash/primi kB del corpo, vendor del blocco e
regola, challenge JS/CAPTCHA, tempi. Per ogni tentativo fallito si conserva un log grezzo (dump HTTP o HAR del
browser) nell'archivio content-addressed: il suo sha256 è nell'open data.

Nessun plugin di occultamento dell'impronta, nessun CAPTCHA risolto, nessuna rotazione di IP o proxy.
"""
from __future__ import annotations

import hashlib
import json
import platform
import re
import socket
import ssl
import time
from pathlib import Path
from urllib.parse import urljoin, urlsplit

import requests
import urllib3

import sonda
from comune import LAVORO, UA_BOT, UA_BROWSER, adesso, salva_blob

urllib3.disable_warnings()
PRIMI_KB = 2048

# Segni di CDN/WAF nelle intestazioni e negli alias DNS (presenza, non blocco)
CDN = [
    ("Cloudflare", r"(^|\n)(server: cloudflare|cf-ray:)|\.cdn\.cloudflare\.net"),
    ("Akamai", r"(^|\n)(server: akamaighost|x-akamai-[\w-]+:|akamai-grn:)|\.(edgekey|edgesuite|akamaiedge|akamaized)\.net"),
    ("Imperva/Incapsula", r"(^|\n)(x-iinfo:|x-cdn: imperva)|\.incapdns\.net"),
    ("Azure Front Door/App Gateway", r"(^|\n)(x-azure-ref:|server: microsoft-azure-application-gateway)|\.azurefd\.net|\.trafficmanager\.net"),
    ("AWS CloudFront", r"(^|\n)(x-amz-cf-id:|via: [^\n]*cloudfront)|\.cloudfront\.net"),
    ("Sucuri", r"(^|\n)(x-sucuri-id:|server: sucuri)|sucuri\.net"),
    ("Fastly", r"(^|\n)(x-served-by: cache-|via: [^\n]*varnish[^\n]*fastly)|\.fastly\.net"),
    ("F5 BIG-IP", r"(^|\n)(server: big-?ip|set-cookie: (bigipserver|ts0[0-9a-f]{6}))"),
    ("Seeweb", r"seeweb"),
]

_ORIGINE: dict = {}


def origine(nome: str) -> dict:
    """IP pubblico e ASN dell'osservatore (una volta per processo)."""
    if _ORIGINE.get("origine") == nome:
        return _ORIGINE
    o = {"origine": nome, "ip": "", "asn": "", "asn_nome": "", "host": platform.node(),
         "sistema": f"{platform.system()} {platform.release()}", "python": platform.python_version(),
         "requests": requests.__version__}
    try:
        o["ip"] = requests.get("https://api.ipify.org?format=json", timeout=20).json()["ip"]
        ni = requests.get(f"https://stat.ripe.net/data/network-info/data.json?resource={o['ip']}", timeout=30).json()
        asn = (ni["data"].get("asns") or [""])[0]
        o["asn"] = f"AS{asn}" if asn else ""
        if asn:
            ov = requests.get(f"https://stat.ripe.net/data/as-overview/data.json?resource=AS{asn}", timeout=30).json()
            o["asn_nome"] = ov["data"].get("holder", "")
    except Exception as e:  # noqa: BLE001
        o["errore_origine"] = str(e)[:200]
    _ORIGINE.clear()
    _ORIGINE.update(o)
    return o


def dns(host: str) -> dict:
    out = {"host": host, "a": [], "aaaa": [], "alias": [], "canonico": "", "errore": ""}
    try:
        can, alias, _ = socket.gethostbyname_ex(host)
        out["canonico"], out["alias"] = can, alias
    except Exception as e:  # noqa: BLE001
        out["errore"] = f"{type(e).__name__}: {e}"[:200]
    for fam, k in ((socket.AF_INET, "a"), (socket.AF_INET6, "aaaa")):
        try:
            out[k] = sorted({x[4][0] for x in socket.getaddrinfo(host, 443, fam, socket.SOCK_STREAM)})
        except Exception:  # noqa: BLE001
            pass
    return out


def tls(host: str, porta: int = 443) -> dict:
    out = {"host": host, "valido": None, "errore": ""}
    t0 = time.monotonic()
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, porta), timeout=10) as s, ctx.wrap_socket(s, server_hostname=host) as ss:
            c = ss.getpeercert()
            der = ss.getpeercert(binary_form=True)
            out |= {"valido": True, "versione": ss.version(), "cifrario": ss.cipher()[0],
                    "soggetto": dict(x[0] for x in c.get("subject", [])).get("commonName", ""),
                    "emittente": " / ".join(v for k, v in (x[0] for x in c.get("issuer", [])) if k in ("organizationName", "commonName")),
                    "scadenza": c.get("notAfter", ""), "inizio": c.get("notBefore", ""),
                    "san": [v for k, v in c.get("subjectAltName", [])][:20], "sha256_cert": hashlib.sha256(der).hexdigest()}
    except ssl.SSLCertVerificationError as e:
        out |= {"valido": False, "errore": f"verifica: {e.verify_message} ({e.verify_code})"}
        try:  # si legge comunque il certificato presentato, senza fidarsene
            ctx = ssl.create_default_context()
            ctx.check_hostname, ctx.verify_mode = False, ssl.CERT_NONE
            with socket.create_connection((host, porta), timeout=10) as s, ctx.wrap_socket(s, server_hostname=host) as ss:
                out |= {"versione": ss.version(), "sha256_cert": hashlib.sha256(ss.getpeercert(binary_form=True)).hexdigest()}
        except Exception:  # noqa: BLE001
            pass
    except Exception as e:  # noqa: BLE001
        out |= {"valido": False, "errore": f"{type(e).__name__}: {e}"[:200]}
    out["tipo_errore"] = tipo_errore_tls(out["errore"])
    out["secondi"] = round(time.monotonic() - t0, 2)
    return out


def riconosci_blocco(status, intest: dict, corpo: str, alias: list[str]) -> dict:
    it = "\n".join(f"{k.lower()}: {v}" for k, v in intest.items())
    vendor = [(n, rx) for n, dove, rx in sonda.FIRME
              if re.search(rx, it if dove == "intest" else corpo[:200_000], re.I)]
    if status == 200 and len(corpo) > 20_000:
        vendor = [v for v in vendor if v[0] not in ("CAPTCHA", "JS-challenge generica")]
    cdn = [(n, rx) for n, rx in CDN if re.search(rx, (it + "\n" + "\n".join(alias)).lower(), re.I)]
    return {"vendor_blocco": [v[0] for v in vendor], "regole_blocco": [v[1] for v in vendor],
            "cdn": [c[0] for c in cdn], "regole_cdn": [c[1] for c in cdn],
            "captcha": any(v[0] == "CAPTCHA" for v in vendor),
            "challenge_js": any(v[0] in ("JS-challenge generica", "Cloudflare challenge", "Imperva/Incapsula", "AWS WAF")
                                for v in vendor) or bool(re.search(r"document\.cookie.{0,200}location\.(reload|href)", corpo[:20000], re.S))}


def tentativo_http(url: str, ua: str, alias: list[str], verify=True, max_hop=10) -> dict:
    """Redirect seguiti a mano: per ogni passo stato e intestazioni complete."""
    catena, t0, sess = [], time.monotonic(), requests.Session()
    u, r, err, corpo = url, None, "", b""
    try:
        for _ in range(max_hop):
            t1 = time.monotonic()
            r = sess.get(u, headers={"User-Agent": ua, "Accept": "text/html,*/*;q=0.8", "Accept-Language": "it-IT,it;q=0.9"},
                         timeout=(10, 25), allow_redirects=False, stream=True, verify=verify)
            corpo = r.raw.read(3_000_000, decode_content=True) or b""
            catena.append({"url": u, "status": r.status_code, "intestazioni": dict(r.headers),
                           "secondi": round(time.monotonic() - t1, 2), "http": f"HTTP/{r.raw.version / 10:.1f}" if r.raw.version else ""})
            if r.is_redirect and r.headers.get("location"):
                u = urljoin(u, r.headers["location"])
                continue
            break
    except Exception as e:  # noqa: BLE001
        err = f"{type(e).__name__}: {e}"[:300]
    testo = corpo.decode("utf-8", "replace")
    ultimo = catena[-1] if catena else {"status": None, "intestazioni": {}}
    d = {"client": f"python-requests/{requests.__version__}", "user_agent": ua, "url": url, "catena": catena,
         "url_finale": catena[-1]["url"] if catena else "", "status": ultimo["status"], "errore": err,
         "byte": len(corpo), "sha256_corpo": hashlib.sha256(corpo).hexdigest() if corpo else "",
         "primi_kb": testo[:PRIMI_KB], "secondi": round(time.monotonic() - t0, 2)}
    d |= riconosci_blocco(ultimo["status"], ultimo["intestazioni"], testo, alias)
    if err or (ultimo["status"] or 0) >= 400 or d["vendor_blocco"]:
        dump = [f"# origine {_ORIGINE.get('origine')} ip {_ORIGINE.get('ip')} {_ORIGINE.get('asn')} — {adesso()}",
                f"# User-Agent: {ua}"]
        for h in catena:
            dump += [f"\n>>> GET {h['url']}", f"<<< {h['http']} {h['status']}"] + [f"{k}: {v}" for k, v in h["intestazioni"].items()]
        if err:
            dump.append(f"\n!!! errore: {err}")
        grezzo = ("\n".join(dump) + "\n\n" + testo).encode("utf-8")
        d["grezzo_sha256"], d["grezzo_tipo"] = salva_blob(grezzo), "dump-http"
    return d


def tentativo_browser(pw, url: str, headed: bool, canale: str | None = None) -> dict:
    har = LAVORO / "har" / f"{hashlib.sha1((url + adesso()).encode()).hexdigest()}.har"
    har.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.monotonic()
    br = pw.chromium.launch(headless=not headed, channel=canale) if canale else pw.chromium.launch(headless=not headed)
    ctx = br.new_context(user_agent=None, locale="it-IT", record_har_path=str(har), record_har_content="embed")
    ua_reale = ""
    d = {"client": f"playwright-chromium/{br.version}" + (" (headed)" if headed else " (headless)") + (f" canale {canale}" if canale else ""), "url": url}
    try:
        pg = ctx.new_page()
        ua_reale = pg.evaluate("navigator.userAgent")
        resp = pg.goto(url, timeout=45000, wait_until="domcontentloaded")
        pg.wait_for_timeout(8000)  # una JS-challenge non interattiva si completa da sola; nessun CAPTCHA si risolve
        html = pg.content()
        intest = resp.all_headers() if resp else {}
        d |= {"status": resp.status if resp else None, "url_finale": pg.url, "titolo": pg.title()[:160],
              "intestazioni": intest, "byte": len(html.encode()), "sha256_corpo": hashlib.sha256(html.encode()).hexdigest(),
              "primi_kb": html[:PRIMI_KB], "errore": ""}
        d |= riconosci_blocco(d["status"], intest, html, [])
    except Exception as e:  # noqa: BLE001
        d |= {"status": None, "errore": f"{type(e).__name__}: {e}"[:300]}
    finally:
        ctx.close()
        br.close()
    d["user_agent"] = ua_reale  # UA standard del browser: nessuna falsificazione
    d["secondi"] = round(time.monotonic() - t0, 2)
    if har.exists():
        if d.get("errore") or (d.get("status") or 0) >= 400 or d.get("vendor_blocco"):
            d["grezzo_sha256"], d["grezzo_tipo"] = salva_blob(har.read_bytes()), "har"
        har.unlink()
    return d


def diagnostica(ente: dict, nome_origine: str, browser=True, headed=False, canale=None, pw=None) -> list[dict]:
    """Tutti i tentativi su un ente: HTTP bot, HTTP browser-UA, browser reale."""
    at = ente.get("at_url") or ente.get("sito_ipa")
    if not at or "://" not in at:
        return []
    o = origine(nome_origine)
    host = urlsplit(at).hostname or ""
    dn = dns(host)
    tl = tls(host) if at.startswith("https") else {"host": host, "valido": None, "errore": "http senza TLS"}
    comune = {"cf": ente["cf"], "origine": o["origine"], "ip": o["ip"], "asn": o["asn"], "asn_nome": o["asn_nome"],
              "osservatore": {k: o[k] for k in ("host", "sistema", "python")}, "dns": dn, "tls": tl, "metodo": "1.1.0-sperimentale"}
    alias = dn["alias"] + [dn["canonico"]]
    out = []
    for ua in (UA_BOT, UA_BROWSER):
        out.append(comune | {"ts": adesso(), "tipo": "http"} | tentativo_http(at, ua, alias, verify=tl.get("valido") is not False))
        time.sleep(5)
    if browser and pw is not None:
        out.append(comune | {"ts": adesso(), "tipo": "browser"} | tentativo_browser(pw, at, headed, canale))
        time.sleep(5)
    return out


# --- caratterizzazione: due vie e ricercabilità -------------------------------------------------

def _norm(u: str) -> str:
    p = urlsplit(u or "")
    return (p.netloc.lower().removeprefix("www.") + p.path.rstrip("/").lower())


CAMPI_RICERCA = ("input[type=search]", "input[name=q]", "input[name=s]", "input[name=search]", "input[name=cerca]",
                 "input[name=ricerca]", "input[name=keyword]", "input[name=keywords]", "input[name=testo]",
                 "input[name*=search i]", "input[name*=cerca i]", "input[placeholder*=cerca i]", "input[aria-label*=cerca i]")


def _cerca(pg, termine: str) -> dict:
    for sel in CAMPI_RICERCA:
        loc = pg.locator(sel)
        if loc.count() and loc.first.is_visible():
            prima = pg.url
            loc.first.fill(termine)
            loc.first.press("Enter")
            try:
                pg.wait_for_load_state("domcontentloaded", timeout=20000)
            except Exception:  # noqa: BLE001
                pass
            pg.wait_for_timeout(4000)
            html = pg.content()
            return {"selettore": sel, "query": termine, "url_risultati": pg.url, "url_partenza": prima,
                    "trovato": termine.lower() in re.sub(r"<[^>]+>", " ", html).lower().replace(f'value="{termine.lower()}"', ""),
                    "byte": len(html), "sha256": salva_blob(html.encode()), "estratto": _intorno(html, termine)}
    return {}


def _intorno(html: str, t: str) -> str:
    s = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))
    i = s.lower().find(t.lower())
    return s[max(0, i - 150): i + 150] if i >= 0 else s[:300]


def classifica_ricerca(r_cig: dict, r_banale: dict) -> str:
    if not r_cig:
        return "ricerca assente"
    if r_cig.get("errore") or (r_banale and not r_banale.get("trovato")):
        return "ricerca non funzionante"
    return "trovato" if r_cig.get("trovato") else "non trovato"


def caratterizza(pw, ente: dict, cig: str, headed=False) -> dict:
    out = {"cf": ente["cf"], "ts": adesso(), "via_anac": ente.get("at_url_anac") or "", "via_home": "", "percorso_home": [],
           "cig_test": cig}
    br = pw.chromium.launch(headless=not headed)
    ctx = br.new_context(locale="it-IT")
    pg = ctx.new_page()
    try:
        if ente.get("sito_ipa"):
            pg.goto(ente["sito_ipa"], timeout=45000, wait_until="domcontentloaded")
            pg.wait_for_timeout(3000)
            out["percorso_home"].append(pg.url)
            link = sonda.link_at(pg.content(), pg.url)
            if link:
                time.sleep(5)
                pg.goto(link, timeout=45000, wait_until="domcontentloaded")
                pg.wait_for_timeout(3000)
                out["percorso_home"] += [link, pg.url]
                out["via_home"] = pg.url
        if not out["via_home"] and out["via_anac"]:
            time.sleep(5)
            pg.goto(out["via_anac"], timeout=45000, wait_until="domcontentloaded")
            pg.wait_for_timeout(3000)
        out["coincidono"] = bool(out["via_anac"] and out["via_home"]) and _norm(out["via_anac"]) == _norm(out["via_home"])
        out["sezione_usata"] = pg.url
        base = pg.url
        r_cig = _cerca(pg, cig) if cig else {}
        r_ban = {}
        if r_cig:
            time.sleep(5)
            pg.goto(base, timeout=45000, wait_until="domcontentloaded")
            pg.wait_for_timeout(2000)
            r_ban = _cerca(pg, "determina")
        out |= {"ricerca_cig": r_cig, "ricerca_banale": r_ban, "ricercabilita": classifica_ricerca(r_cig, r_ban) if cig else "nessun CIG di test"}
    except Exception as e:  # noqa: BLE001
        out["errore"] = f"{type(e).__name__}: {e}"[:300]
        out.setdefault("ricercabilita", "non verificata (errore di navigazione)")
    finally:
        br.close()
    return out


def esporta_pacchetto(righe: list[dict], dest: Path):
    """Pacchetto portabile dal desktop al server: tentativi.jsonl + blobs/ dei log grezzi."""
    from comune import ARCHIVIO
    (dest / "blobs").mkdir(parents=True, exist_ok=True)
    with (dest / "tentativi.jsonl").open("a", encoding="utf-8") as fh:
        for r in righe:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            for k in ("grezzo_sha256",):
                s = r.get(k)
                if s:
                    src = ARCHIVIO / "blobs" / "sha256" / s[:2] / s[2:4] / s
                    if src.exists():
                        (dest / "blobs" / s).write_bytes(src.read_bytes())


def tipo_errore_tls(errore: str) -> str:
    e = (errore or "").lower()
    for chiave, tipo in (("unable to get local issuer", "catena incompleta o CA sconosciuta"),
                         ("expired", "certificato scaduto"), ("not yet valid", "certificato non ancora valido"),
                         ("hostname mismatch", "nome non corrispondente"), ("doesn't match", "nome non corrispondente"),
                         ("self-signed", "certificato autofirmato"), ("self signed", "certificato autofirmato"),
                         ("wrong version number", "porta 443 senza TLS"), ("handshake", "handshake fallito"),
                         ("unsupported protocol", "protocollo obsoleto")):
        if chiave in e:
            return tipo
    return "altro" if e else ""
