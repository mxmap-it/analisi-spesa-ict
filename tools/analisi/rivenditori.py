"""Mappa dei rivenditori dei prodotti cloud (#41): chi incassa i contratti il cui prodotto è di un provider, e quanto.
Legge lavoro/attribuzione/*.csv (attribuisci_provider.py). Esclude i padri di accordo quadro (massimali, non spesa).
Per ogni contratto con un provider attribuito: canale diretto (incassa il provider) o rivenditore; il PSN è marcato
a parte quando nel testo compare anche un prodotto di big tech (PSN che eroga tecnologia di hyperscaler).
Uso: python tools/analisi/rivenditori.py  -> lavoro/attribuzione/rivenditori.csv e .json (la copia pubblicata è report/metodo/rivenditori-v3.*)"""
import collections, csv, datetime, glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from classifica import Classificatore  # noqa: E402

BIGTECH = {"Microsoft", "Amazon Web Services", "Google", "Oracle", "IBM", "Salesforce", "ServiceNow", "Adobe", "Zoom", "Cisco Webex", "Cloudera"}

def normalizza(nome):
    """Denominazione confrontabile: maiuscolo, senza punteggiatura e forme societarie."""
    n = re.sub(r"[^\w\s]", " ", nome.upper())
    n = re.sub(r"\b(S\s*P\s*A|S\s*R\s*L|SPA|SRL|S\s*C\s*P\s*A|SCPA|SOCIETA\s+PER\s+AZIONI|IN\s+FORMA\s+ABBREVIATA.*)\b", " ", n)
    return re.sub(r"\s+", " ", n).strip()

def main():
    c = Classificatore()
    oggi = datetime.date.today().isoformat()
    agg = collections.defaultdict(lambda: {"contratti": 0, "importo": 0.0, "provider": collections.Counter(), "nomi": set()})
    psn_bigtech = []
    totali = collections.Counter()
    da_verificare = collections.Counter()
    for f in sorted(glob.glob("lavoro/attribuzione/[0-9]*.csv") + []):
        if "campione" in os.path.basename(f): continue
        for r in csv.DictReader(open(f, encoding="utf-8")):
            if r["e_padre"] == "1" or not r["provider"] or r["servizio"] in ("servizi-professionali", "in-house", "software-infrastruttura"): continue
            imp = float(r["importo_lotto"] or 0)
            if r.get("importo_da_verificare"):  # probabile massimale di convenzione: contato a parte (attribuisci_provider.py)
                da_verificare[r["provider"]] += imp; continue
            presenti = c.marchi_presenti(r["testo"])
            if "Polo Strategico Nazionale" in presenti and BIGTECH & set(presenti):
                psn_bigtech.append({"cig": r["cig"], "importo": imp, "bigtech": sorted(BIGTECH & set(presenti)), "aggiudicatari": r["aggiudicatari"], "testo": r["testo"][:300]})
            canale = c.canale(r["provider"], [a.strip() for a in r["aggiudicatari"].split(";") if a.strip()])
            totali[(r["provider"], canale)] += imp
            if canale != "rivenditore": continue
            for nome in [a.strip() for a in r["aggiudicatari"].split(";") if a.strip()]:
                k = normalizza(nome)
                a = agg[k]
                a["contratti"] += 1; a["importo"] += imp; a["provider"][r["provider"]] += imp; a["nomi"].add(nome)
    righe = sorted(agg.items(), key=lambda kv: -kv[1]["importo"])
    os.makedirs("lavoro/attribuzione", exist_ok=True)
    with open("lavoro/attribuzione/rivenditori.csv", "w", newline="", encoding="utf-8") as fo:
        w = csv.writer(fo)
        w.writerow(["rivenditore", "contratti", "importo_eur", "quota_bigtech", "provider_rivenduti", "denominazioni"])
        for k, a in righe:
            bt = sum(v for p, v in a["provider"].items() if p in BIGTECH)
            w.writerow([k, a["contratti"], round(a["importo"]), round(bt / a["importo"], 3) if a["importo"] else "",
                        " ; ".join(f"{p}={round(v)}" for p, v in a["provider"].most_common()), " | ".join(sorted(a["nomi"])[:5])])
    sintesi = {"generato": oggi, "regole": "v3", "nota": "importi = importo_lotto dei contratti attuativi (padri di AQ e importi da verificare esclusi), anni di pubblicazione 2022-2026; per ogni CIG l’ultima versione pubblicata",
               "per_provider_e_canale": [{"provider": p, "canale": ch, "importo": round(v)} for (p, ch), v in sorted(totali.items(), key=lambda x: -x[1])],
               "esclusi_importi_da_verificare": {p: round(v) for p, v in da_verificare.most_common()},
               "rivenditori": len(righe),
               "primi_20": [{"rivenditore": k, "contratti": a["contratti"], "importo": round(a["importo"]), "provider": dict(a["provider"].most_common(5))} for k, a in righe[:20]],
               "psn_con_bigtech": {"contratti": len(psn_bigtech), "importo": round(sum(x["importo"] for x in psn_bigtech)), "esempi": psn_bigtech[:15]}}
    json.dump(sintesi, open("lavoro/attribuzione/rivenditori.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=float)
    print(json.dumps({k: v for k, v in sintesi.items() if k != "psn_con_bigtech"} | {"psn_con_bigtech": {k: v for k, v in sintesi["psn_con_bigtech"].items() if k != "esempi"}}, indent=1, ensure_ascii=False))

if __name__ == "__main__":
    main()
