# Scheda normativa: accessibilità dei documenti di gara dal link PVL

Versione 1.0 del 4/11/2026 (#63). Riguarda il campo PVL `documenti_di_gara_link` (vedi
[`acquisizione/dettaglio-cig.md`](acquisizione/dettaglio-cig.md)): che cosa si viola quando il link
manca o non porta ai documenti, chi ne risponde e chi vigila.

**Legenda.** **[V]** = verificato da noi sul testo della fonte primaria, archiviato in
[`prove-normativa/`](prove-normativa/) (sha256 in `SHA256SUMS`, data 4/11/2026; per le delibere ANAC
URL e ora in `manifest-anac.jsonl`). **[R]** = riferito da terzi (commenti, banche dati private),
*da verificare*. Le citazioni testuali sono brevi; il testo completo è nei file archiviati.

Fonti: Normattiva, testo vigente al 4/11/2026 (`dlgs36-art*.html`, `dlgs33-art*.html`, URN
`urn:nir:stato:decreto.legislativo:2023-03-31;36` e `...:2013-03-14;33`); anticorruzione.it (PDF e
XLSX delle delibere).

## 1. Le norme, una per una

### d.lgs. 36/2023 (codice dei contratti)

| Art. | Che cosa dice (sintesi) | Esito della verifica |
|---|---|---|
| **88 c.1** [V] | Dalla pubblicazione dell'avviso (o dall'invio dell'invito a confermare l'interesse) i documenti di gara sono disponibili in forma digitale «in modo gratuito, illimitato e diretto»; l'avviso indica il collegamento ipertestuale. | **Confermato.** |
| 88 c.2 [V] | Se i mezzi elettronici non si possono usare, l'avviso lo dice e indica come si trasmettono i documenti (termine prorogato fino a 5 giorni). | Confermato: è la sola deroga scritta; va dichiarata nell'avviso. |
| **27 c.3** [V] | La documentazione di gara è «resa costantemente disponibile» sulle piattaforme (art. 25) e sui siti istituzionali, ed è «costantemente accessibile attraverso il collegamento» con la BDNCP. | **Confermato**, ed è più forte dell'88: obbligo di disponibilità costante, non solo dalla pubblicazione. |
| 25 c.2 e c.4 [V] | Le piattaforme non possono alterare la parità di accesso né limitare la partecipazione; divieto di porre a carico dei concorrenti costi di gestione delle piattaforme. | Confermato. Riguarda i **concorrenti**, non chiunque: utile per il pagamento, meno per la registrazione del pubblico. |
| 20 c.1 [V] | Trasparenza dei contratti: dati e atti indicati all'art. 28, pubblicati secondo il d.lgs. 33/2013. | Confermato (norma di rinvio). |
| 28 c.2-3 [V] | Collegamento tra «Amministrazione trasparente» e BDNCP; per la trasparenza fanno fede i dati trasmessi alla BDNCP. | Confermato. |
| 222 [V] | Vigilanza e controllo ANAC sui contratti pubblici (c.1; poteri al c.3). | Confermato come norma di **vigilanza**. **Correzione:** l'art. 222 non contiene una sanzione specifica per la mancata disponibilità dei documenti o per la piattaforma che li nega; non va citato come norma «violata». |

### Direttiva 2014/24/UE

| Art. | Esito |
|---|---|
| **53 par. 1** [R] | Testo atteso: accesso elettronico «gratuito, illimitato e diretto» ai documenti di gara dalla pubblicazione del bando; l'art. 88 lo recepisce quasi alla lettera. **Non verificato sulla fonte primaria in questa sessione:** EUR-Lex risponde HTTP 202 con verifica anti-bot (AWS WAF) al nostro client, e non la aggiriamo. Da verificare con un browser reale (ticket #63). La direttiva vale solo **sopra soglia**. |

### d.lgs. 33/2013 (trasparenza)

