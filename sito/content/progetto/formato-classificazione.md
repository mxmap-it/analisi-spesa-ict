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

### Regole di attendibilità

- **alta**: un atto dell'ente sul contratto nomina il prodotto (`fonte_primaria: true`), oppure il prodotto è nominato in modo univoco nel testo **e** confermato da una fonte aperta;
- **media**: deduzione forte senza conferma documentale;
- **bassa**: indizi deboli.

Nei numeri pubblicati entrano come fatti solo le classificazioni ad alta confidenza o confermate in revisione umana; la precisione di ciascun livello è misurata su un campione rivisto alla cieca.

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
