"""#30 SIOPE via BDAP contro SIOPE diretto (www.siope.it, open data), anni 2024 e 2025, cinque regioni.

BDAP («<anno> - <regione> - SIOPE Movimenti cumulati mensili di Spesa», CKAN datastore/dump, cp1252): ente per nome,
provincia e comune ISTAT, codice gestionale «U1030219001», importo CUMULATO per mese. Si prende il cumulato del mese
più alto (dicembre) per ente x codice.
SIOPE diretto (SIOPE_USCITE.<anno>.zip: codice ente, anno, mese, codice gestionale «1.03.02.19.001», importo in
centesimi; SIOPE_ANAGRAFICHE.zip/ANAG_ENTI: codice, CF, nome, comune e provincia ISTAT): somma dei mesi per ente x codice.
Abbinamento degli enti: (provincia ISTAT, comune ISTAT, nome normalizzato), solo coppie univoche da entrambe le parti.
Codici: «U» + cifre senza punti su entrambi i lati.
Misure: enti abbinati e non; per le coppie ente x codice: uguali (|diff| <= 1 €), diverse, presenti da una parte sola;
totali; lo stesso per i codici ICT (U1030219 servizi informatici e TLC, U2020107 hardware, U2020301 software).

Per il 2025 si misura anche il troncamento riferito da AgID (#30): ultimo mese per ente nelle due fonti.

Uso (server): nice .venv/bin/python tools/verifiche/siope_bdap_vs_diretto.py [2024|2025] -> esiti/<oggi>/siope/bdap-vs-diretto-<anno>.json"""
import collections, csv, datetime, hashlib, io, json, os, re, sys, zipfile
from pathlib import Path

R = Path(__file__).resolve().parents[2]
ARC = Path(os.environ.get("ARCHIVIO_ROOT", R / "archivio"))
DUMP = ARC / "mirror/bdap-opendata.rgs.mef.gov.it/SpodCkanApi/api/3/datastore/dump"
SIO = ARC / "mirror/www.siope.it/documenti/siope2/open/last"
ANNO = int(sys.argv[1]) if len(sys.argv) > 1 else 2024
RISORSE = {2024: {"LAZIO": "7db1ef58-43c0-4f75-b6cc-b73f982c930c", "UMBRIA": "fb4ba0a9-3caa-4053-a594-3d4d2d5f003a",
                  "BASILICATA": "9fe0c5ec-ee29-464a-bfe5-2b7ae62ab800", "MOLISE": "2f93d1d1-2878-4060-9cf2-f322834c44ae",
                  "LIGURIA": "03686c85-97ad-4e3b-916b-cb771e5e08fc"},
           2025: {"LAZIO": "33d82c62-46d3-4194-9484-1fb710cfef88", "UMBRIA": "327259cc-9b32-4247-9611-3766815d8a58",
                  "BASILICATA": "a0987ac6-d2e4-4de3-b068-ffcfa553f731", "MOLISE": "fe81de16-1502-4e1f-b0ec-adecc324c1d7",
                  "LIGURIA": "afeb3b7f-b1c0-426c-b862-6f29af0a0358"}}
BDAP = RISORSE[ANNO]
ICT = ("U1030219", "U2020107", "U2020301")


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


