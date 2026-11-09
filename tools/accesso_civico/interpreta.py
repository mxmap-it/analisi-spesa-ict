#!/usr/bin/env python3
"""Interpretazione delle risposte degli enti alle richieste di accesso civico (#58, versione 0.1, 9/11/2026).

Specifica § 4.4, § 6, § 10. Ingresso: la richiesta (voci chieste), i NOMI degli allegati e il testo GIÀ REDATTO
(redazione.py) della risposta. Uscita:
1. un'interpretazione (esito, motivi art. 5-bis, voci fornite/non fornite, link, scadenze, richieste
   all'interessato, confidenza, citazioni) registrata in `spesaict.classificazione/1` (un record per voce con CIG,
   blocco `esito.accesso_civico`), con sha256 di ingresso e uscita, modello e versione delle istruzioni;
2. una PROPOSTA di evento per stati.py, MAI applicata: va nella coda «da-rivedere»; solo `rivedi --applica`,
   eseguito da una persona, scrive l'evento nel registro.

Due passate:
- regole deterministiche (parole chiave + allegati, `regole()`): rispondono solo quando un'unica famiglia di esito
  è riconosciuta senza segnali in conflitto; altrimenti si astengono;
- LLM (`claude -p` in abbonamento tramite tools/llm/claude_tetto.py, etichetta «accesso-civico-interpreta», istruzioni
  report/metodo/llm/accesso-civico-interpreta/istruzioni-v1.md) solo sul resto. Le citazioni sono ricontrollate alla
  lettera; senza citazioni valide la confidenza scende a «bassa».

Revisione umana (`revisione()` + `campione()`): obbligatoria per ogni esito diverso da «accolta», per confidenza non
alta, per citazioni non valide; tra le «accolta» ad alta confidenza almeno il 10 % per ondata (scelta deterministica:
sha256 dell'id richiesta, così il campione è riproducibile e non scelto a mano), in modalità cieca. Metrica:
`accordo()` (accordo percentuale e kappa di Cohen sull'esito, Jaccard sui motivi, matrice di confusione).

Uso:
  interpreta.py regole <caso.json>                           solo prima passata (stampa)
  interpreta.py interpreta <caso.json> [--modello haiku] [--coda F] [--classificazioni F]
  interpreta.py valuta <set.jsonl> [--modello haiku] [--llm-tutti] [--uscita F]
  interpreta.py rivedi <coda.jsonl> <id_proposta> --esito E --chi NOME [--applica eventi.jsonl]
Il caso è {"richiesta": {"id", "voci": [...]}, "allegati": [...], "testo": "...", "data": "AAAA-MM-GG"}.
"""
import argparse
import datetime as dt
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]
ISTRUZIONI = R / "report/metodo/llm/accesso-civico-interpreta/istruzioni-v1.md"
VERSIONE_ISTRUZIONI = "v1"
VERSIONE_REGOLE = "regole-0.1"
ETICHETTA = "accesso-civico-interpreta"
CODA = R / "lavoro/accesso-civico/code/da-rivedere.jsonl"
REVISIONI = R / "lavoro/accesso-civico/code/revisioni.jsonl"
CLASSIFICAZIONI = R / "dati/classificazioni/accesso-civico-interpreta.jsonl"
BLOBS = R / "lavoro/accesso-civico/blobs/sha256"

ESITI = ["accolta", "parziale", "diniego", "differimento", "chiarimento", "controinteressati", "rinvio-altro-ufficio",
         "già-pubblicato", "non-pertinente"]
MOTIVI = [f"5bis-c1-{x}" for x in "abcdefg"] + [f"5bis-c2-{x}" for x in "abc"] + ["5bis-c3"] + \
         ["massiva", "inesistente", "generica", "interesse", "altro", "non-motivato"]
CON_MOTIVO = {"diniego", "parziale", "differimento"}
QUOTA_CAMPIONE = 0.10


