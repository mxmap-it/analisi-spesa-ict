"""#62, passi 2 e 4: base dati delle iniziative ICT con inventario dei documenti e mancanze.

Ingressi (tutti nel repo, quindi rieseguibile da un clone pulito):
  report/convenzioni/database/censimento.csv     (tools/convenzioni/censimento.py)
  report/convenzioni/database/consip/*.json      (tools/convenzioni/consip_pagine.py)
  report/convenzioni/database/archiviati.jsonl   (tools/convenzioni/archivia_documenti.py)
  report/convenzioni/database/curate.yaml        (dati curati a mano, ognuno con la fonte)
  config/iniziative_ict.yaml                     (dossier, categoria, documenti TED con sha256)
Uscite: iniziative.json (una voce per iniziativa, con i lotti) e lotti.csv (una riga per lotto); schema in schema.json.
Uso: python tools/convenzioni/base_dati.py"""
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import yaml

R = Path(__file__).resolve().parent.parent.parent
DB = R / "report/convenzioni/database"

# documento atteso -> (descrizione, dove si trova di norma, via se manca)
ATTESI = {
    "bando": ("bando o avviso di gara (GUUE)", "consip.it o sito dell'aggregatore; TED", "scraping TED"),
    "disciplinare": ("disciplinare o condizioni della procedura", "consip.it o sito dell'aggregatore (pacchetto documentazione)", "scraping"),
    "capitolato": ("capitolato tecnico", "consip.it o sito dell'aggregatore (pacchetto documentazione)", "scraping"),
    "schema_aq_convenzione": ("schema di accordo quadro o di convenzione", "consip.it o sito dell'aggregatore", "scraping"),
    "listini": ("listini e appendici di prezzo", "consip.it, acquistinretepa (scheda dell'iniziativa)", "scraping; poi richiesta a Consip o all'aggregatore"),
    "determina": ("determina o decisione a contrarre", "consip.it o AT dell'aggregatore", "scraping"),
    "chiarimenti": ("risposte ai chiarimenti", "consip.it o sito dell'aggregatore", "scraping"),
    "aggiudicazione": ("avviso di aggiudicazione o esito", "consip.it, TED", "scraping TED"),
    "offerta_tecnica": ("offerta tecnica dell'aggiudicatario", "di norma non pubblicata", "richiesta a Consip o all'aggregatore; accesso civico generalizzato come ultima risorsa (art. 5 c. 2 d.lgs. 33/2013, limiti dell'art. 5-bis per i segreti commerciali)"),
    "offerta_economica": ("offerta economica e listino offerto", "acquistinretepa (catalogo) o non pubblicata", "scraping di acquistinretepa senza login; poi richiesta a Consip"),
    "transato_monitoraggio": ("transato e monitoraggio per lotto e listino", "open data Consip (aggregato), relazioni al MEF", "richiesta a Consip del transato per lotto e listino"),
    "ordinativi": ("ordinativi e contratti attuativi delle PA", "AT degli enti; PVL (link ai documenti dal 2024)", "PVL documenti_di_gara_link, poi AT degli enti"),
    "cig_derivati": ("CIG derivati e importi", "BDNCP ANAC (nostro mirror)", "-"),
}
EXTRA = {"psn": ["progetti_fabbisogni"], "consip-1403": ["progetti_fabbisogni"]}
ATTESI_EXTRA = {"progetti_fabbisogni": ("piani e progetti dei fabbisogni delle PA", "PSN, AT degli enti", "richiesta al DTD o al PSN; AT degli enti")}
# offerta economica: i listini offerti possono stare su acquistinretepa (non ancora consultato): resta «da verificare» (revisione 5/11)
NON_PUBBLICATI_DI_NORMA = ("offerta_tecnica", "transato_monitoraggio", "ordinativi")
# tipo del documento dal nome del file (anche dentro gli zip); ordine = priorita'
REGOLE = [
    ("aggiudicazione", r"aggiudicaz|esito|graduatoria"),
    ("chiarimenti", r"chiariment"),
    ("determina", r"determina|decisione a contrarre"),
    ("offerta_tecnica", r"offerta tecnica"),
    ("offerta_economica", r"offerta economica"),
    ("listini", r"listin|prezz|corrispettiv"),
    ("capitolato", r"capitolato"),
    ("schema_aq_convenzione", r"schema|accordo quadro|convenzione|contratto quadro"),
    ("disciplinare", r"disciplinare|\bcdo\b|condizioni"),
    ("bando", r"bando|guue"),
]


