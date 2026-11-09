#!/usr/bin/env python3
"""Destinatari dell'accesso civico (#58): RPCT e recapiti dalla sezione Amministrazione trasparente, per ente.

Ingresso: esiti/<DATA>/accesso-civico/enti.csv (6.626 enti), in priorità decrescente (priorita_somma).
Fase 1 (senza rete): per i CF senza PEC in IndicePA si cerca il destinatario negli altri file IndicePA del mirror
  (CF dell'amministrazione; CF delle unità di fatturazione/NSO -> amministrazione e UO con PEC; nome identico).
Fase 2 (rete, un ente alla volta, max 10 host insieme, >= 5 s per host): sezione AT (tabella enti del monitor AT,
  lavoro/trasparenza/stato.sqlite; altrimenti sito IndicePA + visibilita_pa locate.link_at) -> pagine «Accesso
  civico», «Altri contenuti», «Prevenzione della corruzione», «Registro degli accessi» (fino a MAX_PAGINE). Ogni
  pagina è archiviata (tools/archivia.py via piattaforme_cig.archivia, sha256). Fetch, refresh/JS, robots e blocchi
  sono quelli di at_cig.py / piattaforme_cig.py / visibilita_pa: qui non si riscrivono.
Attendibilità per campo: A = IndicePA per lo stesso CF (o tabella AT del monitor); B = letto nella pagina AT
  dell'ente (archiviata) accanto all'etichetta pertinente, o IndicePA tramite il CF di un'unità; C = euristica
  (abbinamento per nome, estrazione automatica del nome RPCT, modulo online, link al registro non aperto);
  vuoto = non trovato. I campi C vanno controllati a mano prima dell'invio.
Uso (server): SPESAICT_BASE=$PWD setsid nohup nice -n 15 .venv/bin/python tools/accesso_civico/rpct_destinatari.py 2026-11-09 \
  >> lavoro/accesso-civico-rpct/giro.log 2>&1 &     env: LIMITE=N (primi N enti), HOST_PARALLELI=10, MAX_PAGINE=8.
Ripartibile e idempotente: gli enti già in lavoro/accesso-civico-rpct/enti.jsonl si saltano; destinatari.csv e
  STATO.md si rigenerano da enti.jsonl ogni 25 enti e alla fine. Nessun contatto con gli enti: solo lettura pubblica.
"""
import csv, json, os, re, shutil, sqlite3, sys, threading, time, html
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "acquisizione"))
import at_cig as A  # noqa: E402  (importa piattaforme_cig e visibilita_pa)
P, LOC = A.P, A.LOC
import requests  # noqa: E402

R = P.RADICE
DATA = sys.argv[1] if len(sys.argv) > 1 else time.strftime("%Y-%m-%d")
LAV = R / "lavoro/accesso-civico-rpct"
OUT = R / f"esiti/{DATA}/accesso-civico"
MAX_PAGINE = int(os.environ.get("MAX_PAGINE", "8"))
LIMITE = int(os.environ.get("LIMITE", "0"))
IPA_DIR = R / "archivio/mirror/indicepa.gov.it/ipa-dati/dataset"

