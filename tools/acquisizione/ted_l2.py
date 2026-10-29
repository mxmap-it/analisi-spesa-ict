#!/usr/bin/env python3
"""Livello L2 (acquisizione documenti): abbina i CIG con data GUCE (dataset ANAC pubblicazioni) agli avvisi TED
e ne ricava il link ai documenti di gara (eForms BT-15, campo "document-url-lot").
L avviso TED non contiene il CIG: si cerca per paese IT + data di pubblicazione (±3 giorni) + somiglianza
di ente e oggetto. Uscita: report/metodo/acquisizione/ted-l2-campione.jsonl (un record per CIG, con punteggio).
Metodo: sito/content/progetto/acquisizione-documenti.md"""
import csv, glob, io, json, re, sys, time, zipfile
from datetime import date, timedelta
from difflib import SequenceMatcher
from pathlib import Path
import requests
R = Path(__file__).resolve().parents[2]
OUT = R / "report/metodo/acquisizione/ted-l2-campione.jsonl"
camp = {r["cig"]: r for r in csv.DictReader(open(R / "report/metodo/campione-misura-v3-cieco.csv", encoding="utf-8"))}
guce = {}
for f in sorted(glob.glob(str(R / "archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/pubblicazioni/filesystem/*csv.zip"))):
    z = zipfile.ZipFile(f)
    for r in csv.DictReader(io.TextIOWrapper(z.open(z.namelist()[0]), encoding="utf-8", errors="replace"), delimiter=";"):
        if r["cig"] in camp and r["data_guce"].strip():
            guce[r["cig"]] = r["data_guce"].strip()[:10]
def txt(v):
    if isinstance(v, dict): return " ".join(txt(x) for x in v.values())
    if isinstance(v, list): return " ".join(txt(x) for x in v)
    return str(v or "")
norm = lambda s: re.sub(r"[^a-z0-9 ]", " ", (s or "").lower())
sim = lambda a, b: SequenceMatcher(None, norm(a)[:300], norm(b)[:300]).ratio()
OUT.parent.mkdir(parents=True, exist_ok=True)
out = []
for cig, d in sorted(guce.items()):
    c = camp[cig]; g = date.fromisoformat(d)
    q = f"buyer-country = ITA AND publication-date >= {(g - timedelta(days=3)):%Y%m%d} AND publication-date <= {(g + timedelta(days=10)):%Y%m%d}"
    migliore, tok, n = None, None, 0
    while True:
        body = {"query": q, "fields": ["publication-number", "publication-date", "notice-title", "buyer-name", "document-url-lot", "notice-type"],
                "limit": 250, "paginationMode": "ITERATION"}
        if tok: body["iterationNextToken"] = tok
        r = requests.post("https://api.ted.europa.eu/v3/notices/search", json=body, timeout=120).json()
        for nt in r.get("notices", []):
            n += 1
            ente = txt(nt.get("buyer-name"))
            tit = txt((nt.get("notice-title") or {}).get("ita") or nt.get("notice-title"))
            p = 0.4 * sim(c["stazione_appaltante"], ente) + 0.6 * sim(c["testo"], tit)
            if not migliore or p > migliore["punteggio"]:
                migliore = {"punteggio": round(p, 3), "avviso": nt["publication-number"], "titolo": tit[:200], "ente_ted": ente[:120],
                            "document_url": nt.get("document-url-lot") or [], "tipo": nt.get("notice-type")}
        tok = r.get("iterationNextToken")
        if not tok: break
        time.sleep(1)
    rec = {"cig": cig, "importo": float(c["importo_lotto"] or 0), "data_guce": d, "avvisi_esaminati": n, "migliore": migliore,
           "abbinato": bool(migliore and migliore["punteggio"] >= 0.5), "livello": "L2"}
    out.append(rec); print(cig, n, migliore and migliore["punteggio"], migliore and migliore["avviso"], flush=True)
    time.sleep(1)
OUT.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in out), encoding="utf-8")
tot = sum(float(c["importo_lotto"] or 0) for c in camp.values())
print(f"CIG con GUCE {len(guce)}/{len(camp)}; abbinati {sum(x[abbinato] for x in out)}; con link documenti {sum(1 for x in out if x[abbinato] and x[migliore][document_url])}; quota importo con GUCE {sum(x[importo] for x in out)/tot:.1%}")
