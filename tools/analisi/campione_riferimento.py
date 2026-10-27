"""Campione di riferimento per validare l'attribuzione del provider (metodo, sezione 'Come si verifica').
Strati: via x servizio x fascia di importo; seed fisso. Esce un CSV da annotare a mano con colonne vuote.
Uso: python tools/analisi/campione_riferimento.py 1000 -> lavoro/attribuzione/campione-riferimento.csv"""
import csv, random, sys, collections, glob
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
random.seed(20261027)
strati = collections.defaultdict(list)
for f in sorted(glob.glob("lavoro/attribuzione/*.csv")):
    if "campione" in f: continue
    for r in csv.DictReader(open(f, encoding="utf-8")):
        if r["e_padre"] == "1": continue
        imp = float(r["importo_lotto"] or 0)
        fascia = "<40k" if imp < 40000 else "<215k" if imp < 215000 else "<1M" if imp < 1e6 else ">=1M"
        via = r["via"]
        if via == "0-ict-non-cloud":
            strato = ("0-ict-non-cloud", "", fascia)  # serve a stimare il richiamo: cloud sfuggito
        else:
            strato = (via, r["servizio"], fascia)
        strati[strato].append(r)
quota = max(5, N // len(strati))
scelti = []
for s, rs in sorted(strati.items()):
    scelti += random.sample(rs, min(quota, len(rs)))
random.shuffle(scelti)
campi = ["cig", "cod_cpv", "importo_lotto", "stazione_appaltante", "aggiudicatari", "testo", "via", "provider", "servizio"]
with open("lavoro/attribuzione/campione-riferimento.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(campi + ["e_cloud (s/n)", "provider_corretto", "giurisdizione_corretta", "annotatore", "note"])
    for r in scelti:
        w.writerow([r[c] for c in campi] + ["", "", "", "", ""])
print(len(strati), "strati,", len(scelti), "contratti")
