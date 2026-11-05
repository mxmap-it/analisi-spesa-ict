"""#62: importo ordinato per iniziativa dagli open data Consip (dati.consip.it, «Ordini diretti di acquisto in Convenzione» e
«... su Accordi Quadro senza rilancio competitivo», 2024 e 2025), archiviati con tools/archivia.py.

È una seconda via per il valore delle iniziative, indipendente da BDNCP: Consip pubblica per anno l'importo ordinato per
convenzione o AQ e lotto (con tipologia e provincia della PA), ma non per ente, listino o marchio.
Abbinamento nome Consip → iniziativa del censimento: il nome normalizzato della convenzione Consip deve comparire nell'oggetto
di un CIG padre dell'iniziativa (regola stretta, niente somiglianze); gli abbinamenti sono elencati nell'uscita per il controllo.
Uscita (versionata): report/convenzioni/database/consip-ordinato.csv e consip-ordinato-fonti.json (URL e sha256 dei file letti).
Uso: python tools/convenzioni/consip_opendata.py"""
import csv
import hashlib
import io
import json
import os
import re
from collections import defaultdict
from pathlib import Path

R = Path(__file__).resolve().parent.parent.parent
DB = R / "report/convenzioni/database"
ROOT = Path(os.environ.get("ARCHIVIO_ROOT", R / "archivio"))
FILE = {f"https://dati.consip.it/download/dataset/{n}.csv": n for n in
        ("ordini-convenzione-2024", "ordini-convenzione-2025", "ordini-aq-2024", "ordini-aq-2025")}


def norm(s):
    s = s.upper().replace("�", "A")
    s = re.sub(r"[^A-Z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def importo(x):
    try:
        return float((x or "").replace(".", "").replace(",", ".")) if x not in ("", "NA", "ND") else 0.0
    except ValueError:
        return 0.0


def main():
    voci = json.loads((DB / "iniziative.json").read_text(encoding="utf-8"))
    ogg = {v["id"]: " | ".join(norm(l["oggetto"]) for l in v["lotti"]) + " | " + norm(v["nome"]) for v in voci if v["tipo_soggetto"] == "consip"}
    tot = defaultdict(lambda: defaultdict(float))
    nomi = defaultdict(set)
    fonti = []
    for url, n in FILE.items():
        p = ROOT / "mirror/dati.consip.it/download/dataset" / f"{n}.csv"
        if not p.exists():
            continue
        dati = p.read_bytes()
        fonti.append({"url": url, "sha256": hashlib.sha256(dati).hexdigest()})
        anno = n[-4:]
        for r in csv.DictReader(io.StringIO(dati.decode("latin-1").lstrip("#"))):
            conv = r.get("Convenzione") or r.get("Accordo_Quadro") or r.get("Iniziativa") or ""
            tot[norm(conv)][anno] += importo(r.get("Importo_Ordinato") or r.get("Valore_economico_ordini"))
    import yaml
    mappa = yaml.safe_load(open(DB / "consip-ordinato-mappa.yaml", encoding="utf-8")) or {}
    righe = []
    for conv, anni in tot.items():
        if conv in mappa:
            m = mappa[conv]
            righe.append({"iniziativa": m["iniziativa"], "nome_consip": conv, "ordinato_2024": round(anni.get("2024", 0)),
                          "ordinato_2025": round(anni.get("2025", 0)), "abbinamento": f"a mano (V-testo): {m['perche']}"})
            continue
        if not conv or len(conv) < 8:
            continue
        cand = [i for i, o in ogg.items() if re.search(rf"(^|[ |]){re.escape(conv)}($|[ |])", o)]
        if len(cand) == 1:
            nomi[cand[0]].add(conv)
            righe.append({"iniziativa": cand[0], "nome_consip": conv, "ordinato_2024": round(anni.get("2024", 0)), "ordinato_2025": round(anni.get("2025", 0)),
                          "abbinamento": "nome nell'oggetto del CIG padre (V-testo)"})
    righe.sort(key=lambda r: (r["iniziativa"], r["nome_consip"]))
    with open(DB / "consip-ordinato.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["iniziativa", "nome_consip", "ordinato_2024", "ordinato_2025", "abbinamento"])
        w.writeheader()
        w.writerows(righe)
    (DB / "consip-ordinato-fonti.json").write_text(json.dumps({"fonti": fonti, "convenzioni_nei_dati": len(tot),
                                                               "abbinate": len(righe)}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(tot), "convenzioni/AQ negli open data;", len(righe), "abbinate a", len(nomi), "iniziative")


if __name__ == "__main__":
    main()
