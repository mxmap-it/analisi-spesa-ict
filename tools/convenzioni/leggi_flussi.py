"""#62: legge gli allegati «flussi dati del fatturato» di tutte le iniziative (individuati da base_dati.py) e annota quale
dettaglio riceve Consip: fattura, ordine, ente, listino/prodotto, marchio, CIG, lotto. Gira sul server (archivio completo).
Testo con pdftotext; .p7m sbustati con openssl; file dentro gli zip estratti in memoria.
Uscita (versionata): report/convenzioni/database/flussi-dati.csv
Uso: python tools/convenzioni/leggi_flussi.py"""
import csv
import io
import json
import os
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

R = Path(__file__).resolve().parent.parent.parent
DB = R / "report/convenzioni/database"
ROOT = Path(os.environ.get("ARCHIVIO_ROOT", R / "archivio"))
CAMPI = {
    "fattura": r"numero fattura|data emissione fattura|tipo fattura",
    "ordine": r"id ordine|identificativo dell.ordine|numero (dell.)?ordin",
    "ente": r"codice fiscale (dell.)?amministrazion|denominazione (dell.)?amministrazion|amministrazione contraente|partita iva (dell.)?amministrazion|ipa",
    "listino_prodotto": r"codice (articolo|prodotto)|descrizione (articolo|prodotto)|part ?number|sku|listino",
    "marchio": r"\bbrand\b|marchio|produttore",
    "cig": r"\bcig\b",
    "lotto": r"\blotto\b",
    "imponibile": r"imponibile",
}


def blob(sha):
    return ROOT / "blobs/sha256" / sha[:2] / sha[2:4] / sha


def testo_pdf(dati):
    if dati[:4] != b"%PDF":
        r = subprocess.run(["openssl", "smime", "-verify", "-noverify", "-inform", "DER"], input=dati, capture_output=True)
        dati = r.stdout
    if dati[:4] != b"%PDF":
        return ""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False, dir=R / "lavoro") as f:
        f.write(dati)
    try:
        return subprocess.run(["pdftotext", "-layout", f.name, "-"], capture_output=True, timeout=120).stdout.decode("utf-8", "ignore")
    finally:
        os.unlink(f.name)


def main():
    voci = json.loads((DB / "iniziative.json").read_text(encoding="utf-8"))
    righe = []
    for v in voci:
        for e in v.get("evidenze_dato_esistente") or []:
            b = blob(e["sha256"]) if e.get("sha256") else None
            if not b or not b.exists():
                righe.append({"iniziativa": v["id"], "documento": e["documento"], "sha256": e.get("sha256"), "esito": "blob assente"})
                continue
            dati = b.read_bytes()
            if "#" in e["url"]:
                interno = e["url"].split("#", 1)[1]
                try:
                    dati = zipfile.ZipFile(io.BytesIO(dati)).read(interno)
                except (zipfile.BadZipFile, KeyError):
                    righe.append({"iniziativa": v["id"], "documento": e["documento"], "sha256": e["sha256"], "esito": "zip illeggibile"})
                    continue
            t = testo_pdf(dati).lower()
            if not t.strip():
                righe.append({"iniziativa": v["id"], "documento": e["documento"], "sha256": e["sha256"], "esito": "testo non estraibile (scansione o formato)"})
                continue
            # la parte che descrive i campi del tracciato, se c'è
            m = re.search(r"descrizione dei flussi|tracciat|campi", t)
            sez = t[m.start(): m.start() + 12000] if m else t
            r = {"iniziativa": v["id"], "documento": e["documento"], "sha256": e["sha256"], "esito": "letto",
                 "frequenza": "mensile" if re.search(r"mese|mensil", t) else "", "sezione_campi_trovata": "si" if m else "no"}
            for k, rx in CAMPI.items():
                r[k] = "si" if re.search(rx, sez) else "no"
            righe.append(r)
    campi = ["iniziativa", "documento", "sha256", "esito", "frequenza", "sezione_campi_trovata"] + list(CAMPI)
    with open(DB / "flussi-dati.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campi)
        w.writeheader()
        for r in righe:
            w.writerow({k: r.get(k, "") for k in campi})
    print(len(righe), "allegati;", sum(1 for r in righe if r["esito"] == "letto"), "letti")


if __name__ == "__main__":
    main()
