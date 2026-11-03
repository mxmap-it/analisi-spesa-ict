# Metodo — versione 1.1.0-beta (4/11/2026)

## Base normativa
- Art. 9 c. 1 d.lgs. 33/2013: le amministrazioni «non possono disporre filtri e altre soluzioni tecniche atte ad
  impedire ai motori di ricerca web di indicizzare ed effettuare ricerche all'interno della sezione» (verificato su
  Normattiva il 3/11/2026).
- Art. 45 d.lgs. 33/2013: vigilanza di ANAC. Art. 1 c. 32 L. 190/2012: comunicazione ad ANAC dell'URL dei dati sui contratti.

## Fonti degli URL (per ogni URL si registra la provenienza in `at_provenienza`)
1. **Registro ANAC «comunicazioni Art.1 comma 32 L.190/2012»** — `https://dati.anticorruzione.it/rest/legge190/ricerca`
   (pagina `dati.anticorruzione.it/#/l190`), anni 2015-2023 (il 2023 è l'ultimo disponibile al 3/11/2026; dati 2022).
   Campi: `codiceFiscale`, `ragioneSociale`, `url` (file XML), `esitoUltimoTentativoAccessoUrl`. Si tiene l'URL
   dell'anno più recente. **Non è il link alla sezione AT** ma al file XML che la norma vuole pubblicato in AT >
   Bandi di gara e contratti. Regole di derivazione:
   - `anac-l190-prefisso`: il percorso contiene un segmento con «trasparen» → URL fino a quel segmento;
   - `anac-l190-host-trasparenza`: l'host contiene «trasparen» → radice dell'host;
   - `anac-l190-regola-zf`: percorso con `/zf/index.php/` → `.../zf/index.php/trasparenza/index/index`.
2. **IndicePA** (CKAN JSON `datastore_search`, risorse `enti` e `categorie-enti`): codice IPA, sito istituzionale,
   categoria, comune ISTAT, PEC.
3. **Scoperta dalla home** (`home-sito-indicepa`, poi `home-host-l190`): link il cui testo è «Amministrazione /
   Società / Ente / Azienda trasparente», o href con `amministrazione-trasparente`/`/trasparenza`, o testo «Trasparenza».
4. **Anagrafica ANAC stazioni appaltanti** (mirror): natura giuridica e regione per chi non è in IndicePA.

Nei mirror ANAC dei dataset di open data (CIG, OCDS, stazioni appaltanti, centri di costo, pubblicazioni) **non c'è**
un campo con l'URL della sezione AT o del profilo del committente (verificato il 3/11/2026).

## Prove per ente
1. robots.txt dell'host della sezione (UA bot), archiviato con sha256; parser RFC 9309 (gruppo più specifico,
   regola più lunga, Allow vince a parità, `*` e `$`). Si valuta il percorso AT e, se sullo stesso host, l'URL del
   file XML L.190 per gli agenti `*`, `Googlebot`, `bingbot`. 4xx = tutto consentito; 5xx/errore = per RFC tutto vietato
   (registrato, non conta come blocco).
2. GET della pagina AT con UA da bot dichiarato e con UA da browser + URL del progetto. Si registrano HTTP,
   redirect, tempi, intestazioni rilevanti. Errore di rete solo sul bot: una ripetizione.
3. `X-Robots-Tag` e `<meta name="robots|googlebot|bingbot">` con `noindex`/`none`.
4. Firme di challenge/WAF (`sonda.py` FIRME): Cloudflare, Imperva/Incapsula, Akamai, Azure Application Gateway/Front Door,
   F5 ASM, Sucuri, AWS WAF, Radware, DDoS-Guard, JS-challenge, CAPTCHA (solo su pagine di blocco).
5. Facoltativa: seconda prova con Chromium headless (`browser`), senza risolvere CAPTCHA.

