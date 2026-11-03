# Limiti di calcolo incontrati e dimensionamento proposto (3/11/2026)

Server attuale: `51.158.36.151`, **condiviso** con altri progetti (dossierlatina, pairtrading, bot, mxmap).

| risorsa | oggi (V, 3/11/2026) | note |
|---|---|---|
| CPU | 8 core, condivisi | carico medio 1,5-2 |
| RAM | 31 GB, condivisi | job pesanti con `nice`, DuckDB con `memory_limit` 6 GB |
| disco | 915 GB, **804 occupati (93%), 65 liberi** | archivio di questo progetto 121 GB; la guardia del mirror si ferma sotto 40 GB |

## Limiti incontrati

| data | limite | effetto | come l'abbiamo aggirato |
|---|---|---|---|
| 27/10 | RAM: caricamento di tutti i CIG in memoria | server irraggiungibile | regola: mai tutti i CIG in memoria, solo streaming (AGENTS §4) |
| 3/11 | RAM: `righe_cig("delta")` carica in memoria tutto l'aggiornamento mensile (~10 GB) | rischio di ripetere il 27/10; server ha retto (18 GB liberi) | script del dossier riscritto in streaming; da correggere anche `padri_ict.py` e `imbuto.py` |
| continuo | CPU e I/O: ogni passata sui CIG dal 2020 rilegge e decomprime gli zip ANAC (~15-30 minuti a passata) | ogni modifica a una regola costa un giro intero; più agenti in parallelo si contendono la stessa macchina | `nice`, esecuzioni in sequenza |
| imminente | **disco**: 65 GB liberi, guardia a 40 GB | restano ~25 GB prima che il mirror si fermi; l'acquisizione dei documenti (livelli L1-L7) non ci sta | — |

## Cosa crescerà (stime, da misurare)

- **Documenti degli acquisti** (atti, capitolati, determine) per i contratti ICT. Ordine di grandezza: centinaia di migliaia di contratti × alcuni PDF × circa 1 MB. Fa **0,5-2 TB** se si scarica tutto il perimetro ICT dal 2020; molto meno se si scarica solo il residuo incerto, come prevede l'imbuto.
- **SmartCIG** 2020-2023: circa 4,5 milioni di righe l'anno. Il testo va classificato tutto, e su questo volume l'approccio a streaming ripetuto è lento.
- **Estrazione del testo e OCR** dei PDF, più gli indici per la ricerca: CPU e RAM.
- **Modelli locali eventuali** (EuroTender/Zenodo, classificatori): GPU facoltativa.

## Proposta

**Primo passo, senza hardware nuovo (software):** convertire una volta sola CIG, SmartCIG e aggiudicatari in **Parquet** e interrogarli con DuckDB su disco. Ogni giro dell'imbuto scende da decine di minuti a pochi minuti e non usa più RAM a sorpresa. Il problema di memoria si risolve così, non con più RAM.

**Dimensionamento consigliato per una macchina dedicata al progetto:**

| componente | minimo | consigliato | perché |
|---|---|---|---|
| CPU | 8 vCPU dedicate | 16 vCPU | estrazione dei PDF e passate in parallelo senza disturbare altri progetti |
| RAM | 32 GB dedicati | 64 GB | DuckDB con margine, OCR, più agenti contemporanei |
| disco veloce (NVMe) | 1 TB | 2 TB | dati ANAC in Parquet, indici, lavoro |
| archivio documenti | 2 TB | 4 TB, anche su storage economico o oggetti S3-compatibile | archivio append-only dei documenti, che cresce ogni anno |
| GPU | no | facoltativa (≥ 16 GB VRAM) | solo se si usano modelli locali di classificazione o OCR al posto dei servizi a consumo |
| backup | copia remota dell'archivio | idem | l'archivio è la base della riproducibilità (sha256) |

**Alternativa a costo minore:** restare sul server condiviso, liberare o aggiungere disco (almeno +2 TB) e fare il passo Parquet. Basta fino all'acquisizione massiva dei documenti. Una macchina dedicata serve solo quando i livelli L1-L7 vanno a regime.

Decisione: Fabio (budget e fornitore).

## Opzione futura: mirror costante e ricercabile delle sezioni «Amministrazione trasparente» (valutazione, 4/11/2026, #61)

**Da non costruire ora.** Si attiva solo se il monitor (`tools/trasparenza/`) mostra che i blocchi o l'assenza di ricerca
sono troppo diffusi per lavorare sui siti degli enti. Tutte le cifre sono **stime da verificare** su un campione (lo
scaricamento completo di 20 sezioni stratificate darebbe le misure vere).

| voce | ipotesi | stima |
|---|---|---|
| enti | registro ANAC L.190 + IndicePA | ~30.700 (V, 3/11/2026) |
| pagine HTML per sezione | 300-3.000, media 1.000, ~50 kB | ~30 M pagine, ~1,5 TB |
| allegati per sezione | 1.000-10.000, media 3.000, ~300 kB (PDF, p7m) | ~90 M file, ~25-30 TB |
| ritmo | 1 richiesta ogni 5 s per host, ~50 host in parallelo (~10 richieste/s) | HTML: ~35 giorni; allegati: ~3-4 mesi per il primo giro |
| aggiornamento | incrementale (sitemap, date, ETag), ~5 % al mese | ~1 settimana al mese |
| testo estratto e indice | testo ~10 % degli allegati, OCR per le scansioni (vedi sopra, OCR) | ~3 TB di testo; indice full-text ~1-2 TB |
| hardware | 2 nodi di raccolta + 1 nodo indice (OpenSearch/Meilisearch) + storage a blocchi | ~300-500 €/mese (storage ~30 TB ~ 60-120 €/mese, indice dedicato ~200-300 €/mese) |
| OCR | solo scansioni, stima 20 % degli allegati | dominante: vedi la voce OCR (decine di migliaia di euro una tantum ai prezzi di mercato) |

Vincoli: stessa regola di AGENTS.md §3 (art. 9: robots.txt non vincola le sezioni obbligatorie; niente CAPTCHA, proxy,
rotazione di IP); archivio content-addressed; dati personali negli atti (pubblicati per obbligo ma con limiti di
riutilizzo e durata, art. 7-bis e 8 d.lgs. 33/2013): servirebbe una valutazione legale prima di ripubblicare i testi.
Alternativa più leggera: mirror dei soli indici (elenchi degli atti con metadati e URL), ~1-2 % del volume.
