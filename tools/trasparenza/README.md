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
