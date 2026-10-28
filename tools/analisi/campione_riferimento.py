"""Campione di riferimento per validare l'attribuzione del provider (metodo, sezione 'Come si verifica').
Strati: via x servizio x fascia di importo; seed fisso. Esce un CSV da annotare a mano con colonne vuote.
Uso: python tools/analisi/campione_riferimento.py 1000 -> lavoro/attribuzione/campione-riferimento.csv"""
import csv, random, sys, collections, glob
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 20261027
NOME = sys.argv[3] if len(sys.argv) > 3 else "campione-riferimento"
random.seed(SEED)
strati = collections.defaultdict(list)
# il campione di misura esclude i contratti già visti nel campione di sviluppo
import os
# un contratto già visto da chi ha scritto le regole (qualunque campione pubblicato in report/metodo) non entra in una misura
visti = set()
for f in glob.glob("report/metodo/campione-*.csv"):
    visti |= {r["cig"] for r in csv.DictReader(open(f, encoding="utf-8"))}
for f in sorted(glob.glob("lavoro/attribuzione/*.csv")):
    if "campione" in f: continue
    for r in csv.DictReader(open(f, encoding="utf-8")):
        if r["e_padre"] == "1" or r["cig"] in visti: continue
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
with open("lavoro/attribuzione/" + NOME + ".csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(campi + ["e_cloud (s/n)", "provider_corretto", "giurisdizione_corretta", "annotatore", "note"])
    for r in scelti:
        w.writerow([r[c] for c in campi] + ["", "", "", "", ""])
# copia cieca per l'annotazione umana: senza le colonne prodotte dal classificatore, così l'annotatore non è ancorato
cieca = ["cig", "cod_cpv", "importo_lotto", "stazione_appaltante", "aggiudicatari", "testo"]
with open("lavoro/attribuzione/" + NOME + "-cieco.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(cieca + ["e_cloud (s/n)", "servizio (cloud/licenza/servizi-professionali/psn/in-house/altro)", "provider_prodotto", "giurisdizione (IT/UE/EXTRA-UE)", "annotatore", "note"])
    for r in scelti:
        w.writerow([r[c] for c in cieca] + ["", "", "", "", "", ""])
print(len(strati), "strati,", len(scelti), "contratti, esclusi", len(visti), "già visti")