MODELLO = re.compile(r"schema di offerta|fac.?simile|modello|modulo|format|istruzioni|dichiarazion|template|dgue", re.I)


def tipo_nome(n):
    n = n.lower()
    # nelle pagine di gara i file «offerta tecnica/economica» sono modelli o regole per i concorrenti, mai l'offerta del vincitore:
    # l'offerta dell'aggiudicatario entra solo da curate.yaml, letta e confermata
    if re.search(r"offert[ae]", n):
        return None
    return next((t for t, rx in REGOLE if re.search(rx, n)), None)


def carica():
    cens = list(csv.DictReader(open(DB / "censimento.csv", encoding="utf-8")))
    arch = {}
    if (DB / "archiviati.jsonl").exists():
        for riga in open(DB / "archiviati.jsonl", encoding="utf-8"):
            a = json.loads(riga)
            arch[a["url"]] = a
    kb_lista = yaml.safe_load(open(R / "config/iniziative_ict.yaml", encoding="utf-8")) or []
    kb = {str(v["cig"]): v for v in kb_lista if isinstance(v, dict) and v.get("cig")}
    cur = {}
    if (DB / "curate.yaml").exists():
        cur = yaml.safe_load(open(DB / "curate.yaml", encoding="utf-8")) or {}
    return cens, arch, kb, cur


def documenti_osservati(ini, lotti, arch, kb, c):
    cp = DB / "consip" / f"{ini}.json"
    pag = json.loads(cp.read_text(encoding="utf-8")) if cp.exists() else None
    pagine_ok = [p for p in (pag or {}).get("pagine", []) if p.get("cita_chiave")]
    docs = []
    for p in pagine_ok:
        for d in p["documenti"]:
            # le pagine Consip linkano a volte documenti di altre gare (es. «ID 2912» nella pagina dell'ID 2928): si scartano
            altri = set(re.findall(r"ID\s*(\d{4})", d["nome"])) - {ini.split("-", 1)[-1]}
            if altri and ini.startswith("consip-"):
                continue
            a = arch.get(d["url"])
            t = tipo_nome(d["nome"]) or ("pacchetto_documentazione" if d["nome"].lower().endswith(".zip") else d["tipo"])
            docs.append({"tipo": t, "nome": d["nome"], "url": d["url"], "dove": "consip.it",
                         "stato": "archiviato" if a else "pubblicato-non-archiviato",
                         "sha256": a["sha256"] if a else None, "data": (a or {}).get("acquisito")})
            for f in (a or {}).get("contenuto") or []:
                if ini.startswith("consip-") and set(re.findall(r"\bID\s*(\d{4})\b", f)) - {ini.split("-", 1)[-1]}:
                    continue  # file di un'altra gara dentro lo zip
                tz = tipo_nome(f.rsplit("/", 1)[-1])
                if tz:
                    docs.append({"tipo": tz, "nome": f.rsplit("/", 1)[-1], "url": d["url"] + "#" + f, "dove": "consip.it (nello zip)",
                                 "stato": "archiviato", "sha256": a["sha256"], "data": a.get("acquisito")})
    for lotto in lotti:
        for d in kb.get(lotto["cig_padre"], {}).get("documenti") or []:
            cc = (d.get("cosa_conferma") or "").lower()
            if "aggiudic" in cc:
                t = "aggiudicazione"
            elif "bando" in cc:
                t = "bando"
            else:
                t = tipo_nome(cc)
            if t and d.get("sha256"):
                docs.append({"tipo": t, "nome": (d.get("cosa_conferma") or "")[:140], "url": d["url"],
                             "dove": re.sub(r"https?://([^/]+).*", r"\1", d["url"]), "stato": "archiviato", "sha256": d["sha256"], "data": None})
    for d in c.get("documenti", []) or []:
        docs.append(dict(d))
    docs.extend(ALTROVE.get(ini, []))
    if ini == "psn":  # progetti dei fabbisogni e lettere di attivazione gia' archiviati (#55, report/convenzioni/psn-database/)
        for d in csv.DictReader(open(R / "report/convenzioni/psn-database/documenti-psn.csv", encoding="utf-8")):
            if d.get("sha256"):
                docs.append({"tipo": "progetti_fabbisogni" if d["tipo"] == "P" else "ordinativi", "nome": f"{d['id']} {d['ente']} {d['codice_piano']}",
                             "url": d["url"], "dove": "AT degli enti", "stato": "archiviato", "sha256": d["sha256"], "data": None})
    visti, uniq = set(), []
    for d in docs:
        if d["url"] not in visti:
            visti.add(d["url"])
            uniq.append(d)
    return uniq, pagine_ok, pag


