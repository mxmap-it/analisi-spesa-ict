# Come riprodurre tutto da zero: mirror, verifiche ANAC, misura della spesa cloud

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
| [`tools/verifiche/seconde_vie.py`](tools/verifiche/seconde_vie.py) | Conferme indipendenti, con codice diverso e su un altro mese (P03-P05, P11, P14, P16) |
| [`tools/anac_integrita.py`](tools/anac_integrita.py) `--completo` | Controlli di integrità su CIG, aggiudicazioni, aggiudicatari, CUP, stazioni appaltanti (§3, P14, P16, P17) |

L'elenco completo dei problemi, con prova, controvalidazione, azione correttiva e metrica, è in
[`report/anac/problemi.yaml`](report/anac/problemi.yaml).

## Misura della spesa in servizi cloud

Il [rendiconto sulla spesa cloud](https://analisi-spesa-ict.mxmap.it/rendiconti/cloud-metodo-2026-10/)
usa gli stessi file ANAC: prima `ambiente`, `scarica` e `snapshot` qui sopra (i dataset `cig-20*`,
`cig` e `aggiudicatari` bastano), poi:

```bash
tools/misura_cloud.sh test          # casi di riferimento del classificatore: devono passare tutti
tools/misura_cloud.sh attribuisci   # provider, giurisdizione, tipo e canale per ogni contratto ICT 2022-2026 (dal primo avviso PNRR cloud) (~30 min)
tools/misura_cloud.sh rivenditori   # mappa dei rivenditori, PSN compreso
tools/archivia.py --lista config/pnrr-risorse.txt   # dati aperti PA Digitale 2026 (finanziamenti PNRR)
tools/misura_cloud.sh pnrr          # finanziamenti PNRR cloud (Misure 1.1, 1.2) collegati ai contratti, via CUP
tools/misura_cloud.sh campione      # ri-estrae il campione di misura: stesso seme, stesso campione
tools/misura_cloud.sh confronta     # ogni numero confrontato con report/metodo/*-v3.json
```

Per **rifare la verifica umana**: compila la copia cieca del campione
(`esiti/AAAA-MM-GG/cloud/campione-misura-v3-cieco.csv`, senza le colonne del classificatore),
poi `tools/misura_cloud.sh misura la-tua-annotazione.csv`. Con due annotazioni calcola anche
l'accordo (kappa di Cohen).

| Script | Cosa fa |
|---|---|
| [`tools/analisi/classifica.py`](tools/analisi/classifica.py) | Le regole: funzione pura, nessun accesso ai dati |
| [`config/lotti_cloud.yaml`](config/lotti_cloud.yaml), [`config/marchi_cloud.yaml`](config/marchi_cloud.yaml) | Le tabelle curate a mano, con la fonte di ogni riga |
| [`tests/casi_classifica.yaml`](tests/casi_classifica.yaml) | Contratti reali con l'esito atteso |
| [`tools/analisi/attribuisci_provider.py`](tools/analisi/attribuisci_provider.py) | Applica le regole ai dati ANAC, esclude i padri di accordo quadro |
| [`tools/analisi/rivenditori.py`](tools/analisi/rivenditori.py) | Chi incassa i contratti di prodotti cloud |
| [`tools/analisi/campione_riferimento.py`](tools/analisi/campione_riferimento.py) | Campione stratificato, seme fisso, esclude i contratti già visti |
| [`tools/analisi/misura_campione.py`](tools/analisi/misura_campione.py) | Precisione, richiamo e kappa sulle annotazioni |

## Imbuto e raffinamento a livelli

Dopo la misura qui sopra, sul server come `mxmap.it` (un job pesante alla volta). Il metodo è nella pagina
[Raffinamento dell'imbuto a livelli](https://analisi-spesa-ict.mxmap.it/progetto/raffinamento-imbuto/).

```bash
nice .venv/bin/python tools/verifiche/imbuto_strati.py            # L1: strati dell'imbuto (lavoro/imbuto/ict.csv)
nice .venv/bin/python tools/verifiche/imbuto_bdncp.py             # B: quadro economico, in-house, durate, PNRR (BDNCP)
nice .venv/bin/python tools/llm/raffinamento.py l2                # L2: stampanti, consumabili, cablaggio
.venv/bin/python tools/llm/raffinamento.py prepara-l3 tutti       # L3: pacchetti ciechi per Claude Opus
nohup setsid tools/llm/raffinamento_catena.sh &                   # L3 poi L4 (atti), ripartibile, sotto il tetto di spesa
.venv/bin/python tools/llm/raffinamento.py esito                  # tabella L3 e riepilogo
```

B e L2 sono deterministici (stessi file per sha256, stesso risultato). L3 e L4 usano un modello linguistico: i loro
esiti sono versionati in `report/metodo/llm/raffinamento*/esiti/` e si rileggono, non si rigenerano.

### Ingressi fuori dal mirror ANAC (M12)

Quattro ingressi dell'imbuto stanno in `lavoro/` e non vengono dal mirror ANAC. Il registro
[`config/ingressi-lavoro.yaml`](config/ingressi-lavoro.yaml) ne dà sha256, chi li usa e come si rigenerano:

| Ingresso | Usato da | Dove si conserva |
|---|---|---|
| `lavoro/pvl/cig_link.csv` (406 MB, link PVL per CIG) | `imbuto_strati.py --rigenera` | blob nell'archivio content-addressed (`archivio/blobs/sha256/0b/fd/…`, vista `archivio/mirror/_derivati/`); si rigenera con `pvl_avvisi.py estrai` + `pvl_analisi.py` dalle pagine API PVL archiviate |
| `lavoro/pvl/indice.jsonl` (pagine API PVL con sha256) | `pvl_avvisi.py` | git, `dati/ingressi/lavoro/pvl/indice.jsonl.gz` |
| `lavoro/convenzioni/attuativi.csv` | `imbuto_licenze.py` | git, `dati/ingressi/lavoro/convenzioni/attuativi.csv.gz` |
| `lavoro/raffinamento/pacchetti/` (ingressi ciechi di L3) | `raffinamento.py esito` | git, `dati/ingressi/lavoro/raffinamento/pacchetti.tar.gz` |

```bash
python3 tools/ingressi_lavoro.py verifica     # ci sono tutti, con lo sha256 del registro?
python3 tools/ingressi_lavoro.py ripristina   # rimette ciò che manca da git (e cig_link.csv dall'archivio)
```

Da un clone pulito senza l'archivio del server, `cig_link.csv` si rigenera con la ricetta del registro; se ANAC ha
cambiato i dataset nel frattempo lo sha256 può differire e i numeri del link PVL per strato con lui (chi vuole la copia
esatta può chiedercela: lo sha256 ne prova l'identità).

### Prova di ripetibilità

`tools/verifiche/ripetibilita.sh` rifà da zero in `lavoro/ripetibilita/<data>/` tutta la catena deterministica (circa
70 minuti, un job pesante) e `tools/verifiche/ripetibilita_confronta.py` confronta ogni uscita con quella pubblicata
(esito in `esiti/<data>/ripetibilita/`). Dal 19/11/2026 `ict.csv` esce in ordine canonico per CIG (stesso sha256 a ogni
esecuzione: `tools/verifiche/ripetibilita_ordina_ict.py`) e le somme in euro della distribuzione sono al centesimo.

## Il mirror completo dei dati

Le verifiche usano 349 file. Il **mirror completo** del portale ANAC (1.797 risorse, in tutti i
formati) si rifà con `tools/censisci_anac.py` (censimento delle risorse dal catalogo CKAN, scrive `config/anac-risorse.jsonl`) e poi `tools/mirror_anac.py` senza `--dataset` (il 28/10/2026 l’archivio occupa 120 GB; ripartibile, rilanciarlo costa solo le richieste HEAD). L'archivio è
append-only e indirizzato per contenuto: ogni file è salvato una volta sola sotto il suo sha256,
con una vista che replica i percorsi originali e un `manifest.jsonl` con una riga per ogni tentativo
di download. Quindi si sa, per ogni file, cosa ANAC pubblicava e quando.

## Se un numero non torna

Apri una issue su <https://github.com/mxmap-it/analisi-spesa-ict/issues> con l'output di
`confronta` e di `snapshot`. Un errore nostro si corregge e si registra nel registro delle
revisioni del rendiconto.