def sha(x):
    if isinstance(x, str):
        x = x.encode("utf-8")
    return hashlib.sha256(x).hexdigest()


def canonico(caso):
    """Ingresso canonico (ciò che entra nell'interpretazione): il suo sha256 è input_sha256."""
    return json.dumps({"richiesta": caso["richiesta"], "allegati": caso.get("allegati") or [], "testo": caso["testo"]},
                      ensure_ascii=False, sort_keys=True)


def _n(s):
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


# ---------------------------------------------------------------- prima passata: regole
FAMIGLIE = {
    "non-pertinente": [r"generato automaticamente", r"abilitata alla sola ricezione", r"non rispondere a questo messaggio",
                       r"(?:è stata|risulta) protocollat[ao]"],
    "controinteressati": [r"controinteressat"],
    "differimento": [r"\bdifferit[oaie]\b", r"\bdifferimento\b"],
    "rinvio-altro-ufficio": [r"inoltrat[ao],? (?:.{0,60})?per competenza", r"\bnon (?:è|risulta|siamo) competent",
                             r"rivolgere (?:l'|la )?(?:istanza|richiesta) a"],
    "già-pubblicato": [r"già (?:stat[ie] )?pubblicat"],
    "chiarimento": [r"si chiede (?:cortesemente |gentilmente )?di (?:voler )?(?:meglio )?(?:precisare|specificare|chiarire|"
                    r"confermare|integrare|trasmettere copia di un documento)", r"documento di (?:identità|riconoscimento)"],
    "diniego": [r"\bdiniego\b", r"\bsi rigetta\b", r"\bè rigettat[ao]", r"non può essere accolt[ao]",
                r"non può essere consentit[ao]", r"\binammissibil", r"non è possibile dar(?:e)? corso",
                r"non (?:può essere|è) ostensibil", r"\bsi respinge\b"],
}
TRASMISSIONE = [r"\bsi trasmett", r"\bsi allega", r"\bin allegato\b", r"\ble inviamo\b", r"\bscaricabil", r"\bè accolta\b",
                r"\bsi accoglie\b", r"\bsi invia\b"]
PARZIALE = [r"parzialmente", r"oscurament", r"\bnon (?:è |sono )?detenut", r"\bnon (?:può essere|è) ostensibil"]
URL = re.compile(r"https?://[^\s<>\"]+[^\s<>\".,;)]")

MOTIVI_REGEX = [
    (r"(?:sicurezza|ordine) pubblic", "5bis-c1-a"), (r"sicurezza nazionale", "5bis-c1-b"),
    (r"difesa e (?:le )?questioni militari", "5bis-c1-c"), (r"relazioni internazionali", "5bis-c1-d"),
    (r"stabilità finanziaria", "5bis-c1-e"), (r"indagini sui reati", "5bis-c1-f"), (r"attività ispettiv", "5bis-c1-g"),
    (r"protezione dei dati personali", "5bis-c2-a"), (r"segretezza della corrispondenza", "5bis-c2-b"),
    (r"interessi economici e commerciali|segreti? commercial|proprietà intellettuale", "5bis-c2-c"),
    (r"segreto di stato|art\. ?53 del d\.?lgs\.? ?(?:n\. ?)?50|art\. ?35 del d\.?lgs\.? ?(?:n\. ?)?36|art\. ?24,? comma 1", "5bis-c3"),
    (r"massiv|manifestamente irragionevol", "massiva"), (r"\bnon (?:è |sono )?detenut|\bnon esist", "inesistente"),
    (r"\bgeneric[ao]\b|esplorativ", "generica"), (r"interesse diretto|interesse (?:concreto|qualificato)", "interesse"),
]
ART5BIS = re.compile(r"5-?\s?bis,?\s*(?:comma|c\.)\s*(\d)(?:,?\s*(?:lett\.|lettera)\s*([a-g])\))?")


