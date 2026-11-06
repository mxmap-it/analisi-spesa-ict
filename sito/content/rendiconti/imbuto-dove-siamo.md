---
title: "Imbuto: dove siamo"
subtitle: "Quanto dell'universo ANAC si esclude o si include con certezza, quanto resta incerto, e le cinque cose da fare per la completezza"
date: 2026-11-06
lastmod: 2026-11-06
datiAl: 2026-11-03
description: "Dimensione di ogni strato dell'imbuto (CIG ANAC dal 2020) in numero ed euro, per i due assi (è cloud? giurisdizione?), con soglia, residuo per gruppo, tetti di accordo quadro separati dalla spesa, PSN impegni contro bilanci, link ai documenti, test di Zenodo ed EuroTender, censimento ICT AgID e top-5."
sitemap:
  disable: true
build:
  list: never
---

**Versione 0.2 del 2026-11-06 · BOZZA non annunciata: la pubblicazione la decide Fabio Pietrosanti** · [registro delle revisioni](#registro-delle-revisioni) · [disegno dell'imbuto](/progetto/imbuto/) · ticket [#55](https://github.com/mxmap-it/analisi-spesa-ict/issues/55), [#57](https://github.com/mxmap-it/analisi-spesa-ict/issues/57), [#59](https://github.com/mxmap-it/analisi-spesa-ict/issues/59), [#60](https://github.com/mxmap-it/analisi-spesa-ict/issues/60)

Legenda: **[V]** misurato da noi, con il comando per rifarlo; **[R]** riferito da terzi, non verificato.

## 1. Sintesi

- **Universo:** CIG ANAC pubblicati dal 2020 (file annuali 2020-2025 + aggiornamenti mensili), SmartCIG esclusi. Dal 2024: **3.745.883 CIG**; 2020-2023: **1.967.915 CIG** [V].
- **Esclusione certa (non ICT):** dal 2024 **3.216.533 CIG (85,9 %)**. Il 2020-2023 dà l'**82,8 %** [V]. Per escludere servono tre segnali concordi: CPV non ICT, nessun termine ICT nell'oggetto, nessun lotto o convenzione ICT. La precisione di questo strato **non è ancora misurata** (punto 1 della top-5).
- **Inclusione certa sull'asse A (è cloud?):** dal 2024 **4.537 CIG cloud per 1,21 miliardi**, più 894 CIG di infrastruttura in-house per 0,72 miliardi [V]. È la «superficie scalfita».
- **Incerto dal 2024:**
  - **55.946 CIG per 12,5 miliardi** nel residuo S6;
  - **3.515 CIG per 6,5 miliardi** di licenze, software e PSN con marchio o lotto noti ma con il cloud ancora da accertare [V].
- **Giurisdizione degli inclusi certi dal 2024:** extra-UE 0,87 miliardi (45 %), IT 0,80 (41 %), UE 0,26 (14 %) [V]. È provvisoria: la precisione di S3 e S4 è misurata solo sul campione stratificato (§ 4).
- **Soglia:** 500 € toglie 147.715 CIG e una quota d'importo trascurabile. Alzarla a 5.000 € toglierebbe un altro 6 % dei CIG ICT per lo 0,04 % degli euro [V]. **Proposta:** tenere 500 € per la misura e usare 40.000 € solo per separare G3 da G4 (§ 3).
- **Tetti separati dalla spesa (nuovo in 0.2):** dei 2.130 CIG sopra 50 milioni, 781 sono tetti certi per 178 miliardi, 32 sono contratti aggiudicati e 1.317 restano incerti [V]. Negli strati ICT S3-S6 gli euro dal 2024 scendono da **113,3 a 76,5 miliardi**, di cui 33,6 ancora incerti (§ 2.2).
- **PSN (nuovo in 0.2):** al netto dei tetti certi, gli impegni ANAC sono 4,38 miliardi, contro un portafoglio ordini di 3,8 miliardi [R]. I ricavi PSN 2023-2025 sono 0,79 miliardi, circa il 18 % degli impegni [R, bilanci PSN] (§ 4.1).
- **Zenodo 10007545:** fuori, con il motivo scritto. **EuroTender:** non testato, fuori per ora (§ 6).

## 2. Gli strati, per periodo e per asse A (è cloud o infrastruttura IT?)

Gli euro sono l'importo dichiarato (aggiudicazione, altrimenti base d'asta) e **comprendono i massimali** («importo da verificare», § 2.1).

