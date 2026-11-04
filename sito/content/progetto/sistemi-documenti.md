---
title: "Dove sono i documenti di gara: il link per CIG e la mappa dei sistemi"
date: 2026-11-04
description: "Quota dei CIG 2024-2026 con il link ai documenti di gara pubblicato da ANAC (Pubblicità a valore legale), e mappa dei 36.888 domini e piattaforme a cui punta."
weight: 19
---

Versione 1.0 del 4/11/2026 (#57). Metodo e ripetizione: [`report/metodo/acquisizione/dettaglio-cig.md`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/metodo/acquisizione/dettaglio-cig.md).

## Da dove viene il link

Per ogni CIG la scheda di [dettaglio-cig](https://dettaglio-cig.anticorruzione.it/) mostra il link alla pagina dell'ente o della piattaforma con i documenti della gara. Quella pagina interroga un servizio protetto da CAPTCHA, che non usiamo in massa. Lo stesso valore (`documenti_di_gara_link`) è nell'API pubblica della **Pubblicità a valore legale** (PVL) di ANAC, che abbiamo scaricato per intero: 2.753.119 avvisi pubblicati dal 1/1/2024 al 3/11/2026. Il campo **non c'è nei dataset open data in blocco** e la PVL **non ha avvisi prima del 2024**.

## Disponibilità (verificata, CIG BDNCP con anno di pubblicazione 2024-2026)

| | CIG | quota |
|---|---:|---:|
| CIG nel BDNCP 2024-2026 | 3.734.845 | 100 % |
| con almeno un avviso PVL | 2.611.389 | 69,9 % |
| con il link ai documenti | 2.431.252 | **65,1 %** |

- **Per mese:** quasi nulla a gennaio e febbraio 2024 (1,5 % e 3,2 %), poi stabile fra il 62 % e il 77 %.
- **Per procedura:** gli affidamenti diretti hanno il link nel 69,7 % dei casi. Restano senza nessun avviso le adesioni a convenzioni e accordi quadro (93.485 CIG, 0 %) e gli affidamenti in house (30.214 CIG, avviso presente, link 0 %).
- **Per importo:** il link c'è nel 79 % dei CIG fra 5 e 40 mila euro e nel 16 % di quelli sotto 5 mila; sopra 221 mila euro fra il 41 % e il 52 %.
- **Per scheda PVL:** AD3 (affidamenti diretti) 96 %, bandi P1_16 99 %; esiti A3_6 0 %.
- 174.834 CIG che compaiono negli avvisi PVL non sono nei file BDNCP 2024+ (CIG più vecchi o mancanti nei mensili): da analizzare.

Le somme degli importi (colonna `importo_mln`) contengono valori anomali dei file BDNCP e non vanno lette come spesa.

## La mappa dei sistemi

36.888 domini distinti. La piattaforma è attribuita solo quando il dominio la identifica con certezza; tutto il resto è «ignota» (34.464 domini, 1,8 milioni di CIG).

| piattaforma | gestore | domini | CIG |
|---|---|---:|---:|
| MePA / Acquisti in rete | Consip | 5 | 126.648 |
| Traspare | Traspare | 1.179 | 112.477 |
| Appalti e Contratti e-Procurement | Maggioli | 290 | 96.015 |
| TuttoGare | Studio Amica | 858 | 95.638 |
| Portale appalti Alto Adige | Provincia di Bolzano | 4 | 65.907 |
| Sintel | ARIA | 12 | 61.512 |
| START | Regione Toscana | 9 | 51.923 |
| ASMECOMM | ASMEL | 2 | 36.404 |
| SATER | Intercent-ER | 1 | 28.387 |
| STELLA | Regione Lazio | 1 | 21.560 |
| EmPULIA | InnovaPuglia | 2 | 15.426 |
| Soresa | So.Re.Sa. | 3 | 14.448 |
| eAppaltiFVG | Regione FVG | 2 | 12.460 |
| SaturnWeb | Saturn | 16 | 12.129 |

Fra i domini «ignoti» più frequenti ci sono dati.anticorruzione.it (89.873 CIG: l'ente rimanda alla stessa ANAC), trasparenza-pa.net, halleyweb.com, app.albofornitori.it, web.spaggiari.eu, trasparenzascuole.it, nuvola.madisoft.it, cioè software di trasparenza molto diffusi fra comuni e scuole. Si possono attribuire dopo una verifica, famiglia per famiglia.

**Verifica a campione** (un link per dominio, 300 domini principali e 100 a caso, una richiesta ogni ≥ 3 s, senza login): 44 pagine con documenti scaricabili nell'HTML, 1 documento diretto, 158 con indizi di login o area riservata, 65 senza documenti visibili, 39 errori HTTP, 93 senza risposta. Sono stime per difetto: molti portali caricano i documenti via JavaScript, e l'indizio «login» scatta anche per un semplice link «Accedi». Il passo successivo è un controllo con un browser reale, famiglia per famiglia.

## Open data

In [`esiti/pvl-link-cig/2026-11-04/`](https://github.com/mxmap-it/analisi-spesa-ict/tree/main/esiti/pvl-link-cig/2026-11-04): `totale`, `anno-mese`, `procedura`, `classe-importo`, `tipo-ente`, `regione`, `oggetto`, `scheda-pvl`, `stazione-appaltante` (per codice fiscale), `pvl-vs-bdncp`, `sistemi` (un dominio per riga), `piattaforme`, `verifica-link`. CSV UTF-8. Gli avvisi grezzi sono archiviati con il loro sha256.
