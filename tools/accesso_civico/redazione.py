#!/usr/bin/env python3
"""Redazione della versione PUBBLICA di richieste, eventi e testi dell'accesso civico (#58, versione 0.1, 9/11/2026).

Specifica § 5.4-5.5. Si rimuovono:
- dati del richiedente: documento d'identità, firma, codice fiscale, indirizzo, telefono; la PEC personale salvo
  `template.pec_richiedente_pubblica = true` nella campagna (decisione aperta di Fabio: default NON pubblica);
- dati personali di terzi nel testo: codici fiscali di persona fisica, IBAN, email non istituzionali, telefoni;
- negli eventi: `documento.percorso` (archivio privato), `chi` se non è un agente/strumento, il testo dei
  controinteressati (solo data ed esito), `note` libere ripulite con le stesse regole.

Si conservano: nome del richiedente (in pubblico solo il nome, § 3.2), dati dell'ente (CF numerico a 11 cifre, PEC
istituzionale), CIG, importi, date, esiti, sha256.

Il rilevamento è a regole (regex); i nomi di persone fisiche di terzi nei documenti ricevuti NON sono rilevati qui
(servono LLM + revisione umana, § 5.5 punto 1): `residui()` è il controllo finale che l'output pubblico non contenga
CF/IBAN/email/telefoni personali; `pubblica.py` si ferma se trova residui.
"""
import copy
import re

SEGNAPOSTO = {"cf": "[CF OSCURATO]", "iban": "[IBAN OSCURATO]", "email": "[EMAIL OSCURATA]",
              "telefono": "[TELEFONO OSCURATO]", "pec_richiedente": "[PEC DEL RICHIEDENTE, non pubblicata]",
              "firma": "[firma del richiedente, non pubblicata]",
              "documento": "[allegato documento d'identità, non pubblicato]"}

# codice fiscale di persona fisica (16 caratteri, con omocodie); quello degli enti è numerico a 11 cifre e resta
CF_PF = re.compile(r"\b[A-Z]{6}[0-9LMNPQRSTUV]{2}[ABCDEHLMPRST][0-9LMNPQRSTUV]{2}[A-Z][0-9LMNPQRSTUV]{3}[A-Z]\b", re.I)
IBAN = re.compile(r"\b[A-Z]{2}\d{2}(?:[ ]?[A-Z0-9]){11,30}\b")
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
# telefoni italiani (non dopo «AIC», codice farmaco a 9 cifre): fissi (0...) e mobili (3..), con prefisso +39/0039 facoltativo e separatori spazio . - /
TELEFONO = re.compile(r"(?<!AIC )(?<!AIC: )(?<!AIC n\. )(?<![\w/.-])(?:(?:\+|00)39[ .-]?)?(?:3\d{2}|0\d{1,3})[ ./-]?\d{3,4}[ .-]?\d{3,4}(?!\w)(?![.,]\d)(?!\s*(?:€|euro|EUR))")
# i CIG (10 caratteri con lettere) non corrispondono; gli importi «1.234.567» sì solo se iniziano per 0 o 3: per
# questo gli importi si scrivono sempre con «€» e i campi numerici non passano dalla redazione del testo.
AGENTI = {"bozze.py", "pec.py", "pubblica.py", "stati.py", "agente", "claude", "sistema"}


def _email_ok(addr, consentite):
    a = addr.lower()
    return a in consentite


def redigi_testo(testo, consentite=(), richiedente=None, pec_pubblica=False):
    """Restituisce (testo_redatto, conteggi). `consentite`: email istituzionali pubblicabili (PEC dell'ente)."""
    if not testo:
        return testo, {}
    cons = {e.lower() for e in consentite if e}
    rich = richiedente or {}
    n = {"cf": 0, "iban": 0, "email": 0, "telefono": 0, "pec_richiedente": 0, "firma": 0}
    t = testo
    if rich.get("firma"):
        n["firma"] = t.count(rich["firma"])
        t = t.replace(rich["firma"], SEGNAPOSTO["firma"])
    for campo in ("codice_fiscale", "indirizzo", "telefono", "documento"):
        v = rich.get(campo)
        if v and v in t:
            n[campo] = t.count(v)
            t = t.replace(v, SEGNAPOSTO.get(campo, "[DATO DEL RICHIEDENTE OSCURATO]"))
    pec_r = (rich.get("pec") or "").lower()
    if pec_r and not pec_pubblica:
        k = len(re.findall(re.escape(pec_r), t, re.I))
        n["pec_richiedente"] = k
        t = re.sub(re.escape(pec_r), SEGNAPOSTO["pec_richiedente"], t, flags=re.I)
    elif pec_r:
        cons.add(pec_r)

    def em(m):
        if _email_ok(m.group(0), cons):
            return m.group(0)
        n["email"] += 1
        return SEGNAPOSTO["email"]
    t = EMAIL.sub(em, t)

    def cf(m):
        n["cf"] += 1
        return SEGNAPOSTO["cf"]
    t = CF_PF.sub(cf, t)

    def iban(m):
        if not _iban_valido(m.group(0).replace(" ", "")):
            return m.group(0)
        n["iban"] += 1
        return SEGNAPOSTO["iban"]
    t = IBAN.sub(iban, t)

    def tel(m):
        if not _e_telefono(m.group(0)):
            return m.group(0)
        n["telefono"] += 1
        return SEGNAPOSTO["telefono"]
    t = TELEFONO.sub(tel, t)
    return t, {k: v for k, v in n.items() if v}


