# STATE — punto di ripresa

Per chiunque riprenda il lavoro, umano o Claude. Si aggiorna a ogni avanzamento.

**Ultimo aggiornamento:** 2026-10-29

## Aggiornamento 29/10/2026 — via 6, classificazione con modello e fonti (#55) — PUNTO DI RIPRESA

Indicazione di Fabio (29/10): la classificazione va portata avanti **costi quel che costi**, con metodo scientifico, attendibilità, ripetibilità, basi dati; ogni ostacolo va registrato come raccomandazione di policy (`report/metodo/richieste-e-raccomandazioni.yaml`, nuove R16-R18).

- **Giro 1 (p1, Opus, 611 contratti):** `report/metodo/llm/esiti/`. Quasi solo dal testo: 404 alta / 161 media / 46 bassa, 204 disaccordi con regole v3.1, 0 atti dell'ente. Istruzioni `tools/llm/istruzioni.md`.
- **Giro 2 (p2, Haiku, 337 contratti in 68 pacchetti da 5):** `report/metodo/llm/giro2/`. Fatti g2-001..009 (45): 1 solo atto dell'ente, quasi tutto declassato. Causa: WebFetch non legge i PDF delle determine; siti degli enti 403/404/502. **Sospeso** fino allo strumento server di scaricamento + estrazione testo. Istruzioni `tools/llm/istruzioni-p2.md`.
- **Architettura proposta (da decidere):** `report/metodo/via6-architettura.md` — deterministico (regole, tabelle iniziative, scaricamento + pdftotext/tesseract con sha256) + modello solo per trovare l'URL e leggere il testo estratto + revisione umana sui dubbi e a campione.
- **Base di conoscenza iniziative:** `report/metodo/llm/conoscenza-iniziative.yaml` (21 voci, 15 controvalidate) e pagina in bozza `sito/content/progetto/iniziative-consip-cloud.md` (draft). In corso: SPC Cloud lotti 2-4 e Sistema Cloud Toscana (mandataria TIM o Accenture: fonti discordanti).
- **Errori delle regole dal giro 1, da trasformare in test (v3.2):** falsi positivi lessicali ("AWS" stazioni meteo, "Azure S DR" pacemaker, "lotto N" fuori AQ); "PSN" nel testo ≠ servizio PSN; rivenditore ≠ provider (TIM/Fastweb su Pure Storage, Oracle, Microsoft EA); committente ≠ fornitore (ARIA, Sogei, CINECA marcati in-house); Cloud Toscana non in-house; "Google Suite"/Workspace; consumo Azure in Enrollment; Oracle Fusion Cloud.
- **Server:** CLI `claude` autenticata per mxmap.it (login /login del 29/10). Annotazioni: servizio `tools/annotazioni/server.py` su 127.0.0.1:8790 (cron @reboot), API esposta da Caddy su https://annotazioni.51-158-36-151.sslip.io (il sito resta su GitHub Pages, DNS invariato). Trascrizione completa della sessione, fuori da git perché il repo è pubblico: `~/analisi-spesa-ict/lavoro/sessioni/2026-10-29-via6.jsonl`.
- **Aggiornamento 29/10 pomeriggio:** giro 2 su **Sonnet** (Haiku scartato, esiti in `giro2/esiti-haiku/`), passa da `tools/llm/claude_tetto.py` (tetto + attesa del reset del limite) e da `tools/llm/verifica_esiti.py` (R1-R4); guardiano cron `tools/llm/giro2_guardiano.sh` ogni 30 min lo rilancia finché i 68 pacchetti sono completi. Annotazioni volontari: https://annotazioni.51-158-36-151.sslip.io/ (servizio `tools/annotazioni/`, export orario in `dati/annotazioni/`, coda documenti da cercare). Acquisizione documenti a livelli L0-L7 (`sito/content/progetto/acquisizione-documenti.md`); pilota L2 TED in corso (`tools/acquisizione/ted_l2.py`, #57): solo 16/611 CIG del campione hanno data GUCE. Principio a imbuto in AGENTS.md. Ricerca di classificatori esistenti su GitHub in corso → `report/metodo/ricerca-classificatori-esistenti.md`.
- **Prossimi passi:** 1) `tools/llm/atti.py` (scarica nell'archivio, estrae testo, OCR); 2) runner server `claude -p` con Haiku, ripartibile, per i 59 pacchetti restanti; 3) regole v3.2 con i test sopra; 4) pagina di revisione con proposta del modello, confidenza e fonti.

## Aggiornamento 28/10/2026 — misura della spesa cloud v3

- **Rendiconto pubblico** `/rendiconti/cloud-metodo-2026-10/` (v1.0), per la revisione pubblica.
  Riproduzione: `tools/misura_cloud.sh` (test, attribuisci, rivenditori, pnrr, campione, misura,
  confronta). Il 28/10 sono stati riprodotti 1.449 numeri su 1.449.
- **Classificatore** `tools/analisi/classifica.py` (funzione pura). Regole in `config/`, 58 casi
  in `tests/casi_classifica.yaml`. Contratti 2022-2026; un CIG si conta una volta sola (ultima
  versione, il delta vince).
- **Pubblicati** `report/metodo/*-v3.*`:
  - riepilogo, rivenditori, PNRR, importi da verificare (84 contratti, 9,8 miliardi);
  - campione v3 di 611 contratti, con la copia cieca;
  - `fonti-v3.sha256`.
- **Registri:**
  - `report/metodo/REGISTRO-PROCEDIMENTI.md`, il racconto peritale del lavoro;
  - `report/metodo/richieste-e-raccomandazioni.yaml`, con R01-R15 per ANAC, Consip, PSN, DTD,
    ACN, Sogei. Va aggiornato sempre (AGENTS.md §3). Nulla è stato inviato.
- **Pagina di revisione** (privata, claude.ai): https://claude.ai/artifact/1wcRRvBGz6u2H5D8kbWPVq . Annotazione cieca
  A/B, verifica importi, decisioni R01-R15, lacune. Si ricostruisce con `node tools/revisione/costruisci.js`;
  le risposte stanno nel db della pagina (collezioni campione, importi, richieste) e si leggono con ArtifactData.
- **Prossimo:**
  1. Annotazione alla cieca del campione v3 da parte di due persone. **Serve sapere da Fabio chi
     la fa.**
  2. Verifica degli 84 importi da verificare.
  3. Via 4 (PSN) e catalogo ACN.
- **Ticket:** #48 metodo, #41 rivenditori, #43 PNRR, #52 in-house e datacenter (dopo), #53
  interfaccia di drilldown (dopo), #54 richieste ad ANAC, #22 proposta ad aborruso a fine lavoro.

## Aggiornamento 27/10/2026 (sera)

- **Mirror ANAC completo** (#9 chiuso): 1.793 risorse servite tutte archiviate; 4 rispondono 404 da ANAC.
- **Rendiconto ANAC 1.5**: mesi OCDS duplicati provati byte per byte (24 mesi in 8 gruppi su 96); OCDS vs tabellari (§3.5); controlli CIG su tutto il mirror (12.079.473 CIG); nuovo reperto CD-CSV.
- **Registro problemi** `report/anac/problemi.yaml`: 17 schede, 6 pronte per ANAC (P01 P02 P07 P08 P10 P12); le altre hanno il campo `manca` (quasi sempre la seconda via).
- **Contatti ANAC**: li ha Fabio, non cercarli (#51 chiuso).
- **Metodo cloud provider (#48)**: `tools/analisi/attribuisci_provider.py` (vie 1,2,3,5,7), dizionari in `config/`; campione di sviluppo e campione di misura in `report/metodo/`; prima misura v2 (non cieca): precisione provider 94,6%, provider+servizio 86,6%. Prossimo: regole v3 (sviluppo/sandbox, PSN omonimi, GCP clinico, SAP, in-house pubblico e telco IT), nuovo campione, annotazione umana cieca.
- **#50** `cig_accordo_quadro` vuoto nel 20% (2025) delle adesioni dichiarate: in validazione.
- **Server condiviso**: duckdb con memory_limit 6 GB e nice (il 27/10 un job ha reso il server irraggiungibile).

Prossimi passi ANAC: seconde vie per le 11 schede non pronte (#33), controlli su smartcig, poi documento, presentazione e sito (#34-#36) con la sezione «Come riprodurre tutto» (#47).

## Dove sta cosa

| Cosa | Dove |
|---|---|
| Repository | `mxmap-it/analisi-spesa-ict`, pubblico |
| Sito | https://analisi-spesa-ict.mxmap.it/ — sorgenti Hugo in `sito/`, build in `docs/`: `hugo --source sito --minify --cleanDestinationDir` |
| Server | `mxmap.it@51.158.36.151`, cartella `~/analisi-spesa-ict` (clone del repo, push con la deploy key `~/.ssh/id_ed25519_spesaict`, alias `github-spesaict`) |
| Archivio | `~/analisi-spesa-ict/archivio/` sul server, fuori da git: `blobs/` per contenuto, `mirror/` con i percorsi originali, `manifest.jsonl` |
| Clone locale | `C:\Users\admin\Claude\analisi-spesa-ict` |
| Decisioni | [DECISIONI.md](DECISIONI.md) |
| Analisi tecnica | [sito/content/progetto/analisi-tecnica.md](sito/content/progetto/analisi-tecnica.md) |
| Ticket | https://github.com/mxmap-it/analisi-spesa-ict/issues |

## In esecuzione sul server

- **Mirror completo di ANAC** (`tools/mirror_anac.py`, ticket #9): 1.797 risorse, tutti i formati,
  OCDS bulk incluso. Alle 18 del 26/10 era a 719 risorse e 13,1 GB. Si ferma da solo sotto i 40 GB
  liberi.
- **Sonda** ogni giorno alle 06:10 e **metriche di non ricorrenza ANAC** (I1-I9) alle 06:40, esiti in `stato/sonda/` e `stato/metriche/`. Al 26/10: 7 violate su 9; I6 rispettata solo perché l'archivio è nato oggi.
- **Guardiano** in cron ogni 15 minuti (`tools/guardiano.sh`): riavvia il mirror se muore e non ha
  finito.

Controllare con:

```
ssh mxmap.it@51.158.36.151 'cd ~/analisi-spesa-ict && tail -2 log/mirror-anac.log && .venv/bin/python tools/stato_mirror.py | head -9'
```

## Fatto

- Analisi di fonti e strumenti, con le strade scartate → analisi tecnica.
- Roadmap, perimetro delle fonti, attese verso le autorità, registro delle decisioni.
- Censimento ANAC completo: 70 dataset, 1.801 risorse, 128,9 GB reali.
- **Rapporto ANAC pubblicato** e versionato (1.1): https://analisi-spesa-ict.mxmap.it/rendiconti/anac-2026-10/
- Registry delle risorse e sonda; prima sonda su 125 risorse.
- Sito con il tema di osservatorio.mxmap.it.
- 31 ticket, i completati chiusi.

## Prossimo passo

1. **Chiudere ANAC**, macro-obiettivo del setup: criteri nella [roadmap](sito/content/progetto/roadmap.md#8quater-quando-anac-è-finito). Ogni problema con prova, controvalidazione indipendente, azione correttiva e metrica di non ricorrenza (#32, #33); poi documento, presentazione e sito (#34-#36). Prima: lasciar finire il mirror e **riverificare il rapporto su tutte le risorse** (#31) e
   misurare la deduplicazione dell'OCDS (#10).
2. Poi i dataset nell'ordine della [roadmap](sito/content/progetto/roadmap.md#8ter-i-dataset-in-ordine-prima-anac-poi-gli-altri):
   **Consip per primo**, perché cancella oltre i tre anni.

## Bloccanti, che dipendono da Fabio

- ~~**Board di progetto**~~ creata: https://github.com/orgs/mxmap-it/projects/1
- **Tetto**: 20% del limite settimanale su 7 giorni, 2,86% al giorno (`config/budget.yaml`). Da tarare la conversione in token prima di avviare compiti automatici (#20).

## Vincoli da ricordare

- **ANAC respinge gli user-agent non-browser** rispondendo 200 con una pagina HTML: `archivia.py`
  lo riconosce e non lo salva come file. Il blocco degli IP cloud è riferito da altri, non verificato.
- **Il catalogo dichiara dimensioni 4,1 volte quelle vere**: per lo spazio contano gli `HEAD`.
- **I delta ANAC spariscono** senza regola; il file annuale dell'anno in corso non esiste.
- **Consip cancella oltre i tre anni**: il 2023 è già perso.
- **BDAP** in manutenzione straordinaria, segnalata con HTTP 200.
- Importi **SIOPE** in centesimi e mensili puri; join per codice fiscale.
- Sul server **non usare `/tmp`** per file di lavoro: è condiviso con altri progetti. E un `pkill -f`
  con un pattern presente nel proprio comando uccide la propria sessione: usare `tools/avvia.sh`.
- Distinguere sempre **verificato da noi** e **riferito da altri**.
