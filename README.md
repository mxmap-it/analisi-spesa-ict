# analisi-spesa-ict

**Quanta parte della spesa ICT della Pubblica Amministrazione italiana va a fornitori sotto
giurisdizione italiana, europea o extra-europea.**

Secondo asse dell'[Osservatorio Nazionale Sovranità Digitale](https://osservatorio.mxmap.it/),
accanto alla posta elettronica misurata da [mxmap.it](https://mxmap.it/). Stessa definizione di
sovranità — **giurisdizione giuridica del fornitore e del suo gruppo**, non collocazione fisica
dei server — e stessa classificazione a quattro categorie: `it`, `eu_non_it`, `extra_eu`,
`unknown`.

La domanda non è *quanto* spende la PA in digitale, ma **verso quale giurisdizione va l'euro
speso**.

## Obiettivo

**L'obiettivo finale è misurare la spesa ICT della Pubblica Amministrazione italiana per
giurisdizione del fornitore**, e pubblicare quella misura in modo verificabile: quanta parte va a
soggetti sotto ordinamento italiano, quanta a soggetti europei, quanta a soggetti extra-europei —
quelli esposti, per esempio, al CLOUD Act statunitense.

Serve a dare a decisori, amministrazioni, giornalisti e cittadini un numero che oggi non esiste, con
i suoi limiti dichiarati. È lo stesso lavoro che mxmap.it fa sulla posta elettronica degli enti,
applicato al denaro.

Per arrivarci il progetto attraversa quattro fasi, ciascuna abilitante per la successiva e nessuna
fine a sé stessa:

1. **Mettere a disposizione i dati, e misurare quanto sono disponibili.** Un mirror dei dati grezzi
   di spesa e appalti, sempre aggiornato e fruibile da chiunque, con una dashboard pubblica che
   mostra dove mancano e un report periodico a ciascuna autorità che li produce. È un risultato
   intermedio, con un tetto di sforzo: esiste perché l'analisi abbia una base completa, e perché i
   problemi trovati vengano corretti alla fonte invece di essere aggirati ogni volta.
2. **Misurarne la qualità.** Errori, incongruenze fra fonti, dati mancanti, collegamenti che non si
   chiudono — registrati una volta, pubblicati e segnalati.
3. **Definire il perimetro e attribuire la giurisdizione.** Quali acquisti sono ICT, e di quale
   giurisdizione è ciascun fornitore e il suo gruppo.
4. **Analizzare e interpretare.** La spesa ICT per giurisdizione, con il pavimento misurato e la
   dichiarazione esplicita di ciò che il dato pubblico non consente di sapere.

Il dettaglio di fasi, tetti di sforzo e criteri di chiusura è nella [roadmap](https://analisi-spesa-ict.mxmap.it/progetto/roadmap/).

---

## Indice

1. [Dove gira e perché](#1-dove-gira-e-perché)
2. [I dataset disponibili](#2-i-dataset-disponibili)
3. [Le strade che non abbiamo seguito](#3-le-strade-che-non-abbiamo-seguito)
4. [Gli strumenti che riusiamo](#4-gli-strumenti-che-riusiamo)
5. [Cosa costruiamo noi](#5-cosa-costruiamo-noi)
6. [Architettura della pipeline](#6-architettura-della-pipeline)
7. [Cosa si potrà dire, e cosa no](#7-cosa-si-potrà-dire-e-cosa-no)
8. [Licenze](#8-licenze)
9. [Stato](#9-stato)

---

## 1. Dove gira e perché

Tutto il lavoro gira sul **server di mxmap.it** (`mxmap.it@51.158.36.151`, 8 core, 31 GB di RAM,
~246 GB liberi), non su runner cloud e non sul portatile. Tre motivi, tutti verificati:

- **ANAC blocca gli indirizzi IP cloud** con un WAF, e respinge gli user-agent che non sembrano
  browser. Chi ci riesce usa runner non-cloud oppure un proxy: lo documentano sia DataCivicLab
  sia Radar-Appalti. Un workflow GitHub Actions normale non scarica nulla.
- **I file sono grandi**: un singolo delta mensile dei CIG pesa ~110-120 MB compressi, il dataset
  `cup` 83 MB, i mensili OCDS superano i 3 GB. L'elaborazione va fatta in streaming e su disco.
- **I job sono lunghi e vanno ripresi**: il portatile si disconnette, il server no.

Ogni job è idempotente e ripartibile, lo stato sta in [`STATE.md`](STATE.md).

## 2. I dataset disponibili

Stato **verificato il 2026-10-26** con richieste HTTP reali dal server. Le righe senza nota di
verifica vengono da documentazione di terzi e vanno ricontrollate prima dell'uso.

### Appalti

| Fonte | Cosa misura | Chiavi | Licenza | Stato verificato |
|---|---|---|---|---|
| **ANAC — dataset tabellari BDNCP** | Base d'asta (`cig`), aggiudicazioni, aggiudicatari, partecipanti, subappalti, quadro economico, stati di avanzamento | CIG | CC BY-SA 4.0 | **La spina dorsale.** Aggiornati al 2026-10-05. API CKAN funzionante ma **non documentata**: richiede user-agent da browser |
| **ANAC — `cup`** | Ponte CIG ↔ CUP | CIG, CUP | CC BY-SA 4.0 | 7.103.635 CIG distinti, ma solo 5.149.498 (72,5%) con un CUP valido: 1.951.844 righe hanno `ND` al posto del CUP. Join uno-a-molti |
| **ANAC — `stazioni-appaltanti`** | Anagrafe delle SA, con codice AUSA | CF, AUSA | CC BY-SA 4.0 | Aggiornato al 2026-10-13 |
| **ANAC — smartCIG** | Affidamenti semplificati sotto soglia | CIG semplificato | CC BY-SA 4.0 | Serve: è dove vive gran parte della spesa ICT corrente |
| **ANAC — OCDS bulk** | Stesso contenuto in Open Contracting Data Standard | ocid, CIG | CC BY 4.0 | **Fermo a marzo 2026**: i mesi da aprile a settembre rispondono 404. Vedi §3 |
| **ANAC — Pubblicità a Valore Legale** | Avvisi che fanno fede per legge dal 2024 | CIG | — | La fonte più tempestiva. Categoria merceologica in testo libero, non CPV |
| **Consip** `dati.consip.it` | 16 dataset. Utili: `gare-asp` e `bandi-e-gare` (**record-level, con CIG**); ordini MePA e convenzioni (aggregati annuali) | CIG dove c'è, CF PA, codice IPA | CC BY 4.0 | **Finestra mobile**: in linea 2024-2026, il 2023 risponde 404 |
| **TED — API v3 eForms** | Bandi e aggiudicazioni sopra soglia UE | numero avviso, CPV, CF ente | riuso UE | API anonima senza chiave. **Il CIG non è un campo standard eForms** |

### Spesa effettiva

| Fonte | Cosa misura | Chiavi | Licenza | Stato verificato |
|---|---|---|---|---|
| **SIOPE — bulk diretto** `siope.it/documenti/siope2/open/last` | **Pagamenti di cassa** per codice gestionale | CF ente, codice gestionale | CC BY 4.0 | `SIOPE_USCITE.2025.zip` 75 MB, `.2026.zip` 66 MB, `SIOPE_ANAGRAFICHE.zip` 863 KB, aggiornati al 2026-10-22. Importi **in centesimi**, **mensili puri non cumulati** |
| **BDAP Open Data** | ~3.700 dataset: bilancio dello Stato, gestione spese, bilanci enti | CF ente, capitolo, piano dei conti | CC BY | API CKAN funzionante. Per SIOPE **non** usarlo: vedi §3 |
| **CPT** | Spesa consolidata del Settore Pubblico Allargato | regione, settore | aperta | Serie 2000-2023, annuale. Contesto, non misura |

### ICT in senso stretto

| Fonte | Cosa misura | Stato |
|---|---|---|
| **PA Digitale 2026** `teamdigitale/padigitale2026-opendata` | Finanziamenti ICT-PNRR **per singolo ente**, con CUP | CSV e JSON, CC BY 4.0, ricostruito ogni giorno. La fonte open più granulare sull'ICT per ente |
| **ACN — catalogo servizi cloud qualificati** | Infrastrutture e servizi qualificati, con fornitore e livello | CSV, IODL 2.0. Misura i servizi qualificati, non la spesa |
| **AgID — rilevazione annuale spesa ICT** | Spesa per cluster di ~77 amministrazioni | **solo PDF** |
| **AgID/DTD — Censimento del patrimonio ICT** | Per singolo ente: voci di costo e **licenze software** | **non pubblicato.** È il dato più rilevante che manca: candidato per un accesso civico |

### Anagrafiche e societario

| Fonte | Cosa dà | Licenza | Stato |
|---|---|---|---|
| **IndicePA** (CKAN) | 28 dataset: enti, unità organizzative, responsabili della transizione al digitale | CC BY 4.0 | Aggiornamento giornaliero |
| **GLEIF** golden copy | LEI e relazioni di controllo madre-figlia | **CC0** | Bulk giornaliero. Copertura italiana molto magra: vedi §3 |
| **EU Financial Transparency System** | Beneficiari del bilancio UE 2007-2025, **con partita IVA** | riuso UE | Bulk libero, sottoutilizzato in Italia |

### Il perimetro ICT sui CPV

Divisioni di riferimento: **48** software e sistemi, **72** servizi IT, **30** macchine per ufficio
e computer, **32** apparecchiature TLC, **64** servizi di telecomunicazione.

Tre avvertenze misurate su dati reali, che rendono il perimetro una scelta da documentare e non una
lista da copiare:

1. **La divisione 30 non è hardware ICT.** I codici più frequenti sono buoni pasto e cancelleria.
   Senza una lista bianca, "divisione 30 = hardware" è falso.
2. **I server stanno nella 48** (CPV 48820000): un prodotto hardware classificato come software.
3. **Le licenze non hanno un CPV proprio.** Licenza perpetua, canone SaaS e sviluppo su misura
   ricadono indistintamente sotto 48 e 72.

## 3. Le strade che non abbiamo seguito

Questa sezione esiste perché le scelte di perimetro valgono più del codice, e perché chi arriva
dopo deve sapere cosa è già stato provato e scartato.

### Il canale OCDS di ANAC — scartato come fonte primaria

È il formato più bello e lo standard internazionale, ma **è fermo a marzo 2026**: verificato oggi,
i file di aprile, maggio, giugno, luglio, agosto e settembre 2026 rispondono tutti 404, mentre i
dataset tabellari sono aggiornati al 5 ottobre. Non è un episodio: AppaltIntel ha documentato che
**per trenta mesi fra il 2020 e il 2026 il canale OCDS non ha mai pubblicato il file del mese**, e
ha dovuto ritirare pubblicamente un'analisi in cui aveva attribuito al mercato un calo del 2023
che era invece un buco della fonte.

La lezione, che vale come principio di progetto: *una serie storica che scende può raccontare il
mercato oppure la fonte, e le due cose si distinguono solo guardando quali mesi ci sono.*

→ **Usiamo i dataset tabellari.** L'OCDS resta utile per il confronto incrociato quando riparte.

### L'API REST OCDS di ANAC — scartata, è morta

Dichiarata sul portale, con Swagger UI raggiungibile. Ma tutti gli endpoint su
`api.anticorruzione.it` rispondono **404** attraverso il gateway, e il file `swagger.json` **non è
JSON valido**. → Usiamo l'**API CKAN**, che funziona benissimo e non è documentata da nessuna parte.

### SIOPE attraverso BDAP — da verificare, e specchiato comunque

**Quello che sappiamo è di seconda mano.** AgID, nel commento al proprio modulo `siope.py` di
Cruscotto Italia, scrive di aver abbandonato BDAP perché **genera i dump a richiesta** con un tetto
di 400 secondi lato server e 503 ricorrenti, i `resource_id` sono cablati per regione e anno, e
**il 2025 era troncato a marzo per 1.717 comuni** fra Lombardia e Friuli e assente per 84 comuni di
Trento. **Non l'abbiamo verificato noi.**

E al 26 ottobre 2026 non si può verificare: il catalogo open data di BDAP è in **manutenzione
straordinaria**, e lo comunica rispondendo **HTTP 200** con una pagina HTML invece che con un
errore — chi lo interroga in automatico crede che vada tutto bene.

→ **Usiamo come via principale il bulk nazionale di `siope.it`**, che espone `Last-Modified` e
`Accept-Ranges`. Ma **specchiamo anche la via BDAP** appena torna disponibile, e confrontiamo le due
comune per comune e mese per mese: è esattamente il tipo di difformità fra vie di accesso allo
stesso dato che il progetto deve misurare, non presumere.

### I 23 portali regionali di e-procurement — fuori perimetro

Dal 1° gennaio 2024 le piattaforme di approvvigionamento digitale certificate **devono** comunicare
ad ANAC attraverso le API della Piattaforma Contratti Pubblici (`comunicaAppalto` per ottenere il
CIG, `pubblicaAvviso`, `comunicaPostPubblicazione` per aggiudicazione ed esecuzione). La sostanza
dei contratti è quindi già in ANAC: i portali danno **tempestività e documenti**, non contratti
diversi.

→ Integrarne ventitré costerebbe mesi di manutenzione di scraper per un guadagno che non cambia la
risposta sulla sovranità. Restano fuori, con un'unica eccezione a campione (sotto).

### I documenti di gara in massa — impossibile, misurato

Per sapere *quale prodotto* è stato comprato servirebbero capitolato e disciplinare. La verifica è
netta: sul perimetro ANAC la reperibilità del documento è **circa zero** — il bulk non contiene
allegati e non espone un URL per CIG — e sui portali regionali i documenti coprono lo **0,2%**
delle procedure aggiudicate, concentrati di fatto su un solo portale (SATER, Emilia-Romagna).

→ I documenti si useranno **solo come campione** su SATER, per validare le altre misure. Non come
statistica.

### Il CUP come chiave dell'analisi — declassato a etichetta

Il ponte ufficiale CIG ↔ CUP esiste, è il dataset `cup` di ANAC, e **nessuno dei progetti mappati
lo usa**. Va però letto con attenzione: alla rilevazione del 26 ottobre 2026 contiene 7.103.635 CIG
distinti, ma **1.951.844 righe hanno come CUP la stringa `ND`**. I CIG con almeno un CUP valido
sono 5.149.498, il 72,5%: chi conta le righe sovrastima i collegamenti di un quarto.

Sul perimetro ICT, misurato sul delta di ottobre 2026, **i CIG con CUP valido sono il 13,7%**
(3.360 su 24.580). Una misura precedente su un campione diverso, i mesi 2024-2026 di un altro
progetto, dava il 20,2% contando la sola presenza nel file: in entrambi i casi una minoranza.

La bassa copertura non è un difetto dei dati — il `ND` invece sì, ed è nel [rapporto ANAC](https://analisi-spesa-ict.mxmap.it/rendiconti/anac-2026-10/): il CUP identifica un **progetto di investimento pubblico**, e licenze,
canoni, manutenzione e connettività non lo sono. Il CUP serve a dire "questo contratto nasce dal
PNRR" per una minoranza dei casi, e a saltare verso OpenCoesione, ReGiS e OpenCUP.

→ La chiave dell'analisi resta il **CIG**.

### Gli XML della Legge 190 pubblicati da ogni ente — fuori perimetro

Sono l'unica fonte veramente alternativa ad ANAC, ed è su quella che Atoka PA (SpazioDati, gruppo
Cerved) ha costruito un prodotto commerciale dal 2016. Significa inseguire migliaia di siti di enti
con formati e qualità disomogenei. → Fuori: costo altissimo, e nulla che cambi la classificazione
di giurisdizione.

### Un aggregatore generalista della spesa pubblica — già fatto, due volte

- **Cruscotto Italia** (AgID, AGPL-3.0): ~24 fonti, mirror in DuckDB e Parquet, endpoint MCP,
  aggiornamento giornaliero.
- **DataCivicLab** (~40 repo, MIT): contratto RAW → CLEAN → MART, Parquet su bucket pubblico,
  `metadata.json` e `validation.json` per l'audit trail.

→ Non ne serve un terzo. Noi facciamo l'**unico pezzo che non c'è**: l'attribuzione di giurisdizione.

### La normalizzazione di tutto in un unico schema — scartata per principio

Competenza del bilancio dello Stato, cassa del SIOPE, aggiudicato di ANAC, ordinato di Consip e
consolidato dei CPT misurano cose diverse e **non sono sommabili**. Un progetto che le fonde in un
numero unico di "spesa pubblica" produce un numero falso. → Un modello canonico **per dominio**, con
i ponti dichiarati e il loro tasso di aggancio misurato.

E un ponte, in particolare, **non esiste**: fra il mondo RGS (capitolo di bilancio, codice
gestionale SIOPE) e il mondo appalti (CIG) non c'è alcuna chiave comune. La catena impegno →
contratto → pagamento non si chiude con i dati pubblici, e va detto invece di simularla.

### L'attribuzione esaustiva della capogruppo — ridimensionata dai numeri

Misurato su GLEIF, che è l'unica fonte aperta e in CC0: circa 259.000 entità italiane censite, ma
solo **~6.800 con capogruppo diretta** e **~7.150 con capogruppo ultima**, di cui l'82,9% con
capogruppo a sua volta italiana. Restano **~1.200 imprese italiane con controllante estero
verificabile**: lo **0,03%** delle imprese italiane. Oltre sei milioni di record sono "reporting
exception", cioè entità che dichiarano di non avere un parent identificato.

Buona notizia sul join: il **96,4%** dei LEI italiani ha il campo `registeredAs` popolato, nel
90,5% dei casi come codice fiscale a 11 cifre. **La chiave partita IVA → LEI funziona**; è la catena
di controllo a essere sparsa.

Tutto il resto è chiuso: il Registro Imprese non pubblica la catena di controllo, BRIS consente solo
ricerche umane una società per volta, il registro dei titolari effettivi richiede interesse
legittimo e pagamento, il bulk di OpenCorporates è commerciale, il Public CbCR parte a fine 2026
senza database centrale. Con copertura ampia c'è solo ORBIS di Moody's, a pagamento.

→ Il registro si costruisce **per valore, non per numerosità**: poche centinaia di fornitori coprono
la gran parte del valore ICT. Copertura dichiarata, mai simulata.

### Un classificatore ML addestrato sulle proprie predizioni — scartato

Esiste un precedente italiano che classifica l'oggetto delle gare con TF-IDF più regressione
logistica, ma rilegge come training set le etichette che ha scritto ai run precedenti: l'accuratezza
in cross-validation misura la coerenza del modello con sé stesso, non la correttezza. → Se useremo
un classificatore, il **ground truth sarà congelato** e mai riscritto dal modello.

### opentender.eu — non è una fonte viva

La piattaforma del Government Transparency Institute (esito del progetto europeo DIGIWHIST) gira
ancora, ma nel registro OCP il dato italiano risulta **fermo a marzo 2024**. → Utile per il metodo
(il loro *mastering* dei duplicati è ben documentato) e per la profondità storica 2007-2024, non
come fonte corrente.

### Una conservazione dei dati che si possa dare per scontata — non esiste

Osservazione diretta, ed è la ragione per cui l'archiviazione è il primo stadio della pipeline:

- **Consip** tiene una finestra mobile: oggi 2024-2026, il 2023 risponde 404. Nessuna politica
  pubblicata.
- **ANAC** fa sparire i delta vecchi: i file di gennaio, febbraio e marzo 2026 rispondono 404,
  mentre aprile-ottobre sono in linea. A settembre i delta erano sei, oggi sono sette: **non è una
  finestra a sei mesi, e la regola non è deducibile né documentata**. Intanto il file annuale
  `cig-2026` non esiste ancora, quindi tutto il 2026 vive solo nei delta.
- **soldipubblici.gov.it** è dismesso e reindirizza alla pagina di manutenzione di AgID.
- **Il portale MIT** ha bandi ed esiti congelati al 31 dicembre 2023.

→ Chi non archivia ogni mese perde, e non recupera.

## 4. Gli strumenti che riusiamo

Principio: **riusiamo ciò che è libreria o servizio invocabile**, non ciò che è applicazione. Sulle
licenze non abbiamo preclusioni — rilasciamo tutto, quindi il copyleft non è un ostacolo e l'AGPL va
benissimo. Restano fuori solo i repo **senza licenza dichiarata** (che sono tutti i diritti
riservati) e le licenze **non libere** (Elastic License, clausole non commerciali).

| Serve per | Strumento | Licenza | Come lo usiamo |
|---|---|---|---|
| Motore di pipeline | `dataciviclab/toolkit` | MIT | Come libreria: `dataset.yml` più SQL, RAW → CLEAN → MART su DuckDB, Parquet in output, `metadata.json` e `validation.json` a ogni run. Plugin già pronti per HTTP, CKAN, SDMX, SPARQL |
| Radar disponibilità fonti | `dataciviclab/source-observatory` | MIT | Monitora già 36 cataloghi, ANAC e Consip inclusi. Ci appoggiamo e contribuiamo le fonti mancanti |
| Pubblicità a Valore Legale, vocabolario CPV, validazione CIG | `aborruso/anac-pl-pp-cli` | Apache-2.0 | Unico strumento al mondo su quella fonte. Porta anche i 9.454 codici CPV, la validazione del CIG con cifra di controllo, uno store SQLite e un server MCP |
| Catalogo BDAP, IndicePA | `aborruso/openbdap-pp-cli`, `openipa` | Apache-2.0 | Per la scoperta; l'ingestione resta nel toolkit |
| Ingestione SIOPE e PNRR | `AgID/cruscotto-italia`, `etl/sources/` | AGPL-3.0 | Moduli già scritti sulle stesse fonti: `siope.py`, `pnrr_progetti.py`, `bdap.py`, `anac.py`. Valgono soprattutto per **le trappole già pagate da altri** |
| Qualità del contenuto tabellare | `frictionless-py` | MIT | Schema, tipi, valori nulli, unicità |
| Validazione metadati DCAT | `ISAITB/shacl-validator` | EUPL-1.2 | Servizio Docker self-hostabile, shapes da `SEMICeu/DCAT-AP` |
| Anagrafiche e LEI | GLEIF golden copy | CC0 | Bulk giornaliero |
| Entity resolution | `opensanctions/nomenklatura` | MIT | Libreria agnostica, usata sui nostri dati |
| Convenzione di provenienza | source-spec di `DoveVannoINostriSoldi` | AGPL-3.0 | Riusiamo il **formato dei metadati** (hash, byte, data di acquisizione, limiti dichiarati) |

### Il seme del registro esiste già

`anac-pl-pp-cli` contiene il package `internal/giurisdizione` (Apache-2.0, con test) che classifica
un fornitore in **IT / UE / EXTRA-UE** dalla denominazione e ne riporta il gruppo, con la **nostra
stessa definizione**: giurisdizione del fornitore e del gruppo, CLOUD Act citato nel commento al
codice. E chi non è riconosciuto resta `?`, non diventa italiano per difetto — che è la scelta
metodologicamente corretta.

→ Il nostro registro **parte da lì**, non in concorrenza: la lista va estratta dal codice Go e
portata in un file dati che manteniamo noi e che la sua CLI può consumare dall'esterno.

## 5. Cosa costruiamo noi

1. **L'archivio delle risorse deperibili.** Nessuno lo fa, e ogni mese si perde qualcosa.
2. **Il livello di qualità dei dati che manca al radar.** `source-observatory` misura la salute
   della *fonte*; mancano continuità temporale, persistenza, qualità del contenuto, agganciabilità
   e le **pagelle per produttore**, che sono l'artefatto di advocacy.
3. **Il perimetro ICT documentato**, con le esclusioni motivate e i test che le verificano.
4. **Il registro fornitore → gruppo → giurisdizione**, per valore e con copertura dichiarata.

## 6. Architettura della pipeline

```
   ARCHIVIO                NORMALIZZAZIONE            ATTRIBUZIONE           PUBBLICAZIONE
   (append-only)           (per dominio)              (il nostro pezzo)
┌─────────────────┐    ┌──────────────────────┐    ┌──────────────────┐   ┌────────────────┐
│ fetch + sha256  │    │ toolkit: RAW→CLEAN   │    │ perimetro ICT    │   │ kpi.json       │
│ manifest per    │───▶│ →MART su DuckDB      │───▶│ (CPV motivati)   │──▶│ dashboard      │
│ risorsa         │    │ un modello per       │    │ registro         │   │ qualità        │
│ mai sovrascrive │    │ dominio, non uno     │    │ giurisdizioni    │   │ report         │
└─────────────────┘    └──────────────────────┘    └──────────────────┘   └────────────────┘
        │                                                                         ▲
        └────────────────▶ MONITOR QUALITÀ ───────────────────────────────────────┘
                     disponibilità, freschezza, continuità,
                     persistenza, contenuto, agganciabilità
```

Quattro regole che valgono per ogni stadio:

- **Append-only sull'archivio.** Una risorsa scaricata non viene mai sovrascritta: nuova
  acquisizione, nuovo file, nuovo hash, nuova riga di manifest.
- **Idempotenza.** Rilanciare un job non duplica e non rompe: ciò che è già acquisito si salta.
- **Ripartibilità.** Ogni job scrive il proprio avanzamento su file e riprende da dove si era
  interrotto; lo stato complessivo sta in [`STATE.md`](STATE.md).
- **Provenienza obbligatoria.** Ogni numero pubblicato risale alla risorsa, all'hash e alla data di
  acquisizione da cui viene.

## 7. Cosa si potrà dire, e cosa no

Il dato pubblico **non consente** di affermare "il X% della tecnologia della PA italiana è estera".
Due limiti strutturali:

1. **ANAC registra chi firma il contratto, non di chi è la tecnologia.** L'aggiudicatario è quasi
   sempre una società italiana anche quando rivende prodotto estero.
2. **Il divieto di citare marchi nelle specifiche tecniche** (art. 79 e Allegato II.5 del
   d.lgs. 36/2023, prima art. 68 del d.lgs. 50/2016) sopprime deliberatamente il segnale.

Quello che si può pubblicare in modo difendibile è un **pavimento misurato**, con la dichiarazione
esplicita che la dipendenza reale è più alta e che il dato pubblico ne struttura la maschera. È una
posizione più solida di una percentuale finta-precisa.

## 8. Licenze

- **Codice**: libero. I pacchetti che vogliamo far accettare a monte in progetti permissivi restano
  MIT e scritti come libreria pura; il resto può essere AGPL dove solleviamo codice AGPL.
- **Dati e documentazione**: **CC BY-SA 4.0**, come il resto dell'Osservatorio.
- **Dati di origine**: ANAC CC BY-SA 4.0, Consip CC BY 4.0, SIOPE CC BY 4.0, GLEIF CC0, IndicePA
  CC BY 4.0. Ogni dataset derivato cita la fonte e la data di acquisizione.

## 9. Stato

Vedi [`STATE.md`](STATE.md). Al 2026-10-26: repository appena creato, analisi delle fonti
e degli strumenti conclusa, pipeline da costruire a partire dallo stadio di archiviazione.
