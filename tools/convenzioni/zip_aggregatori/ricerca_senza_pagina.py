"""Ricerca per altre vie delle 17 iniziative «pagina-non-trovata» del giro 7/11 (#62).

Ingresso: report/convenzioni/aggregatori/ricerca-2026-11-06-sha.json (sha256 dal manifest dell'archivio;
elenco dei documenti delle pagine di Azienda Zero letto dall'API pubblica jsonws del profilo del committente).
Uscita: report/convenzioni/aggregatori/aggregatori-ricerca-2026-11-06.csv (stesse colonne degli altri CSV aggregatori).
Script, copie e log del giro: server, lavoro/convenzioni/aggregatori/r1108/.
HERA (cig-A0260B3155) e PAT (cig-95643027B0) restano come nel CSV del 7/11: pagina individuata, dietro login.
"""
import csv
import json
from pathlib import Path

R = Path(__file__).resolve().parents[3]
A = R / "report/convenzioni/aggregatori"
D = "2026-11-06"
CAMPI = ["iniziativa", "piattaforma", "url_pagina", "documento", "tipo_documento", "url_documento", "sha256", "data", "esito", "dati_estratti", "note"]
AZ = "https://www.azero.veneto.it/web/guest/bandi-di-gara-fornitori"
DOC = "https://www.azero.veneto.it/documents/20126/"

NEG = "pagina-non-trovata"
WEB = "ricerca web per CIG e per titolo senza risultati pertinenti"
PVL = "PVL ANAC (lavoro/pvl/link_cig.csv): nessun avviso con link ai documenti"
ESITI = {  # iniziativa -> (piattaforma, url_pagina, esito, nota)
    "cig-949554539F": ("Azienda Zero (profilo del committente)", AZ + "#articleId=637636", "pagina-trovata",
                       "V: articolo 637636 «Procedura aperta telematica per l'affidamento del Servizio di Gestione Informatizzata del Personale…» (2^ ed.); "
                       "CIG 949554539F nel disciplinare, nella domanda, nel modello di offerta e nelle delibere 814/2022, 275/2023 e 641/2023 (aggiudicazione); "
                       "via: API pubblica jsonws del sito; dietro_login=no"),
    "cig-B736423C63": ("Azienda Zero (profilo del committente)", AZ + "#articleId=1230414", "pagina-trovata",
                       "V: il CIG è il «CIG Master» del contratto Azienda Zero – Consorzio Arsenàl.IT (DDG 407/2025, 33 mesi dal 1/4/2025 al 31/12/2027), "
                       "citato nel DDG 370/2026 dentro lo zip «Documentazione per Sintel» dell'articolo 1230414 (affidamento in house 1/7-31/12/2026); "
                       "R: la pagina è dell'affidamento successivo, l'atto originario DDG 407/2025 non è nel profilo del committente; dietro_login=no"),
    "cig-99617296D3": ("SUAM Regione Marche", "", NEG,
                       "le liste «bandi scaduti» ed «esiti» del PortaleAppalti SUAM chiedono una «Verifica Anti-Robot» (CAPTCHA, non superato; blocchi-accesso.csv); "
                       "R: il capitolato dell'appalto specifico ECM (bandi.regione.marche.it, archiviato) rimanda allo stesso «AQ-ICT in 9 lotti, art. 59 c. 4 lett. b)» senza CIG; "
                       + WEB + "; TED 0; dietro_login=ignoto"),
    "cig-9777818EA8": ("Provincia di Brescia (CUC Area Vasta)", "", NEG,
                       "Amministrazione trasparente della Provincia dietro verifica anti-robot «Cloud Web Accelerator» (non superata; blocchi-accesso.csv); "
                       "TED 240261-2023 e 661555-2023 già noti; " + WEB + "; dietro_login=ignoto"),
    "cig-945403654F": ("Portale acquisti ANAS (Jaggaer)", "", NEG,
                       "elenco pubblico «gare scadute» di acquisti.stradeanas.it (2.966 procedure) consultato da anonimo, filtro per descrizione non usabile in headless; "
                       "R: il comunicato ANAS del 21/10/2022 (archiviato) descrive la «gara 2 Piattaforma Digitale, Big Data & Advanced Analytics» del programma SHM, "
                       "scadenza 28/11/2022, senza CIG; " + WEB + "; TED 0; dietro_login=ignoto"),
    "cig-88556834CB": ("Masaf", "", NEG, WEB + "; TED 0; " + PVL + "; R: probabile procedura del programma nazionale raccolta dati alieutici; dietro_login=ignoto"),
    "cig-7991036B82": ("Trenitalia / FS", "", NEG, WEB + "; TED 0; " + PVL + "; R: affidamento infragruppo a FSTechnology; dietro_login=ignoto"),
    "cig-87332390D0": ("START (ESTAR)", "", NEG, "ricerca START per CIG senza esito (7/11); " + WEB + "; " + PVL + "; R: negoziata ex art. 63 senza bando; dietro_login=ignoto"),
    "cig-8716552642": ("START (ESTAR)", "", NEG, "ricerca START per CIG senza esito (7/11); " + WEB + "; " + PVL + "; R: negoziata ex art. 63 senza bando; dietro_login=ignoto"),
    "cig-B715929978": ("START (ESTAR)", "", NEG, "ricerca START per CIG senza esito (7/11); PVL: avviso A2_29 «RISULTATI» del 21/07/2025 senza link ai documenti; "
                       + WEB + "; dietro_login=ignoto"),
    "cig-9603457F68": ("START (ESTAR)", "", NEG, "ricerca START per CIG senza esito (7/11); " + WEB + "; " + PVL
                       + "; R: prosecuzione della gara 009511-2022 (cig-9216207E99); dietro_login=ignoto"),
    "cig-7812108376": ("START (ESTAR, piattaforma 2019)", "", NEG, "TED 98378-2019, 347586-2020, 530975-2023 già noti; start.e.toscana.it/estar non risponde; "
                       + WEB + "; dietro_login=ignoto"),
    "cig-759453695C": ("START (ESTAR, piattaforma 2018)", "", NEG, "TED 388213-2018 già noto; start.e.toscana.it/estar non risponde; " + WEB + "; dietro_login=ignoto"),
    "cig-7930885557": ("START (Regione Toscana, piattaforma 2019)", "", NEG,
                       "TED 268988-2019 ed esiti 2021 già noti; il decreto del Consiglio regionale n. 266/2022 (adesione al rinnovo START, archiviato) "
                       "non contiene il CIG nel testo; " + WEB + "; dietro_login=ignoto"),
    "cig-7246653F38": ("Sintel (ARIA, ex Lombardia Informatica)", "", NEG,
                       "ricerca ARIA per CIG senza esito (7/11); R: la gara 7/2017/LI (fleet management PdL, 3 lotti; lotto 2 RTI BCS-Esprinet-Fastweb) "
                       "è citata nelle delibere di adesione e proroga delle ATS (ATS Bergamo del. 643, archiviata, senza CIG nel testo estraibile); "
                       + WEB + "; dietro_login=ignoto"),
}
FUORI = {  # documenti trovati fuori piattaforma, collegati per oggetto (R)
    "cig-99617296D3": [("Capitolato tecnico appalto specifico ECM (rimanda all'AQ-ICT in 9 lotti)",
                        "https://bandi.regione.marche.it/Allegati/9999\\04%20AllegatoB_CapitolatoTecnicoECM.docx")],
    "cig-945403654F": [("Comunicato ANAS 21/10/2022 sulle gare SHM (gara 2 Piattaforma Digitale)", "https://www.stradeanas.it/en/print/pdf/node/226018")],
    "cig-7930885557": [("Decreto Consiglio regionale Toscana n. 266/2022 (adesione al rinnovo START)",
                        "https://trasparenza.consiglio.regione.toscana.it/sites/default/files/atti-2025-01/Decreto_n.266_del_19-04-2022%20-%20Testo%20atto.pdf")],
    "cig-7246653F38": [("ATS Bergamo del. 643, prosecuzione del contratto Fleet Management",
                        "https://ats-bg.it/system/files/field_blocco_redazionale/allegati/1344/paragrafi/15972/del%20643%20prosecuzione%20contratto%20Fleet%20Management%20nelle%20more%20di%20attivaizone%20ARIA.pdf")],
}
TIPI_AZ = (("bando", "bando"), ("disciplinare", "disciplinare"), ("fac-simile", "modulistica"), ("modello di offerta", "modulistica"),
           ("capitolato", "capitolato"), ("chiariment", "chiarimenti"), ("verbal", "verbale-seduta"), ("delibera n. 814", "determina"),
           ("deli0000641", "aggiudicazione"), ("documentazione per sintel", "documentazione-gara-zip"))


