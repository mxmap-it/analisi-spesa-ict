# #62 — Progresso della base dati delle convenzioni ICT

File di ripresa (regola di resilienza): ogni passo chiuso si annota qui, con commit e push.

| data | passo | stato | note |
|---|---|---|---|
| 5/11 | lettura AGENTS, STATE, DECISIONI, ticket #62 | fatto | |
| 5/11 | PRINCO ID 2928: 16 documenti riscaricati da consip.it e archiviati con `tools/archivia.py` (sha256 in `documenti.yaml`) | fatto | pagina HTML respinta da archivia (risposta HTML): salvata a parte |
| 5/11 | `padri_ict.py` parametrizzato (anni e uscita); job 2024-2025 sul server in `lavoro/convenzioni/` | fatto | 1.991 padri ICT 2024-2025 |
| 5/11 | censimento (86 iniziative, 295 lotti) e base dati | fatto | `censimento.py`, `base_dati.py` |
| 5/11 | pagine Consip delle iniziative (`consip_pagine.py`) | fatto | 44 trovate, 1.503 documenti |
| 5/11 | archiviazione documenti Consip sul server | in corso | `lavoro/convenzioni/archivia-documenti.log` |
| 5/11 | pagine del sito | fatto | commit faee151b |
| 5/11 | verifica rieseguibile | fatto | ricostruzione identica, seconda via OK |
| | reimportare archiviati.jsonl dal server e rigenerare | da fare | vedi STATE.md |
| | aggregatori/consorzi via mappa piattaforme #57 | da fare | |
| 5/11 | carenze C1-C8, bozze accesso civico (127, non inviate), registro, R37-R42, DECISIONI | fatto | |
| 5/11 | rilettura atti PRINCO archiviati (R → V) | fatto | curate.yaml |
| 5/11 | scarto dei documenti di altre gare linkati nelle pagine Consip | fatto | |
| 5/11 | ricerca online complementare: 7 documenti archiviati (6 atti di enti aderenti su 2746, 2755, 2615 come «fonte non ufficiale»; chiarimenti 2746 che confermano le Region dichiarate ex DPR 445) | fatto | curate.yaml |
| 5/11 | cruscotto a griglia `/convenzioni/griglia/` (JSON da base_dati.py, filtri, riepiloghi, dettaglio cella, simboli+legenda) | fatto | testato nel browser locale |