## Esito principale (in ordine di priorità)
`url non valido` (URL malformato, 404/410, nessun URL) · `irraggiungibile` (DNS, connessione, timeout, 5xx) ·
`tls invalido` · `bloccato da WAF/anti-bot` (firma riconosciuta, oppure bot respinto e browser accettato, oppure
401/403/405/406/428/429/503 a entrambi: in quest'ultimo caso `da_confermare_con_browser`) · `bloccato da robots.txt` ·
`noindex` · `accessibile`; `sezione non individuata` quando la home è leggibile ma non ha un link riconoscibile.
Tutti i segnali presenti finiscono in `segnali`. **Violazioni art. 9** = robots, noindex, WAF/anti-bot.

## Piattaforma
Solo con prova (host del fornitore, `generator` dichiarato, nome del fornitore nella pagina); altrimenti «ignota».
Gli indizi (es. percorso `/L190/`, tema Bootstrap Italia) stanno in `indizi` e non sono attribuzioni. Regole in
`piattaforme.py`. WordPress, Drupal, Joomla, Liferay sono CMS dichiarati, non fornitori.

## Verifica estesa (1.1.0-beta, sugli enti con esito dubbio)
- **Identità oneste** nelle richieste reali: bot del progetto, python-requests e curl con UA di default, UA da browser
  con l'URL del progetto, browser reale (Chromium di Playwright, UA standard, nessun plugin di occultamento).
  Googlebot, Bingbot e crawler AI (GPTBot, ClaudeBot, CCBot, Google-Extended, PerplexityBot) **solo** nelle regole di robots.txt.
- **Origini:** server (datacenter, IP e ASN registrati) e desktop (IP residenziale), stesso codice.
- **Resilienza:** errori transitori (timeout, connessione chiusa, 502/503/504 senza firma) ripetuti con backoff 10 s e 30 s.
  **Conferma:** un blocco è «confermato» se si ripete in due giri a distanza ≥ 60 minuti; se all'ultimo giro non si
  ripete è «non riprodotto» e l'esito diventa «accessibile» (l'esito della prima prova resta in `esito_sonda`).
- **Meccanismi** (`tassonomia.py`): robots.txt (motori / altri client), WAF per User-Agent, WAF per IP/ASN, challenge JS,
  CAPTCHA, nessun client accettato (blocco totale o sito guasto), nessuna risposta, errore transitorio.
- **Diagnostica per tentativo:** DNS (A, AAAA, alias dal resolver di sistema), TLS (versione, emittente, scadenza, errore e tipo),
  catena dei redirect con intestazioni complete, dimensione, sha256 e primi 2 kB del corpo, vendor e regola, tempi.
  Log grezzo (dump HTTP o HAR) per ogni tentativo fallito, sha256 nei dati.
- **Caratterizzazione** (campione stratificato): via ANAC e via navigazione dalla home IndicePA e se coincidono;
  ricerca nella sezione di un CIG reale 2024-2025 dell'ente (preferito importo del lotto ≥ 40.000 €) e di «determina»:
  trovato / non trovato / ricerca assente / ricerca non funzionante.
- **Terza via** (aggancio a #57): link ai documenti di gara e piattaforme di e-procurement dalla Pubblicità a valore legale.

## Limiti noti
- L'URL ANAC è quello comunicato per i dati 2022 o precedenti: può essere superato.
- La scoperta dalla home non vede menu generati via JavaScript.
- «Bloccato» con 403 a entrambi i client senza firma può essere un sito rotto: si conferma con `browser`.
- `bloccato da robots.txt` su un host di servizio (es. host che ospita solo i file XML) è comunque un filtro che
  impedisce l'indicizzazione di contenuti della sezione.

## Registro delle revisioni
| versione | data | cambiamento |
|---|---|---|
| 1.0.0 | 2026-11-03 | prima versione (pilota 2 × 200 enti, censimento completo) |
| 1.1.0-beta | 2026-11-04 | verifica estesa: identità, due origini, conferma in due giri, log grezzi, caratterizzazione, terza via PVL |