def inventario(ini, docs, pagine_ok, pag, c):
    righe = []
    for t in list(ATTESI) + EXTRA.get(ini, []):
        desc, dove, via = ATTESI.get(t) or ATTESI_EXTRA[t]
        altrove = [d for d in docs if d["tipo"] == t and d.get("ufficiale") is False]  # fonte non ufficiale: non cambia lo stato
        dt = [d for d in docs if d["tipo"] == t and d.get("ufficiale") is not False]
        nota = ""
        if t == "cig_derivati":
            st, nota = "archiviato", "BDNCP ANAC, verificato (tools/analisi/padri_ict.py)"
        elif any(d["stato"] == "archiviato" for d in dt):
            st = "archiviato"
        elif dt:
            st = "pubblicato-non-archiviato"
        elif t in (c.get("non_pubblicati") or {}):
            st, nota = "non-pubblicato", c["non_pubblicati"][t]
        elif pagine_ok and t in NON_PUBBLICATI_DI_NORMA:
            st, nota = "non-pubblicato", f"non individuato sulla pagina del bando su consip.it (consultata il {pag['data'][:10]}; tipo dedotto dal nome dei file); acquistinretepa e AT di Consip non ancora consultati"
        elif pagine_ok:
            st, nota = "da-verificare", "non riconosciuto dal nome dei file della pagina Consip: controllo a mano"
        else:
            st, nota = "da-verificare", "pagina pubblica dell'iniziativa non ancora individuata"
        righe.append({"tipo": t, "descrizione": desc, "stato": st, "dove_di_norma": dove, "via_se_manca": via, "nota": nota,
                      "documenti": [{k: d.get(k) for k in ("nome", "url", "dove", "stato", "sha256", "data", "nota")} for d in dt],
                      "reperiti_altrove": [{k: d.get(k) for k in ("nome", "url", "fonte", "affidabilita", "sha256", "data")} for d in altrove]})
    return righe


CAMPI_DOSSIER = {"aggiudicatari": r"aggiudicatar", "massimali": r"massimal|valore", "durata": r"durata"}


def dai_dossier(percorsi):
    """Aggiudicatari, massimali e durata dalle tabelle «| Campo | Valore | Fonte | Livello |» dei rendiconti esistenti (riuso, non rifare)."""
    out = {}
    for p in percorsi:
        f = R / p
        if not f.exists():
            continue
        for riga in f.read_text(encoding="utf-8").splitlines():
            c = [x.strip() for x in riga.strip().strip("|").split("|")]
            if len(c) < 4 or not riga.startswith("|"):
                continue
            for campo, rx in CAMPI_DOSSIER.items():
                if re.match(rx, c[0], re.I):
                    out.setdefault(campo, []).append(f"{c[0]}: {c[1]} (fonte: {c[2]}; livello {c[3]}; da {p.rsplit('/', 1)[-1]})")
    return {k: " · ".join(v[:3]) for k, v in out.items()}


def nomi_file(ini, pagine_ok, arch):
    """Tutti i nomi di file dell'iniziativa: documenti della pagina ufficiale e contenuto degli zip archiviati."""
    out = []
    for p in pagine_ok:
        for d in p["documenti"]:
            out.append((d["nome"], d["url"], (arch.get(d["url"]) or {}).get("sha256")))
            for f in (arch.get(d["url"]) or {}).get("contenuto") or []:
                out.append((f.rsplit("/", 1)[-1], d["url"] + "#" + f, arch[d["url"]]["sha256"]))
    return out


