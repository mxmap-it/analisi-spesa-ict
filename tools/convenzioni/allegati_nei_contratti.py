"""#62, revisione dell'inventario dei mancanti: offerte, listini e corrispettivi PUBBLICATI DENTRO i contratti firmati.

Molti accordi quadro e convenzioni stipulati (PDF firmati sulla pagina Consip) contengono in coda gli allegati: offerta tecnica,
offerta economica del fornitore, «Corrispettivi e tariffe», listini. Il metodo «rimando» li segnalava come mancanti (il contratto
li cita), ma sono nel PDF stesso. Questo strumento li trova pagina per pagina:
  - pagina di copertina «ALLEGATO X – OFFERTA ECONOMICA/TECNICA…», «CORRISPETTIVI E TARIFFE», «LISTINO», «PREZZI»;
  - oppure pagina del modulo di offerta economica del sistema (« Offerta economica relativa a: »), o tabelle con «Prezzo offerto»;
e registra se le pagine seguenti hanno contenuto reale (testo, cifre in euro) o sono oscurate/vuote.
Ingressi: archiviati.jsonl, consip/*.json, archivio content-addressed. Uscita: report/convenzioni/database/allegati-nei-contratti.jsonl.
Ripartibile (cache per sha256 in lavoro/allegati-contratti-cache/), deterministico. Gira sul server con nice.
Uso: python tools/convenzioni/allegati_nei_contratti.py"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from estrai_documenti import DB, R, blob  # noqa: E402
from rimandi_documenti import pagine  # noqa: E402

CACHE = R / "lavoro" / "allegati-contratti-cache"
OUT = DB / "allegati-nei-contratti.jsonl"
COPERTINA = re.compile(r"(?i)^\W*(?:classificazione del documento:?\s*consip \w+\s*)?(allegato|appendice)\s+[0-9A-Z.]{1,4}\b[^\n]{0,40}?"
                       r"(offerta\s+economica|offerta\s+tecnica|corrispettivi|listin[oi]|prezz[oi]|relazione\s+tecnica)")
MODULO_OE = re.compile(r"(?i)offerta economica relativa a\s*:|prezzo offerto|ribasso (percentuale )?offerto|prezzo unitario offerto")
TIPO = [("offerta_economica", r"(?i)offerta\s+economica|offerta economica relativa"), ("listini", r"(?i)listin|corrispettiv|prezz"),
        ("offerta_tecnica", r"(?i)offerta\s+tecnica|relazione\s+tecnica")]
EURO = re.compile(r"€\s?\d|\d[\d.]*,\d{2}\s?€|\d+,\d{2}\b")


def tipo_di(t):
    for k, rx in TIPO:
        if re.search(rx, t):
            return k
    return "altro"


def analizza(sha, nome):
    c = CACHE / f"{sha}.json"
    if c.exists():
        return json.loads(c.read_text(encoding="utf-8"))
    out = []
    p = blob(sha)
    if p.exists():
        for sub, pp in pagine(nome, p.read_bytes()):
            for i, t in enumerate(pp, 1):
                testa = "\n".join(x.strip() for x in t.splitlines() if x.strip())[:400]
                m = COPERTINA.search(testa[:200])
                mod = MODULO_OE.search(t)
                if not (m or mod):
                    continue
                seg = " ".join(pp[i:i + 5]) if m else t  # dopo la copertina, le 5 pagine seguenti
                out.append({"interno": sub, "pagina": i, "via": "copertina" if m else "modulo/tabella",
                            "tipo": tipo_di(m.group(0) if m else mod.group(0)), "intestazione": re.sub(r"\s+", " ", testa[:140]),
                            "car_seguenti": len(re.sub(r"\s+", "", seg)), "cifre_euro_seguenti": len(EURO.findall(seg)),
                            "pagine_doc": len(pp)})
    CACHE.mkdir(parents=True, exist_ok=True)
    c.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    return out


def main():
    arch = {json.loads(x)["url"]: json.loads(x) for x in open(DB / "archiviati.jsonl", encoding="utf-8")}
    righe = []
    for f in sorted((DB / "consip").glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        ini = d["iniziativa"]
        visti = set()
        for pg in d.get("pagine", []):
            if not pg.get("cita_chiave"):
                continue
            for doc in pg["documenti"]:
                a = arch.get(doc["url"])
                if not a or a["sha256"] in visti:
                    continue
                visti.add(a["sha256"])
                for r in analizza(a["sha256"], doc["nome"]):
                    # un modulo vuoto (fac-simile) non è l'offerta: serve contenuto reale dopo la copertina o cifre nel modulo
                    pieno = r["car_seguenti"] > 1500 and (r["tipo"] != "offerta_economica" and r["tipo"] != "listini" or r["cifre_euro_seguenti"] >= 3)
                    fac = re.search(r"(?i)fac[ -]?simile|schema di offerta|modello", r["intestazione"] + " " + r["interno"])
                    righe.append({"iniziativa": ini, "documento": doc["nome"] + ("#" + r["interno"] if r["interno"] != doc["nome"] else ""),
                                  "url": doc["url"], "sha256": a["sha256"], **{k: r[k] for k in ("pagina", "via", "tipo", "intestazione",
                                  "car_seguenti", "cifre_euro_seguenti", "pagine_doc")},
                                  "esito": "fac-simile" if fac else ("pubblicato-nel-documento" if pieno else "copertina-senza-contenuto/oscurato")})
        print(ini, sum(1 for x in righe if x["iniziativa"] == ini), flush=True)
    with open(OUT, "w", encoding="utf-8") as fo:
        for r in sorted(righe, key=lambda r: (r["iniziativa"], r["documento"], r["pagina"])):
            fo.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(len(righe), "->", OUT)


if __name__ == "__main__":
    main()
