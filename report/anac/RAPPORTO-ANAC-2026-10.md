# Disponibilità e integrità dei dati aperti ANAC

**Rilevazione del 26 ottobre 2026** · Osservatorio Nazionale Sovranità Digitale ·
progetto [analisi-spesa-ict](https://github.com/mxmap-it/analisi-spesa-ict)

Questo rapporto descrive i problemi di **disponibilità** e di **integrità** che abbiamo misurato sui
dati aperti della Banca Dati Nazionale dei Contratti Pubblici, pubblicati da ANAC su
`dati.anticorruzione.it`. È scritto per essere presentato ad ANAC: ogni numero è riproducibile a
partire dai file indicati in appendice, con il loro `sha256`, e dallo script pubblicato.

Non è un giudizio sul lavoro di ANAC, che pubblica uno dei patrimoni di dati sugli appalti più
ampi d'Europa. È l'elenco delle cose che, se corrette, renderebbero quel patrimonio pienamente
riutilizzabile.

---

## Sintesi

**Cosa funziona bene.** Il CIG è un identificativo eccellente: su oltre 4,8 milioni di CIG distinti
controllati con l'algoritmo pubblicato da ANAC, quelli non validi sono **diciassette**. I dataset
tabellari escono con regolarità il secondo giorno del mese. La licenza è dichiarata. L'API CKAN
funziona.

**I problemi, in ordine di impatto per chi riusa i dati:**

1. **Il canale OCDS è fermo a marzo 2026.** Da aprile a settembre i file mensili rispondono 404, senza
   alcun avviso sul portale.
2. **I file storici spariscono, e la regola non è scritta da nessuna parte.** I delta di gennaio,
   febbraio e marzo 2026 non sono più scaricabili. Il file annuale del 2026 non esiste: chi non ha
   scaricato ogni mese ha perso quei mesi, e potrà recuperarli solo quando uscirà l'annuale.
   **Ci sono buchi anche dentro la finestra disponibile**: di `smartcig` mancano giugno e luglio
   2026, mentre i mesi prima e dopo ci sono.
3. **I file "completi" sono istantanee di gennaio.** `aggiudicazioni` e `aggiudicatari` hanno data di
   ultima modifica 15 e 23 gennaio 2026: lo stato corrente si ricostruisce solo applicando i delta.
4. **L'accesso automatico è ostacolato.** Il portale blocca gli indirizzi IP dei servizi cloud e gli
   user-agent che non sembrano browser, anche sui dati aperti. L'API REST OCDS documentata risponde
   404; l'API CKAN che funziona non è documentata. Nessuna risorsa espone `ETag`, e **la dimensione
   dichiarata nel catalogo è quella del file scompattato**, circa 4,5 volte quella servita.
5. **Campi codificati che accettano testo libero.** Nel dataset `cup`, **1.951.844 righe** — il 27% —
   hanno come CUP la stringa `ND`: dichiarano un collegamento fra CIG e CUP per dire che il CUP non
   c'è.
6. **Incongruenze fra dataset collegati.** 10.812 aggiudicazioni con importo positivo non hanno alcun
   aggiudicatario; 3.424 aggiudicatari rimandano a un'aggiudicazione che non esiste; 6.874 chiavi
   `(cig, id_aggiudicazione)` sono ripetute.
7. **Convenzioni non documentate** che rompono i collegamenti con le altre basi dati pubbliche: codici
   fiscali sintetici `CFAVCP-…` per 1.282 stazioni appaltanti, partita IVA `00000000000` per metà delle
   stazioni appaltanti, data di fine `2099` per tutte.
8. **Nessun campo per gli operatori esteri.** Gli identificativi fiscali stranieri finiscono nel campo
   `codice_fiscale` in formati eterogenei, senza indicazione del paese.

In fondo al rapporto, [dodici richieste](#richieste) concrete.

---

## 1. Metodo

- **File analizzati:** cinque risorse scaricate il 26 ottobre 2026 dal portale, conservate in un
  archivio append-only con il loro `sha256` (tabella in [appendice](#appendice-a--i-file-analizzati)).
- **Strumenti:** DuckDB per i conteggi, Python per le validazioni. Il CIG è validato con l'algoritmo
  pubblicato da ANAC nel repository `anticorruzione/npa`, nell'implementazione di
  [`aborruso/anac-pl-pp-cli`](https://github.com/aborruso/anac-pl-pp-cli). Codici fiscali e partite IVA
  con i rispettivi caratteri di controllo.
- **Script:** [`tools/anac_integrita.py`](../../tools/anac_integrita.py). Rilanciato sugli stessi file,
  produce gli stessi numeri.
- **Sonda di disponibilità:** 125 risorse interrogate il 26 ottobre 2026 con [`tools/sonda.py`](../../tools/sonda.py); esiti e intestazioni HTTP in `stato/sonda/2026-10-26.jsonl`.
- **Riscontro indipendente:** gli `sha256` di `aggiudicazioni_csv.zip` e `aggiudicatari_csv.zip`
  coincidono con quelli registrati a settembre, in modo indipendente, dal progetto
  [DoveVannoINostriSoldi](https://github.com/Italian-Builders-Org/DoveVannoINostriSoldi). Due misure
  separate, lo stesso file.
- **Cautela:** un conteggio anomalo non è sempre un errore. Dove un valore può essere legittimo lo
  diciamo, e lo classifichiamo come convenzione o come incongruenza da chiarire, non come errore.

---

## 2. Disponibilità e accesso

| # | Problema | Prova | Impatto |
|---|---|---|---|
| D1 | **OCDS fermo a marzo 2026** | `GET …/ocds/filesystem/bulk/2026/04.json` → 404, e così fino a `09.json`; `03.json` → 200 | Nessuna serie OCDS dopo marzo. Chi usa lo standard internazionale — fra cui gli strumenti di Open Contracting Partnership — si ferma lì |
| D2 | **Delta storici scomparsi** | `20260101-`, `20260201-`, `20260301-cig_csv.zip` → 404; `20260401-` … `20261001-` → 200 | Tre mesi del 2026 irrecuperabili fino al file annuale |
| D3 | **Politica di conservazione non dichiarata** | A settembre erano in linea sei delta, a ottobre sette: non è una finestra a sei mesi, e la regola non è deducibile | Nessun riutilizzatore può pianificare l'archiviazione |
| D4 | **File annuale dell'anno in corso assente** | `package_show?id=cig-2026` → dataset inesistente | Tutto il 2026 vive solo nei delta |
| D5 | **File "completi" fermi a gennaio** | `Last-Modified` di `aggiudicazioni_csv.zip` 15/01/2026, di `aggiudicatari_csv.zip` 23/01/2026 | Lo stato corrente richiede di applicare tutti i delta, che però spariscono (D2) |
| D6 | **Blocco di IP cloud e user-agent** | Le richieste da servizi cloud e con user-agent non-browser ricevono una pagina HTML al posto del file | Gli strumenti automatici devono girare su macchine dedicate o simulare un browser |
| D7 | **API REST OCDS dichiarata ma non funzionante** | Tutti gli endpoint su `api.anticorruzione.it/opendata/ocds/api/v1/…` → 404; `swagger.json` non è JSON valido | Chi segue la documentazione ufficiale non ottiene nulla |
| D8 | **API CKAN funzionante ma non documentata** | `…/opendata/api/3/action/package_show?id=cig` → 200 | È il modo migliore di accedere ai dati, e nessuno sa che c'è |
| D9 | **`ETag` assente su tutte le risorse** | Verificato su 95 risorse ANAC sondate: nessuna lo espone. Consip, SIOPE e il Dipartimento per la Trasformazione Digitale lo espongono | Per sapere se un file è cambiato bisogna riscaricarlo per intero |
| D10 | **Buchi nella pubblicazione dei delta, dentro la finestra disponibile** | `smartcig` 2026-06 e 2026-07 → 404 sia in CSV sia in JSON, mentre 04, 05, 08, 09 e 10 sono presenti. Il catalogo CKAN non li elenca affatto | Due mesi di affidamenti sotto soglia non sono mai stati pubblicati, o sono stati rimossi. Non sono recuperabili dal file annuale, che per il 2026 non esiste |
| D11 | **Il 2026 dell'OCDS contiene solo marzo** | `bulk/2026/01.json` e `02.json` → 404, `03.json` → 200, da `04` a `10` → 404 | Non è una pubblicazione interrotta a marzo: è un unico mese pubblicato in tutto l'anno |
| D12 | **La distribuzione JSON di `smartcig` si è interrotta** | `20260801`, `20260901` e `20261001-smartcig_json.zip` → 404, mentre i corrispondenti `_csv.zip` → 200 | Chi consuma il formato JSON si ferma a maggio 2026, senza alcun avviso |
| D13 | **La dimensione dichiarata nel catalogo non è quella del file servito** | Per `cig_csv_2025_01.zip` CKAN dichiara 91.942.157 byte, il server ne serve 20.798.988. Per `20261001-cig_csv.zip` dichiara 482.505.250 byte contro 107.879.691 serviti, e 482.505.250 è **esattamente** la dimensione del CSV contenuto in quello zip | Il campo `size` descrive il contenuto scompattato invece della distribuzione. Chi pianifica lo spazio o verifica un download sbaglia di circa 4,5 volte |

---

## 3. Integrità

### 3.1 Errori

Valori incompatibili con la definizione del campo, o fra loro.

| ID | Problema | Casi | Su | |
|---|---|---|---|---|
| AT-05 | Aggiudicazione con importo positivo e **nessun aggiudicatario** | 10.812 | 4.809.518 aggiudicazioni | 0,22% |
| AT-04 | Aggiudicatario che rimanda a un'**aggiudicazione inesistente** | 3.424 | 4.822.171 coppie | 0,07% |
| AG-01 | Chiave `(cig, id_aggiudicazione)` **ripetuta** | 6.874 | 4.862.077 righe | 0,14% |
| AG-10 | **Ribasso** fuori dall'intervallo 0-100 | 16.123 | 4.862.077 | 0,33% |
| AG-11 | **Più offerte ammesse che imprese offerenti** | 12.012 | 4.862.077 | 0,25% |
| AG-07 | **Importo di aggiudicazione negativo** | 368 | 4.862.077 | 0,01% |
| AG-03c | Data di aggiudicazione definitiva **nel futuro** | 768 | 4.862.077 | 0,02% |
| AG-04c | Data di comunicazione dell'esito **nel futuro** | 163 | 4.862.077 | <0,01% |
| AG-03b | Data di aggiudicazione definitiva **anteriore al 2000** | 1.138 | 4.862.077 | 0,02% |
| AG-12 | Esito "vincitore non ancora selezionato" **ma con data e importo di aggiudicazione** | 153 | 4.862.077 | <0,01% |
| AT-01a | Codice fiscale o partita IVA italiani con **carattere di controllo errato** | 8.016 | 527.722 identificativi distinti | 1,52% |
| CD-03 | Importo del lotto nullo o negativo (delta di ottobre) | 377 | 565.864 | 0,07% |
| AG-02 · AT-03 · CU-01 · CD-01 | CIG non valido | 17 · 16 · 13 · 3 | milioni | ≈0% |

### 3.2 Incongruenze da chiarire

Possono avere una spiegazione procedurale, ma chi riusa i dati non ha modo di saperlo.

| ID | Problema | Casi | |
|---|---|---|---|
| AG-05 | Esito **comunicato prima dell'aggiudicazione definitiva** | 225.914 | 4,6% |
| AG-08 | Importo di aggiudicazione pari a zero | 19.067 | 0,39% |
| AG-09 | Importo pari o superiore a un miliardo di euro | 298 | da verificare uno per uno |
| AG-03d | Data di aggiudicazione definitiva mancante | 42.479 | 0,87% |

### 3.3 Campi codificati che accettano testo libero

Il problema non sono i singoli valori, ma l'assenza di validazione all'inserimento.

**Il CUP nel dataset `cup`.** Su 7.228.216 righe, 1.955.119 non contengono un CUP ben formato:

| Contenuto del campo | Righe |
|---|---|
| `ND` | **1.951.844** |
| altro testo libero o codice malformato | 2.013 |
| CUP valido ma con spazi o minuscole | 942 |
| `NON APPLICABILE` | 632 |
| più CUP o note nello stesso campo, per esempio `I53D23002750001 € 454,55 I53D23002620006 € 277,27` | 80 |

Conseguenza pratica: dei 7.103.635 CIG presenti nel dataset, quelli con almeno un CUP valido sono
**5.149.498, il 72,5%**. Chi conta le righe sovrastima i collegamenti di un quarto.

**Gli identificativi degli aggiudicatari.** 2.012 campi `codice_fiscale` contengono più identificativi
o annotazioni, per esempio `C.F. … - P. IVA …`.

### 3.4 Convenzioni non documentate

Non sono errori, ma senza documentazione rompono i collegamenti con IndicePA, il Registro Imprese e
le altre basi dati pubbliche.

| ID | Convenzione | Casi |
|---|---|---|
| SA-02 | **Codici fiscali sintetici `CFAVCP-…`** per stazioni appaltanti senza codice fiscale proprio, per lo più centrali uniche di committenza. 1.194 sono attive | 1.282 su 48.040 |
| SA-03 | Partita IVA **`00000000000`** al posto del valore mancante | 24.818 su 48.040 (51,7%) |
| SA-05 | Data di fine **`2099-12-31`** come "ancora attivo" | 48.040 su 48.040 |
| AG-13 | **Criterio di aggiudicazione mancante** | 3.226.120 su 4.862.077 (66,4%) |
| — | **Due vocabolari coesistenti** per lo stesso campo: `PREZZO PIU' BASSO` accanto a `OFFERTA ECONOMICAMENTE PIÙ VANTAGGIOSA: CRITERIO DEL MINOR PREZZO`; `IMPRESA` accanto a `IMPRESA SINGOLA (…)`, `DITTA INDIVIDUALE`, `MONOSOGGETTIVO` | — |

### 3.5 Un'assenza di schema: gli operatori esteri

Il dataset `aggiudicatari` non ha un campo per il paese dell'operatore né per il tipo di
identificativo. Gli operatori stranieri finiscono quindi in `codice_fiscale` con formati eterogenei:

| Forma dell'identificativo | Distinti |
|---|---|
| Codice fiscale o partita IVA italiani validi | 483.510 (91,6%) |
| Identificativo IVA con prefisso del paese, per esempio `ATU…`, `IE…` | 6.449 |
| 9-10 cifre: identificativi esteri o italiani troncati, non distinguibili | 10.214 |
| Altri formati: identificativi nazionali esteri, per esempio `G62060421` per la Spagna | 17.521 |

Per chi studia **a quali paesi vanno gli appalti pubblici italiani** — cioè per questo progetto, ma
anche per qualunque analisi sul mercato unico europeo — è un'informazione essenziale, ed è oggi
ricostruibile solo per euristica.

---

## Richieste

In ordine di impatto per chi riusa i dati.

1. **Ripristinare la pubblicazione OCDS**, o dichiararne pubblicamente la sospensione con una data di
   ripresa.
2. **Non rimuovere i delta storici**, oppure pubblicare un archivio permanente, e **dichiarare la
   politica di conservazione**.
3. **Pubblicare il file dell'anno in corso**, aggiornato insieme ai delta, così che lo stato corrente
   non dipenda dall'aver scaricato ogni mese.
4. **Documentare l'API CKAN** e dichiarare formalmente dismessa l'API REST OCDS, o ripristinarla.
5. **Esporre `ETag` e pubblicare i checksum** di ogni risorsa.
6. **Consentire l'accesso automatico ai dati aperti** senza blocchi sugli IP cloud e sullo user-agent,
   eventualmente con un limite di frequenza dichiarato.
7. **Validare in inserimento i campi codificati**: un CUP assente è un valore nullo, non `ND`; un campo
   codice fiscale contiene un identificativo, non note.
8. **Documentare le convenzioni** — i codici `CFAVCP-…`, la partita IVA `00000000000`, la data `2099` —
   e indicare per le centrali di committenza il codice fiscale degli enti aderenti.
9. **Aggiungere paese e tipo di identificativo** per gli operatori economici esteri.
10. **Correggere le chiavi duplicate e i riferimenti orfani** fra `aggiudicazioni` e `aggiudicatari`.
11. **Pubblicare i mesi mancanti** di `smartcig`, giugno e luglio 2026, e ripristinare la
    distribuzione JSON, interrotta da agosto 2026.
12. **Correggere il campo `size`** del catalogo, perché descriva la distribuzione scaricabile e non il
    file scompattato.

Siamo disponibili a fornire gli elenchi completi dei record interessati da ciascun controllo e a
ripetere la rilevazione dopo eventuali correzioni.

---

## Appendice A — I file analizzati

Scaricati il 26 ottobre 2026 da `https://dati.anticorruzione.it/opendata/download/dataset/`.

| Risorsa | Byte | Last-Modified | sha256 |
|---|---|---|---|
| `stazioni-appaltanti/filesystem/stazioni-appaltanti_csv.zip` | 3.131.101 | 13/10/2026 | `fa27841b2379bb07cd1dfcab334ea85e4bc92472571a93dca4db450efb8804f8` |
| `cup/filesystem/cup_csv.zip` | 82.859.488 | 13/10/2026 | `d83b0d42e6574eed3c26de59d6ffc124c0ce4756b5d34013e7bbe31daafb39cb` |
| `aggiudicazioni/filesystem/aggiudicazioni_csv.zip` | 151.402.917 | 15/01/2026 | `70f2e7ccad625f3db3d3a2285c65aaa8eac35bf70b25570774224ac869f8d631` |
| `aggiudicatari/filesystem/aggiudicatari_csv.zip` | 151.222.321 | 23/01/2026 | `6908a361f581824ce144414116301234fc113230230634b0942b988f9173d60f` |
| `cig/filesystem/20261001-cig_csv.zip` | 107.879.691 | 05/10/2026 | `204f820f5222f6c975c45998b2bd8f69bec0ca90a4cbeea55e7a25ec09c0924a` |

## Appendice B — Tutti i controlli

L'elenco completo, con esempi, sta in [`integrita-2026-10-26.json`](integrita-2026-10-26.json).
