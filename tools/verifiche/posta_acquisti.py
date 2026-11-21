"""Controprova mxmap.it × acquisti (#83 voce B): gli enti con la posta su Microsoft o Google comprano quei marchi?

Seconda via indipendente per la lente prodotto: la posta (MX/SPF/DKIM, scansione di mxmap.it) dice quale piattaforma
l'ente usa davvero; i CIG dicono che cosa compra. Se la lente prodotto funziona, gli enti con posta Microsoft devono
avere acquisti Microsoft più spesso degli altri enti (e lo stesso per Google).

Ingressi:
  archivio/mirror/raw.githubusercontent.com/mxmap-it/mxmap.it/main/data.json   scansione mxmap.it (provider di posta)
  archivio/mirror/indicepa.gov.it/.../enti.xlsx                                 codice IPA -> codice fiscale
  lavoro/inhouse/cig-cf.csv.gz                                                  CIG -> CF della stazione appaltante
  lavoro/imbuto/ict.csv                                                         CIG -> marchio (lente prodotto)
Finestra: CIG 2023-2026 (gli ultimi tre anni pieni più l'anno in corso).
Uscita: esiti/<giorno>/statistiche/posta-acquisti.json
Uso: python tools/verifiche/posta_acquisti.py [giorno]
"""
import collections, csv, gzip, json, os, sys
import duckdb

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GIORNO = sys.argv[1] if len(sys.argv) > 1 else "2026-11-21"
MX = os.path.join(R, "archivio/mirror/raw.githubusercontent.com/mxmap-it/mxmap.it/main/data.json")
IPA = os.path.join(R, "archivio/mirror/indicepa.gov.it/ipa-dati/dataset/5baa3eb8-266e-455a-8de8-b1f434c279b2/resource/d09adf99-dc10-4349-8c53-27b1e5aa97b6/download/enti.xlsx")
CIGCF = os.path.join(R, "lavoro/inhouse/cig-cf.csv.gz")
ICT = os.path.join(R, "lavoro/imbuto/ict.csv")
ANNI = {"2023", "2024", "2025", "2026"}
MARCHI = {"microsoft": "Microsoft", "google": "Google"}

d = json.load(open(MX))
m = d["municipalities"]
m = list(m.values()) if isinstance(m, dict) else m
posta = {r["bfs"].split("-")[-1].upper(): (r.get("provider") or "unknown") for r in m if r.get("bfs")}

c = duckdb.connect(); c.sql("INSTALL excel; LOAD excel")
ipa_cf = {k.upper(): v.zfill(11) for k, v in c.sql(f"select Codice_IPA, Codice_fiscale_ente from read_xlsx('{IPA}', all_varchar=true) where Codice_fiscale_ente is not null").fetchall()}
cf_posta = {}
for k, p in posta.items():
    if k in ipa_cf:
        cf_posta.setdefault(ipa_cf[k], p)

csv.field_size_limit(10**9)
marchio = {}
with open(ICT, newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["anno"] in ANNI and r["provider"]:
            q = r["provider"].lower()
            for k, v in MARCHI.items():
                if k in q:
                    marchio[r["cig"]] = v
comprato = collections.defaultdict(set)
with gzip.open(CIGCF, "rt", newline="") as f:
    for r in csv.DictReader(f):
        v = marchio.get(r["cig"])
        if v and r["cf_sa"]:
            comprato[r["cf_sa"].zfill(11)].add(v)

tab = {}
for gruppo_posta in ("microsoft", "google", "altro"):
    enti = [cf for cf, p in cf_posta.items() if (p if p in MARCHI else "altro") == gruppo_posta]
    tab[gruppo_posta] = {"enti": len(enti), **{f"con_acquisti_{v}": sum(v in comprato[cf] for cf in enti) for v in MARCHI.values()}}
    for v in MARCHI.values():
        tab[gruppo_posta][f"quota_{v}"] = round(100 * tab[gruppo_posta][f"con_acquisti_{v}"] / max(1, len(enti)), 1)
out = {"versione": "0.1", "strumento": "tools/verifiche/posta_acquisti.py", "giorno": GIORNO,
       "mxmap_generato": d.get("generated"), "enti_mxmap": len(posta), "enti_con_cf": len(cf_posta),
       "finestra_anni": sorted(ANNI), "per_provider_di_posta": tab}
os.makedirs(os.path.join(R, "esiti", GIORNO, "statistiche"), exist_ok=True)
json.dump(out, open(os.path.join(R, "esiti", GIORNO, "statistiche", "posta-acquisti.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
