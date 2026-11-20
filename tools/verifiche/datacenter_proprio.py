#!/usr/bin/env python3
"""Cloud in proprio: riconoscere la spesa per datacenter propri nell'imbuto (#52). Versione 0.1 (20/11/2026).

Decisioni di Fabio del 20/11/2026 (DECISIONI.md): il datacenter di proprietà dell'ente è sovrano (IT) anche con
tecnologia extra-UE; il calcolo scientifico entra come voce separata; nei contratti misti serve la prevalenza della parte
da datacenter; rete e gestione dei sistemi contano solo se la gara nomina il datacenter.

Ingressi: lavoro/imbuto/ict.csv (tutti gli anni), config/datacenter_proprio.yaml (regole con i CPV),
config/societa_inhouse_ict.yaml (per le in-house ICT «cloud» nel testo è il loro cloud, non un servizio esterno).
0.2: «San» luogo, CPV 30236 generico e UPS da postazione tolti; famiglia backup separata (peso 1) dalla virtualizzazione
(peso 2); 0.3: servizi di datacenter o cloud affidati a una società ICT in-house (config/societa_inhouse_ict.yaml) = esito «servizio-inhouse»; 0.4: workstation, assistenza generica, smart card contro; noleggio di server, server virtuali, servizi a consumo e offsite esterni; edizioni «Data Center» di Atlassian tolte; CPV piattaforme e lettori fuori; contratti madre di convenzioni e accordi quadro esclusi (massimali); server di videosorveglianza, presenze, diagnostica pesano contro; Microsoft 365 è esterno.
0.5 (20/11/2026, #82): le società ICT pubbliche si riconoscono per CODICE FISCALE (stazione appaltante e aggiudicatari,
lavoro/inhouse/cig-cf.csv.gz da tools/verifiche/inhouse_cf.py) contro il dataset dal censimento MEF
(dati/inhouse/societa-ict-pa.csv, classi in-house, controllata, controllo-pubblico-congiunto); il nome
(config/societa_inhouse_ict.yaml) resta solo se mancano i codici fiscali, e il riepilogo conta le differenze fra le due vie.
Per ogni CIG dell'imbuto che tocca almeno una famiglia:
  punteggio datacenter = somma dei pesi delle famiglie trovate (rete e gestione solo con il sito) + bonus se il CPV è da datacenter;
  punteggio postazioni = segni di PC, stampanti, telefonia, didattica + bonus se il CPV è da postazioni;
  esito «dc-proprio» se c'è una famiglia nucleo, nessun segno di servizio esterno (cloud, hosting, housing, PSN…),
  punteggio datacenter > punteggio postazioni e, per le sottoclassi generiche, punteggio datacenter >= soglia;
  «misto-incerto» se le due parti si equivalgono; «esterno» se ci sono segni di servizio esterno; altrimenti «debole».
La decisione finale (da quale stato dell'imbuto si può arrivare) la prende tools/verifiche/imbuto_spostamenti.py (livello DC).

Uso: python3 tools/verifiche/datacenter_proprio.py [AAAA-MM-GG]
Uscite: esiti/<data>/imbuto/datacenter/{datacenter-cig.csv.gz, riepilogo.json}
"""
import collections
import csv
import gzip
import io
import json
import os
import re
import sys
from datetime import date

import yaml

VERSIONE = "0.5"
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GIORNO = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
ICT = os.environ.get("IMBUTO_ICT", os.path.join(R, "lavoro/imbuto/ict.csv"))
OUT = os.path.join(R, "esiti", GIORNO, "imbuto", "datacenter")
CFG = yaml.safe_load(open(os.path.join(R, "config/datacenter_proprio.yaml"), encoding="utf-8"))
csv.field_size_limit(10**9)
SOC = yaml.safe_load(open(os.path.join(R, "config/societa_inhouse_ict.yaml"), encoding="utf-8"))["societa"]
RX_INHOUSE = re.compile("|".join(f"(?:{v['regex']})" for v in SOC.values()))
PUBBLICHE = {"in-house", "controllata", "controllo-pubblico-congiunto"}
SOC_CF = {k: r["classe"] for r in csv.DictReader(open(os.path.join(R, "dati/inhouse/societa-ict-pa.csv"), encoding="utf-8"))
          if r["classe"] in PUBBLICHE for k in (r["cf"], r["partita_iva"]) if k}
