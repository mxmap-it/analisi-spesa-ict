#!/usr/bin/env python3
"""#58 Elenco unico dei documenti mancanti, candidato all'accesso civico generalizzato (L7). NON GENERA RICHIESTE, NON INVIA.

Unisce due fonti:
  A) convenzioni (#62): report/convenzioni/database/documenti-mancanti.csv (una riga = iniziativa x documento atteso);
  B) residuo imbuto (#57): lavoro/residuo-s6/ingresso.csv (CIG S6 e affini, priorità P1-P5) dopo i livelli L0-L6,
     con esito da esiti/<DATA_66>/imbuto/residuo-s6-per-66.csv (materiale), lavoro/residuo-s6/out/esiti.jsonl (L3/MePA),
     lavoro/residuo-s6/l4/esiti.jsonl (L4) e strato/sottoclasse da lavoro/imbuto/ict.csv.
Esclude ciò che risulta pubblicato: per B i CIG con «documento-cita-cig» (il documento c'è, va solo letto);
per A le voci già scartate stanno in documenti-mancanti-scartati.csv e non sono nell'inventario.
Ente: codice fiscale dall'ANAC (cf_amministrazione_appaltante del CIG; per le iniziative senza CIG, dal nome della
stazione appaltante o, per Consip, dal CF noto); codice IPA e PEC da IndicePA (amministrazioni.txt nel mirror, prima
mail di tipo Pec). RPCT: IndicePA non lo riporta (nome_resp/cogn_resp = responsabile dell'ente, NON l'RPCT): colonna
«rpct» vuota, da ricavare dalla sezione Amministrazione trasparente al momento della preparazione.
Priorità = criticità (1-3) x peso del valore (1 + log10(1 + importo/100.000), max 5), dove per B la criticità viene
dalla classe: P1 incerti ICT 3, P3 G2 informazione mancante 3, P2 G3 2, P4 nuovi RX 2, P5 G4 campione 1;
-1 se c'è già una pagina con il CIG o un documento senza CIG (resta da chiedere, ma meno urgente).
Uscite in esiti/<DATA>/accesso-civico/: elenco-mancanti.csv (~20 MB, NON versionato) e elenco-mancanti.csv.gz (versionato), enti.csv (accorpamento per ente), stima-ondate.json.
Uso (server): nice .venv/bin/python tools/accesso_civico/elenco_mancanti.py [DATA] [--data-66 AAAA-MM-GG]
"""
import collections, csv, datetime, json, math, sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/analisi"))
csv.field_size_limit(10**9)
IPA = R / ("archivio/mirror/indicepa.gov.it/ipa-dati/dataset/502ff370-1b2c-4310-94c7-f39ceb7500e3/resource/"
           "3ed63523-ff9c-41f6-a6fe-980f3d9e501f/download/amministrazioni.txt")
CF_CONSIP = "05359681003"
CRIT_B = {"P1-incerti-ict": 3, "P3-g2": 3, "P2-g3": 2, "P4-nuovi-rx": 2, "P5-g4-campione": 1}
TETTI = [5, 10, 20, 50]
CAMPI = ["fonte", "id", "cig", "cf", "codice_ipa", "ente", "pec", "pec_fonte", "rpct", "oggetto", "documento_atteso",
         "importo", "anno", "criticita", "peso_valore", "priorita", "livelli_tentati", "esito_livelli", "note"]


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if p.exists() else []


def peso(imp):
    return round(min(5.0, 1 + math.log10(1 + max(imp, 0) / 1e5)), 3)


def norm(s):
    return " ".join((s or "").upper().replace(".", " ").replace(",", " ").split())


def indicepa():
    per_cf = {}
    for r in csv.DictReader(open(IPA, encoding="utf-8-sig"), delimiter="\t"):
        pec = next((r[f"mail{i}"] for i in range(1, 6) if (r.get(f"tipo_mail{i}") or "").lower() == "pec"
                    and r.get(f"mail{i}") not in (None, "", "null")), "")
        cf = (r.get("cf") or "").strip()
        if cf and (cf not in per_cf or (pec and not per_cf[cf]["pec"])):
            per_cf[cf] = {"codice_ipa": r["cod_amm"], "ente": r["des_amm"], "pec": pec}
    return per_cf


def dettagli_documento(sottoclasse, materiale, cig, oggetto):
    base = (f"atto di affidamento/aggiudicazione (determina o delibera) e contratto, ordinativo o contratto attuativo "
            f"relativo al CIG {cig}")
    if "licenz" in sottoclasse:
        extra = "con l'elenco dei prodotti software e dei produttori (marchi) acquistati, quantità e durata delle licenze"
    elif "cloud" in sottoclasse or "psn" in sottoclasse:
        extra = ("con servizi cloud acquistati, fornitore del servizio e del prodotto (provider), localizzazione "
                 "dei data center/region, durata e importo")
    else:
        extra = ("con la descrizione dei beni/servizi ICT (prodotti, marchi, eventuale servizio cloud e suo provider), "
                 "fornitore, durata e importo")
    if materiale == "solo-pagina-con-cig":
        extra += "; la pagina pubblica cita il CIG ma non contiene l'atto"
    elif materiale == "documento-senza-cig":
        extra += "; i documenti pubblicati trovati non citano il CIG"
    return f"{base}, {extra}"


