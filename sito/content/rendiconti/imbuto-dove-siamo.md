---
title: "Imbuto: dove siamo"
subtitle: "Quanto dell'universo ANAC si esclude o si include con certezza, quanto resta incerto, e le cinque cose da fare per la completezza"
date: 2026-11-06
lastmod: 2026-11-09
datiAl: 2026-11-03
description: "Dimensione di ogni strato dell'imbuto (CIG ANAC dal 2020) in numero ed euro, per i due assi (è cloud? giurisdizione?), con soglia, residuo per gruppo, tetti di accordo quadro separati dalla spesa, PSN impegni contro bilanci, link ai documenti, test di Zenodo ed EuroTender, censimento ICT AgID e top-5."
sitemap:
  disable: true
build:
  list: never
---

**Versione 0.14 del 2026-11-09, per la consegna del 12/11 · BOZZA non annunciata: la pubblicazione la decide Fabio Pietrosanti** · [registro delle revisioni](#registro-delle-revisioni) · [disegno dell'imbuto](/progetto/imbuto/) · ticket [#55](https://github.com/mxmap-it/analisi-spesa-ict/issues/55), [#57](https://github.com/mxmap-it/analisi-spesa-ict/issues/57), [#59](https://github.com/mxmap-it/analisi-spesa-ict/issues/59), [#60](https://github.com/mxmap-it/analisi-spesa-ict/issues/60), [#50](https://github.com/mxmap-it/analisi-spesa-ict/issues/50), [#66](https://github.com/mxmap-it/analisi-spesa-ict/issues/66), [#67](https://github.com/mxmap-it/analisi-spesa-ict/issues/67), [#68](https://github.com/mxmap-it/analisi-spesa-ict/issues/68), [#71](https://github.com/mxmap-it/analisi-spesa-ict/issues/71), [#73](https://github.com/mxmap-it/analisi-spesa-ict/issues/73), [#58](https://github.com/mxmap-it/analisi-spesa-ict/issues/58)

Legenda: **[V]** misurato da noi, con il comando per rifarlo; **[R]** riferito da terzi, non verificato.

## 1. Sintesi

**Per chi legge per la prima volta (0.14).**

- **Cosa misuriamo.** Tutti i contratti pubblici censiti da ANAC (CIG) dal 2020 passano per un *imbuto*: si toglie prima ciò che è **certamente non ICT** o non cloud, si tiene ciò che è **certamente cloud** (con la giurisdizione del prodotto: IT, UE, extra-UE), e lo sforzo di lettura degli atti va solo sull'**incerto**. Due domande per ogni contratto: è cloud? di quale giurisdizione?
- **Numeri chiave verificati, dal 2024** [V, imbuto 0.3.1 salvo dove detto]:
  - universo 3.745.883 CIG; esclusi con certezza come non ICT l'85,9 %;
  - spesa ICT (strati S3-S6) al netto dei tetti di accordo quadro: **56,06 mld** con la regola 0.3.4 (una riga per CIG, perimetro CPV 0.3.3), misurata in prova a secco; l'imbuto ufficiale pubblicato è ancora 0.3.1 (55,70 mld con la stessa misura) (§ 2.7);
  - cloud certo: 4.537 CIG per 1,21 mld, più 0,72 mld di infrastruttura in-house; giurisdizione degli inclusi certi extra-UE 45 %, IT 41 %, UE 14 %;
  - residuo incerto S6: 55.946 CIG per 12,5 mld dichiarati (0.3.1; 59.406 / 16,37 mld con la 0.3.4, § 2.7).
- **Cosa è stima, non misura.** I rapporti fra CIG e pagato BDAP per ministero (§ 4.10-4.12: buco MEF circa 0,3 mld l'anno); la forbice cloud degli EA Microsoft (0,55-0,81 mld, campione non casuale, § 4.6); le proposte della via 6 (lettura degli atti con modello linguistico) finché non superano la revisione C1-C4 (§ 4.3.2); la giurisdizione degli inclusi certi, perché la precisione di S3-S4 è misurata solo su campione.
- **Cosa manca e perché.** Per gran parte del residuo **l'atto che dice il prodotto non è raggiungibile da fonti aperte**: dopo i livelli L3 (link PVL), MePA e L4 (sezioni «Bandi di gara e contratti» di 4.007 enti su 4.352) solo **535 CIG per 304,7 M€** hanno un documento che cita il CIG (§ 4.11). Il resto passa alla richiesta di **accesso civico** massiva ([#58](https://github.com/mxmap-it/analisi-spesa-ict/issues/58)), non ancora inviata (decisione di Fabio). La via 6 su G3 è parziale (764 CIG su 1.000 al 9/11 ore 20).
- **Cloud e giurisdizione per prodotto e rivenditore:** lente prodotto, mappa dei rivenditori (v4.5: prodotti extra-UE 3,023 mld, rivenditori con CF italiano 61,2 %) e infrastruttura sono nel rendiconto [Obiettivo 6](/rendiconti/obiettivo-6/).

**Nuovo in 0.14 (9/11/2026):** § 2.7 anteprima della rigenerazione 0.3.4 (56,06 mld, effetto separato dei cambiamenti, 0 CIG ripetuti, 29 G1 nuovi e proposta P1 da decidere); § 4.11 L4 finito (#68 chiuso), ripasso #73 in corso; § 4.3.3 segnaposto per la ricerca mirata degli atti C1.

**Nuovo in 0.10-0.12 (9/11/2026):**
- **CIG ripetuti, correzione del totale** (§ 2.6, R53, 0.12): il 55,3 mld di S3-S6 dal 2024 era sottostimato di circa 0,43 mld, quasi tutto S5. Con una riga per CIG il totale è **circa 55,7 mld**: è una **stima** fino alla rigenerazione con la regola imbuto 0.3.4 (`tools/verifiche/imbuto_cig_ripetuti.py`) [V sui conteggi].
- **Via 6, a oggi e parziale** (§ 4.3.1): G1 classificato per intero (196 CIG, 4,70 mld), G3 a metà (514 dei primi 1.000 CIG, 1,15 dei 1,55 mld). In G1 la via 6 propone 1,21 mld non ICT (verso S1), 1,77 mld ICT non cloud (verso S5), 83 M€ cloud certo, 1,64 mld ancora incerti [V; **proposte da revisionare**, fuori dai totali].
- **CIG derivati da accordo quadro non collegabili** (§ 4.9, #50): dei 55.114 CIG ICT discendenti da AQ o convenzione (89,2 mld), 1.666 non si collegano a un padre esistente, per **734 M€, lo 0,82 %**. Il prodotto ereditato dall'AQ manca quindi per una quota trascurabile [V].
- **Denominatore BDAP dello Stato centrale** (§ 4.10, #67): pagato ICT 2024 **1.141 M€** sui codici gestionali ICT, **979 M€** per la seconda via (classificazione economica) [V]. I rapporti CIG/pagato per ministero sono una **stima** di dove l'imbuto è cieco, non una percentuale di copertura. Con l'abbinamento per codice fiscale (0.11, § 4.12) il buco della Giustizia si rivela un artefatto della regola sul nome (0,96 nel 2024); resta il **MEF** (0,25 nel 2024), circa **0,3 miliardi l'anno** [V sui conteggi, stima sull'interpretazione].
- **Residuo S6, documenti** (§ 4.11, #57): 535 CIG per 304,7 M€ hanno un documento che cita il CIG e possono passare da incerto a leggibile; in S6/G3 sono il 2,1 % dei CIG. L4 finito il 9/11 (4.007 enti su 4.352; aggiornato in 0.14) [V].

- **Universo:** CIG ANAC pubblicati dal 2020 (file annuali 2020-2025 + aggiornamenti mensili), SmartCIG esclusi. Dal 2024: **3.745.883 CIG**; 2020-2023: **1.967.915 CIG** [V].
- **Esclusione certa (non ICT):** dal 2024 **3.216.533 CIG (85,9 %)**. Il 2020-2023 dà l'**82,8 %** [V]. Per escludere servono tre segnali concordi: CPV non ICT, nessun termine ICT nell'oggetto, nessun lotto o convenzione ICT. La precisione di questo strato **non è ancora misurata** (punto 1 della top-5).
- **Inclusione certa sull'asse A (è cloud?):** dal 2024 **4.537 CIG cloud per 1,21 miliardi**, più 894 CIG di infrastruttura in-house per 0,72 miliardi [V]. È la «superficie scalfita».
- **Incerto dal 2024:**
  - **55.946 CIG per 12,5 miliardi** nel residuo S6;
  - **3.515 CIG per 6,5 miliardi** di licenze, software e PSN con marchio o lotto noti ma con il cloud ancora da accertare [V].
- **Giurisdizione degli inclusi certi dal 2024:** extra-UE 0,87 miliardi (45 %), IT 0,80 (41 %), UE 0,26 (14 %) [V]. È provvisoria: la precisione di S3 e S4 è misurata solo sul campione stratificato (§ 4).
- **Soglia:** 500 € toglie 147.715 CIG e una quota d'importo trascurabile. Alzarla a 5.000 € toglierebbe un altro 6 % dei CIG ICT per lo 0,04 % degli euro [V]. **Proposta:** tenere 500 € per la misura e usare 40.000 € solo per separare G3 da G4 (§ 3).
- **Tetti separati dalla spesa (nuovo in 0.2):** dei 2.130 CIG sopra 50 milioni, 781 sono tetti certi per 178 miliardi, 32 sono contratti aggiudicati e 1.317 restano incerti [V]. Negli strati ICT S3-S6 gli euro dal 2024 scendono da **113,3 a 76,5 miliardi**, di cui 33,6 ancora incerti (§ 2.2).
- **Tetti, precisione e revisione (nuovo in 0.3):** su un campione stratificato giudicato sugli atti, T4 accordo quadro e T3 non tondo risultano precisi al 100 % (intervallo 80-100 %) e T4 concessione al 73 % (48-89 %). T3 con importo tondo si ferma al 53 % ed è ristretto [V]. Con le regole v2, i dati PVL e la revisione degli incerti ICT (10 errori d'importo per 14,1 mld), **S3-S6 dal 2024 scende a 58,2 miliardi**, di cui 14,4 ancora incerti in 80 CIG (§ 2.3).
- **Concessioni, quadro economico, CUP (nuovo in 0.4):**
  - con 30 CIG giudicati, T4 concessione è precisa al 67 %; dopo la regola I6 (concessioni con canoni a carico della PA tornano incerte) sale al 94 % (74-99 %);
  - il quadro economico ANAC conferma gli errori d'importo: 8 CIG dichiarati per 10,1 mld valgono 70.150 €;
  - i SAL certificati sono 0,40 mld;
  - 238 CUP PNRR 1.1 su 312 sono collegati ai CIG: 431 M€ di contributo coprono circa un quinto dei 2,20 mld dei contratti PSN collegati [V] (§ 2.4, § 4.4).
- **Piattaforme e Oracle (nuovo in 0.8):** l'adattatore per PortaleAppalti ha scaricato da anonimo l'aggiudicazione Oracle di CINECA: ULA, nessun cloud. Nessuno dei 5 atti Oracle letti contiene servizi cloud (0-43 %). Per gli EA Microsoft la ricerca per ente non rende: 1 atto su 50 (§ 4.7).
- **EA Microsoft e Oracle (nuovo in 0.7):** negli 8 atti di adesione agli EA letti la quota cloud pesata è il 92 % (8 su 8 a prevalenza cloud, 68-100 %). Sul residuo Microsoft di 819 M€ la forbice cloud passa a 0,55-0,81 mld, con un campione non casuale. I primi 20 Oracle (261 M€) sono supporto e rinnovi: on premises probabile (§ 4.6).
- **Doppioni e licenze (nuovo in 0.6):**
  - 11.043 righe erano un CIG ripetuto dentro lo stesso file annuale (2024 o 2025): tolte, gli strati ICT S3-S6 dal 2024 scendono a **circa 55,7 miliardi** (stima corretta in 0.12, era 55,3; valore esatto alla rigenerazione 0.3.4) (§ 2.6);
  - fra licenze e marchi, cloud certo 168 M€ (extra-UE 141), non cloud certo 892 M€ (VMware 595), incerto 1,68 mld, quasi tutto EA Microsoft e licenze Oracle senza dettaglio [V] (§ 4.5).
- **Chiusura del giro sugli incerti (nuovo in 0.5):** le sezioni AT di 40 enti, con 64 dei 79 CIG ICT incerti, non contengono **nessun atto con l'importo**; ci sono 4 blocchi (403 e CAPTCHA), già registrati. I 79 CIG (14,4 mld) restano incerti: l'ordinativo non è raggiungibile da fonti aperte (R54). E4 toglie correttamente l'importo errato in 14 casi su 15 (70-99 %), ma il quadro economico è plausibile solo in 9 su 15 (36-80 %). PNRR chiuso a 16 decreti, 537,6 M€ (§ 2.5).
- **PNRR 1.1 (nuovo in 0.3):** lo spoglio di 15 decreti di finanziamento dà 524 milioni a 274 enti, cioè il 75 % dei ~700 milioni assegnati dichiarati da PSN [V; riferimento R] (§ 4.2).
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
| incerto: residuo S6 (di cui con documento che cita il CIG: 532 CIG, 304,5 M€, potenziale, § 4.11) | 55.946 | 12,50 mld | 24.132 | 7,19 mld |
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

### 2.3 Quanto sono precise le regole dei tetti, e la revisione degli incerti ICT (nuovo in 0.3)

**Campione stratificato:** 15 CIG per ognuno dei quattro gruppi di T3 e T4, estratti con seme fisso (`imbuto_revisione.py --campione`). Ogni CIG è giudicato sugli atti pubblicati: l'oggetto ANAC e l'avviso PVL (campo `accordo_quadro`, descrizione, valore aggiudicato). «Confermato» vuol dire che l'importo dichiarato **non è spesa della PA** per quel CIG [V]:

| gruppo | CIG nel gruppo | confermati nel campione | precisione | intervallo di Wilson 95 % |
|---|---:|---:|---:|---|
| T3 importo ripetuto, tondo (multiplo di 100.000 €) | 103 | 8/15 | 53 % | 30-75 % |
| T3 importo ripetuto, non tondo | 84 | 15/15 | 100 % | 80-100 % |
| T4 accordo quadro | 368 | 15/15 | 100 % | 80-100 % |
| T4 concessione | 134 | 11/15 | 73 % | 48-89 % |

Controllo esaustivo di T4 sull'avviso PVL: dei 192 accordi quadro che hanno il campo nell'avviso, **191 sono «accordo quadro» anche lì** (99,5 %, intervallo 97,1-99,9 %) [V].

Lettura:
- **T3 con importo tondo non regge:** 50, 60 o 100 milioni si ripetono per caso fra appalti veri (una nave, un satellite, un depuratore). Nel campione i tondi confermati sono tutti adesioni a convenzioni o AQ. Dalla regola v2 un T3 tondo resta tetto solo se la modalità è «discendente da AQ/convenzione»; gli altri tornano incerti (51 CIG, 4,5 mld);
- **T4 concessione è precisa al 73 %:** le eccezioni sono partenariati in cui i canoni li paga la PA (efficienza energetica, impianti termici, centro cottura). Per questo il dato in euro di T4-concessione (42,8 mld nel gruppo) va letto con questa forchetta.

**Regole v2, dall'avviso PVL** (`esiti/2026-11-06/imbuto/pvl-percig.csv`, estratto dagli avvisi già scaricati per #57) [V]:
- un incerto che nel PVL è dichiarato accordo quadro diventa tetto (T5, 30 CIG);
- un incerto che nel PVL non è AQ e ha un valore aggiudicato più basso diventa spesa effettiva, con l'importo del PVL (E2, 188 CIG: 34,9 → 23,4 mld).

**Revisione a mano dei CIG ICT incerti** (`revisione-incerti-ict.csv`, una riga e un motivo per CIG) [V-testo]:
- **10 errori d'importo evidenti per 14,1 mld**, tolti dai totali: una telecamera da 4,7 miliardi, due licenze software da 3,1 miliardi, il servizio di trasparenza di un piccolo comune da 3,0 miliardi, 55 notebook da 862 milioni. L'importo del PVL è lo stesso di BDNCP, quindi l'errore nasce alla fonte (raccomandazione **R51**);
- **9 tetti**: lotti ripetuti degli AQ PC e valori della convenzione SPC.

**Importo dell'ordinativo per gli incerti ICT:** dei 114 CIG di partenza,
- 18 hanno ora un valore aggiudicato dal PVL o da ANAC (1,68 → 0,94 mld);
- 54 sono tetti e 10 errori;
- **80 restano incerti, per 14,4 mld**. Sono quasi tutti attuativi di AQ e adesioni PSN, che non hanno né l'avviso PVL né il link ai documenti (§ 5). Il loro ordinativo sta solo negli atti dell'ente (determina di adesione, contratto esecutivo), da cercare uno per uno, oppure nei flussi di Consip e PSN (R49, R50).

**Strati ricalcolati dal 2024 (v2)** [V]:

| strato | euro dichiarati | 0.2 (regole v1) | **0.3 (regole v2)** | di cui incerti > 50 M€ |
|---|---:|---:|---:|---:|
| S3 convenzione o lotto | 4,83 mld | 2,53 | **2,53 mld** | 0,59 |
| S4 marchio | 3,61 mld | 3,05 | **3,01 mld** | 0,18 |
| S5 ICT non cloud | 92,39 mld | 59,87 | **41,78 mld** | 10,98 |
| S6 residuo | 12,50 mld | 11,08 | **10,92 mld** | 2,67 |
| **S3-S6** | **113,3 mld** | 76,5 | **58,2 mld** | **14,4** |
| S1 escluso non ICT | 1.286,3 mld | 1.140,0 | 1.132,4 mld | 549,1 |

### 2.4 Concessioni, quadro economico ANAC e atti degli incerti (nuovo in 0.4)

**Secondo campione di T4 concessione** (15 CIG in più, seme 20261107, giudizi nello stesso file) [V]:
- su 30 CIG i confermati sono **20 (67 %, intervallo 49-81 %)**;
- le 10 eccezioni sono concessioni in cui i canoni li paga la PA: servizi energetici ed efficientamento, impianti termici e trigenerazione, TPL, infrastrutture tecnologiche comunali, centri cottura;
- **regola v3 (I6):** una concessione il cui oggetto contiene quei termini torna incerta (35 CIG, 3,7 mld);
- sui 18 CIG del campione che la regola lascia tetti, i confermati sono **17 (94 %, intervallo 74-99 %)**.

**Quadro economico e SAL ANAC** (`tools/verifiche/imbuto_qe_sal.py`, dataset `quadro-economico` e `stati-avanzamento` del mirror) [V]. È una seconda fonte ANAC, indipendente dall'importo del lotto, e copre 442 dei 2.130 CIG.
- **Conferma gli errori d'importo:**
  - la telecamera da 4,7 miliardi ha un quadro economico di 10.000 €;
  - lo School Net da 648 milioni ne ha 10.000;
  - i ricambi Hytera da 1,03 miliardi ne hanno 20.000.

  Gli 8 errori con quadro economico valgono in tutto **70.150 €**, contro i 10,1 miliardi dichiarati.
- **Regola E4:** per un incerto o un errore, se il quadro economico è positivo e inferiore alla metà dell'importo dichiarato, vale il quadro economico. Riguarda 107 CIG + 8 errori, quasi tutti in S1.
  - Per l'ICT, per esempio: adesione ad AQ cybersicurezza di una ASL da 60 milioni a 0,6; supporto Nutanix da 79,5 milioni a 0,79 (consuntivo); sviluppi del Ministero dell'Interno da 63,3 a 7,9.
  - La precisione di E4 non è misurata: il quadro economico registra spesso la sola base d'asta.
- **SAL certificati:** 41 CIG, 0,40 miliardi, di cui 0,15 negli strati ICT. È l'unica misura di **spesa effettivamente eseguita** disponibile in open data per questi CIG.

**Atti degli incerti ICT, ricerca sul web** [V, esito negativo]:
- 6 ricerche per codice CIG hanno dato **0 risultati pertinenti**: il motore non indicizza i codici, come già visto con i codici PPdF;
- 4 ricerche per ente e oggetto (ASPAL, ENPAIA, ARIA, Careggi) hanno dato 0 determine con l'importo del CIG. Si trovano solo atti di altri enti o del padre;
- con una resa così bassa, la ricerca uno per uno non è proseguita: costerebbe ~80 ricerche per una resa attesa vicina a zero. La via utile è l'accesso agli atti dell'ente, cioè «Bandi di gara e contratti» o albo, per le stazioni appaltanti dei 79 CIG (R54).

**Strati dal 2024 (v3):**
- S3-S6 resta a **58,3 miliardi**, di cui 14,4 incerti in 79 CIG ICT;
- S5 scende a 41,6 miliardi;
- S1 escluso scende da 1.132 a 998 miliardi, per effetto di E4 sulle forniture non ICT (precisione da misurare).

### 2.5 Ultimo giro: sezioni AT degli enti, precisione di E4, chiusura (nuovo in 0.5)

**Visita delle sezioni «Bandi di gara e contratti»** dei 55 enti titolari dei 79 CIG ICT incerti, con lo strumento già usato per #62 (`tools/convenzioni/fuori_piattaforma_at.py`):
- sito ricavato da IndicePA (API CKAN); browser headless, almeno 5,5 secondi fra le richieste, mai login né CAPTCHA;
- ingresso in `lavoro/imbuto/at79/derivati.csv`, esito in `esiti/2026-11-06/imbuto/at79-visite.csv` [V].

| esito | enti |
|---|---:|
| sezione «Bandi di gara e contratti» raggiunta | 22 |
| sito irraggiungibile | 9 |
| sezione AT senza bandi / AT non trovata | 3 / 1 |
| sito assente in IndicePA | 2 |
| bloccata | 3 (+1 CAPTCHA del cruscotto ANAC a cui rimanda l'AT) |
| **totale visitati** (64 CIG) | **40** |

- **CIG trovati nelle pagine: 0. Allegati con l'importo: 0.** Il giro si è fermato da solo dopo un blocco di 20 enti a resa zero, come previsto dalla regola dello strumento.
- **Blocchi**, aggiunti a `report/convenzioni/blocchi-accesso.csv` e da validare nel monitoraggio PVL/AT (R45/R46):
  - SOGEI e CINECA: HTTP 403;
  - Università di Bari: CAPTCHA Radware;
  - ASL Pescara: l'AT rimanda al cruscotto ANAC, protetto da reCAPTCHA.
- **Conclusione:** per gli attuativi di AQ e le adesioni PSN l'importo dell'ordinativo **non è raggiungibile da fonti aperte**, né dal CIG (PVL, motori), né dalle sezioni AT. Resta l'accesso agli atti, escluso per ora. Gli **79 CIG (14,4 mld) restano incerti** e sono il perimetro di R54.

**Precisione di E4** (quadro economico al posto dell'importo dichiarato). Campione casuale di 15 dei 115 CIG E4, seme 20261108, giudizi in `campione-e4-giudizi.csv` [V]:
- **l'importo dichiarato è errato: 14/15 (93 %, intervallo 70-99 %)**. Esempi: asfaltatura comunale da 198 milioni, buoni pasto di un comune da 2,9 miliardi, marcatore laser da 417 milioni;
- **il quadro economico è plausibile: 9/15 (60 %, intervallo 36-80 %)**. Negli altri casi è anch'esso implausibile (poche decine di euro) o parziale;
- in 46 dei 115 CIG il rapporto fra dichiarato e quadro economico è una potenza di 10 esatta. È il segno di un errore di separatore decimale o di unità all'immissione (R51).
- **Lettura:** E4 è affidabile per togliere l'importo errato, meno per sostituirlo. L'effetto sugli strati ICT è trascurabile: il quadro economico vale in tutto pochi milioni.

**PNRR 1.1, ultimo giro mirato:**
- una ricerca sui decreti ASL/AO (multimisura 2023) trova solo atti degli enti che citano i decreti di finestra 48-x/2023 (per esempio ASL BT, 68.100 € a valere sull'1.1), non i decreti stessi;
- la Presidenza pubblica solo la prima e la seconda finestra;
- **chiuso a 16 decreti, 537,6 M€ (77 %)**. Il resto è in R50.

### 2.6 CIG contati due volte (nuovo in 0.6, R53)

`imbuto.py` salta nei file annuali solo i CIG degli aggiornamenti mensili. Un CIG che compare due volte nello stesso file annuale viene quindi contato due volte, in numero e in euro. Succede **solo nei file 2024 (3.773 CIG) e 2025 (4.089)**. `tools/verifiche/imbuto_doppioni.py` ricostruisce le righe contate (stesse fonti, stesso filtro sull'anno, stesso salto del delta) e trova le ripetizioni.

**I conti tornano** [V]:
- le righe ricostruite sono 5.713.798, uguali al riepilogo;
- quelle in eccesso sono 11.043;
- i CIG distinti sono 5.702.755 = righe meno eccesso.

`ict.csv` non è stato riscritto, perché la via 6 in corso lo usa: la correzione è applicata ai totali.

| strato, dal 2024 | righe in eccesso | euro in eccesso | CIG corretti | euro dopo tetti e doppioni |
|---|---:|---:|---:|---:|
| S1 escluso non ICT | 8.387 | 7,83 mld | 3.208.146 | 990,2 mld |
| S3 convenzione o lotto | 4 | **1,22 mld** | 893 | **1,32 mld** |
| S4 marchio | 33 | 0,005 mld | 8.016 | 3,01 mld |
| S5 ICT non cloud | 1.744 | 1,47 mld | 226.086 | 40,18 mld |
| S6 residuo | 312 | 0,30 mld | 55.634 | 10,77 mld |
| **S3-S6** | 2.093 | 2,99 mld | | ~~55,3 mld~~ **circa 55,7 mld** (stima 0.12) |

Altri dettagli [V]:
- nel residuo S6 i doppioni sono G1 16 righe (0,22 mld), G2 12, G3 75, G4 209;
- nel 2020-2023 non ci sono doppioni;
- i 4 doppioni di S3 sono grandi CIG di convenzione, già trattati come tetti o incerti in § 2.2-2.4: la seconda copia non era mai stata tolta.

I conteggi per gruppo differiscono da quelli della revisione della via 6 (13 in G1, 52 in G3). Qui si contano tutte le righe in eccesso, comprese le copie oltre la seconda.

**Correzione in 0.12 (R53, 9/11/2026).** Verifica `tools/verifiche/imbuto_cig_ripetuti.py` (`--mirror` sul server), esito `esiti/2026-11-09/imbuto/cig-ripetuti.json`; dettagli in `report/metodo/imbuto.md`, criticità «CIG ripetuti con strati diversi» [V].
- **Causa:** nei file annuali 2024 e 2025 un CIG ha una riga per ogni CPV. Anno, importo e testo sono identici fra le righe e cambia solo il CPV (982 dei 1.016 CIG ripetuti in `ict.csv`; gli altri 34 hanno righe identiche).
- **Eccesso vero dal 2024 in S3-S6:** 1.509 righe e 2,565 mld (S3 1,216, S4 0,005, S5 1,065, S6 0,278), non 2,99. `imbuto_doppioni.py` toglieva anche righe che la 0.3.1 metteva in S1 (285 CIG, 0,267 mld) e copie in più di 87 CIG (0,159 mld).
- **Totale S3-S6 dal 2024, una riga per CIG:** circa **55,7 mld** (+0,43 mld, quasi tutto S5). È una **stima**: il valore esatto si avrà alla rigenerazione con la regola imbuto 0.3.4 (`DEDUP_CPV`), dopo la via 6, perché va combinato con i tetti.
- **Strati incoerenti:** 152 CIG ripetuti stanno insieme in S5 e in S6, e lo strato dipende dalla riga tenuta. La regola 0.3.4 classifica con il più basso dei CPV ICT del CIG; l'effetto stimato fra S6 e S5 è di 47 CIG e 23,2 M€.

### 2.7 Anteprima della rigenerazione 0.3.4 (#71, nuovo in 0.14)

**Prova a secco, non applicata.** L'imbuto ufficiale resta 0.3.1 (3/11): la rigenerazione si fa a via 6 finita, perché la via 6 legge `ict.csv`. La prova calcola sul mirror ANAC quattro varianti, cambiando una cosa alla volta: A = 0.3.4 (R53 «una riga per CIG col CPV ICT minimo», perimetro CPV 0.3.3, lente v4.3), B senza R53, C col perimetro del 3/11, D con la lente del 3/11. Verifica `tools/verifiche/imbuto_prova_034.py tutto` (sul server, circa 2,5 h, un job alla volta) e `tools/verifiche/imbuto_prova_034_confronto.py 2026-11-09`; esiti `esiti/2026-11-09/imbuto-prova/` (`confronto.json`, `sezione-per-66.md`) [V].

**S3-S6 dal 2024 al netto dei tetti: 56,06 mld** (289.192 CIG, 114,38 mld dichiarati), contro 55,70 della base 0.3.1 contata una riga per CIG. La stima «circa 55,7» della 0.12 era quindi giusta per la base; lo scarto di +0,36 mld viene dai cambiamenti di regola. Netti per strato: S3 1,32, S4 3,03, S5 40,01, S6 11,70 mld [V].

| cambiamento, dal 2024 | CIG S3-S6 | mld netti | dove |
|---|---:|---:|---|
| R53, una riga per CIG (A − B) | +161 | +0,064 | 161 CIG da S1 a S5 |
| perimetro CPV 0.3.3 (B − C) | −1.992 | +0,479 | 79342 fuori (S5 −5.725); sw e connettività dentro (S6 +3.733, G1 +32) |
| lente v4.3 (C − D) | +1 | +0,004 | 354 CIG da S5 a S4 (marchi) |
| difetto della prima riga 0.3.2 (D − base) | −191 | −0,184 | CIG finiti in S1 per la riga tenuta |

- **CIG ripetuti:** da 1.016 a **0** in tutte le varianti; per A la verifica fallisce se ne trova [V].
- **Residuo S6 con la 0.3.4:** 59.406 CIG / 16,37 mld dichiarati (G1 227 / 8,53; G2 867 / 4,03; G3 13.437 / 3,16; G4 44.875 / 0,65) [V].
- **Selezione via 6:** dei 1.196 CIG G1+G3, 5 (27 M€) passano da S6 a S5; nessuno esce dall'imbuto [V].
- **29 G1 nuovi dal 2024 (3,82 mld dichiarati)** entrano col perimetro 0.3.3: 8 Consip SPC/connettività (i maggiori), 6 ASI «HW/SW» di missioni spaziali, 11 di multiutility, altri. Sul netto contano poco (+0,48 mld) perché i tetti SPC sono già classificati. Vanno in coda alla via 6 alla rigenerazione [V].
- **Revisione a mano degli 11 multiutility** (`tools/verifiche/imbuto_g1_segnali_deboli.py`, `g1-revisione.json`): 7 ICT veri (E-Distribuzione 6, A2A Smart City 1), **4 falsi per 29,2 M€** (Padania Acque 2 contatori smart, Sorical 2 lavori su rete idrica e contatori) [V].
- **Decisione aperta: proposta P1 (Fabio, #71).** Se il CIG entra solo per segnali deboli («connettività», «sw») e il CPV è 33, 38, 41-45 o 73, resta fuori. Sui 59 G1 nuovi dal 2020 escono 13 CIG / 0,467 mld (dal 2024 11 / 0,438 mld): i 4 falsi multiutility (0 ICT veri persi), 6 ASI, autoclavi ASST Bergamo Est, un lotto G.A.I.A. Misura su tutto S6 da fare alla rigenerazione (job pesante). **Non applicata.**
- **Limite:** le varianti C e D ricostruiscono regole e lente del 3/11 sostituendo moduli; D non coincide con la base per la deduplica della 0.3.2.


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

### 4.2 PNRR 1.1: chi è stato finanziato per migrare al PSN (nuovo in 0.3)

I decreti di finanziamento dell'Investimento 1.1 «Infrastrutture digitali» sono quindici:
- dodici sono su presidenza.governo.it, nella pagina «Criteri e modalità» archiviata il 6/11;
- tre (PAC pilota 2023, bis 2024, ter 2025) solo su assets.innovazione.gov.it.

Tutti sono archiviati con sha256. `tools/verifiche/pnrr11_decreti.py` legge l'elenco degli ammessi e prende CUP, ente e importo 1.1; per i multimisura prende la sola colonna 1.1. Ne escono `esiti/2026-11-06/pnrr11/finanziati.csv` e `decreti.json` [V].

- **Controllo interno:** in **15 decreti su 15** la somma delle righe coincide con un importo scritto nel decreto stesso. Solo il PAC pilota ter differisce di 2 € (312.798.116,16 contro 312.798.118,16).
- **Totale lordo: 524,2 milioni**, su 298 CUP e 274 enti. Il PAC pilota ter (312,8 M€, 20 PA centrali) ne fa il 60 %. Per esempio: Difesa 44,0 M€, Ambiente 50,2 M€, Interno-Vigili del fuoco 33,5 M€.
- **Controvalidazione:** PSN dichiara circa 700 milioni assegnati su 900 [R]. Lo spoglio ne trova **il 75 %**. Mancano le finestre i cui decreti non sono linkati dalla pagina, come la «fin 3.1» delle altre PAC 2023, che troviamo citata altrove. Le rinunce non sono sottratte.
- **Uso nell'imbuto:** il finanziamento PNRR è un tetto forfettario per la migrazione, versato a migrazione completata. È un **minimo** della spesa PSN dell'ente, non il suo contratto di utenza. Il collegamento CUP → CIG (dataset CUP ANAC) è il passo successivo.
- Raccomandazione R50 (elenco aperto dei finanziamenti con CUP) confermata: oggi lo spoglio richiede quindici PDF con tre impaginazioni diverse.

### 4.3 G1 e primi 1.000 G3 con la via 6 (top-5 punto 4, in corso, nuovo in 0.4)

Decisione di Fabio del 7/11: solo i primi 1.000 CIG di G3 per importo (stima 360 USD-eq, fermarsi oltre +20 %) e tutti i G1, guardati uno per uno.

- **Selezione** (`report/metodo/llm/imbuto-g1g3/selezione.json`): G1 **196 CIG unici** per 4,70 mld; G3 primi 1.000 per 1,55 mld (importo da 598 k€ in su). Il link PVL c'è per 112 G1 e 507 G3. Più 15 CIG del campione 611 che cadono in G1/G3 fuori selezione, classificati alla cieca come controllo.
- **Doppioni in `ict.csv`:** lo stesso CIG compare in più anni. Sono 13 righe in G1 e 52 in G3, e i 4,88 mld di G1 del § 4 li contano due volte: al netto G1 vale 4,70 mld. Va corretto in imbuto.py (R53).
- **Metodo:** Claude Sonnet in abbonamento sul server, con le istruzioni p3 (due assi con stato). Il modello apre per primo il link PVL, poi cerca gli atti dell'ente; ogni documento è archiviato con sha256. Una verifica a regole (`tools/llm/verifica_imbuto.py`) riporta a «incerto» ogni stato certo senza prova. Tutto è **proposta da revisionare**; i numeri non entrano nei totali finché non sono rivisti.
- **Numeri:** `esiti/imbuto-via6/via6-g1g3.json`, rigenerato ogni 30 minuti dal server (`tools/verifiche/imbuto_via6.py`). Contiene CIG ed euro per stato degli assi, gli euro che si spostano di strato (S1 non ICT, S5 ICT non cloud, incluso cloud per giurisdizione, resta S6), la precisione sul controllo e il consumo.
- **Primo parziale (6/11, ore 13:30, [V]):** classificati 28 G1 su 196 (2,75 mld) e 10 G3 su 1.000. Sono proposte da revisionare:
  - G1: 9 escluse non ICT (0,61 mld, verso S1); 13 ICT non cloud (1,11 mld, verso S5); 1 cloud extra-UE certo (44 M€); 5 restano incerte (0,98 mld);
  - G3: 1 verso S1, 1 verso S5, 8 restano incerte;
  - la fonte primaria (un atto che cita il CIG, archiviato) c'è in 8 casi su 38.
- **Consumo:** G3 a 0,32 USD-eq per CIG, cioè circa 320 sui 1.000 (stima 360, guardia a 432); G1 a circa 0,70 per CIG, cioè circa 140 in tutto. Con il tetto di 100 USD-eq al giorno il giro finisce in circa 5 giorni.
- **Ostacoli:** in 38 CIG, 16 documenti non pertinenti, 7 errori 404, 4 login, 3 errori 403, 1 PDF illeggibile (R53).

### 4.4 PNRR 1.1: decreto mancante e collegamento CUP → CIG (nuovo in 0.4)

- **Decreto aggiunto:** finestra 3 delle «altre PAC» di giugno 2023, 14 enti per 13,4 M€. L'abbiamo trovato su iss.it, non sulla pagina della Presidenza. I decreti sono ora **16, tutti coerenti** con i totali che dichiarano, per **537,6 M€ su 312 CUP e 288 enti**: il 77 % dei ~700 M€ [R]. Il resto (~160 M€) non è stato trovato in rete (R50).
- **CUP → CIG** (`tools/verifiche/pnrr11_cup_cig.py`, dataset ANAC `cup` del mirror):
  - **238 CUP su 312** hanno almeno un CIG, per 435 M€ finanziati (81 %), con 322 CIG;
  - 284 di quei CIG sono nel residuo S6, quasi tutti PSN;
  - **231 CUP sono legati a CIG PSN**: finanziati 431 M€, contro **2,20 mld** di importo dei CIG PSN collegati [V].
- **Lettura:**
  - il contributo PNRR copre circa **un quinto** del valore dei contratti PSN che finanzia;
  - in ANAC il valore del CIG è il contratto di utenza pluriennale, oppure, per qualche adesione, il valore della convenzione;
  - il resto lo paga l'ente con fondi propri negli anni del contratto.
- **Da fare:** confrontare, per gli stessi CIG, il finanziato con il SAL e con i ricavi PSN per ente, che oggi non sono pubblicati (R50).

### 4.5 Licenze e marchi: cloud sì o no (top-5 punto 5, nuovo in 0.6)

Perimetro: i CIG dal 2024 in S3/S4 con licenze, software d'infrastruttura, servizi professionali o telefonia («incerto: marchio o lotto noto»). Ogni CIG conta una volta sola, al netto dei tetti: **3.508 CIG, 5,29 mld dichiarati, 2,76 mld netti**. `tools/verifiche/imbuto_licenze.py` assegna a ogni CIG l'asse A (è cloud?), la via e la giurisdizione del prodotto, cioè la sede del produttore. Esito in `licenze-cig.csv` [V]:

| via | prova | CIG | euro netti | esito |
|---|---|---:|---:|---|
| L1 capitolato | Oracle da Licenze multibrand 6: il capitolato prevede solo prodotti on premises, consegnati via edelivery (dossier 9660108D4B) | 7 | 78,7 M€ | non cloud |
| L2 prodotto | VMware (vSphere/VCF) e Cloudera (CDP Private), software installato presso l'ente, se l'oggetto non dice «cloud» | 669 | 650,4 M€ | non cloud |
| L3 testo SaaS | l'oggetto nomina un servizio erogato dal produttore (M365/O365, Azure, Dynamics 365, OCI, RISE, SuccessFactors, Workspace, AWS…) | 288 | 168,2 M€ | **cloud** |
| L4 testo on premises | l'oggetto nomina solo prodotti installati (Windows Server, SQL Server, CAL, perpetue, Oracle Database/WebLogic) | 378 | 41,7 M€ | non cloud |
| L5 categoria | servizi professionali e telefonia: consulenza e connettività, non servizi cloud | 482 | 120,6 M€ | non cloud |
| misto esplicito | nomina sia SaaS sia on premises | 15 | 20,2 M€ | misto |
| **resta incerto** | «licenze Microsoft», adesione EA, «licenze Oracle/SAP» senza dettaglio | **1.669** | **1.680 M€** | incerto |

Lettura:
- **cloud certo: 168 M€**. Per giurisdizione del prodotto: extra-UE 141 M€ (Microsoft 114, Oracle 22), UE 25 M€ (SAP), IT 0,7 M€ [V-testo].
- **Non cloud certo: 892 M€.** VMware da solo vale 595 M€: è l'infrastruttura interna su software statunitense (Broadcom), voce «datacenter interni».
- **Il residuo è 1,68 mld:**
  - Microsoft 799 M€ (968 CIG);
  - Oracle 401 M€;
  - marchio non attribuito 396 M€;
  - SAP 83 M€.

  Il carrello (SKU) di questi contratti sta solo nell'atto dell'ente o nell'ordinativo, come per gli attuativi (§ 2.5). Per Microsoft la forbice resta quella di `ea-quota-cloud-elaborazione.md`: almeno il 44 % cloud nell'EA6 secondo i pesi di gara, che ne danno solo un limite inferiore; il valore vero sta fra 0 e 100 %.
- **Atti:**
  - i link PVL coprono 746 dei 1.682 CIG incerti o misti, ma solo 215 M€;
  - i primi 30 per importo puntano quasi tutti alla home di una piattaforma di e-procurement (Terna, Cineca, Banca d'Italia, Regione Calabria), non all'atto;
  - la lettura dei contratti, cioè il censimento dei primi 50 EA con il campione già disegnato, resta da fare e richiede gli atti degli enti (R23, R54).

### 4.6 Censimento dei prodotti negli EA Microsoft e nelle licenze Oracle (nuovo in 0.7)

**Come:** `tools/verifiche/ea_censimento.py` e gli atti in `esiti/2026-11-06/imbuto/ea-campione.csv`, tutti archiviati con sha256.
- **Vie tentate per i primi 50 EA Microsoft e i primi 20 Oracle per importo:**
  - link PVL: per i primi 30 puntano alla home di una piattaforma. La ricerca del CIG dentro le piattaforme da anonimo non è stata fatta in questo giro, perché ogni piattaforma ha una sua ricerca (da fare);
  - sezioni AT: non ripetute per questi enti, perché il giro del § 2.5 su enti dello stesso tipo ha reso zero;
  - **10 ricerche web** per ente, oggetto e anno, sugli enti più grandi: Roma Capitale, Regione Emilia-Romagna, INSIEL, ANAS, Regione Campania, ASL Caserta, INPS e altri;
  - ricerche per edizione dell'EA (EA8, EA9) con «M365» e prezzo unitario.
- **Resa sui primi 50:** 1 atto su 50. È MAECI, determina 1019/2025: EA9, 7,71 M€ IVA esclusa = 9,41 M€ del CIG B89CF8349C. Per gli altri 49 la ricerca non ha trovato l'atto.
- **Resa per edizione:** 7 atti di altri enti, più piccoli, con il dettaglio dei prodotti, quasi tutti con i prezzi unitari dell'ordinativo Consip.

**Esito Microsoft** [V sugli atti; la quota MAECI usa i prezzi unitari EA8 di un altro atto, quindi è una stima]:

| atto | anno, edizione | prodotti | quota cloud |
|---|---|---|---:|
| MAECI (fra i primi 50) | 2025, EA9 | M365 E3 per 8.000 utenti, CIS Suite, SQL Server, RDS CAL | ~92 % |
| Consiglio regionale del Lazio | 2023, EA8 | M365 E3/E5, Core CAL, Office Pro Plus SA, Windows Server | 92 % |
| Autorità dei trasporti | 2024, EA8 | O365 E5/E3, EMS E3, Visio Online | 100 % |
| Autorità dei trasporti | 2026, EA8 | Copilot add-on, Copilot Studio | 100 % |
| Comune di Firenze | 2024, EA7 | O365 E1 | 100 % |
| Città metropolitana di Firenze | 2025, EA9 | 365 Apps for Enterprise, Windows Enterprise | 57 % |
| Regione Emilia-Romagna | 2024, EA7 | Copilot per M365 | 100 % |
| Ministero della giustizia (UCAN) | 2026, EA9 | Dynamics 365 Finance & Operations | 100 % |

Sintesi del campione:
- quota cloud pesata **92 %**, media per atto 93 %;
- **8 atti su 8** a prevalenza cloud (intervallo di Wilson 68-100 %);
- giurisdizione del prodotto: **extra-UE** (Microsoft, USA) per tutti.

**Forbice EA aggiornata** (aggiorna `report/convenzioni/ea-quota-cloud-elaborazione.md`):
- il residuo Microsoft incerto è di 819 M€;
- applicando l'intervallo del campione, la quota cloud sta fra **554 e 819 M€**, contro la forbice 0-100 % della 0.6;
- **non è ancora una misura**: il campione non è casuale, è fatto degli atti che si trovano in rete (enti piccoli e autorità) più MAECI. Potrebbe sovrastimare il cloud, se i grandi enti comprano più licenze on premises;
- il dato certo resta per contratto: 9,4 M€ (MAECI) dei primi 50.

**Oracle, primi 20 incerti (261 M€):**
- tutti gli oggetti parlano di supporto, rinnovo, manutenzione, Exadata o licenze; nessuno nomina cloud o OCI;
- classificazione: **on premises probabile**, non certo, perché nessun atto è stato letto. Giurisdizione extra-UE;
- è coerente con il capitolato di Multibrand 6, che non prevede OCI.

**Strato licenze dopo 0.7:**
- cloud certo 168 M€ + MAECI 8,7 M€ (quota cloud di 9,4) ≈ **177 M€**;
- non cloud certo 892 M€;
- Oracle on premises probabile 261 M€;
- Microsoft incerto 810 M€, con forbice cloud 0,55-0,81 mld;
- resto incerto (Oracle oltre i primi 20, SAP, marchio non attribuito) ≈ 0,62 mld.

### 4.7 Piattaforme di e-procurement da anonimo, EA mancanti, Oracle (nuovo in 0.8)

**Adattatori per piattaforma** (`tools/acquisizione/piattaforme_cig.py`, riusabile). Le regole sono le solite: UA da browser con l'URL del progetto, almeno 6 secondi fra le richieste, mai login né CAPTCHA, ogni pagina e documento archiviato con sha256.

| famiglia | come lavora |
|---|---|
| `portaleappalti` (Maggioli/Eldasoft) | dalla pagina della procedura passa ad «Altri atti e documenti» e scarica i documenti pubblici |
| `esop` (Jaggaer) | cerca il CIG nell'elenco pubblico delle opportunità; un rimando a `login.html` è un blocco |
| `generico` | cerca il CIG nella pagina e in fino a 15 sottopagine della stessa sezione |

Esito sui 7 CIG dei primi 50 EA e dei primi 20 Oracle che hanno un link PVL (`piattaforme-esiti.jsonl`) [V]:
- **CINECA, PortaleAppalti: raggiunto da anonimo.** 2 documenti pubblici, fra cui il provvedimento di aggiudicazione. È Oracle in **ULA** (licenze ULA e ULA Capped, manutenzione, giornate di consulenza): **nessun servizio cloud**;
- Banca d'Italia (esop): il CIG non è nell'elenco pubblico delle opportunità;
- Terna (esop): la home rimanda al login, quindi è un blocco. L'adattatore non lo ha riconosciuto perché il rimando passa da JavaScript, ed è da correggere;
- Regione Calabria, CSI Piemonte, Hera (generico): CIG non trovato nella pagina né nelle sottopagine.

**EA Microsoft mancanti** (49):
- altre 3 ricerche per ente e oggetto (ANCI, Azienda sanitaria dell'Alto Adige, Unione dei comuni della Bassa Romagna) hanno dato **0 atti dell'ente**;
- con 13 ricerche in tutto e un solo atto trovato fra i primi 50, la ricerca web per ente non rende. Restano le sezioni AT, già a resa zero, e l'accesso agli atti, escluso.

**Oracle con lo stesso metodo:** 1 atto fra i primi 20 (CINECA, sopra) e 4 di enti fuori dai primi 20, trovati con una ricerca per prodotto (`oracle-campione.csv`) [V]:
- ISTAT: accordo ULA con hardware, software e supporto;
- MAECI: ULA database per i servizi consolari. OCI compare solo nei crediti di formazione Oracle University;
- Ministero della giustizia (DIT): supporto ULA;
- Lepida: contratto Oracle 2023-2026 per gli enti dell'Emilia-Romagna.

**0 atti su 5 contengono servizi cloud** (intervallo 0-43 %). La classificazione «on premises probabile» dei primi 20 Oracle (261 M€) è sostenuta da questi atti. Diventa **certa solo per CINECA** (14,4 M€).

**Rigenerazione di imbuto 0.3.2:** non è stata fatta. La via 6 (`giro_imbuto.sh`) è ancora in corso e il suo guardiano la rilancia finché mancano esiti. L'esecuzione automatica a fine via 6 con una regola cron non è stata autorizzata: va lanciata a mano (`python tools/analisi/imbuto.py 2020` sul server) quando `giro_imbuto.sh` ha finito.

### 4.8 TED come seconda fonte degli aggiudicatari (nuovo in 0.9)

**Regola:** se un CIG non ha aggiudicatari in ANAC e il suo avviso di aggiudicazione TED nomina il vincitore con la P.IVA, il vincitore TED entra come aggiudicatario. La via è registrata come «TED» per la lente fornitore.

**Precisione:** dove ci sono entrambe le fonti, la P.IVA TED coincide con quella ANAC nell'**89 %** dei casi. La misura è dell'agente del mirror TED (#27, `tools/verifiche/ted_esiti.py`) e qui non è stata rifatta.

**Esito** (`tools/verifiche/ted_imbuto.py`, `esiti/2026-11-06/imbuto/ted-vincitori.{csv,json}`) [V]:
- 84 CIG hanno un vincitore TED e nessun aggiudicatario ANAC;
- 72 sono nell'imbuto: S5 55 CIG per 156 M€, S0 9, S4 1 (Oracle Italia, già attribuito per marchio), S6 7 per 19 M€ (G1 1, G3 6).

**Effetto sugli strati: nessuno.** La giurisdizione si attribuisce al prodotto, non al fornitore (AGENTS.md § 2). I 7 vincitori in S6 sono integratori e rivenditori italiani (N&C, R1, SMITT, Aditinet, Converge, un RTI con Innovery): non sono produttori cloud, quindi non spostano nessun CIG verso S4. Il vincitore TED serve alla lente fornitore e alla via 6, come indizio nella lettura degli atti.

### 4.3.1 Via 6 al 9/11/2026: G1 completo, G3 parziale (nuovo in 0.10)

**Parzialità dichiarata.** Fotografia del 9/11/2026, ore 12 circa: 725 CIG con esito in `report/metodo/llm/imbuto-g1g3/verificati.jsonl` (196 G1, 514 G3, 15 di controllo). G3 è al 51 % dei CIG e al 74 % degli euro della selezione; il giro continua sul server e i numeri cambieranno. La verifica a regole (`tools/llm/verifica_imbuto.py`, regole R1-R2, A1-A2, B1) ha corretto almeno un campo in **604 dei 725 esiti**, quasi sempre abbassando la confidenza senza fonte primaria (R2, 443 casi) o riportando un asse a «incerto» (A1 115, A2 109, B1 40) [V, dal log della verifica]. Tutto è **proposta della via 6 da revisionare**: non entra nei totali dei § 1-4 finché non è rivisto. Esito congelato: `esiti/2026-11-09/imbuto/via6-g1g3.json` [V].

| gruppo | verso S1 (non ICT) | verso S5 (ICT non cloud) | cloud certo | resta incerto (S6) |
|---|---:|---:|---:|---:|
| G1, 196/196 CIG (4,70 mld) | 62 CIG, 1,21 mld | 65 CIG, 1,77 mld | 5 CIG, 83 M€ (extra-UE 54, IT 15, UE 14) | 64 CIG, 1,64 mld |
| G3, 514/1.000 CIG (1,15 di 1,55 mld) | 176 CIG, 400 M€ | 94 CIG, 206 M€ | 8 CIG, 22 M€ (IT 11, UE 10, extra-UE 2) | 236 CIG, 517 M€ |

- **Cosa vuol dire:** in G1 il 64 % degli euro esce dall'incerto, ma quasi tutto verso «non ICT» o «ICT non cloud»; il cloud certo è l'1,8 %. G3, per la parte vista, ha lo stesso profilo.
- **Prove:** la fonte primaria (un atto che cita il CIG, archiviato con sha256) c'è per 55 G1 e 50 G3. Il resto si regge su ricerche e deduzioni: per questo serve la revisione.
- **Precisione sul controllo** (campione 611, a sua volta via 6 + regole, non verità assoluta): asse A 20 su 23 (Wilson 68-96 %), asse B 8 su 9 (57-98 %). Il campione è piccolo.
- **Ostacoli:** 54 errori 403, 52 errori 404, 45 login, 10 PDF illeggibili, 8 link PVL rotti, 220 altri (soprattutto documenti non pertinenti).
- **Consumo reale:** G1 138 USD-eq; G3 167 USD-eq per 514 CIG, cioè 0,33 per CIG. La proiezione sui 1.000 è 326, sotto la stima di 360 e la guardia di 432.

### 4.3.2 Revisione delle proposte della via 6 (#55, #66, nuovo in 0.13)

**Cosa.** Le proposte della via 6 di passaggio a «certo» (verso S5, ICT non cloud, e verso cloud certo; S1 escluso) entrano nei totali solo se reggono a quattro criteri (`tools/verifiche/imbuto_via6_revisione.py`, docstring):

- **C1**, una fonte primaria: un atto archiviato con sha256 il cui testo cita il CIG;
- **C2**, le regole di `verifica_imbuto.py` rieseguite danno lo stesso esito, con campi coerenti con lo stato;
- **C3**, per il cloud, il prodotto porta alla giurisdizione del dizionario dei marchi (`config/marchi_cloud.yaml`);
- **C4**, una seconda lettura cieca (Claude Opus, istruzioni diverse, solo gli estratti degli atti archiviati, niente web) dice la stessa cosa con certezza alta.

**Stato al 9/11/2026, sera [V].** La seconda lettura delle 176 proposte del primo `prepara` è finita (30 pacchetti su 30): **175 lette**, 1 rimasta senza lettura (G1, 13,1 M€). Nel frattempo il giro G3 è salito a 765 CIG su 1.000 e ha prodotto **38 proposte nuove** (36 S5, 2 cloud): sono in lettura in 7 pacchetti aggiuntivi (r031-r037) sotto il tetto condiviso e fino ad allora restano «da leggere», fuori dai totali. Esito: `esiti/2026-11-09/imbuto/revisione-via6.json`, coda `revisione-coda-discordi.csv`.

**Concordanza della seconda lettura** (CIG e M€; «non confermato» vuol dire che la seconda lettura non dà la stessa risposta con certezza alta, senza contraddirla):

| gruppo e strato proposto | concorde | non confermato | discorde | da leggere |
|---|---:|---:|---:|---:|
| G1 verso S5 (65) | 24, 963,5 | 30, 651,5 | 10, 143,8 | 1, 13,1 |
| G1 cloud certo (5) | 3, 31,6 | 1, 43,5 | 1, 8,0 | 0 |
| G3 verso S5 (130) | 28, 60,5 | 41, 92,5 | 25, 53,2 | 36, 34,4 |
| G3 cloud certo (10) | 4, 12,8 | 4, 9,6 | 0 | 2, 1,9 |
| CTL, controllo (4) | 3, 0,7 | 0 | 1, 0,1 | 0 |
| **tutti (214)** | **62** | **76** | **37** | **39** |

Sui 99 casi letti con certezza da entrambe le parti l'accordo è 62 su 99.

**Quanto entra nei totali** (tutti e quattro i criteri; CTL compreso: 1 CIG S5 e 2 cloud IT, 0,8 M€):

| destinazione | proposti | C1 fonte primaria | C1+C2+C3 | entra (C1-C4) |
|---|---:|---:|---:|---:|
| verso S5 (ICT non cloud) | 197 CIG, 2,01 mld | 49 CIG, 640,4 M€ | 47 CIG, 573,3 M€ | **15 CIG, 397,4 M€** |
| cloud certo, IT | 9 CIG, 27,2 M€ | 5 CIG, 11,8 M€ | 5 CIG, 11,8 M€ | **2 CIG, 0,4 M€** (entrambi CTL) |
| cloud certo, UE | 4 CIG, 24,2 M€ | 4 CIG, 24,2 M€ | 4 CIG, 24,2 M€ | **4 CIG, 24,2 M€** |
| cloud certo, extra-UE | 4 CIG, 56,4 M€ | 2 CIG, 2,6 M€ | 2 CIG, 2,6 M€ | **0** |

- **Cosa vuol dire:** delle proposte via 6 regge il 20 % degli euro verso S5 e nessun euro di cloud extra-UE. Il filtro più severo è C1: 1.024 M€ di S5 hanno una seconda lettura concorde ma nessun atto che citi il CIG, e restano proposte.
- **I discordi (37, in coda per Fabio):** 33 sono proposte S5 che la seconda lettura dice **non ICT** (stampanti a noleggio, consumabili, cablaggio e lavori di rete, scuolabus, apparecchiature sanitarie): se Fabio conferma, vanno verso S1. 3 S5 sono **cloud** per la seconda lettura (A038DA0645 e B22FF5E298, adesioni agli AQ Consip Public Cloud IaaS/PaaS; B2B394AF2D, migrazione in cloud, 18,9 M€). 1 cloud IT (BC74911F16, Aruba, 8,0 M€) è **non cloud** per la seconda lettura.
- **Effetto sui § 1-2:** nessuno per ora. Lo spostamento da S6 a S5 non cambia il totale S3-S6; i 24,6 M€ di cloud certo (IT 0,4, UE 24,2) entreranno nella superficie del § 1 alla rigenerazione dell'imbuto, insieme alle decisioni sulla coda.

### 4.3.3 Ricerca mirata degli atti per il criterio C1 (#66, segnaposto 0.14)

*Segnaposto.* Un'altra linea di lavoro cerca in modo mirato l'atto che cita il CIG per le proposte via 6 che oggi falliscono solo C1 (esiti attesi in `esiti/<data>/imbuto/c1-*`). L'esito si inserisce qui alla consegna; fino ad allora valgono le cifre del § 4.3.2.

### 4.9 CIG derivati da accordo quadro senza padre (#50, nuovo in 0.10)

Un CIG discendente da AQ o convenzione eredita il prodotto dal padre. Se il campo `cig_accordo_quadro` è vuoto o punta a un CIG inesistente, l'eredità si perde. Verifica `tools/verifiche/cig_aq_tipo.py`, esito `esiti/2026-11-09/cig-aq/tipo.json` (commit 794e84c1) [V].

- **Nell'imbuto** (`ict.csv`, 2020-2026): 55.114 CIG ICT discendenti per 89,2 mld. Di questi **1.666 non sono collegabili, per 734 M€ (0,82 %)**. Il 2024 pesa 432 M€, il 2025 223 M€.
- **Sulla base CIG intera, 2025:** 356.312 discendenti; 3.944 con il campo vuoto, 14.267 con un padre inesistente; collegabili il 94,9 %.
- **Coerenza dei padri:** nel 2025, 171.063 dei 338.101 padri esistenti non sono a loro volta AQ o convenzione: 170.751 sono «contratto d’appalto», contro 119.014 accordi quadro e 40.409 convenzioni. I padri inesistenti hanno tutti 10 caratteri, come un CIG valido (10.993 iniziano per «B», 882 per «b» minuscola): sono CIG plausibili ma assenti dalla base, non campi sporchi. Questi conteggi, prima in uno script di lavoro, sono ora nella verifica (campi modalita_padre_per_anno e forma_padre_inesistente_per_anno, regola #47).
- **Effetto:** trascurabile sugli strati; resta la raccomandazione ad ANAC sulla validazione del campo (P15).

### 4.10 BDAP: quanto paga lo Stato centrale in ICT (#67, nuovo in 0.10)

Dalla pagina [BDAP](/progetto/bdap/) (versione 0.1, 9/11/2026). Verifica `tools/verifiche/bdap_ict_stato.py`, esito `esiti/2026-11-09/bdap/ict-stato.json` con lo sha256 di ogni file [V].

- **Via 1, pagamenti per codice gestionale ICT (11 codici):** 987 M€ nel 2022, 1.199 nel 2023, **1.141 nel 2024**, 1.286 nel 2025 [V].
- **Via 2, controvalidazione per classificazione economica di 3° livello** (rendiconto 2024 per piano di gestione): **979 M€** [V]. Le due vie differiscono del 14 %.
- **Sanità:** voce BA1620 del CE SSN 2023 (servizi di assistenza informatica), 604 M€, denominatore minimo [V].
- **Rapporto CIG ICT / pagato ICT 2024, per ministero (abbinamento per nome, superato in 0.11):** Interno 2,0; Difesa 3,5; Infrastrutture 2,2; MEF 0,17; Giustizia 0,03 [V sui conteggi, **stima** sull'interpretazione]. Per codice fiscale e con la quota annua dei contratti (§ 4.12): Giustizia 0,96 (artefatto del nome), MEF 0,25; il buco residuo è il MEF, circa 0,3 miliardi l'anno. Un CIG vale il contratto pluriennale e il pagato è la cassa di un anno: il rapporto non è una copertura. Il buco residuo è del MEF (Sogei in-house senza CIG per Ragioneria, Tesoro e Amministrazione generale, R71).

### 4.11 Riepilogo del residuo S6: documenti dai livelli L3, MePA, L4 (#57, nuovo in 0.10)

Per il residuo S6 si cercano gli atti che dicono il prodotto, livello per livello ([acquisizione dei documenti](/progetto/acquisizione-documenti/)). Verifica `python tools/verifiche/residuo_s6_riepilogo.py 2026-11-09`, esiti `esiti/2026-11-09/acquisizione/residuo-s6-riepilogo.json` e `esiti/2026-11-09/imbuto/residuo-s6-per-66.csv`, rieseguita il 9/11/2026 [V]. In ingresso 28.583 CIG del residuo, di cui 16.403 senza link PVL (4.352 enti).

| livello | CIG provati | CIG trovati | con documenti | documento che cita il CIG | stato |
|---|---:|---:|---:|---:|---|
| L3, link PVL | 11.589 (2,31 mld) | 2.483 (906 M€) | 1.076 (783 M€) | **453 (262,1 M€)** | finito |
| MePA, vetrina pubblica | 591 (419 M€) | 0 | 0 | 0 | finito: nessuna pagina pubblica |
| L4, sezione «Bandi di gara e contratti» | 4.007/4.352 enti | 4.393 (7,36 mld) | 981 (650 M€) | **82 (42,6 M€)** | finito 9/11 (#68); ripasso #73 |

- **Passaggio potenziale da incerto a leggibile:** 535 CIG per 304,7 M€ hanno un documento archiviato che cita il CIG. Nel gruppo S6/G3 sono 454 su 21.525 CIG (2,1 %), cioè 81,6 M€ su 3,84 mld [V]. È un potenziale: gli strati **non sono ricalcolati** finché quei documenti non sono letti e classificati (via 6).
- **Perché così poco:** in L3 3.292 link portano alla sola home della piattaforma (R66); 1.126 CIG su 381 host sono esclusi da robots.txt, 641 danno 403, 115 anti-bot, 115 login (R68); gli atti trovati spesso non riportano il CIG (L3: 453 su 1.076; L4: 79 su 871, R67). In L4, 261 enti hanno un blocco; degli enti elaborati 1.319 danno CIG trovati, 901 non hanno una sezione «Bandi» riconoscibile, 436 errore di rete, 394 sito ignoto, 176 pagina quasi vuota (resa da JavaScript).
- **Costo:** L3 33.826 richieste, L4 21.885; nessun token.
- **Ripasso in corso (#73):** i 436 enti in errore di rete e 345 rinviati per robots.txt (notte), e i 176 enti con pagina quasi vuota più 41 della Difesa con browser headless (L4-js). Parziale alle 20:12 del 9/11: 9 enti su 217, 34 CIG trovati, 0 documenti che citano il CIG. Le cifre si aggiornano a fine giro con la stessa verifica.
- **Dopo L4, accesso civico (#58):** l'elenco unico rigenerato a L4 finito ha 28.804 voci (756 convenzioni + 28.048 CIG del residuo, esclusi i 535 sopra), 6.624 enti, 775 senza PEC [V, `tools/accesso_civico/elenco_mancanti.py`]. L'invio è una decisione di Fabio.

### 4.12 BDAP fase 2: codice fiscale, quota annua, Sogei, SIOPE (#67, #30, nuovo in 0.11)

Dalla pagina [BDAP](/progetto/bdap/) (versione 0.2, 9/11/2026). Verifiche, dal mirror: `tools/verifiche/bdap_ict_stato.py`
(esito `esiti/2026-11-09/bdap/ict-stato.json`), `tools/verifiche/bdap_cig_ministeri_cf.py` (`esiti/2026-11-09/bdap/cig-ministeri-cf.json`),
`tools/verifiche/siope_bdap_vs_diretto.py 2024` e `2025` (`esiti/2026-11-09/siope/bdap-vs-diretto-<anno>.json`), tutte con lo sha256 dei file.

- **Stazione appaltante → ministero per codice fiscale** (IndicePA: CF degli enti e degli uffici di fatturazione,
  2.661 CF ministeriali) invece che per nome: i CIG ICT ministeriali 2020-2026 passano da 10.758 a 23.644, da 5,0 a
  8,2 miliardi [V]. Per nome se ne perdevano 13.007 per 3,24 miliardi.
- **Giustizia:** il buco era un artefatto della regola sul nome. Nel 2024 i CIG ICT sono 359 per 213 M€ (erano 13 per
  9); la quota 2024 dei contratti attivi vale **0,96** volte il pagato ICT (304 contro 315 M€) [V sui conteggi, stima
  sull'interpretazione].
- **MEF:** il buco resta. Nel 2024 quota dei CIG attivi 97 M€ contro 388 pagati (**0,25**); 0,36 nel 2025 [V]. I
  contratti in-house con Sogei che hanno un CIG con SA del MEF (Dipartimento delle finanze 77 M€ sul triennio
  2024-2026, Giustizia tributaria 47 M€) spiegano circa 26 M€ l'anno [stima]. Ragioneria, Tesoro e Amministrazione
  generale non hanno contratti Sogei con CIG in ANAC [V sull'assenza nei dati] (R71). Peso della criticità 9 ridotto
  da circa 0,7 a circa **0,3 miliardi l'anno**.
- **Sogei come stazione appaltante:** quota 2024 dei suoi CIG ICT attivi circa 0,69 miliardi [V sui conteggi]. Sono
  acquisti per tutti i committenti (MEF e agenzie fiscali), non attribuibili a un ministero, e non vanno sommati al
  pagato del MEF: sarebbe un doppio conteggio della stessa catena in-house.
- **Quota annua dei contratti pluriennali:** ogni CIG si ripartisce sulla durata prevista ANAC. Dal 2024 la durata
  manca nel **90 % dei CIG** (0,1 % nel 2022) [V]: per i contratti 2024-2025 la quota è l'importo intero (R69).
  Rapporti sopra 1 (Difesa 9,1, Cultura 11,5) non sono coperture: per CF entrano uffici con bilancio proprio (musei e
  parchi autonomi, Agenzia industrie difesa).
- **Seconda via per anno** (rendiconto per piano di gestione, CE di 3° livello): 492, 740, 675, 452, 1.007, 979 M€ dal
  2019 al 2024 [V]. Il salto del 2023 è una riclassificazione (MEF da 18 a 297 M€): la controvalidazione vale dal 2023
  (84-86 % della via per gestionali), non prima.
- **SIOPE via BDAP contro SIOPE diretto** (#30; Lazio, Umbria, Basilicata, Molise, Liguria): sui codici ICT 99,4 %
  (2024) e 99,5 % (2025) delle coppie ente × codice uguali all'euro, totali 473,35 contro 473,36 M€ [V]; sul totale
  BDAP è più basso dello 0,7 % (2024) per i pagamenti da regolarizzare. Il **troncamento del 2025 a marzo** riferito da
  AgID [R] non si ripresenta sui file attuali di queste regioni: tutti i 1.507 enti abbinati arrivano a dicembre [V].
  Le altre 15 regioni non sono misurate. BDAP non ha il codice ente (R70): resta la fonte diretta.

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
| 2 | **Separare spesa e massimali**. **Fatto in 0.2** (§ 2.2): tolti 781 tetti; S3-S6 scende da 113,3 a 76,5 mld; restano incerti 1.317 CIG per 612,8 mld, di cui 33,6 negli strati ICT . **0.3** (§ 2.3): precisione di T3 e T4 misurata, regole v2, valori PVL; S3-S6 a 58,2 mld; restano 80 CIG ICT incerti per 14,4 mld (attuativi AQ e adesioni PSN senza avviso PVL) . **0.4** (§ 2.4): secondo campione T4 concessione e regola I6; quadro economico e SAL ANAC; la ricerca degli atti per CIG non rende (0 su 10) | prossimo passo: atti dalle sezioni «Bandi di gara e contratti» delle stazioni appaltanti dei 79 CIG; misurare la precisione di E4 | lettura atti per ente; accesso civico solo con l'ok di Fabio | noi; **ANAC/Consip** per l'ordinato per CIG (R14, R37, R49) |
| 3 | **PSN**. **Fatto in 0.2** (§ 4.1): impegni ANAC 4,38 mld contro un portafoglio di 3,8 [R] e ricavi 2023-2025 di 0,79 [R]; PPdF pubblicati dal 3,2 % delle PA . **0.3** (§ 4.2): decreti PNRR 1.1 spogliati, 524 M€ su 274 enti (75 % del riferimento) . **0.4** (§ 4.4): 16 decreti, 537,6 M€; CUP → CIG per 238 CUP | prossimo passo: ~160 M€ di decreti non trovati; PPdF dei 9 CIG PSN incerti | lettura dei PDF, decine di USD-eq | noi; **DTD/PSN** per piani e consuntivi per ente (R20, R39, R50) |
| 4 | **G1 + G3 con la via 6** (12.824 CIG, 7,8 mld) | G1 (209) a mano; G3 in ordine d'importo con il modello e gli atti dal link PVL (73 % raggiungibile) | ~1,8 USD-eq per 5 CIG (giro 2): G3 intero ≈ 4.500 USD-eq, oltre 10 settimane di tetto (400/settimana); i primi 1.000 CIG per importo ≈ 360 USD-eq | noi; **enti** per i link che non funzionano (R31-R33) |
| 5 | **Licenze e marchi «cloud da accertare»** (3.515 CIG, 6,5 mld). **0.6** (§ 4.5): cloud certo 168 M€, non cloud certo 892 M€, incerto 1,68 mld (Microsoft 0,80, Oracle 0,40), da leggere negli atti e controprova dal censimento AgID | lettura dei contratti Microsoft (decisione del 3/11) e Oracle; richiesta dei dati del censimento 2026 | lettura, centinaia di USD-eq; accesso civico solo dopo l'ok di Fabio | noi; **AgID** (R48); **ANAC/ACN** per un campo strutturato su prodotto e modalità (R21) |

## 9. Rifare i numeri

Da un clone pulito, senza dati grezzi (legge gli esiti versionati):

```
python tools/verifiche/imbuto_strati.py        # strati, assi, soglia, gruppi, link PVL; controlla la coerenza
python tools/verifiche/zenodo_test.py          # esito del test Zenodo
python tools/verifiche/imbuto_tetti.py         # tetti, spesa e incerti sopra 50 M€; strati ricalcolati
python tools/verifiche/imbuto_psn.py           # PSN: impegni ANAC contro bilanci PSN e piani dei fabbisogni
python tools/verifiche/imbuto_revisione.py     # precisione T3/T4 (Wilson), regole v2, strati ricalcolati
python tools/verifiche/pnrr11_decreti.py       # PNRR 1.1: finanziati per ente dai decreti, con controllo interno
python tools/verifiche/pnrr11_cup_cig.py       # PNRR 1.1: CUP → CIG e confronto con i contratti PSN
python tools/verifiche/imbuto_via6.py --json esiti/<data>/imbuto/via6-g1g3.json   # via 6 su G1/G3 (§ 4.3.1)
python tools/verifiche/imbuto_via6_revisione.py esito <data>   # revisione C1-C4 delle proposte via 6 (§ 4.3.2)
# sul server, dal mirror: cig_aq_tipo.py (§ 4.9)
# sul server, dal mirror (giro 0.2 di BDAP, § 4.10 e § 4.12)
nice .venv/bin/python tools/verifiche/bdap_ict_stato.py
nice .venv/bin/python tools/verifiche/bdap_cig_ministeri_cf.py
nice .venv/bin/python tools/verifiche/siope_bdap_vs_diretto.py 2024
nice .venv/bin/python tools/verifiche/siope_bdap_vs_diretto.py 2025
# sul server: imbuto_qe_sal.py (quadro economico e SAL dal mirror) prima di imbuto_revisione.py
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

## 9.1 Riproducibilità su altri modelli (nuovo in 0.4)

Chiunque può rifare la classificazione documentale con un altro modello, anche open-weight e senza rete:

- **Prompt:** `report/metodo/llm/prompt-analisi-documentale-v1.md`, autosufficiente e con sha256. Contiene i due assi, la tassonomia, i criteri, le prove (citazione letterale, pagina, sha256), 7 esempi dal campione 611 e cosa fare senza documenti.
- **Schema:** `schemi/analisi-documentale.schema.json`.
- **Runner neutro:** `tools/llm/analisi_documentale.py`, solo libreria standard. Funziona con qualunque endpoint compatibile OpenAI, con Ollama in locale, oppure stampando il prompt da incollare a mano.
- **Pacchetto:** `report/metodo/llm/riproduzione/v1/`, con gli ingressi e i loro sha256 e con gli esiti di Claude.
- **Confronto:** `tools/verifiche/concordanza_llm.py`, che calcola l'accordo per asse, Wilson e kappa.

**Prova pilota (12 CIG, [V]):** lo stesso prompt portabile, dato a Claude Haiku senza strumenti e con i soli testi archiviati, concorda con la via 6 completa così (`esiti/imbuto-via6/concordanza-haiku-pilota12.json`):
- stato dell'asse B: 10 su 12 (kappa 0,69);
- servizio: 8 su 12 (kappa 0,55);
- stato dell'asse A: 6 su 12 (kappa 0,29);
- giurisdizione: 4 su 12.

Le citazioni sono tutte letterali (10 su 10). Le uscite valide sono 7 su 12, perché per gli esclusi il modello scriveva `non-applicabile` come giurisdizione; lo schema ora lo ammette. Il disaccordo sull'asse A è atteso: la via 6 ha la ricerca web, il prompt portabile ha solo i documenti forniti. Il pacchetto da 50 CIG si congela da solo quando ci sono 50 esiti (`tools/llm/riproduzione.sh`).

**Concordanza (in corso):** primo confronto con un modello open-weight già presente sul server, senza installazioni né spese: qwen3-vl:8b via Ollama, solo CPU. È lento (decine di minuti per CIG su un server condiviso), quindi gira in background a bassa priorità sul pacchetto. L’esito andrà in `esiti/imbuto-via6/concordanza-qwen3-vl_8b.json`. Per i modelli in cloud a tier gratuito (DeepSeek, Qwen/DashScope, OpenRouter) serve una chiave che oggi non è configurata: decide Fabio.

## Limiti

- I numeri sono di imbuto-0.3.1 (3/11), che non tiene conto dei miglioramenti successivi alle convenzioni (#62).
- SmartCIG resta fuori.
- Gli euro includono gli importi negativi della fonte.
- L'asse B è riportato solo per gli inclusi certi.
- La via 6 su G3 è parziale (§ 4.3.1) e i suoi esiti sono proposte non revisionate.
- L4 del residuo S6 è parziale (§ 4.11).
- **CIG ripetuti (R53):** nei file ANAC 2024-2025 un CIG ha una riga per CPV; finché `ict.csv` non è rigenerato con la regola 0.3.4 il totale S3-S6 dal 2024 (circa 55,7 mld) è una stima e 152 CIG hanno lo strato S5/S6 dipendente dall'ordine del file (§ 2.6).
- SIOPE via BDAP è confrontato con la fonte diretta solo per 5 regioni su 20 (§ 4.12).

## Registro delle revisioni

| versione | data | cosa |
|---|---|---|
| 0.1 | 2026-11-06 | prima bozza per Fabio: strati, soglia, gruppi, link PVL per strato, Zenodo/EuroTender, censimento AgID, top-5 |
| 0.2 | 2026-11-06 | § 2.2: tetti e spesa per i 2.130 CIG sopra 50 M€, con la via di ogni CIG e gli strati ricalcolati; § 4.1: PSN, impegni contro bilanci 2024-2025 e piani dei fabbisogni; top-5 punti 2 e 3 aggiornati; R49 e R50 |
| 0.3 | 2026-11-06 | § 2.3: precisione di T3 e T4 su un campione stratificato (Wilson) e sul PVL; regole v2 (T3 tondo ristretto, T5/E2 dal PVL); revisione degli incerti ICT (errori d'importo, lotti ripetuti); S3-S6 a 58,2 mld. § 4.2: decreti PNRR 1.1 per ente. R51 |
| 0.4 | 2026-11-06 | § 4.3: via 6 su G1 (196 CIG unici) e primi 1.000 G3, in corso, proposte da revisionare; doppioni di CIG in ict.csv (R53); § 9.1: prompt portabile e pacchetto di riproduzione su altri modelli. § 2.4: secondo campione T4 concessione e regola I6, quadro economico e SAL ANAC (E4), ricerca degli atti degli incerti (esito negativo); § 4.4: decreto PNRR mancante e CUP → CIG; R54 |
| 0.5 | 2026-11-06 | § 2.5: visita delle sezioni AT di 40 enti per i 79 CIG ICT incerti (0 atti, 4 blocchi in blocchi-accesso.csv), precisione di E4 su campione (Wilson), chiusura del giro PNRR 1.1 |
| 0.6 | 2026-11-06 | § 2.6: CIG contati due volte (11.043 righe, i conti tornano; S3-S6 dal 2024 a 55,3 mld); § 4.5: licenze e marchi, cloud sì o no con la via di ogni CIG (cloud 168 M€, non cloud 892 M€, incerto 1,68 mld); top-5 punto 5 aggiornato |
| 0.7 | 2026-11-06 | § 4.6: censimento dei prodotti negli EA Microsoft (8 atti, quota cloud pesata 92 %, forbice sul residuo 0,55-0,81 mld) e nei primi 20 Oracle (on premises probabile, 261 M€); imbuto.py 0.3.2 contro i doppioni (non ancora rigenerato) |
| 0.8 | 2026-11-06 | § 4.7: adattatori per piattaforme di e-procurement (PortaleAppalti, esop, generico); CINECA Oracle raggiunto da anonimo (ULA, nessun cloud); 5 atti Oracle, 0 con cloud; 3 ricerche EA in più (0 atti); rigenerazione 0.3.2 rinviata |
| 0.9 | 2026-11-06 | § 4.8: TED come seconda fonte degli aggiudicatari (84 CIG, 72 nell'imbuto; precisione P.IVA 89 % riferita da #27); nessun effetto sugli strati |
| 0.10 | 2026-11-09 | § 4.3.1: via 6 al 9/11 (G1 196/196, G3 514/1.000, parziale e da revisionare); § 4.9: CIG derivati da AQ non collegabili, 0,82 % / 734 M€ (#50), conteggi di aq_pmod.py portati in cig_aq_tipo.py; § 4.10: BDAP 0.1, pagato ICT Stato 1.141 M€ 2024 e controvalidazione 979 M€, rapporti CIG/pagato come stima; § 4.11: riepilogo del residuo S6 (#57: L3 453 CIG/262,1 M€, MePA 0, L4 parziale 79/42,4 M€, potenziale 532 CIG/304,5 M€); correzioni della verifica a regole (604 su 725); segnaposto § 4.12 (BDAP fase 2); § 9 e limiti aggiornati |
| 0.11 | 2026-11-09 | § 4.12 BDAP fase 2: abbinamento per codice fiscale (Giustizia 0,96, MEF 0,25 nel 2024), quota annua e durata mancante dal 2024 (R69), Sogei (R71), seconda via 2019-2024, SIOPE BDAP contro diretto (#30, R70); criticità 9 a circa 0,3 miliardi; § 1, § 4.10 e § 9 aggiornati |
| 0.12 | 2026-11-09 | § 2.6 e § 1: CIG ripetuti (R53, `imbuto_cig_ripetuti.py`): eccesso vero 2,565 mld invece di 2,99, S3-S6 dal 2024 da 55,3 a circa 55,7 mld (stima fino alla rigenerazione 0.3.4); criticità nei limiti |
| 0.13 | 2026-11-09 | § 4.3.2: revisione delle proposte via 6 con i criteri C1-C4 (175 su 214 lette; 62 concordi, 76 non confermate, 37 discordi in coda per Fabio; entrano 15 CIG/397,4 M€ verso S5 e 6 CIG/24,6 M€ di cloud certo, 0 extra-UE); 38 proposte nuove del G3 in lettura; § 1-2 invariati |
| 0.14 | 2026-11-09 | Per la consegna del 12/11. § 1: sintesi riscritta per un lettore esterno (cosa misuriamo, numeri verificati, stime, cosa manca e perché, rimando a Obiettivo 6). § 2.7: anteprima della rigenerazione 0.3.4 (prova a secco, #71): S3-S6 dal 2024 56,06 mld contro 55,70, effetti R53 +0,064, perimetro +0,479, lente +0,004; 0 CIG ripetuti; 29 G1 nuovi e proposta P1 (decisione aperta). § 4.11: L4 finito (#68), 535 CIG / 304,7 M€, ripasso #73 in corso. § 4.3.3 segnaposto C1 |