def main():
    csv.field_size_limit(10 ** 8)
    ing = {}
    anag = zipfile.ZipFile(SIO / "SIOPE_ANAGRAFICHE.zip"); ing["SIOPE_ANAGRAFICHE.zip"] = sha(SIO / "SIOPE_ANAGRAFICHE.zip")
    nm = lambda p: next(i for i in anag.namelist() if i.startswith(p))
    reg = {r[3]: r[2] for r in csv.reader(io.TextIOWrapper(anag.open(nm("ANAG_REG_PROV")), encoding="utf-8-sig"))}
    ent_d = collections.defaultdict(list)  # (prov, com, nome) -> codici ente
    for r in csv.reader(io.TextIOWrapper(anag.open(nm("ANAG_ENTI")), encoding="utf-8-sig", errors="replace")):
        if reg.get(r[6]) in BDAP: ent_d[(r[6], r[5], norm(r[4]))].append(r[0])
    cod2key = {v[0]: k for k, v in ent_d.items() if len(v) == 1}
    # SIOPE diretto
    z = SIO / f"SIOPE_USCITE.{ANNO}.zip"; ing[z.name] = sha(z); zf = zipfile.ZipFile(z)
    d = collections.Counter(); mese_d = {}
    for r in csv.reader(io.TextIOWrapper(zf.open(zf.namelist()[0]), encoding="utf-8-sig", errors="replace")):
        k = cod2key.get(r[0])
        if k and r[1] == str(ANNO):
            d[(k, cod(r[3]))] += int(r[4] or 0) / 100; mese_d[k] = max(mese_d.get(k, ""), r[2])
    # BDAP
    b = {}; ent_b = collections.Counter(); bm = {}
    for regione, rid in BDAP.items():
        p = DUMP / f"{rid}.csv"; ing[f"bdap-{regione}"] = {"file": str(p.relative_to(ARC)), "sha256": sha(p)}
        for x in csv.DictReader(open(p, encoding="cp1252", newline=""), delimiter=";"):
            k = (x["Codice istat provincia"], x["Codice istat comune"], norm(x["Descrizione Ente BDAP"]))
            kk = (k, x["Codice Gestionale Enti Locali"].strip()); mese = x["Anno/Mese calendario"]
            ent_b[k] = max(ent_b[k], int(mese[-2:]))
            if kk not in bm or mese > bm[kk]: bm[kk] = mese; b[kk] = float(x["Importo cumulato"] or 0)
    eb = set(ent_b); ed = set(k for k in ent_d if len(ent_d[k]) == 1); ent_comuni = eb & ed
    out = {"versione": "siope-bdap-vs-diretto 0.1 (2026-11-09)", "anno": ANNO, "regioni": list(BDAP), "ingressi": ing,
           "enti": {"bdap": len(eb), "diretto_univoci": len(ed), "diretto_ambigui": sum(1 for v in ent_d.values() if len(v) > 1),
                    "abbinati": len(ent_comuni), "solo_bdap": len(eb - ed), "esempi_solo_bdap": sorted(eb - ed)[:20]}}
    # troncamento (#30, riferito da AgID per il 2025): ultimo mese presente in BDAP contro ultimo mese con movimenti nel diretto
    tr = collections.Counter(); tr_es = []
    for k in ent_comuni:
        mb, md = ent_b[k], int(mese_d.get(k) or 0)
        t = "uguale" if mb == md else "bdap_prima" if mb < md else "bdap_dopo"; tr[t] += 1
        if t == "bdap_prima": tr[f"bdap_prima_{'comuni' if k[2].startswith('COMUNE') else 'altri'}"] += 1
        if t == "bdap_prima" and len(tr_es) < 15: tr_es.append({"ente": list(k), "ultimo_mese_bdap": mb, "ultimo_mese_diretto": md})
    out["ultimo_mese"] = dict(tr) | {"distribuzione_bdap": dict(collections.Counter(ent_b[k] for k in ent_comuni)),
                                     "distribuzione_diretto": dict(collections.Counter(int(mese_d.get(k) or 0) for k in ent_comuni)), "esempi": tr_es}
    for nome, filtro in (("tutti", lambda c: True), ("ict", lambda c: c.startswith(ICT))):
        chiavi = {k for k in set(b) | set(d) if k[0] in ent_comuni and filtro(k[1])}
        m = collections.Counter(); diffs = []
        for k in chiavi:
            vb, vd = b.get(k), d.get(k)
            if vb is None: m["solo_diretto"] += 1; m["euro_solo_diretto"] += vd; continue
            if vd is None: m["solo_bdap"] += 1; m["euro_solo_bdap"] += vb; continue
            m["euro_bdap"] += vb; m["euro_diretto"] += vd
            if abs(vb - vd) <= 1: m["uguali"] += 1
            else: m["diverse"] += 1; m["euro_diff_assoluta"] += abs(vb - vd); diffs.append((abs(vb - vd), k, vb, vd))
        diffs.sort(reverse=True)
        out[nome] = {kk: round(v) for kk, v in m.items()} | {"coppie": len(chiavi), "esempi_diverse": [
            {"ente": list(k[0]), "codice": k[1], "bdap": round(vb, 2), "diretto": round(vd, 2)} for _, k, vb, vd in diffs[:15]]}
    o = R / f"esiti/{datetime.date.today().isoformat()}/siope"; os.makedirs(o, exist_ok=True)
    json.dump(out, open(o / f"bdap-vs-diretto-{ANNO}.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({k: out[k] for k in ("enti", "ultimo_mese", "tutti", "ict")}, indent=1, ensure_ascii=False)[:5000])


if __name__ == "__main__":
    main()
