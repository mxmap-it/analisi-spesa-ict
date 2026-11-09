#!/usr/bin/env python3
"""L4-js (#73): ripasso con browser headless degli enti L4 rimasti «pagina-quasi-vuota-js», poi Difesa di notte.

Riusa at_cig.main (stesso giro per ente, stessa ricerca CIG, stessi documenti e stesso formato enti.jsonl/esiti.jsonl)
cambiando solo come si prende una pagina: sempre Chromium headless (visibilita_pa checks.browser_playwright via
at_cig.rendi_js), al massimo BROWSER (2) browser insieme, >= 5 s per host (P.attendi). Se la pagina AT del registro è
vuota o in errore (404, radice di piattaforma, pagina d'errore) si riparte dal sito istituzionale IndicePA e si cerca
la sezione AT con visibilita_pa locate.link_at. Atti che citano il CIG registrati con livello «L4-js».
Fase 1: i 176 enti «pagina-quasi-vuota-js» di l4/enti.jsonl. Fase 2: enti Difesa (difesa.it, esercito.difesa.it) in
errore di rete nel giro L4, solo in ORE_DIFESA (default 1-5), 1 ente alla volta, PAUSA_DIFESA (30) s per host.
Mai login/CAPTCHA/proxy (AGENTS.md §3). Ripartibile: gli enti già in l4-js/enti.jsonl si saltano; progresso in STATO.md.
Uso (server): (SPESAICT_BASE=$PWD setsid nohup nice -n 15 .venv/bin/python tools/acquisizione/at_cig_js.py >> lavoro/residuo-s6/l4-js/giro.log 2>&1 &)
"""
import csv, json, os, sys, threading, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ.setdefault("RICERCA_BROWSER", "1")
import at_cig as A  # noqa: E402
P, LOC, CHK = A.P, A.LOC, A.CHK

BASE = A.BASE
L4 = BASE / "lavoro/residuo-s6/l4"
OUT = BASE / "lavoro/residuo-s6/l4-js"
RX_DIFESA = "difesa.it"
ORE_DIFESA = os.environ.get("ORE_DIFESA", "1-5")
A.JS_LOCK = threading.BoundedSemaphore(int(os.environ.get("BROWSER", "2")))   # max 2 browser insieme
TL = threading.local()
INFO = {}   # cf -> (at_url, sito_ipa)
_bp = CHK.browser_playwright


def bp(*a, **k):   # ricorda lo stato HTTP dell'ultima resa nel filo
    d = _bp(*a, **k); TL.status = d.get("status"); TL.errore = d.get("errore", ""); return d


CHK.browser_playwright = bp
_ra = P.registra_atto
P.registra_atto = lambda cig, d, livello, ente: _ra(cig, d, "L4-js", ente)


def povera(t):
    return len(t) < 1500 or (getattr(TL, "status", 200) or 0) >= 400


def prendi_js(s, u, out, salti=3):
    """Pagina resa col browser; prima pagina dell'ente povera -> sito IndicePA -> sezione AT (locate.link_at)."""
    prima = getattr(TL, "prima", False); TL.prima = False
    try:
        r, h, t = A.rendi_js(u, out)
    except Exception:
        TL.status = None; r, h, t = ORIG(s, u, out, salti)   # browser fallito: requests, come L4
    if prima and povera(t):
        at, sito = INFO.get(TL.cf, ("", ""))
        sito = P.normalizza(sito or "")
        if sito and sito.rstrip("/") != u.rstrip("/"):
            try:
                r2, h2, t2 = A.rendi_js(sito, out)
                TL.sito = {"url": r2.url, "sha256": h2, "status": TL.status}
                la = LOC.link_at(r2.text, r2.url).get("url")
                if la:
                    r3, h3, t3 = A.rendi_js(la, out)
                    if not povera(t3): return r3, h3, t3
                if len(t2) > len(t): return r2, h2, t2
            except Exception:
                pass
    return r, h, t


