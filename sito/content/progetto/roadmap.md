---
title: "Roadmap"
date: 2026-10-26
---


**Stato:** proposta · **Ultimo aggiornamento:** 2026-10-26

Lo scopo del progetto è uno: misurare **verso quale giurisdizione va l'euro speso in digitale
dalla PA italiana**. Tutto il resto è strumentale, e va tenuto strumentale.

## 0. I principi che rendono ogni fase abilitante

Cinque regole che valgono per tutte le fasi. Servono a non ripassare mai due volte sullo stesso
problema.

1. **Ogni problema si registra una volta e non si riscopre.** Difficoltà di accesso, buchi,
   anomalie e incongruenze finiscono nel [registro dei problemi](#6-il-registro-dei-problemi) con
   un identificativo stabile, la prova riproducibile e la data. Chi riprende il lavoro legge il
   registro, non ricomincia l'indagine.
2. **La copia che usiamo è la copia che pubblichiamo.** Nessun archivio privato "di lavoro" diverso
   da quello esposto: se il nostro dato è aggiornato, lo è anche quello di chiunque altro.
3. **Ogni difficoltà è pubblica e notificata.** Finisce in dashboard e, con periodicità, in un
   report indirizzato all'autorità che produce il dato. Un buco segnalato una volta e poi
   dimenticato non migliora niente.
4. **È un byproduct, e ha un tetto di sforzo.** Lo strumento serve a mettere tutti i dataset a
   disposizione dell'analisi. Non diventa il progetto. Il tetto è un numero massimo di **token al
   giorno**, applicato automaticamente al lavoro di Claude sul server (vedi la fase 1).
5. **Portabilità per costruzione.** I dati stanno su questo VPS adesso e si sposteranno. Quindi:
   nessun percorso assoluto nel codice, un manifest autosufficiente che descrive l'archivio, e un
   layout trasferibile con un `rsync` senza riscaricare nulla.

## 1. Fase 0 — Cosa le autorità dovrebbero garantire

**Esito:** `docs/ATTESE-AUTORITA.md`, scritto adesso e **mantenuto aggiornato**.

È il documento che dichiara, per ogni autorità e per ogni dataset, **cosa ci aspettiamo** in termini
di disponibilità: cadenza di pubblicazione, profondità storica, conservazione delle versioni
passate, formato, presenza di API, licenza leggibile da macchina, checksum.

Ogni riga nasce come **ipotesi** e porta uno stato che cambia man mano che il mirror la verifica:

| Stato | Significato |
|---|---|
| `atteso` | È quello che riteniamo dovuto, non ancora misurato |
| `confermato` | Il mirror ha verificato che l'autorità lo rispetta |
| `smentito` | Il mirror ha verificato che non lo rispetta → genera una voce nel registro problemi |

Dallo stesso documento nascono **le nostre richieste**, uguali per tutte le autorità dove hanno
senso, perché una richiesta ripetuta e identica è più efficace di dieci richieste diverse:

1. **Non cancellare.** Le versioni passate restano scaricabili, o esiste un archivio permanente.
2. **Pubblicare la politica di conservazione.** Oggi nessuno la dichiara: la retention dei delta
   ANAC si deduce solo elencando le risorse, e quella di Consip si scopre andando in 404.
3. **Pubblicare il file dell'anno in corso**, non solo i delta incrementali.
4. **Dichiarare la cadenza reale** e segnalare le interruzioni: l'OCDS fermo da sette mesi non ha
   un avviso da nessuna parte.
5. **Documentare l'API** quando esiste, e dichiararla dismessa quando non funziona più.
6. **Pubblicare i checksum** di ogni risorsa.
7. **Licenza leggibile da macchina** su ogni dataset.
8. **Non bloccare il riuso civico**: nessun filtro sugli indirizzi IP e nessuna discriminazione
   sullo user-agent per i dati aperti.

**Tetto di sforzo:** una giornata per la prima stesura. Si aggiorna poi a costo marginale, perché
le verifiche arrivano dal mirror.

## 2. Fase 1 — Mirror e monitoraggio della disponibilità

È il pezzo da costruire adesso. **Non include l'analisi di qualità del contenuto**, che è la fase 2.

### 1A — Registry delle risorse

Un'anagrafica per **risorsa**, non per fonte: è la differenza principale rispetto a
`source-observatory`, che monitora 36 cataloghi. Per ogni risorsa: identificativo stabile, URL,
protocollo, autorità produttrice, cadenza attesa, partizionamento temporale, e **le altre vie in cui
lo stesso dato è disponibile** (bulk, API, altro portale).

Formato compatibile con `sources_registry.yaml` di source-observatory, così da poterlo contribuire
a monte quando avrà senso.

### 1B — Sonda di disponibilità

Giornaliera, per ogni risorsa: codice HTTP, dimensione, `Last-Modified`, `ETag`, tipo di contenuto,
tempo di risposta, e rilevamento esplicito del blocco WAF. Una richiesta al secondo per autorità,
user-agent che dichiara chi siamo e dove scrivere.

Esito: una riga di storico al giorno per risorsa. Mai sovrascritta.

### 1C — Mirror append-only

Scarica, calcola lo `sha256`, e **se l'hash è nuovo conserva una nuova versione**. Se è identico,
non riscarica e registra solo che era identico. Nessuna sovrascrittura, mai.

Budget di spazio misurato sul campo: **~3,2 GB** per le 111 risorse disponibili del registry, crescita
di **~2 GB l'anno**. Sul VPS attuale ci sono 246 GB liberi.

**Fuori dal mirror per ora:** l'OCDS bulk di ANAC, oltre 100 GB per lo storico, canale fermo da
sette mesi e ridondante rispetto ai tabellari. Resta nel registry come *monitorato ma non
specchiato*, e si riconsidera se riparte.

### 1D — Continuità e persistenza

Si calcolano **dal nostro manifest**, non dalla fonte: la fonte mostra solo ciò che ha oggi.

- **Continuità**: per i dataset partizionati nel tempo, quali periodi esistono e quali mancano.
- **Persistenza**: cosa è sparito dalla fonte ma è nel nostro archivio. È la metrica che nessuno ha
  e la ragione per cui mirror e monitor sono la stessa macchina.
- **Freschezza**: scarto fra cadenza dichiarata e cadenza reale.

### 1E — Dashboard pubblica

Statica, alimentata da un `qualita.json`, dentro il sito Hugo dell'Osservatorio. Mostra, per
autorità e per dataset: stato corrente, storico della disponibilità, periodi mancanti, risorse
sparite, anomalie aperte. Il JSON è pubblico e riutilizzabile.

### 1F — Il mirror deve essere usabile dagli altri

Requisito esplicito: chi oggi scarica questi dati con i propri strumenti deve poter puntare a noi
**cambiando solo l'URL di base**. Quindi:

- **percorsi identici a quelli originali** sotto il nostro prefisso, così che un tool si rediriga
  cambiando una costante;
- **`index.json` e `manifest.jsonl`** con URL originale, `sha256`, dimensione, data di acquisizione
  e intestazioni HTTP viste;
- **endpoint minimi compatibili con CKAN** (`package_list`, `package_show`, `package_search`), così
  che `kingfisher-collect` e il plugin CKAN del toolkit di DataCivicLab funzionino senza modifiche;
- **`Last-Modified`, `ETag` e `Accept-Ranges`** serviti correttamente: è esattamente ciò che manca a
  BDAP e che ha costretto AgID a cambiare fonte per SIOPE;
- **nessun filtro WAF, nessuna discriminazione sullo user-agent**, e un limite di banda dichiarato;
- un `datapackage.json` Frictionless per dataset, dove lo schema è noto.

I quattro consumatori da tenere come riferimento di compatibilità: `kingfisher-collect` (OCP),
`etl/sources/*` di `cruscotto-italia` (AgID), `scripts/etl` di DoveVannoINostriSoldi, e il
`toolkit` di DataCivicLab.

### 1G — Report alle autorità

Per ogni autorità, un **report periodico** con: disponibilità nel periodo, periodi mancanti, risorse
sparite, interruzioni di cadenza, e le richieste aperte della fase 0. Pubblicato sul sito e
**notificato ai riferimenti dell'autorità**.

Cadenza: **trimestrale** per i report ordinari, **immediata** per le regressioni gravi — un dataset
che sparisce o una cadenza che si interrompe.

### Tetto di sforzo: token al giorno

Il tetto non è sul tempo ma sul **consumo di token al giorno** del lavoro svolto da Claude.

- Il valore sta in `config/budget.yaml` (`token_giornalieri`), ed è deciso da Fabio.
- Il lavoro **a script** — scarichi, sonde, controlli in DuckDB — non consuma token e non è
  soggetto al tetto: ha solo i limiti di cortesia verso i portali, una richiesta al secondo.
- Il lavoro **di Claude sul server** passa da un wrapper che invoca `claude -p --output-format
  json`, legge il consumo dal campo `usage`, lo registra in `stato/budget/<data>.jsonl` e **non
  avvia un nuovo compito se il totale del giorno ha raggiunto il tetto**. Il compito resta in coda
  e riparte il giorno dopo, perché ogni compito è ripartibile per costruzione.
- Il lavoro interattivo con Fabio si conta a parte, con la stessa contabilità giornaliera.

Due regole che restano, perché il tetto da solo non le garantisce:

- **Nessuna fonte vale il tetto di un giorno.** Se una fonte richiede scraping fragile,
  autenticazione, captcha o reverse engineering, si marca `non-specchiabile` con il motivo e si passa
  oltre.
- **Nessun recupero retroattivo.** Ciò che è già sparito dalla fonte si registra come perduto e si
  usa come prova nel registro dei problemi. Non si inseguono archivi di terzi: i file sono grandi,
  la copertura è casuale e il tempo speso non porta avanti l'analisi. Da qui in poi non sparisce
  più nulla, perché l'archivio parte adesso.

### Definizione di "fatto"

La fase 1 è chiusa quando, tutte insieme:

1. ogni dataset del perimetro è specchiato e si aggiorna da solo, oppure è marcato
   `non-specchiabile` con il motivo;
2. la dashboard è online e si aggiorna da sola;
3. il mirror è raggiungibile da terzi e almeno uno degli strumenti di riferimento ci punta senza
   modifiche al codice;
4. il primo report per autorità è pubblicato e notificato.

## 3. Fase 2 — Qualità, incongruenze e dati mancanti

Si apre dopo la fase 1. In sintesi, perché i dettagli si decidono con il mirror in mano:

- validità e riempimento dei campi chiave, codici fiscali con cifra di controllo, date impossibili,
  importi anomali, unicità delle chiavi;
- **incongruenze fra fonti** sullo stesso fatto: è il pezzo che non esiste da nessuna parte, e il
  mirror lo rende possibile perché conserva le due versioni;
- **agganciabilità**: tasso di join reale su CIG, CUP, codice fiscale e codice IPA;
- ogni anomalia entra nel registro problemi e nel report all'autorità.

**Tetto:** da definire all'apertura, con lo stesso meccanismo per fonte.

## 4. Fase 3 — Perimetro ICT e registro delle giurisdizioni

- lista CPV motivata, con le esclusioni verificate e i test;
- registro fornitore → gruppo → giurisdizione, seme da `internal/giurisdizione` di
  `anac-pl-pp-cli`, arricchimento GLEIF, curatela **per valore e non per numerosità**.

## 5. Fase 4 — Analisi e interpretazione

Lo scopo del progetto: spesa ICT per giurisdizione, con il pavimento dichiarato e i limiti in
chiaro. Le incongruenze trovate nella fase 2 diventano parte del risultato, non una nota a piè di
pagina: dire *quanto* non si può sapere è parte della misura.

## 6. Il registro dei problemi

`docs/REGISTRO-PROBLEMI.md`, append-only, una voce per problema:

```
ID            PROB-2026-0001
autorità      ANAC
risorsa       ocds bulk 2026/04..09
tipo          interruzione di pubblicazione
rilevato      2026-09-23  (confermato 2026-10-26)
prova         GET .../bulk/2026/04.json -> 404, mentre i tabellari sono al 2026-10-05
impatto       nessuna serie OCDS dopo marzo 2026
stato         aperto · segnalato il <data> · risposta: <nessuna>
```

Ciclo di vita: `aperto` → `segnalato` → `risposta ricevuta` → `risolto` oppure `cronico`. Un
problema `cronico` resta in dashboard a tempo indeterminato: è il suo scopo.

Le voci già pronte all'apertura del registro, tutte verificate:

| Problema | Autorità |
|---|---|
| OCDS bulk fermo a marzo 2026, senza avviso | ANAC |
| API REST OCDS dichiarata ma tutti gli endpoint in 404, `swagger.json` non valido | ANAC |
| Retention dei delta non documentata né deducibile; gennaio-marzo 2026 spariti | ANAC |
| File annuale dell'anno in corso assente: tutto il 2026 vive nei delta | ANAC |
| Rifiuto degli user-agent non-browser con pagina HTML servita come 200 | ANAC |
| API CKAN funzionante ma non documentata | ANAC |
| Finestra mobile di tre anni senza politica pubblicata: il 2023 è sparito | Consip |
| Dataset su ordini e convenzioni aggregati senza CIG né CF della PA | Consip |
| Dump generati a richiesta, 503 ricorrenti, annualità troncate | MEF-RGS (BDAP) |
| `soldipubblici.gov.it` dismesso senza reindirizzamento ai dati | AgID |
| Bandi ed esiti congelati al 31 dicembre 2023 (riferito, da verificare) | MIT |
| Censimento del patrimonio ICT raccolto per ente e non pubblicato | AgID / DTD |
| API OpenCUP documentata come pubblica ma risponde 401 | DIPE |

## 7. Cadenze operative

| Quando | Cosa |
|---|---|
| Giornaliero | Sonda di disponibilità su tutte le risorse; dashboard rigenerata |
| Mensile | Fetch di ciò che scade: delta ANAC, annualità Consip, SIOPE |
| Trimestrale | Report per autorità, pubblicati e notificati |
| All'evento | Regressione grave: voce nel registro e notifica immediata |

## 8. Portabilità

L'archivio sta sul VPS di mxmap.it e si sposterà, probabilmente su una macchina dedicata. Perché
sia un `rsync` e non un progetto:

- un solo albero di dati, descritto interamente dal manifest;
- nessun percorso assoluto nel codice: una variabile d'ambiente per la radice;
- il manifest contiene tutto ciò che serve a ricostruire l'archivio altrove, o a verificarlo;
- il nome di dominio da cui il mirror è servito è una configurazione, non una costante.

## 8ter. I dataset, in ordine: prima ANAC, poi gli altri

Decisione di Fabio del 26 ottobre 2026: **ANAC fino in fondo**, poi tutti gli altri dataset mappati.
Ogni gruppo ha il suo ticket.

| # | Gruppo | Cosa entra | Perché in questa posizione | Ticket |
|---|---|---|---|---|
| **0** | **ANAC** | Tutti i 70 dataset, 1.797 risorse, CSV, JSON e TTL, **OCDS bulk 2018-2026 incluso** | È la spina dorsale degli appalti; in corso | [#9](https://github.com/mxmap-it/analisi-spesa-ict/issues/9), [#10](https://github.com/mxmap-it/analisi-spesa-ict/issues/10), [#31](https://github.com/mxmap-it/analisi-spesa-ict/issues/31) |
| 1 | **Consip** | 16 dataset; `gare-asp` e `bandi-e-gare` con CIG; ordini MePA e convenzioni | **Cancella oltre i tre anni**: ogni mese perso è irrecuperabile. E il canale centralizzato è dove passa molta spesa ICT | [#11](https://github.com/mxmap-it/analisi-spesa-ict/issues/11) |
| 2 | **SIOPE** | Bulk di `siope.it`, tutti gli anni; più la via BDAP, da confrontare | È l'unica misura di **cassa**, ente per ente | [#12](https://github.com/mxmap-it/analisi-spesa-ict/issues/12), [#30](https://github.com/mxmap-it/analisi-spesa-ict/issues/30) |
| 3 | **ICT e anagrafi** | PA Digitale 2026, IndicePA, catalogo cloud ACN | Specifiche dell'ICT, e servono all'attribuzione | [#13](https://github.com/mxmap-it/analisi-spesa-ict/issues/13) |
| 4 | **BDAP** | Bilancio dello Stato, gestione delle spese, bilanci degli enti | Spesa di competenza e cassa; oggi in manutenzione | [#25](https://github.com/mxmap-it/analisi-spesa-ict/issues/25) |
| 5 | **Finanziamenti** | OpenCUP, OpenCoesione, ItaliaDomani/ReGiS, ponte CUP-CIG di openpnrr | Marcano la fonte di finanziamento dei contratti, PNRR incluso | [#26](https://github.com/mxmap-it/analisi-spesa-ict/issues/26) |
| 6 | **Altre fonti di spesa di DataCivicLab** | OpenCivitas, Registro Aiuti di Stato, INPS, AIFA; da verificare DAIT e NoiPA | Spesa pubblica diretta, fuori dall'ICT | [#14](https://github.com/mxmap-it/analisi-spesa-ict/issues/14) |
| 7 | **Europa** | TED, EU Financial Transparency System | Gare sopra soglia e fondi UE diretti | [#27](https://github.com/mxmap-it/analisi-spesa-ict/issues/27) |
| 8 | **Attribuzione** | GLEIF | Fornitore → gruppo → giurisdizione | [#28](https://github.com/mxmap-it/analisi-spesa-ict/issues/28) |
| 9 | **Contesto** | CPT, ISTAT, Eurostat COFOG | Denominatori e confronti, non misura | [#29](https://github.com/mxmap-it/analisi-spesa-ict/issues/29) |

**Fuori**, deciso: i ventitré portali regionali, gli XML della Legge 190 per ente, la Wayback
Machine, i documenti di gara in massa. I documenti di gara rientreranno solo a campione, per
l'obiettivo finale.

## 8bis. Il perimetro delle fonti

Entrano **solo le fonti che riguardano, direttamente o indirettamente, la spesa pubblica**.
Criterio, tre livelli di relazione e classificazione delle 36 fonti di DataCivicLab —
ventidue delle quali restano fuori — in [PERIMETRO-FONTI.md](../perimetro-fonti/).

Vale anche quando contribuiremo a monte: a `source-observatory` portiamo il livello per risorsa
**sulle sole fonti di spesa**, lasciando a loro le altre.

## 9. Fuori perimetro, per non riaprire la discussione

Deciso e motivato nel [README](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/README.md): l'OCDS come fonte primaria, l'API REST di ANAC, SIOPE
via BDAP, i ventitré portali regionali, i documenti di gara in massa, il CUP come chiave, gli XML
della Legge 190, un aggregatore generalista della spesa pubblica, la normalizzazione di tutto in un
unico schema, l'attribuzione esaustiva della capogruppo, i classificatori autoalimentati e
opentender come fonte corrente.
