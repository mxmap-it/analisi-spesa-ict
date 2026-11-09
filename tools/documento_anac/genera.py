"""Documento per ANAC (#34): PDF impaginato con typst dal registro report/anac/problemi.yaml.

Non è la stampa del sito: il testo viene dal registro (unica fonte) e l'impaginazione da
documento.typ (A4, copertina, sintesi, schede, appendice). Uso:
  python tools/documento_anac/genera.py [--data 2026-11-06]
Requisiti: pip install typst pyyaml. Font: solo quelli inclusi in typst (riproducibile ovunque).
"""

import argparse
import hashlib
import json
import pathlib

import typst
import yaml

RADICE = pathlib.Path(__file__).resolve().parents[2]
QUI = pathlib.Path(__file__).resolve().parent
ORDINE = {"alta": 0, "media": 1, "bassa": 2, "da_valutare": 3}
VERSIONE = "1.1"
# Registro delle revisioni del documento (la più recente in fondo).
REVISIONI = [
    ("1.0", "2026-11-06", "Prima impaginazione typst dal registro: 17 problemi pronti, P15 in appendice come interno."),
    ("1.1", "2026-11-09", "P15 (contratti attuativi senza collegamento all'accordo quadro) pronta e inserita fra le schede: "
     "misure su campi strutturati (cig_aq_tipo.py, cig_aq_padre_appalto.py), originali ANAC archiviati (scheda AD4 nel "
     "modello dati github.com/anticorruzione/npa, comunicato del Presidente 5/6/2024), campione di 30 vuoti 2025; "
     "raccomandazione R81. P04 aggiornata con la misura su tutto il mirror OCDS (96 mesi, 0 date conformi da 2019/12, "
     "3,59 milioni di release senza data). Le schede riportano ora anche le misure successive alla prima. 18 problemi pronti su 18."),
]
# Campi del registro con misure successive alla prima, mostrati nella scheda (etichetta).
ALTRE_MISURE = {
    "misura_mirror": "Misura su tutto il mirror",
    "misura_9_11": "Misura per tipo di adesione (9/11/2026)",
    "anomalia_padre_appalto_9_11": "Natura del padre persa (9/11/2026)",
    "norma_9_11": "Obbligo normativo",
    "originali_9_11": "Originali ANAC archiviati",
    "campione_vuoti_9_11": "Campione dei campi vuoti",
}


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--data", default="2026-11-09")
    a = a.parse_args()
    reg = RADICE / "report/anac/problemi.yaml"
    probl = yaml.safe_load(reg.read_text(encoding="utf-8"))
    for p in probl:
        p["rif"] = ", ".join(str(r) for r in p.get("rif", []))
        p["prova"] = {k: str(v) for k, v in p.get("prova", {}).items()}
        p["altre_misure"] = [{"etichetta": e, "testo": str(p[k])} for k, e in ALTRE_MISURE.items() if p.get(k)]
    pronti = [p for p in probl if p.get("pronto_per_anac")]
    interni = [p for p in probl if not p.get("pronto_per_anac")]
    pronti.sort(key=lambda p: (ORDINE.get(p.get("gravita"), 9), p["id"]))
    # Ripetibilità: ogni scheda pronta deve citare uno script e un esito presenti nel repository.
    for p in pronti:
        for k in ("script", "esito"):
            v = p["prova"].get(k, "").split()[0] if p["prova"].get(k) else ""
            if not v or not (RADICE / v).exists():
                raise SystemExit(f"{p['id']}: prova.{k} assente o inesistente ({v!r})")
    dati = {
        "data": a.data,
        "versione": VERSIONE,
        "revisioni": [{"versione": v, "data": d, "nota": n} for v, d, n in REVISIONI],
        "registro_sha256": hashlib.sha256(reg.read_bytes()).hexdigest(),
        "pronti": pronti,
        "interni": interni,
        "totale": len(probl),
        "gravita": {g: sum(p.get("gravita") == g for p in pronti) for g in ORDINE},
    }
    (QUI / "dati.json").write_text(
        json.dumps(dati, ensure_ascii=False, indent=1, default=str), encoding="utf-8"
    )
    out = RADICE / "sito/static/pdf/anac-problemi-e-rimedi-2026-10.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    typst.compile(str(QUI / "documento.typ"), output=str(out), root=str(QUI))
    h = hashlib.sha256(out.read_bytes()).hexdigest()
    print(f"v{VERSIONE}: {len(pronti)} pronti, {len(interni)} interni -> {out} sha256 {h}")


if __name__ == "__main__":
    main()
