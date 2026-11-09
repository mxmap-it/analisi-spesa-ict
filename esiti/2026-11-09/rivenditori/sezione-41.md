## 2. Rivenditori dei prodotti cloud esteri (#41), v4 del 9/11/2026

Sezione scritta a parte per il rendiconto obiettivo 6 (da integrare alla prossima versione; non tocca la § #43).
Giurisdizione del **prodotto** da `config/marchi_cloud.yaml`; giurisdizione del **fornitore** dal capogruppo (GLEIF, o `config/rivenditori_capogruppo.yaml` con fonte per riga). Perimetro invariato rispetto alla v3.1: contratti attuativi 2022-2026, padri di AQ e importi da verificare esclusi, RTI ripartiti (alla mandataria se indicata, altrimenti in parti uguali).

Rifare (server, circa 6 minuti la prima volta, poi la cache GLEIF in `lavoro/rivenditori/`):
`nice .venv/bin/python tools/verifiche/rivenditori_mappa.py` → `esiti/2026-11-09/rivenditori/` (`mappa-v4.json`, `mappa-v4.csv` per rivenditore, `cig-rivenditore.csv` per CIG, `campione-precisione.csv`).

### 2.1 Quanto passa dai rivenditori [V]

| Prodotti extra-UE (2022-2026) | Importo | Quota sul totale | Quota sul noto |
|---|---|---|---|
| Totale | 2,949 mld | 100 % | |
| Canale noto (diretto + rivenditore) | 2,278 mld | 77,2 % | 100 % |
| Via rivenditore | 1,824 mld | 61,8 % | 80,1 % |
| … con CF italiano (**la lente fornitore li direbbe IT**) | **1,797 mld** | **60,9 %** | **78,9 %** |
| … CF italiano e capogruppo italiano (o capogruppo non trovato) | 1,658 mld | 56,2 % | 72,8 % |

Per capogruppo dei rivenditori con CF italiano: IT 1,464 mld; capogruppo non trovato («IT?») 0,194 mld; **CH 0,124 mld** (Fastweb → Swisscom 76 M€, SoftwareOne Italia → SoftwareOne Holding 48 M€); UE 11,5 M€ (es. Accenture → Accenture plc, IE); extra-UE 3,9 M€ (NTT Data Italia → NTT DATA, JP, riga curata [R]). CF assente 25,5 M€ (CIG con il solo nome, per intero o per qualche membro dell RTI), CF estero 0,9 M€.

Anche una lente fornitore che risale al capogruppo classificherebbe IT il **56 %** della spesa in prodotti extra-UE: il problema non è la nazionalità della controllante ma il canale di rivendita.

### 2.2 Chi vende cosa [V]

1.375 rivenditori (CF distinti o, senza CF, nome), 1.235 con prodotti extra-UE, su 6.470 CIG; i prodotti extra-UE via rivenditore vanno a **2.121 enti** (primi: INPS 96 M€, CRUI 80 M€, ANAS 61 M€, DTD Giustizia 54 M€, Sogei 51 M€, ACI Informatica 50 M€, ANCI 46 M€).

| Rivenditore (CF) | Capogruppo (paese, fonte) | Prodotti extra-UE | Principali marchi |
|---|---|---|---|
| TIM 00488410010 | TIM, nessuna controllante in GLEIF (IT) | 1.049 M€ | Microsoft, Salesforce, Oracle, Google, AWS |
| Fastweb 12878470157 | Swisscom AG (CH, GLEIF RR) | 76 M€ | AWS, IBM, Microsoft, Google |
| Eurolink 01973270604 | non trovato (nessun LEI) | 69 M€ | Oracle, AWS, Microsoft |
| SoftwareOne Italia 06169220966 | SoftwareOne Holding AG (CH, GLEIF RR) | 48 M€ | Microsoft |
| Var Group 03301640482 | Sesa (IT, GLEIF RR) | 43 M€ | Microsoft, Oracle, Salesforce |
| «IMPRESA INESISTENTE» 02102821002 | non trovato | 42 M€ | Oracle, Microsoft (R56) |
| Italware 08619670584 | Digital Value (IT, GLEIF RR) | 33 M€ | Oracle, IBM |
| Project Informatica 02006010165 | nessuna controllante (IT) | 31 M€ | Oracle, Microsoft |
| R1 05231661009 (+ Gway, controllata) | nessuna controllante (IT) | 23 + 16 M€ | Oracle, Microsoft |
| Postel (3 CF/nomi) | Poste Italiane (IT, curato [R]) | 45 M€ | Microsoft |

Tabella completa: `mappa-v4.csv` (per riga: CF, capogruppo, paese, fonte del capogruppo, CIG, euro, enti, marchio:giurisdizione=euro, primi 5 enti, fonte del CF).

### 2.3 Fonti nuove usate e loro resa [V]

- **Codici fiscali**: dataset ANAC aggiudicatari per 4.773 CIG; per i **1.530 CIG senza righe** (i «0,41 mld» del punto aperto 2 della 0.5) il CF si ricava dal nome con il dizionario nome → CF dello stesso dataset (accettato solo se un CF copre ≥ 90 % delle occorrenze): 405,5 M€ di prodotti extra-UE ora hanno un CF. Restano 167 CIG solo col nome (8,6 M€ extra-UE).
- **Vincitori TED** (`ted-vincitori.csv`, `ted-esiti.csv`) come seconda fonte: **0 CIG** in comune con il canale rivenditore senza ANAC (riguardano CIG senza provider attribuito). Restano utili per l'imbuto, non per questa mappa.
- **GLEIF** (golden copy 6/11/2026, LEI2 + RR del mirror): 249.738 identificativi italiani con LEI; capogruppo da GLEIF per 1,540 mld su 1,824 (84 %), da righe curate 63 M€ (6 righe, tutte [R]), non trovato 194 M€.
- **Convenzioni**: i 48 CIG attuativi dei lotti Consip con aggiudicatario dichiarato in `config/lotti_cloud.yaml` hanno lo stesso rivenditore nei dati ANAC: **48/48**.
- **Atti #57** (`dati/atti/`): dei 6.470 CIG via rivenditore solo **45** hanno un atto archiviato, e solo **8** di questi citano il CIG (gli altri sono pagine generiche di portale). Negli 8 pertinenti il prodotto c'è 8/8, il nome o la P.IVA del rivenditore 4/8 (ricerca testuale).

### 2.4 Precisione su campione [V, con limiti]

Campione: tutti i 45 CIG via rivenditore con atto archiviato (seme 20261109, nessuna estrazione: sono tutti). Etichette a mano in `report/metodo/rivenditori-v4/etichette-campione.csv`: atto quando pertinente (9), altrimenti oggetto ANAC (36). Domanda: il prodotto attribuito è quello comprato?

| | CIG | € |
|---|---|---|
| Corretto | 30 | 13,1 M€ |
| Errato | 9 | 1,7 M€ |
| Incerto | 6 | 1,5 M€ |
| **Precisione** | **30/39 = 77 %** (Wilson 62-87 %); 67 % se gli incerti fossero errori | **88 %** sui decisi |

Gli errori sono tutti falsi positivi della lente prodotto in gare non ICT o con oggetti misti (antisettici → AWS e Microsoft; reti idriche → AWS ×2; dispositivi cardiaci → Microsoft; hardware di rete, museo, software gestionale → PSN). Vanno come casi in `tests/casi_classifica.yaml` alla prossima revisione delle regole (#40, non toccata qui). Sul rivenditore i riscontri sono 48/48 lotti Consip coincidenti e 4/8 atti pertinenti che lo nominano (negli altri 4 il nome non compare nel testo estratto): nessun caso contrario trovato, ma la prova sugli atti è debole.

Limiti: il campione non è casuale (dipende da quali CIG avevano atti); la fonte primaria copre 9 CIG su 45; un solo etichettatore (Claude), non a cieco rispetto all'uscita. Su 2,95 mld la precisione del 77 % per CIG va letta come indicazione, non come correzione da applicare.

### 2.5 Raccomandazioni

R76 (ANAC: aggiudicatari senza righe e marchio del prodotto rivenduto) e R77 (capogruppo dei fornitori: LEI e relazioni di controllo) in `report/metodo/richieste-e-raccomandazioni.yaml`.

### 2.6 Prossimi passi

1. Atti pertinenti per i primi 20 rivenditori (TIM-Microsoft EA in testa): un campione casuale con atti, non di comodo.
2. Capogruppo delle 6 righe [R] e di Eurolink, Arslogica, «IMPRESA INESISTENTE» da visura o bilancio.
3. I 9 falsi positivi come casi di test della lente (#40).

## 2bis. Aggiornamento v4.1 (9/11/2026, pomeriggio)

Rifare: `nice .venv/bin/python tools/verifiche/rivenditori_mappa.py v4.1` (riclassifica ogni riga dei file di attribuzione con le regole **correnti** di `tools/analisi/classifica.py`; `v4` = provider congelato al 28/10, `v4.1-prima` = regole correnti prima della correzione qui sotto). Uscite `*-v4.1.*` e `*-v4.1-prima.*` in `esiti/2026-11-09/rivenditori/`.

### 2bis.1 Correzione delle regole (#40) [V]

I 9 falsi positivi del campione v4 sono casi di test in `tests/casi_classifica.yaml` (76/76 superati). Cause e correzioni:

| CIG | Errore | Causa | Correzione |
|---|---|---|---|
| A028289D6D, A0282C0AD1 | antisettici → AWS, Microsoft | via 2: «2746» trovato dentro «GARA ANAC 91**2746**2» | `RX_AQ2746` vuole il numero a sé e un contesto cloud/Consip/AQ (`RX_CONTESTO_AQ`) |
| 9867759C52, 9886177B56 | reti idriche → AWS | idem dentro «ACTC2**2746**4» | idem |
| 9134580DDE | pacemaker «AZURE S DR» → Microsoft | marchio omonimo | esclusione in `config/marchi_cloud.yaml` |
| B374A4175C | 150 licenze «Microsoft Business 365 … nel PSN» → PSN | il marchio Microsoft non riconosciuto, vinceva PSN | regex `microsoft (business\|office) 365`: ora Microsoft (giusto) |
| A069537FBA | «hardware speciale rete PSN» → PSN | rete, non servizio | esclusione `hardware … rete psn` |
| B2764FE7BE | affiancamento e spostamento contenuti su PSN | servizio professionale | `affiancamento` fra i servizi professionali (esce dalla spesa in abbonamento) |
| BC1296935C | licenza Microsoft SQL Server dentro una manutenzione | **etichetta sbagliata** (il prodotto c'è) | nessuna: etichetta corretta in `etichette-campione-v4.1.csv`, caso di test che fissa il comportamento |

Nessuna regressione sui tre campioni a cieco esistenti (`lente_cieco.py`, prima e dopo in `esiti/2026-11-09/rivenditori/lente-prima|dopo/`): big tech P/R e tutti i provider P/R **identici** prima e dopo (cieco 1: big tech 66/0/1 TP/FP/FN; cieco 2: 62/0/1; cieco 3: 62/0/8). Le regole toccate non compaiono in quei 600 CIG: la correzione non migliora né peggiora la misura a cieco.

Effetto sulla mappa (v4.1-prima → v4.1): −26 CIG attribuiti, −3,5 M€ di prodotti extra-UE (3,069 → 3,065 mld), −2,9 M€ via rivenditore. Piccolo in euro, ma toglie errori grossolani.

### 2bis.2 Numeri v4.1 [V]

| Prodotti extra-UE | v4 (regole 28/10) | v4.1 (regole correnti) |
|---|---|---|
| Totale | 2,949 mld | 3,065 mld |
| Via rivenditore | 1,824 mld | 1,911 mld |
| Via rivenditore con CF italiano | 1,797 mld | **1,884 mld** |
| … sul totale / sul noto | 60,9 % / 78,9 % | **61,5 % / 79,3 %** |
| … CF IT e capogruppo IT o non trovato, sul totale | 56,2 % | 56,9 % |

La crescita v4 → v4.1 (+116 M€ di totale) viene dalle regole aggiunte dopo il 28/10 (#40, v0.3-v0.5), non da questa correzione. 1.393 rivenditori, 6.611 CIG. Capogruppo: GLEIF 1,669 mld, curato 63 M€, non trovato 152 M€ (era 194: Italware, sotto).

### 2bis.3 Campione casuale sui primi 20 rivenditori [V]

60 CIG di prodotti extra-UE, 3 per ciascuno dei primi 20 rivenditori per importo extra-UE, estratti con seme 20261109 fra **tutti** i loro CIG (`campione-top20-v4.1.csv`, etichette `report/metodo/rivenditori-v4/etichette-top20.csv`). Nessuno dei 60 ha un atto archiviato pertinente: le etichette vengono dall'oggetto ANAC.

| | CIG | € |
|---|---|---|
| Prodotto corretto | 58 | 51,3 M€ |
| Errato | 2 | 16,0 M€ |
| **Precisione** | **58/60 = 96,7 %** (Wilson 88,6-99,1 %) | **76,2 %** |

I 2 errori: CRUI 92870750BD (16 M€, Maticmind): gara multi-lotto, il lotto 1 sono licenze Cisco ma il testo della procedura nomina IBM Cloud dei lotti 3-4 (classe nuova: **marchio di un altro lotto**); B273B14113 (Maticmind): Check Point «Harmony Email and Office365 Protection», marchio come oggetto di un prodotto di terzi. Un solo CIG da 16 M€ pesa per un quarto degli euro del campione: la precisione in euro ha varianza alta. Il campione v4 di comodo (45 CIG con atti), dopo la correzione, dà 32/32 decisi e 6 incerti, ma è il campione su cui le regole sono state corrette: non vale come misura.

### 2bis.4 Eurolink, Arslogica, «IMPRESA INESISTENTE» [V]

Fonti: dataset ANAC aggiudicatari (denominazioni per CF), CIG e padri di AQ, GLEIF (nessun LEI per i tre), **VIES** della Commissione europea (servizio pubblico gratuito, senza login; risposte del 9/11/2026 archiviate in `report/metodo/rivenditori-v4/vies/` con `SHA256SUMS`).

- **«IMPRESA INESISTENTE» (02102821002) è Italware S.r.l.** VIES: P.IVA valida, «ITALWARE - S.R.L.», via della Magliana­nella 65/E, Roma. Indizi concordi in ANAC: 1.520 CIG con quel CF, 1.516 righe «IMPRESA INESISTENTE» e 4 «ITALWARE»; dei 473 CIG derivati da AQ, **398** hanno il padre aggiudicato a Italware (Licenze software multibrand e simili). Il CF 08619670584, quello con LEI (capogruppo Digital Value S.p.A., GLEIF RR), non è una P.IVA valida in VIES: è il codice fiscale della stessa società. In v4.1 i due identificativi sono uniti (`stesso_soggetto` in `config/rivenditori_capogruppo.yaml`, stato V): **Italware sale a 74,5 M€ di prodotti extra-UE, terzo rivenditore dopo TIM e Fastweb**, 82 CIG, 49 enti, capogruppo Digital Value (IT). R56 va aggiornata: il segnaposto copre la P.IVA di un'impresa reale e attiva.
- **Eurolink S.r.l. (01973270604)**: P.IVA valida (VIES), Roma, via di Tor Pagnotta 86; 110 CIG in ANAC sempre con la stessa denominazione; rivenditore Oracle dei grandi enti centrali (Consip, Sogei, INAIL, IPZS, ANAS, DTD Giustizia), indicata in ANAC come aggiudicataria del lotto Oracle di Licenze software multibrand 6 (ID 2599) e di forniture Oracle SaaS. Nessun LEI: capogruppo non ricavabile da fonti gratuite (resta «IT?»).
- **Arslogica Sistemi S.r.l. (04108030281)**: P.IVA valida (VIES), Padova; 255 CIG; rivenditore Oracle (licenze, Exadata, Oracle Cloud IaaS/PaaS e SaaS) soprattutto per sanità veneta e lombarda e per Informatica Alto Adige. Nessun LEI: capogruppo non ricavabile da fonti gratuite.

Primi rivenditori di prodotti extra-UE in v4.1: TIM 1.133 M€, Fastweb 76,1 M€ (capogruppo Swisscom, CH), **Italware 74,5 M€**, Eurolink 69,1 M€, SoftwareOne 47,7 M€ (CH), Var Group 42,8 M€, Project Informatica 30,9 M€, R1 24,3 M€, Informatica Alto Adige 20,6 M€.

### 2bis.5 Prossimi passi

1. Classe «marchio di un altro lotto» (gare multi-lotto con testo della procedura): regola da scrivere e misurare (#40).
2. Atti pertinenti per i 60 CIG del campione top-20 (oggi 0).
3. Capogruppo di Eurolink e Arslogica e verifica delle 6 righe [R]: solo con fonti gratuite (bilanci depositati pubblicati dalle società, siti istituzionali).
