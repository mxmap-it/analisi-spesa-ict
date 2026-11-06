# Istanza di accesso civico generalizzato ad ANAC: estrazione della tabella «Incaricati» (RUP) della BDNCP e sua pubblicazione in formato aperto

**Bozza non inviata** (2026-11-06, ticket #65). Destinatario: Autorità Nazionale Anticorruzione, ufficio che detiene i dati (Ufficio/Area BDNCP) o, in alternativa, ufficio indicato in «Amministrazione trasparente» per l'accesso civico (indirizzo PEC da ricavare dalla sezione AT di anticorruzione.it prima dell'invio). **Approvazione: Fabio.**

Legenda: [V] testo letto da noi (copia archiviata in `report/convenzioni/accesso-civico/prove-anac-incaricati/`, sha256 in `SHA256SUMS`); [R] riferito, non letto: da verificare prima dell'invio.

---

**Oggetto:** istanza di accesso civico generalizzato (art. 5, c. 2, d.lgs. 33/2013) ai dati della sezione «Incaricati», per un elenco di CIG, della Banca dati nazionale dei contratti pubblici, e richiesta di pubblicazione degli stessi in formato aperto.

Il sottoscritto Fabio Pietrosanti, per il progetto indipendente analisi-spesa-ict.mxmap.it,

**chiede**

1. ai sensi dell'art. 5, c. 2, del d.lgs. 33/2013 [V], i dati della BDNCP che alimentano la sezione «Incaricati» della scheda pubblica di dettaglio CIG (https://dettaglio-cig.anticorruzione.it/cig/<CIG>) **per i soli CIG elencati nel file allegato** (`notify-cigs-<ciclo>.csv`: CIG per i quali il monitoraggio ha rilevato una carenza di pubblicità PVL/AT da segnalare alla stazione appaltante; l'elenco si rigenera a ogni ciclo di notifica e ogni ciclo produrrà, se necessario, una nuova istanza con il solo elenco aggiornato), con i campi:
   - CIG;
   - codice del ruolo e sua descrizione (campi `RUOLO` / `DESCRIZIONE_RUOLO` o equivalenti);
   - nome e cognome dell'incaricato (campi `NOME`, `COGNOME`);
   - data di inizio e, se presente, di fine dell'incarico, o in mancanza la data di registrazione/aggiornamento del dato;
   - codice fiscale della stazione appaltante del CIG (per il collegamento con i dataset aperti già pubblicati).

   **Non** si chiede il codice fiscale delle persone fisiche.
2. che i dati siano forniti in **CSV** (UTF-8, una riga per coppia CIG–incaricato, nello stesso ordine dell'elenco allegato) o in altro formato aperto ai sensi dell'art. 7 del d.lgs. 33/2013 [V], senza elaborazioni ulteriori rispetto all'estrazione;
3. che, ai sensi degli artt. 7 [V] e 7-bis [V] del d.lgs. 33/2013 e dell'art. 28, c. 3, del d.lgs. 36/2023 [V] («periodica pubblicazione [dei dati ricevuti] in formato aperto»), ANAC valuti di **aggiungere questi campi ai dataset aperti della BDNCP** su dati.anticorruzione.it, con la stessa periodicità degli altri dataset (oggi nessuno dei 70 dataset CKAN contiene i nominativi dei RUP: verifica del 6/11/2026).

**In subordine**, se ANAC preferisce non lavorare su un elenco: (a) l'estrazione completa per tutti i CIG acquisiti dal 1° gennaio 2024 (o l'intero storico); oppure (b) un accesso tramite API senza CAPTCHA, o l'inserimento del richiedente in una lista di accesso per finalità di ricerca e monitoraggio civico (whitelist), con i limiti di ritmo che ANAC indicherà. In caso di limiti ex art. 5-bis [V] chiede l'**accesso parziale** (art. 5-bis, c. 4 [V]), ad esempio limitato al solo ruolo di RUP.

**Motivazione** (facoltativa, art. 5, c. 3 [V]):

