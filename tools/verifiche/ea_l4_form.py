# Form ASP.NET con Chrome headless (#55). Uso: pwform.py URL "sel=valore;sel2=valore" SUBMIT_SEL [regex]
import sys,time,re,os,hashlib,urllib.parse
from playwright.sync_api import sync_playwright
UA_B="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36 (analisi-spesa-ict; +https://analisi-spesa-ict.mxmap.it)"
u,fill,sub=sys.argv[1:4]; pat=re.compile(sys.argv[4] if len(sys.argv)>4 else "(?i)microsoft")
D=os.path.expanduser("~/analisi-spesa-ict/lavoro/ea-campione/pw")
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path="/usr/bin/google-chrome",headless=True); pg=b.new_context(user_agent=UA_B,locale="it-IT").new_page()
    pg.goto(u,wait_until="networkidle",timeout=60000); time.sleep(5)
    for kv in fill.split(";"):
        if kv: s,v=kv.split("=",1); pg.fill(s,v)
    pg.click(sub); pg.wait_for_load_state("networkidle",timeout=90000); time.sleep(5)
    h=pg.content(); p=f"{D}/{urllib.parse.urlparse(u).netloc}_{time.strftime('%Y%m%dT%H%M%S')}_form.html"; open(p,"w").write(h)
    print("FILE",p,hashlib.sha256(h.encode()).hexdigest())
    t=pg.inner_text("body")
    for l in t.splitlines():
        if pat.search(l): print(" T:",l.strip()[:300])
    for a in pg.query_selector_all("a"):
        hr=a.get_attribute("href") or ""; tx=(a.inner_text() or "").strip()
        if pat.search(tx) or re.search(r"(?i)\.pdf|allegat|download|getfile",hr): print(" L:",tx[:100],"->",urllib.parse.urljoin(pg.url,hr)[:250])
    b.close()
