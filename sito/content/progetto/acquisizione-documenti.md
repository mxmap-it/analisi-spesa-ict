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
| **L3** | Piattaforme di e-procurement | dal 2024 ogni gara passa da una piattaforma certificata (MePA, Sintel, START, piattaforme commerciali) che pubblica la documentazione | basso-medio; il link per CIG viene dalla PVL (campo `documenti_di_gara_link`, dal 2024; vedi `report/metodo/acquisizione/dettaglio-cig.md`) | basso-medio | in corso sul residuo S6 (#57, misure sotto) |
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

## Misure L3 sul residuo S6 (7/11/2026, parziali)

Sul residuo S6 dell'imbuto che la via 6 non copre (28.583 CIG: 70 ICT con importo incerto, 21.525 G3 oltre i primi 1.000, 2.395 G2, 3.593 entrati con «sw»/«connettività», 1.000 G4 a campione) lo strumento per famiglia di piattaforma (`tools/acquisizione/piattaforme_cig.py`, lanciato da `residuo_s6.sh`) segue il link PVL, cerca il CIG e scarica i documenti collegati. Misura: `tools/verifiche/residuo_s6_copertura.py`, esito in `esiti/2026-11-07/acquisizione/`.

- **Senza link PVL: 16.403 CIG su 28.583 (57 %)**, quasi tutti precedenti al 2024: per loro L3 non si applica (servono L4-L5). Fra questi 55 dei 70 ICT incerti (11,3 mld) e 2.222 dei 2.395 G2.
- **Con link: 12.180 CIG.** Famiglie: generico 7.092, home della piattaforma 3.292, PortaleAppalti 1.180, MePA (JavaScript, non tentato) 591, esop 25. 4.217 host diversi.
- **Primi 2.093 CIG con link elaborati** (circa 35 minuti di orologio, 10 host in parallelo, 5 s per host, zero token): CIG citato in una pagina pubblica 137 (6,5 %), CIG con documenti scaricati 62 (201 + 21 documenti), **CIG con almeno un documento che cita il CIG 20** (1,0 %); robots.txt che esclude 317, blocchi 19 (anti-bot ANAC, 403), link alla sola home 314. Costo medio circa 8 s di lavoro per host e 1,3 richieste per CIG.
- Il link PVL porta raramente all'atto: è il limite di L3 (R30). Il residuo va a L4 (sezioni «Bandi di gara e contratti») e L5.
- Blocchi e robots.txt in `esiti/2026-11-07/acquisizione/residuo-s6-blocchi.csv`, da validare nel monitoraggio PVL/AT prima di diventare evidenza: trasparenza-pa.net, cloud.urbi.it e sicopat2 sono software di Amministrazione trasparente, per cui robots.txt non vincola (art. 9 d.lgs. 33/2013): **decisione di Fabio** se ripassarli.

## Misure finora (29/10/2026)

- **L0-L1:** dati aperti ANAC verificati: né l'OCDS bulk né il dataset delle pubblicazioni contengono link ai documenti. Il dataset delle pubblicazioni ha solo CIG e date.
- **L5 (giro 2 della via 6):** con la ricerca web generica un atto dell'ente che cita il CIG si trova in circa 1 contratto su 10. Lo strumento web dell'agente non legge i PDF; da qui lo strumento di archiviazione con estrazione del testo.
- **L6:** prime annotazioni in corso.

## Prima e dopo il 2024

Con il nuovo Codice dei contratti (d.lgs. 36/2023) dal 2024 ogni fase dell'acquisto passa da piattaforme certificate, che trasmettono le schede alla BDNCP. I documenti di gara dovrebbero essere raggiungibili da un puntatore nei dati. Prima, i documenti stavano solo sui siti degli enti, senza un collegamento leggibile da una macchina tra CIG e documento.

Copertura misurata del link ai documenti per CIG e mappa delle piattaforme: [Dove sono i documenti di gara](../sistemi-documenti/) (65,1 % dei CIG 2024-2026).

Per il periodo dal 2024 contano quindi soprattutto i livelli L1-L3, che leggono il puntatore; per il periodo precedente servono scraping e accesso civico (L4-L7). In entrambi i casi non c'è un campo che dica quale prodotto si compra né sotto quale giurisdizione.

Il quadro normativo è **riferito, da verificare** sulle delibere ANAC 261, 263 e 264/2023.

**Misura in programma** (dalla settimana del 2 novembre 2026):
- quota di contratti con il puntatore ai documenti;
- quota di puntatori funzionanti;
- quota di documenti coerenti con il CIG e leggibili;
- completezza delle fasi di esecuzione;
- confronto con il 2022-2023.

Dettaglio e percorso multi-livello in [prima-e-dopo-2024.md](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/metodo/acquisizione/prima-e-dopo-2024.md) (#57).

## Registro delle revisioni

| data | modifica |
|---|---|
| 2026-11-07 | misure L3 sul residuo S6 della via 6 (#57) |
| 2026-10-31 | prima e dopo il 2024: puntatori ai documenti nella BDNCP, misura in programma, percorso multi-livello |
| 2026-10-29 | prima versione: livelli L0-L7, principi, prime misure |
