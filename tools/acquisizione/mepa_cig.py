#!/usr/bin/env python3
"""MePA / acquistinretepa con browser reale headless (Playwright), da anonimo (#57; AGENTS.md §3: browser reale ammesso).

Le schede di acquistinretepa sono in JavaScript; l'unica ricerca pubblica è la vetrina dei bandi
(POST /publicservices/vetrineservices/getBandi, la stessa chiamata della pagina vetrina_bandi.html). Per ogni CIG con
link PVL ad acquistinretepa si cerca il CIG nel campo «idt» della vetrina, fra i bandi attivi e in archivio.
Controllo: con idt = numero bando (6666984) la vetrina risponde con il bando (Microsoft EA, ID 3048), quindi la
ricerca funziona; con un CIG di ordine/trattativa di un'amministrazione non trova nulla perché ODA, TD e RDO
chiuse non hanno una pagina pubblica. Mai login, mai CAPTCHA; >= 6 s fra richieste.
Uso (server): nice .venv/bin/python tools/acquisizione/mepa_cig.py lavoro/residuo-s6/out
  legge out/esiti.jsonl (famiglia js, ultimo esito non-tentato-js) e accoda gli esiti nuovi allo stesso file.
"""
import json, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36 "
      "analisi-spesa-ict (+https://github.com/mxmap-it/analisi-spesa-ict)")
JS_FETCH = """b => fetch("/publicservices/vetrineservices/getBandi", {method: "POST",
  headers: {"Content-Type": "application/json"}, body: JSON.stringify(b)}).then(r => r.json())"""


def main():
    out = Path(sys.argv[1]); f = out / "esiti.jsonl"
    ultimo = {}
    for l in open(f, encoding="utf-8"):
        x = json.loads(l); ultimo[x["cig"]] = x
    da_fare = [x for x in ultimo.values() if x["famiglia"] == "js" and x["esito"] == "non-tentato-js"]
    print(len(da_fare), "CIG MePA", flush=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(user_agent=UA)
        pg.goto("https://www.acquistinretepa.it/opencms/opencms/vetrina_bandi.html", wait_until="networkidle", timeout=90000)
        for x in da_fare:
            t0 = time.time(); trovati = []
            for arch in (False, True):
                time.sleep(6)
                body = {"isArchive": arch, "strumento": [], "categoria": [], "idt": x["cig"], "tempo": {"dataDa": None, "dataA": None},
                        "paginazione": {"pagina": 1, "itemPagina": 20}, "orderBy": {"campo": "dataPubblicazione", "verso": "desc"}, "listTipoContratto": []}
                try:
                    j = pg.evaluate(JS_FETCH, body)
                except Exception as e:
                    trovati = None; err = str(e)[:200]; break
                trovati += [{"idBando": e.get("idBando"), "titolo": e.get("titoloBando"), "archivio": arch} for e in (j.get("payload") or {}).get("elencoBandi") or []]
            rec = {**x, "famiglia": "js", "pagine": [], "documenti": [], "data": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   "metodo": "playwright vetrina getBandi idt=CIG", "secondi": round(time.time() - t0, 1)}
            if trovati is None: rec.update(esito="errore", errore=err)
            else: rec.update(esito="mepa-cig-in-vetrina" if trovati else "mepa-nessuna-pagina-pubblica", vetrina=trovati)
            with open(f, "a", encoding="utf-8") as o: o.write(json.dumps(rec, ensure_ascii=False) + "\n")
            print(x["cig"], rec["esito"], flush=True)
        b.close()


if __name__ == "__main__":
    main()
