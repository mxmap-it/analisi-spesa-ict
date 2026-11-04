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
| **53 par. 1** [V] | Accesso elettronico «gratuito, illimitato e diretto» ai documenti di gara dalla pubblicazione dell'avviso (art. 51) o dall'invito a confermare interesse; l'avviso indica l'indirizzo Internet dei documenti. Eccezioni solo per motivi tecnici (art. 22) o di riservatezza (art. 21 par. 2), dichiarate nell'avviso, con proroga di 5 giorni. | **Verificato il 4/11/2026** su EUR-Lex con un browser reale (prova `prove-normativa/direttiva-2014-24-UE-art53.txt`, con sha256). L'art. 88 lo recepisce quasi alla lettera. Nessun considerando della direttiva tratta la registrazione per consultare. La direttiva vale solo **sopra soglia**. |

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
  condiziona l'accesso ai documenti a registrazione o identificazione. Estremi identificati il 4/11:
  **delibera ANAC n. 968 del 23/10/2019** [R]. Il numero e il contenuto sono riferiti da due fonti
  secondarie indipendenti e concordi (entilocali-online.it, codiceappalti.it). L'oggetto Fratta-Gorzone
  risulta dall'indice delle delibere. Il testo integrale non è stato trovato su anticorruzione.it (le
  ricerche nel portale e nei motori non lo restituiscono): va scaricato dall'archivio delibere ANAC
  prima di citarlo in un atto.
- **TAR, Consiglio di Stato, Corte di giustizia UE.** Non abbiamo trovato e verificato pronunce che
  decidano sulla registrazione ex art. 88 o art. 53 della direttiva. La giurisprudenza trovata (es.
  TAR Lazio, sez. IV, 1/7/2024 n. 13225 [R]) riguarda l'accesso agli atti dopo l'aggiudicazione
  (art. 36), altro tema. Un sito di massime riporta una pronuncia del **Consiglio di Stato del 2020**
  con lo stesso principio della delibera 968 (illegittima la lex specialis che subordina l'accesso a
  registrazione, autenticazione o identificazione) [R]. Gli estremi non sono identificati: il sito
  della massima non risponde. **Punto aperto**: ricerca su giustizia-amministrativa.it e CURIA.
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

## 6. Giurisprudenza sulla responsabilità di ente, dirigente e funzionario

