# Accesso civico massivo (L7): elenco dei mancanti, piattaforme riusabili, punti normativi

**Bozza 0.3 del 9/11/2026 (#58).** Documento preparatorio. **Nessuna richiesta è stata inviata (le bozze dell'ondata 0 sono solo generate, § 3bis; l'adattatore PEC, § 3ter, è stato provato solo in modalità secca su messaggi di esempio);
nessun contatto con enti o terzi; nessuna registrazione o login.**

**Legenda.** **[V]** = verificato da noi sulla fonte primaria (testo archiviato in
[`prove-normativa/`](prove-normativa/), sha256 in `SHA256SUMS`) o misurato da noi (codice e dati citati).
**[R]** = riferito da terzi, *da verificare*.

## Sintesi

- **Elenco unico [V, misurato]:** 28.807 voci = 756 documenti mancanti delle convenzioni + 28.051 CIG del residuo
  dell'imbuto dopo L0-L6 (esclusi 532 CIG per cui un documento che cita il CIG è già stato trovato). Valore dei CIG
  del residuo: 25,3 mld € (importi ANAC, con i limiti noti sugli importi dei padri AQ e sui doppioni, R53).
  **6.626 enti** distinti; 775 enti (3.485 voci) senza PEC in IndicePA per quel codice fiscale.
- **Concentrazione:** 3.261 enti con 1 voce, 2.394 con 2-5, 716 con 6-20, 242 con 21-100, 13 con oltre 100
  (massimo 520, Trenitalia; Consip 419).
- **Ondate:** una richiesta per ente per ondata. La prima ondata tocca tutti i 6.626 enti; con un tetto di 20 voci
  per richiesta servono 7.103 richieste in tutto e 26 ondate per esaurire l'ente più carico; con tetto 50, 6.719 e 11.
  L'ondata 2 riguarda 255 enti (tetto 20) o 60 (tetto 50).
- **Piattaforma:** raccomandazione **Froide** (MIT, Python/Django, mantenuta, ha progetti multi-ente, scadenze per
  legge, mediatore e posta in entrata), con un **adattatore PEC** nostro e il calendario dei termini italiani.
  Alaveteli (AGPL) è la seconda scelta; l'istanza italiana su Alaveteli (Diritto di Sapere) risulta dismessa.
- **Norme [V]:** 30 giorni, controinteressati 10 giorni con sospensione, riesame RPCT 20 giorni, difensore civico
  30 giorni (regioni ed enti locali), TAR ex art. 116 c.p.a.; identificazione con PEC valida (art. 65 c. 1 lett. c-bis
  CAD); le richieste massive vanno accolte salvo manifesta irragionevolezza motivata, **e la PA può valutare l'impatto
  cumulativo di più domande dello stesso soggetto** (circ. FP 2/2017 § 7 lett. d): il tetto per ente e le ondate
  servono proprio a questo.

## 1. Elenco unico dei documenti mancanti

### 1.1 Codice e uscite

- `tools/accesso_civico/elenco_mancanti.py` (generatore) e `tools/accesso_civico/verifica_elenco.py` (verifica
  V1-V7, tutte superate il 9/11: `esiti/2026-11-09/accesso-civico/verifica.json`).
- Uscite in `esiti/2026-11-09/accesso-civico/`: `elenco-mancanti.csv.gz` (una riga per documento mancante; il CSV
  in chiaro di ~20 MB resta sul server, non versionato), `enti.csv` (accorpamento per ente), `stima-ondate.json`.
- Uso (server): `nice .venv/bin/python tools/accesso_civico/elenco_mancanti.py 2026-11-09` poi
  `.venv/bin/python tools/accesso_civico/verifica_elenco.py 2026-11-09`. Zero token, ~3 minuti.

### 1.2 Fonti unite

| Fonte | File | Voci |
|---|---|---|
| A. Convenzioni (#62) | `report/convenzioni/database/documenti-mancanti.csv` (gli scartati sono già fuori, in `documenti-mancanti-scartati.csv`) | 756 |
| B. Residuo imbuto (#57) | `lavoro/residuo-s6/ingresso.csv` (P1-P5), esiti L3/MePA `out/esiti.jsonl`, L4 `l4/esiti.jsonl`, materiale da `esiti/2026-11-09/imbuto/residuo-s6-per-66.csv`, strato/sottoclasse da `lavoro/imbuto/ict.csv` | 28.583 − 532 = 28.051 |

**Escluso perché pubblicato:** i 532 CIG con «documento-cita-cig». Restano dentro, con criticità ridotta di 1, i
4.030 CIG con sola pagina che cita il CIG e i 1.414 con documenti che non lo citano: l'atto non l'abbiamo.

### 1.3 Colonne

`fonte, id, cig, cf, codice_ipa, ente, pec, pec_fonte, rpct, oggetto, documento_atteso, importo, anno, criticita,
peso_valore, priorita, livelli_tentati, esito_livelli, note`.

- **CF:** `cf_amministrazione_appaltante` ANAC del CIG; per le iniziative senza CIG, Consip (05359681003) o il CF
  trovato per il nome della stazione appaltante. PSN lasciato senza CF: il destinatario è la Presidenza del
  Consiglio, che ha una bozza dedicata. 7 voci senza CF.
- **Codice IPA e PEC:** IndicePA `amministrazioni.txt` del mirror (6/11/2026), prima mail di tipo «Pec». 3.475 voci
  senza codice IPA: sono soprattutto società e stazioni appaltanti non censite in IndicePA con quel CF.
- **RPCT:** IndicePA **non** lo riporta (i campi `nome_resp`/`cogn_resp` sono il responsabile dell'ente). Colonna
  vuota: va presa dalla sezione Amministrazione trasparente al momento della preparazione (#58, fase successiva).
- **Documento atteso:** per i CIG, atto di affidamento/aggiudicazione e contratto o ordinativo relativo al CIG, con
  il dettaglio che serve all'analisi secondo la sottoclasse (licenze: prodotti e marchi; cloud/PSN: servizio,
  provider, region; altrimenti beni/servizi, marchi, eventuale cloud). Per le convenzioni, la descrizione
  dell'inventario (documento e contenuto presunto).
- **Livelli tentati ed esito:** per B, L0-L2 (imbuto/PVL), L3 o MePA, L4 con l'esito registrato e il «materiale»;
  per A, metodo, pagina, dietro_login ed evidenza dell'inventario.
- **Priorità** = criticità × peso del valore. Criticità: A dall'inventario (1-3); B dalla classe (P1 incerti ICT 3,
  P3 G2 informazione mancante 3, P2 G3 2, P4 nuovi RX 2, P5 G4 campione 1). Peso = 1 + log10(1 + importo/100.000),
  al massimo 5. Per le convenzioni l'importo è il valore ICT 2024-2025 dell'iniziativa. Scelta da rivedere con Fabio.

### 1.4 Numeri [V, misurato il 9/11/2026]

| | Voci |
|---|---|
| A criticità 3 / 2 / 1 | 414 / 123 / 219 |
| B criticità 3 / 2 / 1 | 1.908 / 20.393 / 5.750 |
| Enti | 6.626 (2 senza CF) |
| Enti senza PEC IndicePA | 775 (3.485 voci) |
| Enti con almeno una voce di priorità ≥ 10 | 61 |

Primi enti per priorità complessiva: Consip (419 voci), Trenitalia (520), ESTAR Toscana (148), Azienda sanitaria
dell'Alto Adige (240), ASST Fatebenefratelli Sacco (213), Policlinico di Bari (159), RFI (145), CNR (197),
ASL 5 Spezzino (141), Intercent-ER (65).

### 1.5 Stima delle ondate (una richiesta per ente per ondata)

| Tetto voci per richiesta | Richieste totali | Ondata 1 | Ondata 2 | Ondata 3 | Ondate per esaurire |
|---|---|---|---|---|---|
| 5 | 9.879 | 6.626 | 971 | 521 | 104 |
| 10 | 7.932 | 6.626 | 521 | 255 | 52 |
| 20 | 7.103 | 6.626 | 255 | 90 | 26 |
| 50 | 6.719 | 6.626 | 60 | 13 | 11 |

Lettura: l'onere è nella prima ondata (tutti gli enti, perlopiù con 1-5 voci); la coda è fatta di poche decine di
enti grandi. Proposta da discutere: ondata 0 di prova su 20-50 enti; poi ondate per priorità, con tetto 20 e una
richiesta per ente ogni 30-45 giorni (dopo la risposta o la scadenza), per non offrire l'argomento del carico
cumulativo (§ 3.6). Le voci senza PEC richiedono prima la ricerca dell'indirizzo (AT dell'ente).

## 2. Piattaforme riusabili

Verifiche del 9/11/2026 da API GitHub e dal codice sorgente [V]; il resto [R].

| | Froide (Open Knowledge Foundation Deutschland, FragDenStaat) | Alaveteli (mySociety, WhatDoTheyKnow) |
|---|---|---|
| Licenza | MIT [V] | AGPL-3.0 [V, LICENSE.txt] |
| Stack | Python/Django, Celery [V]; PostgreSQL, Elasticsearch [R] | Ruby on Rails [V]; PostgreSQL, Xapian [R] |
| Manutenzione | ultimo push 6/11/2026, rilascio continuo senza tag [V] | ultimo push 9/11/2026, rilascio 0.46.0.0 del 10/11/2025 [V] |
| Campagne di massa | `FoiProject`: una richiesta a molti enti (`froide/foirequest/models/project.py`) [V]; moduli `froide-campaign` e `froide-legalaction` (MIT, attivi ottobre 2026) [V] | `InfoRequestBatch`: richieste in lotti [V]; in pratica riservato agli utenti Pro [R] |
| Posta in entrata | indirizzo dedicato per richiesta, smistamento delle risposte, gestione bounce (`froide/bounce`) [V] | indirizzo dedicato per richiesta, smistamento [R] |
| Scadenze | per legge: `FoiLaw.max_response_time` + unità, `calculate_due_date`, richieste scadute [V] | globale: `REPLY_LATE_AFTER_DAYS` 20, `REPLY_VERY_LATE_AFTER_DAYS` 40, giorni lavorativi o di calendario [V] |
| Riesame / ricorsi | `FoiLaw.mediator` (organo di mediazione), modulo azioni legali [V] | ricorso interno come stato della richiesta [R] |
| Pubblicità | pensato per pubblicare le richieste; si può tenere privato [R] | idem [R] |

**Progetti italiani.**
- *Diritto di Sapere* usava Alaveteli (tema `mysociety/dirittodisapere-theme`, MIT, ultimo push 1/7/2020 [V]).
  Il 9/11/2026 `chiedi.dirittodisapere.it` e `www.dirittodisapere.it` mostrano una pagina di dominio parcheggiato
  («registrato con mvmnet.com») [V]: l'istanza italiana non è più attiva.
- *FOIA4Italy*: coalizione della società civile (2014-2016), sito attivo, oggi raccoglie esperienze e proposte di
  riforma [V, meta del sito]; non risulta un software di invio [R].
- Su GitHub non risultano altri strumenti italiani di invio massivo; solo dataset di risposte (es.
  `maidati/RisposteRegioni22`, CC0) [V, ricerca del 9/11].
- Portale FOIA della Funzione Pubblica (foia.gov.it): non raggiungibile dal server il 9/11 [V]; ruolo da rivedere.

**Cosa serve in ogni caso per l'Italia (nostro adattatore):**
1. **PEC al posto della mail:** invio SMTP/IMAP sulla casella PEC di Fabio (non un indirizzo per richiesta: le PEC
   non si moltiplicano a costo zero), abbinamento della risposta con identificativo nell'oggetto e nel corpo;
   acquisizione delle ricevute di accettazione e consegna (`daticert.xml`) e delle mancate consegne come eventi del
   registro (già impostato in `tools/trasparenza/pec.py`, registro append-only).
2. **Calendario dei termini:** 30 giorni dalla ricezione (data della ricevuta di consegna, circ. 2/2017 § 5.1);
   sospensione fino a 10 giorni per controinteressati; riesame da chiedere entro 30 giorni (circ. 1/2019 § 7) e da
   decidere in 20; difensore civico 30; TAR 30 giorni (art. 116 c. 1 c.p.a. [V], § 3ter).
3. **Destinatari:** enti da IndicePA (CF, codice IPA, PEC), RPCT e ufficio indicato in AT, difensore civico
   territoriale per regioni ed enti locali.
4. **Riservatezza:** il nostro uso è interno finché Fabio non decide; Froide va configurato senza pubblicazione.

**Raccomandazione.** Froide come base: licenza permissiva, stesso linguaggio dei nostri strumenti (Python), modello
dei dati già con progetti multi-ente, leggi con termini e mediatore. Alternativa leggera, da valutare prima: tenere
il nostro registro append-only e gli script esistenti e prendere da Froide solo il modello (stati, eventi,
scadenze), se l'installazione completa (Elasticsearch, Celery, interfaccia pubblica) risulta sproporzionata per un
solo richiedente. Decisione di Fabio.

## 3. Punti normativi

Fonti archiviate il 9/11/2026: `dlgs33-art5.html` (già presente), `dlgs33-art5bis.html`, `cad-art65.html`
(Normattiva, testo vigente), `fp-circolare-2-2017.pdf` (copia da unicas.it), `fp-circolare-1-2019.pdf` (copia
dalla sezione AT della Regione Abruzzo). Le circolari sono copie di terzi del testo ufficiale: contenuto [V],
provenienza da confrontare con la GU o il sito della Funzione Pubblica.

| # | Punto | Esito |
|---|---|---|
| 3.1 | Istanza senza motivazione né legittimazione; deve identificare i dati o documenti; telematica secondo il CAD; a ufficio che detiene i dati, URP, altro ufficio indicato in AT, RPCT solo per dati a pubblicazione obbligatoria (art. 5 c. 3) | [V] |
| 3.2 | Termine: provvedimento espresso e motivato entro 30 giorni dalla presentazione (art. 5 c. 6); non ammesso il silenzio-diniego (circ. 2/2017 § 5); il termine decorre dalla ricezione, non dal protocollo (§ 5.1) | [V] |
| 3.3 | Controinteressati: comunicazione; opposizione motivata entro 10 giorni; termine sospeso (art. 5 c. 5); se accolto nonostante l'opposizione, consegna non prima di 15 giorni (c. 6) | [V] |
| 3.4 | Riesame al RPCT su diniego o mancata risposta, decisione entro 20 giorni; sentito il Garante (10 giorni) per i dati personali (art. 5 c. 7); da proporre entro 30 giorni dalla decisione (circ. 1/2019 § 7, interpretazione, non norma) | [V] |
| 3.5 | Difensore civico per regioni ed enti locali, territoriale o di ambito superiore; si pronuncia in 30 giorni; se l'ente non conferma il diniego entro 30 giorni, l'accesso è consentito (art. 5 c. 8). TAR ex art. 116 c.p.a. contro la decisione (art. 5 c. 7) | [V]; termine di 30 giorni per il ricorso al TAR [V] (`cpa-art116.html`, § 3ter) |
| 3.6 | Richieste massive: accolte anche per un numero cospicuo di documenti, salvo manifesta irragionevolezza (carico che compromette il buon andamento), da provare e motivare; prima la PA deve aiutare a ridefinire la domanda; può valutare l'impatto cumulativo di più domande dello stesso soggetto in un periodo limitato; può non rispondere a una richiesta identica già soddisfatta (circ. 2/2017 § 7 lett. d, § 8) | [V] |
| 3.7 | Limiti: interessi economici e commerciali, inclusi proprietà intellettuale, diritto d'autore e segreti commerciali (art. 5-bis c. 2 lett. c): pertinente per offerte tecniche e listini; accesso parziale e differimento obbligatori se bastano (c. 4-5) | [V] |
| 3.8 | Identificazione: istanza valida se inviata dal proprio domicilio digitale iscritto (INI-PEC/INAD) o, in mancanza, da una PEC, che vale come elezione di domicilio digitale speciale (art. 65 c. 1 lett. c-bis CAD, vigente). La circ. 2/2017 § 3.3 cita la versione precedente («propria casella PEC») | [V] |
| 3.9 | Gratuità, salvo il rimborso dei costi di riproduzione su supporti materiali; nessun costo per l'invio via PEC (circ. 1/2019 § 4) | [V] |
| 3.10 | Registro degli accessi pubblico, preferibilmente trimestrale (circ. 2/2017 § 9) | [V]: utile per verificare che le nostre istanze siano registrate |
| 3.11 | Limiti di invio dei gestori PEC: policy Aruba citata da terzi con 250 destinatari per messaggi di contenuto analogo; altre fonti 500 destinatari per invio, Poste 200 invii al giorno | [R]: non verificato (la copia della policy non è scaricabile); da verificare sul contratto della casella di Fabio prima di qualunque invio |

## 3bis. Modelli, registro e ondata 0 (0.2, 9/11/2026) — NESSUN INVIO

Invio deciso da Fabio (DECISIONI.md 2026-11-09): PEC istituzionale IndicePA (protocollo/URP), testo indirizzato
all'ufficio che detiene i dati (art. 5 c. 3 lett. a). Richiedente, casella PEC, tetto e ondate restano da decidere:
i valori usati sono **proposte** in `config/accesso-civico/parametri.yaml`.

- **Modelli** (`config/accesso-civico/modelli/`, Markdown con variabili `{{ }}` compatibili Jinja; Jinja non è
  installato, il riempimento è in `bozze.py`): `istanza.md`, `sollecito.md`, `chiarimento.md`, `riesame-diniego.md`,
  `riesame-silenzio.md`, `difensore-civico.md`. Ogni modello elenca in testa le norme citate e il file di
  `prove-normativa/` su cui sono state verificate [V]; i tre punti allora [R] (proroga dei termini festivi, 4 ottobre,
  art. 116 c.p.a.) sono stati verificati nella 0.3 (§ 3ter)
- **Registro** append-only (`schemi/accesso-civico-richiesta.schema.json`, `schemi/accesso-civico-evento.schema.json`)
  e macchina a stati `tools/accesso_civico/stati.py`: stati bozza, approvata, inviata, consegnata,
  sospesa-controinteressati, chiarimento, accolta, parziale, diniego, silenzio, riesame, difensore,
  difensore-conferma, chiusa, annullata. Lo stato si ricalcola dagli eventi; silenzio e «accesso consentito» dopo il
  difensore (art. 5 c. 8) sono derivati dalla data. Termini: 30 gg dalla consegna PEC (+ giorni di sospensione per i
  controinteressati), riesame 20 gg (+10 Garante), presentazione del riesame 30 gg (circ. 1/2019, interpretazione),
  difensore 30 + 30 gg. Scelte prudenti: il chiarimento **non** riavvia il termine; un solo riesame. 16 test
  (`.venv/bin/python -m unittest tests/test_accesso_civico_stati.py`).
- **Generatore** `tools/accesso_civico/bozze.py <data> --ondata <nome> [--tetto N] [--proponi N | --enti cf,...]`:
  una richiesta per ente, voci in ordine di priorità fino al tetto, PEC IndicePA (ripiego su `destinatari.csv` con
  attendibilità); testi e JSON in `lavoro/accesso-civico/<ondata>-bozze/` (non in git), evento «creazione»
  nel registro, riepilogo committato in `esiti/<data>/accesso-civico/<ondata>/`. Le note di lavoro dell'elenco
  («i documenti pubblicati trovati non citano il CIG» ecc.) non passano nel testo.
- **Ondata 0 di prova [V, misurato]:** 30 enti, 501 voci (70 di convenzioni), 4,15 mld € di importi ANAC, 1.049 voci
  oltre il tetto rinviate; 24 tipologie IPA, 12 regioni; difensore civico competente per 13 enti. Selezione proposta:
  6 enti con convenzioni (quota 8: gli altri hanno già una bozza «mancanti-*» o non sono «Pubbliche Amministrazioni»
  in IPA) + 24 dal residuo, a turno per tipologia (massimo 3 per tipologia). Escluse società e gestori (ambito
  dell'art. 2-bis da verificare caso per caso). Elenco in `esiti/2026-11-09/accesso-civico/ondata-0/riepilogo.md`.

## 3ter. Punti normativi chiusi e adattatore PEC (0.3, 9/11/2026) — NESSUN INVIO

### 3ter.1 Tre punti verificati su fonte primaria [V]

Testi archiviati il 9/11/2026 da Normattiva (testo vigente, articolo singolo) e GU, in `prove-normativa/` con
`SHA256SUMS` e nell'archivio content-addressed (`tools/archivia.py --da-file … --url …`):
`cc-art2963.html`, `cpc-art155.html`, `cpa-art52.html`, `cpa-art116.html`, `l241-art2.html`, `l260-1949-art1.html`,
`l260-1949-art2.html`, `l151-2025.html`, `gu-l151-2025.html`.

| # | Punto | Esito |
|---|---|---|
| 3ter.a | **Proroga dei termini che scadono in giorno festivo** | Art. 2963 c. 3 c.c. (termini di prescrizione): «prorogato di diritto al giorno seguente non festivo» [V]. Art. 155 c. 4 c.p.c.: stessa regola; c. 5: anche il **sabato**, ma solo per gli atti processuali fuori udienza [V]. Art. 52 c. 3 e 5 c.p.a.: stessa regola per i termini del processo amministrativo, sabato compreso [V]. **L. 241/1990 e d.lgs. 33/2013 non contengono una regola propria** (art. 2 L. 241 archiviato: fissa i termini, non il computo) [V]: l'applicazione al procedimento amministrativo è un principio generale di origine giurisprudenziale [interpretazione, non norma]. Scelta in `stati.py`: proroga applicata a tutti i termini, sabato non festivo (tranne il ricorso al TAR); per prudenza i nostri atti (riesame) vanno fatti entro la data non prorogata. |
| 3ter.b | **4 ottobre festivo dal 2026** | L. 8 ottobre 2025, n. 151, «Istituzione della festa nazionale di San Francesco d'Assisi», GU SG n. 236 del 10/10/2025, **in vigore dal 1/1/2026** [V, Normattiva e GU]; inserisce il 4 ottobre nell'art. 2 della L. 260/1949 (testo vigente archiviato) [V]. Il 2 giugno è festa nazionale per l'art. 1 L. 260/1949 [V]. Il 4 novembre resta nel testo dell'art. 2 ma non è festivo dalla L. 54/1977 [R, non archiviata]. Calendario di `stati.py` invariato nei valori, fonti ora [V]. |
| 3ter.c | **Art. 116 c.p.a., termine per il ricorso** | Testo vigente (dal 20/4/2013): ricorso «entro trenta giorni dalla conoscenza della determinazione impugnata o dalla formazione del silenzio», esteso dal d.lgs. 33/2013 alla «tutela del diritto di accesso civico» [V]. `stati.py` 0.2: termine `ricorso_tar` = 30 gg, funzione `termine_tar` (proroga anche del sabato, art. 52 c. 5), indicato nella prossima azione dopo il riesame/difensore. |

Test: 19 su `stati.py` (3 nuovi sulle fonti verificate: 4 ottobre dal 2026, 2 giugno/1 novembre/4 novembre, TAR).

### 3ter.2 Adattatore PEC `tools/accesso_civico/pec.py` 0.1 (solo libreria standard)

- **Modalità secca di default**: nessuna connessione. La modalità reale richiede insieme `--reale` e `PEC_REALE=1`;
  credenziali **solo** da variabili d'ambiente (`PEC_UTENTE`, `PEC_PASSWORD`, `PEC_MITTENTE`, `PEC_SMTP_HOST`,
  `PEC_IMAP_HOST`, porte 465/993). In secca il registro vero non si tocca: gli eventi vanno in `eventi-secca.jsonl`.
- **`invia <cartella-bozze>`**: solo richieste nello stato «approvata» (evento di Fabio); oggetto e testo dalla bozza
  `<id>.md` (l'oggetto deve contenere il codice `rif. ac-…`, che serve all'abbinamento); **allegato obbligatorio**
  `<id>.pdf.p7m` (firmato) o `<id>.pdf`, altrimenti la richiesta è saltata; Message-ID con il codice della
  richiesta; SMTP-SSL; ogni messaggio archiviato come `.eml` con sha256; evento «invio» con sha256, percorso e
  Message-ID. **Tetto giornaliero** (contato dagli «invio» già registrati nel giorno) e **intervallo** fra due invii
  parametrici (`parametri.yaml`, sezione `pec`: proposte 20/giorno e 120 s).
- **`leggi <cartella-bozze>`**: in secca solo da file `.eml` (`--da-cartella`); in reale IMAP-SSL in sola lettura
  (EXAMINE e `BODY.PEEK`: nessun flag, nessuna cancellazione), ripartibile dall'ultimo UID. Riconosce le ricevute
  secondo le regole tecniche (DM 2/11/2005, allegato al DPR 68/2005): header `X-Ricevuta`,
  `X-Riferimento-Message-ID`, allegato `daticert.xml` (tipo, errore, giorno/ora/zona, identificativo, msgid,
  consegna, errore-esteso), controllando che header e `daticert.xml` coincidano; riconosce le buste di trasporto
  (`X-Trasporto: posta-certificata`) e ne apre il `postacert.eml`. Abbinamento: Message-ID dell'invio
  (`X-Riferimento-Message-ID`, `In-Reply-To`, `References`), poi codice `ac-…` nell'oggetto o nel testo.
- **Eventi registrati**: avvenuta-consegna -> «consegna» con la data di `daticert.xml` (da qui partono i 30 giorni);
  errore-consegna e preavviso di mancata consegna -> «mancata-consegna» (la richiesta torna «approvata»);
  accettazione/presa in carico -> solo giornale. **Le risposte degli enti non generano eventi**: vanno nella coda
  «da-esaminare» del giornale, perché l'esito (accolta/parziale/diniego) va letto da una persona. Ricevute
  incoerenti, non abbinate o in uno stato inatteso: nessun evento, «da esaminare». Idempotente (sha256).
- **Limite dichiarato**: la firma S/MIME delle ricevute **non è verificata** (la libreria standard non lo consente):
  annotato in ogni riga del giornale. Prima dell'uso reale: verifica con `openssl smime -verify` sui `.eml`
  archiviati, se Fabio lo ritiene necessario.
- **Archivio** (non in git, dati personali): `lavoro/accesso-civico/pec/{secca,reale}/blobs/<aa>/<sha256>.eml`
  e `giornale.jsonl`.
- **Test** (`.venv/bin/python -m unittest tests/test_accesso_civico_pec.py`, 8 test, nessuna connessione): sette
  messaggi costruiti a mano in `tests/dati/pec/` (accettazione, avvenuta consegna, busta con risposta dell'ente,
  errore di consegna, ricevuta con `daticert.xml` incoerente, busta abbinata solo per codice, messaggio estraneo);
  SMTP finto per tetto, intervallo, allegato e Message-ID; secca che non tocca il registro; `--reale` rifiutato
  senza `PEC_REALE=1`.
- Rispetto a `tools/trasparenza/pec.py` (registro manuale degli invii art. 9): stesso schema di eventi; il
  riconoscimento delle ricevute di `pec.py` (#58) potrebbe essere riusato là (proposta, non fatto).

## 4. Prossimi passi (proposti, non avviati)

1. Fabio: richiedente e casella PEC, tetto per richiesta (proposta 20), cadenza delle ondate, approvazione (o modifica) dei 30 enti dell'ondata 0 e dei modelli, scelta Froide o registro nostro (il registro nostro, § 3bis, basta per l'ondata 0).
2. RPCT e ufficio competente per i primi enti (da AT); ricerca della PEC per i 775 enti senza.
3. Limiti della casella PEC che si userà (contratto del gestore).
4. Archiviare la circolare 2/2017 dalla GU (l'art. 116 c.p.a. è archiviato, § 3ter).
5. Fabio: casella PEC e suoi limiti, credenziali in ambiente sul server, tetto giornaliero e intervallo dell'adattatore
   (`parametri.yaml`, sezione `pec`), firma digitale dell'istanza (allegato `<id>.pdf.p7m`), poi approvazione per richiesta.

## Registro revisioni

| Versione | Data | Autore | Modifiche |
|---|---|---|---|
| 0.1 bozza | 9/11/2026 | Claude (agente) | Prima stesura: elenco unico (28.807 voci, 6.626 enti), confronto Froide/Alaveteli/progetti italiani, punti normativi su fonti archiviate. |
| 0.2 bozza | 9/11/2026 | Claude (agente) | § 3bis: sei modelli con norme verificate, schemi e macchina a stati con scadenze e test, generatore di bozze, ondata 0 di prova (30 enti, 501 voci), nessun invio. |
| 0.3 bozza | 9/11/2026 | Claude (agente) | § 3ter: proroga dei termini festivi, 4 ottobre (L. 151/2025) e art. 116 c.p.a. verificati su Normattiva/GU (9 testi archiviati); `stati.py` 0.2 con termine TAR e 19 test; adattatore PEC `pec.py` 0.1 (secca di default, solo libreria standard, 8 test su .eml di esempio), nessun invio. |