def motivi_da_testo(t):
    t = _n(t)
    m = set()
    for c, l in ART5BIS.findall(t):
        cod = f"5bis-c{c}-{l}" if l else f"5bis-c{c}"
        if cod in MOTIVI:
            m.add(cod)
    for rx, cod in MOTIVI_REGEX:
        if re.search(rx, t):
            m.add(cod)
    return sorted(m)


def _trovati(t, rxs):
    return [rx for rx in rxs if re.search(rx, t)]


def regole(caso):
    """Prima passata. Restituisce (interpretazione | None, traccia). None = astensione (va all'LLM)."""
    # l'oggetto/riferimento all'istanza ripete il nostro testo: le regole guardano il resto
    t = _n(re.sub(r"(?im)^\s*(?:oggetto|rif\.?|riferimento)\s*:.*$", "", caso["testo"]))
    allegati = caso.get("allegati") or []
    link = URL.findall(caso["testo"])
    fam = {f: _trovati(t, rxs) for f, rxs in FAMIGLIE.items()}
    fam = {f: v for f, v in fam.items() if v}
    tr, pz = _trovati(t, TRASMISSIONE), _trovati(t, PARZIALE)
    traccia = {"versione": VERSIONE_REGOLE, "famiglie": fam, "trasmissione": tr, "parziale": pz,
               "allegati": len(allegati), "link": len(link)}
    esito = None
    consegna = bool(allegati) or bool(link)
    if tr and consegna:
        altre = set(fam) - {"diniego"}
        if not altre:
            esito = "parziale" if (pz or "diniego" in fam) else "accolta"
    elif not tr:
        if len(fam) == 1:
            esito = next(iter(fam))
            if esito == "già-pubblicato" and (allegati or not link):
                esito = None
            if esito == "non-pertinente" and len(t) > 400:
                esito = None  # un testo lungo con solo l'avviso di protocollo può contenere altro
    traccia["decisione"] = esito or "astensione"
    if not esito:
        return None, traccia
    voci = [v["id"] for v in caso["richiesta"]["voci"]]
    mot = motivi_da_testo(t) if esito in CON_MOTIVO else []
    if esito == "diniego" and not mot:
        mot = ["non-motivato"]
    if esito == "parziale":
        return None, dict(traccia, decisione="astensione", nota="parziale: la ripartizione per voce la fa l'LLM")
    out = {"esito": esito, "motivi": mot, "motivo_testo": "", "voci_fornite": [], "voci_non_fornite": [],
           "link_pubblicazioni": link, "scadenze": [], "richieste_all_interessato": [], "confidenza": "alta",
           "citazioni": [], "note": "regole " + VERSIONE_REGOLE}
    if esito == "accolta":
        out["voci_fornite"] = [{"voce": v, "documenti": allegati or link, "oscurato": False} for v in voci]
    elif esito == "diniego":
        out["voci_non_fornite"] = [{"voce": v, "motivo": mot[0]} for v in voci]
    # citazioni: le frasi che contengono i segnali (alla lettera dal testo originale)
    frasi = re.split(r"(?<=[.;])\s+", caso["testo"])
    segnali = (fam.get(esito) or []) + (tr if esito == "accolta" else [])
    out["citazioni"] = [f.strip() for f in frasi if any(re.search(rx, _n(f)) for rx in segnali)][:3]
    return out, traccia


# ---------------------------------------------------------------- seconda passata: LLM
def prompt(caso):
    voci = [{k: v.get(k) for k in ("id", "cig", "oggetto", "documento_atteso")} for v in caso["richiesta"]["voci"]]
    return (ISTRUZIONI.read_text(encoding="utf-8") + "\n\n---\nRICHIESTA: " +
            json.dumps({"id": caso["richiesta"]["id"], "voci": voci}, ensure_ascii=False) +
            "\nALLEGATI: " + json.dumps(caso.get("allegati") or [], ensure_ascii=False) +
            "\nRISPOSTA:\n<<<\n" + caso["testo"] + "\n>>>\n")


