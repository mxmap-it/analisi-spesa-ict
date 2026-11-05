# Enti campione — documenti di adesione in Amministrazione trasparente (ticket #62)

Data di consultazione: 2026-11-05. File: `enti-campione-2026-11-05.csv` (48 righe, 10 iniziative, 4–5 enti ciascuna).

## Metodo
1. Enti individuati con ricerca web (nome iniziativa / ID Consip / «adesione determina»); la ricerca per CIG padre non ha restituito risultati utili. BDNCP locale non disponibile, quindi niente CIG derivati da ANAC: i CIG derivati riportati sono letti nei documenti.
2. Home istituzionale scaricata una volta (UA dichiarato, ≥3 s fra richieste); `at_raggiungibile_da_home = si` se l'HTML della home contiene il testo/link «Amministrazione trasparente».
3. Documenti scaricati e archiviati con `tools/archivia.py` (sha256 = ultima riga di `archivio/manifest.jsonl` per l'URL); testo estratto con `pdftotext` (prime 6 pagine) per oggetto, CIG, importi.
4. `esito`: `trovato-in-AT` se l'URL sta sotto un percorso AT / bandi di gara e contratti / profilo del committente; `trovato-fuori-AT` se il file è in repository generici (`wp-content`, `fileadmin`, `cmsresources`, `statics`…) o su siti terzi. Il collegamento effettivo dalla pagina AT al file **non** è stato verificato (R).

## Limiti
- Campione di comodo (ciò che i motori indicizzano), sbilanciato su autorità e ministeri; pochi comuni grandi e ASL.
- Alcune righe sono «di controllo»: documento trovato ma riferito a un'edizione o ID diverso (OGS → PC portatili ed. successiva; ASL VCO → ID 2365; CONSOB/Polizia → Multibrand precedente; Insubria SM → nessuna adesione). È indicato nelle note.
- URL indicizzati ma ora 404 (AgID `download/*.html`, AUSL Modena, sanita.puglia.it) → `non-trovato`; Regione Abruzzo (errore TLS), legacy.ats-brescia.it, CONSOB (503) → `AT-irraggiungibile`.
- esteri.it e ministeroturismo.gov.it: la home restituisce una challenge anti-bot, non aggirata.
- Pagine HTML (Regione Siciliana DRG 2316, scheda ISTAT) non archiviate: `archivia.py` accetta solo file.
- Nelle note: V = visto nel documento o nella risposta HTTP; R = dedotto (anche dagli snippet dei motori di ricerca).
