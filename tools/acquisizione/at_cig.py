#!/usr/bin/env python3
"""L4: CIG nelle sezioni «Bandi di gara e contratti» di Amministrazione trasparente (#57).

Per i CIG del residuo S6 senza link PVL (quasi tutti precedenti al 2024), a partire dagli importi maggiori:
1. CF della stazione appaltante dai CIG ANAC (lavoro/cig_completo, duckdb 6 GB, 2 thread);
2. URL della sezione AT dalla tabella enti del monitor AT (lavoro/trasparenza/stato.sqlite: registro L.190 e
   IndicePA da CKAN JSON, tools/trasparenza/fonti.py); in mancanza il sito istituzionale IndicePA;
3. un giro per ENTE (non per CIG): pagina AT -> link «Bandi di gara e contratti» -> fino a MAX_SOTTO sottopagine
   pertinenti (gare, bandi, contratti, affidamenti, esiti, determine, anni); su ogni pagina si cercano TUTTI i CIG
   dell'ente; per i CIG trovati si scaricano i documenti collegati (piattaforme_cig.documenti_pagina);
4. robots.txt: le sezioni AT sono esenti (AGENTS.md §3, art. 9 d.lgs. 33/2013); se robots.txt le esclude si passa
   solo in orari di poco carico (ORE_AT) e robots.txt si archivia come evidenza. >= 5 s per host, 10 host insieme,
   mai login/CAPTCHA, blocchi registrati come esito.
Uso (server): SPESAICT_BASE=$PWD nice .venv/bin/python tools/acquisizione/at_cig.py lavoro/residuo-s6/ingresso.csv lavoro/residuo-s6/l4
Uscita: l4/enti.jsonl (una riga per ente), l4/esiti.jsonl (una riga per CIG); atti che citano il CIG in dati/atti (L4).
Ripartibile: gli enti già in enti.jsonl si saltano. Guardia disco GUARDIA_GB (15).
"""
import csv, json, os, re, shutil, sqlite3, sys, threading, time, html
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urljoin, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
import piattaforme_cig as P  # noqa: E402
import requests  # noqa: E402

R = P.RADICE
BASE = Path(os.environ.get("SPESAICT_BASE", R))
MAX_SOTTO = int(os.environ.get("MAX_SOTTO", "20"))
RX_BANDI = re.compile(r"bandi[\s_-]*(di[\s_-]*)?gar[ae]|bandi.{0,8}contratt|gare[\s_-]*e[\s_-]*contratti|ricerca[\s_-]*gare|bandi[\s_-]*e[\s_-]*gare", re.I)
RX_AT = re.compile(r"amministrazione[\s_-]*trasparente|trasparenza", re.I)
RX_SOTTO = re.compile(r"gar[ae]|band|contratt|affidament|esit|determin|aggiudic|avvis|20(1[89]|2[0-6])", re.I)
RX_CIG = re.compile(r"\b[0-9A-Z]{10}\b")
csv.field_size_limit(10**9)


RX_REFRESH = re.compile(r"http-equiv=[\"']?refresh[\"']?[^>]*url=([^\"'>\s]+)|(?:window\.)?location(?:\.href)?\s*=\s*[\"']([^\"']+)[\"']", re.I)


def prendi_seg(s, u, out, salti=3):
    """Come P.prendi, ma segue i meta refresh e i redirect JavaScript semplici delle pagine quasi vuote."""
    r, h, t = P.prendi(s, u, out)
    while salti and len(t) < 3000 and (m := RX_REFRESH.search(r.text)):
        salti -= 1; r, h, t = P.prendi(s, urljoin(r.url, html.unescape(m.group(1) or m.group(2))), out)
    return r, h, t


def cf_dei_cig(cigs):
    import duckdb
    c = duckdb.connect(); c.execute("set memory_limit='6GB'; set threads=2; set preserve_insertion_order=false")
    c.execute(f"set temp_directory='{BASE}/lavoro/duck/tmp'")
    c.execute("create temp table t(cig varchar)"); c.executemany("insert into t values (?)", [(x,) for x in cigs])
    fs = sorted(str(p) for p in (BASE / "lavoro/cig_completo").glob("*cig_csv*.csv"))
    return dict(c.execute(f"""select distinct on (cig) cig, cf_amministrazione_appaltante from read_csv({fs}, delim=';', header=true,
        all_varchar=true, ignore_errors=true, union_by_name=true) where cig in (select cig from t)""").fetchall())


def link_con(r, rx):
    for m in re.finditer(r"<a\s[^>]*href=[\"']([^\"'#]+)[\"'][^>]*>(.*?)</a>", r.text, re.I | re.S):
        if rx.search(re.sub(r"<[^>]+>", " ", m.group(2))) or rx.search(m.group(1)):
            yield urljoin(r.url, html.unescape(m.group(1)))


