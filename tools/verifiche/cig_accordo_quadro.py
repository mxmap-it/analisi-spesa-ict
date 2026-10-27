"""Verifica #50: il campo cig_accordo_quadro (CIG derivato -> CIG dell accordo quadro/convenzione) è presente e compilato?
Per anno: presenza della colonna, quota compilata, CIG il cui testo dichiara adesione ad AQ/convenzione ma con campo vuoto,
CIG con campo compilato che punta a un CIG inesistente nella base. Uso: python tools/verifiche/cig_accordo_quadro.py"""
import csv, glob, io, json, re, zipfile, collections
D = "archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/"
ADESIONE = re.compile(r"adesion\w*\s+(a(l|ll\W?)?\s*)?(accordo\s+quadro|\baq\b|convenzion)|\bin\s+adesione\b|ordinativo\s+di\s+fornitura|contratto\s+(esecutivo|attuativo|applicativo)|appalto\s+specifico", re.I)
CONSIP = re.compile(r"consip|accordo\s+quadro|\baq\b|convenzion", re.I)
anni = {}; tutti = set(); puntati = collections.Counter()
for d in sorted(glob.glob(D + "cig-20*")):
    anno = d[-4:]; s = collections.Counter(); col = None
    for z in sorted(glob.glob(d + "/filesystem/cig_csv_*.zip")):
        zf = zipfile.ZipFile(z)
        rd = csv.DictReader(io.TextIOWrapper(zf.open(zf.namelist()[0]), encoding="utf-8-sig", errors="replace"), delimiter=";")
        col = "cig_accordo_quadro" in (rd.fieldnames or [])
        for r in rd:
            s["cig"] += 1; tutti.add(r["cig"])
            aq = (r.get("cig_accordo_quadro") or "").strip()
            testo = (r.get("oggetto_lotto") or "") + " " + (r.get("oggetto_gara") or "")
            dich = bool(ADESIONE.search(testo))
            if aq: s["compilato"] += 1; puntati[aq] += 1
            if dich: s["dichiara_adesione"] += 1
            if dich and not aq: s["dichiara_adesione_campo_vuoto"] += 1
            if dich and aq: s["dichiara_adesione_campo_ok"] += 1
    anni[anno] = dict(s, colonna_presente=col)
orfani = sum(1 for p in puntati if p not in tutti)
out = {"per_anno": anni, "cig_padre_distinti_puntati": len(puntati), "cig_padre_non_trovati_nella_base": orfani}
json.dump(out, open("lavoro/verifica_cig_accordo_quadro.json", "w"), indent=1)
print(json.dumps(out, indent=1))
