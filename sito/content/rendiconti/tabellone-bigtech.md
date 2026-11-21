---
title: "Tabellone big tech: cloud e licenze per anno"
subtitle: "Google, Microsoft, Amazon, Oracle e altri: quanto della spesa ICT riconosciuta va in servizi cloud e quanto in licenze"
date: 2026-11-21
lastmod: 2026-11-21T12:00:00Z
description: "Prima versione del tabellone per marchio del prodotto, dai CIG ANAC 2020-2026 classificati dall'imbuto: cloud, licenze e software installato, incerto."
---

**Versione 0.6 del 2026-11-21** · ticket [#83](https://github.com/mxmap-it/analisi-spesa-ict/issues/83) (voce A) · [registro delle revisioni](#registro-delle-revisioni)

Legenda: **[V]** misurato da noi, con il comando per rifarlo; **[S]** stima o risultato parziale.

## 1. Cosa misura

Per ogni CIG che l'imbuto ha attribuito a un **marchio di prodotto** (lente prodotto, [metodo](/progetto/metodo-cloud-provider/)) si conta l'importo netto (al netto dei tetti degli accordi quadro e degli errori d'importo) in tre colonne:

- **cloud**: servizio erogato dal produttore o per suo conto (stato *cloud certo*);
- **licenze**: licenze, software installato presso l'ente, supporto (stato *ICT non cloud* con marchio);
- **incerto**: il marchio è certo ma non si sa se è cloud, ad esempio «licenze Microsoft» o adesioni all'Enterprise Agreement senza dettaglio: il carrello sta nell'atto.

È un risultato **parziale [S]**: conta solo i CIG in cui il marchio si riconosce dal testo, non la spesa che passa da rivenditori o convenzioni senza marchio nell'oggetto. La colonna *licenze* è misurata **solo dal 2024** (perimetro della [verifica delle licenze](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/tools/verifiche/imbuto_licenze.py)): per il 2020-2023 quei CIG restano nell'incerto.

## 2. Totale 2020-2026 (milioni di euro netti) [V]

<!-- GEN:totale -->
| marchio | cloud | licenze (dal 2024) | incerto |
|---|---:|---:|---:|
| Microsoft | 639,7 (2.668 CIG) | 50,5 (460) | 1.852,1 (2.063) |
| Oracle | 112,8 (239) | 131,6 (98) | 813,2 (753) |
| Amazon | 145,0 (276) | 1,6 (51) | 2,5 (21) |
| Google | 134,5 (677) | 1,9 (43) | 9,4 (17) |
| altri marchi | 986,3 (2.709) | 572,4 (470) | 400,6 (724) |
<!-- /GEN:totale -->

**Come leggerlo.** Il grosso di Microsoft (1,85 miliardi) e Oracle (0,81) è ancora *incerto*: sono licenze ed Enterprise Agreement di cui non sappiamo se coprono servizi cloud (Microsoft 365, Azure) o software installato. Risolverlo richiede gli atti (accesso civico, [#58](https://github.com/mxmap-it/analisi-spesa-ict/issues/58)).

## 3. Per anno (milioni: cloud / licenze / incerto) [V]

<!-- GEN:anni -->
| marchio | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|
| Microsoft | 45/–/160 | 31/–/121 | 76/–/220 | 78/–/486 | 100/11/523 | 198/31/207 | 111/8/135 |
| Oracle | 4/–/77 | 12/–/134 | 20/–/120 | 14/–/138 | 14/108/75 | 13/6/159 | 35/17/111 |
| Amazon | 1/–/0 | 4/–/0 | 32/–/1 | 27/–/1 | 10/0/0 | 36/1/0 | 34/1/0 |
| Google | 3/–/0 | 6/–/5 | 37/–/1 | 31/–/4 | 7/1/0 | 16/0/0 | 33/1/0 |
| altri | 20/–/64 | 72/45/63 | 79/33/80 | 165/1/101 | 212/82/39 | 261/203/32 | 177/209/20 |
<!-- /GEN:anni -->

«–» = non misurato in quell'anno (la verifica delle licenze copre in modo sistematico solo dal 2024; i valori 2021-2023 di «altri» vengono da altre vie dell'imbuto). Il 2026 è parziale: il mirror ANAC arriva al delta CIG del 1/10/2026.

## 4. Copertura dei dati per trimestre [V]

CIG pubblicati per trimestre nel mirror ANAC (tra parentesi quelli che l'imbuto tiene come ICT). Il mirror arriva al delta CIG del 1/10/2026: **il trimestre corrente (T4 2026) è di fatto assente** e il T3 2026 può ancora crescere con i delta successivi. I dati OCDS si fermano a marzo 2026 ([rapporto ANAC](/rendiconti/anac-2026-10-problemi/)).

| anno | T1 | T2 | T3 | T4 |
|---|---:|---:|---:|---:|
| 2020 | 86.303 (3.801 ICT) | 88.481 (3.792 ICT) | 95.384 (3.722 ICT) | 118.446 (6.575 ICT) |
| 2021 | 99.513 (4.383 ICT) | 112.695 (4.571 ICT) | 103.392 (4.181 ICT) | 115.861 (6.451 ICT) |
| 2022 | 104.481 (7.376 ICT) | 122.510 (5.800 ICT) | 123.227 (4.844 ICT) | 141.080 (12.288 ICT) |
| 2023 | 150.407 (16.487 ICT) | 174.964 (23.945 ICT) | 136.859 (23.071 ICT) | 194.393 (22.245 ICT) |
| 2024 | 223.805 (12.705 ICT) | 319.094 (17.632 ICT) | 282.790 (19.367 ICT) | 399.414 (34.643 ICT) |
| 2025 | 348.231 (29.387 ICT) | 369.306 (28.314 ICT) | 328.541 (22.955 ICT) | 418.328 (37.695 ICT) |
| 2026 | 366.220 (32.837 ICT) | 360.857 (27.173 ICT) | 319.799 (24.715 ICT) | 2.183 (237 ICT) |

Comando: `python tools/verifiche/copertura_trimestri.py 2026-11-21` → `esiti/2026-11-21/statistiche/copertura-trimestri.{csv,json}`.

## 5. Controprova con la posta degli enti (mxmap.it) [V]

Seconda via indipendente ([#83](https://github.com/mxmap-it/analisi-spesa-ict/issues/83) voce B): la scansione di [mxmap.it](https://mxmap.it/) dice su quale piattaforma ogni ente ha la posta; i CIG 2023-2026 dicono se l'ente ha acquisti con quel marchio riconosciuti dalla lente prodotto. Abbinati tramite IndicePA (codice IPA → codice fiscale) 14.915 enti su 22.912.

| posta dell'ente | enti | con acquisti Microsoft | con acquisti Google |
|---|---:|---:|---:|
| Microsoft | 1.854 | 557 (30,0 %) | 29 (1,6 %) |
| Google | 5.750 | 155 (2,7 %) | 169 (2,9 %) |
| altri provider | 7.311 | 341 (4,7 %) | 79 (1,1 %) |

**Cosa ci dice.**
- La lente prodotto riconosce Microsoft dove Microsoft c'è davvero: gli enti con posta Microsoft hanno acquisti Microsoft **6 volte** più spesso degli altri.
- Ma **il 70 % degli enti con posta Microsoft non ha nessun CIG Microsoft riconosciuto**: la spesa passa da convenzioni, rivenditori o oggetti senza marchio. È la misura del punto cieco della lente, e il motivo per cui il tabellone è un minimo, non un totale [S].
- Per Google lo scarto è piccolo (2,9 % contro 1,1 %): l'87 % degli enti con posta Google sono scuole (categoria IPA L33: 4.986 su 5.750), che usano di norma Google Workspace for Education senza un contratto a pagamento.

Comando: `python tools/verifiche/posta_acquisti.py 2026-11-21` → `esiti/2026-11-21/statistiche/posta-acquisti.json`.

## 6. Confronto con un altro progetto civico (sovranita-digitale.it) [V]

Controprova con la [dashboard dei contratti ICT](https://www.sovranita-digitale.it/contratti-ict/) di sovranita-digitale.it ([#83](https://github.com/mxmap-it/analisi-spesa-ict/issues/83) voce C). I loro dati (`kpi_report.json` del 19/9/2026, archiviato con sha256 nel nostro mirror) sono **riferiti da loro**, non riprodotti: li usiamo solo per vedere se gli ordini di grandezza tornano.

| marchio | loro: OCDS gen 2024-mar 2026, CPV 48/72, importi lordi | noi: tutti i CIG 2024-set 2026, importi netti (cloud+licenze+incerto) |
|---|---:|---:|
| Microsoft | 1.857,0 M€ (765 contratti) | 1.324,5 M€ (3.759 CIG) |
| Oracle | 173,5 M€ (231) | 538,9 M€ (543) |
| Google | 30,0 M€ (166) | 58,7 M€ (564) |
| Amazon | 16,1 M€ (49) | 82,2 M€ (253) |

**Perché differiscono.** (1) L'OCDS contiene circa un quinto degli affidamenti ([#38](https://github.com/mxmap-it/analisi-spesa-ict/issues/38)): noi troviamo 3-5 volte più CIG; (2) loro contano importi lordi, inclusi i massimali degli accordi quadro che noi togliamo, e per questo Microsoft risulta più alto da loro pur con meno contratti; (3) il filtro per CPV 48/72 perde gli acquisti classificati con CPV non ICT ([rapporto CPV](/rendiconti/perimetro-cpv/)). Lo stesso errore d'importo di Lunamatrona compare nelle loro anomalie (ANOM-020); quello di Roseto degli Abruzzi pesa invece ancora nel loro totale dei fornitori. Curiosità che spiega l'errore: i 384.350.435 € dichiarati sono la partita IVA del fornitore (Halley Informatica, 00384350435) scritta nel campo importo.

Non è stato possibile un confronto analogo con [dovevannoinostrisoldi.com](https://www.dovevannoinostrisoldi.com/): la piattaforma copre la spesa pubblica in generale, non pubblica una ripartizione per marchio ICT e i suoi dati passano da `/api/`, escluso dal robots.txt.

## 7. Università statali e AWS: un'ipotesi alla prova dei CIG [V]

Ipotesi **riferita, non verificata** ([#83](https://github.com/mxmap-it/analisi-spesa-ict/issues/83) voce D): le università starebbero spostando le infrastrutture su AWS con i fondi PNRR. Con i CIG delle 71 università statali (IndicePA categoria L17, 35.880 CIG 2020-2026):

- **cloud certo**: 15,6 M€ in sette anni; **AWS diretto: 0,47 M€** (2021: 0,26; 2023: 0,03; 2025: 0,11; 2026: 0,07). Google 2,15 M€, Microsoft 1,06 M€, Oracle 0,75 M€, altri marchi 11,1 M€;
- ancora **incerti** 320 M€ (strato S6), più 226 M€ di datacenter propri e 25,9 M€ affidati a in-house.

**Conclusione [S].** Nei CIG diretti delle università la migrazione su AWS **non si vede**. Non si può però escludere: passerebbe da rivenditori o convenzioni con oggetti senza marchio, dai 320 M€ ancora incerti, o dai servizi del consorzio CINECA. Per chiuderla servono gli atti (accesso civico) o i dati dei progetti PNRR delle università.

Comando: `python tools/verifiche/universita_cloud.py 2026-11-21` → `esiti/2026-11-21/statistiche/universita-cloud.{csv,json}`.

## 8. Contesto: la Strategia Cloud Italia 2027-2029

Il 16/11/2026 il Comitato interministeriale per la transizione digitale ha approvato la nuova Strategia Cloud Italia 2027-2029 ([annuncio del Dipartimento](https://innovazione.gov.it/notizie/articoli/strategia-cloud-italia-2027-2029-levoluzione-delle-infrastrutture-digitali-del-nostro-paese/), archiviato, sha256 `517de8b9…`). Entra in vigore nel 2027 dopo la Conferenza unificata; **il testo integrale non è ancora pubblicato** ([#83](https://github.com/mxmap-it/analisi-spesa-ict/issues/83) voce F). Dall'annuncio, due obiettivi toccano direttamente questa misura:

- «promuovere soluzioni tecnologiche europee e open-source, **mappando e riducendo le dipendenze da fornitori extra-UE**»: è esattamente ciò che il tabellone prova a misurare, e la Strategia non dice ancora con quale base dati;
- un «ecosistema nazionale federato» del PSN con le **infrastrutture territoriali adeguate**: rientra nella misura del [cloud in proprio](/rendiconti/cloud-in-proprio/) e delle [società ICT pubbliche](/rendiconti/societa-ict-pubbliche/).

Raccomandazione annotata (R91): pubblicare il testo e la **base di partenza** della mappatura delle dipendenze extra-UE, con il metodo, perché sia ripetibile da chiunque.

## 9. Rifare il calcolo

```
python tools/verifiche/tabellone_bigtech.py 2026-11-21
```
Ingressi: `lavoro/imbuto/stati-finali.csv.gz` e `lavoro/imbuto/ict.csv` (ripristinabili dal registro, `tools/ingressi_lavoro.py ripristina`). Uscita: `esiti/2026-11-21/statistiche/tabellone-bigtech.{csv,json}`.

## Registro delle revisioni

| versione | data | cosa cambia |
|---|---|---|
| 0.1 | 2026-11-21 | Prima versione: tabellone per marchio e anno, tre colonne (#83 voce A). |
| 0.2 | 2026-11-21 | Controprova con la posta degli enti da mxmap.it (#83 voce B). |
| 0.3 | 2026-11-21 | Confronto con sovranita-digitale.it (#83 voce C). |
| 0.4 | 2026-11-21 | Università statali e AWS (#83 voce D). |
| 0.5 | 2026-11-21 | Contesto: Strategia Cloud Italia 2027-2029 (#83 voce F). |
| 0.6 | 2026-11-21 | Copertura dei dati per trimestre; nota su dovevannoinostrisoldi.com (#83 voci A e C). |
