"""#62: acquistinretepa con un browser reale (Playwright + Chrome, headless), parti pubbliche, senza login né CAPTCHA.

Fase «vetrina»: apre la vetrina delle iniziative (convenzioni, AQ; attive e archivio) e registra le risposte JSON dei servizi
che il client chiama davvero (vetrineservices/*): URL, corpo della richiesta, data, sha256 del corpo della risposta.
Fase «schede»: per ogni idIniziativa apre la scheda pubblica e registra le risposte JSON (dettaglio, documenti, lotti, erosione)
e i link a file (pdf, zip, xlsx...).
Uscite: lavoro/convenzioni/aretepa/risposte/<sha256>.json (contenuto, fuori git), report/convenzioni/aretepa/chiamate.jsonl
(una riga per risposta: fase, id, url, metodo, corpo richiesta, http, data, sha256, dimensione), report/convenzioni/aretepa/
schede/<idIniziativa>.json (riepilogo: titolo, documenti, campi di erosione trovati).
Ripartibile: salta le schede già scritte. Ritmo: >= 4 s fra le pagine, una pagina alla volta.
Uso: python tools/convenzioni/aretepa_browser.py vetrina | schede [--max N]"""
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

R = Path(__file__).resolve().parent.parent.parent
LAV = R / "lavoro/convenzioni/aretepa"
OUT = R / "report/convenzioni/aretepa"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36 "
      "analisi-spesa-ict (+https://github.com/mxmap-it/analisi-spesa-ict)")
BASE = "https://www.acquistinretepa.it"
PAUSA = 4


def adesso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def registra(fase, ident, resp, metodo=None, richiesta=None):
    try:
        corpo = resp.body()
    except Exception:
        return None
    sha = hashlib.sha256(corpo).hexdigest()
    (LAV / "risposte").mkdir(parents=True, exist_ok=True)
    f = LAV / "risposte" / f"{sha}.json"
    if not f.exists():
        f.write_bytes(corpo)
    req = getattr(resp, "request", None)
    metodo = metodo or (req.method if req else "")
    richiesta = richiesta if richiesta is not None else ((req.post_data or "") if req else "")
    rec = {"fase": fase, "id": ident, "url": resp.url, "metodo": metodo, "richiesta": richiesta[:4000],
           "http": resp.status, "data": adesso(), "sha256": sha, "byte": len(corpo)}
    with open(OUT / "chiamate.jsonl", "a", encoding="utf-8") as g:
        g.write(json.dumps(rec, ensure_ascii=False) + "\n")
    try:
        return json.loads(corpo)
    except ValueError:
        return None


def json_servizio(resp):
    ct = resp.headers.get("content-type", "")
    return "acquistinretepa.it" in resp.url and "json" in ct


