#!/usr/bin/env python3
"""Generatore PUBBLICO statico dell'accesso civico (#58, versione 0.1, 9/11/2026). SOLO ANTEPRIMA, NESSUNA PUBBLICAZIONE.

Specifica §§ 5 e 7. Dal registro (richieste JSON + eventi.jsonl) e dalle campagne produce, in una cartella di uscita:
- sito/content/accesso-civico/: panoramica con dashboard, campagne/<cmp>.md, richieste/<id>.md, enti/<cf>.md, dati.md
  (pagine Hugo, stesso tema di sito/);
- sito/static/accesso-civico/dashboard.json: indicatori totali e per campagna, calcolati SOLO dagli eventi;
- sito/static/accesso-civico/dati/v/<data>/ (+ copia in dati/ultima/): richieste.csv, eventi.jsonl, enti-tempi.csv,
  campagne.json, campagne/<cmp>/richieste.csv, dizionario.md, LICENZA.txt, manifest.json (sha256, byte, righe),
  SHA256SUMS.
Tutto passa da redazione.py; alla fine `residui()` su ogni file: se resta un dato personale il generatore si ferma.

Default di uscita: lavoro/accesso-civico/anteprima-pubblico/ (fuori da git). NON scrive in sito/ né in docs/:
le pagine di richieste non inviate non vanno pubblicate. Licenza dei dati: segnaposto finché Fabio non decide.

Uso:
  pubblica.py --sintetico [--oggi AAAA-MM-GG]          # dati SINTETICI di prova (enti e persone inventati)
  pubblica.py --registro lavoro/accesso-civico/ondata-0-bozze [--oggi ...] [--uscita ...]
"""
import argparse
import collections
import csv
import datetime as dt
import hashlib
import io
import json
import shutil
import statistics
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import campagna as cmp  # noqa: E402
import redazione  # noqa: E402
import stati  # noqa: E402

VERSIONE = "0.1"
USCITA = R / "lavoro/accesso-civico/anteprima-pubblico"
LICENZA_SEGNAPOSTO = "[LICENZA DEI DATI: da decidere (Fabio), proposta CC-BY-4.0 — specifica § 7 e § 15]"
MOTIVI = {"5bis-c1": "art. 5-bis c. 1 (interessi pubblici)", "5bis-c2a": "art. 5-bis c. 2 lett. a (dati personali)",
          "5bis-c2b": "art. 5-bis c. 2 lett. b (libertà e segretezza della corrispondenza)",
          "5bis-c2c": "art. 5-bis c. 2 lett. c (interessi economici e commerciali)", "5bis-c3": "art. 5-bis c. 3 (divieti di legge)",
          "inesistente": "documento inesistente o non detenuto", "massiva": "richiesta massiva / irragionevole",
          "altro": "altro motivo", "": "motivo non indicato"}
BANNER_SINTETICO = ("> **ANTEPRIMA CON DATI SINTETICI.** Enti, persone, CIG ed eventi di questa pagina sono inventati per "
                    "mostrare come apparirà la piattaforma. Nessuna richiesta è stata inviata.\n")
BANNER_ANTEPRIMA = "> **ANTEPRIMA, non pubblicata.** Nessuna richiesta è stata inviata.\n"


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------- dati sintetici (mai reali)

