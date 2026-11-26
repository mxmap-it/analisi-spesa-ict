"""Indisponibilità persistente (#85): prova la home IndicePA (e il dominio della PEC) degli enti persistenti, un GET per host.
Ingressi: lavoro/trasparenza/stato.sqlite, lavoro/trasparenza/persistenti-2026-11.json. Uscita: lavoro/indisponibilita/home.jsonl
Uso: python tools/verifiche/indisponibilita_home.py"""
import json, sqlite3, sys, time, hashlib, concurrent.futures as F
from urllib.parse import urlsplit
import requests
sys.path.insert(0, "tools/trasparenza"); from comune import UA_BOT
c = sqlite3.connect("lavoro/trasparenza/stato.sqlite"); c.row_factory = sqlite3.Row
per = set(json.load(open("lavoro/trasparenza/persistenti-2026-11.json")))
h = lambda u: (urlsplit(u if "://" in u else "http://" + u).hostname or "").lower() if u else ""
def prova(u):
    try:
        r = requests.get(u, headers={"User-Agent": UA_BOT}, timeout=(10, 25), allow_redirects=True)
        return {"url": u, "status": r.status_code, "finale": r.url, "byte": len(r.content)}
    except Exception as e:
        return {"url": u, "status": None, "errore": f"{type(e).__name__}: {e}"[:160]}
enti = [dict(r) for r in c.execute("select cf,denominazione,sito_ipa,pec_ipa,at_url from enti") if r["cf"] in per]
def lavora(e):
    out = {"cf": e["cf"], "at_host": h(e["at_url"]), "ipa_host": h(e["sito_ipa"])}
    dom = (e["pec_ipa"] or "").split("@")[-1].lower()
    out["pec_dominio"] = dom
    if e["sito_ipa"]:
        out["ipa"] = prova(e["sito_ipa"] if "://" in e["sito_ipa"] else "http://" + e["sito_ipa"])
    if dom and not dom.startswith(("pec.", "legalmail", "postacert", "cert.", "pcert", "arubapec", "pec")) and dom not in (out["ipa_host"], out["at_host"]):
        out["pec_sito"] = prova("https://www." + dom.split("pec.")[-1])
    time.sleep(5)
    return out
with F.ThreadPoolExecutor(8) as ex, open("lavoro/indisponibilita/home.jsonl", "w") as f:
    for r in ex.map(lavora, enti):
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(len(enti))
