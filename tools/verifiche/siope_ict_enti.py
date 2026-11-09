"""#12 SIOPE come denominatore per ente della spesa ICT (enti territoriali, sanità, altri enti non statali) e copertura dei CIG ICT dell'imbuto.

1. Codici gestionali ICT (anagrafica SIOPE ANAG_CODGEST_USCITE, archiviata, descrizioni lette dal file):
   - piano dei conti armonizzato (tutti i comparti tranne SAN e STA, d.lgs. 118/2011, codici «x.xx.xx.xx.xxx»):
     servizi    1.03.02.19.*  servizi informatici e di telecomunicazioni (001-011, 999)
     licenze    1.03.02.07.006 licenze d'uso per software;  noleggi 1.03.02.07.004 noleggi di hardware
     materiale  1.03.01.02.006 materiale informatico
     hardware   2.02.01.07.* hardware;  2.02.04.07.* hardware in leasing finanziario
     software   2.02.03.02.* sviluppo e acquisto software;  2.02.06.01.001 software in leasing finanziario
     telefonia  1.03.02.05.001/002 telefonia fissa e mobile (riportata a parte: «ICT» = senza telefonia, «ICT+TLC» = con)
   - strutture sanitarie (comparto SAN, codifica SIOPE sanità a 4 cifre, d.m. 2007 e ss.):
     3212 assistenza informatica e manutenzione software (servizi); 5205 licenze software (licenze);
     3208 utenze e canoni per telefonia e reti di trasmissione (telefonia).
     NON in ICT perché misti: 2204 supporti informatici e cancelleria, 6200 immobilizzazioni immateriali, 6103/6199
     (impianti, altri beni): riportati come «san_misti» per dare il limite superiore. L'hardware sanitario non ha un codice
     proprio: la sanità è sottostimata dall'inizio.
   - comparto STA (Stato) escluso: lo Stato si misura con BDAP (bdap_ict_stato.py), per non contarlo due volte.
   Sono codici di ACQUISTO: i trasferimenti fra enti (1.04/2.03, 41xx) non entrano, quindi niente doppio conteggio da
   trasferimenti; restano i pagamenti fra enti per servizi (es. ente che paga una società in-house o un altro ente).
2. Pagato per ente = somma dei mesi (SIOPE_USCITE.<anno>.zip, centesimi) per codice fiscale (ANAG_ENTI_SIOPE: più codici
   ente SIOPE possono avere lo stesso CF: articolazioni, gestioni; si sommano). Anni 2022-2025 (cassa).
3. CIG ICT dell'imbuto (lavoro/imbuto/ict.csv, strati S3-S6, senza S0/S2 né importi da verificare, come bdap_cig_ministeri_cf):
   CF della stazione appaltante e del delegante dal CIG ANAC (ultima versione), importo per anno di pubblicazione e quota
   annua dei CIG attivi (stessa regola: uniforme sulla durata, senza durata tutto nell'anno, max 10 anni).
4. Abbinamento per CF SA == CF ente SIOPE. Copertura = quota annua CIG attivi / pagato ICT SIOPE (non è una percentuale
   in senso stretto: competenza contrattuale contro cassa). Per comparto, sottocomparto, regione, classe di dimensione
   (popolazione per i comuni dall'anagrafica SIOPE; pagato totale per gli altri).
5. CE SSN (BDAP, voce BA1620 «servizi di assistenza informatica», righe 999 = consolidato regionale) 2022-2024 per regione, contro SIOPE SAN 3212 per regione.

Uso (server): nice -n 19 ionice -c3 .venv/bin/python tools/verifiche/siope_ict_enti.py
  -> esiti/<oggi>/siope/ict-enti.json, ict-enti.csv (per CF), ict-enti-scarti.csv (enti con molto pagato e pochi CIG e viceversa)
Lettura in streaming; in memoria solo i CIG di ict.csv (come bdap_cig_ministeri_cf)."""
import collections, csv, datetime, hashlib, io, json, os, sys, zipfile
from pathlib import Path

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/verifiche")); sys.path.insert(0, str(R / "tools/analisi"))
import bdap_cig_ministeri_cf as M  # noqa: E402

