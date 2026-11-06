---
title: "Convenzioni e accordi quadro ICT"
date: 2026-11-05
description: "Le principali iniziative ICT (Consip, PSN, soggetti aggregatori, consorzi): valore, documenti archiviati e mancanti."
---

<!-- Generata da tools/convenzioni/pagine.py dalla base dati report/convenzioni/database/: non modificare a mano. -->


**[Apri la griglia di tutte le iniziative](/convenzioni/griglia/)**: documenti archiviati, reperiti altrove, mancanti e richiesti, in una vista sola. Rapporto: [Trasparenza delle convenzioni ICT](/rendiconti/convenzioni-trasparenza/) (bozza).

Censimento di **86 iniziative** (82 attive, 4 storiche) con i loro lotti, i documenti pubblici archiviati e quelli che mancano. Copertura documentale media: **37 %** dei tipi di documento attesi.

**Criterio.** Un'iniziativa è un ID Sigef Consip, o una gara (CIG padre) di un altro soggetto. È «attiva» se ha CIG derivati con CPV ICT nel 2024-2025 (o è nuova: PRINCO ID 2928, IaaS/PaaS 2 ID 2746). Si prendono le prime per valore dei derivati ICT 2024-2025 in ciascun tipo di soggetto (40 Consip, 25 aggregatori regionali, 15 consorzi o unioni, 10 altri; fuori Consip almeno 3 derivati e 1 M€), più il PSN. Le iniziative della base di conoscenza senza derivati recenti ma con almeno 100 M€ dal 2020 sono elencate a parte come «storiche». Dettagli: [README della base dati](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/database/README.md).

Per il contesto cloud vedi [Iniziative Consip cloud](/progetto/iniziative-consip-cloud/).

Le tabelle si possono ordinare e filtrare (anche per tipo di soggetto, colonna «Tipo»).

## Carenze di trasparenza

Dati che non vengono pubblicati pur servendo a controllare la spesa e la sovranità. «Accertato» = non trovato sulla pagina del bando su consip.it, negli open data Consip né nel campione di enti (consultati il 05/11/2026; tipo dedotto dal nome dei file); «da verificare» = fonti non ancora consultate. Valore = somma dei derivati ICT 2024-2025 delle iniziative colpite (BDNCP, elaborazione del 05/11/2026; ordine di grandezza, non transato).

| Carenza | Iniziative colpite (accertato / da verificare) | M€ coinvolti (accertato) | Obbligo di pubblicare? | Proposta |
|---|---|---|---|---|
| **C1** Offerte tecniche dei vincitori | 41 / 45 | 50.697,5 | no | R39 |
| **C2** Listini e prezzi offerti dagli aggiudicatari | 1 / 85 | 0,0 | no | R39 |
| **C3** Transato per listino, marchio ed ente | 39 / 47 | 50.468,3 | no | R37 |
| **C4** Ordinativi e contratti attuativi | 41 / 44 | 50.697,5 | in parte | R08 |
| **C5** Progetti e piani dei fabbisogni | 0 / 1 | 0,0 | no | R41 |
| **C6** Region e data center dichiarati | 2 / 3 | 0,0 | no | R42 |
| **C7** Monitoraggio delle soglie di erosione dei massimali | 26 / 60 | 46.283,1 | no | R37 |
| **C8** Indice ID Sigef ↔ CIG dei lotti | 4 / 41 | 951,7 | no | R38 |

Per tipo di soggetto (iniziative colpite / iniziative del tipo):

| Carenza | Consip | PSN | Aggregatore regionale | Consorzio o unione | Altro |
|---|---|---|---|---|---|
| C1 Offerte tecniche dei vincitori | 45/45 | 1/1 | 25/25 | 4/4 | 11/11 |
| C2 Listini e prezzi offerti dagli aggiudicatari | 45/45 | 1/1 | 25/25 | 4/4 | 11/11 |
| C3 Transato per listino, marchio ed ente | 45/45 | 1/1 | 25/25 | 4/4 | 11/11 |
| C4 Ordinativi e contratti attuativi | 45/45 | 0/1 | 25/25 | 4/4 | 11/11 |
| C5 Progetti e piani dei fabbisogni | 1/45 | 0/1 | 0/25 | 0/4 | 0/11 |
| C6 Region e data center dichiarati | 4/45 | 1/1 | 0/25 | 0/4 | 0/11 |
| C7 Monitoraggio delle soglie di erosione dei massimali | 45/45 | 1/1 | 25/25 | 4/4 | 11/11 |
| C8 Indice ID Sigef ↔ CIG dei lotti | 45/45 | 0/1 | 0/25 | 0/4 | 0/11 |

