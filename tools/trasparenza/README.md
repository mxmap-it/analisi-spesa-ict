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

## Giro completo e origini (metodo 1.1.0-beta)

`tools/trasparenza/giro.sh [AAAA-MM]`: fonti → indice CIG → sonda (tutti gli enti) → diagnosi giro 1 sui dubbi
(cinque identità oneste + browser reale, DNS, TLS, intestazioni, log grezzi) → caratterizzazione su un campione
(`CAMPIONE_CARATTERI`, due vie e ricerca per CIG) → diagnosi giro 2 a ≥ 60 minuti (conferma) → esporta.

**Origine desktop (IP residenziale)** sul portatile Windows, stesso codice:

```sh
# sul server: elenco dei dubbi
.venv/bin/python tools/trasparenza/censimento.py elenco --run 2026-11 --elenco lavoro/trasparenza/elenco-2026-11.json
# sul portatile (Python 3.12+, requests, playwright + «playwright install chromium»)
set ARCHIVIO_ROOT=lavoro	rasparenza-desktoprchivio & set TRASPARENZA_DB=lavoro	rasparenza-desktop\stato.sqlite
python tools/trasparenza/censimento.py diagnosi --run 2026-11 --origine desktop --elenco elenco-2026-11.json --pacchetto lavoro/trasparenza-desktop/pacchetto-2026-11 [--headed --canale chrome]
# di nuovo sul server, dopo rsync del pacchetto
.venv/bin/python tools/trasparenza/censimento.py importa --pacchetto lavoro/trasparenza/pacchetto-2026-11
.venv/bin/python tools/trasparenza/censimento.py esporta --run 2026-11 --forza   # correzione documentata
```

Ogni tentativo registra origine, IP pubblico e ASN (api.ipify.org e RIPEstat), ora UTC, client e versione, User-Agent.

**Terza via d'accesso (#57, aggancio):** se esistono `lavoro/pvl/link_cig.csv` e `lavoro/pvl/sistemi.csv` (Pubblicità a
valore legale, prodotti da `tools/acquisizione/`, formato in `report/metodo/acquisizione/dettaglio-cig.md`), `esporta`
aggiunge per ente `pvl_link_n` (link ai documenti di gara) e `pvl_sistemi` (piattaforme di e-procurement). Senza i file
le colonne restano vuote.

## Catalogo delle problematiche

Ogni voce: definizione, come la rileviamo, esempio reale dal pilota del 3/11/2026 (log grezzo nell'archivio
content-addressed, pubblicato in `/dati/trasparenza/prove/<sha256>.*.gz` per i giri pubblicati), test automatico in
`test_trasparenza.py`.