ARC = M.ARC
SIO = ARC / "mirror/www.siope.it/documenti/siope2/open/last"
DUMP = ARC / "mirror/bdap-opendata.rgs.mef.gov.it/SpodCkanApi/api/3/datastore/dump"
CE_SSN = {2022: "5afc4cf8-a13e-4fb6-a81b-61896de5f9ea", 2023: "57bb2cce-4fdd-4de1-88b5-8e7551408481", 2024: "94083af2-a542-482d-8ad6-5877d04cd1ca"}
ANNI = (2022, 2023, 2024, 2025)
VERSIONE = "siope-ict-enti 0.1.1 (2026-11-10)"
CAT_ARM = [("1.03.02.19.", "servizi"), ("1.03.02.07.006", "licenze"), ("1.03.02.07.004", "noleggi"), ("1.03.01.02.006", "materiale"),
           ("2.02.01.07.", "hardware"), ("2.02.04.07.", "hardware"), ("2.02.03.02.", "software"), ("2.02.06.01.001", "software"),
           ("1.03.02.05.001", "telefonia"), ("1.03.02.05.002", "telefonia")]
CAT_SAN = {"3212": "servizi", "5205": "licenze", "3208": "telefonia", "2204": "san_misti", "6200": "san_misti"}
ICT = ("servizi", "licenze", "noleggi", "materiale", "hardware", "software")


def cat(codice, san):
    if san: return CAT_SAN.get(codice)
    for p, c in CAT_ARM:
        if codice.startswith(p): return c
    return None


def sha(p): return M.sha(p)


def classe(comparto, sotto, pop, tot):
    if sotto == "COMUNE" and pop:
        p = int(pop)
        return "comune <5k" if p < 5000 else "comune 5-20k" if p < 20000 else "comune 20-100k" if p < 100000 else "comune >=100k"
    t = tot / 1e6
    return "pagato tot <10 M€" if t < 10 else "pagato tot 10-100 M€" if t < 100 else "pagato tot 100M-1mld" if t < 1000 else "pagato tot >=1 mld"


