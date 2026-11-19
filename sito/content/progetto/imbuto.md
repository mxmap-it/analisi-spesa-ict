---
title: "L'imbuto: come funziona e dove siamo"
date: 2026-11-03
lastmod: 2026-11-19
description: "Come i contratti pubblici ANAC vengono esclusi, inclusi o lasciati incerti, strato per strato, con i numeri aggiornati dagli esiti: spesa ICT, cloud certo e sua giurisdizione, residuo incerto, livelli di raffinamento."
weight: 11
gruppo: inizio
---

<!-- PAGINA GENERATA da tools/pagina_mappa_imbuto.py dagli esiti più recenti e da config/mappa-imbuto.yaml: non modificarla a mano. -->

**Numeri aggiornati automaticamente dagli esiti** (imbuto-0.3.4 (2026-11-09) PROVA-A; fonte `esiti/2026-11-18/imbuto/strati.json`). Gli importi sono **dichiarati**, cioè il valore dei contratti e non la spesa di un anno. La mappa dei dati, dei limiti e delle mancanze è nella [Mappa dell'imbuto](/progetto/mappa-imbuto/). Il dettaglio di ogni passaggio è nel rendiconto [Imbuto: dove siamo](/rendiconti/imbuto-dove-siamo/).

## Che cosa misuriamo

Quanto spende la PA italiana in **servizi cloud** e in **infrastrutture informatiche proprie**, divisa per **giurisdizione del prodotto**: Italia, UE, extra-UE. La giurisdizione si attribuisce al prodotto comprato, non al rivenditore che lo fattura. Il cloud di Microsoft, Google, Amazon e Oracle è extra-UE chiunque lo rivenda, PSN compreso ([criteri di sovranità](/progetto/criteri-sovranita/)).

L'unità di misura è il **contratto** (CIG ANAC). Per ogni contratto ci sono due domande:
1. **è cloud?** (asse A);
2. **di quale giurisdizione?** (asse B).

## Come funziona

Ogni contratto passa per gli strati in ordine, e ogni strato lavora su ciò che resta dal precedente. Il principio (Fabio, 29/10/2026) è:
1. escludere ciò che è **certamente fuori**;
2. includere ciò che è **certamente dentro**;
3. concentrare lo sforzo costoso **solo sull'incerto**.

| strato | che cosa contiene | dal 2024: CIG | dal 2024: mld € dichiarati |
|---|---|---:|---:|
| S0 | accordi quadro e convenzioni «padre»: massimali, contati nei contratti attuativi | 88.792 | — |
| S1 | **esclusi con certezza**: non ICT (CPV, testo e lotto lo escludono insieme) | 3.209.583 | 1.274,5 |
| S2 | sotto 500 € | 147.273 | — |
| S3 | **inclusi** da convenzione o lotto noto ([iniziative](/progetto/iniziative-consip-cloud/)) | 891 | 3,61 |
| S4 | **inclusi** per marchio del prodotto nell'oggetto ([metodo](/progetto/metodo-cloud-provider/)) | 8.370 | 3,63 |
| S5 | ICT non cloud: hardware, reti, servizi applicativi, consulenza | 220.525 | 90,76 |
| S6 | **residuo incerto**: PSN con servizio non noto, cloud senza provider, oggetto ICT con CPV non ICT | 59.406 | 16,37 |

La **spesa ICT** è S3-S6: **289.192 CIG per 114,4 miliardi dichiarati**, che scendono a circa **56 miliardi** al netto dei massimali di accordo quadro copiati sugli attuativi ([rendiconto, § 2.7](/rendiconti/imbuto-dove-siamo/)).

![Il disegno dell'imbuto con i numeri dal 2024](/img/mappa-imbuto/imbuto.svg)

## Il cloud certo e la sua giurisdizione

Dal 2024 sono certi:
- **1,21 miliardi** di cloud (4.556 CIG);
- **0,66 miliardi** di infrastruttura in-house (816 CIG).

L'in-house va letto con cautela, per due motivi:
- **0,36 miliardi** stanno in pochi contratti con importo da verificare. Sono grandi affidamenti come Cloud Toscana e un impianto energetico di CINECA, da rivedere uno per uno.
- **Il livello B** ha controllato chi vince gli altri 298 M€: solo **78 M€** vanno a società pubbliche dell'Indice PA. Il resto va a privati e torna da attribuire ([rendiconto, § 2.9](/rendiconti/imbuto-dove-siamo/)).

![Giurisdizione degli inclusi certi](/img/mappa-imbuto/giurisdizione.svg)

La precisione di S3 e S4 è misurata su sei campioni a cieco annotati da Claude. Quella pesata in euro è circa il 99 % ([metodo](/progetto/metodo-cloud-provider/)). Il settimo campione si fa una sola volta, prima del rendiconto finale.

## Che cosa resta incerto

- **Licenze e software con marchio noto** ma cloud da accertare (Microsoft, Oracle, VMware): **3.889 CIG, 5,37 mld**.
- **Residuo S6:** **59.406 CIG, 16,37 mld**, in quattro gruppi:

| gruppo | che cosa | CIG | mld € |
|---|---|---:|---:|
| G1 | oltre 5 milioni: letti uno per uno (via 6) | 227 | 8,53 |
| G2 | informazione mancante (soprattutto PSN, servizio non noto) | 867 | 4,03 |
| G3 | incerti fra 40.000 € e 5 milioni | 13.437 | 3,16 |
| G4 | coda sotto i 40.000 €, stimata dal campione | 44.875 | 0,65 |

Per la maggior parte del residuo **l'atto di gara che direbbe il prodotto non è raggiungibile da fonti aperte**. Si lavora a livelli, dal più economico al più costoso ([raffinamento](/progetto/raffinamento-imbuto/)). L'accesso civico si usa **solo alla fine**, dopo il rendiconto del risultato parziale ([#78](https://github.com/mxmap-it/analisi-spesa-ict/issues/78)).

## Dopo i livelli di raffinamento: un contratto, un esito

I livelli di raffinamento ([pagina](/progetto/raffinamento-imbuto/)) sono uniti in **una sola tabella per contratto** (`tools/verifiche/imbuto_spostamenti.py`, esito `esiti/2026-11-19/imbuto/spostamenti/riepilogo.json`). Ogni contratto conta una volta. Se due livelli lo spostano in modo diverso vince quello con la prova più forte: verifica sugli atti a mano, poi Claude Opus con gli atti (L4), via 6 controvalidata, Indice PA (B2), quadro economico (B1), Opus sul testo (L3), regole delle licenze, regole sul testo (L2). I contratti toccati sono **14.044**; quelli su cui due livelli non concordano sono 236.

Dal 2024, **al netto dei massimali** di accordo quadro:

| stato | CIG prima | CIG dopo | mld € prima | mld € dopo |
|---|---:|---:|---:|---:|
| incluso certo: cloud | 4.556 | 5.035 | 1,09 | 1,29 |
| incluso certo: infrastruttura in-house | 816 | 438 | 0,42 | 0,08 |
| incerto: marchio o lotto noto, da attribuire | 3.889 | 2.039 | 2,85 | 1,80 |
| incerto: residuo S6 | 59.406 | 48.964 | 11,70 | 10,67 |
| ICT non cloud | 220.525 | 231.137 | 40,01 | 41,90 |
| tolto dall'ICT dai livelli (lavori, non ICT) | 0 | 1.578 | 0,00 | 0,19 |

Che cosa vuol dire, in breve:
- il **cloud certo** sale a **1,29 miliardi**, soprattutto perché le regole delle licenze riconoscono come cloud abbonamenti come Microsoft 365, Azure od Oracle Cloud;
- l'**infrastruttura in-house certa** scende a **0,08 miliardi**: il resto non è confermato dall'Indice PA (aggiudicatari privati o mancanti) e torna da attribuire;
- il **residuo incerto** scende da 11,70 a **10,67 miliardi**.

**Giurisdizione del prodotto sul cloud certo dopo i livelli** (al netto dei massimali): extra-UE **74,9 %**, UE **18,6 %**, Italia **6,4 %**. La quota italiana è bassa perché nel cloud certo pesano gli abbonamenti dei grandi produttori; l'infrastruttura in-house (0,08 mld, Italia) è contata a parte.

Questa quota vale **sui certi**. Sul cloud complessivo non si misura ancora, perché l'incerto (12,5 mld) vale molto più del certo. Per questo non pubblichiamo forbici calcolate su ipotesi. Le mancanze, con peso e gravità, sono nella [Mappa](/progetto/mappa-imbuto/#4-che-cosa-manca-quanto-pesa-come-lo-risolviamo).

## Registro delle revisioni

| data | modifica |
|---|---|
| 2026-11-03 | prima versione: imbuto 0.3, quota di sovranità 2024-2025 con forbice, precisione sul campione |
| 2026-11-03 | licenze separate dal cloud; criteri di sovranità semplificati; imbuto 0.3.1 (PSN incerto) |
| 2026-11-09 | criticità 9: denominatore BDAP dello Stato centrale (#67) |
| 2026-11-19 | nuova sezione «Dopo i livelli di raffinamento»: tabella unica degli spostamenti per contratto (#71), cloud certo netto 1,28 mld, giurisdizione sul cloud certo |
| 2026-11-19 | riscritta e generata dagli esiti (decisione di Fabio): imbuto 0.3.4, giurisdizione degli inclusi certi, residuo per gruppo, raffinamento a livelli; la forbice 13-96 % della 0.3.1 non è più pubblicata finché i livelli non sono uniti; le criticità passano nella Mappa |