def sintetici(oggi):
    """Una campagna e 12 richieste inventate che coprono i percorsi principali della macchina a stati."""
    o = stati.data(oggi)

    def g(n):
        return (o - dt.timedelta(days=n)).isoformat()
    c = {"formato": cmp.FORMATO, "id": "cmp-prova-sintetica", "versione": "0.1",
         "titolo": "Campagna SINTETICA di prova", "scopo": "Mostrare pagine, dashboard e dataset con dati inventati.",
         "progetto": {"nome": "analisi-spesa-ict", "issue": "#58"}, "responsabile": {"nome": "Responsabile di prova"},
         "richiedente_id": None, "perimetro": {"enti": "enti inventati", "documenti": "contratti inventati", "periodo": "-"},
         "criteri": ["dati sintetici"], "selezione": {"comando": "pubblica.py --sintetico"},
         "parametri": {"tetto_voci": 20}, "modelli": {"istanza": {"path": "config/accesso-civico/modelli/istanza.md",
                                                                    "sha256": "0" * 64, "versione": "0.1"}},
         "template": {"pec_richiedente_pubblica": False}, "licenza_dati": LICENZA_SEGNAPOSTO, "stato": "proposta",
         "creata": g(90)}
    rich = {"nome": "Richiedente Di Prova", "pec": "richiedente.prova@pec.esempio.invalid", "firma": "FIRMA-PROVA-XYZ",
            "codice_fiscale": "RSSMRA80A01H501U"}
    percorsi = [  # (eventi relativi: (tipo, giorni fa, dati, note))
        [("creazione", 80, {}, ""), ("approvazione", 75, {}, ""), ("invio", 70, {}, ""), ("consegna", 70, {}, ""),
         ("risposta", 50, {"esito": "accolta", "voci_rilasciate": ["v1", "v2"]}, "rilasciati 2 contratti")],
        [("creazione", 80, {}, ""), ("approvazione", 75, {}, ""), ("invio", 70, {}, ""), ("consegna", 70, {}, ""),
         ("risposta", 45, {"esito": "diniego", "motivo": "5bis-c2c", "limite_5bis": "interessi commerciali"},
          "referente dell'ufficio: tel. 06 1234 5678, mario.bianchi@gmail.com")],
        [("creazione", 80, {}, ""), ("approvazione", 75, {}, ""), ("invio", 70, {}, ""), ("consegna", 70, {}, ""),
         ("risposta", 60, {"esito": "parziale", "motivo": "5bis-c2a"}, "IBAN fornitore IT60X0542811101000000123456 oscurato")],
        [("creazione", 80, {}, ""), ("approvazione", 75, {}, ""), ("invio", 70, {}, ""), ("consegna", 70, {}, ""),
         ("sollecito", 38, {}, ""), ("silenzio", 35, {}, "")],
        [("creazione", 80, {}, ""), ("approvazione", 75, {}, ""), ("invio", 70, {}, ""), ("consegna", 70, {}, ""),
         ("risposta", 55, {"esito": "diniego", "motivo": "inesistente"}, ""), ("riesame", 50, {}, ""),
         ("risposta", 32, {"esito": "accolta"}, "")],
        [("creazione", 80, {}, ""), ("approvazione", 75, {}, ""), ("invio", 70, {}, ""), ("mancata-consegna", 70, {}, "")],
        [("creazione", 40, {}, ""), ("approvazione", 35, {}, ""), ("invio", 20, {}, ""), ("consegna", 20, {}, "")],
        [("creazione", 40, {}, ""), ("approvazione", 35, {}, ""), ("invio", 20, {}, ""), ("consegna", 20, {}, ""),
         ("richiesta-chiarimento", 15, {}, "chiede di precisare la voce 2")],
        [("creazione", 40, {}, ""), ("approvazione", 35, {}, ""), ("invio", 20, {}, ""), ("consegna", 20, {}, ""),
         ("comunicazione-controinteressati", 12, {}, "controinteressato: Luigi Verdi VRDLGU70B02F205X")],
        [("creazione", 40, {}, ""), ("approvazione", 35, {}, ""), ("invio", 30, {}, ""), ("consegna", 30, {}, ""),
         ("risposta", 5, {"esito": "diniego", "motivo": "massiva"}, "")],
        [("creazione", 10, {}, "")],
        [("creazione", 10, {}, ""), ("annullamento", 8, {}, "ente fuori perimetro")],
    ]
    tip = ["Comuni", "Regioni", "Aziende Sanitarie Locali", "Universita' e Istituti di Istruzione Universitaria Pubblici"]
    richieste, eventi, testi = [], [], {}
    for i, p in enumerate(percorsi, 1):
        cf = f"{90000000000 + i:011d}"
        rid = f"ac-prova-{cf}-1"
        voci = [{"id": f"v{j}", "fonte": "B-residuo-imbuto", "cig": f"Z{i:02d}{j:02d}ABCDEF"[:10],
                 "oggetto": f"Servizio informatico di prova n. {j}", "documento_atteso": "contratto o determina",
                 "importo": 10000.0 * i * j, "anno": "2024", "priorita": float(10 - j)} for j in range(1, 1 + (i % 4) + 1)]
        pec = f"protocollo@pec.ente-prova-{i}.invalid"
        richieste.append({"formato": "spesaict.accesso-civico-richiesta/1", "id": rid, "campagna": c["id"],
                          "ondata": "ondata-prova", "ente": {"cf": cf, "nome": f"Ente di prova {i}",
                                                             "tipologia_istat": tip[i % 4], "regione": ["Lazio", "Puglia", "Veneto"][i % 3],
                                                             "difensore_civico_competente": i % 4 in (0, 1)},
                          "destinatario": {"pec": pec, "fonte": "sintetico", "attendibilita": "A"},
                          "voci": voci, "tetto": 20, "modello": "istanza.md 0.1", "testo_sha256": "0" * 64,
                          "generata": g(80) + "T00:00:00Z", "approvazione": None})
        for tipo, n, dati, note in p:
            ev = {"formato": stati.FORMATO, "id_richiesta": rid, "campagna": c["id"], "tipo": tipo, "data": g(n),
                  "registrato": g(n) + "T12:00:00Z", "chi": "Operatore Rossi" if tipo == "risposta" else "pec.py"}
            if dati:
                ev["dati"] = dati
            if note:
                ev["note"] = note
            if tipo in ("invio", "consegna", "risposta"):
                ev["documento"] = {"sha256": sha(f"{rid}{tipo}{n}"), "percorso": f"registro-privato/eml/{rid}-{tipo}.eml"}
            eventi.append(ev)
        testi[rid] = (f"**Da:** {rich['nome']} — {rich['pec']}\n**A:** Ente di prova {i} — {pec}\n\n"
                      f"Il sottoscritto {rich['nome']}, C.F. {rich['codice_fiscale']}, chiede l'accesso ai documenti.\n\n"
                      f"Allegato: copia del documento d'identità\n\n{rich['firma']}\n")
    return [c], richieste, eventi, testi, rich


