"""Verifica «quadro economico e SAL» (#66, rendiconto 0.4): per i 2.130 CIG sopra 50 M€ dal 2024 legge dal mirror ANAC
i dataset quadro-economico (ultimo evento: base d asta, variante, consuntivo) e stati-avanzamento (somma degli importi SAL).
Seconda fonte ANAC indipendente dall importo del lotto: conferma gli errori d importo e dà un valore per gli incerti.
Uscita versionata: esiti/2026-11-06/imbuto/anac-qe-sal.csv (+ -fonti.json). Uso (SUL SERVER): python tools/verifiche/imbuto_qe_sal.py"""
import zipfile,glob,io,csv,collections,json
D="archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/"
T={r["cig"]:r for r in csv.DictReader(open("esiti/2026-11-06/imbuto/tetti-cig.csv"))}
def rows(ds):
  z=sorted(glob.glob(D+ds+"/filesystem/*csv*.zip"))[-1]; zf=zipfile.ZipFile(z); m=[n for n in zf.namelist() if n.endswith(".csv")][0]
  return z, csv.DictReader(io.TextIOWrapper(zf.open(m),encoding="utf-8-sig",errors="replace"),delimiter=";")
def f(x):
  try: return float((x or "0").replace(",", "."))
  except ValueError: return 0.0
qe=collections.defaultdict(list); sal=collections.defaultdict(float); fonti={}
z,R=rows("quadro-economico"); fonti["quadro-economico"]=z
for r in R:
  if r["cig"] in T: qe[r["cig"]].append((r["data"], f(r["importo_forniture"])+f(r["importo_servizi"])+f(r["importo_lavori"])+f(r["importo_progettazione"])+f(r["importo_sicurezza"]), r["descrizione_evento"]))
z,R=rows("stati-avanzamento"); fonti["stati-avanzamento"]=z
for r in R:
  if r["cig"] in T: sal[r["cig"]]+=f(r["importo_sal"])
w=csv.writer(open("esiti/2026-11-06/imbuto/anac-qe-sal.csv","w")); w.writerow(["cig","qe_ultimo_importo","qe_ultimo_evento","qe_data","n_eventi_qe","sal_cumulato"])
for c in sorted(set(qe)|set(sal)):
  u=sorted(qe.get(c,[("",0,"")]))[-1]
  w.writerow([c,round(u[1],2),u[2],u[0],len(qe.get(c,[])),round(sal.get(c,0),2)])
json.dump(fonti,open("esiti/2026-11-06/imbuto/anac-qe-sal-fonti.json","w"),indent=1)
cl=collections.Counter((T[c]["classe"], T[c]["strato"]!="S1-escluso-non-ict") for c in set(qe)|set(sal))
print(len(qe),len(sal),cl)
