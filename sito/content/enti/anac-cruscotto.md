---
title: "ANAC: cruscotto di disponibilità"
date: 2026-11-09
description: "Esito giornaliero delle metriche di non ricorrenza I1-I9 sui dati aperti ANAC e stato di ogni problema del registro. Ultima misura: 2026-11-09."
---
Ogni mattina alle 06:40 la sonda misura dal vivo il portale `dati.anticorruzione.it`. **Ultima misura: 2026-11-09: 8 metriche violate su 9.** Quando ANAC corregge un problema la sua metrica passa a *rispettata*.

Dati aperti: [anac-cruscotto.json](/dati/anac-cruscotto.json). Metodo: `tools/metriche_anac.py`, pagina generata da `tools/cruscotto_anac.py`.

## Metriche di non ricorrenza

| Metrica | Controllo | Ultimo esito | Giorni violata / misurati | Problemi |
|---|---|---|---|---|
| I1 | file OCDS del mese precedente pubblicato dopo il giorno 2 | **violata** | 13 / 15 | P02 |
| I2 | endpoint dell'API REST OCDS raggiungibili e swagger valido | **violata** | 15 / 15 | P06 |
| I3 | licenza del catalogo uguale a quella nel file OCDS | **violata** | 15 / 15 | P07 |
| I4 | nessun mese OCDS con contenuto identico a un altro | **violata** | 15 / 15 | P01 |
| I5 | nessun mese mancante nelle serie di delta | **violata** | 15 / 15 | P09 |
| I6 | nessuna risorsa delta archiviata sparita dalla fonte | rispettata | 0 / 15 | P08 |
| I7 | dimensione dichiarata entro il 5% di quella servita | **violata** | 15 / 15 | P11 |
| I8 | nessuna risorsa elencata che risponda 404 | **violata** | 15 / 15 | P10 |
| I9 | nessuna risposta 200 text/html al posto del file o dei suoi metadati, per HEAD e GET | **violata** | 15 / 15 | P12 |

Serie dal 2026-10-26 al 2026-11-09; un giorno senza file significa che la sonda non ha girato.

## Registro dei problemi

Schede complete: [problemi e rimedi](/rendiconti/anac-2026-10-problemi/).

| Id | Problema | Gravità | Stato | Pronto per ANAC |
|---|---|---|---|---|
| P01 | Mesi OCDS diversi servono lo stesso file, con il solo campo uri riscritto | alta | aperto | sì |
| P02 | OCDS fermo a marzo 2026; del 2026 è pubblicato solo marzo | alta | aperto | sì |
| P03 | OCDS 2026: il fornitore aggiudicatario manca nell'80% degli award, contro il 99% degli anni precedenti | alta | aperto | sì |
| P04 | OCDS: date delle release in formato non conforme in tutte le release | media | aperto | sì |
| P05 | OCDS: copertura parziale delle aggiudicazioni rispetto ai tabellari | media | aperto | sì |
| P06 | API REST OCDS dichiarata ma non funzionante | media | aperto | sì |
| P07 | Licenza dell'OCDS: CC BY 4.0 nel catalogo e nella pagina, CC BY-SA 4.0 nel file | bassa | aperto | sì |
| P08 | Aggiornamenti mensili (delta) rimossi senza regola dichiarata; gennaio-marzo 2026 persi | alta | aperto | sì |
| P09 | Mesi mancanti di smartcig (giugno e luglio 2026) e distribuzione JSON interrotta | media | aperto | sì |
| P10 | Il catalogo elenca risorse inesistenti | media | aperto | sì |
| P11 | Dimensioni dichiarate dal catalogo 4,1 volte quelle servite | bassa | aperto | sì |
| P12 | HEAD dei programmi non-browser: risposta 200 text/html invece dei metadati del file | media | aperto | sì |
| P13 | Nessun ETag sulle risorse | bassa | aperto | sì |
| P14 | CUP 'ND' al posto del codice in 1.951.844 righe | media | aperto | sì |
| P15 | Contratti attuativi senza collegamento all'accordo quadro o convenzione | da_valutare | aperto | sì |
| P16 | Aggiornamenti mensili 2026 con righe non conformi al formato CSV (escape \" invece di "") | media | aperto | sì |
| P17 | Codici fiscali segnaposto delle stazioni appaltanti (es. CFAVCP-0001C57) | bassa | aperto | sì |
| P18 | Il link ai documenti di gara di ciascun CIG non è negli open data: solo nell'API PVL, dal 2024, e manca per 1 CIG su 3 | alta | aperto | sì |
