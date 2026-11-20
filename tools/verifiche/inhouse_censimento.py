#!/usr/bin/env python3
"""Elenco delle società ICT in-house e controllate dalla PA, dal censimento MEF delle partecipazioni (#52). Versione 0.2 (20/11/2026).

Richiesta di Fabio del 20/11/2026: l'elenco delle in-house ICT deve venire dal censimento ufficiale delle partecipazioni
pubbliche (MEF, Dipartimento dell'Economia, dati al 31/12/2023, CC BY 4.0), per codice fiscale, non dai soci Assinter.

Criteri (una riga per società partecipata, chiave: codice fiscale):
  ICT          (0.2) anche i soci Assinter con ATECO dichiarato diverso (es. InnovaPuglia: «consulenza gestionale»),
               con ateco=altro; per il resto divisione ATECO 62 (software e consulenza informatica) o 63 (servizi d'informazione), dichiarata dagli enti;
  classe       in-house    almeno un ente dichiara «controllo analogo» (anche congiunto) o un affidamento «Diretto»
                           insieme a un controllo pubblico;
               (l'affidamento diretto a una società pubblica è in-house per legge: art. 7 d.lgs. 36/2023);
               controllata almeno un ente dichiara un controllo (solitario o congiunto) senza i segni dell'in-house;
               partecipata nessun controllo dichiarato (quote di minoranza): resta nel dataset, fuori dalla vista in-house.
  Gli enti dichiarano cose diverse sulla stessa società: si conta quanti enti dichiarano ciascun segno.
Sito web: dall'Indice PA (amministrazioni.txt, campo sito_istituzionale) per codice fiscale, quando la società è
iscritta come gestore di pubblico servizio; altrimenti vuoto (si completa in config/inhouse_siti.yaml, con la fonte).
Controprova: config/societa_inhouse_ict.yaml (soci Assinter + Sogei, CINECA, PagoPA), per nome.

Uso: python3 tools/verifiche/inhouse_censimento.py
Uscite: dati/inhouse/societa-ict-pa.csv (dataset), dati/inhouse/riepilogo.json
"""
import collections
import csv
import glob
import hashlib
import json
import os
import re

import yaml

VERSIONE = "0.2"
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MEF_URL = "https://www.de.mef.gov.it/modules/documenti_it/attivo_patrimonio/partecipazioni_2023/dati_partecipazioni_anno_2023.csv"
MEF = os.path.join(R, "archivio/mirror/www.de.mef.gov.it/modules/documenti_it/attivo_patrimonio/partecipazioni_2023/dati_partecipazioni_anno_2023.csv")
IPA = glob.glob(os.path.join(R, "archivio/mirror/indicepa.gov.it/ipa-dati/dataset/*/resource/*/download/amministrazioni.txt"))
SITI = os.path.join(R, "config/inhouse_siti.yaml")
OUT = os.path.join(R, "dati/inhouse")
ICT = {"PRODUZIONE DI SOFTWARE, CONSULENZA INFORMATICA E ATTIVITÀ CONNESSE": "62",
       "ATTIVITÀ DEI SERVIZI D'INFORMAZIONE E ALTRI SERVIZI INFORMATICI": "63"}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def num(x):
    try:
        return float((x or "").replace(".", "").replace(",", "."))
    except ValueError:
        return None


