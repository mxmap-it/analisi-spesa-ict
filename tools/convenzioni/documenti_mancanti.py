"""#62: inventario ANALITICO, file per file, dei documenti che mancano dalla pubblicazione per ogni iniziativa ICT della base dati.

Tre metodi, registrati per riga (colonna «metodo»):
  numerazione  buchi nella numerazione degli allegati/appendici/annessi pubblicati (nomi dei file della pagina e degli zip);
  rimando      allegati citati nei testi archiviati (rimandi.jsonl, da tools/convenzioni/rimandi_documenti.py) ma non pubblicati;
  atteso       documenti attesi per legge o prassi (classi di carenze.yaml e mancanze dell'inventario in iniziative.json).
Un documento si dichiara mancante [V] solo se la pagina ufficiale è stata ricontrollata dal vivo (ricontrollo-pagine.json, da
tools/convenzioni/ricontrollo_pagine.py) e il file non c'è; altrimenti [R]. I blocchi incontrati (login, 401/403/429) vanno in
blocchi-accesso.csv. Deterministico: stessi ingressi, stessa uscita.
Ingressi: report/convenzioni/database/{iniziative.json, consip/*.json, archiviati.jsonl, rimandi.jsonl, ricontrollo-pagine.json,
carenze.yaml}, report/convenzioni/accesso-civico/registro.csv.
Uscite: report/convenzioni/database/documenti-mancanti.csv, blocchi-accesso.csv; con --bozze anche le bozze raggruppate per
destinatario in report/convenzioni/accesso-civico/bozze/mancanti-*.{json,md} e le righe nel registro (NESSUN INVIO).
Uso: python tools/convenzioni/documenti_mancanti.py [--bozze]"""
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

R = Path(__file__).resolve().parent.parent.parent
DB = R / "report/convenzioni/database"
AC = R / "report/convenzioni/accesso-civico"
OUT = DB / "documenti-mancanti.csv"
BLOCCHI = DB / "blocchi-accesso.csv"
CAMPI = ["iniziativa", "documento_atteso", "metodo", "evidenza", "contenuto_presunto", "base_normativa", "criticita", "livello",
         "data_controllo", "url_pagina", "bozza_accesso_civico", "dietro_login"]
DATA_BOZZE = "2026-11-06"

# identificativi nei NOMI dei file pubblicati
RX_NOME = re.compile(r"(?i)(?<![a-z])(allegat[oi]|appendice|annesso|sub[- ]?allegato|all\.?(?=[ _.-]*\d)|app\.?(?=[ _.-]*\d))[ _.-]*(?:n\.?[ _]*)?"
                     r"(\d{1,2}(?:[.\-]\d{1,2})?(?:[ _]?[A-Z](?![a-z]))?|[A-Z](?![A-Za-z]))")
DI_NOME = [("capitolato", r"(?i)\b(al|del)[ _]+(CT|capitolato)"), ("schema", r"(?i)\b(allo|dello|al|del)[ _]+(schema|AQ\b|accordo|convenzione|contratto)"),
           ("disciplinare", r"(?i)\b(al|del)[ _]+disciplinare"), ("offerta", r"(?i)\b(all|dell)['’ _]+offerta")]
# rimandi a norme e a documenti di altri soggetti: non sono allegati della gara
NORMA = re.compile(r"(?i)(d\.?\s?lgs|decreto|codice|legge|l\.\s?\d|regolamento|direttiva|d\.?p\.?r|d\.?m\.|dpcm|circolare|"
                   r"determinazione|delibera|ANAC|GDPR|CAD\b|TUEL|norma UNI|ISO)")
