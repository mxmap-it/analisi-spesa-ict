"""#27 FTS -> P.IVA: quali aggiudicatari ANAC dei contratti cloud (rivenditori e produttori, esiti/*/rivenditori/rivenditori-cf.csv)
ricevono anche fondi UE in gestione diretta (Financial Transparency System 2007-2025, archiviato).
L'xlsx si legge con la sola libreria standard (zip + XML in streaming): nessuna dipendenza nuova.
Chiave: partita IVA italiana a 11 cifre (FTS: colonna con «VAT»; si toglie il prefisso IT). Si conta per anno l'importo FTS
dei beneficiari italiani e di quelli che compaiono fra gli aggiudicatari cloud.

Uso (server): nice .venv/bin/python tools/verifiche/fts_piva.py -> esiti/<oggi>/mirror/fts-piva.json"""
import csv, glob, json, os, re, zipfile, datetime, collections
import xml.etree.ElementTree as ET
from pathlib import Path

R = Path(__file__).resolve().parents[2]
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def righe_xlsx(path):
    z = zipfile.ZipFile(path)
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        for _, el in ET.iterparse(z.open("xl/sharedStrings.xml")):
            if el.tag == NS + "si":
                ss.append("".join(t.text or "" for t in el.iter(NS + "t"))); el.clear()
    foglio = sorted(n for n in z.namelist() if n.startswith("xl/worksheets/sheet"))[0]
    for _, el in ET.iterparse(z.open(foglio)):
        if el.tag == NS + "row":
            r = {}
            for c in el.iter(NS + "c"):
                col = re.sub(r"\d", "", c.get("r")); v = c.find(NS + "v")
                if v is None:
                    t = c.find(NS + "is"); val = "".join(x.text or "" for x in t.iter(NS + "t")) if t is not None else ""
                else:
                    val = ss[int(v.text)] if c.get("t") == "s" else v.text
                r[col] = val
            yield r; el.clear()


def main():
    cf = {}
    f = sorted(glob.glob(str(R / "esiti/*/rivenditori/rivenditori-cf.csv")))[-1]
    for r in csv.DictReader(open(f, encoding="utf-8")):
        if re.fullmatch(r"\d{11}", r["cf"]): cf[r["cf"]] = r
    out = {"ingresso_aggiudicatari": f, "aggiudicatari_cloud_con_piva": len(cf), "anni": {}, "trovati": collections.Counter()}
    trovati_eur = collections.Counter(); nomi = {}
    for x in sorted(glob.glob(str(R / "archivio/mirror/ec.europa.eu/budget/financial-transparency-system/download/*_FTS_dataset_en.xlsx"))):
        anno = os.path.basename(x)[:4]; intest = None; it = 0; it_eur = 0.0; hit = collections.Counter(); hit_eur = 0.0
        for r in righe_xlsx(x):
            if intest is None:
                if any("VAT" in (v or "").upper() for v in r.values()):
                    intest = {k: (v or "").strip() for k, v in r.items()}
                    cvat = next(k for k, v in intest.items() if "VAT" in v.upper())
                    cpaese = next((k for k, v in intest.items() if "country" in v.lower() and "beneficiar" in v.lower()), None)
                    cimp = next((k for k, v in intest.items() if "amount" in v.lower()), None)
                    cnome = next((k for k, v in intest.items() if "name of beneficiary" in v.lower()), None)
                continue
            vat = re.sub(r"\W", "", (r.get(cvat) or "").upper())
            paese = (r.get(cpaese) or "").upper() if cpaese else ""
            if not (vat.startswith("IT") or paese.startswith("ITA") or paese == "IT"): continue
            try: imp = float(r.get(cimp) or 0)
            except ValueError: imp = 0.0
            it += 1; it_eur += imp
            p = vat[2:] if vat.startswith("IT") else vat
            if p in cf:
                hit[p] += 1; hit_eur += imp; trovati_eur[p] += imp; nomi[p] = cf[p]["denominazione"]
        out["anni"][anno] = {"intestazione_trovata": intest is not None, "righe_it": it, "importo_it": round(it_eur),
                             "righe_aggiudicatari_cloud": sum(hit.values()), "aggiudicatari_cloud_distinti": len(hit), "importo_aggiudicatari_cloud": round(hit_eur)}
        print(anno, out["anni"][anno], flush=True)
    out["trovati"] = [{"piva": p, "denominazione": nomi[p], "importo_fts_2007_2025": round(v)} for p, v in trovati_eur.most_common(30)]
    out["aggiudicatari_cloud_in_fts"] = len(trovati_eur)
    o = R / f"esiti/{datetime.date.today().isoformat()}/mirror"; os.makedirs(o, exist_ok=True)
    json.dump(out, open(o / "fts-piva.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(out["trovati"][:15], ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
