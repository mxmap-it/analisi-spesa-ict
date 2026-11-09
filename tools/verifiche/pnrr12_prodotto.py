"""#43 Misura 1.2 (Abilitazione e facilitazione migrazione al cloud): universo CUP/CIG, prodotto cloud, quota per giurisdizione.

Ingressi (tutti nell'archivio o già prodotti, nessuna rete, nessun LLM):
- PA Digitale 2026 `candidature_finanziate_12.csv` (CUP, ente, tipologia, importo finanziato) e `avvisi.csv`;
- dataset ANAC `cup` (CIG ↔ CUP), stesso file di tools/analisi/pnrr_cloud.py;
- attribuzione v3 per prodotto dei CIG collegati: report/metodo/pnrr-contratti-v3.csv;
- elenco ACN dei servizi cloud qualificati (schede_qualificate_tipo_servizi_cloud_csv, archiviato il 6/11/2026);
- testi degli atti già archiviati: dati/atti/atti.jsonl + dati/atti/testi/.

Strati di attribuzione del PRODOTTO, in ordine (vince il primo):
 S1 marchio v3 (config/marchi_cloud.yaml, lotti, convenzioni): provider e giurisdizione del prodotto;
 S2 aggiudicatario con servizio SaaS/PaaS/IaaS qualificato ACN: il prodotto è il servizio qualificato del fornitore
    (giurisdizione del fornitore: sede IT dal nome e forma giuridica italiana); l'infrastruttura sotto il SaaS NON è
    nell'elenco ACN (manca la colonna) e resta ignota;
 S3 aggiudicatario software house italiana non trovata nell'elenco ACN (forma giuridica italiana, non in GRUPPI_ESTERI);
 S4 aggiudicatario vuoto, fornitore riconosciuto nel testo (token distintivo dei fornitori S2/S3 con >= 5 CIG);
 S5 aggiudicatario a controllo extra-UE senza marchio (lente fornitore, NON prodotto: contato a parte);
 S6 residuo senza prodotto né fornitore.
Precisione di S4 misurata sulla metà prova dei CIG con aggiudicatario (token scelti sulla metà sviluppo).
Campione per S2 (abbinamento nome ACN ↔ aggiudicatario): 60 righe estratte con seme fisso in esiti/<data>/pnrr12/.

Uso: python tools/verifiche/pnrr12_prodotto.py [--data AAAA-MM-GG] -> esiti/<data>/pnrr12/"""
import collections, csv, hashlib, io, json, os, random, re, sys, zipfile, datetime
from pathlib import Path

R = Path(__file__).resolve().parents[2]
PAD = R / "archivio/mirror/raw.githubusercontent.com/teamdigitale/padigitale2026-opendata/main/data"
CUP = R / "archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/cup/filesystem/cup_csv.zip"
ACN = R / "archivio/mirror/www.acn.gov.it/portale/documents/d/guest/schede_qualificate_tipo_servizi_cloud_csv"
V3 = R / "report/metodo/pnrr-contratti-v3.csv"
OCDS = R / "lavoro/pnrr12/ocds-1.2.jsonl"
BIGTECH = {"Microsoft", "Amazon Web Services", "Google", "Oracle", "IBM", "Salesforce", "ServiceNow", "Adobe", "Zoom",
           "Cisco Webex", "Cloudera", "VMware"}
# controllo extra-UE noto (lente fornitore, secondaria): gruppo USA/UK/CH
GRUPPI_ESTERI = [r"\bibm\b", r"enterprise services italia", r"\biqvia\b", r"\bdxc\b", r"kyndryl", r"\bey advisory\b",
                 r"ernst", r"claranet", r"\bdeloitte\b", r"\bpwc\b|pricewaterhouse", r"\bkpmg\b"]
FORME = r"\b(s\s*r\s*l\s*s?|s\s*p\s*a|s\s*a\s*s|s\s*n\s*c|s\s*c\s*a\s*r\s*l|soc(ieta)?\s+coop\w*|a\s+socio\s+unico|socio\s+unico|" \
        r"societa\s+benefit|s\s*b|unipersonale|in\s+breve.*|ovvero.*|s\s*a|srl|spa|sa|gmbh|ltd|inc)\b"
