"""#12 Regione Lombardia (CF 80050050154): dove va la spesa ICT pagata in SIOPE (GSA e bilancio ordinario).

1. SIOPE uscite 2022-2025 per CODICE ENTE SIOPE (lo stesso CF ha più codici: Regione ordinaria, gestione sanitaria
   accentrata, ecc.; siope_ict_enti.py li somma per CF): codici gestionali ICT (stesse regole di siope_ict_enti.cat),
   per mese, e i codici ICT più grandi; più i trasferimenti verso imprese/partecipate (1.04.03.*, 2.03.03.*, SAN 41xx/42xx)
   per vedere se l'ICT verso ARIA passa come trasferimento e non come acquisto.
2. ANAC: CIG con SA = ARIA S.p.A. (CF 05017630152, solo quello: la regex della 0.1 di siope_inhouse_4enti prendeva
   anche IM.I.S.C.A. e altri «ARIA») per anno, ICT (imbuto ict.csv, senza S0/S2) e no; CIG con aggiudicataria ARIA per SA.
Uso (server): nice -n 19 ionice -c3 .venv/bin/python tools/verifiche/siope_lombardia_gsa.py
  -> esiti/<oggi>/siope/lombardia-gsa.json, lombardia-gsa-mesi.csv"""
import collections, csv, datetime, glob, io, json, os, sys, zipfile
from pathlib import Path

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/verifiche")); sys.path.insert(0, str(R / "tools/analisi"))
import bdap_cig_ministeri_cf as M  # noqa: E402
import siope_ict_enti as S  # noqa: E402

CF = "80050050154"; ARIA = "05017630152"; ANNI = S.ANNI
VERSIONE = "siope-lombardia-gsa 0.1 (2026-11-10)"


def csvzip(z, delim=","):
    zf = zipfile.ZipFile(z); m = next(i for i in zf.namelist() if i.lower().endswith(".csv")) if delim == ";" else zf.namelist()[0]
    t = io.TextIOWrapper(zf.open(m), encoding="utf-8-sig", errors="replace")
    return csv.DictReader(t, delimiter=";") if delim == ";" else csv.reader(t)


