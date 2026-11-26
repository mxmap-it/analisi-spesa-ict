---
title: "Indisponibilità persistente del sito: analisi giuridica, metodo e diagnosi (proposta)"
date: 2026-11-26
description: "Quando un sito istituzionale o la sezione «Amministrazione trasparente» non risponde a nessuno, l'ente è in violazione? Analisi delle norme, metodo per accertare un'indisponibilità persistente e diagnosi della causa (dominio scaduto, IndicePA o link ANAC non aggiornati, piattaforma migrata). Proposta, versione 0.1."
weight: 44
gruppo: documenti
---

**Stato: proposta per Fabio (versione 0.3, #85).** È la nostra interpretazione, non giurisprudenza consolidata. Nessun ente è stato contattato su questa base.

## 0. Due misure distinte: AT e PVL

Si misurano due cose diverse, con rendiconti separati e questo metodo comune:

| | AT: sezione «Amministrazione trasparente» | PVL: link ai documenti di gara nella scheda ANAC del CIG |
|---|---|---|
| unità | l'ente (un sito) | il CIG (un link per procedura) |
| obbligo | d.lgs. 33/2013 artt. 8-9, CAD | d.lgs. 36/2023 art. 28, delibera ANAC 264/2023 |
| diagnosi tipiche | D1-D5, D7 | D6, link mancante |
| correzione | sito, IndicePA, URL comunicato | link dei CIG, redirect dalla piattaforma dismessa |
| rendiconto | «AT: indisponibilità persistente» (da scrivere) | «PVL: link ai documenti non raggiungibili» (prosegue [`pvl-link-cig`](../sistemi-documenti/)) |

In comune: il motore delle prove, la soglia di persistenza (§ 3), l'analisi giuridica (§ 2) e **una sola PEC per ente**, con una parte AT e una parte PVL.

## 1. Il problema in breve

Nel censimento dell'art. 9 ([pagina](../trasparenza-accessibilita/)) circa 4.600 enti risultano «irraggiungibili» e circa 1.400 «nessun client accettato». Dopo il giro da IP residenziale (#84) sappiamo che 986 enti bloccano solo i datacenter; il resto non risponde **a nessuno**, né dal server né da una linea di casa.

Esempio: il sito della sezione indicato all'ANAC è `www.ente-vecchio.it/AmministrazioneTrasparente/`; il dominio non esiste più (DNS) e l'ente pubblica ora su `www.ente-nuovo.it`. Chi parte dal dato ufficiale non trova nulla.

## 2. Analisi giuridica (interpretazione favorevole alla violazione)

La tesi: **la raggiungibilità è parte dell'obbligo di pubblicazione e la responsabilità è dell'ente**, qualunque sia la causa tecnica. Un contenuto obbligatorio che nessuno può aprire equivale a un contenuto non pubblicato, per tutto il tempo in cui resta irraggiungibile.

### 2.1 Pubblicare significa rendere accessibile

- **d.lgs. 33/2013, art. 2 c. 2**: la pubblicazione è la diffusione sul sito istituzionale con *accesso diretto e immediato*, senza autenticazione né identificazione.
- **art. 6**: le amministrazioni garantiscono integrità, costante aggiornamento, completezza, tempestività, semplicità di consultazione e *facile accessibilità*.
- **art. 8 c. 3**: i dati restano pubblicati per **cinque anni** (pubblicazione continua, non un istante).
- **art. 9 c. 1**: la sezione «Amministrazione trasparente» sta nella home page; sono vietati filtri e soluzioni tecniche che impediscono ai motori di ricerca di indicizzarla. Un sito che non risponde impedisce l'indicizzazione a tutti: è il caso limite del divieto.
- **d.lgs. 82/2005 (CAD), art. 53**: i siti delle PA rispettano accessibilità, reperibilità, completezza, aggiornamento; **art. 51** e misure di sicurezza AgID: disponibilità dei dati e dei servizi.

### 2.2 La responsabilità resta all'ente

- **art. 43 d.lgs. 33/2013**: il Responsabile della prevenzione della corruzione e della trasparenza (RPCT) controlla l'adempimento e segnala gli inadempimenti; i dirigenti garantiscono il flusso tempestivo delle informazioni.
- **art. 46**: l'inadempimento è elemento di valutazione della responsabilità dirigenziale, causa eventuale di responsabilità per danno all'immagine e si valuta ai fini della retribuzione di risultato.
- **art. 45**: l'ANAC vigila e può ordinare la pubblicazione.
- Il fornitore di hosting o del portale non sposta la responsabilità: l'ente lo sceglie, lo controlla e deve prevedere la continuità. Per analogia, nelle gare telematiche il giudice amministrativo pone sulla stazione appaltante il rischio del malfunzionamento informatico, anche di causa ignota (TAR Sicilia n. 383/2024; Consiglio di Stato sull'art. 79 c. 5-bis d.lgs. 50/2016: le clausole di esonero non coprono le regole di condotta imposte dalla legge).

