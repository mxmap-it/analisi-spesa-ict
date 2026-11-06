#!/usr/bin/env python3
"""Verifica deterministica degli esiti del giro imbuto G1/G3 (istruzioni p3) e registro spesaict.classificazione/1.

Regole (formato-classificazione.md § Confidenza, più quelle degli assi):
  R1 fonte_primaria solo se esiste un atto archiviato (dati/atti/atti-server.jsonl, sha256, esito ok) il cui testo cita il CIG;
  R2 «alta» senza fonte primaria né (provider nominato nell'oggetto + documento archiviato) scende a «media»;
  R3 campi mancanti o fuori vocabolario -> «bassa», stati -> «incerto»;
  R4 PSN senza servizio indicato -> giurisdizione «non-determinabile»;
  A1 asse A «incluso-certo» richiede confidenza «alta» dopo R1-R2, oppure «alta» del modello + oggetto con saas/iaas/paas/cloud; altrimenti «incerto»;
  A2 asse A «escluso-certo» richiede e_cloud = n, oggetto senza parole cloud e: confidenza «alta» (anche solo del modello) o servizio non ICT dichiarato (ict = n);
  B1 asse B «incluso-certo» richiede asse A «incluso-certo», provider, giurisdizione IT/UE/EXTRA-UE e confidenza «alta»;
  B2 asse A «escluso-certo» -> asse B «non-applicabile».
Tutte le classificazioni sono PROPOSTE: revisione.stato = «da-rivedere», «campione-controllo» se il CIG è nel campione 611.
Scrive report/metodo/llm/imbuto-g1g3/verificati.jsonl e dati/classificazioni/imbuto-g1g3.jsonl. Idempotente.
Uso: verifica_imbuto.py [cartella esiti]   (default report/metodo/llm/imbuto-g1g3/esiti; altre LLM: report/metodo/llm/riproduzione/esiti-<modello>)
"""
import json
import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]
B = R / "report/metodo/llm/imbuto-g1g3"
ATTI = R / "dati/atti/atti-server.jsonl"
CLOUD = re.compile(r"cloud|saas|iaas|paas|hosting|data ?center|psn|polo strategico|piattaforma", re.I)
NON_ICT = {"lavori-non-ict", "sanitario-non-ict", "altro", "hardware", "connettivita"}


def righe(p):
    fs = sorted(p.glob("*.jsonl")) if p.is_dir() else ([p] if p.exists() else [])
    for f in fs:
        for l in f.read_text(encoding="utf-8").splitlines():
            if l.strip():
                try:
                    yield json.loads(l)
                except json.JSONDecodeError:
                    pass


def testo_atti(lst):
    out = []
    for a in lst:
        f = R / "dati/atti/testi" / f"{a['sha256']}.txt"
        if f.exists():
            out.append(f.read_text(encoding="utf-8", errors="replace"))
    return " ".join(out)


def verifica(e, c, atti):
    A, Bx = dict(e.get("asse_a") or {}), dict(e.get("asse_b") or {})
    prima = {"confidenza": e.get("confidenza"), "fonte_primaria": e.get("fonte_primaria"), "asse_a": dict(A), "asse_b": dict(Bx)}
    docs = [a for a in atti if a.get("sha256") and a.get("esito_recupero") == "ok"]
    citato = [a for a in docs if a.get("pertinenza") == "cig-citato"]
    reg = []
    fp = bool(citato)
    if bool(e.get("fonte_primaria")) != fp:
        reg.append("R1")
    conf = e.get("confidenza")
    if conf not in ("alta", "media", "bassa") or A.get("stato") not in ("escluso-certo", "incluso-certo", "incerto"):
        conf = "bassa"; reg.append("R3"); A["stato"] = "incerto"
    if Bx.get("stato") not in ("incluso-certo", "incerto", "non-applicabile"):
        Bx["stato"] = "incerto"
    prov = (Bx.get("provider_prodotto") or "").strip()
    nominato = bool(prov) and any(re.search(r"\b" + re.escape(t) + r"\b", c["testo"], re.I) for t in re.split(r"[\s/(),]+", prov) if len(t) >= 3)
    if A.get("servizio") == "psn" and Bx.get("giurisdizione") != "non-determinabile":
        if not re.search(r"industry\s+standard|housing|hosting|secure\s+public\s+cloud|psn\s+managed|hybrid", c["testo"] + " " + testo_atti(citato), re.I):
            Bx["giurisdizione"] = "non-determinabile"; reg.append("R4")
            if conf == "alta":
                conf = "media"
    if conf == "alta" and not (fp or (nominato and docs)):
        conf = "media"; reg.append("R2")
    oggetto_cloud = bool(re.search(r"(saas|iaas|paas|cloud)", c["testo"], re.I))
    alta_modello = e.get("confidenza") == "alta"  # prima di R1-R2: per l asse A l oggetto univoco basta (istruzioni p3)
    if A["stato"] == "incluso-certo" and conf != "alta" and not (alta_modello and A.get("e_cloud") == "s" and oggetto_cloud):
        A["stato"] = "incerto"; reg.append("A1")
    if A["stato"] == "escluso-certo" and conf != "alta" and not (
            A.get("e_cloud") == "n" and not CLOUD.search(c["testo"]) and (alta_modello or (A.get("servizio") in NON_ICT and A.get("ict") == "n"))):
        A["stato"] = "incerto"; reg.append("A2")
    if A["stato"] == "escluso-certo":
        if Bx["stato"] != "non-applicabile":
            reg.append("B2")
        Bx["stato"] = "non-applicabile"
    elif Bx["stato"] == "incluso-certo" and not (
            A["stato"] == "incluso-certo" and prov and Bx.get("giurisdizione") in ("IT", "UE", "EXTRA-UE") and conf == "alta"):
        Bx["stato"] = "incerto"; reg.append("B1")
    v = dict(e, asse_a=A, asse_b=Bx, confidenza=conf, fonte_primaria=fp,
             verifica={"regole": reg, "prima": prima, "documenti_archiviati": len(docs), "documenti_cig_citato": len(citato),
                       "strumento": "tools/llm/verifica_imbuto.py"})
    return v, docs, citato