RX_ACC = re.compile(r"accesso[\s_-]*civico|accesso[\s_-]*generalizzato|\bfoia\b", re.I)
RX_ALTRI = re.compile(r"altri[\s_-]*contenuti", re.I)
RX_CORR = re.compile(r"prevenzione[\s_-]*(della[\s_-]*)?corruzione|anticorruzione|\brpct\b", re.I)
RX_REG = re.compile(r"registro[\s_-]*(degli[\s_-]*|delle[\s_-]*)?(accessi|richieste[\s_-]*di[\s_-]*accesso)", re.I)
RX_MAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
RX_MOD = re.compile(r"istanza[\s_-]*on[\s_-]*line|compila(re)?[\s_-]*(il[\s_-]*)?modulo[\s_-]*on[\s_-]*line|modulo[\s_-]*on[\s_-]*line|presenta[\s_-]*(la[\s_-]*|una[\s_-]*)?(domanda|istanza|richiesta)[\s_-]*on[\s_-]*line|servizi[\s_-]*on[\s_-]*line|accedi[\s_-]*al[\s_-]*servizio|spid", re.I)
RX_RPCT = re.compile(r"responsabile\s+(della\s+|per\s+la\s+)?prevenzione\s+(della\s+)?corruzione(\s+e\s+(della\s+|per\s+la\s+)?trasparenza)?|\bR\.?P\.?C\.?T\.?\b", re.I)
TITOLI = r"(?:dott(?:\.ssa|oressa|\.)?|dr\.?(?:ssa)?|ing\.|avv\.|arch\.|prof\.(?:ssa)?|sig\.(?:ra)?|rag\.|geom\.)\s*"
RX_NOME = re.compile(r"(" + TITOLI + r")?([A-ZÀ-Ý][a-zà-ÿ']+(?:\s+[A-ZÀ-Ý][a-zà-ÿ']+){1,2}|[A-ZÀ-Ý]{2,}(?:\s+[A-ZÀ-Ý]{2,}){1,2})")
VIETATE = {"amministrazione", "trasparente", "responsabile", "prevenzione", "corruzione", "trasparenza", "piano", "segretario",
           "comunale", "generale", "direttore", "il", "la", "del", "della", "accesso", "civico", "rpct", "ufficio", "sezione",
           "dati", "atti", "decreto", "delibera", "nomina", "anno", "triennale", "ptpct", "piao", "dirigente", "area", "settore",
           "servizio", "documenti", "allegati", "home", "altri", "contenuti", "pubblicazione", "aggiornamento", "data",
           "pdf", "formati", "dall", "relazione", "annuale", "scheda", "modulo", "regolamento", "misure", "codice",
           "organismo", "nucleo", "valutazione", "struttura", "comune", "provincia", "regione", "azienda", "università"}


def ipa_file(nome):
    f = next(IPA_DIR.glob(f"*/resource/*/download/{nome}"))
    return f, list(csv.DictReader(open(f, encoding="utf-8-sig"), delimiter="\t"))


def pec_di(r):
    for i in range(1, 6):
        if (r.get(f"tipo_mail{i}") or "").lower() == "pec" and r.get(f"mail{i}"): return r[f"mail{i}"].strip()
    return ""


def norm(s): return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def fase1(enti):
    """Destinatario per i CF senza PEC IndicePA: {cf: {via, codice_ipa, ente_destinatario, uo, pec, att, fonte}}."""
    fa, righe = ipa_file("amministrazioni.txt"); amm = {r["cod_amm"]: r for r in righe}
    per_cf = {}
    for r in amm.values():
        if r.get("cf"): per_cf.setdefault(r["cf"].strip(), r)
    per_nome = {}
    for r in amm.values(): per_nome.setdefault(norm(r["des_amm"]), []).append(r)
    _, ou_r = ipa_file("ou.txt"); ou = {(r["cod_amm"], r["cod_uni_ou"]): r for r in ou_r}
    unita = {}
    for nome in ("servizi-fatturazione-elettronica.txt", "nodi-smistamento-ordini.txt"):
        _, rr = ipa_file(nome)
        for r in rr:
            if r.get("cf"): unita.setdefault(r["cf"].strip(), []).append((nome, r))
    fonte_amm = "IndicePA amministrazioni.txt (mirror) " + str(fa.relative_to(R))
    ris = {}
    for e in enti:
        if e["pec"]: continue
        cf, d = e["cf"], {"cf": e["cf"]}
        if cf in per_cf and pec_di(per_cf[cf]):
            a = per_cf[cf]; d.update(via="ipa-cf", codice_ipa=a["cod_amm"], ente_destinatario=a["des_amm"], pec=pec_di(a), att="A", fonte=fonte_amm)
        elif cf in unita:
            nome, u = unita[cf][0]; a = amm.get(u["cod_amm"], {}); o = ou.get((u["cod_amm"], u["cod_uni_ou"]), {})
            p_o, p_a = pec_di(o), pec_di(a)
            d.update(via="ipa-cf-unita", codice_ipa=u["cod_amm"], codice_uo=u["cod_uni_ou"], ente_destinatario=a.get("des_amm", ""),
                     uo=u.get("des_ou", ""), pec=p_o or p_a, pec_livello="uo" if p_o else "amministrazione", att="B" if (p_o or p_a) else "",
                     fonte=f"IndicePA {nome}: CF {cf} -> unità {u['cod_uni_ou']} di {u['cod_amm']} ({len(unita[cf])} unità); PEC da ou.txt/amministrazioni.txt")
        elif len(c := per_nome.get(norm(e["ente"]), [])) == 1 and pec_di(c[0]):
            d.update(via="ipa-nome", codice_ipa=c[0]["cod_amm"], ente_destinatario=c[0]["des_amm"], pec=pec_di(c[0]), att="C",
                     fonte=f"{fonte_amm}: denominazione identica, CF diverso ({c[0].get('cf')})")
        else:
            d.update(via="", att="")
        ris[cf] = d
    return ris, amm, per_cf


