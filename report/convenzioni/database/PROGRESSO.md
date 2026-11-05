# #62 — Progresso della base dati delle convenzioni ICT

File di ripresa (regola di resilienza): ogni passo chiuso si annota qui, con commit e push.

| data | passo | stato | note |
|---|---|---|---|
| 5/11 | lettura AGENTS, STATE, DECISIONI, ticket #62 | fatto | |
| 5/11 | PRINCO ID 2928: 16 documenti riscaricati da consip.it e archiviati con `tools/archivia.py` (sha256 in `documenti.yaml`) | fatto | pagina HTML respinta da archivia (risposta HTML): salvata a parte |
| 5/11 | `padri_ict.py` parametrizzato (anni e uscita); job 2024-2025 sul server in `lavoro/convenzioni/` | in corso | `lavoro/convenzioni/padri-2024-2025.log` |
| | censimento + base dati (`tools/convenzioni/base_dati.py`) | da fare | |
| | pagine del sito (`tools/convenzioni/pagine.py`) | da fare | |
| | verifica rieseguibile (`tools/verifiche/convenzioni_copertura.py`) | da fare | |