class TettoRaggiunto(RuntimeError):
    pass


def chiama_llm(testo, modello):
    p = subprocess.run([sys.executable, str(R / "tools/llm/claude_tetto.py"), "--progetto", "analisi-spesa-ict", "--",
                        "claude", "-p", "--model", modello, "--allowedTools", ""], input=testo, capture_output=True,
                       text=True, encoding="utf-8", env=dict(os.environ, TETTO_ETICHETTA=ETICHETTA))
    if p.returncode == 75:
        raise TettoRaggiunto(p.stderr.strip())
    if p.returncode != 0:
        raise RuntimeError(f"claude -p codice {p.returncode}: {p.stderr[-400:]}")
    return p.stdout


def analizza_uscita(grezza, caso):
    """JSON dell'LLM -> (interpretazione normalizzata, errori). Le citazioni si ricontrollano alla lettera."""
    err = []
    m = re.search(r"\{.*\}", grezza or "", re.S)
    try:
        o = json.loads(m.group(0)) if m else None
    except json.JSONDecodeError:
        o = None
    if not isinstance(o, dict):
        return None, ["uscita non JSON"]
    if o.get("esito") not in ESITI:
        err.append(f"esito fuori vocabolario: {o.get('esito')}")
    o["motivi"] = sorted({x for x in (o.get("motivi") or []) if x in MOTIVI})
    ids = {v["id"] for v in caso["richiesta"]["voci"]}
    for k in ("voci_fornite", "voci_non_fornite"):
        o[k] = [x for x in (o.get(k) or []) if isinstance(x, dict) and x.get("voce") in ids]
    for k in ("link_pubblicazioni", "scadenze", "richieste_all_interessato", "citazioni"):
        o.setdefault(k, [])
    if o.get("confidenza") not in ("alta", "media", "bassa"):
        o["confidenza"] = "bassa"
    t = _n(caso["testo"])
    valide = [bool(_n(c)) and _n(c) in t for c in o["citazioni"] if isinstance(c, str)]
    o["citazioni_valide"] = bool(valide) and all(valide)
    if not o["citazioni_valide"]:
        err.append("citazioni assenti o non letterali")
        o["confidenza"] = "bassa"
    return o, err


def salva_blob(testo, radice=BLOBS):
    h = sha(testo)
    p = radice / h[:2] / h[2:4] / h
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(testo, encoding="utf-8")
    return h


def interpreta(caso, modello="haiku", llm=None, sempre_llm=False, blob=True):
    """Restituisce {interpretazione, fonte, passaggi, input_sha256, ...}. `llm` sostituisce la chiamata (test)."""
    ingresso = canonico(caso)
    passaggi = []
    r, traccia = regole(caso)
    passaggi.append({"n": 1, "tipo": "regola", "strumento": "tools/accesso_civico/interpreta.py",
                     "versione": VERSIONE_REGOLE, "parametri": traccia, "risultato": {"esito": r and r["esito"]}})
    out = {"input_sha256": sha(ingresso), "regole": r, "fonte": "regole", "interpretazione": r, "errori": []}
    if r is None or sempre_llm:
        testo = prompt(caso)
        grezza = (llm or chiama_llm)(testo, modello) if llm is not False else None
        if grezza is None:
            out.update(fonte="nessuna", interpretazione=None, errori=["LLM non eseguito"])
            return dict(out, passaggi=passaggi)
        o, err = analizza_uscita(grezza, caso)
        osha = salva_blob(grezza) if blob else sha(grezza)
        passaggi.append({"n": 2, "tipo": "modello", "strumento": f"claude-cli/{modello}", "versione": f"istruzioni-{VERSIONE_ISTRUZIONI}",
                         "parametri": {"prompt_sha256": sha(ISTRUZIONI.read_bytes()), "input_sha256": out["input_sha256"],
                                       "richiesta_llm_sha256": sha(testo), "etichetta": ETICHETTA},
                         "risultato": {"output_sha256": osha, "esito": o and o.get("esito"), "errori": err}})
        out.update(fonte="modello", interpretazione=o, errori=err, modello=modello, output_sha256=osha, llm=o)
        if r is not None and o and r["esito"] != o.get("esito"):
            out["disaccordo_regole_llm"] = True
            o["confidenza"] = "bassa"
    return dict(out, passaggi=passaggi)


