# Aggregatori regionali: convenzioni e AQ ICT (ticket #62)

Data della ricognizione: 5-6 novembre 2026. Elenco completo dei documenti: `aggregatori-2026-11-06.csv`. Blocchi di accesso: righe con data 2026-11-05/06 in `../blocchi-accesso.csv`.

Legenda: **V** = visto (letto da noi sulla pagina o nel documento); **R** = dedotto da noi, non scritto dalla fonte.

## Metodo

- Abbiamo consultato solo le parti pubbliche delle piattaforme: niente login, niente registrazione, niente CAPTCHA. Lo user-agent era dichiarato e fra due richieste allo stesso host passavano almeno 3 s.
- **Intercent-ER**: il sito è un Plone/Volto. L'elenco dei file viene dall'API JSON pubblica `++api++/<pagina>/@search`. I documenti di gara sono i link `DisplayAttach.ASP` di SATER che compaiono nella pagina del bando. File archiviati con `tools/archivia.py`.
- **EmPULIA**: è raggiungibile solo in `http://` (la 443 va in timeout, sia dal PC sia dal server). Pagine trovate con la ricerca SharePoint del sito (`_layouts/OSSSearchResults.aspx`). File archiviati con `tools/archivia.py`.
- **Sintel (ARIA)**: la procedura si trova con la ricerca pubblica `arcaSearch.xhtml` (codice gara), aperta con Chrome headless sul server. Gli allegati sono link JSF che scaricano in POST e non hanno un URL GET stabile. Li abbiamo scaricati senza login con il browser del server (`lavoro/convenzioni/aggregatori/sintel_ARIA_2023_807/`, sha256 nel CSV). Non sono in `archivio/`.
- **START (ESTAR)**: è una SPA Angular. La pagina della procedura l'abbiamo letta con Chrome headless e gli allegati li abbiamo scaricati con un click. Gli URL `documents-api/documents/?access-code=…` valgono una volta sola: un secondo GET risponde 404. Per questo i file stanno solo sul server (`lavoro/convenzioni/aggregatori/start_*`, sha256 nel CSV).
- Abbiamo archiviato anche le pagine HTML (bando, convenzione, schede), con `archivia()` e `accetta_html=True`, perché la CLI rifiuta l'HTML ("probabile blocco WAF").

## Esiti per iniziativa (sintesi)

| Iniziativa | Piattaforma | Trovato |
|---|---|---|
| cig-A008DB40BA | Intercent-ER | V convenzione "Sviluppo sistemi informativi 2": attiva dal 28/05/2024, scade il 28/05/2027, RTI Almaviva. Allegati (convenzione, listino, capitolato, CIG) e documenti di gara SATER (bando, disciplinare, capitolato, schema di convenzione, aggiudicazione) |
| cig-97219284C8 | Intercent-ER | V convenzione ITSM 2 + Sicurezza informatica 2: rinnovo di 24 mesi fino al 17/11/2028 e al 05/02/2029; det. 848/2026 "Lotto 1 – Estensione del quinto" |
| cig-9845010742 | Intercent-ER | V PC Desktop e Notebook 11, Team Memores: rinnovi; det. 511/2025 "Lotto 2 – Estensione del quinto" |
| cig-993049146A | EmPULIA | V pagina "Telemedicina": AS SDAPA in 3 lotti con importi, CIG e RTI; convenzioni firmate, capitolato, listini "Prodotti corrispettivi SLA" (7 revisioni) |
| cig-8637686BF8 | EmPULIA | V pagina AQ RUPAR-SPC: 30 M€, estendibili a 33 M€; 48 mesi dal 16/03/2022; 5 operatori; AQ firmato e zip della documentazione |
| cig-989984280E | Sintel | V ARIA_2023_807 è l'**AQ Infrastruttura Regionale di Telemedicina**, non un AQ ICT generico. 16 allegati pubblici, fra cui chiarimenti e comunicazione di aggiudicazione (det. 446 dell'08/05/2024) |
| cig-81636687F2 | START | V ESTAR, Area Vasta Sud Est, 11,3 M€: 10 documenti scaricati (bando, disciplinare, capitolati, bozza di convenzione) |
| cig-84163618CE | START | V ESTAR, Area Vasta Centro, 20 M€: 9 documenti elencati ma **non più scaricabili** (disponibili solo fino alla scadenza delle offerte, 17/10/2020) |

## Dati di consumo/erosione

- **Nessuna** delle quattro piattaforme pubblica l'erosione delle iniziative esaminate.
- Sintel/NECA (V): la scheda pubblica di una convenzione mostra MASSIMALE ed ESTENSIONE. Per il RESIDUO la nota dice che è "consultabile accedendo a NECA con le proprie credenziali", quindi sta dietro login.
- Intercent-ER (V): gli open data su dati.emilia-romagna.it contengono solo i listini degli ordinativi SATER, senza le quantità ordinate. R: le determine di "estensione del quinto" (ITSM 2 lotto 1, PC 11 lotto 2) indicano un massimale vicino all'esaurimento.
- START (V): la scheda di aggiudicazione è dietro login.

## Limiti

- In `archivio/manifest.jsonl` restano alcune righe con URL che finiscono in `\r`. Sono un errore del primo giro: il file di elenco aveva i fine riga CRLF. Gli URL Intercent-ER corrispondenti sono stati riarchiviati con l'URL corretto. Il manifest è append-only e non è stato corretto.
- Non abbiamo scaricato le determine di autorizzazione al subappalto di Intercent-ER (circa 120): sono elencate nel CSV come `pubblicato-non-archiviato`.
- Non abbiamo letto i chiarimenti START (scheda "Chiarimenti" della SPA) né i chiarimenti in testo di SATER, se non dentro la pagina archiviata.
- Le copie dei file Sintel e START stanno sul server, fuori da `archivio/`. Per portarle nell'archivio content-addressed serve un'estensione di `archivia.py` che accetti file locali.