def contesto_mail(t, rx, w=400):
    """Email entro w caratteri da un'etichetta rx: [(email, è_pec)]."""
    out = []
    for m in rx.finditer(t):
        seg = t[max(0, m.start() - 150): m.end() + w]
        for mm in RX_MAIL.finditer(seg):
            x = mm.group(0).strip(".").lower()
            if x.endswith((".png", ".jpg", ".gif", ".svg", ".webp")) or x in [o[0] for o in out]: continue
            prima = seg[max(0, mm.start() - 30): mm.start()]
            prima = prima[prima.rfind("@") + 1:] if "@" in prima else prima   # l'etichetta non deve precedere un'altra email
            out.append((x, any(k in x for k in ("pec", "legalmail", "postacert", "cert.", "certificat", "pcert")) or bool(re.search(r"\bpec\b|certificata", prima, re.I))))
    return out


def nome_rpct(t):
    for m in RX_RPCT.finditer(t):
        seg = t[m.end(): m.end() + 200]
        seg2 = re.sub(r"^[\s:,\-–(«\"]*(\(?R\.?P\.?C\.?T\.?\)?)?[\s:,\-–]*(è|e'|é|risulta|nominat[oa]|individuat[oa]|:)?[\s:,\-–]*(il|la)?\s*", "", seg)
        n = RX_NOME.match(seg2)
        if n and not set(n.group(2).lower().split()) & VIETATE and (n.group(1) or not n.group(2).isupper()):
            return n.group(0).strip(), t[m.start(): m.end() + 160]
    return "", ""


