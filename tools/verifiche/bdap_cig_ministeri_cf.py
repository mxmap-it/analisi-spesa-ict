"""#67 BDAP nell'imbuto, giro 0.2: CIG ICT dei ministeri abbinati per CODICE FISCALE, quota annua dei contratti, Sogei.

 1. Stazione appaltante -> ministero per codice fiscale: il CF della SA (e, se c'è, il CF della SA delegante) dei CIG ANAC
    si cerca in IndicePA (amministrazioni.txt, campo cf, e servizi-fatturazione-elettronica.txt, CF degli uffici di
    fatturazione, che dà il CF di prefetture, tribunali, comandi... con il cod_amm del ministero). cod_amm -> ministero BDAP
    con la tabella COD_AMM sotto. Si confronta con l'abbinamento per nome del giro 0.1 (bdap_ict_stato.ministero).
 2. Per ogni CIG ICT (lavoro/imbuto/ict.csv, strati S3-S6, senza S0/S2 né importi da verificare): importo, data di
    pubblicazione e DURATA_PREVISTA (giorni) dal CIG ANAC (ultima versione: file annuali, poi delta mensili).
    Quota annua = importo distribuito uniformemente da data_pubblicazione per la durata; CIG senza durata o con durata <= 0
    tutto nell'anno di pubblicazione; durate oltre 10 anni troncate a 10. Pluriennale = durata > 365 giorni.
 3. Confronto per ministero e anno (2022-2025) con il pagato ICT per gestionale (BDAP, stessa via del giro 0.1):
    (a) importo dei CIG pubblicati nell'anno, (b) quota dell'anno dei CIG attivi (pubblicati dal 2020 in poi).
 4. Sogei (CF 02327910580): CIG con Sogei aggiudicataria (aggiudicatari ANAC) e CIG con Sogei stazione appaltante.

Uso (server): nice .venv/bin/python tools/verifiche/bdap_cig_ministeri_cf.py -> esiti/<oggi>/bdap/cig-ministeri-cf.json
Lettura in streaming (niente caricamento di tutti i CIG in memoria): si tengono solo i CIG di ict.csv e quelli di Sogei."""
import collections, csv, datetime, glob, hashlib, io, json, os, sys, zipfile
from pathlib import Path

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/verifiche")); sys.path.insert(0, str(R / "tools/analisi"))
import bdap_ict_stato as B  # noqa: E402

ARC = B.ARC
D = ARC / "mirror/dati.anticorruzione.it/opendata/download/dataset"
IPA = ARC / "mirror/indicepa.gov.it/ipa-dati/dataset"
SOGEI = "02327910580"
COD_AMM = {"m_ae": "ESTERI", "m_amte": "AMBIENTE", "m_bac": "CULTURA", "m_d": "DIFESA", "cc": "DIFESA", "m_dg": "GIUSTIZIA",
           "m_ef": "ECONOMIA E FINANZE", "gdf": "ECONOMIA E FINANZE", "m_inf": "INFRASTRUTTURE", "m_it": "INTERNO",
           "XZR4RNHR": "INTERNO", "m_lps": "LAVORO", "m_paf": "AGRICOLTURA", "m_pi": "ISTRUZIONE", "m_sa": "SALUTE",
           "m_svec": "IMPRESE", "WQF3ZW8F": "TURISMO", "m_ur": "UNIVERSITA"}
ANNI = range(2022, 2026)


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


def ipa():
    ingressi = {}; cf2amm = {}
    for nome, ccf, camm in (("amministrazioni.txt", "cf", "cod_amm"), ("servizi-fatturazione-elettronica.txt", "cf", "cod_amm")):
        p = sorted(IPA.glob(f"*/resource/*/download/{nome}"))[0]; ingressi[nome] = {"file": str(p.relative_to(ARC)), "sha256": sha(p)}
        for r in csv.DictReader(open(p, encoding="utf-8-sig", newline=""), delimiter="\t"):
            if r[camm] in COD_AMM and (r.get(ccf) or "").strip():
                cf2amm.setdefault(r[ccf].strip(), r[camm])
    return cf2amm, ingressi


