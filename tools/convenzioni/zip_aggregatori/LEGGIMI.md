# Zip degli aggregatori (#62, giro del 7/11) — spostati da lavoro/ per la regola #47

Producono `report/convenzioni/aggregatori/zip-letti-2026-11-07.csv` e (porta.py) l'archiviazione delle copie headless.
Si eseguono sul server con la cartella di lavoro `report/convenzioni/aggregatori/` (dove stanno i CSV e `zip_indice.json`):
1. `estrai.py` apre gli zip dall'archivio content-addressed (sha256 nel CSV del 7/11), scrive i testi in `lavoro/convenzioni/aggregatori/t62_testi/` e `zip_indice.json`;
2. `ox.py` estrae i fogli ODS/XLSX non letti da pdftotext;
3. `zipcsv.py` applica la classificazione letta a mano (dizionario sha256 → tipo e contenuto, livello V) e scrive il CSV;
4. `porta.py` porta le copie scaricate con Chrome headless nell'archivio (`tools/archivia.py --da-file`).
Gli script hanno i percorsi del server scritti dentro: rieseguirli da lì.
