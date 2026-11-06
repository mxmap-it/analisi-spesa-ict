"""Verifica «Imbuto: licenze e marchi, cloud sì o no» (#66, top-5 punto 5, rendiconto 0.6).

Perimetro: CIG dal 2024 di imbuto-0.3.1 in S3/S4 con sottoclasse diversa da cloud/in-house (licenze, software di
infrastruttura, servizi professionali, telefonia: 3.515 righe, 6,51 mld dichiarati), un CIG una volta sola, al netto dei
tetti e degli errori d'importo di imbuto_revisione.py (tetti-cig-v2.csv).

Asse A (è cloud?) e asse B (giurisdizione del prodotto), con la via di ogni decisione:
  L1-capitolato   Oracle da Licenze multibrand 6 (padre 9660108D4B): il capitolato prevede solo prodotti on premises,
                  consegna via edelivery (report/convenzioni/9660108D4B-multibrand6-oracle.md, V) -> non cloud, extra-UE
  L2-prodotto     marchio il cui prodotto ha una sola modalità di erogazione, documentata nel listino del produttore:
                  Salesforce (solo SaaS) -> cloud; VMware vSphere/VCF e Cloudera CDP Private Base (software installato
                  presso l'ente) -> non cloud, salvo «cloud» nell'oggetto
  L3-testo-saas   l'oggetto nomina un servizio erogato dal produttore (M365, O365, Azure, Dynamics 365, Intune, Copilot,
                  Teams; OCI, Oracle Cloud, Fusion; RISE, S/4HANA Cloud, SuccessFactors, Ariba, Concur, BTP;
                  Workspace, GCP; AWS) -> cloud
  L4-testo-onprem l'oggetto nomina solo prodotti installati presso l'ente (Windows Server, SQL Server, CAL, licenze
                  perpetue, Exchange/SharePoint Server, Oracle Database/WebLogic con supporto) -> non cloud
  L5-categoria    servizi professionali e telefonia: non sono servizi cloud (consulenza, connettività) -> non cloud
  I-misto         Microsoft EA o «licenze Microsoft/Oracle/SAP» senza dettaglio: resta incerto (il carrello sta nell'atto)
Giurisdizione del prodotto: sede del produttore (Microsoft, Oracle, VMware/Broadcom, Cloudera, Salesforce, Google,
AWS, ServiceNow, Cisco: USA -> extra-UE; SAP: DE -> UE; TIM, Fastweb, Retelit, Aruba, WIIT, PSN: IT).

Uso:
  python tools/verifiche/imbuto_licenze.py             # da un clone: legge esiti/2026-11-06/imbuto/licenze-cig.csv
  python tools/verifiche/imbuto_licenze.py --rigenera  # SUL SERVER: rilegge lavoro/imbuto/ict.csv (sola lettura)
"""
import csv, collections, json, os, re, sys

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.normpath(os.path.join(QUI, "..", ".."))
E = os.path.join(RADICE, "esiti/2026-11-06/imbuto")
OUT = os.path.join(E, "licenze-cig.csv")
ICT = os.path.join(RADICE, "lavoro/imbuto/ict.csv")
GIUR = {"Microsoft": "extra-UE", "Oracle": "extra-UE", "VMware": "extra-UE", "Cloudera": "extra-UE", "Salesforce": "extra-UE",
        "Google": "extra-UE", "Amazon Web Services": "extra-UE", "ServiceNow": "extra-UE", "Cisco Webex": "extra-UE",
        "SAP": "UE", "TIM": "IT", "Fastweb": "IT", "Retelit": "IT", "Aruba": "IT", "WIIT": "IT", "Polo Strategico Nazi": "IT",
        "Nextcloud": "UE", "SPC Cloud lotto 1": "IT"}
RX_SAAS = re.compile(r"\b(m365|microsoft\s*365|office\s*365|o365|azure|dynamics\s*365|intune|copilot|teams|exchange\s+online|"
                     r"sharepoint\s+online|oci\b|oracle\s+cloud|fusion|rise\s+with\s+sap|s/?4\s*hana\s+cloud|successfactors|ariba|concur|"
                     r"\bbtp\b|google\s+workspace|gsuite|g\s*suite|google\s+cloud|gcp\b|aws\b|amazon\s+web\s+services|saas|cloud|servizi\s+online|online\s+services)\b", re.I)
RX_ONPREM = re.compile(r"windows\s+server|sql\s+server|\bcal\b|perpetu|exchange\s+server|sharepoint\s+server|system\s+center|"
                       r"oracle\s+database|weblogic|database\s+enterprise|vsphere|vcenter|on[\s-]?prem", re.I)