| asse A | dal 2024: CIG | dal 2024: euro | 2020-2023: CIG | 2020-2023: euro |
|---|---:|---:|---:|---:|
| escluso certo, non ICT (S1) | 3.216.533 | 1.286,3 mld | 1.629.304 | 921,8 mld |
| sotto soglia di 500 € (S2, contato e fuori misura) | 147.715 | ≈ 0 ¹ | 56.983 | 0,01 mld |
| padre di accordo quadro (S0, contato negli attuativi) | 88.913 | 0 | 126.904 | 0 |
| ICT non cloud (S5, voce «infrastrutture interne» da ripartire) | 227.830 | 92,4 mld | 126.723 | 34,6 mld |
| **incluso certo: cloud** (S3 + S4) | **4.537** | **1,21 mld** | 1.561 | 0,83 mld |
| **incluso certo: infrastruttura in-house** (S4) | **894** | **0,72 mld** | 161 | 0,06 mld |
| incerto: marchio o lotto noto, cloud da accertare (licenze, software, servizi, PSN) | 3.515 | 6,51 mld | 2.147 | 2,03 mld |
| incerto: residuo S6 | 55.946 | 12,50 mld | 24.132 | 7,19 mld |
| **totale** | **3.745.883** | **1.399,7 mld** | **1.967.915** | **966,6 mld** |

¹ Somma negativa (-1,7 milioni): ci sono importi negativi nella fonte, da segnalare con il problema degli importi.

### 2.1 Importi da verificare (sopra 50 milioni, probabili massimali)

Dal 2024 questi CIG pesano più del resto, quindi i totali in euro vanno letti al netto:

| strato | CIG | euro |
|---|---:|---:|
| S1 escluso non ICT | 1.993 | 731,1 mld |
| S5 ICT non cloud | 118 | 63,1 mld |
| S3 convenzione o lotto | 11 | 4,1 mld |
| S4 marchio | 12 | 1,1 mld |
| S6 residuo | 26 | 4,2 mld |

Per esempio, S5 ICT non cloud dal 2024 scende da 92,4 a **29,3 miliardi** al netto. La raccomandazione è già scritta (R14).

### 2.2 Tetti o spesa? I CIG sopra 50 milioni, uno per uno (top-5 punto 2, nuovo in 0.2)

I 2.160 «da verificare» dal 2024 sono **2.130 CIG distinti**: 30 righe sono CIG ripetuti nei file annuali ANAC [V]. Ogni CIG ha una classe e la via che l'ha decisa (`esiti/2026-11-06/imbuto/tetti-cig.csv`). Le vie valgono in ordine, e vince la prima che scatta [V]:

