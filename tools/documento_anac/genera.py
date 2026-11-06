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


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--data", default="2026-11-06")
    a = a.parse_args()
    reg = RADICE / "report/anac/problemi.yaml"
    probl = yaml.safe_load(reg.read_text(encoding="utf-8"))
    for p in probl:
        p["rif"] = ", ".join(str(r) for r in p.get("rif", []))
        p["prova"] = {k: str(v) for k, v in p.get("prova", {}).items()}
    pronti = [p for p in probl if p.get("pronto_per_anac")]
    interni = [p for p in probl if not p.get("pronto_per_anac")]
    pronti.sort(key=lambda p: (ORDINE.get(p.get("gravita"), 9), p["id"]))
    dati = {
        "data": a.data,
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
    print(f"{len(pronti)} pronti, {len(interni)} interni -> {out} sha256 {h}")


if __name__ == "__main__":
    main()
