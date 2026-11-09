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

**Versione 0.6 del 2026-11-09 · BOZZA non annunciata: la pubblicazione la decide Fabio Pietrosanti** · ticket [#40](https://github.com/mxmap-it/analisi-spesa-ict/issues/40), [#41](https://github.com/mxmap-it/analisi-spesa-ict/issues/41), [#43](https://github.com/mxmap-it/analisi-spesa-ict/issues/43), [#45](https://github.com/mxmap-it/analisi-spesa-ict/issues/45), parte di [#24](https://github.com/mxmap-it/analisi-spesa-ict/issues/24)

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
2. #41: aggiudicatari dei 0,41 mld senza righe ANAC.
3. #43: residuo S6 (7.672 CIG, 162,3 M€) dagli atti della via 6 e dagli esiti PVL; giudizio per CIG sulla scheda ACN comprata (campione S2); i 1.064 CIG 1.2 senza flag; i 74 CUP 1.1 senza CIG; il file ReGiS quando sarà raggiungibile (R57).
4. #27: integrare nell'imbuto i 88 vincitori TED dei CIG senza aggiudicatari ANAC.
5. #26 e #29: URL di OpenCUP, CPT e ISTAT; nuovo tentativo sui 7 file Consip.
4. #45: catalogo ACN a mano con Fabio (consultazione da browser, non automatica) o richiesta ad ACN (R55).

## Registro delle revisioni

| Versione | Data | Modifica |
|---|---|---|
| 0.6 | 2026-11-09 | § 3.1 Misura 1.2 per prodotto: universo per tipologia, strati S1-S6 con elenco ACN dei servizi qualificati e fornitore nel testo (precisione misurata), big tech 1,7 % (73 CIG, 0,6 %) con limiti 2,1-25 %; seconda via sugli atti; R73-R74; correzione § 4 (CSV ACN archiviato) |
| 0.5.1 | 2026-11-06 | OpenCUP e CPT trovati e specchiati; vincitori TED nell'imbuto (esito per #66); nuovi tentativi su Consip (curl con ripresa) e BDAP |
| 0.5 | 2026-11-06 | Regole correttive e terzo campione a cieco (big tech P 100 %, R 89 %); Consip a fine giro 94/50/7; TED come fonte di esiti (88 vincitori, 298 M€); mirror SIOPE, IndicePA, PA Digitale 2026, BDAP, Eurostat, GLEIF, OpenCoesione |
| 0.4 | 2026-11-06 | Secondo campione a cieco (regole v0.3 misurate: big tech P 95 %, R 89 %); 1.064 CIG senza flag (R58); filtro TED verificato, TED v2 e TED → CIG; FTS → P.IVA; Consip in tutti i formati; correzione 33 → 34 mesi TED |
| 0.3 | 2026-11-06 | Regole della lente applicate (non misurate); sottocampione sugli atti 1/9; rivenditori v3.1 con RTI ripartiti; FLAG_PNRR_PNC; R57; mirror Consip, TED e FTS |
| 0.2 | 2026-11-06 | Campione a cieco di 240 CIG (`lente_cieco.py`); CF e nazionalità dei rivenditori, riconciliazione 2,04/1,82 mld (`rivenditori_cf.py`); 1.1 dai 312 CUP dei decreti (`pnrr11_prodotto.py`) |
| 0.1 | 2026-11-06 | Prima bozza: tre verifiche nuove (`lente_prodotto.py`, `rivenditori_esteri.py`, `pnrr_bigtech.py`), R55-R56 |