# ---------------------------------------------------------------- proposta di evento, revisione, campione
def evento_proposto(interp, id_richiesta, data):
    """Esito -> evento di stati.py (o None) + coda di lavoro (specifica § 10.2). Non viene mai applicato qui."""
    e = interp["esito"]
    dati, tipo, coda = {}, None, "esame-risposta"
    fornite = [x["voce"] for x in interp.get("voci_fornite") or []]
    negate = [x["voce"] for x in interp.get("voci_non_fornite") or []]
    if e in ("accolta", "parziale", "diniego", "già-pubblicato", "differimento"):
        tipo = "risposta"
        dati["esito"] = {"già-pubblicato": "accolta", "differimento": "diniego"}.get(e, e)
        if fornite:
            dati["voci_rilasciate"] = fornite
        if negate:
            dati["voci_negate"] = negate
        if interp.get("motivi"):
            dati["limite_5bis"] = ",".join(interp["motivi"]) + (" (differimento art. 5-bis c. 5)" if e == "differimento" else "")
        if e in ("parziale", "diniego", "differimento"):
            coda = "seguito"
    elif e == "chiarimento":
        tipo, coda = "richiesta-chiarimento", "chiarimento"
        if any(re.search(r"identit|riconoscimento", x, re.I) for x in interp.get("richieste_all_interessato") or []):
            coda = "documento-richiesto"
    elif e == "controinteressati":
        tipo, coda = "comunicazione-controinteressati", "controinteressati"
    elif e == "rinvio-altro-ufficio":
        coda = "abbinamento"  # nessun cambio di stato: il termine continua a decorrere
    elif e == "non-pertinente":
        coda = "abbinamento"
    ev = None
    if tipo:
        ev = {"formato": "spesaict.accesso-civico-evento/1", "id_richiesta": id_richiesta, "tipo": tipo, "data": data,
              "dati": dati, "chi": "<da compilare alla revisione>",
              "note": f"proposto da interpreta.py ({e}); non applicato"}
    return ev, coda


def revisione(interp, fonte_errori=(), disaccordo=False):
    """Revisione obbligatoria o no (prima del campione). Restituisce (obbligatoria, motivo)."""
    if interp is None:
        return True, "nessuna interpretazione"
    if interp["esito"] != "accolta":
        return True, f"esito {interp['esito']}: revisione al 100 %"
    if interp.get("confidenza") != "alta":
        return True, f"confidenza {interp.get('confidenza')}"
    if disaccordo:
        return True, "regole e LLM in disaccordo"
    if fonte_errori:
        return True, "; ".join(fonte_errori)
    return False, "accolta ad alta confidenza"


def campione(ids, quota=QUOTA_CAMPIONE):
    """Sottoinsieme deterministico (sha256 dell'id) di almeno ceil(quota*n) elementi, minimo 1 se n>0."""
    ids = sorted(set(ids))
    k = math.ceil(quota * len(ids)) if ids else 0
    return set(sorted(ids, key=lambda i: sha("campione|" + i))[:k])