def _e_telefono(s):
    """Almeno 8 cifre. Senza separatori conta solo la forma tipica: cellulare 3xx a 10 cifre, fisso 0x a 8-10 cifre;
    così un CF/partita IVA di ente (11 cifre) o un importo in un CSV (es. 324571809) non sono telefoni."""
    cifre = re.sub(r"\D", "", s)
    if s.isdigit():
        return (s[0] == "3" and len(s) == 10) or (s[0] == "0" and 8 <= len(s) <= 10)
    return len(cifre) >= 8


def _iban_valido(s):
    s = s.upper()
    r = s[4:] + s[:4]
    try:
        return int("".join(str(int(c, 36)) for c in r)) % 97 == 1
    except ValueError:
        return False


def residui(testo, consentite=(), richiedente=None, pec_pubblica=False):
    """Elenco dei dati personali ancora presenti (vuoto = ok). Stesse regole di redigi_testo, senza sostituire."""
    out = []
    if not testo:
        return out
    cons = {e.lower() for e in consentite if e}
    rich = richiedente or {}
    if pec_pubblica and rich.get("pec"):
        cons.add(rich["pec"].lower())
    for campo in ("firma", "codice_fiscale", "indirizzo", "telefono", "documento", "pec"):
        v = rich.get(campo)
        if v and (campo != "pec" or not pec_pubblica) and v.lower() in testo.lower():
            out.append(f"richiedente.{campo}")
    out += [f"cf:{m.group(0)}" for m in CF_PF.finditer(testo)]
    out += [f"email:{m.group(0)}" for m in EMAIL.finditer(testo) if m.group(0).lower() not in cons]
    out += [f"iban:{m.group(0)}" for m in IBAN.finditer(testo) if _iban_valido(m.group(0).replace(" ", ""))]
    out += [f"telefono:{m.group(0)}" for m in TELEFONO.finditer(testo) if _e_telefono(m.group(0))]
    return out


def redigi_richiesta(rec, campagna=None):
    """Versione pubblica di una richiesta (spesaict.accesso-civico-richiesta/1)."""
    pub = copy.deepcopy(rec)
    pec_ente = (rec.get("destinatario") or {}).get("pec", "")
    cons = [pec_ente, (rec.get("destinatario") or {}).get("pec_rpct", "")]
    for campo in ("richiedente", "firma", "documento_identita", "testo"):
        pub.pop(campo, None)
    for v in pub.get("voci", []):
        for k in ("oggetto", "documento_atteso"):
            if v.get(k):
                v[k] = redigi_testo(v[k], cons)[0]
    pub["redazione"] = {"versione": "0.1", "modulo": "tools/accesso_civico/redazione.py"}
    return pub


def redigi_evento(ev, consentite=(), richiedente=None, pec_pubblica=False):
    """Versione pubblica di un evento; None se l'evento non è pubblico (campo pubblico=false)."""
    if ev.get("pubblico") is False:
        return None
    pub = copy.deepcopy(ev)
    doc = pub.get("documento")
    if isinstance(doc, dict):
        doc.pop("percorso", None)
    if pub.get("chi") and pub["chi"] not in AGENTI and pub["chi"] != "Fabio":
        pub["chi"] = "[persona, non pubblicata]"
    if pub.get("tipo") == "comunicazione-controinteressati":
        pub.pop("note", None)
        if isinstance(doc, dict):
            pub["documento"] = {k: doc[k] for k in ("sha256",) if k in doc}
    if pub.get("note"):
        pub["note"] = redigi_testo(pub["note"], consentite, richiedente, pec_pubblica)[0]
    return pub


def redigi_istanza(testo, rec, richiedente=None, pec_pubblica=False):
    """Testo pubblico dell'istanza: via firma, documento, CF, PEC personale (salvo decisione), dati di terzi."""
    d = rec.get("destinatario") or {}
    t = re.sub(r"(?im)^(\s*allegat[oi]:?.*documento.*)$", SEGNAPOSTO["documento"], testo or "")
    return redigi_testo(t, [d.get("pec", ""), d.get("pec_rpct", "")], richiedente, pec_pubblica)
