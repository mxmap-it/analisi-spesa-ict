# Visibilità della PA: specifica funzionale e tecnica (bozza 0.2, 4/11/2026)

Nome provvisorio: **Visibilità PA** (repo futuro dedicato; per ora vive qui in `progetti/visibilita-pa/`).
Stato: **proposta da approvare** (Fabio). Le decisioni aperte sono in §10. Nulla è implementato.

## 0. In una pagina

Una piattaforma unica, a tre rilasci che condividono lo stesso nucleo:

| rilascio | cosa fa | perimetro | dipende da |
|---|---|---|---|
| **R1 – Osservatorio robots** | Mappa **tutti i siti e sottositi** della PA, raccoglie `robots.txt` (e `llms.txt`, meta robots, X-Robots-Tag), li interpreta per identità di crawler, **categorizza con LLM che cosa viene escluso**, pubblica cruscotto per ente e per sito, serie storica | Italia completa → poi UE (27 paesi) | — |
| **R2 – Monitor Amministrazione trasparente** | Sopra R1: individua le sezioni AT (anche su domini diversi dal sito istituzionale), verifica accesso per **navigazione dal sito**, **ricerca interna** e **URL diretti**, valuta **ogni link ai documenti di gara (PVL) per CIG**, produce rendiconti, PEC massive (ente e RPCT), rendiconto ANAC | Italia | R1 (host, robots, sonde, archivio) |
| **R3 – Re-indicizzatore** | Reverse proxy su dominio dedicato che espone ai motori i contenuti PA bloccati da robots, registra quali documenti vengono effettivamente scoperti dai motori, genera indici HTML e sitemap dinamiche, sollecita Wayback e i motori | Italia, perimetro da decidere (§10) | R1 (cosa è bloccato), R2 (cosa è obbligatorio) |

Principio architetturale: **un solo motore** (scoperta host → sonde → archivio → interpretazione → esiti → esportazione)
con **profili di misura** a plug-in. R1 è il profilo `robots`; R2 aggiunge i profili `at-sezione`, `at-ricerca`,
`at-link-cig`; R3 è un servizio che legge il catalogo di R1/R2 e scrive nel medesimo archivio.
Nessuna riscrittura: l'attuale `tools/trasparenza/` (monitor #61, 1.1.0-beta) diventa il primo cliente di R1 e
ne migra le parti generiche (sonda, robots, archivio, esportazione) nel nucleo (§8).

---

## 1. Obiettivi e non-obiettivi

**Obiettivi**
1. Censimento **esaustivo** degli host web della PA italiana (enti di IndicePA, partecipate e società in house
   dal registro L.190, scuole, ASL, ordini professionali), **siti e sottositi**: un ente può averne decine.
2. Per ogni host: robots.txt e affini, raccolti, archiviati (sha256), interpretati per identità di crawler,
   con serie storica e registro dei cambiamenti.
3. **Che cosa** viene escluso: classificazione LLM dei percorsi esclusi (es. «Amministrazione trasparente»,
   «albo pretorio», «bandi», «area riservata», «risorse tecniche»).
4. Cruscotto pubblico per **ente** e per **sito**, open data versionati, metodologia riproducibile.
5. Estensione UE con lo stesso schema, fonti nazionali per paese.
6. Base per R2 e R3.

**Non-obiettivi**
- Non si scaricano i siti interi in R1: si misura l'accessibilità, non si fa mirror (il mirror è R3, opzionale).
- Non si qualifica giuridicamente in R1 (la qualificazione di violazione è di R2, solo per sezioni obbligatorie).
- Nessuna comunicazione automatica a terzi: PEC e segnalazioni le invia Fabio.

## 2. Vincoli e regole (validi per tutti i rilasci)

- Regole di `AGENTS.md` §3: nessun CAPTCHA risolto, nessuna rotazione di IP o proxy per eludere blocchi,
  nessuna credenziale, nessuna area riservata. User-Agent **dichiarati** con URL del progetto.
- **Mai impersonare** Googlebot, Bingbot o crawler AI nelle richieste: le loro regole si **leggono** dal
  robots.txt, non si provano fingendosi loro. (Vincolo che R3 rispetta, §7.4.)
