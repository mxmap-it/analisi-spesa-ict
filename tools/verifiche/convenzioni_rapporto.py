"""#62: verifica dei numeri del rapporto «Trasparenza delle convenzioni ICT» (sito/content/rendiconti/convenzioni-trasparenza.md).

Seconda via: ricalcola da iniziative.json, senza usare tools/convenzioni/rapporto.py, le classi di visibilità, il valore non ben
visibile e i conteggi delle istanze, e li confronta con report/convenzioni/rapporto/metriche-ultime.json.
Uso: python tools/verifiche/convenzioni_rapporto.py   (codice 1 se qualcosa non torna)"""
import csv
import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parent.parent.parent
voci = json.loads((R / "report/convenzioni/database/iniziative.json").read_text(encoding="utf-8"))
m = json.loads((R / "report/convenzioni/rapporto/metriche-ultime.json").read_text(encoding="utf-8"))["globali"]
reg = list(csv.DictReader(open(R / "report/convenzioni/accesso-civico/registro.csv", encoding="utf-8")))

FUORI = {"consip-2638"}  # fuori perimetro (energia), come in rapporto.py
celle = {"pubblico": 0, "altrove": 0, "assente": 0, "ignoto": 0}
tot = nbv = bv = 0
for v in voci:
    val = v["valore_ict_2024_2025"] or 0
    tot += val
    stati = {}
    for i in v["inventario"]:
        pubblico = i["stato"] in ("archiviato", "pubblicato-non-archiviato")
        k = "pubblico" if pubblico else "altrove" if i.get("reperiti_altrove") else "assente" if i["stato"] == "non-pubblicato" else "ignoto"
        celle[k] += 1
        stati[i["tipo"]] = pubblico
    ok = all(stati.get(t) for t in ("offerta_tecnica", "offerta_economica", "transato_monitoraggio", "ordinativi"))
    bv += ok
    nbv += 0 if ok else val
attesi = {"iniziative": len(voci), "valore_2024_2025": tot, "valore_non_ben_visibile": nbv, "iniziative_ben_visibili": bv,
          "istanze_preparate": sum(1 for r in reg if r["stato"] == "preparata"),
          "od_ordinato": sum(v["ordinato_consip"]["2024"] + v["ordinato_consip"]["2025"] for v in voci if v.get("ordinato_consip") and v["id"] not in FUORI),
          "od_bdncp": sum(v["valore_ict_2024_2025"] or 0 for v in voci if v.get("ordinato_consip") and v["id"] not in FUORI)}
# terza via per l'ordinato: direttamente dal CSV versionato
import csv as _c
attesi["od_ordinato_csv"] = sum(int(r["ordinato_2024"]) + int(r["ordinato_2025"]) for r in _c.DictReader(open(R / "report/convenzioni/database/consip-ordinato.csv", encoding="utf-8")) if r["iniziativa"] not in FUORI)
m["od_ordinato_csv"] = m["od_ordinato"]
errori = 0
for k, a in attesi.items():
    print(f"{k}: seconda via {a} / rapporto {m[k]}", "OK" if a == m[k] else "DIVERSO")
    errori += a != m[k]
for k, a in celle.items():
    b = m["celle"].get(k, 0)
    print(f"celle {k}: seconda via {a} / rapporto {b}", "OK" if a == b else "DIVERSO")
    errori += a != b
sys.exit(1 if errori else 0)
