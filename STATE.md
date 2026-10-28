# STATE — punto di ripresa

Per chiunque riprenda il lavoro, umano o Claude. Si aggiorna a ogni avanzamento.

**Ultimo aggiornamento:** 2026-10-28

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
