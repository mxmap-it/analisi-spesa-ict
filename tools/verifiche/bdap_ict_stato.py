"""#67 BDAP nell'imbuto: spesa ICT del Bilancio dello Stato per ministero e anno, e copertura dei CIG ICT.

Tre misure, tutte da file BDAP archiviati (archivio/mirror/bdap-opendata.rgs.mef.gov.it/..., sha256 nell'esito):
 1. Rendiconto per Piano di gestione (PG, serie 2019-2024): PG ICT per classificazione economica di 3° livello
    (CE 2.2.19 servizi informatici e TLC, 21.1.1 licenze, 21.1.2 sviluppo software, 21.2.5 infrastrutture telematiche,
    21.2.19 hardware) e, separatamente, per regola sul nome del capitolo/PG. Euro = Pagato CS (cassa, competenza + residui).
 2. Rendiconto per Capitolo (serie 2019-2024): lo stesso sul «Codice Puntato CE» del capitolo.
 3. Pagamenti con mandati informatici per codice gestionale (consuntivo 2022-2025): i 11 gestionali ICT
    (032 materiale informatico, 051/052 manutenzione hw/sw, 056 noleggi hw, 036 consulenza informatica, 206 software
    prodotto, 233 hardware, 276/277 manut. straordinaria, 289 licenze, 290 sviluppo sw). È il denominatore più fine.
 4. Copertura: importo dei CIG ICT (lavoro/imbuto/ict.csv, strati S3-S6, senza padri AQ S0 e sotto soglia S2) delle
    stazioni appaltanti ministeriali, per anno, contro il pagato ICT per gestionale. Grandezze diverse (valore del contratto
    contro cassa annua): il rapporto è un indicatore d'ordine di grandezza, non una percentuale di copertura.

Uso (server): nice .venv/bin/python tools/verifiche/bdap_ict_stato.py -> esiti/<oggi>/bdap/ict-stato.{json,csv}
Lo stesso dallo snapshot: i file si cercano nella vista mirror dell'archivio (ARCHIVIO_ROOT), con sha256 registrato."""
import csv, collections, datetime, hashlib, json, os, re, sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]
ARC = Path(os.environ.get("ARCHIVIO_ROOT", R / "archivio"))
DUMP = ARC / "mirror/bdap-opendata.rgs.mef.gov.it/SpodCkanApi/api/3/datastore/dump"
# risorse CKAN (datastore/dump/<id>.csv), dai metadati in lavoro/bdap-pagine (tools/acquisizione/bdap_metadati.sh)
PG = {2019: "3d71a658-a9a0-4b1c-a210-2c1b0a2a6878", 2020: "658002af-c4ee-4731-8daf-8dfa4f64567f",
      2021: "aedc9cb7-e787-450c-8034-f2fb417d2367", 2022: "56e43168-0527-47be-aecb-769c721f7ed7",
      2023: "587d1a31-4ff0-457b-9b94-da58a658b063", 2024: "d73a538b-5652-463f-8c97-b09b3ec818cd"}
CAP = {2019: "6ec860e9-5583-478d-b203-a7ad87a463f8", 2020: "e008e761-e602-4277-b619-d3e3a45fe8e3",
       2021: "e7a17214-3b88-451e-a411-26d1d6691efc", 2022: "c72b5f41-8de9-45b4-b2b4-21fab3f4ba57",
       2023: "57ef91e8-960f-4937-8669-e30998e69bff", 2024: "940dd84e-6b32-4286-a3a3-2bbd74d96c4e"}
MICGS = {2022: "92d90dbc-465c-4aa8-8766-021668dbb41d", 2023: "c5a04b27-6fa2-40d0-9516-f3d5f1f9fd55",
         2024: "f945fcf7-580c-4d25-b309-68f4c7a5f45f", 2025: "9c17c64c-bb7d-40b5-84c7-3e39f1cb7727"}
CE_ICT = {"2.2.19", "21.1.1", "21.1.2", "21.2.5", "21.2.19"}
GEST_ICT = {"032", "036", "051", "052", "056", "206", "233", "276", "277", "289", "290"}
RX_NOME = re.compile(r"informatic|telematic|sistem\w*\s+informativ|software|hardware|elaborazion\w*\s+(automatica\s+)?(dei\s+)?dati|"
                     r"\bcloud\b|data\s*cent|cybersicurezza|sicurezza\s+informatica|meccanizzazion|automazione\s+(degli\s+)?uffici|"
                     r"transizione\s+digitale|digitalizzazion", re.I)
