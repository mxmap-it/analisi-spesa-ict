#!/usr/bin/env python3
"""Adattatore PEC dell'accesso civico (#58, versione 0.1, 9/11/2026). Solo libreria standard.

Modalità SECCA di default: nessuna connessione. Si passa alla modalità reale solo con ENTRAMBI `--reale` e la
variabile d'ambiente PEC_REALE=1, e con le credenziali presenti in ambiente:
  PEC_UTENTE, PEC_PASSWORD, PEC_MITTENTE (indirizzo), PEC_SMTP_HOST [PEC_SMTP_PORT=465], PEC_IMAP_HOST
  [PEC_IMAP_PORT=993], PEC_IMAP_CARTELLA [INBOX]. Nessuna credenziale nei file del progetto.

invia  <cartella-bozze>: per ogni richiesta nello stato «approvata» (registro eventi.jsonl, stati.py) compone il
       messaggio (oggetto e testo dal <id>.md, allegato obbligatorio <id>.pdf.p7m o <id>.pdf firmato), lo archivia
       come .eml con sha256 e, in modalità reale, lo invia via SMTP-SSL e registra l'evento «invio» col Message-ID.
       Ritmo (--intervallo secondi fra due invii) e tetto giornaliero (--tetto-giorno, contando gli «invio» già
       registrati oggi) sono parametrici (default in config/accesso-civico/parametri.yaml, sezione pec).
       In secca il .eml va in <cartella>/pec-secca/ e gli eventi in <cartella>/eventi-secca.jsonl (copia del
       registro): il registro vero non si tocca.
leggi  <cartella-bozze> [--da-cartella DIR]: legge i messaggi (in secca SOLO da file .eml di DIR; in reale via
       IMAP-SSL, in sola lettura: EXAMINE, nessun flag, nessuna cancellazione), archivia ogni .eml con sha256,
       riconosce le ricevute PEC (regole tecniche DM 2/11/2005, DPR 68/2005: header X-Ricevuta,
       X-Riferimento-Message-ID, allegato daticert.xml) e le buste di trasporto (X-Trasporto: posta-certificata con
       postacert.eml), le abbina alla richiesta (Message-ID dell'invio, poi codice «rif. ac-…» nell'oggetto/testo)
       e registra:
         avvenuta-consegna            -> evento «consegna» (data = giorno della ricevuta in daticert.xml)
         errore-consegna / preavviso  -> evento «mancata-consegna» (la richiesta torna «approvata»)
         accettazione, presa-in-carico, non-accettazione -> solo nel giornale pec (nessuno stato corrispondente)
         messaggio dell'ente          -> coda «da-esaminare» (l'esito accolta/parziale/diniego lo decide una persona)
       La firma S/MIME delle ricevute NON è verificata (la libreria standard non lo consente): annotato nel giornale.

Archivio (non in git: contiene dati personali): lavoro/accesso-civico/pec/blobs/<aa>/<sha256>.eml e
lavoro/accesso-civico/pec/giornale.jsonl (una riga per messaggio: sha256, direzione, tipo, abbinamento, esito).
Idempotente: un messaggio già nel giornale (stesso sha256) non genera eventi una seconda volta.
"""
import argparse
import datetime as dt
import email
import email.policy
import email.utils
import hashlib
import imaplib
import json
import mimetypes
import os
import re
import smtplib
import ssl
import sys
import time
import xml.etree.ElementTree as ET
from email.message import EmailMessage
from pathlib import Path

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import stati  # noqa: E402

VERSIONE = "0.1"
CODICE = re.compile(r"\bac-[a-z0-9]+(?:-[a-z0-9]+)*-\d+\b")
RICEVUTE_CONSEGNA = {"avvenuta-consegna"}
RICEVUTE_MANCATA = {"errore-consegna", "preavviso-errore-consegna"}
RICEVUTE_SOLO_GIORNALE = {"accettazione", "non-accettazione", "presa-in-carico", "rilevazione-virus"}
DEFAULT = {"tetto_giorno": 20, "intervallo_secondi": 120}


class ErrorePec(RuntimeError):
    pass


# ---------------------------------------------------------------- archivio e giornale
def sha(b):
    return hashlib.sha256(b).hexdigest()


