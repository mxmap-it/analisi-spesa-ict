#!/usr/bin/env python3
"""Pagina «Raccomandazioni» del sito dal registro report/metodo/richieste-e-raccomandazioni.yaml.

Uso:
  .venv/bin/python tools/raccomandazioni_pagina.py            # controllo + pagina + CSV/JSON
  .venv/bin/python tools/raccomandazioni_pagina.py --verifica # solo controllo (exit 1 se mancano campi obbligatori)

Il registro NON viene modificato: destinatari, temi, stato e data sono normalizzati qui, in modo
deterministico (parole chiave), e i campi che mancano vengono elencati come «da completare».
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parent.parent
YAML = BASE / "report/metodo/richieste-e-raccomandazioni.yaml"
PAGINA = BASE / "sito/content/progetto/raccomandazioni.md"
DATI = BASE / "sito/static/dati"
REPO = "https://github.com/mxmap-it/analisi-spesa-ict/blob/main/"
TICKET = "https://github.com/mxmap-it/analisi-spesa-ict/issues/"

OBBLIGATORI = ["id", "destinatario", "tipo", "stato", "titolo", "richiesta", "rif"]

# destinatario normalizzato: (etichetta, espressione sul testo libero del campo)
DESTINATARI = [
    ("ANAC", r"\bANAC\b"),
    ("ACN", r"\bACN\b"),
    ("AgID", r"\bAgID\b"),
    ("DTD", r"\bDTD\b|trasformazione digitale"),
    ("Consip", r"\bConsip\b"),
    ("PSN", r"\bPSN\b|Polo Strategico"),
    ("MEF-RGS / BDAP / Sogei", r"MEF|RGS|BDAP|Sogei|Italia Domani"),
    ("IndicePA", r"IndicePA"),
    ("Centrali di committenza / soggetti aggregatori", r"centrali di committenza|soggetti aggregatori"),
    ("Gestori piattaforme e-procurement", r"piattaform"),
    ("Enti e stazioni appaltanti", r"\benti\b|stazioni appaltanti|amministrazioni|EAV|ASL|ICE|in-house|in house|PagoPA"),
    ("Legislatore / Funzione pubblica", r"legislat|Funzione pubblica|\bDFP\b"),
    ("Commissione europea / UE", r"Commissione europea|Ufficio delle pubblicazioni"),
    ("Registro imprese / GLEIF", r"InfoCamere|GLEIF"),
    ("Interno (progetto)", r"interno"),
]

# tema: (etichetta, espressione su titolo + richiesta + perche_serve)
TEMI = [
    ("Trasparenza art. 9 / Amministrazione trasparente", r"trasparen|art\. ?9|Amministrazione trasparente|\bAT\b|robots|WAF|RPCT|OIV"),
    ("Accesso civico", r"accesso civico|FOIA"),
    ("Cloud, ACN e PSN", r"cloud|\bACN\b|\bPSN\b|qualificat|SaaS|IaaS|data ?center"),
    ("Convenzioni e accordi quadro", r"accordo quadro|accordi quadro|\bAQ\b|convenzion|Consip|MePA|attuativ"),
    ("Classificazione (CPV, prodotto, ICT)", r"\bCPV\b|prodotto|classific|ICT"),
    ("Qualità del dato", r"vuot|valid|errat|duplic|non compilat|incoeren|formato|minuscol|segnaposto|codice fiscale|partita IVA|P\.? ?IVA"),
    ("Dati aperti e accesso ai dataset", r"open ?data|dataset|download|delta|API|bulk|OCDS|eForms|licenz|pubblicare"),
    ("Spesa e bilancio (BDAP, SIOPE, PNRR)", r"BDAP|SIOPE|bilancio|PNRR|Italia Domani|pagament|liquidat|mandat"),
]

DATA_RE = re.compile(r"\b(\d{1,2})/(\d{1,2})/(20\d\d)\b")


def carica() -> list[dict]:
    return yaml.safe_load(YAML.read_text(encoding="utf-8")) or []


def testo(v) -> str:
    if v is None:
        return ""
    if isinstance(v, (list, tuple)):
        return ", ".join(str(x) for x in v)
    if isinstance(v, dict):
        return "; ".join(f"{k}: {testo(x)}" for k, x in v.items())
    return str(v)


def destinatari(v: dict) -> list[str]:
    t = testo(v.get("destinatario"))
    out = [e for e, rx in DESTINATARI if re.search(rx, t, re.I if e not in ("ANAC", "ACN", "DTD", "PSN") else 0)]
    return out or ["Altro"]


def temi(v: dict) -> list[str]:
    t = " ".join(testo(v.get(k)) for k in ("titolo", "richiesta", "perche_serve"))
    out = [e for e, rx in TEMI if re.search(rx, t, re.I if "ACN" not in rx else 0)]
    return out or ["Altro"]


def stato_norm(v: dict) -> str:
    s = testo(v.get("stato")).lower()
    if s.startswith("verificat"):
        return "verificato"
    if s.startswith("da_verificare") or s.startswith("da verificare") or s.startswith("in raccolta"):
        return "da verificare"
    if s.startswith("proposta"):
        return "proposta"
    return "altro"


def inviata(v: dict) -> str:
    s = testo(v.get("stato")).lower()
    if "nessuna richiesta inviata" in s or "nessun invio" in s:
        return "no"
    if re.search(r"\binviat[ao]\b", s):
        return "sì"
    return "no (nessun invio registrato)"


def data(v: dict) -> str:
    """Data esplicita (campo `data`) oppure la più recente citata in stato/evidenza/misure."""
    if v.get("data"):
        return str(v["data"])
    trovate = []
    for k in ("stato", "evidenza", "misura_9_11", "prova", "nota"):
        for g, m, a in DATA_RE.findall(testo(v.get(k))):
            trovate.append(f"{a}-{int(m):02d}-{int(g):02d}")
    for p in re.findall(r"esiti/(20\d\d-\d\d-\d\d)/", testo(v.get("prova")) + testo(v.get("evidenza"))):
        trovate.append(p)
    return max(trovate) if trovate else _DATE_GIT.get(str(v.get("id")), "")


def _date_git() -> dict:
    """Data del commit che ha introdotto la riga «- id: Rxx» (git blame): data di annotazione."""
    import datetime as dt
    import subprocess
    try:
        out = subprocess.run(["git", "blame", "--line-porcelain", str(YAML.relative_to(BASE))], cwd=BASE,
                             capture_output=True, text=True, encoding="utf-8", check=True).stdout
    except Exception:
        return {}
    res, t = {}, None
    for riga in out.splitlines():
        if riga.startswith("author-time "):
            t = dt.datetime.fromtimestamp(int(riga.split()[1]), dt.timezone.utc).date().isoformat()
        m = re.match(r"\t- id: (R\d+)", riga)
        if m and t:
            res[m.group(1)] = t
    return res


_DATE_GIT = _date_git()


def file_citati(v: dict) -> list[str]:
    t = " ".join(testo(v.get(k)) for k in ("prova", "evidenza", "verifica", "misura_9_11"))
    out = []
    for p in re.findall(r"((?:tools|esiti|report|config|sito/content|lavoro)/[\w./\-]+)", t):
        p = p.rstrip(".)")
        if p not in out:
            out.append(p)
    return out


def controlla(voci: list[dict]) -> tuple[list[str], list[str]]:
    """Restituisce (errori bloccanti, avvisi da completare)."""
    errori, avvisi = [], []
    ids = [str(v.get("id", "")) for v in voci]
    for i, n in Counter(ids).items():
        if n > 1:
            errori.append(f"id duplicato: {i} ({n} volte)")
    num = sorted(int(i[1:]) for i in ids if re.fullmatch(r"R\d+", i))
    if num:
        buchi = sorted(set(range(1, num[-1] + 1)) - set(num))
        for b in buchi:
            avvisi.append(f"R{b:02d}: numero non usato (buco; non si rinumera)")
    for v in voci:
        vid = v.get("id", "?")
        for k in OBBLIGATORI:
            if not v.get(k):
                errori.append(f"{vid}: manca il campo obbligatorio «{k}»")
        if stato_norm(v) != "proposta" and not (v.get("evidenza") or v.get("prova")):
            errori.append(f"{vid}: stato «{stato_norm(v)}» senza «evidenza» né «prova»")
        if stato_norm(v) == "altro":
            errori.append(f"{vid}: stato non riconosciuto «{v.get('stato')}»")
        if not v.get("prova") and stato_norm(v) != "proposta":
            avvisi.append(f"{vid}: nessun file di prova («prova» assente)")
        elif v.get("prova") and not file_citati(v):
            avvisi.append(f"{vid}: la prova non cita un file del repository")
        else:
            mancanti = [p for p in file_citati(v) if not (BASE / p).exists()]
            if mancanti:
                avvisi.append(f"{vid}: file citati non presenti nel repository: {', '.join(mancanti)}")
        if "sha256" not in json.dumps(v, ensure_ascii=False).lower():
            avvisi.append(f"{vid}: nessuno sha256 (richiesto da AGENTS.md §3 prima di comunicarla)")
        if not data(v):
            avvisi.append(f"{vid}: nessuna data ricavabile")
        if not v.get("perche_serve"):
            avvisi.append(f"{vid}: manca «perche_serve»")
    return errori, avvisi


def righe(voci: list[dict]) -> list[dict]:
    out = []
    for v in voci:
        out.append(OrderedDict(
            id=v["id"],
            titolo=testo(v.get("titolo")),
            destinatario=testo(v.get("destinatario")),
            destinatari_norm="; ".join(destinatari(v)),
            temi="; ".join(temi(v)),
            tipo=testo(v.get("tipo")),
            stato=stato_norm(v),
            stato_esteso=testo(v.get("stato")),
            inviata=inviata(v),
            data=data(v),
            richiesta=testo(v.get("richiesta")),
            perche_serve=testo(v.get("perche_serve")),
            evidenza=testo(v.get("evidenza")),
            prova=testo(v.get("prova")),
            file_prova="; ".join(file_citati(v)),
            rif=testo(v.get("rif")),
        ))
    return out


def md(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ").strip()


def link_file(p: str) -> str:
    m = re.match(r"sito/content/(.+?)\.md(#.*)?$", p)
    if m:
        url = "/" + m.group(1).removesuffix("/_index") + "/" + (m.group(2) or "")
        return f"[{p.split('/')[-1]}]({url})"
    return f"[{md(p)}]({REPO}{p})"


def link_rif(r: str) -> str:
    out = []
    for x in [x.strip() for x in r.split(",") if x.strip()]:
        m = re.fullmatch(r"#(\d+)", x)
        out.append(f"[{x}]({TICKET}{m.group(1)})" if m else md(x))
    return ", ".join(out)


def pagina(voci: list[dict], rr: list[dict], avvisi: list[str]) -> str:
    oggi = max((r["data"] for r in rr if r["data"]), default="")
    st = Counter(r["stato"] for r in rr)
    L = [
        "---",
        'title: "Raccomandazioni"',
        "date: 2026-11-09",
        f"datiAl: {oggi}" if oggi else "",
        "---",
        "",
        "<!-- Generato da tools/raccomandazioni_pagina.py dal registro report/metodo/richieste-e-raccomandazioni.yaml: non modificare a mano. -->",
        "",
        "> **Proposte di lavoro.** Sono le richieste e raccomandazioni annotate durante l'analisi per rendere "
        "misurabile la spesa ICT della PA. **Nulla è stato inviato agli enti**, salvo quanto indicato nella colonna "
        "«inviata» (oggi: nessuna). Ogni invio richiede l'approvazione di Fabio Pietrosanti e, per i difetti, "
        "evidenza riproducibile con sha256, azione correttiva e metrica (AGENTS.md §3).",
        "",
        f"**Voci:** {len(rr)} · verificate {st['verificato']} · da verificare {st['da verificare']} · "
        f"proposte {st['proposta']} · inviate {sum(r['inviata'] == 'sì' for r in rr)}.",
        "",
        "Scarica: [CSV](/dati/raccomandazioni.csv) · [JSON](/dati/raccomandazioni.json) · "
        f"registro sorgente [richieste-e-raccomandazioni.yaml]({REPO}report/metodo/richieste-e-raccomandazioni.yaml).",
        "",
        "*Stato*: **verificato** = misurato da noi, con prova; **da verificare** = segnale non ancora misurato; "
        "**proposta** = miglioramento di policy o di dato nuovo. Destinatario e tema sono assegnati per parole chiave "
        "(una voce può comparire in più gruppi); la data è quella più recente citata nella voce o, in mancanza, quella del commit che l'ha annotata nel registro.",
        "",
        "## Riepilogo per destinatario",
        "",
        "| Destinatario | Voci | Verificate | Da verificare | Proposte |",
        "|---|---|---|---|---|",
    ]
    def riepilogo(chiave, etichette):
        for e in etichette:
            g = [r for r in rr if e in r[chiave].split("; ")]
            if not g:
                continue
            c = Counter(r["stato"] for r in g)
            L.append(f"| [{e}](#{ancora(chiave, e)}) | {len(g)} | {c['verificato']} | {c['da verificare']} | {c['proposta']} |")
    riepilogo("destinatari_norm", [e for e, _ in DESTINATARI] + ["Altro"])
    L += ["", "## Riepilogo per tema", "", "| Tema | Voci | Verificate | Da verificare | Proposte |", "|---|---|---|---|---|"]
    riepilogo("temi", [e for e, _ in TEMI] + ["Altro"])

    def gruppo(titolo, chiave, etichette):
        L.extend(["", f"## {titolo}"])
        for e in etichette:
            g = [r for r in rr if e in r[chiave].split("; ")]
            if not g:
                continue
            L.extend(["", f'### {e} ({len(g)}) {{#{ancora(chiave, e)}}}', "",
                  "| Id | Raccomandazione | Destinatario | Stato | Data | Evidenze | Ticket |", "|---|---|---|---|---|---|---|"])
            for r in g:
                fl = [x for x in r["file_prova"].split("; ") if x]
                ev = " · ".join(link_file(p) for p in fl) or md(r["prova"])[:160] or "—"
                L.append(
                    f"| [{r['id']}](#{r['id'].lower()}) | {md(r['titolo'])} | {md(r['destinatario'])} | {r['stato']} | "
                    f"{r['data'] or '—'} | {ev} | {link_rif(r['rif']) or '—'} |"
                )
    gruppo("Per destinatario", "destinatari_norm", [e for e, _ in DESTINATARI] + ["Altro"])
    gruppo("Per tema", "temi", [e for e, _ in TEMI] + ["Altro"])

    L += ["", "## Schede", ""]
    for r in rr:
        L += [f"### {r['id']} — {md(r['titolo'])} {{#{r['id'].lower()}}}", "",
              f"- **Destinatario:** {md(r['destinatario'])}",
              f"- **Tema:** {r['temi']} · **Tipo:** {md(r['tipo'])}",
              f"- **Stato:** {md(r['stato_esteso'])} · **Data:** {r['data'] or '—'} · **Inviata:** {r['inviata']}",
              f"- **Richiesta:** {md(r['richiesta'])}"]
        if r["perche_serve"]:
            L.append(f"- **Perché serve:** {md(r['perche_serve'])}")
        if r["evidenza"]:
            L.append(f"- **Evidenza:** {md(r['evidenza'])}")
        if r["prova"]:
            fl = [x for x in r["file_prova"].split("; ") if x]
            L.append(f"- **Prova:** {md(r['prova'])}" + (f" ({' · '.join(link_file(p) for p in fl)})" if fl else ""))
        L += [f"- **Riferimenti:** {link_rif(r['rif']) or '—'}", ""]

    L += ["## Voci da completare", "",
          "Controllo automatico del registro (`tools/raccomandazioni_pagina.py --verifica`). Gli sha256 vanno aggiunti prima di "
          "qualsiasi comunicazione a un ente.", ""]
    L += [f"- {md(a)}" for a in avvisi] or ["- nessuna"]
    return "\n".join(x for x in L if x is not None) + "\n"


def ancora(chiave, e):
    pref = "dest" if chiave.startswith("dest") else "tema"
    return pref + "-" + re.sub(r"[^a-z0-9]+", "-", e.lower()).strip("-")


def main() -> int:
    voci = carica()
    errori, avvisi = controlla(voci)
    print(f"{len(voci)} voci; {len(errori)} errori bloccanti; {len(avvisi)} avvisi")
    for e in errori:
        print("ERRORE", e)
    if "--verifica" in sys.argv:
        for a in avvisi:
            print("avviso", a)
        return 1 if errori else 0
    if errori:
        return 1
    rr = righe(voci)
    PAGINA.write_text(pagina(voci, rr, avvisi), encoding="utf-8")
    DATI.mkdir(parents=True, exist_ok=True)
    (DATI / "raccomandazioni.json").write_text(json.dumps(rr, ensure_ascii=False, indent=1), encoding="utf-8")
    with (DATI / "raccomandazioni.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rr[0].keys()))
        w.writeheader()
        w.writerows(rr)
    print("scritti", PAGINA.relative_to(BASE), "e sito/static/dati/raccomandazioni.{csv,json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
