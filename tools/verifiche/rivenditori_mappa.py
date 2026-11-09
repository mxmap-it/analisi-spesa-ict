"""#41 Mappa dei rivenditori dei prodotti cloud (v4, 9/11/2026): chi vende quale prodotto, a chi, con quale capogruppo.

Per ogni rivenditore (CF/P.IVA): capogruppo e sua giurisdizione, prodotti cloud venduti (marchio -> giurisdizione del
PRODOTTO, config/marchi_cloud.yaml), CIG, euro, enti. Quota della spesa in prodotti extra-UE che passa da rivenditori con
CF italiano (la lente fornitore la classificherebbe IT a torto). Precisione su campione con fonte primaria.

Ingressi (tutti nel clone o nell'archivio del server, sha256 nel manifest):
  - lavoro/attribuzione/[0-9]*.csv (regole v3, stessi filtri di tools/analisi/rivenditori.py e rivenditori_cf.py);
  - ANAC aggiudicatari (aggiudicatari_csv.zip del mirror): CF, ruolo (mandataria), denominazione;
  - fonti di seconda via per i CIG senza righe ANAC: vincitori TED (esiti/2026-11-06/imbuto/ted-vincitori.csv,
    esiti/2026-11-06/mirror/ted-esiti.csv), poi nome -> CF dal dataset aggiudicatari (solo se il nome normalizzato ha un
    CF unico o dominante >= 90 %);
  - GLEIF golden copy 6/11/2026 (LEI2 + RR del mirror): CF italiano -> LEI -> capogruppo ultimo (IS_ULTIMATELY_CONSOLIDATED_BY,
    in mancanza IS_DIRECTLY_CONSOLIDATED_BY); cache idempotente in lavoro/rivenditori/gleif-it.json;
  - config/rivenditori_capogruppo.yaml: righe curate (fonte per riga) che prevalgono su GLEIF;
  - fonte primaria per la precisione: atti archiviati (#57, dati/atti/atti-server.jsonl + dati/atti/testi/<sha256>.txt)
    e lotti Consip con aggiudicatario dichiarato (config/lotti_cloud.yaml).

Uso (server): nice .venv/bin/python tools/verifiche/rivenditori_mappa.py -> esiti/<oggi>/rivenditori/mappa-v4.{json,csv},
  campione-precisione.csv, cig-rivenditore.csv"""
import collections, csv, datetime, glob, io, json, os, random, re, sys, zipfile
from pathlib import Path
import yaml

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/analisi"))
from classifica import Classificatore  # noqa: E402
from rivenditori import normalizza  # noqa: E402

ZIP_AGG = R / "archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/aggiudicatari/filesystem/aggiudicatari_csv.zip"
GLEIF = R / "archivio/mirror/goldencopy.gleif.org/storage/golden-copy-files/2026/11/06"
CACHE = R / "lavoro/rivenditori/gleif-it.json"
UE27 = set("AT BE BG HR CY CZ DK EE FI FR DE GR IE IT LV LT LU MT NL PL PT RO SK SI ES SE HU".split())
NOME = {"AWS": "Amazon Web Services", "Google Cloud": "Google", "Microsoft Azure": "Microsoft", "Oracle Cloud": "Oracle", "IBM Cloud": "IBM"}
RX_IT = re.compile(r"^(\d{11}|[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z])$")
SEME = 20261109


def cf_norm(cf):
    cf = (cf or "").strip().upper().replace(" ", "")
    if cf.startswith("IT") and cf[2:].isdigit(): cf = cf[2:]
    if cf.isdigit() and 8 <= len(cf) < 11: cf = cf.zfill(11)  # zero iniziale perso (R56/v0.2)
    return cf


def bucket(paese):
    if not paese: return "?"
    if paese == "IT": return "IT"
    if paese in UE27: return "UE"
    if paese == "CH": return "CH"  # DECISIONI: Svizzera sovrana, si registra a parte
    return "EXTRA-UE"


