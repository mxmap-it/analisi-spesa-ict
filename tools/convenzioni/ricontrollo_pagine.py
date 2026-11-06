"""#62, documenti mancanti: ricontrollo dal vivo delle pagine ufficiali delle iniziative prima di dichiarare un documento mancante.

Per ogni pagina consip.it già trovata (consip/<iniziativa>.json, cita_chiave) la riscarica con User-Agent da browser più l'URL
del progetto (AGENTS.md §3), una richiesta ogni 5 s, nessun login né CAPTCHA, e ne registra http, sha256 e i nomi dei documenti linkati.
Una pagina che risponde 401/403/429 o con una maschera di login si registra come blocco (blocchi-accesso.csv lo scrive
documenti_mancanti.py). Ripartibile: salta le pagine già ricontrollate nella stessa data, salvo --rifai.
Uscita: report/convenzioni/database/ricontrollo-pagine.json
Uso: python tools/convenzioni/ricontrollo_pagine.py [--rifai]"""
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

import requests

R = Path(__file__).resolve().parent.parent.parent
DB = R / "report/convenzioni/database"
OUT = DB / "ricontrollo-pagine.json"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36 "
      "analisi-spesa-ict (+https://github.com/mxmap-it/analisi-spesa-ict)")
PAUSA = 5
LOGIN = re.compile(r"(type=\"password\"|accedi per (visualizzare|scaricare)|area riservata|effettua il login)", re.I)


def main(rifai=False):
    oggi = datetime.now(timezone.utc).date().isoformat()
    esiti = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    s = requests.Session()
    s.headers["User-Agent"] = UA
    for f in sorted((DB / "consip").glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        for pg in d.get("pagine", []):
            if not pg.get("cita_chiave"):
                continue
            u = pg["url"]
            if not rifai and esiti.get(u, {}).get("data", "")[:10] == oggi:
                continue
            time.sleep(PAUSA)
            e = {"iniziativa": d["iniziativa"], "data": datetime.now(timezone.utc).isoformat(timespec="seconds")}
            try:
                r = s.get(u, timeout=60)
                html = r.text
                nomi = sorted({unquote(h.rsplit("/", 1)[-1]) for h in
                               re.findall(r'href="([^"]+\.(?:pdf|p7m|zip|xlsx?|docx?|odt|ods|rar))"', html, re.I)})
                e.update(http=r.status_code, sha256_html=hashlib.sha256(r.content).hexdigest(), documenti=nomi,
                         login=bool(LOGIN.search(html)), blocco=r.status_code in (401, 403, 429))
            except requests.RequestException as x:
                e.update(http=None, errore=str(x)[:200], blocco=True, documenti=[])
            esiti[u] = e
            OUT.write_text(json.dumps(esiti, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
            print(d["iniziativa"], e.get("http"), len(e["documenti"]), flush=True)


if __name__ == "__main__":
    main("--rifai" in sys.argv)
