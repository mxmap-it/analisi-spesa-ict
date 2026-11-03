import sys, csv, glob, os, zipfile, io
sys.path.insert(0, "tools/analisi")
from attribuisci_provider import D
T = {"8335254532","97431204F9","B1D4011AB2","9660108D4B"}
out = csv.writer(open("lavoro/convenzioni55/attuativi.csv","w",newline="",encoding="utf-8"))
out.writerow(["fonte","cig","cig_aq","stato_padre_o_figlio","oggetto_lotto","importo_lotto","data_pubblicazione","anno","sa","cpv","oggetto_gara","importo_gara","stato"])
files = sorted(glob.glob(D+"cig-*/filesystem/cig_csv_*.zip"))+sorted(glob.glob(D+"cig/filesystem/*-cig_csv.zip"))
for z in files:
    zf = zipfile.ZipFile(z); m = next(i for i in zf.namelist() if i.endswith(".csv"))
    for r in csv.DictReader(io.TextIOWrapper(zf.open(m), encoding="utf-8-sig", errors="replace"), delimiter=";"):
        c, a = r["cig"], r["cig_accordo_quadro"]
        if c in T or a in T:
            out.writerow([os.path.basename(z), c, a, "padre" if c in T else "figlio", r["oggetto_lotto"], r["importo_lotto"], r["data_pubblicazione"], r["anno_pubblicazione"], r["denominazione_amministrazione_appaltante"], r["cod_cpv"], r["oggetto_gara"], r["importo_complessivo_gara"], r["stato"]])
    print(z, flush=True)
