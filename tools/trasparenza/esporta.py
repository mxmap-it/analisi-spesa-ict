"""Esportazione di un giro come open data (decisione di Fabio, 3/11/2026: pubblicazione nominativa).

Cartella pubblica (TRASPARENZA_PUBBLICA, default sito/static/dati/trasparenza/):
    giri/AAAA-MM-GG/enti.csv, enti.json       esito per ente (schema: schema/enti.schema.json)
    giri/AAAA-MM-GG/riepilogo.json, per-*.csv  aggregati
    ultimo/...                                 copia dell'ultimo giro
    indice.json                                elenco dei giri
    storico.json                               cf -> [[giro, esito], ...] (serie storica)
    invii.json                                 stato delle PEC dal registro degli invii
Un giro pubblicato non si sovrascrive (serve --forza, per correzioni documentate nel registro
delle revisioni). Gli aggregati vanno anche in esiti/AAAA-MM-GG/trasparenza/.
Un run che non è un mese (es. «pilota-...») si esporta in lavoro/trasparenza/pilota/<run>/.
"""
from __future__ import annotations

import csv
import gzip
import io
import json
import os
import shutil
from collections import Counter, defaultdict
from pathlib import Path

from comune import LAVORO, RADICE, VERSIONE_METODO, adesso, connetti

PUBBLICA = Path(os.environ.get("TRASPARENZA_PUBBLICA", RADICE / "sito" / "static" / "dati" / "trasparenza"))
ESITI = ["accessibile", "bloccato da robots.txt", "noindex", "bloccato da WAF/anti-bot",
         "irraggiungibile", "tls invalido", "url non valido", "sezione non individuata", "errore dello strumento"]
VIOLAZIONI = {"bloccato da robots.txt", "noindex", "bloccato da WAF/anti-bot"}
CAMPI = ["cf", "ipa", "denominazione", "tipologia", "categoria", "regione", "sito_ipa", "url_l190", "anno_l190",
         "esito_anac", "at_url", "at_provenienza", "esito", "dettaglio_esito", "segnali", "status_bot", "status_browser",
         "tls_valido", "robots_url", "robots_sha256", "robots_stato", "robots_blocchi", "noindex", "firme_waf",
         "piattaforma", "piattaforma_prova", "piattaforma_corrispondenza", "generator", "indizi", "conferma_browser", "ts"]


DASH = ["cf", "denominazione", "categoria", "regione", "esito", "dettaglio_esito", "piattaforma", "at_url", "segnali", "esito_server", "esito_desktop", "lettura_origini", "vendor_blocco", "ricercabilita", "vie_coincidono", "prove"]


def _gz(path: Path, testo: str):
    with path.open("wb") as fh, gzip.GzipFile(fileobj=fh, mode="wb", mtime=0, filename="") as g:
        g.write(testo.encode("utf-8"))


def riga(e: dict, ts: str, d: dict) -> dict:
    rb = d.get("robots") or {}
    pf = d.get("piattaforma") or {}
    return e | {
        "at_url": d.get("at_url") or e.get("at_url") or "", "at_provenienza": d.get("at_provenienza") or e.get("at_provenienza") or "",
        "esito": d.get("esito"), "dettaglio_esito": d.get("dettaglio_esito", ""), "segnali": ";".join(d.get("segnali", [])),
        "status_bot": d.get("status_bot"), "status_browser": d.get("status_browser"), "tls_valido": d.get("tls_valido"),
        "robots_url": rb.get("url", ""), "robots_sha256": rb.get("sha256", ""), "robots_stato": rb.get("stato", ""),
        "robots_blocchi": "; ".join(f"{b['agente']} {b['percorso']} <- {b['regola']}" for b in rb.get("blocchi", [])),
        "noindex": " | ".join(d.get("noindex", [])),
        "firme_waf": "; ".join(sorted(set(d.get("firme_bot", []) + d.get("firme_browser", [])))),
        "piattaforma": pf.get("piattaforma", ""), "piattaforma_prova": pf.get("prova", ""),
        "piattaforma_corrispondenza": pf.get("corrispondenza", ""), "generator": pf.get("generator", ""),
        "indizi": pf.get("indizi", ""), "conferma_browser": d.get("conferma_browser", ""), "ts": ts}


