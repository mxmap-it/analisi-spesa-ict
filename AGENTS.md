# AGENTS.md — regole per chi lavora su questo progetto (persone e agenti AI)

Questo file vale per qualunque agente (Claude Code, Codex, Cursor, Copilot, Gemini…).
`CLAUDE.md` rimanda qui. Se una regola cambia, cambiala **qui** e annota il perché in `DECISIONI.md`.

## 1. Prima di iniziare

1. Leggi `STATE.md` (punto di ripresa: cosa gira, prossimi passi, blocchi), poi `DECISIONI.md` (le decisioni prese e il perché).
2. Guarda la board: <https://github.com/orgs/mxmap-it/projects/1> e le issue aperte.
3. **Prendi un ticket prima di lavorare**: assegnatelo e spostalo in *In Progress* (`tools/stato_ticket.sh <n> "In Progress"`). Se il lavoro non ha un ticket, crealo. Non lavorare su un ticket già *In Progress* di altri senza coordinarti nel ticket stesso.
4. Non ri-derivare ciò che è già accertato in `STATE.md`, `DECISIONI.md` o nei rendiconti: richiamalo.

## 2. Obiettivo e perimetro

- **Obiettivo finale (consegnato per ultimo):** misurare la spesa ICT della PA italiana in servizi cloud esterni e datacenter/infrastrutture interne, per giurisdizione (IT / UE / extra-UE, i 4 bucket di mxmap.it), come processo ripetibile ogni anno. **Non ci sono altri obiettivi di analisi.**
- **Obiettivi intermedi, in ordine:** 1) mirror dei dataset; 2) disponibilità e integrità, incluse le discrepanze fra ciò che l'ente dichiara e ciò che pubblica; 3) rendiconto per ente nel tempo; 4) report e presentazioni con evidenze empiriche; 5) analisi degli strumenti (massimo riuso, poco codice nostro); 6) spesa ICT cloud.
- **Fase attuale:** ANAC è il macro-obiettivo. Si chiude ANAC per intero (mirror in tutti i formati, OCDS bulk compreso; criteri di chiusura in `sito/content/progetto/roadmap.md` §8quater), poi gli altri dataset nell'ordine della roadmap (§8ter).
- **Perimetro delle fonti:** solo ciò che serve alla spesa ICT (`sito/content/progetto/perimetro-fonti.md`). Escluse: RNA, INPS, AIFA, DAIT, NoiPA, ministero_salute, OpenCivitas, mef_irpef, pagopa. Le entrate non entrano; la sanità entra solo per il suo ICT. Wayback Machine: abbandonata.
- **Metodo:** la giurisdizione si attribuisce al **prodotto** (dalla descrizione della gara), non al fornitore/rivenditore. Due lenti (prodotto primaria, fornitore secondaria); i rivenditori sono un tema a sé. Sottoinsieme prioritario: fondi PNRR cloud (Misure 1.1 e 1.2) e Polo Strategico Nazionale. Cruscotto Italia (AgID): solo per controvalidare, a fine percorso.

## 3. Regole sulle affermazioni (evitare figuracce)