RX_GENERICO = re.compile(r"enterprise\s+agreement|\bea\s*\d|licenz|rinnov|manutenz|support|assistenz|sottoscrizion|subscription", re.I)


def decidi(r):
    p, t, sc, aq = r["provider"], r["testo"], r["sottoclasse"], r.get("aq", "")
    if sc in ("servizi-professionali", "telefonia"): return "non-cloud", "L5-categoria"
    if p == "Oracle" and re.search(r"multibrand", t, re.I): return "non-cloud", "L1-capitolato"
    if p == "Salesforce": return "cloud", "L2-prodotto"
    if p in ("VMware", "Cloudera") and not re.search(r"\bcloud\b", t, re.I): return "non-cloud", "L2-prodotto"
    s, o = bool(RX_SAAS.search(t)), bool(RX_ONPREM.search(t))
    if s and not o: return "cloud", "L3-testo-saas"
    if o and not s: return "non-cloud", "L4-testo-onprem"
    if s and o: return "misto", "I-misto-esplicito"
    return "incerto", "I-misto"


def rigenera():
    T = {r["cig"]: r for r in csv.DictReader(open(os.path.join(E, "tetti-cig-v2.csv"), encoding="utf-8"))}
    visti = set(); righe = []
    for r in csv.DictReader(open(ICT, encoding="utf-8")):
        if int(r["anno"]) < 2024 or r["cig"] in visti: continue
        if r["strato"] not in ("S3-convenzione-lotto", "S4-marchio") or r["sottoclasse"] in ("cloud", "in-house"): continue
        visti.add(r["cig"]); imp = float(r["importo"] or 0)
        t = T.get(r["cig"]); netti = float(t["euro_netti"]) if t else imp
        nota = t["classe"] + "/" + t["via"] if t else ""
        if t and t["classe"] == "incerto": netti = imp
        x = {"cig": r["cig"], "anno": r["anno"], "strato": r["strato"], "sottoclasse": r["sottoclasse"], "provider": r["provider"],
             "importo": imp, "euro_netti": netti, "nota_tetti": nota, "testo": r["testo"][:300], "aq": ""}
        righe.append(x)
    # padre AQ per gli Oracle (via L1): dal riepilogo dei derivati di Multibrand 6 nel censimento delle convenzioni
    der = os.path.join(RADICE, "lavoro/convenzioni/attuativi.csv")
    padri = {}
    if os.path.exists(der):
        for r in csv.DictReader(open(der, encoding="utf-8")):
            if r.get("cig") and r.get("cig_accordo_quadro"): padri[r["cig"]] = r["cig_accordo_quadro"]
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["cig", "anno", "strato", "sottoclasse", "provider", "importo", "euro_netti", "nota_tetti",
                                        "asse_a", "via", "giurisdizione_prodotto", "testo"])
        for x in righe:
            x["aq"] = padri.get(x["cig"], "")
            a, v = decidi(x)
            w.writerow([x["cig"], x["anno"], x["strato"], x["sottoclasse"], x["provider"], round(x["importo"], 2), round(x["euro_netti"], 2),
                        x["nota_tetti"], a, v, GIUR.get(x["provider"], "non determinata"), x["testo"]])
    print("scritto", OUT, len(righe), "CIG; padri noti", len(padri))


def main():
    if "--rigenera" in sys.argv: return rigenera()
    R = list(csv.DictReader(open(OUT, encoding="utf-8")))
    agg = lambda f: _agg(R, f)
    T = {"cig": len(R), "euro_dichiarati": round(sum(float(r["importo"]) for r in R)), "euro_netti": round(sum(float(r["euro_netti"]) for r in R)),
         "per_asse_a": agg(lambda r: r["asse_a"]), "per_via": agg(lambda r: (r["asse_a"], r["via"])),
         "per_provider_asse_a": agg(lambda r: (r["provider"] or "?", r["asse_a"])),
         "cloud_per_giurisdizione": agg(lambda r: r["giurisdizione_prodotto"] if r["asse_a"] == "cloud" else None)}
    print(json.dumps(T, ensure_ascii=False, indent=1))
    if "--json" in sys.argv: json.dump(T, open(sys.argv[sys.argv.index("--json") + 1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def _agg(R, f):
    a = collections.defaultdict(lambda: [0, 0.0])
    for r in R:
        k = f(r)
        if k is None: continue
        k = " / ".join(k) if isinstance(k, tuple) else k
        a[k][0] += 1; a[k][1] += float(r["euro_netti"])
    return [{"chiave": k, "cig": v[0], "euro_netti": round(v[1])} for k, v in sorted(a.items(), key=lambda x: -x[1][1])]


if __name__ == "__main__":
    main()