# stazioni appaltanti (nome ANAC) -> ministero (nome BDAP abbreviato); prima regola che corrisponde
MIN = [("INTERNO", r"\bINTERNO\b|PREFETTUR|QUESTUR|VIGILI DEL FUOCO|P\.S\.|POLIZIA DI STATO"),
       ("DIFESA", r"DIFESA|CARABINIERI|ESERCITO|MARINA MILITARE|AERONAUTICA"),
       ("GIUSTIZIA", r"GIUSTIZIA|PENITENZIARI|CASA CIRCONDARIALE|CASA DI RECLUSIONE|MINORIL"),
       ("ECONOMIA E FINANZE", r"ECONOMIA E DELLE FINANZE|GUARDIA DI FINANZA|RAGIONERIA"),
       ("ESTERI", r"AFFARI ESTERI"), ("INFRASTRUTTURE", r"INFRASTRUTTUR|M\.C\.T\.C|MOTORIZZAZIONE|CAPITANERIA|OO\.?PP"),
       ("ISTRUZIONE", r"ISTRUZIONE"), ("UNIVERSITA", r"UNIVERSITA' E DELLA RICERCA|UNIVERSITA E RICERCA"),
       ("CULTURA", r"BENI E DELLE ATTIVITA|MINISTERO DELLA CULTURA|BENI CULTURALI"), ("SALUTE", r"SALUTE"),
       ("LAVORO", r"LAVORO E DELLE POLITICHE SOCIALI"), ("AGRICOLTURA", r"AGRICOL|FORESTAL"),
       ("AMBIENTE", r"AMBIENTE|TRANSIZIONE ECOLOGICA"), ("IMPRESE", r"SVILUPPO ECONOMICO|IMPRESE E DEL MADE"),
       ("TURISMO", r"MINISTERO DEL TURISMO")]
RX_SA_STATO = re.compile(r"^\W*MINISTERO|PREFETTUR|QUESTUR|CARABINIERI|GUARDIA DI FINANZA|VIGILI DEL FUOCO|CAPITANERIA", re.I)


def ministero(nome):
    n = nome.upper()
    for k, rx in MIN:
        if re.search(rx, n): return k
    return "ALTRO"


def leggi(rid):
    p = DUMP / f"{rid}.csv"
    if not p.exists(): return None, None
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    return list(csv.DictReader(open(p, encoding="cp1252", newline=""), delimiter=";")), {"file": str(p.relative_to(ARC)), "sha256": h}


def num(x):
    try: return float(x or 0)
    except ValueError: return 0.0


