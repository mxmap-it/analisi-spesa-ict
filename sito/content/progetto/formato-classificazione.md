---
title: "Formato della classificazione e artefatti intermedi"
date: 2026-10-29
description: "Come documentiamo ogni classificazione di un CIG (esito, attendibilità, passaggi, fonti) e i collegamenti CIG → atti, in formati aperti riusabili da terzi."
weight: 17
---

Ogni numero che pubblichiamo deriva da una classificazione per contratto (CIG). Per renderla **verificabile, contestabile e riprendibile da terzi con altri software** pubblichiamo, oltre ai risultati, gli **artefatti intermedi** in formato strutturato (JSON Lines, una riga per record) con schema JSON.

| artefatto | file | schema | contenuto |
|---|---|---|---|
| Registro di classificazione | `dati/classificazioni/*.jsonl` | [`schemi/classificazione.schema.json`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/schemi/classificazione.schema.json) | per ogni CIG: dati di ingresso con provenienza (sha256), esito, attendibilità, **tutti i passaggi** eseguiti, fonti, stato della revisione |
| Collegamenti CIG → atti | `dati/atti/atti.jsonl` | [`schemi/atto.schema.json`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/schemi/atto.schema.json) | per ogni documento collegato a un CIG (determina, contratto, convenzione): URL, come è stato trovato, sha256, testo estratto, pertinenza |
| Base di conoscenza delle iniziative | `report/metodo/llm/conoscenza-iniziative.yaml` | — | convenzioni e accordi quadro (Consip, PSN, regionali): lotti, aggiudicatari, prodotti, giurisdizione, fonti, stato di verifica |

Il collegamento **CIG → atto** è quello che oggi manca fra la Banca dati nazionale dei contratti pubblici (BDNCP/ANAC) e i documenti pubblicati dagli enti in Amministrazione trasparente: lo ricostruiamo e lo pubblichiamo come dataset a sé (vedi la raccomandazione R17).

## Il registro di classificazione

Un record per CIG e per versione del metodo. Campi principali:

- **`ingresso`** — oggetto, CPV, importo, stazione appaltante, aggiudicatari, con il file di origine e il suo sha256.
- **`esito`** — è cloud (`e_cloud`), tipo di servizio (cloud, licenza, servizi professionali, PSN, in-house, telefonia, connettività, hardware, altro), **provider del prodotto**, **giurisdizione** (IT / UE / EXTRA-UE / ignota), `cloud_sovrano`, `dipendenze_tecnologiche`, via di attribuzione, **confidenza** (alta / media / bassa), `fonte_primaria`, motivazione.
- **`passaggi`** — l'elenco ordinato di *tutto* ciò che è stato fatto: regola scattata (con il testo della regola e la versione del codice), modello linguistico usato (nome e versione delle istruzioni), ricerche web (query), pagine aperte, documenti scaricati, estrazione del testo o OCR, revisione umana, decisione. Ogni passaggio riporta strumento, versione, parametri, risultato, data e chi l'ha eseguito.
- **`fonti`** — URL effettivamente aperti, con tipo e sha256 del documento archiviato.
- **`revisione`** — `da-rivedere` (confidenza non alta o disaccordo fra vie), `campione-controllo`, `confermata`, `corretta`; modalità cieca o assistita.

### Confidenza: definizione operativa

La confidenza dice **quanto è provata** una classificazione. Ha due componenti:

1. **un livello dichiarato per regole**, che chiunque può ricontrollare;
2. **una precisione misurata** per ciascun livello su un campione rivisto da persone alla cieca.

Il livello, da solo, non è una probabilità: lo diventa solo quando la sua precisione è stata misurata.

**Definizioni**

- **Documento archiviato:** un documento scaricato dallo strumento `tools/llm/atti.py` e conservato nell'archivio con il suo sha256, con testo estratto e leggibile (`esito_recupero: ok`).
- **Atto dell'ente:** un documento archiviato emesso dalla stazione appaltante sul contratto (determina, contratto, delibera) il cui testo **contiene il CIG** (`pertinenza: cig-citato`).
- **Fonte primaria** (`fonte_primaria: true`): c'è almeno un atto dell'ente. Lo stabilisce il codice, non chi classifica.
- **Prodotto nominato:** il nome del provider del prodotto compare nell'oggetto del contratto in BDNCP.

**Livelli**

| livello | condizione (tutte verificabili da codice o da persona) |
|---|---|
| **alta** | c'è una fonte primaria che conferma prodotto e servizio; **oppure** il prodotto è nominato e c'è almeno un documento archiviato che lo conferma (scheda della convenzione, catalogo, determina di un'iniziativa di cui il CIG è attuativo) |
| **media** | deduzione forte ma senza documento archiviato che la provi: un fornitore che vende un solo prodotto, una convenzione nota ma non collegata al CIG, l'oggetto che descrive il servizio senza nominare il prodotto |
| **bassa** | indizi deboli o contraddittori, campi essenziali mancanti, oppure classificazione non riuscita |

**Regole applicate dal codice** (`tools/llm/verifica_esiti.py`, a ogni esecuzione):

- **R1:** la fonte primaria dichiarata dal modello vale solo se esiste l'atto dell'ente archiviato che cita il CIG.
- **R2:** «alta» senza i requisiti scende a «media».
- **R3:** confidenza mancante o campi obbligatori assenti diventano «bassa».

Ogni correzione resta registrata nel campo `verifica`, con il valore prima e dopo.

**Precisione misurata.** Per ogni livello e per ciascuna via di attribuzione si rivede alla cieca:

- un campione casuale stratificato: tutte le «bassa» e le «media», più almeno il 10% delle «alta»;
- su quel campione si pubblica la precisione con il suo intervallo di confidenza al 95% (Wilson).

**Uso nei numeri.** Nei numeri pubblicati come fatti entrano solo:

- le classificazioni ad alta confidenza la cui precisione misurata è almeno del 95%;
- le classificazioni confermate in revisione umana.

Il resto si pubblica come intervallo («da… a…») oppure come quota non attribuita.

## Giurisdizione e cloud sovrano

La giurisdizione è quella del **controllo giuridico di chi eroga il servizio** (sede e controllo della capogruppo del provider del prodotto), non del rivenditore. Un servizio con data center in Italia, erogato e gestito da un'azienda italiana a controllo italiano non soggetta a leggi extraterritoriali come il CLOUD Act statunitense (immunità giuridica sul modello di SecNumCloud 3.2) è **cloud sovrano**, anche se usa software di produttori extra-UE: quel software si registra come *dipendenza tecnologica*, in un campo separato, e non cambia la giurisdizione. Esempio: Sistema Cloud Toscana (decisione del 29/10/2026, `DECISIONI.md`).

## Riproducibilità

- `node tools/llm/registro.js` rigenera registro e collegamenti dai file in git (idempotente).
- Le istruzioni date ai modelli sono versionate (`tools/llm/istruzioni.md` p1, `istruzioni-p2.md` p2) e citate in ogni passaggio.
- Le conversazioni di lavoro con gli agenti sono versionate in `sessioni/`.

## Registro delle revisioni

| data | modifica |
|---|---|
| 2026-10-29 | prima versione: schemi `spesaict.classificazione/1` e `spesaict.atto/1`; registro del campione v3 (611 CIG) con regole v3.1 e giri 1-2 della via 6 |
