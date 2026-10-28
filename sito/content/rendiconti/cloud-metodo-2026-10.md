---
title: "Spesa della PA in servizi cloud: metodo e risultati intermedi"
subtitle: "Rendiconto per la revisione pubblica · regole v3 · contratti ANAC 2022-2026"
date: 2026-10-28
description: "Come attribuiamo ogni contratto pubblico al cloud provider del prodotto, con tutti i risultati intermedi, gli errori trovati, le misure di precisione, la mappa dei rivenditori, il collegamento ai fondi PNRR cloud e i comandi per rifare tutto da zero."
---
**Versione 1.0 del 28 ottobre 2026** · regole v3 · [registro delle revisioni](#registro-delle-revisioni)

Questo rendiconto è scritto **per essere rivisto e contestato**. Ogni numero ha il file da cui
viene e il comando che lo rifà. Gli errori trovati lungo la strada restano scritti. Le
segnalazioni si aprono su [GitHub](https://github.com/mxmap-it/analisi-spesa-ict/issues).

## 1. Sintesi

- **La domanda.** Quanto spende la PA italiana in servizi cloud, e verso chi: big tech
  statunitensi, provider europei, provider italiani con datacenter propri.
- **Il metodo.** La giurisdizione si attribuisce al **prodotto** comprato, non a chi lo vende.
  Nei dati ANAC il prodotto non è un campo, quindi lo ricaviamo per cinque vie diverse:
  - il lotto dell'accordo quadro;
  - il lotto citato nel testo;
  - il marchio nella descrizione;
  - il fornitore, quando è il provider stesso;
  - quando nessuna via decide, il contratto resta *non attribuito* e non lo stimiamo.
- **Cosa misuriamo, sui contratti 2022-2026.** Questi i valori al netto di padri e importi da
  verificare:
  - Il cloud con provider riconosciuto vale **fra 230 e 300 milioni l'anno**, per quasi tutto
    extra-UE: Microsoft, Salesforce, AWS, Google, Oracle, ServiceNow.
  - Il **PSN** vale **fra 500 e 550 milioni l'anno** dal 2023.
  - Il cloud senza provider riconoscibile vale **fra 400 e 660 milioni l'anno**: soprattutto
    software in abbonamento di produttori italiani, di cui non sappiamo dove gira.
- **Chi incassa.** I prodotti big tech arrivano quasi sempre tramite **rivenditori**. Per
  Microsoft sono **1,10 miliardi da rivenditori contro 0,12 miliardi venduti direttamente**.
  Il primo rivenditore è **TIM**: 1.573 contratti, 1,12 miliardi.
- **Fondi PNRR cloud (Misura 1.2).**
  - Sono 20.855 finanziamenti per 1,26 miliardi.
  - Solo il **55,5%** dei CUP finanziati è collegato a un contratto nei dati ANAC.
  - Fra i contratti collegati, metà dell'importo non ha un provider riconoscibile. Delle big
    tech riconosciamo pochi milioni.
- **I dati alla fonte rendono la misura fragile.** In particolare:
  - in molte adesioni l'importo è il massimale della convenzione: **84 contratti da 9,8
    miliardi** sono marcati *da verificare* e tenuti fuori dai totali netti;
  - il collegamento all'accordo quadro manca;
  - un campo chiave è vuoto nel 99% dei casi;
  - 789 contratti hanno come aggiudicatario "IMPRESA INESISTENTE".

  Le [richieste ad ANAC, Consip, PSN e DTD](#9-richieste-e-raccomandazioni) servono a
  correggere questi problemi.
- **La precisione non è ancora misurata alla cieca.** La misura precedente (v2) dava il
  94,6% di provider corretti, ma con un'annotazione non indipendente. La misura v3 attende
  l'annotazione umana di un campione nuovo di 611 contratti.

**Come leggere i numeri.** Sono **importi a base di gara dei lotti attuativi** (`importo_lotto`),
non pagamenti. Indicano l'ordine di grandezza e la composizione, non la cassa: per la cassa
servono i pagamenti SIOPE ([#12](https://github.com/mxmap-it/analisi-spesa-ict/issues/12)).
Il 2026 è parziale (dati fino a ottobre).

## 2. Domanda e perimetro

**Si misura** la spesa per i servizi cloud, distinta per tipo:

| Tipo | Cosa è | Nei totali cloud |
|---|---|---|
| `cloud` | Abbonamento a un servizio cloud (IaaS, PaaS, SaaS) | sì |
| `psn` | Adesione al Polo Strategico Nazionale | sì, a parte |
| `licenza` | Licenza software installata dall'ente | no, a parte |
| `servizi-professionali` | Sviluppo, migrazione, consulenza su una piattaforma | no, a parte |
| `software-infrastruttura` | Software per costruire cloud in casa (VMware) | no: punto aperto [#52](https://github.com/mxmap-it/analisi-spesa-ict/issues/52) |
| `in-house` | Società in-house pubbliche (Lepida, Cineca, CSI…) | no: punto aperto #52 |

**Giurisdizione** del provider: IT, UE, EXTRA-UE.

**Perimetro dei contratti:** CPV ICT (48, 72, 302, 3223-3226, 50312, 50320, 51611, 64216,
64222, 79342), più i contratti con un marchio cloud riconosciuto anche fuori da questi CPV,
contati a parte (`-fuori-cpv-ict`).

**Fuori da questa misura**, come punto aperto dopo la sua chiusura: gli acquisti in-house e i
datacenter propri ([#52](https://github.com/mxmap-it/analisi-spesa-ict/issues/52)).

## 3. I dati

| Fonte | Cosa usiamo | Archiviata |
|---|---|---|
| ANAC, `cig-2022` … `cig-2025` e aggiornamenti mensili | Oggetto, CPV, importo, accordo quadro, ente | sì, sha256 in [`report/anac/snapshot-2026-10-27.tsv`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/anac/snapshot-2026-10-27.tsv) |
| ANAC, `aggiudicatari` | Chi vince, con il ruolo nell'RTI | sì |
| ANAC, `cup` | Collegamento CIG-CUP | sì |
| PA Digitale 2026 (DTD) | Finanziamenti PNRR 1.1 e 1.2 con CUP | sì, sha256 in [`report/metodo/fonti-v3.sha256`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/metodo/fonti-v3.sha256) |

Il mirror completo di ANAC (1.797 risorse, 120 GB nell'archivio) è descritto nel
[rendiconto ANAC](/rendiconti/anac-2026-10/). L'archivio è append-only e indirizzato per
contenuto: si sa cosa era pubblicato e quando.

**Una regola di lettura, scoperta a nostre spese.** Gli aggiornamenti mensili di ANAC contengono
CIG di **tutti gli anni dal 2007**, non solo gli ultimi. Per ogni CIG vale l'ultima versione
pubblicata, e il contratto va all'anno di pubblicazione. Senza questa regola si conta due volte
(§8, errore 6).

## 4. La catena di elaborazione

```text
mirror ANAC + PA Digitale 2026 (sha256)
  → attribuisci   un CIG una volta (ultima versione) → classificatore → padri esclusi → importi da verificare marcati
  → rivenditori   canale diretto / rivenditore / ignoto per ogni contratto attribuito
  → pnrr          finanziamento (CUP) → CIG → contratto attribuito
  → campione      stratificato, seme fisso, esclusi i contratti già visti, copia cieca
  → misura        annotazioni umane alla cieca → precisione, richiamo, kappa
  → confronta     ogni numero rifatto contro quello pubblicato
```

Il classificatore è una funzione pura
([`tools/analisi/classifica.py`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/tools/analisi/classifica.py)).
Le regole sono dati
([`config/marchi_cloud.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/marchi_cloud.yaml),
[`config/lotti_cloud.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/lotti_cloud.yaml)),
con la fonte di ogni riga. Gli errori trovati diventano casi di test
([`tests/casi_classifica.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/tests/casi_classifica.yaml),
**58 casi**, tutti superati). Il metodo per esteso, con le difficoltà e le vie, è nella pagina
[Come si riconosce il cloud provider](/progetto/metodo-cloud-provider/).

## 5. Risultati intermedi

Fonte: [`report/metodo/attribuzione-riepilogo-v3.json`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/metodo/attribuzione-riepilogo-v3.json).
Gli importi sono in milioni di euro, CPV ICT, al **netto** dei padri di accordo quadro e degli
importi da verificare. Fra parentesi c'è il **lordo**, quando è diverso.

### 5.1 Per anno, tipo e giurisdizione

| Anno | Cloud IT | Cloud UE | Cloud EXTRA-UE | PSN | Licenze EXTRA-UE | Cloud senza provider |
|---|---|---|---|---|---|---|
| 2022 | 109,8 | 5,4 | 233,8 (273,8) | 19,9 | 311,6 | 630,7 |
| 2023 | 17,9 | 7,0 (15,0) | 256,4 (296,4) | 545,2 (744,6) | 326,9 (587,9) | 640,6 |
| 2024 | 21,8 | 25,9 (95,2) | 174,6 (296,5) | 502,0 (636,7) | 288,2 (2.216,3) | 659,8 |
| 2025 | 18,4 | 43,8 | 255,4 (380,9) | 508,6 (874,6) | 482,2 (912,2) | 475,8 |
| 2026* | 24,2 | 52,6 (109,8) | 231,8 (249,8) | 139,9 (741,8) | 270,3 | 405,7 |

\* fino a ottobre 2026.

Come leggerla:

- **La distanza fra lordo e netto è il problema dei massimali.** Nel 2024 le licenze extra-UE
  passano da 2,2 miliardi lordi a 0,29 netti: quattro contratti Microsoft EA da 430-607 milioni
  e uno Oracle da 398 (§6).
- **Il cloud IT del 2022 (109,8)** è da rivedere sul campione: è molto più alto degli altri
  anni.
- **Il "cloud senza provider"** sono contratti con parole cloud (cloud, SaaS, hosting,
  datacenter) e CPV ICT, ma senza un marchio o un lotto riconoscibile. Per il campione v2 sono
  soprattutto software italiano in abbonamento. Il PNRR conferma (§7).

### 5.2 Provider, cloud e PSN, 2022-2026 (netto)

| Provider | Giurisdizione | Milioni | Contratti |
|---|---|---|---|
| Polo Strategico Nazionale | IT | 1.715,5 | 621 |
| Microsoft | EXTRA-UE | 446,7 | 2.405 |
| Salesforce | EXTRA-UE | 269,2 | 311 |
| SAP | UE | 132,1 | 94 |
| Amazon Web Services | EXTRA-UE | 108,8 | 257 |
| ServiceNow | EXTRA-UE | 100,6 | 42 |
| TIM | IT | 91,8 | 331 |
| Oracle | EXTRA-UE | 80,9 | 182 |
| Google | EXTRA-UE | 78,6 | 614 |
| SPC Cloud lotto 1 | IT | 69,4 | 129 |
| IBM | EXTRA-UE | 53,3 | 23 |
| Fastweb | IT | 19,6 | 46 |
| Aruba | IT | 7,1 | 177 |
| Cisco Webex, Adobe, Zoom | EXTRA-UE | 14,0 | 509 |
| Retelit, Seeweb | IT | 4,2 | 48 |
| Nextcloud, OVHcloud | UE | 2,6 | 43 |

### 5.3 Quale via ha attribuito i contratti

| Via | Contratti 2022-2026 |
|---|---|
| 3. Marchio nella descrizione | 11.026 |
| 5. Il fornitore è il provider | 1.141 |
| 1. Lotto di accordo quadro (`cig_accordo_quadro`) | 149 |
| 2. Lotto citato nel testo | 10 |

La via più affidabile, il lotto, attribuisce pochissimo, perché il collegamento all'accordo
quadro manca o non è tabellato (§9, R01 e R07). Quasi tutto passa dal testo libero.

## 6. Importi da verificare

In molte adesioni l'importo del lotto sembra il **massimale della convenzione**, non la spesa
dell'ente. Alcuni esempi:

- **430,0 milioni identici** per Banca d'Italia e, due volte, per Infocamere (Microsoft
  Enterprise Agreement);
- 607,4 milioni per l'ASL Napoli 3 Sud;
- 723,3 milioni per un museo, che è la convenzione PSN del Dipartimento per la trasformazione
  digitale.

**Regola, trasparente e senza correzioni a mano.** Marchiamo i contratti di almeno 50 milioni e
quelli con un importo identico (≥ 5 milioni) presso enti diversi. Il risultato sono
**84 contratti per 9,77 miliardi**: 49 per soglia, 35 per importo ripetuto. Li pubblichiamo
uno per uno in
[`report/metodo/importi-da-verificare-v3.csv`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/metodo/importi-da-verificare-v3.csv),
e i totali escono **con e senza**. La verifica caso per caso si fa sui documenti di gara:
chiunque può contribuire.

## 7. PNRR cloud: i finanziamenti e i contratti

Catena: candidatura finanziata (CUP, PA Digitale 2026) → dataset ANAC `cup` → contratto.
Fonte: [`report/metodo/pnrr-cloud-v3.json`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/metodo/pnrr-cloud-v3.json).
Il dettaglio contratto per contratto è in
[`pnrr-contratti-v3.csv`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/metodo/pnrr-contratti-v3.csv).

| | Misura 1.1 (infrastrutture digitali) | Misura 1.2 (abilitazione al cloud) |
|---|---|---|
| Finanziamenti | 206 | 20.855 |
| Importo finanziato | 91,1 milioni | 1.263,4 milioni |
| CUP con almeno un contratto in ANAC | 79,6% | **55,5%** |
| Contratti collegati | 70 | 17.973 |
| …nel perimetro attribuito | 61 | 12.504 |
| Importo dei contratti nel perimetro | 270,3 milioni | 818,9 milioni |
| …con provider attribuito | 96,7% (quasi tutto PSN) | **51,6%** |

Cosa dice la Misura 1.2:

1. **Metà dei finanziamenti non si ritrova nei contratti** tramite il CUP. Può essere che il
   CUP non sia indicato nel CIG, che l'acquisto sia avvenuto fuori dalla BDNCP o che il progetto
   non sia ancora a contratto. È un difetto da capire (§9, R15).
2. **Della spesa collegata, il provider riconosciuto è soprattutto il PSN** (316 milioni). Il
   resto è **cloud senza provider**: 10.626 contratti, 290 milioni. Sono le migrazioni dei
   comuni a software in abbonamento di produttori italiani.
3. **Le big tech compaiono poco**: Microsoft 32 contratti per 7,1 milioni, AWS 3 contratti per
   0,4 milioni. Non vuol dire che il software comprato non giri su un hyperscaler: è la
   dimensione "dove gira", che richiede il catalogo ACN (R11).

Siccome questi contratti sono cloud **per definizione**, la quota non attribuita (circa metà
dell'importo) è una **stima indipendente** di quanto cloud sfugge alle vie basate su marchio e
lotto.

## 8. Rivenditori e PSN

Fonte: [`report/metodo/rivenditori-v3.csv`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/metodo/rivenditori-v3.csv)
e [`.json`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/metodo/rivenditori-v3.json).
Il calcolo copre cloud e licenze dei provider, al netto dei padri e degli importi da verificare.

**Canale.** È *diretto* se fra gli aggiudicatari c'è il provider stesso o, per il PSN, un socio
del concessionario (TIM, Leonardo, CDP Equity, Sogei). È *rivenditore* negli altri casi, e
*ignoto* se l'aggiudicatario manca.

| Provider | Diretto | Rivenditore | Ignoto |
|---|---|---|---|
| Microsoft | 119,7 | **1.098,0** | 245,3 |
| Oracle | 261,2 | 296,8 | 223,3 |
| SAP | 69,5 | 201,8 | 75,3 |
| Salesforce | — | 133,7 | 113,2 |
| AWS | — | 91,1 | — |
| Google | — | 61,9 | — |

Milioni di euro, 2022-2026; "—" indica una voce sotto le prime 16 del file.

**I primi rivenditori:**

| Rivenditore | Contratti | Milioni | Prodotti principali |
|---|---|---|---|
| TIM | 1.573 | 1.120,7 | Microsoft, Salesforce, Oracle |
| Postel | 149 | 94,8 | Microsoft, SPC Cloud |
| Eurolink | 28 | 94,5 | Oracle, AWS |
| Fastweb | 90 | 87,6 | AWS, IBM |
| "IMPRESA INESISTENTE" | 31 | 79,5 | SAP, Oracle, Microsoft |
| Italware | 60 | 58,4 | Oracle, SAP |
| Var Group | 179 | 48,3 | Microsoft, Oracle, Salesforce |
| SoftwareOne Italia | 85 | 47,9 | Microsoft |

**PSN e big tech.**
- Solo **12 contratti, per 9,2 milioni**, nominano nel testo sia il PSN sia una big tech: per
  esempio "PSN – Secure Public Cloud Azure". È un **limite inferiore**.
- Il PSN eroga anche tecnologia di hyperscaler, ma le voci delle adesioni non sono nei dati
  aperti (R09).
- Quindi i 1.715 milioni del PSN sono "giurisdizione IT" per il canale, **non** per la
  tecnologia sottostante. Questa resta indeterminata.

## 9. Richieste e raccomandazioni

Il registro completo, aggiornato man mano, è in
[`report/metodo/richieste-e-raccomandazioni.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/metodo/richieste-e-raccomandazioni.yaml).
Nessuna è stata ancora inviata.

| # | A chi | Cosa | Stato |
|---|---|---|---|
| R01 | ANAC | Collegamento all'accordo quadro (`cig_accordo_quadro`) vuoto nel 20% delle adesioni dichiarate (2025) | verificato |
| R02 | ANAC | `STRUMENTO_SVOLGIMENTO` vuoto nel 97,7% (2024) e nel 99,6% (2025) dei contratti con CPV 48/72 | verificato, da classificare |
| R03 | ANAC | I delta contengono CIG di tutti gli anni senza dire cosa è cambiato | verificato |
| R04 | ANAC | `anno_pubblicazione` con valori non validi | verificato |
| R05 | ANAC | Prodotto o servizio cloud come campo strutturato (codice del catalogo ACN) | proposta |
| R06 | ANAC | Importi separati per abbonamento, licenze e servizi | proposta |
| R07 | Consip | Tabella aperta lotto → prodotto e provider | proposta |
| R08 | Consip | Ordinativi delle convenzioni ICT con il prodotto | proposta |
| R09 | PSN, Difesa Servizi, DTD | Adesioni PSN voce per voce, con la tecnologia sottostante | proposta |
| R10 | DTD | PNRR 1.1 e 1.2 per ente, con fornitore, servizio e CIG | proposta |
| R11 | ACN | Catalogo cloud con identificativo stabile e infrastruttura sottostante | proposta |
| R12 | Sogei, in-house | Acquisti cloud fatti per conto degli enti | proposta |
| R13 | ANAC | 789 contratti con aggiudicatario "IMPRESA INESISTENTE" | verificato, da classificare |
| R14 | ANAC, Consip | Importo dell'adesione pari al massimale della convenzione | da verificare |
| R15 | DTD, ANAC | Solo il 55,5% dei CUP finanziati dalla Misura 1.2 ha un CIG collegato | verificato, da capire |

## 10. Verifica umana a campione

| Versione | Campione | Annotazione | Provider corretto | Provider e tipo |
|---|---|---|---|---|
| v2 | 437 righe | Claude, **non alla cieca** | 94,6% | 86,6% |
| v3 | **611 contratti**, 47 strati, seme 20261028 | **persone, alla cieca**: da fare | — | — |

Il campione v3 esclude i 1.404 contratti già visti da chi ha scritto le regole. La
[copia cieca](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/metodo/campione-misura-v3-cieco.csv)
non ha le colonne del classificatore. Chi vuole contribuire la compila e lancia
`tools/misura_cloud.sh misura la-sua-annotazione.csv`. Con due annotatori si misura anche
l'accordo (kappa di Cohen).

## 11. Errori trovati e correzioni

Il racconto completo, passo per passo, è nel
[registro dei procedimenti](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/metodo/REGISTRO-PROCEDIMENTI.md).

| # | Errore | Effetto | Correzione |
|---|---|---|---|
| 1 | Massimali di accordo quadro sommati come spesa | "Cloud generico" gonfiato (top 10 = 85%) | Padri esclusi |
| 2 | Sigle omonime (PSN = Piano sanitario, PAC; GCP = Good Clinical Practice) | Falsi PSN e Google | Esclusioni sul contesto |
| 3 | AQ 2213 scambiato per AQ 2746 | Provider sbagliato | Via 2 solo per la seconda edizione |
| 4 | Ambienti di sviluppo, contratti misti | Tipo sbagliato | Regole abbonamento/servizi |
| 5 | In-house prima dei prodotti | VMware di Lepida attribuito all'in-house | In-house in fondo, con contesto obbligatorio |
| 6 | **Delta sommato agli annuali** | **Doppio conteggio**, anche nel riepilogo v2 pubblicato il 27/10 | Un CIG una volta, ultima versione |
| 7 | Via 5 con RTI | RTI guidato da GPI attribuito a TIM | Tutti gli aggiudicatari devono essere il provider |
| 8 | Massimali nelle adesioni | Totali inutilizzabili | Importi da verificare, totali con e senza |
| 9 | SAP Italia e ServiceNow come rivenditori di sé stessi | Canale sbagliato | Denominazioni societarie aggiunte |

Il riepilogo v2 (`report/metodo/attribuzione-riepilogo-2026-10-27.json`) è superato da quello
v3 e contiene l'errore 6: resta pubblicato per la tracciabilità.

## 12. Limiti noti

- **Precisione v3 non ancora misurata alla cieca.**
- **Importi a base di gara, non pagamenti.**
- **Perimetro CPV.** Un contratto cloud con CPV non ICT e senza marchio sfugge. La stima PNRR
  dice quanto: 5.469 contratti collegati alla 1.2 sono fuori perimetro.
- **PSN: tecnologia sottostante indeterminata.**
- **SaaS italiano: "dove gira" non noto.**
- **Vie 4 (PSN voce per voce) e 6 (modello linguistico) non implementate.**
- **Rivenditori:** le denominazioni sono normalizzate in modo semplice, senza capogruppo (GLEIF, [#28](https://github.com/mxmap-it/analisi-spesa-ict/issues/28)).

## 13. Come riprodurre tutto da zero

Con il mirror e la misura, su una macchina Linux con circa 100 GB liberi:

```bash
git clone https://github.com/mxmap-it/analisi-spesa-ict.git && cd analisi-spesa-ict
tools/verifica_anac.sh ambiente                        # Python e librerie a versioni bloccate
tools/verifica_anac.sh scarica                         # file ANAC usati (~77 GB)
tools/verifica_anac.sh snapshot                        # sono gli stessi del 27/10/2026? (sha256)
tools/archivia.py --lista config/pnrr-risorse.txt      # dati PA Digitale 2026
tools/misura_cloud.sh test                             # 58 casi di riferimento
tools/misura_cloud.sh attribuisci                      # contratti 2022-2026
tools/misura_cloud.sh rivenditori
tools/misura_cloud.sh pnrr
tools/misura_cloud.sh campione                         # stesso seme, stesso campione
tools/misura_cloud.sh confronta                        # ogni numero contro quello pubblicato
```

Il 28/10/2026 la riesecuzione sul server ha riprodotto **1.449 numeri su 1.449**. Il mirror
completo del portale ANAC si rifà con `tools/censisci_anac.py` e `tools/mirror_anac.py`. Tutto
è spiegato in [RIPRODURRE.md](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/RIPRODURRE.md).

## 14. Prossimi passi

1. Annotazione alla cieca del campione v3 da parte di due persone, poi la misura.
2. Verifica, uno per uno, degli 84 importi da verificare.
3. Via 4 (PSN) e collegamento al catalogo ACN per la dimensione "dove gira".
4. Capogruppo dei rivenditori (GLEIF).
5. Interfaccia per il drilldown e la diagnostica
   ([#53](https://github.com/mxmap-it/analisi-spesa-ict/issues/53)).
6. Punto aperto: in-house e datacenter propri
   ([#52](https://github.com/mxmap-it/analisi-spesa-ict/issues/52)).

## Registro delle revisioni

| Versione | Data | Modifica |
|---|---|---|
| 1.0 | 28/10/2026 | Prima pubblicazione: regole v3, contratti 2022-2026, rivenditori, PNRR, importi da verificare |