Basi normative e ragioni: [carenze.yaml](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/database/carenze.yaml) e [scheda normativa](/progetto/normativa-documenti-gara/). Rimedio di breve periodo: [bozze di accesso civico generalizzato](/convenzioni/accesso-civico/) (preparate, non inviate). Proposte di policy: R08, R37-R43 in richieste-e-raccomandazioni.yaml.

## Iniziative attive

Valori: BDNCP, derivati ICT 2024-2025 (mirror ANAC, elaborazione del 05/11/2026); documenti al 05/11/2026.

| # | Iniziativa | Tipo | M€ ICT 2024-25 | Derivati | Documenti presenti | Mancanti (crit. 3/2/1) | Accesso civico | Copertura |
|---|---|---|---|---|---|---|---|---|
| 1 | [Consip AQ Servizi applicativi in ottica cloud e Demand/PMO PA centrali, seconda edizione (ID Sigef 2483), lott](/convenzioni/consip-2483/) | Consip | 29.917,7 | 414 | 66 | 9 (6/0/3) | 2 istanze in preparazione | 69 % |
| 2 | [Consip Servizi applicativi in ottica cloud 3 (PAL), ID 2610](/convenzioni/consip-2610/) | Consip | 5.953,3 | 286 | 53 | 6 (4/1/1) | 2 istanze in preparazione | 69 % |
| 3 | [Consip Licenze Microsoft Enterprise Agreement 8, ID 2615](/convenzioni/consip-2615/) | Consip | 3.015,2 | 321 | 37 | 9 (5/1/3) | 2 istanze in preparazione | 77 % |
| 4 | [Polo Strategico Nazionale (PPP, Presidenza del Consiglio)](/convenzioni/psn/) | PSN | 2.077,9 | 433 | 45 | 6 (3/1/2) | 1 istanza in preparazione | 36 % |
| 5 | [Consip AQ PC portatili, mobile workstation e Chromebook, ID 2425, lotto 1 PC portatili](/convenzioni/consip-2425/) | Consip | 1.616,7 | 468 | 67 | 5 (4/0/1) | 1 istanza in preparazione | 69 % |
| 6 | [Consip AQ Servizi di sicurezza da remoto, compliance e controllo, ID 2296, lotto 1 sicurezza da remoto](/convenzioni/consip-2296/) | Consip | 1.324,8 | 248 | 38 | 8 (2/5/1) | 1 istanza in preparazione | 62 % |
| 7 | [Consip Digital transformation 2, ID 2536, lotto 2 digitalizzazione dei processi](/convenzioni/consip-2536/) | Consip | 969,7 | 146 | 32 | 13 (5/2/6) | 1 istanza in preparazione | 69 % |
| 8 | [Consip Licenze software multibrand 6, ID 2599, lotto 1 prodotti Oracle](/convenzioni/consip-2599/) | Consip | 918,2 | 387 | 99 | 5 (3/0/2) | 2 istanze in preparazione | 77 % |
| 9 | [Consip AQ Sanità digitale, sistemi informativi gestionali](/convenzioni/consip-2366/) | Consip | 834,1 | 45 | 85 | 12 (7/0/5) | 1 istanza in preparazione | 62 % |
| 10 | [Consip AQ System management ed. 3, ID 2275, lotto 1](/convenzioni/consip-2275/) | Consip | 746,9 | 119 | 27 | 8 (7/1/0) | 1 istanza in preparazione | 62 % |
| 11 | [GARA A PROCEDURA APERTA PER L’APPALTO DI FORNITURA MULTIBRAND DI PRODOTTI SOFTWARE, MANUTENZIONE SOFTWARE E SE](/convenzioni/consip-2738/) | Consip | 696,5 | 380 | 101 | 3 (3/0/0) | 2 istanze in preparazione | 77 % |
| 12 | [Consip Licenze Microsoft Enterprise Agreement 9, ID 2755 (ipotesi forte, CIG non presente negli avvisi eForms)](/convenzioni/consip-2755/) | Consip | 691,6 | 186 | 37 | 4 (3/0/1) | 2 istanze in preparazione | 77 % |
| 13 | [Consip Sanità digitale, sistemi clinico assistenziali 2, ID 2601, lotto 2 cartella clinica](/convenzioni/consip-2601/) | Consip | 557,5 | 242 | 57 | 11 (5/0/6) | 1 istanza in preparazione | 69 % |
| 14 | [Consip Reti locali 8, ID 2223, lotto 2 PAL](/convenzioni/consip-reti-locali-8/) | Consip | 554,2 | 251 | 9 | 10 (4/2/4) | 1 istanza in preparazione | 31 % |
| 15 | [Consip PC desktop e workstation 3, ID 2631, lotto 2](/convenzioni/consip-2631/) | Consip | 469,4 | 1383 | 30 | 7 (4/0/3) | 1 istanza in preparazione | 69 % |
| 16 | [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN ACCORDO QUADRO, AI SENSI DEL D.LGS. 50/2016 E S.M.I., AVENTE ](/convenzioni/cig-91881762b3/) | Consip | 354,3 | 149 | 0 | 8 (5/2/1) | 1 istanza in preparazione | 8 % |
| 17 | [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN ACCORDO QUADRO, AI SENSI DEL D.LGS. 50/2016 E S.M.I., AVENTE ](/convenzioni/cig-8765571a03/) | Consip | 325,0 | 206 | 36 | 13 (7/1/5) | 1 istanza in preparazione | 54 % |
| 18 | [AQ SERVIZI DI GESTIONE E MANUTENZIONE DI SISTEMI IP E POSTAZIONE DI LAVORO 2 - ID 2648 / LOTTO 4](/convenzioni/consip-2648/) | Consip | 307,8 | 80 | 51 | 7 (5/0/2) | 1 istanza in preparazione | 69 % |
| 19 | [Consip AQ Sanità digitale, sistemi informativi sanitari e servizi al cittadino (ID Sigef 2365), lotto 2 CUP e ](/convenzioni/consip-2365/) | Consip | 297,1 | 69 | 69 | 11 (6/1/4) | 1 istanza in preparazione | 69 % |
| 20 | [Consip SPC2 Connettività (contratto quadro OPA)](/convenzioni/cig-5133642f61/) | Consip | 257,8 | 444 | 1 | 9 (5/2/2) | 1 istanza in preparazione | 15 % |
| 21 | [AQ PER I SERVIZI DI GESTIONE E MANUTENZIONE DI SISTEMI IP E POSTAZIONI DI LAVORO PER LE PPAA - ID 2181 / AQ SG](/convenzioni/consip-2181/) | Consip | 232,3 | 53 | 50 | 9 (5/3/1) | 1 istanza in preparazione | 77 % |
| 22 | [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN ACCORDO QUADRO, AI SENSI DEL D.LGS. 50/2016 E S.M.I., AVENTE ](/convenzioni/cig-9030521daa/) | Consip | 227,5 | 198 | 52 | 13 (7/1/5) | 1 istanza in preparazione | 54 % |
| 23 | [GARA A PROCEDURA APERTA PER L'AFFIDAMENTO DI UN ACCORDO QUADRO AI SENSI DELL'ART. 54 COMMA 3 DEL D. LGS. 50/20](/convenzioni/cig-8898059e90/) | Consip | 225,4 | 274 | 0 | 8 (5/2/1) | 1 istanza in preparazione | 8 % |
| 24 | [CLOUD ENABLING 1 ID 2652 / LOTTO 1: SERVIZI SUPPORTO ALL'ADOZIONE E PMO - PAC1](/convenzioni/consip-2652/) | Consip | 189,8 | 99 | 46 | 6 (5/0/1) | 1 istanza in preparazione | 69 % |
| 25 | [ARIA_2023_807 - PROCEDURA APERTA, AI SENSI DELL’ART. 60 DEL D.LGS. N. 50/2016, PER LA STIPULA DI UN ACCORDO QU](/convenzioni/cig-989984280e/) | Aggregatore regionale | 160,1 | 15 | 7 | 8 (5/1/2) | 1 istanza in preparazione | 8 % |
| 26 | [GARA A PROCEDURA APERTA SUDDIVISA IN 4 LOTTI PER L'AFFIDAMENTO DEI SERVIZI DI SVILUPPO E GESTIONE DEL SISTEMA ](/convenzioni/consip-1774/) | Altro | 147,4 | 15 | 9 | 29 (5/6/18) | 2 istanze in preparazione | 31 % |
| 27 | [Consip AQ System management ed. 4, ID 2710 (lotto unico)](/convenzioni/consip-2710/) | Consip | 145,4 | 49 | 37 | 8 (4/3/1) | 1 istanza in preparazione | 62 % |
| 28 | [GARA A PROCEDURA APERTA, SUDDIVISA IN 8 LOTTI, PER LA STIPULA DI UNA CONVENZIONE PER OGNI LOTTO, AI SENSI DELL](/convenzioni/cig-b0da5c472c/) | Consip | 114,2 | 640 | 0 | 7 (5/1/1) | 1 istanza in preparazione | 8 % |
| 29 | [PROCEDURA NEGOZIATA PER L'AFFIDAMENTO DI SERVIZI IN OUTSOURCING DI CUSTOMER CARE (CALL CENTER INBOUND E ATTIVI](/convenzioni/cig-a0260b3155/) | Altro | 100,4 | 21 | 0 | 11 (5/3/3) | – | 8 % |
| 30 | [AQ PER LA FORNITURA DI PRODOTTI CLOUD IAAS E PAAS - ID 2213 / LOTTO 8 - PAC2 - SERVIZI TECNOLOGICI](/convenzioni/consip-2213/) | Consip | 90,2 | 41 | 83 | 6 (5/0/1) | 1 istanza in preparazione | 77 % |
| 31 | [PROCEDURA APERTA PER LA FORNITURA DI SERVIZI DI SVILUPPO, EVOLUZIONE E GESTIONE DEI SISTEMI INFORMATIVI A SUPP](/convenzioni/cig-a008db40ba/) | Aggregatore regionale | 86,4 | 112 | 20 | 4 (4/0/0) | 1 istanza in preparazione | 69 % |
| 32 | [ID 2453 - GARA PUBLIC CLOUD SAAS ITSM](/convenzioni/consip-2453/) | Consip | 83,7 | 16 | 4 | 8 (5/2/1) | 1 istanza in preparazione | 15 % |
| 33 | [L'APPALTO HA AD OGGETTO L'ACQUISIZIONE DI SERVIZI DI SVILUPPO, MANUTENZIONE E SUPPORTO PER INAIL E NELLO SPECI](/convenzioni/cig-b2fb115279/) | Altro | 81,8 | 4 | 16 | 14 (5/4/5) | 2 istanze in preparazione | 46 % |
| 34 | [SERVIZIO DI RACCOLTA, GESTIONE ED ELABORAZIONE DI DATI NEL SETTORE DELLA PESCA, DELLACQUACOLTURA E DELLINDUSTR](/convenzioni/cig-88556834cb/) | Altro | 67,4 | 3 | 0 | 12 (5/3/4) | – | 8 % |
| 35 | [ACQUISIZIONE DI PC DESKTOP, WORKSTATION E MONITOR ED. 4 – ID 2781 / FORNITURA IN ACQUISTO DI PERSONAL COMPUTER](/convenzioni/consip-2781/) | Consip | 59,6 | 1786 | 40 | 6 (5/0/1) | 1 istanza in preparazione | 62 % |
| 36 | [SERVIZIO DI GESTIONE DEL SISTEMA TELEMATICO ACQUISTI REGIONALE DELLA TOSCANA (START)](/convenzioni/cig-7930885557/) | Altro | 52,1 | 126 | 0 | 12 (5/3/4) | – | 8 % |
| 37 | [SERVIZI DI POSTA ELETTRONICA CERTIFICATA (PEC) 2 - ID 2556](/convenzioni/consip-2556/) | Consip | 51,5 | 79 | 0 | 8 (5/2/1) | 1 istanza in preparazione | 8 % |
| 38 | [Consip Licenze Microsoft Enterprise Agreement 6, ID 2187](/convenzioni/consip-2187/) | Consip | 49,6 | 54 | 26 | 7 (3/1/3) | 1 istanza in preparazione | 62 % |
| 39 | [PROCEDURA APERTA PER L'ACQUISIZIONE DI SERVIZI DI IT SYSTEM MANAGEMENT E SICUREZZA INFORMATICA 2 / SERVIZI DI ](/convenzioni/cig-97219284c8/) | Aggregatore regionale | 46,5 | 192 | 43 | 4 (4/0/0) | 1 istanza in preparazione | 69 % |
| 40 | [APPALTO SPECIFICO INDETTO DA INNOVAPUGLIA S.P.A. FINALIZZATO ALLA STIPULA DI PIÙ CONVENZIONI PER LA 'ACQUISIZI](/convenzioni/cig-993049146a/) | Aggregatore regionale | 44,7 | 55 | 13 | 9 (4/1/4) | 1 istanza in preparazione | 31 % |
| 41 | [AOV/SUA SF 009/2021 - CONVENZIONE QUADRO ACP PER SERVIZI ICT / LOTTO 2: : SERVIZI INFORMATICI ICT PER APPLICAZ](/convenzioni/cig-8664818204/) | Altro | 40,5 | 98 | 0 | 8 (4/2/2) | 1 istanza in preparazione | 8 % |
| 42 | [SERVIZI INFORMATICI PER L EVOLUZIONE DEI SISTEMI INFORMATIVI DEGLI ENTI NELL AMBITO DI GESTIONE DEI FONDI SIE ](/convenzioni/cig-b1ffb3098a/) | Consorzio o unione | 38,1 | 3 | 0 | 7 (5/1/1) | 1 istanza in preparazione | 8 % |
| 43 | [SERVIZI E PRESTAZIONI INERENTI LA PROGETTAZIONE, SVILUPPO, CONFIGURAZIONE, POPOLAMENTO ED EROGAZIONE IN MODALI](/convenzioni/cig-94252656ba/) | Altro | 37,2 | 33 | 0 | 7 (5/1/1) | 1 istanza in preparazione | 8 % |
| 44 | [ACCORDO QUADRO AVENTE AD OGGETTO LA FORNITURA DI UN 'CATALOGO DI PRODOTTI SAAS NELL'AMBITO DELLA PRODUTTIVITÀ ](/convenzioni/consip-2297/) | Consip | 36,5 | 41 | 59 | 8 (6/0/2) | 1 istanza in preparazione | 62 % |
| 45 | [PRODOTTI CLOUD IN MODALITÀ SOFTWARE AS A SERVICE NELL'AMBITO DEL CRM E MARKETING PER LE PUBBLICHE AMMINISTRAZI](/convenzioni/consip-2700/) | Consip | 32,2 | 25 | 33 | 7 (4/0/3) | 1 istanza in preparazione | 62 % |
| 46 | [SERVIZI DI DATA MANAGEMENT PER LA PUBBLICA AMMINISTRAZIONE 2 ID 2566 / LOTTO 2 SERVIZI DI DATA MANAGEMENT PER ](/convenzioni/consip-2566/) | Consip | 31,8 | 26 | 62 | 10 (7/1/2) | 1 istanza in preparazione | 62 % |
| 47 | [ENERGIA ELETTRICA 21 - ID 2638 / LOMBARDIA ESCLUSE LA PROVINCIA DI MILANO E LA PROVINCIA DI LODI](/convenzioni/consip-2638/) | Consip | 30,1 | 6 | 43 | 5 (4/0/1) | 1 istanza in preparazione | 69 % |
| 48 | [ACCORDO QUADRO PER LA FORNITURA DI UNA PIATTAFORMA PER IL MONITORAGGIO DINAMICO DELLE OPERE D'ARTE E SERVIZI C](/convenzioni/cig-945403654f/) | Altro | 28,0 | 33 | 0 | 12 (5/3/4) | – | 8 % |
| 49 | [ACCORDO QUADRO, SUDDIVISO IN 9 LOTTI, CON PIÙ OPERATORI ECONOMICI, AI SENSI DELL'ART. 59, COMMA 4, LETT. B) DE](/convenzioni/cig-99617296d3/) | Altro | 26,7 | 18 | 0 | 12 (5/3/4) | – | 8 % |
| 50 | [CONVENZIONE PER IL SERVIZIO DI DESKTOP OUTSOURCING](/convenzioni/cig-95643027b0/) | Altro | 26,4 | 9 | 0 | 11 (5/2/4) | – | 8 % |
| 51 | [FORNITURA IN NOLEGGIO DI APPARECCHIATURE MULTIFUNZIONE DI FASCIA MEDIA ED ALTA PER SCANSIONE, COPIA E STAMPA E](/convenzioni/cig-b1457d3391/) | Consip | 25,3 | 409 | 35 | 5 (5/0/0) | 1 istanza in preparazione | 62 % |
| 52 | [GARA A PROCEDURA APERTA PER L'AFFIDAMENTO DELLA FORNITURA DI PRODOTTI SOFTWARE MULTIBRAND, MANUTENZIONE SOFTWA](/convenzioni/consip-2480/) | Consip | 25,0 | 12 | 83 | 6 (4/1/1) | 1 istanza in preparazione | 69 % |
| 53 | [ID 2452 GARA A PROCEDURA APERTA AI SENSI DEL D.LGS. 50/2016 E S.M.I., PER L'AFFIDAMENTO DEI SERVIZI DI TELEFON](/convenzioni/consip-2452/) | Consip | 21,0 | 234 | 45 | 5 (5/0/0) | 1 istanza in preparazione | 62 % |
| 54 | [GARA PER LA FORNITURA DI SERVIZI INTEGRATI, GESTIONALI ED OPERATIVI, DA ESEGUIRSI NEGLI ISTITUTI E LUOGHI DI C](/convenzioni/consip-1561/) | Consip | 21,0 | 4 | 47 | 6 (4/1/1) | 1 istanza in preparazione | 54 % |
| 55 | [PROCEDURA APERTA PER LA CONCLUSIONE DI UNA CONVENZIONE DELLA DURATA DI 72 MESI, PER IL SERVIZIO DI ASSISTENZA ](/convenzioni/cig-84163618ce/) | Aggregatore regionale | 19,6 | 9 | 1 | 7 (5/1/1) | 1 istanza in preparazione | 8 % |
| 56 | [GARA A PROCEDURA APERTA PER L'AFFIDAMENTO DI UN ACCORDO QUADRO IN UN UNICO LOTTO AI SENSI DELL'ART. 54 COMMA 4](/convenzioni/cig-8784303c25/) | Consip | 19,4 | 18 | 22 | 7 (5/1/1) | 1 istanza in preparazione | 62 % |
| 57 | [AQ CENTRALI TELEFONICHE 9 - ID 2496](/convenzioni/consip-2496/) | Consip | 19,3 | 37 | 62 | 10 (5/2/3) | 1 istanza in preparazione | 69 % |
| 58 | [PROCEDURA AOERTA PER LA CONCLUSIONE DI UNA CONVENZIONE DELLA DURATA DI 72 MESI PER IL SERVIZIO DI ASSISTENZA E](/convenzioni/cig-81636687f2/) | Aggregatore regionale | 13,6 | 3 | 10 | 7 (5/1/1) | 1 istanza in preparazione | 8 % |
| 59 | [ACCORDO QUADRO PER L'AFFIDAMENTO, IN FORMA AGGREGATA E AD UN UNICO FORNITORE, DEL SERVIZIO DI SUPPORTO ALLA GE](/convenzioni/cig-9777818ea8/) | Consorzio o unione | 12,6 | 6 | 0 | 12 (5/3/4) | – | 8 % |
| 60 | [GARA TELEMATICA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN ACCORDO QUADRO CON PIÙ OPERATORI ECONOMICI AI SENS](/convenzioni/cig-8637686bf8/) | Aggregatore regionale | 11,5 | 5 | 3 | 10 (5/1/4) | 1 istanza in preparazione | 15 % |
| 61 | [APPALTO SPECIFICO (SDA) PER LA FORNITURA IN ACQUISTO E NOLEGGIO DI PC DESKTOP E NOTEBOOK 11 / LOTTO 2 NOLEGGIO](/convenzioni/cig-9845010742/) | Aggregatore regionale | 11,3 | 985 | 18 | 5 (4/0/1) | 1 istanza in preparazione | 62 % |
| 62 | [PROCEDURA DI AFFIDAMENTO IN HOUSE AI SENSI DELL'ART. 7 DEL D.LGS. 36/2023, PER LA FORNITURA DI SERVIZI PROFESS](/convenzioni/cig-b736423c63/) | Aggregatore regionale | 10,0 | 12 | 0 | 12 (5/3/4) | 1 istanza in preparazione | 8 % |
| 63 | [APPALTO SPECIFICO PER L’ACQUISIZIONE DEL SERVIZIO DI ASSISTENZA TECNICA AL SISTEMA INFORMATIVO LAVORO DELL'EMI](/convenzioni/cig-9936839af1/) | Aggregatore regionale | 9,6 | 8 | 0 | 8 (4/1/3) | 1 istanza in preparazione | 8 % |
| 64 | [GARA EUROPEA A LOTTI PER L'ACQUISIZIONE, MEDIANTE ACCORDO QUADRO, DI SERVIZI INFORMATICI PER L'EVOLUZIONE DI P](/convenzioni/cig-9769148bf3/) | Consorzio o unione | 9,3 | 3 | 0 | 7 (5/0/2) | 1 istanza in preparazione | 8 % |
| 65 | [PROCEDURA NEGOZIATA, EX ART. 63, COMMA 2 - LETT. B) PUNTO 3), D. LGS. N. 50/16 PER LA STIPULA DI CONVENZIONE Q](/convenzioni/cig-87332390d0/) | Aggregatore regionale | 9,0 | 44 | 0 | 12 (5/3/4) | – | 8 % |
| 66 | [PROCEDUTA APERTA TELEMATICA PER L'AFFIDAMENTO DEL SERVIZIO DI GESTIONE INFORMATIZZATA DEL PERSONALE A QUALSIAS](/convenzioni/cig-949554539f/) | Aggregatore regionale | 8,6 | 5 | 0 | 6 (5/1/0) | 1 istanza in preparazione | 8 % |
| 67 | [APPALTO SPECIFICO (SDA) PER L'ACQUISIZIONE DI SERVIZI DI BUSINESS ANALYTICS E DATA MANAGEMENT 2 / SERVIZI DI B](/convenzioni/cig-9923894067/) | Aggregatore regionale | 8,3 | 37 | 0 | 9 (4/1/4) | 1 istanza in preparazione | 8 % |
| 68 | [SERVIZI DI MANUTENZIONE, ASSISTENZA HARDWARE E SOFTWARE DI BASE PER LE INFRASTRUTTURE DELLE AZIENDE SANITARIE ](/convenzioni/cig-7812108376/) | Aggregatore regionale | 7,7 | 12 | 0 | 12 (5/3/4) | – | 8 % |
| 69 | [GARA 7/2017/LI: PROCEDURA RISTRETTA AI SENSI DELL'ART. 61 DEL D.LGS. 50/2006, PER LA SELEZIONE DI OPERATORI PE](/convenzioni/cig-7246653f38/) | Aggregatore regionale | 6,5 | 10 | 0 | 12 (5/3/4) | – | 8 % |
| 70 | [GARA EUROPEA A LOTTI PER L'ACQUISIZIONE, MEDIANTE ACCORDO QUADRO, DI SERVIZI INFORMATICI SU TECNOLOGIE E METOD](/convenzioni/cig-a02b1c8a8a/) | Consorzio o unione | 6,5 | 3 | 0 | 7 (5/1/1) | 1 istanza in preparazione | 8 % |
| 71 | [PA PER LA STIPULA DI UNA CONVENZIONE, DELLA DURATA DI 72 MESI, PER IL 'SERVIZIO DI CONSERVAZIONE A NORMA PER L](/convenzioni/cig-9216207e99/) | Aggregatore regionale | 5,2 | 6 | 0 | 8 (5/2/1) | 1 istanza in preparazione | 8 % |
| 72 | [PROCEDURA NEGOZIATA, EX ART. 63, COMMA 2 - LETT. B) PUNTO 3), D. LGS. N. 50/16 PER LA STIPULA DI CONVENZIONE Q](/convenzioni/cig-8716552642/) | Aggregatore regionale | 4,8 | 42 | 0 | 12 (5/3/4) | – | 8 % |
| 73 | [PROCEDURA APERTA PER L'AFFIDAMENTO DEL SERVIZIO DI LETTURA ED ELABORAZIONI DATI DELLE PRESCRIZIONI FARMACEUTIC](/convenzioni/cig-9837572d38/) | Aggregatore regionale | 4,6 | 3 | 0 | 9 (5/2/2) | 1 istanza in preparazione | 8 % |
| 74 | [PROCEDURA NEGOZIATA SENZA BANDO AI SENSI DELL'ART. 76, C. 2, LETT. B), SUB. 2, D. LGS. 36/2023, PER L'AFFIDAME](/convenzioni/cig-b715929978/) | Aggregatore regionale | 4,3 | 5 | 0 | 12 (5/3/4) | – | 8 % |
| 75 | [PROSECUZIONE SERVIZIO DI CONSERVAZIONE A NORMA PER AZIENDE ED ENTI DEL SERVIZIO SANITARIO REGIONALE DELLA TOSC](/convenzioni/cig-9603457f68/) | Aggregatore regionale | 4,3 | 10 | 0 | 12 (5/3/4) | – | 8 % |
| 76 | [PROCEDURA APERTA PER L’AFFIDAMENTO DEI SERVIZI DI GESTIONE DELLE SANZIONI AMMINISTRATIVE RELATIVE ALLE ATTIVIT](/convenzioni/cig-9580558e8e/) | Aggregatore regionale | 2,9 | 25 | 0 | 8 (4/1/3) | 1 istanza in preparazione | 8 % |
| 77 | [PROCEDURA NEGOZIATA PER L’AFFIDAMENTO DEI SERVIZI DI MANUTENZIONE, ASSISTENZA TECNICA E SERVIZI PROFESSIONALI ](/convenzioni/cig-9482392d69/) | Aggregatore regionale | 2,6 | 29 | 0 | 9 (4/2/3) | 1 istanza in preparazione | 8 % |
| 78 | [P.A. IN DUE LOTTI PER LA STIPULA DI UNA CONVENZIONE PER LA FORNITURA IN LOCAZIONE OPERATIVA DI UN SISTEMA INFO](/convenzioni/cig-759453695c/) | Aggregatore regionale | 2,1 | 8 | 0 | 12 (5/3/4) | – | 8 % |
| 79 | [PROCEDURA APERTA PER LA FORNITURA DI SERVIZI DI TRASMISSIONE DATI E VOCE SU RETI FISSE E MOBILI E GESTIONE E M](/convenzioni/cig-9016294130/) | Aggregatore regionale | 2,0 | 73 | 0 | 9 (4/1/4) | 1 istanza in preparazione | 8 % |
| 80 | [PROCEDURA NEGOZIATA PER L’AFFIDAMENTO DEI SERVIZI DI MANUTENZIONE, ASSISTENZA TECNICA E SERVIZI PROFESSIONALI ](/convenzioni/cig-9481064585/) | Aggregatore regionale | 2,0 | 40 | 0 | 9 (4/2/3) | 1 istanza in preparazione | 8 % |
| 81 | [FORNITURA DI SERVIZI CLOUD IAAS E PAAS / FORNITURA SERVIZI IAAS E PAAS](/convenzioni/consip-2746/) | Consip | 0,0 | 0 | 27 | 9 (6/0/3) | 4 istanze in preparazione | 54 % |
| 82 | [Consip PRINCO, Public cloud SaaS produttività individuale e collaboration (ID 2928)](/convenzioni/consip-2928/) | Consip | 0,0 | 0 | 34 | 6 (5/1/0) | 4 istanze in preparazione | 69 % |

## Iniziative storiche (ancora rilevanti)

Valori: BDNCP, derivati ICT 2024-2025 (mirror ANAC, elaborazione del 05/11/2026); documenti al 05/11/2026.

| # | Iniziativa | Tipo | M€ ICT 2024-25 | Derivati | Documenti presenti | Mancanti (crit. 3/2/1) | Accesso civico | Copertura |
|---|---|---|---|---|---|---|---|---|
| 1 | [GARA STRATEGICA SERVIZI APPLICATIVI IN OTTICA CLOUD E PMO PER LE P.A. - ID 2212 / PAL MACROAREA CENTRO SUD - L](/convenzioni/consip-2212/) | Consip | 11,1 | 11 | 43 | 8 (7/1/0) | 1 istanza in preparazione | 62 % |
| 2 | [Consip AQ System management, ID 1836](/convenzioni/consip-1836/) | Consip | 3,3 | 1 | 18 | 6 (5/0/1) | 1 istanza in preparazione | 54 % |
| 3 | [Consip SPC Cloud lotto 1, servizi di cloud computing (SIGEF 1403)](/convenzioni/consip-1403/) | Consip | 2,1 | 5 | 9 | 12 (6/2/4) | 1 istanza in preparazione | 21 % |
| 4 | [Trenitalia, affidamento di servizi ICT](/convenzioni/cig-7991036b82/) | Altro | 2,1 | 11 | 1 | 11 (5/3/3) | – | 15 % |

Fonte e ripetibilità: `tools/convenzioni/*.py`; numeri ricontrollati da `tools/verifiche/convenzioni_copertura.py`.