def accordo(coppie):
    """coppie: [(proposto, umano)] di esiti (o dict con esito/motivi). Accordo %, kappa di Cohen, confusione, Jaccard motivi."""
    if not coppie:
        return {"n": 0}
    es = lambda x: x["esito"] if isinstance(x, dict) else x
    a = [(es(p), es(u)) for p, u in coppie]
    n = len(a)
    po = sum(p == u for p, u in a) / n
    cat = sorted({x for c in a for x in c})
    pe = sum((sum(p == c for p, _ in a) / n) * (sum(u == c for _, u in a) / n) for c in cat)
    kappa = (po - pe) / (1 - pe) if pe < 1 else 1.0
    conf = {}
    for p, u in a:
        conf.setdefault(u, {}).setdefault(p, 0)
        conf[u][p] += 1
    jac = []
    for p, u in coppie:
        if isinstance(p, dict) and isinstance(u, dict) and (p.get("motivi") or u.get("motivi")):
            sp, su = set(p.get("motivi") or []), set(u.get("motivi") or [])
            jac.append(len(sp & su) / len(sp | su))
    return {"n": n, "accordo": round(po, 4), "kappa": round(kappa, 4), "jaccard_motivi": round(sum(jac) / len(jac), 4) if jac else None,
            "n_motivi": len(jac), "confusione_umano_x_proposto": conf}


# ---------------------------------------------------------------- registrazione
def record_classificazione(caso, ris, quando=None):
    """Un record spesaict.classificazione/1 per voce con CIG valido (le voci senza CIG restano nella proposta)."""
    i = ris["interpretazione"] or {}
    quando = quando or dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    fornite = {x["voce"]: x for x in i.get("voci_fornite") or []}
    negate = {x["voce"]: x for x in i.get("voci_non_fornite") or []}
    out = []
    for v in caso["richiesta"]["voci"]:
        if not re.fullmatch(r"[0-9A-Z]{10}", v.get("cig") or ""):
            continue
        ev = "fornita" if v["id"] in fornite else "non-fornita" if v["id"] in negate else "non-determinata"
        out.append({
            "schema": "spesaict.classificazione/1", "cig": v["cig"], "versione_metodo": f"accesso-civico-interpreta-{VERSIONE_ISTRUZIONI}+{VERSIONE_REGOLE}",
            "generato_il": quando,
            "ingresso": {"fonte": {"dataset": "accesso-civico-risposta", "file": caso["richiesta"]["id"], "sha256": ris["input_sha256"]},
                         "oggetto": v.get("oggetto", "")},
            "esito": {"accesso_civico": {"id_richiesta": caso["richiesta"]["id"], "voce": v["id"], "esito": i.get("esito"),
                                         "esito_voce": ev, "motivi": i.get("motivi") or [],
                                         "motivo_voce": (negate.get(v["id"]) or {}).get("motivo"),
                                         "documenti": (fornite.get(v["id"]) or {}).get("documenti") or [],
                                         "link_pubblicazioni": i.get("link_pubblicazioni") or [], "scadenze": i.get("scadenze") or [],
                                         "richieste_all_interessato": i.get("richieste_all_interessato") or [],
                                         "citazioni": i.get("citazioni") or [], "fonte": ris["fonte"],
                                         "modello": ris.get("modello"), "prompt_versione": VERSIONE_ISTRUZIONI,
                                         "prompt_sha256": sha(ISTRUZIONI.read_bytes()), "input_sha256": ris["input_sha256"],
                                         "output_sha256": ris.get("output_sha256")},
                      "confidenza": i.get("confidenza", "bassa"), "via": "AC-" + ris["fonte"],
                      "motivazione": i.get("motivo_testo") or ""},
            "passaggi": ris["passaggi"], "revisione": {"stato": "da-rivedere"}})
    return out