def righe_run(c, run: str) -> list[dict]:
    cols = [x[1] for x in c.execute("PRAGMA table_info(enti)")]
    out = []
    for row in c.execute("SELECT e.*, x.ts, x.dettaglio FROM esiti x JOIN enti e USING(cf) WHERE x.run=?", (run,)):
        e = dict(zip(cols, row[:len(cols)]))
        out.append(riga(e, row[-2], json.loads(row[-1])))
    return out


def _agg(righe, chiave):
    t = defaultdict(Counter)
    for r in righe:
        t[r[chiave] or "(n.d.)"][r["esito"]] += 1
    return t


def _tabella(path: Path, chiave: str, righe: list[dict]):
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow([chiave, "totale"] + ESITI + ["violazioni_art9", "quota_violazioni"])
        for k, c in sorted(_agg(righe, chiave).items(), key=lambda kv: -sum(kv[1].values())):
            tot = sum(c.values())
            v = sum(c[x] for x in VIOLAZIONI)
            w.writerow([k, tot] + [c[x] for x in ESITI] + [v, f"{v / tot:.3f}"])


CAMPI_DIAG = ["esito_server", "esito_desktop", "lettura_origini", "vendor_blocco", "cdn", "challenge_js", "captcha",
              "dns_alias", "tls_emittente", "tls_scadenza", "tls_errore", "prove",
              "via_anac", "via_home", "vie_coincidono", "ricercabilita", "cig_test"]
CAMPI_TENTATIVI = ["cf", "origine", "ip", "asn", "asn_nome", "ts", "tipo", "client", "user_agent", "url", "url_finale",
                   "redirect", "status", "errore", "byte", "sha256_corpo", "vendor_blocco", "regole_blocco", "cdn",
                   "challenge_js", "captcha", "dns_a", "dns_aaaa", "dns_alias", "tls_versione", "tls_emittente",
                   "tls_scadenza", "tls_errore", "secondi", "grezzo_tipo", "grezzo_sha256", "grezzo_url"]
MAX_PROVA = 5_000_000


def _fallito(t: dict) -> bool:
    return bool(t.get("errore")) or (t.get("status") or 0) >= 400 or bool(t.get("vendor_blocco"))


def _sintesi(ts: list[dict]) -> str:
    if not ts:
        return ""
    ok = [t for t in ts if not _fallito(t)]
    return "accessibile" if ok else "bloccato o irraggiungibile"