def estratti_di(ini):
    """Estratti per parole chiave (tools/convenzioni/estrai_documenti.py): al massimo 2 per tema, marcati «automatico, da leggere»."""
    p = DB / "estratti" / f"{ini}.json"
    if not p.exists():
        return None
    e = json.loads(p.read_text(encoding="utf-8"))
    per = defaultdict(list)
    for x in e["estratti"]:
        if len(per[x["tema"]]) < 2 and x["documento"] not in [y["documento"] for y in per[x["tema"]]]:
            per[x["tema"]].append({k: x[k] for k in ("documento", "url", "sha256")} | {"testo": x["testo"][:420]})
    return {"documenti_letti": e["documenti_letti"], "conteggi": dict(Counter(x["tema"] for x in e["estratti"])), "esempi": dict(per)}


CARENZA_TIPO = {"C1": "offerta_tecnica", "C2": "offerta_economica", "C3": "transato_monitoraggio", "C4": "ordinativi", "C5": "progetti_fabbisogni"}
ID_FONTI = {"2483": "consip-2483", "2610": "consip-2610", "PSN": "psn", "SPC Cloud 1403": "consip-1403", "2746/2213": "consip-2746"}


def carica_altrove():
    """Documenti da fonte non ufficiale raccolti il 5/11: campione di enti aderenti (enti-campione/) e ricerca web (fonti-non-ufficiali/).
    Non cambiano lo stato della carenza; le righe «di controllo» (altra edizione o altro ID) si scartano."""
    out, extra = defaultdict(list), defaultdict(list)
    p = R / "report/convenzioni/enti-campione/enti-campione-2026-11-05.csv"
    if p.exists():
        for r in csv.DictReader(open(p, encoding="utf-8")):
            if r["documento_trovato"] != "si" or not r["sha256"] or "controllo" in (r["note"] or "").lower():
                continue
            out[r["iniziativa"]].append({"tipo": "ordinativi", "ufficiale": False, "fonte": f"{r['ente']} ({r['esito']})", "affidabilita": "A",
                                         "nome": f"{r['ente']}: {r['tipo_documento']} — {r['dati_estratti'][:140]}", "url": r["url_documento"],
                                         "stato": "archiviato", "sha256": r["sha256"], "data": r["data_consultazione"]})
    p = R / "report/convenzioni/fonti-non-ufficiali/fonti-2026-11-05.csv"
    if p.exists():
        for r in csv.DictReader(open(p, encoding="utf-8")):
            ini = ID_FONTI.get(r["iniziativa"])
            if not ini:
                continue
            d = {"ufficiale": False, "fonte": f"{r['autore_sito']} ({r['fonte_tipo']}) [R]", "affidabilita": r["affidabilita"],
                 "nome": f"{r['titolo'][:90]} — {r['dato_estratto'][:140]}", "url": r["url"], "stato": "archiviato" if r["sha256"] else "pubblicato-non-archiviato",
                 "sha256": r["sha256"] or None, "data": r["data_reperimento"]}
            t = CARENZA_TIPO.get(r["carenza"])
            if t and r["sha256"]:
                out[ini].append(dict(d, tipo=t))
            else:
                extra[ini].append(dict(d, carenza=r["carenza"]))
    return out, extra