# ---------------------------------------------------------------- indicatori

def mediana_p90(xs):
    if not xs:
        return None, None
    s = sorted(xs)
    return statistics.median(s), s[min(len(s) - 1, int(round(0.9 * (len(s) - 1))))]


def stato_richiesta(evs, oggi):
    return stati.alla_data(stati.ricostruisci(evs), oggi)


def tempo_risposta(evs):
    cons = next((stati.data(e["data"]) for e in evs if e["tipo"] == "consegna"), None)
    risp = next((stati.data(e["data"]) for e in evs if e["tipo"] == "risposta"), None)
    return (risp - cons).days if cons and risp else None


def indicatori(richieste, ev_per_id, oggi):
    tipi = collections.Counter(e["tipo"] for r in richieste for e in ev_per_id.get(r["id"], []))
    st = collections.Counter()
    esiti, motivi, tempi = collections.Counter(), collections.Counter(), []
    for r in richieste:
        evs = ev_per_id.get(r["id"], [])
        if not evs:
            continue
        s = stato_richiesta(evs, oggi)
        st[s["stato"]] += 1
        for e in evs:
            if e["tipo"] == "risposta":
                d = e.get("dati") or {}
                esiti[d.get("esito")] += 1
                if d.get("esito") in ("diniego", "parziale"):
                    motivi[MOTIVI.get(d.get("motivo") or "", MOTIVI["altro"])] += 1
        t = tempo_risposta(evs)
        if t is not None:
            tempi.append(t)
    med, p90 = mediana_p90(tempi)
    return {"richieste": len(richieste), "create": tipi["creazione"], "approvate": tipi["approvazione"],
            "inviate": tipi["invio"], "consegnate": tipi["consegna"], "mancata_consegna": tipi["mancata-consegna"],
            "stati": dict(sorted(st.items())), "esiti_risposte": dict(sorted((k or "?", v) for k, v in esiti.items())),
            "dinieghi_per_motivo": dict(motivi.most_common()),
            "tempi_risposta_giorni": {"n": len(tempi), "mediana": med, "p90": p90},
            "seguiti": {"solleciti": tipi["sollecito"], "riesami": tipi["riesame"], "difensore": tipi["difensore"],
                        "chiarimenti": tipi["richiesta-chiarimento"], "controinteressati": tipi["comunicazione-controinteressati"]},
            "scadute_in_silenzio": st["silenzio"],
            "in_attesa_nei_termini": sum(st[k] for k in stati.ATTESA)}


