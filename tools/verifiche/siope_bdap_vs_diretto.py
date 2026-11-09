"""#30 SIOPE via BDAP contro SIOPE diretto (www.siope.it, open data), per anno, tutte le regioni presenti nel mirror.

BDAP («<anno> - <regione> - SIOPE Movimenti cumulati mensili di Spesa», CKAN datastore/dump, cp1252): ente per nome,
provincia e comune ISTAT, tipo ente BDAP, codice gestionale «U1030219001», importo CUMULATO per mese. Si prende il
cumulato del mese più alto per ente x codice.
SIOPE diretto (SIOPE_USCITE.<anno>.zip: codice ente, anno, mese, codice gestionale «1.03.02.19.001», importo in
centesimi; SIOPE_ANAGRAFICHE.zip/ANAG_ENTI: codice, CF, nome, comune e provincia ISTAT): somma dei mesi per ente x codice.

Risorse BDAP: lette dalle pagine package_search archiviate (titolo -> URL datastore/dump), solo quelle presenti nel mirror.

Abbinamento degli enti (BDAP non ha codice ente né CF, R70), a livelli, solo coppie univoche:
  L1 (provincia, comune, nome normalizzato) identici;
  L2 stessa (provincia, comune), nome con somiglianza >= 0,90 (difflib), migliore univoco fra i non abbinati;
  L3 stessa (provincia, comune), ente BDAP di tipo CO (comune) e un solo ente diretto non abbinato «COMUNE DI ...».
Codici: «U» + cifre senza punti su entrambi i lati.
Misure: enti abbinati e non; coppie ente x codice uguali (|diff| <= 1 €), diverse, presenti da una parte sola;
totali; lo stesso per i codici ICT (U1030219, U2020107, U2020301); per regione.
Troncamento riferito da AgID (#30: «2025 troncato a marzo per 1.717 comuni»): ultimo mese per ente in BDAP (tutti gli
enti, non solo gli abbinati, per regione e per i soli comuni) e nel diretto (tutti i comuni d'Italia).

Uso (server): nice .venv/bin/python tools/verifiche/siope_bdap_vs_diretto.py ANNO -> esiti/<oggi>/siope/bdap-vs-diretto-<anno>.json"""
import collections, csv, datetime, difflib, glob, hashlib, io, json, os, re, sys, zipfile
from pathlib import Path

R = Path(__file__).resolve().parents[2]
ARC = Path(os.environ.get("ARCHIVIO_ROOT", R / "archivio"))
API = ARC / "mirror/bdap-opendata.rgs.mef.gov.it/SpodCkanApi/api/3"
DUMP = API / "datastore/dump"
SIO = ARC / "mirror/www.siope.it/documenti/siope2/open/last"
ANNO = int(sys.argv[1]) if len(sys.argv) > 1 else 2024
ICT = ("U1030219", "U2020107", "U2020301")
VERSIONE = "siope-bdap-vs-diretto 0.2 (2026-11-09)"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


def norm(s):
    return re.sub(r"[^A-Z0-9]+", " ", s.upper().replace("'", " ")).strip()


def cod(c):
    c = c.strip()
    return c if c.startswith("U") else "U" + c.replace(".", "")


def risorse(anno):
    """{REGIONE: id risorsa} dalle pagine package_search archiviate."""
    out = {}
    for f in sorted(glob.glob(str(API / "action/package_search__allegati/*/_"))):
        for p in json.load(open(f, encoding="utf-8"))["result"]["results"]:
            t = p["title"]
            if not t.startswith(f"{anno} - ") or not t.endswith("SIOPE Movimenti cumulati mensili di Spesa"): continue
            for r in p["resources"]:
                if "/datastore/dump/" in r.get("url", ""):
                    out[t.split(" - ")[1].upper()] = (r["url"].rsplit("/", 1)[1].removesuffix(".csv"), p.get("metadata_modified"), r.get("created"))
    return out


