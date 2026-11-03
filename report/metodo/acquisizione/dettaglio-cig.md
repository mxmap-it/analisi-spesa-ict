# Link ai documenti di gara per CIG: da dettaglio-cig alla PVL (#57)

Versione 1.0, 3/11/2026. Livello di acquisizione L1-L3 (`sito/content/progetto/acquisizione-documenti.md`).

## Sintesi

- **Il dato esiste in forma aperta e scaricabile in massa, ma non nei dataset bulk.** Il link che dettaglio-cig mostra in fondo alla scheda (`pubblicazioni.LINK_SITO_COMMITTENTE`) è lo stesso valore che la **Piattaforma di Pubblicità a valore legale (PVL)** espone come `documenti_di_gara_link`. L'API JSON della PVL è pubblica, senza CAPTCHA né autenticazione, paginata per giorno di pubblicazione. *Verificato* sul CIG d'esempio B320E66854 (scheda AD3 del 23/9/2024): stesso URL SaturnWeb in entrambe le fonti.
- **dettaglio-cig non si può interrogare in massa**: è una SPA React che chiama `POST /api/v1/operations/consultaCIG/1.0/exec` con token CAPTCHA mosparo obbligatori (senza token: HTTP 403 «I token mosparo sono obbligatori"). Per le regole del progetto non si aggira: la usiamo solo per il confronto puntuale.
- **Copertura temporale**: la PVL contiene avvisi solo dal 1/1/2024 (0 avvisi con data 2020-2023). Per i CIG precedenti il link non è disponibile in nessuna fonte aperta trovata: resta la proposta R30, da inviare col futuro sistema di invii massivi di richieste FOIA.
- **Scaricamento completo avviato** il 3/11/2026 sul server: 2.753.119 avvisi (2024: 851.200; 2025: 1.037.356; 2026 al 3/11: 864.563), circa 2.800 pagine da 1.000, ritmo una richiesta ogni ≥ 2 s, tempo stimato 2-3 ore.
- **Prima misura** (avvisi dal 1/1 al 22/2/2024, 18.285 CIG): 15,0 % dei CIG con link. Quasi sempre presente nei bandi (P1_16: 95 %; P2_16: 70 %), quasi assente negli affidamenti diretti AD3 (0,3 %), che sono la maggioranza dei CIG. Da rimisurare sull'universo a scaricamento finito (inizio 2024 è il periodo di transizione).

## Fonti verificate

| fonte | link ai documenti? | anni | accesso | esito |
|---|---|---|---|---|
| dataset `pubblicazioni` (CKAN ANAC) | no: colonne `cig, data_creazione, data_albo, data_guri, data_guce, data_bore, SCADENZA_INVITO, DATA_LETTERA_INVITO` (verificato su `20261001-pubblicazioni_csv.zip`) | tutti | bulk | V |
| altri 76 dataset del catalogo CKAN (`package_list`, 3/11/2026) | nessun campo URL nei dataset già scaricati (verifica del 3/11 su cig-2025, aggiudicazioni, avvio-contratto, stazioni-appaltanti); OCDS 2024-2025: solo URI dei CPV | 2007-2026 | bulk | V |
| dettaglio-cig.anticorruzione.it | sì, `pubblicazioni.LINK_SITO_COMMITTENTE` (campo letto dal bundle `index-B7M5ZtB7.js`; altri blocchi: bando, aggiudicazione, partecipanti, incaricati, subappalti, varianti, sospensioni, collaudo) | tutti (riferito: è la vista BDNCP) | per CIG, **CAPTCHA mosparo** | V (accesso) |
| PVL `pubblicitalegale.anticorruzione.it/api/v0/avvisi` | sì, `documenti_di_gara_link` (Sez. B e per lotto in Sez. C), più `indirizzo_internet_sa` e `link_eform_ted` | dal 1/1/2024 | bulk paginato, senza CAPTCHA | V |
| PVL `api/v0/avvisi-full-text?keywords=<CIG>` | sì, stesso campo | dal 2024 | per CIG | V |
| TED eForms BT-15 (`ted_l2.py`) | sì, solo sopra soglia UE | dal 2023 | API | già in L2 |
| `dati.anticorruzione.it/superset/dashboard/dettaglio_cig/?cig=` | collegato dalla PVL; non esplorato | - | dashboard | da verificare |
| PDND e-service ANAC, PCP/interoperabilità | riservati a enti e piattaforme accreditati | - | non pubblici | R (non provato) |

robots.txt: né dettaglio-cig né pubblicitalegale hanno un robots.txt (la richiesta restituisce la SPA, quindi nessuna esclusione). Termini e licenza della PVL: non trovati sul portale; i dataset ANAC sono riferiti come CC BY 4.0 (da verificare per l'API PVL).

## Endpoint PVL

```
GET https://pubblicitalegale.anticorruzione.it/api/v0/avvisi
    ?dataPubblicazioneStart=DD/MM/YYYY&dataPubblicazioneEnd=DD/MM/YYYY
    &page=N&size=1000&sortField=idAvviso&sortDirection=ASC
```

- `size=1000` accettato (~1,6 MB, ~2 s); senza filtro di data i parametri sconosciuti sono ignorati (restituisce tutto).
- Ordine stabile solo con `sortField=idAvviso`; altrimenti `sorted:false`.
- Altri endpoint del frontend: `/avvisi/{id}`, `/avvisi/{id}/cronologia`, `/avvisi-full-text`, `/avvisi-full-text-specializzata`, `/date`, `/map`, `/lavori`, `/news`.
- Struttura: `content[].templates[].template.sections[]`; Sez. A committente (`soggetti_sa[].codice_fiscale`), Sez. B dati generali (`documenti_di_gara_link`), Sez. C oggetto (`items[].cig`, per lotto anche `documenti_di_gara_link`, importi, aggiudicatari).

## Piattaforme di destinazione (prima misura, 2.734 link)

520 domini. In testa: centraleacquisti.regione.lazio.it (STELLA), soresa.it, empulia.it, ariaspa.it (Sintel), piattaforma.asmecomm.it, app.albofornitori.it, intercenter.regione.emilia-romagna.it, start.toscana.it, acquistinretepa.it (MePA), istanze `*.tuttogare.it`, `*.maggiolicloud.it`, aflink, traspare.com, SaturnWeb (servizipubblicaamministrazione.it). Le famiglie software (TuttoGare, Maggioli, Net4market, DigitalPA/traspare) coprono molti enti con un solo crawler: censimento completo a scaricamento finito.

## Scaricatore

`tools/acquisizione/pvl_avvisi.py` (scarica / estrai), `tools/acquisizione/pvl_copertura.py`.

- un giorno alla volta; ogni pagina grezza in `archivio/blobs/sha256/ab/cd/<sha256>.json.gz`, riga in `lavoro/pvl/indice.jsonl`;
- un giorno è chiuso (`lavoro/pvl/stato.jsonl`, esito `ok`) solo se gli `idAvviso` unici = `totalElements`, altrimenti `discrepanza` e si riprende;
- ripartibile: rilanciare lo stesso comando salta i giorni chiusi; pausa ≥ 1 s (default 2 s), backoff fino a 30 min sugli errori;
- UA da browser con l'URL del progetto, nessuna email.

Ripresa sul server:

```
cd ~/analisi-spesa-ict
nohup nice -n 15 .venv/bin/python tools/acquisizione/pvl_avvisi.py scarica --da 2024-01-01 --a $(date +%F) >> log/pvl_avvisi.log 2>&1 < /dev/null &
nice .venv/bin/python tools/acquisizione/pvl_avvisi.py estrai > lavoro/pvl/link_cig.csv
nice .venv/bin/python tools/acquisizione/pvl_copertura.py lavoro/pvl/link_cig.csv
```

Aggiornamento: rilanciare ogni giorno con `--da` = ultimi 7 giorni (gli avvisi possono arrivare con ritardo; i giorni recenti vanno ripresi rimuovendone la riga in `stato.jsonl` o con un `--da` successivo).

## Statistica e mappa dei sistemi

`tools/acquisizione/pvl_analisi.py` (DuckDB su disco, 4 GB, 2 thread) incrocia i CIG PVL con l'universo BDNCP 2024+ (`lavoro/cig_completo/cig_csv_202[4-9]_*.csv` e delta `2026*-cig_csv.csv`, filtro `anno_pubblicazione >= 2024`) e l'anagrafica delle stazioni appaltanti. Statistiche versionate in `esiti/pvl-link-cig/<data>/`: `totale`, `anno-mese`, `procedura`, `classe-importo`, `tipo-ente` (natura giuridica), `regione` (sezione regionale), `oggetto`, `stazione-appaltante`, `scheda-pvl`, `pvl-vs-bdncp`, `sistemi`, `piattaforme`, `verifica-link`. Colonne comuni: `cig`, `in_pvl` (CIG con almeno un avviso PVL), `con_link`, `pct_in_pvl`, `pct_link`, `importo_mln`, `pct_importo_link`.

`tools/acquisizione/pvl_verifica_link.py` apre una volta il `link_esempio` dei primi 300 domini per numero di CIG e di 100 domini a caso (≥ 3 s fra richieste, nessun login): esito `documenti scaricabili` / `documento diretto` / `login o area riservata` / `pagina senza documenti visibili` / `errore http` / `non risponde`. Limite: i documenti caricati via JavaScript non si vedono nell'HTML statico, quindi «senza documenti visibili» non vuol dire «senza documenti».

La piattaforma si attribuisce **solo** quando dominio o percorso identificano con certezza una famiglia nota (tabella `FAMIGLIE` in `pvl_analisi.py`, es. `*.tuttogare.it`, `*.maggiolicloud.it`, `acquistinretepa.it`, Sintel, START, EmPULIA, SATER, STELLA, SaturnWeb); altrimenti `ignota`. Il tipo di link è una regola sull'URL: estensione di file → documento diretto; parametro o percorso di gara → pagina di gara; altrimenti home o profilo del committente.

Catena completa dopo lo scaricamento: `tools/acquisizione/pvl_dopo.sh` (log `log/pvl_dopo.log`).

### File per il monitor di Amministrazione trasparente (chiave: codice fiscale dell'ente)

| file | una riga per | colonne |
|---|---|---|
| `lavoro/pvl/cig_link.csv` | CIG | `cig, cf_ente, link, dominio, sito_ente, schede, n_avvisi, prima_pubblicazione` |
| `lavoro/pvl/enti_sistemi.csv` | ente × dominio | `cf_ente, dominio, piattaforma, n_cig, link_esempio` |
| `lavoro/pvl/sistemi.csv` | dominio | `dominio, piattaforma, gestore, n_enti, n_cig, importo, n_pagina_gara, n_documento, n_home_profilo, tipo_link_prevalente, link_esempio` |
| `lavoro/pvl/verifica_link.csv` | dominio verificato | `dominio, link, http, url_finale, content_type, bytes, login, n_link_documenti, esito, sha256, ts` |
| `lavoro/pvl/link_cig.csv` | avviso × CIG | `cig, id_avviso, id_appalto, codice_scheda, tipologia, data_pubblicazione, cf_sa, documenti_di_gara_link, indirizzo_internet_sa, link_eform_ted, sha256_pagina` |

`cf_ente` è il codice fiscale del committente nella Sez. A dell'avviso (`soggetti_sa[0].codice_fiscale`), lo stesso di `cf_amministrazione_appaltante` nel BDNCP e di `codice_fiscale` in IndicePA per gli enti pubblici. `sito_ente` è `indirizzo_internet_sa` quando l'ente lo compila. CSV UTF-8, separatore virgola, intestazione in prima riga.

## Cosa resta

1. A scaricamento finito: copertura per anno, scheda, tipo di ente, importo, sul campione `lavoro/imbuto/ict.csv`; censimento dei domini; esito versionato `esiti/pvl-link-cig/` (CIG → link, piattaforma).
2. Pilota L3 su un campione di link per famiglia: la pagina porta ai documenti scaricabili?
3. Pre-2024 e affidamenti diretti senza link: R30 resta una proposta, da inviare quando ci sarà il sistema di invii massivi di richieste FOIA (nessun invio ad-hoc).
