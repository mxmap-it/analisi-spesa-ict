"""#62: secondo tentativo sul «Massimale residuo» delle schede pubbliche di acquistinretepa.
Attesa esplicita della risposta XHR di iniziativaservices/getDettaglioLotti (fino a 90 s), poi prova a scegliere ogni lotto nel
menu «Seleziona Lotto» e a premere «Cerca», registrando ogni risposta JSON (sha256) e il testo della sezione.
Modalità: headless (default) oppure --visibile (Chrome con finestra, da lanciare con xvfb-run, di notte a carico basso).
Uscita: report/convenzioni/aretepa/residuo-<modo>.jsonl (una riga per scheda). Senza login, nessun CAPTCHA.
Uso: python tools/convenzioni/aretepa_residuo.py [--visibile] [--solo SIGEF,SIGEF]"""
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

R = Path(__file__).resolve().parent.parent.parent
OUT = R / "report/convenzioni/aretepa"
LAV = R / "lavoro/convenzioni/aretepa/risposte"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36 "
      "analisi-spesa-ict (+https://github.com/mxmap-it/analisi-spesa-ict)")


def salva(corpo):
    sha = hashlib.sha256(corpo).hexdigest()
    LAV.mkdir(parents=True, exist_ok=True)
    (LAV / f"{sha}.json").write_bytes(corpo)
    return sha


def main():
    visibile = "--visibile" in sys.argv
    solo = set(sys.argv[sys.argv.index("--solo") + 1].split(",")) if "--solo" in sys.argv else None
    schede = [json.loads(f.read_text(encoding="utf-8")) for f in sorted((OUT / "schede").glob("*.json"))]
    dest = OUT / f"residuo-{'visibile' if visibile else 'headless'}.jsonl"
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=not visibile)
        ctx = b.new_context(user_agent=UA, locale="it-IT", viewport={"width": 1400, "height": 1000})
        page = ctx.new_page()
        for d in schede:
            if solo and str(d["cdSigef"]) not in solo:
                continue
            rec = {"cdSigef": d["cdSigef"], "url": d["url"], "data": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                   "modo": "visibile" if visibile else "headless", "lotti_risposte": [], "opzioni_lotto": [], "righe_tabella": []}
            catturate = []

            def r(resp):
                if "getDettaglioLotti" in resp.url or "Residuo" in resp.url or "residuo" in resp.url.lower() or "Massimal" in resp.url:
                    try:
                        corpo = resp.body()
                        catturate.append({"url": resp.url, "http": resp.status, "sha256": salva(corpo), "anteprima": corpo[:300].decode("utf-8", "ignore"),
                                          "richiesta": (resp.request.post_data or "")[:500]})
                    except Exception as e:
                        catturate.append({"url": resp.url, "errore": str(e)[:100]})
            page.on("response", r)
            try:
                with page.expect_response(lambda x: "getDettaglioLotti" in x.url, timeout=90000):
                    page.goto(d["url"], wait_until="domcontentloaded", timeout=120000)
                page.wait_for_timeout(15000)
                sel = page.locator("select").filter(has_text="Seleziona")
                if sel.count():
                    opz = sel.first.locator("option").all_inner_texts()
                    rec["opzioni_lotto"] = opz[:50]
                    for o in opz[1:12]:
                        try:
                            sel.first.select_option(label=o)
                            page.locator("button:has-text('Cerca')").first.click(timeout=5000)
                            page.wait_for_timeout(6000)
                        except Exception:
                            pass
                testo = page.inner_text("body")
                i = testo.find("MASSIMALE RESIDUO")
                j = testo.find("Modalità di acquisto", i)
                rec["sezione"] = testo[i: j if j > i else i + 3000] if i >= 0 else ""
                righe = page.locator("table tr").all_inner_texts()
                rec["righe_tabella"] = [x for x in righe if "%" in x or "€" in x][:60]
            except Exception as e:
                rec["errore"] = str(e)[:200]
            page.remove_listener("response", r)
            rec["lotti_risposte"] = catturate
            rec["esito"] = "residuo visibile" if rec["righe_tabella"] or ("Nessun risultato" not in rec.get("sezione", "") and rec.get("sezione")) else "vuoto"
            with open(dest, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            print(d["cdSigef"], rec["esito"], len(rec["opzioni_lotto"]), "opzioni;", [c.get("anteprima", "")[:120] for c in catturate][:2], flush=True)
            time.sleep(5)
        b.close()


if __name__ == "__main__":
    main()
