# Come riprodurre le verifiche del rendiconto ANAC

Ogni numero del [rendiconto ANAC](https://analisi-spesa-ict.mxmap.it/rendiconti/anac-2026-10/) si
può rifare da zero, su una macchina qualunque, con questi comandi.

## Requisiti

- Linux o macOS, Python 3.12, `git`.
- **Disco:** circa 77 GB per i file ANAC che le verifiche leggono (dimensione misurata sullo snapshot), più circa 20 GB di lavoro.
- **Memoria:** 8 GB bastano: le verifiche limitano duckdb a 6 GB (`DUCKDB_MEMORIA` per cambiarlo).
- **Tempo:** il download richiede alcune ore; le verifiche circa un'ora e mezza.
- **Rete:** il server di ANAC dà metadati sbagliati alle richieste `HEAD` dei programmi che non si
  presentano come browser (problema P12); gli script usano lo user-agent di un browser più l'indirizzo
  del progetto.

## In sei comandi

```bash
git clone https://github.com/mxmap-it/analisi-spesa-ict.git && cd analisi-spesa-ict
tools/verifica_anac.sh ambiente     # crea .venv con le versioni bloccate di requirements.txt
tools/verifica_anac.sh dal-vivo     # misura ORA il server ANAC: metriche I1-I9, pochi minuti
tools/verifica_anac.sh scarica      # scarica i file che servono alle verifiche (~77 GB)
tools/verifica_anac.sh snapshot     # i file scaricati sono gli stessi usati per il rendiconto?
tools/verifica_anac.sh verifiche    # esegue tutte le verifiche; esiti in esiti/AAAA-MM-GG/
tools/verifica_anac.sh confronta    # confronta ogni numero con quelli pubblicati
```

`tools/verifica_anac.sh tutto` esegue in fila dall'ambiente al confronto.

## Due modi di verificare

**Dal vivo** (`dal-vivo`): misura lo stato attuale del server ANAC, senza scaricare i file grandi.
Se ANAC ha corretto un problema, la metrica corrispondente passa da *violata* a *rispettata*. È
anche il modo in cui seguiamo i problemi nel tempo: lo stesso controllo gira ogni mattina sul
nostro server.

**Dallo snapshot** (`scarica`, `snapshot`, `verifiche`, `confronta`): riproduce i numeri esatti del
rendiconto. Lo snapshot ([`report/anac/snapshot-2026-10-27.tsv`](report/anac/snapshot-2026-10-27.tsv))
elenca i 349 file usati, con URL, dimensione e sha256.
- Se lo sha256 di un file scaricato coincide con lo snapshot, i numeri devono coincidere.
- Se non coincide, ANAC ha cambiato il file dopo il 27 ottobre 2026: il numero può essere
  diverso, e la differenza è informativa.
- Alcuni file non sono più scaricabili: ANAC rimuove gli aggiornamenti mensili dopo alcuni mesi
  (P08). Chi ne ha bisogno può chiederci la copia: ogni file ha il suo sha256, quindi l'identità
  con l'originale si controlla.

## Cosa controlla ogni verifica

| Script | Problemi del rendiconto |
|---|---|
| [`tools/metriche_anac.py`](tools/metriche_anac.py) | I1-I9: ciò che ANAC dichiara e ciò che accade (P02, P06-P10, P12) |
| [`tools/verifiche/ocds_mesi_duplicati.py`](tools/verifiche/ocds_mesi_duplicati.py) | Mesi OCDS che servono lo stesso file (P01) |
| [`tools/verifiche/verifica_38_42.py`](tools/verifiche/verifica_38_42.py) | OCDS rispetto ai dati tabellari: copertura, fornitore, date (P03-P05) |
| [`tools/verifiche/cig_accordo_quadro.py`](tools/verifiche/cig_accordo_quadro.py) | Collegamento fra contratti attuativi e accordi quadro (P15) |
| [`tools/anac_integrita.py`](tools/anac_integrita.py) `--completo` | Controlli di integrità su CIG, aggiudicazioni, aggiudicatari, CUP, stazioni appaltanti (§3, P14, P16, P17) |

L'elenco completo dei problemi, con prova, controvalidazione, azione correttiva e metrica, è in
[`report/anac/problemi.yaml`](report/anac/problemi.yaml).

## Se un numero non torna

Apri una issue su <https://github.com/mxmap-it/analisi-spesa-ict/issues> con l'output di
`confronta` e di `snapshot`. Un errore nostro si corregge e si registra nel registro delle
revisioni del rendiconto.
