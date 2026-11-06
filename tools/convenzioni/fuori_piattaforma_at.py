"""#62 fuori piattaforma, passo 4: visita della sezione «Amministrazione trasparente → Bandi di gara e contratti» (e Provvedimenti)
degli enti aderenti alle iniziative con righe di criticità 3, alla ricerca degli atti dei loro CIG derivati (determina di adesione,
contratto esecutivo, ordinativo, piano dei fabbisogni, offerta/listino allegati).

Sito dell'ente: IndicePA via CKAN JSON API (datastore_search sul dataset «Enti», campo Sito_istituzionale; cache ipa.json).
Ordine: i 10 enti con più adesioni senza link PVL, poi tutti gli altri per numero di adesioni decrescente, a blocchi di 20;
ci si ferma dopo un blocco intero a resa zero (nessun atto trovato).
Regole (AGENTS.md §3): browser reale (Playwright + Chrome headless), UA da browser con URL del progetto, >= 5,5 s fra richieste allo
stesso host (lock su file condiviso fra i processi), max WORKER processi; mai login/CAPTCHA/registrazioni/proxy: il blocco si registra.
Ripartibile: un record per ente in <dir>/at-visite.jsonl, allegati in <dir>/at-allegati.jsonl (enti già fatti saltati).
Uso (server): ARCHIVIO_ROOT=... nice .venv/bin/python fuori_piattaforma_at.py <dir con derivati.csv e trovati-2026-11-07.csv>"""
import csv, fcntl, hashlib, json, os, re, subprocess, sys, time
from collections import defaultdict
from datetime import datetime, timezone
from multiprocessing import Pool
from pathlib import Path
from urllib.parse import urljoin, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import requests
import archivia as A

L = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
WORKER, BLOCCO, PRIMI = 5, 20, 10
MAXSUB, MAXDOC = 10, 6
IPA = "https://indicepa.gov.it/ipa-dati/api/3/action/datastore_search"
IPA_RES = "d09adf99-dc10-4349-8c53-27b1e5aa97b6"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36 "
      "analisi-spesa-ict (+https://github.com/mxmap-it/analisi-spesa-ict)")
RX_AT = re.compile(r"amministrazione\s+trasparente|societ[aà]\s+trasparente|ente\s+trasparente|trasparenza", re.I)
RX_BANDI = re.compile(r"bandi\s+di\s+gara|bandi\s+e\s+contratti|gare\s+e\s+contratti", re.I)
RX_PROVV = re.compile(r"^\s*provvedimenti|albo\s+pretorio|determin", re.I)
RX_SUB = re.compile(r"atti delle amministrazioni|affidament|determin|provvediment|delibere? a contrarre|adesion|convenzion|consip|"
                    r"contratti|esiti|aggiudicazion|202[3-6]|ricerca|elenco|archivio", re.I)
DOC = re.compile(r"\.(pdf|p7m|zip|docx?|xlsx?|odt)(\?|$)|download|allegat|getfile|scarica|attachment|documento", re.I)
KW = re.compile(r"offert|listino|ordinativ|ordine|\boda\b|contratt|fabbisogn|preventiv|adesion|determin|decreto|delibera|progetto|"
                r"atto|provvedimento|allegat", re.I)
SEGNI = {"CAPTCHA": r"captcha|recaptcha|hcaptcha|turnstile|authentic user check", "challenge": r"just a moment|checking your browser|access denied|request rejected|radware|imperva|incapsula|attention required",
         "login": r"inserisci (username|nome utente) e password|accedi con spid per (visualizzare|consultare)"}
PAROLE = {"ordinativo": r"ordinativo|ordine diretto|\bODA\b|ordine di (fornitura|acquisto)", "contratto_esecutivo": r"contratto (esecutivo|attuativo|applicativo|specifico)",
          "piano_fabbisogni": r"piano dei fabbisogni", "progetto_fabbisogni": r"progetto dei fabbisogni|progetto esecutivo",
          "offerta_economica": r"offerta economica", "offerta_tecnica": r"offerta tecnica", "listino": r"listino", "prezzi": r"prezz[oi] unitari",
          "transato": r"erosione|massimale residuo|transato", "adesione": r"adesione|aderire", "convenzione": r"convenzione|accordo quadro"}
LOCK = L / "at-host"


def attendi(url):
    """>= 5,5 s fra richieste allo stesso host, anche fra processi diversi."""
    h = urlsplit(url).netloc.lower() or "x"
    LOCK.mkdir(exist_ok=True)
    with open(LOCK / re.sub(r"[^a-z0-9.-]", "_", h), "a+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0); t = float(f.read() or 0)
        d = time.time() - t
        if d < 5.5:
            time.sleep(5.5 - d)
        f.seek(0); f.truncate(); f.write(str(time.time())); f.flush()
        fcntl.flock(f, fcntl.LOCK_UN)


def ipa():
    p = L / "ipa.json"
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    out, off = {}, 0
    while True:
        r = requests.get(IPA, params={"resource_id": IPA_RES, "limit": 5000, "offset": off,
                                      "fields": "Codice_fiscale_ente,Denominazione_ente,Sito_istituzionale,Codice_IPA"}, timeout=120).json()["result"]
        for x in r["records"]:
            out.setdefault(x["Codice_fiscale_ente"], x)
        off += 5000
        if off >= r["total"]:
            break
        time.sleep(5.5)
    json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False)
    return out


