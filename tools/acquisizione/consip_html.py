#!/usr/bin/env python3
"""#11: elenco delle risorse Consip dalle pagine HTML del catalogo.

Il robots.txt di dati.consip.it esclude /api/ (R86) e chiede Crawl-Delay 10: si leggono /dataset?page=N e
/dataset/<nome> con 10 s fra le richieste e si estraggono i link /download/.

    consip_html.py > lavoro/mirror-completamento/consip/html-elenco.tsv   (una riga per risorsa: dataset TAB url)
"""
import re, sys, time, urllib.request, json, csv
UA = "Mozilla/5.0 (compatible; analisi-spesa-ict; +https://analisi-spesa-ict.mxmap.it)"
B = "https://dati.consip.it"
def get(u):
    time.sleep(10)
    return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=60).read().decode("utf-8", "replace")
ds = set(); p = 1
while True:
    h = get(f"{B}/dataset?page={p}")
    nuovi = set(re.findall(r'href="/dataset/([a-z0-9_\-]+)"', h)) - ds
    if not nuovi: break
    ds |= nuovi; p += 1
print("dataset", len(ds), file=sys.stderr)
link = set()
for d in sorted(ds):
    h = get(f"{B}/dataset/{d}")
    for u in re.findall(r'href="(https?://dati\.consip\.it/download/[^"]+)"', h): link.add((d, u))
for d, u in sorted(link): print(f"{d}\t{u}")