| via | regola | classe | CIG | euro dichiarati |
|---|---|---|---:|---:|
| T1 padre copiato | derivato (`cig_accordo_quadro`) con importo uguale, ±1 %, a quello del CIG padre | tetto | 78 | 14,75 mld |
| T2 oltre l'ordinato | derivato di un'iniziativa Consip con importo maggiore dell'ordinato Consip 2024-2026 **dell'intera iniziativa** (open data dati.consip.it, #62) | tetto | 14 | 31,86 mld |
| T3 importo ripetuto | stesso importo, all'euro, in almeno 3 CIG di stazioni appaltanti diverse | tetto | 187 | 38,23 mld |
| T4 modalità | modalità di realizzazione ANAC «accordo quadro» o concessione non discendente | tetto | 502 | 93,22 mld |
| E1 aggiudicato | contratto d'appalto senza AQ, esito «aggiudicata», importo di aggiudicazione presente | spesa effettiva ¹ | 32 | 9,78 → 4,68 mld |
| I1 derivato senza riscontro | discende da un AQ o da una convenzione, ma nessuna via lo conferma | incerto | 477 | 313,94 mld |
| I2 testo | il testo parla di AQ, convenzione, massimale o concessione | incerto | 79 | 11,56 mld |
| I3 senza aggiudicazione | appalto senza importo di aggiudicazione | incerto | 761 | 287,30 mld |

¹ «Spesa effettiva» qui vuol dire valore contrattuale aggiudicato, cioè un impegno: non è un pagamento. Gli euro sono quelli dell'aggiudicazione.

In tutto: **781 tetti per 178,0 miliardi** tolti dai totali, 32 contratti con spesa effettiva, **1.317 incerti per 612,8 miliardi** [V].

Gli strati dal 2024 si ricalcolano così [V]. La colonna «dopo» comprende ancora gli incerti sopra 50 milioni:

| strato | euro prima | euro dopo | di cui incerti > 50 M€ |
|---|---:|---:|---:|
| S1 escluso non ICT | 1.286,3 mld | 1.140,0 mld | 579,2 mld |
| S3 convenzione o lotto | 4,83 mld | **2,53 mld** | 0,59 mld |
| S4 marchio | 3,61 mld | **3,05 mld** | 0,54 mld |
| S5 ICT non cloud | 92,39 mld | **59,87 mld** | 29,65 mld |
| S6 residuo | 12,50 mld | **11,08 mld** | 2,82 mld |
| **S3-S6** | **113,3 mld** | **76,5 mld** | 33,6 mld |

Lettura:
- negli strati ICT (162 CIG sopra 50 milioni) i tetti certi pesano **36,8 miliardi**. Il 33,6 restante, quasi tutto S5, è ancora incerto;
- **S3** (l'inclusione certa da convenzione) perde il 48 % degli euro: gli attuativi registrano spesso il massimale;
- gli incerti si sciolgono solo con l'importo dell'ordinativo per CIG. Consip lo pubblica **per iniziativa e lotto, non per CIG né per ente** [V], e il link PVL manca per tutte le adesioni (§ 5). Raccomandazioni R14 e **R49**;
- le regole T3 e T4 sono nuove. La loro precisione non è ancora misurata: serve un controllo a campione sugli atti (da fare).

## 3. Distribuzione degli importi e soglia

Il calcolo riguarda i CIG che restano dopo S1: strati S3-S6, dal 2024, in tutto 292.722 CIG [V].

| fino a | CIG nella classe | quota CIG cumulata | quota euro cumulata |
|---|---:|---:|---:|
| 1.000 € | 3.139 | 1,1 % | 0,002 % |
| 5.000 € | 14.385 | 6,0 % | 0,04 % |
| 40.000 € | 206.355 | 76,5 % | 2,8 % |
| 140.000 € | 47.524 | 92,7 % | 6,2 % |
| 1 M€ | 15.192 | 97,9 % | 11,1 % |
| 5 M€ | 4.516 | 99,5 % | 19,8 % |
| 50 M€ | 1.444 | 99,94 % | 36,0 % |
| oltre | 167 | 100 % | 100 % |

Lettura:
- tre CIG su quattro stanno sotto i 40.000 € e valgono meno del 3 % degli euro;
- 167 CIG sopra i 50 milioni valgono il 64 % degli euro, e sono quasi tutti massimali;
- la soglia di 500 € decisa il 2/11 è già quasi senza costo in euro.

**Proposta, da decidere con Fabio:**
- tenere 500 € come soglia di misura;
- tenere 40.000 € come confine G3/G4: la coda G4 si stima dal campione invece di leggerla;
- trattare a mano tutto ciò che supera i 5 milioni (G1).

## 4. Il residuo per gruppo (dal 2024) e la precisione degli strati

| gruppo | perché è incerto | CIG | euro | con link PVL ai documenti |
|---|---|---:|---:|---:|
| G1 mega (> 5 M€) | provider indeterminato (43) o CPV non ICT con testo ICT (166) | 209 | 4,88 mld | 53,6 % dei CIG |
| G2 informazione mancante | **PSN, servizio da determinare** (864), iniziative multi-provider o da decifrare (20) | 884 | 4,08 mld | **19,6 %** |
| G3 incerti significativi (40 k-5 M€) | provider indeterminato (3.568), CPV non ICT con testo ICT (9.047) | 12.615 | 2,94 mld | 73,1 % |
| G4 coda (< 40 k€) | come G3 | 42.238 | 0,61 mld | 78,3 % |

2020-2023, per confronto [V]:
- G1: 104 CIG, 2,53 miliardi;
- G2: 1.532 CIG, 2,05 miliardi, di cui PSN 235 CIG per 1,03 miliardi;
- G3: 9.977 CIG, 2,48 miliardi;
- G4: 12.519 CIG, 0,14 miliardi.

**Precisione misurata** sul campione stratificato v3 di 611 CIG, dato del 3/11, intervalli di Wilson al 95 % [V]. Il campione **non è casuale sull'universo**: la precisione vale per strato e non si estende all'universo senza pesi.

| strato | asse A (è cloud?) | asse B (giurisdizione) |
|---|---|---|
| S3 convenzione o lotto | 7/13, da 29 a 77 % | 7/7, da 65 a 100 % |
| S4 marchio | 290/371, da 74 a 82 % | 335/355, da 92 a 96 % |
| S5 ICT non cloud | 63/71, da 79 a 94 % | non applicabile |

S1 (esclusione certa) non è misurato: il campione v3 è centrato sull'ICT.

### 4.1 PSN: impegni ANAC contro bilanci PSN (top-5 punto 3, nuovo in 0.2)

Il confronto mette gli impegni registrati in ANAC accanto a quello che PSN S.p.A. dichiara nei bilanci 2024 e 2025. I PDF sono archiviati con sha256, e le cifre sono ricontrollate nel testo da `imbuto_psn.py --rigenera`.

| voce | valore | fonte |
|---|---:|---|
| impegni ANAC, CIG PSN 2020-2026 (235 + 864 CIG) | 5,10 mld | [V] imbuto-0.3.1 |
| … meno i tetti certi sopra 50 M€ (1 CIG: il museo di Taranto, 723,3 M€ = valore della convenzione, T1) | **4,38 mld** | [V] § 2.2 |
| … di cui ancora incerti sopra 50 M€ (9 adesioni, fra cui Aria Lombardia 580 M€ e Careggi 123 M€) | 1,22 mld | [V] |
| portafoglio ordini PSN al 31/12/2025 | 3,8 mld | [R] bilancio 2025 (2,6 a fine 2024) |
| **ricavi PSN 2023-2025** (78,3 + 255,5 + 454,3 M€): la spesa fatturata alle PA | **0,79 mld** | [R] bilanci 2024 e 2025 |
| ricavi 2025 da servizi professionali (migrazione, replatform…) | 79 % | [R] bilancio 2025 |
| PA contrattualizzate / migrate al 31/12/2025 | 617 / 417 | [R] bilancio 2025 |

Lettura:
- anche al netto del tetto certo, gli impegni ANAC (4,38 miliardi) **superano del 15 % il portafoglio** che PSN dichiara (3,8). È coerente con altri massimali ancora nascosti fra i 9 incerti;
- la spesa fatturata finora è **circa il 18 % degli impegni ANAC** e il 21 % del portafoglio. Il resto è spesa futura, per contratti che durano fino a 10 anni;
- per la giurisdizione il bilancio 2025 dà il mix dei **canoni** dei contratti firmati [R]: Secure Public Cloud (Azure, Google, AWS) 15 % (24 % nelle PA centrali); Oracle PSN 14 %; IaaS 32 %; backup 13 %; housing e hosting 13 %. Dall'inizio i canoni sono il 40 % dei contratti e i servizi professionali il 60 %. Applicato al portafoglio (3,8 × 40 % × 15 %), il Secure Public Cloud extra-UE vale circa **0,23 miliardi** di canoni, 0,44 con Oracle PSN [stima da dati R, non per ente];
- **piani dei fabbisogni:** il database del 3/11 (`report/convenzioni/psn-database/`) ha 20 Progetti del Piano dei Fabbisogni pubblicati da 20 enti, il **3,2 % delle 617 PA** contrattualizzate [V]. I grandi contratti ministeriali non li pubblicano;
- **PA digitale 2026:** la misura PNRR 1.1 ha assegnato circa 700 dei 900 milioni [R, bilancio 2025]. I decreti di finanziamento per ente sono pubblicati in PDF su presidenza.governo.it, **non in open data** (R50). Il loro spoglio è il passo successivo: dà il finanziato per ente da confrontare con il CIG.

## 5. Puntatori ai documenti prima e dopo il 2024 (#57, esiti del 4/11 riusati)

Dal 2024 [V, `esiti/pvl-link-cig/2026-11-04/`]:
- **presenza:** il link ai documenti è nell'API PVL per il **65,1 % dei 3,73 milioni di CIG** 2024-2026, pari al 43,7 % dell'importo. Il link manca per tutte le 93.485 **adesioni a convenzioni e accordi quadro** e per i 30.214 affidamenti in house. A gennaio-febbraio 2024, in piena transizione, c'è solo nell'1,5-3,2 % dei CIG;
- **nell'imbuto** (incrocio nuovo di questo rendiconto, [V]):
  - S3 attuativi di convenzione: link nello **0,1 %** dei CIG. L'inclusione certa da convenzione non ha documenti dell'ente raggiungibili dal CIG;
  - S4: 69,6 %;
  - S5: 82,0 %;
  - G2 PSN e simili: 19,6 %;
  - G3: 73,1 %;
- **funzionamento**, sul campione di 402 domini di destinazione (uno per dominio, stratificato per famiglia di sistema):
  - documenti scaricabili su 45;
  - login o area riservata su 158;
  - pagina senza documenti visibili su 64;
  - nessuna risposta su 89;
  - errore HTTP su 39;
- **coerenza:** 174.834 CIG con avviso PVL non stanno nei file BDNCP 2024+, causa da accertare.

Prima del 2024 [V]: nessuna fonte aperta del link (R30). Il 2020-2023 resta senza puntatore ai documenti in open data. Per questo la prima statistica di sovranità riguarda il 2024 e oltre.

## 6. Test di Zenodo 10007545 ed EuroTender (#59)

**Zenodo 10007545** (Siciliani et al., CLiC-it 2023, CC-BY-4.0; `cpv_5M.csv.gz`, md5 verificato) [V]:
- **che cos'è:** 5 milioni di coppie oggetto→CPV, ricavate dagli stessi dati ANAC. Solo 70.846 dei suoi CIG cadono negli strati ICT 2020-2022 del nostro universo, nessuno dal 2023: copre soprattutto gli anni precedenti al 2020;
- **test:** dal dataset abbiamo ricavato un lessico «puro non ICT» di 1.200 parole, ciascuna con almeno 500 occorrenze e al più lo 0,1 % di righe con CPV ICT. La regola esclude un CIG quando contiene almeno 2 parole del lessico e nessun termine ICT forte;
- **guadagno:** la regola escluderebbe in più **245 CIG del residuo S6 dal 2024 per 58,8 milioni**, lo **0,44 %** del residuo. Sul campione v3 esclude 3 CIG, nessuno cloud per il riferimento: 3 casi non bastano a misurare la precisione;
- **esito: fuori.**
  - il guadagno è marginale;
  - la fonte è la stessa di S1, quindi non porta un segnale indipendente;
  - un lessico così si ricava, se servisse, dal nostro mirror ANAC, che è più recente.

  Il dataset resta utile per il rapporto CPV: la prima riga del file abbina «manutenzione mezzi da lavoro» al CPV «etichette autoadesive».

**EuroTender** (`sinceaihq/eurotender-cpv-baseline`, Apache-2.0):
- **non testato:** l'installazione del pacchetto sul server è stata negata dal controllo dei permessi e non l'abbiamo aggirata;
- **valutazione sulla carta:**
  - il modello predice la **divisione CPV** (top-1 82 % [R, numeri degli autori, su dati TED]);
  - quindi risponde a «è ICT?», non a «è cloud?» e non alla giurisdizione;
  - lì l'imbuto ha già S1 a tre segnali;
- **esito: fuori per ora.** Rientra solo come voto indipendente per misurare S1, se Fabio autorizza l'installazione in un ambiente separato (`lavoro/eurotender/`, già clonato al commit f3ab5f8).

## 7. Censimento del patrimonio ICT della PA (AgID, #60) — solo ricerca, nessun contatto

- **Chi lo compila e quando:** tutte le PA [R, pagina padigitale2026.gov.it letta il 6/11]. Le scadenze 2026 sono due:
  - **10 novembre**: comuni, province, città metropolitane, regioni, PA centrali, ASL e aziende ospedaliere;
  - **1 dicembre**: scuole, università, enti di ricerca e AFAM.

  Il censimento è triennale e obbligatorio (art. 33-septies c. 1-ter d.l. 179/2012). Si compila nell'area riservata di PA digitale 2026 (SPID/CIE) e l'attestato va firmato dal legale rappresentante o dall'RTD.
- **Quali dati:**
  - organizzazione ICT;
  - data center di proprietà (ubicazione, potenza, storage);
  - servizi e livello di migrazione al cloud qualificato ACN, con i fornitori;
  - **spesa ICT** (costi operativi, investimenti, licenze, previsioni triennali, acquisti di servizi cloud e criticità con gli accordi quadro).

  Per l'obiettivo finale è la **controprova** più diretta, dichiarata dall'ente, della spesa misurata dagli appalti.
- **Pubblicazione:** la pagina dice solo che i dati si condividono fra AgID, DTD e altri enti con appositi accordi, senza promettere una pubblicazione. Per l'edizione precedente (2018-2020) [R]:
  - AgID ha pubblicato solo una **sintesi**: 1.252 data center, 35 candidabili al PSN, 27 in gruppo A, 1.190 in gruppo B;
  - non abbiamo trovato un dataset aperto per ente.
- **Come ottenerli** (proposta, NESSUNA richiesta senza l'ok di Fabio):
  1. cercare prima eventuali pubblicazioni AgID dopo le scadenze;
  2. accesso civico generalizzato ad AgID (Area Infrastrutture e sicurezza, tramite l'URP; responsabile da individuare sul sito AgID) per il dataset per ente, almeno spesa ICT e cloud aggregate per ente e anno;
  3. in subordine, ai singoli enti per il questionario compilato.

  Raccomandazione nuova: **R48**.

## 8. Top-5 per la completezza dei dati

| # | cosa | metodo | costo stimato | chi deve agire |
|---|---|---|---|---|
| 1 | **Misurare la precisione di S1** (3,2 M CIG, 85,9 %), che oggi è un'ipotesi | campione casuale di ~400 CIG di S1 annotato (volontari + via 6 a regole); con 0 errori il limite superiore Wilson è ~1 % | ~400 annotazioni, qualche ora di volontari; token trascurabili | noi |
| 2 | **Separare spesa e massimali**. **Fatto in 0.2** (§ 2.2): tolti 781 tetti; S3-S6 scende da 113,3 a 76,5 mld; restano incerti 1.317 CIG per 612,8 mld, di cui 33,6 negli strati ICT | prossimo passo: l'importo dell'ordinativo per CIG, dagli atti (link PVL dove c'è) o da Consip; controllo a campione delle regole T3 e T4 | script, zero token; lettura degli atti per i ~110 CIG ICT incerti | noi; **ANAC/Consip** per l'ordinato per CIG (R14, R37, R49) |
| 3 | **PSN**. **Fatto in 0.2** (§ 4.1): impegni ANAC 4,38 mld contro un portafoglio di 3,8 [R] e ricavi 2023-2025 di 0,79 [R]; PPdF pubblicati dal 3,2 % delle PA | prossimo passo: spoglio dei decreti di finanziamento PNRR 1.1 per ente; ricerca dei PPdF dei 9 CIG PSN incerti sopra 50 M€ | lettura dei PDF, decine di USD-eq | noi; **DTD/PSN** per piani e consuntivi per ente (R20, R39, R50) |
| 4 | **G1 + G3 con la via 6** (12.824 CIG, 7,8 mld) | G1 (209) a mano; G3 in ordine d'importo con il modello e gli atti dal link PVL (73 % raggiungibile) | ~1,8 USD-eq per 5 CIG (giro 2): G3 intero ≈ 4.500 USD-eq, oltre 10 settimane di tetto (400/settimana); i primi 1.000 CIG per importo ≈ 360 USD-eq | noi; **enti** per i link che non funzionano (R31-R33) |
| 5 | **Licenze e marchi «cloud da accertare»** (3.515 CIG, 6,5 mld) e controprova dal censimento AgID | lettura dei contratti Microsoft (decisione del 3/11) e Oracle; richiesta dei dati del censimento 2026 | lettura, centinaia di USD-eq; accesso civico solo dopo l'ok di Fabio | noi; **AgID** (R48); **ANAC/ACN** per un campo strutturato su prodotto e modalità (R21) |

## 9. Rifare i numeri

Da un clone pulito, senza dati grezzi (legge gli esiti versionati):

```
python tools/verifiche/imbuto_strati.py        # strati, assi, soglia, gruppi, link PVL; controlla la coerenza
python tools/verifiche/zenodo_test.py          # esito del test Zenodo
python tools/verifiche/imbuto_tetti.py         # tetti, spesa e incerti sopra 50 M€; strati ricalcolati
python tools/verifiche/imbuto_psn.py           # PSN: impegni ANAC contro bilanci PSN e piani dei fabbisogni
```

Sul server, `imbuto_tetti.py --rigenera` rilegge il mirror ANAC (righe ≥ 45 M€, aggiudicazioni) e riscrive `tetti-cig.csv`. `imbuto_psn.py --rigenera` ricontrolla gli sha256 dei bilanci PSN e cerca le cifre nel loro testo.

Dal mirror, sul server:
- `python tools/analisi/imbuto.py 2020` rigenera `lavoro/imbuto/ict.csv` e il riepilogo;
- `imbuto_strati.py --rigenera` e `zenodo_test.py --rigenera` rifanno la distribuzione, con DuckDB su disco, 6 GB e 2 thread.

Ingressi:
- `esiti/2026-11-03/imbuto/riepilogo-0.3.1.json` (imbuto-0.3.1, regole v3.1);
- `esiti/2026-11-06/imbuto/distribuzione.json` (con lo sha256 di `ict.csv`);
- `esiti/2026-11-06/zenodo/esito.json`;
- `esiti/2026-11-06/imbuto/tetti-cig.csv` (una riga per CIG, con classe e via) e `tetti.json`;
- `esiti/2026-11-06/psn/bilanci-psn.json` (cifre [R] di PSN, con lo sha256 dei PDF) e `psn.json`.

Coerenza controllata: i CIG non esclusi coincidono fra riepilogo e `ict.csv`, 386.911 dal 2024 e 284.629 nel 2020-2023.

## Limiti

- I numeri sono di imbuto-0.3.1 (3/11), che non tiene conto dei miglioramenti successivi alle convenzioni (#62).
- SmartCIG resta fuori.
- Gli euro includono gli importi negativi della fonte.
- L'asse B è riportato solo per gli inclusi certi.

## Registro delle revisioni

| versione | data | cosa |
|---|---|---|
| 0.1 | 2026-11-06 | prima bozza per Fabio: strati, soglia, gruppi, link PVL per strato, Zenodo/EuroTender, censimento AgID, top-5 |
| 0.2 | 2026-11-06 | § 2.2: tetti e spesa per i 2.130 CIG sopra 50 M€, con la via di ogni CIG e gli strati ricalcolati; § 4.1: PSN, impegni contro bilanci 2024-2025 e piani dei fabbisogni; top-5 punti 2 e 3 aggiornati; R49 e R50 |