- La deroga al robots.txt vale **solo** per le sezioni a pubblicazione obbligatoria (art. 9 c.1 d.lgs.
  33/2013): R1 legge solo `/robots.txt`, `/llms.txt` e la home (consentiti a chiunque); R2 entra nelle sezioni AT;
  R3 si applica al perimetro deciso in §10.
- Ritmo: 1 richiesta alla volta per host, ≥ 5 s fra richieste allo stesso host, parallelismo fra host; orari
  di basso carico per i giri completi.
- Resilienza: ogni giro è ripartibile e idempotente; stato su disco; retry con backoff per errori di rete;
  un giro pubblicato non si sovrascrive. Server condiviso: `nice`, niente `/tmp`, memoria limitata.
- Ogni tentativo fallito ha un **log grezzo** (richiesta, risposta, header, tempi, TLS, corpo troncato + sha256).
- Verificato vs riferito: ogni numero pubblicato viene da una verifica rieseguibile da un clone pulito.

---

## 3. Modello dei dati (comune ai tre rilasci)

Entità e chiavi (SQLite per lo stato operativo; Parquet/CSV/JSON per gli esiti; DuckDB per l'analisi):

| entità | chiave | campi principali |
|---|---|---|
| `paese` | ISO 3166 | fonti nazionali, regole specifiche |
| `ente` | `paese:id_nazionale` (IT: codice fiscale; IPA come attributo) | denominazione, categoria, livello, regione/NUTS, PEC, RPCT se noto, fonti |
| `dominio` | nome registrabile (eTLD+1, Public Suffix List) | ente proprietario (con **evidenza** e confidenza), registrar/WHOIS se lecito |
| `host` | FQDN | dominio, ente, origine della scoperta (§4), primo/ultimo visto, stato (vivo, morto, parcheggiato, redirect) |
| `sito` | host canonico + base path | host, ruolo (istituzionale, AT, albo, gare, tematico, scuola…), piattaforma (se certa) |
| `giro` | `AAAA-MM-GG[-tipo]` | versione software, versione metodo, perimetro |
| `tentativo` | (giro, host, risorsa, via) | via (`http-bot`, `http-browser-ua`, `browser-reale`, `desktop-residenziale`), esito, log grezzo, sha256 |
| `documento` | sha256 | contenuto archiviato (content-addressed, `archivio/blobs/sha256/…`) |
| `robots` | (host, giro) | sha256, stato HTTP, redirect, dimensione, parse (gruppi, regole, sitemap, crawl-delay), errori |
| `verdetto` | (host, giro, identità, percorso) | consentito/vietato, regola che decide, fonte (robots, meta, header, WAF) |
| `categoria_percorso` | (host, giro, regola) | categoria LLM, confidenza, modello e versione istruzioni, revisione umana |
| `cambiamento` | (host, giro_prec, giro) | tipo (nuovo blocco, sblocco, contenuto cambiato…), diff |

Identità dei crawler (tabella versionata `identita.yaml`): `*`, Googlebot, Bingbot, Applebot,
DuckDuckBot, YandexBot, Baiduspider, crawler AI (GPTBot, ChatGPT-User, OAI-SearchBot, ClaudeBot, anthropic-ai,
Claude-SearchBot, Google-Extended, CCBot, PerplexityBot, Bytespider, Meta-ExternalAgent, Amazonbot,
Applebot-Extended, cohere-ai…), archivi (ia_archiver, archive.org_bot), strumenti (curl, wget,
python-requests). L'elenco si aggiorna da fonti pubbliche (documentazione dei produttori), con data.

## 4. R1 – Scoperta degli host (mappatura estensiva)

L'universo è il punto più difficile: si costruisce **per strati**, ognuno con la propria evidenza di
appartenenza all'ente. Un host entra nel cruscotto solo con appartenenza **certa** o **probabile** (marcata).

| strato | fonte | appartenenza |
|---|---|---|
| S1 | IndicePA (CKAN JSON): sito istituzionale, domini delle UO/AOO | certa (dichiarata) |
| S2 | Registro ANAC L.190 (URL della sezione AT): 27.045 URL, 30.701 enti | certa (comunicata dall'ente) |
| S3 | PVL `indirizzo_internet_sa` e `documenti_di_gara_link`: 36.888 domini (#57) | certa per la SA che pubblica; il dominio può essere di una piattaforma (multi-tenant) |
| S4 | Certificate Transparency (crt.sh / dump CT) per ogni dominio di S1-S3 | probabile (sottodominio di dominio dell'ente) |
| S5 | DNS: record già raccolti da mxmap.it (MX, NS), zone `gov.it`, `comune.*.it`, `regione.*.it`, `edu.it`… | probabile |
| S6 | Collegamenti in uscita dalla home e dal footer dei siti S1 (verso altri host) | probabile se dichiarati come «sito dell'ente» |
| S7 | Sitemap dichiarate nei robots.txt | certa per host già noti, scopre path e sottositi |
| S8 | Piattaforme multi-tenant note (trasparenza-pa.net, halleyweb, portaletrasparenza.net, Maggioli, spaggiari, madisoft…): host per ente o path per ente | certa se il tenant è legato all'ente da S2/S3 |

Regole:
- **Host di piattaforma condivisi** (un host per molti enti): il robots.txt è uno per tutti → verdetto
  attribuito a ogni ente servito, ma conteggiato **una volta** nelle statistiche per host. Il cruscotto
  mostra «blocco della piattaforma» separato da «blocco dell'ente».
- Normalizzazione: IDNA, Public Suffix List, `www` e apex trattati come host distinti ma raggruppati nel sito.
- Host morti, parcheggiati (es. domini scaduti), redirect fuori PA: registrati con esito, esclusi dalle
  percentuali di blocco ma mostrati (sono anch'essi un dato: siti PA scaduti e rivenduti).
- Dimensione attesa Italia (da misurare): ~25-35 mila enti, 100-300 mila host candidati, decine di migliaia vivi.

## 5. R1 – Misura

### 5.1 Sonde (per host, per giro)
1. DNS (A/AAAA/CNAME), TLS (versione, catena, scadenza, nome), redirect della home.
2. `GET /robots.txt` con UA bot dichiarato. Conservare: stato, header, corpo (sha256), Content-Type, redirect.
   Casi RFC 9309: 4xx = tutto consentito; 5xx/irraggiungibile = tutto vietato; HTML al posto del testo; >500 KiB.
3. `GET /llms.txt` (e `/llms-full.txt`): presenza, sha256, struttura.
4. `GET /` (home): meta robots, `X-Robots-Tag`, link canonici, footer (piattaforma), link verso altri host (S6).
5. Seconda via sugli esiti anomali: stessa richiesta con UA da browser dichiarato; poi browser reale headless
   (Playwright); per un campione, **desktop residenziale** (la via già prevista nel monitor #61).
   Scopo: distinguere robots.txt da blocchi WAF/anti-bot che colpiscono gli UA non-browser.
6. Sitemap dichiarate: solo indice (numero di URL, date), senza seguire tutto.
7. **Matrice dei blocchi per User-Agent** (Fabio, 4/11): sulla home e su `/robots.txt` si ripete la stessa
   richiesta con un insieme fisso e versionato di UA, **tutti dichiarati con l'URL del progetto**: bot del
   progetto, browser desktop, browser mobile, curl, wget, python-requests, Go-http-client, UA vuoto. Per i
   crawler di terzi (Googlebot, crawler AI) **non** si invia il loro UA: si registra solo il verdetto del
   robots.txt e, dal lato R3, la risposta reale dell'origine ai crawler che passano dal proxy.
   Esito per host: quali UA ricevono 200, 403/429/5xx, pagina di sfida (CAPTCHA, JS challenge), contenuto
   diverso (sha256 e dimensione), e con quale firma WAF (header `server`, `cf-ray`, `x-akamai-*`, cookie di
   sfida). La matrice è un dato pubblicato e la prova per R2 e per la configurazione di R3.

### 5.2 Interpretazione
- Parser **Protego** (Scrapy, RFC 9309 + estensioni Google: `*`, `$`, precedenza per lunghezza) come riferimento;
  seconda via con il parser di Google (`google/robotstxt`, C++, tramite binding o binario) su campione e
  sui casi discordanti → test di non regressione. Discordanze tra parser = dato da pubblicare.
- Verdetto per (identità × percorso) su un **insieme di percorsi di controllo**:
  `/`, sezione AT (da S2), albo, `/bandi`, path delle sitemap, più **tutti i path citati nelle regole**.
- Classi di esito per host (tassonomia R1, versionata):
  `aperto`, `blocco-totale` (`Disallow: /` per `*`), `blocco-totale-tranne-google`, `blocco-solo-ai`,
  `blocco-selettivo` (alcuni path), `blocco-at` (la sezione AT è esclusa), `robots-5xx` (equivale a tutto vietato),
  `robots-html`, `robots-assente`, `robots-invalido`, `waf-per-ua` (robots non raggiungibile per i bot ma sì
  per i browser), `meta-noindex-home`, `x-robots-noindex`.

### 5.3 Categorizzazione LLM di ciò che è escluso
Input: ogni regola `Disallow`/`Allow` (path e pattern), contesto (host, ente, piattaforma, gruppo UA), titolo e
pochi link della home, eventualmente il titolo della pagina del path (solo se il path è pubblico e consentito
dalla deroga, altrimenti no). Output nel formato `spesaict.classificazione/1` già in uso, con tutti i passaggi.

Tassonomia delle categorie (v1, da rivedere su campione):
`amministrazione-trasparente`, `albo-pretorio`, `bandi-gare-contratti`, `atti-delibere-determine`,
`documenti-allegati` (es. `/uploads`, `/allegati`, `*.pdf`), `ricerca-interna`, `area-riservata-login`,
`risorse-tecniche` (admin, cgi-bin, cache, css/js), `cms-standard` (regole di default di WordPress, Drupal,
Joomla, Liferay…), `dati-personali-dichiarati`, `servizi-online`, `contenuti-istituzionali`, `altro`.

Metodo (coerente con il progetto): prima regole deterministiche (pattern noti: `/wp-admin/`, `/amministrazione-trasparente`,
`/albo`…, default dei CMS riconosciuti per hash del robots.txt), poi LLM solo per il residuo; deduplicazione per
**regola normalizzata** (stesse regole su migliaia di host → una classificazione); campione di revisione umana
con accordo misurato; costo e consumi registrati. Modello: Claude via `tools/claude_cli.py` (abbonamento) per
volumi; registro di versione delle istruzioni.

### 5.4 Prodotti di R1
- Open data per giro: `host.csv`, `robots.csv`, `verdetti.parquet`, `regole_categorie.csv`, `cambiamenti.csv`,
  `ente.csv` (aggregato), schema JSON, sha256, metodo e versione.
- Cruscotto:
  - **Italia**: mappa per regione/provincia, distribuzione delle classi, top piattaforme, crawler AI vs motori,
    trend nel tempo (giro per giro), registro cambiamenti;
  - **Ente**: tutti i suoi siti e sottositi, per ognuno classe, regole, categorie escluse, storico, prove;
  - **Sito/host**: robots.txt corrente e storico (diff), verdetti per identità, log grezzi, sha256;
  - **Piattaforma**: enti serviti, configurazione robots comune, effetto aggregato.
- API statica (JSON su GitHub Pages) per R2, R3 e riusi terzi.

### 5.5 Estensione UE
- Stesso nucleo; per paese un **adattatore di fonti** (registri ufficiali delle PA: es. FR annuaire
  service-public / data.gouv.fr, DE Behördenverzeichnis e domini `.bund.de`/Länder, ES DIR3, NL
  organisaties.overheid.nl, ecc.; più CT logs sui domini governativi nazionali). Da censire in una fase 0 UE.
- Chiave ente nazionale + codici NUTS; categorie normalizzate (COFOG o tassonomia propria mappata).
- Ordine: Italia completa → 3-5 paesi pilota → UE-27. Contatti con osservatori nazionali (sinergia con
  osservatorio.mxmap.it e i lavori europei già mappati).

---

## 6. R2 – Monitor «Amministrazione trasparente» (sopra R1)

Riprende e generalizza il monitor #61 (1.1.0-beta) e la campagna #63.

### 6.1 Individuare le sezioni AT
Fonti di partenza, tutte conservate come vie distinte:
1. URL dal registro ANAC L.190 (S2);
2. **navigazione dal sito istituzionale**: link «Amministrazione trasparente» in home/footer (obbligatorio per
   le linee guida AgID), seguendo i redirect anche verso **domini diversi** (piattaforme);
3. URL dei link PVL ai documenti di gara (S3) → host AT/gare effettivamente usati;
4. sitemap e ricerca interna.
Esito per ente: insieme delle sezioni AT (spesso più d'una), concordanza fra vie, piattaforma.

### 6.1-bis Mappare l'albo pretorio (Fabio, 4/11)
Per ogni ente si cerca anche il **path dell'albo pretorio online**, che serve a R3 per le regole privacy (§7.4).
Vie: link «Albo pretorio» dalla home e dal footer; path noti per piattaforma (es. `/albo`, `albo-pretorio`,
`albopretorio`, moduli Halley, Maggioli, DigitalPA, ISWEB…); regole robots che lo escludono (categoria LLM
`albo-pretorio` di R1); sitemap. Esito per ente: URL dell'albo (host + prefisso di path, anche su dominio di
piattaforma), via che l'ha trovato, confidenza (`certa`, `probabile`, `non trovato`). È un dato del catalogo,
pubblicato e riusato da R3 come proposta di esclusione.

### 6.2 Tre modalità di accesso, misurate separatamente
| modalità | cosa si verifica | esito |
|---|---|---|
| **Navigazione** | dal sito istituzionale si arriva alla sezione e alle sottosezioni obbligatorie (es. «Bandi di gara e contratti») | raggiungibile / non raggiungibile / solo via JS |
| **Ricerca** | ricerca interna esiste, funziona, trova un **CIG campione** dell'ente (dalla BDNCP) | assente / non funzionante / trova / non trova |
| **URL diretto** | i link conosciuti (ANAC L.190, PVL) rispondono e mostrano il contenuto | come tassonomia link (§6.3) |
Ognuna con le vie di R1 (bot dichiarato, UA browser, browser reale, desktop residenziale) e la tassonomia anti-bot
già definita in #61 (WAF, CAPTCHA, 403 per UA, geoblocco, rate limit), più robots.txt e meta/X-Robots-Tag
**specifici della sezione** (da R1).

### 6.3 Valutazione esatta di tutti i CIG con link (edizione AT, ex #63)
- Universo: tutti i `documenti_di_gara_link` PVL (2,43 M CIG 2024-2026, 36.888 domini) + CIG senza link
  (per tipo di procedura, P18).
- Strategia di scala: **deduplicazione per URL e per template** (molte piattaforme hanno un URL per
  procedura con struttura fissa): si misura ogni URL distinto, ma l'interpretazione si fa per famiglia di
  piattaforma con adattatori; ritmo per host rispettato (stima del tempo per host dominanti → giri distribuiti
  su settimane, con priorità per campione stratificato e poi censimento).
- Esiti per link (tassonomia della scheda normativa §2): mancante, DNS/TLS/HTTP, pagina senza documenti,
  login/registrazione/pagamento, CAPTCHA/WAF/robots, solo JS, documenti presenti (numero, formato, p7m/scansione).
- Persistenza: un esito di violazione richiede ≥ 3 misure in giorni diversi; termini di pubblicazione
  rispettati (del. 263 art. 6.2, art. 8 c.3 d.lgs. 33/2013).

### 6.4 Prodotti di R2
- Cruscotto AT: per ente (tutte le sezioni AT, tre modalità, link CIG), per piattaforma, per regione; trend.
- **Rendiconti**: nazionale, per categoria di ente, per piattaforma; rendiconto per **ANAC** (formato del
  registro problemi, con prove).
- **PEC massive** (preparate, inviate da Fabio): all'ente, al **RPCT**, eventualmente all'OIV; testo per classe
  di violazione con norme (scheda normativa), prove (sha256, date) e richiesta (accesso civico semplice art. 5
  c.1 dove l'atto manca). Registro invii, ricevute, risposte, esiti successivi (risolto/non risolto) → cruscotto.
- Ingresso per il futuro sistema di accesso civico massivo.

---

## 7. R3 – Re-indicizzatore (reverse proxy)

### 7.1 Scopo
Rendere **trovabili** dai motori di ricerca e dai sistemi di IA i contenuti pubblici della PA che i robots.txt
escludono, misurando quanti documenti esclusi vengono effettivamente scoperti e indicizzati.

### 7.2 Funzionamento proposto
- Dominio dedicato (es. `<nome>.it`), host per sito originale: `https://<host-originale>.<dominio-proxy>/<path>`
  oppure `https://<dominio-proxy>/<host-originale>/<path>`.
- Il proxy serve **il proprio** `robots.txt` (senza `Disallow`) e, per ogni sito, una **sitemap dinamica**
  generata dal catalogo R1/R2 (URL esclusi dal robots originale, scoperti da sitemap originali, link PVL, indici
  AT) + **indici HTML** navigabili e ri-scansionabili (per ente, per sezione, per data).
- Su richiesta di un crawler: il proxy scarica la pagina dall'origine (UA dichiarato del progetto, ritmo
  rispettoso, cache), la serve con:
  - `<link rel="canonical">` verso l'**URL originale** (evita contenuto duplicato e indirizza i motori alla fonte);
  - banner «copia di servizio, fonte: …, data, sha256»;
  - riscrittura dei link interni verso il proxy solo per i path esclusi dal robots originale.
- **Registro dei passaggi**: ogni richiesta di crawler (UA + verifica inversa DNS/IP per Googlebot, Bingbot e
  crawler AI che pubblicano gli IP) → quale documento, quando, quale motore. Cruscotto «documenti bloccati
  dall'ente e scoperti dai motori tramite il proxy», per ente e per sito.
- **Wayback Machine**: per ogni URL escluso, verifica in CDX se esiste copia; se manca, richiesta di
  archiviazione (Save Page Now, nei limiti di uso del servizio); il proxy può servire la copia Wayback quando
  l'origine non risponde.
- **Sollecito ai motori**: sitemap inviate tramite i canali per i proprietari del dominio proxy (Search Console,
  Bing Webmaster, **IndexNow**), ping delle sitemap; nessun canale non ufficiale.

### 7.3 Copia locale: sì o no
| opzione | pro | contro |
|---|---|---|
| A. **Nessuna copia** (proxy puro + cache breve) | poco disco; sempre aggiornato; meno responsabilità sul contenuto | dipende dall'origine (WAF, down); il crawler può essere bloccato dal WAF dell'origine verso il proxy |
| B. **Cache content-addressed** dei soli documenti richiesti dai crawler | prova di cosa è stato servito (sha256), resilienza | disco crescente; obblighi di rimozione (§7.4) |
| C. **Mirror completo** delle sezioni escluse | indice completo indipendente | molto disco; massima responsabilità; contrasta con la scelta di non fare mirror |
Proposta: **B** con limiti di dimensione e tempo, più ricorso a Wayback come archivio di lungo periodo.

### 7.4 Rischi e vincoli (revisione avversariale: da decidere prima di costruire)
1. **Dati personali: regole di esclusione esplicite e configurabili per sito** (Fabio, 4/11). Molti
   robots.txt escludono **l'albo pretorio** e allegati con dati personali. Il Garante privacy (linee guida 2014
   sulla trasparenza on line, da verificare nel testo vigente) chiede che i dati personali pubblicati per obbligo
   non siano indicizzati fuori dalla sezione AT e che gli atti dell'albo non restino reperibili dopo
   l'affissione; re-indicizzarli può renderci titolari del trattamento. Quindi R3 ha un **file di regole di
   esclusione** versionato (`r3/esclusioni.yaml`), pubblico, con:
   - regole **globali** (default, proposte): albo pretorio (dal catalogo §6.1-bis), path con categorie LLM
     `area-riservata-login` e `dati-personali-dichiarati`, pattern di atti con dati personali (es. concorsi,
     graduatorie, sanzioni, notifiche), documenti oltre i termini di pubblicazione;
   - **impostazioni per sito**, esplicite: `albo: escludi | includi`, `path_esclusi: [...]`,
     `path_inclusi: [...]`, `motivazione`, `deciso_da`, `data`. Nessun sito entra in R3 senza una voce
     esplicita; il default per l'albo è `escludi` finché non viene deciso diversamente sito per sito;
   - procedura di **rimozione su richiesta** (contatto pubblico, tempi, registro delle rimozioni).
2. **User-Agent: header sostituibile solo per configurazione** (Fabio, 4/11). Il proxy usa di norma il
   proprio UA dichiarato. Se la matrice dei blocchi per UA di R1 (§5.1 punto 7) **prova** che un sito blocca
   specificamente quel UA, la configurazione del sito in R3 può impostare manualmente un header `User-Agent`
   diverso (`user_agent: "<valore>"`, con `motivazione` e riferimento alla prova della matrice). Il sistema
   **non** cambia UA in modo proattivo o automatico, non ruota UA e non usa mai gli UA dei motori o dei crawler
   AI. Ogni richiesta registra l'UA effettivamente usato. Se l'origine blocca comunque, si registra e si serve
   la copia Wayback.
3. **Diritto d'autore e riuso.** Gli atti amministrativi sono in larga parte esclusi dalla tutela (art. 5 l.
   633/1941) e il CAD (art. 52) favorisce il riuso dei dati pubblicati: da verificare caso per caso per
   allegati di terzi (progetti, offerte tecniche, elaborati di professionisti).
4. **Contenuto duplicato / spam.** I motori possono declassare un dominio proxy; il `canonical` verso
   l'originale riduce il rischio ma rende l'indicizzazione dipendente dalla scelta del motore. Da misurare con un
   pilota.
5. **Responsabilità del servizio.** Hosting, notifiche di rimozione, termini d'uso, contatto pubblico.
6. **Integrità.** Ogni pagina servita deve essere identica all'origine (sha256 registrato), senza modifiche al
   contenuto oltre a banner e link.
7. **Carico sulle origini.** Ritmo e cache come in R1; mai amplificare il traffico dei crawler verso la PA.

---

## 8. Architettura tecnica

```
                ┌──────────────── nucleo (libreria Python) ─────────────────┐
fonti/adattatori│ scoperta host │ coda giri │ sonde HTTP/TLS/DNS │ browser │ archivio sha256 │ esiti │ export │
  IT, UE (§4)   └──────┬───────────────┬────────────────┬────────────┬──────────────┬─────────┘
                       │               │                │            │              │
               profilo robots   profilo at-*      classificatore   cruscotto      servizio R3
                    (R1)            (R2)             LLM (R1)      statico        (proxy, R3)
```

- **Linguaggio**: Python ≥ 3.11 (coerente con il repo). HTTP asincrono con `httpx` (HTTP/2) e limitatore per
  host; DNS con `dnspython`; TLS con `ssl`/`cryptography`; browser con **Playwright**.
- **Coda**: SQLite (WAL) per lo stato dei giri (come `tools/trasparenza/stato.sqlite`), un lavoro per
  (giro, host, sonda); idempotente; ripresa dopo interruzione; watchdog e auto-ripresa (cron + `tools/avvia.sh`).
- **Archivio**: content-addressed esistente (`archivio/blobs/sha256`, `manifest.jsonl`); robots.txt e home
  compressi; log grezzi gz.
- **Analisi**: DuckDB su Parquet (memory_limit, pochi thread: regole del server condiviso).
- **Esportazione**: CSV/JSON/Parquet per giro, schema JSON versionato, sha256; cruscotto **statico** (Hugo +
  JS leggero che legge JSON per ente, come `/progetto/trasparenza-accessibilita/`), su GitHub Pages.
- **Scala**: 300 mila host × 3-5 richieste ≈ 1-1,5 M richieste per giro R1; con parallelismo 50-100 host e
  ritmo per host, 1-2 giorni-macchina. Giri: completo **mensile**, **giornaliero** sui cambiamenti
  (host con blocco, host nuovi, campione di controllo). UE: un giro per paese, sfalsato.
- **R3**: servizio separato (es. Caddy/nginx + app Python o Go) su macchina dedicata, mai sul server
  condiviso di analisi; legge il catalogo esportato (JSON) e scrive il registro dei passaggi in un archivio
  append-only sincronizzato al repo dei dati.
- **Qualità**: test senza rete su fixture di robots.txt reali (corpus anonimizzato), test di concordanza fra
  parser, test di invarianza degli esiti fra giri (guardia anti-regressione), verifica in `tools/verifiche/`.

### 8.1 Migrazione da `tools/trasparenza/` (nessuna riscrittura)
| oggi (`tools/trasparenza/`) | domani |
|---|---|
| `fonti.py` (L.190, IndicePA) | nucleo `fonti/it/` (S1, S2) + R2 |
| `sonda.py`, `diagnosi.py` | nucleo `sonde/` (generiche) |
| `robots.py`, `tassonomia.py` (parte robots) | profilo `robots` (R1) |
| `tassonomia.py` (WAF, anti-bot), `piattaforme.py` | nucleo `diagnosi/`, `piattaforme/` |
| `censimento.py` (orchestrazione) | CLI del nucleo con profili |
| `esporta.py`, `schema/` | nucleo `export/` + schemi per profilo |
| `pec.py`, `comune.py` | R2 `azioni/` |
I giri già pubblicati restano validi: lo schema R2 è un'estensione compatibile dello schema 1.x.

## 9. Piano dei rilasci

| fase | contenuto | criterio di chiusura |
|---|---|---|
| **R1.0 pilota** | nucleo estratto da #61; S1-S3; robots/llms/home; parser doppio; 2.000 host stratificati | concordanza parser ≥ 99 % su casi non ambigui; log grezzi completi |
| **R1.1 Italia** | S4-S8; tutti gli host; classificazione deterministica + LLM; cruscotto ente/sito/piattaforma | universo documentato con coperture per strato; revisione umana del campione LLM con accordo misurato |
| **R1.2 serie** | giri mensili + giornalieri sui cambiamenti; registro cambiamenti pubblico | 3 giri consecutivi senza regressioni |
| **R2.0** | migrazione del monitor #61 sul nucleo; tre modalità di accesso; CIG campione per ente | parità di esiti con 1.1.0-beta sui giri esistenti |
| **R2.1** | valutazione di tutti i link PVL (#63) per famiglia di piattaforma; persistenza | tutti i 36.888 domini classificati; censimento link completato |
| **R2.2** | rendiconti, PEC massive (ente, RPCT), rendiconto ANAC, registro invii | approvazione di Fabio dei testi |
| **R3.0 pilota** | proxy su 20-50 siti AT bloccati, cache B, sitemap, registro passaggi, Wayback | decisioni §10 prese; misura di scoperta/indicizzazione dopo 30-60 giorni |
| **R3.1** | estensione a tutte le sezioni AT bloccate | esito del pilota |
| **UE** | fase 0 fonti per paese; 3-5 paesi pilota | registri ufficiali identificati per paese |

Ticket: uno per rilascio; il monitor #61 e la campagna #63 diventano figli di R2.

## 10. Decisioni per Fabio

1. **Nome e repo** (es. «Visibilità PA», «Indicizzabile», «Aperto ai motori») e organizzazione GitHub
   (mxmap-it o nuova).
2. **Perimetro di R3**: solo sezioni AT obbligatorie (proposta) o anche altri contenuti esclusi?
   *Deciso 4/11:* regole di esclusione esplicite e impostazioni per sito; albo mappato per ente e incluso o
   escluso sito per sito (default `escludi`).
3. **R3 copia locale**: opzione B (proposta), A o C.
4. ~~User-Agent di R3~~ *Deciso 4/11:* UA dichiarato di norma; header sostituibile **solo manualmente** per
   sito, quando la matrice dei blocchi per UA lo prova; mai proattivo.
5. **Dominio del proxy** e soggetto responsabile (associazione/osservatorio), contatto per rimozioni.
6. **llms.txt** in R1: solo presenza e contenuto (proposta) o anche valutazione qualitativa.
7. **Frequenze**: mensile completo + giornaliero sui cambiamenti (proposta).
8. **Paesi pilota UE**.
9. **Budget LLM** per la categorizzazione (stima dopo la deduplicazione per regola).

## 11. Rischi principali di progetto
- Universo incompleto o con falsi positivi di appartenenza → evidenza per host e marcatura della confidenza.
- Host di piattaforma che falsano le statistiche → conteggio per host e per ente separati.
- Blocchi WAF verso il nostro server → seconda e terza via, desktop residenziale, registrazione come dato.
- Carico sul server condiviso → giri notturni, `nice`, memoria limitata; R3 su macchina propria.
- R3 legale/privacy → pilota piccolo, perimetro AT, parere preventivo.

## Registro delle revisioni
- 0.1 (4/11/2026): prima stesura.
- 0.2 (4/11/2026, Fabio): matrice dei blocchi per User-Agent (§5.1.7); mappatura dell'albo pretorio per ente (§6.1-bis); R3 con regole di esclusione esplicite, impostazioni per sito e header User-Agent sostituibile solo manualmente su prova (§7.4, §10).
