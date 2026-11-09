# Accesso civico massivo (L7): elenco dei mancanti, piattaforme riusabili, punti normativi

**Bozza 0.1 del 9/11/2026 (#58).** Documento preparatorio. **Nessuna richiesta è stata generata né inviata;
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
   decidere in 20; difensore civico 30; TAR 30 giorni (art. 116 c.p.a. [R per il termine, da archiviare]).
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
| 3.5 | Difensore civico per regioni ed enti locali, territoriale o di ambito superiore; si pronuncia in 30 giorni; se l'ente non conferma il diniego entro 30 giorni, l'accesso è consentito (art. 5 c. 8). TAR ex art. 116 c.p.a. contro la decisione (art. 5 c. 7) | [V]; termine di 30 giorni per il ricorso al TAR [R, da archiviare l'art. 116] |
| 3.6 | Richieste massive: accolte anche per un numero cospicuo di documenti, salvo manifesta irragionevolezza (carico che compromette il buon andamento), da provare e motivare; prima la PA deve aiutare a ridefinire la domanda; può valutare l'impatto cumulativo di più domande dello stesso soggetto in un periodo limitato; può non rispondere a una richiesta identica già soddisfatta (circ. 2/2017 § 7 lett. d, § 8) | [V] |
| 3.7 | Limiti: interessi economici e commerciali, inclusi proprietà intellettuale, diritto d'autore e segreti commerciali (art. 5-bis c. 2 lett. c): pertinente per offerte tecniche e listini; accesso parziale e differimento obbligatori se bastano (c. 4-5) | [V] |
| 3.8 | Identificazione: istanza valida se inviata dal proprio domicilio digitale iscritto (INI-PEC/INAD) o, in mancanza, da una PEC, che vale come elezione di domicilio digitale speciale (art. 65 c. 1 lett. c-bis CAD, vigente). La circ. 2/2017 § 3.3 cita la versione precedente («propria casella PEC») | [V] |
| 3.9 | Gratuità, salvo il rimborso dei costi di riproduzione su supporti materiali; nessun costo per l'invio via PEC (circ. 1/2019 § 4) | [V] |
| 3.10 | Registro degli accessi pubblico, preferibilmente trimestrale (circ. 2/2017 § 9) | [V]: utile per verificare che le nostre istanze siano registrate |
| 3.11 | Limiti di invio dei gestori PEC: policy Aruba citata da terzi con 250 destinatari per messaggi di contenuto analogo; altre fonti 500 destinatari per invio, Poste 200 invii al giorno | [R]: non verificato (la copia della policy non è scaricabile); da verificare sul contratto della casella di Fabio prima di qualunque invio |

## 4. Prossimi passi (proposti, non avviati)

1. Fabio: tetto per richiesta (proposta 20), cadenza delle ondate, ondata 0 di prova, scelta Froide o registro nostro.
2. RPCT e ufficio competente per i primi enti (da AT); ricerca della PEC per i 775 enti senza.
3. Limiti della casella PEC che si userà (contratto del gestore).
4. Archiviare l'art. 116 c.p.a. e la circolare 2/2017 dalla GU.

## Registro revisioni

| Versione | Data | Autore | Modifiche |
|---|---|---|---|
| 0.1 bozza | 9/11/2026 | Claude (agente) | Prima stesura: elenco unico (28.807 voci, 6.626 enti), confronto Froide/Alaveteli/progetti italiani, punti normativi su fonti archiviate. |
