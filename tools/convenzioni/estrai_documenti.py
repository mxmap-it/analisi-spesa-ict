"""#62: estratti per parole chiave dai documenti archiviati delle iniziative (prodotti e marchi, tetti, region e data center,
obblighi di reporting e monitoraggio). Serve a orientare la lettura: un estratto NON è un'analisi, e nel sito resta marcato
«estratto automatico, da leggere» finché qualcuno non lo conferma in curate.yaml.

Testo: pdftotext (poppler) per i PDF, anche dentro gli zip e i .p7m (si estrae il PDF firmato con openssl se c'è).
Ingressi: report/convenzioni/database/archiviati.jsonl, consip/*.json, archivio content-addressed (ARCHIVIO_ROOT o ./archivio).
Uscita (piccola, versionata): report/convenzioni/database/estratti/<iniziativa>.json, al massimo 3 estratti per tema e documento.
Ripartibile e deterministico. Gira sul server: nice, un file alla volta, niente in RAM oltre al singolo testo.
Uso: python tools/convenzioni/estrai_documenti.py"""
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

R = Path(__file__).resolve().parent.parent.parent
DB = R / "report/convenzioni/database"
ROOT = Path(os.environ.get("ARCHIVIO_ROOT", R / "archivio"))
OUT = DB / "estratti"
TEMI = {
    "prodotti_marchi": r"\b(brand|marchi?o?|produttor[ei]|vendor|cloud service provider|CSP)\b",
    "tetti_erosione": r"(soglia massima di erosione|massimale|quota minima|tetto)",
    "region_datacenter": r"\b(region[ei]?|data ?cent(er|re)|sede del trattamento|localizzazione dei dati|spazio economico europeo|extra.?UE)\b",
    "reporting": r"(reportistica|report (mensil|trimestral|semestral)|monitoraggio|flussi dati|dati di consumo|rendicontazion)",
}
PER_TEMA = 3


def blob(sha):
    return ROOT / "blobs" / "sha256" / sha[:2] / sha[2:4] / sha


def pdf_testo(dati):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False, dir=R / "lavoro") as f:
        f.write(dati)
        nome = f.name
    try:
        return subprocess.run(["pdftotext", "-q", "-layout", nome, "-"], capture_output=True, timeout=120).stdout.decode("utf-8", "ignore")
    except subprocess.TimeoutExpired:
        return ""
    finally:
        os.unlink(nome)


def p7m(dati):
    try:
        r = subprocess.run(["openssl", "smime", "-verify", "-noverify", "-inform", "DER"], input=dati, capture_output=True, timeout=60)
        return r.stdout if r.stdout[:4] == b"%PDF" else b""
    except Exception:
        return b""


def testi(nome, dati):
    n = nome.lower()
    if n.endswith(".zip"):
        try:
            z = zipfile.ZipFile(io.BytesIO(dati))
        except zipfile.BadZipFile:
            return
        for i in z.infolist():
            if not i.is_dir() and i.file_size < 30_000_000:
                yield from testi(i.filename, z.read(i))
    elif n.endswith(".p7m"):
        d = p7m(dati)
        if d:
            yield nome, pdf_testo(d)
    elif n.endswith(".pdf"):
        yield nome, pdf_testo(dati)


def main():
    (R / "lavoro").mkdir(exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    arch = {}
    for riga in open(DB / "archiviati.jsonl", encoding="utf-8"):
        a = json.loads(riga)
        arch[a["url"]] = a
    for cp in sorted((DB / "consip").glob("*.json")):
        ini = cp.stem
        dest = OUT / f"{ini}.json"
        if dest.exists():
            continue
        e = json.loads(cp.read_text(encoding="utf-8"))
        docs = [d for p in e.get("pagine", []) if p.get("cita_chiave") for d in p["documenti"]]
        # solo documenti chiave, firmati esclusi se c'è la copia non firmata
        chiave = [d for d in docs if re.search(r"capitolato|schema|convenzione|listin|condizioni|chiariment|determina|doc.*uff|cdo|disciplinare", d["nome"], re.I)
                  and "firmata/" not in d["url"].replace("non_firmata/", "")]
        out = {"iniziativa": ini, "documenti_letti": 0, "estratti": []}
        for d in chiave:
            a = arch.get(d["url"])
            if not a or not blob(a["sha256"]).exists():
                continue
            for nome, t in testi(d["nome"], blob(a["sha256"]).read_bytes()):
                if not t:
                    continue
                out["documenti_letti"] += 1
                t = re.sub(r"\s+", " ", t)
                for tema, rx in TEMI.items():
                    for m in list(re.finditer(rx, t, re.I))[:PER_TEMA]:
                        out["estratti"].append({"tema": tema, "documento": nome.rsplit("/", 1)[-1][:120], "url": d["url"], "sha256": a["sha256"],
                                                "testo": t[max(0, m.start() - 220): m.end() + 280]})
        dest.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print(ini, out["documenti_letti"], len(out["estratti"]), flush=True)


if __name__ == "__main__":
    main()