GENERICI = {"ITALIA", "SISTEMI", "SERVIZI", "DIGITALE", "SOLUZIONI", "INFORMATICA", "SOFTWARE", "GROUP", "GRUPPO", "CONSULTING",
            "TECHNOLOGY", "TECHNOLOGIES", "SOCIETA", "SYSTEM", "SYSTEMS", "SERVICE", "SERVICES", "CONSORZIO", "STUDIO",
            "INFORMATICI", "DATA", "CLOUD", "COMPUTER", "NETWORK", "SOLUTIONS", "OFFICE", "TECHNICAL", "ENGINEERING", "COMUNE",
            "PUBBLICA", "AMMINISTRAZIONE", "DIGITAL", "PARTNER", "PROGETTI", "SVILUPPO", "INNOVAZIONE", "MEDIA", "TECH"}


def norm(s):
    s = re.sub(r"[^a-z0-9 ]", " ", (s or "").lower().replace("'", " ").replace("&", " "))
    s = re.sub(FORME, " ", s)
    return re.sub(r"\s+", " ", s).strip()


def pct(a, b): return round(100 * a / b, 1) if b else None


def main():
    data = sys.argv[sys.argv.index("--data") + 1] if "--data" in sys.argv else datetime.date.today().isoformat()
    out_dir = R / f"esiti/{data}/pnrr12"; os.makedirs(out_dir, exist_ok=True)
    csv.field_size_limit(10 ** 8)
    # --- universo dei finanziamenti
    cand = {}
    for r in csv.DictReader(open(PAD / "candidature_finanziate_12.csv", encoding="utf-8")):
        c = (r["codice_cup"] or "").strip().upper()
        if c: cand[c] = {"tip": r["tipologia_ente"], "imp": float(r["importo_finanziamento"] or 0), "ente": r["ente"]}
    avvisi = [r for r in csv.DictReader(open(PAD / "avvisi.csv", encoding="utf-8")) if r["misura"].startswith("1.2")]
    cig_cup = collections.defaultdict(set)
    z = zipfile.ZipFile(CUP)
    for r in csv.DictReader(io.TextIOWrapper(z.open(z.namelist()[0]), encoding="utf-8-sig", errors="replace"), delimiter=";"):
        c = (r["CUP"] or "").strip().upper()
        if c in cand: cig_cup[r["CIG"].strip()].add(c)
    cup_con_cig = {c for cs in cig_cup.values() for c in cs}
    # --- elenco ACN
    acn = collections.defaultdict(lambda: collections.Counter())
    acn_nomi = {}
    acn_schede = collections.defaultdict(list)
    for r in csv.DictReader(open(ACN, encoding="utf-8-sig"), delimiter=";"):
        k = norm(r["Nome Fornitore"]); acn[k][r["Tipologia"]] += 1; acn_nomi[k] = r["Nome Fornitore"]
        acn_schede[k].append((r["Id Scheda"], r["Nome"], r["Tipologia"]))
    acn_keys = [k for k in acn if len(k) >= 4]

    def in_acn(den):
        k = norm(den)
        if not k: return None
        if k in acn: return k
        for a in acn_keys:  # prefisso lungo almeno 8 caratteri, una sola corrispondenza
            if len(min(a, k, key=len)) >= 8 and (a.startswith(k + " ") or k.startswith(a + " ")): return a
        return None

    # --- aggiudicatari dall'OCDS bulk ANAC (tools/verifiche/pnrr12_ocds.py), dove il dataset aggiudicatari manca
    ocds_sup, ocds_lot = {}, {}
    if OCDS.exists():
        for l in open(OCDS, encoding="utf-8"):
            d = json.loads(l)
            nomi = [x["name"] for x in d["suppliers"] if x.get("name")]
            if nomi: ocds_sup[d["cig"]] = nomi
            t = d.get("tender") or {}
            ocds_lot[d["cig"]] = " ".join(filter(None, (t.get("title"), t.get("lot"), t.get("description"))))
    # --- contratti v3
    rows = [r for r in csv.DictReader(open(V3, encoding="utf-8")) if r["misura"] == "1.2"]
    # token distintivi dei fornitori (per S4)
    n_forn = collections.Counter()
    for r in rows:
        for a in filter(None, (x.strip() for x in r["aggiudicatari"].split(";"))): n_forn[norm(a)] += 1
    tok = {}
    for f, n in n_forn.items():
        if n < 5: continue
        t = next((w for w in f.upper().split() if len(w) >= 5 and w not in GENERICI and not w.isdigit()), None)
        if t: tok.setdefault(t, set()).add(f)
    tok_re = {t: re.compile(r"\b" + re.escape(t) + r"\b", re.I) for t in tok}
    # selezione dei token su metà sviluppo (CIG con hash pari), misura sulla metà prova (dispari): niente overfit
    con_agg = [r for r in rows if r["aggiudicatari"].strip()]
    svil = [r for r in con_agg if int(hashlib.sha256(r["cig"].encode()).hexdigest(), 16) % 2 == 0]
    prova = [r for r in con_agg if int(hashlib.sha256(r["cig"].encode()).hexdigest(), 16) % 2 == 1]

    def giusto(r, t): return any(t in norm(a).upper().split() for a in r["aggiudicatari"].split(";"))
    sc = collections.defaultdict(lambda: [0, 0])
    for r in svil:
        for t, rx in tok_re.items():
            if rx.search(r["testo"] or ""): sc[t][0] += 1; sc[t][1] += giusto(r, t)
    tok_re = {t: rx for t, rx in tok_re.items() if sc[t][0] >= 3 and sc[t][1] / sc[t][0] >= 0.9}

    def da_testo(testo):
        hit = [t for t, rx in tok_re.items() if rx.search(testo or "")]
        return hit[0] if len(hit) == 1 else None

    s4_ok = s4_tot = 0; s4_err = []; s4_rich = 0
    for r in prova:
        t = da_testo(r["testo"])
        if any(giusto(r, tt) for tt in tok_re): s4_rich += 1
        if not t: continue
        s4_tot += 1
        if giusto(r, t): s4_ok += 1
        elif len(s4_err) < 25: s4_err.append({"cig": r["cig"], "token": t, "aggiudicatari": r["aggiudicatari"][:120]})
    oc_ok = oc_tot = 0; oc_err = []
    for r in rows:
        if r["aggiudicatari"].strip() and r["cig"] in ocds_sup:
            oc_tot += 1
            anac = {w for a in r["aggiudicatari"].split(";") for w in norm(a).split() if len(w) >= 4}
            if any(set(w for w in norm(n).split() if len(w) >= 4) & anac for n in ocds_sup[r["cig"]]): oc_ok += 1
            elif len(oc_err) < 20: oc_err.append({"cig": r["cig"], "anac": r["aggiudicatari"][:100], "ocds": ocds_sup[r["cig"]][:3]})

    def scheda(k, testo):
        t = " " + norm(testo) + " "
        for sid, nome, tip in acn_schede.get(k, []):
            n = norm(nome)
            if len(n) >= 6 and n != k and n.upper() not in GENERICI and f" {n} " in t: return f"{sid} {nome} ({tip})"
        return None
    camp_scheda = []; scheda_tot = collections.Counter()
    est = [re.compile(x, re.I) for x in GRUPPI_ESTERI]

    tot = collections.defaultdict(lambda: {"cig": 0, "eur": 0.0}); per_tip = collections.defaultdict(lambda: collections.defaultdict(float))
    per_prov = collections.Counter(); esclusi = {"cig": 0, "eur": 0.0}; camp_s2 = []; dett = []
    for r in rows:
        imp = float(r["importo_lotto"] or 0)
        if r["e_padre"] == "1" or r["importo_da_verificare"]:
            esclusi["cig"] += 1; esclusi["eur"] += imp; continue
        tips = {cand[c]["tip"] for c in cig_cup.get(r["cig"], ()) if c in cand} or {"?"}
        tip = sorted(tips)[0] if len(tips) == 1 else "più tipologie"
        aggs = [a.strip() for a in r["aggiudicatari"].split(";") if a.strip()]; fonte = ""
        if not aggs and not r["provider"] and r["cig"] in ocds_sup: aggs = ocds_sup[r["cig"]]; fonte = " (aggiudicatario da OCDS)"
        quote = []  # (strato, giurisdizione, chi, quota)
        if r["provider"]:
            g = "EXTRA-UE big tech" if r["provider"] in BIGTECH else r["giurisdizione"]
            quote = [("S1 marchio v3", g, r["provider"], imp)]
        elif aggs:
            q = imp / len(aggs)  # RTI: parti uguali, come rivenditori v3.1
            for a in aggs:
                if any(x.search(a) for x in est): quote.append(("S5 fornitore a controllo extra-UE (non prodotto)" + fonte, "fornitore EXTRA-UE", a, q))
                elif (k := in_acn(a)):
                    quote.append(("S2 servizio qualificato ACN del fornitore" + fonte, "IT", acn_nomi[k], q))
                    if not fonte: camp_s2.append({"cig": r["cig"], "aggiudicatario": a, "fornitore_acn": acn_nomi[k], "schede": dict(acn[k])})
                    sc_ = scheda(k, r["testo"] + " " + ocds_lot.get(r["cig"], ""))
                    scheda_tot["cig"] += 1 / len(aggs); scheda_tot["eur"] += q
                    if sc_:
                        scheda_tot["cig_con_scheda"] += 1 / len(aggs); scheda_tot["eur_con_scheda"] += q
                        camp_scheda.append({"cig": r["cig"], "fornitore": acn_nomi[k], "scheda": sc_, "testo": (r["testo"] + " | " + ocds_lot.get(r["cig"], ""))[:300]})
                else: quote.append(("S3 fornitore italiano fuori elenco ACN" + fonte, "IT (fornitore)", a, q))
        elif (t := da_testo(r["testo"] + " " + ocds_lot.get(r["cig"], ""))):
            quote = [("S4 fornitore riconosciuto nel testo", "IT (fornitore)", t, imp)]
        else:
            quote = [("S6 residuo", "ignoto", "", imp)]
        for s, g, chi, q in quote:
            k = (s, g); tot[k]["cig"] += 1 / len(quote); tot[k]["eur"] += q
            per_tip[tip][g] += q
            if s.startswith("S1") and g.startswith("EXTRA"): per_prov[chi] += q
        dett.append([r["cig"], tip, imp, " | ".join(f"{s}:{g}:{chi}" for s, g, chi, _ in quote)])
    # seconda via: testi degli atti archiviati dei CIG 1.2 (menzioni di infrastrutture cloud nel documento)
    strato_cig = {d[0]: d[3] for d in dett}
    HYP = re.compile(r"\b(aws|amazon\s+web\s+services|microsoft\s+azure|azure|google\s+cloud|oracle\s+cloud|ovh\w*|aruba|tim\s+enterprise|polo\s+strategico)\b", re.I)
    atti = collections.defaultdict(list)
    for f in ("dati/atti/atti.jsonl", "dati/atti/atti-server.jsonl"):
        for l in open(R / f, encoding="utf-8"):
            d = json.loads(l)
            if d.get("cig") in strato_cig and d.get("sha256"): atti[d["cig"]].append(d["sha256"])
    via_atti = {"cig_con_atti": len(atti), "cig_con_testo": 0, "menzioni": collections.Counter(), "esempi": []}
    for cig, shas in atti.items():
        testo = ""
        for h in set(shas):
            p_ = R / "dati/atti/testi" / f"{h}.txt"
            if p_.exists(): testo += p_.read_text(encoding="utf-8", errors="replace")
        if not testo: continue
        via_atti["cig_con_testo"] += 1
        m = sorted({x.lower() for x in HYP.findall(testo)})
        for x in m: via_atti["menzioni"][x] += 1
        if m and len(via_atti["esempi"]) < 30: via_atti["esempi"].append({"cig": cig, "menzioni": m, "strato": strato_cig[cig][:160]})
    via_atti["menzioni"] = dict(via_atti["menzioni"].most_common())
    # stima del residuo S6 per imputazione: quota big tech nei CIG confrontabili attribuiti (stessa tipologia e anno, importo < 140 mila)
    anno = {r["cig"]: r["anno"] for r in rows}
    cfr = collections.defaultdict(lambda: [0.0, 0.0]); s6g = collections.defaultdict(float)
    for d_ in dett:
        imp_ = float(d_[2]); k_ = (d_[1], anno.get(d_[0]))
        if "S6 residuo" in d_[3]: s6g[k_] += imp_
        elif imp_ < 140000: cfr[k_][0] += imp_; cfr[k_][1] += imp_ if "EXTRA-UE big tech" in d_[3] else 0
    s6_imp = sum(v * (cfr[k][1] / cfr[k][0] if cfr[k][0] else 0) for k, v in s6g.items())
    T = sum(v["eur"] for v in tot.values()); N = sum(v["cig"] for v in tot.values())
    bt = sum(v["eur"] for (s, g), v in tot.items() if g == "EXTRA-UE big tech")
    bt_n = sum(v["cig"] for (s, g), v in tot.items() if g == "EXTRA-UE big tech")
    res = sum(v["eur"] for (s, g), v in tot.items() if s.startswith("S6"))
    s2 = sum(v["eur"] for (s, g), v in tot.items() if s.startswith("S2"))
    random.seed(43); campione = random.sample(camp_s2, min(60, len(camp_s2)))
    random.seed(4343); camp_sc = random.sample(camp_scheda, min(40, len(camp_scheda)))
    with open(out_dir / "campione-scheda.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, ["cig", "fornitore", "scheda", "testo", "giudizio"]); w.writeheader()
        for x in camp_sc: w.writerow({**x, "giudizio": ""})
    # pilota infrastruttura (esiti/<data>/pnrr12/saas-infra-pilota.json): euro S2/S3 dei fornitori misurati
    PIL = {"maggioli": "AS208761 Maggioli (IT)", "digitalpa": "AS31898 Oracle (EXTRA-UE)", "dedagroup": "AS8075 Microsoft (EXTRA-UE)",
           "studio amica": "AS12637 Seeweb (IT)", "internet soluzioni": "AS12637 Seeweb (IT)"}
    pil = collections.defaultdict(lambda: {"cig": 0.0, "eur": 0.0})
    for d_ in dett:
        for part in d_[3].split(" | "):
            st, g, chi = (part.split(":", 2) + ["", ""])[:3]
            if not (st.startswith("S2") or st.startswith("S3")): continue
            for k_, v_ in PIL.items():
                if norm(chi).startswith(k_): pil[f"{k_} → {v_}"]["cig"] += 1; pil[f"{k_} → {v_}"]["eur"] += float(d_[2]) / len(d_[3].split(" | "))
    with open(out_dir / "campione-s2.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, ["cig", "aggiudicatario", "fornitore_acn", "schede", "giudizio"]); w.writeheader()
        for x in campione: w.writerow({**x, "schede": json.dumps(x["schede"]), "giudizio": ""})
    with open(out_dir / "pnrr12-dettaglio.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["cig", "tipologia_ente", "importo_lotto", "strati"]); w.writerows(dett)
    tips_fin = collections.defaultdict(lambda: [0, 0.0, 0])
    for c, v in cand.items():
        tips_fin[v["tip"]][0] += 1; tips_fin[v["tip"]][1] += v["imp"]; tips_fin[v["tip"]][2] += c in cup_con_cig
    out = {
        "data": data,
        "universo": {
            "avvisi_1_2": len(avvisi), "stanziato_avvisi_eur": round(sum(float(a["totale_importo_stanziato"] or 0) for a in avvisi)),
            "cup_finanziati": len(cand), "importo_finanziato_eur": round(sum(v["imp"] for v in cand.values())),
            "cup_con_almeno_un_cig": len(cup_con_cig), "copertura_pct": pct(len(cup_con_cig), len(cand)),
            "cig_collegati": len(cig_cup), "cig_nel_perimetro_v3": len(rows),
            "per_tipologia": {k: {"cup": v[0], "finanziato_eur": round(v[1]), "cup_con_cig": v[2], "copertura_pct": pct(v[2], v[0])}
                              for k, v in sorted(tips_fin.items(), key=lambda x: -x[1][1])}},
        "contratti_contati": {"cig": round(N), "eur": round(T)},
        "esclusi_padri_o_da_verificare": {"cig": esclusi["cig"], "eur": round(esclusi["eur"])},
        "per_strato": {f"{s} | {g}": {"cig": round(v["cig"], 1), "eur": round(v["eur"]), "quota_eur_pct": pct(v["eur"], T),
                                       "quota_cig_pct": pct(v["cig"], N)} for (s, g), v in sorted(tot.items())},
        "big_tech_per_provider_eur": {k: round(v) for k, v in per_prov.most_common()},
        "quota_big_tech": {
            "eur": round(bt), "cig": round(bt_n),
            "punto_pct_eur": pct(bt, T), "punto_pct_cig": pct(bt_n, N),
            "limite_alto_pct_eur": pct(bt + res, T),
            "stima_s6_imputata_eur": round(s6_imp), "stima_pct_eur_con_imputazione": pct(bt + s6_imp, T),
            "nota": "limite alto = tutto il residuo S6 come big tech (caso peggiore); l'infrastruttura sotto i SaaS S2/S3 non è misurabile (R55, R73)"},
        "per_tipologia_eur": {t: {g: round(v) for g, v in d.items()} for t, d in per_tip.items()},
        "precisione_s4_censimento": {"metodo": "token scelti su metà sviluppo (sha256(CIG) pari, precisione >= 90 %, >= 3 casi), misurati sulla metà prova (dispari)", "token_tenuti": sorted(tok_re), "vincitori_con_token_nella_prova": s4_rich, "casi": s4_tot, "corretti": s4_ok, "precisione_pct": pct(s4_ok, s4_tot), "errori_esempi": s4_err},
        "s2_eur": round(s2), "acn_schede": sum(sum(c.values()) for c in acn.values()), "acn_fornitori": len(acn),
        "via_atti": via_atti,
        "ocds": {"cig_1_2_in_ocds": len(ocds_lot), "s6_in_ocds_senza_fornitori": sum(1 for d_ in dett if "S6 residuo" in d_[3] and d_[0] in ocds_lot), "con_fornitori": len(ocds_sup), "precisione_vs_anac": {"casi": oc_tot, "corretti": oc_ok, "pct": pct(oc_ok, oc_tot), "errori_esempi": oc_err}},
        "scheda_acn_dal_testo": {"cig_s2": round(scheda_tot["cig"], 1), "eur_s2": round(scheda_tot["eur"]), "cig_con_scheda": round(scheda_tot["cig_con_scheda"], 1),
                                 "eur_con_scheda": round(scheda_tot["eur_con_scheda"]), "campione": "campione-scheda.csv (40, seme 4343)"},
        "pilota_infra_eur_s2_s3": {k: {"cig": round(v["cig"], 1), "eur": round(v["eur"])} for k, v in pil.items()},
        "token_s4_candidati": len(tok), "token_s4_tenuti": len(tok_re)}
    json.dump(out, open(out_dir / "pnrr12-prodotto.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in out.items() if k != "precisione_s4_censimento"} | {"precisione_s4": {k: out["precisione_s4_censimento"][k] for k in ("casi", "corretti", "precisione_pct")}}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
