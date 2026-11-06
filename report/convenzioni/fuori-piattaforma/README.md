# Documenti delle convenzioni fuori dalle piattaforme delle centrali (ticket #62)

`trovati-2026-11-07.csv`: una riga per ognuna delle 415 coppie (iniziativa, documento atteso) di criticità 3 di `database/documenti-mancanti.csv` (offerte, listini, ordinativi, transato, progetti dei fabbisogni), cercate fuori da Consip, PSN e aggregatori. Se un documento è stato trovato in più atti, ci sono più righe.

## Metodo
1. `tools/convenzioni/fuori_piattaforma_derivati.py` (server): CIG derivati dei padri (`lotti.csv`; `cig_accordo_quadro` nei file CIG ANAC 2022-2026) → 48.200 derivati, uniti al link «documenti di gara» della PVL (`lavoro/pvl/cig_link.csv`). **Solo 43 derivati (14 iniziative) hanno un link**: le adesioni quasi mai indicano in BDNCP dove sono gli atti (R30).
2. `tools/convenzioni/fuori_piattaforma_cerca.py` (server): browser reale (Playwright + Chrome headless, UA con l'URL del progetto), ≥ 5,5 s per host, ordine 17 «pagina-non-trovata» → altre non Consip → Consip; fino a 6 pagine per iniziativa su host diversi; allegati pertinenti archiviati con `tools/archivia.py` (sha256) e letti con pdftotext. 27 pagine, 9 allegati.
3. `tools/convenzioni/fuori_piattaforma_esiti.py`: abbinamento per parole nel testo, poi **lettura a mano** degli allegati (correzioni in post-elaborazione: gli allegati della Regione Siciliana sono la RdO e i modelli dell'Appalto Specifico, non l'offerta dell'aggiudicatario).
4. Ricerca web per CIG e oggetto sulle 17 iniziative prioritarie e sui 10 enti con più adesioni senza link PVL (Univ. Bologna, CNR, Informatica Alto Adige, Sogei, Min. Interno PS, Roma Capitale, Regione Siciliana, ESTAR, INFN, Univ. Padova): 3 atti trovati e archiviati.

## Esiti
- 5 righe **trovato-parziale** (V, letti da noi), nessuna completa: ordinativi singoli per consip-2483 (Giustizia, det. 8784/2026, 45c16e2f…), consip-2610 (Trieste, det. 1345/2026, 5b16263d…; Regione Siciliana DDG 292/2026, 8c8dc80b…), cig-91881762B3 = ID 2366 (Regione Siciliana, RdO AS lotto 4, 201817bc…), listino PSN (AdSP MAM, det. 167/2025 «aggiornamento listino 2025», ca0f1fb5…, solo importi del progetto).
- 411 righe **non-trovato**, con le fonti provate in `note`.
- Nessuna offerta tecnica o economica dell'aggiudicatario, nessun listino completo, nessun dato di transato/erosione trovato fuori dalle centrali.
- Blocchi: 1 reale (ICE, HTTP 428 «Seeweb authentic user check») in `blocchi-accesso.csv` e R45. I «login» dei portali PortaleAppalti (Eldasoft/Maggioli) erano il solo link «Area riservata»: falsi positivi, non registrati. Altri errori: TLS (Acquirente Unico), HTML al posto del file (Sintel, piattaforma non AT), 404/500 (Sispi, ASST Bergamo Ovest, Città metr. Catania, ASREM).

## Limiti
- Copertura bassa: 43 link PVL su 48.200 derivati. La via albo/AT per cf_ente è stata provata solo con ricerca web sui primi 10 enti, non visitando ogni sezione AT; resta da fare con un elenco dei siti degli enti (IndicePA).
- Il controllo per parole legge le prime 30 pagine; i livelli V valgono per le righe trovate, lette a mano. Le note «non-trovato» valgono per le fonti elencate, non escludono l'esistenza del documento.

## Passo 4: sezioni AT degli enti aderenti (6/11/2026)
**Metodo.** `tools/convenzioni/fuori_piattaforma_at.py` (server): enti dei 48.200 derivati delle iniziative di criticità 3 (8.018 cf_ente), ordinati: i 10 con più adesioni senza link PVL, poi gli altri per adesioni decrescenti, a blocchi di 20, stop al primo blocco a resa zero. Sito da IndicePA (CKAN `datastore_search`, risorsa «Enti», `Sito_istituzionale`). Chrome headless (UA con URL del progetto), ≥ 5,5 s per host (lock condiviso), 5 processi: home → link «Amministrazione/Società trasparente» → «Bandi di gara e contratti» (+ «Provvedimenti» se presente) → fino a 10 sottopagine pertinenti (atti, affidamenti, determine, anni) → dettagli con CIG nel testo del link → allegati (archiviati con sha256, pdftotext, parole crit. 3). Esiti con `fuori_piattaforma_at_esiti.py` → `at-enti-2026-11-07.csv`; in `trovati-2026-11-07.csv` le note delle righe non-trovato elencano le sezioni AT provate.

**Resa per blocco** (enti con almeno un CIG derivato nelle pagine visitate): blocco 0 = 1/20, blocco 1 = 1/20, blocco 2 = 0/20 → stop. 60 enti: 37 sezione «Bandi» raggiunta, 4 AT senza voce «Bandi», 10 bloccate (HTTP 403/428, challenge), 4 senza sito in IndicePA, 4 irraggiungibili, 1 altro.

**Esiti (V).** CIG derivati trovati in pagina: 2 (Informatica Alto Adige, B205A147EF in «delibere a contrarre o atti equivalenti»; Insiel, BCBE18FE56 in «elenco dei provvedimenti»), senza allegati con contenuto di criticità 3 (l'unico allegato archiviato, Insiel 823af46c…, è un modello di autocertificazione). **Nessuna riga passa da non-trovato a trovato**: restano 5 parziali e 411 non-trovato.

**Blocchi.** 12 righe nuove in `../blocchi-accesso.csv` (tipo `#62-at`) e voce R46 in `richieste-e-raccomandazioni.yaml` (evidenza di possibile violazione art. 9 d.lgs. 33/2013; da riconfermare a mano). Il reCAPTCHA del portale ANAC (dati.anticorruzione.it), raggiunto da un link dell'ARES Sardegna, non è stato registrato come blocco dell'ente.

**V/R.** V: HTTP, presenza dei CIG nelle pagine e contenuto degli allegati misurati da noi (HTML archiviati per sha256 in `lavoro/.../at-html/` sul server). Nessun dato riferito.

**Limiti.** Visita superficiale (≤ 10 sottopagine per ente, nessuna ricerca interna né paginazione): «0 CIG» non prova l'assenza dell'atto. Molte sezioni AT delegano gli atti a piattaforme esterne (PortaleAppalti, albo) non seguite; i CIG di adesione spesso non compaiono nelle pagine di elenco. Alcune righe di blocco sono pagine collegate (non la sezione AT in senso stretto). Il criterio di stop (resa zero al blocco 2) chiude la via dopo 60 enti su 8.018: per i restanti la via utile resta l'accesso civico (L7).
