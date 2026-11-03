"""Imbuto (report/metodo/imbuto.md): assegna ogni CIG ANAC dal 2020 a uno strato S0-S6 e conta contratti ed euro
per anno, strato, gruppo e giurisdizione. Le regole di attribuzione sono quelle di classifica.py; qui si aggiungono
l'esclusione certa (S1), la soglia d'importo (S2), la sottoclasse ICT non cloud (S5) e i gruppi del residuo (S6).

Memoria: nessun caricamento di tutti i CIG (incidente del 27/10). I file annuali si leggono in streaming e si
aggregano subito; i CIG presenti negli aggiornamenti mensili (delta) si saltano nei file annuali e si contano una
volta sola, con l'ultima versione.

Uso: python tools/analisi/imbuto.py [anno_iniziale]   (default 2020)
  -> lavoro/imbuto/riepilogo.json, lavoro/imbuto/ict.csv (tutti i CIG non esclusi in S1/S2, per gli strati successivi)"""
import csv, json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from classifica import Classificatore, CPV_ICT, VERSIONE  # noqa: E402
from attribuisci_provider import righe_cig, aggiudicatari, D, RX_AQ  # noqa: E402
import glob
import yaml

# S3 da base di conoscenza: categoria dell'iniziativa padre -> (strato, sottoclasse, gruppo)
INIZIATIVE = {i["cig"]: i for i in yaml.safe_load(open(os.path.join(os.path.dirname(__file__), "../../config/iniziative_ict.yaml"), encoding="utf-8"))}
DA_CATEGORIA = {
    "cloud-provider": ("S3-convenzione-lotto", "cloud", ""), "licenza-prodotto": ("S3-convenzione-lotto", "licenza", ""),
    "cloud-multi": ("S6-residuo", "cloud-multi-provider-iniziativa", "G2-informazione-mancante"),
    "psn": ("S6-residuo", "psn-servizio-da-determinare", "G2-informazione-mancante"),
    "da-decifrare": ("S6-residuo", "iniziativa-da-decifrare", "G2-informazione-mancante"),
    "licenze-multi": ("S6-residuo", "licenze-multibrand", "G3-incerti-significativi"),
    "servizi-applicativi": ("S5-ict-non-cloud", "consulenza-it-applicativa", ""), "pmo-demand": ("S5-ict-non-cloud", "consulenza-it-altra", ""),
    "system-management": ("S5-ict-non-cloud", "consulenza-infrastruttura-in-house", ""), "sicurezza": ("S5-ict-non-cloud", "sicurezza-ict", ""),
    "connettivita": ("S5-ict-non-cloud", "telefonia-connettivita", ""), "hardware": ("S5-ict-non-cloud", "hardware-infrastruttura", ""),
}

VERSIONE_IMBUTO = "imbuto-0.3 (2026-11-03)"  # 0.3: base di conoscenza delle iniziative (config/iniziative_ict.yaml) in S3, S5, S6
SOGLIA_MIN = 500          # S2, Fabio 2/11
SOGLIA_MEGA = 5e6         # G1: a mano
SOGLIA_G3 = 40e3          # G3 incerti significativi / G4 coda
SOGLIA_DA_VERIFICARE = 50e6  # importo probabilmente massimale, non spesa

# segnali ICT nel testo: se presenti con CPV non ICT il contratto NON è escluso con certezza
# 0.2: tolti "telematic" (procedura telematica), "applicativ" (contratto applicativo), "digitalizzazion", "piattaform",
# "portale", "sap", "pc", "migrazion" da soli: nel giro 0.1 portavano 40 miliardi di lavori e sanità nel residuo
RX_ICT = re.compile(r"\b(software|informatic\w*|licenz\w+\s+(d'uso|software|microsoft|oracle)|cloud|hosting|housing|server|"
                    r"storage|data\s*cent\w*|sistem\w+\s+informativ\w*|servizi\s+applicativ\w*|software\s+applicativ\w*|"
                    r"hardware|personal\s+computer|notebook|stampant\w*|rete\s+(dati|lan|wan)|firewall|"
                    r"cyber\w*|sicurezza\s+informatic\w*|backup|disaster\s+recovery|migrazion\w+\s+(al\s+cloud|dei\s+dati|dei\s+sistemi)|"
                    r"saas|iaas|paas|sito\s+(web|internet)|database|posta\s+elettronic\w*|microsoft|oracle|vmware)\b", re.I)
# sottoclassi di S5 (ICT non cloud)
RX_HW = re.compile(r"hardware|personal\s+computer|\bpc\b|notebook|stampant|monitor|server|storage|apparat|switch|router|tablet|scanner|fotocopiat", re.I)
RX_TEL = re.compile(r"telefon|fonia|mobile|sim\b|connettivit|fibra|banda\s+larga|centralin", re.I)
RX_CONS = re.compile(r"consulenz|supporto\s+(tecnic|specialist)|assistenza\s+(tecnic|specialist|sistemistic)|servizi\s+professional|"
                     r"progettazion|system\s+integrat|sistemistic|presidio|gestione\s+(dei\s+)?sistem", re.I)
RX_CONS_INFRA = re.compile(r"infrastruttur|data\s*cent|server|rete|sistemistic|virtualizz|storage|ced\b|sala\s+macchine|networking|sicurezza", re.I)
RX_CONS_MIGR = re.compile(r"migrazion|cloud", re.I)
RX_PSN = re.compile(r"\bpsn\b|polo\s+strategico", re.I)