def visita(e, at, sito):
    rec = {"cf": e["cf"], "ente": e["ente"], "data": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "at_url": at, "sito_ipa": sito, "pagine": []}
    u = P.normalizza(at or sito or "")
    if not u: rec["esito"] = "sito-ignoto"; return rec
    if not P.robots_ok(u) and not P.ora_at(): rec["esito"] = "rinviato-robots-orario"; return rec
    if not P.robots_ok(u): rec["robots_escluso_at"] = P.robots_evidenza(u, LAV)
    s = requests.Session(); s.headers["User-Agent"] = P.UA
    browser = [False]

    def prendi(v):
        return A.rendi_js(v, LAV) if browser[0] else A.prendi_seg(s, v, LAV)

    r, sh, t = prendi(u)
    ruolo0 = "at" if at else "home"
    rec["pagine"].append({"url": r.url, "sha256": sh, "http": r.status_code, "ruolo": ruolo0})
    if (b := P.blocco(r, t)):
        # AGENTS §3: per le sezioni AT è ammesso un browser reale headless (UA da browser + URL del progetto), mai CAPTCHA
        rec["blocco_requests"] = {"blocco": b, "url": r.url, "http": r.status_code, "sha256": sh}
        try:
            r2, h2, t2 = A.rendi_js(u, LAV)
            if not P.blocco(r2, t2) and len(t2) > 800:
                browser[0] = True; r, t = r2, t2
                rec["pagine"].append({"url": r.url, "sha256": h2, "ruolo": ruolo0, "via": "browser-headless"})
                rec["blocco_requests"]["superato_con_browser"] = True
        except Exception as x:
            rec["blocco_requests"]["browser"] = f"{type(x).__name__}: {x}"[:200]
        if not browser[0]:
            rec.update(esito="blocco", blocco=b, blocco_url=r.url, blocco_http=r.status_code); return rec
    pagine = [(r, t, ruolo0)]
    coda = []
    if not at and (la := LOC.link_at(r.text, r.url).get("url")): coda.append((la, "at"))   # sezione AT: visibilita-pa
    regole = ((RX_ACC, "accesso"), (RX_ALTRI, "altri"), (RX_CORR, "corruzione"), (RX_REG, "registro"))
    for rx, ruolo in regole: coda += [(x, ruolo) for x in list(A.link_con(r, rx))[:2]]
    visti = {r.url}
    dom = lambda x: urlsplit(x).netloc.lower().split(".")[-2:]
    while coda and len(visti) < MAX_PAGINE:
        v, ruolo = coda.pop(0)
        if v in visti or (ruolo != "at" and dom(v) != dom(r.url) and not P.at_esente(v)): continue
        visti.add(v)
        try: rr, hh, tt = prendi(v)
        except Exception as x: rec["pagine"].append({"url": v, "errore": type(x).__name__, "ruolo": ruolo}); continue
        rec["pagine"].append({"url": rr.url, "sha256": hh, "http": rr.status_code, "ruolo": ruolo})
        if (bb := P.blocco(rr, tt)): rec["pagine"][-1]["blocco"] = bb; continue
        if rr.status_code >= 400: continue
        pagine.append((rr, tt, ruolo))
        if ruolo in ("at", "altri"):   # dalla AT o da «Altri contenuti» si scende verso accesso civico, corruzione, registro
            nuovi = []
            for rx, ru in regole:
                if ru == ruolo: continue
                nuovi += [(x, ru) for x in list(A.link_con(rr, rx))[:2] if x not in visti]
            coda = nuovi + coda
    acc = [(p, t, ru) for p, t, ru in pagine if ru == "accesso"]
    sha = {x["url"]: x.get("sha256", "") for x in rec["pagine"]}
    rec["url_accesso_civico"] = acc[0][0].url if acc else ""
    rec["sha_accesso_civico"] = sha.get(rec["url_accesso_civico"], "")
    rec["url_altri_contenuti"] = next((p.url for p, t, ru in pagine if ru == "altri"), "")
    rec["url_registro_accessi"] = next((p.url for p, t, ru in pagine if ru == "registro"), "")
    if not rec["url_registro_accessi"]:
        for p, t, ru in acc:
            if (l := list(A.link_con(p, RX_REG))): rec["url_registro_accessi"] = l[0]; rec["registro_solo_link"] = True; break
    mails = []
    for p, t, ru in acc + [x for x in pagine if x[2] != "accesso"]:
        for m, pec in contesto_mail(t, RX_RPCT if ru == "corruzione" else RX_ACC):
            if m not in [x[0] for x in mails]: mails.append((m, pec, p.url, ru))
    rec["recapiti"] = [{"email": m, "pec": pc, "url": u_, "ruolo": ru} for m, pc, u_, ru in mails[:8]]
    if acc:
        rec["modulo_online"] = any(RX_MOD.search(t) for p, t, ru in acc) or any(re.search(r"<form\b[^>]*>(?:(?!</form>).)*(textarea|richiesta|istanza)", p.text, re.I | re.S) for p, t, ru in acc)
    for p, t, ru in sorted(pagine, key=lambda x: x[2] != "corruzione"):
        n, ctx = nome_rpct(t)
        if n: rec.update(rpct_nome=n, rpct_contesto=ctx[:240], rpct_url=p.url); break
    rec["rpct_ruolo_citato"] = any(RX_RPCT.search(t) for p, t, ru in pagine)
    rec["esito"] = "accesso-civico-trovato" if acc else ("at-raggiunta" if at or any(ru == "at" for *_, ru in pagine) else "at-non-trovata")
    return rec