N_SOC = sum(1 for r in csv.DictReader(open(os.path.join(R, "dati/inhouse/societa-ict-pa.csv"), encoding="utf-8")) if r["classe"] in PUBBLICHE)
CIG_CF_FILE = os.path.join(R, "lavoro/inhouse/cig-cf.csv.gz")
CIG_CF = ({r["cig"]: (r["cf_sa"], r["cf_aggiudicatari"]) for r in csv.DictReader(gzip.open(CIG_CF_FILE, "rt", encoding="utf-8"))}
          if os.path.exists(CIG_CF_FILE) else {})
CONFRONTO = collections.Counter()   # via del nome contro via del codice fiscale
GENERICHE = {"ict-altro", "cpv-non-ict-testo-ict", ""}
ORDINE = ["calcolo-scientifico", "sito", "virtualizzazione", "server-storage", "backup", "rete", "gestione"]


def cpv_in(cpv, lista):
    return any(cpv.startswith(p) for p in lista)


def pubblica(cf):
    return re.sub(r"\D", "", cf or "").zfill(11) in SOC_CF if cf and re.sub(r"\D", "", cf) else False


def classifica(testo, cpv, sottoclasse, sa="", agg="", cig=""):
    t = re.sub(CFG["togli"], " ", testo.lower())
    cpv = (cpv or "").replace("-", "")
    F = CFG["famiglie"]
    trovate, sdc = [], 0
    for k, f in F.items():
        hit = re.search(f["regex"], t) is not None
        hit_cpv = cpv_in(cpv, f.get("cpv") or [])
        if hit or hit_cpv:
            trovate.append(k)
    trovate_valide = [k for k in trovate if not F[k].get("solo_con") or F[k]["solo_con"] in trovate]
    for k in trovate_valide:
        sdc += F[k]["peso"]
        if cpv_in(cpv, F[k].get("cpv") or []):
            sdc += CFG["bonus_cpv"]
    P = CFG["postazioni"]
    spost = len(set(m.group(0) for m in re.finditer(P["regex"], t))) * P["peso"]
    if cpv_in(cpv, P["cpv"]):
        spost += CFG["bonus_cpv"]
    spost += len(set(m.group(0) for m in re.finditer(CFG["altro_scopo"]["regex"], t))) * CFG["altro_scopo"]["peso"]
    nucleo = any(F[k].get("nucleo") for k in trovate_valide)
    nome_sa = RX_INHOUSE.search((sa or "").upper()) is not None
    nome_agg = any(RX_INHOUSE.search(a.strip().upper()) for a in re.split(r"\s*[|;]\s*", agg or "") if a.strip())
    if cig in CIG_CF:
        cf_sa, cf_agg = CIG_CF[cig]
        inhouse = pubblica(cf_sa)
        agg_inhouse = any(pubblica(c) for c in cf_agg.split("|"))
        CONFRONTO[("sa", nome_sa, inhouse)] += 1
        CONFRONTO[("agg", nome_agg, agg_inhouse)] += 1
    else:
        inhouse, agg_inhouse = nome_sa, nome_agg
        CONFRONTO["senza-cf"] += 1
    esterno = not inhouse and re.search(CFG["esterno"]["regex"], re.sub(CFG["esterno"]["eccezioni"], " ", t)) is not None
    padre = re.search(CFG["padre"]["regex"], t) is not None and re.search(CFG["padre"]["salvo"], t) is None
    rx_est = re.search(CFG["esterno"]["regex"], t) is not None
    if agg_inhouse and not padre and (trovate_valide or rx_est) and spost < max(sdc, 2):
        # servizio di datacenter o cloud affidato a una società ICT in-house pubblica: cloud in proprio pubblico
        esito = "servizio-inhouse"
    elif not trovate_valide:
        esito = "nessuna"
    elif padre:
        esito = "padre-convenzione"
    elif esterno:
        esito = "esterno"
    elif sdc > spost and nucleo and (sottoclasse not in GENERICHE or sdc >= CFG["soglia_generico"]):
        esito = "dc-proprio"
    elif sdc == spost or (sdc > spost and sdc < CFG["soglia_generico"]):
        esito = "misto-incerto"
    else:
        esito = "prevalgono-postazioni"
    fam = next((k for k in ORDINE if k in trovate_valide), "")
    return esito, fam, trovate_valide, sdc, spost


