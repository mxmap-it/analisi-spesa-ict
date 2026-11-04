"""PEC agli enti e ad ANAC: preparazione e registro degli invii. QUESTO MODULO NON INVIA NULLA.

L'invio è manuale (Fabio) o, in futuro, automatico solo dopo autorizzazione esplicita.

    censimento.py pec-prepara --giro AAAA-MM-GG [--cf CF ...]
        -> lavoro/trasparenza/pec/<giro>/<cf>/{ente.txt, anac.txt, evidenza.json, allegati/, SHA256SUMS}
    censimento.py pec-registra --cf CF --giro G --destinatario ente|anac --evento invio|accettazione|consegna|
                               mancata-consegna|risposta [--indirizzo ...] [--id-messaggio ...]
                               [--file ricevuta.eml] [--nota ...] [--data AAAA-MM-GG]

Registro: dati/trasparenza/invii.csv, APPEND-ONLY, una riga per evento (schema/invii.schema.json).
Lo stato per ente (ultimo evento, esito al giro successivo) si ricava dal registro e dai giri.
"""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
from pathlib import Path

from comune import ARCHIVIO, DATI, LAVORO, VERSIONE_METODO, adesso, salva_blob

REGISTRO = DATI / "invii.csv"
CAMPI_INVII = ["ts_registrazione", "data_evento", "cf", "giro", "destinatario", "evento", "indirizzo", "modello",
               "id_messaggio", "sha256_file", "sha256_allegati", "nota"]
EVENTI = ["invio", "accettazione", "consegna", "mancata-consegna", "risposta"]
MODELLO = f"trasparenza-art9/{VERSIONE_METODO}"


def _blob(sha: str) -> Path:
    return ARCHIVIO / "blobs" / "sha256" / sha[:2] / sha[2:4] / sha


def evidenze(r: dict) -> str:
    righe = [f"- Pagina verificata: {r['at_url']} (provenienza dell'URL: {r['at_provenienza']})",
             f"- Data e ora della verifica (UTC): {r['ts']}",
             f"- Esito: {r['esito']} — {r['dettaglio_esito']}"]
    if r.get("robots_blocchi"):
        righe.append(f"- robots.txt ({r['robots_url']}, sha256 {r['robots_sha256']}): {r['robots_blocchi']}")
    if r.get("noindex"):
        righe.append(f"- Direttiva di non indicizzazione: {r['noindex']}")
    if r.get("firme_waf") or r.get("status_bot") != r.get("status_browser"):
        righe.append(f"- Risposte HTTP: client automatico dichiarato {r['status_bot']}, browser {r['status_browser']}; "
                     f"protezioni riconosciute: {r.get('firme_waf') or 'nessuna firma'}")
    if r.get("conferma_browser"):
        righe.append(f"- Seconda prova con browser reale: {r['conferma_browser']}")
    return "\n".join(righe)


def testo_ente(r: dict, pec: str) -> str:
    return f"""A: {r['denominazione']} — PEC: {pec or '(non presente in IndicePA)'}
Alla c.a. del Responsabile della prevenzione della corruzione e della trasparenza (RPCT)

Oggetto: sezione «Amministrazione trasparente» non indicizzabile dai motori di ricerca — art. 9, comma 1, d.lgs. 33/2013

Gentile Responsabile,

nell'ambito del progetto indipendente analisi-spesa-ict (https://analisi-spesa-ict.mxmap.it/progetto/trasparenza-accessibilita/)
abbiamo verificato in modo automatico e riproducibile l'accessibilità della sezione «Amministrazione trasparente»
del Vostro ente. L'art. 9, comma 1, del d.lgs. 33/2013 dispone che le amministrazioni «non possono disporre filtri
e altre soluzioni tecniche atte ad impedire ai motori di ricerca web di indicizzare ed effettuare ricerche
all'interno della sezione».

Evidenze (allegate, con impronta sha256 nel file SHA256SUMS):
{evidenze(r)}

Azione correttiva richiesta: rimuovere, per i percorsi della sezione «Amministrazione trasparente», la regola o
la protezione indicata (robots.txt, meta robots/X-Robots-Tag, regole WAF/anti-bot sui client automatici).
Verifica: la stessa prova è ripetuta ogni mese; l'esito per il Vostro ente è pubblicato come open data.

Modello {MODELLO}.
"""


def testo_anac(r: dict) -> str:
    return f"""A: Autorità Nazionale Anticorruzione — vigilanza sugli obblighi di trasparenza

Oggetto: segnalazione ai sensi dell'art. 45 d.lgs. 33/2013 — {r['denominazione']} (C.F. {r['cf']}):
sezione «Amministrazione trasparente» non indicizzabile (art. 9, comma 1)

Si segnala che la sezione «Amministrazione trasparente» dell'ente indicato non risulta accessibile ai motori
di ricerca o ai client automatici, in contrasto con l'art. 9, comma 1, del d.lgs. 33/2013.

{evidenze(r)}

L'URL della sezione è stato ricavato da: {r['at_provenienza']}. Per «anac-l190-*» deriva dall'URL del file XML
comunicato dall'ente all'Autorità ai sensi dell'art. 1, comma 32, L. 190/2012: {r.get('url_l190') or 'n.d.'}.
Si chiede di valutare l'esercizio dei poteri di vigilanza di cui all'art. 45 d.lgs. 33/2013.

Modello {MODELLO}.
"""