def arricchisci(c, run: str, righe: list[dict], pub: Path) -> list[dict]:
    """Aggiunge a ogni ente la diagnostica estesa (due origini) e la caratterizzazione; pubblica i tentativi
    e i log grezzi dei tentativi falliti (prove/<sha256>.<tipo>.gz)."""
    from comune import ARCHIVIO
    per_cf = defaultdict(list)
    for (dati,) in c.execute("SELECT dati FROM tentativi WHERE run=? ORDER BY ts", (run,)):
        t = json.loads(dati)
        per_cf[t["cf"]].append(t)
    car = {cf: json.loads(d) for cf, d in c.execute("SELECT cf, dati FROM caratteri WHERE run=?", (run,))}
    cig = {cf: g for cf, g in c.execute("SELECT cf, cig FROM cig_test")}
    prove_dir = (pub / "prove") if pub.is_relative_to(LAVORO) else PUBBLICA / "prove"  # content-addressed, condivisa fra giri
    prove_dir.mkdir(parents=True, exist_ok=True)
    base_url = "prove/" if pub.is_relative_to(LAVORO) else "/dati/trasparenza/prove/"
    piatti = []
    for r in righe:
        ts = per_cf.get(r["cf"], [])
        srv = [t for t in ts if t["origine"] == "server"]
        dsk = [t for t in ts if t["origine"] == "desktop"]
        r["esito_server"], r["esito_desktop"] = _sintesi(srv), _sintesi(dsk)
        if srv and dsk:
            r["lettura_origini"] = ("blocco legato all'IP o al datacenter" if r["esito_server"] != "accessibile" and r["esito_desktop"] == "accessibile"
                                    else "stesso esito da datacenter e da IP residenziale" if r["esito_server"] == r["esito_desktop"]
                                    else "accessibile dal datacenter, non da IP residenziale")
        r["vendor_blocco"] = ";".join(sorted({v for t in ts for v in t.get("vendor_blocco") or []}))
        r["cdn"] = ";".join(sorted({v for t in ts for v in t.get("cdn") or []}))
        r["challenge_js"] = any(t.get("challenge_js") for t in ts) if ts else ""
        r["captcha"] = any(t.get("captcha") for t in ts) if ts else ""
        if ts:
            r["dns_alias"] = ";".join(ts[0]["dns"].get("alias") or [])
            r["tls_emittente"], r["tls_scadenza"], r["tls_errore"] = (ts[0]["tls"].get(k, "") for k in ("emittente", "scadenza", "errore"))
        prove = []
        for t in ts:
            s = t.get("grezzo_sha256")
            if s:
                nome = f"{s}.{'har' if t.get('grezzo_tipo') == 'har' else 'txt'}.gz"
                src = ARCHIVIO / "blobs" / "sha256" / s[:2] / s[2:4] / s
                if src.exists() and src.stat().st_size <= MAX_PROVA and not (prove_dir / nome).exists():
                    _gzb(prove_dir / nome, src.read_bytes())
                t["grezzo_url"] = f"{base_url}{nome}" if (prove_dir / nome).exists() else f"archivio sha256:{s}"
                prove.append(t["grezzo_url"])
            piatti.append(_piatto(t))
        r["prove"] = " ".join(prove)
        k = car.get(r["cf"], {})
        r |= {"via_anac": k.get("via_anac", ""), "via_home": k.get("via_home", ""),
              "vie_coincidono": k.get("coincidono", "") if k else "", "ricercabilita": k.get("ricercabilita", ""),
              "cig_test": k.get("cig_test") or cig.get(r["cf"], "")}
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=CAMPI_TENTATIVI, extrasaction="ignore")
    w.writeheader()
    w.writerows(piatti)
    _gz(pub / "tentativi.csv.gz", buf.getvalue())
    _gz(pub / "tentativi.jsonl.gz", "".join(json.dumps(t, ensure_ascii=False) + "\n" for ts in per_cf.values() for t in ts))
    _gz(pub / "caratteri.jsonl.gz", "".join(json.dumps(k, ensure_ascii=False) + "\n" for k in car.values()))
    return righe


def _gzb(path: Path, dati: bytes):
    with path.open("wb") as fh, gzip.GzipFile(fileobj=fh, mode="wb", mtime=0, filename="") as g:
        g.write(dati)


def _piatto(t: dict) -> dict:
    return {k: t.get(k, "") for k in CAMPI_TENTATIVI} | {
        "redirect": " -> ".join(f"{h['status']} {h['url']}" for h in t.get("catena", [])),
        "vendor_blocco": ";".join(t.get("vendor_blocco") or []), "regole_blocco": " || ".join(t.get("regole_blocco") or []),
        "cdn": ";".join(t.get("cdn") or []), "dns_a": ";".join(t["dns"].get("a", [])), "dns_aaaa": ";".join(t["dns"].get("aaaa", [])),
        "dns_alias": ";".join(t["dns"].get("alias", [])), "tls_versione": t["tls"].get("versione", ""),
        "tls_emittente": t["tls"].get("emittente", ""), "tls_scadenza": t["tls"].get("scadenza", ""), "tls_errore": t["tls"].get("errore", "")}