def carenze_di(ini, inv, categorie, pagine_ok, pag, car, tipo_sogg):
    """Carenze di trasparenza (report/convenzioni/database/carenze.yaml) che colpiscono l'iniziativa."""
    per_tipo = {i["tipo"]: i for i in inv}
    out = []
    for c in car["carenze"]:
        a = c["applica"]
        st = None
        if a.startswith("inventario:"):
            i = per_tipo.get(a.split(":", 1)[1])
            if i and i["stato"] != "archiviato":
                st = "verificato" if i["stato"] == "non-pubblicato" else "da-verificare"
        elif a == "cloud":
            if ini in car["iniziative_cloud"] or set(categorie) & {"cloud-provider", "cloud-multi", "psn"}:
                st = "da-verificare"
        elif a == "transato_marchio":
            # l'ordinato per lotto è negli open data Consip, ma senza listino, marchio ed ente: verificato se la pagina o gli open data sono letti
            st = "verificato" if (tipo_sogg == "consip" and (pagine_ok or ini in ORDINATO)) else "da-verificare"
        elif a == "tutte":
            st = "da-verificare"
        elif a == "indice" and tipo_sogg == "consip":
            st = "verificato" if (pag and not pagine_ok and pag.get("chiave_ricerca", "").upper() == pag.get("chiave_ricerca", "") and not pag["chiave_ricerca"].isdigit()) else "da-verificare"
        if st:
            nota = ""
            if st == "verificato" and a.startswith("inventario:"):
                nota = per_tipo[a.split(":", 1)[1]]["nota"]
            elif st == "verificato" and a == "transato_marchio":
                nota = "open data Consip: ordinato per lotto e anno, senza listino, marchio ed ente" if ini in ORDINATO else "assente dalla pagina Consip; open data Consip senza listino e marchio"
            elif st == "verificato" and a == "indice":
                nota = f"ricerca pubblica consip.it per CIG {pag['chiave_ricerca']} senza esito ({pag['data'][:10]})"
            out.append({"id": c["id"], "titolo": c["titolo"], "stato": st, "nota": nota, "raccomandazione": c["raccomandazione"]})
    return out