def accoda(caso, ris, coda=CODA, data=None, chi="interpreta.py"):
    i = ris["interpretazione"]
    data = data or caso.get("data") or dt.date.today().isoformat()
    ev, nome_coda = evento_proposto(i, caso["richiesta"]["id"], data) if i else (None, "esame-risposta")
    obbl, motivo = revisione(i, ris.get("errori"), ris.get("disaccordo_regole_llm", False))
    prop = {"formato": "spesaict.accesso-civico-proposta/1", "id": "pr-" + ris["input_sha256"][:16],
            "id_richiesta": caso["richiesta"]["id"], "registrato": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "chi": chi, "input_sha256": ris["input_sha256"], "fonte": ris["fonte"], "esito": i and i["esito"],
            "confidenza": i and i.get("confidenza"), "coda": nome_coda, "stato": "da-rivedere",
            "revisione": "obbligatoria" if obbl else "da-campionare", "motivo_revisione": motivo, "evento_proposto": ev}
    coda.parent.mkdir(parents=True, exist_ok=True)
    gia = {json.loads(l)["id"] for l in coda.read_text(encoding="utf-8").splitlines() if l.strip()} if coda.exists() else set()
    if prop["id"] not in gia:  # idempotente: stesso ingresso, stessa proposta
        with coda.open("a", encoding="utf-8") as f:
            f.write(json.dumps(prop, ensure_ascii=False) + "\n")
    return prop


def assegna_campione(proposte):
    """Per un'ondata: le «da-campionare» diventano campione-controllo (≥10 %, cieco) o conferma-in-blocco."""
    dc = [p for p in proposte if p["revisione"] == "da-campionare"]
    scelti = campione([p["id_richiesta"] for p in dc])
    for p in dc:
        p["revisione"] = "campione-controllo" if p["id_richiesta"] in scelti else "conferma-in-blocco"
    return proposte


# ---------------------------------------------------------------- comandi
def _carica(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]


