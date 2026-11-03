import csv, collections, re, json, statistics
rows=list(csv.DictReader(open("lavoro/convenzioni55/attuativi.csv",encoding="utf-8")))
last={}
for r in rows: last[r["cig"]]=r
MAX={"8335254532":280e6,"97431204F9":430e6,"B1D4011AB2":537.5e6,"9660108D4B":40e6}
CL=[("SaaS (M365/O365/Dynamics/posta)",r"\b[mo]\s?365\b|microsoft\s*365|office\s*365|\be[35]\b|\bf[13]\b|exchange online|teams|dynamics|d365|posta elettronica|power ?bi|intune|copilot"),
("Azure / consumo cloud",r"azure|\boci\b|oracle cloud|cloud oracle|consumo"),
("On-premise esplicito",r"windows\s*server|sql\s*server|\bcal\b|system center|office (pro|professional|standard|20\d\d)|\bcore\b|server|database|weblogic|processor|enterprise edition|exadata|named user|java|mysql|stream analytics|bpm|perpetu"),
("Software Assurance / rinnovo / supporto",r"software assurance|\bSA\b|rinnovo|manutenzione|supporto|assistenza"),]
def imp(r):
    try: return float(r["importo_lotto"].replace(",","."))
    except: return 0.0
res={}
for aq,mx in MAX.items():
    f=[r for r in last.values() if r["cig_aq"]==aq and r["cig"]!=aq]
    anom=[r for r in f if imp(r)>=0.2*mx or imp(r)>=100e6]
    ok=[r for r in f if r not in anom]
    cls=collections.defaultdict(lambda:[0,0.0]); peranno=collections.defaultdict(lambda:[0,0.0])
    for r in ok:
        t=(r["oggetto_lotto"]+" | "+r["oggetto_gara"])
        c=next((n for n,p in CL if re.search(p,t,re.I)),"Generico (solo licenze/EA)")
        cls[c][0]+=1; cls[c][1]+=imp(r)
        a=r["anno"]; peranno[a][0]+=1; peranno[a][1]+=imp(r)
    v=[imp(r) for r in ok]
    res[aq]=dict(n=len(f),n_anom=len(anom),somma_anom=round(sum(imp(r) for r in anom)),somma_ok=round(sum(v)),mediana=round(statistics.median(v)) if v else 0,
      zero=sum(1 for x in v if x==0),
      anomali=[(r["cig"],round(imp(r)),r["anno"],r["sa"][:45],r["oggetto_lotto"][:70]) for r in sorted(anom,key=imp,reverse=True)],
      peranno={k:[n,round(s)] for k,(n,s) in sorted(peranno.items())},
      classi={k:[n,round(s)] for k,(n,s) in sorted(cls.items(),key=lambda x:-x[1][1])})
json.dump(res,open("lavoro/convenzioni55/riepilogo2.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(json.dumps(res,ensure_ascii=False))