| Art. | Che cosa dice | Esito |
|---|---|---|
| **5 c.1** [V] | L'obbligo di pubblicare dà a chiunque il diritto di chiedere ciò che non è stato pubblicato (accesso civico semplice). | Confermato. |
| 5 c.3, 6, 7, 10 [V] | Istanza senza motivazione, anche al RPCT (c.3 lett. d); conclusione in 30 giorni, e per i documenti obbligatori **pubblicazione** sul sito con comunicazione del link (c.6); riesame al RPCT in caso di diniego o silenzio (c.7); se riguarda dati obbligatori il RPCT **deve** segnalare ex art. 43 c.5 (c.10). | Confermato. **Correzione:** il testo vigente dell'art. 5 **non nomina il «titolare del potere sostitutivo»**: dopo il d.lgs. 97/2016 il rimedio scritto è il **riesame del RPCT** (c.7). Il potere sostitutivo deriva dall'art. 2 c.9-bis l. 241/1990 ed è indicato dalla prassi ANAC (delibera 1309/2016) [R]. |
| 6 c.1 [V] | Qualità: integrità, completezza, tempestività, «facile accessibilità», conformità agli originali. | Confermato. |
| 7 [V] | Formato aperto e riutilizzabilità dei documenti obbligatori. | Confermato. |
| 8 c.1 e c.3 [V] | Pubblicazione tempestiva; durata **5 anni** dal 1° gennaio successivo, e comunque finché gli atti producono effetti; dopo, accesso ex art. 5. | Confermato; c.3 è la risposta all'obiezione «periodo scaduto». |
| **9 c.1** [V] | Sezione «Amministrazione trasparente»; ammesso il collegamento ipertestuale ad altra sezione «assicurando la qualità» dell'art. 6; divieto di filtri che impediscono ai motori di ricerca di indicizzare la sezione. | Confermato. |
| 37 [V] | Contratti: si pubblica secondo l'art. 28 del codice; obbligo assolto con l'invio alla BDNCP (rinvio all'art. 9-bis). | Confermato. |
| 43 c.1, c.4 [V] | RPCT: controllo stabile sugli obblighi; segnala a organo di indirizzo, OIV, ANAC e, nei casi gravi, all'ufficio disciplina; vigila sull'accesso civico. | Confermato. |
| 45 c.1-4 [V] | ANAC: poteri ispettivi; ordina la pubblicazione entro 30 giorni; segnala l'illecito disciplinare e gli inadempimenti a vertici, OIV, Corte dei conti; rende pubblici i provvedimenti. | Confermato. |
| 46 c.1 [V] | L'inadempimento e il rifiuto dell'accesso civico sono elementi di responsabilità dirigenziale e possibile danno all'immagine; c.2: esimente per causa non imputabile. | Confermato (c.2 è la difesa dell'ente: vedi §5). |

### Delibere ANAC

| Atto | Contenuto pertinente | Esito |
|---|---|---|
| **261/2023** [V] | Provvedimento ex art. 23 codice: dati da trasmettere alla BDNCP. Richiama l'art. 27 c.3. | Confermato come fonte dei dati trasmessi (il campo del link è fra questi, cfr. 263 art. 6.2). |
| **263/2023** [V] | Pubblicità legale ex art. 27. **Art. 6.2:** dalla pubblicazione in BDNCP le stazioni appaltanti «rendono accessibili i documenti di gara attraverso il collegamento ipertestuale» comunicato alla BDNCP, garantendone accesso e disponibilità «fino al completamento della procedura e all'esecuzione del contratto». | **Confermato, ed è la norma più puntuale** sul nostro campo: fissa anche la durata. |
| **264/2023**, testo modificato dalla **601/2023** [V] | Obblighi di trasparenza ex art. 28 c.4 e art. 37 d.lgs. 33/2013; si applica ai soggetti dell'art. 2-bis d.lgs. 33/2013 (art. 2.2); per le procedure dal 1/1/2024 la trasmissione alla BDNCP avviene tramite le piattaforme (art. 3). | Confermato. |
| **Allegato 1** (264 mod. 601, XLSX) [V] | Per ogni procedura, link alla BDNCP più gli atti non trasmessi; fra questi i «Documenti di gara» (almeno delibera a contrarre, bando/avviso/lettera di invito, disciplinare, capitolato, condizioni contrattuali), aggiornamento «Tempestivo». Nota di testa: se gli atti stanno già sulla piattaforma, basta il link in AT «in modo da consentire a chiunque la visione». | Confermato. La nota è decisiva: il rinvio alla piattaforma vale **solo** se chiunque può vedere i documenti. |

## 2. Esito del link → norma

Destinatari: **SA** = stazione appaltante o ente concedente; **GP** = gestore della piattaforma
(art. 25 c.3); **ANAC** come gestore della BDNCP/PVL. Vigilanza: ANAC (art. 222 codice; art. 45
d.lgs. 33/2013); internamente RPCT (art. 43) e OIV (attestazione annuale).

