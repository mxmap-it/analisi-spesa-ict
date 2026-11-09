---
title: "Obiettivo 6: prodotti, rivenditori, PNRR, PSN"
subtitle: "Lente prodotto misurata sul campione, chi rivende i prodotti esteri, quota big tech nei contratti PNRR, catalogo ACN"
date: 2026-11-06
lastmod: 2026-11-09
datiAl: 2026-10-28
description: "Precisione e richiamo del dizionario dei marchi cloud sul campione di 611 CIG; quota della spesa in prodotti extra-UE intermediata da rivenditori; quota dei prodotti delle big tech USA nei contratti collegati alle Misure PNRR 1.1 e 1.2; stato del catalogo ACN dei servizi qualificati."
sitemap:
  disable: true
build:
  list: never
---

**Versione 0.8 del 2026-11-09 · BOZZA non annunciata: la pubblicazione la decide Fabio Pietrosanti** · ticket [#40](https://github.com/mxmap-it/analisi-spesa-ict/issues/40), [#41](https://github.com/mxmap-it/analisi-spesa-ict/issues/41), [#43](https://github.com/mxmap-it/analisi-spesa-ict/issues/43), [#45](https://github.com/mxmap-it/analisi-spesa-ict/issues/45), parte di [#24](https://github.com/mxmap-it/analisi-spesa-ict/issues/24)

Legenda: **[V]** misurato da noi, con il comando per rifarlo; **[R]** riferito da terzi, non verificato. La giurisdizione è quella del **prodotto** ([metodo](/progetto/metodo-cloud-provider/)).

## 1. Lente prodotto (#40)

Dizionario: `config/marchi_cloud.yaml` (regex ed esclusioni, vie 3), con la fonte della giurisdizione di ogni provider in `config/marchi_cloud_fonti.yaml` (capogruppo e sede; tutte [R] tranne PSN, SPC Cloud e in-house). Misura sul campione v3 di 611 CIG (riferimento: via 6 con atti e revisione, `dati/classificazioni/campione-v3.jsonl`), guardando **solo il testo della gara** [V]:

| Insieme | Precisione | Richiamo |
|---|---|---|
| Prodotti big tech USA (Microsoft, AWS, Google, Oracle, IBM, Salesforce, ServiceNow, Adobe, VMware, Cisco, Zoom, Cloudera) | 168/175 = **96 %** (92-98) | 168/186 = **90 %** (85-94) |
| Tutti i provider del dizionario, provider esatto | 286/336 = 85 % (81-89) | 286/455 = 63 % (58-67) |

Intervalli di Wilson al 95 %. Per provider: Microsoft 97 % / 94 %, VMware 95 % / 100 %, Oracle 100 % / 83 %, SAP 100 % / 74 %, PSN 84 % / 97 %. Il richiamo complessivo basso viene da TIM (0/62), Fastweb (0/15) e in-house (27/84): il riferimento li attribuisce dal fornitore o dagli atti, non dal testo; per la lente prodotto non è un errore ma il limite atteso. **Menzioni in negativo** («migrazione da», «in sostituzione», «dismissione»): 0 falsi positivi su 50.

Limiti: il campione è stratificato, non casuale; il riferimento è stato prodotto anche guardando le vie 3 (possibile circolarità, che gonfia la precisione); per una misura indipendente serve un campione nuovo etichettato a cieco.

Rifare: `python tools/verifiche/lente_prodotto.py` → `esiti/2026-11-06/lente-prodotto/` (errori uno per uno in `errori.csv`).

### 1.1 Campione nuovo a cieco (v0.2)

Per togliere la circolarità: 240 CIG estratti a caso, 40 per ciascuno dei 6 strati dell'imbuto (S0, S2, S3, S4, S5, S6) dal 2024, esclusi i 611 del v3. Il seme è 20261106 (`report/metodo/lente-cieco/disegno.json`). Le etichette sono date leggendo il solo oggetto, senza vedere l'uscita della lente (`etichette.csv`; una riga corretta dopo per un'omissione di trascrizione, annotata). Il riferimento dice **quale prodotto nomina il testo**, non quale prodotto è stato comprato: gli atti non sono stati aperti [V].

| Insieme | Precisione (campione) | Richiamo (campione) | Pesato sull'universo (P / R) |
|---|---|---|---|
| Big tech USA | 54/54 = **100 %** (93-100) | 54/67 = **81 %** (70-88) | 100 % / 94 % |
| Tutti i provider | 64/65 = 98 % (92-100) | 64/80 = 80 % (70-87) | 99 % / 59 % |

- **Mancati** (13 big tech, tutti in S3): sigle delle convenzioni Consip Microsoft (MS EA8, EA9, «Consip Microsoft Agreement»), «Win 10», «licenze SQL - Teams», adesioni all'AQ IaaS/PaaS 2746 con il marchio ma senza lotto. Nell'imbuto questi CIG sono già presi da altre vie (lotto, convenzione), ma la lente da sola li perde.
- **Regole applicate (v0.3).** La via 6 non legge `config/marchi_cloud.yaml` (verificato in `tools/llm/`), quindi le regole sono nel dizionario, con commento e riga nel [metodo](/progetto/metodo-cloud-provider/):
  - aggiunte: sigle MS EA8/EA9, `consip microsoft`, licenze SQL, licenze ed ESU di Windows 10/11, IaaS/PaaS Google e Microsoft;
  - scartata «win 10/11» da sola: sull'universo dal 2024 prendeva 242 CIG di PC con Windows preinstallato;
  - effetto: circa 40 CIG in più sull'universo dal 2024, controllati su un estratto;
  - campione v3 invariato (96 % / 90 %);
  - sul campione a cieco il richiamo big tech sale a 66/67 (98 %), ma è una misura sullo stesso campione usato per scrivere le regole: **non vale come misura**, e il campione diventa di sviluppo. La misura indipendente resta 81 %.
- **Sottocampione sugli atti (v0.3):** 9 CIG positivi con link PVL più specifico (pagine di dettaglio dei portali), scaricati con `tools/llm/atti.py`:
  - 1 atto pertinente (B96E3295BB, licenze Microsoft VDA, R1 S.p.A.): conferma l'etichetta;
  - 2 pagine generiche dei portali, senza il CIG;
  - 6 non trovati o illeggibili.
  Resa 1/9, come nei giri precedenti (R53, R54): fermato. Il confronto «prodotto nominato contro prodotto comprato» resta senza misura.
- Il richiamo pesato di tutti i provider (59 %) è basso per gli strati S2: Aruba firma digitale, in-house Lepida, Google nominato come piattaforma di un SaaS italiano. Gli strati S0 e S5 (315 mila CIG) hanno 0 menzioni su 80, quindi la stima pesata è molto incerta.

Rifare: `python tools/verifiche/lente_cieco.py` → `esiti/2026-11-06/lente-prodotto/lente-cieco.json`.

### 1.2 Secondo campione a cieco: misura delle regole v0.3 (v0.4)

- **Disegno:** 120 CIG nuovi, 40 per strato S2, S3, S4 (dove stanno i prodotti), seme 20261107, esclusi il v3 e il primo campione (`report/metodo/lente-cieco-2/`). Etichette sul solo oggetto, senza vedere la lente. Le regole v0.3 erano già nel dizionario, ma il campione non è stato usato per scriverle.
- **Correzioni dopo la misura:** 3 etichette di provider non big tech (Cloud Toscana, Lepida, Nextcloud), perché il nome stava oltre i 170 caratteri letti in etichettatura (la lente ne legge 400). Sono annotate nel file e non toccano i numeri big tech.

| Insieme | Precisione | Richiamo | Pesato su S2-S4 (P / R) |
|---|---|---|---|
| Big tech USA | 56/59 = **95 %** (86-98) | 56/63 = **89 %** (79-95) | 90 % / 95 % |
| Tutti i provider | 63/67 = 94 % (86-98) | 63/70 = 90 % (81-95) | 89 % / 96 % |

- **Falsi positivi big tech** (3): un servizio di backup *di* Microsoft 365, una collocation al punto di interscambio AWS, un corso di formazione «AWS Cloud Architect». Il marchio è nominato come oggetto, non come prodotto comprato: servono regole di esclusione per formazione, backup e collocation.
- **Mancati** (7, tutti Microsoft): «Consip Enterprise 9» senza la parola Microsoft, «licenze MS CP-PILOT», «software assurance Microsoft», «Windows XP», «licenze d'uso enterprise agreement di software Microsoft», «prodotti e servizi Microsoft», PC «con licenze Office».
- **Non applicate:** le regole per questi errori le scriverei guardando questo campione, che diventerebbe a sua volta di sviluppo. Il richiamo misurato senza circolarità è quindi **89 %** (primo campione a cieco: 81 %, prima delle regole v0.3).

Rifare: `python tools/verifiche/lente_cieco.py report/metodo/lente-cieco-2`.

### 1.3 Regole correttive e terzo campione a cieco (v0.5)

- **Regole applicate** in `config/marchi_cloud.yaml`, dagli errori del secondo campione:
  - esclusioni: AWS in corsi, formazione, collocation e punto di interscambio; backup *di* Microsoft 365;
  - Microsoft licenza: «licenze/subscription/software assurance/enterprise agreement … Microsoft» nei due ordini, «Consip Enterprise N», «MS Copilot», «Windows XP», licenze Office con versione o edizione.
- **Effetto sull'universo dal 2024**, controllato a mano su un estratto: 79 + 37 + 4 + 2 + 1 CIG nuovi. Scartata «licenze … office» generica: prendeva 254 CIG, fra cui Solibri Office.
- **Terzo campione a cieco:** 120 CIG nuovi, S2-S4, seme 20261108, esclusi i campioni precedenti (`report/metodo/lente-cieco-3/`). Etichette sui primi 260 caratteri dell'oggetto, senza vedere la lente.

| Insieme | Precisione | Richiamo | Pesato su S2-S4 (P / R) |
|---|---|---|---|
| Big tech USA | 62/62 = **100 %** (94-100) | 62/70 = **89 %** (79-94) | 100 % / 98 % |
| Tutti i provider | 69/71 = 97 % (90-99) | 69/79 = 87 % (78-93) | 95 % / 94 % |

- **Gli 8 mancati big tech** sono testi che non nominano il produttore o lo scrivono male: «licenze server Windows», «licenze Office» senza versione, «licenze Copilot», «MIRCOSOFT», «enterprice agreement», «licenze Dynamics», «MySQL» (Oracle).
- Dai tre campioni il richiamo indipendente si assesta fra 81 % e 89 %, la precisione fra 95 % e 100 %. Per il resto servono gli atti o una via diversa dal testo: lotti, convenzioni, fornitore.
- Le regole per questi 8 non sono applicate: si misurerebbero solo su un quarto campione.

Rifare: `python tools/verifiche/lente_cieco.py report/metodo/lente-cieco-3`.

## 2. Rivenditori dei prodotti esteri (#41)

### 2.1 Mappa v4.2 (v0.8): chi rivende cosa, a chi, con quale capogruppo

Per ogni rivenditore (CF/P.IVA): capogruppo e suo paese, prodotti cloud venduti (marchio → giurisdizione del **prodotto**, `config/marchi_cloud.yaml`), CIG, euro, enti. Stesso perimetro della v3.1 (contratti attuativi 2022-2026, padri di AQ e importi da verificare esclusi, RTI alla mandataria o in parti uguali), ma ogni riga è riclassificata con le regole **correnti** della lente (comprese le correzioni del § 2.3).

Rifare (server; circa 6 minuti, cache GLEIF in `lavoro/rivenditori/`): `nice .venv/bin/python tools/verifiche/rivenditori_mappa.py v4.2` → `esiti/2026-11-09/rivenditori/` (`mappa-v4.2.json`; `mappa-v4.2.csv` per rivenditore, con la fonte del capogruppo; `cig-rivenditore-v4.2.csv` per CIG). Con l'argomento `v4` si ottiene la mappa con il provider congelato al 28/10.

| Prodotti extra-UE [V] | v4 (regole 28/10) | v4.2 (regole correnti) |
|---|---|---|
| Totale | 2,949 mld | 3,024 mld |
| Canale noto (diretto + rivenditore) | 2,278 mld | 2,336 mld |
| Via rivenditore | 1,824 mld | 1,870 mld |
| Via rivenditore con **CF italiano** (la lente fornitore li direbbe IT) | 1,797 mld | **1,844 mld** |
| … sul totale / sul noto | 60,9 % / 78,9 % | **61,0 % / 78,9 %** |
| … CF italiano e capogruppo italiano o non trovato, sul totale | 56,2 % | 57,2 % |

- **La lente fornitore sbaglia sei euro su dieci** della spesa in prodotti extra-UE. Anche risalendo al capogruppo il 57 % resta IT: il problema è il canale di rivendita, non la proprietà del rivenditore [V].
- Capogruppo dei rivenditori con CF italiano: IT 1,577 mld; non trovato 0,152 mld; **CH 0,099 mld** (Fastweb → Swisscom 51 M€, SoftwareOne Italia → SoftwareOne Holding 48 M€); UE 11,5 M€ (es. Accenture → Accenture plc, IE); extra-UE 3,9 M€ (NTT Data Italia → NTT DATA, JP, riga curata [R]). CF assente 25,9 M€, CF estero 1,0 M€ [V].
- 1.394 rivenditori, 1.257 con prodotti extra-UE, 6.609 CIG; i prodotti extra-UE rivenduti vanno a **2.182 enti** (primi: INPS 96 M€, ANAS 61 M€, ACI Informatica 55 M€, DTD Giustizia 54 M€, Sogei 51 M€) [V].

| Rivenditore (CF) | Capogruppo (paese, fonte) | Prodotti extra-UE | Marchi principali |
|---|---|---|---|
| TIM 00488410010 | nessuna controllante in GLEIF (IT) | 1.133 M€ | Microsoft, Salesforce, Cloudera, Oracle |
| Italware 08619670584 / 02102821002 (§ 2.4) | Digital Value (IT, GLEIF) | 74,5 M€ | Oracle, Microsoft, IBM |
| Eurolink 01973270604 | non trovato (nessun LEI) | 69,1 M€ | Oracle, Microsoft |
| Fastweb 12878470157 | Swisscom AG (CH, GLEIF) | 51,1 M€ | AWS, Microsoft, Google |
| SoftwareOne Italia 06169220966 | SoftwareOne Holding AG (CH, GLEIF) | 47,7 M€ | Microsoft |
| Var Group 03301640482 | Sesa (IT, GLEIF) | 42,8 M€ | Microsoft, Oracle, Salesforce, AWS |
| Project Informatica 02006010165 | nessuna controllante (IT) | 30,9 M€ | Oracle, Microsoft |
| R1 05231661009 | nessuna controllante (IT) | 24,3 M€ | Oracle, Microsoft, AWS |
| Postel (3 CF/nomi) | Poste Italiane (IT, curato [R]) | 45 M€ in tutto | Microsoft (Azure, licenze) |

### 2.2 Fonti nuove e loro resa (v0.8) [V]

- **CF dei 1.530 CIG senza righe nel dataset aggiudicatari** (il punto aperto della 0.5): ricavati dal nome con il dizionario nome → CF dello stesso dataset, accettato solo se un CF copre ≥ 90 % delle occorrenze. Hanno ora un CF 425 M€ di prodotti extra-UE; restano 9,0 M€ con il solo nome.
- **Vincitori TED** come seconda fonte: 0 CIG utili in questo canale (servono all'imbuto, non qui).
- **GLEIF** (golden copy 6/11/2026, LEI2 + RR del mirror): 249.738 identificativi italiani con LEI. Il capogruppo viene da GLEIF per 1,628 mld su 1,870, da `config/rivenditori_capogruppo.yaml` per 63 M€ (6 righe [R] con fonte per riga, 1 [V]); non trovato per 152 M€.
- **Convenzioni Consip**: nei 48 CIG dei lotti con aggiudicatario dichiarato (`config/lotti_cloud.yaml`) il rivenditore ANAC coincide in **48/48**.
- **Atti (#57)**: solo 45 CIG via rivenditore hanno un atto archiviato, e solo 8 citano il CIG. In questi 8 il prodotto c'è sempre (8/8); il rivenditore è nominato in 4/8.

### 2.3 Precisione del prodotto nel canale rivenditore e correzioni della lente (#40)

**Campione casuale (v0.8)**: 60 CIG di prodotti extra-UE, tre per ciascuno dei primi 20 rivenditori, estratti con seme 20261109 fra **tutti** i loro CIG (`esiti/2026-11-09/rivenditori/campione-top20-v4.1.csv`; etichette in `report/metodo/rivenditori-v4/etichette-top20.csv`, date sull'oggetto ANAC perché nessuno dei 60 ha un atto pertinente archiviato). Un solo etichettatore (Claude), non a cieco rispetto all'uscita [V, con questo limite].

| Regole | Prodotto corretto | Precisione | In euro |
|---|---|---|---|
| v4.1 (prima) | 58/60 | **96,7 %** (Wilson 88,6-99,1 %) | 76,2 % |
| v4.2 (dopo) | 58/58 attribuiti; i 2 errori tolti, nessun giusto perso | 100 % sul campione usato per correggere le regole: non è una misura indipendente | 100 % |

Misura prima/dopo: `python tools/verifiche/lente_top20.py <etichetta>` → `esiti/2026-11-09/rivenditori/lente-top20-*.json`.

**Correzioni della lente**, ognuna con un caso in `tests/casi_classifica.yaml` (81/81 superati):

| Errore | Esempio | Correzione |
|---|---|---|
| Numero dell'AQ dentro altri numeri | «2746» in «GARA ANAC 9127462» e «ACTC227464»: antisettici e reti idriche attribuiti ad AWS e Microsoft | via 2: numero a sé e contesto cloud/Consip/AQ |
| Omonimi | pacemaker Medtronic «AZURE S DR» | esclusione |
| Rete, non servizio | «hardware speciale rete PSN» | esclusione |
| Marchio non riconosciuto | «licenze Microsoft Business 365 … nel PSN» attribuito al PSN | regex `microsoft (business/office) 365` |
| Servizio professionale | «affiancamento … spostamento contenuti su PSN» | «affiancamento» fra i servizi professionali |
| **Marchio di un altro lotto** | CRUI 92870750BD, 16 M€: lotto Cisco attribuito a IBM Cloud perché la gara nomina IBM Cloud nei lotti 3-4; 9287118438, 25 M€: lotto Dell APEX attribuito a IBM | se il testo è «oggetto del lotto · oggetto della gara» e la gara elenca più lotti, il marchio si cerca solo nell'oggetto del lotto |
| **Prodotto di terzi col nome del marchio** | Check Point «Harmony Email and Office365 Protection» | esclusione |
| Esclusione troppo larga | CRUI 93147506DD, 15 M€: «servizi cloud AWS, servizi professionali e formazione» escluso come corso | la formazione esclude AWS solo se il testo non compra anche servizi cloud |

Un'etichetta del campione v4 era sbagliata (BC1296935C comprende davvero una licenza Microsoft SQL Server): corretta in `etichette-campione-v4.1.csv`.

**Nessuna regressione sui tre campioni a cieco** (`lente_cieco.py`; esiti in `esiti/2026-11-09/rivenditori/lente-prima/`, `lente-dopo/`, `lente-dopo-multilotto/`): big tech TP/FP/FN 66/0/1, 62/0/1 e 62/0/8, tutti i provider 76/1/4, 69/1/1 e 69/2/10, **identici** prima e dopo. Le regole nuove non toccano quei 600 CIG: non migliorano né peggiorano la misura a cieco [V].

Effetto sulla mappa [V]: le correzioni dei 9 falsi positivi tolgono 26 CIG e 3,5 M€ di prodotti extra-UE; quelle per multi-lotto e prodotti di terzi tolgono altri 41 M€ (Dell APEX 25 M€, Cisco 16 M€, apparati di rete Cisco/Aruba, Check Point) e tengono l'AWS di CRUI (15 M€, prima attribuito per errore a Oracle). La crescita da 2,949 a 3,024 mld rispetto alla v4 viene dalle regole aggiunte dopo il 28/10 (§ 1.2-1.3), non da queste.

Il campione v4 di comodo (45 CIG con atti, `etichette-campione*.csv`) dava 30/39 = 77 % con le regole del 28/10. È il campione su cui sono state scritte le correzioni e non vale più come misura.

### 2.4 Chi sono «IMPRESA INESISTENTE», Eurolink e Arslogica (v0.8) [V]

Fonti gratuite e senza login: dataset ANAC aggiudicatari e CIG, GLEIF, **VIES** della Commissione europea (risposte del 9/11/2026 archiviate in `report/metodo/rivenditori-v4/vies/` con `SHA256SUMS`).

- **«IMPRESA INESISTENTE» (02102821002) è Italware S.r.l.** Per VIES la P.IVA è valida e intestata a «ITALWARE - S.R.L.», Roma. In ANAC quel CF ha 1.520 CIG: 1.516 righe «IMPRESA INESISTENTE», 4 «ITALWARE»; dei 473 CIG derivati da AQ, 398 hanno il padre aggiudicato a Italware. Il CF 08619670584 (LEI GLEIF, capogruppo Digital Value S.p.A.) non è una P.IVA in VIES: è il codice fiscale della stessa società. In ANAC la società ha quindi due identificativi, uno col nome segnaposto. Uniti (`stesso_soggetto` in `config/rivenditori_capogruppo.yaml`, stato V), Italware è il **2° rivenditore di prodotti extra-UE** (74,5 M€, 82 CIG, 49 enti). R56 aggiornata.
- **Eurolink S.r.l. (01973270604)**: P.IVA valida (VIES), Roma; 110 CIG sempre con la stessa denominazione; rivenditore Oracle degli enti centrali (Consip, Sogei, INAIL, IPZS, ANAS, DTD Giustizia), indicata in ANAC come aggiudicataria del lotto Oracle di Licenze software multibrand 6 (ID 2599). Nessun LEI: capogruppo non ricavabile da fonti gratuite.
- **Arslogica Sistemi S.r.l. (04108030281)**: P.IVA valida (VIES), Padova; 255 CIG; rivenditore Oracle (licenze, Exadata, Oracle Cloud IaaS/PaaS e SaaS) per la sanità veneta e lombarda e per Informatica Alto Adige. Nessun LEI: capogruppo non ricavabile da fonti gratuite.

### 2.5 Raccomandazioni

- **R56** (aggiornata): segnaposto «IMPRESA INESISTENTE» sulla P.IVA di Italware; un identificativo per operatore, o una tabella CF/P.IVA pubblica.
- **R76**: marchio del produttore come campo strutturato e righe nel dataset aggiudicatari per ogni CIG.
- **R77**: capogruppo dei fornitori in dati aperti (LEI e relazioni di controllo).

### 2.6 Storico: mappa v3 e v3.1 (v0.1-v0.5)


Dalla mappa v3 (`report/metodo/rivenditori-v3.*`, contratti attuativi 2022-2026, padri di AQ e importi da verificare esclusi) [V]:

| Giurisdizione del prodotto | Totale | Rivenditore | Diretto | Ignoto | Rivenditore sul noto |
|---|---|---|---|---|---|
| EXTRA-UE | 2,95 mld | 1,82 mld | 0,45 mld | 0,67 mld | **80 %** |
| UE | 0,35 mld | 0,20 mld | 0,07 mld | 0,08 mld | 75 % |
| IT | 2,15 mld | 0,09 mld | 1,53 mld | 0,54 mld | 5 % |

- **1.180 rivenditori** hanno venduto prodotti extra-UE; i primi 5 fanno il **66 %**. TIM da sola 1,07 mld (Microsoft 0,87 mld), poi Eurolink 94 M (Oracle), Fastweb 78 M (AWS, IBM), Postel 61 M (Microsoft), Var Group 48 M, SoftwareOne 48 M.
- Il 7° «rivenditore» per importo è il segnaposto ANAC **«IMPRESA INESISTENTE»** (46,5 M€): nuova **R56**.
- **Nazionalità (v0.2), dai codici fiscali del dataset ANAC aggiudicatari** del mirror (`tools/verifiche/rivenditori_cf.py`, sul server) [V]. Dei contratti di prodotti extra-UE via rivenditore con aggiudicatari ANAC (1,41 mld), il **99,9 %** va a soggetti con CF italiano (11 cifre o CF di persona). Restano 1,5 M€ a CF esteri o non validi: P.IVA estere (FR, AT, CH, Zoom «EU…») e CF italiani con lo zero iniziale perso (es. «1682521008» per P.S.N.). Ci sono 1.104 CF distinti. Altri 0,41 mld di CIG via rivenditore non hanno righe nel dataset aggiudicatari: il nome viene da altra fonte del file di attribuzione.
- **Riconciliazione 2,04 contro 1,82 mld** [V]: nessun CIG è ripetuto su più anni (9.580 righe, 9.580 CIG). La differenza di 215 M€ viene dal file per rivenditore, che somma l'importo intero del CIG a **ogni membro dell'RTI**. Il totale corretto è 1,82 mld. Ripartito (alla mandataria, o in parti uguali) fa 1,41 mld con aggiudicatari ANAC più 0,41 mld senza.
- **Rigenerazione v3.1 (v0.3):** `tools/analisi/rivenditori.py` ora divide l'importo degli RTI in parti uguali fra i membri. Rigenerato sul server, è pubblicato come `report/metodo/rivenditori-v3.1.*`; la v3 resta per confronto. Il file per rivenditore ora somma **1,824 mld**, uguale al totale per canale. I primi 5 fanno il 70 %: TIM 1,05 mld, Eurolink 78 M, Fastweb 64 M, SoftwareOne 48 M, Var Group 45 M, Postel 43 M; «IMPRESA INESISTENTE» 40 M. `python tools/verifiche/rivenditori_esteri.py v3.1`.
- **Primi per CF** (ripartito): TIM 874 M, Eurolink 62 M, Fastweb 44 M, «IMPRESA INESISTENTE» 42 M, Var Group 42 M, Italware 32 M.
- **«IMPRESA INESISTENTE»** ha un CF valido (02102821002, 24 CIG, 74,8 M€ in tutto). Il nome è un segnaposto su un CF reale: R56 aggiornata.
- Esclusi perché l'importo è da verificare: Microsoft 2,50 mld, PSN 2,16 mld, Oracle 0,52 mld.

Rifare: `python tools/verifiche/rivenditori_esteri.py` → `esiti/2026-11-06/rivenditori/`.

## 3. PNRR cloud (#43)

Catena PA Digitale 2026 → CUP → dataset ANAC cup → CIG → attribuzione v3 (`report/metodo/pnrr-contratti-v3.csv`, 26/10/2026) [V]:

| Misura | Contratti collegati | Big tech USA | Quota sul totale | Quota sull'attribuito |
|---|---|---|---|---|
| 1.2 (migrazione al cloud) | 818,9 M€ | **13,6 M€** (Microsoft 10,0; Oracle 2,3; AWS 0,5; Google 0,4) | **1,7 %** | 3,2 % |
| 1.1 (infrastrutture, PSN) | 270,3 M€ | 0 | 0 % | 0 % |

- In 1.2 il resto attribuito è IT (408,6 M€, soprattutto SaaS di fornitori italiani e in-house); 396,7 M€ senza provider. Della quota big tech, 6,6 M€ passano da rivenditori e 6,9 M€ hanno canale ignoto; nessuno diretto.
- Sono **importi dei contratti collegati al CUP**, non la quota del finanziamento: un CUP può avere CIG fuori dal progetto e il 47,8 % dei CUP 1.2 non porta a nessun CIG.
- In 1.1 l'assenza di big tech è nel **contratto** (adesioni PSN); quale tecnologia eroga il PSN (Secure Public Cloud su hyperscaler) non si vede dai CIG: vedi § 4 e R50.
- **1.1 dai decreti (v0.2)** [V]: 16 decreti, 312 CUP, 537,6 M€ finanziati. 238 CUP hanno almeno un CIG, per 197 CIG distinti (`tools/verifiche/pnrr11_prodotto.py`, attribuzione v3 per prodotto):
  - PSN: 111 CIG, 732,5 M€, pari all'**89 %** dell'ICT contato (819,5 M€);
  - big tech USA: **5 CIG, 0,61 M€ (0,07 %)**. Google 0,28 M€ in 2 CIG di servizi professionali; Microsoft 0,33 M€ in 3 CIG cloud e licenze;
  - senza provider: 47 CIG, 85,8 M€;
  - padri di AQ o importi da verificare: 9 CIG, 361,9 M€, fuori dal conto;
  - fuori dal perimetro ICT: 20 CIG.
  Il contratto 1.1 è quasi tutto PSN. La tecnologia erogata dentro il PSN resta invisibile (§ 4).
- **Controvalidazione con FLAG_PNRR_PNC (v0.3)** [V], `tools/verifiche/pnrr_flag.py` (server, 229 file CIG ANAC mensili e delta, DuckDB su disco). Il flag lo dichiara la stazione appaltante, la catena nasce da PA Digitale 2026 e dal dataset cup: sono due vie indipendenti.

  | Catena | CIG | Con flag PNRR | Senza flag | Assenti dai file CIG |
  |---|---|---|---|---|
  | 1.2 (v3) | 12.504 | **11.306 (90 %)**, 733,5 M€ | 1.064, 93,1 M€ | 134, 13,5 M€ |
  | 1.1 (v3) | 61 | 48 (79 %), 344,1 M€ | 10, 14,6 M€ | 3, 19,5 M€ |
  | 1.1 (decreti) | 197 | 136 (69 %), 1.048,1 M€ | 26, 90,2 M€ | 35, 43,0 M€ |

  Gli importi qui sono lordi: comprendono padri di AQ e importi da verificare.
- **I 1.064 CIG 1.2 senza flag (v0.4)** [V]:
  - 1.050 hanno il flag a 0 e 14 vuoto, per 93,1 M€;
  - per anno: 2022 37, 2023 348, 2024 379, 2025 291, 2026 9;
  - **627 (59 %) nominano PNRR, misura 1.2, NextGenerationEU o M1C1 nell'oggetto**: il flag è sbagliato o omesso, nuova **R58**;
  - gli altri 437 sono SaaS, conservazione e gestionali comunali collegati al CUP: compatibili con il progetto, ma senza prova nell'oggetto;
  - 1.043 su 1.064 non hanno provider attribuito; 3 sono Microsoft, 1 Google, 1 AWS.
- **Ponte ufficiale CUP → CIG di Italia Domani (gare ReGiS):** la pagina del catalogo c'è (PNRR_Gare.csv, v11, 13/06/2026), ma il file risponde 403 (Akamai) e il pulsante di scaricamento è solo JavaScript. Nuova **R57**. openpnrr: nell'archivio ci sono solo 3 pagine di progetto, nessun file ponte.

Rifare: `python tools/verifiche/pnrr_bigtech.py` → `esiti/2026-11-06/pnrr/pnrr-bigtech.json`.

### 3.1 Misura 1.2 per prodotto: i 396,7 M€ senza provider (v0.6)

Domanda: quanta parte della Misura 1.2 (migrazione al cloud di Comuni, ASL, scuole e altri enti) è andata a prodotti delle big tech statunitensi. Verifica `python tools/verifiche/pnrr12_prodotto.py --data 2026-11-09` → `esiti/2026-11-09/pnrr12/` (nessuna rete, nessun LLM).

**Universo** [V] (PA Digitale 2026, dataset ANAC `cup`, attribuzione v3):

| Tipologia | CUP finanziati | Finanziato | CUP con almeno un CIG |
|---|---|---|---|
| Comuni | 10.122 | 920,3 M€ | 6.594 (65,1 %) |
| ASL | 225 | 195,8 M€ | 166 (73,8 %) |
| Altri enti | 102 | 90,5 M€ | 56 (54,9 %) |
| Scuole | 10.406 | 56,8 M€ | 4.750 (45,6 %) |
| **Totale** | **20.855** | **1.263,4 M€** | **11.566 (55,5 %)** |

14 avvisi 1.2 (1.401,5 M€ stanziati). I CUP portano a 17.973 CIG; 12.504 sono nel perimetro ICT attribuito, 12.501 contati per 818,9 M€ (3 padri o importi da verificare, 21,1 M€, fuori).

**Strati di attribuzione del prodotto** (vince il primo; RTI divisi in parti uguali):

| Strato | Giurisdizione | CIG | Importo | Quota € | Quota CIG | Precisione |
|---|---|---|---|---|---|---|
| S1 marchio v3 (dizionario, lotti, convenzioni) | **big tech USA** | 73 | **13,6 M€** | **1,7 %** | **0,6 %** | P 100 %, R 89 % (terzo campione a cieco, § 1.3) |
| S1 marchio v3 | IT (PSN 389,2 M€, in-house 12,5, TIM, Fastweb) | 257 | 408,6 M€ | 49,9 % | 2,1 % | idem |
| S2 aggiudicatario con servizio qualificato ACN | IT (SaaS del fornitore) | 3.146 | 150,2 M€ | 18,3 % | 25,2 % | abbinamento nome 60/60 (campione, seme 43) |
| S3 aggiudicatario italiano fuori elenco ACN | IT (fornitore) | 1.212 | 53,0 M€ | 6,5 % | 9,7 % | regola, non misurata |
| S4 aggiudicatario assente, fornitore nel testo | IT (fornitore) | 132 | 2,7 M€ | 0,3 % | 1,1 % | 86/89 = 96,6 % (metà prova) |
| S5 aggiudicatario a controllo extra-UE, nessun marchio | fornitore extra-UE (non prodotto) | 9 | 28,5 M€ | 3,5 % | 0,1 % | lente fornitore |
| S6 residuo: nessun marchio, nessun aggiudicatario | ignota | 7.672 | 162,3 M€ | 19,8 % | 61,4 % | — |

- **Risposta** [V]: prodotti delle big tech USA **13,6 M€ su 818,9 M€ di contratti collegati (1,7 %), 73 CIG su 12.501 (0,6 %)**: Microsoft 10,0; Oracle 2,3; AWS 0,45; Google 0,42; Salesforce 0,21; VMware 0,19. Nessun prodotto UE non italiano attribuito.
- **Incertezza esplicita**: limite basso 1,7 %; se il residuo S6 avesse la stessa quota dell'attribuito, circa **2,1 %**; caso peggiore (tutto S6 big tech) 21,5 %, 25,0 % contando anche S5. Il caso peggiore non è plausibile: S6 sono quasi tutti affidamenti piccoli dei Comuni (141,8 M€ dei 162,3) con oggetto «migrazione al cloud» senza marchio, ma **non è escluso** dai dati.
- **Dove sta la big tech**: ASL 7,5 M€, Comuni 6,0 M€, altri enti 0,13 M€, scuole 2 mila €.
- **S2 è nuovo**: l'elenco ACN dei servizi qualificati (CSV `schede_qualificate_tipo_servizi_cloud_csv`, 2.342 schede, 902 fornitori, archiviato il 6/11/2026, sha256 8559a074…) [R, dato ACN]; l'abbinamento all'aggiudicatario è nostro [V]. Il campione verifica che l'aggiudicatario **sia** il fornitore qualificato, non che il CIG abbia comprato **quella** scheda: la precisione del prodotto per CIG non è misurata.
- **Limite che resta**: l'elenco ACN non dice su quale infrastruttura (IaaS) gira ciascun SaaS. I 150,2 M€ di S2 e i 55,7 M€ di S3-S4 sono prodotti di software house italiane, ma la loro infrastruttura può essere di un hyperscaler: è **dipendenza tecnologica**, non misurabile con i dati pubblici. Nuova **R73**. Lo stesso vale per il PSN (R50).
- **Seconda via sugli atti** [V]: dei 131 atti archiviati, 36 CIG 1.2 hanno testo; 5 nominano AWS, Azure, Google Cloud od Oracle Cloud (2 PSN, 1 in-house, 1 SaaS qualificato, 1 S5). Sono menzioni, non prodotti comprati. Base troppo piccola per stimare l'infrastruttura sotto i SaaS.
- **S6 nasce da un dato mancante**: 7.804 CIG collegati (165 M€) senza aggiudicatario nel dataset ANAC; la candidatura PA Digitale 2026 non dice quali servizi sono stati migrati né su quale scheda ACN. Nuova **R74**.
- Correzione al § 4: l'elenco ACN dei servizi qualificati **in CSV** è nell'archivio; resta non specchiabile il portale `catalogocloud.acn.gov.it` (R55), che ha le schede complete.

### 3.2 Residuo S6, scheda comprata, infrastruttura sotto i SaaS (v0.7)

Verifiche: `python tools/verifiche/pnrr12_ocds.py` (OCDS bulk ANAC → `lavoro/pnrr12/ocds-1.2.jsonl`), poi `python tools/verifiche/pnrr12_prodotto.py --data 2026-11-09`; pilota `python tools/verifiche/saas_infra_pilota.py --data 2026-11-09`. Nessun LLM.

**Il residuo S6 non si riduce con le fonti archiviate** [V]. Abbiamo provato quattro vie:

| Via | CIG S6 trovati (su 7.672) | Con aggiudicatario |
|---|---|---|
| OCDS bulk ANAC 2018-2026 (5.565 CIG 1.2 presenti) | 3.445 | **0**: solo bando, nessun award |
| Dataset ANAC `partecipanti` | 5 | 4 con un solo partecipante |
| Residuo S6 L3 (esiti PVL) | 977 | 0 (967 senza link) |
| Residuo S6 L4 (pagine AT) | 114 | 0 (102 «CIG nella pagina», testo non salvato; 12 con documenti non pertinenti) |
| Atti archiviati (`dati/atti/`) | fino a 13 | non estratto |

- La catena TED, OpenCUP e PA Digitale 2026 non ha aggiudicatari per questi CIG: TED non pubblica affidamenti sotto soglia, OpenCUP e PA Digitale 2026 non riportano il fornitore.
- **Cosa sono i CIG S6** [V]:
  - 6.868 su 7.672 sono del 2023;
  - mediana dell'importo 6.100 €, 6.704 sotto 40 mila €, 7.618 sotto 140 mila €;
  - nell'oggetto, 6.757 hanno «cloud», 4.813 «1.2», 2.042 «migrazione»;
  - sono gli affidamenti diretti dei Comuni sui pacchetti dell'avviso, registrati in ANAC senza esito.
- **Stima per imputazione** [V, modello]: ai CIG S6 si applica la quota di big tech dei CIG attribuiti della stessa tipologia di ente e dello stesso anno, sotto 140 mila €. Risultato: +2,6 M€, quota big tech **2,0 %**. È una stima, non una misura.
- **Precisione dell'OCDS come seconda fonte di aggiudicatari**, misurata sui 1.374 CIG che hanno sia ANAC sia OCDS: 1.269 coincidono (92,4 %). Gli scarti di quasi tutti gli esempi sono varianti del nome («TELECOM ITALIA» per TIM, «WINXPAL», «DEDAGROUP PUBLIC SERVICES» per Deda Next). La via è affidabile, ma per S6 è vuota.

**Quale scheda ACN è stata comprata** [V]:
- su 3.146 CIG S2 (150,2 M€), in **84 CIG (2,2 M€)** il nome di una scheda qualificata del fornitore compare nell'oggetto ANAC o nel lotto OCDS. Esempi: Civilia Next (Deda Next), GisMaster (Technical Design), NUVOLAcomuni (Siscom), BabylonWeb (GIES);
- campione di 40 casi (seme 4343): **40/40 coerenti** con l'oggetto;
- negli altri CIG S2 l'oggetto dice «migrazione al cloud» o il nome del modulo, non quello della scheda. Che il servizio comprato sia proprio una scheda qualificata resta una regola, non una misura.

**Pilota sull'infrastruttura sotto i SaaS** [V, 9/11/2026]. Metodo:
- domini delle piattaforme SaaS multi-ente già nell'archivio (≥ 15 sottodomini di enti);
- per ciascun dominio: record A, AS di origine (Team Cymru, via DNS) e intestatario dal whois del Registro .it;
- una richiesta per host, nessun aggiramento.

| Piattaforma | Intestatario (whois) | AS che risponde |
|---|---|---|
| trasparenza-valutazione-merito.it, maggiolicloud.it | Maggioli S.p.A. | AS208761 Maggioli; AS200760 Dinova (IT) |
| tuttogare.it | Studio Amica S.r.l.u. | AS12637 Seeweb (IT) |
| portaleamministrazionetrasparente.it, etrasparenza.it | Internet Soluzioni S.r.l. | AS12637 Seeweb (IT) |
| asmenet.it | Asmenet Soc. Cons. | AS20746 Telecom Italia (IT) |
| acquistitelematici.it | DigitalPA s.r.l. | **AS31898 Oracle Cloud (EXTRA-UE)** |
| soluzionipa.it | Dedagroup S.p.A. | **AS8075 Microsoft (EXTRA-UE)** |
| traspare.com | non pubblico (.com) | **AS16509 Amazon (EXTRA-UE)** |
| portaletrasparenza.net | non pubblico (.net) | **AS31898 Oracle Cloud (EXTRA-UE)** |

- Su 10 domini di piattaforme di fornitori, **4 rispondono da un hyperscaler USA** (Oracle 2, Microsoft 1, Amazon 1) e 6 da operatori italiani. I domini regionali (toscana.it, veneto.it, sicilia.it, ecc.) non sono SaaS di fornitori e restano fuori.
- Legati ai contratti 1.2 (S2+S3): Maggioli 572 CIG, 37,9 M€, su infrastruttura italiana. DigitalPA, Dedagroup e Studio Amica pesano poco nella 1.2 (meno di 0,2 M€ in tutto).
- **Limiti**:
  - si vede dove risponde il servizio pubblico (front-end), non dove stanno i dati né i backup;
  - un CDN nasconde l'origine;
  - l'intestatario del dominio non coincide per forza con il gestore del servizio (Deda Next ≠ Dedagroup, stesso gruppo [R]).
- **Proposta** (da decidere): estendere il pilota ai primi 30 fornitori S2 per euro. Gli host si prendono dal servizio di ciascun ente (link della scheda ACN, link PVL e AT), con controprova sulle pagine pubbliche «sub-processor» o «trust» dei fornitori, archiviate con sha256 [R finché non coincidono con la misura DNS/AS]. Costo: poche centinaia di query DNS e una pagina per fornitore. L'evidenza va ad aggiornare **R73**.

## 4. PSN e catalogo ACN (#45)

- **Catalogo ACN non specchiabile:** `catalogocloud.acn.gov.it/opendata` e `/robots.txt` rispondono **403** (Akamai) anche con User-Agent da browser e URL del progetto, dal server, il 6/11/2026 [V]. Non è una sezione di Amministrazione trasparente: vale la regola generale, non si aggira. Nuova **R55**: pubblicazione in open data scaricabile.
- **PSN dai CIG** (già misurato, [imbuto 0.5](/rendiconti/imbuto-dove-siamo/)): impegni ANAC 4,38 mld al netto dei tetti certi, contro un portafoglio di 3,8 mld e ricavi 2023-25 di 0,79 mld [R, bilanci PSN]. Contratti PSN con un prodotto big tech nel testo: 12 per 9,2 M€ [V, mappa v3].
- Senza catalogo né contratti di utenza per ente (R50) la quota del PSN erogata su tecnologia di hyperscaler non è misurabile.

## 5. Mirror Consip (#11) e TED/FTS (#27)

Con gli strumenti esistenti: `tools/archivia.py` (content-addressed, idempotente) e `config/risorse.yaml`, con guardia sul disco (stop sotto 45 GB liberi).

- **Consip** (v0.5, fine giro): delle 151 risorse, **94 nuove, 50 invariate, 7 errori**. Gli errori sono i JSON più grandi (500 MB e oltre) e i TTL degli operatori economici, con connessione interrotta a metà; sono in coda per un nuovo tentativo (`lavoro/consip/riprova.txt`).
- **Consip, metodo:** `tools/acquisizione/consip_elenco.py` legge il catalogo CKAN: 16 dataset, 151 risorse dal 2024 in poi, 8,3 GB dichiarati. In v0.3 le 49 CSV (1,59 GB); in v0.4 **tutti i formati** (JSON, XLSX, TTL), secondo la regola del mirror in tutti i formati. Lanciatore `lavoro/consip/specchia-tutti.sh`. Esito al momento del commit: **in corso, circa 90 risorse su 151** (le CSV della v0.3 risultano invariate). Il lanciatore è ripartibile e prosegue da solo sul server; disco a 57 GB liberi. Elenco in `esiti/2026-11-06/mirror/consip-risorse.csv`.
- **TED:** `tools/acquisizione/ted_mirror.py`, API v3 anonima, acquirente italiano, CPV 72/48/302 discendenti compresi.
  - **Filtro verificato** sul marzo 2024 [V]: `classification-cpv`, che guarda tutti i CPV compresi gli aggiuntivi, dà 143 avvisi; `main-classification-proc`, solo il principale, ne dà 132. Il filtro usato è quindi il più largo; `IN (…)` equivale a `72* OR 48* OR 302*`. Gli avvisi italiani di tutti i settori nello stesso mese sono 2.012.
  - Non serviva ripetere per il filtro. Si è ripetuto (v2, `lavoro/ted-v2/`) per aggiungere identificativi interni, testi dei lotti e vincitori: **34 mesi (2024-01 → 2026-10), 5.348 avvisi, 34/34 mesi completi**. La v0.3 diceva 33 mesi e 5.254 avvisi: errore di conteggio, la prova di gennaio era già stata contata.
- **TED → CIG** (`tools/verifiche/ted_cig.py`) [V]:
  - il CIG non è un campo TED; lo si cerca negli identificativi interni e nei testi, tenendo solo i codici che esistono nei file CIG ANAC: 495 candidati, 421 esistenti;
  - **355 avvisi su 5.348 (6,6 %)** hanno almeno un CIG valido, di cui 283 dei 1.988 esiti di gara (14 %) e 10 dei 2.704 bandi (0,4 %);
  - controprova sugli esiti con P.IVA del vincitore e aggiudicatari ANAC: **157/177 (89 %)** coincidono.
  Il ponte TED → CIG è quindi affidabile dove c'è, ma copre poco: nuova **R59** (CIG obbligatorio negli avvisi eForms italiani).
- **TED come fonte di esiti (v0.5)** (`tools/verifiche/ted_esiti.py`) [V]:
  - dei 402 CIG collegati a un esito TED, 310 hanno già gli aggiudicatari in ANAC;
  - per le **112 righe senza aggiudicatari ANAC**, TED dà vincitore e P.IVA in 88 casi e il valore in 99, per **298,3 M€**;
  - elenco in `esiti/2026-11-06/mirror/ted-esiti.csv`: è un'integrazione di dati mancanti in ANAC [V], da segnalare con R59.
- **Vincitori TED nell'imbuto (v0.5)** (`tools/verifiche/ted_imbuto.py`): 84 CIG distinti con vincitore TED e senza aggiudicatari ANAC; 72 sono nell'imbuto:
  - 55 in S5, ICT non cloud (156 M€);
  - 9 in S0, padri di AQ;
  - **7 in S6, residuo**: 6 in G3 e 1 in G1 (19 M€);
  - 1 in S4.
  L'esito è in `esiti/2026-11-06/imbuto/ted-vincitori.csv`. Si integra nell'imbuto a cura di chi lo gestisce (#66); questo rendiconto non modifica quello dell'imbuto.
- **FTS → P.IVA** (`tools/verifiche/fts_piva.py`, xlsx letti con la sola libreria standard): FTS 2007-2025, 19 file archiviati [V]:
  - dei 1.018 aggiudicatari dei contratti cloud con P.IVA italiana (`rivenditori-cf.csv`), **90 ricevono anche fondi UE in gestione diretta**;
  - i primi 30 sommano 870 M€ nel 2007-2025: Leonardo 318 M€, Engineering 204 M€, Cogea 72 M€, TIM 52 M€, KPMG Advisory 33 M€, TI Sparkle 31 M€, Maggioli 29 M€;
  - FTS registra l'importo dell'impegno per beneficiario, che per i consorzi di progetto può essere quello del coordinatore: è una misura di presenza, non di incasso.
  Serve a riconoscere i fornitori, non entra nella spesa ICT della PA.

## 6. Mirror della roadmap (v0.5)

Coda unica `config/coda-mirror-2026-11.txt` con `tools/acquisizione/coda_mirror.sh`: `tools/archivia.py` più una guardia a 45 GB liberi. Ogni fonte è registrata in `config/risorse.yaml`.

| Ticket | Fonte | Cosa | Esito |
|---|---|---|---|
| #13 | PA Digitale 2026 | repository open data intero (zip) | archiviato (17,6 MB) |
| #13 | IndicePA | catalogo CKAN, tutte le risorse | 54 risorse in coda (`lavoro/indicepa/mirror.log`), in corso al commit |
| #12 | SIOPE | USCITE 2017-2026 e ANAGRAFICHE (le entrate sono fuori perimetro) | 11/11 archiviati (circa 0,73 GB) |
| #25 | BDAP | catalogo CKAN (`/SpodCkanApi/api/3`, `/api/3` dà 404): package_list e package_search | 4 pagine su 5 (16 MB). La pagina start=1000 cade anche al nuovo tentativo: il server chiude la connessione dopo 120 s; in pagine da 250 righe un primo tentativo fallisce, altri in corso |
| #29 | Eurostat | COFOG `gov_10a_exp` (TSV) | archiviato (16,9 MB) |
| #28 | GLEIF | golden copy del 6/11: LEI2, RR, REPEX in CSV | 4/4 archiviati (595 MB) |
| #26 | OpenCoesione | `progetti_esteso` (circa 270 MB) | archiviato (269,6 MB) |
| #26 | OpenCUP | pagine «accesso-agli-open-data» e «dettaglio-opendata-complessivo» (il vecchio `/opendata` dà 404) | metadati, decodifiche e file CUP PNRR archiviati (111 MB); OpendataComplessivo.zip (3,4 GB) in coda con ripresa, la guardia può fermarlo |
| #26 | Italia Domani | gare ReGiS | 403 Akamai (R57) |
| #29 | CPT | catalogo Open CPT, solo le spese (le entrate sono fuori perimetro) | 36/36 archiviati |
| #29 | ISTAT | COFOG nazionale | non specchiato: coperto da Eurostat `gov_10a_exp` (stessa fonte, trasmessa da ISTAT) |
| #13 | catalogo ACN | — | escluso (R55, decide Fabio) |

## 7. Prossimi passi

1. #40: la lente testuale è al suo limite (81-89 % di richiamo). Il resto passa da lotti e convenzioni (vie 1 e 2) e dagli atti.
2. #41: atti pertinenti per i 60 CIG del campione top-20 (oggi 0); capogruppo di Eurolink e Arslogica e verifica delle 6 righe [R] da fonti gratuite; un campione a cieco nuovo per misurare le regole del § 2.3 fuori dal campione su cui sono state scritte.
3. #43: residuo S6 solo con atti nuovi (via 6 sui CIG S6) o accesso civico; pilota infrastruttura esteso ai primi 30 fornitori S2 (§ 3.2, da decidere); i 1.064 CIG 1.2 senza flag; i 74 CUP 1.1 senza CIG; il file ReGiS quando sarà raggiungibile (R57).
4. #27: integrare nell'imbuto i 88 vincitori TED dei CIG senza aggiudicatari ANAC.
5. #26 e #29: URL di OpenCUP, CPT e ISTAT; nuovo tentativo sui 7 file Consip.
4. #45: catalogo ACN a mano con Fabio (consultazione da browser, non automatica) o richiesta ad ACN (R55).

## Registro delle revisioni

| Versione | Data | Modifica |
|---|---|---|
| 0.8 | 2026-11-09 | § 2 rivenditori v4.2 (#41): mappa per CF con capogruppo GLEIF ed enti; prodotti extra-UE rivenduti da CF italiani 61,0 % del totale (78,9 % del noto), 57,2 % anche col capogruppo; campione casuale top-20 96,7 %; correzioni della lente (via 2 «2746», multi-lotto, prodotti di terzi, omonimi), cieco invariato; «IMPRESA INESISTENTE» = Italware (VIES), R56 aggiornata, R76-R77 |
| 0.7 | 2026-11-09 | § 3.2: residuo S6 non riducibile con OCDS (3.445 CIG senza award), partecipanti, L3/L4 e atti; stima per imputazione 2,0 %; precisione OCDS 92,4 %; scheda ACN comprata 84 CIG (40/40); pilota DNS/AS sull'infrastruttura dei SaaS (4 domini su 10 su hyperscaler USA) |
| 0.6 | 2026-11-09 | § 3.1 Misura 1.2 per prodotto: universo per tipologia, strati S1-S6 con elenco ACN dei servizi qualificati e fornitore nel testo (precisione misurata), big tech 1,7 % (73 CIG, 0,6 %) con limiti 2,1-25 %; seconda via sugli atti; R73-R74; correzione § 4 (CSV ACN archiviato) |
| 0.5.1 | 2026-11-06 | OpenCUP e CPT trovati e specchiati; vincitori TED nell'imbuto (esito per #66); nuovi tentativi su Consip (curl con ripresa) e BDAP |
| 0.5 | 2026-11-06 | Regole correttive e terzo campione a cieco (big tech P 100 %, R 89 %); Consip a fine giro 94/50/7; TED come fonte di esiti (88 vincitori, 298 M€); mirror SIOPE, IndicePA, PA Digitale 2026, BDAP, Eurostat, GLEIF, OpenCoesione |
| 0.4 | 2026-11-06 | Secondo campione a cieco (regole v0.3 misurate: big tech P 95 %, R 89 %); 1.064 CIG senza flag (R58); filtro TED verificato, TED v2 e TED → CIG; FTS → P.IVA; Consip in tutti i formati; correzione 33 → 34 mesi TED |
| 0.3 | 2026-11-06 | Regole della lente applicate (non misurate); sottocampione sugli atti 1/9; rivenditori v3.1 con RTI ripartiti; FLAG_PNRR_PNC; R57; mirror Consip, TED e FTS |
| 0.2 | 2026-11-06 | Campione a cieco di 240 CIG (`lente_cieco.py`); CF e nazionalità dei rivenditori, riconciliazione 2,04/1,82 mld (`rivenditori_cf.py`); 1.1 dai 312 CUP dei decreti (`pnrr11_prodotto.py`) |
| 0.1 | 2026-11-06 | Prima bozza: tre verifiche nuove (`lente_prodotto.py`, `rivenditori_esteri.py`, `pnrr_bigtech.py`), R55-R56 |