ORIG = A.prendi_seg
A.prendi_seg = prendi_js


class Esecutore(A.ThreadPoolExecutor):
    """Imposta nel filo l'ente corrente (serve a prendi_js per il ripiego sul sito IndicePA)."""
    def map(self, fn, it):
        def f(k):
            TL.cf, TL.prima = k, True
            return fn(k)
        return super().map(f, it)


A.ThreadPoolExecutor = Esecutore


def cf_cache(cigs):
    p = OUT / "cf.json"
    if p.exists(): return json.loads(p.read_text())
    m = _cf(cigs); p.write_text(json.dumps(m)); return m


_cf = A.cf_dei_cig
A.cf_dei_cig = cf_cache


def stato(fase, tot):
    n, c = 0, {}
    if (OUT / "enti.jsonl").exists():
        for l in open(OUT / "enti.jsonl", encoding="utf-8"):
            d = json.loads(l); n += 1; c[d["esito"]] = c.get(d["esito"], 0) + 1
    cig = sum(1 for _ in open(OUT / "esiti.jsonl", encoding="utf-8")) if (OUT / "esiti.jsonl").exists() else 0
    (OUT / "STATO.md").write_text(f"# L4-js (#73): stato\n\nAggiornato {time.strftime('%F %T')}. Fase: {fase}.\n\n"
        f"- enti fatti: {n} / {tot}\n- esiti: {json.dumps(c, ensure_ascii=False)}\n- CIG trovati (righe esiti.jsonl): {cig}\n\n"
        "Ripresa: rilanciare lo stesso comando (docstring di tools/acquisizione/at_cig_js.py); gli enti fatti si saltano.\n",
        encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    vuoti, difesa = {}, {}
    for f in [L4 / "enti.jsonl", *sorted(L4.glob("enti-errori-ripasso-*.jsonl"))]:
        for l in open(f, encoding="utf-8"):
            d = json.loads(l)
            if d["esito"] == "pagina-quasi-vuota-js": vuoti[d["cf"]] = d
            elif d["esito"] == "errore" and RX_DIFESA in (d.get("at_url") or "") + (d.get("sito_ipa") or ""): difesa[d["cf"]] = d
    for d in [*vuoti.values(), *difesa.values()]: INFO[d["cf"]] = (d.get("at_url", ""), d.get("sito_ipa", ""))
    ing = list(csv.DictReader(open(BASE / "lavoro/residuo-s6/ingresso.csv", encoding="utf-8")))
    cf = cf_cache([r["cig"] for r in ing if not r["link"]])
    tot = len(vuoti) + len(difesa)
    for fase, insieme in (("1-js", vuoti), ("2-difesa", difesa)):
        sub = OUT / f"ingresso-{fase}.csv"
        with open(sub, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=ing[0].keys()); w.writeheader()
            w.writerows(r for r in ing if not r["link"] and cf.get(r["cig"]) in insieme)
        if fase == "2-difesa":
            a, b = (int(x) for x in ORE_DIFESA.split("-"))
            while not (a <= time.localtime().tm_hour < b):
                stato("2-difesa in attesa delle ore " + ORE_DIFESA, tot); time.sleep(300)
            P.PARALLELO = 1; P.PAUSA = float(os.environ.get("PAUSA_DIFESA", "30"))
        stato(fase, tot)
        sys.argv = [sys.argv[0], str(sub), str(OUT)]
        fermo = threading.Event()
        threading.Thread(target=lambda: [stato(fase, tot) for _ in iter(lambda: fermo.wait(60), True)], daemon=True).start()
        A.main(); fermo.set()
        (OUT / "FINITO.txt").unlink(missing_ok=True)
        (OUT / f"FINITO-{fase}.txt").write_text(time.strftime("%FT%T\n"))
    stato("finito", tot)


if __name__ == "__main__":
    main()
