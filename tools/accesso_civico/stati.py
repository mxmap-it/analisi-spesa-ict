#!/usr/bin/env python3
"""Macchina a stati e scadenze delle richieste di accesso civico (#58, versione 0.2, 9/11/2026).

Registro append-only: un file JSONL di eventi (`spesaict.accesso-civico-evento/1`, schemi/accesso-civico-evento.schema.json).
Lo stato di una richiesta NON si salva: si ricalcola sempre dagli eventi (`ricostruisci`), alla data voluta
(`alla_data`), che aggiunge gli stati derivati dal tempo (silenzio, accesso consentito dopo il difensore civico).

Termini (giorni di calendario, verificati sul testo archiviato in report/metodo/prove-normativa/dlgs33-art5.html):
- 30 gg dalla presentazione per il provvedimento espresso e motivato (art. 5 c. 6) [V];
- comunicazione ai controinteressati: opposizione entro 10 gg dalla ricezione, termine sospeso (art. 5 c. 5) [V];
  la sospensione effettiva va dalla comunicazione all'evento `fine-sospensione` (opposizione o decorso dei 10 gg);
- riesame: decisione del RPCT entro 20 gg (art. 5 c. 7) [V]; +10 gg se sentito il Garante (c. 7) [V];
- presentazione del riesame entro 30 gg dalla decisione: circ. FP 1/2019 § 7 (interpretazione, non norma) [V copia];
- difensore civico: pronuncia entro 30 gg; se ritiene illegittimo il diniego, l'ente ha 30 gg per confermarlo,
  altrimenti l'accesso è consentito (art. 5 c. 8) [V]; solo atti di regioni ed enti locali.
- scadenza in giorno festivo: slitta al primo giorno seguente non festivo. Testi [V] archiviati in prove-normativa/:
  art. 2963 c. 3 c.c. (prescrizione), art. 155 c. 4 c.p.c. (processo civile; c. 5: anche il sabato, solo atti
  processuali), art. 52 c. 3 e 5 c.p.a. (processo amministrativo, anche il sabato). Per il procedimento amministrativo
  (L. 241/1990, d.lgs. 33/2013) NESSUNA norma lo dice espressamente (art. 2 L. 241 archiviato: tace); l'estensione è un
  principio generale di origine giurisprudenziale [interpretazione]. Si applica a tutti i termini (`proroga=True`):
  per i termini dell'ente evita di dichiarare un silenzio un giorno prima; per i nostri (riesame) conviene comunque
  agire entro la data non prorogata. Il sabato non è festivo, tranne per il ricorso al TAR (art. 52 c. 5 c.p.a.).
- festività: L. 260/1949 art. 1 (2 giugno) e art. 2 [V]; 4 ottobre festivo dal 1/1/2026 per L. 8/10/2025 n. 151
  (GU SG n. 236 del 10/10/2025, entrata in vigore 1/1/2026) [V, Normattiva + GU]. Il 4 novembre e le feste religiose
  soppresse restano nel testo dell'art. 2 ma non sono festive dalla L. 54/1977 (Epifania ripristinata con DPR 792/1985)
  [R, non archiviate]. Il santo patrono locale non è festività nazionale: non conta.
- ricorso al TAR in materia di accesso civico: 30 gg dalla conoscenza della decisione o dalla formazione del silenzio
  (art. 116 c. 1 c.p.a., testo vigente: «tutela del diritto di accesso civico») [V].
- il chiarimento NON riavvia né sospende il termine: la norma non lo prevede (scelta prudente, [R]).

Uso: stati.py <eventi.jsonl> [AAAA-MM-GG]  -> stato di ogni richiesta alla data (default oggi).
"""
import datetime as dt
import json
import sys
from pathlib import Path

FORMATO = "spesaict.accesso-civico-evento/1"
TERMINI = {"risposta": 30, "controinteressati": 10, "consegna_dopo_opposizione": 15, "riesame_decisione": 20,
           "garante": 10, "riesame_presentazione": 30, "difensore_decisione": 30, "difensore_conferma_ente": 30,
           "ricorso_tar": 30}

STATI = ["bozza", "approvata", "inviata", "consegnata", "sospesa-controinteressati", "chiarimento", "accolta",
         "parziale", "diniego", "silenzio", "riesame", "difensore", "difensore-conferma", "chiusa", "annullata"]
FINALI = {"chiusa", "annullata"}
ESITI = {"accolta", "parziale", "diniego"}
ATTESA = {"consegnata", "sospesa-controinteressati", "chiarimento", "riesame", "difensore", "difensore-conferma"}