def main():
    csv.field_size_limit(10 ** 8)
    out = {"versione": "bdap-ict-stato 0.2 (2026-11-09)", "ingressi": {}, "regole": {"ce_ict": sorted(CE_ICT),
           "gestionali_ict": sorted(GEST_ICT), "nome": RX_NOME.pattern}}
    # 1. PG, serie 2019-2024 (giro 0.2: la seconda via per anno, non solo il 2024)
    campione = []; out["pg_serie"] = {}
    for y, rid in PG.items():
        righe, meta = leggi(rid)
        if righe is None: continue
        out["ingressi"][f"pg-{y}"] = meta
        pg = collections.Counter(); pge = collections.Counter(); mce = collections.Counter()
        for x in righe:
            ce = f'{x["Codice Categoria"]}.{x["Codice CE 2° Livello"]}.{x["Codice CE 3° Livello"]}'
            a, b = ce in CE_ICT, bool(RX_NOME.search(x["Capitolo di Spesa"] + " " + x["Piano di Gestione"]))
            k = "ce+nome" if a and b else "solo-ce" if a else "solo-nome" if b else None
            if not k: continue
            pg[k] += 1; pge[k] += num(x["Pagato CS"])
            if a: mce[ministero(x["Amministrazione"])] += num(x["Pagato CS"])
            campione.append({"anno": y, "amministrazione": x["Amministrazione"], "capitolo": x["Numero Capitolo di Spesa"],
                             "pg": x["Numero Piano di Gestione"], "ce3": ce, "ce3_nome": x["CE 3° Livello"], "classe": k,
                             "nome": (x["Capitolo di Spesa"] + " | " + x["Piano di Gestione"])[:300], "pagato_cs": num(x["Pagato CS"])})
        out["pg_serie"][y] = {"pg_totali": len(righe), "per_classe": {k: {"pg": pg[k], "pagato_cs": round(pge[k])} for k in pg},
                              "ce_pagato_cs": round(pge["ce+nome"] + pge["solo-ce"]),
                              "ce_per_ministero": {k: round(v) for k, v in mce.most_common()}}
    out["pg_2024"] = out["pg_serie"][2024]
    # 2. Capitoli, serie
    serie = {}
    for y, rid in CAP.items():
        righe, meta = leggi(rid)
        if righe is None: continue
        out["ingressi"][f"cap-{y}"] = meta
        c = collections.Counter(); e = collections.Counter(); m = collections.Counter()
        for x in righe:
            a = x["Codice Puntato CE"] in CE_ICT; b = bool(RX_NOME.search(x["Capitolo di Spesa"]))
            if a or b:
                k = "ce" if a else "solo-nome"; c[k] += 1; e[k] += num(x["Pagato CS"])
                if a: m[ministero(x["Amministrazione"])] += num(x["Pagato CS"])
        serie[y] = {"capitoli": len(righe), "per_classe": {k: {"capitoli": c[k], "pagato_cs": round(e[k])} for k in c},
                    "ce_per_ministero": {k: round(v) for k, v in m.most_common()}}
    out["capitoli_serie"] = serie
    # 3. gestionali ICT
    gest = {}
    for y, rid in MICGS.items():
        righe, meta = leggi(rid)
        if righe is None: continue
        out["ingressi"][f"micgs-{y}"] = meta
        tot = collections.Counter(); per_g = collections.Counter(); per_m = collections.Counter()
        for x in righe:
            g = x["Codice Gestionale"][:3]
            if g in GEST_ICT:
                v = num(x["OP"]); tot["ict"] += v; per_g[x["Codice Gestionale"]] += v; per_m[ministero(x["Amministrazione"])] += v
            tot["tutto"] += num(x["OP"])
        gest[y] = {"op_ict": round(tot["ict"]), "op_totale": round(tot["tutto"]), "per_gestionale": {k: round(v) for k, v in per_g.most_common()},
                   "per_ministero": {k: round(v) for k, v in per_m.most_common()}}
    out["gestionali_ict"] = gest
    # 4. copertura CIG ICT dei ministeri
    cig = collections.defaultdict(collections.Counter); ncig = collections.defaultdict(collections.Counter)
    for r in csv.DictReader(open(R / "lavoro/imbuto/ict.csv", encoding="utf-8")):
        if r["strato"][:2] in ("S0", "S2") or r["importo_da_verificare"] == "1": continue
        if not RX_SA_STATO.search(r["stazione_appaltante"]): continue
        y = int(r["anno"]); m = ministero(r["stazione_appaltante"]); cig[y][m] += num(r["importo"]); ncig[y][m] += 1
    cop = {}
    for y in sorted(gest):
        cop[y] = {m: {"cig_ict_n": ncig[y][m], "cig_ict_importo": round(cig[y][m]), "bdap_op_ict": gest[y]["per_ministero"].get(m, 0),
                      "rapporto": round(cig[y][m] / gest[y]["per_ministero"][m], 2) if gest[y]["per_ministero"].get(m) else None}
                  for m in sorted(set(cig[y]) | set(gest[y]["per_ministero"]))}
    out["copertura_cig"] = cop
    o = R / f"esiti/{datetime.date.today().isoformat()}/bdap"; os.makedirs(o, exist_ok=True)
    json.dump(out, open(o / "ict-stato.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    with open(o / "pg-ict.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(campione[0])); w.writeheader(); w.writerows(sorted(campione, key=lambda r: (r["anno"], -r["pagato_cs"])))
    print(json.dumps({k: out[k] for k in ("pg_serie", "gestionali_ict")}, indent=1, ensure_ascii=False)[:6000])


if __name__ == "__main__":
    main()