def valuta(percorso, modello="haiku", llm_tutti=False, uscita=None, llm=None, cartella_grezze=None):
    """Valuta regole e LLM sul set sintetico. Ripartibile: le uscite grezze già salvate non si richiedono."""
    casi = _carica(percorso)
    cartella_grezze = Path(cartella_grezze or R / f"report/metodo/llm/accesso-civico-interpreta/valutazione/{modello}")
    righe, fermato = [], None
    for c in casi:
        r, _ = regole(c)
        riga = {"id": c["id"], "atteso": c["atteso"]["esito"], "motivi_attesi": c["atteso"].get("motivi", []),
                "regole": r and r["esito"], "motivi_regole": r and r["motivi"]}
        if (r is None or llm_tutti) and not fermato:
            f = cartella_grezze / f"{c['id']}.txt"
            if f.exists():
                grezza = f.read_text(encoding="utf-8")
            else:
                try:
                    grezza = (llm or chiama_llm)(prompt(c), modello)
                except TettoRaggiunto as x:
                    fermato, grezza = str(x), None
                if grezza is not None:
                    f.parent.mkdir(parents=True, exist_ok=True)
                    f.write_text(grezza, encoding="utf-8")
            if grezza is not None:
                o, err = analizza_uscita(grezza, c)
                riga.update(llm=o and o.get("esito"), motivi_llm=o and o.get("motivi"), confidenza_llm=o and o.get("confidenza"),
                            errori_llm=err, output_sha256=sha(grezza))
        riga["finale"] = riga["regole"] or riga.get("llm")
        righe.append(riga)
    cop = [x for x in righe if x["regole"]]
    con_llm = [x for x in righe if x.get("llm")]
    fin = [x for x in righe if x["finale"]]
    ris = {"set": str(percorso), "set_sha256": sha(Path(percorso).read_bytes()), "n": len(casi), "modello": modello,
           "istruzioni": VERSIONE_ISTRUZIONI, "regole": VERSIONE_REGOLE, "quando": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
           "regole_copertura": f"{len(cop)}/{len(casi)}",
           "regole_accuratezza": accordo([(x["regole"], x["atteso"]) for x in cop]).get("accordo"),
           "llm_valutati": len(con_llm),
           "llm": accordo([({"esito": x["llm"], "motivi": x["motivi_llm"]}, {"esito": x["atteso"], "motivi": x["motivi_attesi"]}) for x in con_llm]),
           "pipeline": accordo([(x["finale"], x["atteso"]) for x in fin]), "pipeline_valutati": len(fin),
           "fermato_dal_tetto": fermato, "righe": righe}
    if uscita:
        Path(uscita).parent.mkdir(parents=True, exist_ok=True)
        Path(uscita).write_text(json.dumps(ris, ensure_ascii=False, indent=1), encoding="utf-8")
    return ris


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("regole"); a.add_argument("caso")
    a = sp.add_parser("interpreta"); a.add_argument("caso"); a.add_argument("--modello", default="haiku")
    a.add_argument("--coda", default=str(CODA)); a.add_argument("--classificazioni", default=str(CLASSIFICAZIONI))
    a = sp.add_parser("valuta"); a.add_argument("set"); a.add_argument("--modello", default="haiku")
    a.add_argument("--llm-tutti", action="store_true"); a.add_argument("--uscita")
    a = sp.add_parser("rivedi"); a.add_argument("coda"); a.add_argument("id"); a.add_argument("--esito", required=True, choices=ESITI)
    a.add_argument("--chi", required=True); a.add_argument("--modalita", default="cieca", choices=["cieca", "assistita"])
    a.add_argument("--applica", help="registro eventi.jsonl: scrive l'evento confermato (solo persona)")
    x = ap.parse_args(argv)
    if x.cmd == "regole":
        print(json.dumps(regole(json.loads(Path(x.caso).read_text(encoding="utf-8"))), ensure_ascii=False, indent=1))
    elif x.cmd == "interpreta":
        caso = json.loads(Path(x.caso).read_text(encoding="utf-8"))
        try:
            ris = interpreta(caso, x.modello)
        except TettoRaggiunto as e:
            print(f"tetto raggiunto, riprovare più tardi: {e}", file=sys.stderr)
            return 75
        recs = record_classificazione(caso, ris)
        p = Path(x.classificazioni); p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("a", encoding="utf-8") as f:
            for r in recs:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(json.dumps(accoda(caso, ris, Path(x.coda)), ensure_ascii=False, indent=1))
    elif x.cmd == "valuta":
        ris = valuta(x.set, x.modello, x.llm_tutti, x.uscita)
        print(json.dumps({k: v for k, v in ris.items() if k != "righe"}, ensure_ascii=False, indent=1))
        return 75 if ris["fermato_dal_tetto"] else 0
    elif x.cmd == "rivedi":
        if x.chi.lower() in ("interpreta.py", "agente", "claude", "sistema"):
            raise SystemExit("la revisione la fa una persona")
        prop = next((p for p in _carica(x.coda) if p["id"] == x.id), None)
        if not prop:
            raise SystemExit(f"proposta {x.id} non trovata")
        rev = {"formato": "spesaict.accesso-civico-revisione/1", "proposta": x.id, "id_richiesta": prop["id_richiesta"],
               "esito_proposto": prop["esito"], "esito_umano": x.esito, "concorda": prop["esito"] == x.esito, "chi": x.chi,
               "modalita": x.modalita, "registrato": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
        REVISIONI.parent.mkdir(parents=True, exist_ok=True)
        with REVISIONI.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rev, ensure_ascii=False) + "\n")
        if x.applica:
            sys.path.insert(0, str(Path(__file__).parent))
            import stati
            ev = prop["evento_proposto"]
            if x.esito != prop["esito"]:
                raise SystemExit("esito corretto: scrivere l'evento a mano (la proposta non vale più)")
            if not ev:
                raise SystemExit("nessun evento da applicare per questo esito")
            ev = dict(ev, chi=x.chi, note=ev["note"].replace("non applicato", f"confermato da {x.chi}"))
            stati.aggiungi(x.applica, ev)
        print(json.dumps(rev, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