class Archivio:
    def __init__(self, radice):
        self.radice = Path(radice)
        self.giornale = self.radice / "giornale.jsonl"

    def visti(self):
        if not self.giornale.exists():
            return set()
        with open(self.giornale, encoding="utf-8") as f:
            return {json.loads(r)["sha256"] for r in f if r.strip()}

    def salva(self, grezzo):
        h = sha(grezzo)
        p = self.radice / "blobs" / h[:2] / f"{h}.eml"
        if not p.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
            tmp = p.with_suffix(".part")
            tmp.write_bytes(grezzo)
            tmp.replace(p)
        return h, p

    def annota(self, riga):
        self.radice.mkdir(parents=True, exist_ok=True)
        riga = dict({"registrato": ora_utc(), "versione": VERSIONE}, **riga)
        with open(self.giornale, "a", encoding="utf-8") as f:
            f.write(json.dumps(riga, ensure_ascii=False) + "\n")


def ora_utc():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def relativo(p):
    try:
        return str(Path(p).resolve().relative_to(R))
    except ValueError:
        return str(p)


# ---------------------------------------------------------------- configurazione
def parametri():
    try:
        import yaml
        p = yaml.safe_load((R / "config/accesso-civico/parametri.yaml").read_text(encoding="utf-8")) or {}
        return dict(DEFAULT, **(p.get("pec") or {}))
    except Exception:  # noqa: BLE001 - i default bastano
        return dict(DEFAULT)


def credenziali():
    env = os.environ
    mancano = [k for k in ("PEC_UTENTE", "PEC_PASSWORD", "PEC_MITTENTE") if not env.get(k)]
    if mancano:
        raise ErrorePec(f"variabili d'ambiente mancanti: {', '.join(mancano)}")
    return {"utente": env["PEC_UTENTE"], "password": env["PEC_PASSWORD"], "mittente": env["PEC_MITTENTE"],
            "smtp": (env.get("PEC_SMTP_HOST"), int(env.get("PEC_SMTP_PORT", "465"))),
            "imap": (env.get("PEC_IMAP_HOST"), int(env.get("PEC_IMAP_PORT", "993"))),
            "cartella": env.get("PEC_IMAP_CARTELLA", "INBOX")}


def reale_ammesso(flag):
    return bool(flag) and os.environ.get("PEC_REALE") == "1"


# ---------------------------------------------------------------- invio
def testo_e_oggetto(md):
    """Dal testo della bozza: oggetto dalla riga **Oggetto:**, corpo senza le righe Da/A/Oggetto né commenti."""
    oggetto, corpo = None, []
    for riga in md.splitlines():
        m = re.match(r"\*\*Oggetto:\*\*\s*(.+)", riga)
        if m:
            oggetto = m.group(1).strip()
        elif re.match(r"\*\*(Da|A):\*\*", riga):
            continue
        else:
            corpo.append(riga)
    if not oggetto:
        raise ErrorePec("bozza senza riga **Oggetto:**")
    return oggetto, "\n".join(corpo).strip() + "\n"


def allegato(cartella, rid):
    for nome in (f"{rid}.pdf.p7m", f"{rid}.pdf"):
        p = Path(cartella) / nome
        if p.exists():
            return p
    return None


def componi(rid, md, pdf, mittente, destinatario, dominio=None, adesso=None):
    oggetto, corpo = testo_e_oggetto(md)
    if rid not in oggetto:
        raise ErrorePec(f"{rid}: il codice della richiesta non è nell'oggetto (serve all'abbinamento)")
    m = EmailMessage(policy=email.policy.SMTP)
    m["From"] = mittente
    m["To"] = destinatario
    m["Subject"] = oggetto
    m["Date"] = email.utils.format_datetime(adesso or dt.datetime.now(dt.timezone.utc))
    dominio = dominio or (mittente.split("@")[-1] if "@" in mittente else "accesso-civico.invalid")
    m["Message-ID"] = email.utils.make_msgid(idstring=rid, domain=dominio)
    m["X-Spesaict-Richiesta"] = rid
    m.set_content(corpo)
    tipo = mimetypes.guess_type(pdf.name)[0] or ("application/pkcs7-mime" if pdf.name.endswith(".p7m") else "application/pdf")
    principale, sotto = tipo.split("/")
    m.add_attachment(pdf.read_bytes(), maintype=principale, subtype=sotto, filename=pdf.name)
    return m


def invii_del_giorno(per_id, giorno):
    return sum(1 for evs in per_id.values() for e in evs if e["tipo"] == "invio" and e["data"] == giorno)


