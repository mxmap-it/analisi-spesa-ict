# Monitor dell'accessibilità di «Amministrazione trasparente»

Modulo autonomo (separabile dal resto del repository) che, per ogni amministrazione italiana:

1. ricava l'URL della sezione «Amministrazione trasparente» (AT) dal **registro ANAC delle comunicazioni
   art. 1 c. 32 L. 190/2012** e da **IndicePA**;
2. verifica se la sezione è indicizzabile da motori di ricerca e bot, come chiede l'**art. 9 c. 1
   d.lgs. 33/2013** (robots.txt, meta robots / X-Robots-Tag, blocchi WAF/anti-bot, TLS, raggiungibilità);
3. riconosce, solo quando è certo, la **piattaforma** del portale;
4. pubblica l'esito per ente come **open data** datato (CSV + JSON, schema in `schema/`), con serie storica;
5. prepara le **PEC** all'ente e ad ANAC e tiene il **registro degli invii**. Il modulo non invia nulla.

Metodo, regole e versioni: [`METODO.md`](METODO.md). Licenza del codice: EUPL-1.2 ([`LICENSE`](LICENSE)); dati: CC BY 4.0.

## Requisiti

Python ≥ 3.10, `requests`; facoltativo `playwright` (seconda prova con browser reale:
`pip install playwright && playwright install chromium`). Nessun'altra dipendenza dal repository.

## Uso

```sh
cd <clone>
python tools/trasparenza/censimento.py tutto            # fonti + sonda + esporta, giro del mese corrente
python tools/trasparenza/censimento.py fonti            # solo la tabella degli enti
python tools/trasparenza/censimento.py sonda --campione 200 --run pilota-AAAA-MM-GG   # pilota stratificato
python tools/trasparenza/censimento.py browser          # seconda prova (Chromium headless) sui bloccati
python tools/trasparenza/censimento.py esporta          # open data in sito/static/dati/trasparenza/giri/<data>/
python tools/trasparenza/censimento.py pec-prepara --giro AAAA-MM-GG
python tools/trasparenza/censimento.py pec-registra --cf CF --giro AAAA-MM-GG --destinatario ente --evento invio --indirizzo pec@ente.it
python tools/trasparenza/test_trasparenza.py            # test senza rete
```

- **Ripartibile e idempotente:** lo stato sta in `lavoro/trasparenza/stato.sqlite`; rilanciare lo stesso
  `--run` riprende dagli enti mancanti. Un giro pubblicato non si sovrascrive.
- **Rispettoso:** una richiesta alla volta per host, ≥ 5 s fra due richieste allo stesso host
  (`TRASPARENZA_INTERVALLO`), parallelismo fra host `--paralleli` (24). Nessun CAPTCHA, nessuna rotazione di IP,
  nessun proxy, nessuna area riservata. Non si usa mai lo User-Agent di Googlebot o di Bingbot.
- **User-Agent dichiarati:** `analisi-spesa-ict-trasparenza/1.0 (+pagina del progetto)` per il bot e un browser
  con l'URL del progetto. Nessuna email.
- **Evidenze:** robots.txt e risposte dei casi non accessibili nell'archivio content-addressed
  (`$ARCHIVIO_ROOT/blobs/sha256/..`), sha256 nei dati.

Variabili: `ARCHIVIO_ROOT`, `TRASPARENZA_DB`, `TRASPARENZA_PUBBLICA` (cartella open data),
`TRASPARENZA_DATI` (registro invii), `TRASPARENZA_INTERVALLO`.

Cron consigliato (mensile, ore di poco carico):
`0 1 2 * * cd ~/analisi-spesa-ict && nice -n 10 .venv/bin/python tools/trasparenza/censimento.py tutto >> log/trasparenza-$(date +\%Y-\%m).log 2>&1`

## File

| file | ruolo |
|---|---|
| `censimento.py` | comando unico |
| `fonti.py` | registro ANAC L.190, IndicePA, anagrafica ANAC → tabella enti |
| `sonda.py` | prove HTTP per ente, firme anti-bot, classificazione |
| `robots.py` | parser robots.txt (RFC 9309) |
| `piattaforme.py` | regole di riconoscimento della piattaforma |
| `esporta.py` | open data, indici, serie storica |
| `pec.py` | PEC pronte (testo + allegati) e registro degli invii |
| `schema/` | schema JSON di `enti.json` e del registro invii |

## Stato della fase 2 (sperimentale, 3/11/2026)
Già scritti e provati sul pilota, **non usati nel giro 2026-11**: `diagnosi.py` e i comandi `diagnosi`, `elenco`,
`importa`, `caratterizza`, `indice-cig` (due origini server/desktop con IP e ASN, DNS, TLS, catena dei redirect,
intestazioni complete, vendor e regola, HAR o dump grezzo con sha256; due vie e test di ricerca con un CIG reale).
Test del catalogo in `test_trasparenza.py` (`test_cat_*`). Sospesi per priorità (#57).

## Requisiti futuri (Fabio, 3/11/2026 — da costruire, non ancora fatti)
1. **Progetto autonomo:** nome proprio e repository GitHub dedicato, dati pubblicati in self hosting su GitHub Pages; per ora resta una sezione di analisi-spesa-ict.
2. **Esecuzione periodica** mensile o anche quotidiana, con **log dei cambiamenti** per ente fra un giro e l'altro.
3. **Resilienza agli errori di rete:** ritentativi con backoff, distinzione fra errore transitorio e blocco; un blocco si conferma solo dopo più tentativi in momenti diversi.
4. **Tassonomia dei blocchi per tipo di client.** Per ogni identità dichiarata si verificano le regole di robots.txt e, dove ammesso, le risposte reali: bot generico dichiarato; motori di ricerca (Googlebot, Bingbot: **solo lettura delle regole**, mai impersonati); crawler AI (GPTBot, ClaudeBot, CCBot…: lettura delle regole); curl, wget e python-requests con UA di default; browser. Per ente: quali identità sono bloccate e da quale meccanismo (robots.txt, WAF per UA, WAF per IP/ASN, challenge JS, CAPTCHA).
5. **Due punti di osservazione:** server (Python + Playwright/Chrome reale, anche non-headless con Xvfb) e desktop di Fabio con IP residenziale (stesso codice, `--origine desktop`, pacchetto importato nel database con origine, IP e ASN). Mai plugin di occultamento dell'impronta, CAPTCHA, rotazione di IP o proxy.
6. **Diagnostica estesa** per tentativo in open data e dashboard: origine/IP/ASN, ora UTC, client e versione, UA, redirect, DNS A/AAAA/CNAME, TLS (versione, certificato, emittente, scadenza, errore), HTTP e intestazioni complete, dimensione/hash/primi kB del corpo, vendor e regola, challenge JS/CAPTCHA, tempi; **log grezzo** (HAR o dump) con sha256 per ogni tentativo fallito, archiviato e linkato.
7. **Caratterizzazione della sezione:** accesso dal link ANAC e dalla navigazione dalla home IndicePA (e se coincidono); piattaforma; **ricercabilità** con un CIG reale 2024-2025 dell'ente (trovato / non trovato / ricerca assente / non funzionante, con query e risposta).
8. **Catalogo delle problematiche** in questo README: definizione, come si rileva, esempio reale con log grezzo, test automatico.
9. **Mirror opzionale** costante e ricercabile di tutte le sezioni AT: solo valutazione (dimensione, ritmo, costo) in `report/metodo/dimensionamento.md`.
