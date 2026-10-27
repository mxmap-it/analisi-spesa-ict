---
title: "Come si riconosce il cloud provider in un contratto"
date: 2026-10-27
description: "Le vie, distinte e documentate, con cui attribuiamo un contratto pubblico al cloud provider il cui prodotto viene comprato. Bozza di metodo, in validazione."
weight: 15
---
**Stato: bozza in validazione** ([#48](https://github.com/mxmap-it/analisi-spesa-ict/issues/48)).
I numeri citati vengono dal pilota sul 2025 e sono ordini di grandezza finché la precisione
non è misurata su un campione verificato a mano.

## Il principio

Si attribuisce la giurisdizione al **prodotto** comprato, non a chi lo vende. Microsoft 365
venduto da un rivenditore italiano resta Microsoft; AWS comprato tramite Fastweb resta AWS.

Nei dati ANAC il prodotto non è un campo: sta scritto nella descrizione, oppure si ricava dal
lotto della convenzione a cui il contratto aderisce, oppure non si ricava affatto. Per questo il
provider si riconosce con **più processamenti differenziati**. Ognuno ha un input, una regola,
un livello di confidenza e una verifica. Ogni contratto registra **quale via** lo ha attribuito,
così che ogni numero pubblicato si possa scomporre per via e ricontrollare.

## Le vie, in ordine di applicazione

La prima via che dà un risultato vince; le successive servono per ciò che resta.

| Via | Input | Regola | Confidenza |
|---|---|---|---|
| **1. Lotto di convenzione o accordo quadro** | `cig_accordo_quadro` del contratto | Il contratto eredita il provider del lotto padre, da una tabella dei lotti curata a mano ([`config/lotti_cloud.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/lotti_cloud.yaml)) | Alta |
| **2. Lotto dichiarato nel testo** | Descrizione, quando `cig_accordo_quadro` è vuoto | Riconoscimento di "adesione AQ… lotto N" o del nome dell'iniziativa Consip, poi come la via 1 | Media |
| **3. Marchio nella descrizione** | `oggetto_lotto` e `oggetto_gara` | Dizionario di marchi e alias (Microsoft 365, Azure, AWS, Google Workspace…) con regole di esclusione | Alta se il marchio è esplicito |
| **4. Polo Strategico Nazionale** | Contratti PSN e piani dei fabbisogni | Il PSN offre servizi su tecnologie diverse (Azure, Google, Oracle, AWS, cloud privato): si attribuisce la singola voce, non il contratto intero | Dipende dal documento disponibile |
| **5. Il fornitore è il provider** | Aggiudicatario e capogruppo | Se l'aggiudicatario appartiene al gruppo del provider (Aruba, Seeweb, Microsoft Ireland…) e la descrizione è di servizi cloud | Media |
| **6. Classificazione con modello linguistico** | Descrizione residua | Solo su ciò che le vie 1-5 non attribuiscono; modello e prompt versionati, risultati in cache, validazione sul campione | Misurata |
| **7. Indeterminato** | — | Ciò che resta si pubblica come quota **non attribuita**, mai distribuita per stima | — |

Una dimensione a parte, per il software in abbonamento (SaaS) di produttori italiani:
**dove gira**. Il prodotto è italiano, ma l'infrastruttura sottostante può essere di un
hyperscaler USA. Si registra come secondo livello, quando una fonte lo dichiara (catalogo ACN,
documentazione del fornitore); altrimenti resta "hosting non noto".

## Perché servono vie diverse: cosa abbiamo misurato

- **L'importo non è la spesa.** Nel 2025 i dieci contratti più grandi della classe "cloud
  generico" valgono l'85% del suo importo: sono massimali di accordi quadro. I padri si
  escludono dalle somme; si contano i contratti attuativi e, per la cassa, i pagamenti SIOPE.
- **Il lotto dice il provider anche quando il testo non lo dice.** L'accordo quadro Consip
  "Cloud IaaS e PaaS 2" (ID 2746) ha un lotto per provider: AWS, Google, Microsoft, Oracle,
  IBM, Aruba. L'aggiudicatario registrato per AWS è Fastweb.
- **Il collegamento al lotto spesso manca.** Fra i contratti che nella descrizione dichiarano
  un'adesione, il campo `cig_accordo_quadro` è vuoto nel 20% dei casi nel 2025 e nel 56% nel
  2017 ([#50](https://github.com/mxmap-it/analisi-spesa-ict/issues/50)). Per questo la via 2
  esiste, e per questo la sua quota va pubblicata: misura un difetto del dato alla fonte.
- **Il "cloud" senza marchio è soprattutto software italiano in abbonamento** (gestionali per
  comuni, scuole, sanità). Da qui la dimensione "dove gira".

## Come si verifica

1. **Campione di riferimento:** 1.000-2.000 contratti estratti per strato (via, classe,
   importo), classificati a mano; almeno il 20% da due persone, con accordo misurato (kappa di
   Cohen).
2. **Precisione e richiamo per via e per classe**, pubblicati insieme ai risultati.
3. **Totali con intervallo di confidenza**, corretti per gli errori misurati sul campione.
4. **Riproducibilità:** ogni via è uno script in `tools/`, eseguibile da un clone pulito
   ([#47](https://github.com/mxmap-it/analisi-spesa-ict/issues/47)); le tabelle curate a mano
   (lotti, marchi, capogruppo) stanno in `config/` con la fonte di ogni riga.

## Due lenti, per essere confrontabili

Accanto alla lente prodotto pubblichiamo la lente **capogruppo del vincitore**, la stessa usata
dallo studio del Parlamento europeo sui dati TED. Una tabella incrocia le due: misura quanto
della spesa verso prodotti extra-UE passa da vincitori italiani o europei.

## Cosa resta aperto

- Tabella completa dei lotti: altre iniziative Consip (licenze, SaaS, data center), SPC Cloud,
  convenzioni regionali.
- Dizionario dei marchi e regole di esclusione, con i falsi positivi del pilota
  (per esempio "Jira Data Center" non è un data center).
- Accesso ai dettagli dei contratti PSN.
- Confronto con il catalogo ACN per la dimensione "dove gira".