def invia(cartella, registro, archivio, mittente, smtp=None, tetto_giorno=20, intervallo=0, soli=None,
          oggi=None, dormi=time.sleep, chi="pec.py"):
    """Invia le richieste approvate. `smtp` è un oggetto con send_message(msg) (None = secca: nessun invio)."""
    cartella = Path(cartella)
    oggi = oggi or dt.date.today().isoformat()
    per_id = stati.leggi(registro) if Path(registro).exists() else {}
    fatti = invii_del_giorno(per_id, oggi)
    esito = []
    for rid in sorted(per_id):
        if soli and rid not in soli:
            continue
        if stati.ricostruisci(per_id[rid])["stato"] != "approvata":
            continue
        if fatti >= tetto_giorno:
            esito.append((rid, "rinviata: tetto giornaliero raggiunto"))
            continue
        j = json.loads((cartella / f"{rid}.json").read_text(encoding="utf-8"))
        dest = (j.get("destinatario") or {}).get("pec")
        pdf = allegato(cartella, rid)
        if not dest:
            esito.append((rid, "saltata: PEC del destinatario mancante"))
            continue
        if not pdf:
            esito.append((rid, "saltata: manca l'allegato firmato (<id>.pdf.p7m o <id>.pdf)"))
            continue
        md = (cartella / f"{rid}.md").read_text(encoding="utf-8")
        msg = componi(rid, md, pdf, mittente, dest)
        grezzo = msg.as_bytes()
        h, p = archivio.salva(grezzo)
        if fatti and intervallo:
            dormi(intervallo)
        if smtp is not None:
            smtp.send_message(msg)
        stati.aggiungi(registro, {"id_richiesta": rid, "tipo": "invio", "data": oggi, "chi": chi,
                                  "documento": {"sha256": h, "percorso": relativo(p), "message_id": msg["Message-ID"]},
                                  "note": "invio reale SMTP-SSL" if smtp is not None else "SECCA: nessun invio"})
        archivio.annota({"sha256": h, "direzione": "uscita", "tipo": "istanza", "id_richiesta": rid,
                         "message_id": msg["Message-ID"], "allegato": pdf.name, "allegato_sha256": sha(pdf.read_bytes()),
                         "secca": smtp is None})
        fatti += 1
        esito.append((rid, "inviata" if smtp is not None else "secca: composta e archiviata"))
    return esito


# ---------------------------------------------------------------- lettura e riconoscimento
def daticert(msg):
    """Primo allegato daticert.xml del messaggio (anche dentro una busta), come dict; None se manca."""
    for parte in msg.walk():
        if (parte.get_filename() or "").lower() == "daticert.xml":
            try:
                x = ET.fromstring(parte.get_payload(decode=True))
            except ET.ParseError:
                return {"errore_xml": True}
            d = {"tipo": x.get("tipo"), "errore": x.get("errore")}
            for k, perc in (("mittente", "intestazione/mittente"), ("oggetto", "intestazione/oggetto"),
                            ("gestore", "dati/gestore-emittente"), ("giorno", "dati/data/giorno"),
                            ("ora", "dati/data/ora"), ("identificativo", "dati/identificativo"),
                            ("msgid", "dati/msgid"), ("consegna", "dati/consegna"),
                            ("errore_esteso", "dati/errore-esteso")):
                n = x.find(perc)
                d[k] = (n.text or "").strip() if n is not None and n.text else None
            zona = x.find("dati/data")
            d["zona"] = zona.get("zona") if zona is not None else None
            d["destinatari"] = [(n.text or "").strip() for n in x.findall("intestazione/destinatari")]
            return d
    return None


def postacert(msg):
    for parte in msg.walk():
        if parte.get_content_type() == "message/rfc822" and (parte.get_filename() or "").lower() == "postacert.eml":
            interno = parte.get_payload()
            return interno[0] if isinstance(interno, list) else interno
    return None


def giorno_iso(dc, msg):
    if dc and dc.get("giorno"):
        try:
            return dt.datetime.strptime(dc["giorno"], "%d/%m/%Y").date().isoformat()
        except ValueError:
            pass
    d = msg.get("Date")
    return email.utils.parsedate_to_datetime(d).date().isoformat() if d else dt.date.today().isoformat()


def classifica(msg):
    """-> (classe, dettagli). classe: ricevuta | busta | messaggio | anomalia."""
    ric = (msg.get("X-Ricevuta") or "").strip().lower()
    tra = (msg.get("X-Trasporto") or "").strip().lower()
    dc = daticert(msg)
    if ric:
        tipo_xml = (dc or {}).get("tipo")
        dett = {"tipo": ric, "riferimento": (msg.get("X-Riferimento-Message-ID") or "").strip(), "daticert": dc,
                "coerente": dc is not None and tipo_xml == ric}
        if dc and dc.get("msgid") and dett["riferimento"] and dc["msgid"] != dett["riferimento"]:
            dett["coerente"] = False
        return "ricevuta", dett
    if tra in ("posta-certificata", "errore"):
        return "busta", {"tipo": tra, "daticert": dc, "interno": postacert(msg)}
    return "messaggio", {"tipo": "ordinario", "daticert": dc}