def main():
    csv.field_size_limit(10 ** 8)
    ing = {}
    za = SIO / "SIOPE_ANAGRAFICHE.zip"; ing[za.name] = sha(za); anag = zipfile.ZipFile(za)
    nm = lambda p: next(i for i in anag.namelist() if i.startswith(p))
    rd = lambda p: csv.reader(io.TextIOWrapper(anag.open(nm(p)), encoding="utf-8-sig", errors="replace"))
    reg = {r[3]: r[2] for r in rd("ANAG_REG_PROV")}
    sotto2comp = {r[0]: r[2] for r in rd("ANAG_SOTTOCOMPARTI")}
    desc = {}
    for r in rd("ANAG_CODGEST_USCITE"):
        desc.setdefault((r[0], r[1] == "SAN"), r[2])
    cod2cf = {}; ente = {}
    for r in rd("ANAG_ENTI_SIOPE"):
        cf = r[3].strip(); comp = sotto2comp.get(r[8], "?")
        cod2cf[r[0]] = (cf, comp == "SAN")
        e = ente.setdefault(cf, {"nomi": [], "comparto": comp, "sotto": r[8], "regione": reg.get(r[6], "?"), "pop": "", "codici": 0})
        e["codici"] += 1; e["nomi"].append((r[2] < "9999", len(r[0]), r[4], r[8]))
        if r[7] != "N.A." and not e["pop"]: e["pop"] = r[7]
        if r[0].strip() and len(r[0]) <= 9 and r[2].startswith("9999"): e["comparto"], e["sotto"] = comp, r[8]  # ente principale
    # 1-2. SIOPE uscite
    pag = collections.defaultdict(collections.Counter)  # cf -> (anno, cat) -> euro
    codici = collections.defaultdict(collections.Counter)  # (anno) -> codice -> euro (ICT)
    for a in ANNI:
        z = SIO / f"SIOPE_USCITE.{a}.zip"; ing[z.name] = sha(z); zf = zipfile.ZipFile(z)
        for r in csv.reader(io.TextIOWrapper(zf.open(zf.namelist()[0]), encoding="utf-8-sig", errors="replace")):
            if r[1] != str(a): continue
            x = cod2cf.get(r[0])
            if not x: pag["?" + r[0]][(a, "tot")] += int(r[4] or 0) / 100; continue
            cf, san = x; v = int(r[4] or 0) / 100
            pag[cf][(a, "tot")] += v
            c = cat(r[3], san)
            if c: pag[cf][(a, c)] += v; codici[a][r[3] + ("|SAN" if san else "")] += v
        print("siope", a, flush=True)
    # 3. CIG
    ict = {}
    for r in csv.DictReader(open(R / "lavoro/imbuto/ict.csv", encoding="utf-8")):
        if r["strato"][:2] in ("S0", "S2") or r["importo_da_verificare"] == "1": continue
        ict[r["cig"]] = (int(r["anno"]), M.B.num(r["importo"]), r["strato"][:2])
    ing["ict.csv"] = {"file": "lavoro/imbuto/ict.csv", "sha256": sha(R / "lavoro/imbuto/ict.csv"), "cig_s3_s6": len(ict)}
    anac, files = M.cig_anac(set(ict)); ing["cig_anac"] = {"file": files, "nota": "sha256 nel manifest dell'archivio"}
    cf2amm, ing_ipa = M.ipa(); ing |= ing_ipa
    cig = collections.defaultdict(collections.Counter)  # cf -> chiave -> valore
    tot_cig = collections.defaultdict(collections.Counter)  # anno -> destinazione -> euro
    for c, (anno, imp, strato) in ict.items():
        a = anac.get(c)
        if not a: tot_cig[anno]["senza-cig-anac"] += imp; continue
        cf = a["cf"]; dest = "siope" if cf in ente and ente[cf]["comparto"] != "STA" else "stato" if cf in cf2amm or (cf in ente and ente[cf]["comparto"] == "STA") else "altro"
        tot_cig[anno][dest] += imp; tot_cig[anno]["tutti"] += imp
        cig[cf][(anno, "imp")] += imp; cig[cf][(anno, "n")] += 1; cig[cf][(anno, "imp_" + strato)] += imp
        if a["cf_del"] and a["cf_del"] != cf and a["cf_del"] in ente: cig[a["cf_del"]][(anno, "imp_delegante")] += imp
        for y, v in M.quote(imp, a["data"], a["durata"]).items():
            cig[cf][(y, "quota")] += v; tot_cig[y]["quota_" + dest] += v; tot_cig[y]["quota_tutti"] += v
    print("cig", len(anac), flush=True)
    # 4. abbinamento e tabelle
    righe = []; grp = collections.defaultdict(collections.Counter)
    for cf, e in ente.items():
        if e["comparto"] == "STA": continue
        p = pag.get(cf); g = cig.get(cf, collections.Counter())
        if not p: continue
        nome = sorted(e["nomi"], key=lambda t: (t[3] != e["sotto"], t[0], t[1]))[0][2]
        row = {"cf": cf, "ente": nome, "comparto": e["comparto"], "sottocomparto": e["sotto"], "regione": e["regione"], "popolazione": e["pop"]}
        for a in ANNI:
            ictv = sum(p[(a, k)] for k in ICT); row[f"ict_{a}"] = round(ictv); row[f"tlc_{a}"] = round(p[(a, "telefonia")])
            row[f"tot_{a}"] = round(p[(a, "tot")]); row[f"cig_imp_{a}"] = round(g[(a, "imp")]); row[f"cig_n_{a}"] = g[(a, "n")]
            row[f"cig_quota_{a}"] = round(g[(a, "quota")])
            if e["comparto"] == "SAN": row[f"san_misti_{a}"] = round(p[(a, "san_misti")])
            cl = classe(e["comparto"], e["sotto"], e["pop"], p[(2024, "tot")])
            for dim, val in (("comparto", e["comparto"]), ("sottocomparto", e["sotto"]), ("regione", e["regione"]), ("classe", cl), ("tutti", "tutti")):
                k = grp[(a, dim, val)]
                k["enti"] += 1; k["ict"] += ictv; k["tlc"] += p[(a, "telefonia")]; k["cig_imp"] += g[(a, "imp")]; k["cig_n"] += g[(a, "n")]
                k["cig_quota"] += g[(a, "quota")]; k["san_misti"] += p[(a, "san_misti")]
                for s in ("S3", "S4", "S5", "S6"): k["cig_imp_" + s] += g[(a, "imp_" + s)]
                if ictv > 0: k["enti_con_ict"] += 1
                if ictv > 0 and g[(a, "n")] == 0 and g[(a, "quota")] == 0: k["enti_ict_senza_cig"] += 1; k["ict_senza_cig"] += ictv
                for c2 in ICT: k["ict_" + c2] += p[(a, c2)]
        row["classe"] = classe(e["comparto"], e["sotto"], e["pop"], p[(2024, "tot")])
        righe.append(row)
    tab = {}
    for (a, dim, val), k in grp.items():
        d = {kk: round(v) for kk, v in k.items()}
        d["copertura_quota"] = round(k["cig_quota"] / k["ict"], 3) if k["ict"] else None
        d["copertura_quota_con_tlc"] = round(k["cig_quota"] / (k["ict"] + k["tlc"]), 3) if k["ict"] + k["tlc"] else None
        d["rapporto_importo_anno"] = round(k["cig_imp"] / k["ict"], 3) if k["ict"] else None
        tab.setdefault(str(a), {}).setdefault(dim, {})[val] = d
    # scarti: 2024, pagato ICT >= 1 M€
    sc = []
    for r in righe:
        ictv = r["ict_2024"] + r["ict_2023"]; q = r["cig_quota_2024"] + r["cig_quota_2023"]
        if ictv >= 2e6 and q / ictv < 0.2: sc.append(r | {"tipo": "molto pagato, pochi CIG", "rapporto_2023_24": round(q / ictv, 3)})
        elif q >= 2e6 and q / max(ictv, 1) > 5: sc.append(r | {"tipo": "molti CIG, poco pagato", "rapporto_2023_24": round(q / max(ictv, 1), 3)})
    sc.sort(key=lambda r: -(r["ict_2024"] + r["ict_2023"] + r["cig_quota_2024"] + r["cig_quota_2023"]))
    # codici effettivamente usati
    cod_tab = {str(a): sorted(([k, desc.get((k.split("|")[0], k.endswith("|SAN")), "?"), round(v)] for k, v in codici[a].items()), key=lambda x: -x[2]) for a in ANNI}
    # 5. CE SSN BA1620 per regione e SIOPE SAN servizi per regione
    ce = {}
    for a, rid in CE_SSN.items():
        p = DUMP / f"{rid}.csv"; ing[f"ce-ssn-{a}"] = {"file": str(p.relative_to(ARC)), "sha256": sha(p)}
        c = collections.Counter(); voci = {}
        for x in csv.DictReader(open(p, encoding="cp1252", newline=""), delimiter=";"):
            if x["Tipo Rilevazione"] != "CONSUNTIVO" or x["Codice Ente SSN"] != "999": continue  # 999 = consolidato regionale (= enti + GSA «000»)
            v = x["Codice Voce Contabile"]
            if v in ("BA1620",):
                c[x["Descrizione Regione"].upper()] += M.B.num(x["Importo Totale"]); voci[v] = x["Descrizione Voce Contabile"]
        ce[str(a)] = {"voci": voci, "totale": round(sum(c.values())), "per_regione": {k: round(v) for k, v in sorted(c.items())},
                      "siope_san_servizi_per_regione": {k: v["ict_servizi"] for k, v in tab.get(str(a), {}).get("regione", {}).items()}}
    out = {"versione": VERSIONE, "ingressi": ing,
           "regole": {"armonizzato": CAT_ARM, "sanita": CAT_SAN, "ict": ICT, "esclusi": "comparto STA (Stato, si usa BDAP)"},
           "enti_siope_con_pagamenti": len(righe), "codici_ict_usati": cod_tab,
           "cig_per_destinazione": {str(a): {k: round(v) for k, v in c.items()} for a, c in sorted(tot_cig.items())},
           "tabelle": tab, "ce_ssn_ba1620": ce, "scarti_n": collections.Counter(r["tipo"] for r in sc)}
    o = R / f"esiti/{datetime.date.today().isoformat()}/siope"; os.makedirs(o, exist_ok=True)
    json.dump(out, open(o / "ict-enti.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=str)
    campi = list(righe[0].keys())
    for f, rows, extra in (("ict-enti.csv", sorted(righe, key=lambda r: -r["ict_2024"]), []), ("ict-enti-scarti.csv", sc, ["tipo", "rapporto_2023_24"])):
        with open(o / f, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=campi + [c for c in ("san_misti_2022", "san_misti_2023", "san_misti_2024", "san_misti_2025") if c not in campi] + extra, extrasaction="ignore")
            w.writeheader(); [w.writerow(r) for r in rows if r.get("ict_2024", 0) or r.get("cig_quota_2024", 0) or f.endswith("scarti.csv")]
    for a in ANNI: print(a, json.dumps(tab[str(a)]["tutti"]["tutti"]), json.dumps(out["cig_per_destinazione"].get(str(a), {})))
    for a in ("2024",):
        for dim in ("comparto", "classe"):
            for v, d in sorted(tab[a][dim].items(), key=lambda t: -t[1]["ict"]): print(a, dim, v, d["enti"], d["ict"], d["cig_quota"], d["copertura_quota"], d.get("enti_ict_senza_cig", 0))
    print(json.dumps({k: v["totale"] for k, v in ce.items()}), out["scarti_n"])


if __name__ == "__main__":
    main()