| problematica | definizione | come la rileviamo | esempio reale (CF, URL, sha256 del log grezzo) | test |
|---|---|---|---|---|
| robots.txt (motori) | robots.txt vieta la sezione a `*`, Googlebot o Bingbot: violazione art. 9 | parser RFC 9309 sul robots.txt archiviato, percorso della sezione e del file XML L.190 | 00470090549, trasparenza.comune.valtopina.pg.it, robots `dc1dbe14168d…556a7e`; tutto l'host avcp.trasparenza-pa.net ha `Disallow: /` | `test_robots_lunghezza_e_gruppi`, `test_cat_robots_intero_sito` |
| robots.txt (altri client) | vieta la sezione a crawler AI, curl, wget, python: informativo, non violazione art. 9 | stesse regole valutate per GPTBot, ClaudeBot, CCBot, Google-Extended, PerplexityBot, curl, Wget, python-requests | pilota: CCBot 28, GPTBot 25, ClaudeBot 21 enti | `test_cat_robots_per_identita` |
| noindex | meta robots o X-Robots-Tag con `noindex`/`none` sulla pagina della sezione | lettura di intestazioni e `<meta>` | 80001370784, cs-camcom.portaletrasparenza.net (`noindex, nofollow`) | `test_firme_e_noindex` |
| WAF per User-Agent | alcune identità oneste respinte, il browser accettato | 5 identità per tentativo; meccanismo da `tassonomia.classifica` | 01644090134, ateinsubriaolona.it, dump `5b7a0c0f8448…40e1e` (403) | `test_cat_waf_per_user_agent_confermato` |
| WAF per IP/datacenter | tutte le identità respinte dal server, accettate dal desktop residenziale | confronto fra origini | (in verifica sul pilota desktop) | `test_cat_waf_per_ip_datacenter` |
| WAF con firma | pagina di blocco di un vendor riconoscibile (Cloudflare, Akamai, Imperva, Azure, F5, Sucuri, AWS WAF, Radware, DDoS-Guard) | regex su intestazioni e corpo (`sonda.FIRME`), la regola che ha riconosciuto è nei dati | 81002390540, web.spaggiari.eu, HAR `7bfabb3774e3…7a842` (Akamai «Access Denied») | `test_cat_waf_cloudflare`, `test_cat_waf_akamai`, `test_cat_waf_imperva_f5_azure_aws` |
| challenge JS | pagina che richiede l'esecuzione di JavaScript prima del contenuto | firme + `document.cookie…location.reload` in pagine piccole | (nessuno nel pilota) | `test_cat_waf_cloudflare` |
| CAPTCHA | verifica umana su pagina di blocco (non su pagine normali o d'errore) | reCAPTCHA, hCaptcha, Turnstile, captcha-delivery su risposta di blocco | (nel pilota un solo falso positivo, corretto: reCAPTCHA in una pagina 404) | `test_cat_captcha` |
| CDN | presenza di una CDN o WAF davanti al sito (non è un blocco) | intestazioni e alias DNS (`diagnosi.CDN`) | — | `test_cat_cdn_da_dns` |
| nessun client accettato | tutte le identità e tutte le origini ricevono errore: blocco totale o sito guasto | tassonomia; da distinguere a mano | 02493770206, halleyweb.com/ucminciopo, dump `1b5e32489387…b8da8` (HTTP 500) | `test_cat_waf_per_ip_datacenter` (caso opposto) |
| blocco non riprodotto / transitorio | errore alla prima prova, assente alla verifica successiva, oppure solo timeout e connessioni chiuse | ritentativi con backoff (10 s, 30 s) e due giri di conferma a ≥ 60 minuti | 00101410074, trasparenza.partout.it, dump `81cd406947b1…6d` (timeout) | `test_cat_blocco_non_riprodotto_e_transitorio` |
| TLS non valido | certificato scaduto, autofirmato, nome errato o catena incompleta | `ssl` con verifica; tipo in `diagnosi.tipo_errore_tls` | 00425000213, ww2.gazzettaamministrativa.it, catena incompleta (il browser la accetta, python no), dump `c70e1c6e54dc…db76`; 17579021001, cd-servizi.it, autofirmato | `test_cat_tls` |
| irraggiungibile | DNS inesistente, connessione rifiutata o assente | resolver di sistema, socket | 00709690721, aspoperapiadivenere.it, dump `a5bf9c1fe24c…c6ba` (DNS) | `test_cat_blocco_non_riprodotto_e_transitorio` |
| URL ANAC rotto | l'URL comunicato ad ANAC non porta alla sezione (404, malformato, dominio scaduto) | derivazione dal registro L.190 + GET | 02021850066, asmt.it/AmministrazioneTrasparente, dump `3b441ac1e7e8…e712` (404) | `test_deriva_at`, `test_cat_sezione_non_individuata_e_url_anac_rotto` |
| sezione non individuata | la home si legge ma non ha un link riconoscibile alla sezione | `sonda.link_at` | pilota: 29 enti su 200 | `test_link_at`, `test_cat_sezione_non_individuata_e_url_anac_rotto` |
| ricerca assente / non funzionante | la sezione non ha una ricerca, o non trova nemmeno «determina» | browser: campo di ricerca, CIG reale 2024-2025 dell'ente, termine banale | campione della caratterizzazione | `test_cat_ricercabilita` |

## Requisiti futuri (Fabio, 3/11/2026)
1. **Progetto autonomo:** nome proprio e repository GitHub dedicato, dati in self hosting su GitHub Pages.
2. **Esecuzione quotidiana** (oggi mensile) con log dei cambiamenti (già prodotto: `cambiamenti.csv`).
3. **Caratterizzazione di tutti gli enti** (oggi un campione) e origine desktop su tutti i dubbi.
4. **Mirror opzionale** delle sezioni AT: solo valutato (`report/metodo/dimensionamento.md`).
