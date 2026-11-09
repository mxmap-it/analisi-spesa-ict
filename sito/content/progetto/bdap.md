---
title: "BDAP, la Banca dati delle amministrazioni pubbliche"
date: 2026-11-09
description: "Che cosa c'è in BDAP (MEF-RGS), come si scarica, che difetti ha, e come entra nell'imbuto della spesa ICT come denominatore dello Stato centrale e della sanità."
---

**Versione 0.1 del 9/11/2026** ([#67](https://github.com/mxmap-it/analisi-spesa-ict/issues/67), [#25](https://github.com/mxmap-it/analisi-spesa-ict/issues/25), [#30](https://github.com/mxmap-it/analisi-spesa-ict/issues/30)).
Legenda: **[V]** verificato da noi su file archiviati con sha256; **[R]** riferito da altri o dalla
documentazione della fonte, non riprodotto.

## In breve

- BDAP è l'unica fonte aperta che misura la **spesa ICT pagata dallo Stato centrale**, ministero per
  ministero, con un codice di spesa specifico per l'ICT. Nel 2024: **1,14 miliardi** pagati con
  mandati informatici sugli 11 codici gestionali ICT [V].
- Una seconda via indipendente, la classificazione economica di 3° livello del rendiconto per piano
  di gestione, dà **0,98 miliardi** per il 2024 [V]. Le due vie differiscono del 14 %.
- I nostri CIG ICT dei ministeri non sono una misura della stessa grandezza (valore del contratto
  contro cassa dell'anno), ma il confronto mostra dove mancano: MEF e Giustizia hanno pagamenti ICT
  molto maggiori dei CIG che vediamo (in-house Sogei, acquisti Consip per conto loro).
- Per la sanità il Conto economico degli enti del SSN ha una voce esplicita, **servizi di
  assistenza informatica: 604 milioni nel 2023** [V].

## Ente, portale, accesso

| | |
|---|---|
| Ente | Ministero dell'economia e delle finanze, Ragioneria generale dello Stato (RGS) |
| Portale | <https://bdap-opendata.rgs.mef.gov.it/> (CKAN; API su `/SpodCkanApi/api/3/action/`) |
| Formati | CSV (`datastore/dump/<id>.csv`, separatore `;`, **codifica Windows-1252**), XML OData (`/ODataProxy/MdData('<id>@rgs')/DataRows`), PDF di metadati per famiglia [V] |
| Licenza | Creative Commons Attribution (`license_id` cc-by su tutti i 3.684 dataset) [V sui metadati; versione della licenza non indicata] |
| Catalogo | 3.684 dataset, 11.025 risorse, circa 60 GB (raccolti il 7/11/2026, `tools/acquisizione/bdap_metadati.sh`) [V] |

Gli URL dei file che CKAN pubblica sono in `http://`: sulla porta 80 il server non risponde (timeout
il 9/11/2026), in `https://` sì [V]. `tools/archivia.py` va chiamato con gli URL riscritti in https.

## Famiglie di dataset

382 famiglie (titolo senza anno o mese). Le principali [V]:

| Famiglia | Dataset | Anni | Granularità | Per noi |
|---|---|---|---|---|
| Pagamenti Bilancio dello Stato (8 viste: per missione, amministrazione, categoria, CE di 2° livello, **gestionale**) | 8 × 128 | 2014-2026 (13 annualità), mensili e consuntivo | ministero × missione × CE2 × **codice gestionale** | **usato**: la vista «con mandati informatici … e gestionale» |
| Rendiconto pubblicato elaborabile spese, per Capitolo e per Piano di gestione | 15 + 15 | 2011-2025 | capitolo o PG, con CE di 3° livello, missione, programma, azione, centro di responsabilità | **usato**: seconda via, controllo sul nome del capitolo |
| Legge di bilancio, disegno di legge, assestamento, note di variazione (Capitolo, PG, entrate) | 16-17 ciascuna | 2011-2026 | come il rendiconto, ma previsioni | non usato: previsioni, non spesa |
| Conto economico degli enti del SSN (annuale e trimestrale, per ente, regione, nazionale) | 13 + 4 × 14 | 2008-2025 | ente SSN × voce del modello CE | **usato** per la voce BA1620 |
| SIOPE per regione (spesa e entrata cumulate, disponibilità liquide) | 20 regioni × 3 × 13 | 2014-2026 | ente × mese × codice gestionale | da confrontare con la fonte SIOPE diretta (#30) |
| Spesa statale regionalizzata | 4 × 16 | 2008-2023 | regione | non usato: nessun dettaglio ICT |
| Dipendenti pubblici, mutui e prestiti degli enti territoriali | circa 20 famiglie | | | fuori perimetro (non è spesa ICT) |

## Campi che usiamo

- **Pagamenti con mandati informatici** (consuntivo): `Esercizio finanziario`, `Codice STP`,
  `Amministrazione`, `Missione`, `Categoria`, `CE2`, `Codice Gestionale`, `OP Erario`, `OP Tesoreria`,
  `OP Esterno`, `OP` (totale ordinativi di pagamento).
- **Rendiconto per PG**: `Amministrazione`, `Numero Capitolo di Spesa`, `Capitolo di Spesa`,
  `Numero Piano di Gestione`, `Piano di Gestione`, `Codice Categoria`, `Codice CE 2° Livello`,
  `Codice CE 3° Livello`, `Pagato CP` / `Pagato RS` / `Pagato CS` (competenza, residui, cassa).
  Il rendiconto per capitolo ha lo stesso, con `Codice Puntato CE` al posto dei tre codici.
- **CE SSN**: `Anno di Riferimento`, `Codice Voce Contabile`, `Descrizione Voce Contabile`, `Importo Totale`.

## Le misure (verifica `tools/verifiche/bdap_ict_stato.py`)

Esito in `esiti/2026-11-09/bdap/ict-stato.json` (con lo sha256 di ogni file) e
`esiti/2026-11-09/bdap/pg-ict-2024.csv` (i PG ICT, per il controllo a campione).

**Via 1, codici gestionali ICT** (032 materiale informatico, 036 consulenza informatica, 051/052
manutenzione hw/sw, 056 noleggi hw, 206 software prodotto, 233 hardware, 276/277 manutenzione
straordinaria, 289 licenze, 290 sviluppo software) [V]:

| Anno | Pagato ICT | su tutti i pagamenti |
|---|---|---|
| 2022 | 987 M€ | 0,15 % |
| 2023 | 1.199 M€ | 0,18 % |
| 2024 | 1.141 M€ | 0,16 % |
| 2025 | 1.286 M€ | 0,19 % |

Nel 2024 il 63 % è software (manutenzione straordinaria 336 M€, software prodotto 241, sviluppo 152,
manutenzione ordinaria 129, licenze 73); l'hardware pesa 75 M€.

**Via 2, classificazione economica di 3° livello** (CE 2.2.19 servizi informatici e TLC, 21.1.1
licenze, 21.1.2 sviluppo software, 21.2.5 infrastrutture telematiche, 21.2.19 hardware), rendiconto
2024 per PG: 415 PG su 13.066, **979 M€** di cassa [V]. Per capitolo, serie 2019-2024: 529, 796,
731, 680, 1.077, 1.013 M€ [V].

**Regola sul nome** (informatico, telematico, sistema informativo, software, digitalizzazione…): 687
PG in più, 1,64 miliardi, **ma con molti falsi**. Controllo a campione sui 20 PG «solo nome» con più
pagato: 7 acquisti ICT veri (sistemi informativi di Interno, Giustizia, MEF, Istruzione, CED dei
Trasporti; digitalizzazione della Difesa), 5 trasferimenti legati all'ICT ma non acquisti (ACN, fondo
per l'innovazione della Presidenza del Consiglio, strategia cyber del DIS), 8 falsi (forniture
militari, lotterie telematiche, automezzi, Agenzia delle dogane) [V, a mano]. Il nome serve a trovare
capitoli da rivedere, non a misurare.

**Per ministero, 2024 (via 1)** [V]: MEF 388 M€, Giustizia 315, Interno 194, Infrastrutture 55,
Difesa 48, Esteri 28, Agricoltura 25, Lavoro 23, Cultura 16, Salute 14, Imprese 11, Università 10,
Ambiente 8, Turismo 6, Istruzione 0,2.

## Copertura dei nostri CIG

Importo dei CIG ICT dell'imbuto (strati S3-S6; esclusi i padri di accordo quadro S0, il sotto soglia
S2 e gli importi da verificare) delle stazioni appaltanti ministeriali, contro il pagato ICT per
gestionale dello stesso anno [V sui conteggi, **stima** sull'interpretazione]:

| Ministero | CIG ICT 2024 | Importo CIG | Pagato ICT BDAP | Rapporto |
|---|---|---|---|---|
| Interno | 920 | 384 M€ | 194 M€ | 2,0 |
| Difesa | 804 | 168 M€ | 48 M€ | 3,5 |
| Infrastrutture | 149 | 121 M€ | 55 M€ | 2,2 |
| MEF | 325 | 67 M€ | 388 M€ | **0,17** |
| Giustizia | 13 | 9 M€ | 315 M€ | **0,03** |
| Esteri | 168 | 11 M€ | 28 M€ | 0,38 |
| Salute | 6 | 1 M€ | 14 M€ | 0,07 |
| Lavoro | 0 | 0 | 23 M€ | 0 |

Il rapporto non è una percentuale: un CIG vale l'intero contratto pluriennale, il pagato è la cassa
di un anno, e la stessa spesa può passare per Consip o per una centrale di committenza con un altro
nome di stazione appaltante. Indica però dove l'imbuto è cieco: **MEF, Giustizia, Salute, Lavoro ed
Esteri pagano in ICT molto più di quanto i loro CIG mostrino**. Le spiegazioni probabili, da
verificare caso per caso: affidamenti in-house a Sogei (MEF, Giustizia), contratti stipulati da
Consip o da DGSIA con un nome di stazione appaltante che la nostra regola non riconosce, convenzioni
pluriennali con CIG negli anni precedenti.

## Sanità

Nel Conto economico SSN 2023, livello nazionale [V]: **BA1620 servizi di assistenza informatica
604 M€**; BA0350 supporti informatici e cancelleria 109 M€ (mista, non separabile); BA1650 utenze
telefoniche 161 M€. Manutenzioni (BA1910 e seguenti) e noleggi (BA2010) non hanno una sotto-voce
ICT. Gli investimenti in hardware e software stanno nello stato patrimoniale, non nel CE. BA1620 è
quindi un **denominatore minimo** dei servizi ICT della sanità, per ente e per anno.

## SIOPE via BDAP

Il file regionale (Lazio 2024, 435.707 righe) ha per ogni ente il codice gestionale e l'importo
**cumulato** mese per mese, con provincia, comune ISTAT, tipologia ente e popolazione [V]. Rispetto
alla fonte SIOPE diretta aggiunge l'anagrafica dell'ente, non nuovi importi [V sulla struttura;
l'uguaglianza degli importi resta da misurare, #30]. Per l'imbuto non serve: la fonte diretta resta
la via principale.

## Difetti noti

- **R61** [V]: `result.count` di `package_search` vale la dimensione della pagina, non il totale;
  pagine con offset alto in timeout a caso; metadati in repr Python invece che JSON.
- **R63** [V]: URL delle risorse in `http://` che non rispondono; CSV in Windows-1252 non dichiarato.
- **R64** [proposta]: i pagamenti per gestionale non hanno capitolo né CIG; il rendiconto per PG ha
  il capitolo ma non il gestionale. Non si può collegare un pagamento a un contratto.
- **R65** [proposta]: la spesa ICT fatta per trasferimento (ACN, AgID, fondo per l'innovazione, Sogei
  in-house, agenzie fiscali) non è marcata come ICT nel bilancio dello Stato.

## Cosa usiamo e cosa no

| Usiamo | Perché |
|---|---|
| Pagamenti con mandati informatici per gestionale, consuntivo | denominatore ICT dello Stato centrale per ministero e anno |
| Rendiconto per PG e capitolo | seconda via (CE3) per la controvalidazione; elenco dei capitoli ICT |
| CE SSN, voce BA1620 | denominatore minimo dei servizi ICT della sanità |

| Non usiamo | Perché |
|---|---|
| Leggi di bilancio, assestamenti, note di variazione | sono previsioni, non spesa |
| SIOPE via BDAP | stessi dati della fonte diretta, con l'anagrafica in più |
| Pagamenti mensili | il consuntivo li somma; i mensili servono solo a vedere la stagionalità |
| Spesa regionalizzata, dipendenti, mutui | nessun dettaglio ICT, fuori perimetro |

## Registro delle revisioni

| data | modifica |
|---|---|
| 2026-11-09 | prima versione: famiglie, campi, misure 2019-2025, copertura CIG per ministero, CE SSN, SIOPE via BDAP, R63-R65 |
