# Rapporto CPV, parte A: rassegna della letteratura sull'attendibilità del CPV

Stato: prima ricognizione, 30/10/2026 (#59). Legenda: **V** = verificato aprendo la fonte primaria; **R** = riferito da terzi (snippet di ricerca, citazione secondaria). Distinguiamo misure di **COMPILAZIONE** (il campo c'è) da misure di **CORRETTEZZA** (il codice è coerente con l'oggetto).

## Executive summary

- **Nessuna fonte trovata misura in modo rigoroso e pubblico il tasso di CPV *sbagliati* (correttezza) né per l'ICT né per il cloud.** La lacuna è il nostro spazio originale (parte B).
- Le misure esistenti sono soprattutto di **compilazione/qualità generica**: la Corte dei conti europea (SR 28/2023, PDF aperto il 6/11/2026) misura **valori mancanti in circa il 30 % dei contratti TED** (p. 35, fig. 12-13) e cita in modo solo qualitativo una «inaccurate contract classification» (§ 74, p. 36); la cifra del **49,8 % attribuita alla ECA da OCP non compare** nel testo inglese né in quello italiano (V, vedi fonte 1). Lo Single Market Scoreboard ha indicatori di qualità (10–12) che **non** riguardano il CPV (R).
- Le uniche indicazioni di **correttezza** sono: studio Ramboll/BME per la Commissione (dicembre 2012, MARKT/2011/111/C, PDF aperto il 6/11/2026): su **405 avvisi TED** controllati, codice **inesatto nel 23 %** (10 % non descrive l'oggetto, 8 % troppo generico, 4 % troppo specifico; lavori 28 %) (V, vedi fonte 1-bis); dati commerciali Tendios (Spagna): **34%** codici troppo generici, **7%** chiaramente errati, metodo non pubblicato (R, indicativo).
- Sui dati **ANAC** (5 milioni di coppie descrizione→CPV, Zenodo 10007545) Siciliani et al. (2023) dichiarano qualitativamente che le etichette contengono "refusi o interpretazioni errate" e un uso molto sbilanciato dei codici, ma **non quantificano** l'errore delle etichette (V). Il loro miglior modello indovina il codice esatto solo nel **37,2%** dei casi e la divisione con accuratezza 0,78 (SVC): numeri del classificatore, non dell'errore umano.
- Sull'aggiornamento del vocabolario: la competenza è della **Commissione** (revisione per comitato, Reg. 2195/2002) (R); dal 2017–18 esiste un gruppo di esperti CPV di DG GROW (R); OCP nel 2025 propone di **sganciare l'evoluzione del CPV dal regolamento** per stare al passo con le nuove tecnologie (V).

## Fonti

### 1. Corte dei conti europea, Relazione speciale 28/2023 "Appalti pubblici nell'UE"
- Autore/anno: ECA, 4/12/2023; periodo 2011–2021. URL: https://www.eca.europa.eu/en/publications/SR-2023-28
- Perimetro: dati TED, tutta l'UE. Misura: qualità generica (completezza/coerenza), **non specifica per CPV** in quanto reperito.
- PDF archiviati il 6/11/2026: EN sha256 `620c6d6798c08f27dbf2d36f5c8bc24f593dc0fc1391be23dd79bcf5db671e00`, IT sha256 `694e7e91a44b354cb7d35c48b10c0965006c20b4c384d75b784de42041825d04` (archivio/mirror/www.eca.europa.eu/ECAPublications/SR-2023-28/).
- Numeri **V**: valori mancanti in circa il 30 % dei contratti, stabile dal 2017 (§ 71, fig. 12, p. 35); campi più spesso vuoti: numero di registrazione nazionale 86,3 %, valore stimato 63,6 % (fig. 13); § 74 (p. 36): valori anomali frequenti e, fra gli errori, «inaccurate contract classification», **senza una cifra**.
- **La cifra del 49,8 % (p. 37) citata da OCP non c'è**: ricerca di «49,8» e «49.8» nel testo estratto (pdftotext) delle versioni EN e IT, zero risultati; a p. 37 c'è il § 75 sugli identificativi unici. Resta una citazione OCP non riscontrata nella fonte: non usarla.
- Seguito: conclusioni del Consiglio del 24/5/2024 sulla disponibilità di dati di qualità (R).
- Dati aperti: un dataset ECA collegato è segnalato su baselight.app (R).

### 1-bis. Ramboll Management Consulting e BME per la Commissione (DG MARKT), «Review of the functioning of the CPV codes/system», dicembre 2012
- URL: https://ec.europa.eu/docsroom/documents/21583/attachments/1/translations/en/renditions/pdf — archiviato il 6/11/2026, sha256 `6f49d824693eb84616ef81c887ed9c559089721a1753ed86673f5620a91b38ae` (archivio/mirror/ec.europa.eu/docsroom/documents/21583/…). **V**.
- Misura di **correttezza** (sintesi, «Extent of (in)correct use of the CPV»): campione di **405 avvisi TED**; codice inesatto in circa il **23 %**: circa 10 % il codice non descrive l'oggetto, circa 8 % troppo generico, circa 4 % troppo specifico; per i lavori circa 28 %. Il precedente «450 documenti» era una lettura di seconda mano: è 405.
- Altro (V): 1.221 codici su 9.454 (13 %) fanno l'80 % degli usi; il CPV è usato in circa il 15 % delle ricerche degli offerenti, che preferiscono le parole chiave.

### 2. Open Contracting Partnership, contributo alla consultazione sulla revisione delle direttive appalti (2025)
- URL: https://www.open-contracting.org/wp-content/uploads/2025/08/EU-DirectivesConsultation2025-Submission-OCP.pdf — **V** (testo estratto).
- Contenuto: "i dati pan-UE sono buoni solo a metà" (cita 49,8% ECA); TED copre circa il 30% degli appalti europei; propone di **disaccoppiare l'evoluzione delle classificazioni CPV dal regolamento CPV** e una nuova classificazione che consideri le nuove tecnologie. Nessuna misura propria di correttezza CPV.

### 3. Siciliani, Tanzi, Basile, Lops (Univ. Bari), "Automatic Generation of Common Procurement Vocabulary Codes", CLiC-it 2023
- URL: https://aclanthology.org/2023.clicit-1.47.pdf; dataset https://zenodo.org/records/10007545; codice https://github.com/ematanzi/Valutazione-CPV/; modelli https://huggingface.co/basilepp19/cpv-it5 — **V**.
- Perimetro: ~5 milioni di coppie (oggetto gara, CPV) dagli open data ANAC; split 3,2M/0,8M/1M.
- Affermazione qualitativa (V): il gran numero di codici (9.454 termini) "porta frequentemente a errori nell'assegnazione del CPV come refusi o interpretazione errata della descrizione"; uso sbilanciato (pochi codici molto usati, molti sottoutilizzati). **Nessun tasso di errore delle etichette misurato**: le etichette ANAC sono trattate come verità.
- Numeri (del classificatore, V): baseline motore di ricerca, corrispondenza perfetta 11,34%, nessuna corrispondenza utile 61,77%; IT5-large codice esatto 37,22%, nessuna corrispondenza 11,06%; IT5-base 35,94%. Classificazione della sola divisione: Linear SVC accuratezza 0,777 (macro-F1 0,40), BERT 0,741.
- Dati e codice aperti: sì.
- Uso per noi: l'errore residuo del classificatore include anche errore delle etichette, ma non si può separarlo senza annotazione umana.

### 4. Studio Ramboll/BME per la Commissione europea, "Review of the functioning of the CPV codes/system" (2012)
- URL repository: https://ec.europa.eu/docsroom/documents/21583 (redirect a CIRCABC, **404** al 30/10/2026). Sintesi: vergabeblog.de (R).
- Metodo (R): 25 interviste, sondaggio online con ~12.000 utenti, **analisi dettagliata di 450 documenti per individuare codifiche CPV errate**. Tasso di errore non reperito.
- Raccomandazioni (R): ridurre il dettaglio (~9.500 codici), eliminare il vocabolario supplementare inutilizzato, togliere codici poco usati, migliori strumenti di ricerca per le stazioni appaltanti, versioning trasparente (oggi non è chiaro come nascano le nuove versioni).

### 5. Kuljanin (DTVP/cosinex), studio empirico sull'uso del CPV in TED, 2018 (da tesi di dottorato)
- URL: https://blog.cosinex.de/2018/02/16/empirische-studie-zur-verwendung-des-cpv-codes-teil-2/ — **V** (sintesi dell'autrice).
- Perimetro: 2.041.756 bandi TED 2011–2015, DE/AT/FR/UK. Misura di **compilazione/uso**: media 2,48 codici per bando (mediana 1); il 58,9% usa un solo codice. Qualitativo su correttezza: coppie generico+specifico ridondanti, sinonimi usati incoerentemente, **lacune della nomenclatura**. Nessun tasso di errore.
- Un sondaggio tedesco citato in rete riporta il 45% di uso di codici molto generici (R, fonte primaria non aperta).

### 6. Tendios (fornitore commerciale, Spagna), guida ai CPV
- URL: https://tendios.com/en/blog/cpv-codes-definition-and-tender-search-guide — **R** (snippet).
- Numeri: **34%** dei bandi con codici eccessivamente generici (2–3 cifre), **7%** con codici chiaramente errati; per l'IT molte amministrazioni usano il generico 72000000-5. Metodo e dati non pubblicati: solo indicativo.

### 7. Single Market Scoreboard (Commissione), appalti pubblici
- URL: https://single-market-scoreboard.ec.europa.eu/ — **R**.
- Indicatori di qualità dati 10–12: aggiudicazioni senza riferimento al bando, numero di registrazione fornitore/acquirente mancante. **Nessun indicatore CPV**.

### 8. Public Procurement Data Space (PPDS) e eForms
- URL: https://www.public-procurement-data-space.europa.eu/dashboards — **R**.
- Regole di qualità per validità, completezza, coerenza, accuratezza; cruscotto qualità previsto. Cifre CPV non reperite. Telles (2024, CBS) conclude che PPDS ed eForms migliorano "in parte" completezza e qualità (R).
- eForms: CPV principale obbligatorio; dal 15/1/2020 il CPV principale deve essere coerente con il tipo di servizio, pena il rifiuto dell'avviso (regola di validazione, non misura) (R, vergabeblog).

### 9. DIGIWHIST / Opentender
- Presentazione DIGIWHIST 2015 (slideshare) su tassi di dati mancanti in TED per campi obbligatori (R). **Nessuna misura di correttezza CPV reperita**; indicatori di completezza CPV per Paese non verificati.

### 10. Spend Network / Open Opps
- Assegna un CPV con classificatore bayesiano quando manca (R, https://spendnetwork.com/european-procurement-around-covid-our-data-analysis/). Pubblica report giornalieri di qualità (openopps.com/blog/data-quality-reports-*) non esaminati per il CPV. **Nessun tasso di errore pubblicato reperito**. Tussell: nulla reperito.

### 11. Altri lavori accademici
- TU Delft, DGO 2025: qualità TED scarsa, risultati sensibili al sottoinsieme di CPV scelto (R).
- Zero-shot hierarchical classification on CPV (arXiv 2405.09983) e tesi UPM (Guerra): classificazione automatica, nessun tasso di errore delle etichette reperito (R).
- arXiv 2602.16731 (BOE Spagna 2014–2024): segnala contratti senza CPV (compilazione) (R).

### 12. OCSE, ANAC, AgID, Corte dei conti italiana
- OCSE/SIGMA: documenti generali sul CPV (sigmaweb.org), nessuna misura reperita (R).
- ANAC: usa il CPV indicato all'acquisizione del CIG come chiave di selezione nelle proprie analisi di prezzo (R); obbligo storico di monitorare la **completezza** della BDNCP (R). **Nessuno studio ANAC/AgID/Corte dei conti sulla correttezza del CPV reperito.**

## ICT e cloud
- **Nessuna misura specifica di correttezza del CPV per ICT/cloud/SaaS trovata.** Unico indizio: uso diffuso del generico 72000000-5 (R, Tendios). Lacune qualitative note: nomenclatura statica rispetto a nuove tecnologie (OCP, V); lacune e sinonimi (Kuljanin, V).

## Chi aggiorna il CPV e come
- Reg. (CE) 2195/2002: la struttura va adattata ai mercati; le misure di revisione sono adottate dalla **Commissione** con procedura di comitato (art. 3(2)) (R). Ultima revisione sostanziale: Reg. (CE) 213/2008 (R).
- Consultazioni pubbliche: 2006 (R); studio Ramboll 2012 (R); gruppo di esperti CPV con consulenza DG GROW.A.1, 2017–18 (https://ec.europa.eu/docsroom/documents/27821, R, solo metadati). Nessuna revisione recente reperita.
- Proposta OCP 2025: classificazione evolvibile fuori dal regolamento (V).

## Da fare
- ~~Aprire il PDF ECA SR 28/2023 (p. 37)~~ fatto il 6/11/2026: il 49,8 % non c'è (fonte 1). ~~Rapporto Ramboll/BME 2012~~ trovato e letto (fonte 1-bis).
- Cercare il rapporto finale Ramboll 2012 (tasso sui 450 documenti) e il dataset dei cruscotti PPDS.