PLURALE_E = re.compile(r"(?i)\b(allegati|appendici|annessi)\s+[EO]\b")
PLURALE = re.compile(r"(?i)\b(allegati|appendici|annessi|sub-?allegati)\s+(?:n\.?\s*)?([0-9A-Z.]+)")
ROMANI = re.compile(r"^(I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII)(\.\d+)?$")
CRIT3 = re.compile(r"(?i)(listin|prezz|offerta econ|corrispettiv|elenco (dei )?prodott|catalog|configurator|brand|marc|"
                   r"open ?source|fatturat|transat|erogat|ordinat|piano dei fabbisogni|progetto dei fabbisogni|data ?cent|region)")
CRIT2 = re.compile(r"(?i)(offerta tecnic|capitolato|flussi|monitoraggio|report|livelli di servizio|SLA|penali|piano|"
                   r"subappalt|sicurezza|trattamento dei dati|nomina a responsabile|DPA|verbale|proroga|increment|modific|contratto|schema)")

ATTESI = {  # tipo dell'inventario -> (documento atteso, criticità, carenza, base se la carenza non c'è)
    "offerta_tecnica": ("Offerta tecnica dell'aggiudicatario (per lotto)", 3, "C1", None),
    "offerta_economica": ("Offerta economica e listino offerto dall'aggiudicatario (per lotto)", 3, "C2", None),
    "listini": ("Listini prezzi applicati alle amministrazioni (per lotto e listino)", 3, "C2", None),
    "transato_monitoraggio": ("Flussi di monitoraggio: transato/erogato per lotto, listino e marchio", 3, "C3", None),
    "ordinativi": ("Elenco degli ordinativi e contratti attuativi delle PA", 3, "C4", None),
    "progetti_fabbisogni": ("Progetti dei Piani dei Fabbisogni approvati", 3, "C5", None),
    "capitolato": ("Capitolato tecnico", 2, None, "Documenti di gara: pubblicazione sul sito della stazione appaltante e in BDNCP (art. 27-28 d.lgs. 36/2023; art. 37 d.lgs. 33/2013) [R]"),
    "schema_aq_convenzione": ("Convenzione / accordo quadro stipulato (o schema)", 2, None, "Atti della procedura e contratto: art. 28 d.lgs. 36/2023, art. 37 d.lgs. 33/2013 [R]"),
    "aggiudicazione": ("Provvedimento o avviso di aggiudicazione", 2, None, "Avviso di aggiudicazione: art. 50 c. 9 e art. 84-85 d.lgs. 36/2023 (GUUE/BDNCP); provvedimento ex art. 28 [R]"),
    "disciplinare": ("Disciplinare di gara o condizioni della procedura", 1, None, "Documenti di gara: art. 82-85 d.lgs. 36/2023 [R]"),
    "determina": ("Determina o decisione a contrarre", 1, None, "Decisione di contrarre: art. 17 c. 1 d.lgs. 36/2023; pubblicazione ex art. 28 [R]"),
    "bando": ("Bando o avviso di gara", 1, None, "Bando: art. 84-85 d.lgs. 36/2023 (GUUE, BDNCP) [R]"),
    "chiarimenti": ("Risposte ai chiarimenti", 1, None, "Chiarimenti: art. 88 d.lgs. 36/2023 (pubblicati sul sito) [R]"),
}
# tipo atteso -> regex sui nomi dei file pubblicati dal vivo (se c'è, non è mancante)
PRESENTE = {"offerta_tecnica": r"offerta[ _-]*tecnica(?!.*(fac|schema|modello))", "offerta_economica": r"offerta[ _-]*economica(?!.*(fac|schema|modello))",
            "listini": r"listin|prezz", "transato_monitoraggio": r"monitoragg|transat|erogat", "ordinativi": r"ordinativ",
            "capitolato": r"capitolato", "schema_aq_convenzione": r"schema|accordo|convenzione|contratto",
            "aggiudicazione": r"aggiudic|esito", "disciplinare": r"disciplinare|cdo|condizioni", "determina": r"determina|contrarre",
            "bando": r"bando|guue", "chiarimenti": r"chiariment", "progetti_fabbisogni": r"fabbisogn"}