def cig_anac(voluti):
    """ultima versione di ogni CIG voluto: file annuali 2020-2025, poi delta (che vincono)."""
    out = {}; files = []
    zz = [z for a in range(2020, 2026) for z in sorted(glob.glob(str(D / f"cig-{a}/filesystem/cig_csv_*.zip")))]
    zz += sorted(glob.glob(str(D / "cig/filesystem/*-cig_csv.zip")))
    for z in zz:
        files.append(os.path.relpath(z, ARC)); zf = zipfile.ZipFile(z)
        m = next(i for i in zf.namelist() if i.endswith(".csv"))
        for r in csv.DictReader(io.TextIOWrapper(zf.open(m), encoding="utf-8-sig", errors="replace"), delimiter=";"):
            if r["cig"] in voluti:
                out[r["cig"]] = {"cf": (r["cf_amministrazione_appaltante"] or "").strip(), "sa": r["denominazione_amministrazione_appaltante"],
                                 "cf_del": (r.get("CF_SA_DELEGANTE") or "").strip(), "data": r["data_pubblicazione"][:10],
                                 "durata": B.num(r.get("DURATA_PREVISTA")), "importo": B.num(r["importo_lotto"]),
                                 "oggetto": r["oggetto_lotto"][:200], "cpv": r["cod_cpv"], "scelta": r["tipo_scelta_contraente"]}
    return out, files


def quote(importo, data, durata):
    """quota per anno solare dell'importo distribuito da data per durata giorni."""
    try: d0 = datetime.date.fromisoformat(data)
    except ValueError: return {}
    if durata <= 0: return {d0.year: importo}
    durata = min(durata, 3650)  # durate oltre 10 anni (errori di compilazione, es. 99999) si troncano a 10 anni
    d1 = d0 + datetime.timedelta(days=durata); q = {}
    for y in range(d0.year, d1.year + 1):
        a = max(d0, datetime.date(y, 1, 1)); b = min(d1, datetime.date(y + 1, 1, 1))
        if b > a: q[y] = importo * (b - a).days / durata
    return q


