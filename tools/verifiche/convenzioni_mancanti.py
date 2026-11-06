"""#62: verifica di report/convenzioni/database/documenti-mancanti.csv, eseguibile da un clone pulito.

1. Ripetibilità: rigenera l'inventario con tools/convenzioni/documenti_mancanti.py (senza scrivere bozze) e controlla che il CSV
   non cambi (stesso sha256).
2. Seconda via per i buchi di numerazione: ricalcola, con un'espressione indipendente sui nomi dei file pubblicati (pagine Consip e
   contenuto degli zip archiviati), gli «Allegato N» assenti fra 1 e il massimo, e controlla che ognuno sia nel CSV.
3. Coerenza: colonne, valori ammessi (metodo, criticità, livello, dietro_login), ogni riga [V] ha data_controllo e url_pagina,
   ogni bozza citata esiste nel registro.
Uso: python tools/verifiche/convenzioni_mancanti.py   (codice 1 se qualcosa non torna)"""
import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

R = Path(__file__).resolve().parent.parent.parent
DB = R / "report/convenzioni/database"
CSV = DB / "documenti-mancanti.csv"
err = 0


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


prima = sha(CSV)
subprocess.run([sys.executable, str(R / "tools/convenzioni/documenti_mancanti.py")], check=True, capture_output=True)
if sha(CSV) != prima:
    print("ERRORE: la rigenerazione cambia documenti-mancanti.csv"); err += 1
righe = list(csv.DictReader(open(CSV, encoding="utf-8")))
reg = {r["id"] for r in csv.DictReader(open(R / "report/convenzioni/accesso-civico/registro.csv", encoding="utf-8"))}
for r in righe:
    ok = (set(r["metodo"].split(";")) <= {"numerazione", "rimando", "atteso"} and r["criticita"] in "123" and r["livello"] in ("[V]", "[R]")
          and r["dietro_login"] in ("sì", "no", "ignoto") and (r["livello"] != "[V]" or (r["data_controllo"] and r["url_pagina"]))
          and (not r["bozza_accesso_civico"] or r["bozza_accesso_civico"] in reg))
    if not ok:
        print("ERRORE riga:", r["iniziativa"], r["documento_atteso"][:60]); err += 1
# seconda via: solo «Allegato <intero>» senza «al/allo …» (serie principale)
arch = {}
for x in open(DB / "archiviati.jsonl", encoding="utf-8"):
    a = json.loads(x); arch[a["url"]] = a
attesi = 0
for f in sorted((DB / "consip").glob("*.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    ini, sig = d["iniziativa"], d["iniziativa"].split("-")[-1]
    nomi = []
    for p in d.get("pagine", []):
        if not p.get("cita_chiave"):
            continue
        for doc in p["documenti"]:
            m = re.search(r"ID[ _]*(\d{4})", doc["nome"])
            if m and sig.isdigit() and m.group(1) != sig:
                continue
            for n in [doc["nome"]] + list(arch.get(doc["url"], {}).get("contenuto") or []):
                m = re.search(r"ID[ _]*(\d{4})", n)
                if not (m and sig.isdigit() and m.group(1) != sig):
                    nomi.append(n)
    nums = set()
    for n in nomi:
        for m in re.finditer(r"(?i)allegato[ _-]+(?:n\.?\s*)?(\d{1,2})(?![\d.])(?![ _-]*(?:al|allo|del|dello|all)\b)", n):
            nums.add(int(m.group(1)))
    if len(nums) >= 2:
        for k in range(1, max(nums)):
            if k not in nums:
                attesi += 1
                if not any(r["iniziativa"] == ini and "numerazione" in r["metodo"] and re.match(rf"Allegato {k}\b", r["documento_atteso"]) for r in righe):
                    print("ERRORE seconda via: manca nel CSV", ini, "Allegato", k); err += 1
# 4. il rapporto riporta gli stessi conteggi
mu = R / "report/convenzioni/rapporto/metriche-ultime.json"
if mu.exists():
    mm = json.loads(mu.read_text(encoding="utf-8")).get("mancanti")
    from collections import Counter
    if mm and (mm["righe"] != len(righe) or mm["criticita"] != dict(sorted(Counter(r["criticita"] for r in righe).items()))):
        print("ERRORE: conteggi del rapporto diversi dal CSV (rilanciare tools/convenzioni/rapporto.py)"); err += 1
print(len(righe), "righe;", attesi, "buchi di numerazione ricalcolati per seconda via;", "OK" if not err else f"{err} errori")
sys.exit(1 if err else 0)