CAMPI = ["cf", "ente", "priorita_somma", "voci", "codice_ipa", "pec_indicepa", "pec_indicepa_att",
         "dest_via", "dest_ente", "dest_codice_ipa", "dest_uo", "dest_pec", "dest_att", "dest_fonte",
         "rpct_nome", "rpct_nome_att", "rpct_ruolo", "rpct_url", "rpct_sha256",
         "accesso_email", "accesso_email_pec", "accesso_email_att", "accesso_email_url", "accesso_email_sha256",
         "modulo_online", "modulo_att", "url_at", "url_at_att", "url_accesso_civico", "url_accesso_civico_sha256", "url_accesso_att",
         "url_altri_contenuti", "url_registro_accessi", "registro_att", "esito", "blocco", "data"]


def riga(e, d1, v):
    sha = {p.get("url"): p.get("sha256", "") for p in v.get("pagine", [])}
    rc = v.get("recapiti") or []
    best = (next((x for x in rc if x["pec"] and x["ruolo"] == "accesso"), None) or next((x for x in rc if x["ruolo"] == "accesso"), None)
            or next((x for x in rc if x["pec"]), None) or (rc[0] if rc else None)) or {}
    att_m = ("B" if best.get("ruolo") in ("accesso", "corruzione") else "C") if best else ""
    at_pag = next((p["url"] for p in v.get("pagine", []) if p.get("ruolo") == "at" and p.get("sha256")), "")
    dest_at = not e["pec"] and not d1.get("pec") and best.get("pec")
    return {"cf": e["cf"], "ente": e["ente"], "priorita_somma": e["priorita_somma"], "voci": e["voci"], "codice_ipa": e["codice_ipa"],
            "pec_indicepa": e["pec"], "pec_indicepa_att": "A" if e["pec"] else "",
            "dest_via": d1.get("via", "") or ("pagina-at" if dest_at else ""), "dest_ente": d1.get("ente_destinatario", ""),
            "dest_codice_ipa": d1.get("codice_ipa", ""), "dest_uo": d1.get("uo", ""),
            "dest_pec": d1.get("pec", "") or (best.get("email", "") if dest_at else ""),
            "dest_att": d1.get("att", "") or (att_m if dest_at else ""),
            "dest_fonte": d1.get("fonte", "") or ((best.get("url", "") + " sha256 " + sha.get(best.get("url"), "")) if dest_at else ""),
            "rpct_nome": v.get("rpct_nome", ""), "rpct_nome_att": "C" if v.get("rpct_nome") else "",
            "rpct_ruolo": "RPCT citato nelle pagine AT" if v.get("rpct_ruolo_citato") else "", "rpct_url": v.get("rpct_url", ""),
            "rpct_sha256": sha.get(v.get("rpct_url"), ""),
            "accesso_email": best.get("email", ""), "accesso_email_pec": ("sì" if best.get("pec") else "no") if best else "", "accesso_email_att": att_m,
            "accesso_email_url": best.get("url", ""), "accesso_email_sha256": sha.get(best.get("url"), ""),
            "modulo_online": "" if v.get("modulo_online") is None else ("sì" if v["modulo_online"] else "no"),
            "modulo_att": "C" if v.get("modulo_online") is not None else "",
            "url_at": v.get("at_url") or at_pag, "url_at_att": "A" if v.get("at_url") else ("B" if at_pag else ""),
            "url_accesso_civico": v.get("url_accesso_civico", ""), "url_accesso_civico_sha256": v.get("sha_accesso_civico", ""),
            "url_accesso_att": "B" if v.get("url_accesso_civico") else "", "url_altri_contenuti": v.get("url_altri_contenuti", ""),
            "url_registro_accessi": v.get("url_registro_accessi", ""),
            "registro_att": ("C" if v.get("registro_solo_link") else "B") if v.get("url_registro_accessi") else "",
            "esito": v.get("esito", "da-fare"), "blocco": v.get("blocco", ""), "data": v.get("data", "")}