def scrivi_griglia(voci):
    """JSON compatto per il cruscotto a griglia (/convenzioni/griglia/): una riga per iniziativa, una cella per tipo atteso.
    Stato della cella: ufficiale | non-ufficiale | pubblicato | carenza | da-verificare | richiesto (istanza nel registro)."""
    reg = {}
    rp = R / "report/convenzioni/accesso-civico/registro.csv"
    if rp.exists():
        for r in csv.DictReader(open(rp, encoding="utf-8")):
            reg[r["id"]] = r
    car_tipo = {c["applica"].split(":", 1)[1]: c["id"] for c in CAR["carenze"] if c["applica"].startswith("inventario:")}
    tipi = list(ATTESI) + ["progetti_fabbisogni"]
    righe = []
    for v in voci:
        celle = {}
        for i in v["inventario"]:
            cid = car_tipo.get(i["tipo"])
            istanza = reg.get(f"{v['id']}-{cid}".lower()) if cid else None
            if i["stato"] == "archiviato":
                st = "ufficiale"
            elif i["reperiti_altrove"]:
                st = "non-ufficiale"
            elif istanza and istanza["stato"] != "preparata":
                st = "richiesto"
            elif i["stato"] == "pubblicato-non-archiviato":
                st = "pubblicato"
            elif i["stato"] == "non-pubblicato":
                st = "carenza"
            else:
                st = "da-verificare"
            d0 = (i["documenti"] or i["reperiti_altrove"] or [{}])[0]
            celle[i["tipo"]] = {"s": st, "n": len(i["documenti"]), "a": len(i["reperiti_altrove"]), "nota": i["nota"][:200],
                                "doc": d0.get("nome", "")[:120], "url": d0.get("url"), "sha": d0.get("sha256"), "fonte": d0.get("fonte") or d0.get("dove"),
                                "carenza": cid, "istanza": (istanza or {}).get("id"), "istanza_stato": (istanza or {}).get("stato")}
        righe.append({"id": v["id"], "nome": v["nome"][:140], "tipo": v["tipo_soggetto"], "stato": v["stato_iniziativa"],
                      "categoria": v["categoria"][0] if v["categoria"] else "non-classificata", "valore": v["valore_ict_2024_2025"] or 0,
                      "copertura": v["copertura"], "carenze": [k["id"] for k in v["carenze"]], "celle": celle})
    out = {"generato": "tools/convenzioni/base_dati.py", "tipi": [{"id": t, "descrizione": (ATTESI.get(t) or ATTESI_EXTRA[t])[0]} for t in tipi],
           "istanze": {"preparate": sum(1 for r in reg.values() if r["stato"] == "preparata"), "inviate": sum(1 for r in reg.values() if r["stato"] != "preparata")},
           "righe": righe}
    dest = R / "sito/static/dati/convenzioni-griglia.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def main():
    cens, arch, kb, cur = carica()
    global CAR, ORDINATO, ALTROVE, ALTROVE_EXTRA, FLUSSI
    FLUSSI = {}
    if (DB / "flussi-dati.csv").exists():
        for r in csv.DictReader(open(DB / "flussi-dati.csv", encoding="utf-8")):
            if r["esito"] == "letto":
                si = [k for k in ("fattura", "ordine", "ente", "listino_prodotto", "marchio", "cig", "lotto", "imponibile") if r.get(k) == "si"]
                no = [k for k in ("ente", "listino_prodotto", "marchio") if r.get(k) == "no"]
                FLUSSI[r["iniziativa"]] = (f"Allegato «flussi dati» letto il 5/11 (tools/convenzioni/leggi_flussi.py): invio {r['frequenza'] or 'periodico'} a Consip; "
                                           f"campi del tracciato trovati: {', '.join(si) or 'nessuno'}; non trovati: {', '.join(no) or '–'} (ricerca per parole nel testo, R)")
    ALTROVE, ALTROVE_EXTRA = carica_altrove()
    ORDINATO = defaultdict(list)
    if (DB / "consip-ordinato.csv").exists():
        for r in csv.DictReader(open(DB / "consip-ordinato.csv", encoding="utf-8")):
            ORDINATO[r["iniziativa"]].append(r)
    fonti_od = json.loads((DB / "consip-ordinato-fonti.json").read_text(encoding="utf-8"))["fonti"] if (DB / "consip-ordinato-fonti.json").exists() else []
    CAR = yaml.safe_load(open(DB / "carenze.yaml", encoding="utf-8"))
    gruppi = defaultdict(list)
    for r in cens:
        gruppi[r["iniziativa"]].append(r)
    voci = []
    for ini, lotti in gruppi.items():
        c = cur.get(ini, {}) or {}
        docs, pagine_ok, pag = documenti_osservati(ini, lotti, arch, kb, c)
        for f in (fonti_od if ini in ORDINATO else []):
            docs.append({"tipo": "transato_monitoraggio", "nome": "open data Consip: " + f["url"].rsplit("/", 1)[-1] + " (ordinato per lotto, aggregato)",
                         "url": f["url"], "dove": "dati.consip.it", "stato": "archiviato", "sha256": f["sha256"], "data": "2026-11-05"})
        inv = inventario(ini, docs, pagine_ok, pag, c)
        ok = sum(1 for i in inv if i["stato"] == "archiviato")
        categorie = sorted({kb.get(x["cig_padre"], {}).get("categoria") for x in lotti} - {None})
        nf = nomi_file(ini, pagine_ok, arch)
        flusso = [(n, u, h) for n, u, h in nf if re.search(r"flussi? dati|flusso.*commission|dati di fatturato", n, re.I)]
        evidenze = []
        if flusso:
            letto = c.get("flusso_letto") or FLUSSI.get(ini)
            evidenze.append({"carenza": "C3", "livello": "V (letto)" if letto else "R (dal nome del file)",
                             "testo": letto or "Allegato sui flussi dati del fatturato da trasmettere a Consip per la commissione a carico del fornitore (d.m. MEF 23/11/2012): individuato dal nome del file, da leggere",
                             "documento": flusso[0][0], "url": flusso[0][1], "sha256": flusso[0][2]})
        car_ini = carenze_di(ini, inv, categorie, pagine_ok, pag, CAR, lotti[0]["tipo_soggetto"])
        for k in car_ini:  # accertamenti a mano (curate.yaml: carenze_verificate {Cn: nota con fonte})
            if k["id"] in (c.get("carenze_verificate") or {}):
                k["stato"], k["nota"] = "verificato", c["carenze_verificate"][k["id"]]
        l0 = lotti[0]
        kb0 = kb.get(l0["cig_padre"], {})
        dd = dai_dossier(sorted({kb[x["cig_padre"]]["dossier"] for x in lotti if kb.get(x["cig_padre"], {}).get("dossier")}))
        regola = c.get("regola_giurisdizione") or next(
            (kb[x["cig_padre"]].get("regola_sovranita") for x in lotti if kb.get(x["cig_padre"], {}).get("regola_sovranita")), None)
        voci.append({
            "id": ini, "tipo_soggetto": l0["tipo_soggetto"], "stato_iniziativa": l0["stato_iniziativa"],
            "nome": c.get("nome") or kb0.get("iniziativa") or l0["oggetto"][:160],
            "stazione_appaltante": l0["stazione_appaltante"] or c.get("stazione_appaltante", ""),
            "categoria": sorted({kb.get(x["cig_padre"], {}).get("categoria") for x in lotti} - {None}),
            "dossier": sorted({kb[x["cig_padre"]]["dossier"] for x in lotti if kb.get(x["cig_padre"], {}).get("dossier")}),
            "valore_ict_2024_2025": int(l0["valore_iniziativa"]) if l0["criterio_valore"] == "euro_ict_2024_2025" else None,
            "valore_ict_2020_2026": int(l0["valore_iniziativa_2020_2026"]), "rango_valore": int(l0["rango_iniziativa"] or 0) or None,
            "derivati_ict_2024_2025": sum(int(x["derivati_ict_2024_2025"]) for x in lotti),
            "aggiudicatari": c.get("aggiudicatari") or dd.get("aggiudicatari"), "massimali": c.get("massimali") or dd.get("massimali"),
            "durata": c.get("durata") or dd.get("durata"),
            "listini_marchi_prodotti": c.get("listini_marchi_prodotti"), "regola_giurisdizione": regola,
            "pagina_consip": [p["url"] for p in pagine_ok], "pagina_consip_sha256": [p["sha256_html"] for p in pagine_ok],
            "lotti": [{"cig_padre": x["cig_padre"], "oggetto": x["oggetto"], "anno_padre": x["anno_padre"],
                       "derivati_ict_2020_2026": int(x["derivati_ict_2020_2026"]), "euro_ict_2020_2026": int(x["euro_ict_2020_2026"]),
                       "derivati_ict_2024_2025": int(x["derivati_ict_2024_2025"]), "euro_ict_2024_2025": int(x["euro_ict_2024_2025"])}
                      for x in lotti],
            "inventario": inv, "copertura": round(ok / len(inv), 3),
            "mancanze": [{"tipo": i["tipo"], "descrizione": i["descrizione"], "stato": i["stato"], "fonte": i["dove_di_norma"], "via": i["via_se_manca"]}
                         for i in inv if i["stato"] != "archiviato"],
            "ordinato_consip": {"2024": sum(int(r["ordinato_2024"]) for r in ORDINATO.get(ini, [])), "2025": sum(int(r["ordinato_2025"]) for r in ORDINATO.get(ini, [])),
                                "2026": sum(int(r.get("ordinato_2026") or 0) for r in ORDINATO.get(ini, [])),
                                "nomi": [r["nome_consip"] + " [" + r["abbinamento"] + "]" for r in ORDINATO.get(ini, [])]} if ini in ORDINATO else None,
            "carenze": car_ini, "evidenze_dato_esistente": evidenze, "altrove_su_carenze": ALTROVE_EXTRA.get(ini, []), "estratti": estratti_di(ini),
            "analisi": c.get("analisi"), "note": c.get("note"),
        })
    voci.sort(key=lambda v: (v["stato_iniziativa"] != "attiva", -(v["valore_ict_2024_2025"] or 0), -v["valore_ict_2020_2026"], v["id"]))
    (DB / "iniziative.json").write_text(json.dumps(voci, ensure_ascii=False, indent=1), encoding="utf-8")
    scrivi_griglia(voci)
    with open(DB / "lotti.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["iniziativa", "tipo_soggetto", "stato_iniziativa", "cig_padre", "anno_padre", "derivati_ict_2024_2025", "euro_ict_2024_2025",
                    "derivati_ict_2020_2026", "euro_ict_2020_2026", "copertura_iniziativa", "oggetto"])
        for v in voci:
            for x in v["lotti"]:
                w.writerow([v["id"], v["tipo_soggetto"], v["stato_iniziativa"], x["cig_padre"], x["anno_padre"], x["derivati_ict_2024_2025"],
                            x["euro_ict_2024_2025"], x["derivati_ict_2020_2026"], x["euro_ict_2020_2026"], v["copertura"], x["oggetto"]])
    media = sum(v["copertura"] for v in voci) / len(voci)
    print(len(voci), "iniziative,", sum(len(v["lotti"]) for v in voci), "lotti; copertura media", round(media, 3))


if __name__ == "__main__":
    main()
