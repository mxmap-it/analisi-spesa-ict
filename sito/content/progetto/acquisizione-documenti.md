---
title: "Acquisizione dei documenti: modalità a complessità crescente"
date: 2026-10-29
description: "Come troviamo il documento che chiarisce che cosa compra un contratto pubblico: dai dati strutturati al crawling di Amministrazione trasparente fino all'accesso civico generalizzato, in ordine di costo e complessità."
weight: 18
---

Spesso il testo di un contratto in BDNCP non basta a dire **quale prodotto** si compra e **sotto quale giurisdizione** (esempio: «adesione alla convenzione PSN, piano dei fabbisogni …»: il PSN vende servizi italiani ed extra-UE). Serve un documento: la determina, il contratto, il piano dei fabbisogni, la scheda del prodotto.

Usiamo **più modalità di acquisizione**, in ordine di complessità e costo crescenti. Si passa alla modalità successiva solo per i contratti che quella precedente non ha chiuso. Ogni documento trovato è archiviato con il suo sha256, il testo estratto (anche con OCR) e la **modalità che lo ha trovato** (`trovato_con.livello` nel [dataset CIG → atti](../formato-classificazione/)). Così si misura, modalità per modalità, quanto copre e quanto costa.

| livello | modalità | cosa usa | costo | stato |
|---|---|---|---|---|
| **L0** | Testo del contratto | oggetto, CPV, aggiudicatari, importo in BDNCP/ANAC | nullo | in uso |
| **L1** | Dati strutturati collegati | collegamento all'accordo quadro (`cig_accordo_quadro`), base di conoscenza delle iniziative (Consip, PSN, regionali), dati aperti PNRR (CUP), catalogo ACN | nullo, deterministico | in uso; dipende dalla qualità dei collegamenti ANAC (R01) |
| **L2** | Avvisi europei (TED) | per le gare sopra soglia, gli avvisi eForms contengono l'indirizzo dei documenti di gara (BT-15) | basso, deterministico | da sperimentare |
| **L3** | Piattaforme di e-procurement | dal 2024 ogni gara passa da una piattaforma certificata (MePA, Sintel, START, piattaforme commerciali) che pubblica la documentazione | basso-medio | da sperimentare |
| **L4** | Crawling mirato di Amministrazione trasparente | sito dell'ente da IndicePA → sezione «Bandi di gara e contratti» → riconoscimento del software di trasparenza (pochi fornitori coprono la maggior parte degli enti) → ricerca per CIG → scaricamento | medio, deterministico e ripetibile | da sviluppare |
| **L5** | Ricerca assistita da modello linguistico | per i casi che L1-L4 non chiudono: l'agente cerca sul web e nei siti degli enti, scarica con lo strumento di archiviazione, legge il testo estratto | alto (token) | in sperimentazione (via 6, giro 2) |
| **L6** | Segnalazione umana | gli annotatori indicano quale documento esterno servirebbe (determina, piano dei fabbisogni, contratto, convenzione, scheda prodotto); le richieste alimentano una coda (`dati/annotazioni/documenti-da-cercare.jsonl`) per L2-L5 | tempo dei volontari | in uso ([annotazioni](../../annotazioni/)) |
| **L7** | Accesso civico generalizzato (FOIA) | richiesta formale all'ente per i documenti non pubblicati | molto alto: richiede un sistema dedicato per richieste massive, scadenze, solleciti e ricorsi; è un **progetto a parte** | ultima istanza, non avviato |

## Principi

- **Prima il deterministico.** L1-L4 sono codice ripetibile: lo stesso input dà lo stesso documento, senza token. L5 e L7 servono solo per il residuo.
- **Priorità per importo.** Si cercano prima i documenti dei contratti che pesano di più nella spesa e di quelli con giurisdizione «non determinabile».
- **Una volta per sempre.** Un documento trovato resta nel dataset CIG → atti, con sha256: non si cerca più ed è riutilizzabile da chiunque.
- **Ogni modalità è misurata.** Per ciascun livello pubblichiamo la quota di contratti chiusi, il costo e i blocchi incontrati (siti irraggiungibili, scansioni, CAPTCHA che non aggiriamo).
- **Ogni ostacolo diventa una richiesta di policy.** Se un documento dovuto non è raggiungibile, lo segnaliamo (R16-R20): il link CIG → atto in BDNCP renderebbe superflui i livelli L4-L7.

## Misure finora (29/10/2026)

- **L0-L1:** dati aperti ANAC verificati: né l'OCDS bulk né il dataset delle pubblicazioni contengono link ai documenti. Il dataset delle pubblicazioni ha solo CIG e date.
- **L5 (giro 2 della via 6):** con la ricerca web generica un atto dell'ente che cita il CIG si trova in circa 1 contratto su 10. Lo strumento web dell'agente non legge i PDF; da qui lo strumento di archiviazione con estrazione del testo.
- **L6:** prime annotazioni in corso.

## Registro delle revisioni

| data | modifica |
|---|---|
| 2026-10-29 | prima versione: livelli L0-L7, principi, prime misure |