def main():
    ing, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    righe = [r for r in csv.DictReader(open(ing, encoding="utf-8")) if not r["link"]]
    righe.sort(key=lambda r: -float(r["importo"] or 0))
    fatti = {json.loads(l)["cf"] for l in open(out / "enti.jsonl", encoding="utf-8")} if (out / "enti.jsonl").exists() else set()
    cf = cf_dei_cig([r["cig"] for r in righe])
    db = sqlite3.connect(BASE / "lavoro/trasparenza/stato.sqlite")
    enti = {a: (b, c, d) for a, b, c, d in db.execute("select cf, at_url, sito_ipa, denominazione from enti")}
    gruppi = {}
    for r in righe:
        k = cf.get(r["cig"]) or ""
        gruppi.setdefault(k, []).append(r)
    ordine = [k for k in sorted(gruppi, key=lambda k: -max(float(x["importo"] or 0) for x in gruppi[k])) if k not in fatti]
    print(len(righe), "CIG,", len(gruppi), "enti,", len(ordine), "da fare", flush=True)
    stop = threading.Event()
    host_lock = {}

    def scrivi(nome, rec):
        with P.LOCK, open(out / nome, "a", encoding="utf-8") as f: f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    def ente(k):
        if stop.is_set(): return
        if shutil.disk_usage(R).free / 1e9 < P.GUARDIA_GB:
            stop.set(); (out / "STOP-disco.txt").write_text(time.strftime("%FT%T ") + f"sotto {P.GUARDIA_GB} GB\n"); return
        at, sito, den = enti.get(k, ("", "", ""))
        u = P.normalizza(at or sito or "")
        cigs = {r["cig"]: r for r in gruppi[k]}
        e = {"cf": k, "denominazione": den, "at_url": at, "sito_ipa": sito, "cig": len(cigs), "pagine": [], "esito": "", "data": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        trovati = {}
        t0 = time.time()
        h = urlsplit(u).netloc.lower()
        lk = host_lock.setdefault(h, threading.Lock())
        with lk:
            try:
                if not k: e["esito"] = "cf-ignoto"
                elif not u: e["esito"] = "sito-ignoto"
                elif not P.robots_ok(u) and not P.ora_at(): e["esito"] = "rinviato-robots-orario"
                else:
                    if not P.robots_ok(u): e["robots_escluso_at"] = P.robots_evidenza(u, out)
                    s = requests.Session(); s.headers["User-Agent"] = P.UA
                    r, sh, t = prendi_seg(s, u, out); e["pagine"].append({"url": r.url, "sha256": sh})
                    if (b := P.blocco(r, t)): e["esito"] = "blocco"; e["blocco"] = b
                    else:
                        coda = []
                        if not at:   # sito istituzionale: prima la sezione AT
                            coda += list(link_con(r, RX_AT))[:1]
                        coda += list(link_con(r, RX_BANDI))[:2]
                        visti = {r.url}; pagine = [(r, t)]
                        while coda and len(visti) <= MAX_SOTTO:
                            v = coda.pop(0)
                            if v in visti or urlsplit(v).netloc.split(".")[-2:] != urlsplit(r.url).netloc.split(".")[-2:]: continue
                            visti.add(v)
                            try: rr, hh, tt = prendi_seg(s, v, out)
                            except Exception: continue
                            e["pagine"].append({"url": rr.url, "sha256": hh}); pagine.append((rr, tt))
                            if RX_AT.search(rr.url) and not RX_BANDI.search(rr.url): coda = list(link_con(rr, RX_BANDI))[:2] + coda
                            elif RX_BANDI.search(rr.url + tt[:3000]):
                                coda += [x for x in link_con(rr, RX_SOTTO) if x not in visti][:MAX_SOTTO]
                            for c in cigs:
                                if c in tt and c not in trovati: trovati[c] = rr
                        for c in cigs:
                            if c not in trovati and c in t: trovati[c] = r
                        e["esito"] = "cig-trovati" if trovati else ("pagina-quasi-vuota-js" if len(t) < 1500 and len(e["pagine"]) == 1 else "sezione-bandi-raggiunta" if any(RX_BANDI.search(p["url"]) for p in e["pagine"]) else "sezione-bandi-non-trovata")
                        for c, rr in trovati.items():
                            rec = {"cig": c, "documenti": []}
                            P.documenti_pagina(s, c, rr, out, rec)
                            for d in rec["documenti"]:
                                if d.get("cig_presente") and d.get("testo"): P.registra_atto(c, d, "L4", den)
                            scrivi("esiti.jsonl", {"cig": c, "cf": k, "priorita": cigs[c]["priorita"], "importo": cigs[c]["importo"], "pagina": rr.url,
                                                   "documenti": [{**d, "testo": d.get("testo", "")[:500]} for d in rec["documenti"]], "esito": "documenti" if rec["documenti"] else "cig-nella-pagina"})
            except Exception as x:
                e["esito"] = "errore"; e["errore"] = str(x)[:200]
        e["cig_trovati"] = len(trovati); e["secondi"] = round(time.time() - t0, 1)
        e["importo"] = sum(float(x["importo"] or 0) for x in cigs.values()); e["priorita"] = sorted({x["priorita"] for x in cigs.values()})
        if e["esito"] != "rinviato-robots-orario": scrivi("enti.jsonl", e)
        print(k, e["esito"], len(cigs), len(trovati), flush=True)

    with ThreadPoolExecutor(P.PARALLELO) as ex:
        list(ex.map(ente, ordine))
    if not stop.is_set(): (out / "FINITO.txt").write_text(time.strftime("%FT%T\n"))


if __name__ == "__main__":
    main()
