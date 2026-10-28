"""Controllo di sviluppo delle regole v3 sulle 437 righe annotate della misura v2 (report/metodo/campione-misura-2026-10-27.csv).
Non è una misura: le regole v3 sono state scritte guardando questi errori. Dice solo se ogni classe di errore è stata chiusa
e se la v3 ha rotto righe che la v2 attribuiva bene. La misura v3 si fa su un campione nuovo (campione_riferimento.py).
Uso: python tools/analisi/sviluppo_v3.py  (dopo attribuisci_provider.py 2024 2025 delta)"""
import ast, csv, glob, json

# le annotazioni v2 sono costanti in misura_annotazione_v2.py: si leggono senza eseguirlo
_src = ast.parse(open("tools/analisi/misura_annotazione_v2.py", encoding="utf-8").read())
_k = {t.id: ast.literal_eval(n.value) for n in _src.body if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name) and t.id in ("PROVIDER_ERRATO", "SERVIZIO_ERRATO", "MANCATI")}
PROVIDER_ERRATO, SERVIZIO_ERRATO, MANCATI = _k["PROVIDER_ERRATO"], _k["SERVIZIO_ERRATO"], _k["MANCATI"]

camp = list(csv.DictReader(open("report/metodo/campione-misura-2026-10-27.csv", encoding="utf-8")))[:437]
v3 = {}
for f in glob.glob("lavoro/attribuzione/*.csv"):
    if "campione" in f: continue
    for r in csv.DictReader(open(f, encoding="utf-8")):
        v3[r["cig"]] = r
esito = {"provider_errato_v2": {}, "servizio_errato_v2": {}, "mancati_v2": {}, "rotti": []}
for i, r in enumerate(camp):
    n = v3.get(r["cig"], {"via": "0-fuori", "provider": "", "servizio": ""})
    riga = f'{r["via"]}/{r["provider"]}/{r["servizio"]} -> {n["via"]}/{n["provider"]}/{n["servizio"]}'
    if i in PROVIDER_ERRATO: esito["provider_errato_v2"][i] = riga
    elif i in SERVIZIO_ERRATO: esito["servizio_errato_v2"][i] = riga
    elif i in MANCATI: esito["mancati_v2"][i] = MANCATI[i] + ": " + riga
    elif (r["provider"], r["servizio"]) != (n["provider"], n["servizio"]): esito["rotti"].append(f"{i} " + riga)
print(json.dumps(esito, indent=1, ensure_ascii=False))
