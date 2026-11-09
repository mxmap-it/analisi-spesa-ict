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

## Test automatici

Ogni errore trovato diventa un **caso di test**: un contratto reale con l'esito atteso
([`tests/casi_classifica.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/tests/casi_classifica.yaml)).
Un caso aggiunto non si toglie: se una regola nuova lo rompe, si corregge la regola. Il
classificatore è una funzione pura che non legge i dati ANAC
([`tools/analisi/classifica.py`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/tools/analisi/classifica.py)),
quindi si usa anche su OCDS, TED o registri regionali.

```bash
python tests/test_classifica.py      # 101/101 casi superati, regole v4.3 (9/11/2026)
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
