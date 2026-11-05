---
title: "Trasparenza delle convenzioni ICT della PA"
subtitle: "Rendiconto iterativo: cosa si può verificare delle convenzioni e degli accordi quadro ICT, e cosa no"
date: 2026-11-05
description: "Stato della trasparenza delle principali convenzioni e accordi quadro ICT (Consip, PSN, soggetti aggregatori): documenti pubblici, dati assenti, valore non verificabile, rimedi."
---

<!-- Generato da tools/convenzioni/rapporto.py dalla base dati: non modificare a mano. -->

**Versione 0.1 del 2026-11-05** · [registro delle revisioni](#registro-delle-revisioni) · **bozza da presentare a Fabio Pietrosanti prima di ogni diffusione esterna**

Ogni numero viene dalla base dati `report/convenzioni/database/` e si rifà con `python tools/verifiche/convenzioni_rapporto.py`.

## 1. Sintesi

*Cosa non diciamo:* che un dato non individuato sia nascosto di proposito; che un dato reperito presso un ente valga per tutta la convenzione; che le somme BDNCP siano spesa. Molte carenze riguardano dati che oggi nessuna norma obbliga a pubblicare.

- **Perimetro.** 86 iniziative ICT (82 attive): Consip, PSN, soggetti aggregatori regionali, consorzi e altre stazioni appaltanti con più contratti derivati. Criterio nel [README della base dati](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/database/README.md).
- **Valore.** I contratti derivati con CPV ICT pubblicati nel 2024-2025 dichiarano in BDNCP circa **54.798 M€**. È un ordine di grandezza, non la spesa: in molti casi l'importo dichiarato è il massimale o il valore pluriennale (§ 2).
- **Visibilità.** Dei 1120 dati attesi (iniziativa × tipo di documento o dato): pubblici dalla fonte ufficiale 382 (34 %); reperiti solo presso enti aderenti 3 (0,3 %); non individuati sulla pagina del bando 101 (9 %); non ancora verificati 634 (57 %). Indice di visibilità medio **34 %**, da leggere come limite inferiore finché le celle non verificate restano così tante.
- **Dati per controllare spesa e sovranità.** Nessuna iniziativa pubblica insieme offerte dei vincitori, transato per marchio ed elenco degli ordinativi per ente: sono dati che oggi la norma non obbliga la centrale a pubblicare (carenze C1-C4, con la base di ciascuna).
- **Carenze principali** (pagine dei bandi su consip.it consultate il 5/11/2026; acquistinretepa e Amministrazione trasparente di Consip non ancora consultate): offerte tecniche dei vincitori, transato per listino e marchio, elenco degli ordinativi per ente non individuati. Gli ordinativi si trovano in parte negli atti dei singoli enti. Region e data center: per IaaS/PaaS 2 (ID 2746) e PRINCO (ID 2928) i documenti di gara prevedono che il fornitore li dichiari, ma la dichiarazione non è pubblicata.
- **Il dato è presso Consip, con dettaglio ignoto.** In 36 iniziative la documentazione di gara contiene un allegato sui flussi dati del fatturato da trasmettere a Consip per la commissione a carico del fornitore (d.m. MEF 23/11/2012); individuato dal nome del file, da leggere. Il transato dovrebbe quindi esistere presso Consip; non sappiamo con quale dettaglio.
- **Rimedi.** 127 bozze di accesso civico generalizzato preparate e **non inviate**; proposte di policy R08 e R37-R42 perché questi dati diventino pubblici senza bisogno di chiederli.

## 2. Due misure del valore

Per 20 iniziative Consip esiste una seconda misura: gli **open data Consip** degli ordini diretti (dati.consip.it, 2024 e 2025, file archiviati con sha256): **6.349 M€** ordinati. Le stesse iniziative dichiarano in BDNCP **47.410 M€** di derivati ICT 2024-2025. **Le due grandezze non sono confrontabili** una a una: gli open data contano gli ordini diretti dell'anno (non gli appalti specifici degli accordi quadro con rilancio competitivo); BDNCP l'importo dichiarato all'acquisizione del CIG, spesso pluriennale o pari al massimale. La tabella serve a mostrare l'ordine di grandezza e i casi da spiegare (es. ID 2496, dove l'ordinato supera il dichiarato: probabili derivati con CPV non ICT o lotti mancanti, da verificare). Gli abbinamenti «a mano (R)», compreso l'ID 2483, sono da confermare con l'ID Sigef. Gli open data non riportano listino, marchio né ente: la carenza C3 resta.

| Iniziativa | M€ BDNCP 2024-25 | M€ ordinati 2024+2025 (open data Consip) | Abbinamento |
|---|---|---|---|
| [Consip AQ Servizi applicativi in ottica cloud e Demand/PMO P](/convenzioni/consip-2483/) | 29.918 | 2.369 | a mano (R): ID 2483 = seconda edizione d |
| [Consip Servizi applicativi in ottica cloud 3 (PAL), ID 2610](/convenzioni/consip-2610/) | 5.953 | 465 | nome nell'oggetto del CIG padre (V) |
| [Consip Licenze Microsoft Enterprise Agreement 8, ID 2615](/convenzioni/consip-2615/) | 3.015 | 342 | nome nell'oggetto del CIG padre (V) |
| [Consip AQ PC portatili, mobile workstation e Chromebook, ID ](/convenzioni/consip-2425/) | 1.617 | 54 | a mano (R): ID 2425 = AQ PC portatili, m |
| [Consip Digital transformation 2, ID 2536, lotto 2 digitalizz](/convenzioni/consip-2536/) | 970 | 469 | nome nell'oggetto del CIG padre (V) |
| [Consip Licenze software multibrand 6, ID 2599, lotto 1 prodo](/convenzioni/consip-2599/) | 918 | 316 | nome nell'oggetto del CIG padre (V) |
| [Consip AQ Sanità digitale, sistemi informativi gestionali](/convenzioni/consip-2366/) | 834 | 279 | a mano (R): dossier 2366-sanita-digitale |
| [GARA A PROCEDURA APERTA PER L?APPALTO DI FORNITURA MULTIBRAN](/convenzioni/consip-2738/) | 697 | 390 | a mano (R): ID 2738 = gara multibrand 20 |
| [Consip Licenze Microsoft Enterprise Agreement 9, ID 2755 (ip](/convenzioni/consip-2755/) | 692 | 262 | nome nell'oggetto del CIG padre (V) |
| [Consip Sanità digitale, sistemi clinico assistenziali 2, ID ](/convenzioni/consip-2601/) | 558 | 163 | nome nell'oggetto del CIG padre (V) |
| [Consip Reti locali 8, ID 2223, lotto 2 PAL](/convenzioni/consip-reti-locali-8/) | 554 | 298 | nome nell'oggetto del CIG padre (V) |
| [Consip PC desktop e workstation 3, ID 2631, lotto 2](/convenzioni/consip-2631/) | 469 | 74 | nome nell'oggetto del CIG padre (V) |
| [AQ SERVIZI DI GESTIONE E MANUTENZIONE DI SISTEMI IP E POSTAZ](/convenzioni/consip-2648/) | 308 | 291 | nome nell'oggetto del CIG padre (V) |
| [Consip AQ Sanità digitale, sistemi informativi sanitari e se](/convenzioni/consip-2365/) | 297 | 159 | a mano (R): dossier 2365-sanita-digitale |
| [AQ PER I SERVIZI DI GESTIONE E MANUTENZIONE DI SISTEMI IP E ](/convenzioni/consip-2181/) | 232 | 48 | a mano (R): ID 2181 = AQ SGM ed. 1 (ogge |
| [CLOUD ENABLING 1 ID 2652 | LOTTO 1: SERVIZI SUPPORTO ALL'ADO](/convenzioni/consip-2652/) | 190 | 168 | nome nell'oggetto del CIG padre (V) |
| [AQ PER LA FORNITURA DI PRODOTTI CLOUD IAAS E PAAS - ID 2213 ](/convenzioni/consip-2213/) | 90 | 85 | a mano (R): ID 2213 = AQ prodotti cloud  |
| [Consip Licenze Microsoft Enterprise Agreement 6, ID 2187](/convenzioni/consip-2187/) | 50 | 14 | nome nell'oggetto del CIG padre (V) |
| [AQ CENTRALI TELEFONICHE 9 - ID 2496 | AQ CENTRALI TELEFONICH](/convenzioni/consip-2496/) | 19 | 102 | nome nell'oggetto del CIG padre (V) |

## 3. Matrice

La [griglia di tutte le iniziative](/convenzioni/griglia/) mostra cella per cella cosa è pubblico, cosa è reperito altrove, cosa manca e cosa è stato richiesto, con i riepiloghi in alto. L'[indice delle convenzioni](/convenzioni/) riporta il riquadro delle carenze di trasparenza.

| Classe | Celle | Quota |
|---|---|---|
| pubblico (fonte ufficiale) | 382 | 34,1 % |
| solo da fonte non ufficiale | 3 | 0,3 % |
| non individuato sulla pagina del bando | 101 | 9,0 % |
| non ancora verificato | 634 | 56,6 % |

## 4. Convenzione per convenzione

Le iniziative principali (attive, per valore). Indice = dati pubblici / dati attesi (13; 14 per PSN e SPC Cloud, con i progetti dei fabbisogni). «Non individuati» = non trovati sulla pagina del bando, con tipo dedotto dal nome dei file. Il PSN non ha una pagina Consip: le sue celle sono quasi tutte «non verificate», il che non significa assenza di carenze.

| Iniziativa | Soggetto | M€ 2024-25 | Pubblici | Altrove | Non individuati | Non verificati | Indice | Carenze accertate |
|---|---|---|---|---|---|---|---|---|
| [Consip AQ Servizi applicativi in ottica cloud e Demand/PMO PA centrali](/convenzioni/consip-2483/) | Consip | 29.918 | 9 | 0 | 2 | 2 | 69 % | C1, C3, C4 |
| [Consip Servizi applicativi in ottica cloud 3 (PAL), ID 2610](/convenzioni/consip-2610/) | Consip | 5.953 | 9 | 0 | 2 | 2 | 69 % | C1, C3, C4 |
| [Consip Licenze Microsoft Enterprise Agreement 8, ID 2615](/convenzioni/consip-2615/) | Consip | 3.015 | 10 | 1 | 1 | 1 | 77 % | C1, C3, C4 |
| [Polo Strategico Nazionale (PPP, Presidenza del Consiglio)](/convenzioni/psn/) | PSN | 2.078 | 5 | 0 | 0 | 9 | 36 % | – |
| [Consip AQ PC portatili, mobile workstation e Chromebook, ID 2425, lott](/convenzioni/consip-2425/) | Consip | 1.617 | 9 | 0 | 2 | 2 | 69 % | C1, C3, C4 |
| [Consip AQ Servizi di sicurezza da remoto, compliance e controllo, ID 2](/convenzioni/consip-2296/) | Consip | 1.325 | 8 | 0 | 3 | 2 | 62 % | C1, C3, C4 |
| [Consip Digital transformation 2, ID 2536, lotto 2 digitalizzazione dei](/convenzioni/consip-2536/) | Consip | 970 | 9 | 0 | 2 | 2 | 69 % | C1, C3, C4 |
| [Consip Licenze software multibrand 6, ID 2599, lotto 1 prodotti Oracle](/convenzioni/consip-2599/) | Consip | 918 | 10 | 0 | 2 | 1 | 77 % | C1, C3, C4 |
| [Consip AQ Sanità digitale, sistemi informativi gestionali](/convenzioni/consip-2366/) | Consip | 834 | 8 | 0 | 2 | 3 | 62 % | C1, C3, C4 |
| [Consip AQ System management ed. 3, ID 2275, lotto 1](/convenzioni/consip-2275/) | Consip | 747 | 8 | 0 | 3 | 2 | 62 % | C1, C3, C4 |
| [GARA A PROCEDURA APERTA PER L?APPALTO DI FORNITURA MULTIBRAND DI PRODO](/convenzioni/consip-2738/) | Consip | 697 | 10 | 0 | 2 | 1 | 77 % | C1, C3, C4 |
| [Consip Licenze Microsoft Enterprise Agreement 9, ID 2755 (ipotesi fort](/convenzioni/consip-2755/) | Consip | 692 | 10 | 1 | 1 | 1 | 77 % | C1, C3, C4 |
| [Consip Sanità digitale, sistemi clinico assistenziali 2, ID 2601, lott](/convenzioni/consip-2601/) | Consip | 558 | 9 | 0 | 2 | 2 | 69 % | C1, C3, C4 |
| [Consip Reti locali 8, ID 2223, lotto 2 PAL](/convenzioni/consip-reti-locali-8/) | Consip | 554 | 4 | 0 | 2 | 7 | 31 % | C1, C3, C4 |
| [Consip PC desktop e workstation 3, ID 2631, lotto 2](/convenzioni/consip-2631/) | Consip | 469 | 9 | 0 | 2 | 2 | 69 % | C1, C3, C4 |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN ACCORDO QUADRO, AI SE](/convenzioni/cig-91881762b3/) | Consip | 354 | 1 | 0 | 0 | 12 | 8 % | C8 |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN ACCORDO QUADRO, AI SE](/convenzioni/cig-8765571a03/) | Consip | 325 | 7 | 0 | 3 | 3 | 54 % | C1, C3, C4 |
| [AQ SERVIZI DI GESTIONE E MANUTENZIONE DI SISTEMI IP E POSTAZIONE DI LA](/convenzioni/consip-2648/) | Consip | 308 | 9 | 0 | 2 | 2 | 69 % | C1, C3, C4 |
| [Consip AQ Sanità digitale, sistemi informativi sanitari e servizi al c](/convenzioni/consip-2365/) | Consip | 297 | 9 | 0 | 2 | 2 | 69 % | C1, C3, C4 |
| [Consip SPC2 Connettività (contratto quadro OPA)](/convenzioni/cig-5133642f61/) | Consip | 258 | 2 | 0 | 0 | 11 | 15 % | C8 |
| [AQ PER I SERVIZI DI GESTIONE E MANUTENZIONE DI SISTEMI IP E POSTAZIONI](/convenzioni/consip-2181/) | Consip | 232 | 9 | 0 | 2 | 2 | 69 % | C1, C3, C4 |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN ACCORDO QUADRO, AI SE](/convenzioni/cig-9030521daa/) | Consip | 227 | 7 | 0 | 3 | 3 | 54 % | C1, C3, C4 |
| [GARA A PROCEDURA APERTA PER L'AFFIDAMENTO DI UN ACCORDO QUADRO AI SENS](/convenzioni/cig-8898059e90/) | Consip | 225 | 1 | 0 | 0 | 12 | 8 % | C8 |
| [CLOUD ENABLING 1 ID 2652 | LOTTO 1: SERVIZI SUPPORTO ALL'ADOZIONE E PM](/convenzioni/consip-2652/) | Consip | 190 | 9 | 0 | 2 | 2 | 69 % | C1, C3, C4 |
| [ARIA_2023_807 - PROCEDURA APERTA, AI SENSI DELL’ART. 60 DEL D.LGS. N. ](/convenzioni/cig-989984280e/) | Aggregatori regionali | 160 | 1 | 0 | 0 | 12 | 8 % | – |
| [GARA A PROCEDURA APERTA SUDDIVISA IN 4 LOTTI PER L'AFFIDAMENTO DEI SER](/convenzioni/consip-1774/) | Altri | 147 | 4 | 0 | 3 | 6 | 31 % | C1, C4 |
| [Consip AQ System management ed. 4, ID 2710 (lotto unico)](/convenzioni/consip-2710/) | Consip | 145 | 8 | 0 | 3 | 2 | 62 % | C1, C3, C4 |
| [GARA A PROCEDURA APERTA, SUDDIVISA IN 8 LOTTI, PER LA STIPULA DI UNA C](/convenzioni/cig-b0da5c472c/) | Consip | 114 | 1 | 0 | 0 | 12 | 8 % | C8 |
| [PROCEDURA NEGOZIATA PER L'AFFIDAMENTO DI SERVIZI IN OUTSOURCING DI CUS](/convenzioni/cig-a0260b3155/) | Altri | 100 | 1 | 0 | 0 | 12 | 8 % | – |
| [AQ PER LA FORNITURA DI PRODOTTI CLOUD IAAS E PAAS - ID 2213 | LOTTO 8 ](/convenzioni/consip-2213/) | Consip | 90 | 9 | 0 | 2 | 2 | 69 % | C1, C3, C4 |

Le altre 56 iniziative sono nell'[indice](/convenzioni/) e nella [griglia](/convenzioni/griglia/).

## 5. Per tipo di soggetto

| Soggetto | Iniziative | M€ 2024-25 | Indice medio | Non individuati | Non verificati |
|---|---|---|---|---|---|
| Consip | 45 | 51.555 | 56 % | 95 | 160 |
| PSN | 1 | 2.078 | n.d. (non ancora verificati) | 0 | 9 |
| Aggregatori regionali | 25 | 488 | n.d. (non ancora verificati) | 0 | 300 |
| Consorzi e unioni | 4 | 67 | n.d. (non ancora verificati) | 0 | 48 |
| Altri | 11 | 610 | n.d. (non ancora verificati) | 6 | 117 |

Per aggregatori regionali e consorzi quasi tutti i dati sono «da verificare»: le loro piattaforme (Sintel, Intercent-ER, EmPULIA, START…) non sono ancora state visitate, i CIG padre non hanno link ai documenti in PVL (verificato: nessuno dei 295 CIG padre) e su TED l'abbinamento riesce solo per testo. **Un indice basso qui misura il nostro lavoro ancora da fare, non la loro trasparenza.**

## 6. Metodo e limiti

- **Fonti.** BDNCP ANAC (nostro mirror, sha256 nel manifest) per i CIG padre e derivati; pagine dei bandi su consip.it, consultate il 5/11/2026; TED; open data Consip degli ordini (dati.consip.it, file 2024-2025 archiviati il 5/11/2026); atti di enti aderenti trovati con ricerca online (fonte non ufficiale, archiviati con sha256).
- **Verificato e riferito.** «Assente» vuol dire che abbiamo consultato la pagina ufficiale dell'iniziativa e il documento non c'è; il tipo di documento si deduce dal nome del file (controllo a mano solo per PRINCO). Le norme e i dati che non abbiamo letto sulla fonte sono marcati [R] nelle schede ([carenze.yaml](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/database/carenze.yaml)).
- **Valori.** Somme di importi dichiarati in BDNCP: ordine di grandezza, non spesa né transato (seconda misura al § 2). La prima iniziativa per valore pesa 29.918 M€ (55 % del totale).
- **Archivio.** 1806 documenti ufficiali collegati alle iniziative (compresi i file dentro gli zip), archiviati con sha256; una cella «pubblico» può contenerne molti.
- **PVL.** Nessuno dei 295 CIG padre ha un link ai documenti di gara nei dati PVL scaricati il 3-4/11/2026 (verificato): è lo stato dei dati PVL, non un'assenza dei documenti, che gli aggregatori pubblicano sulle proprie piattaforme.
- **Rumore nel censimento.** Il filtro per CPV ICT sui derivati lascia passare iniziative non ICT (es. ID 2638 Energia elettrica 21, 30 M€): restano in elenco finché il filtro non viene corretto, con peso trascurabile sul totale.
- **Lettura dei documenti.** Letti per intero solo gli atti di PRINCO (ID 2928) e alcune determine di enti; per le altre iniziative le schede mostrano estratti automatici per parole chiave, marcati «da leggere».
- **Aggregatori.** Ancora da verificare (sopra). Il tipo di soggetto si assegna con regole sul nome della stazione appaltante, da controvalidare con l'elenco ANAC dei soggetti aggregatori.
- **Cosa non diciamo.** Che un dato assente sia nascosto di proposito; che un dato reperito presso un ente valga per tutta la convenzione.

## 7. Rimedi

- **Accesso civico generalizzato** (art. 5 c. 2 d.lgs. 33/2013), come rimedio di breve periodo: 127 bozze preparate, 0 inviate. [Registro](/convenzioni/accesso-civico/) e [analisi dei dinieghi](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/accesso-civico/analisi-dinieghi.md).
- **Proposte di policy** (stato «proposta», nessuna inviata):
  - C1 Offerte tecniche dei vincitori → R39
  - C2 Listini e prezzi offerti dagli aggiudicatari → R39
  - C3 Transato per listino, marchio ed ente → R37
  - C4 Ordinativi e contratti attuativi → R08
  - C5 Progetti e piani dei fabbisogni → R41
  - C6 Region e data center dichiarati → R42
  - C7 Monitoraggio delle soglie di erosione dei massimali → R37
  - C8 Indice ID Sigef ↔ CIG dei lotti → R38

## Registro delle revisioni

| Versione | Data | Nota | Cosa è cambiato |
|---|---|---|---|
| 0.1 | 2026-11-05 | prima versione (bozza dopo revisione avversariale): 86 iniziative, documenti Consip archiviati, open data Consip degli ordini | prima versione |
