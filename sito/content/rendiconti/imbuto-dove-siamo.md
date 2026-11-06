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

**Versione 0.4 del 2026-11-06 · BOZZA non annunciata: la pubblicazione la decide Fabio Pietrosanti** · [registro delle revisioni](#registro-delle-revisioni) · [disegno dell'imbuto](/progetto/imbuto/) · ticket [#55](https://github.com/mxmap-it/analisi-spesa-ict/issues/55), [#57](https://github.com/mxmap-it/analisi-spesa-ict/issues/57), [#59](https://github.com/mxmap-it/analisi-spesa-ict/issues/59), [#60](https://github.com/mxmap-it/analisi-spesa-ict/issues/60)

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
- **Tetti, precisione e revisione (nuovo in 0.3):** su un campione stratificato giudicato sugli atti, T4 accordo quadro e T3 non tondo risultano precisi al 100 % (intervallo 80-100 %) e T4 concessione al 73 % (48-89 %). T3 con importo tondo si ferma al 53 % ed è ristretto [V]. Con le regole v2, i dati PVL e la revisione degli incerti ICT (10 errori d'importo per 14,1 mld), **S3-S6 dal 2024 scende a 58,2 miliardi**, di cui 14,4 ancora incerti in 80 CIG (§ 2.3).
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
| 2 | **Separare spesa e massimali**. **Fatto in 0.2** (§ 2.2): tolti 781 tetti; S3-S6 scende da 113,3 a 76,5 mld; restano incerti 1.317 CIG per 612,8 mld, di cui 33,6 negli strati ICT . **0.3** (§ 2.3): precisione di T3 e T4 misurata, regole v2, valori PVL; S3-S6 a 58,2 mld; restano 80 CIG ICT incerti per 14,4 mld (attuativi AQ e adesioni PSN senza avviso PVL) | prossimo passo: determina di adesione o contratto esecutivo degli 80, ente per ente; secondo campione per T4 concessione | lettura atti, ~80 ricerche | noi; **ANAC/Consip** per l'ordinato per CIG (R14, R37, R49) |
| 3 | **PSN**. **Fatto in 0.2** (§ 4.1): impegni ANAC 4,38 mld contro un portafoglio di 3,8 [R] e ricavi 2023-2025 di 0,79 [R]; PPdF pubblicati dal 3,2 % delle PA . **0.3** (§ 4.2): decreti PNRR 1.1 spogliati, 524 M€ su 274 enti (75 % del riferimento) | prossimo passo: decreti mancanti (~176 M€), collegamento CUP → CIG, PPdF dei 9 CIG PSN incerti | lettura dei PDF, decine di USD-eq | noi; **DTD/PSN** per piani e consuntivi per ente (R20, R39, R50) |
| 4 | **G1 + G3 con la via 6** (12.824 CIG, 7,8 mld) | G1 (209) a mano; G3 in ordine d'importo con il modello e gli atti dal link PVL (73 % raggiungibile) | ~1,8 USD-eq per 5 CIG (giro 2): G3 intero ≈ 4.500 USD-eq, oltre 10 settimane di tetto (400/settimana); i primi 1.000 CIG per importo ≈ 360 USD-eq | noi; **enti** per i link che non funzionano (R31-R33) |
| 5 | **Licenze e marchi «cloud da accertare»** (3.515 CIG, 6,5 mld) e controprova dal censimento AgID | lettura dei contratti Microsoft (decisione del 3/11) e Oracle; richiesta dei dati del censimento 2026 | lettura, centinaia di USD-eq; accesso civico solo dopo l'ok di Fabio | noi; **AgID** (R48); **ANAC/ACN** per un campo strutturato su prodotto e modalità (R21) |

## 9. Rifare i numeri

Da un clone pulito, senza dati grezzi (legge gli esiti versionati):

```
python tools/verifiche/imbuto_strati.py        # strati, assi, soglia, gruppi, link PVL; controlla la coerenza
python tools/verifiche/zenodo_test.py          # esito del test Zenodo
python tools/verifiche/imbuto_tetti.py         # tetti, spesa e incerti sopra 50 M€; strati ricalcolati
python tools/verifiche/imbuto_psn.py           # PSN: impegni ANAC contro bilanci PSN e piani dei fabbisogni
python tools/verifiche/imbuto_revisione.py     # precisione T3/T4 (Wilson), regole v2, strati ricalcolati
python tools/verifiche/pnrr11_decreti.py       # PNRR 1.1: finanziati per ente dai decreti, con controllo interno
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

**Concordanza (in corso):** primo confronto con un modello open-weight già presente sul server, senza installazioni né spese: qwen3-vl:8b via Ollama, solo CPU. È lento (decine di minuti per CIG su un server condiviso), quindi gira in background a bassa priorità sul pacchetto. L’esito andrà in `esiti/imbuto-via6/concordanza-qwen3-vl_8b.json`. Per i modelli in cloud a tier gratuito (DeepSeek, Qwen/DashScope, OpenRouter) serve una chiave che oggi non è configurata: decide Fabio.

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
| 0.3 | 2026-11-06 | § 2.3: precisione di T3 e T4 su un campione stratificato (Wilson) e sul PVL; regole v2 (T3 tondo ristretto, T5/E2 dal PVL); revisione degli incerti ICT (errori d'importo, lotti ripetuti); S3-S6 a 58,2 mld. § 4.2: decreti PNRR 1.1 per ente. R51 |
| 0.4 | 2026-11-06 | § 4.3: via 6 su G1 (196 CIG unici) e primi 1.000 G3, in corso, proposte da revisionare; doppioni di CIG in ict.csv (R53); § 9.1: prompt portabile e pacchetto di riproduzione su altri modelli |
