# Via 6 — classificazione con modello linguistico e fonti: architettura proposta (bozza, 29/10/2026, #55)

Stato: **proposta**, da decidere con Fabio (`decisione-fabio`). Numeri: misurati sul campione di 611 contratti.

## Cosa abbiamo misurato oggi

| giro | modello | contratti | ricerche web | atti dell'ente aperti | esito |
|---|---|---|---|---|---|
| 1 (p1) | Opus | 611 | ~60 in tutto | 0 | classificazione dal testo; 404 alta / 161 media / 46 bassa; 204 disaccordi con regole v3.1 |
| 2 (p2) | Haiku | 45 (9 pacchetti) | 2-5 per contratto | **0** | quasi tutto declassato a media/bassa: le determine sono PDF e `WebFetch` non le legge (binario), molti siti degli enti danno 403/404/502 |

Conclusione verificata: **l'agente da solo non chiude il cerchio sugli atti dell'ente.** Il collo di bottiglia non è il ragionamento ma lo scaricamento e la lettura dei PDF.

## Divisione del lavoro: deterministico vs modello

1. **Deterministico (codice, ripetibile, senza token)** — la parte maggioritaria:
   - via 1/2 (lotti di AQ/convenzioni) da `config/lotti_cloud.yaml` e dalla base di conoscenza delle iniziative (controvalidata, `report/metodo/llm/conoscenza-iniziative.yaml` → `config/`);
   - via 3 (marchi) con le correzioni emerse dal giro 1 (falsi positivi lessicali: "AWS" stazioni meteo, "Azure S DR" pacemaker, "PSN" nel testo, "lotto N" fuori AQ, committente ≠ fornitore, rivenditore ≠ provider), ciascuna come caso in `tests/casi_classifica.yaml`;
   - **raccolta degli atti**: script server che, dato un URL, scarica nell'archivio content-addressed (sha256) ed estrae il testo (`pdftotext`, OCR `tesseract` se scansione). Questo rende verificabile e riproducibile ogni fonte primaria.
2. **Modello linguistico (token, solo dove serve)**:
   - trovare l'URL dell'atto (ricerca web sul CIG/oggetto, navigazione di Amministrazione trasparente);
   - leggere il **testo estratto** dallo script (non il PDF) e classificare con confidenza e motivazione;
   - solo per i contratti che le regole non chiudono o su cui regole e modello divergono.
3. **Revisione umana**: tutti i casi a confidenza bassa/disaccordo + un campione casuale dell'alta (precisione misurata per livello di confidenza).

## Ciclo annuale (aggiornamento)

nuovi CIG → regole (deterministiche) → residuo → modello trova l'URL → script scarica/estrae/archivia → modello classifica sul testo → revisione umana a campione → le regolarità ricorrenti diventano regole/tabelle in `config/` (il residuo si riduce ogni anno).

## Dove gira

Sul server (`mxmap.it@51.158.36.151`), CLI `claude -p` in abbonamento, modello Haiku per la classificazione, job ripartibili con stato su file, `nice`, massimo 10 in parallelo. Richiede l'autenticazione della CLI per l'utente `mxmap.it` (da fare da Fabio).

## Da decidere

- soglia di precisione per usare l'"alta" del modello nei numeri pubblicati senza revisione;
- quota di token annua accettabile per il residuo.
