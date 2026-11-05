---
title: "Trasparenza delle convenzioni ICT della PA"
subtitle: "Rendiconto iterativo: cosa si può verificare delle convenzioni e degli accordi quadro ICT, e cosa no"
date: 2026-11-05
lastmod: 2026-11-06
datiAl: 2026-11-05
description: "Stato della trasparenza delle principali convenzioni e accordi quadro ICT (Consip, PSN, soggetti aggregatori): documenti pubblici, dati assenti, valore non verificabile, rimedi."
---

<!-- Generato da tools/convenzioni/rapporto.py dalla base dati: non modificare a mano. -->

**Versione 0.3 del 2026-11-06** · [registro delle revisioni](#registro-delle-revisioni) · **bozza da presentare a Fabio Pietrosanti prima di ogni diffusione esterna**

Ogni numero viene dalla base dati `report/convenzioni/database/` e si rifà con `python tools/verifiche/convenzioni_rapporto.py`.

## 1. Sintesi

*Cosa non diciamo:* che un dato non individuato sia nascosto di proposito; che un dato reperito presso un ente valga per tutta la convenzione; che le somme BDNCP siano spesa. Molte carenze riguardano dati che oggi nessuna norma obbliga a pubblicare.

- **Perimetro.** 86 iniziative ICT (82 attive): Consip, PSN, soggetti aggregatori regionali, consorzi e altre stazioni appaltanti con più contratti derivati. Criterio nel [README della base dati](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/database/README.md).
- **Valore.** I contratti derivati con CPV ICT pubblicati nel 2024-2025 dichiarano in BDNCP circa **54.798 M€**. È un ordine di grandezza, non la spesa: in molti casi l'importo dichiarato è il massimale o il valore pluriennale (§ 2).
- **Visibilità.** Dei 1.120 dati attesi (iniziativa × tipo di documento o dato): pubblici dalla fonte ufficiale 385 (34 %); reperiti solo presso enti aderenti 11 (1,0 %); non individuati sulla pagina del bando 93 (8 %); non ancora verificati 631 (56 %). Indice di visibilità medio **34 %**, da leggere come limite inferiore finché le celle non verificate restano così tante.
- **Dati per controllare spesa e sovranità.** Nelle iniziative verificate non abbiamo individuato, pubblicati insieme, offerte dei vincitori, transato per marchio ed elenco degli ordinativi per ente: sono dati che oggi la norma non obbliga la centrale a pubblicare (carenze C1-C4, con la base di ciascuna).
- **Carenze principali** (pagine dei bandi su consip.it, open data Consip, Amministrazione trasparente di Consip e campione di enti, consultati il 5/11/2026; acquistinretepa solo in parte): offerte tecniche dei vincitori, transato per listino e marchio, elenco degli ordinativi per ente non individuati. Gli ordinativi si trovano in parte negli atti dei singoli enti. Region e data center: per IaaS/PaaS 2 (ID 2746) e PRINCO (ID 2928) i documenti di gara prevedono che il fornitore li dichiari, ma la dichiarazione non è pubblicata.
- **Il dato dovrebbe essere presso Consip.** Secondo l'allegato 4E della convenzione Microsoft EA8 (ID 2615, letto per intero), il fornitore deve trasmettere ogni mese a Consip il dettaglio delle fatture, con l'ID dell'ordine sulla piattaforma e l'imponibile, per il calcolo della commissione (d.m. MEF 23/11/2012). Se il flusso è rispettato, Consip dispone dei dati per ricostruire il transato per ordine e quindi per ente; non abbiamo verificato che il flusso avvenga né in che forma sia conservato. Gli altri 35 allegati, analizzati per parole chiave (R), seguono in gran parte lo stesso schema; fa eccezione quello di System Management 3 (ID 2275), sui flussi di monitoraggio, dove compaiono campi per ente e prodotto.
- **Rimedi.** Dopo le fonti online del § 3 (acquistinretepa ancora parziale), 19 bozze di accesso civico generalizzato, tutte verso Consip, restano utili all'analisi; 114 sono ritirate, con il motivo di ciascuna nel registro; **nessuna inviata**; proposte di policy R08 e R37-R44 perché questi dati diventino pubblici senza bisogno di chiederli.

## 2. Due misure del valore

Per 20 iniziative Consip esiste una seconda misura: gli **open data Consip** degli ordini diretti (dati.consip.it, 2024 e 2025, file archiviati con sha256): **6.349 M€** ordinati. Le stesse iniziative dichiarano in BDNCP **47.410 M€** di derivati ICT 2024-2025. **Le due grandezze non sono confrontabili** una a una: gli open data contano gli ordini diretti dell'anno (non gli appalti specifici degli accordi quadro con rilancio competitivo); BDNCP l'importo dichiarato all'acquisizione del CIG, spesso pluriennale o pari al massimale. La tabella serve a mostrare l'ordine di grandezza e i casi da spiegare (es. ID 2496, dove l'ordinato supera il dichiarato: cause possibili derivati con CPV non ICT, lotti non censiti o abbinamento da rivedere). Gli abbinamenti sono per coincidenza del nome («V-testo»): confermati con il titolo della pagina Consip trovata per ID Sigef, o per il 2.483 con atti di enti che riportano ID e CIG; nessun open data riporta l'ID Sigef. Gli open data non riportano listino, marchio né ente: la carenza C3 resta.

Open data Consip scaricati il 05/11/2026; BDNCP elaborato il 05/11/2026.

| Iniziativa | M€ BDNCP 2024-25 | M€ ordinati 2024+2025 (open data Consip) | Abbinamento |
|---|---|---|---|
| [Consip AQ Servizi applicativi in ottica cloud e Demand/PMO P](/convenzioni/consip-2483/) | 29.918 | 2.369 | a mano (V-testo): ID 2483 = «Servizi app |
| [Consip Servizi applicativi in ottica cloud 3 (PAL), ID 2610](/convenzioni/consip-2610/) | 5.953 | 465 | nome nell'oggetto del CIG padre (V-testo |
| [Consip Licenze Microsoft Enterprise Agreement 8, ID 2615](/convenzioni/consip-2615/) | 3.015 | 342 | nome nell'oggetto del CIG padre (V-testo |
| [Consip AQ PC portatili, mobile workstation e Chromebook, ID ](/convenzioni/consip-2425/) | 1.617 | 54 | a mano (V-testo): pagina consip.it trova |
| [Consip Digital transformation 2, ID 2536, lotto 2 digitalizz](/convenzioni/consip-2536/) | 970 | 469 | nome nell'oggetto del CIG padre (V-testo |
| [Consip Licenze software multibrand 6, ID 2599, lotto 1 prodo](/convenzioni/consip-2599/) | 918 | 316 | nome nell'oggetto del CIG padre (V-testo |
| [Consip AQ Sanità digitale, sistemi informativi gestionali](/convenzioni/consip-2366/) | 834 | 279 | a mano (V-testo): pagina consip.it trova |
| [GARA A PROCEDURA APERTA PER L’APPALTO DI FORNITURA MULTIBRAN](/convenzioni/consip-2738/) | 697 | 390 | a mano (V-testo): pagina consip.it trova |
| [Consip Licenze Microsoft Enterprise Agreement 9, ID 2755 (ip](/convenzioni/consip-2755/) | 692 | 262 | nome nell'oggetto del CIG padre (V-testo |
| [Consip Sanità digitale, sistemi clinico assistenziali 2, ID ](/convenzioni/consip-2601/) | 558 | 163 | nome nell'oggetto del CIG padre (V-testo |
| [Consip Reti locali 8, ID 2223, lotto 2 PAL](/convenzioni/consip-reti-locali-8/) | 554 | 298 | nome nell'oggetto del CIG padre (V-testo |
| [Consip PC desktop e workstation 3, ID 2631, lotto 2](/convenzioni/consip-2631/) | 469 | 74 | nome nell'oggetto del CIG padre (V-testo |
| [AQ SERVIZI DI GESTIONE E MANUTENZIONE DI SISTEMI IP E POSTAZ](/convenzioni/consip-2648/) | 308 | 291 | nome nell'oggetto del CIG padre (V-testo |
| [Consip AQ Sanità digitale, sistemi informativi sanitari e se](/convenzioni/consip-2365/) | 297 | 159 | a mano (V-testo): pagina consip.it trova |
| [AQ PER I SERVIZI DI GESTIONE E MANUTENZIONE DI SISTEMI IP E ](/convenzioni/consip-2181/) | 232 | 48 | a mano (V-testo): pagina consip.it trova |
| [CLOUD ENABLING 1 ID 2652 | LOTTO 1: SERVIZI SUPPORTO ALL'ADO](/convenzioni/consip-2652/) | 190 | 168 | nome nell'oggetto del CIG padre (V-testo |
| [AQ PER LA FORNITURA DI PRODOTTI CLOUD IAAS E PAAS - ID 2213 ](/convenzioni/consip-2213/) | 90 | 85 | a mano (V-testo): pagina consip.it trova |
| [Consip Licenze Microsoft Enterprise Agreement 6, ID 2187](/convenzioni/consip-2187/) | 50 | 14 | nome nell'oggetto del CIG padre (V-testo |
| [AQ CENTRALI TELEFONICHE 9 - ID 2496](/convenzioni/consip-2496/) | 19 | 102 | nome nell'oggetto del CIG padre (V-testo |

### Consumato per convenzione, fonte per fonte

Consultazioni del 05/11/2026. [V] = dato letto da noi sulla fonte archiviata; [R] = riferito. Nessuna fonte pubblica dà il consumato per listino, marchio o ente.

Legenda: «–» = iniziativa non abbinata negli open data; «0» = abbinata con importo nullo; «<0,1» = importo positivo sotto 0,05 M€. Ordinato 2026: file open data Consip scaricato il 05/11/2026 (copertura dell'anno non dichiarata dal file). Separatore delle migliaia: punto; decimali: virgola.

| Iniziativa | BDNCP derivati ICT 2024-25 (M€) [V] | Ordinato 2024 (M€) [V] | Ordinato 2025 (M€) [V] | Ordinato 2026, file del 05/11/2026 (M€) [V] | Massimale residuo su acquistinretepa | Corte dei conti [R] |
|---|---|---|---|---|---|---|
| [Consip AQ Servizi applicativi in ottica cloud e Demand/PMO P](/convenzioni/consip-2483/) | 29.918 | 839,8 | 1.529,5 | 491,8 | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [Consip Servizi applicativi in ottica cloud 3 (PAL), ID 2610](/convenzioni/consip-2610/) | 5.953 | 0 | 465,1 | 375,5 | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [Consip Licenze Microsoft Enterprise Agreement 8, ID 2615](/convenzioni/consip-2615/) | 3.015 | 317,2 | 25,2 | 11,4 | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [Consip AQ PC portatili, mobile workstation e Chromebook, ID ](/convenzioni/consip-2425/) | 1.617 | 42,4 | 11,5 | 0 | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [Consip Digital transformation 2, ID 2536, lotto 2 digitalizz](/convenzioni/consip-2536/) | 970 | 404,1 | 64,9 | 34,6 | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [Consip Licenze software multibrand 6, ID 2599, lotto 1 prodo](/convenzioni/consip-2599/) | 918 | 311,4 | 4,2 | 0 | scheda non individuata da noi | solo aggregato degli AQ |
| [Consip AQ Sanità digitale, sistemi informativi gestionali](/convenzioni/consip-2366/) | 834 | 134,0 | 145,4 | 96,7 | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [GARA A PROCEDURA APERTA PER L’APPALTO DI FORNITURA MULTIBRAN](/convenzioni/consip-2738/) | 697 | 0 | 389,8 | 77,6 | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [Consip Licenze Microsoft Enterprise Agreement 9, ID 2755 (ip](/convenzioni/consip-2755/) | 692 | 0 | 261,5 | 84,1 | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [Consip Sanità digitale, sistemi clinico assistenziali 2, ID ](/convenzioni/consip-2601/) | 558 | 50,7 | 112,3 | 55,7 | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [Consip Reti locali 8, ID 2223, lotto 2 PAL](/convenzioni/consip-reti-locali-8/) | 554 | 234,5 | 63,7 | 0 | scheda non individuata da noi | solo aggregato degli AQ |
| [Consip PC desktop e workstation 3, ID 2631, lotto 2](/convenzioni/consip-2631/) | 469 | 64,0 | 10,4 | 0,1 | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [AQ SERVIZI DI GESTIONE E MANUTENZIONE DI SISTEMI IP E POSTAZ](/convenzioni/consip-2648/) | 308 | 0 | 290,8 | 462,3 | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [Consip AQ Sanità digitale, sistemi informativi sanitari e se](/convenzioni/consip-2365/) | 297 | 124,1 | 35,2 | 0 | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [AQ PER I SERVIZI DI GESTIONE E MANUTENZIONE DI SISTEMI IP E ](/convenzioni/consip-2181/) | 232 | 47,5 | 0,1 | 0 | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [CLOUD ENABLING 1 ID 2652 | LOTTO 1: SERVIZI SUPPORTO ALL'ADO](/convenzioni/consip-2652/) | 190 | 59,3 | 108,9 | 77,1 | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [Consip AQ System management ed. 4, ID 2710 (lotto unico)](/convenzioni/consip-2710/) | 145 | – | – | – | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [AQ PER LA FORNITURA DI PRODOTTI CLOUD IAAS E PAAS - ID 2213 ](/convenzioni/consip-2213/) | 90 | 85,5 | 0 | 0 | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [ID 2453 - GARA PUBLIC CLOUD SAAS ITSM](/convenzioni/consip-2453/) | 84 | – | – | – | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [ACQUISIZIONE DI PC DESKTOP, WORKSTATION E MONITOR ED. 4 – ID](/convenzioni/consip-2781/) | 60 | – | – | – | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [Consip Licenze Microsoft Enterprise Agreement 6, ID 2187](/convenzioni/consip-2187/) | 50 | 14,0 | 0,3 | 0 | scheda non individuata da noi | solo aggregato degli AQ |
| [PRODOTTI CLOUD IN MODALITÀ SOFTWARE AS A SERVICE NELL'AMBITO](/convenzioni/consip-2700/) | 32 | – | – | – | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [SERVIZI DI DATA MANAGEMENT PER LA PUBBLICA AMMINISTRAZIONE 2](/convenzioni/consip-2566/) | 32 | – | – | – | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [ID 2452 GARA A PROCEDURA APERTA AI SENSI DEL D.LGS. 50/2016 ](/convenzioni/consip-2452/) | 21 | – | – | – | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [GARA PER LA FORNITURA DI SERVIZI INTEGRATI, GESTIONALI ED OP](/convenzioni/consip-1561/) | 21 | – | – | – | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [AQ CENTRALI TELEFONICHE 9 - ID 2496](/convenzioni/consip-2496/) | 19 | 18,7 | 83,3 | 43,1 | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [FORNITURA DI SERVIZI CLOUD IAAS E PAAS | FORNITURA SERVIZI I](/convenzioni/consip-2746/) | 0 | – | – | – | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |
| [Consip PRINCO, Public cloud SaaS produttività individuale e ](/convenzioni/consip-2928/) | 0 | – | – | – | sezione presente ma vuota alla consultazione («Nessun risultato») | solo aggregato degli AQ |

**Perché le fonti non coincidono.** BDNCP registra l'importo dichiarato quando l'ente acquisisce il CIG derivato (spesso pluriennale o pari al massimale) e solo per i derivati con CPV ICT; gli open data Consip contano gli ordini diretti dell'anno (non gli appalti specifici con rilancio competitivo) per convenzione o AQ; la Corte dei conti riporta l'erogato complessivo degli accordi quadro, non per iniziativa. Per alcune iniziative (es. ID 2648 e 2.496) l'ordinato supera il dichiarato BDNCP (derivati senza CPV ICT o CIG fuori dal 2024-25): le due misure non vanno sommate né sottratte. Il massimale residuo, che darebbe l'erosione per lotto, ha una sezione nella scheda pubblica di acquistinretepa che il 05/11/2026 risultava vuota («Nessun risultato»); alcune parti della pagina mostravano date segnaposto, quindi la resa potrebbe essere stata incompleta: non abbiamo verificato se il dato compaia dopo l'accesso. È nell'[elenco dei blocchi](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/blocchi-accesso.csv) da provare a mano.


## 3. Fonti online consultate prima dell'accesso civico

Tutte consultate il 05/11/2026, senza login né CAPTCHA, a ritmo basso e con User-Agent dichiarato.

| Fonte | Esito | Livello |
|---|---|---|
| Pagine dei bandi su consip.it | documentazione di gara di 44 iniziative; offerte, transato per marchio ed elenco degli ordinativi non individuati | V per la presenza dei file; R per il tipo dedotto dal nome |
| Open data Consip (dati.consip.it) | ordinato per anno, convenzione o AQ e lotto (2024-2025); niente ente, listino, marchio | V |
| acquistinretepa (browser reale, Chrome headless) | vetrina: 663 iniziative (servizio getIniziative, attive e archivio); schede pubbliche trovate per 26 iniziative del censimento, con 259 documenti linkati; sezione «Massimale residuo» vuota alla consultazione (resa forse incompleta: date segnaposto); catalogo e acquisto dietro «Accedi»; chiamate JSON registrate con sha256 | V per ciò che è stato visto; da riverificare il residuo |
| Amministrazione trasparente di Consip | le sottosezioni di «Bandi di gara e contratti» riguardano gli acquisti di Consip per sé; «Controlli e rilievi» rinvia alla Corte dei conti | V (indice delle sezioni) |
| Campione di enti aderenti | 45 righe valide (righe di controllo escluse), 28 enti, 10 iniziative: file nel percorso AT 6, URL esterno al percorso AT 27 (collegamento dalla sezione AT non verificato), non trovato 7, AT non verificabile automaticamente il 5/11 5 (da ripetere); 31 archiviati | V per i documenti letti; R per la posizione rispetto all'AT |
| Ricerca web (Corte dei conti, stampa, atti di enti) | 15 dati da 13 URL, 9 archiviati; erogato per iniziativa non trovato (nelle due relazioni della Corte dei conti consultate, gestioni 2021 e 2022, l'erogato degli AQ è aggregato) | R |
| Allegati «flussi dati del fatturato» | 36 allegati acquisiti e analizzati per parole chiave, letto per intero quello di EA8: invio mensile a Consip del dettaglio delle fatture (numero, data, ID dell'ordine, imponibile); in 35 non compaiono campi per ente, prodotto o marchio; in quello di System Management 3 (ID 2275, flussi di monitoraggio) compaiono campi per ente e prodotto (da leggere) | V per EA8; R per gli altri |

Il dettaglio per iniziativa e per ente è nelle [schede](/convenzioni/) e nei file [enti-campione](https://github.com/mxmap-it/analisi-spesa-ict/tree/main/report/convenzioni/enti-campione) e [fonti-non-ufficiali](https://github.com/mxmap-it/analisi-spesa-ict/tree/main/report/convenzioni/fonti-non-ufficiali), in un formato riusabile dal monitor dell'Amministrazione trasparente.


## 4. Matrice

La [griglia di tutte le iniziative](/convenzioni/griglia/) mostra cella per cella cosa è pubblico, cosa è reperito altrove, cosa manca e cosa è stato richiesto, con i riepiloghi in alto. L'[indice delle convenzioni](/convenzioni/) riporta il riquadro delle carenze di trasparenza.

Celle al 05/11/2026 (documenti) e BDNCP elaborato il 05/11/2026.

| Classe | Celle | Quota |
|---|---|---|
| pubblico (fonte ufficiale) | 385 | 34,4 % |
| solo da fonte non ufficiale | 11 | 1,0 % |
| non individuato sulla pagina del bando | 93 | 8,3 % |
| non ancora verificato | 631 | 56,3 % |

## 5. Convenzione per convenzione

Le iniziative principali (attive, per valore). Indice = dati pubblici / dati attesi (13; 14 per PSN e SPC Cloud, con i progetti dei fabbisogni). «Non individuati» = non trovati sulla pagina del bando, con tipo dedotto dal nome dei file. Il PSN non ha una pagina Consip: le sue celle sono quasi tutte «non verificate», il che non significa assenza di carenze.

Fonti consultate il 05/11/2026; valori BDNCP elaborati il 05/11/2026.

| Iniziativa | Soggetto | M€ 2024-25 | Pubblici | Altrove | Non individuati | Non verificati | Indice | Carenze accertate |
|---|---|---|---|---|---|---|---|---|
| [Consip AQ Servizi applicativi in ottica cloud e Demand/PMO PA centrali](/convenzioni/consip-2483/) | Consip | 29.918 | 9 | 1 | 1 | 2 | 69 % | C1, C3, C4, C7 |
| [Consip Servizi applicativi in ottica cloud 3 (PAL), ID 2610](/convenzioni/consip-2610/) | Consip | 5.953 | 9 | 1 | 1 | 2 | 69 % | C1, C3, C4, C7 |
| [Consip Licenze Microsoft Enterprise Agreement 8, ID 2615](/convenzioni/consip-2615/) | Consip | 3.015 | 10 | 1 | 1 | 1 | 77 % | C1, C3, C4, C7 |
| [Polo Strategico Nazionale (PPP, Presidenza del Consiglio)](/convenzioni/psn/) | PSN | 2.078 | 5 | 0 | 0 | 9 | 36 % | – |
| [Consip AQ PC portatili, mobile workstation e Chromebook, ID 2425, lott](/convenzioni/consip-2425/) | Consip | 1.617 | 9 | 1 | 1 | 2 | 69 % | C1, C3, C4, C7 |
| [Consip AQ Servizi di sicurezza da remoto, compliance e controllo, ID 2](/convenzioni/consip-2296/) | Consip | 1.325 | 8 | 1 | 2 | 2 | 62 % | C1, C3, C4 |
| [Consip Digital transformation 2, ID 2536, lotto 2 digitalizzazione dei](/convenzioni/consip-2536/) | Consip | 970 | 9 | 1 | 1 | 2 | 69 % | C1, C3, C4, C7 |
| [Consip Licenze software multibrand 6, ID 2599, lotto 1 prodotti Oracle](/convenzioni/consip-2599/) | Consip | 918 | 10 | 1 | 1 | 1 | 77 % | C1, C3, C4 |
| [Consip AQ Sanità digitale, sistemi informativi gestionali](/convenzioni/consip-2366/) | Consip | 834 | 8 | 1 | 1 | 3 | 62 % | C1, C3, C4, C7 |
| [Consip AQ System management ed. 3, ID 2275, lotto 1](/convenzioni/consip-2275/) | Consip | 747 | 8 | 1 | 2 | 2 | 62 % | C1, C3, C4 |
| [GARA A PROCEDURA APERTA PER L’APPALTO DI FORNITURA MULTIBRAND DI PRODO](/convenzioni/consip-2738/) | Consip | 697 | 10 | 0 | 2 | 1 | 77 % | C1, C3, C4, C7 |
| [Consip Licenze Microsoft Enterprise Agreement 9, ID 2755 (ipotesi fort](/convenzioni/consip-2755/) | Consip | 692 | 10 | 1 | 1 | 1 | 77 % | C1, C3, C4, C7 |
| [Consip Sanità digitale, sistemi clinico assistenziali 2, ID 2601, lott](/convenzioni/consip-2601/) | Consip | 558 | 9 | 0 | 2 | 2 | 69 % | C1, C3, C4, C7 |
| [Consip Reti locali 8, ID 2223, lotto 2 PAL](/convenzioni/consip-reti-locali-8/) | Consip | 554 | 4 | 0 | 2 | 7 | 31 % | C1, C3, C4 |
| [Consip PC desktop e workstation 3, ID 2631, lotto 2](/convenzioni/consip-2631/) | Consip | 469 | 9 | 0 | 2 | 2 | 69 % | C1, C3, C4, C7 |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN ACCORDO QUADRO, AI SE](/convenzioni/cig-91881762b3/) | Consip | 354 | 1 | 0 | 0 | 12 | 8 % | C8 |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN ACCORDO QUADRO, AI SE](/convenzioni/cig-8765571a03/) | Consip | 325 | 7 | 0 | 3 | 3 | 54 % | C1, C3, C4 |
| [AQ SERVIZI DI GESTIONE E MANUTENZIONE DI SISTEMI IP E POSTAZIONE DI LA](/convenzioni/consip-2648/) | Consip | 308 | 9 | 0 | 2 | 2 | 69 % | C1, C3, C4, C7 |
| [Consip AQ Sanità digitale, sistemi informativi sanitari e servizi al c](/convenzioni/consip-2365/) | Consip | 297 | 9 | 0 | 2 | 2 | 69 % | C1, C3, C4, C7 |
| [Consip SPC2 Connettività (contratto quadro OPA)](/convenzioni/cig-5133642f61/) | Consip | 258 | 2 | 0 | 0 | 11 | 15 % | C8 |
| [AQ PER I SERVIZI DI GESTIONE E MANUTENZIONE DI SISTEMI IP E POSTAZIONI](/convenzioni/consip-2181/) | Consip | 232 | 10 | 0 | 2 | 1 | 77 % | C1, C3, C4, C7 |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN ACCORDO QUADRO, AI SE](/convenzioni/cig-9030521daa/) | Consip | 227 | 7 | 0 | 3 | 3 | 54 % | C1, C3, C4 |
| [GARA A PROCEDURA APERTA PER L'AFFIDAMENTO DI UN ACCORDO QUADRO AI SENS](/convenzioni/cig-8898059e90/) | Consip | 225 | 1 | 0 | 0 | 12 | 8 % | C8 |
| [CLOUD ENABLING 1 ID 2652 | LOTTO 1: SERVIZI SUPPORTO ALL'ADOZIONE E PM](/convenzioni/consip-2652/) | Consip | 190 | 9 | 0 | 2 | 2 | 69 % | C1, C3, C4, C7 |
| [ARIA_2023_807 - PROCEDURA APERTA, AI SENSI DELL’ART. 60 DEL D.LGS. N. ](/convenzioni/cig-989984280e/) | Aggregatori regionali | 160 | 1 | 0 | 0 | 12 | 8 % | – |
| [GARA A PROCEDURA APERTA SUDDIVISA IN 4 LOTTI PER L'AFFIDAMENTO DEI SER](/convenzioni/consip-1774/) | Altri | 147 | 4 | 0 | 3 | 6 | 31 % | C1, C4 |
| [Consip AQ System management ed. 4, ID 2710 (lotto unico)](/convenzioni/consip-2710/) | Consip | 145 | 8 | 0 | 3 | 2 | 62 % | C1, C3, C4, C7 |
| [GARA A PROCEDURA APERTA, SUDDIVISA IN 8 LOTTI, PER LA STIPULA DI UNA C](/convenzioni/cig-b0da5c472c/) | Consip | 114 | 1 | 0 | 0 | 12 | 8 % | C8 |
| [PROCEDURA NEGOZIATA PER L'AFFIDAMENTO DI SERVIZI IN OUTSOURCING DI CUS](/convenzioni/cig-a0260b3155/) | Altri | 100 | 1 | 0 | 0 | 12 | 8 % | – |
| [AQ PER LA FORNITURA DI PRODOTTI CLOUD IAAS E PAAS - ID 2213 | LOTTO 8 ](/convenzioni/consip-2213/) | Consip | 90 | 10 | 0 | 2 | 1 | 77 % | C1, C3, C4, C7 |

Le altre 56 iniziative sono nell'[indice](/convenzioni/) e nella [griglia](/convenzioni/griglia/).

## 6. Per tipo di soggetto

Fonti consultate il 05/11/2026.

| Soggetto | Iniziative | M€ 2024-25 | Indice medio | Non individuati | Non verificati |
|---|---|---|---|---|---|
| Consip | 45 | 51.555 | 56 % | 87 | 157 |
| PSN | 1 | 2.078 | n.d. (non ancora verificati) | 0 | 9 |
| Aggregatori regionali | 25 | 488 | n.d. (non ancora verificati) | 0 | 300 |
| Consorzi e unioni | 4 | 67 | n.d. (non ancora verificati) | 0 | 48 |
| Altri | 11 | 610 | n.d. (non ancora verificati) | 6 | 117 |

Per aggregatori regionali e consorzi quasi tutti i dati sono «da verificare»: le loro piattaforme (Sintel, Intercent-ER, EmPULIA, START…) non sono ancora state visitate, i CIG padre non hanno link ai documenti in PVL (verificato: nessuno dei 295 CIG padre) e su TED l'abbinamento riesce solo per testo. **Un indice basso qui misura il nostro lavoro ancora da fare, non la loro trasparenza.**

## 7. Metodo e limiti

- **Fonti.** BDNCP ANAC (nostro mirror, sha256 nel manifest) per i CIG padre e derivati; pagine dei bandi su consip.it, consultate il 5/11/2026; TED; open data Consip degli ordini (dati.consip.it, file 2024-2025 archiviati il 5/11/2026); atti di enti aderenti trovati con ricerca online (fonte non ufficiale, archiviati con sha256).
- **Verificato e riferito.** «Assente» vuol dire che abbiamo consultato la pagina ufficiale dell'iniziativa e il documento non c'è; il tipo di documento si deduce dal nome del file (controllo a mano solo per PRINCO). Le norme e i dati che non abbiamo letto sulla fonte sono marcati [R] nelle schede ([carenze.yaml](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/database/carenze.yaml)).
- **Valori.** Somme di importi dichiarati in BDNCP: ordine di grandezza, non spesa né transato (seconda misura al § 2). La prima iniziativa per valore pesa 29.918 M€ (55 % del totale).
- **Archivio.** 1.926 documenti ufficiali collegati alle iniziative (compresi i file dentro gli zip), archiviati con sha256; una cella «pubblico» può contenerne molti.
- **PVL.** Nessuno dei 295 CIG padre ha un link ai documenti di gara nei dati PVL scaricati il 3-4/11/2026 (verificato): è lo stato dei dati PVL, non un'assenza dei documenti, che gli aggregatori pubblicano sulle proprie piattaforme.
- **Rumore nel censimento.** Il filtro per CPV ICT sui derivati lascia passare iniziative non ICT (es. ID 2638 Energia elettrica 21, 30 M€): restano in elenco finché il filtro non viene corretto, con peso trascurabile sul totale.
- **Lettura dei documenti.** Letti per intero solo gli atti di PRINCO (ID 2928) e alcune determine di enti; per le altre iniziative le schede mostrano estratti automatici per parole chiave, marcati «da leggere».
- **Aggregatori.** Ancora da verificare (sopra). Il tipo di soggetto si assegna con regole sul nome della stazione appaltante, da controvalidare con l'elenco ANAC dei soggetti aggregatori.
- **Cosa non diciamo.** Che un dato assente sia nascosto di proposito; che un dato reperito presso un ente valga per tutta la convenzione.

## 8. Rimedi

- **Accesso civico generalizzato** (art. 5 c. 2 d.lgs. 33/2013), come rimedio di breve periodo e solo dopo le fonti del § 3: 19 bozze necessarie (carenza accertata e dato utile all'imbuto: prodotti e marchi delle iniziative cloud e multibrand, ordinativi delle più grandi, region e data center, erosione), 114 ritirate, 0 inviate. [Registro](/convenzioni/accesso-civico/) e [analisi dei dinieghi](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/accesso-civico/analisi-dinieghi.md).
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
| 0.3 | 2026-11-06 | acquistinretepa con browser reale (vetrina e schede pubbliche, documenti archiviati, sezione massimale residuo vuota alla consultazione), 36 allegati flussi dati analizzati, consumato per convenzione fonte per fonte, open data Consip 2026, siti AT in browser, elenco dei blocchi di accesso; revisione avversariale (10 punti) | consip-2483: documenti ufficiali da 56 a 66; consip-2610: documenti ufficiali da 51 a 53; consip-2615: documenti ufficiali da 33 a 37; consip-2425: documenti ufficiali da 59 a 67; consip-2536: documenti ufficiali da 26 a 32; consip-2599: documenti ufficiali da 97 a 99; consip-2366: documenti ufficiali da 77 a 85; consip-2738: documenti ufficiali da 99 a 101; consip-2755: documenti ufficiali da 35 a 37; consip-2601: documenti ufficiali da 53 a 57; consip-reti-locali-8: documenti ufficiali da 7 a 9; consip-2631: documenti ufficiali da 28 a 30; consip-2648: documenti ufficiali da 45 a 51; consip- |
| 0.2 | 2026-11-05 | fonti online consultate prima dell'accesso civico (acquistinretepa in parte, AT di Consip, campione di enti, ricerca web), allegato flussi dati di EA8 letto, abbinamenti open data confermati per testo, istanze ridotte con motivo per istanza, revisione avversariale (12 punti) | consip-2483: documenti da fonte non ufficiale da 0 a 7; consip-2610: documenti da fonte non ufficiale da 0 a 3; consip-2615: documenti da fonte non ufficiale da 1 a 4; psn: documenti da fonte non ufficiale da 0 a 4; consip-2425: documenti da fonte non ufficiale da 0 a 4; consip-2296: documenti da fonte non ufficiale da 0 a 3; consip-2536: documenti da fonte non ufficiale da 0 a 3; consip-2599: documenti da fonte non ufficiale da 0 a 2; consip-2366: documenti da fonte non ufficiale da 0 a 2; consip-2275: documenti da fonte non ufficiale da 0 a 3; istanze preparate: da 127 a 19 |
| 0.1 | 2026-11-05 | prima versione (bozza dopo revisione avversariale): 86 iniziative, documenti Consip archiviati, open data Consip degli ordini | prima versione |
