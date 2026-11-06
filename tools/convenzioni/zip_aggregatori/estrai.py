import csv,zipfile,hashlib,subprocess,re,json,os,sys
A="/home/mxmap.it/analisi-spesa-ict/archivio/blobs/sha256/"
OUT="/home/mxmap.it/analisi-spesa-ict/lavoro/convenzioni/aggregatori/t62_testi/"
SKIP=re.compile(r"(/$|desktop\.ini|DGUE|Domanda|Dich|Patto|DPA|VPN|Modello A|Modulo|DUVRI|Clausole|ClausoleVess|titolare|Collaudo|Rischi|delega|Schema_relazione|PA-4|PA-90|Linee guida|Check Compliance|Allegato A\.1|A\.2 - |\.xml$|Profili)",re.I)
idx=[];visti=set()
for r in csv.DictReader(open("aggregatori-2026-11-07.csv",encoding="utf-8")):
  h=r["sha256"]
  if not h or not (".zip" in (r["documento"]+r["url_documento"]).lower() or "zip" in r["tipo_documento"]): continue
  z=zipfile.ZipFile(A+h[:2]+"/"+h[2:4]+"/"+h)
  for n in z.namelist():
    if n.endswith("/"): continue
    b=z.read(n); s=hashlib.sha256(b).hexdigest()
    rel=not SKIP.search(n)
    idx.append(dict(iniziativa=r["iniziativa"],zip=r["documento"],sha256_zip=h,file_interno=n,sha256_file=s,rilevante=rel))
    if not rel or s in visti: continue
    visti.add(s); f=OUT+s[:16]; open(f+".bin","wb").write(b); t=""
    low=n.lower()
    try:
      if low.endswith(".p7m"):
        subprocess.run(["openssl","cms","-verify","-noverify","-inform","DER","-in",f+".bin","-out",f+".pdf"],capture_output=True); 
        t=subprocess.run(["pdftotext","-layout",f+".pdf","-"],capture_output=True,text=True).stdout
      elif low.endswith(".pdf"): t=subprocess.run(["pdftotext","-layout",f+".bin","-"],capture_output=True,text=True).stdout
      elif low.endswith(".xlsx"):
        import openpyxl; wb=openpyxl.load_workbook(f+".bin",read_only=True,data_only=True)
        for ws in wb.worksheets:
          t+=f"=== foglio {ws.title}\n"
          for row in ws.iter_rows(values_only=True):
            v=[str(c) for c in row if c is not None]
            if v: t+=" | ".join(v)+"\n"
      elif low.endswith(".docx"):
        import docx; t="\n".join(p.text for p in docx.Document(f+".bin").paragraphs)
      else: t=subprocess.run(["strings","-n","6",f+".bin"],capture_output=True,text=True).stdout
    except Exception as e: t="ERRORE "+repr(e)
    open(f+".txt","w",encoding="utf-8").write(t)
json.dump(idx,open("zip_indice.json","w",encoding="utf-8"),ensure_ascii=False,indent=0)
print(len(idx),sum(i["rilevante"] for i in idx),len(visti))
