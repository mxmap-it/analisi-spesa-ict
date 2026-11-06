"""#62 fuori piattaforma, passo 2: per ogni iniziativa con righe di criticità 3 apre con browser reale (Playwright + Chrome headless)
le pagine «documenti di gara» (PVL) dei CIG derivati degli enti aderenti, cerca allegati pertinenti (offerta, listino, ordinativo/ODA,
contratto esecutivo/attuativo, piano dei fabbisogni, preventivo, adesione), li archivia con tools/archivia.py (sha256) e ne legge il
testo (pdftotext) per confermare il contenuto (livello V).
Ordine: 17 iniziative «pagina-non-trovata» degli aggregatori, poi altre non Consip, poi Consip. Max MAXP pagine per iniziativa,
hosts diversi preferiti; >= 5 s fra richieste allo stesso host; mai login/CAPTCHA (si registra il blocco).
Ripartibile: progresso in lavoro/convenzioni/fuori-piattaforma/pagine.jsonl e allegati.jsonl (righe già fatte saltate).
Uso (server): nice .venv/bin/python tools/convenzioni/fuori_piattaforma_cerca.py"""
import csv, json, re, subprocess, sys, time, hashlib
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import requests
import archivia as A
from playwright.sync_api import sync_playwright

R = Path(__file__).resolve().parent.parent.parent
L = R / "lavoro/convenzioni/fuori-piattaforma"
MAXP = 6
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36 "
      "analisi-spesa-ict (+https://github.com/mxmap-it/analisi-spesa-ict)")
KW = re.compile(r"offert|listino|ordinativ|ordine|\boda\b|contratto (esecutivo|attuativo|applicativo|di fornitura)|contratto|"
                r"piano dei fabbisogni|fabbisogn|preventiv|adesione|determin|delibera|progetto", re.I)
DOC = re.compile(r"\.(pdf|p7m|zip|docx?|xlsx?|odt)(\?|$)|download|allegat|getfile|scarica|attachment", re.I)
SEGNI = {"CAPTCHA": r"captcha|recaptcha|hcaptcha|turnstile", "challenge": r"just a moment|checking your browser|access denied|request rejected|radware|imperva|incapsula",
         "login": r"effettua (il )?login|area riservata|inserisci (username|nome utente) e password|accedi con spid"}
ultimo = defaultdict(float)


def attendi(host):
    d = time.time() - ultimo[host]
    if d < 5.5:
        time.sleep(5.5 - d)
    ultimo[host] = time.time()


def fatti(p):
    return {json.loads(l)["chiave"] for l in open(p, encoding="utf-8")} if p.exists() else set()


def main():
    agg = {r["iniziativa"] for r in csv.DictReader(open(L / "input/aggregatori-2026-11-07.csv", encoding="utf-8")) if r["esito"] == "pagina-non-trovata"}
    der = defaultdict(list)
    for r in csv.DictReader(open(L / "derivati.csv", encoding="utf-8")):
        if r["link"].startswith("http"):
            der[r["iniziativa"]].append(r)
    ordine = sorted(der, key=lambda i: (0 if i in agg else 1 if not i.startswith("consip") else 2, i))
    pf, af = L / "pagine.jsonl", L / "allegati.jsonl"
    pd, ad = fatti(pf), fatti(af)
    sess = requests.Session()
    (L / "testi").mkdir(exist_ok=True); (L / "html").mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        ctx = b.new_context(user_agent=UA, locale="it-IT")
        page = ctx.new_page()
        for i in ordine:
            # derivati recenti, host diversi
            vis, scelti = set(), []
            for r in sorted(der[i], key=lambda r: r["anno"], reverse=True):
                h = urlsplit(r["link"]).netloc
                if h not in vis and len(scelti) < MAXP:
                    vis.add(h); scelti.append(r)
            for r in scelti:
                chiave = f"{i}|{r['cig']}"
                if chiave in pd:
                    continue
                rec = {"chiave": chiave, "iniziativa": i, "cig": r["cig"], "ente": r["ente"], "url": r["link"],
                       "data": datetime.now(timezone.utc).isoformat(timespec="seconds"), "link": []}
                try:
                    attendi(urlsplit(r["link"]).netloc)
                    resp = page.goto(r["link"], wait_until="domcontentloaded", timeout=60000)
                    page.wait_for_timeout(5000)
                    html = page.content(); testo = page.inner_text("body") if page.locator("body").count() else ""
                    rec["http"] = resp.status if resp else ""
                    sha = hashlib.sha256(html.encode()).hexdigest(); (L / "html" / f"{sha}.html").write_text(html, encoding="utf-8")
                    rec["sha256_html"] = sha
                    rec["blocco"] = next((t for t, rx in SEGNI.items() if re.search(rx, testo[:20000], re.I)), "")
                    rec["cig_in_pagina"] = r["cig"] in testo or r["cig"] in html
                    for a in page.query_selector_all("a[href]")[:3000]:
                        try:
                            href = a.get_attribute("href") or ""; t = (a.inner_text() or "").strip()[:200]
                        except Exception:
                            continue
                        u = urljoin(page.url, href)
                        if u.startswith("http") and DOC.search(u + " " + t) and KW.search(t + " " + u):
                            rec["link"].append({"url": u, "testo": t})
                except Exception as e:
                    rec["errore"] = str(e)[:200]
                with open(pf, "a", encoding="utf-8") as f:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                print(i, r["cig"], rec.get("http"), rec.get("blocco"), len(rec["link"]), rec.get("errore", "")[:60], flush=True)
                for d in rec["link"][:8]:
                    k2 = f"{i}|{d['url']}"
                    if k2 in ad:
                        continue
                    attendi(urlsplit(d["url"]).netloc)
                    a = A.archivia(sess, d["url"]); A.scrivi_manifest(a)
                    out = {"chiave": k2, "iniziativa": i, "cig": r["cig"], "ente": r["ente"], "url_pagina": r["link"], **d,
                           "esito": a.get("esito"), "sha256": a.get("sha256", ""), "errore": a.get("errore", ""), "tipo": a.get("tipo", "")}
                    if out["sha256"]:
                        blob = A.percorso_blob(out["sha256"])
                        try:
                            txt = subprocess.run(["pdftotext", "-l", "30", str(blob), "-"], capture_output=True, timeout=120).stdout.decode("utf-8", "replace")
                        except Exception:
                            txt = ""
                        (L / "testi" / f"{out['sha256']}.txt").write_text(txt, encoding="utf-8")
                        out["parole"] = {k: len(re.findall(rx, txt, re.I)) for k, rx in {
                            "offerta_economica": r"offerta economica", "offerta_tecnica": r"offerta tecnica", "listino": r"listino",
                            "prezzi": r"prezz[oi] unitari|€\s?\d", "ordinativo": r"ordinativo|ordine diretto|\bODA\b|ordine di fornitura",
                            "piano_fabbisogni": r"piano dei fabbisogni", "progetto_fabbisogni": r"progetto dei fabbisogni|progetto esecutivo",
                            "contratto_esecutivo": r"contratto (esecutivo|attuativo|applicativo)", "transato": r"erosione|massimale residuo|transato",
                            "cig_padre": re.escape(r["padre"]), "cig": re.escape(r["cig"])}.items()}
                        out["pagine_testo"] = txt.count("\f")
                    with open(af, "a", encoding="utf-8") as f:
                        f.write(json.dumps(out, ensure_ascii=False) + "\n")
                    print("   ", out["esito"], out.get("parole", ""), d["url"][:100], flush=True)
        b.close()
    print("FINE", flush=True)


if __name__ == "__main__":
    main()
