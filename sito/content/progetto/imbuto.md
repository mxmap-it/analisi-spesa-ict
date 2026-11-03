---
title: "L'imbuto: stato e primi numeri (2024-2025)"
date: 2026-11-03
description: "Come i contratti ANAC dal 2020 vengono esclusi, inclusi o lasciati incerti, strato per strato. Prima quota di sovranità sulla spesa cloud identificata con certezza, forbice sull'incerto, precisione misurata, criticità aperte e azioni proposte."
weight: 18
---

<style>
.imb-bar{display:flex;align-items:center;gap:.5rem;margin:.25rem 0;font-size:.9rem}
.imb-bar .lab{flex:0 0 15rem;max-width:45%}
.imb-bar .trk{flex:1;background:#e8ecef;border-radius:3px;height:1.1rem;overflow:hidden;white-space:nowrap}
.imb-bar .fill{height:100%;display:inline-block}
.imb-bar .val{flex:0 0 4.5rem;text-align:right;font-variant-numeric:tabular-nums}
.c-ex{background:#b3261e}.c-ue{background:#1f5fa8}.c-it{background:#2e7d32}.c-inc{background:#9e9e9e}
.imb-leg span{display:inline-block;margin-right:1rem;font-size:.85rem}.imb-leg i{display:inline-block;width:.8rem;height:.8rem;margin-right:.3rem;vertical-align:middle}
@media (max-width:600px){.imb-bar .lab{flex-basis:8rem}}
</style>

**Risultati provvisori.** Cifre misurate da noi sui file ANAC archiviati (**V**) con [`tools/analisi/imbuto.py`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/tools/analisi/imbuto.py) versione 0.3.1; esiti in [`esiti/2026-11-03/imbuto/`](https://github.com/mxmap-it/analisi-spesa-ict/tree/main/esiti/2026-11-03/imbuto). Sono **importi dichiarati**, non spesa liquidata. Le qualificazioni seguono i [criteri di sovranità](../criteri-sovranita/): extra-UE è il cloud di Microsoft, Google, Amazon e Oracle chiunque lo rivenda (PSN compreso); il resto segue l'operatore che eroga in proprio.

## 1. In breve

- Sul **cloud identificato con certezza** (~594 M€ nel 2024-2025) la quota **extra-UE è il 78 %**.
- Ma il cloud certo è piccolo: l'**incerto vale circa 5 volte tanto** (~2,95 miliardi), soprattutto **PSN** (1,9 miliardi), di cui non sappiamo quale servizio sia stato comprato.
- Per questo la quota extra-UE sul cloud complessivo sta oggi in una **forbice 13-96 %**. Per stringerla servono documenti che nei dati ANAC non ci sono: progetti PSN, carrelli delle licenze Microsoft. Molti non sono pubblicati: servirà l'accesso civico.

## 2. Gli strati

Ogni contratto passa per gli strati in ordine; ogni strato lavora sul residuo del precedente.

| strato | cosa contiene | 2024-2025 |
|---|---|---|
| S0 | accordi quadro e convenzioni padre: massimali, contati a parte | — |
| S1 | esclusi con certezza: non ICT | 2,3 milioni di contratti |
| S2 | sotto 500 € | — |
| S3 | inclusi con certezza da convenzione o lotto noto ([base di conoscenza](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/iniziative_ict.yaml), 31 iniziative con dossier) | 539 M€ |
| S4 | inclusi con certezza: marchio del prodotto nell'oggetto | 1.870 M€ |
| S5 | ICT non cloud: hardware, reti, servizi applicativi, consulenza | 21,0 miliardi |
| S6 | residuo incerto: PSN, cloud senza provider, oggetto ICT con CPV non ICT | 6,4 miliardi |

Gli importi da 50 M€ in su sono **esclusi** e marcati «da verificare»: spesso sono il massimale dell'accordo quadro copiato sul contratto attuativo (raccomandazione R22).

## 3. Spesa ICT identificata con certezza (S3 + S4, M€)

<div class="imb-leg"><span><i class="c-ex"></i>extra-UE</span><span><i class="c-ue"></i>UE</span><span><i class="c-it"></i>Italia</span></div>
<div class="imb-bar"><span class="lab">cloud (prodotto nominato)</span><span class="trk"><span class="fill c-ex" style="width:41.1%"></span><span class="fill c-ue" style="width:7.7%"></span><span class="fill c-it" style="width:4.2%"></span></span><span class="val">594</span></div>
<div class="imb-bar"><span class="lab">licenze</span><span class="trk"><span class="fill c-ex" style="width:91.8%"></span><span class="fill c-ue" style="width:8.2%"></span></span><span class="val">1.122</span></div>
<div class="imb-bar"><span class="lab">software infrastrutturale</span><span class="trk"><span class="fill c-ex" style="width:27.3%"></span></span><span class="val">306</span></div>
<div class="imb-bar"><span class="lab">società in house</span><span class="trk"><span class="fill c-it" style="width:27.5%"></span></span><span class="val">308</span></div>
<div class="imb-bar"><span class="lab">servizi professionali sul prodotto</span><span class="trk"><span class="fill c-ex" style="width:5.3%"></span><span class="fill c-ue" style="width:1.7%"></span><span class="fill c-it" style="width:.7%"></span></span><span class="val">87</span></div>

| voce | extra-UE | UE | Italia | totale |
|---|---|---|---|---|
| cloud (prodotto nominato) | 461 (**78 %**) | 86 | 47 | 594 |
| licenze | 1.030 | 92 | — | 1.122 |
| software infrastrutturale | 306 | — | — | 306 |
| società in house | — | — | 308 | 308 |
| servizi professionali sul prodotto | 60 | 19 | 8 | 87 |

Una licenza installata nei server dell'ente **non è cloud** (R-S5). Fra le licenze, quelle **Microsoft** valgono 611 M€. Dall'oggetto risultano 88 M€ di abbonamenti cloud espliciti (Microsoft 365, Dynamics) e 18 M€ di prodotti installati; **504 M€ hanno un oggetto generico** («licenze Microsoft»). Vedi §5.

## 4. Il cloud incerto e la forbice

<div class="imb-bar"><span class="lab">cloud certo</span><span class="trk"><span class="fill c-ex" style="width:15.6%"></span><span class="fill c-ue" style="width:2.9%"></span><span class="fill c-it" style="width:1.6%"></span></span><span class="val">594</span></div>
<div class="imb-bar"><span class="lab">PSN, servizio non noto</span><span class="trk"><span class="fill c-inc" style="width:65%"></span></span><span class="val">1.918</span></div>
<div class="imb-bar"><span class="lab">cloud senza provider</span><span class="trk"><span class="fill c-inc" style="width:34.9%"></span></span><span class="val">1.031</span></div>
<div class="imb-leg"><span><i class="c-inc"></i>incerto</span></div>

**Forbice.** Sul cloud (certo 594 + incerto ~2.950 M€) la quota extra-UE va dal **13 %**, se l'incerto fosse tutto sovrano, al **96 %**, se fosse tutto extra-UE.

Con la regola proposta per le licenze Microsoft (§5) la forbice diventerebbe circa **20-97 %**. La regola conta come cloud certo extra-UE gli 88 M€ di abbonamenti espliciti e tratta il generico come forbice 44-100 %. È una proposta: l'imbuto non la applica ancora.

## 5. Le due incertezze più grandi

### PSN: 1,9 miliardi, servizio non noto
- Nell'oggetto ANAC il servizio è scritto per **l'1 % del valore** (692 contratti): quasi sempre solo «adesione PSN» o «contratto di utenza» ([analisi](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/approfondimento-psn-ea.md)).
- Il documento che lo dice è il **Progetto del piano dei fabbisogni** firmato da PSN. Il suo capitolo «Configuratore» riporta il riepilogo prezzi per famiglia di servizio:
  - Industry Standard (IT);
  - Secure Public Cloud su Azure, Google o AWS, e PSN Managed su Oracle (extra-UE);
  - Hybrid;
  - migrazione e servizi professionali.
- **Campione** di 22 contratti fra i primi 100: Progetto trovato per 2, un addendum per 1 ([dettaglio](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/psn-progetti-campione.md)).
  - Lo pubblicano soprattutto aziende sanitarie e regioni; ministeri e in-house no.
  - Più determine dichiarano l'allegato ma non lo pubblicano.
  - Il riepilogo è un'**immagine** dentro il PDF: si legge solo con OCR.
- Esempi letti (V):
  - Difesa: Secure Public Cloud su **Azure**, 1,7 M€ di canone su 3 anni.
  - ARES Sardegna (una scheda su circa 10): Industry Standard e PSN Managed con canoni piccoli; prevalgono i servizi professionali.
  
  Cinque progetti non bastano per generalizzare.

### Licenze Microsoft: 504 M€ con oggetto generico
- I pesi di gara Consip (44 % «Microsoft 365» in EA6) sono **solo un minimo**, non una stima ([elaborazione](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/ea-quota-cloud-elaborazione.md)).
- I carrelli letti finora (5 enti) sono quasi tutti abbonamenti cloud (ARPA Piemonte 96 %): è un'indicazione, non una stima.
- Il valore è concentrato: i **primi 50 contratti fanno il 77 %**. Leggerli uno per uno li porta a «certo».

## 6. Quanto è precisa (V, campione di 611 contratti)

| strato | contratti nel campione | giurisdizione corretta | è davvero cloud o software? |
|---|---|---|---|
| S4 marchio | 371 | **94 %** (92-96 %) | 78 % (74-82 %) |
| S3 convenzione | 13 | 7 su 7 | 7 su 13 |
| S5 ICT non cloud | 71 | — | non cloud nell'89 % (79-94 %) |
| S6 residuo | 149 | — | 106 cloud secondo il riferimento, fra cui 63 PSN |

Intervalli di Wilson al 95 %. Il campione è stratificato: la precisione vale per strato.

## 7. Criticità aperte e azioni proposte

| # | criticità | peso | azione proposta | stato |
|---|---|---|---|---|
| 1 | PSN: servizio comprato non noto | 1,9 miliardi | Progetti dei piani dei fabbisogni: ricerca sui siti degli enti (copertura bassa), poi **accesso civico a PSN S.p.A. e al DTD** per il riepilogo prezzi di ogni contratto; bilancio PSN 2026 come controllo aggregato | campione fatto; accesso civico: **decisione di Fabio** |
| 2 | Licenze Microsoft con oggetto generico | 504 M€ | lettura dei primi 50 contratti (77 % del valore) e campione del resto; transato per famiglia da Consip (R23) | disegno pronto |
| 3 | Cloud senza provider nell'oggetto | 1,0 miliardi | atti dei contratti (acquisizione a livelli L1-L7) | da avviare |
| 4 | Importi anomali ≥ 50 M€ (massimali copiati, errori ×1000) | esclusi dai totali | regola unica: confronto col massimale del padre, revisione manuale dei casi estremi, totali con e senza | proposta |
| 5 | «ICT altro» in S5 | 12,8 miliardi | scomposizione per escludere con certezza ciò che non è cloud | da avviare |
| 6 | Oggetto ICT con CPV non ICT | 3,5 miliardi | vaglio a campione | da avviare |
| 7 | SmartCIG (indispensabile per il 2020-2023) | — | aggiunta all'imbuto | da avviare |
| 8 | Affidamenti intragruppo (es. Trenitalia → FSTechnology) | caso per caso | sapere come eroga l'affidatario | incerto |

Le richieste ad ANAC, Consip, PSN e DTD emerse dal lavoro sono in [`richieste-e-raccomandazioni.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/metodo/richieste-e-raccomandazioni.yaml). Nessuna è stata inviata.

## Registro delle revisioni

| data | modifica |
|---|---|
| 2026-11-03 | prima versione: imbuto 0.3, quota di sovranità 2024-2025 con forbice, precisione sul campione |
| 2026-11-03 | licenze separate dal cloud (Fabio): una licenza on-premise non è cloud; forbice ricalcolata sul solo cloud |
| 2026-11-03 | criteri di sovranità semplificati applicati alla base di conoscenza (sicurezza da remoto ID 2296 sovrana, SPC Cloud lotto 1 italiano) |
| 2026-11-03 | imbuto 0.3.1: il PSN con servizio non noto è «incerto», non più «Italia»; licenze da convenzione 539 M€; sintesi con grafici, campione dei progetti PSN, elaborazione sulle licenze Microsoft, criticità e azioni |