MODIFICA = r"proroga|increment|estension|modific|quinto|rinnovo"


def leggi_jsonl(p):
    return [json.loads(x) for x in open(p, encoding="utf-8")] if p.exists() else []


def di_da_nome(n):
    for k, rx in DI_NOME:
        if re.match(r"[\s_\-–]*" + rx.replace(r"(?i)\b", "").replace("(?i)", ""), n, re.I):
            return k
    return ""


def ident(n):
    n = re.sub(r"[\s_]+", "", n).upper().replace("-", ".")
    m = re.match(r"^(\d+)", n)
    return n, (int(m.group(1)) if m else None)


def pulisci(t):
    """titolo del rimando: fino alla chiusura delle virgolette o alla prima virgola, senza le parole che seguono nel testo."""
    t = re.split(r"[”\"»,;]| (?:i quali|che |del presente|di cui|sono |è |nel |nella )", t, maxsplit=1)[0].strip(" –-:.")
    return t[:80]


def critic(testo, base=1):
    if CRIT3.search(testo):
        return 3
    if CRIT2.search(testo):
        return max(base, 2)
    return base


def carica():
    voci = json.loads((DB / "iniziative.json").read_text(encoding="utf-8"))
    car = {c["id"]: c for c in yaml.safe_load(open(DB / "carenze.yaml", encoding="utf-8"))["carenze"]}
    arch = {a["url"]: a for a in leggi_jsonl(DB / "archiviati.jsonl")}
    vivo = json.loads((DB / "ricontrollo-pagine.json").read_text(encoding="utf-8")) if (DB / "ricontrollo-pagine.json").exists() else {}
    rim = defaultdict(list)
    for r in leggi_jsonl(DB / "rimandi.jsonl"):
        rim[r["iniziativa"]].append(r)
    pag = {}
    for f in sorted((DB / "consip").glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        pag[d["iniziativa"]] = [p for p in d.get("pagine", []) if p.get("cita_chiave")]
    reg = list(csv.DictReader(open(AC / "registro.csv", encoding="utf-8"))) if (AC / "registro.csv").exists() else []
    return voci, car, arch, vivo, rim, pag, reg


def pubblicati(ini, pagine, arch):
    """nomi pubblicati (pagina + contenuto degli zip archiviati), escluse le altre gare linkate per errore."""
    sig = re.match(r"consip-(\d{4})$", ini)
    nomi = []
    for p in pagine:
        for d in p["documenti"]:
            altra = re.search(r"\bID[ _%20]*(\d{4})\b", d["nome"])
            if sig and altra and altra.group(1) != sig.group(1):
                continue
            nomi.append((d["nome"], d["url"], arch.get(d["url"], {}).get("sha256", "")))
            for c in arch.get(d["url"], {}).get("contenuto", []) or []:
                altra = re.search(r"ID[ _]*(\d{4})", c)
                if sig and altra and altra.group(1) != sig.group(1):
                    continue
                nomi.append((c, d["url"] + "#" + c, arch[d["url"]]["sha256"]))
    return nomi


def main(bozze=False):
    voci, car, arch, vivo, rim, pag, reg = carica()
    righe, blocchi = [], []
    per_reg = {(r["iniziativa"], r["carenza"]): r["id"] for r in reg if r["stato"] == "preparata"}
    for v in voci:
        ini = v["id"]
        pagine = pag.get(ini, [])
        url_pag = pagine[0]["url"] if pagine else (v.get("pagina_consip") or [""])[0] if v.get("pagina_consip") else ""
        live = [vivo[p["url"]] for p in pagine if p["url"] in vivo]
        ok = [x for x in live if x.get("http") == 200 and not x.get("blocco")]
        data_c = max((x["data"][:10] for x in live), default="")
        login = "sì" if any(x.get("login") or x.get("blocco") for x in live) else ("no" if ok else "ignoto")
        for p in pagine:
            x = vivo.get(p["url"])
            if x and (x.get("blocco") or x.get("login")):
                blocchi.append({"iniziativa": ini, "url": p["url"], "data": x["data"], "http": x.get("http"),
                                "tipo": "login" if x.get("login") else "blocco", "nota": x.get("errore", "")})
        nomi_vivi = " | ".join(n for x in ok for n in x["documenti"]).lower()
        livello_ok = "[V]" if ok else "[R]"
        nomi = pubblicati(ini, pagine, arch)
        # indice dei pubblicati per (tipo, di, numero)
        pub = defaultdict(dict)  # (tipo, di) -> {numero_int: [ident...]}
        pub_id = set()
        for n, u, sha in nomi:
            for m in RX_NOME.finditer(n):
                t = "sub-allegato" if m.group(1).lower().startswith("sub") else ("appendice" if m.group(1).lower().startswith("appendic")
                                                                                  else ("annesso" if m.group(1).lower().startswith("annes") else "allegato"))
                idn, num = ident(m.group(2))
                di = di_da_nome(n[m.end():m.end() + 30])
                pub[(t, di)].setdefault(num if num is not None else idn, []).append((n, sha))
                pub_id.add((t, idn))
                pub_id.add((t, str(num)))
        cit = {}
        sig = re.match(r"consip-(\d{4})$", ini)
        for r in rim.get(ini, []):
            idn, num = ident(r["numero"])
            altra = re.search(r"\bID[ _]*(\d{4})\b", r["documento"])
            if sig and altra and altra.group(1) != sig.group(1):
                continue  # documento di un'altra gara linkato per errore sulla pagina
            if PLURALE_E.search(r["citazione"]):
                continue
            proprio = r["documento"].rsplit("/", 1)[-1].rsplit("#", 1)[-1]
            if any(ident(m.group(2))[0] == idn for m in RX_NOME.finditer(proprio)):
                continue  # il documento cita sé stesso (intestazione «ALLEGATO 9 …»): è pubblicato
            if any(re.sub(r"[\s.-]", "", m.group(2)).upper() == idn.replace(".", "") for m in PLURALE.finditer(r["citazione"])):
                continue  # «Allegati 21» negli indici o elenchi al plurale: troppo ambiguo
            mm = re.search(r"(?i)(allegat|appendic|annes)\w*\s+(?:n\.?\s*)?" + re.escape(r["numero"]), r["citazione"])
            dopo = r["citazione"][mm.end():mm.end() + 45] if mm else r["titolo"]
            if re.fullmatch(r"[A-Z]{2,}", idn) or re.fullmatch(r"[\d\s.]*", r["titolo"]) and r["titolo"] or "...." in r["citazione"]:
                continue  # «APPENDICE AL CAPITOLATO», numeri di pagina e indici
            if ROMANI.match(idn) or NORMA.search(dopo):
                continue  # allegati di norme (codice, decreti) o di altri soggetti
            cit.setdefault((r["tipo"], idn), r)
        viste = set()
        # metodo 1: buchi di numerazione
        for (t, di), serie in sorted(pub.items()):
            interi = sorted(k for k in serie if isinstance(k, int))
            lettere = sorted(k for k in serie if isinstance(k, str) and len(k) == 1 and k.isalpha())
            mancanti = [str(k) for k in range(1, interi[-1]) if k not in interi] if len(interi) >= 2 else []
            if len(lettere) >= 2:
                mancanti += [chr(c) for c in range(ord("A"), ord(lettere[-1])) if chr(c) not in lettere]
            for k in mancanti:
                lato = [serie[j][0] for j in serie if isinstance(j, int) and str(j) in (str(int(k) - 1), str(int(k) + 1))] if k.isdigit() else []
                r = cit.get((t, k))
                doc = f"{t.capitalize()} {k}" + (f" al/allo {di}" if di else "")
                tit = pulisci(r["titolo"]) if r else ""
                ev = "numerazione: presenti " + ", ".join(str(j) for j in interi[:30] + lettere) + "; vicini: " + \
                     "; ".join(f"{n} (sha256 {s[:12]})" for n, s in lato[:2])
                if r:
                    ev += f" | citato in «{r['documento']}» p. {r['pagina']} (sha256 {r['sha256'][:12]}): «{r['citazione'][:160]}»"
                righe.append({"iniziativa": ini, "documento_atteso": doc + (f" – {tit}" if tit else ""),
                              "metodo": "numerazione" + (";rimando" if r else ""), "evidenza": ev,
                              "contenuto_presunto": tit or "non dedotto (numero saltato: forse ritirato, rinumerato o non pubblicato)",
                              "base_normativa": "Documenti di gara: messa a disposizione integrale e gratuita (art. 25, 27 e 85 d.lgs. 36/2023) [R]",
                              "criticita": critic(tit or "", 1), "livello": livello_ok if k.lower() not in nomi_vivi else "[R]",
                              "data_controllo": data_c, "url_pagina": url_pag, "bozza_accesso_civico": "", "dietro_login": login})
                viste.add((t, k))
        # metodo 2: rimandi non pubblicati
        for (t, idn), r in sorted(cit.items()):
            num = ident(idn)[1]
            if (t, idn) in viste or (t, idn) in pub_id or (num is not None and (t, str(num)) in pub_id and not re.search(r"[A-Z]", idn)):
                continue
            offerta = r["di"] == "offerta" or re.search(r"(?i)offert", r["titolo"])
            tit = pulisci(r["titolo"])
            righe.append({"iniziativa": ini, "documento_atteso": f"{t.capitalize()} {idn}" + (f" {('al/allo ' + r['di']) if r['di'] else ''}") + (f" – {tit}" if tit else ""),
                          "metodo": "rimando",
                          "evidenza": f"«{r['citazione'][:200]}» — {r['documento']}, p. {r['pagina']}, sha256 {r['sha256']} ({r['n_citazioni']} citazioni)",
                          "contenuto_presunto": (tit or "titolo non leggibile dal rimando") + (" (parte dell'offerta dell'aggiudicatario)" if offerta else ""),
                          "base_normativa": ("Offerta: messa a disposizione dei soli concorrenti (art. 36 d.lgs. 36/2023) [R]; per chiunque accesso civico generalizzato (art. 5 c. 2 d.lgs. 33/2013) [V]"
                                             if offerta else "Documenti di gara: messa a disposizione integrale (art. 25, 27, 85 d.lgs. 36/2023) [R]"),
                          "criticita": critic(tit + " " + r["citazione"][-120:], 2 if offerta else 1), "livello": livello_ok,
                          "data_controllo": data_c, "url_pagina": url_pag, "bozza_accesso_civico": "", "dietro_login": login})
        # metodo 3: attesi per legge o prassi
        for m in v["mancanze"]:
            if m["tipo"] not in ATTESI:
                continue
            doc, cr, c, base = ATTESI[m["tipo"]]
            if ok and re.search(PRESENTE[m["tipo"]], nomi_vivi):
                continue  # ora c'è sulla pagina: non mancante
            b = car[c]["base"] if c else base
            lv = "[V]" if (m["stato"] == "non-pubblicato" and ok) else "[R]"
            dl = login
            if m["tipo"] in ("listini", "offerta_economica", "transato_monitoraggio") and v.get("aretepa"):
                dl = "ignoto"  # acquistinretepa mostra prezzi e residuo solo a utenti registrati [R]: da provare con Fabio
            righe.append({"iniziativa": ini, "documento_atteso": doc, "metodo": "atteso",
                          "evidenza": f"inventario: stato «{m['stato']}» ({m.get('fonte', '')})" + (f"; classe {c}" if c else "")
                                      + ("; pagina ricontrollata dal vivo senza file del tipo" if ok else "; pagina ufficiale non ricontrollata/non individuata"),
                          "contenuto_presunto": m["descrizione"], "base_normativa": b, "criticita": cr, "livello": lv,
                          "data_controllo": data_c, "url_pagina": url_pag, "bozza_accesso_civico": per_reg.get((ini, c), "") if c else "",
                          "dietro_login": dl})
        if v["tipo_soggetto"] == "consip" and v["stato_iniziativa"] == "attiva" and ok and not re.search(MODIFICA, nomi_vivi):
            righe.append({"iniziativa": ini, "documento_atteso": "Atti di proroga, incremento del massimale o modifica (se adottati)",
                          "metodo": "atteso", "evidenza": "nessun file con proroga/incremento/estensione/modifica/quinto sulla pagina ricontrollata",
                          "contenuto_presunto": "atti di modifica della convenzione/AQ in corso di validità (esistenza non accertata)",
                          "base_normativa": "Modifiche dei contratti: art. 120 d.lgs. 36/2023, avviso ex c. 14 e pubblicazione ex art. 28 [R]",
                          "criticita": 2, "livello": "[R]", "data_controllo": data_c, "url_pagina": url_pag,
                          "bozza_accesso_civico": "", "dietro_login": login})
    for c in yaml.safe_load(open(DB / "documenti-mancanti-curati.yaml", encoding="utf-8")) or []:
        v = next(x for x in voci if x["id"] == c["iniziativa"])
        pg = pag.get(c["iniziativa"], [])
        lv = [vivo[p["url"]] for p in pg if p["url"] in vivo]
        righe.append({**{k: c[k] for k in ("iniziativa", "documento_atteso", "metodo", "evidenza", "contenuto_presunto", "base_normativa", "criticita", "livello")},
                      "data_controllo": max((x["data"][:10] for x in lv), default=""), "url_pagina": pg[0]["url"] if pg else "",
                      "bozza_accesso_civico": {(r["iniziativa"], r["carenza"]): r["id"] for r in reg if r["stato"] == "preparata"}.get((c["iniziativa"], c.get("carenza")), ""),
                      "dietro_login": "no" if lv else "ignoto"})
    righe.sort(key=lambda r: (r["iniziativa"], -r["criticita"], r["metodo"], r["documento_atteso"]))
    prepara_bozze(voci, righe, scrivi=bozze)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPI)
        w.writeheader()
        w.writerows(righe)
    with open(BLOCCHI, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["iniziativa", "url", "data", "http", "tipo", "nota"])
        w.writeheader()
        w.writerows(sorted(blocchi, key=lambda b: (b["iniziativa"], b["url"])))
    print(len(righe), "righe;", len(blocchi), "blocchi")
    return righe


