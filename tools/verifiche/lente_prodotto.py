"""#40 Lente prodotto: precisione e richiamo del dizionario dei marchi (config/marchi_cloud.yaml, vie 3)
sul campione v3 di 611 CIG (riferimento: dati/classificazioni/campione-v3.jsonl, via 6 + revisione).

Si guarda SOLO il testo della gara (oggetto del CIG), non il fornitore: è la lente prodotto.
- predetto: primo marchio del dizionario che compare nel testo (Classificatore.marchio), nome canonico;
- riferimento: esito.provider_prodotto del campione, ricondotto allo stesso nome canonico (tabella RIF sotto);
- per provider: TP/FP/FN, precisione e richiamo con Wilson 95%;
- aggregato "prodotti esteri" (provider EXTRA-UE del dizionario) e "big tech USA";
- menzioni in negativo: falsi positivi il cui testo contiene una formula di uscita/migrazione/sostituzione.
Il campione è stratificato (non casuale sull'universo): i valori valgono per il campione.

Uso: python tools/verifiche/lente_prodotto.py -> esiti/<oggi>/lente-prodotto/lente-prodotto.json (+ errori.csv)"""
import csv, json, os, re, sys, math, datetime, collections
from pathlib import Path

RADICE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RADICE / "tools/analisi"))
from classifica import Classificatore, NOME_CANONICO  # noqa: E402

# riferimento (testo libero del campione) -> nome canonico del dizionario; il primo che combacia vince
RIF = [(r"spc\s*cloud|rti\s+spc", "SPC Cloud lotto 1"), (r"polo\s+strategico|\bpsn\b", "Polo Strategico Nazionale"),
       (r"microsoft|azure|office\s*365", "Microsoft"), (r"amazon|\baws\b", "Amazon Web Services"),
       (r"google", "Google"), (r"oracle", "Oracle"), (r"\bsap\b", "SAP"), (r"vmware|broadcom", "VMware"),
       (r"salesforce", "Salesforce"), (r"servicenow", "ServiceNow"), (r"\bibm\b", "IBM"), (r"adobe", "Adobe"),
       (r"webex|cisco", "Cisco Webex"), (r"zoom", "Zoom"), (r"cloudera", "Cloudera"), (r"nextcloud", "Nextcloud"),
       (r"aruba", "Aruba"), (r"ovh", "OVHcloud"), (r"seeweb", "Seeweb"), (r"wiit", "WIIT"), (r"retelit", "Retelit"),
       (r"fastweb", "Fastweb"),
       (r"lepida|liguria digitale|csi piemonte|trentino digitale|\binva\b|cineca|in-house|sistema cloud toscana|cloud toscana",
        "In-house pubblico"),
       (r"^tim\b|telecom italia", "TIM")]
BIGTECH_USA = {"Microsoft", "Amazon Web Services", "Google", "Oracle", "IBM", "Salesforce", "ServiceNow", "Adobe",
               "VMware", "Cisco Webex", "Zoom", "Cloudera"}
RX_NEG = re.compile(r"migrazion\w*\s+(da|dal|dalla|dell)|dismission|in\s+sostituzione|uscita\s+da|\bexit\b|"
                    r"alternativ\w+\s+a|abbandon|da\s+\w+\s+a\s+", re.I)


def canon_rif(s):
    s = (s or "").strip().lower()
    for rx, n in RIF:
        if re.search(rx, s): return n
    return s and "altro:" + s


def wilson(k, n, z=1.96):
    if not n: return None
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - m, 3), round(c + m, 3)]


def pr(tp, fp, fn):
    return {"tp": tp, "fp": fp, "fn": fn,
            "precisione": round(tp / (tp + fp), 3) if tp + fp else None, "precisione_w95": wilson(tp, tp + fp),
            "richiamo": round(tp / (tp + fn), 3) if tp + fn else None, "richiamo_w95": wilson(tp, tp + fn)}


