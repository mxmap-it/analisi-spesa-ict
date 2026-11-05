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

- **Perimetro.** 86 iniziative ICT (82 attive): Consip, PSN, soggetti aggregatori regionali, consorzi e altre stazioni appaltanti con più contratti derivati. Criterio nel [README della base dati](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/database/README.md).
- **Valore.** I contratti derivati con CPV ICT pubblicati nel 2024-2025 dichiarano in BDNCP circa **54.798 M€**. È un ordine di grandezza, non la spesa: alcuni attuativi riportano il massimale dell'accordo quadro invece del valore del contratto.
- **Visibilità.** Dei 1120 dati attesi (iniziativa × tipo di documento o dato), sono pubblici dalla fonte ufficiale 382 (34 %); reperibili solo altrove 3; assenti (verificato) 141 (13 %); ancora da verificare 594 (53 %). Indice di visibilità medio: **34 %**.
- **Valore non ben visibile.** 0 iniziative su 86 pubblicano tutti e quattro i dati che servono a controllare spesa e sovranità (offerte tecnica ed economica, transato, ordinativi) nella fonte ufficiale dell'iniziativa. Il valore delle altre è circa **54.798 M€**, cioè 100 % del totale; per 594 dati la verifica non è ancora fatta, quindi è un limite superiore provvisorio.
- **Concentrazione.** La prima iniziativa per valore (Consip AQ Servizi applicativi in ottica cloud e Demand/PMO PA centrali, seconda ) pesa 29.918 M€, 55 % del totale: il dato è dominato da pochi accordi quadro e da importi che sono massimali.
- **Carenze principali.** Offerte dei vincitori, listini offerti, transato per lotto e marchio, elenco degli ordinativi: non pubblicati dalla centrale su nessuna delle pagine Consip consultate (gli ordinativi si trovano, in parte, negli atti dei singoli enti aderenti). Region e data center: dichiarati in gara (verificato per IaaS/PaaS 2 e PRINCO), non pubblicati.
- **Il dato esiste.** Per 36 iniziative la documentazione di gara prevede che il fornitore trasmetta a Consip i flussi del fatturato (d.m. MEF 23/11/2012, commissioni): il transato è quindi presso Consip, ma non è pubblicato per lotto né per marchio.
- **Rimedi.** 127 bozze di accesso civico generalizzato preparate e **non inviate**; proposte di policy R08 e R37-R42 perché questi dati diventino pubblici senza bisogno di chiederli.

## 2. Due misure del valore

Per 20 iniziative Consip il valore si può misurare anche con gli **open data Consip** degli ordini diretti (dati.consip.it, 2024 e 2025, file archiviati con sha256): **6.349 M€** ordinati, contro **47.410 M€** dichiarati in BDNCP per i loro CIG derivati ICT 2024-2025. Le due misure non sono la stessa grandezza: gli open data contano solo gli ordini diretti (non gli appalti specifici con rilancio competitivo) e l'anno dell'ordine, BDNCP l'importo dichiarato all'acquisizione del CIG (spesso il massimale). La distanza conferma che la somma BDNCP va letta come ordine di grandezza; per l'ID 2483 il rapporto è di circa 13 a 1. Gli open data non riportano listino, marchio né ente: la carenza C3 resta.

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
| [ENERGIA ELETTRICA 21 - ID 2638 | LOMBARDIA ESCLUSE LA PROVIN](/convenzioni/consip-2638/) | 30 | 0 | nome nell'oggetto del CIG padre (V) |
| [AQ CENTRALI TELEFONICHE 9 - ID 2496 | AQ CENTRALI TELEFONICH](/convenzioni/consip-2496/) | 19 | 102 | nome nell'oggetto del CIG padre (V) |

## 3. Matrice

La [griglia di tutte le iniziative](/convenzioni/griglia/) mostra cella per cella cosa è pubblico, cosa è reperito altrove, cosa manca e cosa è stato richiesto, con i riepiloghi in alto. L'[indice delle convenzioni](/convenzioni/) riporta il riquadro delle carenze di trasparenza.

| Classe | Celle | Quota |
|---|---|---|
| pubblico (fonte ufficiale) | 382 | 34 % |
| solo da fonte non ufficiale | 3 | 0 % |
| assente (verificato) | 141 | 13 % |
| da verificare | 594 | 53 % |

## 4. Convenzione per convenzione

Le iniziative principali (attive, per valore). Indice = dati pubblici / dati attesi; «ben visibile» = offerte, transato e ordinativi tutti pubblici.