def esporta(run: str, data: str = "", forza: bool = False) -> Path:
    c = connetti()
    if not data:
        data = (c.execute("SELECT min(ts) FROM esiti WHERE run=?", (run,)).fetchone()[0] or adesso())[:10]
    pilota = not (run[:2] == "20" and len(run) == 7)
    pub = (LAVORO / "pilota" / run) if pilota else PUBBLICA / "giri" / data
    if (pub / "enti.csv.gz").exists() and not forza and not pilota:
        raise SystemExit(f"giro {data} già pubblicato in {pub}: non si sovrascrive (--forza solo per correzioni documentate)")
    pub.mkdir(parents=True, exist_ok=True)
    righe = sorted(righe_run(c, run), key=lambda r: r["cf"])
    righe = arricchisci(c, run, righe, pub)
    # gzip con mtime=0: stesso contenuto, stessi byte (sha256 stabile fra rigenerazioni)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=CAMPI + CAMPI_DIAG, extrasaction="ignore")
    w.writeheader()
    w.writerows(righe)
    _gz(pub / "enti.csv.gz", buf.getvalue())
    _gz(pub / "enti.json.gz", json.dumps({"schema": "trasparenza.enti/1", "metodo": VERSIONE_METODO, "giro": data, "run": run,
                                          "licenza": "CC BY 4.0", "enti": [{k: r.get(k) for k in CAMPI + CAMPI_DIAG} for r in righe]},
                                         ensure_ascii=False, separators=(",", ":")))
    # file leggero per la dashboard: una lista per ente
    (pub / "dashboard.json").write_text(json.dumps(
        {"campi": DASH, "giro": data, "enti": [[r.get(k) or "" for k in DASH] for r in righe]},
        ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    for k in ("esito", "categoria", "regione", "piattaforma"):
        _tabella(pub / f"per-{k}.csv", k, righe)
    seg = Counter(s for r in righe for s in (r["segnali"].split(";") if r["segnali"] else []))
    riep = {"schema": "trasparenza.riepilogo/1", "run": run, "giro": data, "metodo": VERSIONE_METODO,
            "generato": adesso(), "enti": len(righe),
            "esiti": dict(Counter(r["esito"] for r in righe).most_common()),
            "segnali": dict(seg), "violazioni_art9": sum(r["esito"] in VIOLAZIONI for r in righe),
            "piattaforme": dict(Counter(r["piattaforma"] or "(non provata)" for r in righe).most_common()),
            "provenienza_at": dict(Counter(r["at_provenienza"] or "(nessuna)" for r in righe).most_common()),
            "firme_waf": dict(Counter(f for r in righe for f in r["firme_waf"].split("; ") if f).most_common())}
    for k in ("categoria", "regione", "piattaforma"):
        riep[f"per_{k}"] = {a: dict(b) for a, b in _agg(righe, k).items()}
    (pub / "riepilogo.json").write_text(json.dumps(riep, ensure_ascii=False, indent=1), encoding="utf-8")
    if not pilota:
        agg = RADICE / "esiti" / data / "trasparenza"
        agg.mkdir(parents=True, exist_ok=True)
        for f in ("riepilogo.json", "per-esito.csv", "per-categoria.csv", "per-regione.csv", "per-piattaforma.csv"):
            shutil.copy2(pub / f, agg / f)
        aggiorna_indici()
    print(json.dumps({"pubblicato": str(pub), "enti": len(righe), "esiti": riep["esiti"]}, ensure_ascii=False))
    return pub


def aggiorna_indici():
    """indice.json, storico.json, ultimo/ e invii.json nella cartella pubblica."""
    giri = sorted(p.name for p in (PUBBLICA / "giri").iterdir() if (p / "enti.json.gz").exists())
    indice, storico = [], defaultdict(list)
    for g in giri:
        rp = json.loads((PUBBLICA / "giri" / g / "riepilogo.json").read_text(encoding="utf-8"))
        indice.append({"giro": g, "enti": rp["enti"], "esiti": rp["esiti"], "metodo": rp.get("metodo"),
                       "violazioni_art9": rp["violazioni_art9"]})
        for e in json.loads(gzip.decompress((PUBBLICA / "giri" / g / "enti.json.gz").read_bytes()))["enti"]:
            storico[e["cf"]].append([g, e["esito"]])
    (PUBBLICA / "indice.json").write_text(json.dumps({"giri": indice}, ensure_ascii=False, indent=1), encoding="utf-8")
    (PUBBLICA / "storico.json").write_text(json.dumps(storico, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    ult = PUBBLICA / "ultimo"
    shutil.rmtree(ult, ignore_errors=True)
    shutil.copytree(PUBBLICA / "giri" / giri[-1], ult)
    (ult / "GIRO").write_text(giri[-1] + "\n", encoding="utf-8")
    for g in giri[:-1]:  # il file della dashboard serve solo nell'ultimo giro
        (PUBBLICA / "giri" / g / "dashboard.json").unlink(missing_ok=True)
    import pec
    pec.esporta_stato_invii(PUBBLICA / "invii.json")