# evento -> (stati di partenza ammessi, stato di arrivo; None = resta, "esito" = da dati.esito)
TRANSIZIONI = {
    "creazione": ({None}, "bozza"),
    "approvazione": ({"bozza"}, "approvata"),
    "annullamento": ({"bozza", "approvata"}, "annullata"),
    "invio": ({"approvata"}, "inviata"),
    "mancata-consegna": ({"inviata"}, "approvata"),
    "consegna": ({"inviata"}, "consegnata"),
    "richiesta-chiarimento": ({"consegnata", "sospesa-controinteressati"}, "chiarimento"),
    "invio-chiarimento": ({"chiarimento"}, "consegnata"),
    "comunicazione-controinteressati": ({"consegnata", "chiarimento"}, "sospesa-controinteressati"),
    "fine-sospensione": ({"sospesa-controinteressati"}, "consegnata"),
    "sollecito": ({"consegnata", "chiarimento", "silenzio", "riesame", "difensore", "sospesa-controinteressati"}, None),
    "silenzio": ({"consegnata", "chiarimento", "riesame", "difensore"}, "silenzio"),
    "risposta": ({"consegnata", "sospesa-controinteressati", "chiarimento", "silenzio", "riesame", "difensore-conferma"},
                 "esito"),
    "riesame": ({"parziale", "diniego", "silenzio"}, "riesame"),
    "richiesta-garante": ({"riesame", "difensore"}, None),
    "difensore": ({"parziale", "diniego", "silenzio"}, "difensore"),
    "pronuncia-difensore": ({"difensore"}, "esito-difensore"),
    "conferma-diniego": ({"difensore-conferma"}, "diniego"),
    "chiusura": (set(STATI) - FINALI, "chiusa"),
}

# festività nazionali fisse (L. 260/1949 artt. 1-2 [V]); il 4 ottobre (San Francesco) dal 2026: L. 151/2025 [V]
FESTIVI_FISSI = {(1, 1), (1, 6), (4, 25), (5, 1), (6, 2), (8, 15), (11, 1), (12, 8), (12, 25), (12, 26)}
FESTIVI_DAL = {(10, 4): 2026}


class ErroreTransizione(ValueError):
    pass


def pasqua(anno):
    a, b, c = anno % 19, anno // 100, anno % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mese = (h + l - 7 * m + 114) // 31
    giorno = (h + l - 7 * m + 114) % 31 + 1
    return dt.date(anno, mese, giorno)


def festivo(d, sabato=False):
    if d.weekday() == 6 or (sabato and d.weekday() == 5):
        return True
    if (d.month, d.day) in FESTIVI_FISSI:
        return True
    if (d.month, d.day) in FESTIVI_DAL and d.year >= FESTIVI_DAL[(d.month, d.day)]:
        return True
    return d == pasqua(d.year) + dt.timedelta(days=1)


def termine(inizio, giorni, proroga=True, sabato=False):
    """Scadenza a `giorni` di calendario da `inizio` (escluso il giorno iniziale), prorogata se festiva."""
    d = inizio + dt.timedelta(days=giorni)
    while proroga and festivo(d, sabato):
        d += dt.timedelta(days=1)
    return d


def termine_tar(inizio, giorni=None):
    """Ricorso al TAR (art. 116 c. 1 c.p.a.): 30 gg, prorogati se festivi o sabato (art. 52 c. 3 e 5 c.p.a.)."""
    return termine(inizio, giorni or TERMINI["ricorso_tar"], proroga=True, sabato=True)


def data(s):
    return s if isinstance(s, dt.date) else dt.date.fromisoformat(s[:10])


def ricostruisci(eventi, termini=None, proroga=True):
    """Applica gli eventi di UNA richiesta in ordine; solleva ErroreTransizione se un evento non è ammesso."""
    t = dict(TERMINI, **(termini or {}))
    s = {"stato": None, "fase": None, "presentazione": None, "sospensione_giorni": 0, "sospensione_inizio": None,
         "scadenza": None, "decisione": None, "termine_riesame": None, "riesame_fatto": False,
         "difensore_fatto": False, "solleciti": 0, "storia": []}
    ultima = None
    for ev in eventi:
        tipo, d = ev["tipo"], data(ev["data"])
        if ultima and d < ultima:
            raise ErroreTransizione(f"{ev.get('id_richiesta')}: evento {tipo} del {d} precede il precedente ({ultima})")
        ultima = d
        if tipo not in TRANSIZIONI:
            raise ErroreTransizione(f"evento sconosciuto: {tipo}")
        da, a = TRANSIZIONI[tipo]
        if s["stato"] not in da:
            raise ErroreTransizione(f"{ev.get('id_richiesta')}: evento {tipo} non ammesso nello stato {s['stato']}")
        dati = ev.get("dati") or {}
        if tipo == "consegna":
            s.update(presentazione=d, fase="istanza", scadenza=termine(d, t["risposta"], proroga))
        elif tipo == "comunicazione-controinteressati":
            s["sospensione_inizio"] = d
        elif tipo == "fine-sospensione":
            s["sospensione_giorni"] += (d - s["sospensione_inizio"]).days
            s["sospensione_inizio"] = None
            s["scadenza"] = termine(s["presentazione"], t["risposta"] + s["sospensione_giorni"], proroga)
        elif tipo == "silenzio":
            if s["scadenza"] and d <= s["scadenza"]:
                raise ErroreTransizione(f"{ev.get('id_richiesta')}: silenzio il {d} prima della scadenza {s['scadenza']}")
            s["termine_riesame"] = termine(s["scadenza"], t["riesame_presentazione"], proroga) \
                if s["fase"] == "istanza" else None
        elif tipo == "sollecito":
            s["solleciti"] += 1
        elif tipo == "riesame":
            if s["riesame_fatto"] or s["fase"] != "istanza":
                raise ErroreTransizione(f"{ev.get('id_richiesta')}: riesame già chiesto o fase {s['fase']}")
            s.update(fase="riesame", riesame_fatto=True, scadenza=termine(d, t["riesame_decisione"], proroga),
                     termine_riesame=None)
        elif tipo == "difensore":
            if s["difensore_fatto"]:
                raise ErroreTransizione(f"{ev.get('id_richiesta')}: difensore civico già adito")
            s.update(fase="difensore", difensore_fatto=True, scadenza=termine(d, t["difensore_decisione"], proroga),
                     termine_riesame=None)
        elif tipo == "richiesta-garante":
            s["scadenza"] = termine(s["scadenza"], t["garante"], proroga)
        elif tipo in ("risposta", "pronuncia-difensore", "conferma-diniego"):
            s.update(decisione=d, scadenza=None)
            s["termine_riesame"] = termine(d, t["riesame_presentazione"], proroga) \
                if s["fase"] == "istanza" else None
        if a == "esito":
            esito = dati.get("esito")
            if esito not in ESITI:
                raise ErroreTransizione(f"{ev.get('id_richiesta')}: risposta senza esito valido ({esito})")
            a = esito
        elif a == "esito-difensore":
            esito = dati.get("esito")
            if esito == "illegittimo":
                a = "difensore-conferma"
                s["scadenza"] = termine(d, t["difensore_conferma_ente"], proroga)
            elif esito in ("legittimo", "inammissibile"):
                a = "diniego"
            else:
                raise ErroreTransizione(f"{ev.get('id_richiesta')}: pronuncia del difensore senza esito valido")
        if a:
            s["stato"] = a
        s["storia"].append((d.isoformat(), tipo, s["stato"]))
    return s