def enti_ordinati():
    crit3 = {r["iniziativa"] for r in csv.DictReader(open(L / "trovati-2026-11-07.csv", encoding="utf-8"))}
    e = defaultdict(lambda: {"cig": [], "link": False, "ente": "", "ini": set()})
    for r in csv.DictReader(open(L / "derivati.csv", encoding="utf-8")):
        if r["iniziativa"] in crit3 and r["cf_ente"]:
            x = e[r["cf_ente"]]; x["cig"].append((r["cig"], r["iniziativa"], r["padre"], r["oggetto"])); x["ente"] = r["ente"]; x["ini"].add(r["iniziativa"])
            x["link"] |= r["link"].startswith("http")
    tutti = sorted(e, key=lambda c: (-len(e[c]["cig"]), c))
    primi = [c for c in tutti if not e[c]["link"]][:PRIMI]
    return [(c, e[c]) for c in primi + [c for c in tutti if c not in primi]]


def blocco_di(testo, status):
    if status in (401, 403, 428, 429, 503):
        return f"HTTP {status}"
    return next((t for t, rx in SEGNI.items() if re.search(rx, testo[:20000], re.I)), "")


def apri(page, url):
    attendi(url)
    resp = page.goto(url, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(3500)
    html = page.content()
    testo = page.inner_text("body") if page.locator("body").count() else ""
    links = []
    for a in page.query_selector_all("a[href]")[:4000]:
        try:
            links.append((urljoin(page.url, a.get_attribute("href") or ""), (a.inner_text() or "").strip()[:200]))
        except Exception:
            pass
    sha = hashlib.sha256(html.encode()).hexdigest()
    (L / "at-html").mkdir(exist_ok=True); (L / "at-html" / f"{sha}.html").write_text(html, encoding="utf-8")
    return {"url": page.url, "http": resp.status if resp else "", "testo": testo, "html": html, "links": links, "sha256": sha}


def scegli(links, rx, base=None):
    c = [(u, t) for u, t in links if u.startswith("http") and rx.search(t)]
    c.sort(key=lambda x: (len(x[1]), 0 if base and urlsplit(x[0]).netloc == base else 1))
    return c[0] if c else None


def visita(arg):
    cf, info, sito = arg
    from playwright.sync_api import sync_playwright
    rec = {"cf_ente": cf, "ente": info["ente"], "sito_ipa": sito, "data": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "n_cig": len(info["cig"]), "pagine": [], "cig_trovati": {}, "allegati": [], "blocco": "", "esito_sezione": ""}
    cigs = {c for c, *_ in info["cig"]}
    if not sito:
        rec["esito_sezione"] = "sito-assente-ipa"; return rec
    url = sito if sito.startswith("http") else "https://" + sito.strip("/")
    sess = requests.Session(); sess.headers["User-Agent"] = UA
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        page = b.new_context(user_agent=UA, locale="it-IT", ignore_https_errors=True).new_page()

        def passo(u, ruolo):
            try:
                x = apri(page, u)
            except Exception as e:
                rec["pagine"].append({"ruolo": ruolo, "url": u, "errore": str(e)[:160]}); return None
            bl = blocco_di(x["testo"], x["http"])
            trov = sorted(c for c in cigs if c in x["testo"] or c in x["html"])
            rec["pagine"].append({"ruolo": ruolo, "url": x["url"], "http": x["http"], "sha256": x["sha256"], "blocco": bl, "cig": trov})
            if bl and not rec["blocco"]:
                rec["blocco"] = bl; rec["url_blocco"] = x["url"]; rec["sha_blocco"] = x["sha256"]; rec["http_blocco"] = x["http"]
            for c in trov:
                rec["cig_trovati"].setdefault(c, x["url"])
            x["cig"] = trov; x["blocco"] = bl
            return x

        try:
            home = passo(url, "home")
            if home and not home["blocco"]:
                base = urlsplit(home["url"]).netloc
                at = scegli(home["links"], RX_AT, base)
                atp = passo(at[0], "at") if at else None
                sez = None
                if atp and not atp["blocco"]:
                    bnd = scegli(atp["links"], RX_BANDI, base)
                    sez = passo(bnd[0], "bandi") if bnd else None
                    pv = scegli(atp["links"], RX_PROVV, base)
                    if pv:
                        provv = passo(pv[0], "provvedimenti")
                    else:
                        provv = None
                else:
                    bnd = scegli(home["links"], RX_BANDI, base)
                    sez = passo(bnd[0], "bandi") if bnd else None
                    provv = None
                rec["url_sezione_at"] = sez["url"] if sez else (atp["url"] if atp else "")
                rec["http"] = sez["http"] if sez else (atp["http"] if atp else "")
                rec["esito_sezione"] = ("bloccata" if rec["blocco"] else "bandi-raggiunta" if sez else "at-senza-bandi" if atp else "at-non-trovata")
                # sottopagine pertinenti della sezione bandi (atti, affidamenti, anni, adesioni)
                visti = {q["url"] for q in rec["pagine"]}
                coda = []
                for x in [sez, provv]:
                    if x and not x["blocco"]:
                        coda += [(u, t) for u, t in x["links"] if u.startswith("http") and RX_SUB.search(t) and u not in visti and not DOC.search(u)]
                pagine_cig = [x for x in [home, atp, sez, provv] if x and x["cig"]]
                n = 0
                for u, t in coda:
                    if n >= MAXSUB or rec["blocco"]:
                        break
                    if u in visti:
                        continue
                    visti.add(u); n += 1
                    x = passo(u, "sotto:" + t[:40])
                    if x and x["cig"]:
                        pagine_cig.append(x)
                # pagine con CIG: segui il dettaglio col CIG nel testo del link, poi raccogli allegati
                docs = []
                for x in pagine_cig[:6]:
                    for u, t in x["links"]:
                        if any(c in t for c in cigs) and u not in visti and not DOC.search(u) and len(rec["pagine"]) < 30:
                            visti.add(u); y = passo(u, "dettaglio-cig")
                            if y:
                                docs += [(u2, t2, y["url"], y["cig"]) for u2, t2 in y["links"] if DOC.search(u2 + " " + t2) and KW.search(t2 + " " + u2)]
                    docs += [(u, t, x["url"], x["cig"]) for u, t in x["links"] if DOC.search(u + " " + t) and KW.search(t + " " + u)
                             and (any(c in t for c in cigs) or len(x["cig"]) and x["url"] != (home or {}).get("url"))]
                seen = set()
                for u, t, pu, pc in docs:
                    if u in seen or len(seen) >= MAXDOC * max(1, len(rec["cig_trovati"])) or len(seen) >= 24:
                        continue
                    seen.add(u)
                    attendi(u)
                    a = A.archivia(sess, u); A.scrivi_manifest(a)
                    d = {"url": u, "testo": t, "url_pagina": pu, "cig_pagina": pc, "esito": a.get("esito"), "sha256": a.get("sha256", ""), "tipo": a.get("tipo", "")}
                    if d["sha256"]:
                        try:
                            txt = subprocess.run(["pdftotext", "-l", "30", str(A.percorso_blob(d["sha256"])), "-"], capture_output=True, timeout=120).stdout.decode("utf-8", "replace")
                        except Exception:
                            txt = ""
                        (L / "at-testi").mkdir(exist_ok=True); (L / "at-testi" / f"{d['sha256']}.txt").write_text(txt, encoding="utf-8")
                        d["parole"] = {k: len(re.findall(rx, txt, re.I)) for k, rx in PAROLE.items()}
                        d["cig_nel_testo"] = sorted(c for c in cigs if c in txt)
                        d["padri_nel_testo"] = sorted({pa for c, i, pa, o in info["cig"] if pa and pa in txt})
                    rec["allegati"].append(d)
            elif home:
                rec["esito_sezione"] = "bloccata"; rec["url_sezione_at"] = home["url"]; rec["http"] = home["http"]
            else:
                rec["esito_sezione"] = "sito-irraggiungibile"
        finally:
            b.close()
    return rec


def main():
    fatti = {json.loads(l)["cf_ente"] for l in open(L / "at-visite.jsonl", encoding="utf-8")} if (L / "at-visite.jsonl").exists() else set()
    ip = ipa()
    enti = enti_ordinati()
    print("enti", len(enti), "già fatti", len(fatti), flush=True)
    stato = L / "at-blocchi.jsonl"
    for k in range(0, len(enti), BLOCCO):
        blocco = enti[k:k + BLOCCO]
        todo = [(c, {**i, "ini": sorted(i["ini"])}, (ip.get(c) or {}).get("Sito_istituzionale") or "") for c, i in blocco if c not in fatti]
        if todo:
            with Pool(WORKER) as pool, open(L / "at-visite.jsonl", "a", encoding="utf-8") as f:
                for rec in pool.imap_unordered(visita, todo):
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush()
                    print(k // BLOCCO, rec["cf_ente"], rec["ente"][:40], rec["esito_sezione"], rec["blocco"], len(rec["cig_trovati"]), len(rec["allegati"]), flush=True)
        recs = {json.loads(l)["cf_ente"]: json.loads(l) for l in open(L / "at-visite.jsonl", encoding="utf-8")}
        resa = sum(1 for c, _ in blocco if recs.get(c, {}).get("cig_trovati") or any(a.get("sha256") for a in recs.get(c, {}).get("allegati", [])))
        with open(stato, "a", encoding="utf-8") as f:
            f.write(json.dumps({"blocco": k // BLOCCO, "enti": len(blocco), "resa_enti": resa, "data": datetime.now(timezone.utc).isoformat(timespec="seconds")}) + "\n")
        print("BLOCCO", k // BLOCCO, "resa", resa, flush=True)
        if resa == 0 and k >= PRIMI:
            print("STOP: blocco a resa zero", flush=True); break
    print("FINE", flush=True)


if __name__ == "__main__":
    main()
