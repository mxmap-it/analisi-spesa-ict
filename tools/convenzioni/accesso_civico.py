"""#62: bozze di istanze di accesso civico generalizzato (art. 5 c. 2 d.lgs. 33/2013) per le carenze di trasparenza.

Una bozza per ogni coppia (iniziativa principale, carenza che la colpisce). NESSUN INVIO: le istanze le invia Fabio.
Ingressi: report/convenzioni/database/iniziative.json, carenze.yaml. Analisi dei dinieghi: report/convenzioni/accesso-civico/analisi-dinieghi.md.
Uscite in report/convenzioni/accesso-civico/:
  bozze/<id>.json   formato riusabile dal futuro sistema di invii massivi (spesaict.istanza/1)
  bozze/<id>.md     testo leggibile
  registro.csv      stato di ogni istanza: preparata / inviata / risposta / esito. Le righe già oltre «preparata» non si toccano.
Iniziative principali: attive; prime 15 Consip per valore, PSN, PRINCO (consip-2928), prime 5 degli aggregatori regionali.
Uso: python tools/convenzioni/accesso_civico.py"""
import csv
import json
from pathlib import Path

import yaml

R = Path(__file__).resolve().parent.parent.parent
DB = R / "report/convenzioni/database"
OUT = R / "report/convenzioni/accesso-civico"
DATA = "2026-11-05"
CAMPI_REG = ["id", "iniziativa", "carenza", "destinatario", "stato", "preparata", "inviata", "protocollo", "risposta", "esito", "note"]

RICHIESTA = {
    "C1": ("copia delle sezioni dell'offerta tecnica dell'aggiudicatario di ciascun lotto che indicano prodotti, marchi e produttori offerti, "
           "region e data center di erogazione e subappaltatori", "l'elenco dei prodotti e dei marchi offerti per ciascun lotto"),
    "C2": ("copia del listino prezzi (o dell'allegato economico) applicato alle amministrazioni aderenti, per ciascun lotto e listino",
           "l'elenco dei codici e delle descrizioni dei prodotti a listino"),
    "C3": ("copia dell'estrazione o del report di monitoraggio già esistente del transato (o del valore degli ordinativi) per lotto e, "
           "dove disponibile, per listino o marchio, per anno dal 1/1/2024", "il totale del transato per lotto"),
    "C4": ("copia dell'estrazione già esistente degli ordinativi dal 1/1/2024, con amministrazione, data, lotto, importo e CIG derivato",
           "numero e importo degli ordinativi per lotto e per amministrazione"),
    "C5": ("copia della sola tabella «Riepilogo prezzi» dei Progetti dei Piani dei Fabbisogni approvati, con i totali per famiglia di servizio",
           "l'importo per famiglia di servizio di ciascun contratto"),
    "C6": ("l'indicazione, per ciascun lotto, del paese e della region o città dei data center dichiarati dall'aggiudicatario",
           "il paese del trattamento dei dati per ciascun lotto"),
    "C7": ("il valore del massimale eroso per ciascun lotto alla data della risposta, come risulta dai sistemi di monitoraggio esistenti",
           "la percentuale di erosione per lotto"),
    "C8": ("l'elenco dei lotti dell'iniziativa con il CIG di ciascun lotto", None),
}
ESCLUSIONI = {
    "C1": "Non chiedo l'offerta integrale. Accetto l'oscuramento delle parti che l'offerente ha motivatamente dichiarato coperte da segreto tecnico o commerciale.",
    "C6": "Non chiedo indirizzi, schemi di rete, configurazioni né misure di sicurezza.",
    "C5": "Non chiedo architetture, configurazioni, inventari, indirizzi, piani di sicurezza né il dettaglio voce per voce.",
}


def destinatario(v):
    if v["tipo_soggetto"] == "consip":
        return "Consip S.p.A., Responsabile della prevenzione della corruzione e della trasparenza (indirizzo PEC da ricavare dalla sezione Società trasparente)"
    if v["tipo_soggetto"] == "psn":
        return "Presidenza del Consiglio dei ministri, Dipartimento per la trasformazione digitale (concedente del PSN), ufficio per l'accesso civico"
    return f"{v['stazione_appaltante']}, ufficio per l'accesso civico o RPCT (indirizzo da ricavare dalla sezione Amministrazione trasparente)"


# Istanze davvero necessarie (giro del 5/11, dopo pagina del bando, open data Consip, AT di Consip, campione di enti e ricerca web):
# solo carenze «verificate» e solo dove il dato serve all'imbuto (prodotto, marchio, giurisdizione). Il resto si ritira.
NECESSARIE = {
    "C1": {"consip-2746", "consip-2928", "consip-2213", "consip-1403", "consip-2599", "consip-2738"},  # prodotti/CSP offerti: cloud e multibrand
    "C3": {"consip-2746", "consip-2928", "consip-2213", "consip-2599", "consip-2738"},  # transato per marchio: solo iniziative multi-marchio
    "C4": {"consip-2483", "consip-2610", "consip-2615", "consip-2755", "consip-2746", "consip-2928"},  # elenco ordinativi per ente: le più grandi e le cloud
    "C6": {"consip-2746", "consip-2928"},  # dichiarazione region/data center: esiste, accertato negli atti
    "C7": {"consip-2928"},  # erosione per Brand: soglia accertata nel Capitolato
}
MOTIVO_RITIRO = ("ritirata il 5/11: carenza non confermata su tutte le fonti online, oppure dato non necessario all'imbuto per questa "
                 "iniziativa (es. marchio unico, servizi professionali), oppure già reperibile altrove")