def main():
    csv.field_size_limit(10 ** 8)
    cf2amm, ingressi = ipa()
    ict = {}
    for r in csv.DictReader(open(R / "lavoro/imbuto/ict.csv", encoding="utf-8")):
        if r["strato"][:2] in ("S0", "S2") or r["importo_da_verificare"] == "1": continue
        ict[r["cig"]] = (int(r["anno"]), B.num(r["importo"]), r["strato"])
    ingressi["ict.csv"] = {"file": "lavoro/imbuto/ict.csv", "sha256": sha(R / "lavoro/imbuto/ict.csv"), "cig_s3_s6": len(ict)}
    # Sogei aggiudicataria
    sog = {}
    for z in sorted(glob.glob(str(D / "aggiudicatari/filesystem/*_csv.zip"))):
        ingressi["aggiudicatari"] = {"file": os.path.relpath(z, ARC), "sha256": sha(z)}
        zf = zipfile.ZipFile(z); m = next(i for i in zf.namelist() if i.endswith(".csv"))
        for r in csv.DictReader(io.TextIOWrapper(zf.open(m), encoding="utf-8-sig", errors="replace"), delimiter=";"):
            if (r["codice_fiscale"] or "").strip().lstrip("IT") == SOGEI: sog[r["cig"]] = r["ruolo"]
    anac, files = cig_anac(set(ict) | set(sog))
    ingressi["cig_anac"] = {"file": files, "nota": "sha256 nel manifest dell'archivio"}
    # 1. abbinamento per CF, confronto con il nome
    per = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))  # anno -> ministero -> misure
    conf = collections.Counter(); confe = collections.Counter(); esempi = collections.defaultdict(list)
    quota = collections.defaultdict(collections.Counter); quota_n = collections.defaultdict(collections.Counter)
    for c, (anno, imp, strato) in ict.items():
        a = anac.get(c)
        if not a: conf["senza-cig-anac"] += 1; continue
        amm = cf2amm.get(a["cf"]); via = "cf-sa"
        if not amm and a["cf_del"] in cf2amm: amm = cf2amm[a["cf_del"]]; via = "cf-delegante"
        m_cf = COD_AMM.get(amm) if amm else None
        m_nome = B.ministero(a["sa"]) if B.RX_SA_STATO.search(a["sa"]) else None
        if m_nome == "ALTRO": m_nome = None
        k = ("uguale" if m_cf == m_nome else "solo-cf" if m_cf and not m_nome else "solo-nome" if m_nome and not m_cf
             else "diverso") if (m_cf or m_nome) else None
        if not k: continue
        conf[k] += 1; confe[k] += imp
        if k != "uguale" and len(esempi[k]) < 15: esempi[k].append({"cig": c, "sa": a["sa"], "cf": a["cf"], "cf_del": a["cf_del"], "min_cf": m_cf, "min_nome": m_nome, "importo": round(imp)})
        if not m_cf: continue
        pl = a["durata"] > 365
        per[anno][m_cf]["n"] += 1; per[anno][m_cf]["importo"] += imp
        per[anno][m_cf]["n_plur" if pl else "n_ann"] += 1; per[anno][m_cf]["imp_plur" if pl else "imp_ann"] += imp
        if via == "cf-delegante": per[anno][m_cf]["n_delega"] += 1; per[anno][m_cf]["imp_delega"] += imp
        for y, v in quote(imp, a["data"], a["durata"]).items():
            quota[y][m_cf] += v; quota_n[y][m_cf] += 1
    # 3. pagato BDAP per gestionale (stessa via del giro 0.1)
    pag = {}
    for y in ANNI:
        righe, meta = B.leggi(B.MICGS[y]); ingressi[f"micgs-{y}"] = meta; c = collections.Counter()
        for x in righe:
            if x["Codice Gestionale"][:3] in B.GEST_ICT: c[B.ministero(x["Amministrazione"])] += B.num(x["OP"])
        pag[y] = c
    tab = {}
    for y in ANNI:
        tab[y] = {}
        for m in sorted(set(per[y]) | set(pag[y]) - {"ALTRO"}):
            p = per[y][m]; b = pag[y].get(m, 0)
            tab[y][m] = {"cig_n": p["n"], "cig_importo": round(p["importo"]), "cig_plur_n": p["n_plur"], "cig_plur_importo": round(p["imp_plur"]),
                         "cig_delega_n": p["n_delega"], "cig_delega_importo": round(p["imp_delega"]),
                         "quota_anno_cig_attivi": round(quota[y][m]), "cig_attivi_n": quota_n[y][m], "bdap_pagato_ict": round(b),
                         "rapporto_importo": round(p["importo"] / b, 2) if b else None, "rapporto_quota": round(quota[y][m] / b, 2) if b else None}
    # 4. Sogei
    s = {"aggiudicataria": collections.defaultdict(collections.Counter), "sa": collections.defaultdict(collections.Counter), "elenco_aggiudicataria": []}
    for c, ruolo in sog.items():
        a = anac.get(c)
        if not a: s["aggiudicataria"]["senza-cig-anac"]["n"] += 1; continue
        m = COD_AMM.get(cf2amm.get(a["cf"]) or cf2amm.get(a["cf_del"]), "ALTRO" if a["cf"] != SOGEI else "SOGEI")
        y = a["data"][:4]; s["aggiudicataria"][f"{y}|{m}"]["n"] += 1; s["aggiudicataria"][f"{y}|{m}"]["importo"] += round(a["importo"])
        s["elenco_aggiudicataria"].append({"cig": c, "anno": y, "sa": a["sa"], "ministero": m, "importo": round(a["importo"]), "durata": a["durata"],
                                           "scelta": a["scelta"], "oggetto": a["oggetto"], "in_ict_csv": c in ict})
    for c, (anno, imp, strato) in ict.items():
        a = anac.get(c)
        if a and a["cf"] == SOGEI:
            s["sa"][anno]["n"] += 1; s["sa"][anno]["importo"] += round(imp)
            if a["durata"] > 365: s["sa"][anno]["n_plur"] += 1; s["sa"][anno]["imp_plur"] += round(imp)
            for yy, v in quote(imp, a["data"], a["durata"]).items(): s["sa"][anno][f"quota_{yy}"] += round(v)
    s["elenco_aggiudicataria"].sort(key=lambda r: -r["importo"])
    out = {"versione": "bdap-cig-ministeri-cf 0.2 (2026-11-09)", "ingressi": ingressi, "cf_ministeriali_ipa": len(cf2amm),
           "abbinamento_cf_vs_nome": {"cig": dict(conf), "importo": {k: round(v) for k, v in confe.items()}, "esempi": esempi},
           "per_ministero_anno": tab, "sogei": {k: ({kk: dict(vv) for kk, vv in v.items()} if isinstance(v, dict) else v) for k, v in s.items()}}
    o = R / f"esiti/{datetime.date.today().isoformat()}/bdap"; os.makedirs(o, exist_ok=True)
    json.dump(out, open(o / "cig-ministeri-cf.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=str)
    print(json.dumps({k: out[k] for k in ("cf_ministeriali_ipa", "abbinamento_cf_vs_nome")}, indent=1, ensure_ascii=False, default=str)[:4000])
    for y in ANNI:
        print(y); [print(" ", m, v) for m, v in tab[y].items()]
    print(json.dumps({k: out["sogei"][k] for k in ("aggiudicataria", "sa")}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