- **Il dato è già pubblico campo per campo.** La scheda di dettaglio CIG pubblicata da ANAC mostra a chiunque, per ogni CIG, la tabella «Incaricati» con nome, cognome e ruolo. Lo si verifica dal codice pubblico dell'applicazione (bundle `assets/index-B7M5ZtB7.js`, sha256 `1d737e6620c0a1375ad51be50fdbce2b32d715a5aa3a971d794673b17922bbe4`, scaricato il 6/11/2026 alle 09:38 UTC), che rende la sezione con i campi `NOME`, `COGNOME`, `DESCRIZIONE_RUOLO`. L'istanza chiede lo stesso dato in forma completa, non un dato nuovo.
- **La consultazione è oggi possibile solo una scheda alla volta e dietro CAPTCHA.** `runtime-config.js` (sha256 `827e45556dc481a591581d4fa2e252050ab09c835d9cb106bc51012d643aa122`) imposta `CAPTCHA_ENABLED: true` (mosparo) e l'API `consultaCIG` riceve il token del CAPTCHA. Non abbiamo aggirato né risolto il CAPTCHA. Con ~2,4 milioni di CIG con avviso PVL dal 2024, la consultazione scheda per scheda non è praticabile.
- **Il RUP è un ruolo pubblico la cui identità la legge vuole conoscibile.** L'art. 15, c. 3, del d.lgs. 36/2023 [V] dispone che «il nominativo del RUP è indicato nel bando o nell'avviso di indizione della gara» o, in mancanza, nell'invito o nel provvedimento di affidamento diretto. L'art. 15, c. 1-2 [V] lo qualifica come dipendente della stazione appaltante nominato nel primo atto dell'intervento. Il dato riguarda l'esercizio di una funzione pubblica, non la sfera privata (cfr. art. 7-bis, c. 5 [V], sulle notizie relative allo svolgimento delle prestazioni di chi è addetto a una funzione pubblica).
- **La BDNCP serve anche alla trasparenza.** L'art. 23, c. 4, del d.lgs. 36/2023 [V] prevede che la BDNCP renda disponibili le informazioni sul ciclo di vita dei contratti «anche ai fini del rispetto» del d.lgs. 33/2013; l'art. 28, c. 3 [V] stabilisce che per la trasparenza dei contratti «fanno fede» i dati trasmessi alla BDNCP e che ANAC ne cura la pubblicazione periodica in formato aperto. La delibera ANAC 261/2023 individua le informazioni da trasmettere alla BDNCP [R: non letta; verificare se il RUP vi figura fra i dati di pubblicazione] e la delibera 264/2023 gli obblighi di pubblicazione [R].
- **Uso e minimizzazione.** Il dato serve solo per notificare le carenze di pubblicità legale (link PVL mancanti o non funzionanti) alla persona responsabile del singolo procedimento, **tramite l'ente** (RPCT): per questo si chiede il RUP dei soli CIG da notificare e non un'anagrafica generale. Non è prevista pubblicazione nominativa di presunte violazioni; nelle pagine pubbliche il RUP compare al più con nome e iniziale del cognome, gli elenchi restano non pubblici.

**Possibile obiezione e risposta.** L'art. 7-bis, c. 8 [V] esclude dall'ambito del decreto «i servizi di aggregazione, estrazione e trasmissione massiva degli atti memorizzati in banche dati rese disponibili sul web». L'istanza non chiede di attivare un servizio di estrazione massiva di *atti*, ma un'estrazione una tantum di una tabella di *dati* che ANAC già detiene in forma strutturata e già espone; in ogni caso il punto 3 chiede la pubblicazione nel dataset aperto, che renderebbe superflue istanze di questo tipo. Se ANAC ritenesse l'estrazione completa sproporzionata, si chiede in subordine il solo periodo dal 1/1/2024 o il solo ruolo RUP (accesso parziale).

Il rilascio in formato elettronico è gratuito (art. 5, c. 4 [V]). Termine: 30 giorni (art. 5, c. 6 [V]); in caso di diniego o silenzio, riesame al RPCT (art. 5, c. 7 [V]).

Luogo, data, firma.

---

**Note interne (non vanno nell'istanza):**
- Prima dell'invio: (a) leggere la del. ANAC 261/2023 e la 264/2023 e togliere le [R]; (b) verificare con una consultazione manuale (Fabio, CAPTCHA risolto da persona) che la sezione «Incaricati» compaia davvero su un CIG di esempio e annotare data e CIG; (c) ricavare la PEC corretta dalla sezione AT di ANAC.
- Evidenze: `prove-anac-incaricati/` (index.html, runtime-config.js, bundle JS, articoli Normattiva; `SHA256SUMS`). Il codice fiscale nella scheda compare per **partecipanti** e aggiudicatari, non per gli incaricati: la nota dello Stato precedente («forse CODICE_FISCALE») è smentita dal bundle.
- Allegato: `notify-cigs-<ciclo>.csv` generato da visibilita-pa (`python -m visibilita_pa.products.pvl.rup notify-list --cycle <ciclo>`); al 6/11 il ciclo 2026-11 conta 796.826 CIG dal livello 0 (C1 146.901 + C1-bis 649.925, validazione ⛔ in corso): **prima dell'invio ridurlo ai CIG effettivamente da notificare nel ciclo** (validati, livello 1 confermato), decisione di Fabio. Perimetro deciso da Fabio il 6/11: RUP solo per i CIG da notificare.
- Raccomandazione collegata: R47 in `report/metodo/richieste-e-raccomandazioni.yaml`.
