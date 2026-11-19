#!/usr/bin/env python3
"""Controllo dei link interni e delle ancore del sito costruito (docs/), da eseguire dopo ogni build (AGENTS.md § 6).
Ignora i link esterni e gli URL costruiti dal JavaScript delle pagine (contengono ${ o '+).
Uso:  python3 tools/verifiche/link_sito.py   -> elenco dei link rotti; codice 1 se ce ne sono."""
import os,re,sys,html,collections
from urllib.parse import urlparse,unquote
D='docs';H='analisi-spesa-ict.mxmap.it'
ids={};pagine={}
for r,_,fs in os.walk(D):
  for f in fs:
    if f.endswith('.html'):
      p=os.path.join(r,f);t=open(p,encoding='utf-8',errors='replace').read();pagine[p]=t
      ids[p]=set(re.findall(r'\sid="?([^"\s>]+)',t))
def risolvi(src,u):
  pu=urlparse(u)
  if pu.scheme in('http','https'):
    if pu.netloc!=H: return None
    path=pu.path
  elif pu.scheme: return None
  else:
    path=pu.path
    if not path: return (src,pu.fragment)
    if not path.startswith('/'):
      path=os.path.normpath(os.path.join(os.path.dirname(src)[len(D):] or '/',path))
  path=unquote(path)
  f=D+path
  if os.path.isdir(f) or path.endswith('/'): f=os.path.join(f,'index.html')
  return (os.path.normpath(f),pu.fragment)
rotti=collections.defaultdict(set);anc=collections.defaultdict(set)
for p,t in pagine.items():
  for u in re.findall(r'(?:href|src)="?([^"\s>]+)',t):
    u=html.unescape(u)
    if u.startswith(('mailto:','javascript:','data:','#!')) or '${' in u or "'+" in u or '`' in u: continue
    x=risolvi(p,u)
    if not x: continue
    f,fr=x
    if not os.path.exists(f): rotti[u].add(p)
    elif fr and f in ids and fr not in ids[f] and unquote(fr) not in ids[f]: anc[u].add(p)
print('LINK ROTTI',len(rotti))
for u,ps in sorted(rotti.items()): print(' ',u,'<-',len(ps),sorted(ps)[:3])
print('ANCORE ROTTE',len(anc))
for u,ps in sorted(anc.items()): print(' ',u,'<-',len(ps),sorted(ps)[:2])
sys.exit(1 if rotti or anc else 0)
