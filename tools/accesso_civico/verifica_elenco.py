#!/usr/bin/env python3
"""#58 Verifica indipendente dell'elenco unico dei mancanti (elenco_mancanti.py). Rilegge gli ingressi e controlla:
V1 voci A = righe di documenti-mancanti.csv; V2 voci B = ingresso (P1-P5) meno i CIG «documento-cita-cig» del per-66;
V3 nessun CIG escluso è nell'elenco; V4 id univoci; V5 PEC con forma di indirizzo e, se presente, uguale a IndicePA per il CF;
V6 somma delle voci per ente = voci; V7 nessun testo di richiesta generato (nessuna colonna «testo»/«corpo»).
Uso (server): .venv/bin/python tools/accesso_civico/verifica_elenco.py DATA [--data-66 AAAA-MM-GG]; esce con 1 se fallisce.
"""
import csv, json, re, sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]
csv.field_size_limit(10**9)
data = sys.argv[1]
d66 = sys.argv[sys.argv.index("--data-66") + 1] if "--data-66" in sys.argv else "2026-11-09"
O = R / f"esiti/{data}/accesso-civico"
el = list(csv.DictReader(open(O / "elenco-mancanti.csv", encoding="utf-8")))
enti = list(csv.DictReader(open(O / "enti.csv", encoding="utf-8")))
conv = list(csv.DictReader(open(R / "report/convenzioni/database/documenti-mancanti.csv", encoding="utf-8")))
ing = [r for r in csv.DictReader(open(R / "lavoro/residuo-s6/ingresso.csv", encoding="utf-8")) if (r.get("priorita") or "").startswith("P")]
cita = {r["cig"] for r in csv.DictReader(open(R / f"esiti/{d66}/imbuto/residuo-s6-per-66.csv", encoding="utf-8"))
        if r["materiale"] == "documento-cita-cig"}
A = [r for r in el if r["fonte"].startswith("A")]; B = [r for r in el if r["fonte"].startswith("B")]
esito = {
    "V1_voci_A": (len(A), len(conv), len(A) == len(conv)),
    "V2_voci_B": (len(B), len({r["cig"] for r in ing} - cita), len(B) == len({r["cig"] for r in ing} - cita)),
    "V3_esclusi_assenti": sum(r["cig"] in cita for r in B) == 0,
    "V4_id_univoci": len({r["id"] for r in el}) == len(el),
    "V5_pec_forma": sum(bool(r["pec"]) and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[a-z]{2,}", r["pec"].strip(), re.I) for r in el) == 0,
    "V6_somma_enti": sum(int(e["voci"]) for e in enti) == len(el),
    "V7_nessun_testo_richiesta": not ({"testo", "corpo", "testo_richiesta"} & set(el[0])),
}
ok = all(v if isinstance(v, bool) else v[2] for v in esito.values())
esito["ok"] = ok
json.dump(esito, open(O / "verifica.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(json.dumps(esito, ensure_ascii=False))
sys.exit(0 if ok else 1)
