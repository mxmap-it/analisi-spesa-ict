import zipfile,glob,io,csv,collections,json
D="archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/"
out={}
for y in (2022,2023,2024,2025):
  c=collections.Counter(); e=collections.Counter()
  for z in glob.glob(D+f"smartcig-{y}/filesystem/*.zip"):
    zf=zipfile.ZipFile(z)
    for r in csv.DictReader(io.TextIOWrapper(zf.open(zf.namelist()[0]),encoding="utf-8-sig",errors="replace"),delimiter=";"):
      k=(r.get("tipo_fattispecie_contrattuale") or "")[:70]+" / "+(r.get("tipo_scelta_contraente") or "")[:40]
      c[k]+=1
      try: e[k]+=float(r.get("importo_lotto") or 0)
      except: pass
  out[y]=[(k,c[k],round(e[k]/1e9,2)) for k in sorted(c,key=lambda k:-e[k])[:8]]
json.dump(out,open("lavoro/smartcig_profilo.json","w"),indent=1,ensure_ascii=False)