### 2.3 Migrare senza aggiornare è un inadempimento autonomo

1. **Link alla BDNCP e atti di gara**: la delibera ANAC n. 264/2023 (modificata dalla n. 601/2023), attuativa dell'art. 28 d.lgs. 36/2023, impone in «Bandi di gara e contratti» il collegamento alla BDNCP per ogni procedura con CIG e la pubblicazione sul sito degli atti che la BDNCP non raccoglie. Se gli indirizzi comunicati portano a una piattaforma dismessa, il collegamento obbligatorio è rotto.
2. **IndicePA**: l'art. 6-ter del CAD e le linee guida AgID impongono di tenere aggiornati i dati dell'ente, sito istituzionale compreso.
3. **Continuità quinquennale (art. 8)**: con la migrazione i contenuti già pubblicati devono restare raggiungibili (redirect dai vecchi indirizzi o nuovi indirizzi comunicati).

### 2.4 Rimedi a disposizione di chiunque

- **Accesso civico semplice (art. 5 c. 1)**: chiunque può chiedere ciò che doveva essere pubblicato e non lo è; risposta entro 30 giorni (c. 6), poi potere sostitutivo e ricorso (art. 116 c.p.a.).
- **Segnalazione all'RPCT** e, in caso di inerzia, **all'ANAC** (art. 45).

### 2.5 Giurisprudenza: cosa c'è e cosa manca

- **Manca** (finora) una pronuncia diretta su una sezione «Amministrazione trasparente» irraggiungibile: ricerca da completare nelle banche dati della giustizia amministrativa.
- **Per analogia**:
  - rischio del guasto informatico a carico dell'amministrazione (gare telematiche, sopra);
  - pubblicità legale online e continuità: per l'albo online la pubblicazione è assolta con almeno 12 ore di disponibilità al giorno, e le interruzioni allungano il periodo (regole tecniche e vademecum sull'albo online); TAR Marche n. 56/2026 sulla funzione di pubblicità legale dell'albo online (*riferita da* una sola fonte, testo da verificare).
- In pubblico e nelle PEC la tesi si presenta come **interpretazione**, con le norme, non come giurisprudenza consolidata.

### 2.6 Limiti della tesi

- Un guasto breve non è una violazione: serve **persistenza** (§ 3).
- Va distinto il sito spento dall'indirizzo ufficiale non aggiornato: sono due rilievi diversi, con azioni correttive diverse (§ 4).
- Un blocco dei soli datacenter è un'altra categoria (WAF per IP, decisione aperta su #84).

## 3. Metodo: quando un'indisponibilità è «persistente» (proposta)

Un ente è in **indisponibilità persistente** se tutte le condizioni valgono:

| condizione | soglia proposta |
|---|---|
| origini | nessuna risposta utile sia dal server (datacenter) sia dall'IP residenziale |
| ripetizioni | almeno **3 prove** con esito negativo |
| arco temporale | prima e ultima prova distanti almeno **7 giorni**, prove in giorni diversi |
| orari | almeno una prova in orario d'ufficio (9-13 di un giorno feriale) |
| identità | tutte le identità oneste falliscono (bot del progetto, browser reale) |
| indirizzi | falliscono sia l'URL della sezione noto ad ANAC sia la home di IndicePA (o la diagnosi § 4 ne spiega la differenza) |

«Risposta utile» = HTTP 2xx/3xx con contenuto. Sono negative: DNS inesistente, connessione rifiutata o assente, timeout, errori 5xx, 4xx a tutti i client, certificato che non permette la connessione al browser.

