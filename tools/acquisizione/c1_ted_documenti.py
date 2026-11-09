#!/usr/bin/env python3
"""L2 per la ricerca mirata C1 (#55 #66): dal link TED dell avviso (PVL link_eform_ted) al link dei documenti di gara.

La pagina ted.europa.eu/…/detail risponde con una verifica anti-bot (esito «blocco» in piattaforme_cig.py): si usa
l API v3 anonima di TED (la stessa di ted_mirror.py) per leggere, per numero di pubblicazione, il campo eForms
BT-15 «document-url-lot». Pausa 2 s. Uscita: CSV nel formato di ingresso di piattaforme_cig.py (link = URL documenti).
Uso: .venv/bin/python tools/acquisizione/c1_ted_documenti.py lavoro/c1-mirata/ingresso.csv lavoro/c1-mirata/ingresso-ted-doc.csv
"""
import csv, re, sys, time
import requests

API = "https://api.ted.europa.eu/v3/notices/search"
UA = "analisi-spesa-ict (+https://analisi-spesa-ict.mxmap.it)"

righe = [r for r in csv.DictReader(open(sys.argv[1], encoding="utf-8")) if r["link_ted"]]
out = []
for r in righe:
    m = re.search(r"NOTICE:(\d+-\d{4})", r["link_ted"]) or re.search(r"detail/(\d+-\d{4})", r["link_ted"])
    if not m:
        continue
    q = {"query": f"publication-number={m.group(1)}", "fields": ["publication-number", "document-url-lot", "buyer-name"], "limit": 1}
    try:
        j = requests.post(API, json=q, headers={"User-Agent": UA}, timeout=60).json()
    except Exception as e:
        print(r["cig"], "errore", e); continue
    urls = set()
    for n in j.get("notices", []):
        v = n.get("document-url-lot") or []
        for x in (v if isinstance(v, list) else [v]):
            urls |= set(x if isinstance(x, list) else [x]) if not isinstance(x, dict) else {u for l in x.values() for u in (l if isinstance(l, list) else [l])}
    print(r["cig"], m.group(1), sorted(urls))
    for u in sorted(urls)[:2]:
        d = dict(r); d["link"] = u; out.append(d)
    time.sleep(2)
with open(sys.argv[2], "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(righe[0].keys())); w.writeheader(); w.writerows(out)
print(len(out), "righe ->", sys.argv[2])
