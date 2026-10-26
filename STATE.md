# STATE — stato del lavoro

Punto di ripresa per chiunque (umano o Claude) riprenda il progetto. Da aggiornare a ogni
avanzamento, prima di chiudere la sessione.

**Ultimo aggiornamento:** 2026-10-26

**Sito:** https://analisi-spesa-ict.mxmap.it/ — sorgenti Hugo in `sito/`, build in `docs/` (`hugo --source sito --minify --cleanDestinationDir`).

## Dove si lavora

- **Server:** `mxmap.it@51.158.36.151` (sd-172212, 8 core, 31 GB RAM, ~246 GB liberi).
- **Repo:** `mxmap-it/analisi-spesa-ict`, oggi **privato**.
- **Clone locale:** `C:\Users\admin\Claude\analisi-spesa-ict` (solo per redazione e push).
- **Clone sul server:** *da fare* — vedi "Bloccanti".

## Fatto

- [x] Analisi delle fonti e degli strumenti, con le strade scartate e il perché → `README.md`.
- [x] Verifica dello stato delle fonti dal server (2026-10-26).
- [x] Repository creato.
- [x] Primo scarico ANAC nel mirror (5 risorse, sha256 nel manifest) e prima analisi di integrità → https://analisi-spesa-ict.mxmap.it/rendiconti/anac-2026-10/.
- [x] Tetto di sforzo ridefinito in token al giorno → `config/budget.yaml` (valore da decidere).

## Da fare, in ordine

1. **Stadio archivio** (`tools/archivia.py`): fetch con user-agent da browser, sha256, manifest
   append-only, scarico mensile di ciò che scade — delta ANAC e annualità Consip. **È il primo
   perché è l'unico con una scadenza imposta da altri.**
2. **Monitor qualità**: disponibilità, freschezza, continuità, persistenza, contenuto,
   agganciabilità. Pagelle per produttore.
3. **Perimetro ICT**: lista CPV motivata, con i test.
4. **Registro fornitore → gruppo → giurisdizione**: seme da `internal/giurisdizione` di
   `anac-pl-pp-cli`, arricchimento GLEIF, curatela per valore.
5. **Pubblicazione**: `kpi.json` + dashboard sul sito dell'Osservatorio.

## Bloccanti

- **Il server non può ancora fare `git push`.** La sua chiave `~/.ssh/id_ed25519` è una deploy key
  limitata al repo `selective-copy-trader`; non ha `gh` né credenziali per questo repository.
  Serve una delle due cose, a scelta di Fabio:
  - aggiungere la chiave pubblica del server come **deploy key con accesso in scrittura** su
    `mxmap-it/analisi-spesa-ict`;
  - oppure rendere il repository **pubblico**, così il server può almeno clonare in lettura, e
    tenere il push dal portatile.

## Ambiente sul server

Presenti: `python3` 3.12.3, `pip` 24.0, `git`, `jq`, `curl`, `claude` CLI 2.1.170 (autenticata).
Presenti come pacchetti Python: `PyYAML`, `requests`.

Da installare quando si parte: `duckdb`, `frictionless`. Assenti e da valutare: `go` (serve solo
per compilare le CLI di aborruso dai sorgenti; in alternativa si usano i binari delle release).

## Vincoli da non dimenticare

- **ANAC blocca gli IP cloud** e gli user-agent non-browser: il fetch gira solo da qui.
- **I delta ANAC spariscono** e la regola non è documentata: a settembre erano sei, a ottobre
  sette, e gennaio-marzo 2026 rispondono già 404.
- **Consip cancella oltre i tre anni**: il 2023 non è più scaricabile.
- **Il file annuale `cig-2026` non esiste ancora**: tutto il 2026 vive nei delta.
- Importi SIOPE **in centesimi** e **mensili puri, non cumulati**.
- Il join con le anagrafiche SIOPE va fatto **per codice fiscale**: la codifica provincia-comune
  non è ISTAT per la Sardegna.
