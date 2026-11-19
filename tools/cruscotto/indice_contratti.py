#!/usr/bin/env python3
"""Indice dei contratti dell'imbuto per il cruscotto (#53, mancanza M13; decisione di Fabio del 19/11/2026: «tutti i
contratti ricercabili e annotabili, con una dashboard, assieme alla pubblicazione dei risultati»).

Costruisce lavoro/cruscotto/contratti.sqlite (derivato, non in git, si rifà da zero con questo comando) con:
  contratti      una riga per CIG di lavoro/imbuto/ict.csv (tutti gli strati scritti dall'imbuto: S0, S2 ICT, S3-S6, dal 2020;
                 S1 non ICT e S2 non ICT non sono nel file), con la colonna «livelli» (quali livelli hanno detto qualcosa)
  contratti_fts  indice a testo pieno SQLite FTS5 su oggetto, stazione appaltante, aggiudicatari, CPV, CIG
  esiti          una riga per CIG e livello di raffinamento: L2, B1, B2, B4, L3, via 6, revisione, L4, licenze, tetti,
                 campione a cieco (Claude), acquisizione degli atti; esito, certezza, giurisdizione, dettaglio, file di origine
  bdncp          segnali B3 (durate) e B4 (PNRR) per CIG, senza codici fiscali
  atti           atti archiviati per CIG (dati/atti, schema spesaict.atto/1) con URL e sha256
  meta           versione dell'imbuto, data, sha256 di ogni ingresso
Nessun livello modifica l'imbuto: l'indice mostra lo strato dell'imbuto e, accanto, che cosa ha detto ogni livello.

Dati personali: gli aggiudicatari persone fisiche (codice fiscale personale di 16 caratteri nel dataset ANAC
«aggiudicatari») sono sostituiti da «[persona fisica]» nel campo aggiudicatari e, se il nome compare, nell'oggetto.
I codici fiscali non entrano nell'indice.

Esiti: esiti/<oggi>/cruscotto/indice.json (conteggi per livello, persone oscurate, sha256 degli ingressi).
Uso (sul server, come mxmap.it, un job pesante alla volta):
  flock lavoro/pesante.lock nice -n 15 .venv/bin/python tools/cruscotto/indice_contratti.py
Il file si scrive in .tmp e si sostituisce alla fine: il servizio (tools/annotazioni/server.py) può restare acceso.
"""
import csv, datetime, glob, hashlib, io, json, os, re, sqlite3, sys, zipfile
from pathlib import Path

R = Path(__file__).resolve().parents[2]
ICT = R / os.environ.get("IMBUTO_ICT", "lavoro/imbuto/ict.csv")
OUT = R / os.environ.get("CRUSCOTTO_DB", "lavoro/cruscotto/contratti.sqlite")
OGGI = os.environ.get("ESITI_DATA", datetime.date.today().isoformat())
ESITI = R / f"esiti/{OGGI}/cruscotto"
AGG = R / "archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/aggiudicatari/filesystem"
# codice fiscale di persona fisica (con le lettere dell'omocodia al posto delle cifre)
RX_CF_PF = re.compile(r"^[A-Z]{6}[0-9LMNPQRSTUV]{2}[A-Z][0-9LMNPQRSTUV]{2}[A-Z][0-9LMNPQRSTUV]{3}[A-Z]$")
RX_SOCIETA = re.compile(r"\b(S\.?R\.?L|S\.?P\.?A|S\.?N\.?C|S\.?A\.?S|S\.?C\.?A?R?\.?L|SOC|SOCIET|COOP|CONSORZ|SRLS|SAPA|ONLUS|"
                        r"FONDAZION|ASSOCIAZ|ENTE|UNIVERSIT|ISTITUT|AZIENDA|STUDIO ASSOCIATO|GROUP|ITALIA|LTD|GMBH|INC|SPA|SRL)\b", re.I)
PF = "[persona fisica]"
csv.field_size_limit(1 << 30)
ingressi = {}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


def usa(p):
    """registra l'ingresso (percorso relativo e sha256) e lo restituisce"""
    p = Path(p); ingressi[str(p.relative_to(R))] = sha(p); return p


def ultimo(modello):
    """l'esito più recente: esiti/<data>/... con la data più alta"""
    f = sorted(glob.glob(str(R / modello)))
    return usa(f[-1]) if f else None


def jl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def url(f):
    return f if isinstance(f, str) else (f or {}).get("url", "")


