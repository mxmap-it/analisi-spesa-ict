"""Parser robots.txt secondo RFC 9309: gruppi per user-agent, corrispondenza più lunga,
Allow vince a parità, caratteri * e $. (urllib.robotparser usa la prima regola che corrisponde
e ignora i caratteri jolly: darebbe esiti diversi da quelli di Google.)"""
from __future__ import annotations

import re
from urllib.parse import unquote


def analizza(testo: str) -> dict[str, list[tuple[bool, str]]]:
    gruppi: dict[str, list[tuple[bool, str]]] = {}
    agenti: list[str] = []
    in_regole = False
    for riga in testo.splitlines():
        riga = riga.split("#", 1)[0].strip()
        if ":" not in riga:
            continue
        k, v = (x.strip() for x in riga.split(":", 1))
        k = k.lower()
        if k == "user-agent":
            if in_regole:
                agenti, in_regole = [], False
            agenti.append(v.lower())
            for a in agenti:
                gruppi.setdefault(a, [])
        elif k in ("allow", "disallow"):
            in_regole = True
            for a in agenti:
                gruppi.setdefault(a, []).append((k == "allow", v))
    return gruppi


def _regex(pat: str) -> re.Pattern:
    fine = pat.endswith("$")
    if fine:
        pat = pat[:-1]
    r = "".join(".*" if ch == "*" else re.escape(ch) for ch in unquote(pat))
    return re.compile(r + ("$" if fine else ""))


def regole_per(gruppi, agente: str):
    a = agente.lower()
    # Gruppo più specifico: nome del prodotto contenuto (es. «googlebot»), altrimenti «*».
    for nome, regole in gruppi.items():
        if nome != "*" and nome and nome in a:
            return nome, regole
    return ("*", gruppi["*"]) if "*" in gruppi else (None, [])


def consentito(gruppi, agente: str, percorso: str) -> tuple[bool, str]:
    """(consentito, regola che decide)."""
    nome, regole = regole_per(gruppi, agente)
    percorso = unquote(percorso or "/")
    migliore, lung, ok = "", -1, True
    for allow, pat in regole:
        if pat == "":
            continue  # «Disallow:» vuoto = nessun divieto
        if _regex(pat).match(percorso):
            l = len(pat)
            if l > lung or (l == lung and allow):
                migliore, lung, ok = f"{'Allow' if allow else 'Disallow'}: {pat} [{nome}]", l, allow
    return ok, migliore