def rendiconto(enti, d1, inizio, n_inizio):
    fatti = {}
    if (LAV / "enti.jsonl").exists():
        for l in open(LAV / "enti.jsonl", encoding="utf-8"):
            x = json.loads(l); fatti[x["cf"]] = x
    righe = [riga(e, d1.get(e["cf"], {}), fatti.get(e["cf"], {})) for e in enti]
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = OUT / "destinatari.csv.parziale"
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, CAMPI); w.writeheader(); w.writerows(righe)
    os.replace(tmp, OUT / "destinatari.csv")
    es = Counter(r["esito"] for r in righe)
    vis = [r for r in righe if r["esito"] != "da-fare"]
    c = lambda k: sum(1 for r in vis if r[k])
    sp = [r for r in righe if not r["pec_indicepa"]]
    fatti_ora = len(fatti) - n_inizio; el = time.time() - inizio
    resto = len(enti) - len(fatti)
    stima = f"{resto / (fatti_ora / el) / 3600:.1f} h" if fatti_ora > 5 else "n.d."
    txt = f"""# Accesso civico #58: RPCT e destinatari, stato del giro

Aggiornato {time.strftime('%Y-%m-%d %H:%M')} (ora del server). Codice `tools/accesso_civico/rpct_destinatari.py`; uscita
`esiti/{DATA}/accesso-civico/destinatari.csv`, rigenerata da `lavoro/accesso-civico-rpct/enti.jsonl` (una riga per ente).

- Enti visitati: **{len(fatti)} / {len(enti)}**; in questo avvio {fatti_ora} in {el / 60:.0f} min; resto stimato {stima}
- Esiti: {', '.join(f'{k} {v}' for k, v in es.most_common())}
- Fra i visitati: pagina «Accesso civico» {c('url_accesso_civico')}, email/PEC per l'accesso {c('accesso_email')}
  (di cui PEC {sum(1 for r in vis if r['accesso_email_pec'] == 'sì')}), nome RPCT (C) {c('rpct_nome')}, RPCT citato {c('rpct_ruolo')},
  modulo online sì {sum(1 for r in vis if r['modulo_online'] == 'sì')}, registro accessi {c('url_registro_accessi')}
- Senza PEC IndicePA per il CF: {len(sp)}; destinatario trovato {sum(1 for r in sp if r['dest_pec'])}
  ({', '.join(f'{k or "nessuna via"} {v}' for k, v in Counter((r['dest_via'], r['dest_att']) for r in sp).most_common())})
- Blocchi: {es.get('blocco', 0)} (evidenze in `lavoro/accesso-civico-rpct/blocchi.jsonl`: URL, data, HTTP, sha256)

Ripresa (salta gli enti già fatti):
`cd ~/analisi-spesa-ict && SPESAICT_BASE=$PWD setsid nohup nice -n 15 .venv/bin/python tools/accesso_civico/rpct_destinatari.py {DATA} >> lavoro/accesso-civico-rpct/giro.log 2>&1 &`
Gli esiti «rinviato-robots-orario» ed «errore» si ripassano togliendo le loro righe da enti.jsonl (ORE_AT per i primi).
{'FINITO' if (LAV / 'FINITO.txt').exists() else 'IN CORSO o interrotto: vedi `pgrep -af [r]pct_destinatari`'}
"""
    (LAV / "STATO.md").write_text(txt, encoding="utf-8")