def persone(cigs):
    """cig -> nomi degli aggiudicatari persone fisiche, da tutti gli zip CSV del dataset aggiudicatari (pieno + mensili)"""
    pf = {}
    for z in sorted(AGG.glob("*aggiudicatari_csv.zip")):
        usa(z)
        with zipfile.ZipFile(z) as zf:
            for m in (i for i in zf.namelist() if i.endswith(".csv")):
                for r in csv.DictReader(io.TextIOWrapper(zf.open(m), encoding="utf-8-sig", errors="replace"), delimiter=";"):
                    if r["cig"] in cigs and RX_CF_PF.match((r.get("codice_fiscale") or "").strip().upper()):
                        pf.setdefault(r["cig"], set()).add((r["denominazione"] or "").strip().upper())
    return pf


def oscura(agg, testo, nomi):
    """sostituisce i nomi delle persone fisiche; se il CIG ha persone fisiche, oscura anche le parti senza forma societaria"""
    parti = []
    for p in [x.strip() for x in agg.split(" ; ")] if agg else []:
        # nome di persona fisica; parte senza forma societaria in un CIG con persone fisiche; codice fiscale personale come nome
        parti.append(PF if p.upper() in nomi or (nomi and not RX_SOCIETA.search(p)) or RX_CF_PF.match(p.upper()) else p)
    for n in sorted(nomi, key=len, reverse=True):
        if len(n) >= 5:
            testo = re.sub(re.escape(n), PF, testo, flags=re.I)
    return " ; ".join(parti), testo


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True); ESITI.mkdir(parents=True, exist_ok=True)
    tmp = OUT.with_suffix(".tmp")
    if tmp.exists(): tmp.unlink()
    c = sqlite3.connect(tmp)
    c.executescript("""
      PRAGMA journal_mode=OFF; PRAGMA synchronous=OFF; PRAGMA cache_size=-200000;
      CREATE TABLE meta (chiave TEXT PRIMARY KEY, valore TEXT);
      CREATE TABLE contratti (cig TEXT PRIMARY KEY, anno INTEGER, strato TEXT, sottoclasse TEXT, gruppo TEXT, via TEXT,
        provider TEXT, giurisdizione TEXT, servizio TEXT, cpv TEXT, cpv_ict INTEGER, importo REAL, importo_da_verificare INTEGER,
        ente TEXT, aggiudicatari TEXT, testo TEXT, livelli TEXT DEFAULT '', n_atti INTEGER DEFAULT 0, persona_fisica INTEGER DEFAULT 0);
      CREATE TABLE esiti (cig TEXT, livello TEXT, esito TEXT, certezza TEXT, giurisdizione TEXT, provider TEXT, dettaglio TEXT, fonte TEXT);
      CREATE TABLE bdncp (cig TEXT PRIMARY KEY, qe_evento TEXT, qe_quota_lavori REAL, data_pub TEXT, durata_prevista REAL,
        d0 TEXT, d1 TEXT, durata_eff REAL, flag_pnrr TEXT, ind_pnrr TEXT, cup TEXT, v3 TEXT);
      CREATE TABLE atti (cig TEXT, url TEXT, sha256 TEXT, tipo_atto TEXT, esito_recupero TEXT, recuperato_il TEXT, livello TEXT);
    """)
    # 1. contratti dell'imbuto
    ict = usa(ICT)
    cigs = set()
    with open(ict, encoding="utf-8") as f:
        for r in csv.DictReader(f): cigs.add(r["cig"])
    pf = persone(cigs)
    n = doppi = 0
    with open(ict, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            nomi = pf.get(r["cig"], set())
            agg, testo = oscura(r["aggiudicatari"], r["testo"], nomi)
            cur = c.execute("INSERT OR IGNORE INTO contratti (cig, anno, strato, sottoclasse, gruppo, via, provider, giurisdizione, servizio,"
                            " cpv, cpv_ict, importo, importo_da_verificare, ente, aggiudicatari, testo, persona_fisica) VALUES"
                            " (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                            (r["cig"], int(r["anno"]), r["strato"], r["sottoclasse"], r["gruppo"], r["via"], r["provider"], r["giurisdizione"],
                             r["servizio"], r["cod_cpv"], int(r["cpv_ict"] or 0), float(r["importo"] or 0), int(r["importo_da_verificare"] or 0),
                             r["stazione_appaltante"], agg, testo, int(bool(nomi) or PF in agg)))
            n += 1; doppi += cur.rowcount == 0
    # 2. esiti dei livelli
    E = []
    def es(cig, liv, esito, cert="", giur="", prov="", dett="", fonte=None):
        E.append((cig, liv, esito, cert, giur, prov, (dett or "")[:1500], str(fonte.relative_to(R)) if fonte else ""))

    if (p := ultimo("esiti/*/imbuto/raffinamento-l2.csv")):
        for r in csv.DictReader(open(p, encoding="utf-8")):
            es(r["cig"], "L2", "fuori-misura-cloud", "regola", dett=f"regola «{r['motivo']}» (periferiche, consumabili, cablaggio): resta ICT, non cloud", fonte=p)
    if (p := ultimo("esiti/*/imbuto/bdncp/segnali.csv")):
        for r in csv.DictReader(open(p, encoding="utf-8")):
            if r["cig"] not in cigs: continue
            c.execute("INSERT OR IGNORE INTO bdncp VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                      (r["cig"], r["qe_evento"], float(r["qe_quota_lavori"]) if r["qe_quota_lavori"] else None, r["data_pub"],
                       float(r["durata_prevista"]) if r["durata_prevista"] else None, r["d0"], r["d1"],
                       float(r["durata_eff"]) if r["durata_eff"] else None, r["flag_pnrr"], r["ind_pnrr"], r["cup"], r["v3"]))
            if r["b1"]:
                es(r["cig"], "B1", r["b1"], "regola", dett=f"quadro economico ({r['qe_evento']}): quota lavori {r['qe_quota_lavori']}", fonte=p)
            if r["b2"]:
                es(r["cig"], "B2", "in-house-" + r["b2"], "regola", dett="aggiudicatario " + {"ipa": "nell'Indice PA (soggetto pubblico): in-house regge",
                   "non-sa": "privato: in-house non regge", "sa-non-ipa": "registrato come stazione appaltante, non nell'Indice PA",
                   "senza-aggiudicatario": "nessun aggiudicatario pubblicato"}.get(r["b2"], r["b2"]), fonte=p)
            vie = [k for k, ok in (("FLAG_PNRR_PNC", r["flag_pnrr"] == "1"), ("indicatori-pnrrpnc", r["ind_pnrr"] == "True"),
                                   ("CUP", r["cup"] == "True"), (f"catena v3 misura {r['v3']}", bool(r["v3"]))) if ok]
            if vie:
                es(r["cig"], "B4", "pnrr", "segnale", dett="PNRR secondo: " + ", ".join(vie), fonte=p)
    if (p := ultimo("esiti/*/imbuto/raffinamento-l3.csv")):
        for r in csv.DictReader(open(p, encoding="utf-8")):
            es(r["cig"], "L3", r["esito_l3"], r["certezza"], dett=f"{r['categoria']}: {r['evidenza']}", fonte=p)

    def classif(p, liv):
        for d in jl(p):
            e = d.get("esito", {})
            a, b = e.get("asse_a", ""), e.get("asse_b", "")
            esito = f"A:{a} B:{b}" if a else f"cloud={e.get('e_cloud', '')}"
            rev = d.get("revisione") or {}
            dett = (e.get("motivazione") or "") + (f" [revisione: {rev.get('stato')}]" if rev.get("stato") else "")
            if d.get("fonti"): dett += " Fonti: " + " ".join(url(f) for f in d["fonti"][:5])
            es(d["cig"], liv, esito, e.get("confidenza", ""), e.get("giurisdizione", ""), e.get("provider_prodotto", ""), dett, p)
    for pat, liv in (("dati/classificazioni/imbuto-g1g3.jsonl", "via6"), ("dati/classificazioni/imbuto-revisione.jsonl", "revisione"),
                     ("dati/classificazioni/campione-v3.jsonl", "campione-cieco")):
        if (R / pat).exists(): classif(usa(R / pat), liv)
    for p in sorted((R / "report/metodo/llm/raffinamento-l4/esiti").glob("*.jsonl")):
        usa(p)
        for d in jl(p):
            a, b = d.get("asse_a", {}), d.get("asse_b", {})
            dett = " ".join(x for x in [d.get("motivazione", ""), "Atto: " + d["atto_ente"] if d.get("atto_ente") else "",
                                         "Fonti: " + " ".join(url(f) for f in d.get("fonti", [])[:5]) if d.get("fonti") else ""] if x)
            es(d["cig"], "L4", f"A:{a.get('stato', '')} B:{b.get('stato', '')}", d.get("confidenza", ""), b.get("giurisdizione", ""),
               b.get("provider_prodotto", ""), dett, p)
    if (p := ultimo("esiti/*/imbuto/licenze-cig.csv")):
        for r in csv.DictReader(open(p, encoding="utf-8")):
            es(r["cig"], "licenze", r["asse_a"], "regola", r["giurisdizione_prodotto"], r["provider"], f"via {r['via']}; euro netti {r['euro_netti']}", p)
    if (p := ultimo("esiti/*/imbuto/tetti-cig-v2.csv")):
        for r in csv.DictReader(open(p, encoding="utf-8")):
            es(r["cig"], "tetti", r["classe"], "regola", dett=f"via {r['via']}; euro netti {r['euro_netti']}; accordo quadro {r['cig_accordo_quadro']}", fonte=p)
    if (p := ultimo("esiti/*/imbuto/residuo-s6-per-66.csv")):
        for r in csv.DictReader(open(p, encoding="utf-8")):
            if r["materiale"] != "nulla":
                es(r["cig"], "atti-cercati", r["materiale"], r["livello"], dett=f"priorità {r['priorita']}; documenti che citano il CIG: {r['documenti_che_citano']}; atto registrato: {r['atto_registrato']}", fonte=p)
    # anche le motivazioni dei livelli possono citare l'aggiudicatario persona fisica
    E = [e[:6] + (oscura("", e[6], pf[e[0]])[1],) + e[7:] if e[0] in pf else e for e in E]
    c.executemany("INSERT INTO esiti VALUES (?,?,?,?,?,?,?,?)", [e for e in E if e[0] in cigs])
    fuori = sum(e[0] not in cigs for e in E)
    # 3. atti archiviati
    for p in sorted((R / "dati/atti").glob("*.jsonl")):
        usa(p)
        c.executemany("INSERT INTO atti VALUES (?,?,?,?,?,?,?)", [(d["cig"], d.get("url", ""), d.get("sha256", ""), d.get("tipo_atto", ""),
                      d.get("esito_recupero", ""), d.get("recuperato_il", ""), (d.get("trovato_con") or {}).get("metodo", ""))
                      for d in jl(p) if d.get("cig") in cigs])
    c.executescript("""
      CREATE INDEX esiti_cig ON esiti(cig); CREATE INDEX esiti_liv ON esiti(livello, esito); CREATE INDEX atti_cig ON atti(cig);
      UPDATE contratti SET livelli = coalesce((SELECT group_concat(livello, ',') FROM (SELECT DISTINCT livello FROM esiti e
             WHERE e.cig = contratti.cig ORDER BY livello)), '');
      UPDATE contratti SET n_atti = (SELECT count(*) FROM atti a WHERE a.cig = contratti.cig AND a.esito_recupero = 'ok');
      CREATE INDEX c_strato ON contratti(strato, anno); CREATE INDEX c_giur ON contratti(giurisdizione); CREATE INDEX c_gruppo ON contratti(gruppo);
      CREATE INDEX c_importo ON contratti(importo);
      CREATE VIRTUAL TABLE contratti_fts USING fts5(cig, testo, ente, aggiudicatari, cpv, content='contratti', content_rowid='rowid',
             tokenize="unicode61 remove_diacritics 2");
      INSERT INTO contratti_fts(rowid, cig, testo, ente, aggiudicatari, cpv) SELECT rowid, cig, testo, ente, aggiudicatari, cpv FROM contratti;
      INSERT INTO contratti_fts(contratti_fts) VALUES('optimize');
    """)
    versione = (R / "lavoro/imbuto/VERSIONE.txt").read_text(encoding="utf-8").split("=")[0].strip() if (R / "lavoro/imbuto/VERSIONE.txt").exists() else ""
    liv = dict(c.execute("SELECT livello, count(*) FROM esiti GROUP BY 1").fetchall())
    T = {"versione_indice": "cruscotto-indice 0.1", "data": OGGI, "imbuto": versione, "righe_ict_csv": n, "cig": n - doppi, "cig_doppi_ignorati": doppi,
         "cig_s3_s6_dal_2024": c.execute("SELECT count(*) FROM contratti WHERE anno >= 2024 AND substr(strato,1,2) IN ('S3','S4','S5','S6')").fetchone()[0],
         "per_strato": {s: {"cig": k, "euro": round(e or 0)} for s, k, e in c.execute("SELECT strato, count(*), sum(importo) FROM contratti GROUP BY 1")},
         "esiti_per_livello": liv, "esiti_fuori_imbuto_scartati": fuori,
         "atti": c.execute("SELECT count(*), count(DISTINCT cig) FROM atti").fetchone(),
         "cig_con_persona_fisica_oscurata": c.execute("SELECT count(*) FROM contratti WHERE persona_fisica = 1").fetchone()[0],
         "ingressi_sha256": ingressi}
    c.executemany("INSERT INTO meta VALUES (?,?)", [("riepilogo", json.dumps(T, ensure_ascii=False)), ("imbuto", versione), ("data", OGGI)])
    c.commit(); c.execute("PRAGMA journal_mode=DELETE"); c.close()
    os.replace(tmp, OUT)
    (ESITI / "indice.json").write_text(json.dumps(T, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in T.items() if k != "ingressi_sha256"}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
