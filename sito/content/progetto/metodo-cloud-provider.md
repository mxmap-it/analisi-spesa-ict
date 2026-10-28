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
propri** sono fuori da questa misura: sono riconosciuti e marcati, ma trattati come punto
aperto dopo la chiusura della misura cloud
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

La misura v2 è stata letta per scrivere la v3: quelle righe sono ora campione di sviluppo e non
valgono più come misura.

## Test automatici

Ogni errore trovato diventa un **caso di test**: un contratto reale con l'esito atteso
([`tests/casi_classifica.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/tests/casi_classifica.yaml)).
Un caso aggiunto non si toglie: se una regola nuova lo rompe, si corregge la regola. Il
classificatore è una funzione pura che non legge i dati ANAC
([`tools/analisi/classifica.py`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/tools/analisi/classifica.py)),
quindi si usa anche su OCDS, TED o registri regionali.

```bash
python tests/test_classifica.py      # 48/48 casi superati, regole v3
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