# ---------------------------------------------------------------- scrittura

def fm(titolo, descr, data):
    return (f"---\ntitle: \"{titolo}\"\ndate: {data}\ndescription: \"{descr}\"\nrobots: \"noindex\"\n---\n\n"
            f"<!-- Generata da tools/accesso_civico/pubblica.py {VERSIONE}: non modificare a mano. -->\n\n")


def tab_indicatori(k):
    righe = ["| Indicatore | Valore |", "|---|---|"]
    for et, v in (("Richieste", k["richieste"]), ("Approvate", k["approvate"]), ("Inviate", k["inviate"]),
                  ("Consegnate (ricevuta PEC)", k["consegnate"]), ("Mancata consegna", k["mancata_consegna"]),
                  ("In attesa nei termini", k["in_attesa_nei_termini"]), ("Scadute in silenzio", k["scadute_in_silenzio"]),
                  ("Tempo di risposta, mediana (giorni)", k["tempi_risposta_giorni"]["mediana"]),
                  ("Tempo di risposta, 90° percentile (giorni)", k["tempi_risposta_giorni"]["p90"])):
        righe.append(f"| {et} | {'—' if v is None else v} |")
    righe += ["", "**Stati alla data**", "", "| Stato | Richieste |", "|---|---|"]
    righe += [f"| {s} | {n} |" for s, n in k["stati"].items()] or ["| — | 0 |"]
    righe += ["", "**Esiti delle risposte**", "", "| Esito | Risposte |", "|---|---|"]
    righe += [f"| {s} | {n} |" for s, n in k["esiti_risposte"].items()] or ["| — | 0 |"]
    righe += ["", "**Dinieghi e accoglimenti parziali per motivo**", "", "| Motivo | Numero |", "|---|---|"]
    righe += [f"| {s} | {n} |" for s, n in k["dinieghi_per_motivo"].items()] or ["| — | 0 |"]
    righe += ["", "**Seguiti**", "", "| Seguito | Numero |", "|---|---|"]
    righe += [f"| {s} | {n} |" for s, n in k["seguiti"].items()]
    return "\n".join(righe) + "\n"


def csv_testo(righe, campi):
    b = io.StringIO()
    w = csv.DictWriter(b, fieldnames=campi, lineterminator="\n")
    w.writeheader()
    for r in righe:
        w.writerow({k: r.get(k, "") for k in campi})
    return b.getvalue()


CAMPI_RICHIESTE = ["id", "campagna", "ondata", "ente_cf", "ente_nome", "tipologia_istat", "regione", "pec_ente", "voci",
                   "euro", "stato", "fase", "scadenza", "consegna", "prima_risposta", "giorni_risposta", "esito", "motivo",
                   "solleciti", "pagina"]
DIZIONARIO = """# Dizionario dei dati (accesso civico, #58)

Generato da `tools/accesso_civico/pubblica.py`. Tutti i dati sono già redatti (`tools/accesso_civico/redazione.py`).

## richieste.csv
- `id`: identificativo della richiesta (`ac-…`); `campagna`, `ondata`
- `ente_cf`, `ente_nome`, `tipologia_istat`, `regione`, `pec_ente` (PEC istituzionale, pubblica in IndicePA)
- `voci`: numero di documenti chiesti; `euro`: somma degli importi dei CIG chiesti
- `stato`, `fase`, `scadenza`: stato alla data di generazione, ricalcolato dagli eventi (`stati.py`)
- `consegna`, `prima_risposta`, `giorni_risposta`: date (AAAA-MM-GG) e giorni di calendario fra le due
- `esito`, `motivo`: ultimo esito e motivo del diniego (codici: 5bis-c1, 5bis-c2a/b/c, 5bis-c3, inesistente, massiva, altro)
- `solleciti`, `pagina`

## eventi.jsonl
Una riga per evento (`spesaict.accesso-civico-evento/1`), senza percorsi d'archivio privati, senza dati personali.

## enti-tempi.csv
Per ente: richieste, risposte, mediana e 90° percentile dei giorni di risposta, dinieghi, silenzi.

## campagne.json
Campagne (`spesaict.accesso-civico-campagna/1`) senza `richiedente_id`.
"""


