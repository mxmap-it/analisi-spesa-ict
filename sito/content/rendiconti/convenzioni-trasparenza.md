---
title: "Trasparenza delle convenzioni ICT della PA"
subtitle: "Rendiconto iterativo: cosa si può verificare delle convenzioni e degli accordi quadro ICT, e cosa no"
date: 2026-11-05
lastmod: 2026-11-06
datiAl: 2026-11-06
description: "Stato della trasparenza delle principali convenzioni e accordi quadro ICT (Consip, PSN, soggetti aggregatori): documenti pubblici, dati assenti, valore non verificabile, rimedi."
---

<!-- Generato da tools/convenzioni/rapporto.py dalla base dati: non modificare a mano. -->

**Versione 0.9 del 2026-11-06** · [registro delle revisioni](#registro-delle-revisioni) · [metodo](/progetto/metodo-convenzioni-trasparenza/) · **bozza da presentare a Fabio Pietrosanti prima di ogni diffusione esterna**

Ogni numero viene dalla base dati `report/convenzioni/database/` e si rifà con `python tools/verifiche/convenzioni_rapporto.py`.

## 1. Sintesi

*Cosa non diciamo:* che un dato non individuato sia nascosto di proposito; che un dato reperito presso un ente valga per tutta la convenzione; che le somme BDNCP siano spesa. Molte carenze riguardano dati che oggi nessuna norma obbliga a pubblicare.

- **Perimetro.** 86 iniziative ICT (82 attive): Consip, PSN, soggetti aggregatori regionali, consorzi e altre stazioni appaltanti con più contratti derivati. Criterio nel [README della base dati](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/database/README.md).
- **Valore.** I contratti derivati con CPV ICT pubblicati nel 2024-2025 dichiarano in BDNCP circa **54.798 M€**. È un ordine di grandezza, non la spesa: in molti casi l'importo dichiarato è il massimale o il valore pluriennale (§ 2).
- **Visibilità.** Dei 1.120 dati attesi (iniziativa × tipo di documento o dato): pubblici dalla fonte ufficiale 424 (37,9 %); reperiti solo presso enti aderenti 11 (1,0 %); non individuati sulla pagina del bando 93 (8,3 %); non ancora verificati 592 (52,9 %). Indice di visibilità medio **38 %**, da leggere come limite inferiore finché le celle non verificate restano così tante.
- **Dati per controllare spesa e sovranità.** Nelle iniziative verificate non abbiamo individuato, pubblicati insieme, offerte dei vincitori, transato per marchio ed elenco degli ordinativi per ente: sono dati che oggi la norma non obbliga la centrale a pubblicare (carenze C1-C4, con la base di ciascuna).
- **Carenze principali** (pagine dei bandi su consip.it, open data Consip, Amministrazione trasparente di Consip e campione di enti, consultati il 5-6/11/2026; acquistinretepa senza accesso): offerte tecniche dei vincitori, transato per listino e marchio, elenco degli ordinativi per ente non individuati. Gli ordinativi si trovano in parte negli atti dei singoli enti. Region e data center: per IaaS/PaaS 2 (ID 2746) e PRINCO (ID 2928) i documenti di gara prevedono che il fornitore li dichiari, ma la dichiarazione non è pubblicata.
- **Gli obblighi contrattuali prevedono che Consip riceva dati di dettaglio.** Secondo l'allegato 4E della convenzione Microsoft EA8 (ID 2615, letto per intero), il fornitore deve trasmettere ogni mese a Consip il dettaglio delle fatture, con l'ID dell'ordine sulla piattaforma e l'imponibile, per il calcolo della commissione (d.m. MEF 23/11/2012). Se il flusso è rispettato, Consip dispone dei dati per ricostruire il transato per ordine e quindi per ente (nostra deduzione, R); non abbiamo verificato che il flusso avvenga né in che forma sia conservato. Gli altri allegati sui flussi di fatturato li abbiamo letti per intero il 6/11 (`flussi-dati-letti.yaml`, V): 34 sono solo flussi per le commissioni sullo stesso modello (7 campi: tipo, numero, riferimento e data della fattura, partita IVA del fornitore, ID dell'ordine, imponibile; mensili più una dichiarazione semestrale), senza ente, prodotto, marchio né CIG; in 10 allegati recenti l'invio è dovuto anche a fatturato zero, «pena applicazione delle penali previste». Due allegati di **monitoraggio**, letti per intero, prevedono come obbligo contrattuale del fornitore l'invio mensile a Consip del flusso «Erogato» (ordine, lotto, sede beneficiaria, prodotto, quantità, importo IVA esclusa), entro il 15 del mese successivo, tramite la funzione «Gestione flussi» di acquistinretepa, pena le penali previste: l'allegato 18 «Flussi dati per il sistema di monitoraggio delle Convenzioni/AQ», versione 1.4 del 15/5/2019, all'AQ System Management 3 (ID 2275), e l'allegato B, versione non indicata nel testo, alla convenzione Telefonia mobile 9 (ID 2452). Non sappiamo se lo stesso obbligo valga per altre iniziative, i cui allegati di monitoraggio non abbiamo letto; non abbiamo verificato l'invio dei flussi né come Consip li conservi. Nessuna norma, a nostra conoscenza, ne impone la pubblicazione, che proponiamo in R37.
- **Rimedi.** Dopo le fonti online del § 3 (acquistinretepa ancora parziale), 30 bozze di accesso civico generalizzato, tutte verso Consip, restano utili all'analisi; 114 sono ritirate, con il motivo di ciascuna nel registro; **nessuna inviata**; proposte di policy R08 e R37-R44 perché questi dati diventino pubblici senza bisogno di chiederli.

## 2. Due misure del valore

Per 19 iniziative Consip esiste una seconda misura: gli **open data Consip** degli ordini diretti (dati.consip.it, 2024 e 2025, file archiviati con sha256): **6.349 M€** ordinati. Le stesse iniziative dichiarano in BDNCP **47.380 M€** di derivati ICT 2024-2025. **Le due grandezze non sono confrontabili** una a una: gli open data contano gli ordini diretti dell'anno (non gli appalti specifici degli accordi quadro con rilancio competitivo); BDNCP l'importo dichiarato all'acquisizione del CIG, spesso pluriennale o pari al massimale. La tabella serve a mostrare l'ordine di grandezza e i casi da spiegare (es. ID 2496, dove l'ordinato supera il dichiarato: cause possibili derivati con CPV non ICT, lotti non censiti o abbinamento da rivedere). Gli abbinamenti sono per coincidenza del nome («V-testo»): confermati con il titolo della pagina Consip trovata per ID Sigef, o per l'ID 2483 con atti di enti che riportano ID e CIG; nessun open data riporta l'ID Sigef. Gli open data non riportano listino, marchio né ente: la carenza C3 resta.

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
| [Consip AQ Servizi applicativi in ottica cloud e Demand/PMO P](/convenzioni/consip-2483/) | 29.918 | 839,8 | 1.529,5 | 491,8 | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [Consip Servizi applicativi in ottica cloud 3 (PAL), ID 2610](/convenzioni/consip-2610/) | 5.953 | 0 | 465,1 | 375,5 | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [Consip Licenze Microsoft Enterprise Agreement 8, ID 2615](/convenzioni/consip-2615/) | 3.015 | 317,2 | 25,2 | 11,4 | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [Consip AQ PC portatili, mobile workstation e Chromebook, ID ](/convenzioni/consip-2425/) | 1.617 | 42,4 | 11,5 | 0 | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [Consip Digital transformation 2, ID 2536, lotto 2 digitalizz](/convenzioni/consip-2536/) | 970 | 404,1 | 64,9 | 34,6 | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [Consip Licenze software multibrand 6, ID 2599, lotto 1 prodo](/convenzioni/consip-2599/) | 918 | 311,4 | 4,2 | 0 | scheda non individuata da noi | solo dato aggregato (relazioni gestioni 2021-2022) |
| [Consip AQ Sanità digitale, sistemi informativi gestionali](/convenzioni/consip-2366/) | 834 | 134,0 | 145,4 | 96,7 | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [GARA A PROCEDURA APERTA PER L’APPALTO DI FORNITURA MULTIBRAN](/convenzioni/consip-2738/) | 697 | 0 | 389,8 | 77,6 | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [Consip Licenze Microsoft Enterprise Agreement 9, ID 2755 (ip](/convenzioni/consip-2755/) | 692 | 0 | 261,5 | 84,1 | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [Consip Sanità digitale, sistemi clinico assistenziali 2, ID ](/convenzioni/consip-2601/) | 558 | 50,7 | 112,3 | 55,7 | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [Consip Reti locali 8, ID 2223, lotto 2 PAL](/convenzioni/consip-reti-locali-8/) | 554 | 234,5 | 63,7 | 0 | scheda non individuata da noi | solo dato aggregato (relazioni gestioni 2021-2022) |
| [Consip PC desktop e workstation 3, ID 2631, lotto 2](/convenzioni/consip-2631/) | 469 | 64,0 | 10,4 | 0,1 | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [AQ SERVIZI DI GESTIONE E MANUTENZIONE DI SISTEMI IP E POSTAZ](/convenzioni/consip-2648/) | 308 | 0 | 290,8 | 462,3 | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [Consip AQ Sanità digitale, sistemi informativi sanitari e se](/convenzioni/consip-2365/) | 297 | 124,1 | 35,2 | 0 | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [AQ PER I SERVIZI DI GESTIONE E MANUTENZIONE DI SISTEMI IP E ](/convenzioni/consip-2181/) | 232 | 47,5 | 0,1 | 0 | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [CLOUD ENABLING 1 ID 2652 | LOTTO 1: SERVIZI SUPPORTO ALL'ADO](/convenzioni/consip-2652/) | 190 | 59,3 | 108,9 | 77,1 | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [Consip AQ System management ed. 4, ID 2710 (lotto unico)](/convenzioni/consip-2710/) | 145 | – | – | – | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [AQ PER LA FORNITURA DI PRODOTTI CLOUD IAAS E PAAS - ID 2213 ](/convenzioni/consip-2213/) | 90 | 85,5 | 0 | 0 | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [ID 2453 - GARA PUBLIC CLOUD SAAS ITSM](/convenzioni/consip-2453/) | 84 | – | – | – | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [ACQUISIZIONE DI PC DESKTOP, WORKSTATION E MONITOR ED. 4 – ID](/convenzioni/consip-2781/) | 60 | – | – | – | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [Consip Licenze Microsoft Enterprise Agreement 6, ID 2187](/convenzioni/consip-2187/) | 50 | 14,0 | 0,3 | 0 | scheda non individuata da noi | solo dato aggregato (relazioni gestioni 2021-2022) |
| [PRODOTTI CLOUD IN MODALITÀ SOFTWARE AS A SERVICE NELL'AMBITO](/convenzioni/consip-2700/) | 32 | – | – | – | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [SERVIZI DI DATA MANAGEMENT PER LA PUBBLICA AMMINISTRAZIONE 2](/convenzioni/consip-2566/) | 32 | – | – | – | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [ID 2452 GARA A PROCEDURA APERTA AI SENSI DEL D.LGS. 50/2016 ](/convenzioni/consip-2452/) | 21 | – | – | – | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [GARA PER LA FORNITURA DI SERVIZI INTEGRATI, GESTIONALI ED OP](/convenzioni/consip-1561/) | 21 | – | – | – | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [AQ CENTRALI TELEFONICHE 9 - ID 2496](/convenzioni/consip-2496/) | 19 | 18,7 | 83,3 | 43,1 | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [FORNITURA DI SERVIZI CLOUD IAAS E PAAS | FORNITURA SERVIZI I](/convenzioni/consip-2746/) | 0 | – | – | – | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |
| [Consip PRINCO, Public cloud SaaS produttività individuale e ](/convenzioni/consip-2928/) | 0 | – | – | – | sezione presente, vuota alla consultazione senza accesso (causa non accertata) | solo dato aggregato (relazioni gestioni 2021-2022) |

**Perché le fonti non coincidono.** BDNCP registra l'importo dichiarato quando l'ente acquisisce il CIG derivato (spesso pluriennale o pari al massimale) e solo per i derivati con CPV ICT; gli open data Consip contano gli ordini diretti dell'anno (non gli appalti specifici con rilancio competitivo) per convenzione o AQ; la Corte dei conti riporta l'erogato complessivo degli accordi quadro, non per iniziativa. Per alcune iniziative (es. ID 2648 e ID 2496) l'ordinato supera il dichiarato BDNCP (derivati senza CPV ICT o CIG fuori dal 2024-25): le due misure non vanno sommate né sottratte. Il massimale residuo, che darebbe l'erosione per lotto, ha una sezione nella scheda pubblica di acquistinretepa che risulta vuota («Nessun risultato»): riprovato il 5-6/11 con attesa esplicita della risposta del servizio e con browser visibile (non headless) di notte, il servizio getDettaglioLotti risponde 200 senza dati. Non sappiamo se il dato sia visibile dopo l'accesso, se non sia popolato o se sia aggiornato altrove. È nell'[elenco dei blocchi](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/blocchi-accesso.csv) da provare a mano.


## 3. Fonti online consultate prima dell'accesso civico

Consultate il 5-6/11/2026 (date per fonte nelle schede), senza login né CAPTCHA, a ritmo basso e con User-Agent dichiarato.

| Fonte | Esito | Livello |
|---|---|---|
| Pagine dei bandi su consip.it | documentazione di gara di 44 iniziative; offerte, transato per marchio ed elenco degli ordinativi non individuati | V per la presenza dei file; R per il tipo dedotto dal nome |
| Open data Consip (dati.consip.it) | ordinato per anno, convenzione o AQ e lotto (2024-2025); niente ente, listino, marchio | V |
| acquistinretepa (browser reale, Chrome headless) | vetrina: 663 iniziative (servizio getIniziative, attive e archivio); schede pubbliche trovate per 26 iniziative del censimento, con 259 documenti linkati; sezione «Massimale residuo» vuota alla consultazione senza accesso (risposta senza dati in tre tentativi, anche con browser visibile; causa non accertata); catalogo e acquisto dietro «Accedi»; chiamate JSON registrate con sha256 | V |
| Amministrazione trasparente di Consip | le sottosezioni di «Bandi di gara e contratti» riguardano gli acquisti di Consip per sé; «Controlli e rilievi» rinvia alla Corte dei conti | V (indice delle sezioni) |
| Campione di enti aderenti | 45 righe valide (righe di controllo escluse), 28 enti, 10 iniziative: file nel percorso AT 6, URL esterno al percorso AT 27 (collegamento dalla sezione AT non verificato), non trovato 7, AT non verificabile automaticamente il 5/11 5 (da ripetere); 31 archiviati | V per i documenti letti; R per la posizione rispetto all'AT |
| Piattaforme degli aggregatori (Intercent-ER, EmPULIA, Sintel/NECA, START), parti pubbliche, browser reale | pagine pubbliche per 8 iniziative; documenti di gara, convenzioni e listini archiviati per Intercent-ER ed EmPULIA; su NECA (ARIA) la scheda pubblica mostra massimale ed estensione e per il residuo rinvia ai titolari di credenziali; su START le schede di aggiudicazione portano al login e i documenti della gara 015433-2020 sono elencati ma scaricabili solo fino alla scadenza delle offerte (17/10/2020), come prevede la piattaforma | V |
| Ricerca web (Corte dei conti, stampa, atti di enti) | 15 dati da 13 URL, 9 archiviati; erogato per iniziativa non trovato (nelle due relazioni della Corte dei conti consultate, gestioni 2021 e 2022, l'erogato degli AQ è aggregato) | R |
| Allegati «flussi dati del fatturato» | 36 allegati acquisiti e letti per intero (6/11), compreso quello di EA8: invio mensile a Consip del dettaglio delle fatture (numero, data, ID dell'ordine, imponibile); in 35 non compaiono campi per ente, prodotto o marchio; inoltre due allegati di **monitoraggio**, letti per intero (ID 2275, All. 18 v1.4 del 15/5/2019; ID 2452, All. B), prevedono il flusso mensile «Erogato» per ordine, lotto, sede, prodotto, quantità e importo; quello dell'ID 2648 riguarda invece solo le commissioni | V (tutti letti per intero) |

Il dettaglio per iniziativa e per ente è nelle [schede](/convenzioni/) e nei file [enti-campione](https://github.com/mxmap-it/analisi-spesa-ict/tree/main/report/convenzioni/enti-campione) e [fonti-non-ufficiali](https://github.com/mxmap-it/analisi-spesa-ict/tree/main/report/convenzioni/fonti-non-ufficiali), in un formato riusabile dal monitor dell'Amministrazione trasparente.


## 4. Matrice

La [griglia di tutte le iniziative](/convenzioni/griglia/) mostra cella per cella cosa è pubblico, cosa è reperito altrove, cosa manca e cosa è stato richiesto, con i riepiloghi in alto. L'[indice delle convenzioni](/convenzioni/) riporta il riquadro delle carenze di trasparenza.

Celle al 05/11/2026 (documenti) e BDNCP elaborato il 05/11/2026.

| Classe | Celle | Quota |
|---|---|---|
| pubblico (fonte ufficiale) | 424 | 37,9 % |
| solo da fonte non ufficiale | 11 | 1,0 % |
| non individuato sulla pagina del bando | 93 | 8,3 % |
| non ancora verificato | 592 | 52,9 % |

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
| [ARIA_2023_807 - PROCEDURA APERTA, AI SENSI DELL’ART. 60 DEL D.LGS. N. ](/convenzioni/cig-989984280e/) | Aggregatori regionali | 160 | 6 | 0 | 0 | 7 | 46 % | – |
| [GARA A PROCEDURA APERTA SUDDIVISA IN 4 LOTTI PER L'AFFIDAMENTO DEI SER](/convenzioni/consip-1774/) | Altri | 147 | 4 | 0 | 3 | 6 | 31 % | C1, C4 |
| [Consip AQ System management ed. 4, ID 2710 (lotto unico)](/convenzioni/consip-2710/) | Consip | 145 | 8 | 0 | 3 | 2 | 62 % | C1, C3, C4, C7 |
| [GARA A PROCEDURA APERTA, SUDDIVISA IN 8 LOTTI, PER LA STIPULA DI UNA C](/convenzioni/cig-b0da5c472c/) | Consip | 114 | 1 | 0 | 0 | 12 | 8 % | C8 |
| [PROCEDURA NEGOZIATA PER L'AFFIDAMENTO DI SERVIZI IN OUTSOURCING DI CUS](/convenzioni/cig-a0260b3155/) | Altri | 100 | 1 | 0 | 0 | 12 | 8 % | – |
| [AQ PER LA FORNITURA DI PRODOTTI CLOUD IAAS E PAAS - ID 2213 | LOTTO 8 ](/convenzioni/consip-2213/) | Consip | 90 | 10 | 0 | 2 | 1 | 77 % | C1, C3, C4, C7 |

Le altre 56 iniziative sono nell'[indice](/convenzioni/) e nella [griglia](/convenzioni/griglia/).

## 5bis. Documenti mancanti, file per file

Inventario analitico ([CSV](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/database/documenti-mancanti.csv), [metodo](/progetto/metodo-convenzioni-trasparenza/)): **782 documenti mancanti** in 86 iniziative; criticità 3: **415**, criticità 2: 131, criticità 1: 236. Per metodo: numerazione 13, rimando 143, atteso 633 (una riga può averne due). Livello: [V] 421 (pagina ufficiale ricontrollata dal vivo, file assente), [R] 361 (da verificare). Blocchi incontrati nel ricontrollo: 0; documenti forse in aree riservate (dietro_login «ignoto»): 234, da provare in un giro assistito.

**Esempio guida: PRINCO, ID 2928, Allegato 12.** L'Allegato 12 «Facsimile per allegato al Listino OpenSource» è pubblicato, ma è un modulo vuoto: l'Appendice 3 al Capitolato (Listino Open Source) dice che i prodotti «saranno presentati dai concorrenti conformemente all'allegato 12». Manca quindi l'Allegato 12 **compilato** dall'aggiudicatario (Converge): l'unico documento con i prodotti del listino 3 e dunque con la loro giurisdizione [V, atti letti].

Conteggi per iniziativa:

| Iniziativa | Criticità 3 | Criticità 2 | Criticità 1 | Totale | di cui [V] |
|---|---|---|---|---|---|
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN ACCORDO QUADRO, AI SE](/convenzioni/cig-8765571a03/) | 7 | 1 | 5 | 13 | 10 |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN ACCORDO QUADRO, AI SE](/convenzioni/cig-9030521daa/) | 7 | 1 | 5 | 13 | 10 |
| [Consip AQ Sanità digitale, sistemi informativi gestionali](/convenzioni/consip-2366/) | 7 | 0 | 5 | 12 | 9 |
| [SERVIZI DI DATA MANAGEMENT PER LA PUBBLICA AMMINISTRAZIONE 2 ID 2566 |](/convenzioni/consip-2566/) | 7 | 1 | 2 | 10 | 7 |
| [GARA STRATEGICA SERVIZI APPLICATIVI IN OTTICA CLOUD E PMO PER LE P.A. ](/convenzioni/consip-2212/) | 7 | 1 | 0 | 8 | 6 |
| [Consip AQ System management ed. 3, ID 2275, lotto 1](/convenzioni/consip-2275/) | 7 | 1 | 0 | 8 | 6 |
| [Consip SPC Cloud lotto 1, servizi di cloud computing (SIGEF 1.403)](/convenzioni/consip-1403/) | 6 | 2 | 4 | 12 | 4 |
| [Consip AQ Sanità digitale, sistemi informativi sanitari e servizi al c](/convenzioni/consip-2365/) | 6 | 1 | 4 | 11 | 9 |
| [Consip AQ Servizi applicativi in ottica cloud e Demand/PMO PA centrali](/convenzioni/consip-2483/) | 6 | 0 | 3 | 9 | 7 |
| [FORNITURA DI SERVIZI CLOUD IAAS E PAAS | FORNITURA SERVIZI IAAS E PAAS](/convenzioni/consip-2746/) | 6 | 0 | 3 | 9 | 6 |
| [ACCORDO QUADRO AVENTE AD OGGETTO LA FORNITURA DI UN 'CATALOGO DI PRODO](/convenzioni/consip-2297/) | 6 | 0 | 2 | 8 | 4 |
| [GARA A PROCEDURA APERTA SUDDIVISA IN 4 LOTTI PER L'AFFIDAMENTO DEI SER](/convenzioni/consip-1774/) | 5 | 6 | 18 | 29 | 19 |
| [L'APPALTO HA AD OGGETTO L'ACQUISIZIONE DI SERVIZI DI SVILUPPO, MANUTEN](/convenzioni/cig-b2fb115279/) | 5 | 4 | 5 | 14 | 10 |
| [Consip Digital transformation 2, ID 2536, lotto 2 digitalizzazione dei](/convenzioni/consip-2536/) | 5 | 2 | 6 | 13 | 10 |
| [GARA 7/2017/LI: PROCEDURA RISTRETTA AI SENSI DELL'ART. 61 DEL D.LGS. 5](/convenzioni/cig-7246653f38/) | 5 | 3 | 4 | 12 | 0 |
| [P.A. IN DUE LOTTI PER LA STIPULA DI UNA CONVENZIONE PER LA FORNITURA I](/convenzioni/cig-759453695c/) | 5 | 3 | 4 | 12 | 0 |
| [SERVIZI DI MANUTENZIONE, ASSISTENZA HARDWARE E SOFTWARE DI BASE PER LE](/convenzioni/cig-7812108376/) | 5 | 3 | 4 | 12 | 0 |
| [SERVIZIO DI GESTIONE DEL SISTEMA TELEMATICO ACQUISTI REGIONALE DELLA T](/convenzioni/cig-7930885557/) | 5 | 3 | 4 | 12 | 0 |
| [PROCEDURA NEGOZIATA, EX ART. 63, COMMA 2 - LETT. B) PUNTO 3), D. LGS. ](/convenzioni/cig-8716552642/) | 5 | 3 | 4 | 12 | 0 |
| [PROCEDURA NEGOZIATA, EX ART. 63, COMMA 2 - LETT. B) PUNTO 3), D. LGS. ](/convenzioni/cig-87332390d0/) | 5 | 3 | 4 | 12 | 0 |
| [SERVIZIO DI RACCOLTA, GESTIONE ED ELABORAZIONE DI DATI NEL SETTORE DEL](/convenzioni/cig-88556834cb/) | 5 | 3 | 4 | 12 | 0 |
| [GARA A PROCEDURA APERTA PER L'AFFIDAMENTO DI UN ACCORDO QUADRO AI SENS](/convenzioni/cig-8898059e90/) | 5 | 3 | 4 | 12 | 0 |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN ACCORDO QUADRO, AI SE](/convenzioni/cig-91881762b3/) | 5 | 3 | 4 | 12 | 0 |
| [ACCORDO QUADRO PER LA FORNITURA DI UNA PIATTAFORMA PER IL MONITORAGGIO](/convenzioni/cig-945403654f/) | 5 | 3 | 4 | 12 | 0 |
| [PROSECUZIONE SERVIZIO DI CONSERVAZIONE A NORMA PER AZIENDE ED ENTI DEL](/convenzioni/cig-9603457f68/) | 5 | 3 | 4 | 12 | 0 |
| [ACCORDO QUADRO PER L'AFFIDAMENTO, IN FORMA AGGREGATA E AD UN UNICO FOR](/convenzioni/cig-9777818ea8/) | 5 | 3 | 4 | 12 | 0 |
| [ACCORDO QUADRO, SUDDIVISO IN 9 LOTTI, CON PIÙ OPERATORI ECONOMICI, AI ](/convenzioni/cig-99617296d3/) | 5 | 3 | 4 | 12 | 0 |
| [GARA A PROCEDURA APERTA, SUDDIVISA IN 8 LOTTI, PER LA STIPULA DI UNA C](/convenzioni/cig-b0da5c472c/) | 5 | 3 | 4 | 12 | 0 |
| [PROCEDURA NEGOZIATA SENZA BANDO AI SENSI DELL'ART. 76, C. 2, LETT. B),](/convenzioni/cig-b715929978/) | 5 | 3 | 4 | 12 | 0 |
| [PROCEDURA DI AFFIDAMENTO IN HOUSE AI SENSI DELL'ART. 7 DEL D.LGS. 36/2](/convenzioni/cig-b736423c63/) | 5 | 3 | 4 | 12 | 12 |
| [SERVIZI DI POSTA ELETTRONICA CERTIFICATA (PEC) 2 - ID 2556](/convenzioni/consip-2556/) | 5 | 3 | 4 | 12 | 0 |
| [Consip SPC2 Connettività (contratto quadro OPA)](/convenzioni/cig-5133642f61/) | 5 | 2 | 4 | 11 | 0 |
| [Trenitalia, affidamento di servizi ICT](/convenzioni/cig-7991036b82/) | 5 | 3 | 3 | 11 | 0 |
| [CONVENZIONE PER IL SERVIZIO DI DESKTOP OUTSOURCING](/convenzioni/cig-95643027b0/) | 5 | 2 | 4 | 11 | 0 |
| [PROCEDURA NEGOZIATA PER L'AFFIDAMENTO DI SERVIZI IN OUTSOURCING DI CUS](/convenzioni/cig-a0260b3155/) | 5 | 3 | 3 | 11 | 0 |
| [ID 2453 - GARA PUBLIC CLOUD SAAS ITSM](/convenzioni/consip-2453/) | 5 | 3 | 3 | 11 | 0 |
| [Consip Sanità digitale, sistemi clinico assistenziali 2, ID 2601, lott](/convenzioni/consip-2601/) | 5 | 0 | 6 | 11 | 9 |
| [GARA TELEMATICA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN ACCORDO QU](/convenzioni/cig-8637686bf8/) | 5 | 1 | 4 | 10 | 10 |
| [AQ CENTRALI TELEFONICHE 9 - ID 2496](/convenzioni/consip-2496/) | 5 | 2 | 3 | 10 | 8 |
| [PROCEDURA APERTA PER L'AFFIDAMENTO DEL SERVIZIO DI LETTURA ED ELABORAZ](/convenzioni/cig-9837572d38/) | 5 | 2 | 2 | 9 | 9 |
| [AQ PER I SERVIZI DI GESTIONE E MANUTENZIONE DI SISTEMI IP E POSTAZIONI](/convenzioni/consip-2181/) | 5 | 3 | 1 | 9 | 8 |
| [Consip Licenze Microsoft Enterprise Agreement 8, ID 2615](/convenzioni/consip-2615/) | 5 | 1 | 3 | 9 | 8 |
| [PA PER LA STIPULA DI UNA CONVENZIONE, DELLA DURATA DI 72 MESI, PER IL ](/convenzioni/cig-9216207e99/) | 5 | 2 | 1 | 8 | 8 |
| [ARIA_2023_807 - PROCEDURA APERTA, AI SENSI DELL’ART. 60 DEL D.LGS. N. ](/convenzioni/cig-989984280e/) | 5 | 1 | 2 | 8 | 8 |
| [PROCEDURA AOERTA PER LA CONCLUSIONE DI UNA CONVENZIONE DELLA DURATA DI](/convenzioni/cig-81636687f2/) | 5 | 1 | 1 | 7 | 7 |
| [PROCEDURA APERTA PER LA CONCLUSIONE DI UNA CONVENZIONE DELLA DURATA DI](/convenzioni/cig-84163618ce/) | 5 | 1 | 1 | 7 | 7 |
| [GARA A PROCEDURA APERTA PER L'AFFIDAMENTO DI UN ACCORDO QUADRO IN UN U](/convenzioni/cig-8784303c25/) | 5 | 1 | 1 | 7 | 5 |
| [SERVIZI E PRESTAZIONI INERENTI LA PROGETTAZIONE, SVILUPPO, CONFIGURAZI](/convenzioni/cig-94252656ba/) | 5 | 1 | 1 | 7 | 7 |
| [GARA EUROPEA A LOTTI PER L'ACQUISIZIONE, MEDIANTE ACCORDO QUADRO, DI S](/convenzioni/cig-9769148bf3/) | 5 | 0 | 2 | 7 | 7 |
| [GARA EUROPEA A LOTTI PER L'ACQUISIZIONE, MEDIANTE ACCORDO QUADRO, DI S](/convenzioni/cig-a02b1c8a8a/) | 5 | 1 | 1 | 7 | 7 |
| [SERVIZI INFORMATICI PER L EVOLUZIONE DEI SISTEMI INFORMATIVI DEGLI ENT](/convenzioni/cig-b1ffb3098a/) | 5 | 1 | 1 | 7 | 7 |
| [AQ SERVIZI DI GESTIONE E MANUTENZIONE DI SISTEMI IP E POSTAZIONE DI LA](/convenzioni/consip-2648/) | 5 | 0 | 2 | 7 | 4 |
| [PROCEDUTA APERTA TELEMATICA PER L'AFFIDAMENTO DEL SERVIZIO DI GESTIONE](/convenzioni/cig-949554539f/) | 5 | 1 | 0 | 6 | 6 |
| [Consip AQ System management, ID 1836](/convenzioni/consip-1836/) | 5 | 0 | 1 | 6 | 3 |
| [AQ PER LA FORNITURA DI PRODOTTI CLOUD IAAS E PAAS - ID 2213 | LOTTO 8 ](/convenzioni/consip-2213/) | 5 | 0 | 1 | 6 | 5 |
| [CLOUD ENABLING 1 ID 2652 | LOTTO 1: SERVIZI SUPPORTO ALL'ADOZIONE E PM](/convenzioni/consip-2652/) | 5 | 0 | 1 | 6 | 4 |
| [ACQUISIZIONE DI PC DESKTOP, WORKSTATION E MONITOR ED. 4 – ID 2781 | FO](/convenzioni/consip-2781/) | 5 | 0 | 1 | 6 | 4 |
| [Consip PRINCO, Public cloud SaaS produttività individuale e collaborat](/convenzioni/consip-2928/) | 5 | 1 | 0 | 6 | 5 |
| [FORNITURA IN NOLEGGIO DI APPARECCHIATURE MULTIFUNZIONE DI FASCIA MEDIA](/convenzioni/cig-b1457d3391/) | 5 | 0 | 0 | 5 | 3 |
| [ID 2452 GARA A PROCEDURA APERTA AI SENSI DEL D.LGS. 50/2016 E S.M.I., ](/convenzioni/consip-2452/) | 5 | 0 | 0 | 5 | 3 |
| [Consip Reti locali 8, ID 2223, lotto 2 PAL](/convenzioni/consip-reti-locali-8/) | 4 | 2 | 4 | 10 | 6 |
| [PROCEDURA APERTA PER LA FORNITURA DI SERVIZI DI TRASMISSIONE DATI E VO](/convenzioni/cig-9016294130/) | 4 | 1 | 4 | 9 | 9 |
| [PROCEDURA NEGOZIATA PER L’AFFIDAMENTO DEI SERVIZI DI MANUTENZIONE, ASS](/convenzioni/cig-9481064585/) | 4 | 2 | 3 | 9 | 9 |
| [PROCEDURA NEGOZIATA PER L’AFFIDAMENTO DEI SERVIZI DI MANUTENZIONE, ASS](/convenzioni/cig-9482392d69/) | 4 | 2 | 3 | 9 | 9 |
| [APPALTO SPECIFICO (SDA) PER L'ACQUISIZIONE DI SERVIZI DI BUSINESS ANAL](/convenzioni/cig-9923894067/) | 4 | 1 | 4 | 9 | 9 |
| [APPALTO SPECIFICO INDETTO DA INNOVAPUGLIA S.P.A. FINALIZZATO ALLA STIP](/convenzioni/cig-993049146a/) | 4 | 1 | 4 | 9 | 9 |
| [Polo Strategico Nazionale (PPP, Presidenza del Consiglio)](/convenzioni/psn/) | 4 | 2 | 3 | 9 | 0 |
| [AOV/SUA SF 009/2021 - CONVENZIONE QUADRO ACP PER SERVIZI ICT | LOTTO 2](/convenzioni/cig-8664818204/) | 4 | 2 | 2 | 8 | 8 |
| [PROCEDURA APERTA PER L’AFFIDAMENTO DEI SERVIZI DI GESTIONE DELLE SANZI](/convenzioni/cig-9580558e8e/) | 4 | 1 | 3 | 8 | 8 |
| [APPALTO SPECIFICO PER L’ACQUISIZIONE DEL SERVIZIO DI ASSISTENZA TECNIC](/convenzioni/cig-9936839af1/) | 4 | 1 | 3 | 8 | 8 |
| [Consip AQ System management ed. 4, ID 2710 (lotto unico)](/convenzioni/consip-2710/) | 4 | 3 | 1 | 8 | 6 |
| [Consip PC desktop e workstation 3, ID 2631, lotto 2](/convenzioni/consip-2631/) | 4 | 0 | 3 | 7 | 4 |
| [PRODOTTI CLOUD IN MODALITÀ SOFTWARE AS A SERVICE NELL'AMBITO DEL CRM E](/convenzioni/consip-2700/) | 4 | 0 | 3 | 7 | 5 |
| [GARA PER LA FORNITURA DI SERVIZI INTEGRATI, GESTIONALI ED OPERATIVI, D](/convenzioni/consip-1561/) | 4 | 1 | 1 | 6 | 3 |
| [GARA A PROCEDURA APERTA PER L'AFFIDAMENTO DELLA FORNITURA DI PRODOTTI ](/convenzioni/consip-2480/) | 4 | 1 | 1 | 6 | 4 |
| [Consip Servizi applicativi in ottica cloud 3 (PAL), ID 2610](/convenzioni/consip-2610/) | 4 | 1 | 1 | 6 | 4 |
| [APPALTO SPECIFICO (SDA) PER LA FORNITURA IN ACQUISTO E NOLEGGIO DI PC ](/convenzioni/cig-9845010742/) | 4 | 0 | 1 | 5 | 5 |
| [Consip AQ PC portatili, mobile workstation e Chromebook, ID 2425, lott](/convenzioni/consip-2425/) | 4 | 0 | 1 | 5 | 3 |
| [ENERGIA ELETTRICA 21 - ID 2638 | LOMBARDIA ESCLUSE LA PROVINCIA DI MIL](/convenzioni/consip-2638/) | 4 | 0 | 1 | 5 | 3 |
| [PROCEDURA APERTA PER L'ACQUISIZIONE DI SERVIZI DI IT SYSTEM MANAGEMENT](/convenzioni/cig-97219284c8/) | 4 | 0 | 0 | 4 | 4 |
| [PROCEDURA APERTA PER LA FORNITURA DI SERVIZI DI SVILUPPO, EVOLUZIONE E](/convenzioni/cig-a008db40ba/) | 4 | 0 | 0 | 4 | 4 |
| [Consip Licenze Microsoft Enterprise Agreement 6, ID 2187](/convenzioni/consip-2187/) | 3 | 1 | 3 | 7 | 3 |
| [Consip Licenze software multibrand 6, ID 2599, lotto 1 prodotti Oracle](/convenzioni/consip-2599/) | 3 | 0 | 2 | 5 | 4 |
| [Consip Licenze Microsoft Enterprise Agreement 9, ID 2755 (ipotesi fort](/convenzioni/consip-2755/) | 3 | 0 | 1 | 4 | 3 |
| [GARA A PROCEDURA APERTA PER L’APPALTO DI FORNITURA MULTIBRAND DI PRODO](/convenzioni/consip-2738/) | 3 | 0 | 0 | 3 | 2 |
| [Consip AQ Servizi di sicurezza da remoto, compliance e controllo, ID 2](/convenzioni/consip-2296/) | 2 | 5 | 1 | 8 | 8 |

Mancanti di criticità 3 (decisivi per giurisdizione del prodotto o controllo della spesa):

| Iniziativa | Documento | Metodo | Livello | Contenuto presunto | Accesso civico |
|---|---|---|---|---|---|
| [Consip SPC2 Connettività (contratto quadro OPA)](/convenzioni/cig-5133642f61/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [R] | ordinativi e contratti attuativi delle PA | – |
| [Consip SPC2 Connettività (contratto quadro OPA)](/convenzioni/cig-5133642f61/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [R] | transato e monitoraggio per lotto e listino | – |
| [Consip SPC2 Connettività (contratto quadro OPA)](/convenzioni/cig-5133642f61/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [Consip SPC2 Connettività (contratto quadro OPA)](/convenzioni/cig-5133642f61/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [Consip SPC2 Connettività (contratto quadro OPA)](/convenzioni/cig-5133642f61/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [R] | offerta tecnica dell'aggiudicatario | – |
| [GARA 7/2017/LI: PROCEDURA RISTRETTA AI SENSI DELL'](/convenzioni/cig-7246653f38/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [R] | ordinativi e contratti attuativi delle PA | – |
| [GARA 7/2017/LI: PROCEDURA RISTRETTA AI SENSI DELL'](/convenzioni/cig-7246653f38/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [R] | transato e monitoraggio per lotto e listino | – |
| [GARA 7/2017/LI: PROCEDURA RISTRETTA AI SENSI DELL'](/convenzioni/cig-7246653f38/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [GARA 7/2017/LI: PROCEDURA RISTRETTA AI SENSI DELL'](/convenzioni/cig-7246653f38/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [GARA 7/2017/LI: PROCEDURA RISTRETTA AI SENSI DELL'](/convenzioni/cig-7246653f38/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [R] | offerta tecnica dell'aggiudicatario | – |
| [P.A. IN DUE LOTTI PER LA STIPULA DI UNA CONVENZION](/convenzioni/cig-759453695c/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [R] | ordinativi e contratti attuativi delle PA | – |
| [P.A. IN DUE LOTTI PER LA STIPULA DI UNA CONVENZION](/convenzioni/cig-759453695c/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [R] | transato e monitoraggio per lotto e listino | – |
| [P.A. IN DUE LOTTI PER LA STIPULA DI UNA CONVENZION](/convenzioni/cig-759453695c/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [P.A. IN DUE LOTTI PER LA STIPULA DI UNA CONVENZION](/convenzioni/cig-759453695c/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [P.A. IN DUE LOTTI PER LA STIPULA DI UNA CONVENZION](/convenzioni/cig-759453695c/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [R] | offerta tecnica dell'aggiudicatario | – |
| [SERVIZI DI MANUTENZIONE, ASSISTENZA HARDWARE E SOF](/convenzioni/cig-7812108376/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [R] | ordinativi e contratti attuativi delle PA | – |
| [SERVIZI DI MANUTENZIONE, ASSISTENZA HARDWARE E SOF](/convenzioni/cig-7812108376/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [R] | transato e monitoraggio per lotto e listino | – |
| [SERVIZI DI MANUTENZIONE, ASSISTENZA HARDWARE E SOF](/convenzioni/cig-7812108376/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [SERVIZI DI MANUTENZIONE, ASSISTENZA HARDWARE E SOF](/convenzioni/cig-7812108376/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [SERVIZI DI MANUTENZIONE, ASSISTENZA HARDWARE E SOF](/convenzioni/cig-7812108376/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [R] | offerta tecnica dell'aggiudicatario | – |
| [SERVIZIO DI GESTIONE DEL SISTEMA TELEMATICO ACQUIS](/convenzioni/cig-7930885557/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [R] | ordinativi e contratti attuativi delle PA | – |
| [SERVIZIO DI GESTIONE DEL SISTEMA TELEMATICO ACQUIS](/convenzioni/cig-7930885557/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [R] | transato e monitoraggio per lotto e listino | – |
| [SERVIZIO DI GESTIONE DEL SISTEMA TELEMATICO ACQUIS](/convenzioni/cig-7930885557/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [SERVIZIO DI GESTIONE DEL SISTEMA TELEMATICO ACQUIS](/convenzioni/cig-7930885557/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [SERVIZIO DI GESTIONE DEL SISTEMA TELEMATICO ACQUIS](/convenzioni/cig-7930885557/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [R] | offerta tecnica dell'aggiudicatario | – |
| [Trenitalia, affidamento di servizi ICT](/convenzioni/cig-7991036b82/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [R] | ordinativi e contratti attuativi delle PA | – |
| [Trenitalia, affidamento di servizi ICT](/convenzioni/cig-7991036b82/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [R] | transato e monitoraggio per lotto e listino | – |
| [Trenitalia, affidamento di servizi ICT](/convenzioni/cig-7991036b82/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [Trenitalia, affidamento di servizi ICT](/convenzioni/cig-7991036b82/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [Trenitalia, affidamento di servizi ICT](/convenzioni/cig-7991036b82/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [R] | offerta tecnica dell'aggiudicatario | – |
| [PROCEDURA AOERTA PER LA CONCLUSIONE DI UNA CONVENZ](/convenzioni/cig-81636687f2/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [PROCEDURA AOERTA PER LA CONCLUSIONE DI UNA CONVENZ](/convenzioni/cig-81636687f2/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [PROCEDURA AOERTA PER LA CONCLUSIONE DI UNA CONVENZ](/convenzioni/cig-81636687f2/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [V] | listini e appendici di prezzo | in preparazione |
| [PROCEDURA AOERTA PER LA CONCLUSIONE DI UNA CONVENZ](/convenzioni/cig-81636687f2/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [PROCEDURA AOERTA PER LA CONCLUSIONE DI UNA CONVENZ](/convenzioni/cig-81636687f2/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [PROCEDURA APERTA PER LA CONCLUSIONE DI UNA CONVENZ](/convenzioni/cig-84163618ce/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [PROCEDURA APERTA PER LA CONCLUSIONE DI UNA CONVENZ](/convenzioni/cig-84163618ce/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [PROCEDURA APERTA PER LA CONCLUSIONE DI UNA CONVENZ](/convenzioni/cig-84163618ce/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [V] | listini e appendici di prezzo | in preparazione |
| [PROCEDURA APERTA PER LA CONCLUSIONE DI UNA CONVENZ](/convenzioni/cig-84163618ce/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [PROCEDURA APERTA PER LA CONCLUSIONE DI UNA CONVENZ](/convenzioni/cig-84163618ce/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [GARA TELEMATICA A PROCEDURA APERTA PER LA CONCLUSI](/convenzioni/cig-8637686bf8/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [GARA TELEMATICA A PROCEDURA APERTA PER LA CONCLUSI](/convenzioni/cig-8637686bf8/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [GARA TELEMATICA A PROCEDURA APERTA PER LA CONCLUSI](/convenzioni/cig-8637686bf8/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [V] | listini e appendici di prezzo | in preparazione |
| [GARA TELEMATICA A PROCEDURA APERTA PER LA CONCLUSI](/convenzioni/cig-8637686bf8/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [GARA TELEMATICA A PROCEDURA APERTA PER LA CONCLUSI](/convenzioni/cig-8637686bf8/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [AOV/SUA SF 009/2021 - CONVENZIONE QUADRO ACP PER S](/convenzioni/cig-8664818204/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [AOV/SUA SF 009/2021 - CONVENZIONE QUADRO ACP PER S](/convenzioni/cig-8664818204/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [AOV/SUA SF 009/2021 - CONVENZIONE QUADRO ACP PER S](/convenzioni/cig-8664818204/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [AOV/SUA SF 009/2021 - CONVENZIONE QUADRO ACP PER S](/convenzioni/cig-8664818204/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [PROCEDURA NEGOZIATA, EX ART. 63, COMMA 2 - LETT. B](/convenzioni/cig-8716552642/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [R] | ordinativi e contratti attuativi delle PA | – |
| [PROCEDURA NEGOZIATA, EX ART. 63, COMMA 2 - LETT. B](/convenzioni/cig-8716552642/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [R] | transato e monitoraggio per lotto e listino | – |
| [PROCEDURA NEGOZIATA, EX ART. 63, COMMA 2 - LETT. B](/convenzioni/cig-8716552642/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [PROCEDURA NEGOZIATA, EX ART. 63, COMMA 2 - LETT. B](/convenzioni/cig-8716552642/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [PROCEDURA NEGOZIATA, EX ART. 63, COMMA 2 - LETT. B](/convenzioni/cig-8716552642/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [R] | offerta tecnica dell'aggiudicatario | – |
| [PROCEDURA NEGOZIATA, EX ART. 63, COMMA 2 - LETT. B](/convenzioni/cig-87332390d0/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [R] | ordinativi e contratti attuativi delle PA | – |
| [PROCEDURA NEGOZIATA, EX ART. 63, COMMA 2 - LETT. B](/convenzioni/cig-87332390d0/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [R] | transato e monitoraggio per lotto e listino | – |
| [PROCEDURA NEGOZIATA, EX ART. 63, COMMA 2 - LETT. B](/convenzioni/cig-87332390d0/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [PROCEDURA NEGOZIATA, EX ART. 63, COMMA 2 - LETT. B](/convenzioni/cig-87332390d0/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [PROCEDURA NEGOZIATA, EX ART. 63, COMMA 2 - LETT. B](/convenzioni/cig-87332390d0/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [R] | offerta tecnica dell'aggiudicatario | – |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN A](/convenzioni/cig-8765571a03/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN A](/convenzioni/cig-8765571a03/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN A](/convenzioni/cig-8765571a03/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN A](/convenzioni/cig-8765571a03/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN A](/convenzioni/cig-8765571a03/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN A](/convenzioni/cig-8765571a03/) | Allegato C  – Offerta economica | rimando | [V] | Offerta economica (parte dell'offerta dell'aggiudicatario) | in preparazione |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN A](/convenzioni/cig-8765571a03/) | Allegato D  – Corrispettivi e tariffe | rimando | [V] | Corrispettivi e tariffe | in preparazione |
| [GARA A PROCEDURA APERTA PER L'AFFIDAMENTO DI UN AC](/convenzioni/cig-8784303c25/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [GARA A PROCEDURA APERTA PER L'AFFIDAMENTO DI UN AC](/convenzioni/cig-8784303c25/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [GARA A PROCEDURA APERTA PER L'AFFIDAMENTO DI UN AC](/convenzioni/cig-8784303c25/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [GARA A PROCEDURA APERTA PER L'AFFIDAMENTO DI UN AC](/convenzioni/cig-8784303c25/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [GARA A PROCEDURA APERTA PER L'AFFIDAMENTO DI UN AC](/convenzioni/cig-8784303c25/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [SERVIZIO DI RACCOLTA, GESTIONE ED ELABORAZIONE DI ](/convenzioni/cig-88556834cb/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [R] | ordinativi e contratti attuativi delle PA | – |
| [SERVIZIO DI RACCOLTA, GESTIONE ED ELABORAZIONE DI ](/convenzioni/cig-88556834cb/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [R] | transato e monitoraggio per lotto e listino | – |
| [SERVIZIO DI RACCOLTA, GESTIONE ED ELABORAZIONE DI ](/convenzioni/cig-88556834cb/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [SERVIZIO DI RACCOLTA, GESTIONE ED ELABORAZIONE DI ](/convenzioni/cig-88556834cb/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [SERVIZIO DI RACCOLTA, GESTIONE ED ELABORAZIONE DI ](/convenzioni/cig-88556834cb/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [R] | offerta tecnica dell'aggiudicatario | – |
| [GARA A PROCEDURA APERTA PER L'AFFIDAMENTO DI UN AC](/convenzioni/cig-8898059e90/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [R] | ordinativi e contratti attuativi delle PA | – |
| [GARA A PROCEDURA APERTA PER L'AFFIDAMENTO DI UN AC](/convenzioni/cig-8898059e90/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [R] | transato e monitoraggio per lotto e listino | – |
| [GARA A PROCEDURA APERTA PER L'AFFIDAMENTO DI UN AC](/convenzioni/cig-8898059e90/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [GARA A PROCEDURA APERTA PER L'AFFIDAMENTO DI UN AC](/convenzioni/cig-8898059e90/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [GARA A PROCEDURA APERTA PER L'AFFIDAMENTO DI UN AC](/convenzioni/cig-8898059e90/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [R] | offerta tecnica dell'aggiudicatario | – |
| [PROCEDURA APERTA PER LA FORNITURA DI SERVIZI DI TR](/convenzioni/cig-9016294130/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [PROCEDURA APERTA PER LA FORNITURA DI SERVIZI DI TR](/convenzioni/cig-9016294130/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [PROCEDURA APERTA PER LA FORNITURA DI SERVIZI DI TR](/convenzioni/cig-9016294130/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [PROCEDURA APERTA PER LA FORNITURA DI SERVIZI DI TR](/convenzioni/cig-9016294130/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN A](/convenzioni/cig-9030521daa/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN A](/convenzioni/cig-9030521daa/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN A](/convenzioni/cig-9030521daa/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN A](/convenzioni/cig-9030521daa/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN A](/convenzioni/cig-9030521daa/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN A](/convenzioni/cig-9030521daa/) | Allegato C  – Offerta economica | rimando | [V] | Offerta economica (parte dell'offerta dell'aggiudicatario) | in preparazione |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN A](/convenzioni/cig-9030521daa/) | Allegato D  – Corrispettivi e tariffe | rimando | [V] | Corrispettivi e tariffe | in preparazione |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN A](/convenzioni/cig-91881762b3/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [R] | ordinativi e contratti attuativi delle PA | – |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN A](/convenzioni/cig-91881762b3/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [R] | transato e monitoraggio per lotto e listino | – |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN A](/convenzioni/cig-91881762b3/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN A](/convenzioni/cig-91881762b3/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN A](/convenzioni/cig-91881762b3/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [R] | offerta tecnica dell'aggiudicatario | – |
| [PA PER LA STIPULA DI UNA CONVENZIONE, DELLA DURATA](/convenzioni/cig-9216207e99/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [PA PER LA STIPULA DI UNA CONVENZIONE, DELLA DURATA](/convenzioni/cig-9216207e99/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [PA PER LA STIPULA DI UNA CONVENZIONE, DELLA DURATA](/convenzioni/cig-9216207e99/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [V] | listini e appendici di prezzo | in preparazione |
| [PA PER LA STIPULA DI UNA CONVENZIONE, DELLA DURATA](/convenzioni/cig-9216207e99/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [PA PER LA STIPULA DI UNA CONVENZIONE, DELLA DURATA](/convenzioni/cig-9216207e99/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [SERVIZI E PRESTAZIONI INERENTI LA PROGETTAZIONE, S](/convenzioni/cig-94252656ba/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [SERVIZI E PRESTAZIONI INERENTI LA PROGETTAZIONE, S](/convenzioni/cig-94252656ba/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [SERVIZI E PRESTAZIONI INERENTI LA PROGETTAZIONE, S](/convenzioni/cig-94252656ba/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [V] | listini e appendici di prezzo | in preparazione |
| [SERVIZI E PRESTAZIONI INERENTI LA PROGETTAZIONE, S](/convenzioni/cig-94252656ba/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [SERVIZI E PRESTAZIONI INERENTI LA PROGETTAZIONE, S](/convenzioni/cig-94252656ba/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [ACCORDO QUADRO PER LA FORNITURA DI UNA PIATTAFORMA](/convenzioni/cig-945403654f/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [R] | ordinativi e contratti attuativi delle PA | – |
| [ACCORDO QUADRO PER LA FORNITURA DI UNA PIATTAFORMA](/convenzioni/cig-945403654f/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [R] | transato e monitoraggio per lotto e listino | – |
| [ACCORDO QUADRO PER LA FORNITURA DI UNA PIATTAFORMA](/convenzioni/cig-945403654f/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [ACCORDO QUADRO PER LA FORNITURA DI UNA PIATTAFORMA](/convenzioni/cig-945403654f/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [ACCORDO QUADRO PER LA FORNITURA DI UNA PIATTAFORMA](/convenzioni/cig-945403654f/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [R] | offerta tecnica dell'aggiudicatario | – |
| [PROCEDURA NEGOZIATA PER L’AFFIDAMENTO DEI SERVIZI ](/convenzioni/cig-9481064585/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [PROCEDURA NEGOZIATA PER L’AFFIDAMENTO DEI SERVIZI ](/convenzioni/cig-9481064585/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [PROCEDURA NEGOZIATA PER L’AFFIDAMENTO DEI SERVIZI ](/convenzioni/cig-9481064585/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [PROCEDURA NEGOZIATA PER L’AFFIDAMENTO DEI SERVIZI ](/convenzioni/cig-9481064585/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [PROCEDURA NEGOZIATA PER L’AFFIDAMENTO DEI SERVIZI ](/convenzioni/cig-9482392d69/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [PROCEDURA NEGOZIATA PER L’AFFIDAMENTO DEI SERVIZI ](/convenzioni/cig-9482392d69/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [PROCEDURA NEGOZIATA PER L’AFFIDAMENTO DEI SERVIZI ](/convenzioni/cig-9482392d69/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [PROCEDURA NEGOZIATA PER L’AFFIDAMENTO DEI SERVIZI ](/convenzioni/cig-9482392d69/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [PROCEDUTA APERTA TELEMATICA PER L'AFFIDAMENTO DEL ](/convenzioni/cig-949554539f/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [PROCEDUTA APERTA TELEMATICA PER L'AFFIDAMENTO DEL ](/convenzioni/cig-949554539f/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [PROCEDUTA APERTA TELEMATICA PER L'AFFIDAMENTO DEL ](/convenzioni/cig-949554539f/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [V] | listini e appendici di prezzo | in preparazione |
| [PROCEDUTA APERTA TELEMATICA PER L'AFFIDAMENTO DEL ](/convenzioni/cig-949554539f/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [PROCEDUTA APERTA TELEMATICA PER L'AFFIDAMENTO DEL ](/convenzioni/cig-949554539f/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [CONVENZIONE PER IL SERVIZIO DI DESKTOP OUTSOURCING](/convenzioni/cig-95643027b0/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [R] | ordinativi e contratti attuativi delle PA | – |
| [CONVENZIONE PER IL SERVIZIO DI DESKTOP OUTSOURCING](/convenzioni/cig-95643027b0/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [R] | transato e monitoraggio per lotto e listino | – |
| [CONVENZIONE PER IL SERVIZIO DI DESKTOP OUTSOURCING](/convenzioni/cig-95643027b0/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [CONVENZIONE PER IL SERVIZIO DI DESKTOP OUTSOURCING](/convenzioni/cig-95643027b0/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [CONVENZIONE PER IL SERVIZIO DI DESKTOP OUTSOURCING](/convenzioni/cig-95643027b0/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [R] | offerta tecnica dell'aggiudicatario | – |
| [PROCEDURA APERTA PER L’AFFIDAMENTO DEI SERVIZI DI ](/convenzioni/cig-9580558e8e/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [PROCEDURA APERTA PER L’AFFIDAMENTO DEI SERVIZI DI ](/convenzioni/cig-9580558e8e/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [PROCEDURA APERTA PER L’AFFIDAMENTO DEI SERVIZI DI ](/convenzioni/cig-9580558e8e/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [PROCEDURA APERTA PER L’AFFIDAMENTO DEI SERVIZI DI ](/convenzioni/cig-9580558e8e/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [PROSECUZIONE SERVIZIO DI CONSERVAZIONE A NORMA PER](/convenzioni/cig-9603457f68/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [R] | ordinativi e contratti attuativi delle PA | – |
| [PROSECUZIONE SERVIZIO DI CONSERVAZIONE A NORMA PER](/convenzioni/cig-9603457f68/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [R] | transato e monitoraggio per lotto e listino | – |
| [PROSECUZIONE SERVIZIO DI CONSERVAZIONE A NORMA PER](/convenzioni/cig-9603457f68/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [PROSECUZIONE SERVIZIO DI CONSERVAZIONE A NORMA PER](/convenzioni/cig-9603457f68/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [PROSECUZIONE SERVIZIO DI CONSERVAZIONE A NORMA PER](/convenzioni/cig-9603457f68/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [R] | offerta tecnica dell'aggiudicatario | – |
| [PROCEDURA APERTA PER L'ACQUISIZIONE DI SERVIZI DI ](/convenzioni/cig-97219284c8/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [PROCEDURA APERTA PER L'ACQUISIZIONE DI SERVIZI DI ](/convenzioni/cig-97219284c8/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [PROCEDURA APERTA PER L'ACQUISIZIONE DI SERVIZI DI ](/convenzioni/cig-97219284c8/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [PROCEDURA APERTA PER L'ACQUISIZIONE DI SERVIZI DI ](/convenzioni/cig-97219284c8/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [GARA EUROPEA A LOTTI PER L'ACQUISIZIONE, MEDIANTE ](/convenzioni/cig-9769148bf3/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [GARA EUROPEA A LOTTI PER L'ACQUISIZIONE, MEDIANTE ](/convenzioni/cig-9769148bf3/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [GARA EUROPEA A LOTTI PER L'ACQUISIZIONE, MEDIANTE ](/convenzioni/cig-9769148bf3/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [V] | listini e appendici di prezzo | in preparazione |
| [GARA EUROPEA A LOTTI PER L'ACQUISIZIONE, MEDIANTE ](/convenzioni/cig-9769148bf3/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [GARA EUROPEA A LOTTI PER L'ACQUISIZIONE, MEDIANTE ](/convenzioni/cig-9769148bf3/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [ACCORDO QUADRO PER L'AFFIDAMENTO, IN FORMA AGGREGA](/convenzioni/cig-9777818ea8/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [R] | ordinativi e contratti attuativi delle PA | – |
| [ACCORDO QUADRO PER L'AFFIDAMENTO, IN FORMA AGGREGA](/convenzioni/cig-9777818ea8/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [R] | transato e monitoraggio per lotto e listino | – |
| [ACCORDO QUADRO PER L'AFFIDAMENTO, IN FORMA AGGREGA](/convenzioni/cig-9777818ea8/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [ACCORDO QUADRO PER L'AFFIDAMENTO, IN FORMA AGGREGA](/convenzioni/cig-9777818ea8/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [ACCORDO QUADRO PER L'AFFIDAMENTO, IN FORMA AGGREGA](/convenzioni/cig-9777818ea8/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [R] | offerta tecnica dell'aggiudicatario | – |
| [PROCEDURA APERTA PER L'AFFIDAMENTO DEL SERVIZIO DI](/convenzioni/cig-9837572d38/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [PROCEDURA APERTA PER L'AFFIDAMENTO DEL SERVIZIO DI](/convenzioni/cig-9837572d38/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [PROCEDURA APERTA PER L'AFFIDAMENTO DEL SERVIZIO DI](/convenzioni/cig-9837572d38/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [V] | listini e appendici di prezzo | in preparazione |
| [PROCEDURA APERTA PER L'AFFIDAMENTO DEL SERVIZIO DI](/convenzioni/cig-9837572d38/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [PROCEDURA APERTA PER L'AFFIDAMENTO DEL SERVIZIO DI](/convenzioni/cig-9837572d38/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [APPALTO SPECIFICO (SDA) PER LA FORNITURA IN ACQUIS](/convenzioni/cig-9845010742/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [APPALTO SPECIFICO (SDA) PER LA FORNITURA IN ACQUIS](/convenzioni/cig-9845010742/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [APPALTO SPECIFICO (SDA) PER LA FORNITURA IN ACQUIS](/convenzioni/cig-9845010742/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [APPALTO SPECIFICO (SDA) PER LA FORNITURA IN ACQUIS](/convenzioni/cig-9845010742/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [ARIA_2023_807 - PROCEDURA APERTA, AI SENSI DELL’AR](/convenzioni/cig-989984280e/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [ARIA_2023_807 - PROCEDURA APERTA, AI SENSI DELL’AR](/convenzioni/cig-989984280e/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [ARIA_2023_807 - PROCEDURA APERTA, AI SENSI DELL’AR](/convenzioni/cig-989984280e/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [V] | listini e appendici di prezzo | in preparazione |
| [ARIA_2023_807 - PROCEDURA APERTA, AI SENSI DELL’AR](/convenzioni/cig-989984280e/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [ARIA_2023_807 - PROCEDURA APERTA, AI SENSI DELL’AR](/convenzioni/cig-989984280e/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [APPALTO SPECIFICO (SDA) PER L'ACQUISIZIONE DI SERV](/convenzioni/cig-9923894067/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [APPALTO SPECIFICO (SDA) PER L'ACQUISIZIONE DI SERV](/convenzioni/cig-9923894067/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [APPALTO SPECIFICO (SDA) PER L'ACQUISIZIONE DI SERV](/convenzioni/cig-9923894067/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [APPALTO SPECIFICO (SDA) PER L'ACQUISIZIONE DI SERV](/convenzioni/cig-9923894067/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [APPALTO SPECIFICO INDETTO DA INNOVAPUGLIA S.P.A. F](/convenzioni/cig-993049146a/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [APPALTO SPECIFICO INDETTO DA INNOVAPUGLIA S.P.A. F](/convenzioni/cig-993049146a/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [APPALTO SPECIFICO INDETTO DA INNOVAPUGLIA S.P.A. F](/convenzioni/cig-993049146a/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [APPALTO SPECIFICO INDETTO DA INNOVAPUGLIA S.P.A. F](/convenzioni/cig-993049146a/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [APPALTO SPECIFICO PER L’ACQUISIZIONE DEL SERVIZIO ](/convenzioni/cig-9936839af1/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [APPALTO SPECIFICO PER L’ACQUISIZIONE DEL SERVIZIO ](/convenzioni/cig-9936839af1/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [APPALTO SPECIFICO PER L’ACQUISIZIONE DEL SERVIZIO ](/convenzioni/cig-9936839af1/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [APPALTO SPECIFICO PER L’ACQUISIZIONE DEL SERVIZIO ](/convenzioni/cig-9936839af1/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [ACCORDO QUADRO, SUDDIVISO IN 9 LOTTI, CON PIÙ OPER](/convenzioni/cig-99617296d3/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [R] | ordinativi e contratti attuativi delle PA | – |
| [ACCORDO QUADRO, SUDDIVISO IN 9 LOTTI, CON PIÙ OPER](/convenzioni/cig-99617296d3/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [R] | transato e monitoraggio per lotto e listino | – |
| [ACCORDO QUADRO, SUDDIVISO IN 9 LOTTI, CON PIÙ OPER](/convenzioni/cig-99617296d3/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [ACCORDO QUADRO, SUDDIVISO IN 9 LOTTI, CON PIÙ OPER](/convenzioni/cig-99617296d3/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [ACCORDO QUADRO, SUDDIVISO IN 9 LOTTI, CON PIÙ OPER](/convenzioni/cig-99617296d3/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [R] | offerta tecnica dell'aggiudicatario | – |
| [PROCEDURA APERTA PER LA FORNITURA DI SERVIZI DI SV](/convenzioni/cig-a008db40ba/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [PROCEDURA APERTA PER LA FORNITURA DI SERVIZI DI SV](/convenzioni/cig-a008db40ba/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [PROCEDURA APERTA PER LA FORNITURA DI SERVIZI DI SV](/convenzioni/cig-a008db40ba/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [PROCEDURA APERTA PER LA FORNITURA DI SERVIZI DI SV](/convenzioni/cig-a008db40ba/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [PROCEDURA NEGOZIATA PER L'AFFIDAMENTO DI SERVIZI I](/convenzioni/cig-a0260b3155/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [R] | ordinativi e contratti attuativi delle PA | – |
| [PROCEDURA NEGOZIATA PER L'AFFIDAMENTO DI SERVIZI I](/convenzioni/cig-a0260b3155/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [R] | transato e monitoraggio per lotto e listino | – |
| [PROCEDURA NEGOZIATA PER L'AFFIDAMENTO DI SERVIZI I](/convenzioni/cig-a0260b3155/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [PROCEDURA NEGOZIATA PER L'AFFIDAMENTO DI SERVIZI I](/convenzioni/cig-a0260b3155/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [PROCEDURA NEGOZIATA PER L'AFFIDAMENTO DI SERVIZI I](/convenzioni/cig-a0260b3155/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [R] | offerta tecnica dell'aggiudicatario | – |
| [GARA EUROPEA A LOTTI PER L'ACQUISIZIONE, MEDIANTE ](/convenzioni/cig-a02b1c8a8a/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [GARA EUROPEA A LOTTI PER L'ACQUISIZIONE, MEDIANTE ](/convenzioni/cig-a02b1c8a8a/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [GARA EUROPEA A LOTTI PER L'ACQUISIZIONE, MEDIANTE ](/convenzioni/cig-a02b1c8a8a/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [V] | listini e appendici di prezzo | in preparazione |
| [GARA EUROPEA A LOTTI PER L'ACQUISIZIONE, MEDIANTE ](/convenzioni/cig-a02b1c8a8a/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [GARA EUROPEA A LOTTI PER L'ACQUISIZIONE, MEDIANTE ](/convenzioni/cig-a02b1c8a8a/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [GARA A PROCEDURA APERTA, SUDDIVISA IN 8 LOTTI, PER](/convenzioni/cig-b0da5c472c/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [R] | ordinativi e contratti attuativi delle PA | – |
| [GARA A PROCEDURA APERTA, SUDDIVISA IN 8 LOTTI, PER](/convenzioni/cig-b0da5c472c/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [R] | transato e monitoraggio per lotto e listino | – |
| [GARA A PROCEDURA APERTA, SUDDIVISA IN 8 LOTTI, PER](/convenzioni/cig-b0da5c472c/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [GARA A PROCEDURA APERTA, SUDDIVISA IN 8 LOTTI, PER](/convenzioni/cig-b0da5c472c/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [GARA A PROCEDURA APERTA, SUDDIVISA IN 8 LOTTI, PER](/convenzioni/cig-b0da5c472c/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [R] | offerta tecnica dell'aggiudicatario | – |
| [FORNITURA IN NOLEGGIO DI APPARECCHIATURE MULTIFUNZ](/convenzioni/cig-b1457d3391/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [FORNITURA IN NOLEGGIO DI APPARECCHIATURE MULTIFUNZ](/convenzioni/cig-b1457d3391/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [FORNITURA IN NOLEGGIO DI APPARECCHIATURE MULTIFUNZ](/convenzioni/cig-b1457d3391/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [FORNITURA IN NOLEGGIO DI APPARECCHIATURE MULTIFUNZ](/convenzioni/cig-b1457d3391/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [FORNITURA IN NOLEGGIO DI APPARECCHIATURE MULTIFUNZ](/convenzioni/cig-b1457d3391/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [SERVIZI INFORMATICI PER L EVOLUZIONE DEI SISTEMI I](/convenzioni/cig-b1ffb3098a/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [SERVIZI INFORMATICI PER L EVOLUZIONE DEI SISTEMI I](/convenzioni/cig-b1ffb3098a/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [SERVIZI INFORMATICI PER L EVOLUZIONE DEI SISTEMI I](/convenzioni/cig-b1ffb3098a/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [V] | listini e appendici di prezzo | in preparazione |
| [SERVIZI INFORMATICI PER L EVOLUZIONE DEI SISTEMI I](/convenzioni/cig-b1ffb3098a/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [SERVIZI INFORMATICI PER L EVOLUZIONE DEI SISTEMI I](/convenzioni/cig-b1ffb3098a/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [L'APPALTO HA AD OGGETTO L'ACQUISIZIONE DI SERVIZI ](/convenzioni/cig-b2fb115279/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [L'APPALTO HA AD OGGETTO L'ACQUISIZIONE DI SERVIZI ](/convenzioni/cig-b2fb115279/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [L'APPALTO HA AD OGGETTO L'ACQUISIZIONE DI SERVIZI ](/convenzioni/cig-b2fb115279/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [L'APPALTO HA AD OGGETTO L'ACQUISIZIONE DI SERVIZI ](/convenzioni/cig-b2fb115279/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [L'APPALTO HA AD OGGETTO L'ACQUISIZIONE DI SERVIZI ](/convenzioni/cig-b2fb115279/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [PROCEDURA NEGOZIATA SENZA BANDO AI SENSI DELL'ART.](/convenzioni/cig-b715929978/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [R] | ordinativi e contratti attuativi delle PA | – |
| [PROCEDURA NEGOZIATA SENZA BANDO AI SENSI DELL'ART.](/convenzioni/cig-b715929978/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [R] | transato e monitoraggio per lotto e listino | – |
| [PROCEDURA NEGOZIATA SENZA BANDO AI SENSI DELL'ART.](/convenzioni/cig-b715929978/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [PROCEDURA NEGOZIATA SENZA BANDO AI SENSI DELL'ART.](/convenzioni/cig-b715929978/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [PROCEDURA NEGOZIATA SENZA BANDO AI SENSI DELL'ART.](/convenzioni/cig-b715929978/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [R] | offerta tecnica dell'aggiudicatario | – |
| [PROCEDURA DI AFFIDAMENTO IN HOUSE AI SENSI DELL'AR](/convenzioni/cig-b736423c63/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [PROCEDURA DI AFFIDAMENTO IN HOUSE AI SENSI DELL'AR](/convenzioni/cig-b736423c63/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [PROCEDURA DI AFFIDAMENTO IN HOUSE AI SENSI DELL'AR](/convenzioni/cig-b736423c63/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [V] | listini e appendici di prezzo | in preparazione |
| [PROCEDURA DI AFFIDAMENTO IN HOUSE AI SENSI DELL'AR](/convenzioni/cig-b736423c63/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [PROCEDURA DI AFFIDAMENTO IN HOUSE AI SENSI DELL'AR](/convenzioni/cig-b736423c63/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [Consip SPC Cloud lotto 1, servizi di cloud computi](/convenzioni/consip-1403/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [Consip SPC Cloud lotto 1, servizi di cloud computi](/convenzioni/consip-1403/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [Consip SPC Cloud lotto 1, servizi di cloud computi](/convenzioni/consip-1403/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [Consip SPC Cloud lotto 1, servizi di cloud computi](/convenzioni/consip-1403/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [Consip SPC Cloud lotto 1, servizi di cloud computi](/convenzioni/consip-1403/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [Consip SPC Cloud lotto 1, servizi di cloud computi](/convenzioni/consip-1403/) | Progetti dei Piani dei Fabbisogni approvati | atteso | [R] | piani e progetti dei fabbisogni delle PA | – |
| [GARA PER LA FORNITURA DI SERVIZI INTEGRATI, GESTIO](/convenzioni/consip-1561/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [GARA PER LA FORNITURA DI SERVIZI INTEGRATI, GESTIO](/convenzioni/consip-1561/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [GARA PER LA FORNITURA DI SERVIZI INTEGRATI, GESTIO](/convenzioni/consip-1561/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [GARA PER LA FORNITURA DI SERVIZI INTEGRATI, GESTIO](/convenzioni/consip-1561/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [GARA A PROCEDURA APERTA SUDDIVISA IN 4 LOTTI PER L](/convenzioni/consip-1774/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [GARA A PROCEDURA APERTA SUDDIVISA IN 4 LOTTI PER L](/convenzioni/consip-1774/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [GARA A PROCEDURA APERTA SUDDIVISA IN 4 LOTTI PER L](/convenzioni/consip-1774/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [GARA A PROCEDURA APERTA SUDDIVISA IN 4 LOTTI PER L](/convenzioni/consip-1774/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [GARA A PROCEDURA APERTA SUDDIVISA IN 4 LOTTI PER L](/convenzioni/consip-1774/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [Consip AQ System management, ID 1836](/convenzioni/consip-1836/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [Consip AQ System management, ID 1836](/convenzioni/consip-1836/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [Consip AQ System management, ID 1836](/convenzioni/consip-1836/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [Consip AQ System management, ID 1836](/convenzioni/consip-1836/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [Consip AQ System management, ID 1836](/convenzioni/consip-1836/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [AQ PER I SERVIZI DI GESTIONE E MANUTENZIONE DI SIS](/convenzioni/consip-2181/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [AQ PER I SERVIZI DI GESTIONE E MANUTENZIONE DI SIS](/convenzioni/consip-2181/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [AQ PER I SERVIZI DI GESTIONE E MANUTENZIONE DI SIS](/convenzioni/consip-2181/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [AQ PER I SERVIZI DI GESTIONE E MANUTENZIONE DI SIS](/convenzioni/consip-2181/) | Allegato C all'AQ – Offerta economica del fornitore | rimando | [V] | del presente Accordo Quadro | in preparazione |
| [AQ PER I SERVIZI DI GESTIONE E MANUTENZIONE DI SIS](/convenzioni/consip-2181/) | Allegato D all'AQ – Corrispettivi e tariffe | rimando | [V] | titolo non leggibile dal rimando | in preparazione |
| [Consip Licenze Microsoft Enterprise Agreement 6, I](/convenzioni/consip-2187/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [Consip Licenze Microsoft Enterprise Agreement 6, I](/convenzioni/consip-2187/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [Consip Licenze Microsoft Enterprise Agreement 6, I](/convenzioni/consip-2187/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [GARA STRATEGICA SERVIZI APPLICATIVI IN OTTICA CLOU](/convenzioni/consip-2212/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [GARA STRATEGICA SERVIZI APPLICATIVI IN OTTICA CLOU](/convenzioni/consip-2212/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [GARA STRATEGICA SERVIZI APPLICATIVI IN OTTICA CLOU](/convenzioni/consip-2212/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [GARA STRATEGICA SERVIZI APPLICATIVI IN OTTICA CLOU](/convenzioni/consip-2212/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [GARA STRATEGICA SERVIZI APPLICATIVI IN OTTICA CLOU](/convenzioni/consip-2212/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [GARA STRATEGICA SERVIZI APPLICATIVI IN OTTICA CLOU](/convenzioni/consip-2212/) | Allegato C  – Offerta Economica | rimando | [V] | Offerta Economica (parte dell'offerta dell'aggiudicatario) | in preparazione |
| [GARA STRATEGICA SERVIZI APPLICATIVI IN OTTICA CLOU](/convenzioni/consip-2212/) | Allegato D  – Corrispettivi e tariffe | rimando | [V] | Corrispettivi e tariffe | in preparazione |
| [AQ PER LA FORNITURA DI PRODOTTI CLOUD IAAS E PAAS ](/convenzioni/consip-2213/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [AQ PER LA FORNITURA DI PRODOTTI CLOUD IAAS E PAAS ](/convenzioni/consip-2213/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [AQ PER LA FORNITURA DI PRODOTTI CLOUD IAAS E PAAS ](/convenzioni/consip-2213/) | Allegato C all'AQ – Offerta economica del fornitore | rimando | [V] | del presente Accordo Quadro | in preparazione |
| [AQ PER LA FORNITURA DI PRODOTTI CLOUD IAAS E PAAS ](/convenzioni/consip-2213/) | Allegato D all'AQ – Corrispettivi e tariffe | rimando | [V] | titolo non leggibile dal rimando | in preparazione |
| [AQ PER LA FORNITURA DI PRODOTTI CLOUD IAAS E PAAS ](/convenzioni/consip-2213/) | Appendice 4  – Supporto alla compilazione Offerta Economica Lotto 4 | rimando | [V] | Supporto alla compilazione Offerta Economica Lotto 4 (parte dell'offerta dell'aggiudicatario) | in preparazione |
| [Consip AQ System management ed. 3, ID 2275, lotto ](/convenzioni/consip-2275/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [Consip AQ System management ed. 3, ID 2275, lotto ](/convenzioni/consip-2275/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [Consip AQ System management ed. 3, ID 2275, lotto ](/convenzioni/consip-2275/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [Consip AQ System management ed. 3, ID 2275, lotto ](/convenzioni/consip-2275/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [Consip AQ System management ed. 3, ID 2275, lotto ](/convenzioni/consip-2275/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [Consip AQ System management ed. 3, ID 2275, lotto ](/convenzioni/consip-2275/) | Allegato B all'AQ (fra offerta tecnica e corrispettivi: presumibilmente offerta economica) | rimando | [V] | titolo non leggibile dal rimando | in preparazione |
| [Consip AQ System management ed. 3, ID 2275, lotto ](/convenzioni/consip-2275/) | Allegato C all'AQ – Corrispettivi e tariffe | rimando | [V] | titolo non leggibile dal rimando | in preparazione |
| [Consip AQ Servizi di sicurezza da remoto, complian](/convenzioni/consip-2296/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [Consip AQ Servizi di sicurezza da remoto, complian](/convenzioni/consip-2296/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [ACCORDO QUADRO AVENTE AD OGGETTO LA FORNITURA DI U](/convenzioni/consip-2297/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [ACCORDO QUADRO AVENTE AD OGGETTO LA FORNITURA DI U](/convenzioni/consip-2297/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [ACCORDO QUADRO AVENTE AD OGGETTO LA FORNITURA DI U](/convenzioni/consip-2297/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [ACCORDO QUADRO AVENTE AD OGGETTO LA FORNITURA DI U](/convenzioni/consip-2297/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [ACCORDO QUADRO AVENTE AD OGGETTO LA FORNITURA DI U](/convenzioni/consip-2297/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [ACCORDO QUADRO AVENTE AD OGGETTO LA FORNITURA DI U](/convenzioni/consip-2297/) | Allegato B  – Corrispettivi e tariffe | rimando | [V] | Corrispettivi e tariffe | in preparazione |
| [Consip AQ Sanità digitale, sistemi informativi san](/convenzioni/consip-2365/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [Consip AQ Sanità digitale, sistemi informativi san](/convenzioni/consip-2365/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [Consip AQ Sanità digitale, sistemi informativi san](/convenzioni/consip-2365/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [Consip AQ Sanità digitale, sistemi informativi san](/convenzioni/consip-2365/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [Consip AQ Sanità digitale, sistemi informativi san](/convenzioni/consip-2365/) | Allegato C  – Offerta economica | rimando | [V] | Offerta economica (parte dell'offerta dell'aggiudicatario) | in preparazione |
| [Consip AQ Sanità digitale, sistemi informativi san](/convenzioni/consip-2365/) | Allegato D  – Corrispettivi e tariffe | rimando | [V] | Corrispettivi e tariffe | in preparazione |
| [Consip AQ Sanità digitale, sistemi informativi ges](/convenzioni/consip-2366/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [Consip AQ Sanità digitale, sistemi informativi ges](/convenzioni/consip-2366/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [Consip AQ Sanità digitale, sistemi informativi ges](/convenzioni/consip-2366/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [Consip AQ Sanità digitale, sistemi informativi ges](/convenzioni/consip-2366/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [Consip AQ Sanità digitale, sistemi informativi ges](/convenzioni/consip-2366/) | Allegato B  – Offerta economica | rimando | [V] | Offerta economica (parte dell'offerta dell'aggiudicatario) | in preparazione |
| [Consip AQ Sanità digitale, sistemi informativi ges](/convenzioni/consip-2366/) | Allegato C  – Offerta economica | rimando | [V] | Offerta economica (parte dell'offerta dell'aggiudicatario) | in preparazione |
| [Consip AQ Sanità digitale, sistemi informativi ges](/convenzioni/consip-2366/) | Allegato D  – Corrispettivi e tariffe | rimando | [V] | Corrispettivi e tariffe | in preparazione |
| [Consip AQ PC portatili, mobile workstation e Chrom](/convenzioni/consip-2425/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [Consip AQ PC portatili, mobile workstation e Chrom](/convenzioni/consip-2425/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [Consip AQ PC portatili, mobile workstation e Chrom](/convenzioni/consip-2425/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [Consip AQ PC portatili, mobile workstation e Chrom](/convenzioni/consip-2425/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [ID 2452 GARA A PROCEDURA APERTA AI SENSI DEL D.LGS](/convenzioni/consip-2452/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [ID 2452 GARA A PROCEDURA APERTA AI SENSI DEL D.LGS](/convenzioni/consip-2452/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [ID 2452 GARA A PROCEDURA APERTA AI SENSI DEL D.LGS](/convenzioni/consip-2452/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [ID 2452 GARA A PROCEDURA APERTA AI SENSI DEL D.LGS](/convenzioni/consip-2452/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [ID 2452 GARA A PROCEDURA APERTA AI SENSI DEL D.LGS](/convenzioni/consip-2452/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [ID 2453 - GARA PUBLIC CLOUD SAAS ITSM](/convenzioni/consip-2453/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [R] | ordinativi e contratti attuativi delle PA | – |
| [ID 2453 - GARA PUBLIC CLOUD SAAS ITSM](/convenzioni/consip-2453/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [R] | transato e monitoraggio per lotto e listino | – |
| [ID 2453 - GARA PUBLIC CLOUD SAAS ITSM](/convenzioni/consip-2453/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [ID 2453 - GARA PUBLIC CLOUD SAAS ITSM](/convenzioni/consip-2453/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [ID 2453 - GARA PUBLIC CLOUD SAAS ITSM](/convenzioni/consip-2453/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [R] | offerta tecnica dell'aggiudicatario | – |
| [GARA A PROCEDURA APERTA PER L'AFFIDAMENTO DELLA FO](/convenzioni/consip-2480/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [GARA A PROCEDURA APERTA PER L'AFFIDAMENTO DELLA FO](/convenzioni/consip-2480/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [GARA A PROCEDURA APERTA PER L'AFFIDAMENTO DELLA FO](/convenzioni/consip-2480/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [GARA A PROCEDURA APERTA PER L'AFFIDAMENTO DELLA FO](/convenzioni/consip-2480/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [Consip AQ Servizi applicativi in ottica cloud e De](/convenzioni/consip-2483/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [Consip AQ Servizi applicativi in ottica cloud e De](/convenzioni/consip-2483/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [Consip AQ Servizi applicativi in ottica cloud e De](/convenzioni/consip-2483/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [Consip AQ Servizi applicativi in ottica cloud e De](/convenzioni/consip-2483/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [Consip AQ Servizi applicativi in ottica cloud e De](/convenzioni/consip-2483/) | Allegato B all'AQ – Offerta economica del fornitore | rimando | [V] | del presente Accordo Quadro e nel | in preparazione |
| [Consip AQ Servizi applicativi in ottica cloud e De](/convenzioni/consip-2483/) | Allegato C all'AQ – Corrispettivi e tariffe | rimando | [V] | titolo non leggibile dal rimando | in preparazione |
| [AQ CENTRALI TELEFONICHE 9 - ID 2496](/convenzioni/consip-2496/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [AQ CENTRALI TELEFONICHE 9 - ID 2496](/convenzioni/consip-2496/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [AQ CENTRALI TELEFONICHE 9 - ID 2496](/convenzioni/consip-2496/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [AQ CENTRALI TELEFONICHE 9 - ID 2496](/convenzioni/consip-2496/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [AQ CENTRALI TELEFONICHE 9 - ID 2496](/convenzioni/consip-2496/) | Allegato B all'AQ – Offerta economica del fornitore | rimando | [V] | titolo non leggibile dal rimando | in preparazione |
| [Consip Digital transformation 2, ID 2536, lotto 2 ](/convenzioni/consip-2536/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [Consip Digital transformation 2, ID 2536, lotto 2 ](/convenzioni/consip-2536/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [Consip Digital transformation 2, ID 2536, lotto 2 ](/convenzioni/consip-2536/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [Consip Digital transformation 2, ID 2536, lotto 2 ](/convenzioni/consip-2536/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [Consip Digital transformation 2, ID 2536, lotto 2 ](/convenzioni/consip-2536/) | Allegato C all'AQ – Offerta economica del fornitore | rimando | [V] | del presente Accordo Quadro | in preparazione |
| [SERVIZI DI POSTA ELETTRONICA CERTIFICATA (PEC) 2 -](/convenzioni/consip-2556/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [R] | ordinativi e contratti attuativi delle PA | – |
| [SERVIZI DI POSTA ELETTRONICA CERTIFICATA (PEC) 2 -](/convenzioni/consip-2556/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [R] | transato e monitoraggio per lotto e listino | – |
| [SERVIZI DI POSTA ELETTRONICA CERTIFICATA (PEC) 2 -](/convenzioni/consip-2556/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [SERVIZI DI POSTA ELETTRONICA CERTIFICATA (PEC) 2 -](/convenzioni/consip-2556/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [SERVIZI DI POSTA ELETTRONICA CERTIFICATA (PEC) 2 -](/convenzioni/consip-2556/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [R] | offerta tecnica dell'aggiudicatario | – |
| [SERVIZI DI DATA MANAGEMENT PER LA PUBBLICA AMMINIS](/convenzioni/consip-2566/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [SERVIZI DI DATA MANAGEMENT PER LA PUBBLICA AMMINIS](/convenzioni/consip-2566/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [SERVIZI DI DATA MANAGEMENT PER LA PUBBLICA AMMINIS](/convenzioni/consip-2566/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [SERVIZI DI DATA MANAGEMENT PER LA PUBBLICA AMMINIS](/convenzioni/consip-2566/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [SERVIZI DI DATA MANAGEMENT PER LA PUBBLICA AMMINIS](/convenzioni/consip-2566/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [SERVIZI DI DATA MANAGEMENT PER LA PUBBLICA AMMINIS](/convenzioni/consip-2566/) | Allegato B all'AQ – Offerta economica del fornitore | rimando | [V] | del presente Accordo Quadro e nel | in preparazione |
| [SERVIZI DI DATA MANAGEMENT PER LA PUBBLICA AMMINIS](/convenzioni/consip-2566/) | Allegato C  – Corrispettivi e tariffe | rimando | [V] | Corrispettivi e tariffe | in preparazione |
| [Consip Licenze software multibrand 6, ID 2599, lot](/convenzioni/consip-2599/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [Consip Licenze software multibrand 6, ID 2599, lot](/convenzioni/consip-2599/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [Consip Licenze software multibrand 6, ID 2599, lot](/convenzioni/consip-2599/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [Consip Sanità digitale, sistemi clinico assistenzi](/convenzioni/consip-2601/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [Consip Sanità digitale, sistemi clinico assistenzi](/convenzioni/consip-2601/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [Consip Sanità digitale, sistemi clinico assistenzi](/convenzioni/consip-2601/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [Consip Sanità digitale, sistemi clinico assistenzi](/convenzioni/consip-2601/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [Consip Sanità digitale, sistemi clinico assistenzi](/convenzioni/consip-2601/) | Allegato C  – Offerta economica | rimando | [V] | Offerta economica (parte dell'offerta dell'aggiudicatario) | in preparazione |
| [Consip Servizi applicativi in ottica cloud 3 (PAL)](/convenzioni/consip-2610/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [Consip Servizi applicativi in ottica cloud 3 (PAL)](/convenzioni/consip-2610/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [Consip Servizi applicativi in ottica cloud 3 (PAL)](/convenzioni/consip-2610/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [Consip Servizi applicativi in ottica cloud 3 (PAL)](/convenzioni/consip-2610/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [Consip Licenze Microsoft Enterprise Agreement 8, I](/convenzioni/consip-2615/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [Consip Licenze Microsoft Enterprise Agreement 8, I](/convenzioni/consip-2615/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [Consip Licenze Microsoft Enterprise Agreement 8, I](/convenzioni/consip-2615/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [Consip Licenze Microsoft Enterprise Agreement 8, I](/convenzioni/consip-2615/) | Appendice 4 al/allo capitolato – Listino Microsoft EA per l’Utente Finale | rimando | [V] | Listino Microsoft EA per l’Utente Finale | in preparazione |
| [Consip Licenze Microsoft Enterprise Agreement 8, I](/convenzioni/consip-2615/) | Appendice 4.1  | rimando | [V] | titolo non leggibile dal rimando | in preparazione |
| [Consip PC desktop e workstation 3, ID 2631, lotto ](/convenzioni/consip-2631/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [Consip PC desktop e workstation 3, ID 2631, lotto ](/convenzioni/consip-2631/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [Consip PC desktop e workstation 3, ID 2631, lotto ](/convenzioni/consip-2631/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [Consip PC desktop e workstation 3, ID 2631, lotto ](/convenzioni/consip-2631/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [ENERGIA ELETTRICA 21 - ID 2638 | LOMBARDIA ESCLUSE](/convenzioni/consip-2638/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [ENERGIA ELETTRICA 21 - ID 2638 | LOMBARDIA ESCLUSE](/convenzioni/consip-2638/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [ENERGIA ELETTRICA 21 - ID 2638 | LOMBARDIA ESCLUSE](/convenzioni/consip-2638/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [ENERGIA ELETTRICA 21 - ID 2638 | LOMBARDIA ESCLUSE](/convenzioni/consip-2638/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [AQ SERVIZI DI GESTIONE E MANUTENZIONE DI SISTEMI I](/convenzioni/consip-2648/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [AQ SERVIZI DI GESTIONE E MANUTENZIONE DI SISTEMI I](/convenzioni/consip-2648/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [AQ SERVIZI DI GESTIONE E MANUTENZIONE DI SISTEMI I](/convenzioni/consip-2648/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [AQ SERVIZI DI GESTIONE E MANUTENZIONE DI SISTEMI I](/convenzioni/consip-2648/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [AQ SERVIZI DI GESTIONE E MANUTENZIONE DI SISTEMI I](/convenzioni/consip-2648/) | Allegato C – Corrispettivi e tariffe | rimando | [V] | titolo non leggibile dal rimando | in preparazione |
| [CLOUD ENABLING 1 ID 2652 | LOTTO 1: SERVIZI SUPPOR](/convenzioni/consip-2652/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [CLOUD ENABLING 1 ID 2652 | LOTTO 1: SERVIZI SUPPOR](/convenzioni/consip-2652/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [CLOUD ENABLING 1 ID 2652 | LOTTO 1: SERVIZI SUPPOR](/convenzioni/consip-2652/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [CLOUD ENABLING 1 ID 2652 | LOTTO 1: SERVIZI SUPPOR](/convenzioni/consip-2652/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [CLOUD ENABLING 1 ID 2652 | LOTTO 1: SERVIZI SUPPOR](/convenzioni/consip-2652/) | Allegato C – Offerta economica | rimando | [V] | Offerta (parte dell'offerta dell'aggiudicatario) | in preparazione |
| [PRODOTTI CLOUD IN MODALITÀ SOFTWARE AS A SERVICE N](/convenzioni/consip-2700/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [PRODOTTI CLOUD IN MODALITÀ SOFTWARE AS A SERVICE N](/convenzioni/consip-2700/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [PRODOTTI CLOUD IN MODALITÀ SOFTWARE AS A SERVICE N](/convenzioni/consip-2700/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [PRODOTTI CLOUD IN MODALITÀ SOFTWARE AS A SERVICE N](/convenzioni/consip-2700/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [Consip AQ System management ed. 4, ID 2710 (lotto ](/convenzioni/consip-2710/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [Consip AQ System management ed. 4, ID 2710 (lotto ](/convenzioni/consip-2710/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [Consip AQ System management ed. 4, ID 2710 (lotto ](/convenzioni/consip-2710/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [Consip AQ System management ed. 4, ID 2710 (lotto ](/convenzioni/consip-2710/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [GARA A PROCEDURA APERTA PER L’APPALTO DI FORNITURA](/convenzioni/consip-2738/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [GARA A PROCEDURA APERTA PER L’APPALTO DI FORNITURA](/convenzioni/consip-2738/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [GARA A PROCEDURA APERTA PER L’APPALTO DI FORNITURA](/convenzioni/consip-2738/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [FORNITURA DI SERVIZI CLOUD IAAS E PAAS | FORNITURA](/convenzioni/consip-2746/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [FORNITURA DI SERVIZI CLOUD IAAS E PAAS | FORNITURA](/convenzioni/consip-2746/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [FORNITURA DI SERVIZI CLOUD IAAS E PAAS | FORNITURA](/convenzioni/consip-2746/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [FORNITURA DI SERVIZI CLOUD IAAS E PAAS | FORNITURA](/convenzioni/consip-2746/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [FORNITURA DI SERVIZI CLOUD IAAS E PAAS | FORNITURA](/convenzioni/consip-2746/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [FORNITURA DI SERVIZI CLOUD IAAS E PAAS | FORNITURA](/convenzioni/consip-2746/) | Allegato A all'AQ – Offerta economica del fornitore | rimando | [V] | del presente | in preparazione |
| [Consip Licenze Microsoft Enterprise Agreement 9, I](/convenzioni/consip-2755/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [Consip Licenze Microsoft Enterprise Agreement 9, I](/convenzioni/consip-2755/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [Consip Licenze Microsoft Enterprise Agreement 9, I](/convenzioni/consip-2755/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [ACQUISIZIONE DI PC DESKTOP, WORKSTATION E MONITOR ](/convenzioni/consip-2781/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [ACQUISIZIONE DI PC DESKTOP, WORKSTATION E MONITOR ](/convenzioni/consip-2781/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [ACQUISIZIONE DI PC DESKTOP, WORKSTATION E MONITOR ](/convenzioni/consip-2781/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [ACQUISIZIONE DI PC DESKTOP, WORKSTATION E MONITOR ](/convenzioni/consip-2781/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [ACQUISIZIONE DI PC DESKTOP, WORKSTATION E MONITOR ](/convenzioni/consip-2781/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [Consip PRINCO, Public cloud SaaS produttività indi](/convenzioni/consip-2928/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [Consip PRINCO, Public cloud SaaS produttività indi](/convenzioni/consip-2928/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [V] | transato e monitoraggio per lotto e listino | in preparazione |
| [Consip PRINCO, Public cloud SaaS produttività indi](/convenzioni/consip-2928/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [V] | offerta economica e listino offerto | in preparazione |
| [Consip PRINCO, Public cloud SaaS produttività indi](/convenzioni/consip-2928/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [Consip PRINCO, Public cloud SaaS produttività indi](/convenzioni/consip-2928/) | Allegato 12 compilato dall'aggiudicatario del listino Open Source (Converge): elenco dei prodotti offerti | rimando | [V] | Foglio xlsx compilato con i prodotti SaaS open source offerti per il listino 3 (nomi, produttori, prezzi): parte dell'of | in preparazione |
| [Consip Reti locali 8, ID 2223, lotto 2 PAL](/convenzioni/consip-reti-locali-8/) | Elenco degli ordinativi e contratti attuativi delle PA | atteso | [V] | ordinativi e contratti attuativi delle PA | in preparazione |
| [Consip Reti locali 8, ID 2223, lotto 2 PAL](/convenzioni/consip-reti-locali-8/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [Consip Reti locali 8, ID 2223, lotto 2 PAL](/convenzioni/consip-reti-locali-8/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [Consip Reti locali 8, ID 2223, lotto 2 PAL](/convenzioni/consip-reti-locali-8/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [V] | offerta tecnica dell'aggiudicatario | in preparazione |
| [Polo Strategico Nazionale (PPP, Presidenza del Con](/convenzioni/psn/) | Flussi di monitoraggio: transato/erogato per lotto, listino e marchio | atteso | [R] | transato e monitoraggio per lotto e listino | – |
| [Polo Strategico Nazionale (PPP, Presidenza del Con](/convenzioni/psn/) | Listini prezzi applicati alle amministrazioni (per lotto e listino) | atteso | [R] | listini e appendici di prezzo | – |
| [Polo Strategico Nazionale (PPP, Presidenza del Con](/convenzioni/psn/) | Offerta economica e listino offerto dall'aggiudicatario (per lotto) | atteso | [R] | offerta economica e listino offerto | – |
| [Polo Strategico Nazionale (PPP, Presidenza del Con](/convenzioni/psn/) | Offerta tecnica dell'aggiudicatario (per lotto) | atteso | [R] | offerta tecnica dell'aggiudicatario | – |

Le criticità si assegnano per regole sul titolo: classificazione automatica, da rivedere prima di ogni richiesta. I «rimandi» a lettere (Allegato A, B…) e i titoli troncati vengono dal testo estratto dei PDF e vanno letti nel contesto (colonna evidenza del CSV).

## 6. Per tipo di soggetto

Fonti consultate il 05/11/2026.

| Soggetto | Iniziative | M€ 2024-25 | Indice medio | Non individuati | Non verificati |
|---|---|---|---|---|---|
| Consip | 45 | 51.555 | 56 % | 87 | 157 |
| PSN | 1 | 2.078 | n.d. (non ancora verificati) | 0 | 9 |
| Aggregatori regionali | 25 | 488 | n.d. (non ancora verificati) | 0 | 261 |
| Consorzi e unioni | 4 | 67 | n.d. (non ancora verificati) | 0 | 48 |
| Altri | 11 | 610 | n.d. (non ancora verificati) | 6 | 117 |

Per aggregatori regionali e consorzi molti dati sono «da verificare»: le parti pubbliche delle piattaforme (Sintel/NECA, Intercent-ER, EmPULIA, START) sono state visitate per 8 delle 25 iniziative degli aggregatori (5-6/11/2026), le altre restano da fare; i CIG padre non hanno link ai documenti in PVL (verificato: nessuno dei 295 CIG padre) e su TED l'abbinamento riesce solo per testo. **Un indice basso qui misura il nostro lavoro ancora da fare, non la loro trasparenza.**

## 7. Metodo e limiti

- **Fonti.** BDNCP ANAC (nostro mirror, sha256 nel manifest) per i CIG padre e derivati; pagine dei bandi su consip.it, consultate il 5/11/2026; acquistinretepa e piattaforme degli aggregatori, 5-6/11/2026; TED; open data Consip degli ordini (dati.consip.it, file 2024-2026 archiviati il 5/11/2026); atti di enti aderenti trovati con ricerca online (fonte non ufficiale, archiviati con sha256).
- **Verificato e riferito.** «Assente» vuol dire che abbiamo consultato la pagina ufficiale dell'iniziativa e il documento non c'è; il tipo di documento si deduce dal nome del file (controllo a mano solo per PRINCO). Le norme e i dati che non abbiamo letto sulla fonte sono marcati [R] nelle schede ([carenze.yaml](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/database/carenze.yaml)).
- **Valori.** Somme di importi dichiarati in BDNCP: ordine di grandezza, non spesa né transato (seconda misura al § 2). La prima iniziativa per valore pesa 29.918 M€ (55 % del totale).
- **Archivio.** 2.041 documenti ufficiali collegati alle iniziative (compresi i file dentro gli zip), archiviati con sha256; una cella «pubblico» può contenerne molti.
- **PVL.** Nessuno dei 295 CIG padre ha un link ai documenti di gara nei dati PVL scaricati il 3-4/11/2026 (verificato): è lo stato dei dati PVL, non un'assenza dei documenti, che gli aggregatori pubblicano sulle proprie piattaforme.
- **Rumore nel censimento.** Il filtro per CPV ICT sui derivati lascia passare iniziative non ICT (es. ID 2638 Energia elettrica 21, 30 M€): restano in elenco finché il filtro non viene corretto, con peso trascurabile sul totale.
- **Lettura dei documenti.** Letti per intero: atti di PRINCO (ID 2928), allegati sui flussi dati degli ID 2615, ID 2275, ID 2452 e ID 2648, alcune determine di enti; per le altre iniziative le schede mostrano estratti automatici per parole chiave, marcati «da leggere».
- **Aggregatori.** Parti pubbliche visitate per 8 iniziative; le altre da verificare (sopra). Il tipo di soggetto si assegna con regole sul nome della stazione appaltante, da controvalidare con l'elenco ANAC dei soggetti aggregatori.
- **Cosa non diciamo.** Che un dato assente sia nascosto di proposito; che un dato reperito presso un ente valga per tutta la convenzione.

## 8. Rimedi

- **Accesso civico generalizzato** (art. 5 c. 2 d.lgs. 33/2013), come rimedio di breve periodo e solo dopo le fonti del § 3: 30 bozze necessarie (carenza accertata e dato utile all'imbuto: prodotti e marchi delle iniziative cloud e multibrand, ordinativi delle più grandi, region e data center, erosione), 114 ritirate, 1 inviate. [Registro](/convenzioni/accesso-civico/) e [analisi dei dinieghi](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/accesso-civico/analisi-dinieghi.md).
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
| 0.9 | 2026-11-06 | bozza: Allegato 6 WebRT18 archiviato; 2 pagine Azienda Zero trovate (25 documenti); dietro_login verificato da anonimo su 25 schede acquistinretepa e 2 pagine Azienda Zero (ignoto 308 → 234) | documenti mancanti per file: 782 (criticità 3: 415), prima 788; istanze preparate: da 29 a 30; istanze inviate: da 0 a 1 |
| 0.8 | 2026-11-07 | bozza non pubblica: zip del giro 7/11 letti (listini Intercent-ER con prezzi offerti e marchi), copie START/Sintel portate in archivio, ricerca fuori piattaforma (5 parziali, 411 non trovati) e visita delle sezioni AT di 60 enti aderenti (nessun documento di criticità 3; 12 blocchi) | documenti mancanti per file: 788 (criticità 3: 415), prima 797 |
| 0.7 | 2026-11-06 | bozza non pubblica: revisione a mano delle righe rimando/numerazione (89 scartate con motivazione, criticità corrette), offerte e corrispettivi trovati dentro gli AQ firmati dell'ID 2296, ricognizione dal vivo di 31 iniziative di aggregatori e altri soggetti, 36 allegati flussi letti per intero, instradamento proposto delle istanze per le gare su delega | documenti mancanti per file: 797 (criticità 3: 415), prima 886; istanze preparate: da 20 a 29 |
| 0.6 | 2026-11-06 | bozza: inventario per file dei documenti mancanti (numerazione, rimandi, attesi), criticità 1-3, ricontrollo dal vivo delle pagine Consip, Allegato 12 della 2.928 chiarito, bozza di accesso civico raggruppata per Consip; non è una release pubblica | documenti mancanti per file: 886 (criticità 3: 431) (nuovo inventario); istanze preparate: da 19 a 20 |
| 0.5 | 2026-11-06 | allegati di monitoraggio dell'ID 2452 e dell'ID 2648 letti per intero (ID 2452: flusso Erogato come l'ID 2275; ID 2648: solo commissioni); flussi di monitoraggio scritti come obbligo contrattuale con allegato e versione; revisione avversariale (10 punti) | nessuna variazione nei dati |
| 0.4 | 2026-11-06 | massimale residuo riprovato con attesa esplicita e browser visibile (sempre vuoto per utente anonimo), allegato di monitoraggio dell'ID 2275 letto per intero (Erogato mensile per ordine, lotto, sede, prodotto), parti pubbliche delle piattaforme degli aggregatori (8 iniziative) | cig-989984280E: documenti ufficiali da 0 a 7; cig-A008DB40BA: documenti ufficiali da 0 a 20; cig-97219284C8: documenti ufficiali da 0 a 43; cig-993049146A: documenti ufficiali da 0 a 13; cig-84163618CE: documenti ufficiali da 0 a 1; cig-81636687F2: documenti ufficiali da 0 a 10; cig-8637686BF8: documenti ufficiali da 0 a 3; cig-9845010742: documenti ufficiali da 0 a 18 |
| 0.3 | 2026-11-06 | acquistinretepa con browser reale (vetrina e schede pubbliche, documenti archiviati, sezione massimale residuo vuota alla consultazione), 36 allegati flussi dati analizzati, consumato per convenzione fonte per fonte, open data Consip 2026, siti AT in browser, elenco dei blocchi di accesso; revisione avversariale (10 punti) | consip-2483: documenti ufficiali da 56 a 66; consip-2610: documenti ufficiali da 51 a 53; consip-2615: documenti ufficiali da 33 a 37; consip-2425: documenti ufficiali da 59 a 67; consip-2536: documenti ufficiali da 26 a 32; consip-2599: documenti ufficiali da 97 a 99; consip-2366: documenti ufficiali da 77 a 85; consip-2738: documenti ufficiali da 99 a 101; consip-2755: documenti ufficiali da 35 a 37; consip-2601: documenti ufficiali da 53 a 57; consip-reti-locali-8: documenti ufficiali da 7 a 9; consip-2631: documenti ufficiali da 28 a 30; consip-2648: documenti ufficiali da 45 a 51; consip- |
| 0.2 | 2026-11-05 | fonti online consultate prima dell'accesso civico (acquistinretepa in parte, AT di Consip, campione di enti, ricerca web), allegato flussi dati di EA8 letto, abbinamenti open data confermati per testo, istanze ridotte con motivo per istanza, revisione avversariale (12 punti) | consip-2483: documenti da fonte non ufficiale da 0 a 7; consip-2610: documenti da fonte non ufficiale da 0 a 3; consip-2615: documenti da fonte non ufficiale da 1 a 4; psn: documenti da fonte non ufficiale da 0 a 4; consip-2425: documenti da fonte non ufficiale da 0 a 4; consip-2296: documenti da fonte non ufficiale da 0 a 3; consip-2536: documenti da fonte non ufficiale da 0 a 3; consip-2599: documenti da fonte non ufficiale da 0 a 2; consip-2366: documenti da fonte non ufficiale da 0 a 2; consip-2275: documenti da fonte non ufficiale da 0 a 3; istanze preparate: da 127 a 19 |
| 0.1 | 2026-11-05 | prima versione (bozza dopo revisione avversariale): 86 iniziative, documenti Consip archiviati, open data Consip degli ordini | prima versione |
