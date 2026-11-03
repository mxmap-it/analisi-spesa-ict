# L4 regola AT (#55): evidenza blocco (requests) + lettura con Chrome headless reale, >=5 s fra richieste.
# Uso: pw.py URL [regex] [--prova]  (--prova: registra anche la risposta a UA dichiarato e robots.txt)
import sys,time,re,json,hashlib,os,urllib.parse,requests
from playwright.sync_api import sync_playwright
UA_P="Mozilla/5.0 (compatible; analisi-spesa-ict; +https://analisi-spesa-ict.mxmap.it)"
UA_B="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36 (analisi-spesa-ict; +https://analisi-spesa-ict.mxmap.it)"
D=os.path.expanduser("~/analisi-spesa-ict/lavoro/ea-campione/pw"); os.makedirs(D,exist_ok=True)
args=[a for a in sys.argv[1:] if not a.startswith("--")]; u=args[0]
pat=re.compile(args[1] if len(args)>1 else "(?i)microsoft|licenz|enterprise|365|EA8|EA9",re.I)
h=urllib.parse.urlparse(u).netloc; ts=time.strftime("%Y%m%dT%H%M%S")
def save(name,b):
    p=f"{D}/{h}_{ts}_{name}"; open(p,"wb").write(b); return p,hashlib.sha256(b).hexdigest()
ev={"url":u,"data":time.strftime("%FT%T%z")}
if "--prova" in sys.argv:
    for nm,url,ua in [("robots",f"https://{h}/robots.txt",UA_P),("ua_progetto",u,UA_P)]:
        try:
            r=requests.get(url,headers={"User-Agent":ua},timeout=30)
            p,s=save(nm+".body",r.content); ev[nm]={"url":url,"http":r.status_code,"headers":dict(r.headers),"file":p,"sha256":s}
        except Exception as e: ev[nm]={"errore":str(e)}
        time.sleep(5)
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path="/usr/bin/google-chrome",headless=True)
    c=b.new_context(user_agent=UA_B,locale="it-IT"); pg=c.new_page()
    try:
        r=pg.goto(u,wait_until="networkidle",timeout=60000); time.sleep(5)
        html=pg.content().encode(); p,s=save("browser.html",html)
        ev["browser"]={"http":r.status if r else None,"headers":r.headers if r else {},"url_finale":pg.url,"file":p,"sha256":s,"titolo":pg.title()}
        t=pg.inner_text("body")
        for a in pg.query_selector_all("a"):
            try: tx=(a.inner_text() or "").strip().replace("\n"," "); hr=a.get_attribute("href") or ""
            except: continue
            if pat.search(tx) or pat.search(hr): print("  L:",tx[:110],"->",urllib.parse.urljoin(pg.url,hr))
        for m in re.findall(r"[^\n]{0,140}(?:Microsoft|MICROSOFT|CIG)[^\n]{0,160}",t)[:20]: print("  T:",m)
        print("  TESTO:",re.sub(r"\s+"," ",t)[:600])
    except Exception as e: ev["browser"]={"errore":str(e)[:300]}
    b.close()
open(f"{D}/evidenze.jsonl","a").write(json.dumps(ev)+"\n")
print(json.dumps({k:(v if k!="browser" else {x:v.get(x) for x in ("http","url_finale","titolo","errore","sha256")}) for k,v in ev.items() if k not in("robots","ua_progetto")}))
for k in("robots","ua_progetto"):
    if k in ev: print(k,ev[k].get("http"),ev[k].get("errore",""),{x:y for x,y in ev[k].get("headers",{}).items() if x.lower() in("server","content-type","x-cdn","cf-ray","x-azure-ref")})
