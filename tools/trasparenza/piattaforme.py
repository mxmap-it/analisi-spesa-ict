"""Riconoscimento della piattaforma del portale (solo se certo; altrimenti «ignota»).

Ogni regola ha un nome, un tipo di prova e un'espressione. Tipi di prova:
- host: il dominio della pagina AT (dopo i redirect) è del fornitore o del servizio;
- generator: <meta name="generator"> o intestazione X-Powered-By/X-Generator dichiarata;
- dichiarazione: il fornitore è nominato in un credito («realizzato da», «powered by», copyright)
  o in un percorso di asset riservato al prodotto.
Le regole sono ordinate: vince la prima. Gli «indizi» (temi, percorsi generici come /L190/)
si registrano a parte e NON diventano piattaforma.
"""
from __future__ import annotations

import re

REGOLE: list[tuple[str, str, str]] = [
    # (piattaforma, prova, regex)
    ("DigitalPA (portaletrasparenza.net)", "host", r"(^|\.)portaletrasparenza\.net$"),
    ("Halley Informatica", "host", r"(^|\.)(halleyweb\.com|halleysac\.it|halleysardegna\.com|halley\w*\.it)$"),
    ("ComuneWeb (comuneweb.it)", "host", r"(^|\.)comuneweb\.it$"),
    ("trasparenza-valutazione-merito.it", "host", r"(^|\.)trasparenza-valutazione-merito\.it$"),
    ("Soluzioni PA (soluzionipa.it)", "host", r"(^|\.)soluzionipa\.it$"),
    ("Maggioli (maggiolicloud.it)", "host", r"(^|\.)maggiolicloud\.it$"),
    ("traspare.com", "host", r"(^|\.)traspare\.com$"),
    ("trasparenza-pa.net", "host", r"(^|\.)trasparenza-pa\.net$"),
    ("ISWEB", "dichiarazione", r"isweb\s*s\.?p\.?a|pa33\b|www\.isweb\.it"),
    ("Maggioli JCityGov", "dichiarazione", r"jcitygov"),
    ("Halley Informatica", "dichiarazione", r"halley\s*informatica|halleyweb"),
    ("DigitalPA", "dichiarazione", r"digitalpa\.it|digital\s*pa\s*s\.r\.l"),
    ("Netribe on.Cube", "dichiarazione", r"netribe|on\.cube"),
    ("Dedagroup", "dichiarazione", r"dedagroup"),
    ("APKappa", "dichiarazione", r"apkappa"),
    ("Municipium", "dichiarazione", r"municipium-images|municipiumapp|municipium\.it"),
    ("Grafiche E. Gaspari", "dichiarazione", r"grafiche\s*e\.?\s*gaspari|gasparionline"),
    ("Studio K", "dichiarazione", r"studiok\.it|studio\s*k\s*s\.r\.l"),
    ("Liferay", "generator", r"liferay"),
    ("WordPress", "generator", r"wordpress"),
    ("Drupal", "generator", r"drupal"),
    ("Joomla", "generator", r"joomla"),
    ("Plone", "generator", r"plone"),
    ("TYPO3", "generator", r"typo3"),
]

INDIZI = [
    ("percorso /L190/", r"/L190/"),
    ("tema Bootstrap Italia", r"bootstrap-italia"),
    ("modello Comuni (Designers Italia)", r"design-comuni|comuni-italia"),
    ("wp-content", r"/wp-content/"),
]


def _generator(html: str, intest: dict) -> str:
    m = re.findall(r"<meta[^>]+name=[\"']generator[\"'][^>]*content=[\"']([^\"']+)", html, re.I)
    m += re.findall(r"<meta[^>]+content=[\"']([^\"']+)[\"'][^>]*name=[\"']generator", html, re.I)
    for k in ("x-powered-by", "x-generator", "liferay-portal"):
        if k in intest:
            m.append(f"{k}: {intest[k]}")
    return " | ".join(m)


def riconosci(host: str, html: str, intest: dict) -> dict:
    host = (host or "").lower()
    intest = {k.lower(): v for k, v in (intest or {}).items()}
    gen = _generator(html or "", intest)
    basso = (html or "")[:600_000].lower()
    for nome, prova, rx in REGOLE:
        testo = {"host": host, "generator": gen.lower(), "dichiarazione": basso}[prova]
        m = re.search(rx, testo, re.I)
        if m:
            return {"piattaforma": nome, "prova": prova, "corrispondenza": m.group(0)[:80], "generator": gen,
                    "indizi": _indizi(html)}
    return {"piattaforma": "ignota", "prova": "", "corrispondenza": "", "generator": gen, "indizi": _indizi(html)}


def _indizi(html: str) -> str:
    return ";".join(n for n, rx in INDIZI if re.search(rx, html or "", re.I))