def gleif_cache():
    """IT: RA entity ID (P.IVA/CF) -> LEI; LEI -> (nome, paese); LEI -> capogruppo. Idempotente."""
    if CACHE.exists(): return json.load(open(CACHE, encoding="utf-8"))
    rr_u, rr_d = {}, {}
    zrr = next(GLEIF.glob("*/*rr-golden-copy.csv.zip"))
    with zipfile.ZipFile(zrr) as z, z.open(z.namelist()[0]) as fb:
        for r in csv.DictReader(io.TextIOWrapper(fb, encoding="utf-8")):
            if r["Relationship.RelationshipStatus"] != "ACTIVE": continue
            t = r["Relationship.RelationshipType"]
            if t == "IS_ULTIMATELY_CONSOLIDATED_BY": rr_u[r["Relationship.StartNode.NodeID"]] = r["Relationship.EndNode.NodeID"]
            elif t == "IS_DIRECTLY_CONSOLIDATED_BY": rr_d[r["Relationship.StartNode.NodeID"]] = r["Relationship.EndNode.NodeID"]
    genitori = set(rr_u.values()) | set(rr_d.values())
    piva, ent = {}, {}
    zl = next(GLEIF.glob("*/*lei2-golden-copy.csv.zip"))
    csv.field_size_limit(10 ** 8)
    with zipfile.ZipFile(zl) as z, z.open(z.namelist()[0]) as fb:
        rd = csv.reader(io.TextIOWrapper(fb, encoding="utf-8"))
        h = next(rd); ix = {k: h.index(k) for k in ("LEI", "Entity.LegalName", "Entity.LegalAddress.Country",
                                                    "Entity.RegistrationAuthority.RegistrationAuthorityEntityID", "Entity.LegalJurisdiction", "Entity.EntityStatus")}
        for row in rd:
            lei = row[ix["LEI"]]; paese = row[ix["Entity.LegalAddress.Country"]]
            it = row[ix["Entity.LegalJurisdiction"]] == "IT" or paese == "IT"
            if it:
                ra = cf_norm(re.sub(r"\W", "", row[ix["Entity.RegistrationAuthority.RegistrationAuthorityEntityID"]]))
                if ra and (ra not in piva or row[ix["Entity.EntityStatus"]] == "ACTIVE"): piva[ra] = lei
            if it or lei in genitori:
                ent[lei] = [row[ix["Entity.LegalName"]], paese]
    out = {"fonte": [str(zrr.relative_to(R)), str(zl.relative_to(R))], "piva_lei": piva, "lei": ent,
           "ultimo": {k: v for k, v in rr_u.items() if k in ent}, "diretto": {k: v for k, v in rr_d.items() if k in ent}}
    os.makedirs(CACHE.parent, exist_ok=True)
    json.dump(out, open(CACHE, "w", encoding="utf-8"))
    return out