def alla_data(s, oggi):
    """Aggiunge gli stati derivati dal tempo (non registrati come evento): silenzio, accesso consentito."""
    r = dict(s, derivato=None, prossima_azione=None)
    oggi = data(oggi)
    if s["stato"] in ("consegnata", "chiarimento", "riesame", "difensore") and s["scadenza"] and oggi > s["scadenza"]:
        r.update(stato="silenzio", derivato=f"scaduto il {s['scadenza']}")
        if s["fase"] == "istanza":
            r["termine_riesame"] = termine(s["scadenza"], TERMINI["riesame_presentazione"])
    elif s["stato"] == "difensore-conferma" and oggi > s["scadenza"]:
        r.update(stato="accolta", derivato=f"accesso consentito: l'ente non ha confermato il diniego entro il {s['scadenza']} (art. 5 c. 8)")
    elif s["stato"] == "sospesa-controinteressati" and oggi > termine(s["sospensione_inizio"], TERMINI["controinteressati"]):
        r["derivato"] = "sospensione oltre i 10 giorni: verificare la data di ricezione dei controinteressati"
    st = r["stato"]
    if st == "silenzio" and s["fase"] == "istanza":
        r["prossima_azione"] = "sollecito" if s["solleciti"] == 0 else "riesame-silenzio"
    elif st == "silenzio":
        r["prossima_azione"] = f"difensore o TAR entro il {termine_tar(s['scadenza'])} (decisione Fabio)"
    elif st in ("parziale", "diniego") and s["fase"] == "istanza":
        r["prossima_azione"] = f"riesame-diniego entro il {r['termine_riesame']}"
    elif st in ("parziale", "diniego"):
        r["prossima_azione"] = f"difensore (enti regionali/locali) o TAR entro il {termine_tar(s['decisione'])} (decisione Fabio)"
    elif st == "chiarimento":
        r["prossima_azione"] = "chiarimento"
    elif st == "accolta":
        r["prossima_azione"] = "archiviare i documenti e chiudere"
    return r


def leggi(percorso):
    per_id = {}
    with open(percorso, encoding="utf-8") as f:
        righe = f.readlines()
    for riga in righe:
        if riga.strip():
            ev = json.loads(riga)
            per_id.setdefault(ev["id_richiesta"], []).append(ev)
    return per_id


def aggiungi(percorso, ev):
    """Append-only: valida l'evento sulla storia della richiesta prima di scriverlo."""
    percorso = Path(percorso)
    storia = leggi(percorso).get(ev["id_richiesta"], []) if percorso.exists() else []
    ev = dict({"formato": FORMATO, "registrato": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}, **ev)
    ricostruisci(storia + [ev])
    with open(percorso, "a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    return ev


def main():
    oggi = sys.argv[2] if len(sys.argv) > 2 else dt.date.today().isoformat()
    for rid, evs in sorted(leggi(sys.argv[1]).items()):
        r = alla_data(ricostruisci(evs), oggi)
        print(json.dumps({"id": rid, "stato": r["stato"], "fase": r["fase"], "scadenza": str(r["scadenza"]),
                          "derivato": r["derivato"], "prossima_azione": r["prossima_azione"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
