# Prova di ripetibilità dell'imbuto, 2026-11-19

Rifatto da zero in `lavoro/ripetibilita/2026-11-19` con `tools/verifiche/ripetibilita.sh`, confronto con `tools/verifiche/ripetibilita_confronta.py`. Commit 07ec7dcd. Durata dei passi: 69.0 minuti.

| passo | durata | codice |
|---|---:|---:|
| a1-prepara | 6 min 21 s | 1 |
| a1-prepara | 6 min 3 s | 0 |
| a2-imbuto-A | 49 min 42 s | 0 |
| b1-strati-rigenera | 0 min 3 s | 0 |
| b2-strati | 0 min 0 s | 0 |
| b3-tetti-rigenera | 3 min 7 s | 0 |
| b4-tetti | 0 min 0 s | 0 |
| b5-revisione | 0 min 0 s | 0 |
| b6-licenze-rigenera | 0 min 3 s | 0 |
| b7-licenze | 0 min 0 s | 0 |
| b8-cig-ripetuti | 0 min 3 s | 0 |
| c1-bdncp | 3 min 33 s | 0 |
| d1-l2 | 0 min 5 s | 0 |
| d2-esito-l3 | 0 min 1 s | 0 |

| passo | file pubblicato | esito |
|---|---|---|
| a | `lavoro/imbuto/ict.csv` | uguale nel contenuto, ordine delle righe diverso (sha256 canonico uguale) |
| a | `esiti/2026-11-18/imbuto/riepilogo-0.3.4.json` | uguale (sha256) |
| b | `esiti/2026-11-18/imbuto/distribuzione.json` | uguale nei numeri: 59 campi diversi solo per virgola-mobile 58, sha256-ict-ordine-righe 1 (Δ massimo 1.2e-04 €) |
| b | `esiti/2026-11-18/imbuto/strati.json` | uguale nei numeri: 11 campi diversi solo per virgola-mobile 11 (Δ massimo 6.1e-05 €) |
| b | `esiti/2026-11-18/imbuto/tetti-cig.csv` | uguale (sha256) |
| b | `esiti/2026-11-18/imbuto/tetti-fonti.json` | uguale nei numeri: 1 campi diversi solo per sha256-ict-ordine-righe 1 |
| b | `esiti/2026-11-18/imbuto/tetti.json` | uguale (sha256) |
| b | `esiti/2026-11-18/imbuto/tetti-cig-v2.csv` | uguale (sha256) |
| b | `esiti/2026-11-18/imbuto/revisione.json` | uguale (sha256) |
| b | `esiti/2026-11-18/imbuto/licenze-cig.csv` | uguale nel contenuto, ordine delle righe diverso (sha256 canonico uguale) |
| b | `esiti/2026-11-18/imbuto/licenze.json` | uguale (sha256) |
| b | `esiti/2026-11-18/imbuto/cig-ripetuti.json` | uguale (sha256) |
| b | `esiti/2026-11-18/imbuto/cig-ripetuti.csv` | uguale (sha256) |
| c | `esiti/2026-11-19/imbuto/bdncp/riepilogo.json` | uguale nei numeri: 1 campi diversi solo per sha256-ict-ordine-righe 1 |
| c | `esiti/2026-11-19/imbuto/bdncp/campione-b1-esce-lavori.csv` | uguale (sha256) |
| c | `esiti/2026-11-19/imbuto/bdncp/campione-b2-non-sa.csv` | uguale (sha256) |
| c | `esiti/2026-11-19/imbuto/bdncp/segnali.csv` | uguale (sha256) |
| d | `esiti/2026-11-18/imbuto/raffinamento-l2.csv` | uguale nel contenuto, ordine delle righe diverso (sha256 canonico uguale) |
| d | `esiti/2026-11-18/imbuto/raffinamento-l2.json` | uguale nei numeri: 1 campi diversi solo per sha256-ict-ordine-righe 1 |
| d | `esiti/2026-11-18/imbuto/raffinamento-l2-campione.csv` | uguale (sha256) |
| d | `esiti/2026-11-18/imbuto/raffinamento-l3.csv` | uguale (sha256) |
| d | `esiti/2026-11-18/imbuto/raffinamento-l3.json` | uguale (sha256) |

## Ingressi

- Mirror ANAC letto dal passo a: 243 file zip, 2.7 GB (sha256 in esito.json).
- Codice e configurazione: sha256 in esito.json.
- Ingressi fuori dall'archivio e fuori da git:
  - `lavoro/pvl/cig_link.csv` (imbuto_strati (link PVL per strato)): in git = False
  - `lavoro/convenzioni/attuativi.csv` (imbuto_licenze (attuativi delle convenzioni)): in git = False
  - `lavoro/raffinamento/pacchetti/d*.jsonl` (raffinamento.py esito (ingresso di L3: importo e oggetto)): in git = False

## Cause delle differenze e deviazioni

- **Ordine delle righe** (ict.csv, licenze-cig.csv, raffinamento-l2.csv): imbuto_prova_034.py legge il delta da duckdb con `preserve_insertion_order=false` e 2 thread, quindi l'ordine delle righe di ict.csv cambia da un'esecuzione all'altra; chi legge ict.csv in sequenza eredita l'ordine. Il contenuto è identico (sha256 canonico, righe ordinate, uguale). Per questo lo sha256 di ict.csv registrato da tetti-fonti.json, bdncp/riepilogo.json e raffinamento-l2.json è diverso. Correzione proposta: scrivere ict.csv ordinato per (anno, cig) e registrare lo sha256 canonico.
- **Virgola mobile** (distribuzione.json, strati.json, solo i campi `euro` e `euro_link` non arrotondati del link PVL): somme parallele di duckdb in ordine diverso, differenza massima sotto 0,001 €. Correzione proposta: arrotondare al centesimo.
- **Deviazione della prova**: «prepara» è andata in Out of Memory con 8 GB di memoria virtuale (ulimit -v) mentre il 9/11 era riuscita; rifatta con 12 GB (memory_limit di duckdb invariato a 4 GB). La variante A ha girato con 8 GB come l'originale.
- **Ingressi fuori dall'archivio content-addressed e fuori da git**: lavoro/pvl/cig_link.csv (scaricamento API PVL del 4/11), lavoro/convenzioni/attuativi.csv, lavoro/raffinamento/pacchetti/ (ingressi di L3). Oggi sono sul server e la prova li ha riletti; da un clone pulito mancherebbero. Correzione proposta: versionarli o archiviarli con sha256.
- **Esiti del modello linguistico**: L3, L4 e via 6 non si rigenerano: si rileggono gli esiti versionati in git.

## Non ripetibili per natura

- **L3**: Claude Opus legge il testo (report/metodo/llm/raffinamento/esiti/, versionati): si rilegge, non si rigenera
- **L4**: Claude Opus cerca e legge gli atti (report/metodo/llm/raffinamento-l4/esiti/, versionati; atti con sha256 in dati/atti/)
- **via6_revisione**: letture del modello (report/metodo/llm/imbuto-g1g3, imbuto-revisione): ingressi versionati di imbuto_revisione