def sottoclasse_s5(testo):
    if RX_CONS.search(testo):
        if RX_CONS_MIGR.search(testo): return "consulenza-migrazione-cloud"
        if RX_CONS_INFRA.search(testo): return "consulenza-infrastruttura-in-house"
        return "consulenza-it-altra"
    if RX_TEL.search(testo): return "telefonia-connettivita"
    if RX_HW.search(testo): return "hardware-infrastruttura"
    return "ict-altro"


def strato(r, e, imp, padre, testo, cpv):
    """Restituisce (strato, sottoclasse, gruppo)."""
    if padre: return "S0-padre-aq", "", ""
    if imp < SOGLIA_MIN: return "S2-sotto-soglia", "ict" if (e or RX_ICT.search(testo)) else "non-ict", ""
    ini = INIZIATIVE.get(r["cig_accordo_quadro"])
    if ini and not (e and e["via"].startswith("1")): return DA_CATEGORIA[ini["categoria"]]
    if e is None:
        if RX_ICT.search(testo): return "S6-residuo", "cpv-non-ict-testo-ict", gruppo(imp, testo)
        return "S1-escluso-non-ict", "", ""
    v = e["via"]
    if RX_PSN.search(testo) or e["provider"].upper().startswith("PSN"):
        return "S6-residuo", "psn-servizio-da-determinare", "G2-informazione-mancante"
    if v.startswith(("1", "2")): return "S3-convenzione-lotto", e["servizio"], ""
    if v.startswith(("3", "5")): return "S4-marchio", e["servizio"], ""
    if v.startswith("0"): return "S5-ict-non-cloud", sottoclasse_s5(testo), ""
    return "S6-residuo", "cloud-provider-indeterminato", gruppo(imp, testo)


def gruppo(imp, testo):
    if imp >= SOGLIA_MEGA: return "G1-mega"
    if imp >= SOGLIA_G3: return "G3-incerti-significativi"
    return "G4-coda"


def main(anno0=2020):
    os.makedirs("lavoro/imbuto", exist_ok=True)
    anni = {str(a) for a in range(anno0, 2027)}
    c = Classificatore()
    agg = aggiudicatari()
    delta_cig = {r["cig"] for r in righe_cig("delta")}
    padri = set()
    for a in [p[-4:] for p in glob.glob(D + "cig-20*")] + ["delta"]:
        padri |= {r["cig_accordo_quadro"] for r in righe_cig(a) if r["cig_accordo_quadro"]}
    n = collections.Counter(); eur = collections.Counter()
    out = open("lavoro/imbuto/ict.csv", "w", newline="", encoding="utf-8")
    w = csv.writer(out)
    w.writerow(["anno", "cig", "strato", "sottoclasse", "gruppo", "via", "provider", "giurisdizione", "servizio", "cod_cpv",
                "cpv_ict", "importo", "importo_da_verificare", "stazione_appaltante", "aggiudicatari", "testo"])
    fonti = sorted(a for a in anni if glob.glob(D + f"cig-{a}/filesystem/cig_csv_*.zip")) + ["delta"]
    for fonte in fonti:
        for r in righe_cig(fonte):
            if fonte != "delta" and r["cig"] in delta_cig: continue
            anno = (r.get("anno_pubblicazione") or "").strip()
            if anno not in anni: continue
            testo = (r["oggetto_lotto"] or "") + " | " + (r["oggetto_gara"] or "")
            aq, cpv = r["cig_accordo_quadro"], r["cod_cpv"] or ""
            try: imp = float(r["importo_lotto"] or 0)
            except ValueError: imp = 0.0
            nomi = sorted(agg.get(r["cig"], set()))
            e = c.classifica(testo, aq, nomi, cpv)
            padre = r["cig"] in padri or (not aq and bool(RX_AQ.search(testo)) and r.get("tipo_scelta_contraente", "").upper().startswith("PROCEDURA"))
            s, sc, g = strato(r, e, imp, padre, testo, cpv)
            ini = INIZIATIVE.get(aq) if s.startswith("S3") else None
            giur = (ini or {}).get("giurisdizione", "") or (e or {}).get("giurisdizione", "") \
                or ("non-determinabile" if sc == "psn-servizio-da-determinare" else "")
            dv = int(imp >= SOGLIA_DA_VERIFICARE)
            k = (anno, s, sc, g, giur, dv)
            n[k] += 1
            if s != "S0-padre-aq": eur[k] += imp
            if s not in ("S1-escluso-non-ict",) and not (s == "S2-sotto-soglia" and sc == "non-ict"):
                w.writerow([anno, r["cig"], s, sc, g, (e or {}).get("via", ""), (e or {}).get("provider", ""), giur, (e or {}).get("servizio", ""),
                            cpv, int(bool(CPV_ICT.match(cpv))), imp, dv, r["denominazione_amministrazione_appaltante"], " ; ".join(nomi), testo[:400]])
    out.close()
    righe = [{"anno": a, "strato": s, "sottoclasse": sc, "gruppo": g, "giurisdizione": gi, "importo_da_verificare": dv,
              "cig": n[k], "euro": round(eur[k])} for k in sorted(n) for (a, s, sc, g, gi, dv) in [k]]
    json.dump({"versione": VERSIONE_IMBUTO, "regole": VERSIONE, "soglie": {"min": SOGLIA_MIN, "mega": SOGLIA_MEGA, "g3": SOGLIA_G3,
               "da_verificare": SOGLIA_DA_VERIFICARE}, "fonti": fonti, "righe": righe},
              open("lavoro/imbuto/riepilogo.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(len(righe), "righe di riepilogo")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2020)