def main():
    assinter = yaml.safe_load(open(os.path.join(R, "config/societa_inhouse_ict.yaml"), encoding="utf-8"))["societa"]
    rx = {k: re.compile(v["regex"]) for k, v in assinter.items()}
    righe = list(csv.DictReader(open(MEF, encoding="latin1", newline=""), delimiter=";"))
    soc = {}
    for x in righe:
        div = ICT.get(x["Partecipata Divisione ATECO"])
        nome = x["Partecipata Denominazione"].strip().upper()
        socio = [k for k, r in rx.items() if r.search(nome)]
        if not div and not socio:
            continue
        cf = re.sub(r"\D", "", x["Partecipata Codice Fiscale"]).zfill(11)
        s = soc.setdefault(cf, {"cf": cf, "denominazione": x["Partecipata Denominazione"].strip(), "ateco": div or "altro",
                                "forma": x["Partecipata Forma Giuridica"], "stato": x["Partecipata Stato Giuridico"],
                                "regione": x["Partecipata Regione Sede"], "comune": x["Partecipata Comune Sede"],
                                "ateco_dichiarato": x["Partecipata Divisione ATECO"], "enti": set(), "analogo": set(), "controllo": set(), "diretto": set(), "quota": 0.0,
                                "addetti": None, "fatturato_2023": None, "valore_produzione": None, "importo_servizi": 0.0,
                                "servizi": collections.Counter()})
        ente = x["Amministrazione Codice Fiscale"].strip()
        s["enti"].add(ente)
        tc = x["Tipo controllo"].lower()
        if "analogo" in tc:
            s["analogo"].add(ente)
        if tc.startswith("controllo"):
            s["controllo"].add(ente)
        s["quota"] += num(x["Quota partecipazione diretta (%)"]) or 0
        for i in range(1, 6):
            if x[f"Modalità affidamento servizio {i}"] == "Diretto":
                s["diretto"].add(ente)
            if x[f"Servizio affidato {i}"]:
                s["servizi"][x[f"Servizio affidato {i}"].strip()] += 1
                s["importo_servizi"] += num(x[f"Importo impegnato servizio {i}"]) or 0
        for k, c in (("addetti", "Partecipata Numero di addetti"), ("fatturato_2023", "Fatturato 2023"),
                     ("valore_produzione", "Partecipata Valore della produzione - CO.E.P.")):
            v = num(x[c])
            if v is not None and (s[k] is None or v > s[k]):
                s[k] = v
    # siti: Indice PA, poi la tabella curata a mano
    ipa = {}
    if IPA:
        for a in csv.DictReader(open(IPA[0], encoding="utf-8-sig", newline=""), delimiter="\t"):
            if a.get("cf") and a.get("sito_istituzionale"):
                ipa[re.sub(r"\D", "", a["cf"]).zfill(11)] = (a["sito_istituzionale"].strip(), a["cod_amm"])
    mano = (yaml.safe_load(open(SITI, encoding="utf-8")) or {}).get("siti", {}) if os.path.exists(SITI) else {}
    out = []
    for cf, s in soc.items():
        classe = ("in-house" if s["analogo"] or s["diretto"] else
                  "controllata" if s["controllo"] else "partecipata")
        sito, fonte_sito = "", ""
        if cf in mano:
            sito, fonte_sito = mano[cf]["sito"], mano[cf].get("fonte", "a mano")
        elif cf in ipa:
            sito, fonte_sito = ipa[cf][0], f"Indice PA ({ipa[cf][1]})"
        if sito and not sito.startswith("http"):
            sito = "https://" + sito
        ass = [k for k, r in rx.items() if r.search(s["denominazione"].upper())]
        out.append({"cf": cf, "denominazione": s["denominazione"], "classe": classe, "ateco": s["ateco"], "ateco_dichiarato": s["ateco_dichiarato"],
                    "stato": s["stato"], "forma": s["forma"], "regione": s["regione"], "comune": s["comune"],
                    "enti_dichiaranti": len(s["enti"]), "enti_controllo_analogo": len(s["analogo"]),
                    "enti_affidamento_diretto": len(s["diretto"]), "quota_pubblica_dichiarata": round(min(s["quota"], 100), 2),
                    "addetti": s["addetti"] or "", "fatturato_2023": s["fatturato_2023"] or "",
                    "valore_produzione": s["valore_produzione"] or "", "importo_servizi_affidati": round(s["importo_servizi"], 2),
                    "servizio_principale": s["servizi"].most_common(1)[0][0] if s["servizi"] else "",
                    "sito": sito, "fonte_sito": fonte_sito, "assinter": "|".join(ass)})
    ordine = {"in-house": 0, "controllata": 1, "partecipata": 2}
    out.sort(key=lambda r: (ordine[r["classe"]], r["stato"] != "Attiva", -(r["fatturato_2023"] or 0)))
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "societa-ict-pa.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    trovati = {k for r in out for k in r["assinter"].split("|") if k}
    c = collections.Counter((r["classe"], r["stato"] == "Attiva") for r in out)
    riep = {"versione": VERSIONE, "strumento": "tools/verifiche/inhouse_censimento.py",
            "fonte": {"url": MEF_URL, "sha256": sha(MEF), "licenza": "CC BY 4.0", "dati_al": "2023-12-31",
                      "editore": "MEF, Dipartimento dell'Economia, censimento delle partecipazioni pubbliche"},
            "righe_censimento": len(righe), "societa_ict": len(out),
            "per_classe": {f"{k[0]}{'' if k[1] else ' (non attiva)'}": v for k, v in sorted(c.items())},
            "con_sito": sum(1 for r in out if r["sito"]),
            "controprova_assinter": {"elenco": len(assinter), "trovate_nel_censimento_ict": sorted(trovati),
                                     "non_trovate": sorted(set(assinter) - trovati)}}
    json.dump(riep, open(os.path.join(OUT, "riepilogo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(riep, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