def prepara(c, run: str, giro: str, solo: list[str] | None = None) -> int:
    """PEC solo per violazioni pubblicate nel giro e, per i blocchi WAF/anti-bot, solo se confermati
    (due giri a >= 60 minuti). Si leggono i dati pubblicati, così la PEC dice esattamente ciò che è online."""
    import gzip
    from esporta import PUBBLICA, VIOLAZIONI
    base = LAVORO / "pec" / giro
    pec_ipa = dict(c.execute("SELECT cf, pec_ipa FROM enti"))
    enti = json.loads(gzip.decompress((PUBBLICA / "giri" / giro / "enti.json.gz").read_bytes()))["enti"]
    n = 0
    for r in enti:
        r["pec_ipa"] = pec_ipa.get(r["cf"], "")
        if r["esito"] not in VIOLAZIONI or (solo and r["cf"] not in solo):
            continue
        if r["esito"] == "bloccato da WAF/anti-bot" and r.get("conferma_blocco") != "confermato":
            continue
        d = base / r["cf"]
        (d / "allegati").mkdir(parents=True, exist_ok=True)
        det = json.loads(c.execute("SELECT dettaglio FROM esiti WHERE run=? AND cf=?", (run, r["cf"])).fetchone()[0])
        if r.get("robots_sha256") and _blob(r["robots_sha256"]).exists():
            shutil.copy2(_blob(r["robots_sha256"]), d / "allegati" / "robots.txt")
        for i, q in enumerate(det.get("richieste", [])):
            if q.get("archiviato") and _blob(q["sha256"]).exists():
                shutil.copy2(_blob(q["sha256"]), d / "allegati" / f"risposta-{i + 1}-{q['ua']}-http{q['status']}.html")
        (d / "allegati" / "evidenza.json").write_text(json.dumps({"ente": r, "prove": det}, ensure_ascii=False, indent=1), encoding="utf-8")
        (d / "ente.txt").write_text(testo_ente(r, r.get("pec_ipa", "")), encoding="utf-8")
        (d / "anac.txt").write_text(testo_anac(r), encoding="utf-8")
        with (d / "SHA256SUMS").open("w", encoding="utf-8") as fh:
            for f in sorted((d / "allegati").iterdir()):
                fh.write(f"{hashlib.sha256(f.read_bytes()).hexdigest()}  allegati/{f.name}\n")
        n += 1
    print(json.dumps({"pec_pronte": n, "cartella": str(base), "nota": "NESSUN INVIO: l'invio è manuale e va autorizzato"}))
    return n


def registra(cf: str, giro: str, destinatario: str, evento: str, indirizzo: str = "", id_messaggio: str = "",
             file: str = "", nota: str = "", data: str = "") -> dict:
    assert destinatario in ("ente", "anac") and evento in EVENTI
    sha_file = salva_blob(Path(file).read_bytes()) if file else ""
    sums = LAVORO / "pec" / giro / cf / "SHA256SUMS"
    sha_all = hashlib.sha256(sums.read_bytes()).hexdigest() if (evento == "invio" and sums.exists()) else ""
    rec = {"ts_registrazione": adesso(), "data_evento": data or adesso()[:10], "cf": cf, "giro": giro,
           "destinatario": destinatario, "evento": evento, "indirizzo": indirizzo, "modello": MODELLO if evento == "invio" else "",
           "id_messaggio": id_messaggio, "sha256_file": sha_file, "sha256_allegati": sha_all, "nota": nota}
    REGISTRO.parent.mkdir(parents=True, exist_ok=True)
    nuovo = not REGISTRO.exists()
    with REGISTRO.open("a", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPI_INVII)
        if nuovo:
            w.writeheader()
        w.writerow(rec)
    return rec


def stato_invii() -> dict:
    """cf -> {destinatario: {invio, accettazione, consegna, risposta, ultimo_evento}}"""
    out: dict = {}
    if not REGISTRO.exists():
        return out
    with REGISTRO.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            s = out.setdefault(r["cf"], {}).setdefault(r["destinatario"], {})
            s[r["evento"]] = r["data_evento"]
            s["ultimo_evento"] = r["evento"]
            s["giro"] = r["giro"] if r["evento"] == "invio" else s.get("giro", r["giro"])
    return out


def esporta_stato_invii(dest: Path):
    dest.write_text(json.dumps({"schema": "trasparenza.invii/1", "generato": adesso(), "invii": stato_invii()},
                               ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
