---
title: "L'imbuto: primi numeri (2024-2025)"
date: 2026-11-03
description: "Come i contratti ANAC dal 2020 vengono esclusi, inclusi o lasciati incerti, strato per strato. Prima quota di sovranità sulla spesa cloud identificata con certezza, con la forbice sull'incerto e la precisione misurata sul campione."
weight: 18
---

**Risultati provvisori.** Le cifre sono misurate da noi sui file ANAC archiviati (**V**) con [`tools/analisi/imbuto.py`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/tools/analisi/imbuto.py) versione 0.3. Gli esiti sono versionati in [`esiti/2026-11-03/imbuto/`](https://github.com/mxmap-it/analisi-spesa-ict/tree/main/esiti/2026-11-03/imbuto). Il metodo è descritto nella [metodologia](../metodologia-sperimentale/) e nell'[evoluzione dei dati](../evoluzione-dati/). Le cifre sono importi dichiarati, non spesa liquidata.

## 1. Gli strati

Ogni contratto ANAC passa per gli strati in ordine. Ogni strato lavora solo sul residuo di quello precedente.

| strato | cosa contiene |
|---|---|
| S0 | accordi quadro e convenzioni padre: sono massimali, non spesa, e si contano a parte |
| S1 | contratti esclusi con certezza perché non ICT (CPV non ICT e nessun termine ICT nell'oggetto) |
| S2 | contratti sotto 500 € |
| S3 | contratti inclusi con certezza da convenzione o lotto noto ([base di conoscenza delle iniziative](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/iniziative_ict.yaml)) |
| S4 | contratti inclusi con certezza perché il marchio di un prodotto è scritto nell'oggetto |
| S5 | ICT non cloud: hardware, reti, servizi applicativi, gestione dei sistemi, consulenza |
| S6 | residuo incerto, in gruppi: mega-contratti, informazione mancante (PSN), incerti significativi, coda |

Importi da 50 milioni in su sono esclusi dai totali e marcati «da verificare». Spesso sono il massimale dell'accordo quadro riportato sul singolo contratto attuativo. Esempio: nell'accordo quadro Consip 91918889EE, 31,7 dei 35,2 miliardi dichiarati stanno in contratti attuativi sopra quella soglia (raccomandazione R22 ad ANAC e Consip).

## 2. Prima quota di sovranità: 2024-2025 (V, provvisoria)

**Spesa identificata con certezza** (S3 e S4), separando il cloud dalle licenze. Il produttore dice la giurisdizione, non se il prodotto è cloud. Una licenza installata nei server dell'ente (on-premise) **non è spesa cloud**. Per le convenzioni di licenze, come Microsoft Enterprise Agreement, la quota cloud (Microsoft 365, Azure) e quella on-premise si accertano nei dossier delle convenzioni, in corso.

| voce | extra-UE | UE | Italia | totale (milioni €) |
|---|---|---|---|---|
| cloud (prodotto nominato) | ~460 (78%) | ~86 | ~47 | ~590 |
| licenze e software, cloud o on-premise da accertare | ~1.140 | ~92 | — | ~1.230 |
| società in house | — | — | ~308 | ~308 |
| servizi professionali sul prodotto | ~60 | ~19 | ~8 | ~87 |

Sul **cloud certo** la quota extra-UE è circa il **78%**. Sulle licenze il produttore è quasi tutto extra-UE, ma resta da stabilire quanta parte sia cloud.

**Spesa incerta sul perimetro cloud** (S6): circa 3,15 miliardi.

| gruppo | milioni € | perché è incerta |
|---|---|---|
| PSN | ~1.920 | dall'oggetto non si sa se il servizio è nativo del PSN (italiano) o cloud pubblico qualificato di un fornitore extra-UE; servono i piani dei fabbisogni (raccomandazione R20) |
| cloud senza provider nell'oggetto | ~1.030 | servono gli atti |
| convenzioni da decifrare | ~200 | in corso di verifica sui documenti Consip |

**Forbice sul cloud.** Si contano il cloud certo (~590 milioni) e l'incerto (~3.150). La quota extra-UE va dal **12%**, se l'incerto fosse tutto italiano, al **96%**, se fosse tutto extra-UE. Il cloud certo è ancora piccolo rispetto all'incerto: restringere la forbice è il lavoro dei prossimi strati, a partire dal PSN.

Fuori dal cloud:
- **ICT non cloud (S5): circa 21 miliardi in due anni.** Comprende servizi applicativi da convenzione (2,6 miliardi), consulenza IT (1,9), hardware (1,9), consulenza per infrastrutture interne (0,66), reti e telefonia (0,75) e una voce «ICT altro» da scomporre (12,8).
- **Oggetto ICT ma categoria merceologica (CPV) non ICT: 3,5 miliardi.** Va vagliato: non è necessariamente cloud.

## 3. Quanto è precisa (V, campione di 611 contratti)

Confronto fra lo strato assegnato dall'imbuto e la classificazione approfondita del campione (modello con ricerca degli atti e revisione), intervallo di Wilson al 95%. Il campione è stratificato, non casuale: la precisione vale per strato.

| strato | contratti nel campione | giurisdizione corretta | è davvero cloud o software? |
|---|---|---|---|
| S4 marchio | 371 | **94%** (92-96%) | 78% (74-82%) |
| S3 convenzione | 13 | 7 su 7 | 7 su 13 |
| S5 ICT non cloud | 71 | — | non cloud nell'89% (79-94%) |
| S6 residuo | 149 | — | 106 cloud secondo il riferimento, fra cui 63 PSN |

**Lettura.**
- Quando l'oggetto nomina un prodotto, la giurisdizione è giusta in più di 9 casi su 10.
- Il dubbio riguarda il perimetro: circa un quinto dei contratti con un marchio sono servizi professionali o altro attorno al prodotto, non il prodotto stesso. Se contarli nella spesa cloud è una decisione di metodo aperta.
- Il residuo S6 è in gran parte davvero cloud. È il punto dove concentrare l'acquisizione dei documenti.

## 4. Cosa manca, in ordine di peso

1. **PSN** (~1,9 miliardi nel 2024-2025): servono i piani dei fabbisogni per contratto (R20).
2. **«ICT altro» in S5** (12,8 miliardi): va scomposto per escludere con certezza ciò che non è cloud.
3. **Contratti cloud senza provider** (~1 miliardo): servono gli atti (livelli L1-L7 di [acquisizione dei documenti](../acquisizione-documenti/)).
4. **SmartCIG**: non ancora nell'imbuto, ed è indispensabile per il 2020-2023.
5. **Base di conoscenza delle convenzioni**: 30 voci, in verifica sui documenti Consip archiviati.

## Registro delle revisioni

| data | modifica |
|---|---|
| 2026-11-03 | prima versione: imbuto 0.3, quota di sovranità 2024-2025 con forbice, precisione sul campione |
| 2026-11-03 | licenze separate dal cloud (Fabio): una licenza on-premise non è cloud; forbice ricalcolata sul solo cloud; regola «verificato = più fonti indipendenti» per le convenzioni |