Ogni prova registra data, origine (IP e ASN), identità, catena delle risposte e sha256 della prova grezza. Ogni prova negativa ha un dump nell'archivio content-addressed.

Esito dell'ente: *persistente* (tutte le condizioni), *intermittente* (almeno una prova positiva nell'arco), *da riprovare* (prove insufficienti).

## 4. Diagnosi della causa

L'obiettivo è dire all'ente **che cosa** non va, non solo che «non funziona». Le diagnosi si basano su prove che possiamo riprodurre.

| codice | diagnosi | come si riconosce | rilievo all'ente | azione correttiva |
|---|---|---|---|---|
| D1 | dominio inesistente o scaduto | DNS NXDOMAIN su tutte le origini; dati di registrazione del dominio | sezione e indirizzi ufficiali puntano a un dominio che non esiste | ripristinare il dominio o redirigerlo e aggiornare IndicePA e i dati ANAC |
| D2 | server spento | DNS risolve, connessione rifiutata o timeout da tutte le origini | sito istituzionale non raggiungibile | ripristinare il servizio; piano di continuità |
| D3 | sito guasto | risponde con 5xx o 4xx a tutti i client e tutte le origini | sezione non consultabile | correggere il portale |
| D4 | IndicePA non aggiornato | il sito di IndicePA è irraggiungibile ma esiste un sito attuale dell'ente (trovato da URL ANAC, dominio della PEC, mxmap.it, redirect, ricerca) che risponde | indirizzo ufficiale del sito istituzionale obsoleto | aggiornare IndicePA (art. 6-ter CAD) |
| D5 | URL della sezione comunicato ad ANAC non aggiornato | l'URL noto ad ANAC (L190 o anagrafica) è irraggiungibile, il sito attuale dell'ente ha la sezione | collegamento ufficiale alla sezione rotto | aggiornare l'URL comunicato; redirect dal vecchio indirizzo |
| D6 | piattaforma degli atti migrata, link nei CIG non aggiornati | gli URL dei documenti di gara associati ai CIG puntano a una piattaforma dismessa; la stessa procedura si trova sulla piattaforma nuova | atti di gara non raggiungibili dagli indirizzi pubblicati (delibera 264/2023) | aggiornare i collegamenti; redirect dalla vecchia piattaforma |
| D7 | blocco dei soli datacenter | accessibile da IP residenziale, non dal server | (categoria WAF per IP, decisione aperta) | — |
| D0 | causa non determinata | nessuna delle precedenti con prove sufficienti | solo «indisponibilità persistente» | — |

Una diagnosi entra nel cruscotto e nella PEC **solo se la prova la sostiene**. D4-D6 richiedono di aver trovato il sito o la piattaforma nuova con una via indipendente; altrimenti l'ente resta D1-D3 o D0.

## 5. Prime misure (26/11/2026, giro 2026-11, da rifinire)

Fra i 4.601 enti con esito «irraggiungibile» nel database del giro:

| gruppo | enti |
|---|---:|
| senza URL della sezione noto (né da ANAC né trovato): esito da rivedere, non è un sito che non risponde | 3.647 |
| URL della sezione sullo stesso host del sito IndicePA | 249 |
| URL della sezione su un host diverso da IndicePA, e il dominio IndicePA funziona per altri enti | 380 |
| URL della sezione su un host diverso, nessun segnale sul dominio IndicePA | 325 |