def main():
    csv.field_size_limit(10 ** 8)
    ing = {}
    za = S.SIO / "SIOPE_ANAGRAFICHE.zip"; ing[za.name] = M.sha(za); anag = zipfile.ZipFile(za)
    nm = lambda p: next(i for i in anag.namelist() if i.startswith(p))
    rd = lambda p: csv.reader(io.TextIOWrapper(anag.open(nm(p)), encoding="utf-8-sig", errors="replace"))
    sotto2comp = {r[0]: r[2] for r in rd("ANAG_SOTTOCOMPARTI")}
    desc = {}
    for r in rd("ANAG_CODGEST_USCITE"): desc[(r[0], r[1] == "SAN")] = r[2]
    codici = {}
    for r in rd("ANAG_ENTI_SIOPE"):
        if r[3].strip() == CF: codici[r[0]] = {"nome": r[4], "sottocomparto": r[8], "san": sotto2comp.get(r[8]) == "SAN", "riga": r[:9]}
    out = {"versione": VERSIONE, "ingressi": ing, "codici_ente": codici, "siope": {}}
    mesi = []
    for a in ANNI:
        z = S.SIO / f"SIOPE_USCITE.{a}.zip"; ing[z.name] = M.sha(z)
        acc = collections.defaultdict(collections.Counter)
        for r in csvzip(z):
            if r[0] not in codici or r[1] != str(a): continue
            k = codici[r[0]]; v = int(r[4] or 0) / 100; c = S.cat(r[3], k["san"]); e = acc[r[0]]
            e["tot"] += v
            if c in S.ICT or c == "telefonia":
                e["cat:" + c] += v; e["cod:" + r[3]] += v
                if c in S.ICT: e["ict"] += v; e["mese:" + r[2]] += v; mesi.append((r[0], a, r[2], r[3], round(v, 2)))
            if r[3].startswith(("1.04.03.", "2.03.03.")) or (k["san"] and r[3][:2] in ("41", "42", "43")):
                e["trasf:" + r[3]] += v
        out["siope"][a] = {ce: {"tot": round(e["tot"]), "ict": round(e["ict"]),
                                "categorie": {k[4:]: round(v) for k, v in e.items() if k.startswith("cat:")},
                                "codici_ict": sorted([[k[4:], desc.get((k[4:], codici[ce]["san"]), "?"), round(v)] for k, v in e.items() if k.startswith("cod:")], key=lambda t: -t[2]),
                                "mesi_ict": {k[5:]: round(v) for k, v in sorted(e.items()) if k.startswith("mese:")},
                                "trasferimenti_top": sorted([[k[6:], desc.get((k[6:], codici[ce]["san"]), "?"), round(v)] for k, v in e.items() if k.startswith("trasf:")], key=lambda t: -t[2])[:12]}
                           for ce, e in acc.items()}
        print("siope", a, flush=True)
    # 2. ANAC
    ict = {}
    for r in csv.DictReader(open(R / "lavoro/imbuto/ict.csv", encoding="utf-8")): ict[r["cig"]] = r["strato"][:2]
    agg = collections.defaultdict(set)
    z = sorted(glob.glob(str(M.D / "aggiudicatari/filesystem/aggiudicatari_csv.zip")))[0]
    for r in csvzip(z, ";"): agg[r["cig"]].add((r["codice_fiscale"] or "").strip())
    ing["aggiudicatari"] = {"file": os.path.relpath(z, M.ARC), "sha256": M.sha(z)}
    zz = [z for a in range(2020, 2027) for z in sorted(glob.glob(str(M.D / f"cig-{a}/filesystem/cig_csv_*.zip")))] + sorted(glob.glob(str(M.D / "cig/filesystem/*-cig_csv.zip")))
    seen = {}
    for z in zz:
        for r in csvzip(z, ";"):
            cf = (r["cf_amministrazione_appaltante"] or "").strip()
            if cf == ARIA or ARIA in agg.get(r["cig"], ()) or cf == CF:
                seen[r["cig"]] = {"cf": cf, "anno": r["data_pubblicazione"][:4], "imp": M.B.num(r["importo_lotto"]), "ogg": r["oggetto_lotto"][:140],
                                  "cpv": r["cod_cpv"], "scelta": r["tipo_scelta_contraente"], "sa": r["denominazione_amministrazione_appaltante"][:60]}
    ing["cig_anac"] = {"n_file": len(zz), "nota": "cig-2020..2026 + delta, ultima versione per CIG; sha256 nel manifest dell'archivio"}
    sa = collections.defaultdict(collections.Counter); a_aria = collections.defaultdict(collections.Counter); top = []; strati = collections.Counter()
    for c, v in seen.items():
        y = v["anno"]; s = ict.get(c)
        if v["cf"] == ARIA:
            sa[y]["n"] += 1; sa[y]["imp"] += v["imp"]
            if s: strati[(y, s)] += v["imp"]
            if s and s not in ("S0", "S2"): sa[y]["n_ict"] += 1; sa[y]["imp_ict"] += v["imp"]; top.append((c, v, s))
        if ARIA in agg.get(c, ()):
            chi = "regione" if v["cf"] == CF else "aria" if v["cf"] == ARIA else "altri"
            a_aria[y]["n_" + chi] += 1; a_aria[y]["imp_" + chi] += v["imp"]
    top.sort(key=lambda t: -t[1]["imp"])
    r2 = lambda d: {y: {k: round(x) for k, x in c.items()} for y, c in sorted(d.items()) if "2020" <= y <= "2026"}
    out["anac"] = {"cig_sa_aria": r2(sa), "cig_sa_aria_per_strato": {f"{y}|{s}": round(v) for (y, s), v in sorted(strati.items())},
                   "cig_aggiudicati_ad_aria": r2(a_aria), "top_ict_sa_aria": [{"cig": c, "strato": s} | v for c, v, s in top[:40]]}
    o = R / f"esiti/{datetime.date.today().isoformat()}/siope"; os.makedirs(o, exist_ok=True)
    json.dump(out, open(o / "lombardia-gsa.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=str)
    with open(o / "lombardia-gsa-mesi.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["codice_ente", "anno", "mese", "codice_gestionale", "euro"]); w.writerows(mesi)
    for ce, k in codici.items(): print(ce, k["nome"], k["sottocomparto"], k["san"])
    for a in ANNI:
        for ce, e in out["siope"][a].items():
            print(a, ce, e["tot"], e["ict"], e["codici_ict"][:4], e["mesi_ict"]); print("   trasf", e["trasferimenti_top"][:6])
    print(json.dumps(out["anac"]["cig_sa_aria"])); print(json.dumps(out["anac"]["cig_aggiudicati_ad_aria"]))
    for t in out["anac"]["top_ict_sa_aria"][:15]: print(t)


if __name__ == "__main__":
    main()
