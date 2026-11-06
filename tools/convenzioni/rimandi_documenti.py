"""#62, documenti mancanti (metodo 2, «rimando»): elenca allegati, appendici e annessi CITATI nei testi archiviati delle iniziative.

Per ogni documento archiviato (PDF, anche dentro zip e .p7m) estrae il testo pagina per pagina (pdftotext, pagine separate da \\f)
e cerca i rimandi del tipo «Allegato 12», «Appendice 1 al Capitolato Tecnico», «Annesso 3», «Sub-allegato B», con il titolo
che segue. Il confronto con i documenti pubblicati lo fa tools/convenzioni/documenti_mancanti.py: qui si registra solo
ciò che i testi dicono, con documento, sha256 e pagina della PRIMA citazione e il numero di citazioni.
Ingressi: report/convenzioni/database/archiviati.jsonl, consip/*.json, archivio content-addressed (ARCHIVIO_ROOT o ./archivio).
Uscita (piccola, versionata): report/convenzioni/database/rimandi.jsonl, una riga per (iniziativa, rimando).
Ripartibile (cache per sha256 in lavoro/rimandi-cache/), deterministico. Gira sul server con nice.
Uso: python tools/convenzioni/rimandi_documenti.py"""
import io
import json
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from estrai_documenti import DB, R, blob, p7m, pdf_testo  # noqa: E402

CACHE = R / "lavoro" / "rimandi-cache"
OUT = DB / "rimandi.jsonl"
# parola chiave (qualunque maiuscola) + identificativo (maiuscolo: «Allegato A», non «allegato a pagina»)
RX = re.compile(r"\b((?i:allegat[oi]|appendic[ei]|annesso|annessi|sub[- ]?allegat[oi]))\s+(?:(?i:n)\.?\s*)?"
                r"(\d{1,2}(?:[.\-]\d{1,2})?(?:\s?[A-Z]\b)?|[A-Z]{1,2}\b(?![a-z'’]))")
RIF = re.compile(r"^\s*(?:,\s*)?(?i:al|alla|allo|all['’]|del|della|dello|dell['’])\s*"
                 r"((?i:capitolato(?: tecnico)?|CT\b|schema(?: di)?(?: accordo quadro| di contratto| di convenzione)?|accordo quadro|"
                 r"convenzione|contratto(?: quadro)?|disciplinare|condizioni|offerta(?: tecnica| economica)?|bando|lettera d.invito))")


def norma_tipo(k):
    k = k.lower().replace(" ", "").replace("-", "")
    if k.startswith("suballegat"):
        return "sub-allegato"
    if k.startswith("allegat"):
        return "allegato"
    if k.startswith("appendic"):
        return "appendice"
    return "annesso"


def norma_rif(r):
    r = (r or "").lower()
    for k, v in (("capitolato", "capitolato"), ("ct", "capitolato"), ("schema", "schema"), ("accordo", "schema"), ("convenzione", "schema"),
                 ("contratto", "schema"), ("disciplinare", "disciplinare"), ("condizioni", "disciplinare"), ("lettera", "disciplinare"),
                 ("offerta", "offerta"), ("bando", "bando")):
        if r.startswith(k):
            return v
    return ""


def titolo(seguito):
    t = re.split(r"[\n;)]|\.\s|\s{3,}", seguito, maxsplit=1)[0]
    t = re.sub(r"^\s*(?:[-–:,]|\(|«|“|\")\s*", "", t).strip(" «»“”\"'")
    return re.sub(r"\s+", " ", t)[:90]


def pagine(nome, dati):
    """(nome interno, [testo pagina 1, ...]) per ogni PDF del file."""
    n = nome.lower()
    if n.endswith(".zip"):
        try:
            z = zipfile.ZipFile(io.BytesIO(dati))
        except zipfile.BadZipFile:
            return
        for i in z.infolist():
            if not i.is_dir() and i.file_size < 30_000_000:
                for sub, pp in pagine(i.filename, z.read(i)):
                    yield sub, pp
    elif n.endswith(".p7m"):
        d = p7m(dati)
        if d:
            yield nome, pdf_testo_pagine(d)
    elif n.endswith(".pdf"):
        yield nome, pdf_testo_pagine(dati)


def pdf_testo_pagine(dati):
    # pdf_testo usa -layout: le pagine restano separate da \f
    return pdf_testo(dati).split("\f")


def rimandi_file(sha, nome):
    c = CACHE / f"{sha}.json"
    if c.exists():
        return json.loads(c.read_text(encoding="utf-8"))
    p = blob(sha)
    out = []
    if p.exists():
        for sub, pp in pagine(nome, p.read_bytes()):
            for i, testo in enumerate(pp, 1):
                for m in RX.finditer(testo):
                    seg = testo[m.end():m.end() + 200]
                    rif = RIF.match(seg)
                    ident = re.sub(r"\s+", "", m.group(2)).upper().replace("-", ".")
                    out.append({"interno": sub, "pagina": i, "tipo": norma_tipo(m.group(1)), "numero": ident,
                                "di": norma_rif(rif.group(1) if rif else ""),
                                "titolo": titolo(seg[rif.end():] if rif else seg),
                                "citazione": re.sub(r"\s+", " ", testo[max(0, m.start() - 60):m.end() + 100]).strip()})
    CACHE.mkdir(parents=True, exist_ok=True)
    c.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    return out


def main():
    arch = {}
    for riga in open(DB / "archiviati.jsonl", encoding="utf-8"):
        a = json.loads(riga)
        arch[a["url"]] = a
    righe = {}
    for f in sorted((DB / "consip").glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        ini = d["iniziativa"]
        for pg in d.get("pagine", []):
            if not pg.get("cita_chiave"):
                continue
            for doc in pg["documenti"]:
                a = arch.get(doc["url"])
                if not a:
                    continue
                for r in rimandi_file(a["sha256"], doc["nome"]):
                    k = (ini, r["tipo"], r["numero"], r["di"])
                    if k not in righe:
                        righe[k] = {"iniziativa": ini, "tipo": r["tipo"], "numero": r["numero"], "di": r["di"], "titolo": r["titolo"],
                                    "documento": doc["nome"] + ("#" + r["interno"] if r["interno"] != doc["nome"] else ""),
                                    "url": doc["url"], "sha256": a["sha256"], "pagina": r["pagina"], "citazione": r["citazione"][:240],
                                    "n_citazioni": 0}
                    righe[k]["n_citazioni"] += 1
        print(ini, sum(1 for k in righe if k[0] == ini), flush=True)
    with open(OUT, "w", encoding="utf-8") as fo:
        for k in sorted(righe):
            fo.write(json.dumps(righe[k], ensure_ascii=False) + "\n")
    print(len(righe), "rimandi ->", OUT)


if __name__ == "__main__":
    main()
