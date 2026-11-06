# Base dati delle convenzioni e degli accordi quadro ICT (#62)

Versione 0.1 — 5/11/2026. Sezione del sito generata: `/convenzioni/` (`tools/convenzioni/pagine.py`).

## File

| File | Cosa | Prodotto da |
|---|---|---|
| `padri-ict-2024-2025.csv` | CIG padre richiamati da attuativi con CPV ICT pubblicati nel 2024-2025, con numero ed euro | `tools/analisi/padri_ict.py 2024 2025 …` (server, streaming) |
| `censimento.csv` | una riga per lotto (CIG padre) delle iniziative scelte, con tipo di soggetto, valore e stato | `tools/convenzioni/censimento.py` |
| `consip/<id>.json` | pagina pubblica dell'iniziativa su consip.it: URL, sha256 dell'HTML, documenti linkati | `tools/convenzioni/consip_pagine.py` |
| `archiviati.jsonl` | documenti archiviati (url, sha256, data, contenuto degli zip) estratti dal manifest dell'archivio | `tools/convenzioni/archivia_documenti.py` |
| `curate.yaml` | dati curati a mano (aggiudicatari, massimali, listini, giurisdizione, analisi), ognuno con fonte e livello V/R | a mano |
| `iniziative.json` | **la base dati**: una voce per iniziativa con i lotti, l'inventario dei documenti e le mancanze | `tools/convenzioni/base_dati.py` |
| `lotti.csv` | vista piatta: una riga per iniziativa e lotto | `tools/convenzioni/base_dati.py` |
| `rimandi.jsonl` | allegati/appendici citati nei PDF archiviati, con documento, pagina, sha256 | `tools/convenzioni/rimandi_documenti.py` (server) |
| `ricontrollo-pagine.json` | ricontrollo dal vivo delle pagine ufficiali (http, sha256, nomi dei file) | `tools/convenzioni/ricontrollo_pagine.py` |
| `documenti-mancanti.csv` | inventario per file dei documenti mancanti (metodo, evidenza, criticità, livello, accesso civico) | `tools/convenzioni/documenti_mancanti.py` |
| `documenti-mancanti-curati.yaml`, `blocchi-accesso.csv` | righe accertate a mano; blocchi (login, 401/403/429) del ricontrollo | a mano; `documenti_mancanti.py` |
| `schema.json` | schema JSON di `iniziative.json` | a mano |
| `PROGRESSO.md` | file di ripresa del lavoro | a mano |

Ricostruzione completa da un clone pulito: `python tools/verifiche/convenzioni_copertura.py` (rifà censimento e base dati,
controlla che l'uscita non cambi e ricalcola i totali per seconda via).

## Criterio del censimento

1. **Iniziativa** = ID Sigef Consip (dall'oggetto del CIG padre in BDNCP, o dalla base di conoscenza `config/iniziative_ict.yaml`);
   per gli altri soggetti, la gara (stesso testo dell'oggetto di gara) identificata dal CIG padre più basso. Il PSN è un'iniziativa a sé.
2. **Valore** = somma dell'importo dichiarato in BDNCP dei CIG derivati con CPV ICT pubblicati nel 2024-2025. Non è il transato:
   alcuni attuativi riportano il massimale dell'AQ (es. 31 G€ dichiarati sul lotto 1 dell'ID 2483 su tutto il periodo). Serve a ordinare, non a misurare.
3. **Non vecchie** (precisazione di Fabio del 5/11): iniziative con CIG derivati ICT nel 2024-2025, oppure nuove senza derivati nei
   dati (PRINCO ID 2928, IaaS/PaaS 2 ID 2746). Le iniziative della base di conoscenza senza derivati recenti ma con almeno 100 M€ dal 2020 restano
   come **storiche**, segnalate a parte.
4. **Tipo di soggetto** dalla stazione appaltante del CIG padre, con le regole di `config/tipi_soggetto.yaml`: Consip, PSN,
   aggregatore regionale (centrali regionali e città metropolitane), consorzio o unione (unioni di comuni, consorzi, CUC, SUA e province), altro.
   Le regole sono **da verificare** con l'elenco ANAC dei soggetti aggregatori archiviato con sha256.
5. **Principali** = le prime per valore in ciascun tipo: 40 Consip, 25 aggregatori regionali, 15 consorzi o unioni, 10 altri; fuori Consip
   servono almeno 3 derivati e 1 M€ (sotto, un CIG padre è un contratto singolo con qualche variante, non un'iniziativa di acquisto aggregato).
   Il tetto non sempre si raggiunge: sopra le soglie ci sono meno consorzi e unioni.
6. **Inventario**: per ogni iniziativa, 13 tipi di documento attesi (più i progetti dei fabbisogni per PSN e SPC Cloud). Stato:
   `archiviato` (copia con sha256), `pubblicato-non-archiviato`, `non-pubblicato` (assente dalla pagina ufficiale consultata, con data),
   `da-verificare`. Il tipo si deduce dal nome del file, anche dentro gli zip della documentazione: una deduzione, controllata a mano solo per PRINCO.
   **Copertura** = tipi archiviati / tipi attesi.

## Limiti noti

- La pagina Consip si cerca con la ricerca pubblica di consip.it: con il solo CIG (iniziative senza ID) di solito non si trova (R38).
- Aggregatori regionali e consorzi: le pagine sono su piattaforme diverse (Sintel, Intercent-ER, EmPULIA, START…) e non ancora visitate.
  Il loro inventario è «da verificare» (R40). La mappa delle piattaforme del #57 (`esiti/pvl-link-cig/2026-11-04/`) è la via successiva.
- Aggiudicatari, massimali e durata sono compilati per ora solo dove c'è un rendiconto o una voce curata.