def main():
    esiti = Path(sys.argv[1]) if len(sys.argv) > 1 else B / "esiti"
    principale = esiti.resolve() == (B / "esiti").resolve()
    lotti = {c["cig"]: c for c in righe(B / "lotti")}
    atti = {}
    for a in righe(ATTI):
        if a.get("cig") in lotti:
            atti.setdefault(a["cig"], []).append(a)
    sel = json.loads((B / "selezione.json").read_text(encoding="utf-8"))
    ver, reg = [], []
    for e in righe(esiti):
        c = lotti.get(e.get("cig"))
        if not c:
            continue
        v, docs, citato = verifica(e, c, atti.get(c["cig"], []))
        ver.append(v)
        A, Bx, conf = v["asse_a"], v["asse_b"], v["confidenza"]
        passi = [{"n": 1, "tipo": "regola", "strumento": "tools/analisi/imbuto.py", "versione": "imbuto-0.3.1 (regole v3.1)",
                  "parametri": {"strato": "S6-residuo", "gruppo": c["gruppo"], "sottoclasse": c["sottoclasse"]}, "risultato": c["regole_v31"], "data": "2026-11-03"}]
        for p in e.get("passaggi") or []:
            if isinstance(p, dict):
                passi.append({"n": len(passi) + 1, "tipo": p.get("tipo", "modello"), "strumento": e.get("modello", ""), "versione": "istruzioni p3",
                              "parametri": {"query_o_url": p.get("query_o_url", "")}, "risultato": {"nota": p.get("risultato", "")}, "data": e.get("data")})
        for a in docs:
            passi.append({"n": len(passi) + 1, "tipo": "documento", "strumento": "tools/llm/atti.py", "versione": "1",
                          "parametri": {"url": a["url"], "livello": (a.get("trovato_con") or {}).get("livello")},
                          "risultato": {"sha256": a["sha256"], "pertinenza": a.get("pertinenza"), "estrazione": (a.get("estrazione") or {}).get("strumento")},
                          "data": (a.get("recuperato_il") or "")[:10]})
        passi.append({"n": len(passi) + 1, "tipo": "verifica", "strumento": "tools/llm/verifica_imbuto.py", "versione": "1", "parametri": {},
                      "risultato": {"regole_applicate": v["verifica"]["regole"], "asse_a": A["stato"], "asse_b": Bx["stato"], "confidenza": conf}, "data": e.get("data")})
        urls = {a["url"] for a in docs}
        reg.append({"schema": "spesaict.classificazione/1", "cig": c["cig"], "versione_metodo": "imbuto-0.3.1+via6-p3", "generato_il": f"{e.get('data')}T00:00:00Z",
                    "ingresso": {"fonte": {"dataset": "BDNCP/ANAC via lavoro/imbuto/ict.csv (imbuto-0.3.1)", "file": "report/metodo/llm/imbuto-g1g3/lotti",
                                           "sha256": sel["ingressi"]["ict.csv"]},
                                 "oggetto": c["testo"], "cpv": c["cpv"], "importo": c["importo"], "stazione_appaltante": c["ente"],
                                 "aggiudicatari": [x for x in re.split(r"\s*;\s*", c.get("aggiudicatari") or "") if x],
                                 "gruppo": c["gruppo"], "link_documenti_pvl": c["link_documenti"]},
                    "esito": {"e_cloud": A.get("e_cloud", ""), "servizio": A.get("servizio", ""), "provider_prodotto": (Bx.get("provider_prodotto") or ""),
                              "giurisdizione": Bx.get("giurisdizione") or "ignota", "via": "6-modello", "confidenza": conf, "fonte_primaria": v["fonte_primaria"],
                              "motivazione": e.get("motivazione", ""), "asse_a": A["stato"], "asse_b": Bx["stato"], "cloud_sovrano": None, "dipendenze_tecnologiche": []},
                    "passaggi": passi,
                    "fonti": [{"url": a["url"], "tipo": "atto-ente" if a in citato else "altro", "sha256": a["sha256"], "aperta": True} for a in docs]
                    + [{"url": u, "tipo": "altro", "sha256": "", "aperta": True} for u in (e.get("fonti") or []) if isinstance(u, str) and u not in urls],
                    "ostacoli": e.get("ostacoli") or [],
                    "revisione": {"stato": "campione-controllo" if c.get("controllo") else "da-rivedere", "nota": "proposta del modello, da revisionare"}})
    out_v = B / "verificati.jsonl" if principale else esiti.parent / (esiti.name + "-verificati.jsonl")
    out_v.write_text("".join(json.dumps(v, ensure_ascii=False) + "\n" for v in ver), encoding="utf-8")
    if principale:
        (R / "dati/classificazioni").mkdir(parents=True, exist_ok=True)
        (R / "dati/classificazioni/imbuto-g1g3.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in reg), encoding="utf-8")
    print(f"{len(ver)} esiti verificati, {sum(bool(v['verifica']['regole']) for v in ver)} corretti, fonte primaria {sum(v['fonte_primaria'] for v in ver)} -> {out_v}")


if __name__ == "__main__":
    main()
