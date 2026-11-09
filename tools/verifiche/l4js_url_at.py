#!/usr/bin/env python3
"""#73 L4-js: quanti enti «pagina AT quasi vuota (JS)» avevano in realtà un URL della sezione AT errato.

Per ogni ente della fase 1 di L4-js (lavoro/residuo-s6/l4-js/enti.jsonl) si rilegge UNA volta l'URL AT dichiarato
(registro L.190 / IndicePA, tabella enti del monitor AT) con una GET semplice (>= 5 s per host, UA del progetto, mai
login/CAPTCHA) e si archivia la risposta come evidenza (blob sha256). Classi, nell'ordine:
  senza-url-at        nessun URL AT dichiarato (si è partiti dal sito istituzionale IndicePA);
  radice-piattaforma  lo stesso URL AT è dichiarato da >= 2 enti (radice di piattaforma/portale condiviso);
  cartella-file       l'URL punta a una cartella di file statici (sites/default/files, content/dam, images/stories...);
  risposta-errore     HTTP >= 400 o errore di rete/TLS;
  pagina-vuota        200 ma < 1500 caratteri di testo anche senza JS (pagina d'indice, redirect, vuota);
  pagina-ok           200 con testo: l'URL è plausibile, la pagina è davvero scritta in JavaScript o povera.
Sono «URL AT errati» le classi radice-piattaforma, cartella-file, risposta-errore.
Uscita: esiti/<DATA>/acquisizione/l4js-url-at.csv e .json. Uso (server): nice .venv/bin/python tools/verifiche/l4js_url_at.py [DATA]
"""
import collections, csv, datetime, html, json, re, sqlite3, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlsplit

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/acquisizione"))
import piattaforme_cig as P  # noqa: E402
import requests  # noqa: E402

D = R / "lavoro/residuo-s6/l4-js"
RX_FILE = re.compile(r"/sites/default/files/|/content/dam/|/images/stories/|/allegati/|/files?/|file_?trasparenza|"
                     r"documenti_trasparenza|/docs/default-source/|/wp-content/uploads/", re.I)
ERRATI = ("radice-piattaforma", "cartella-file", "risposta-errore")


def classifica(at, condiviso, status, testo):
    if not at: return "senza-url-at"
    if condiviso >= 2: return "radice-piattaforma"
    if RX_FILE.search(urlsplit(at).path or ""): return "cartella-file"
    if status is None or status >= 400: return "risposta-errore"
    return "pagina-vuota" if len(testo) < 1500 else "pagina-ok"


def main():
    data = sys.argv[1] if len(sys.argv) > 1 else str(datetime.date.today())
    enti = [json.loads(l) for l in open(D / "enti.jsonl", encoding="utf-8")]
    db = sqlite3.connect(R / "lavoro/trasparenza/stato.sqlite")
    quanti = collections.Counter(P.normalizza(u).rstrip("/").lower() for (u,) in db.execute("select at_url from enti where at_url<>''"))

    def uno(e):
        at = e.get("at_url") or ""; st, fin, sha, tx, err = None, "", "", "", ""
        if at:
            u = P.normalizza(at)
            try:
                P.attendi(u); r = requests.get(u, timeout=45, headers={"User-Agent": P.UA}, allow_redirects=True)
                st, fin = r.status_code, r.url; sha = P.archivia(r.content, r.url, D)
                tx = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?is)<(script|style).*?</\1>", " ", r.text))))
            except Exception as x:
                err = type(x).__name__ + ": " + str(x)[:150]
        k = quanti[P.normalizza(at).rstrip("/").lower()] if at else 0
        c = classifica(at, k, st, tx)
        return {"cf": e["cf"], "denominazione": (e.get("denominazione") or "").strip(), "at_url_dichiarato": at, "sito_ipa": e.get("sito_ipa", ""),
                "enti_con_stesso_url": k, "http": st, "url_finale": fin, "caratteri_testo": len(tx), "errore_rete": err, "sha256": sha,
                "classe": c, "url_at_errato": c in ERRATI, "prima_pagina_l4js": (e["pagine"][0]["url"] if e["pagine"] else ""),
                "esito_l4js": e["esito"], "cig_trovati_l4js": e.get("cig_trovati", 0), "importo": round(e.get("importo", 0), 2)}

    by = collections.defaultdict(list)
    for e in enti: by[urlsplit(P.normalizza(e.get("at_url") or "x://")).netloc].append(e)
    with ThreadPoolExecutor(8) as ex:
        righe = [r for g in ex.map(lambda g: [uno(e) for e in g], by.values()) for r in g]
    righe.sort(key=lambda r: (-r["url_at_errato"], r["classe"], -r["importo"]))
    o = R / f"esiti/{data}/acquisizione"; o.mkdir(parents=True, exist_ok=True)
    with open(o / "l4js-url-at.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=righe[0].keys()); w.writeheader(); w.writerows(righe)
    s = {"generato": data, "enti": len(righe), "classi": dict(collections.Counter(r["classe"] for r in righe).most_common()),
         "url_at_errati": sum(r["url_at_errato"] for r in righe),
         "http": dict(collections.Counter(str(r["http"]) for r in righe if r["at_url_dichiarato"]).most_common()),
         "errati_per_esito_l4js": dict(collections.Counter(r["esito_l4js"] for r in righe if r["url_at_errato"]).most_common()),
         "errati_con_cig_trovati_l4js": sum(1 for r in righe if r["url_at_errato"] and r["cig_trovati_l4js"])}
    json.dump(s, open(o / "l4js-url-at.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(s, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