def main():
    csv.field_size_limit(10 ** 8)
    c = Classificatore()
    giur = dict(c.giur); giur.setdefault("VMware", "EXTRA-UE")
    for k, v in NOME.items(): giur.setdefault(v, giur.get(k, "?"))
    rx_marchi = collections.defaultdict(list)  # provider -> regex, per la verifica sugli atti
    for m in yaml.safe_load(open(R / "config/marchi_cloud.yaml", encoding="utf-8")):
        rx_marchi[NOME.get(m["provider"], m["provider"])] += [re.compile(x, re.I) for x in m.get("regex", [])]
    rx_marchi["VMware"].append(re.compile(r"vmware", re.I))
    # 1. CIG attuativi con provider (ultima versione per CIG)
    cig = {}
    for f in sorted(glob.glob(str(R / "lavoro/attribuzione/[0-9]*.csv"))):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            if r["e_padre"] == "1" or not r["provider"] or r["servizio"] in ("servizi-professionali", "in-house", "software-infrastruttura"): continue
            if r.get("importo_da_verificare"): continue
            ag = [a.strip() for a in r["aggiudicatari"].split(";") if a.strip()]
            cig[r["cig"]] = {"provider": r["provider"], "g": giur.get(r["provider"], "?"), "canale": c.canale(r["provider"], ag),
                             "imp": float(r["importo_lotto"] or 0), "ag": ag, "ente": r["stazione_appaltante"].strip(),
                             "aq": r["cig_accordo_quadro"], "testo": r["testo"]}
    riv = {k for k, v in cig.items() if v["canale"] == "rivenditore"}
    # 2. aggiudicatari ANAC + dizionario nome -> CF
    anac = collections.defaultdict(dict); nomi = collections.defaultdict(collections.Counter)
    with zipfile.ZipFile(ZIP_AGG) as z, z.open("aggiudicatari_csv.csv") as fb:
        for r in csv.DictReader(io.TextIOWrapper(fb, encoding="utf-8", errors="replace"), delimiter=";"):
            cf = cf_norm(r["codice_fiscale"]); den = r["denominazione"].strip()
            if RX_IT.match(cf) or re.match(r"^[A-Z]{2}\w{6,}$", cf): nomi[normalizza(den)][cf] += 1
            if r["cig"] in riv:
                anac[r["cig"]][cf or den] = (cf, den, (r["ruolo"] or "").upper())

    def nome_cf(n):
        cc = nomi.get(normalizza(n))
        if not cc: return ""
        cf, k = cc.most_common(1)[0]
        return cf if k / sum(cc.values()) >= 0.9 else ""
    ted = {}
    for f in ("esiti/2026-11-06/imbuto/ted-vincitori.csv", "esiti/2026-11-06/mirror/ted-esiti.csv"):
        for r in csv.DictReader(open(R / f, encoding="utf-8")):
            ps = [cf_norm(p) for p in r["piva_ted"].split(";") if p.strip()]
            vs = [v.strip() for v in r["vincitore_ted"].split(";") if v.strip()]
            if ps: ted.setdefault(r["cig"], list(dict.fromkeys(zip(ps, vs + [""] * len(ps)))))
    # 3. ripartizione per CIG -> (cf, nome, quota, fonte)
    fonte_cnt = collections.Counter(); fonte_eur = collections.Counter(); quote = {}
    for k in riv:
        v = cig[k]; rows = list(anac.get(k, {}).values()); src = "anac-aggiudicatari"
        if not rows and k in ted:
            rows = [(p, n, "") for p, n in ted[k]]; src = "ted-vincitori"
        if not rows:
            rows = [(nome_cf(n), n, "") for n in v["ag"]]; src = "nome->cf-anac" if any(r[0] for r in rows) else "solo-nome"
        mand = [x for x in rows if "MANDATARI" in x[2]]
        q = [(x, v["imp"]) for x in mand[:1]] if mand else [(x, v["imp"] / len(rows)) for x in rows]
        quote[k] = [(cf, den, imp, src) for (cf, den, _), imp in q]
        fonte_cnt[src] += 1; fonte_eur[(v["g"], src)] += v["imp"]
    # 4. capogruppo: curato > GLEIF
    gl = gleif_cache()
    cur = {cf_norm(str(x["cf"])): x for x in (yaml.safe_load(open(R / "config/rivenditori_capogruppo.yaml", encoding="utf-8")) or [])}

    def capogruppo(cf):
        if cf in cur:
            x = cur[cf]; return x["capogruppo"], x["paese_capogruppo"], "curato: " + x["fonte"]
        lei = gl["piva_lei"].get(cf)
        if not lei: return "", "", "nessun LEI" if RX_IT.match(cf or "") else "cf non italiano/assente"
        p = gl["ultimo"].get(lei) or gl["diretto"].get(lei)
        if p and p in gl["lei"]:
            return gl["lei"][p][0], gl["lei"][p][1], f"GLEIF RR {lei}->{p}"
        return gl["lei"][lei][0] + " (nessun capogruppo dichiarato)", gl["lei"][lei][1], f"GLEIF LEI {lei} senza RR"
    # 5. aggregazione per rivenditore
    per = {}
    for k, qs in quote.items():
        v = cig[k]
        for cf, den, imp, src in qs:
            key = cf or "NOME:" + normalizza(den)
            p = per.setdefault(key, {"cf": cf, "denominazione": den, "cig": set(), "eur": 0.0, "eur_extra_ue": 0.0,
                                     "prodotti": collections.Counter(), "enti": collections.Counter(), "fonti": collections.Counter()})
            p["cig"].add(k); p["eur"] += imp; p["prodotti"][v["provider"]] += imp; p["enti"][v["ente"]] += imp; p["fonti"][src] += 1
            if v["g"] == "EXTRA-UE": p["eur_extra_ue"] += imp
    for p in per.values():
        p["naz_cf"] = "IT" if RX_IT.match(p["cf"] or "") else ("estero" if p["cf"] else "ignota")
        p["capogruppo"], p["paese_capogruppo"], p["fonte_capogruppo"] = capogruppo(p["cf"])
        p["bucket_capogruppo"] = bucket(p["paese_capogruppo"]) if p["paese_capogruppo"] else ("IT?" if p["naz_cf"] == "IT" else "?")
    # 6. quote extra-UE
    tot = collections.Counter();
    for v in cig.values(): tot[(v["g"], v["canale"])] += v["imp"]
    ext_tot = sum(x for (g, _), x in tot.items() if g == "EXTRA-UE")
    ext_noto = tot[("EXTRA-UE", "diretto")] + tot[("EXTRA-UE", "rivenditore")]
    lente = collections.Counter()  # extra-UE via rivenditore per (naz CF, bucket capogruppo)
    for p in per.values():
        lente[(p["naz_cf"], p["bucket_capogruppo"])] += p["eur_extra_ue"]
    via_riv = sum(lente.values()); cf_it = sum(x for (n, _), x in lente.items() if n == "IT")
    cf_it_cap_it = sum(x for (n, b), x in lente.items() if n == "IT" and b in ("IT", "IT?"))
    # 7. precisione su fonte primaria
    atti = collections.defaultdict(list)
    for l in open(R / "dati/atti/atti-server.jsonl", encoding="utf-8"):
        d = json.loads(l)
        if d.get("sha256") and d.get("esito_recupero") == "ok" and d["cig"] in riv and (R / f"dati/atti/testi/{d['sha256']}.txt").exists():
            atti[d["cig"]].append(d["sha256"])
    cand = sorted(atti); random.Random(SEME).shuffle(cand); camp = cand[:80]
    righe_c = []; ok = collections.Counter()
    for k in camp:
        v = cig[k]; testo = " ".join(open(R / f"dati/atti/testi/{s}.txt", encoding="utf-8", errors="replace").read() for s in atti[k])
        tn = set(normalizza(testo).split())
        prod = any(x.search(testo) for x in rx_marchi.get(v["provider"], [])) or v["provider"].lower() in testo.lower()
        tok = lambda d: [t for t in normalizza(d).split() if len(t) >= 3][:1]
        pert = k in testo  # atto pertinente: cita il CIG
        vend = any((cf.isdigit() and cf in testo) or (den and tok(den) and tok(den)[0] in tn) for cf, den, _, _ in quote[k])
        ok["campione"] += 1; ok["atto_pertinente"] += pert
        if pert: ok["pertinente_prodotto_nell_atto"] += prod; ok["pertinente_rivenditore_nell_atto"] += vend
        righe_c.append([k, v["provider"], v["g"], " | ".join(f"{cf} {den}" for cf, den, _, _ in quote[k]), round(v["imp"]), int(pert), int(prod), int(vend), " ".join(atti[k])])
    # etichette manuali del campione (oggetto ANAC + atto quando pertinente): precisione della lente prodotto nel canale rivenditore
    et = {}
    fe = R / "report/metodo/rivenditori-v4/etichette-campione.csv"
    if fe.exists():
        for r in csv.DictReader(open(fe, encoding="utf-8")): et[r["cig"]] = r
    prec = collections.Counter()
    for k in camp:
        if k not in et: continue
        e = et[k]["prodotto_corretto"]; prec[e] += 1; prec["eur_" + e] += cig[k]["imp"]
        if et[k]["fonte"] == "atto": prec["fonte_atto"] += 1
    dec = prec["si"] + prec["no"]
    prec_out = {k: (round(v) if k.startswith("eur") else v) for k, v in prec.items()}
    if dec: prec_out |= {"precisione_decisi": round(prec["si"] / dec, 3), "precisione_minima_incerti_errati": round(prec["si"] / (dec + prec["incerto"]), 3),
                         "precisione_eur_decisi": round(prec["eur_si"] / (prec["eur_si"] + prec["eur_no"]), 3)}
    # seconda fonte primaria: lotti Consip con aggiudicatario dichiarato
    lotti = {}
    for it in yaml.safe_load(open(R / "config/lotti_cloud.yaml", encoding="utf-8")):
        for l in it.get("lotti", []):
            if l.get("aggiudicatario"): lotti[l["cig"]] = (l["aggiudicatario"], it["iniziativa"])
    lotti_chk = collections.Counter()
    for k, v in cig.items():
        if v["aq"] in lotti:
            att = normalizza(lotti[v["aq"]][0]).split()[0]
            nomi_k = [normalizza(d) for _, d, _, _ in quote.get(k, [])] or [normalizza(a) for a in v["ag"]]
            lotti_chk["cig"] += 1; lotti_chk["coincide"] += any(att in n.split() for n in nomi_k)
    # 8. uscite
    oggi = datetime.date.today().isoformat(); o = R / f"esiti/{oggi}/rivenditori"; os.makedirs(o, exist_ok=True)
    top = sorted(per.values(), key=lambda p: -p["eur"])
    with open(o / "mappa-v4.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["cf", "denominazione", "naz_cf", "capogruppo", "paese_capogruppo", "bucket_capogruppo", "fonte_capogruppo",
                    "cig", "eur", "eur_prodotti_extra_ue", "enti", "prodotti (marchio:giurisdizione=eur)", "primi_enti", "fonte_cf"])
        for p in top:
            w.writerow([p["cf"], p["denominazione"], p["naz_cf"], p["capogruppo"], p["paese_capogruppo"], p["bucket_capogruppo"], p["fonte_capogruppo"],
                        len(p["cig"]), round(p["eur"]), round(p["eur_extra_ue"]), len(p["enti"]),
                        " ; ".join(f"{m}:{giur.get(m, '?')}={round(x)}" for m, x in p["prodotti"].most_common()),
                        " ; ".join(f"{e}={round(x)}" for e, x in p["enti"].most_common(5)), " ; ".join(f"{a}={b}" for a, b in p["fonti"].items())])
    with open(o / "cig-rivenditore.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["cig", "provider", "giurisdizione_prodotto", "ente", "cf", "denominazione", "quota_eur", "fonte_cf"])
        for k in sorted(quote):
            for cf, den, imp, src in quote[k]: w.writerow([k, cig[k]["provider"], cig[k]["g"], cig[k]["ente"], cf, den, round(imp), src])
    with open(o / "campione-precisione.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["cig", "provider", "giurisdizione_prodotto", "rivenditori", "eur", "atto_pertinente", "prodotto_nell_atto", "rivenditore_nell_atto", "sha256_atti"])
        w.writerows(righe_c)
    rr = lambda x: round(x)
    out = {"versione": "v4", "generato": oggi, "seme_campione": SEME,
           "cig_attribuiti": len(cig), "cig_rivenditore": len(riv),
           "per_giurisdizione_e_canale": {f"{g}|{ch}": rr(x) for (g, ch), x in sorted(tot.items())},
           "fonte_cf_cig": dict(fonte_cnt), "fonte_cf_eur": {f"{g}|{s}": rr(x) for (g, s), x in sorted(fonte_eur.items())},
           "rivenditori": len(per), "rivenditori_con_prodotti_extra_ue": sum(1 for p in per.values() if p["eur_extra_ue"]),
           "extra_ue": {"totale": rr(ext_tot), "noto": rr(ext_noto), "via_rivenditore": rr(via_riv),
                        "via_rivenditore_cf_it": rr(cf_it), "via_rivenditore_cf_it_capogruppo_it": rr(cf_it_cap_it),
                        "quota_cf_it_sul_totale": round(cf_it / ext_tot, 3), "quota_cf_it_sul_noto": round(cf_it / ext_noto, 3),
                        "quota_cf_it_capogruppo_it_sul_totale": round(cf_it_cap_it / ext_tot, 3),
                        "per_naz_cf_e_capogruppo": {f"{n}|{b}": rr(x) for (n, b), x in lente.most_common()}},
           "capogruppo_copertura_eur_extra_ue": {s: rr(sum(p["eur_extra_ue"] for p in per.values() if p["fonte_capogruppo"].split(" ")[0].rstrip(":") == s))
                                                  for s in ("curato", "GLEIF", "nessun", "cf")},
           "gleif": {"piva_it_con_lei": len(gl["piva_lei"]), "fonte": gl["fonte"]},
           "precisione_atti_automatica": dict(ok), "precisione_etichette": prec_out, "cig_rivenditore_con_atti": len(cand),
           "precisione_lotti_consip": dict(lotti_chk),
           "primi_25": [{"cf": p["cf"], "denominazione": p["denominazione"], "capogruppo": p["capogruppo"], "paese": p["paese_capogruppo"],
                         "fonte_capogruppo": p["fonte_capogruppo"], "cig": len(p["cig"]), "eur": rr(p["eur"]), "eur_extra_ue": rr(p["eur_extra_ue"]),
                         "enti": len(p["enti"]), "prodotti": {m: rr(x) for m, x in p["prodotti"].most_common(6)}} for p in top[:25]]}
    json.dump(out, open(o / "mappa-v4.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in out.items() if k != "primi_25"}, indent=1, ensure_ascii=False))
    for p in out["primi_25"]: print(p["cf"], p["denominazione"][:30], "|", p["capogruppo"][:40], p["paese"], p["eur_extra_ue"], p["fonte_capogruppo"][:40])


if __name__ == "__main__":
    main()