def tipo_az(t):
    tl = t.lower()
    return next((v for k, v in TIPI_AZ if k in tl), "altro")


def main():
    j = json.load(open(A / "ricerca-2026-11-06-sha.json", encoding="utf-8"))
    sha = j["sha"]
    righe = []
    for ini, (pf, up, es, nota) in ESITI.items():
        righe.append({"iniziativa": ini, "piattaforma": pf, "url_pagina": up, "documento": "(pagina)", "tipo_documento": "pagina",
                      "url_documento": "", "sha256": "", "data": D, "esito": es, "dati_estratti": "", "note": nota})
        visti = set()
        for u, t in j["azero"].get(ini, {}).get("docs", []):
            if u in visti:
                continue
            visti.add(u)
            h = sha.get(DOC + u, [""])[0]
            righe.append({"iniziativa": ini, "piattaforma": pf, "url_pagina": up, "documento": t, "tipo_documento": tipo_az(t),
                          "url_documento": DOC + u, "sha256": h, "data": D, "esito": "archiviato" if h else "pubblicato-non-archiviato",
                          "dati_estratti": "", "note": "V; archivia.py"})
        for t, u in FUORI.get(ini, []):
            h = sha.get(u, [""])[0]
            righe.append({"iniziativa": ini, "piattaforma": "fuori piattaforma", "url_pagina": "", "documento": t, "tipo_documento": "altro",
                          "url_documento": u, "sha256": h, "data": D, "esito": "archiviato" if h else "non-trovato", "dati_estratti": "",
                          "note": "R: collegato per oggetto, CIG non nel testo; archivia.py"})
    with open(A / "aggregatori-ricerca-2026-11-06.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPI)
        w.writeheader()
        w.writerows(righe)
    print(len(righe), "righe")


if __name__ == "__main__":
    main()
