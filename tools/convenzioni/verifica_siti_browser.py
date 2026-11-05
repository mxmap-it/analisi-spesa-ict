"""#62: verifica con browser reale (Playwright + Chrome headless) di home e sezioni AT di centrali, aggregatori ed enti (casi R44).
Per ogni URL: stato HTTP, titolo, presenza del link «trasparen» nel DOM renderizzato (anche se generato in JS), segni di
challenge/CAPTCHA/login (NON risolti), sha256 dell'HTML renderizzato e del testo; HTML salvato in lavoro/ (fuori git).
Ritmo: >= 5 s fra le pagine. Uscite: report/convenzioni/enti-campione/siti-browser-<data>.csv e righe in
report/convenzioni/blocchi-accesso.csv per ogni blocco (CAPTCHA, login, registrazione, challenge).
Uso: python tools/convenzioni/verifica_siti_browser.py elenco.csv   (colonne: iniziativa,ente,url)"""
import csv
import hashlib
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

R = Path(__file__).resolve().parent.parent.parent
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36 "
      "analisi-spesa-ict (+https://github.com/mxmap-it/analisi-spesa-ict)")
SEGNI = {
    "CAPTCHA": r"captcha|recaptcha|hcaptcha|mosparo|turnstile",
    "challenge": r"just a moment|checking your browser|verifica.{0,20}browser|attention required|ddos protection|access denied|richiesta bloccata|request rejected|incapsula|radware|imperva",
    "login": r"effettua (il )?login|accedi per (vedere|visualizzare|scaricare)|area riservata|inserisci (username|nome utente) e password",
    "registrazione SPID o account": r"accedi con spid|entra con spid|registrati per",
}
BLOCCHI = R / "report/convenzioni/blocchi-accesso.csv"
CAMPI_B = ["url", "iniziativa", "cosa_dietro", "tipo_blocco", "data", "http", "evidenza_sha256", "evidenza_file", "note"]


def main(elenco):
    oggi = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out = R / f"report/convenzioni/enti-campione/siti-browser-{oggi}.csv"
    lav = R / "lavoro/convenzioni/siti-browser"
    lav.mkdir(parents=True, exist_ok=True)
    nuovo_b = not BLOCCHI.exists()
    righe = []
    with sync_playwright() as p, open(BLOCCHI, "a", newline="", encoding="utf-8") as fb:
        wb = csv.DictWriter(fb, fieldnames=CAMPI_B)
        if nuovo_b:
            wb.writeheader()
        b = p.chromium.launch(channel="chrome", headless=True)
        ctx = b.new_context(user_agent=UA, locale="it-IT")
        page = ctx.new_page()
        for r in csv.DictReader(open(elenco, encoding="utf-8")):
            rec = {"iniziativa": r["iniziativa"], "ente": r["ente"], "url": r["url"], "data": datetime.now(timezone.utc).isoformat(timespec="seconds")}
            try:
                resp = page.goto(r["url"], wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(6000)
                html = page.content()
                testo = page.inner_text("body") if page.locator("body").count() else ""
                rec["http"] = resp.status if resp else ""
                rec["titolo"] = page.title()[:120]
                rec["link_at_nel_dom"] = "si" if re.search(r'href="[^"]*trasparen', html, re.I) or re.search(r"trasparen", testo, re.I) else "no"
                sha = hashlib.sha256(html.encode("utf-8")).hexdigest()
                (lav / f"{sha}.html").write_text(html, encoding="utf-8")
                rec["sha256_html"] = sha
                tipo = next((t for t, rx in SEGNI.items() if re.search(rx, (testo + " " + rec["titolo"])[:20000], re.I)), "")
                rec["blocco"] = tipo
                if tipo or (rec["http"] in (401, 403, 429, 503)):
                    wb.writerow({"url": r["url"], "iniziativa": r["iniziativa"], "cosa_dietro": r.get("cosa_dietro", "home o sezione AT dell'ente"),
                                 "tipo_blocco": tipo or f"HTTP {rec['http']}", "data": rec["data"], "http": rec["http"], "evidenza_sha256": sha,
                                 "evidenza_file": f"lavoro/convenzioni/siti-browser/{sha}.html (server)", "note": "non risolto (AGENTS.md §3)"})
            except Exception as e:
                rec["errore"] = str(e)[:200]
            righe.append(rec)
            print(rec.get("http"), rec.get("blocco"), rec.get("link_at_nel_dom"), r["url"], rec.get("errore", "")[:80], flush=True)
            time.sleep(5)
        b.close()
    campi = ["iniziativa", "ente", "url", "data", "http", "titolo", "link_at_nel_dom", "blocco", "sha256_html", "errore"]
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campi)
        w.writeheader()
        for x in righe:
            w.writerow({k: x.get(k, "") for k in campi})


if __name__ == "__main__":
    main(sys.argv[1])