def main():
    os.makedirs(OUT, exist_ok=True)
    tot = collections.defaultdict(lambda: [0, 0.0])
    visti = set()
    n = 0
    # gzip senza data (mtime=0): stessi byte a ogni esecuzione, così lo sha256 citato dalla tabella unica è
    # ripetibile (prova da clone pulito del 20/11/2026, #81)
    with gzip.GzipFile(os.path.join(OUT, "datacenter-cig.csv.gz"), mode="wb", mtime=0) as gz, \
            io.TextIOWrapper(gz, encoding="utf-8", newline="") as fo:
        w = csv.writer(fo)
        w.writerow(["cig", "anno", "strato", "sottoclasse", "esito", "famiglia", "famiglie", "punti_datacenter", "punti_postazioni", "importo"])
        for r in csv.DictReader(open(ICT, encoding="utf-8", newline="")):
            cig = r["cig"].strip().upper()
            if cig in visti:
                continue
            visti.add(cig)
            esito, fam, tr, sdc, sp = classifica(r["testo"] or "", r["cod_cpv"], r["sottoclasse"], r["stazione_appaltante"], r["aggiudicatari"], cig)
            if esito == "nessuna":
                continue
            n += 1
            imp = float(r["importo"] or 0)
            per = "2020-2023" if int(r["anno"] or 0) <= 2023 else "dal-2024"
            k = (per, esito, fam if esito == "dc-proprio" else "")
            tot[k][0] += 1; tot[k][1] += imp
            w.writerow([cig, r["anno"], r["strato"], r["sottoclasse"], esito, fam, "|".join(tr), sdc, sp, round(imp, 2)])
    out = {"versione": VERSIONE, "data": GIORNO, "strumento": "tools/verifiche/datacenter_proprio.py",
           "config": {"file": "config/datacenter_proprio.yaml", "versione": CFG["versione"]},
           "nota": "esiti per CIG sul solo testo e CPV, prima di guardare lo stato dell'imbuto; importi lordi (importo del lotto)",
           "riconoscimento_societa_pubbliche": {"via": "codice fiscale" if CIG_CF else "nome (cig-cf.csv.gz assente)",
               "societa_pubbliche_ict": N_SOC, "cig_senza_cf": CONFRONTO["senza-cf"],
               "confronto_nome_cf": {f"{k[0]} nome={'sì' if k[1] else 'no'} cf={'sì' if k[2] else 'no'}": v
                                     for k, v in sorted(CONFRONTO.items(), key=str) if isinstance(k, tuple) and (k[1] or k[2])}},
           "cig_con_famiglie": n,
           "per_esito": [{"periodo": k[0], "esito": k[1], "famiglia": k[2], "cig": v[0], "meur_lordi": round(v[1] / 1e6, 1)}
                         for k, v in sorted(tot.items())]}
    json.dump(out, open(os.path.join(OUT, "riepilogo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=0))


if __name__ == "__main__":
    main()
