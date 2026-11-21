"""Università statali e cloud per marchio, per anno (#83 voce D).

Ipotesi riferita (non verificata): le università spostano infrastrutture su AWS con i fondi PNRR. La si mette alla prova
con i CIG: spesa netta delle università (IndicePA categoria L17) per marchio e stato finale, anno per anno.
Ingressi: IndicePA enti.xlsx (L17 -> CF), lavoro/inhouse/cig-cf.csv.gz, lavoro/imbuto/stati-finali.csv.gz, lavoro/imbuto/ict.csv
Uscita: esiti/<giorno>/statistiche/universita-cloud.{csv,json}
Uso: python tools/verifiche/universita_cloud.py [giorno]
"""
import collections, csv, gzip, json, os, sys
import duckdb

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GIORNO = sys.argv[1] if len(sys.argv) > 1 else "2026-11-21"
IPA = os.path.join(R, "archivio/mirror/indicepa.gov.it/ipa-dati/dataset/5baa3eb8-266e-455a-8de8-b1f434c279b2/resource/d09adf99-dc10-4349-8c53-27b1e5aa97b6/download/enti.xlsx")
OUT = os.path.join(R, "esiti", GIORNO, "statistiche")
GRUPPI = [("Amazon", ("amazon", "aws")), ("Google", ("google",)), ("Microsoft", ("microsoft",)), ("Oracle", ("oracle",))]

c = duckdb.connect(); c.sql("INSTALL excel; LOAD excel")
uni = {cf.zfill(11) for (cf,) in c.sql(f"select Codice_fiscale_ente from read_xlsx('{IPA}', all_varchar=true) where Codice_Categoria='L17' and Codice_fiscale_ente is not null").fetchall()}
cig_uni = set()
with gzip.open(os.path.join(R, "lavoro/inhouse/cig-cf.csv.gz"), "rt", newline="") as f:
    for r in csv.DictReader(f):
        if r["cf_sa"] and r["cf_sa"].zfill(11) in uni:
            cig_uni.add(r["cig"])
csv.field_size_limit(10**9)
prov = {}
with open(os.path.join(R, "lavoro/imbuto/ict.csv"), newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["cig"] in cig_uni and r["provider"]:
            prov[r["cig"]] = r["provider"].lower()
T = collections.defaultdict(lambda: [0, 0.0])
with gzip.open(os.path.join(R, "lavoro/imbuto/stati-finali.csv.gz"), "rt", newline="") as f:
    for r in csv.DictReader(f):
        if r["cig"] not in cig_uni:
            continue
        p = prov.get(r["cig"], "")
        g = next((n for n, ks in GRUPPI if any(k in p for k in ks)), "altri marchi" if p else "senza marchio")
        k = (r["anno"], r["stato"], g)
        T[k][0] += 1; T[k][1] += float(r["euro_netti"] or 0)
os.makedirs(OUT, exist_ok=True)
righe = [{"anno": a, "stato": s, "marchio": g, "cig": n, "euro_netti": round(e, 2)} for (a, s, g), (n, e) in sorted(T.items())]
with open(os.path.join(OUT, "universita-cloud.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(righe[0])); w.writeheader(); w.writerows(righe)
cloud = collections.defaultdict(dict)
for (a, s, g), (n, e) in T.items():
    if s == "cloud-certo":
        cloud[g][a] = round(e / 1e6, 2)
out = {"versione": "0.1", "strumento": "tools/verifiche/universita_cloud.py", "giorno": GIORNO, "universita_L17": len(uni),
       "cig_delle_universita": len(cig_uni), "cloud_certo_milioni_per_anno": cloud}
json.dump(out, open(os.path.join(OUT, "universita-cloud.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
