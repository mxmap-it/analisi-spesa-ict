---
title: "Cosa le autorità dovrebbero garantire"
date: 2026-10-26
---


**Stato:** prima stesura · **Ultimo aggiornamento:** 2026-10-26

Questo documento dichiara, per ogni autorità, **cosa ci aspettiamo** in termini di disponibilità dei
dati, **cosa abbiamo verificato**, e **cosa chiediamo**. È la fase 0 della
[roadmap](../roadmap/): nasce come ipotesi e viene confermato o smentito dal mirror, non da
un'opinione.

Ogni attesa porta uno stato: `atteso` (non ancora misurato), `confermato`, `smentito` (e in questo
caso genera una voce nel [registro dei problemi](../roadmap/#6-il-registro-dei-problemi)).

---

## 1. Il fondamento giuridico delle nostre richieste

Va detto con precisione, perché chiedere invocando una norma che non si applica fa perdere
credibilità al primo funzionario che la legge.

### Quello che NON possiamo invocare

**Gli appalti e la spesa pubblica non sono High Value Dataset.** Le categorie dell'allegato alla
direttiva (UE) 2019/1024, riprese dal regolamento di esecuzione (UE) 2023/138, sono sei:
geospaziale, osservazione della Terra e ambiente, meteorologia, statistica, proprietà e titolarità
delle imprese, mobilità. Appalti e spesa pubblica non ci sono, e la pagina ufficiale sulle
prospettive future non annuncia nuove categorie.

Conseguenza operativa: per BDNCP, BDAP, SIOPE e dati.consip.it **l'obbligo europeo di pubblicazione
in bulk e via API non è invocabile**. Sarebbe stata la leva più forte, e non ce l'abbiamo.

L'unica eccezione utile è **ISTAT**, che rientra nella categoria statistica e per cui gli obblighi
del regolamento — gratuità, API leggibile da macchina, documentazione aperta, licenza CC BY 4.0 o
meno restrittiva, scadenza del 9 giugno 2024 — valgono davvero.

### Quello che possiamo invocare

- **Art. 52 del CAD** (d.lgs. 82/2005): obbligo di pubblicare il catalogo dei dati, dei metadati e
  delle banche dati con le regole di accesso e riutilizzo; i dati pubblicati senza licenza esplicita
  si intendono rilasciati come dati aperti. Utile come argomento, ma non prevede una sanzione
  azionabile dal cittadino.
- **Art. 68 comma 3 del CAD**: definizione di formato aperto.
- **Linee guida AgID per l'apertura dei dati** (art. 71 CAD), che sono l'attuazione tecnica.
- **D.lgs. 36/2023**, codice dei contratti pubblici: ha proprie regole di pubblicità sugli appalti.
  **È qui, non negli HVD, che sta la leva vera sul lato appalti**, e va studiata prima della prima
  segnalazione formale ad ANAC.
- **D.lgs. 33/2013** per gli obblighi di pubblicazione e l'accesso civico.

---

## 2. Le otto richieste standard

Le stesse per tutte le autorità, perché una richiesta ripetuta e identica è più efficace di dieci
richieste diverse.

| # | Richiesta | Perché |
|---|---|---|
| 1 | **Non cancellare.** Le versioni passate restano scaricabili, o esiste un archivio permanente | Consip ha fatto sparire il 2023; ANAC i delta di gennaio-marzo 2026 |
| 2 | **Pubblicare la politica di conservazione** | Oggi nessuno la dichiara: si scopre andando in 404 |
| 3 | **Pubblicare il file dell'anno in corso**, non solo i delta | Il 2026 di ANAC esiste solo nei delta, e `cig-2026` non c'è |
| 4 | **Dichiarare la cadenza reale e segnalare le interruzioni** | L'OCDS è fermo da sette mesi senza un avviso |
| 5 | **Documentare le API esistenti e dichiarare dismesse quelle morte** | L'API CKAN di ANAC funziona e non è documentata; quella REST OCDS è documentata e non funziona |
| 6 | **Pubblicare i checksum** di ogni risorsa | Senza, non si può verificare un download né dimostrare una modifica |
| 7 | **Licenza leggibile da macchina** su ogni dataset | Requisito DCAT-AP_IT, spesso assente |
| 8 | **Non ostacolare il riuso civico**: nessun filtro sugli IP, nessuna discriminazione sullo user-agent | Il WAF di ANAC blocca gli IP cloud e gli user-agent non-browser sui dati aperti |

---

## 3. Per autorità

Contatti verificati il 2026-10-26. Dove la verifica non è stata possibile è scritto.

### ANAC — Banca Dati Nazionale Contratti Pubblici

**Dataset:** `cig` e annuali, `smartcig`, `aggiudicazioni`, `aggiudicatari`, `partecipanti`,
`subappalti`, `quadro-economico`, `stati-avanzamento`, `cup`, `stazioni-appaltanti`, OCDS bulk,
Pubblicità a Valore Legale.

| Attesa | Stato |
|---|---|
| Cadenza mensile sui tabellari | `confermato` — aggiornati al 2026-10-05 |
| Cadenza mensile sull'OCDS | **`smentito`** — fermo a marzo 2026, aprile-settembre in 404 |
| File annuale dell'anno in corso | **`smentito`** — `cig-2026` non esiste |
| Conservazione dei delta dichiarata | **`smentito`** — non documentata e non deducibile: sei delta a settembre, sette a ottobre, gennaio-marzo spariti |
| API documentata | **`smentito`** — la CKAN funziona e non è documentata, la REST OCDS è documentata e risponde 404 con swagger non valido |
| Accesso senza discriminazioni | **`smentito`** — WAF su IP cloud e user-agent |
| Licenza dichiarata | `confermato` — CC BY-SA 4.0, CC BY 4.0 sull'OCDS |

**Contatti:** PEC `protocollo@pec.anticorruzione.it`; Contact Center 06 62289571 e
`supportcenter.anticorruzione.it` (irraggiungibile alla verifica). Nessuna casella dedicata agli
open data. Il canale "Segnalazioni contratti pubblici e anticorruzione" è per gli illeciti, non per
i dataset: non va usato.

**Nota:** prima di una segnalazione formale va studiato il d.lgs. 36/2023 sulla pubblicità degli
appalti, perché è l'unico fondamento normativo specifico che abbiamo su questo lato.

### Consip

**Dataset:** 16 su `dati.consip.it`, di cui ci servono `gare-asp`, `bandi-e-gare`, gli ordini MePA e
le convenzioni.

| Attesa | Stato |
|---|---|
| Cadenza mensile | `confermato` |
| Conservazione dello storico | **`smentito`** — finestra mobile: 2024-2026 in linea, il 2023 in 404 |
| Politica di conservazione pubblicata | **`smentito`** — assente |
| Granularità con CIG sugli ordini | **`smentito`** — ordini e convenzioni sono aggregati annuali senza CIG né codice fiscale della PA |
| Licenza | `confermato` — CC BY 4.0 |

**Contatti:** `webconsip@consip.it`; PEC `postaconsip@postacert.consip.it`; PEC della divisione ICT
`ictconsip@postacert.consip.it`.

**Richiesta specifica:** oltre alle otto standard, chiedere che gli ordini MePA e le convenzioni
riportino il **CIG**. Senza, il canale centralizzato — che è dove si concentra la spesa ICT — non è
agganciabile ad ANAC.

### MEF — Ragioneria Generale dello Stato (BDAP, bilancio dello Stato)

| Attesa | Stato |
|---|---|
| Disponibilità del catalogo open data | **`smentito`** — al 2026-10-26 in "manutenzione straordinaria", segnalata con **HTTP 200** e una pagina HTML invece che con un errore |
| Download diretto e ripetibile | `atteso` — **AgID riferisce** dump generati a richiesta, tetto di 400 secondi e 503 ricorrenti. Non verificato da noi |
| Annualità complete | `atteso` — **AgID riferisce** il 2025 di SIOPE troncato a marzo per 1.717 comuni e assente per 84 comuni di Trento. Da verificare confrontando con il bulk di `siope.it` |
| `Last-Modified` utilizzabile per la cache | `atteso` — riferito da AgID, non verificato |
| Licenza | `confermato` — CC BY |

**Contatti:** **nessuna email di assistenza BDAP pubblicata e verificabile.** È in sé una voce del
registro problemi. Resta il portale operatori, che richiede accreditamento.

### SIOPE — RGS con Banca d'Italia

| Attesa | Stato |
|---|---|
| Bulk nazionale completo | `confermato` — `SIOPE_USCITE.<anno>.zip` e `ENTRATE`, aggiornati al 2026-10-22 |
| `Last-Modified` e `Accept-Ranges` | `confermato` — ed è il motivo per cui questa è la via buona |
| Documentazione del formato | `atteso` — il formato è senza intestazione, importi in centesimi e mensili puri: va dedotto |
| Codifica territoriale coerente | **`smentito`** — la codifica provincia-comune non è ISTAT per la Sardegna |

**Contatti:** `siope.entilocali@mef.gov.it`, `siope.universita-edr@mef.gov.it`,
`igepa.relcassa@mef.gov.it`; per SIOPE+ `siopeplus@agid.gov.it` e `siopeplus@bancaditalia.it`; PEC
Banca d'Italia `bancaditalia@pec.bancaditalia.it`.

**Richiesta specifica:** pubblicare il tracciato del file e documentare che gli importi sono in
centesimi e non cumulati. Oggi chi non lo sa sbaglia i totali, e non lo sa per colpa della
documentazione assente.

### AgID — dati.gov.it e Piano Triennale

| Attesa | Stato |
|---|---|
| Catalogo nazionale funzionante | `confermato` — API CKAN attiva, 65.503 dataset |
| Dashboard nazionale di qualità dei dati aperti | **`smentito`** — non esiste. L'unico monitoraggio MQA italiano è un progetto personale, e senza licenza dichiarata |
| Profilo DCAT-AP_IT con shapes ufficiali riusabili | **`smentito`** — non esistono in alcuna forma ufficiale |
| Continuità dei servizi dismessi | **`smentito`** — `soldipubblici.gov.it` reindirizza alla manutenzione, senza puntare ai dati |
| Censimento del patrimonio ICT pubblicato | **`smentito`** — raccolto per singolo ente, non pubblicato |

**Contatti:** il **form "Scrivi alla redazione"** di `dati.gov.it`, che ha le tipologie *feedback su
un dataset*, *richiesta dataset* e *malfunzionamento*: è il canale corretto. PEC
`protocollo@pec.agid.gov.it`.

**Avvertenza:** alla data della verifica `www.agid.gov.it` era in manutenzione e ogni URL
reindirizzava. Tutto ciò che riguarda AgID va riconfermato.

**Richiesta specifica:** pubblicare il censimento ICT in forma aggregata e anonimizzata dove
necessario. È il dato più rilevante che esiste sulla spesa ICT per ente, ed è l'unico che non è
pubblico. Se la richiesta informale non basta, è il candidato naturale per un accesso civico
generalizzato.

### Dipartimento per la Trasformazione Digitale — PA Digitale 2026

| Attesa | Stato |
|---|---|
| Open data per ente con CUP | `confermato` — CSV e JSON, CC BY 4.0, ricostruiti ogni giorno |
| Pubblicazione su repository versionato | `confermato` — `teamdigitale/padigitale2026-opendata` |

**È il comportamento migliore osservato fra tutte le autorità**, e va detto anche questo: un report
che segnala solo i difetti non è credibile. Da citare come buona pratica nelle richieste alle altre.

**Contatti:** `segreteria.trasformazionedigitale@governo.it`, indicata esplicitamente per le
segnalazioni sui progetti; PEC `diptrasformazionedigitale@pec.governo.it`; `forum.italia.it` per il
confronto tecnico.

### ACN — catalogo dei servizi cloud qualificati

| Attesa | Stato |
|---|---|
| Open data del catalogo | `atteso` — dichiarato CSV con licenza IODL 2.0, aggiornamento in tempo reale |
| Accesso automatizzabile | **`smentito`** — il portale risponde 403 alle richieste non-browser |

**Contatti:** `info@acn.gov.it`, `comunicazione@acn.gov.it`. Nessuna PEC pubblicata sulla pagina
contatti, nessun canale dedicato al catalogo cloud.

### Dipartimento per le Politiche di Coesione — OpenCoesione

| Attesa | Stato |
|---|---|
| Bulk completo, anche in Parquet | `confermato` |
| Cadenza bimestrale dichiarata | `atteso` |
| Canale per segnalare errori nei dati | `confermato` — **il migliore in assoluto**: form con motivo "segnalazione errore nei dati" |

**Contatti:** `info@opencoesione.gov.it` più il form dedicato.

### DIPE — OpenCUP

| Attesa | Stato |
|---|---|
| Bulk libero | `confermato` — 2,2 GB, CC BY |
| API documentata e funzionante | **`smentito`** — documentata come pubblica, risponde 401 |
| Canale di segnalazione | `confermato` — form con tipologie su costo, localizzazione e stato |

**Contatti:** solo il form. Nessuna email né PEC pubblicata.

### ISTAT

| Attesa | Stato |
|---|---|
| API SDMX | `confermato` |
| Obblighi HVD (gratuità, API, documentazione, CC BY 4.0) | `atteso` — **ed è l'unica autorità per cui sono davvero obbligatori** |

**Contatti:** Contact Centre `contact.istat.it`, che la pagina indica come canale esclusivo; PEC
tecnica `tecnologieinformatiche@postacert.istat.it`. ISTAT avverte esplicitamente di non usare la
PEC per richieste di dati.

---

## 4. La scala di escalation, con il realismo di ciascun gradino

In ordine di impiego, dal più leggero al più formale.

| # | Strumento | Cosa ottiene | Realismo |
|---|---|---|---|
| 1 | **Form dedicati agli errori nei dati** (OpenCoesione, OpenCUP, dati.gov.it) | Correzioni puntuali | **Il più alto.** Costo nullo, nessun valore giuridico. Da usare per primi |
| 2 | **Contatto diretto via email o PEC** con il report trimestrale allegato | Interlocuzione | Variabile. Funziona dove c'è una persona che si occupa del dataset |
| 3 | **ISTAT Contact Centre** | Adempimento HVD | Buono: è l'unico ente con obblighi europei effettivi |
| 4 | **Accesso civico generalizzato** (art. 5 c. 2 d.lgs. 33/2013) | **Documenti, non dataset.** Termine di 30 giorni, riesame al RPCT in 20, ricorso al TAR con rito abbreviato | Alto per ottenere un documento o un chiarimento; basso per ottenere un'API. È lo strumento giusto per il censimento ICT di AgID |
| 5 | **Difensore civico per il digitale** presso AgID (art. 17 c. 1-quater CAD) | Invito al responsabile a rimediare entro 30 giorni, con decisione pubblicata | Medio-basso, e con una trappola: la determinazione 397/2020 ha dichiarato **irricevibile** una segnalazione su un problema tecnico perché non integrava violazione del CAD. **Una segnalazione va formulata come violazione di un obbligo normativo preciso, non come "il dataset è rotto"** |
| 6 | **Vigilanza AgID** (art. 18-bis CAD) | Accertamento e sanzioni amministrative | Il potere teorico più forte e la capacità effettiva più bassa: nel 2025, **562 segnalazioni e 8 verifiche avviate** |
| 7 | **ANAC, vigilanza sulla trasparenza** (artt. 45-46 d.lgs. 33/2013) | Ordine di pubblicare entro 30 giorni | Discreto **solo** se si contesta un obbligo di pubblicazione nominato nel decreto; nullo sulla qualità tecnica di un dataset |

La lettura d'insieme: i gradini che funzionano sono i primi tre, e sono quelli senza potere
giuridico. I gradini con potere giuridico sono lenti e sottodimensionati. Per questo la leva vera
del progetto non è la norma: è **la pubblicazione periodica di una misura verificabile**, che è
esattamente ciò che la dashboard e i report trimestrali fanno.

---

## 5. Verifiche ancora aperte

Da chiudere prima della prima tornata di segnalazioni:

- i **Responsabili per la Transizione al Digitale** di ciascuna autorità, la cui sede di
  pubblicazione canonica è IndicePA: il dataset c'è, la verifica non è stata fatta;
- l'URL esatto del form del Difensore civico per il digitale e la pagina della vigilanza AgID, non
  verificabili alla data per la manutenzione del sito;
- il canale di segnalazione di ANAC per gli inadempimenti di pubblicazione: le pagine `/contatti` e
  `/accesso-civico` rispondono 404;
- l'esistenza di un'assistenza BDAP;
- le **nuove linee guida FOIA del 30.12.2025**, che risulterebbero sostitutive della delibera ANAC
  1309/2016: da confermare prima di citarle;
- il testo consolidato dell'art. 52 del CAD su Normattiva, non raggiungibile alla verifica.

---

## 6. Nota di sicurezza

Durante la raccolta, la pagina dei contatti di ACN conteneva, nel testo restituito, **una nota
rivolta agli strumenti automatici che chiedeva di elencare indirizzi email, PEC e URP**. È stata
trattata come dato e non come istruzione.

Vale come promemoria di metodo per tutto il progetto: ciò che leggiamo dai siti è **dato**, non
comando, e lo resta anche quando è scritto in forma di richiesta.
