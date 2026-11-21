---
title: "Tabellone big tech: cloud e licenze per anno"
subtitle: "Google, Microsoft, Amazon, Oracle e altri: quanto della spesa ICT riconosciuta va in servizi cloud e quanto in licenze"
date: 2026-11-21
lastmod: 2026-11-21T12:00:00Z
description: "Prima versione del tabellone per marchio del prodotto, dai CIG ANAC 2020-2026 classificati dall'imbuto: cloud, licenze e software installato, incerto."
---

**Versione 0.1 del 2026-11-21** · ticket [#83](https://github.com/mxmap-it/analisi-spesa-ict/issues/83) (voce A) · [registro delle revisioni](#registro-delle-revisioni)

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

«–» = non misurato in quell'anno. Il 2026 è parziale: il mirror ANAC arriva al delta CIG del 1/10/2026.

## 4. Copertura dei dati

I CIG ANAC sono nel mirror fino al delta del 1/10/2026; i dati OCDS si fermano a marzo 2026 ([rapporto ANAC](/rendiconti/anac-2026-10-problemi/)). Il grafico per trimestre della copertura è previsto nella prossima versione.

## 5. Rifare il calcolo

```
python tools/verifiche/tabellone_bigtech.py 2026-11-21
```
Ingressi: `lavoro/imbuto/stati-finali.csv.gz` e `lavoro/imbuto/ict.csv` (ripristinabili dal registro, `tools/ingressi_lavoro.py ripristina`). Uscita: `esiti/2026-11-21/statistiche/tabellone-bigtech.{csv,json}`.

## Registro delle revisioni

| versione | data | cosa cambia |
|---|---|---|
| 0.1 | 2026-11-21 | Prima versione: tabellone per marchio e anno, tre colonne (#83 voce A). |