def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    data = a[0] if a else str(datetime.date.today())
    d66 = sys.argv[sys.argv.index("--data-66") + 1] if "--data-66" in sys.argv else "2026-11-09"
    out = R / f"esiti/{data}/accesso-civico"; out.mkdir(parents=True, exist_ok=True)
    ipa = indicepa()

    # --- B: residuo imbuto ---
    D = R / "lavoro/residuo-s6"
    ing = {r["cig"]: r for r in csv.DictReader(open(D / "ingresso.csv", encoding="utf-8")) if r.get("priorita") in CRIT_B}
    p66 = {r["cig"]: r for r in csv.DictReader(open(R / f"esiti/{d66}/imbuto/residuo-s6-per-66.csv", encoding="utf-8"))}
    l3 = {r["cig"]: r for r in jl(D / "out/esiti.jsonl")}
    l4 = {r["cig"]: r for r in jl(D / "l4/esiti.jsonl")}
    ict = {}
    for r in csv.DictReader(open(R / "lavoro/imbuto/ict.csv", encoding="utf-8")):
        if r["cig"] in ing: ict[r["cig"]] = r
    # CF dal dataset ANAC dei CIG (anni del residuo + delta) e mappa nome -> CF per le convenzioni
    from attribuisci_provider import righe_cig
    conv = list(csv.DictReader(open(R / "report/convenzioni/database/documenti-mancanti.csv", encoding="utf-8")))
    ini = {i["id"]: i for i in json.load(open(R / "report/convenzioni/database/iniziative.json", encoding="utf-8"))}
    serve = set(ing) | {c["iniziativa"][4:].upper() for c in conv if c["iniziativa"].startswith("cig-")}
    nomi_sa = {norm(i.get("stazione_appaltante")) for i in ini.values()}
    cf_cig, cf_nome = {}, {}
    anni = sorted({(r.get("anno") or "").strip() for r in ing.values()} - {""}) + ["delta"]
    for fonte in anni:
        try:
            for r in righe_cig(fonte):
                c = r["cig"]
                if c in serve: cf_cig[c] = (r["cf_amministrazione_appaltante"].strip(), r["denominazione_amministrazione_appaltante"])
                n = norm(r["denominazione_amministrazione_appaltante"])
                if n in nomi_sa: cf_nome.setdefault(n, r["cf_amministrazione_appaltante"].strip())
        except Exception as e:  # anno mancante nel mirror: lo si dice
            print("fonte", fonte, "non letta:", e, file=sys.stderr)

    righe, esclusi = [], collections.Counter()
    for c, r in ing.items():
        m = (p66.get(c) or {}).get("materiale", "nulla")
        if m == "documento-cita-cig": esclusi["B: documento che cita il CIG già trovato"] += 1; continue
        imp = float(r.get("importo") or 0)
        cf, nome = cf_cig.get(c, ("", r["stazione_appaltante"]))
        e = ipa.get(cf, {})
        tent = ["L0-L2 via 6/PVL (imbuto)"]; esi = []
        if c in l3: tent.append("L3" if l3[c].get("famiglia") != "mepa" else "MePA"); esi.append(f"L3:{l3[c].get('esito')}")
        if c in l4: tent.append("L4 AT"); esi.append(f"L4:{l4[c].get('esito')}")
        esi.append(f"materiale:{m}")
        cr = CRIT_B[r["priorita"]] - (1 if m in ("solo-pagina-con-cig", "documento-senza-cig") else 0)
        cr = max(cr, 1)
        sc = (ict.get(c) or {}).get("sottoclasse", "")
        righe.append({"fonte": "B-residuo-imbuto", "id": f"{r['priorita']}:{c}", "cig": c, "cf": cf, "codice_ipa": e.get("codice_ipa", ""),
                      "ente": e.get("ente") or nome, "pec": e.get("pec", ""), "pec_fonte": "IndicePA" if e.get("pec") else "",
                      "rpct": "", "oggetto": (r.get("oggetto") or "")[:300],
                      "documento_atteso": dettagli_documento(sc, m, c, r.get("oggetto")), "importo": imp, "anno": r.get("anno", ""),
                      "criticita": cr, "peso_valore": peso(imp), "priorita": round(cr * peso(imp), 3),
                      "livelli_tentati": " ; ".join(tent), "esito_livelli": " ; ".join(esi),
                      "note": f"strato {(ict.get(c) or {}).get('strato', '?')} {sc}".strip()})

    # --- A: convenzioni ---
    for x in conv:
        i = ini.get(x["iniziativa"], {})
        c = x["iniziativa"][4:].upper() if x["iniziativa"].startswith("cig-") else ""
        if c and c in cf_cig: cf = cf_cig[c][0]
        elif x["iniziativa"].startswith(("consip", "psn")) or "CONSIP" in norm(i.get("stazione_appaltante")): cf = CF_CONSIP
        else: cf = cf_nome.get(norm(i.get("stazione_appaltante")), "")
        if x["iniziativa"] == "psn": cf = ""  # destinatario: Presidenza del Consiglio (DTD), bozza dedicata
        e = ipa.get(cf, {})
        imp = float(i.get("valore_ict_2024_2025") or 0)
        cr = int(x["criticita"] or 1)
        righe.append({"fonte": "A-convenzioni", "id": f"{x['iniziativa']}:{x['documento_atteso'][:60]}", "cig": c, "cf": cf,
                      "codice_ipa": e.get("codice_ipa", ""), "ente": e.get("ente") or i.get("stazione_appaltante", "") or x["iniziativa"],
                      "pec": e.get("pec", ""), "pec_fonte": "IndicePA" if e.get("pec") else "", "rpct": "",
                      "oggetto": (i.get("nome") or "")[:300], "documento_atteso": f"{x['documento_atteso']} ({x['contenuto_presunto']})",
                      "importo": imp, "anno": "", "criticita": cr, "peso_valore": peso(imp), "priorita": round(cr * peso(imp), 3),
                      "livelli_tentati": f"{x['metodo']}; pagina {x['url_pagina'] or '-'}; dietro_login {x['dietro_login']}",
                      "esito_livelli": x["evidenza"][:500], "note": f"livello {x['livello']}; bozza {x['bozza_accesso_civico'] or '-'}"})

    righe.sort(key=lambda r: -r["priorita"])
    with open(out / "elenco-mancanti.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, CAMPI); w.writeheader(); w.writerows(righe)
    import gzip, shutil
    with open(out / "elenco-mancanti.csv", "rb") as s, gzip.GzipFile(out / "elenco-mancanti.csv.gz", "wb", mtime=0) as g: shutil.copyfileobj(s, g)

    # --- accorpamento per ente e stima delle ondate ---
    per = collections.defaultdict(list)
    for r in righe: per[r["cf"] or "senza-cf:" + norm(r["ente"])].append(r)
    enti = []
    for k, v in per.items():
        enti.append({"cf": k, "ente": v[0]["ente"], "codice_ipa": v[0]["codice_ipa"], "pec": v[0]["pec"], "voci": len(v),
                     "voci_A": sum(r["fonte"].startswith("A") for r in v), "voci_B": sum(r["fonte"].startswith("B") for r in v),
                     "euro": round(sum(r["importo"] for r in v if r["fonte"].startswith("B"))),
                     "priorita_somma": round(sum(r["priorita"] for r in v), 2), "priorita_max": max(r["priorita"] for r in v)})
    enti.sort(key=lambda e: -e["priorita_somma"])
    with open(out / "enti.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, list(enti[0])); w.writeheader(); w.writerows(enti)
    n = [e["voci"] for e in enti]
    fasce = collections.Counter("1" if x == 1 else "2-5" if x <= 5 else "6-20" if x <= 20 else "21-100" if x <= 100 else ">100" for x in n)
    stima = {"data": data, "voci": len(righe), "voci_A": sum(r["fonte"].startswith("A") for r in righe),
             "voci_B": sum(r["fonte"].startswith("B") for r in righe), "esclusi": dict(esclusi),
             "euro_B": round(sum(r["importo"] for r in righe if r["fonte"].startswith("B"))),
             "enti": len(enti), "enti_senza_cf": sum(e["cf"].startswith("senza-cf") for e in enti),
             "enti_senza_pec": sum(not e["pec"] for e in enti), "voci_senza_pec": sum(not r["pec"] for r in righe),
             "distribuzione_voci_per_ente": dict(sorted(fasce.items())), "max_voci_ente": max(n),
             "primi_10_enti": [{k: e[k] for k in ("ente", "cf", "voci", "euro")} for e in enti[:10]],
             "ondate": {}}
    for t in TETTI:  # una richiesta per ente per ondata, al massimo t voci accorpate per richiesta
        stima["ondate"][f"tetto_{t}"] = {"richieste_totali": sum(math.ceil(x / t) for x in n),
                                         "ondate_per_esaurire": math.ceil(max(n) / t),
                                         "richieste_ondata_1": len(n),
                                         "richieste_ondata_2": sum(x > t for x in n),
                                         "richieste_ondata_3": sum(x > 2 * t for x in n)}
    json.dump(stima, open(out / "stima-ondate.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in stima.items() if k != "primi_10_enti"}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
