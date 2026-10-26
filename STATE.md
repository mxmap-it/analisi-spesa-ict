# STATE — punto di ripresa

Per chiunque riprenda il lavoro, umano o Claude. Si aggiorna a ogni avanzamento.

**Ultimo aggiornamento:** 2026-10-26 sera

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

1. Lasciar finire il mirror ANAC, poi **riverificare il rapporto su tutte le risorse** (#31) e
   misurare la deduplicazione dell'OCDS (#10).
2. Poi i dataset nell'ordine della [roadmap](sito/content/progetto/roadmap.md#8ter-i-dataset-in-ordine-prima-anac-poi-gli-altri):
   **Consip per primo**, perché cancella oltre i tre anni.

## Bloccanti, che dipendono da Fabio

- ~~**Board di progetto**~~ creata: https://github.com/orgs/mxmap-it/projects/1
- **Tetto di token al giorno**: `config/budget.yaml` ha `token_giornalieri: null` (#20).

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
