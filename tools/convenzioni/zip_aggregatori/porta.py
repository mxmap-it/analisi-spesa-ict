import csv,json,glob,os,hashlib,sys
from datetime import datetime,timezone
from pathlib import Path
sys.path.insert(0,os.path.dirname(__file__))
import archivia as A
B='/home/mxmap.it/analisi-spesa-ict/lavoro/convenzioni/aggregatori/'
pag={}
for f in ['06','07']:
  for r in csv.DictReader(open(f'aggregatori-2026-11-{f}.csv',encoding='utf-8')):
    if r['sha256']: pag.setdefault(r['sha256'],r['url_pagina'])
fatti=set()
if A.MANIFEST.exists():
  for l in open(A.MANIFEST,encoding='utf-8'):
    if '"browser-headless"' in l: r=json.loads(l); fatti.add((r['sha256'],r['url']))
out=open('portati.tsv','a',encoding='utf-8')
for j in sorted(glob.glob(B+'**/_scaricati.json',recursive=True)):
  for e in json.load(open(j,encoding='utf-8')):
    if e.get('esito')!='ok': continue
    p=Path(os.path.dirname(j))/os.path.basename(e['file'])
    h=hashlib.sha256(p.read_bytes()).hexdigest()
    if h!=e['sha256']: print('SOVRASCRITTO',p,e['sha256']); continue
    url=pag[h]+'#'+e['nome']
    if (h,url) in fatti: continue
    nota='copia Chrome headless senza login'
    if 'access-code' in e.get('url',''): nota+='; URL monouso START: '+e['url']+'; allegato: '+';'.join(e.get('req',[]))
    else: nota+='; allegato Sintel scaricato con POST JSF dalla pagina'
    data=datetime.fromtimestamp(p.stat().st_mtime,timezone.utc).isoformat(timespec='seconds')
    rec=A.archivia_file(p,url,data,nota=nota); A.scrivi_manifest(rec)
    out.write('\t'.join([rec['esito'],h,url,str(p)])+'\n'); print(rec['esito'],h[:12],e['nome'])