def main():
    cl = Classificatore()
    dizionario = {NOME_CANONICO.get(m["provider"], m["provider"]) for m in cl.marchi}
    giur = {NOME_CANONICO.get(m["provider"], m["provider"]): m["giurisdizione"] for m in cl.marchi}
    testi = {r["cig"]: r for r in csv.DictReader(open(RADICE / "report/metodo/campione-misura-v3-cieco.csv", encoding="utf-8"))}
    righe = []
    for l in open(RADICE / "dati/classificazioni/campione-v3.jsonl", encoding="utf-8"):
        d = json.loads(l); e = d["esito"]; t = testi[d["cig"]]["testo"]
        m, regola = cl.marchio(t)
        pred = NOME_CANONICO.get(m["provider"], m["provider"]) if m else ""
        rif = canon_rif(e.get("provider_prodotto"))
        righe.append({"cig": d["cig"], "pred": pred, "regola": regola, "rif": rif, "rif_testo": e.get("provider_prodotto") or "",
                      "servizio_rif": e.get("servizio") or "", "e_cloud_rif": e.get("e_cloud") or "",
                      "fonte_primaria": bool(e.get("fonte_primaria")), "negazione": bool(RX_NEG.search(t)), "testo": t[:300]})
    per = {}
    for p in sorted(dizionario):
        tp = sum(r["pred"] == p and r["rif"] == p for r in righe)
        fp = sum(r["pred"] == p and r["rif"] != p for r in righe)
        fn = sum(r["pred"] != p and r["rif"] == p for r in righe)
        if tp + fp + fn: per[p] = pr(tp, fp, fn)

    def gruppo(insieme):
        tp = sum(r["pred"] in insieme and r["rif"] == r["pred"] for r in righe)
        fp = sum(r["pred"] in insieme and r["rif"] != r["pred"] for r in righe)
        fn = sum(r["rif"] in insieme and r["pred"] != r["rif"] for r in righe)
        # a livello di "è un prodotto del gruppo?" (senza esigere il provider giusto)
        tp2 = sum(r["pred"] in insieme and r["rif"] in insieme for r in righe)
        fp2 = sum(r["pred"] in insieme and r["rif"] not in insieme for r in righe)
        fn2 = sum(r["rif"] in insieme and r["pred"] not in insieme for r in righe)
        return {"provider_esatto": pr(tp, fp, fn), "appartenenza_al_gruppo": pr(tp2, fp2, fn2)}

    estero = {p for p in dizionario if giur.get(p) == "EXTRA-UE"} | {"VMware"}
    err = [r for r in righe if (r["pred"] or r["rif"] in dizionario) and r["pred"] != r["rif"]]
    fp_neg = [r for r in err if r["pred"] and r["negazione"]]
    rif_nel_diz = sum(r["rif"] in dizionario for r in righe)
    out = {
        "riferimento": "dati/classificazioni/campione-v3.jsonl", "testi": "report/metodo/campione-misura-v3-cieco.csv",
        "dizionario": "config/marchi_cloud.yaml", "n_campione": len(righe),
        "riferimento_con_provider_del_dizionario": rif_nel_diz,
        "riferimento_senza_provider": sum(not r["rif"] for r in righe),
        "riferimento_fuori_dizionario": collections.Counter(r["rif"] for r in righe if r["rif"].startswith("altro:")).most_common(30),
        "predetti": sum(bool(r["pred"]) for r in righe),
        "per_provider": per, "estero_extra_ue": gruppo(estero), "bigtech_usa": gruppo(BIGTECH_USA),
        "tutti_i_provider_del_dizionario": gruppo(dizionario),
        "errori": len(err), "falsi_positivi_con_formula_negativa": len(fp_neg),
        "falsi_positivi_con_formula_negativa_cig": [r["cig"] for r in fp_neg],
        "nota": "campione stratificato v3, non casuale: precisione/richiamo valgono sul campione; VMware conta come estero (Broadcom, USA)",
    }
    oggi = datetime.date.today().isoformat()
    d = RADICE / f"esiti/{oggi}/lente-prodotto"; os.makedirs(d, exist_ok=True)
    json.dump(out, open(d / "lente-prodotto.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    with open(d / "errori.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(righe[0])); w.writeheader(); w.writerows(err)
    print(json.dumps({k: out[k] for k in ("n_campione", "riferimento_con_provider_del_dizionario", "predetti", "estero_extra_ue",
                                           "bigtech_usa", "errori", "falsi_positivi_con_formula_negativa")}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