**Persistenza con le prove già raccolte** (server 3-4/11, IP residenziale 22-25/11): degli irraggiungibili con prove, **1.073 enti** soddisfano tutte le condizioni del § 3 (due origini, ≥ 3 prove, ≥ 7 giorni, orario d'ufficio); 75 tutte tranne l'orario d'ufficio; 1.632 hanno avuto almeno una risposta utile (intermittenti o solo datacenter, da riclassificare).

Sui 954 con URL, il primo errore è: timeout 428, DNS inesistente 289, altro 237. **Sono misure di un solo giro: nessuna è ancora «persistente».** I gruppi «host diverso» sono i candidati a D4-D5.

### 5.1 Prima diagnosi AT dei 1.073 persistenti (26/11, un GET dal server alla home IndicePA)

| candidato | enti | esempio (URL AT noto → home IndicePA) |
|---|---:|---|
| **D5** URL della sezione non aggiornato: la home IndicePA risponde, su un altro host | 196 | `www.autoritadistrettoac.it` → `www.aubac.it` |
| **D5** percorso della sezione non valido: la home IndicePA risponde sullo stesso host | 134 | da controllare a mano (http/https, percorso) |
| **D1** dominio inesistente anche in IndicePA | 317 | sito nuovo da cercare (→ D4 se trovato) |
| **D2** home IndicePA non risponde (timeout, connessione rifiutata) | 64 | |
| **D3** home IndicePA guasta (5xx, TLS, connessione interrotta) | 82 | |
| nessun sito in IndicePA | 275 | già un rilievo IndicePA a sé |
| altro | 5 | |

Sono **candidati**: la home è stata provata una sola volta e da una sola origine. Prima di usarli nel cruscotto o in una PEC servono la riprova (§ 3) e, per D5, la conferma che la sezione esiste sul sito attuale. Strumento: `tools/verifiche/indisponibilita_home.py`; esiti in `esiti/2026-11-26/indisponibilita/`.

## 6. Uso nella comunicazione agli enti (PEC)

La PEC all'RPCT conterrà: le prove (date, origini, sha256), la diagnosi D0-D6 con l'azione correttiva, le norme del § 2 presentate come interpretazione, il riferimento all'accesso civico semplice e la metrica che verifica la correzione (raggiungibile in 3 prove su 7 giorni). **Nessuna PEC parte senza l'approvazione di Fabio.**

## 7. Prossimi passi

1. Riprove D1-D3 per la persistenza (3 prove in 7 giorni, due origini).
2. Diagnosi D4-D5: confronto URL ANAC, IndicePA, dominio della PEC, mxmap.it.
3. Diagnosi D6: link ai documenti dei CIG (BDNCP) verso piattaforme dismesse.
4. Colonna «indisponibilità persistente» e diagnosi nel cruscotto, dopo l'ok di Fabio.
5. Ricerca giurisprudenziale mirata.

## Fonti

- d.lgs. 33/2013 (artt. 2, 5, 6, 8, 9, 43, 45, 46); d.lgs. 82/2005 (artt. 6-ter, 51, 53); d.lgs. 36/2023 (art. 28).
- [Delibera ANAC n. 264/2023 modificata dalla n. 601/2023](https://www.dirittobancario.it/wp-content/uploads/2024/01/Delibera-n.-264-del-20-giugno-2023-modificata-da-Del.-601-19.12.2023.pdf)
- [TAR Sicilia n. 383/2024, rischio del malfunzionamento](https://www.giurisprudenzappalti.it/sentenze/il-rischio-della-causa-ignota-del-malfunzionamento-informatico-ricade-sulla-stazione-appaltante/)
- [Consiglio di Stato, responsabilità per il malfunzionamento della piattaforma](https://www.ildirittoamministrativo.it/Consiglio-Stato-si-esprime-sulla-responsabilit%C3%A0-della-stazione-appaltante-per-il-malfunzionamento-della-piattaforma-relativa-alla-gara-telematica/ult3294)
- [Albo online e malfunzionamenti](https://www.sinetinformatica.it/2011/05/periodo-di-pubblicazione-degli-atti-all%E2%80%99albo-online-in-caso-di-malfunzionamento-del-sistema/); [TAR Marche n. 56/2026 (riferita)](https://www.giurisprudenzappalti.it/sentenze/lalbo-pretorio-non-ha-perso-le-sue-funzioni-originarie/)

## Registro delle revisioni

| versione | data | cambiamento |
|---|---|---|
| 0.3 | 2026-11-26 | prima diagnosi AT dei 1.073 persistenti: D5 330, D1 317, D2 64, D3 82, senza sito IndicePA 275 |
| 0.2 | 2026-11-26 | AT e PVL trattate come misure distinte con metodo comune; persistenza calcolata sulle prove esistenti: 1.073 enti |
| 0.1 | 2026-11-26 | prima stesura: analisi giuridica, metodo della persistenza, diagnosi D0-D7, prime misure del giro 2026-11 |
