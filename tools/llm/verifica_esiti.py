#!/usr/bin/env python3
"""Verifica deterministica degli esiti del modello: la confidenza dichiarata dall'agente non basta, va provata.

Per ogni esito del giro 2 applica le regole di sito/content/progetto/formato-classificazione.md (§ Confidenza):
  R1 fonte_primaria=true solo se in dati/atti/atti-server.jsonl c'è un documento archiviato (sha256) per quel CIG,
     recuperato con esito "ok" e il cui testo cita il CIG (pertinenza "cig-citato"). Altrimenti diventa false.
  R2 confidenza "alta" solo se: R1 vale, oppure il provider_prodotto è nominato nell'oggetto del contratto
     e c'è almeno un documento archiviato "ok" per quel CIG. Altrimenti scende a "media".
  R4 servizio PSN senza indicazione del servizio comprato (né nel testo né in un atto citante il CIG):
     giurisdizione "non-determinabile" e confidenza al massimo "media" (i servizi PSN vanno da IT a extra-UE).
  R3 confidenza mancante o fuori vocabolario -> "bassa"; campi obbligatori mancanti -> "bassa".
Scrive report/metodo/llm/giro2/verificati.jsonl con l'esito verificato e, in "verifica", le regole applicate e i valori prima/dopo.
Idempotente. Uso: verifica_esiti.py [cartella esiti]   (default report/metodo/llm/giro2/esiti)
"""
import json
import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]
ESITI = Path(sys.argv[1]) if len(sys.argv) > 1 else R / "report/metodo/llm/giro2/esiti"
ATTI = R / "dati/atti/atti-server.jsonl"
LOTTI = R / "report/metodo/llm/giro2/lotti"
OUT = R / "report/metodo/llm/giro2/verificati.jsonl"
OBBLIGATORI = ("cig", "e_cloud", "servizio", "giurisdizione", "confidenza")


def righe(p):
    for f in sorted(Path(p).glob("*.jsonl")) if Path(p).is_dir() else [Path(p)]:
        for l in f.read_text(encoding="utf-8").splitlines():
            if l.strip():
                try:
                    yield json.loads(l)
                except json.JSONDecodeError:
                    continue


atti = {}
for a in righe(ATTI) if ATTI.exists() else []:
    atti.setdefault(a["cig"], []).append(a)
oggetto = {c["cig"]: c.get("testo", "") for c in righe(LOTTI)}

out = []
for e in righe(ESITI):
    cig, prima = e.get("cig"), {k: e.get(k) for k in ("confidenza", "fonte_primaria")}
    docs = [a for a in atti.get(cig, []) if a.get("sha256") and a.get("esito_recupero") == "ok"]
    citato = [a for a in docs if a.get("pertinenza") == "cig-citato"]
    regole = []
    fp = bool(citato)
    if bool(e.get("fonte_primaria")) != fp:
        regole.append("R1")
    conf = e.get("confidenza")
    if conf not in ("alta", "media", "bassa") or any(not e.get(k) for k in OBBLIGATORI if k != "confidenza"):
        conf = "bassa"; regole.append("R3")
    prov = (e.get("provider_prodotto") or "").strip()
    nominato = bool(prov) and any(re.search(r"\b" + re.escape(t) + r"\b", oggetto.get(cig, ""), re.I)
                                  for t in re.split(r"[\s/(),]+", prov) if len(t) >= 3)
    testo_atti = " ".join((R / "dati/atti/testi" / (a["sha256"] + ".txt")).read_text(encoding="utf-8", errors="replace")
                         for a in citato if (R / "dati/atti/testi" / (a["sha256"] + ".txt")).exists())
    giur = e.get("giurisdizione")
    if e.get("servizio") == "psn" and giur != "non-determinabile" and not re.search(
            r"industrys+standard|housing|hosting|secures+publics+cloud|psns+managed|hybrids+cloud|alloy|assured", oggetto.get(cig, "") + " " + testo_atti, re.I):
        giur = "non-determinabile"; regole.append("R4")
        if conf == "alta":
            conf = "media"
    if conf == "alta" and not (fp or (nominato and docs)):
        conf = "media"; regole.append("R2")
    v = dict(e, fonte_primaria=fp, confidenza=conf, giurisdizione=giur,
             verifica={"regole": regole, "prima": {**prima, "giurisdizione": e.get("giurisdizione")}, "documenti_archiviati": len(docs), "documenti_cig_citato": len(citato),
                       "atti": [{"url": a["url"], "sha256": a["sha256"]} for a in citato], "strumento": "tools/llm/verifica_esiti.py"})
    out.append(v)
OUT.write_text("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in out), encoding="utf-8")
cambi = sum(1 for o in out if o["verifica"]["regole"])
print(f"{len(out)} esiti verificati, {cambi} corretti; fonte primaria provata: {sum(o['fonte_primaria'] for o in out)}")
