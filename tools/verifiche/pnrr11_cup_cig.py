"""Verifica «PNRR 1.1: CUP → CIG» (#66): collega i CUP finanziati dai decreti PNRR 1.1 (pnrr11_decreti.py) ai CIG
tramite il dataset ANAC «cup» (coppie CIG-CUP, nel mirror) e al loro strato nell'imbuto (lavoro/imbuto/ict.csv,
imbuto-0.3.1). Confronta l'importo finanziato con l'importo dei CIG collegati, per vedere se il contratto PSN
dell'ente supera il contributo forfettario.

Uso:
  python tools/verifiche/pnrr11_cup_cig.py             # da un clone: legge esiti/2026-11-06/pnrr11/cup-cig.csv
  python tools/verifiche/pnrr11_cup_cig.py --rigenera  # SUL SERVER: rilegge il dataset cup del mirror e ict.csv
"""
import csv, collections, glob, hashlib, io, json, os, sys, zipfile

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.normpath(os.path.join(QUI, "..", ".."))
E = os.path.join(RADICE, "esiti/2026-11-06/pnrr11")
OUT = os.path.join(E, "cup-cig.csv")
ZIP = os.path.join(RADICE, "archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/cup/filesystem/cup_csv.zip")
ICT = os.path.join(RADICE, "lavoro/imbuto/ict.csv")


def rigenera():
    F = collections.defaultdict(float); ente = {}
    for r in csv.DictReader(open(os.path.join(E, "finanziati.csv"), encoding="utf-8")):
        if float(r["importo_1_1"]) > 0:      # come pnrr11_decreti.py: un CUP in più finestre vale una volta (l'ultima)
            F[r["cup"]] = float(r["importo_1_1"]); ente[r["cup"]] = r["ente"]
    pref = {c[:13]: c for c in F}            # CUP troncati da pdftotext (13-14 caratteri): confronto sul prefisso
    z = zipfile.ZipFile(ZIP); m = z.namelist()[0]; cc = collections.defaultdict(set)
    for r in csv.DictReader(io.TextIOWrapper(z.open(m), encoding="utf-8-sig", errors="replace"), delimiter=";"):
        c = r["CUP"]
        k = c if c in F else pref.get(c[:13])
        if k: cc[k].add(r["CIG"])
    tutti = set().union(*cc.values()) if cc else set()
    info = {}
    for r in csv.DictReader(open(ICT, encoding="utf-8")):
        if r["cig"] in tutti: info[r["cig"]] = (r["anno"], r["strato"], r["sottoclasse"], float(r["importo"] or 0))
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["cup", "ente", "finanziato_1_1", "cig", "anno", "strato", "sottoclasse", "importo_cig"])
        for c in sorted(F):
            for g in sorted(cc.get(c, [""])):
                a = info.get(g, ("", "fuori-ict-csv" if g else "", "", ""))
                w.writerow([c, ente[c], round(F[c], 2), g, *a])
    json.dump({"zip": os.path.relpath(ZIP, RADICE), "sha256_zip": hashlib.sha256(open(ZIP, "rb").read()).hexdigest(),
               "sha256_ict": hashlib.sha256(open(ICT, "rb").read()).hexdigest()}, open(os.path.join(E, "cup-cig-fonti.json"), "w"), indent=1)
    print("scritto", OUT)


def main():
    if "--rigenera" in sys.argv: return rigenera()
    R = list(csv.DictReader(open(OUT, encoding="utf-8")))
    cup = collections.defaultdict(list)
    for r in R: cup[r["cup"]].append(r)
    con = {c: v for c, v in cup.items() if v[0]["cig"]}
    fin = lambda vv: sum(float(v[0]["finanziato_1_1"]) for v in vv)
    psn = {c: v for c, v in con.items() if any(x["sottoclasse"] == "psn-servizio-da-determinare" for x in v)}
    imp_psn = sum(float(x["importo_cig"]) for v in psn.values() for x in v if x["sottoclasse"] == "psn-servizio-da-determinare")
    T = {"cup": len(cup), "finanziato_totale": round(fin(cup.values())),
         "cup_con_cig": len(con), "finanziato_con_cig": round(fin(con.values())), "cig_collegati": sum(len(v) for v in con.values()),
         "per_strato": collections.Counter(x["strato"] or "senza-cig" for v in cup.values() for x in v),
         "cup_con_cig_psn": len(psn), "finanziato_cup_psn": round(fin(psn.values())), "importo_cig_psn_collegati": round(imp_psn)}
    print(json.dumps(T, ensure_ascii=False, indent=1))
    if "--json" in sys.argv: json.dump(T, open(sys.argv[sys.argv.index("--json") + 1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
