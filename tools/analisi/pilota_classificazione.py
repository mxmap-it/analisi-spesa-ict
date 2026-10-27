"""Pilota #48: quanta spesa ICT si classifica dalla sola descrizione (lente prodotto).
Uso: python tools/analisi/pilota_classificazione.py <anno>  -> lavoro/pilota/<anno>.json + campioni
Regole a priorità: la prima classe che corrisponde vince. Pilota, non misura definitiva."""
import csv, glob, io, json, re, sys, zipfile, collections, random, os
ANNO = sys.argv[1] if len(sys.argv) > 1 else "2025"
D = "archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/"
# perimetro ICT provvisorio per CPV (da documentare in #44)
CPV_ICT = re.compile(r"^(48|72|302|3223|3224|3225|3226|50312|50320|51611|64216|64222|79342)")
CLASSI = [  # (classe, gruppo, regex)
 ("Microsoft cloud", "bigtech_cloud", r"microsoft\s*365|office\s*365|\bo365\b|\bm365\b|azure|exchange\s+online|sharepoint\s+online|dynamics\s*365"),
 ("AWS", "bigtech_cloud", r"\baws\b|amazon\s+web\s+services"),
 ("Google cloud", "bigtech_cloud", r"google\s+workspace|g\s*suite|google\s+cloud|\bgcp\b|google\s+for\s+education"),
 ("Oracle cloud", "bigtech_cloud", r"oracle\s+cloud|\boci\b"),
 ("Altri SaaS USA", "bigtech_cloud", r"salesforce|servicenow|zoom\b|webex|adobe\s+(creative|acrobat|sign)|workday"),
 ("PSN", "psn", r"polo\s+strategico|\bpsn\b"),
 ("Operatori cloud IT/UE", "cloud_it_ue", r"aruba|seeweb|register\.it|\bovh|wiit|retelit|irideos|elmec|enter\s*cloud|cloud\s+italia"),
 ("Licenze bigtech on-prem", "bigtech_licenze", r"licenz\w*\s+(d\w\s+)?(microsoft|windows|oracle|vmware)|windows\s+server|sql\s+server|vmware|oracle\s+database|\bcal\b\s+microsoft"),
 ("Cloud generico", "cloud_generico", r"\bcloud\b|\bsaas\b|\biaas\b|\bpaas\b|in\s+hosting|\bhosting\b|software\s+as\s+a\s+service"),
 ("Infrastruttura propria", "infra_propria", r"\bserver\b|storage|\bnas\b|\bsan\b|\brack\b|data\s*cent|sala\s+(server|macchine|ced)|\bced\b|virtualizzazion|hyper.?converg|iperconverg|backup\s+appliance|\bups\b"),
]
RX = [(c, g, re.compile(r, re.I)) for c, g, r in CLASSI]
tot = collections.Counter(); val = collections.Counter(); per_classe = collections.defaultdict(list)
n_ict = 0; v_ict = 0.0
for z in sorted(glob.glob(D + f"cig-{ANNO}/filesystem/cig_csv_*.zip")):
    with zipfile.ZipFile(z) as zf:
        m = next(i for i in zf.namelist() if i.endswith(".csv"))
        for r in csv.DictReader(io.TextIOWrapper(zf.open(m), encoding="utf-8-sig", errors="replace"), delimiter=";"):
            if not CPV_ICT.match(r.get("cod_cpv") or ""): continue
            try: imp = float((r.get("importo_lotto") or "0").replace(",", "."))
            except ValueError: imp = 0.0
            n_ict += 1; v_ict += imp
            testo = (r.get("oggetto_lotto") or "") + " " + (r.get("oggetto_gara") or "")
            cl = next(((c, g) for c, g, rx in RX if rx.search(testo)), ("Non classificato", "non_classificato"))
            tot[cl] += 1; val[cl] += imp
            if len(per_classe[cl[0]]) < 2000: per_classe[cl[0]].append((r["cig"], r.get("cod_cpv"), imp, testo[:200]))
os.makedirs("lavoro/pilota", exist_ok=True)
random.seed(42)
camp = {c: random.sample(v, min(50, len(v))) for c, v in per_classe.items()}
out = {"anno": ANNO, "cig_ict": n_ict, "importo_ict": round(v_ict),
       "classi": [{"classe": c, "gruppo": g, "cig": n, "quota_cig": round(n / n_ict * 100, 2), "importo": round(val[(c, g)]), "quota_importo": round(val[(c, g)] / v_ict * 100, 2)} for (c, g), n in tot.most_common()]}
json.dump(out, open(f"lavoro/pilota/{ANNO}.json", "w"), indent=1, ensure_ascii=False)
json.dump(camp, open(f"lavoro/pilota/{ANNO}-campioni.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
