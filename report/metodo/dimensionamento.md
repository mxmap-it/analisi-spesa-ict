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
