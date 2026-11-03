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


DASH = ["cf", "denominazione", "categoria", "regione", "esito", "dettaglio_esito", "piattaforma", "at_url", "segnali"]


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
    # gzip con mtime=0: stesso contenuto, stessi byte (sha256 stabile fra rigenerazioni)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=CAMPI, extrasaction="ignore")
    w.writeheader()
    w.writerows(righe)
    _gz(pub / "enti.csv.gz", buf.getvalue())
    _gz(pub / "enti.json.gz", json.dumps({"schema": "trasparenza.enti/1", "metodo": VERSIONE_METODO, "giro": data, "run": run,
                                          "licenza": "CC BY 4.0", "enti": [{k: r.get(k) for k in CAMPI} for r in righe]},
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