def main():
    csv.field_size_limit(10 ** 8)
    ing = {}
    bdap = {k: v for k, v in risorse(ANNO).items() if (DUMP / f"{v[0]}.csv").exists()}
    anag = zipfile.ZipFile(SIO / "SIOPE_ANAGRAFICHE.zip"); ing["SIOPE_ANAGRAFICHE.zip"] = sha(SIO / "SIOPE_ANAGRAFICHE.zip")
    nm = lambda p: next(i for i in anag.namelist() if i.startswith(p))
    reg = {r[3]: r[2] for r in csv.reader(io.TextIOWrapper(anag.open(nm("ANAG_REG_PROV")), encoding="utf-8-sig"))}
    regn = lambda s: norm(s).replace(" ", "")
    bset = {regn(x) for x in bdap}
    ent_d = collections.defaultdict(list)  # (prov, com, nome) -> codici ente
    comuni_d = set()  # codici ente diretto dei comuni (tutta Italia)
    for r in csv.reader(io.TextIOWrapper(anag.open(nm("ANAG_ENTI")), encoding="utf-8-sig", errors="replace")):
        if norm(r[4]).startswith("COMUNE DI "): comuni_d.add(r[0])
        if regn(reg.get(r[6], "")) in bset: ent_d[(r[6], r[5], norm(r[4]))].append(r[0])
    # BDAP
    b = {}; ent_b = collections.Counter(); bm = {}; tipo_b = {}; reg_b = {}
    for regione, (rid, mod, cre) in sorted(bdap.items()):
        p = DUMP / f"{rid}.csv"
        ing[f"bdap-{regione}"] = {"file": str(p.relative_to(ARC)), "sha256": sha(p), "metadata_modified": mod, "risorsa_creata": cre}
        for x in csv.DictReader(open(p, encoding="cp1252", newline=""), delimiter=";"):
            k = (x["Codice istat provincia"], x["Codice istat comune"], norm(x["Descrizione Ente BDAP"]))
            kk = (k, x["Codice Gestionale Enti Locali"].strip()); mese = x["Anno/Mese calendario"]
            ent_b[k] = max(ent_b[k], int(mese[-2:])); tipo_b[k] = x["Codice Tipologia Ente BDAP"]; reg_b[k] = regione
            if kk not in bm or mese > bm[kk]: bm[kk] = mese; b[kk] = float(x["Importo cumulato"] or 0)
    # abbinamento a livelli: chiave BDAP -> codice ente diretto
    ab = {}; livello = collections.Counter()
    for k in ent_b:
        v = ent_d.get(k)
        if v and len(v) == 1: ab[k] = v[0]; livello["L1"] += 1
    usati = set(ab.values())
    per_luogo = collections.defaultdict(list)
    for (pr, co, n), v in ent_d.items():
        if len(v) == 1 and v[0] not in usati: per_luogo[(pr, co)].append((n, v[0]))
    esempi_l2 = []
    for k in sorted(set(ent_b) - set(ab)):
        cand = [(difflib.SequenceMatcher(None, k[2], n).ratio(), n, c) for n, c in per_luogo.get(k[:2], []) if c not in usati]
        cand.sort(reverse=True)
        if cand and cand[0][0] >= 0.90 and (len(cand) == 1 or cand[1][0] < cand[0][0]):
            ab[k] = cand[0][2]; usati.add(cand[0][2]); livello["L2"] += 1
            if len(esempi_l2) < 10: esempi_l2.append([k[2], cand[0][1], round(cand[0][0], 3)])
            continue
        if tipo_b[k] == "CO":
            co = [c for n, c in per_luogo.get(k[:2], []) if n.startswith("COMUNE DI ") and c not in usati]
            if len(co) == 1: ab[k] = co[0]; usati.add(co[0]); livello["L3"] += 1
    cod2key = {c: k for k, c in ab.items()}
    # SIOPE diretto
    z = SIO / f"SIOPE_USCITE.{ANNO}.zip"; ing[z.name] = sha(z); zf = zipfile.ZipFile(z); ing[z.name + ":interno"] = zf.namelist()[0]
    d = collections.Counter(); mese_d = {}; mese_com = {}
    for r in csv.reader(io.TextIOWrapper(zf.open(zf.namelist()[0]), encoding="utf-8-sig", errors="replace")):
        if r[1] != str(ANNO): continue
        if r[0] in comuni_d: mese_com[r[0]] = max(mese_com.get(r[0], ""), r[2])
        k = cod2key.get(r[0])
        if k: d[(k, cod(r[3]))] += int(r[4] or 0) / 100; mese_d[k] = max(mese_d.get(k, ""), r[2])
    eb = set(ent_b); ent_comuni = set(ab)
    out = {"versione": VERSIONE, "anno": ANNO, "regioni": sorted(bdap), "ingressi": ing,
           "enti": {"bdap": len(eb), "diretto_univoci": sum(1 for v in ent_d.values() if len(v) == 1),
                    "diretto_ambigui": sum(1 for v in ent_d.values() if len(v) > 1),
                    "abbinati": len(ent_comuni), "per_livello": dict(livello), "solo_bdap": len(eb - ent_comuni),
                    "solo_bdap_per_tipo": dict(collections.Counter(tipo_b[k] for k in eb - ent_comuni)),
                    "esempi_l2": esempi_l2, "esempi_solo_bdap": sorted(eb - ent_comuni)[:20]}}
    # troncamento
    per_reg = {}
    for regione in sorted(bdap):
        ks = [k for k in eb if reg_b[k] == regione]; com = [k for k in ks if tipo_b[k] == "CO"]
        per_reg[regione] = {"enti": len(ks), "comuni": len(com),
                            "comuni_ultimo_mese": dict(sorted(collections.Counter(ent_b[k] for k in com).items())),
                            "enti_ultimo_mese_lt12": sum(1 for k in ks if ent_b[k] < 12)}
    tr = collections.Counter(); tr_es = []
    for k in ent_comuni:
        mb, md = ent_b[k], int(mese_d.get(k) or 0)
        t = "uguale" if mb == md else "bdap_prima" if mb < md else "bdap_dopo"; tr[t] += 1
        if t != "uguale" and len(tr_es) < 15: tr_es.append({"ente": list(k), "ultimo_mese_bdap": mb, "ultimo_mese_diretto": md})
    out["ultimo_mese"] = dict(tr) | {
        "bdap_comuni_tutti": dict(sorted(collections.Counter(ent_b[k] for k in eb if tipo_b[k] == "CO").items())),
        "diretto_comuni_italia": dict(sorted(collections.Counter(int(m) for m in mese_com.values()).items())),
        "diretto_comuni_italia_senza_movimenti": len(comuni_d - set(mese_com)),
        "per_regione": per_reg, "esempi_differenti": tr_es}
    for nome, filtro in (("tutti", lambda c: True), ("ict", lambda c: c.startswith(ICT))):
        chiavi = {k for k in set(b) | set(d) if k[0] in ent_comuni and filtro(k[1])}
        m = collections.Counter(); diffs = []; preg = collections.defaultdict(collections.Counter)
        for k in chiavi:
            vb, vd = b.get(k), d.get(k); g = preg[reg_b[k[0]]]
            if vb is None: m["solo_diretto"] += 1; m["euro_solo_diretto"] += vd; continue
            if vd is None: m["solo_bdap"] += 1; m["euro_solo_bdap"] += vb; continue
            m["euro_bdap"] += vb; m["euro_diretto"] += vd; g["euro_bdap"] += vb; g["euro_diretto"] += vd; g["coppie"] += 1
            if abs(vb - vd) <= 1: m["uguali"] += 1; g["uguali"] += 1
            else: m["diverse"] += 1; m["euro_diff_assoluta"] += abs(vb - vd); diffs.append((abs(vb - vd), k, vb, vd))
        diffs.sort(reverse=True)
        out[nome] = {kk: round(v) for kk, v in m.items()} | {"coppie": len(chiavi),
            "quota_uguali_su_entrambe": round(m["uguali"] / max(1, m["uguali"] + m["diverse"]), 4),
            "per_regione": {r: {kk: round(v) for kk, v in g.items()} | {"quota_uguali": round(g["uguali"] / max(1, g["coppie"]), 4)}
                            for r, g in sorted(preg.items())},
            "esempi_diverse": [{"ente": list(k[0]), "codice": k[1], "bdap": round(vb, 2), "diretto": round(vd, 2)}
                               for _, k, vb, vd in diffs[:15]]}
    o = R / f"esiti/{datetime.date.today().isoformat()}/siope"; os.makedirs(o, exist_ok=True)
    json.dump(out, open(o / f"bdap-vs-diretto-{ANNO}.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    s = {k: out[k] for k in ("enti",)} | {"ultimo_mese": {k: v for k, v in out["ultimo_mese"].items() if k != "per_regione"}}
    s |= {n: {k: v for k, v in out[n].items() if k not in ("per_regione", "esempi_diverse")} for n in ("tutti", "ict")}
    print(json.dumps(s, indent=1, ensure_ascii=False)[:6000])


if __name__ == "__main__":
    main()
