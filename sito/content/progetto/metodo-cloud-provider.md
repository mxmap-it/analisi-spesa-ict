---
title: "Come si riconosce il cloud provider in un contratto"
date: 2026-10-28
description: "Il metodo con cui attribuiamo un contratto pubblico al cloud provider il cui prodotto viene comprato: difficoltà, vie di analisi, verifica umana a campione, errori misurati, raccomandazioni per semplificare il monitoraggio."
weight: 15
---
**Stato: bozza in validazione, regole v3 del 28 ottobre 2026**
([#48](https://github.com/mxmap-it/analisi-spesa-ict/issues/48)). Le precisioni citate sono
misure intermedie: quella definitiva si fa su un campione nuovo, annotato alla cieca da persone.

## Cosa misuriamo

Quanto spende la PA italiana in servizi cloud, e verso chi: **big tech statunitensi, provider
europei, provider italiani su datacenter propri**. Per ciascun contratto vogliamo sapere:

- **provider del prodotto** e sua **giurisdizione** (IT, UE, EXTRA-UE);
- **tipo di spesa**: abbonamento cloud, licenza software, servizi professionali sulla
  piattaforma, adesione al PSN;
- **canale**: comprato direttamente dal provider o tramite un **rivenditore**.

Si attribuisce la giurisdizione al **prodotto** comprato, non a chi lo vende. Microsoft 365
venduto da TIM resta Microsoft; AWS comprato tramite Fastweb resta AWS. Il rivenditore si
registra a parte, perché dice dove resta il valore economico.

Gli acquisti **in-house** (Lepida, Cineca, CSI Piemonte e simili) e quelli per **datacenter
propri** sono fuori da questa misura. Lo stesso vale per il **software con cui si costruisce un
cloud in casa**, come VMware: non è un cloud provider, ma è una dipendenza rilevante per i
cloud "sovrani" interni. Questi acquisti sono riconosciuti e marcati (tipo `in-house` e
`software-infrastruttura`), ma trattati come punto aperto dopo la chiusura della misura cloud
([#52](https://github.com/mxmap-it/analisi-spesa-ict/issues/52)).

## Perché è difficile

Nei dati ANAC il prodotto **non è un campo**. Abbiamo misurato queste difficoltà:

1. **Il prodotto sta nel testo libero**, scritto in modi diversi: "Microsoft 365", "M365",
   "MO 365", "Office 365", "licenze Exchange 365 Microsoft".
2. **Sigle omonime.** "PSN" è anche il Piano sanitario nazionale e il Piano strategico della PAC
   (sviluppo rurale); "GCP" è anche la Good Clinical Practice; "Aruba" è anche un marchio di
   switch HPE.
3. **Il vincitore spesso non è il provider.** Il prodotto di una big tech arriva quasi sempre
   tramite integratori e telco italiane (TIM, Fastweb, Vodafone, Var Group, Engineering…).
   La lente "chi vince" e la lente "che cosa si compra" danno risultati diversi.
4. **Il collegamento all'accordo quadro manca.** Fra i contratti che dichiarano un'adesione, il
   campo `cig_accordo_quadro` è vuoto nel 20% dei casi nel 2025 e nel 56% nel 2017
   ([#50](https://github.com/mxmap-it/analisi-spesa-ict/issues/50)).
5. **L'importo non è la spesa.** I contratti "padre" degli accordi quadro sono massimali: nel
   2025 i dieci più grandi della classe "cloud generico" valevano l'85% del suo importo.
6. **Contratti misti.** Licenze, migrazione e assistenza nello stesso lotto, con un solo
   importo.
7. **Il PSN è un canale, non un prodotto.** Eroga cloud privato nazionale ma anche tecnologie
   di hyperscaler USA: la giurisdizione va decisa voce per voce, e i dettagli non sono nei dati
   aperti.

## Le vie di analisi, in ordine di applicazione

Per questo il provider si riconosce con **più processamenti differenziati**. La prima via che dà
un risultato vince. Ogni contratto registra la **via** e la **regola** che lo hanno attribuito,
così ogni numero pubblicato si può scomporre e ricontrollare riga per riga.

| Via | Input | Regola | Precisione misurata (v2) |
|---|---|---|---|
| **1. Lotto di AQ o convenzione** | `cig_accordo_quadro` | Il contratto eredita il provider del lotto, da una tabella curata a mano con la fonte di ogni riga ([`config/lotti_cloud.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/lotti_cloud.yaml)) | 30 su 30 |
| **2. Lotto dichiarato nel testo** | Descrizione | "AQ IaaS e PaaS 2 … lotto N", poi come la via 1 | pochi casi |
| **3. Marchio nella descrizione** | `oggetto_lotto`, `oggetto_gara` | Dizionario di marchi, alias ed esclusioni ([`config/marchi_cloud.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/marchi_cloud.yaml)); vince il primo marchio, i prodotti prima degli in-house | provider 93,3%, provider e tipo 83,9% |
| **4. PSN voce per voce** | Contratti PSN e piani dei fabbisogni | Attribuzione della singola voce di catalogo | da implementare: serve accesso ai documenti |
| **5. Il fornitore è il provider** | Aggiudicatario | Aggiudicatario del gruppo del provider (Aruba, Seeweb, Oracle Italia, TIM, Fastweb…) e testo cloud | 29 su 29 |
| **6. Modello linguistico** | Descrizione residua | Solo sul residuo; modello, prompt e risultati versionati | da implementare |
| **7. Indeterminato** | — | Si pubblica come quota **non attribuita**, mai redistribuita per stima | — |

Dopo l'attribuzione, il **tipo di spesa** si decide con due regole: se il testo parla di
sviluppo, manutenzione evolutiva, migrazione o consulenza è **servizi professionali**; ma se
parla anche di licenze, crediti, sottoscrizioni o adesione al PSN resta **abbonamento**, perché
è la voce di costo principale e la dipendenza da misurare.

Il **canale** si ricava confrontando l'aggiudicatario con le denominazioni del provider: diretto
o rivenditore. Da qui la **mappa dei rivenditori**
([#41](https://github.com/mxmap-it/analisi-spesa-ict/issues/41)): chi incassa i contratti di
prodotti big tech, quanto, e quali contratti PSN nominano anche una tecnologia di hyperscaler.

## Verifica umana a campione

Il classificatore sbaglia, e lo diciamo con numeri. Il protocollo:

1. **Campione di sviluppo e campione di misura, separati.** Il primo si legge per correggere le
   regole; la precisione si misura solo sul secondo, estratto **dopo** le correzioni ed
   escludendo ogni contratto già visto. Stratificato per via, tipo di spesa e fascia di
   importo, con seme fisso ([`tools/analisi/campione_riferimento.py`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/tools/analisi/campione_riferimento.py)).
2. **Annotazione alla cieca.** L'annotatore riceve una copia **senza** le colonne del
   classificatore (via, provider, tipo), così non è ancorato all'esito automatico. Indica per
   ogni contratto: è cloud?, tipo di spesa, provider del prodotto, giurisdizione.
3. **Due annotatori** su almeno il 20% delle righe, con accordo misurato (kappa di Cohen); i
   disaccordi si risolvono e si documentano.
4. **Si pubblica** precisione per via e per classe, richiamo (quanto cloud sfugge), e i totali
   con intervallo di confidenza.
5. **Chiunque può rifarlo:** il campione, le annotazioni e lo script di misura sono in
   [`report/metodo/`](https://github.com/mxmap-it/analisi-spesa-ict/tree/main/report/metodo).

### Le misure finora

| Versione | Campione | Annotazione | Precisione provider | Provider e tipo | Cloud sfuggito |
|---|---|---|---|---|---|
| v2 (27/10) | misura, 437 righe | Claude, **non cieca** | 94,6% | 86,6% | 20 su 124 non attribuiti |
| v3 (28/10) | nuovo campione | persone, alla cieca | da misurare | da misurare | da misurare |
| lente prodotto dopo le regole del 9/11 (9/11) | quarto campione a cieco, 150 CIG | Claude, alla cieca, un annotatore | 92,2 % (Wilson 85,3-96,0), 99,0 % in euro | — | big tech: 1 mancato su 95 |
| regole v4.3 (9/11) | quinto campione a cieco, 238 CIG | Claude, alla cieca, un annotatore | big tech 86,2 % (Wilson 79,7-90,9), 80,8 % in euro; pesata 93,9 % | — | big tech: 0 mancati su 125 (R Wilson 97,0-100) |
| regole v4.4 (9/11) | sesto campione a cieco, 250 CIG | Claude, alla cieca, un annotatore | big tech 80,7 % (Wilson 73,4-86,4), 98,1 % in euro; pesata 89,4 % (99,0 % in euro) | — | big tech: 3 mancati su 116 (R 97,4 %, Wilson 92,7-99,1); nello strato N 3 su 80 |
| regole v4.5 (9/11) | da misurare: settimo cieco una sola volta, prima del rendiconto finale | — | sul cieco 6 (ora di sviluppo) 113/4/3, 99,8 % in euro: non è una misura | — | — |

La misura v2 è stata letta per scrivere la v3: quelle righe sono ora campione di sviluppo e non
valgono più come misura.

**Lente prodotto (via 3 sul solo testo), 6/11/2026, #40:**
- sul campione v3 (611 CIG), big tech USA: precisione 96 %, richiamo 90 %;
- su un campione nuovo a cieco di 240 CIG (40 per strato, `report/metodo/lente-cieco/`), prima di ogni modifica: precisione 100 %, richiamo 81 %.

I 13 mancati del campione a cieco hanno portato a regole nuove in `config/marchi_cloud.yaml` (sigle delle convenzioni Consip Microsoft «MS EA8/EA9», licenze SQL, licenze ed ESU di Windows 10/11, IaaS/PaaS Google e Microsoft dell'AQ 2746). La via 6 non legge quel file. Con le regole nuove il richiamo sul campione a cieco sale al 98 %, ma è una misura sullo stesso campione usato per scriverle, quindi **non vale come misura**: quel campione diventa di sviluppo.

Effetto sull'universo dal 2024, verificato a mano su un estratto: le regole nuove aggiungono circa 40 CIG. Si è scartato «win 10/11» da solo perché prendeva 242 CIG di PC con Windows preinstallato. Verifiche: `tools/verifiche/lente_prodotto.py`, `tools/verifiche/lente_cieco.py`.

**v0.5 (6/11/2026):** esclusioni (AWS in corsi e collocation, backup *di* Microsoft 365) e altre regole Microsoft licenza, scritte sugli errori del secondo campione a cieco (`report/metodo/lente-cieco-2/`, big tech P 95 %, R 89 %). Misurate su un **terzo campione a cieco** (`report/metodo/lente-cieco-3/`): big tech P 62/62 = 100 %, R 62/70 = 89 %. I mancati sono testi senza il nome del produttore o con il nome sbagliato.

**Quarto campione a cieco, regole del 9/11/2026 (#40).** Misura indipendente delle regole del commit 9ba5ad88 (marchio di un altro lotto, prodotti di terzi col nome del marchio, formazione AWS). Campione nuovo di 150 CIG 2024-2026 (`report/metodo/lente-cieco-4/`, seme 20261110), esclusi i 15.115 CIG già usati in campioni e test, in quattro strati: marchio extra-UE via rivenditore (R, 50 su 5.477), marchio extra-UE diretto (E, 50 su 555), gare multilotto con un marchio nel testo (M, 7: lo strato ha solo 7 CIG), ICT senza provider attribuito (N, 43 su 237.499). Il file per l'annotatore è mescolato e non ha né lo strato né l'uscita del classificatore; le etichette (prodotto dal testo ANAC e dall'aggiudicatario; nessuno di questi CIG ha un atto in `dati/atti/`) sono state committate col loro sha256 (0818f6fb, `23738e20…`) **prima** del confronto. Verifica `tools/verifiche/lente_cieco4.py`, esiti in `esiti/2026-11-09/lente-cieco-4/`.

| Strato | Big tech USA: precisione | Richiamo | Precisione in euro |
|---|---|---|---|
| R rivenditore | 44/50 = 88 % (76,2-94,4) | 44/44 | 97,1 % |
| E diretto | 48/50 = 96 % (86,5-98,9) | 48/48 | 99,4 % |
| M multilotto | 2/2 | 2/3 (Adobe lotto 3) | 100 % (richiamo 96 % in euro) |
| N senza provider | — | nessun big tech mancato su 43 | — |
| **Totale** | **94/102 = 92,2 % (85,3-96,0)** | **94/95 = 98,9 % (94,3-99,8)** | **99,0 %**, richiamo 99,9 % |

Pesata sull'universo: precisione 88,7 % (97,9 % in euro). Nessun errore di marchio sbagliato: gli 8 falsi positivi sono testi che nominano un marchio senza comprarne il prodotto, da trattare in un giro successivo (non corretti in questo):
- formazione e supporto sistemistico su prodotti Microsoft o Google (corso Teams/Planner, corso LibreOffice e Google Workspace, supporto «ambienti cloud, Microsoft 365», supporto «SQL Server»): 4 casi; l'esclusione della formazione oggi vale solo per AWS;
- prodotti di terzi per Microsoft 365 (Veeam Data Cloud, licenze di backup Commvault): 2 casi; l'esclusione del 9/11 copre solo «365 Protection» e Harmony Email;
- connettività verso Oracle Cloud Infrastructure (Wind Tre) e IaaS «per ambienti VMware» di provider non detto: 2 casi.

Mancati: lotto 3 «licenze Adobe» di una gara multilotto (il dizionario Adobe non prende «licenze Adobe» da sole) e caselle PEC Aruba (perimetro discutibile, provider IT). La regola multilotto non ha prodotto errori nei 7 CIG dello strato M. Limiti: un solo annotatore (Claude), niente kappa; lo strato M è troppo piccolo per misurare la regola multilotto; il richiamo nello strato N (0 big tech mancati su 43) ha un limite superiore di Wilson del 8 % su 237 mila CIG, quindi il richiamo pesato non è stimabile con precisione.

**Regole v4.3, correzione degli errori del quarto campione (9/11/2026, #40).** Le cinque classi d'errore del quarto campione sono corrette in `config/marchi_cloud.yaml`:
- formazione e supporto (corso, docenza, «formazione», supporto sistemistico/informatico/progettuale, help desk, sistemista) su prodotti Microsoft (cloud e licenze) e Google non sono acquisto del prodotto, salvo che il testo compri anche il servizio (licenze, sottoscrizione, canone, crediti, servizi cloud, attivazione, posta elettronica, «e relativo pacchetto formazione», «X e formazione»). Prima valeva solo per AWS;
- prodotti di terzi *per* Microsoft 365 (Veeam, Commvault, Acronis, Keepit, AvePoint, Hornetsecurity, N-able, «backup … Microsoft 365» nella stessa parte del testo, fino a 80 caratteri): esclusi; se il testo compra anche gli utenti Microsoft 365 resta Microsoft;
- connettività verso un cloud (Wind Tre → Oracle Cloud Infrastructure, ExpressRoute, FastConnect) non è acquisto del cloud, salvo licenze o crediti nello stesso testo (Oracle, Microsoft, Google);
- IaaS/cloud/hosting «per ambienti VMware» non è un prodotto VMware;
- «licenze Adobe» e i nomi dei prodotti Adobe (Photoshop, Acrobat, Creative, Stock…) entrano nel dizionario.

Prima e dopo su tutti i campioni etichettati (`tools/verifiche/regole_v43_confronto.py`, `esiti/2026-11-09/regole-v4.3/`):

| Campione | Big tech prima (TP/FP/FN) | Big tech dopo | Tutti i provider prima | Tutti dopo |
|---|---|---|---|---|
| cieco 1 (240) | 66/0/1 | 64/0/3 | 76/1/4 | 74/1/6 |
| cieco 2 | 62/0/1 | 62/0/1 | 69/1/1 | 69/1/1 |
| cieco 3 | 62/0/8 | 62/0/8 | 69/2/10 | 69/2/10 |
| cieco 4 (150) | 94/8/1 (P 92,2 %) | 95/0/0 (P 100 %, R 100 %) | 95/8/2 | 96/0/1 |
| top-20 rivenditori (60) | 58/0/0 | 58/0/0 | 58/0/0 | 58/0/0 |

I due CIG cambiati nel cieco 1 (B40B947819, B33B9DC8D2) sono corsi di formazione su Google Workspace e Office 365: nel cieco 1 l'etichetta era «quale prodotto nomina il testo», dal cieco 4 è «quale prodotto si compra». Non è una regressione ma un **cambio di criterio**, fissato con due casi di test. Due regressioni vere trovate in sviluppo sono state corrette prima del commit (Veeam con 100 utenti Microsoft 365, cieco 2; «licenze Microsoft … Adobe», cieco 3). Restano non correggibili dal testo il mancato PEC (il testo non nomina Aruba) e, per il cieco 4, i casi «altro:» (Veeam, Commvault, Wind Tre), ora correttamente senza provider del dizionario.

**Il quarto campione a cieco non è più indipendente per queste regole**: è stato letto per scriverle ed è ora campione di sviluppo; P 100 % e R 100 % sul cieco 4 non sono una misura. Serve un quinto campione a cieco.

Effetto sulla mappa dei rivenditori (`rivenditori_mappa.py v4.3`, contro v4.2): +427 CIG Adobe (22,9 M€), +7 Microsoft (contratti con licenze Microsoft 365 e backup, prima esclusi perché la finestra «backup … 365» attraversava il « | » fra oggetto del lotto e della gara), −87 Microsoft (2,6 M€), −17 Google (0,24 M€), −7 Oracle (0,66 M€: connettività verso OCI). Extra-UE 3,046 mld (era 3,024), via rivenditore con CF italiano 1,863 mld = **61,2 % del totale, 79,1 % del noto** (erano 61,0 % e 78,9 %), 57,4 % col capogruppo italiano.

**Quinto campione a cieco, regole v4.3 (9/11/2026, #40).** Misura indipendente delle regole v4.3 (commit 08c99907) col criterio «prodotto che si compra». Campione nuovo di 238 CIG 2024-2026 (`report/metodo/lente-cieco-5/`, seme 20261111, `tools/verifiche/lente_cieco5_campione.py`), esclusi i 15.312 CIG già usati in campioni, errori dei ciechi e test, in cinque strati disgiunti: multilotto con un marchio nel testo (M, 48: tutti; la regola multilotto ora guarda tutto il testo, non solo la gara), marchio + formazione/supporto/assistenza/backup/connettività (F, 40 su 916), marchio extra-UE via rivenditore (R, 35 su 5.091), diretto (E, 35 su 398), ICT senza provider (N, 80 su 237.074). Etichette dal testo ANAC (nessun CIG ha un atto in `dati/atti/`), committate con sha256 `284ef7c6…` in 9bb18871 **prima** del confronto (`tools/verifiche/lente_cieco5.py`, esiti in `esiti/2026-11-09/lente-cieco-5/`).

| Strato | Big tech USA: precisione | Richiamo | Precisione in euro |
|---|---|---|---|
| R rivenditore | 34/35 = 97,1 % (85,5-99,5) | 34/34 | 99,6 % |
| E diretto | 33/35 = 94,3 % (81,4-98,4) | 33/33 | 95,1 % |
| M multilotto | 34/42 = 81,0 % (66,7-90,0) | 34/34 | 91,3 % |
| F servizi accessori | 24/33 = 72,7 % (55,8-84,9) | 24/24 | 28,6 % |
| N senza provider | — | 0 big tech mancati su 80 (quota mancata ≤ 4,6 %, Wilson) | — |
| **Totale** | **125/145 = 86,2 % (79,7-90,9)** | **125/125 = 100 % (97,0-100)** | **80,8 %**, richiamo 100 % |

Pesata sull'universo (N_h/n_h): precisione big tech 93,9 %, 82,0 % in euro; richiamo 100 % (lo strato N non ha positivi: il richiamo pesato non è stimabile meglio del limite sopra). Tutti i provider del dizionario: 127/158 = 80,4 % (73,5-85,8), pesata 92,2 %. **Nessun mancato e nessun marchio sbagliato**: i 31 errori sono tutti «marchio nominato senza prodotto comprato», per classe (regole NON corrette, casi in `esiti/2026-11-09/lente-cieco-5/errori.csv`):
- **omonimia**: «Azure» di Medtronic è un pacemaker (lotti di gare sanitarie), 7 CIG Microsoft, 0,24 M€; controller Wi-Fi «Aruba» (HPE Aruba Networks, non Aruba S.p.A.), 1;
- **servizi professionali su una piattaforma** (sviluppo, assistenza, manutenzione applicativa, migrazione, consulenza sulle licenze), 10: Salesforce (Deloitte 6,14 M€, Almaviva AQ 2610 2,50 M€), Oracle ERP Cloud/OCI (2), Dynamics 365 e M365 (2), consulenza licenze Microsoft, SAP Analytics Cloud, assistenza VMware, servizio gestito su AWS (caso ambiguo); da sola questa classe vale circa l'87 % degli euro in errore;
- **formazione e supporto a gare o POC** su marchi non coperti dalla regola di formazione (Cloudera, AWS «supporto gestione gara», POC IBM Cloud), 3;
- **connettività o hardware verso un data center** (fibra e IP transit Fastweb attribuiti a in-house, MPLS verso il PSN, transceiver per Exadata), 4;
- **da rivedere, non necessariamente errori della lente**: 4 «SPC Cloud lotto 1» etichettati `altro:tim-spc-cloud` (stesso prodotto con altro nome: disaccordo di vocabolario dell'annotatore, che non conosceva i nomi canonici), conduzione dei data center Lepida (DGS) e piattaforma gestita del gruppo Retelit, 6.

Lettura: sui contratti di licenza e sottoscrizione (R, E) la lente tiene (P 94-97 %); scende dove il testo nomina il marchio come oggetto di un servizio (strato F, 28,6 % in euro) o come omonimo. Limiti: un solo annotatore (Claude), niente kappa; strati M e F sovra-campionati di proposito; il vocabolario delle etichette non coincide del tutto coi nomi canonici del dizionario (SPC Cloud). **Il quinto campione ora è letto**: correggere queste classi lo rende di sviluppo e richiede un sesto campione.

**Regole v4.4, correzione degli errori del quinto campione (9/11/2026, #40).** Criterio «prodotto comprato» (lo stesso delle etichette del cieco 5). Correzioni in `tools/analisi/classifica.py` e `config/marchi_cloud.yaml`:
- **omonimie**: «Azure» con Medtronic (anche MEDTRONIK/MEDTROMIK) è un pacemaker, non Microsoft; «Aruba» con Wi-Fi o «reti locali» (controller HPE Aruba Networks, Consip Reti locali) non è Aruba S.p.A.;
- **servizi professionali su una piattaforma**: entrano fra i servizi (servizio = `servizi-professionali`, escluso dalla mappa dei rivenditori come prima) supporto tecnico, *application maintenance*, «evolutive su», servizi applicativi (AQ Consip 2610), «assistenza e supporto», «assistenza, manutenzione», «manutenzione e assistenza»; la consulenza sulle licenze (assessment, *licensing advisory*, ottimizzazione del contratto) è un servizio anche se il testo dice «licenze». Resta prodotto se il testo compra anche licenze, sottoscrizione, canone o crediti. **Servizio gestito su AWS** (Advenias Care): si compra il servizio del fornitore, AWS è l'infrastruttura sottostante (tema di #70), quindi servizio professionale, non acquisto AWS;
- **formazione, POC e supporto a una gara** sono servizio per tutti i marchi, anche quelli di licenza (Cloudera), salvo acquisto del prodotto nello stesso testo;
- **connettività e hardware verso un data center**: niente via 5 per la telco se il testo è un collegamento (fibra, IP transit, MPLS, connettività) senza hosting/IaaS/servizi cloud; MPLS esclude il PSN; fibra, IP transit, connettività e «conduzione dei data center» escludono l'in-house; transceiver e connessioni MPO escludono Exadata; «assistenza HW» esclude VMware;
- **nome canonico SPC Cloud lotto 1**: la lente usa già il nome del dizionario; le 4 etichette `altro:tim-spc-cloud` sono lo stesso prodotto con un altro nome e nel confronto valgono «SPC Cloud lotto 1» (alias in `tools/verifiche/regole_v44_confronto.py`, etichette non modificate, sha256 invariato).

Valutazione: per ciechi 4-5 la lente conta il provider salvo `servizi-professionali` (VMware e in-house sono prodotti comprati, anche se la mappa li esclude per perimetro); top-20 col filtro della mappa; ciechi 1-3 primo marchio. «Prima grezza» = come lo misurava `lente_cieco5.py` (senza filtro). Prima/dopo (`esiti/2026-11-09/regole-v4.4/`), big tech TP/FP/FN:

| Campione | Prima grezza | Prima (v4.3) | Dopo (v4.4) | Tutti i provider prima → dopo |
|---|---|---|---|---|
| cieco 1 | 64/0/3 | 64/0/3 | 64/0/3 | 74/1/6 → 73/1/7 |
| cieco 2 | 62/0/1 | 62/0/1 | 62/0/1 | 69/1/1 → 69/1/1 |
| cieco 3 | 62/0/8 | 62/0/8 | 62/0/8 | 69/2/10 → 69/2/10 |
| cieco 4 | 95/0/0 | 89/0/6 | 88/0/7 | 90/0/7 → 89/0/8 |
| cieco 5 (238) | 125/20/0 (P 86,2 %) | 125/17/0 (P 88,0 %) | **125/0/0** | 130/24/1 → 130/0/1 |
| top-20 (60) | 58/0/0 | 58/0/0 | 57/0/1 | 58/0/0 → 57/0/1 |

24 CIG del cieco 5 corretti, nessuno peggiorato. **Tre cambi, tutti cambi di criterio e non errori nuovi delle regole**: cieco 1 B8587E9624 (IP transit dal data center di Liguria Digitale: nel cieco 1 l'etichetta era «chi nomina il testo», qui «chi vende»; lo stesso testo nel cieco 5, BA477DD6AC, è etichettato Fastweb); cieco 4 BD26C6E412 (*application maintenance* su Salesforce) e top-20 BAC86C865B (manutenzione evolutiva su Oracle Cloud): le etichette del cieco 4 e della top-20 contano come prodotto anche i servizi sulla piattaforma, quelle del cieco 5 no. È la stessa divergenza che già c'era nel cieco 4 con le regole v4.3 (6 CIG: manutenzione Salesforce, servizi professionali ServiceNow, migrazione Office 365 e Dynamics 365, *system integration* Salesforce, manutenzione su AWS), visibile solo ora che il cieco 4 si misura col filtro dei servizi. Si adotta il criterio del cieco 5 (il prodotto si conta quando si compra la licenza o la sottoscrizione, non i servizi su di essa); i servizi restano nel dato con servizio `servizi-professionali`. Restano: Aruba BB1804D765 (migrazione a cloud Aruba con assistenza, prodotto comprato ma il testo non lo dice) e il mancato PEC del cieco 4.

**Il quinto campione è ora di sviluppo**: P 100 % sul cieco 5 non è una misura. La misura indipendente delle v4.4 richiede un sesto campione a cieco. **La mappa dei rivenditori va rifatta con le regole v4.4** (`rivenditori_mappa.py`, job pesante): rinviata a quando la prova imbuto (#71) è finita (AGENTS.md § 4).

**Sesto campione a cieco, regole v4.4 (9/11/2026, #40, #72).** Misura indipendente delle regole v4.4 (commit e3c0d197) col criterio «prodotto comprato». Campione nuovo di 250 CIG 2024-2026 (`report/metodo/lente-cieco-6/`, seme 20261112, `tools/verifiche/lente_cieco6_campione.py`), esclusi i 15.560 CIG già usati (ciechi 1-5, campioni rivenditori, esiti delle regole v4.3 e v4.4, test). Strati disgiunti: multilotto M (vuoto: il cieco 5 li aveva presi tutti), **servizi su piattaforma P** (nuovo: marchio del dizionario e consulenza, manutenzione, migrazione, sviluppo, *system integration*, servizi professionali; 50 su 926), servizi accessori F (40 su 575), rivenditore R (40 su 4.716), diretto E (40 su 294), senza provider N (80 su 237.024). Etichette (nomi canonici dell'elenco pubblicato, `altro:` per il resto) committate prima del confronto in 799f2ecc, sha256 eba03237; confronto con `tools/verifiche/lente_cieco6.py`, esiti in `esiti/2026-11-09/lente-cieco-6/` (`misura.json`, `errori.csv`, `classi-errori.csv`).

| Strato | Big tech USA: precisione | Richiamo | Precisione in euro |
|---|---|---|---|
| R rivenditore | 38/40 = 95,0 % (83,5-98,6) | 38/38 | 99,8 % |
| E diretto | 39/40 = 97,5 % (87,1-99,6) | 39/39 | 99,8 % |
| P servizi su piattaforma | 18/29 = 62,1 % (44,0-77,3) | 18/18 | 98,2 % |
| F servizi accessori | 18/31 = 58,1 % (40,8-73,6) | 18/18 | 93,6 % |
| N senza provider | — | **3 big tech mancati su 80** (3,8 %, Wilson 1,3-10,5) | — |
| **Totale** | **113/140 = 80,7 % (73,4-86,4)** | **113/116 = 97,4 % (92,7-99,1)** | **98,1 %**, richiamo 99,8 % |

Pesata sull'universo (N_h/n_h): precisione big tech 89,4 % (99,0 % in euro). Il richiamo pesato in numero scende al 37,6 % (84,9 % in euro) perché i 3 mancati dello strato N, moltiplicati per 237.024/80, valgono circa 8.900 CIG stimati contro 5.359 trovati: la stima è molto incerta (la quota dei mancati nello strato N va da 1,3 a 10,5 %, cioè da circa 3.000 a 25.000 CIG) e riguarda contratti piccoli (0,13 M€ nel campione). Nel cieco 5 lo stesso strato aveva 0 mancati su 80: le due misure insieme danno 3 su 160 (1,9 %). Tutti i provider del dizionario: 124/170 = 72,9 % (65,8-79,1), 97,4 % in euro, pesata 85,2 %.

Errori per classe (regole NON corrette; il criterio delle etichette è quello del cieco 5):
- **servizi professionali su piattaforma** ancora presi come prodotto: 20 big tech (0,94 M€: assistenza/supporto «su ambiente Azure», «in ambito Microsoft 365», «su infrastruttura VMware», «assistenza sistemistica SQL Server», migrazioni a M365/OneDrive/Office 365, migrazione da Azure Data Factory, attività Salesforce, manutenzione di un add-on di Dynamics 365, canone di assistenza Fastweb per l'abilitazione al cloud AWS) e 12 di altri provider (Nextcloud 3, PSN 2 migrazioni di terzi, SAP 2, in-house 4, ex SPC Cloud 1). Le regole v4.4 coprono i servizi solo con alcune parole («servizi professionali», manutenzione applicativa): «assistenza», «supporto», «migrazione» davanti al marchio restano scoperti;
- **cloud come hosting dentro il servizio di un terzo** (manutenzione di un applicativo «comprensiva di hosting su Azure/AWS»): 3, casi di confine;
- **omonimie**: «GCP» = *Good Clinical Practice*, «Next Cloud» di Deda: 2;
- **formazione** (corso Power BI) 1; **IaaS gestita «(VMware)»** di un provider locale (variante non presa da «per ambienti VMware») 1; **prodotto di terzi per Google Workspace** (backup AFI) 1; supporto al RUP della concessione PSN 1;
- **vocabolario, non errori della lente**: 5 contratti in-house (CSI Piemonte Nivola, Lepida, Trentino Digitale) etichettati col nome dell'ente invece di «In-house pubblico»;
- **mancati** (3, strato N, via «ict-non-cloud»): «SERVICE NOW» da solo, «CAL + SERVER MS SQLSRV2022», «Google Suite Enterprise Starter».

Lettura: sui contratti di licenza e sottoscrizione (R, E) la lente tiene (P 95-97 %, 99,8 % in euro); negli strati di servizi la precisione in numero è 58-62 % ma in euro 94-98 %, perché i servizi sbagliati sono piccoli rispetto alle licenze dello stesso strato. Il richiamo non è più 100 %: tre sigle di prodotto (ServiceNow staccato, «MS SQLSRV», «Google Suite») sfuggono al dizionario. Limiti: un solo annotatore (Claude), niente kappa; strati P e F sovra-campionati di proposito; alcuni casi di confine (servizio gestito AWS, canone Office 365 di Halley, Google Workspace con formazione) etichettati come prodotto e annotati in `etichette.csv`. **Le regole non sono state corrette**: correggendole il sesto campione diventa di sviluppo.

**Regole v4.5, correzione delle classi del sesto campione (9/11/2026, #40, #72).** Correzioni in `tools/analisi/classifica.py` e `config/marchi_cloud.yaml`, senza inseguire i singoli CIG:
- **servizio davanti al marchio**: «assistenza», «supporto», «migrazione», «configurazione», «affiancamento», «backlog», «manutenzione ed aggiornamenti» nei 150 caratteri prima del marchio (stessa parte del testo) = `servizi-professionali`, salvo che il testo compri licenze, sottoscrizioni, crediti, servizi cloud o un canone annuale; «canone (di) assistenza» è sempre servizio (Fastweb per AWS). Vale per i marchi cloud e il PSN (Azure, M365, Salesforce, add-on di Dynamics, AWS, Nextcloud). **Cambio di criterio dichiarato** per i marchi di licenza e VMware (SQL Server, Windows Server, VMware, SAP S/4HANA): conta solo il lavoro sistemistico di un terzo («assistenza sistemistica/su/ai sistemi», «supporto specialistico», servizi professionali, giornate, migrazione, configurazione, *system architect/administrator*) e mai se il testo parla di prodotti, rinnovo o fornitura: il «supporto tecnico per il prodotto Oracle Database», l'«assistenza e manutenzione database Oracle» e il «canone di manutenzione e supporto VMware» sono il supporto del produttore, cioè acquisto del prodotto, come li etichettano i ciechi 4-6 (una prima versione senza questa distinzione peggiorava 9 CIG dei ciechi 4-6: scartata);
- **in-house**: migrazione o sviluppo di un terzo (non l'in-house) verso il data center in-house = servizio del terzo;
- **omonimie e prodotti di terzi**: «GCP auditor» (*Good Clinical Practice*), «software Next Cloud» di Deda, backup AFI per G Suite;
- **formazione**: corso «per l'utilizzo di licenze» (Power BI) = servizio anche se il testo dice «licenze»; il supporto al RUP della concessione PSN era già servizio con la v4.4 (ora caso di test);
- **mancati**: «SERVICE NOW» staccato quando è l'intero oggetto, «MS SQLSRV», «Google Suite»;
- **vocabolario in-house** (nel confronto, non nelle etichette): le etichette col nome di una in-house del dizionario (`altro:csi-piemonte`, `altro:lepida`, `altro:trentino-digitale`, `altro:cineca`…) valgono «In-house pubblico», come l'alias SPC Cloud della v4.4.

**Confine dichiarato, non corretto**: il cloud AWS/Azure come hosting dentro il servizio di un terzo («manutenzione del sito comprensiva di hosting su AWS», «spostamento del software nell'ambiente Azure») resta attribuito al marchio: è il tema dell'infrastruttura sottostante (#70), non una regola testuale.

Prima/dopo (`tools/verifiche/regole_v45_confronto.py`, che riusa `regole_v44_confronto.py`; `esiti/2026-11-09/regole-v4.5/`). Criterio della lente come per i ciechi 4-5 (provider salvo `servizi-professionali`) e alias in-house già nel «prima», quindi i numeri «prima» del cieco 6 differiscono dalla misura grezza di `lente_cieco6.py` (113/27/3). Big tech TP/FP/FN:

| Campione | Prima (v4.4) | Dopo (v4.5) | Tutti i provider prima → dopo | Big tech in euro: precisione prima → dopo |
|---|---|---|---|---|
| cieco 1 | 64/0/3 | 64/0/3 | 73/1/7 → invariato | — |
| cieco 2 | 62/0/1 | 62/0/1 | 69/1/1 → invariato | — |
| cieco 3 | 62/0/8 | 62/0/8 | 69/2/10 → invariato | — |
| cieco 4 | 88/0/7 | 88/0/7 | 89/0/8 → invariato | 100 % → 100 % |
| cieco 5 | 125/0/0 | 125/0/0 | 130/0/4 → invariato | 100 % → 100 % |
| top-20 | 57/0/1 | 57/0/1 | 57/0/1 → invariato | — |
| **cieco 6** | **110/20/6** (P 84,6 %) | **113/4/3** (P 96,6 %) | 125/29/7 → 128/7/4 (P 81,2 → 94,8 %) | **98,3 % → 99,8 %** (tutti: 97,9 → 99,5 %) |

25 CIG del cieco 6 corretti, **nessuna regressione** su ciechi 1-5 e top-20; 162/162 casi di test (33 nuovi, fra cui 7 casi che non devono rompersi: supporto del produttore Oracle/VMware, canone annuale Office 365, affidamento in house al CSI Piemonte). Restano nel cieco 6: big tech FP 4 (hosting dentro il servizio di un terzo 2, aggiornamento di un modulo WMS «del cloud AWS in uso», IaaS gestita «(VMware)» di un provider locale) e FN 3 (contratti misti «fornitura, attivazione, migrazione» di Google Workspace e «AQ per AWS cloud e servizi di manutenzione», che le regole v4.4 dei servizi tolgono e le etichette contano come prodotto); fuori dalle big tech, migrazione dentro la convenzione PSN, backup di un terzo sul DC Lepida, assistenza e hosting SAP di Ricca IT, SaaS di un terzo su Cloud Toscana.

**Il sesto campione è ora di sviluppo**: i numeri «dopo» non sono una misura. **Conclusione**: la precisione **in euro**, pesata sull'universo, era già ~99 % con le regole v4.4 (cieco 6: 99,0 %, 98,1 % nel campione); gli errori residui sono contratti piccoli di servizi e di confine, che pesano poco sulla spesa. Rincorrerli con nuove regole a ogni ritocco produce sovra-adattamento e consuma campioni. **Da qui in poi un nuovo campione a cieco (il settimo) si fa una sola volta, prima della pubblicazione del rendiconto finale**, sulle regole congelate a quel momento, e non dopo ogni ritocco. **La mappa dei rivenditori va rifatta con le regole v4.5** (`rivenditori_mappa.py`, job pesante) solo dopo la fine della prova imbuto (#71, AGENTS.md § 4): sostituisce la rigenerazione v4.4 rimasta in sospeso.

## Test automatici

Ogni errore trovato diventa un **caso di test**: un contratto reale con l'esito atteso
([`tests/casi_classifica.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/tests/casi_classifica.yaml)).
Un caso aggiunto non si toglie: se una regola nuova lo rompe, si corregge la regola. Il
classificatore è una funzione pura che non legge i dati ANAC
([`tools/analisi/classifica.py`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/tools/analisi/classifica.py)),
quindi si usa anche su OCDS, TED o registri regionali.

```bash
python tests/test_classifica.py      # 162/162 casi superati, regole v4.5 (9/11/2026)
```

## Errori trovati e come sono corretti

| Classe di errore | Esempio reale | Correzione |
|---|---|---|
| Sigle omonime | "PSN PAC 2023-2027 sviluppo rurale", "auditing GCP" clinico | Esclusioni sul contesto |
| Connettività e sicurezza intorno al PSN | "connettività dedicata verso le sedi PSN", "firewall PSN" | Escluse: non sono spesa cloud |
| Accordi quadro con lotti diversi | Lotto 1 di "Public Cloud IaaS e PaaS" (ID 2213) scambiato per AWS della seconda edizione | La via 2 accetta solo la seconda edizione esplicita |
| Servizi sulla piattaforma | Manutenzione evolutiva su Salesforce, migrazione al PSN | Tipo "servizi professionali" |
| Ambienti di sviluppo | "crediti Oracle Cloud per gli ambienti di sviluppo" classificati come servizi | Sono abbonamento |
| Contratti misti | "licenze Salesforce per l'implementazione del CRM" | Con licenze o crediti resta abbonamento |
| Marchi in altri contesti | Switch HPE Aruba, VMware dentro un acquisto di server | Esclusioni per marchio |
| Marchi mancanti | SAP S/4HANA e R/3, Exchange 365, "MO 365", Oracle ULA ed Exadata, Nextcloud | Aggiunti |
| Ordine dei marchi | SAP Fiori attribuito a Salesforce; VMware per Lepida attribuito all'in-house | Il primo marchio vince: prodotti prima, in-house in fondo |
| Provider italiani assenti | TIM cloud, Fastweb hosting, SPC Cloud lotto 1, in-house pubblici | Aggiunti come provider IT o in-house |
| Numero dell'AQ dentro altri numeri (9/11/2026, #41) | «2746» in «GARA ANAC 9127462» o «ACTC227464»: antisettici e reti idriche attribuiti ad AWS e Microsoft | Via 2: numero a sé e contesto cloud/Consip/AQ obbligatorio |
| Omonimi e marchi come oggetto di altro (9/11/2026, #41) | pacemaker «Azure S DR», «hardware rete PSN», «affiancamento» su PSN | Esclusioni; «affiancamento» = servizi professionali. Prima e dopo sui tre campioni a cieco: invariati (esiti/2026-11-09/rivenditori/lente-prima e lente-dopo) |
| Marchio senza acquisto del prodotto (9/11/2026, v4.3, #40) | corso Teams/Planner, supporto «SQL Server», Veeam Data Cloud per M365, connettività verso Oracle Cloud, IaaS «per ambienti VMware» | Esclusioni sul contesto se il testo non compra anche il prodotto; «licenze Adobe» aggiunte |
| Marchio nominato, prodotto non comprato (9/11/2026, v4.4, #40, cieco 5) | Azure Medtronic (pacemaker), controller Wi-Fi Aruba HPE, manutenzione/consulenza su Salesforce, Oracle ERP Cloud, Dynamics/M365, SAP Analytics Cloud, POC e formazione, collegamenti verso data center | Esclusioni per omonimia e connettività, servizi professionali estesi, formazione/POC/gara per tutti i marchi, niente via 5 per i collegamenti |
| Servizio davanti al marchio (9/11/2026, v4.5, #40/#72, cieco 6) | «supporto su ambiente Azure», «assistenza sistemistica SQL Server», «giornate di supporto specialistico VMware», «canone assistenza» per AWS, «GCP auditor», «Next Cloud» Deda, backup AFI per G Suite; mancati «SERVICE NOW», «MS SQLSRV», «Google Suite» | Servizio davanti al marchio = servizi professionali salvo acquisto; per licenze e VMware solo lavoro sistemistico di terzi (il supporto del produttore resta prodotto); esclusioni e sigle aggiunte; alias in-house nel confronto |

## Raccomandazioni per semplificare il monitoraggio

Gran parte della difficoltà sta nel dato alla fonte. Queste modifiche renderebbero la misura
quasi automatica:

1. **ANAC: rendere obbligatorio e controllato `cig_accordo_quadro`** per ogni adesione, con un
   controllo bloccante in fase di acquisizione del CIG (oggi vuoto nel 20% dei casi).
2. **ANAC e Consip: pubblicare in formato aperto la tabella lotto → prodotto e provider** di
   ogni accordo quadro e convenzione ICT. Oggi la ricostruiamo a mano dai documenti di gara.
3. **ANAC: un campo strutturato per il prodotto o il servizio cloud** (o almeno il codice del
   servizio nel catalogo ACN dei servizi cloud qualificati) nei contratti con CPV ICT.
4. **PSN e Difesa Servizi: pubblicare le adesioni voce per voce**, con la tecnologia
   sottostante (cloud privato nazionale o hyperscaler).
5. **Separare negli importi** abbonamento, licenze e servizi professionali quando stanno nello
   stesso lotto.
6. **Per chi analizza:** tabelle di lotti e marchi come dati aperti condivisi, con la fonte di
   ogni riga, e casi di test comuni. Le nostre sono in `config/` e `tests/`, in licenza libera.

## Riuso e manutenzione

Teniamo il codice nostro al minimo. A fine lavoro proporremo di portare queste capacità negli
strumenti che già esistono, a partire da
[anac-pl-pp-cli](https://github.com/aborruso/anac-pl-pp-cli), che oggi attribuisce la
giurisdizione al **fornitore**: le tabelle come file dati esterni, la lente prodotto accanto a
quella fornitore, il canale diretto/rivenditore, i casi di test
([#22](https://github.com/mxmap-it/analisi-spesa-ict/issues/22)).

## Due lenti, per essere confrontabili

Accanto alla lente prodotto pubblichiamo la lente **capogruppo del vincitore**, la stessa usata
dallo studio del Parlamento europeo sui dati TED. Una tabella incrocia le due: misura quanto
della spesa verso prodotti extra-UE passa da vincitori italiani o europei.

## Cosa resta aperto

- Misura v3 su campione nuovo, annotato alla cieca da persone.
- Via 4 (PSN voce per voce) e via 6 (modello linguistico).
- Tabella completa dei lotti: altre iniziative Consip (licenze, SaaS, data center), SPC Cloud,
  convenzioni regionali.
- SaaS di produttori italiani: **dove gira** (catalogo ACN, documentazione del fornitore).
- In-house e datacenter propri ([#52](https://github.com/mxmap-it/analisi-spesa-ict/issues/52)),
  dopo la chiusura della misura cloud.

## Cloud sovrano e dipendenze tecnologiche (29/10/2026)

La giurisdizione è quella del controllo giuridico di chi eroga il servizio. Data center in Italia + operatore italiano a controllo italiano non soggetto al CLOUD Act (immunità giuridica sul modello SecNumCloud 3.2) = **cloud sovrano (IT)**, anche con software extra-UE, che si registra come *dipendenza tecnologica* separata. Esempio: Sistema Cloud Toscana. Ogni classificazione è documentata nel [registro di classificazione](../formato-classificazione/).

## Registro delle revisioni

| Data | Revisione | Riferimento |
|---|---|---|
| 9/11/2026 | Quarto campione a cieco delle regole del 9/11 (150 CIG): big tech P 92,2 %, R 98,9 %; 8 falsi positivi e 2 mancati elencati come casi da trattare, regole non modificate | #40, `esiti/2026-11-09/lente-cieco-4/` |
| 9/11/2026 | Regole v4.3: formazione/supporto Microsoft e Google, prodotti di terzi per M365, connettività verso un cloud, «ambienti VMware», licenze Adobe; cieco 4 big tech da P 92,2 % a 100 % (ora campione di sviluppo, non più indipendente), ciechi 2-3 e top-20 invariati, cieco 1 −2 per cambio di criterio; mappa rivenditori v4.3 (CF IT 61,2 % dell'extra-UE) | #40, `esiti/2026-11-09/regole-v4.3/` |
| 9/11/2026 | Quinto campione a cieco delle regole v4.3 (238 CIG, 5 strati): big tech P 86,2 % (79,7-90,9), 80,8 % in euro, pesata 93,9 %; R 100 % (97,0-100); 31 errori tutti «marchio senza prodotto» (omonimia Medtronic Azure, servizi professionali su piattaforma, formazione/gare, connettività, vocabolario SPC Cloud), regole non modificate | #40, `esiti/2026-11-09/lente-cieco-5/` |
| 9/11/2026 | Regole v4.4 dalle classi d'errore del cieco 5 (omonimie, servizi su piattaforma, formazione/POC/gara, connettività, nome canonico SPC Cloud): cieco 5 big tech 125/17/0 → 125/0/0 (ora di sviluppo), ciechi 2-3 invariati, 3 cambi di criterio (cieco 1, cieco 4, top-20); 129/129 casi; mappa rivenditori da rifare (v4.4) dopo la prova imbuto | #40, `esiti/2026-11-09/regole-v4.4/` |
| 9/11/2026 | Sesto campione a cieco (250 CIG, seme 20261112, strato nuovo «servizi su piattaforma»): regole v4.4 big tech P 113/140 = 80,7 % (73,4-86,4), 98,1 % in euro, pesata 89,4 %; R 113/116 = 97,4 % (3 mancati nello strato N); 46 errori per classe, regole non corrette | #40, #72, `esiti/2026-11-09/lente-cieco-6/` |
| 9/11/2026 | Regole v4.5 dalle classi del cieco 6 (servizio davanti al marchio, supporto del produttore = prodotto per licenze e VMware, omonimie GCP/Next Cloud/AFI, mancati ServiceNow/SQLSRV/Google Suite, alias in-house nel confronto): cieco 6 big tech 110/20/6 → 113/4/3, in euro 98,3 → 99,8 % (ora di sviluppo); ciechi 1-5 e top-20 invariati; 162/162 casi; hosting dentro il servizio di un terzo lasciato come confine (#70). Conclusione: precisione in euro pesata ~99 % già con v4.4; il settimo cieco si fa una sola volta prima del rendiconto finale. Mappa rivenditori da rifare (v4.5) dopo la prova imbuto | #40, #72, `esiti/2026-11-09/regole-v4.5/` |