| Esito misurato | Norme | Destinatario | Vigilanza |
|---|---|---|---|
| **Link mancante** nell'avviso PVL | art. 88 c.1 secondo periodo; art. 27 c.3; del. 263 art. 6.2; del. 264 All. 1 | SA (compila l'avviso); ANAC per i tipi di scheda che non prevedono il campo (adesioni, in house: vedi R30) | ANAC |
| **Errore DNS, TLS o HTTP** (4xx/5xx persistente) | art. 27 c.3 («costantemente»); del. 263 art. 6.2; d.lgs. 33/2013 artt. 6, 8 c.3 | SA; GP se il guasto è della piattaforma | ANAC; RPCT |
| **Pagina senza documenti** | art. 88 c.1; art. 27 c.3; del. 264 All. 1 (documenti di gara); d.lgs. 33/2013 art. 6 (completezza) | SA | ANAC; RPCT, OIV |
| **Login, registrazione o pagamento** | art. 88 c.1 («gratuito», «diretto»); art. 25 c.4 (costi, per i concorrenti); del. 264 All. 1 nota («chiunque»); d.lgs. 33/2013 art. 5 c.3 (nessuna legittimazione); art. 53 dir. sopra soglia [R] | SA; GP | ANAC |
| **CAPTCHA, WAF o robots.txt** | d.lgs. 33/2013 art. 9 c.1 (divieto di filtri all'indicizzazione) se la pagina è in AT o vi è collegata; art. 6 («facile accessibilità»); art. 88 («diretto») | SA; GP (spesso è il fornitore a impostare WAF e robots) | ANAC; OIV |
| **Documenti solo via JavaScript** | Nessuna violazione di per sé se un browser comune li mostra. Violazione dell'art. 9 c.1 solo se impedisce ai motori di ricerca di indicizzare la sezione AT (da provare caso per caso) | GP | — (raccomandazione, non violazione) |
| **Scansione o .p7m** | d.lgs. 33/2013 art. 7 (formato aperto, rinvio all'art. 68 CAD); art. 6 (riutilizzabilità). Il .p7m è un formato di firma, non escluso in sé: la violazione è l'assenza di una copia leggibile e aperta | SA | ANAC; OIV |

## 3. Prassi e giurisprudenza sull'art. 88

- **Registrazione per la sola consultazione.** Nessun testo primario verificato la ammette: l'88 dice
  «diretto» e la nota dell'Allegato 1 alla 264 dice «chiunque». Precedente sul vecchio art. 74
  d.lgs. 50/2016 (testo equivalente): una **delibera ANAC del 2019** sulla gara per il socio operativo
  del bacino Fratta-Gorzone (CIG 7995138498) avrebbe giudicato illegittima la lex specialis che
  condiziona l'accesso ai documenti a registrazione o identificazione. **[R]** (riferito da
  codiceappalti.it, scheda art. 74): numero e data **non verificati**, da trovare sul sito ANAC.
- **TAR, Consiglio di Stato, Corte di giustizia UE.** Non abbiamo trovato e verificato pronunce che
  decidano sulla registrazione ex art. 88 o art. 53 della direttiva. La giurisprudenza trovata (es.
  TAR Lazio, sez. IV, 1/7/2024 n. 13225 [R]) riguarda l'accesso agli atti dopo l'aggiudicazione
  (art. 36), altro tema. **Punto aperto**: ricerca in banca dati (giustizia-amministrativa.it, CURIA).
- **Affidamenti diretti senza bando.** L'88 parla di «avviso» e di «invito a confermare l'interesse»:
  per un affidamento diretto senza avviso non c'è un termine di decorrenza, quindi la sua
  applicazione letterale è **incerta**. Restano però, verificati: l'art. 27 c.3 (tutta la
  «documentazione di gara», senza distinzione di procedura), la del. 263 art. 6.2 (il link
  comunicato alla BDNCP deve dare accesso fino all'esecuzione) e l'Allegato 1 alla 264 (documenti
  per **ciascuna** procedura, delibera a contrarre compresa). Il link nell'avviso PVL di un AD è
  quindi una promessa di accesso che la del. 263 rende vincolante. Nessun parere ANAC specifico
  sugli AD verificato.

## 4. Rimedi e percorso

1. **Accesso civico semplice** (art. 5 c.1 e c.3 d.lgs. 33/2013) per il documento obbligatorio non
   accessibile, anche al RPCT; nessuna motivazione; 30 giorni; esito atteso: **pubblicazione** e link
   (c.6).
2. Diniego o silenzio: **riesame al RPCT** (c.7, 20 giorni). Il ricorso al **titolare del potere
   sostitutivo** (art. 2 c.9-bis l. 241/1990) è indicato dalla prassi ANAC [R]; si usa dove l'ente lo
   prevede. Resta il ricorso al TAR (art. 116 c.p.a.) [R].
3. **RPCT**: per i dati obbligatori deve segnalare (art. 5 c.10 e art. 43 c.1) a organo di indirizzo,
   OIV, ANAC, eventualmente ufficio disciplina.
4. **OIV**: attesta ogni anno l'assolvimento degli obblighi su griglia ANAC [R per la griglia];
   ANAC può chiedergli informazioni (art. 45 c.2).
5. **Segnalazione ad ANAC** (art. 45): ordine di pubblicazione entro 30 giorni, segnalazione
   disciplinare, pubblicità dei provvedimenti; per il codice, vigilanza ex art. 222.

Nessun invio da parte nostra senza decisione di Fabio: il percorso alimenta il futuro sistema di
invii massivi (R30, #63).

## 5. Revisione avversariale

| Obiezione dell'ente o della piattaforma | Risposta | Come la neutralizziamo nella misura |
|---|---|---|
| «La registrazione è solo tecnica, gratuita» | «Diretto» e «chiunque» escludono un passaggio di identificazione; la registrazione del pubblico non è prevista da nessuna norma verificata | Registriamo se la pagina mostra l'elenco dei documenti prima del login e se il download è possibile senza; distinguiamo «elenco visibile, download con login» da «tutto dietro login» |
| «I documenti ci sono, li carica il JavaScript» | Vero: non è violazione | Misura con browser reale (Chrome headless) prima di classificare; l'esito «solo JS» non si conta come violazione |
| «Errore temporaneo» / «la piattaforma era in manutenzione» | L'art. 27 c.3 chiede disponibilità costante, ma un guasto isolato non prova nulla | Almeno 3 prove in giorni diversi, con data, ora, codice e sha256; si classifica come violazione solo l'errore persistente |
| «Per l'affidamento diretto il documento non è obbligatorio» | L'88 è incerto per l'AD (§3); restano art. 27 c.3, del. 263 art. 6.2, All. 1 alla 264 (delibera a contrarre) | Per gli AD si contesta il documento che l'Allegato 1 elenca, non «i documenti di gara» in generale; esito separato per tipo di procedura |
| «Il periodo di pubblicazione è scaduto» | Del. 263 art. 6.2: fino all'esecuzione del contratto; d.lgs. 33/2013 art. 8 c.3: 5 anni e comunque finché l'atto produce effetti | Si misurano solo CIG entro questi termini, calcolati dalla data di pubblicazione dell'avviso |
| «È il fornitore della piattaforma, non noi» | La SA resta destinataria dell'obbligo e sceglie la piattaforma (art. 25 c.3); il GP è destinatario della raccomandazione | Nell'esito si annotano sia la SA sia la famiglia di piattaforma |
| «Il WAF serve alla sicurezza» | Legittimo per il traffico abusivo, non per bloccare un utente a ritmo basso e dichiarato (art. 9 c.1 per AT) | User-Agent dichiarato, ≥ 3 s fra richieste, nessun CAPTCHA risolto; prova anche da browser reale |
| «Causa non imputabile» (art. 46 c.2) | Va provata dall'ente | Conserviamo le prove ripetute che mostrano la persistenza |
| «Il .p7m è il documento firmato originale» | Ammesso, ma serve anche un formato aperto leggibile (art. 7) | Si conta violazione solo se manca qualunque copia in formato aperto |

## 6. Punti incerti (da chiudere)

1. Art. 53 dir. 2014/24/UE: testo da verificare su EUR-Lex con browser reale.
2. Estremi della delibera ANAC 2019 (Fratta-Gorzone) sulla registrazione.
3. Pronunce di TAR, Consiglio di Stato e CGUE su registrazione o accesso «diretto»: nessuna verificata.
4. Applicabilità dell'art. 88 agli affidamenti diretti senza avviso.
5. Delibera ANAC 1309/2016 e griglie OIV: citate come prassi, non archiviate.

Raccomandazioni: R31-R36 in [`richieste-e-raccomandazioni.yaml`](richieste-e-raccomandazioni.yaml).