def indice_message_id(per_id):
    idx = {}
    for rid, evs in per_id.items():
        for e in evs:
            mid = (e.get("documento") or {}).get("message_id")
            if e["tipo"] == "invio" and mid:
                idx[mid.strip()] = rid
    return idx


def testo_di(msg):
    pezzi = [msg.get("Subject") or ""]
    for parte in msg.walk():
        if parte.get_content_maintype() == "text" and not parte.get_filename():
            try:
                pezzi.append(parte.get_content())
            except (LookupError, KeyError):
                pezzi.append((parte.get_payload(decode=True) or b"").decode("utf-8", "replace"))
    return "\n".join(pezzi)


def abbina(msg, idx, noti):
    """Message-ID dell'invio (riferimento, In-Reply-To, References), poi codice «ac-…» presente nel registro."""
    for h in ("X-Riferimento-Message-ID", "In-Reply-To", "References"):
        for mid in re.findall(r"<[^>]+>", msg.get(h) or ""):
            if mid in idx:
                return idx[mid], f"message-id ({h})"
    for c in CODICE.findall(testo_di(msg)):
        if c in noti:
            return c, "codice nell'oggetto/testo"
    return None, None


def elabora(grezzo, registro, archivio, origine="file", chi="pec.py"):
    """Archivia un messaggio, lo riconosce, lo abbina e registra l'evento. Ritorna la riga di giornale."""
    h, p = archivio.salva(grezzo)
    if h in archivio.visti():
        return {"sha256": h, "esito": "già elaborato"}
    msg = email.message_from_bytes(grezzo, policy=email.policy.default)
    per_id = stati.leggi(registro) if Path(registro).exists() else {}
    idx = indice_message_id(per_id)
    classe, dett = classifica(msg)
    riga = {"sha256": h, "percorso": relativo(p), "direzione": "entrata", "origine": origine, "classe": classe,
            "tipo": dett["tipo"], "message_id": (msg.get("Message-ID") or "").strip(), "oggetto": msg.get("Subject"),
            "firma_smime": "non verificata"}
    interno = dett.get("interno") if classe == "busta" else None
    rid, come = abbina(interno if interno is not None else msg, idx, set(per_id))
    if rid is None and interno is not None:
        rid, come = abbina(msg, idx, set(per_id))
    riga.update(id_richiesta=rid, abbinamento=come)
    if classe == "ricevuta":
        riga["riferimento"] = dett["riferimento"]
        riga["daticert_coerente"] = dett["coerente"]
        dc = dett["daticert"] or {}
        riga["daticert"] = {k: dc.get(k) for k in ("tipo", "errore", "giorno", "ora", "zona", "gestore",
                                                   "identificativo", "msgid", "consegna", "errore_esteso")}
    tipo_ev = None
    if classe == "ricevuta" and dett["tipo"] in RICEVUTE_CONSEGNA:
        tipo_ev = "consegna"
    elif classe == "ricevuta" and dett["tipo"] in RICEVUTE_MANCATA:
        tipo_ev = "mancata-consegna"
    if classe == "ricevuta" and not dett["coerente"]:
        tipo_ev, riga["esito"] = None, "anomalia: daticert.xml assente o incoerente con gli header; da esaminare"
    if tipo_ev and rid:
        stato = stati.ricostruisci(per_id[rid])["stato"]
        if stato != "inviata":
            riga["esito"] = f"ricevuta {dett['tipo']} con richiesta nello stato {stato}: nessun evento, da esaminare"
        else:
            ev = stati.aggiungi(registro, {
                "id_richiesta": rid, "tipo": tipo_ev, "data": giorno_iso(dett["daticert"], msg), "chi": chi,
                "documento": {"sha256": h, "percorso": relativo(p), "message_id": riga["message_id"]},
                "note": f"ricevuta PEC {dett['tipo']} (firma S/MIME non verificata)"})
            riga["esito"] = f"evento {ev['tipo']} del {ev['data']}"
    elif tipo_ev:
        riga["esito"] = "ricevuta non abbinata a nessuna richiesta: da esaminare"
    elif classe == "ricevuta" and "esito" not in riga:
        riga["esito"] = "solo giornale" if dett["tipo"] in RICEVUTE_SOLO_GIORNALE else "ricevuta di tipo ignoto: da esaminare"
    elif classe in ("busta", "messaggio"):
        riga["esito"] = "da-esaminare: possibile risposta dell'ente" if rid else "da-esaminare: non abbinato"
    archivio.annota(riga)
    return riga