def destinatario(v):
    if v["tipo_soggetto"] == "consip":
        return "Consip S.p.A."
    if v["tipo_soggetto"] == "psn":
        return "Presidenza del Consiglio dei ministri - Dipartimento per la trasformazione digitale"
    return v["stazione_appaltante"]


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:50]


def prepara_bozze(voci, righe, scrivi=False):
    """Una bozza per destinatario con i mancanti di criticità 3 e 2 non coperti da una bozza «preparata». NON si invia nulla.
    Solo i mancanti [V] o ricavati dai testi (numerazione/rimando): gli «attesi» [R] restano da verificare prima di chiedere."""
    per_id = {v["id"]: v for v in voci}
    reg_p = AC / "registro.csv"
    reg = {r["id"]: r for r in csv.DictReader(open(reg_p, encoding="utf-8"))}
    campi = list(next(iter(reg.values())).keys())
    gruppi = defaultdict(list)
    for r in righe:
        if r["criticita"] >= 2 and not r["bozza_accesso_civico"] and (r["livello"] == "[V]" or r["metodo"] != "atteso"):
            # chi detiene i documenti: la centrale che ha pubblicato la pagina (Consip anche per le gare su delega di un ente)
            gruppi["Consip S.p.A." if "consip.it" in r["url_pagina"] else destinatario(per_id[r["iniziativa"]])].append(r)
    for dest, rr in sorted(gruppi.items()):
        iid = "mancanti-" + slug(dest)
        if iid in reg and reg[iid]["stato"] not in ("preparata", "ritirata"):
            continue
        elenco = []
        for ini in sorted({r["iniziativa"] for r in rr}):
            v = per_id[ini]
            cig = ", ".join(x["cig_padre"] for x in v["lotti"][:6]) + (" e altri" if len(v["lotti"]) > 6 else "")
            pg = next((r["url_pagina"] for r in rr if r["iniziativa"] == ini), "") or "-"
            elenco.append(f"\n**{v['nome'][:140]}** (CIG dei lotti: {cig or '-'}; pagina: {pg})\n")
            for r in rr:
                if r["iniziativa"] == ini:
                    elenco.append(f"- {r['documento_atteso']} (criticità {r['criticita']}, {r['metodo']})")
                    r["bozza_accesso_civico"] = iid
        testo = ("Ai sensi dell'art. 5, comma 2, del d.lgs. 33/2013 chiedo copia dei seguenti documenti, che non risultano pubblicati "
                 "sulle pagine ufficiali delle iniziative alla data del controllo indicata, oppure risultano citati negli atti pubblicati "
                 "ma non allegati:\n\n" + "\n".join(elenco) +
                 "\n\nPer le offerte accetto l'oscuramento delle parti motivatamente dichiarate segreto tecnico o commerciale. "
                 "Chiedo i documenti nel formato in cui sono già detenuti, senza elaborazione; in caso di limiti ex art. 5-bis, "
                 "l'accesso parziale con oscuramento delle sole parti sottratte.")
        if not scrivi:
            continue
        ist = {"formato": "spesaict.istanza/1", "id": iid, "tipo": "accesso-civico-generalizzato", "base": "art. 5 c. 2 d.lgs. 33/2013",
               "destinatario": dest, "oggetto": f"Istanza di accesso civico generalizzato: documenti non pubblicati di {len({r['iniziativa'] for r in rr})} iniziative ICT",
               "testo": testo, "documenti": [{k: r[k] for k in ("iniziativa", "documento_atteso", "metodo", "criticita", "livello", "evidenza")} for r in rr],
               "riferimenti": ["report/convenzioni/database/documenti-mancanti.csv", "report/convenzioni/accesso-civico/analisi-dinieghi.md"],
               "preparata": DATA_BOZZE, "inviata": None, "approvazione": "da approvare (Fabio)"}
        (AC / "bozze" / f"{iid}.json").write_text(json.dumps(ist, ensure_ascii=False, indent=1), encoding="utf-8")
        (AC / "bozze" / f"{iid}.md").write_text(f"# {ist['oggetto']}\n\n**Bozza non inviata** ({DATA_BOZZE}). Destinatario: {dest}, "
                                                 "ufficio per l'accesso civico o RPCT (indirizzo da ricavare dalla sezione trasparenza).\n\n"
                                                 f"{testo}\n\nEvidenze per riga: `report/convenzioni/database/documenti-mancanti.csv`.\n", encoding="utf-8")
        reg[iid] = {**{k: "" for k in campi}, "id": iid, "iniziativa": ";".join(sorted({r["iniziativa"] for r in rr})), "carenza": "documenti-mancanti",
                    "destinatario": dest, "stato": "preparata", "preparata": DATA_BOZZE, "note": f"{len(rr)} documenti (criticità 2-3)"}
    if not scrivi:
        return
    with open(reg_p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campi)
        w.writeheader()
        for k in sorted(reg):
            w.writerow(reg[k])


if __name__ == "__main__":
    main("--bozze" in sys.argv)
