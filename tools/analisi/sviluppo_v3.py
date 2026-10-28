"""Controllo di sviluppo delle regole v3 sulle 437 righe annotate della misura v2 (report/metodo/campione-misura-2026-10-27.csv).
Non è una misura: le regole v3 sono state scritte guardando questi errori. Dice se ogni classe di errore è chiusa
e se la v3 cambia righe che la v2 attribuiva bene (da rileggere a mano). La misura v3 si fa su un campione nuovo.
Uso: python tools/analisi/sviluppo_v3.py"""
import ast, csv, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from classifica import Classificatore  # noqa: E402

# le annotazioni v2 sono costanti in misura_annotazione_v2.py: si leggono senza eseguirlo
_src = ast.parse(open("tools/analisi/misura_annotazione_v2.py", encoding="utf-8").read())
_k = {t.id: ast.literal_eval(n.value) for n in _src.body if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name) and t.id in ("PROVIDER_ERRATO", "SERVIZIO_ERRATO", "MANCATI")}
PROVIDER_ERRATO, SERVIZIO_ERRATO, MANCATI = _k["PROVIDER_ERRATO"], _k["SERVIZIO_ERRATO"], _k["MANCATI"]

c = Classificatore()
camp = list(csv.DictReader(open("report/metodo/campione-misura-2026-10-27.csv", encoding="utf-8")))[:437]
esito = {"provider_errato_v2": {}, "servizio_errato_v2": {}, "mancati_v2": {}, "cambiati": []}
for i, r in enumerate(camp):
    n = c.classifica(r["testo"], "", [a.strip() for a in r["aggiudicatari"].split(";")], r["cod_cpv"]) or {"via": "fuori", "provider": "", "servizio": ""}
    riga = f'{r["via"]}/{r["provider"]}/{r["servizio"]} -> {n["via"]}/{n["provider"]}/{n["servizio"]}'
    if i in PROVIDER_ERRATO: esito["provider_errato_v2"][i] = riga
    elif i in SERVIZIO_ERRATO: esito["servizio_errato_v2"][i] = riga
    elif i in MANCATI: esito["mancati_v2"][i] = MANCATI[i] + ": " + riga
    elif r["via"][:1] != "1" and (r["provider"], r["servizio"]) != (n["provider"], n["servizio"]):
        esito["cambiati"].append(f"{i} {riga} | {r['testo'][:120]}")
print(json.dumps(esito, indent=1, ensure_ascii=False))