def vetrina(page):
    """Apre la vetrina (per avere sessione e cookie del client), poi rifà la stessa chiamata POST che il client fa
    (publicservices/vetrineservices/getIniziative) con pagine da 100, per convenzioni e AQ, attive e archivio."""
    raccolti = {}
    page.goto(f"{BASE}/opencms/opencms/vetrina_iniziative.html?filter=CO", wait_until="networkidle", timeout=120000)
    time.sleep(PAUSA)
    for sigla, label in (("CO", "Convenzioni"), ("AQ", "Accordi quadro")):
        for archivio in (False, True):
            for pagina in range(1, 200):
                corpo = {"isArchive": archivio, "strumento": [{"label": label, "id": sigla}], "stato": [], "categoria": [],
                         "tempo": {"dataDa": None, "dataA": None, "stato": []}, "paginazione": {"pagina": pagina, "itemPagina": 100},
                         "orderBy": {"campo": "dataPubblicazione", "verso": "desc"}, "idt": "", "flVisibileVetrina": 1}
                resp = page.request.post(f"{BASE}/publicservices/vetrineservices/getIniziative", data=json.dumps(corpo),
                                         headers={"Content-Type": "application/json"})
                j = registra("vetrina", f"{sigla}-{'archivio' if archivio else 'attive'}-p{pagina}", resp, "POST", json.dumps(corpo))
                el = ((j or {}).get("payload") or {}).get("elencoIniziative") or []
                for it in el:
                    raccolti[str(it["idIniziativa"])] = dict(it, _archivio=archivio)
                time.sleep(PAUSA)
                if len(el) < 100:
                    break
    (OUT / "iniziative.json").write_text(json.dumps(raccolti, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(raccolti), "iniziative dalla vetrina")


def trova_iniziative(j):
    out = []
    if isinstance(j, dict):
        if "idIniziativa" in j:
            out.append(j)
        for v in j.values():
            out += trova_iniziative(v)
    elif isinstance(j, list):
        for v in j:
            out += trova_iniziative(v)
    return out


CHIAVI_EROSIONE = re.compile(r"eros|consum|residu|esaur|massimal|percentual|importo", re.I)


def campi(j, pref=""):
    """Coppie (percorso, valore) dei campi foglia: per trovare erosione e consumato senza conoscere lo schema."""
    if isinstance(j, dict):
        for k, v in j.items():
            yield from campi(v, f"{pref}.{k}" if pref else k)
    elif isinstance(j, list):
        for i, v in enumerate(j[:200]):
            yield from campi(v, f"{pref}[{i}]")
    else:
        yield pref, j


def schede(page, massimo):
    inits = json.loads((OUT / "iniziative.json").read_text(encoding="utf-8"))
    filtro = OUT / "sigef-db.txt"
    if filtro.exists():
        voluti = set(filtro.read_text(encoding="utf-8").split())
        inits = {k: v for k, v in inits.items() if str(v.get("codSigef")) in voluti}
    (OUT / "schede").mkdir(parents=True, exist_ok=True)
    fatte = 0
    for ident, it in inits.items():
        dest = OUT / "schede" / f"{ident}.json"
        if dest.exists():
            continue
        if fatte >= massimo:
            break
        risposte = []

        def su_risposta(resp, ident=ident):
            if json_servizio(resp):
                j = registra("scheda", ident, resp)
                if j is not None:
                    risposte.append((resp.url, j))
        page.on("response", su_risposta)
        url = f"{BASE}/opencms/opencms/scheda_iniziativa.html?idIniziativa={ident}"
        esito = "ok"
        link, residuo, testo, html = [], "", "", ""
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(40000)  # il dettaglio arriva da un servizio lento (vetrineservices/geDettagliotIniziativaDummy)
            # la tabella «Massimale residuo» si popola con «Cerca»: si prova a premerlo (nessun login)
            try:
                sez = page.locator("text=MASSIMALE RESIDUO").first
                sez.scroll_into_view_if_needed(timeout=5000)
                page.locator("button:has-text('Cerca'), input[value='Cerca']").first.click(timeout=5000)
                page.wait_for_timeout(8000)
            except Exception:
                pass
            testo = page.inner_text("body")
            html = page.content()
            link = page.eval_on_selector_all("a[href*='getDocument'], a[href$='.pdf'], a[href$='.zip'], a[href$='.xlsx']",
                                             "els => els.map(e => [e.textContent.trim().slice(0,120), e.href])")
            i = testo.find("MASSIMALE RESIDUO")
            if i >= 0:
                j = testo.find("Modalità di acquisto", i)
                residuo = testo[i: j if j > i else i + 3000]
        except Exception as e:
            esito = f"errore: {str(e)[:150]}"
        page.remove_listener("response", su_risposta)
        visti, docs = set(), []
        for nome, h in link:
            if h not in visti and nome:
                visti.add(h)
                docs.append({"nome": nome, "url": h})
        erosione = [(k, v) for u, j in risposte for k, v in campi(j) if CHIAVI_EROSIONE.search(k) and v not in (None, "", [])]
        login = bool(re.search(r"accedi per|effettua (il )?login|area riservata", testo, re.I))
        dest.write_text(json.dumps({"idIniziativa": ident, "titolo": it.get("titoloIniziativa"), "cdSigef": it.get("codSigef"),
                                    "stato": it.get("stato"), "archivio": it.get("_archivio"), "url": url, "data": adesso(), "esito": esito,
                                    "documenti": docs, "residuo_testo": residuo[:4000], "campi_erosione": erosione[:300],
                                    "servizi": sorted({u for u, _ in risposte}), "testo_sha256": hashlib.sha256(testo.encode()).hexdigest(),
                                    "rimandi_al_login": login, "estratto_testo": testo[:3000]}, ensure_ascii=False, indent=1), encoding="utf-8")
        fatte += 1
        print(ident, it.get("codSigef"), esito[:40], len(docs), "documenti,", len(erosione), "campi erosione,", "residuo:", residuo[:200].replace(chr(10), " | "), flush=True)
        time.sleep(PAUSA)


def main():
    fase = sys.argv[1]
    massimo = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 10 ** 6
    LAV.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        ctx = b.new_context(user_agent=UA, locale="it-IT")
        page = ctx.new_page()
        vetrina(page) if fase == "vetrina" else schede(page, massimo)
        b.close()


if __name__ == "__main__":
    main()
