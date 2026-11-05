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
from collections import defaultdict
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
NON_PUBBLICATI_DI_NORMA = ("offerta_tecnica", "offerta_economica", "transato_monitoraggio", "ordinativi")
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


def tipo_nome(n):
    n = n.lower()
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
            a = arch.get(d["url"])
            t = tipo_nome(d["nome"]) or ("pacchetto_documentazione" if d["nome"].lower().endswith(".zip") else d["tipo"])
            docs.append({"tipo": t, "nome": d["nome"], "url": d["url"], "dove": "consip.it",
                         "stato": "archiviato" if a else "pubblicato-non-archiviato",
                         "sha256": a["sha256"] if a else None, "data": (a or {}).get("acquisito")})
            for f in (a or {}).get("contenuto") or []:
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
        dt = [d for d in docs if d["tipo"] == t]
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
            st, nota = "non-pubblicato", f"assente dalla pagina Consip dell'iniziativa (consultata il {pag['data'][:10]})"
        elif pagine_ok:
            st, nota = "da-verificare", "non riconosciuto dal nome dei file della pagina Consip: controllo a mano"
        else:
            st, nota = "da-verificare", "pagina pubblica dell'iniziativa non ancora individuata"
        righe.append({"tipo": t, "descrizione": desc, "stato": st, "dove_di_norma": dove, "via_se_manca": via, "nota": nota,
                      "documenti": [{k: d.get(k) for k in ("nome", "url", "dove", "stato", "sha256", "data")} for d in dt]})
    return righe


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
        elif a == "tutte":
            st = "da-verificare"
        elif a == "indice" and tipo_sogg == "consip":
            st = "verificato" if (pag and not pagine_ok and pag.get("chiave_ricerca", "").upper() == pag.get("chiave_ricerca", "") and not pag["chiave_ricerca"].isdigit()) else "da-verificare"
        if st:
            nota = ""
            if st == "verificato" and a.startswith("inventario:"):
                nota = per_tipo[a.split(":", 1)[1]]["nota"]
            elif st == "verificato" and a == "indice":
                nota = f"ricerca pubblica consip.it per CIG {pag['chiave_ricerca']} senza esito ({pag['data'][:10]})"
            out.append({"id": c["id"], "titolo": c["titolo"], "stato": st, "nota": nota, "raccomandazione": c["raccomandazione"]})
    return out


def main():
    cens, arch, kb, cur = carica()
    global CAR
    CAR = yaml.safe_load(open(DB / "carenze.yaml", encoding="utf-8"))
    gruppi = defaultdict(list)
    for r in cens:
        gruppi[r["iniziativa"]].append(r)
    voci = []
    for ini, lotti in gruppi.items():
        c = cur.get(ini, {}) or {}
        docs, pagine_ok, pag = documenti_osservati(ini, lotti, arch, kb, c)
        inv = inventario(ini, docs, pagine_ok, pag, c)
        ok = sum(1 for i in inv if i["stato"] == "archiviato")
        categorie = sorted({kb.get(x["cig_padre"], {}).get("categoria") for x in lotti} - {None})
        car_ini = carenze_di(ini, inv, categorie, pagine_ok, pag, CAR, lotti[0]["tipo_soggetto"])
        l0 = lotti[0]
        kb0 = kb.get(l0["cig_padre"], {})
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
            "aggiudicatari": c.get("aggiudicatari"), "massimali": c.get("massimali"), "durata": c.get("durata"),
            "listini_marchi_prodotti": c.get("listini_marchi_prodotti"), "regola_giurisdizione": regola,
            "pagina_consip": [p["url"] for p in pagine_ok], "pagina_consip_sha256": [p["sha256_html"] for p in pagine_ok],
            "lotti": [{"cig_padre": x["cig_padre"], "oggetto": x["oggetto"], "anno_padre": x["anno_padre"],
                       "derivati_ict_2020_2026": int(x["derivati_ict_2020_2026"]), "euro_ict_2020_2026": int(x["euro_ict_2020_2026"]),
                       "derivati_ict_2024_2025": int(x["derivati_ict_2024_2025"]), "euro_ict_2024_2025": int(x["euro_ict_2024_2025"])}
                      for x in lotti],
            "inventario": inv, "copertura": round(ok / len(inv), 3),
            "mancanze": [{"tipo": i["tipo"], "descrizione": i["descrizione"], "stato": i["stato"], "fonte": i["dove_di_norma"], "via": i["via_se_manca"]}
                         for i in inv if i["stato"] != "archiviato"],
            "carenze": car_ini,
            "analisi": c.get("analisi"), "note": c.get("note"),
        })
    voci.sort(key=lambda v: (v["stato_iniziativa"] != "attiva", -(v["valore_ict_2024_2025"] or 0), -v["valore_ict_2020_2026"], v["id"]))
    (DB / "iniziative.json").write_text(json.dumps(voci, ensure_ascii=False, indent=1), encoding="utf-8")
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