- Ogni affermazione pubblicata è **verificata da noi e controvalidata** (seconda via indipendente), oppure marcata esplicitamente come *riferita da* (fonte) e *da verificare* con un ticket.
- Mai presentare come fatto ciò che dice un terzo (AgID, DataCivicLab, ecc.) senza averlo riprodotto.
- Ogni problema comunicato a un ente ha: evidenza riproducibile (con sha256), **azione correttiva** e **metrica** che misura che non si ripresenti (metriche I1–I9 in `tools/metriche_anac.py`).
- Citare che AgID conosce e ha reso pubblici i problemi ANAC.
- **Ogni richiesta o raccomandazione** che emerge dal lavoro (ad ANAC, Consip, PSN, Sogei, DTD, ACN…) per rendere questa analisi più facile e manutenibile si annota subito in `report/metodo/richieste-e-raccomandazioni.yaml`, con evidenza, stato (verificato / da verificare / proposta) e riferimenti.
- Niente toni assoluti ("unico al mondo", "morto"): numeri, date, fonti.
- Materiali riservati non si pubblicano: il PDF Proteggimi è una bozza interna (nessuna sua cifra in pubblico). Ad AppaltIntel (commerciale) non si comunica nulla.
- Rispetta robots.txt; non aggirare WAF, Cloudflare o CAPTCHA. Per ANAC serve uno User-Agent da browser (più l'URL del progetto): è documentato come problema, non è un aggiramento.

## 4. Dati e archivio

- Il lavoro lungo gira **sul server**, non sul portatile: `mxmap.it@51.158.36.151`, cartella `~/analisi-spesa-ict` (accesso diretto come `mxmap.it`, mai via `ubuntu`+sudo). Push da lì con l'alias ssh `github-spesaict`.
- Archivio **append-only e content-addressed** (`archivio/blobs/sha256/…`, vista `archivio/mirror/<host>/<path>` via hardlink, `manifest.jsonl` riga per tentativo). Mai sovrascrivere o cancellare blob; mai rigenerare ciò che è costoso se si può ripristinare.
- I dati non vanno in git (`.gitignore`); in git vanno codice, configurazione, rendiconti ed evidenze piccole (`report/**/prove-*`, con `.gitattributes -text` per non alterare gli sha256).
- File di lavoro in `lavoro/`, **mai in `/tmp`** (server condiviso con altri progetti).
- Non usare `pkill -f` con pattern che colpiscono la tua sessione; usa `tools/avvia.sh` e pattern `[t]ools/...`.
- Guardia disco: il mirror si ferma sotto 40 GB liberi.
- **Il server è condiviso con altri progetti** (carico alto, 31 GB di RAM): i job pesanti girano con `nice`, duckdb su disco con `memory_limit` (6 GB) e pochi thread. Il 27/10/2026 un caricamento di tutti i CIG in memoria ha reso il server irraggiungibile.
- Cron sul server: guardiano ogni 15 minuti, sonda 06:10, metriche 06:40. Esiti in `stato/` (giornalieri, mai sovrascritti).
- Ogni job dev'essere ripartibile e idempotente; il progresso si scrive su file, non solo nel contesto dell'agente.

## 5. Codice

- Riuso massimo degli strumenti esistenti (DataCivicLab source-observatory, anac-pl-pp-cli di aborruso, ecc.; vedi `sito/content/progetto/strumenti.md`); scrivere poco codice.
- Python nella `.venv` del server (requests, ijson, DuckDB). Su Windows: I/O sempre in UTF-8.
- Registro delle risorse: `config/risorse.yaml` (formato compatibile con source-observatory).
- Licenze: va bene qualunque licenza libera; tutto viene rilasciato.
- **Ripetibilità da zero:** ogni numero pubblicato dev'essere prodotto da una verifica in `tools/verifiche/` eseguibile da un clone pulito con un solo comando, dal vivo o dallo snapshot (sha256). Niente risultati da script lasciati in `lavoro/` (#47).
- **Attribuzione del cloud provider:** si usano le vie documentate in `sito/content/progetto/metodo-cloud-provider.md`; ogni contratto registra la via che lo ha attribuito; le tabelle curate a mano (lotti, marchi, capogruppo) stanno in `config/` con la fonte di ogni riga. Una via nuova si documenta lì prima di usarla.

## 6. Sito

- Hugo in `sito/`, build in `docs/` (GitHub Pages da `main`), dominio analisi-spesa-ict.mxmap.it. Stesso tema di osservatorio.mxmap.it (Bootstrap Italia, Titillium).
- Comando di build: `hugo --source sito --minify --cleanDestinationDir`; committa insieme sorgente e `docs/`.
- Stile: conciso, in italiano, home centrata sulla spesa ICT. I rendiconti hanno versione e registro delle revisioni.

## 7. Coordinamento e budget

- **Tutto il lavoro è legato a un ticket.** Aggiorna i ticket mentre lavori (commenti con risultati e numeri), chiudili con l'esito, crea ticket nuovi per ogni voce di roadmap emersa. Stati della board: Todo / In Progress / Done.
- Commit piccoli e frequenti, push subito, messaggi in italiano con il riferimento al ticket (`#n`). Fai `git pull --rebase` prima di pushare.
- Aggiorna `STATE.md` a fine sessione; le decisioni nuove vanno in `DECISIONI.md` (data, chi, perché).
- Le decisioni di perimetro, metodo e comunicazione verso gli enti spettano a Fabio Pietrosanti (etichetta `decisione-fabio`): proponi, non decidere.
- Budget token (dopo la chiusura di ANAC): ≤ 20 % del limite settimanale su 7 giorni (`config/budget.yaml`).
- Nessuna comunicazione verso enti o terzi (email, PR su repo altrui, post) senza approvazione di Fabio.
