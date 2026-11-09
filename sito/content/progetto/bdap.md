---
title: "BDAP, la Banca dati delle amministrazioni pubbliche"
date: 2026-11-09
description: "Che cosa c'è in BDAP (MEF-RGS), come si scarica, che difetti ha, e come entra nell'imbuto della spesa ICT come denominatore dello Stato centrale e della sanità."
---

**Versione 0.4 del 10/11/2026** ([#67](https://github.com/mxmap-it/analisi-spesa-ict/issues/67), [#25](https://github.com/mxmap-it/analisi-spesa-ict/issues/25), [#30](https://github.com/mxmap-it/analisi-spesa-ict/issues/30)).
Legenda: **[V]** verificato da noi su file archiviati con sha256; **[R]** riferito da altri o dalla
documentazione della fonte, non riprodotto.

## In breve

- BDAP è l'unica fonte aperta che misura la **spesa ICT pagata dallo Stato centrale**, ministero per
  ministero, con un codice di spesa specifico per l'ICT. Nel 2024: **1,14 miliardi** pagati con
  mandati informatici sugli 11 codici gestionali ICT [V].
- Una seconda via indipendente, la classificazione economica di 3° livello del rendiconto per piano
  di gestione, dà **0,98 miliardi** per il 2024 [V]. Le due vie differiscono del 14 %.
- La seconda via per anno, 2019-2024: 492, 740, 675, 452, 1.007, 979 M€ [V]. Il salto del 2023 è
  soprattutto una riclassificazione dei piani di gestione del MEF (18 M€ nel 2022, 297 nel 2023) [V
  sui numeri, interpretazione da verificare]: prima del 2023 la seconda via non è confrontabile.
- Abbinando stazione appaltante e ministero per **codice fiscale** (IndicePA) invece che per nome,
  i CIG ICT ministeriali passano da 10.758 a 23.644 (da 5,0 a 8,2 miliardi, 2020-2026) [V]. Il buco
  della **Giustizia era quasi tutto un artefatto** della regola sul nome: nel 2024 i suoi CIG ICT sono
  359 per 213 M€, non 13 per 9, e la quota 2024 dei contratti attivi vale 0,96 volte il pagato [V].
- Il buco del **MEF resta**: quota 2024 dei CIG attivi 97 M€ contro 388 pagati (0,25) [V]. I
  contratti in-house con Sogei che hanno un CIG ANAC ne spiegano poco (circa 26 M€ l'anno, [stima]);
  il resto non ha un CIG che vediamo (§ Sogei).
- SIOPE via BDAP e SIOPE diretto coincidono sull'ICT dove BDAP è completo (99,5-100 % delle coppie
  ente × codice uguali all'euro, 20 regioni, 2023-2025) e differiscono dello 0,7 % sul totale, per i pagamenti da
  regolarizzare [V]. Il **difetto riferito da AgID si riproduce** su tutte le 20 regioni [V]: nel 2025
  Lombardia e Friuli-Venezia Giulia si fermano a marzo (1.717 comuni) e mancano 84 comuni di Trento;
  2023 e 2024 sono completi (§ SIOPE via BDAP, R75).
- Per la sanità il Conto economico degli enti del SSN ha una voce esplicita, **servizi di
  assistenza informatica: 604 milioni nel 2023** [V].

- **Giro 0.4 (10/11):** archiviati i CE SSN annuali per ente 2022 e 2024 e il IV trimestre 2025 (prima
  c'era solo il 2023). BA1620, consolidato regionale «999»: **530, 604, 720 M€** nel 2022-2024 [V]. Con
  SIOPE (pagina [SIOPE](/progetto/siope/)) lo Stato BDAP si somma agli enti non statali: **spesa ICT
  pubblica pagata circa 5,1 miliardi nel 2024** (1,14 Stato + 3,97 SIOPE), contro 14,0 miliardi di CIG ICT
  pubblicati nell'anno [V].

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

**Via 2 per anno, rendiconto per PG 2019-2024** (giro 0.2; file archiviati con `tools/archivia.py`,
sha256 in `esiti/2026-11-09/bdap/ict-stato.json`, PG elencati in `esiti/2026-11-09/bdap/pg-ict.csv`) [V]:

| Anno | PG | PG con CE ICT | Pagato CE ICT | Via 1 (gestionali) | CE / gestionali |
|---|---|---|---|---|---|
| 2019 | 11.487 | 330 | 492 M€ | — | — |
| 2020 | 11.677 | 361 | 740 M€ | — | — |
| 2021 | 12.557 | 376 | 675 M€ | — | — |
| 2022 | 12.968 | 376 | 452 M€ | 987 M€ | 46 % |
| 2023 | 13.082 | 418 | 1.007 M€ | 1.199 M€ | 84 % |
| 2024 | 13.066 | 415 | 979 M€ | 1.141 M€ | 86 % |

Dal 2023 i PG con CE ICT che hanno anche un nome ICT passano da 214 a 386, e il MEF da 18 a 297 M€:
i piani di gestione dei sistemi informativi sono stati riclassificati nelle voci ICT [V sui numeri;
la causa è un'interpretazione]. Per gli anni prima del 2023 la seconda via sottostima e non serve
come controvalidazione; la via 1 (gestionali) parte dal 2022 nei file archiviati.

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
pluriennali con CIG negli anni precedenti. *(Tabella del giro 0.1, abbinamento per nome: superata
dalla sezione seguente.)*

### Abbinamento per codice fiscale e quota annua dei contratti (giro 0.2)

Verifica `tools/verifiche/bdap_cig_ministeri_cf.py`, esito `esiti/2026-11-09/bdap/cig-ministeri-cf.json`.

**Come.** Il codice fiscale della stazione appaltante di ogni CIG ICT (e, se manca nel ministero,
quello della SA delegante) si cerca in IndicePA: in `amministrazioni.txt` (CF dell'ente) e in
`servizi-fatturazione-elettronica.txt`, che dà il CF di ogni ufficio di fatturazione (prefetture,
tribunali, comandi, soprintendenze) con il codice IPA del ministero. Sono 2.661 CF ministeriali per
17 codici IPA (Carabinieri con la Difesa, Guardia di finanza con il MEF, Polizia con l'Interno) [V].
Il Ministero dell'università non ha un codice `m_*` nel file di IndicePA archiviato: resta scoperto.

**Confronto con l'abbinamento per nome** (CIG ICT S3-S6 2020-2026) [V]:

| esito | CIG | importo |
|---|---|---|
| stesso ministero | 10.609 | 4,86 mld |
| trovato solo per CF | 13.007 | 3,24 mld |
| trovato solo per nome | 121 | 68 M€ |
| ministero diverso | 28 | 58 M€ |

Il CF trova le SA il cui nome non dice il ministero (Stato maggiore, comandi di brigata, parchi
archeologici, direzioni generali, uffici giudiziari). I 121 «solo nome» sono uffici con CF non in
IndicePA (es. «Prefettura zona telecomunicazioni»).

**Quota annua.** Ogni CIG si distribuisce in modo uniforme dalla data di pubblicazione per la
`DURATA_PREVISTA` ANAC (troncata a 10 anni); la quota di un anno somma i CIG attivi in
quell'anno, pubblicati dal 2020. Limite [V]: **dal 2024 la durata manca nel 90 % dei CIG** (su un
file mensile 2024, 97.611 su 104.587 righe; nel 2022 lo 0,1 %), quindi per i contratti 2024-2025 la
quota coincide con l'importo intero e sovrastima la cassa dell'anno (R69).

**2024, per ministero** [V sui conteggi, **stima** sull'interpretazione]:

| Ministero | CIG ICT 2024 | Importo | Quota 2024 dei CIG attivi | Pagato ICT BDAP | Rapporto importo | Rapporto quota |
|---|---|---|---|---|---|---|
| Interno | 1.048 | 423 M€ | 498 M€ | 194 M€ | 2,2 | 2,6 |
| Difesa | 2.297 | 382 M€ | 434 M€ | 48 M€ | 8,0 | 9,1 |
| Giustizia | 359 | 213 M€ | 304 M€ | 315 M€ | 0,67 | **0,96** |
| Cultura | 898 | 161 M€ | 181 M€ | 16 M€ | 10,3 | 11,5 |
| Infrastrutture | 241 | 125 M€ | 154 M€ | 55 M€ | 2,3 | 2,8 |
| MEF | 375 | 77 M€ | 97 M€ | 388 M€ | 0,20 | **0,25** |
| Salute | 88 | 65 M€ | 95 M€ | 14 M€ | 4,6 | 6,6 |
| Lavoro | 35 | 37 M€ | 56 M€ | 23 M€ | 1,6 | 2,4 |
| Esteri | 168 | 11 M€ | 29 M€ | 28 M€ | 0,38 | 1,0 |
| Università | 0 | — | — | 10 M€ | — | — |

**Serie del rapporto quota/pagato** [V]: MEF 0,04 (2022), 0,08 (2023), 0,25 (2024), 0,36 (2025);
Giustizia 0,39, 0,54, 0,96, 1,17. La crescita dipende anche dal fatto che la serie dei CIG parte nel
2020: i contratti pluriennali più vecchi mancano nei primi anni.

Rapporti molto sopra 1 (Difesa, Cultura, Salute) non vogliono dire copertura: per CF entrano uffici
con bilancio proprio, che non pagano dal bilancio dello Stato (parchi archeologici e musei autonomi,
Agenzia industrie difesa), e acquisti pagati su gestionali non ICT; dal 2024 la durata mancante gonfia
la quota. Il segnale utile resta il rapporto **sotto 1**: oggi è solo il MEF.

### Sogei e contratti in-house (MEF, Giustizia)

Dallo stesso esito, campo `sogei` [V]:

- **Sogei aggiudicataria** (CF 02327910580 negli aggiudicatari ANAC): 26 CIG, di cui 20 con la riga nei file CIG; 19 di questi dal 2024 in
  poi, 14 «affidamento diretto a società in house» (gli altri: adesioni al PSN, acquisti di Consip). I più grandi sono delle agenzie fiscali,
  che non pagano dai gestionali ICT del MEF: Agenzia delle entrate 981 M€ (2024, sistema informativo
  della fiscalità), Dogane 381 M€ (2025), Entrate-Riscossione 298 M€ (2024), Demanio 30 M€. Con SA del
  MEF (per CF): Dipartimento delle finanze 77 M€ (2024, triennio 2024-2026), Giustizia tributaria 47
  M€ (2025), Guardia di finanza 4 M€ (2025). I contratti da 77 M€ in su stanno fra gli importi da
  verificare dell'imbuto (≥ 50 M€) e non entrano nei totali.
- **Quanto spiega del buco del MEF:** 2024, pagato 388 M€ contro una quota dei CIG attivi di 97 M€:
  mancano circa 290 M€. Il contratto del Dipartimento delle finanze, ripartito sul triennio, vale
  circa 26 M€ l'anno [stima]: meno di un decimo. Ragioneria, Tesoro e Amministrazione generale
  (NoiPA) non hanno contratti con Sogei che risultino in ANAC con un CIG [V sull'assenza nei dati].
- **Giustizia:** nessun CIG con Sogei. Il suo buco si chiude con l'abbinamento per CF (sopra).
- **Sogei stazione appaltante:** 69 CIG ICT nel 2024 per 466 M€; la quota 2024 dei suoi CIG attivi
  (pubblicati dal 2021) è di circa 693 M€ [V sui conteggi]. Sono gli acquisti che Sogei fa per tutti i
  suoi committenti: non si attribuiscono a un ministero dai dati ANAC, ma l'ordine di grandezza
  copre il buco del MEF. È la catena in-house: il MEF paga Sogei su un gestionale ICT senza CIG,
  Sogei compra sul mercato con un CIG proprio. Sommare le due cose sarebbe un **doppio conteggio**;
  separarle richiede i corrispettivi di Sogei per committente (R65).

## SIOPE via BDAP contro SIOPE diretto (#30, giro 0.3)

Verifica `tools/verifiche/siope_bdap_vs_diretto.py 2023|2024|2025` (0.2), esiti
`esiti/2026-11-09/siope/bdap-vs-diretto-<anno>.json`, elenco delle 60 risorse in
`esiti/2026-11-09/siope/risorse-bdap-siope-spesa.txt`. **Tutte le 20 regioni, 2023-2025**: file BDAP
«SIOPE Movimenti cumulati mensili di Spesa» archiviati il 9/11/2026 con `archivia.py` (pausa 5 s fra
le richieste); SIOPE diretto `SIOPE_USCITE.<anno>.zip` del 6/11/2026. BDAP non ha il codice ente
SIOPE né il CF: gli enti si abbinano per provincia, comune e nome (R70), a tre livelli (nome
identico; nome simile ≥ 0,90 nello stesso comune; comune BDAP con un solo «COMUNE DI» non abbinato
nello stesso comune). Cumulato dell'ultimo mese in BDAP contro somma dei mesi nel diretto [V]:

| | 2023 | 2024 | 2025 | 2025 senza Lombardia e FVG |
|---|---|---|---|---|
| enti BDAP / abbinati | 10.441 / 9.825 | 11.161 / 10.545 | 11.432 / 11.362 | |
| coppie ente × codice uguali (±1 €) | 99,9 % | 97,8 % | **86,0 %** | 99,2 % |
| totale BDAP / diretto (mld) | 509,63 / 509,63 | 545,63 / 552,97 (−1,3 %) | **510,40 / 593,04 (−13,9 %)** | 489,33 / 491,77 (−0,5 %) |
| **codici ICT** (U1030219, U2020107, U2020301): uguali | 100,0 % | 99,5 % | **88,9 %** | 99,8 % |
| codici ICT: totale BDAP / diretto (M€) | 1.854,33 / 1.854,35 | 2.180,27 / 2.180,75 | **1.998,14 / 2.410,04 (−17,1 %)** | 1.863,00 / 1.863,11 |
| comuni BDAP per ultimo mese | 7.902 a dicembre | 7.903 a dicembre | **1.717 a marzo**, 6.095 a dicembre | |
| comuni con movimenti nel diretto | 7.524 (anagrafica 2026) | 7.903 | 7.895, tutti a dicembre | |

**Il difetto riferito da AgID si riproduce, esattamente [V].** Nei file BDAP 2025 attuali:

- **Lombardia** (risorsa `54644001-abb4-4b21-ba8b-5a39622f6ecd`, sha256 `10e716cec0ff8ff6…`) e
  **Friuli-Venezia Giulia** (`1c572f0e-f80b-4ad7-902b-ebe492ec56dc`, sha256 `2daebadc70a1680e…`)
  contengono **solo i mesi 2025/01-2025/03**, per tutti gli enti (2.056 e 295): 1.502 + 215 =
  **1.717 comuni troncati a marzo**, il numero di AgID. In Lombardia BDAP somma 19,54 mld contro i
  92,67 del diretto; in FVG 1,53 contro 8,60. ICT: 124,7 contro 519,5 M€ (Lombardia), 10,5 contro
  27,4 (FVG).
- **Trentino-Alto Adige** (`e833081d-3f79-4d34-b921-6c38d956e4eb`, sha256 `aa875c9b89890e6c…`): 12
  mesi, ma solo **82 comuni della provincia di Trento**, contro 166 con movimenti 2025 nel diretto:
  **84 comuni assenti**, ancora il numero di AgID.
- Le altre 17 regioni 2025 e tutte le regioni 2023 e 2024 sono complete a dicembre [V].

Le due risorse difettose sono state caricate il **6/3/2026**, cinque giorni prima delle altre 18
(11/3/2026), con `metadata_modified` 11/3/2026 [V, dal catalogo `package_search` archiviato]: è un
caricamento parziale rimasto pubblicato, non un artefatto della cache di AgID. Gli identificativi di
risorsa sono quelli cablati da AgID in `etl/sources/siope.py` prima della migrazione (commit
`dce6351`, archiviato, sha256 `c0713419…`); il commento della versione attuale (commit `7f91f35`,
sha256 `b96c03f7…`) riferisce il difetto [R → ora V]. Il 9/11/2026, otto mesi dopo, il difetto è
ancora lì.

Le altre differenze sono pagamenti «da regolarizzare» (U0000099999) che BDAP mostra e il diretto ha
già attribuito ai codici veri, e voci di personale (2024, Lazio, Campania, Sicilia, Calabria): BDAP è
una fotografia meno aggiornata della stessa base. Gli enti non abbinati del 2023-2024 (circa 600)
sono soprattutto enti rinominati o fusi rispetto all'anagrafica SIOPE del 2026.

Conclusione per l'imbuto: dove BDAP è completo le due vie danno gli stessi importi ICT (99,5-100 %);
ma BDAP **non segnala** i file parziali (nessun campo, nessuna nota), e chi lo usa per il 2025 perde
412 M€ di spesa ICT dei comuni lombardi e friulani. Resta la fonte diretta, che ha il codice ente, il
CF e i 12 mesi (R75).

## Sanità

Nel Conto economico SSN 2023, livello nazionale [V]: **BA1620 servizi di assistenza informatica
604 M€**; BA0350 supporti informatici e cancelleria 109 M€ (mista, non separabile); BA1650 utenze
telefoniche 161 M€. Manutenzioni (BA1910 e seguenti) e noleggi (BA2010) non hanno una sotto-voce
ICT. Gli investimenti in hardware e software stanno nello stato patrimoniale, non nel CE. BA1620 è
quindi un **denominatore minimo** dei servizi ICT della sanità, per ente e per anno.

## Sanità, serie 2022-2024 (giro 0.4)

Voce BA1620, righe «999» (consolidato regionale = enti + gestione sanitaria accentrata «000»; sommare
tutte le righe conta due volte) [V]: 2022 530 M€, 2023 604 M€, 2024 720 M€. SIOPE, codice 3212
«assistenza informatica e manutenzione software» sugli enti sanitari, 2024: 674 M€ di cassa, il 94 %
del costo CE [V]. File: `datastore/dump/5afc4cf8-….csv` (2022), `57bb2cce-….csv` (2023),
`94083af2-….csv` (2024), sha256 in `esiti/2026-11-10/siope/ict-enti.json`. Mancano ancora in archivio
i CE trimestrali 2012-2025 (salvo IV 2025) e gli stati patrimoniali SSN, che per l'ICT non servono.

## Stato più territori: il totale pagato (giro 0.4)

| Anno | Stato (BDAP, gestionali ICT) | Enti non statali (SIOPE) | Totale | CIG ICT S3-S6 pubblicati |
|---|---:|---:|---:|---:|
| 2022 | 987 M€ | 2.993 | 3.980 | 9.470 |
| 2023 | 1.199 | 3.297 | 4.496 | 12.160 |
| 2024 | 1.141 | 3.975 | 5.116 | 14.024 |
| 2025 | 1.286 | 4.618 | 5.904 | 15.308 |

Telefonia esclusa (0,3-0,4 mld l'anno negli enti SIOPE). Dettaglio, avvertenze e abbinamento per
ente in [SIOPE](/progetto/siope/) [V].

## SIOPE via BDAP

Il file regionale (Lazio 2024, 435.707 righe) ha per ogni ente il codice gestionale e l'importo
**cumulato** mese per mese, con provincia, comune ISTAT, tipologia ente e popolazione [V]. Rispetto
alla fonte SIOPE diretta aggiunge l'anagrafica dell'ente, non nuovi importi [V sulla struttura;
importi uguali dove il file è completo, § SIOPE via BDAP contro SIOPE diretto, #30]. Per l'imbuto non serve: la fonte diretta resta
la via principale.

## Difetti noti

- **R61** [V]: `result.count` di `package_search` vale la dimensione della pagina, non il totale;
  pagine con offset alto in timeout a caso; metadati in repr Python invece che JSON.
- **R63** [V]: URL delle risorse in `http://` che non rispondono; CSV in Windows-1252 non dichiarato.
- **R64** [proposta]: i pagamenti per gestionale non hanno capitolo né CIG; il rendiconto per PG ha
  il capitolo ma non il gestionale. Non si può collegare un pagamento a un contratto.
- **R65** [proposta]: la spesa ICT fatta per trasferimento (ACN, AgID, fondo per l'innovazione, Sogei
  in-house, agenzie fiscali) non è marcata come ICT nel bilancio dello Stato.
- **R69** [V]: dal 2024 `DURATA_PREVISTA` manca nel 90 % dei CIG ANAC; senza durata un contratto
  pluriennale non si ripartisce sugli anni (richiesta ad ANAC).
- **R70** [V]: SIOPE via BDAP non ha il codice ente SIOPE né il codice fiscale: l'ente si riconosce
  solo per nome e comune (70 enti su 11.432 non abbinati nel 2025, circa 600 su 10-11 mila nel 2023-2024, con
  l'anagrafica SIOPE del 2026).
- **R75** [V]: SIOPE via BDAP 2025 parziale e non segnalato: Lombardia e Friuli-Venezia Giulia fermi a
  marzo (1.717 comuni), 84 comuni di Trento assenti; caricamento del 6/3/2026 ancora pubblicato il
  9/11/2026.
- **R71** [proposta]: i contratti in-house fra MEF (Ragioneria, Tesoro, Amministrazione generale) e
  Sogei non compaiono in ANAC con un CIG; quelli delle agenzie fiscali e del Dipartimento delle
  finanze sì, dal 2024.

## Cosa usiamo e cosa no

| Usiamo | Perché |
|---|---|
| Pagamenti con mandati informatici per gestionale, consuntivo | denominatore ICT dello Stato centrale per ministero e anno |
| Rendiconto per PG e capitolo | seconda via (CE3) per la controvalidazione; elenco dei capitoli ICT |
| CE SSN, voce BA1620 | denominatore minimo dei servizi ICT della sanità |

| Non usiamo | Perché |
|---|---|
| Leggi di bilancio, assestamenti, note di variazione | sono previsioni, non spesa |
| SIOPE via BDAP | stessi importi della fonte diretta sull'ICT dove è completo, ma il 2025 è parziale (Lombardia, FVG, Trento: R75) e non ha codice ente |
| Pagamenti mensili | il consuntivo li somma; i mensili servono solo a vedere la stagionalità |
| Spesa regionalizzata, dipendenti, mutui | nessun dettaglio ICT, fuori perimetro |

## Registro delle revisioni

| data | modifica |
|---|---|
| 2026-11-09 | prima versione: famiglie, campi, misure 2019-2025, copertura CIG per ministero, CE SSN, SIOPE via BDAP, R63-R65 |
| 2026-11-09 | 0.2: seconda via per PG 2019-2024 (discontinuità 2023); abbinamento SA→ministero per codice fiscale IndicePA (`bdap_cig_ministeri_cf.py`): Giustizia 0,96, MEF 0,25 nel 2024; quota annua dei CIG pluriennali e limite della durata mancante dal 2024; Sogei aggiudicataria e stazione appaltante; SIOPE via BDAP contro diretto 2024-2025 su cinque regioni (`siope_bdap_vs_diretto.py`, #30); R69-R71 |
| 2026-11-10 | 0.4: CE SSN 2022 e 2024 archiviati (BA1620 530/604/720 M€, righe 999); totale pagato Stato + SIOPE 2022-2025 (5,1 mld nel 2024) contro i CIG ICT; rimando alla pagina SIOPE (`siope_ict_enti.py`, #12); R83 |
| 2026-11-09 | 0.3: #30 chiuso. SIOPE via BDAP contro diretto su tutte le 20 regioni, 2023-2025 (60 file archiviati, `siope_bdap_vs_diretto.py` 0.2 con abbinamento a tre livelli): il difetto riferito da AgID **si riproduce** [R → V] — 2025 di Lombardia e FVG fermo a marzo (1.717 comuni), 84 comuni di Trento assenti; 2023 e 2024 completi; R75 |
