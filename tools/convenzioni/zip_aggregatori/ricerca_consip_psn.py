"""Pagine ufficiali delle 7 iniziative Consip/PSN «pagina non individuata» (#62, giro 6/11 sera).

La prima ricerca (consip_pagine.py, 5/11) cercava per CIG padre e trovava pagine sbagliate; qui la ricerca pubblica
consip.it/imprese/bandi per ID Sigef o per titolo ha dato la pagina giusta, verificata dal CIG o dall'ID nell'HTML.
PSN: sezione Amministrazione trasparente della Presidenza del Consiglio (bando e allegati della gara di Difesa Servizi).
Ingresso: report/convenzioni/aggregatori/ricerca-consip-2026-11-06.json (pagine, sha256 dell'HTML, documenti linkati,
sha256 dal manifest dell'archivio). Uscita: report/convenzioni/aggregatori/aggregatori-ricerca-consip-2026-11-06.csv.
Script, HTML e log del giro: server, lavoro/convenzioni/aggregatori/r1109/.
"""
import csv
import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(R / "tools/convenzioni"))
from consip_pagine import tipo  # noqa: E402

A = R / "report/convenzioni/aggregatori"
D = "2026-11-06"
CAMPI = ["iniziativa", "piattaforma", "url_pagina", "documento", "tipo_documento", "url_documento", "sha256", "data", "esito", "dati_estratti", "note"]
PROVA = {  # iniziativa -> prova che la pagina è quella giusta
    "consip-2556": "V: CIG padre 9774270EC1 nell'HTML; Servizi PEC-REM 2",
    "consip-2453": "V: «ID 2453» e CIG padre 942570737B nell'HTML",
    "cig-8898059E90": "V: CIG 8898059E90 e 8898075BC5 nell'HTML; AQ Sicurezza on premises, ID 2367",
    "cig-B0DA5C472C": "V: CIG B0DA5C472C e B0DA5C8A78 nell'HTML; Tecnologie Server ed. 5, ID 2714",
    "cig-5133642F61": "V: CIG 5133642F61 nell'HTML; SPC Connettività (SPC2)",
    "cig-91881762B3": "V: CIG 91881762B3, 9188224A4D, 9188267DC8 nell'HTML; Sanità digitale - sistemi informativi gestionali, ID 2366",
    "psn": "V: CIG 9066973ECE nella pagina AT della Presidenza del Consiglio (bando, disciplinare e allegati della gara PSN)",
}


def main():
    j = json.load(open(A / "ricerca-consip-2026-11-06.json", encoding="utf-8"))
    righe = []
    for ini, p in j["pagine"].items():
        pf = "Presidenza del Consiglio (Amministrazione trasparente)" if ini == "psn" else "consip.it"
        righe.append({"iniziativa": ini, "piattaforma": pf, "url_pagina": p["pagina"], "documento": "(pagina)", "tipo_documento": "pagina",
                      "url_documento": "", "sha256": p["sha256_html"], "data": D, "esito": "pagina-trovata", "dati_estratti": "",
                      "note": PROVA[ini] + "; via: ricerca pubblica del sito, da anonimo; dietro_login=no"})
        for u, nome in p["docs"]:
            h = j["sha"].get(u, "")
            righe.append({"iniziativa": ini, "piattaforma": pf, "url_pagina": p["pagina"], "documento": nome, "tipo_documento": tipo(nome),
                          "url_documento": u, "sha256": h, "data": D, "esito": "archiviato" if h else "pubblicato-non-archiviato",
                          "dati_estratti": "", "note": "V; archivia.py"})
    with open(A / "aggregatori-ricerca-consip-2026-11-06.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPI)
        w.writeheader()
        w.writerows(righe)
    print(len(righe), "righe")


if __name__ == "__main__":
    main()