Ricerca del 4/11/2026 (#63). **[V]** = letto nel testo integrale su fonte ufficiale, prova in
[`prove-normativa/`](prove-normativa/) con sha256 in `SHA256SUMS`. **[R]** = riferito da fonte secondaria, da
verificare prima di citarlo in un atto. Le prove della Corte dei conti sono **estratti**: la banca dati mostra il
testo integrale nel browser, ma non lo offre in download se non chiamando l'API interna dell'applicazione, che non
abbiamo usato.

### 6.1 Il perimetro delle sanzioni (Normattiva, testo vigente)

- **Art. 47 d.lgs. 33/2013** [V] (`dlgs33-art47.html`). Le sanzioni pecuniarie riguardano solo **casi specifici**:
  - c.1 e 1-bis: dati dell'art. 14 (titolari di incarichi politici e dirigenti). Da 500 a 10.000 euro, più la
    decurtazione dal 30 al 60% dell'indennità di risultato del responsabile della mancata pubblicazione;
  - c.1-bis: anche l'art. 4-bis c.2;
  - c.2: art. 22 c.2 (enti e società partecipati).

  Le sanzioni le irroga ANAC secondo la l. 689/1981 (c.3). **L'ipotesi è confermata: l'art. 37 (atti di gara) non
  è richiamato.** Per i documenti di gara non c'è sanzione pecuniaria ANAC ex art. 47.
- **Art. 46** [V] (`dlgs33-art46.html`). Vale per **ogni** obbligo di pubblicazione, art. 37 compreso, e per il
  rifiuto o la limitazione illegittima dell'accesso civico. L'inadempimento è «elemento di valutazione negativa
  della responsabilità dirigenziale» ed «eventuale causa di responsabilità per danno all'immagine». Pesa sulla
  retribuzione di risultato. Il responsabile è esonerato solo se prova la causa non imputabile (c.2).
- **Art. 15 c.2–3** [V] (`dlgs33-art15.html`). Per gli incarichi di collaborazione e consulenza la pubblicazione è
  condizione di efficacia e di liquidazione. Se si paga senza pubblicare, risponde il «dirigente che l'ha
  disposto», con una sanzione pari alla somma corrisposta. È l'unico illecito contabile tipizzato legato alla
  trasparenza, e **non copre gli appalti** (art. 37).
- **Art. 17 c.30-ter d.l. 78/2009** [V] (`dl78-2009-art17.html`). Il primo periodo è abrogato dal d.lgs. 174/2016.
  Il testo vigente limita l'azione delle procure per danno all'immagine «nei soli casi e nei modi» dell'art. 7
  l. 97/2001 (reati). Per una sola omessa pubblicazione, quindi, il danno all'immagine dell'art. 46 resta in
  pratica difficile da far valere. Non abbiamo verificato il rapporto con l'art. 51 c.7 del codice di giustizia
  contabile né la giurisprudenza costituzionale sul punto [R].

### 6.2 Corte dei conti

| Pronuncia | Fatti | Principio | Rilevanza #63 | Stato |
|---|---|---|---|---|
| **Sez. giur. Lazio, sent. 323/2016**, dep. 28/11/2016 (Comune di Nettuno) | Incarichi di consulenza non pubblicati fino al 31/8/2013. Retribuzione di risultato pagata ai dirigenti che li avevano conferiti (art. 11 c.8–9 d.lgs. 150/2009) | Il pagamento vietato è un «illecito tipizzato quanto alla individuazione del danno». Condannati i due dirigenti che hanno liquidato (148.416 e 41.506 euro), assolti tre convenuti | La leva contabile funziona solo se una norma lega un **pagamento** alla pubblicazione. Per gli appalti questa norma non c'è | **[V]** estratto `corteconti-lazio-2016-323-estratto.txt` |
| Sez. giur. Lazio, sent. 81/2015 | Vicenda analoga; condannati anche i dirigenti percettori | Stesso principio | Precedente. Probabilmente è il caso dell'articolo di unitel.it (non confermato) | **[R]** citata dalla 323/2016 |
| **Sez. giur. Puglia, sent. 614/2021**, dep. 6/7/2021 (Provincia di Foggia) | Co.co.co. del 2011; contestata anche l'omessa pubblicazione | L'obbligo di pubblicare è «di per sé privo di sanzioni». La responsabilità erariale non nasce dall'omessa pubblicazione in sé, ma dalla liquidazione senza pubblicazione. Convenuto assolto | **Limite chiave:** l'omissione da sola non è danno erariale. Un esposto alla Procura contabile su documenti di gara non pubblicati non ha base | **[V]** estratto `corteconti-puglia-2021-614-estratto.txt` |
| Sez. giur. Puglia, sent. 185 del 5/3/2018 | Indennità di risultato pagata nonostante l'inadempimento (art. 11 d.lgs. 150/2009) | Il danno sussiste anche dopo l'abrogazione della norma. Responsabile anche il sindaco, che non aveva organizzato la trasparenza; escluso il dirigente della ragioneria | Responsabilità degli organi di indirizzo | **[R]** iusmanagement.org via segretaricomunalivighenzi.it |
| Sez. giur. Molise, sent. 48 del 29/4/2013 | Incarico professionale non pubblicato e pagato | Il responsabile del procedimento è condannato a restituire | Come sopra (incarichi) | **[R]** filodiritto.com; citata anche dalla 323/2016 |
| Condanne 2009–2011 (forumpa.it); assoluzione di un segretario comunale (moltocomuni.it, piano di razionalizzazione delle partecipate) | — | — | Non riguardano gli atti di gara; estremi non trovati | **[R]**, non identificate |

### 6.3 TAR e Consiglio di Stato

| Pronuncia | Fatti | Principio ed esito | Rilevanza #63 | Stato |
|---|---|---|---|---|
| **TAR Friuli-Venezia Giulia, sez. I, sent. 131/2026**, pubbl. 13/4/2026, r.g. 162/2025 (Brigante c. Comune di Aquileia) | Accesso civico semplice del 17/2/2025: 14 richieste di pubblicazione in AT (44 documenti). Quattro restano senza risposta (artt. 16, 17, 30, 35) | Il riesame al RPCT (art. 5 c.7) è **facoltativo**, non pregiudiziale. Non serve notificare il ricorso al RPCT; il rito è quello dell'art. 116 c.p.a. Il Comune pubblica solo dopo l'**ordinanza istruttoria n. 33/2026**: cessata la materia del contendere, spese compensate. Il Comune giudica infondate 5 richieste su 14, e il ricorrente non lo contesta | Il ricorso funziona come leva: l'ente pubblica dopo un anno, e solo per effetto del giudizio. Richieste mirate a obblighi certi evitano le «infondate» e la compensazione delle spese | **[V]** `tar-fvg-2026-131.html` |
| **TAR Sicilia-Palermo, sez. IV, sent. 812/2025**, pubbl. 10/4/2025, r.g. 524/2024 (c. Comune di Partanna) | Accesso civico semplice per i dati dell'art. 15; silenzio; il Comune non si costituisce | Accoglie in parte, con un **ordine di provvedere** entro 30 giorni, non di pubblicare. Il giudice ragiona come per l'accesso generalizzato e lascia impregiudicato il merito | Limite: anche vincendo si può ottenere solo l'obbligo di rispondere. Nel ricorso va chiesto l'**accertamento dell'obbligo di pubblicazione** del singolo atto, come nel caso FVG | **[V]** `tar-palermo-2025-812.html` |
| TAR Calabria-Catanzaro, sent. 1671/2015 | Accesso civico sui dati degli organi politici (art. 14) | Condanna a pubblicare entro 30 giorni | Esempio di ordine di pubblicazione | **[R]** La Gazzetta degli enti locali via segretaricomunalivighenzi.it |
| Cons. Stato 2020, massima sulla registrazione obbligatoria (§3) | — | — | — | **[R]**, estremi non trovati. Il 4/11 la ricerca libera su giustizia-amministrativa.it ha risposto **403**; non l'abbiamo forzata |

### 6.4 ANAC: ordini ex art. 45 e responsabilità disciplinare

- **Delibera ANAC n. 361 del 20/7/2023** [V] (`anac-delibera-361-2023-teano.pdf`). Ordine di pubblicazione al
  Comune di Teano (CE) per la sottosezione «Bandi di gara e contratti». L'ordine riguarda:
  - gli atti degli anni precedenti al 2022–2023;
  - le procedure «segnalate dal privato» con diffida ad adempiere;
  - l'adeguamento all'Allegato 9 del PNA 2022.

  Il RPCT deve dare riscontro entro 30 giorni. Se il Comune non si adegua, si procede ai sensi dell'art. 20 c.3
  del Regolamento di vigilanza (delibera 329/2017). Il procedimento è nato da **una segnalazione di un privato**
  ed è durato circa quattro mesi e mezzo (nota del 3/3/2023, ordine del 20/7/2023). È il precedente più vicino
  alla campagna #63.
- L'ente si è difeso così: il software della sezione AT non consente la trasposizione automatica degli atti, e le
  criticità erano state segnalate al fornitore. La giustificazione non ha evitato l'ordine, e conferma la riga «È
  il fornitore della piattaforma, non noi» del §5.
- Segnalazione all'ufficio disciplinare e agli organi di vertice (art. 45 c.4, art. 43 c.5): non abbiamo
  verificato provvedimenti ANAC che la dispongano per gli atti di gara. Non abbiamo trovato pronunce del giudice
  del lavoro su sanzioni disciplinari per omessa pubblicazione [aperto].
- Un documento ANAC cita la sentenza del Consiglio di Stato n. 6654/2022 sulle sanzioni degli artt. 46–47 [R]; non
  l'abbiamo letta.
- Cassazione sulle opposizioni alle sanzioni ex art. 47: nessuna pronuncia trovata [aperto]. Per gli atti di gara
  il punto è comunque marginale (§6.1).

### 6.5 Sintesi operativa: quali leve producono effetti

| Leva | Effetto reale verificato | Prove necessarie |
|---|---|---|
| **Accesso civico semplice** (art. 5 c.1) | Pubblicazione parziale anche prima del giudizio (FVG: 6 richieste su 14 evase subito) | Istanza con elenco puntuale CIG → documento → norma (art. 37, Allegato 1 alla 264, art. 27 c.3 codice). Data e ricevuta PEC. Misura **prima** dell'istanza, con sha256 |
| **Segnalazione ad ANAC** (art. 45) | Ordine di pubblicazione con termine di 30 giorni e verifica finale (Teano, 2023) | Prova della **persistenza dopo l'accesso civico**: almeno 3 misure in giorni diversi dopo i 30 giorni, con data, ora, esito HTTP e sha256. Copia dell'istanza e della risposta, o prova del silenzio |
| **Ricorso al TAR** (art. 116 c.p.a.) | Pubblicazione ottenuta in corso di giudizio (FVG), oppure solo l'obbligo di rispondere (Palermo) | Domanda di **accertamento dell'obbligo di pubblicazione** del singolo atto. Ricorso entro 30 giorni dal silenzio. sha256 delle misure prima e dopo. Serve un avvocato: non è un passo nostro |
| **Responsabilità dirigenziale** (art. 46) | Pesa sulla retribuzione di risultato, tramite OIV e valutazione. Nessun caso verificato per gli atti di gara | Segnalazione al RPCT e all'OIV con le stesse prove di persistenza; richiesta di riscontro nella relazione annuale |
| **Esposto alla Corte dei conti** | **Debole per gli atti di gara**. Senza un pagamento vietato da una norma non c'è danno (Puglia 614/2021), e il danno all'immagine è limitato ai reati (art. 17 c.30-ter) | Solo se emerge un pagamento condizionato alla pubblicazione (art. 15: incarichi) |
| **Sanzione ANAC ex art. 47** | **Non applicabile** all'art. 37 | — |

Nessun invio da parte nostra senza decisione di Fabio (§4).

## 7. Punti incerti (da chiudere)

1. ~~Art. 53 dir. 2014/24/UE~~: **chiuso il 4/11/2026**, verificato su EUR-Lex con un browser reale.
2. Delibera ANAC 968 del 23/10/2019: estremi identificati [R], manca il testo integrale dal sito ANAC.
3. Pronunce sulla registrazione: una massima del Consiglio di Stato del 2020 [R], senza estremi; nessuna pronuncia di TAR o CGUE verificata. La ricerca libera su giustizia-amministrativa.it ha risposto 403 (4/11).
4. Applicabilità dell'art. 88 agli affidamenti diretti senza avviso.
5. Delibera ANAC 1309/2016 e griglie OIV: citate come prassi, non archiviate.
6. ~~Perimetro dell'art. 47~~: **chiuso il 4/11/2026** [V]: solo artt. 14, 4-bis c.2 e 22 c.2, non l'art. 37 (§6.1).
7. Corte dei conti: Lazio 323/2016 e Puglia 614/2021 lette nel testo integrale, ma archiviate solo come estratti. Restano [R] Lazio 81/2015, Puglia 185/2018, Molise 48/2013 e le pronunce citate da forumpa.it e moltocomuni.it (estremi non trovati).
8. Danno all'immagine: rapporto fra art. 46, art. 17 c.30-ter d.l. 78/2009 e art. 51 c.7 del codice di giustizia contabile [R].
9. Nessuna pronuncia della Cassazione sulle opposizioni alle sanzioni ex art. 47, nessuna del giudice del lavoro sulle sanzioni disciplinari per omessa pubblicazione; Cons. Stato 6654/2022 [R] da leggere.
10. Ordini ANAC ex art. 45 sugli atti di gara: un caso verificato (del. 361/2023, Teano). Serve un censimento degli ordini sulla sottosezione «Bandi di gara e contratti» per stimare tempi ed esiti.

Raccomandazioni: R31-R36 in [`richieste-e-raccomandazioni.yaml`](richieste-e-raccomandazioni.yaml).
