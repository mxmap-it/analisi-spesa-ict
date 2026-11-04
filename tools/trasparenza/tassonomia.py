"""Tassonomia dei blocchi per identità del client e conferma dei blocchi (metodo 1.1.0).

Identità valutate SOLO nelle regole di robots.txt (mai impersonate nelle richieste): Googlebot, Bingbot, crawler AI.
Identità usate nelle richieste reali (oneste): bot del progetto, python-requests e curl con UA di default,
UA da browser con l'URL del progetto, browser reale (Chromium). Due origini: server (datacenter) e desktop (residenziale).
"""
from __future__ import annotations

import calendar
import time

import robots

ROBOTS_IDENTITA = {
    "tutti (*)": "*", "bot del progetto": "analisi-spesa-ict-trasparenza", "Googlebot": "Googlebot", "Bingbot": "bingbot",
    "GPTBot": "GPTBot", "ClaudeBot": "ClaudeBot", "CCBot": "CCBot", "Google-Extended": "Google-Extended",
    "PerplexityBot": "PerplexityBot", "curl": "curl", "Wget": "Wget", "python-requests": "python-requests",
}
MOTORI = {"tutti (*)", "Googlebot", "Bingbot"}  # rilevanti per l'art. 9 (motori di ricerca)
HTTP_ONESTE = ("bot-progetto", "python-requests", "curl", "browser-ua")
DISTANZA_CONFERMA = 3600  # secondi minimi fra due giri di conferma


def robots_negati(testo: str | None, percorso: str) -> list[str]:
    if testo is None:
        return []
    g = robots.analizza(testo)
    return [nome for nome, ua in ROBOTS_IDENTITA.items() if not robots.consentito(g, ua, percorso or "/")[0]]


def fallito(t: dict) -> bool:
    return bool(t.get("errore")) or (t.get("status") or 0) >= 400 or bool(t.get("vendor_blocco"))


def _sec(ts: str) -> float:
    return calendar.timegm(time.strptime(ts, "%Y-%m-%dT%H:%M:%SZ"))


def respinto(t: dict) -> bool:
    """Risposta HTTP di rifiuto o pagina di blocco riconosciuta (non errori di rete o di TLS del client)."""
    return (t.get("status") or 0) >= 400 or bool(t.get("vendor_blocco"))


def per_identita(tentativi: list[dict], criterio=None) -> dict[str, dict]:
    """identità -> {'giri': {n: bloccato}, 'sempre': bool, 'mai': bool}"""
    out: dict[str, dict] = {}
    for t in tentativi:
        if t.get("interferenza_locale"):
            continue  # pagina dell'antivirus dell'osservatore (es. desktop con Bitdefender): non è una misura del sito
        i = t.get("identita") or ("browser-reale" if t.get("tipo") == "browser" else "bot-progetto")
        g = t.get("giro_conferma") or 1
        o = out.setdefault(i, {"giri": {}, "ts": {}})
        o["giri"][g] = (criterio or fallito)(t)
        o["ts"][g] = t["ts"]
    for o in out.values():
        o["sempre"] = all(o["giri"].values())
        o["mai"] = not any(o["giri"].values())
    return out


def classifica(srv: list[dict], dsk: list[dict], negati: list[str]) -> dict:
    mecc, note = [], []
    if any(n in MOTORI for n in negati):
        mecc.append("robots.txt (motori di ricerca)")
    elif negati:
        mecc.append("robots.txt (solo crawler AI o altri client)")
    ids_s, ids_d = per_identita(srv), per_identita(dsk)
    # per il «WAF per identità» contano solo i rifiuti HTTP: un errore di TLS di curl non è un filtro del sito
    rs = per_identita(srv, respinto)
    bl_s = sorted(i for i, o in rs.items() if o["sempre"])
    bl_d = sorted(i for i, o in per_identita(dsk, respinto).items() if o["sempre"])
    ok_s = [i for i, o in ids_s.items() if o["mai"]]
    tutti = [t for t in srv + dsk if not t.get("interferenza_locale")]
    if tutti and all(not t.get("status") and t.get("errore") for t in tutti):
        mecc.append("nessuna risposta (DNS, connessione o TLS)")
    solo_transitori = bool(tutti) and all((not fallito(t)) or t.get("transitorio") for t in tutti) and any(fallito(t) for t in tutti)
    if bl_s and ok_s:
        mecc.append("WAF per User-Agent/identità")
    if ids_s and not ok_s and ids_d and any(o["mai"] for o in ids_d.values()):
        mecc.append("WAF per IP/ASN (datacenter)")
    risposte = any((t.get("status") or 0) >= 400 or t.get("vendor_blocco") for t in tutti)
    if ids_s and not ok_s and risposte and (not ids_d or not any(o["mai"] for o in ids_d.values())):
        mecc.append("nessun client accettato (blocco totale o sito guasto)")
    if any(t.get("challenge_js") and fallito(t) for t in tutti):
        mecc.append("challenge JS")
    if any(t.get("captcha") for t in tutti):
        mecc.append("CAPTCHA")
    if solo_transitori:
        mecc = [m for m in mecc if m.startswith("robots")] + ["errore transitorio"]
    # conferma: stesso blocco in almeno due giri di conferma distanti >= 1 h (lato server)
    giri = sorted({t.get("giro_conferma") or 1 for t in srv})
    conferma = ""
    if srv:
        bloccato_per_giro = {g: any(fallito(t) and not t.get("transitorio") for t in srv if (t.get("giro_conferma") or 1) == g) for g in giri}
        if len(giri) >= 2:
            ts = {g: max(t["ts"] for t in srv if (t.get("giro_conferma") or 1) == g) for g in giri}
            distanti = _sec(ts[giri[-1]]) - _sec(ts[giri[0]]) >= DISTANZA_CONFERMA
            if all(bloccato_per_giro.values()) and distanti:
                conferma = "confermato"
            elif not bloccato_per_giro[giri[-1]]:
                conferma = "non riprodotto"
            else:
                conferma = "da confermare"
        else:
            conferma = "da confermare" if bloccato_per_giro.get(giri[0]) else "non riprodotto"
    if bl_s and bl_d is not None:
        note.append(f"server: {', '.join(bl_s)}")
    if bl_d:
        note.append(f"desktop: {', '.join(bl_d)}")
    return {"meccanismi": mecc, "identita_bloccate": " | ".join(note), "conferma": conferma, "giri_conferma": len(giri),
            "robots_negati": negati}