def principali(voci):
    att = [v for v in voci if v["stato_iniziativa"] == "attiva"]
    scelte = [v for v in att if v["tipo_soggetto"] == "consip"][:15]
    scelte += [v for v in att if (v["id"] in ("psn", "consip-2928") or any(v["id"] in x for x in NECESSARIE.values())) and v not in scelte]
    scelte += [v for v in att if v["tipo_soggetto"] == "aggregatore-regionale"][:5]
    return scelte


def main():
    voci = json.loads((DB / "iniziative.json").read_text(encoding="utf-8"))
    car = {c["id"]: c for c in yaml.safe_load(open(DB / "carenze.yaml", encoding="utf-8"))["carenze"]}
    (OUT / "bozze").mkdir(parents=True, exist_ok=True)
    reg_path = OUT / "registro.csv"
    reg = {}
    if reg_path.exists():
        reg = {r["id"]: r for r in csv.DictReader(open(reg_path, encoding="utf-8"))}
    n = 0
    for v in principali(voci):
        cig = ", ".join(x["cig_padre"] for x in v["lotti"][:12]) + (" e altri" if len(v["lotti"]) > 12 else "")
        for k in v["carenze"]:
            if k["id"] not in RICHIESTA or k["stato"] != "verificato" or v["id"] not in NECESSARIE.get(k["id"], set()):
                continue
            iid = f"{v['id']}-{k['id']}".lower()
            if iid in reg and reg[iid]["stato"] != "preparata":
                continue  # già inviata: la bozza resta com'era
            c = car[k["id"]]
            ric, sub = RICHIESTA[k["id"]]
            oggetto = f"Istanza di accesso civico generalizzato: {c['titolo'].lower()}, iniziativa «{v['nome'][:120]}»"
            testo = (f"Ai sensi dell'art. 5, comma 2, del d.lgs. 33/2013 chiedo, per l'iniziativa «{v['nome']}» (CIG dei lotti: {cig}), {ric}."
                     + (f" In subordine chiedo {sub}." if sub else "")
                     + (f" {ESCLUSIONI[k['id']]}" if k["id"] in ESCLUSIONI else "")
                     + " Chiedo i documenti nel formato in cui sono già detenuti, preferibilmente elettronico e aperto, senza alcuna elaborazione."
                     + " In caso di limiti ex art. 5-bis chiedo l'accesso parziale con oscuramento delle sole parti sottratte.")
            motivazione = (f"Facoltativa. {c['perche_serve']} I dati non risultano pubblicati sulle pagine ufficiali dell'iniziativa consultate "
                           f"({k['stato']}{': ' + k['nota'] if k.get('nota') else ''}).")
            ist = {"formato": "spesaict.istanza/1", "id": iid, "tipo": "accesso-civico-generalizzato", "base": "art. 5 c. 2 d.lgs. 33/2013",
                   "iniziativa": v["id"], "carenza": k["id"], "stato_carenza": k["stato"], "destinatario": destinatario(v),
                   "oggetto": oggetto, "testo": testo, "motivazione_facoltativa": motivazione,
                   "riferimenti": [f"https://analisi-spesa-ict.mxmap.it/convenzioni/{v['id'].lower()}/",
                                   "report/convenzioni/accesso-civico/analisi-dinieghi.md", f"raccomandazione {k['raccomandazione']}"],
                   "preparata": DATA, "inviata": None, "approvazione": "da approvare (Fabio)"}
            (OUT / "bozze" / f"{iid}.json").write_text(json.dumps(ist, ensure_ascii=False, indent=1), encoding="utf-8")
            (OUT / "bozze" / f"{iid}.md").write_text(
                f"# {oggetto}\n\n**Bozza non inviata** ({DATA}). Destinatario: {ist['destinatario']}.\n\n"
                + ("" if k["stato"] == "verificato" else "**Prima dell'invio:** l'assenza del dato è ancora da verificare sulle pagine ufficiali (regola dell'ultima risorsa).\n\n")
                + f"{testo}\n\n"
                f"*Motivazione:* {motivazione}\n\nRiferimenti: {'; '.join(ist['riferimenti'])}.\n", encoding="utf-8")
            reg[iid] = {**{f: "" for f in CAMPI_REG}, **reg.get(iid, {}), "id": iid, "iniziativa": v["id"], "carenza": k["id"],
                        "destinatario": ist["destinatario"].split(",")[0], "stato": "preparata", "preparata": DATA,
                        "note": "" if k["stato"] == "verificato" else "assenza da verificare prima dell'invio"}
            n += 1
    attive = set()
    for v in principali(voci):
        for k in v["carenze"]:
            if k["id"] in RICHIESTA and k["stato"] == "verificato" and v["id"] in NECESSARIE.get(k["id"], set()):
                attive.add(f"{v['id']}-{k['id']}".lower())
    per_id = {v["id"]: v for v in voci}
    for iid, r in reg.items():
        if r["stato"] == "preparata" and iid not in attive:
            v = per_id.get(r["iniziativa"], {})
            k = next((x for x in v.get("carenze", []) if x["id"] == r["carenza"]), None)
            if k is None:
                motivo = "la carenza non risulta più per questa iniziativa"
            elif k["stato"] != "verificato":
                motivo = "carenza non confermata su tutte le fonti online (resta da verificare)"
            else:
                motivo = "dato non necessario all'imbuto per questa iniziativa (es. marchio unico o servizi professionali)"
            r["stato"], r["note"] = "ritirata", "ritirata il 5/11: " + motivo
    with open(reg_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPI_REG)
        w.writeheader()
        for k in sorted(reg):
            w.writerow(reg[k])
    print(n, "bozze preparate;", len(reg), "righe nel registro")


if __name__ == "__main__":
    main()
