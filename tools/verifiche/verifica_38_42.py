# #38 copertura OCDS vs tabellari; #42 fornitori assenti nell OCDS: ci sono nei tabellari?
import ijson, zipfile, io, csv, glob, collections, json, re
D="archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/"
oc={}  # id_aggiudicazione -> (mese award, ha_fornitore)
date_strane=collections.Counter()
with open(D+"ocds/filesystem/bulk/2026/03.json","rb") as f:
    for r in ijson.items(f,"releases.item",use_float=True):
        if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ",str(r.get("date",""))): date_strane["release.date"]+=1
        for a in r.get("awards") or []:
            oc[str(a.get("id"))]=(str(a.get("date",""))[:7], bool(a.get("suppliers")))
def righe(ds):
    for z in sorted(glob.glob(D+ds+"/filesystem/*_csv.zip")):
        with zipfile.ZipFile(z) as zf:
            m=next(i for i in zf.namelist() if i.endswith(".csv"))
            for x in csv.DictReader(io.TextIOWrapper(zf.open(m),encoding="utf-8-sig",errors="replace"),delimiter=";"):
                yield z.rsplit("/",1)[1][:8],x
tab={}
for dl,x in righe("aggiudicazioni"): tab[x["id_aggiudicazione"]]=x["data_aggiudicazione_definitiva"][:7]
fornitori=set(x["id_aggiudicazione"] for _,x in righe("aggiudicatari"))
o={}
o["ocds_award"]=len(oc); o["ocds_award_con_fornitore"]=sum(v[1] for v in oc.values())
senza=[k for k,v in oc.items() if not v[1]]
o["ocds_senza_fornitore"]=len(senza)
o["ocds_senza_fornitore_presenti_nei_tabellari"]=sum(k in tab for k in senza)
o["ocds_senza_fornitore_con_aggiudicatario_nei_tabellari"]=sum(k in fornitori for k in senza)
o["ocds_award_presenti_nei_tabellari"]=sum(k in tab for k in oc)
for m in ("2026-02","2026-03","2026-04"):
    t={k for k,v in tab.items() if v==m}
    o[f"tabellari_aggiudicati_{m}"]=len(t)
    o[f"di_cui_in_ocds_{m}"]=sum(k in oc for k in t)
    o[f"ocds_award_data_{m}"]=sum(v[0]==m for v in oc.values())
o["delta_usati"]=sorted({dl for dl,_ in righe("aggiudicatari")})
o["release_date_malformate"]=date_strane["release.date"]
json.dump(o,open("lavoro/verifica_38_42.json","w"),indent=1); print(json.dumps(o,indent=1))