def leggi_cartella(dir_eml, registro, archivio):
    return [elabora(p.read_bytes(), registro, archivio, origine=f"file:{p.name}")
            for p in sorted(Path(dir_eml).glob("*.eml"))]


def leggi_imap(cred, registro, archivio, stato_uid):
    """IMAP-SSL in sola lettura (EXAMINE): scarica i messaggi con UID oltre l'ultimo elaborato."""
    host, porta = cred["imap"]
    if not host:
        raise ErrorePec("PEC_IMAP_HOST mancante")
    ultimo = int(stato_uid.read_text().strip()) if stato_uid.exists() else 0
    righe = []
    with imaplib.IMAP4_SSL(host, porta, ssl_context=ssl.create_default_context()) as im:
        im.login(cred["utente"], cred["password"])
        im.select(cred["cartella"], readonly=True)
        _, dati = im.uid("SEARCH", None, f"UID {ultimo + 1}:*")
        for uid in sorted(int(u) for u in (dati[0] or b"").split() if int(u) > ultimo):
            _, parti = im.uid("FETCH", str(uid), "(BODY.PEEK[])")
            grezzo = next(p[1] for p in parti if isinstance(p, tuple))
            righe.append(elabora(grezzo, registro, archivio, origine=f"imap:{cred['cartella']}:{uid}"))
            stato_uid.parent.mkdir(parents=True, exist_ok=True)
            stato_uid.write_text(str(uid))
    return righe


# ---------------------------------------------------------------- riga di comando
def registro_di(cartella, reale):
    vero = Path(cartella) / "eventi.jsonl"
    if reale:
        return vero
    secca = Path(cartella) / "eventi-secca.jsonl"
    if not secca.exists() and vero.exists():
        secca.write_bytes(vero.read_bytes())
    return secca


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("comando", choices=["invia", "leggi"])
    ap.add_argument("cartella", help="lavoro/accesso-civico/<ondata>-bozze")
    ap.add_argument("--reale", action="store_true", help="connessione vera (serve anche PEC_REALE=1)")
    ap.add_argument("--id", action="append", help="solo queste richieste")
    ap.add_argument("--tetto-giorno", type=int)
    ap.add_argument("--intervallo", type=float, help="secondi fra due invii")
    ap.add_argument("--da-cartella", help="leggi: cartella di file .eml (unica fonte in secca)")
    ap.add_argument("--archivio", default=str(R / "lavoro/accesso-civico/pec"))
    a = ap.parse_args(argv)
    p = parametri()
    reale = reale_ammesso(a.reale)
    if a.reale and not reale:
        sys.exit("--reale richiede anche PEC_REALE=1 nell'ambiente: resto in secca e mi fermo")
    registro = registro_di(a.cartella, reale)
    archivio = Archivio(Path(a.archivio) / ("reale" if reale else "secca"))
    if a.comando == "invia":
        tetto = a.tetto_giorno if a.tetto_giorno is not None else int(p["tetto_giorno"])
        intervallo = a.intervallo if a.intervallo is not None else float(p["intervallo_secondi"])
        if reale:
            cred = credenziali()
            host, porta = cred["smtp"]
            with smtplib.SMTP_SSL(host, porta, context=ssl.create_default_context()) as s:
                s.login(cred["utente"], cred["password"])
                esito = invia(a.cartella, registro, archivio, cred["mittente"], smtp=s, tetto_giorno=tetto,
                              intervallo=intervallo, soli=a.id)
        else:
            mitt = os.environ.get("PEC_MITTENTE", "richiedente@pec.invalid")
            esito = invia(a.cartella, registro, archivio, mitt, smtp=None, tetto_giorno=tetto, intervallo=0, soli=a.id)
        for rid, e in esito:
            print(f"{rid}\t{e}")
    else:
        if reale:
            righe = leggi_imap(credenziali(), registro, archivio, Path(a.archivio) / "reale" / "ultimo-uid.txt")
        elif a.da_cartella:
            righe = leggi_cartella(a.da_cartella, registro, archivio)
        else:
            sys.exit("secca: indicare --da-cartella con i file .eml (nessuna connessione IMAP)")
        for r in righe:
            print(json.dumps({k: r.get(k) for k in ("sha256", "classe", "tipo", "id_richiesta", "abbinamento", "esito")},
                             ensure_ascii=False))
    print(f"registro: {relativo(registro)}  archivio: {relativo(archivio.radice)}  modalità: {'REALE' if reale else 'secca'}")


if __name__ == "__main__":
    main()