def genera(campagne, richieste, eventi, oggi, uscita, testi=None, richiedente=None, sintetico=False):
    oggi = stati.data(oggi).isoformat()
    banner = BANNER_SINTETICO if sintetico else BANNER_ANTEPRIMA
    if uscita.exists():
        shutil.rmtree(uscita)
    content = uscita / "sito/content/accesso-civico"
    static = uscita / "sito/static/accesso-civico"
    vdir = static / "dati/v" / oggi
    for d in (content / "campagne", content / "richieste", content / "enti", vdir / "campagne"):
        d.mkdir(parents=True, exist_ok=True)
    per_c = {c["id"]: c for c in campagne}
    pec_pub = {c["id"]: bool((c.get("template") or {}).get("pec_richiedente_pubblica")) for c in campagne}
    ev_per_id = collections.defaultdict(list)
    for e in eventi:
        ev_per_id[e["id_richiesta"]].append(e)
    pubbliche = [redazione.redigi_richiesta(r, per_c.get(r.get("campagna"))) for r in richieste]
    consentite = {p for r in richieste for p in ((r.get("destinatario") or {}).get("pec"),
                                                 (r.get("destinatario") or {}).get("pec_rpct")) if p}
    righe, ev_pub = [], []
    for r_orig, r in zip(richieste, pubbliche):
        evs = ev_per_id.get(r["id"], [])
        s = stato_richiesta(evs, oggi) if evs else {"stato": "—", "fase": None, "scadenza": None, "prossima_azione": None,
                                                     "derivato": None, "solleciti": 0}
        cmp_id = r.get("campagna", "")
        epub = [x for x in (redazione.redigi_evento(dict(e, campagna=e.get("campagna", cmp_id)), consentite, richiedente,
                                                    pec_pub.get(cmp_id, False)) for e in evs) if x]
        ev_pub += epub
        risposte = [e for e in evs if e["tipo"] == "risposta"]
        ult = (risposte[-1].get("dati") or {}) if risposte else {}
        cons = next((e["data"] for e in evs if e["tipo"] == "consegna"), "")
        righe.append({"id": r["id"], "campagna": cmp_id, "ondata": r.get("ondata", ""), "ente_cf": r["ente"]["cf"],
                      "ente_nome": r["ente"]["nome"], "tipologia_istat": r["ente"].get("tipologia_istat", ""),
                      "regione": r["ente"].get("regione", ""), "pec_ente": r["destinatario"]["pec"], "voci": len(r["voci"]),
                      "euro": round(sum(v.get("importo") or 0 for v in r["voci"])), "stato": s["stato"],
                      "fase": s["fase"] or "", "scadenza": s["scadenza"] or "", "consegna": cons,
                      "prima_risposta": risposte[0]["data"] if risposte else "",
                      "giorni_risposta": "" if tempo_risposta(evs) is None else tempo_risposta(evs), "esito": ult.get("esito", ""),
                      "motivo": ult.get("motivo", ""), "solleciti": s.get("solleciti", 0),
                      "pagina": f"/accesso-civico/richieste/{r['id']}/"})
        # pagina della richiesta
        md = [fm(f"Richiesta {r['id']}", f"Accesso civico a {r['ente']['nome']}: storia, scadenze, esito.", oggi), banner,
              f"**Ente:** [{r['ente']['nome']}](/accesso-civico/enti/{r['ente']['cf']}/) (CF {r['ente']['cf']}) — "
              f"PEC {r['destinatario']['pec']}  ",
              f"**Campagna:** [{cmp_id}](/accesso-civico/campagne/{cmp_id}/) · ondata {r.get('ondata', '')}  ",
              f"**Stato al {oggi}:** {s['stato']}" + (f" ({s['derivato']})" if s.get("derivato") else "")
              + (f" · scadenza {s['scadenza']}" if s.get("scadenza") else "")
              + (f" · prossima azione: {s['prossima_azione']}" if s.get("prossima_azione") else ""), "",
              "## Documenti chiesti", "", "| # | CIG | Oggetto | Documento | Importo |", "|---|---|---|---|---|"]
        for i, v in enumerate(r["voci"], 1):
            imp = f"{v['importo']:,.0f} €".replace(",", ".") if v.get("importo") else ""
            md.append(f"| {i} | {v.get('cig') or '—'} | {v.get('oggetto', '')} | {v.get('documento_atteso', '')} | {imp} |")
        md += ["", "## Cronologia", "", "| Data | Evento | Esito / dati | Documento (sha256) | Note |", "|---|---|---|---|---|"]
        for e in epub:
            d = e.get("dati") or {}
            dd = ", ".join(f"{k}: {MOTIVI.get(v, v) if k == 'motivo' else v}" for k, v in d.items()
                           if k in ("esito", "motivo", "limite_5bis", "opposizione"))
            if e["tipo"] in ("risposta", "pronuncia-difensore") and not d.get("rivisto"):
                dd += " · *esito non ancora rivisto da un umano*"
            h = (e.get("documento") or {}).get("sha256", "")
            md.append(f"| {e['data']} | {e['tipo']} | {dd} | {('`' + h[:12] + '…`') if h else ''} | {e.get('note', '')} |")
        if testi and r["id"] in testi:
            t = redazione.redigi_istanza(testi[r["id"]], r_orig, richiedente,
                                         pec_pub.get(cmp_id, False))[0]
            md += ["", "## Testo dell'istanza (versione pubblica, redatta)", "", t]
        md += ["", "*Gli esiti non rivisti da un umano sono marcati come tali (§ 1, principio 6); i documenti ricevuti si pubblicano solo dopo la "
               "redazione (specifica § 5.5).*"]
        (content / "richieste" / f"{r['id']}.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # campagne
    k_tot = indicatori(richieste, ev_per_id, oggi)
    k_c = {c["id"]: indicatori([r for r in richieste if r.get("campagna") == c["id"]], ev_per_id, oggi) for c in campagne}
    camp_pub = []
    for c in campagne:
        cp = {k: v for k, v in c.items() if k != "richiedente_id"}
        camp_pub.append(cp)
        k = k_c[c["id"]]
        md = [fm(c["titolo"], c["scopo"][:150], oggi), banner, f"**Stato della campagna:** {c['stato']} · creata il {c['creata']}"
              + (f" · approvata ({c['approvata']['decisione']})" if c.get("approvata") else " · non approvata"), "",
              f"**Scopo.** {c['scopo']}", "", f"**Progetto:** {c['progetto']['nome']} {c['progetto'].get('issue', '')} · "
              f"**Responsabile:** {c['responsabile']['nome']}", "", "## Perimetro e criteri", ""]
        md += [f"- **{k_}:** {v}" for k_, v in c.get("perimetro", {}).items()]
        md += [f"- {x}" for x in c.get("criteri", [])]
        md += ["", f"Selezione ripetibile: `{c.get('selezione', {}).get('comando', '')}`", "", "## Parametri", "",
               "| Parametro | Valore |", "|---|---|"] + [f"| {k_} | {v} |" for k_, v in c.get("parametri", {}).items()]
        md += ["", "## Modelli (versioni bloccate all'approvazione)", "", "| Modello | Versione | sha256 |", "|---|---|---|"]
        md += [f"| {n} | {m['versione']} | `{m['sha256'][:16]}…` |" for n, m in c["modelli"].items()]
        md += ["", f"**Licenza dei dati:** {c['licenza_dati']}", "", "## Dashboard della campagna", "", tab_indicatori(k),
               "## Richieste", "", "| Richiesta | Ente | Stato | Esito |", "|---|---|---|---|"]
        md += [f"| [{x['id']}]({x['pagina']}) | {x['ente_nome']} | {x['stato']} | {x['esito']} |" for x in righe
               if x["campagna"] == c["id"]] or ["| — | nessuna richiesta | | |"]
        (content / "campagne" / f"{c['id']}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
        (vdir / "campagne" / c["id"]).mkdir(parents=True, exist_ok=True)
        (vdir / "campagne" / c["id"] / "richieste.csv").write_text(
            csv_testo([x for x in righe if x["campagna"] == c["id"]], CAMPI_RICHIESTE), encoding="utf-8")
    (content / "campagne" / "_index.md").write_text(fm("Campagne di accesso civico", "Elenco delle campagne.", oggi) + banner
                                                    + "\n".join(f"- [{c['titolo']}](/accesso-civico/campagne/{c['id']}/) — {c['stato']}"
                                                                for c in campagne) + "\n", encoding="utf-8")
    # enti
    per_ente = collections.defaultdict(list)
    for x in righe:
        per_ente[x["ente_cf"]].append(x)
    tempi_enti = []
    for cf, xs in sorted(per_ente.items()):
        gg = [x["giorni_risposta"] for x in xs if isinstance(x["giorni_risposta"], int)]
        med, p90 = mediana_p90(gg)
        tempi_enti.append({"ente_cf": cf, "ente_nome": xs[0]["ente_nome"], "tipologia_istat": xs[0]["tipologia_istat"],
                           "regione": xs[0]["regione"], "richieste": len(xs), "risposte": len(gg), "mediana_giorni": med,
                           "p90_giorni": p90, "dinieghi": sum(x["esito"] == "diniego" for x in xs),
                           "silenzi": sum(x["stato"] == "silenzio" for x in xs)})
        md = [fm(xs[0]["ente_nome"], f"Richieste di accesso civico a {xs[0]['ente_nome']}.", oggi), banner,
              f"CF {cf} · {xs[0]['tipologia_istat']} · {xs[0]['regione']}", "",
              f"Risposte {len(gg)}/{len(xs)}; tempo mediano {med if med is not None else '—'} giorni.", "",
              "| Richiesta | Campagna | Stato | Esito | Giorni |", "|---|---|---|---|---|"]
        md += [f"| [{x['id']}]({x['pagina']}) | {x['campagna']} | {x['stato']} | {x['esito']} | {x['giorni_risposta']} |" for x in xs]
        (content / "enti" / f"{cf}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    for sez, tit in (("richieste", "Richieste"), ("enti", "Enti")):
        (content / sez / "_index.md").write_text(fm(f"{tit} di accesso civico", f"{tit}.", oggi) + banner, encoding="utf-8")
    # dashboard + panoramica
    dash = {"generato": oggi, "versione": VERSIONE, "sintetico": sintetico, "totale": k_tot, "per_campagna": k_c}
    (static / "dashboard.json").write_text(json.dumps(dash, ensure_ascii=False, indent=1), encoding="utf-8")
    md = [fm("Accesso civico", "Richieste di accesso civico generalizzato: campagne, stati, tempi, esiti.", oggi), banner,
          "Ogni richiesta ha una pagina con la sua storia; ogni campagna una dashboard. Indicatori calcolati solo dal "
          "registro degli eventi. [Dati scaricabili](/accesso-civico/dati/) · [JSON della dashboard](/accesso-civico/dashboard.json)", "",
          "## Campagne", "", "| Campagna | Stato | Richieste | Inviate | Risposte | Silenzi |", "|---|---|---|---|---|---|"]
    md += [f"| [{c['titolo']}](/accesso-civico/campagne/{c['id']}/) | {c['stato']} | {k_c[c['id']]['richieste']} | "
           f"{k_c[c['id']]['inviate']} | {sum(k_c[c['id']]['esiti_risposte'].values())} | {k_c[c['id']]['scadute_in_silenzio']} |"
           for c in campagne]
    md += ["", "## Dashboard complessiva", "", tab_indicatori(k_tot)]
    (content / "_index.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    # dataset
    file_ds = {"richieste.csv": csv_testo(righe, CAMPI_RICHIESTE),
               "eventi.jsonl": "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in ev_pub),
               "enti-tempi.csv": csv_testo(tempi_enti, list(tempi_enti[0]) if tempi_enti else ["ente_cf"]),
               "campagne.json": json.dumps(camp_pub, ensure_ascii=False, indent=1) + "\n",
               "dizionario.md": DIZIONARIO,
               "LICENZA.txt": f"{LICENZA_SEGNAPOSTO}\nCodice: vedi il repository. Documenti degli enti: dati pubblici, "
                              "riuso salvo dati personali (art. 7 d.lgs. 33/2013, da rileggere).\n"}
    for n, t in file_ds.items():
        (vdir / n).write_text(t, encoding="utf-8")
    elenco = sorted(p for p in vdir.rglob("*") if p.is_file())
    manifest = {"formato": "spesaict.accesso-civico-manifest/1", "versione": oggi, "generatore": f"pubblica.py {VERSIONE}",
                "sintetico": sintetico, "licenza": LICENZA_SEGNAPOSTO,
                "file": [{"percorso": p.relative_to(vdir).as_posix(), "sha256": sha(p.read_bytes()), "byte": p.stat().st_size,
                          "righe": p.read_text(encoding="utf-8").count("\n")} for p in elenco]}
    (vdir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (vdir / "SHA256SUMS").write_text("".join(f"{f['sha256']}  {f['percorso']}\n" for f in manifest["file"])
                                     + f"{sha((vdir / 'manifest.json').read_bytes())}  manifest.json\n", encoding="utf-8")
    shutil.copytree(vdir, static / "dati/ultima")
    ds = [fm("Dati scaricabili dell'accesso civico", "Dataset versionati con manifest e sha256.", oggi), banner,
          f"Versione corrente: `dati/v/{oggi}/` (alias `dati/ultima/`). Verifica: `sha256sum -c SHA256SUMS`. "
          f"Licenza: {LICENZA_SEGNAPOSTO}", "", "| File | Byte | sha256 |", "|---|---|---|"]
    ds += [f"| [{f['percorso']}](/accesso-civico/dati/v/{oggi}/{f['percorso']}) | {f['byte']} | `{f['sha256'][:16]}…` |"
           for f in manifest["file"]]
    (content / "dati.md").write_text("\n".join(ds) + "\n", encoding="utf-8")
    # controllo finale dei residui su TUTTO l'output
    problemi = {}
    for p in uscita.rglob("*"):
        if p.is_file():
            res = redazione.residui(p.read_text(encoding="utf-8"), consentite, richiedente)
            if res:
                problemi[p.relative_to(uscita).as_posix()] = res
    if problemi:
        raise SystemExit(f"RESIDUI di dati personali nell'output pubblico, generazione respinta: {problemi}")
    return {"uscita": str(uscita), "richieste": len(righe), "eventi": len(ev_pub), "campagne": len(campagne),
            "enti": len(per_ente), "file_dataset": len(manifest["file"]), "sintetico": sintetico}


def carica_registro(d):
    d = Path(d)
    richieste = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(d.glob("ac-*.json"))]
    eventi = [e for evs in stati.leggi(d / "eventi.jsonl").values() for e in evs] if (d / "eventi.jsonl").exists() else []
    return richieste, eventi


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--sintetico", action="store_true")
    g.add_argument("--registro")
    ap.add_argument("--oggi", default=dt.date.today().isoformat())
    ap.add_argument("--uscita", default=str(USCITA))
    a = ap.parse_args()
    uscita = Path(a.uscita).resolve()
    if any(uscita == x or x in uscita.parents for x in (R / "docs", R / "sito")):
        raise SystemExit("uscita in docs/ o sito/ vietata: solo anteprima (nessuna pubblicazione)")
    reali = [cmp.carica(p) for p in sorted(cmp.DIR.glob("cmp-*.json"))]
    if a.sintetico:
        camp, richieste, eventi, testi, rich = sintetici(a.oggi)
        print(json.dumps(genera(reali + camp, richieste, eventi, a.oggi, uscita, testi, rich, sintetico=True), ensure_ascii=False))
    else:
        richieste, eventi = carica_registro(R / a.registro)
        print(json.dumps(genera(reali, richieste, eventi, a.oggi, uscita), ensure_ascii=False))


if __name__ == "__main__":
    main()