def main():
    LAV.mkdir(parents=True, exist_ok=True)
    enti = list(csv.DictReader(open(OUT / "enti.csv", encoding="utf-8")))
    enti.sort(key=lambda e: -float(e["priorita_somma"] or 0))
    d1, amm, per_cf = fase1(enti)
    json.dump(d1, open(LAV / "fase1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    db = sqlite3.connect(R / "lavoro/trasparenza/stato.sqlite")
    tab = {a: (b or "", c or "") for a, b, c in db.execute("select cf, at_url, sito_ipa from enti")}
    fatti = {json.loads(l)["cf"] for l in open(LAV / "enti.jsonl", encoding="utf-8")} if (LAV / "enti.jsonl").exists() else set()
    todo = [e for e in (enti[:LIMITE] if LIMITE else enti) if e["cf"] not in fatti]
    print(time.strftime("%FT%T"), len(enti), "enti,", len(todo), "da fare", flush=True)
    inizio, stop, cont, locks = time.time(), threading.Event(), [0], {}

    def uno(e):
        if stop.is_set(): return
        if shutil.disk_usage(R).free / 1e9 < P.GUARDIA_GB:
            stop.set(); (LAV / "STOP-disco.txt").write_text(time.strftime("%FT%T\n")); return
        cf = e["cf"]; d = d1.get(cf, {})
        at, sito = tab.get(cf, ("", ""))
        if not at and not sito and d.get("codice_ipa"):   # ente vero dietro il CF (fase 1)
            a = amm.get(d["codice_ipa"], {}); at, sito = tab.get(a.get("cf", ""), ("", a.get("sito_istituzionale", "")))
        if not at and not sito and cf in per_cf: sito = per_cf[cf].get("sito_istituzionale", "")
        h = urlsplit(P.normalizza(at or sito or "")).netloc.lower()
        with locks.setdefault(h, threading.Lock()):
            v = None
            for prova in range(2):   # 2a prova: corsa sul file temporaneo di piattaforme_cig.archivia, o AT morta -> sito
                try:
                    v = visita(e, at, sito); break
                except FileNotFoundError:
                    continue
                except Exception as x:
                    if at and sito and prova == 0:
                        errore_at = f"{type(x).__name__}: {x}"[:300]; at = ""
                        continue
                    v = None; ultimo = x; break
            if v is not None and "errore_at" in locals(): v["errore_at_url"] = errore_at
            if v is None:
                x = locals().get("ultimo") or RuntimeError("archivia: file temporaneo assente due volte")
                v = {"cf": cf, "ente": e["ente"], "esito": "errore", "errore": f"{type(x).__name__}: {x}"[:300], "at_url": at, "sito_ipa": sito,
                     "data": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "pagine": []}
        with P.LOCK:
            with open(LAV / "enti.jsonl", "a", encoding="utf-8") as f: f.write(json.dumps(v, ensure_ascii=False) + "\n")
            if v.get("esito") == "blocco" or v.get("blocco_requests") or any(p.get("blocco") for p in v.get("pagine", [])):
                with open(LAV / "blocchi.jsonl", "a", encoding="utf-8") as f:
                    f.write(json.dumps({k: v.get(k) for k in ("cf", "ente", "data", "esito", "blocco", "blocco_url", "blocco_http", "blocco_requests", "pagine", "robots_escluso_at")}, ensure_ascii=False) + "\n")
            cont[0] += 1
        if cont[0] % 25 == 0:
            with P.LOCK: rendiconto(enti, d1, inizio, len(fatti))

    with ThreadPoolExecutor(P.PARALLELO) as ex: list(ex.map(uno, todo))
    if not LIMITE and not stop.is_set():
        tutti = {json.loads(l)["cf"] for l in open(LAV / "enti.jsonl", encoding="utf-8")}
        if all(e["cf"] in tutti for e in enti): (LAV / "FINITO.txt").write_text(time.strftime("%FT%T\n"))
    rendiconto(enti, d1, inizio, len(fatti))
    print(time.strftime("%FT%T"), "fine", flush=True)


if __name__ == "__main__":
    main()