| Iniziativa | Soggetto | M€ 2024-25 | Pubblici | Altrove | Assenti | Da verificare | Indice | Ben visibile | Carenze verificate |
|---|---|---|---|---|---|---|---|---|---|
| [Consip AQ Servizi applicativi in ottica cloud e Demand/PMO PA centrali](/convenzioni/consip-2483/) | Consip | 29.918 | 9 | 0 | 3 | 1 | 69 % | no | C1, C2, C3, C4 |
| [Consip Servizi applicativi in ottica cloud 3 (PAL), ID 2610](/convenzioni/consip-2610/) | Consip | 5.953 | 9 | 0 | 3 | 1 | 69 % | no | C1, C2, C3, C4 |
| [Consip Licenze Microsoft Enterprise Agreement 8, ID 2615](/convenzioni/consip-2615/) | Consip | 3.015 | 10 | 1 | 2 | 0 | 77 % | no | C1, C2, C3, C4 |
| [Polo Strategico Nazionale (PPP, Presidenza del Consiglio)](/convenzioni/psn/) | PSN | 2.078 | 5 | 0 | 0 | 9 | 36 % | no | – |
| [Consip AQ PC portatili, mobile workstation e Chromebook, ID 2425, lott](/convenzioni/consip-2425/) | Consip | 1.617 | 9 | 0 | 3 | 1 | 69 % | no | C1, C2, C3, C4 |
| [Consip AQ Servizi di sicurezza da remoto, compliance e controllo, ID 2](/convenzioni/consip-2296/) | Consip | 1.325 | 8 | 0 | 4 | 1 | 62 % | no | C1, C2, C3, C4 |
| [Consip Digital transformation 2, ID 2536, lotto 2 digitalizzazione dei](/convenzioni/consip-2536/) | Consip | 970 | 9 | 0 | 3 | 1 | 69 % | no | C1, C2, C3, C4 |
| [Consip Licenze software multibrand 6, ID 2599, lotto 1 prodotti Oracle](/convenzioni/consip-2599/) | Consip | 918 | 10 | 0 | 3 | 0 | 77 % | no | C1, C2, C3, C4 |
| [Consip AQ Sanità digitale, sistemi informativi gestionali](/convenzioni/consip-2366/) | Consip | 834 | 8 | 0 | 3 | 2 | 62 % | no | C1, C2, C3, C4 |
| [Consip AQ System management ed. 3, ID 2275, lotto 1](/convenzioni/consip-2275/) | Consip | 747 | 8 | 0 | 4 | 1 | 62 % | no | C1, C2, C3, C4 |
| [GARA A PROCEDURA APERTA PER L?APPALTO DI FORNITURA MULTIBRAND DI PRODO](/convenzioni/consip-2738/) | Consip | 697 | 10 | 0 | 3 | 0 | 77 % | no | C1, C2, C3, C4 |
| [Consip Licenze Microsoft Enterprise Agreement 9, ID 2755 (ipotesi fort](/convenzioni/consip-2755/) | Consip | 692 | 10 | 1 | 2 | 0 | 77 % | no | C1, C2, C3, C4 |
| [Consip Sanità digitale, sistemi clinico assistenziali 2, ID 2601, lott](/convenzioni/consip-2601/) | Consip | 558 | 9 | 0 | 3 | 1 | 69 % | no | C1, C2, C3, C4 |
| [Consip Reti locali 8, ID 2223, lotto 2 PAL](/convenzioni/consip-reti-locali-8/) | Consip | 554 | 4 | 0 | 3 | 6 | 31 % | no | C1, C2, C3, C4 |
| [Consip PC desktop e workstation 3, ID 2631, lotto 2](/convenzioni/consip-2631/) | Consip | 469 | 9 | 0 | 3 | 1 | 69 % | no | C1, C2, C3, C4 |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN ACCORDO QUADRO, AI SE](/convenzioni/cig-91881762b3/) | Consip | 354 | 1 | 0 | 0 | 12 | 8 % | no | C8 |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN ACCORDO QUADRO, AI SE](/convenzioni/cig-8765571a03/) | Consip | 325 | 7 | 0 | 4 | 2 | 54 % | no | C1, C2, C3, C4 |
| [AQ SERVIZI DI GESTIONE E MANUTENZIONE DI SISTEMI IP E POSTAZIONE DI LA](/convenzioni/consip-2648/) | Consip | 308 | 9 | 0 | 3 | 1 | 69 % | no | C1, C2, C3, C4 |
| [Consip AQ Sanità digitale, sistemi informativi sanitari e servizi al c](/convenzioni/consip-2365/) | Consip | 297 | 9 | 0 | 3 | 1 | 69 % | no | C1, C2, C3, C4 |
| [Consip SPC2 Connettività (contratto quadro OPA)](/convenzioni/cig-5133642f61/) | Consip | 258 | 2 | 0 | 0 | 11 | 15 % | no | C8 |
| [AQ PER I SERVIZI DI GESTIONE E MANUTENZIONE DI SISTEMI IP E POSTAZIONI](/convenzioni/consip-2181/) | Consip | 232 | 9 | 0 | 3 | 1 | 69 % | no | C1, C2, C3, C4 |
| [GARA A PROCEDURA APERTA PER LA CONCLUSIONE DI UN ACCORDO QUADRO, AI SE](/convenzioni/cig-9030521daa/) | Consip | 227 | 7 | 0 | 4 | 2 | 54 % | no | C1, C2, C3, C4 |
| [GARA A PROCEDURA APERTA PER L'AFFIDAMENTO DI UN ACCORDO QUADRO AI SENS](/convenzioni/cig-8898059e90/) | Consip | 225 | 1 | 0 | 0 | 12 | 8 % | no | C8 |
| [CLOUD ENABLING 1 ID 2652 | LOTTO 1: SERVIZI SUPPORTO ALL'ADOZIONE E PM](/convenzioni/consip-2652/) | Consip | 190 | 9 | 0 | 3 | 1 | 69 % | no | C1, C2, C3, C4 |
| [ARIA_2023_807 - PROCEDURA APERTA, AI SENSI DELL’ART. 60 DEL D.LGS. N. ](/convenzioni/cig-989984280e/) | Aggregatori regionali | 160 | 1 | 0 | 0 | 12 | 8 % | no | – |
| [GARA A PROCEDURA APERTA SUDDIVISA IN 4 LOTTI PER L'AFFIDAMENTO DEI SER](/convenzioni/consip-1774/) | Altri | 147 | 4 | 0 | 4 | 5 | 31 % | no | C1, C2, C4 |
| [Consip AQ System management ed. 4, ID 2710 (lotto unico)](/convenzioni/consip-2710/) | Consip | 145 | 8 | 0 | 4 | 1 | 62 % | no | C1, C2, C3, C4 |
| [GARA A PROCEDURA APERTA, SUDDIVISA IN 8 LOTTI, PER LA STIPULA DI UNA C](/convenzioni/cig-b0da5c472c/) | Consip | 114 | 1 | 0 | 0 | 12 | 8 % | no | C8 |
| [PROCEDURA NEGOZIATA PER L'AFFIDAMENTO DI SERVIZI IN OUTSOURCING DI CUS](/convenzioni/cig-a0260b3155/) | Altri | 100 | 1 | 0 | 0 | 12 | 8 % | no | – |
| [AQ PER LA FORNITURA DI PRODOTTI CLOUD IAAS E PAAS - ID 2213 | LOTTO 8 ](/convenzioni/consip-2213/) | Consip | 90 | 9 | 0 | 3 | 1 | 69 % | no | C1, C2, C3, C4 |

Le altre 56 iniziative sono nell'[indice](/convenzioni/) e nella [griglia](/convenzioni/griglia/).

## 5. Per tipo di soggetto

| Soggetto | Iniziative | M€ 2024-25 | Indice medio | Ben visibili | Dati assenti | Dati da verificare |
|---|---|---|---|---|---|---|
| Consip | 45 | 51.555 | 56 % | 0 | 133 | 122 |
| PSN | 1 | 2.078 | 36 % | 0 | 0 | 9 |
| Aggregatori regionali | 25 | 488 | 8 % | 0 | 0 | 300 |
| Consorzi e unioni | 4 | 67 | 8 % | 0 | 0 | 48 |
| Altri | 11 | 610 | 14 % | 0 | 8 | 115 |

Per aggregatori regionali e consorzi quasi tutti i dati sono «da verificare»: le loro piattaforme (Sintel, Intercent-ER, EmPULIA, START…) non sono ancora state visitate, i CIG padre non hanno link ai documenti in PVL (verificato: nessuno dei 295 CIG padre) e su TED l'abbinamento riesce solo per testo. **Un indice basso qui misura il nostro lavoro ancora da fare, non la loro trasparenza.**

## 6. Metodo e limiti

- **Fonti.** BDNCP ANAC (nostro mirror, sha256 nel manifest) per i CIG padre e derivati; pagine dei bandi su consip.it, consultate il 5/11/2026; TED; open data Consip degli ordini (dati.consip.it, file 2024-2025 archiviati il 5/11/2026); atti di enti aderenti trovati con ricerca online (fonte non ufficiale, archiviati con sha256).
- **Verificato e riferito.** «Assente» vuol dire che abbiamo consultato la pagina ufficiale dell'iniziativa e il documento non c'è; il tipo di documento si deduce dal nome del file (controllo a mano solo per PRINCO). Le norme e i dati che non abbiamo letto sulla fonte sono marcati [R] nelle schede ([carenze.yaml](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/database/carenze.yaml)).
- **Valori.** Somme di importi dichiarati in BDNCP: ordine di grandezza, non spesa né transato (confronto con gli open data Consip al § 2).
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
| 0.1 | 2026-11-05 | prima versione: 86 iniziative, 1.360 documenti Consip archiviati, open data Consip degli ordini | prima versione |
