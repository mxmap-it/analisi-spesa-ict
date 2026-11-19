---
title: "Cruscotto dei contratti: cercare, controllare, annotare"
date: 2026-11-19
description: "Ogni contratto dell'imbuto si può cercare per testo, ente, aggiudicatario, CPV, strato e livello. Per ciascuno si vede che cosa ha deciso ogni passaggio del metodo, con gli atti archiviati, e lo si può annotare. I totali per strato e giurisdizione portano all'elenco dei contratti che li compongono."
weight: 14
gruppo: inizio
---

**Versione 0.1, 19/11/2026** ([#53](https://github.com/mxmap-it/analisi-spesa-ict/issues/53), [#78](https://github.com/mxmap-it/analisi-spesa-ict/issues/78), mancanza M13 della [Mappa dell'imbuto](/progetto/mappa-imbuto/)).

**Apri il cruscotto:** [analisi-spesa-ict.mxmap.it/contratti/](/contratti/). La stessa pagina è servita anche dal servizio delle annotazioni: [annotazioni.51-158-36-151.sslip.io/contratti](https://annotazioni.51-158-36-151.sslip.io/contratti).

Decisione di Fabio del 19/11/2026: con la pubblicazione dei risultati, **tutti** i contratti dell'imbuto devono essere ricercabili e annotabili. Chi legge un numero deve poter vedere da quali contratti nasce, chi ha deciso che cosa e segnalare un errore. È il controllo pubblico sul metodo.

## Che cosa si può fare

1. **Cercare** per parole dell'oggetto, stazione appaltante, aggiudicatario, CPV o CIG. Si può filtrare per strato, gruppo, giurisdizione, provider, anno, importo, livello di raffinamento ed esito, e scaricare l'elenco in CSV (fino a 10.000 righe).
2. **Aprire la scheda di un contratto**, che mostra:
   - i dati ANAC: oggetto, ente, aggiudicatari, CPV, importo;
   - lo strato dell'[imbuto](/progetto/imbuto/), con via, provider e giurisdizione;
   - che cosa ha detto **ogni livello** di [raffinamento](/progetto/raffinamento-imbuto/): esito, certezza, motivazione, fonti e file di origine;
   - i segnali della Banca dati nazionale dei contratti pubblici: quadro economico, durate, PNRR;
   - gli atti archiviati, con URL e sha256;
   - le annotazioni già ricevute.
3. **Annotare** il contratto. Si risponde a sei domande: è ICT? è cloud? che tipo di servizio è? qual è la giurisdizione del provider del prodotto? serve un documento? quanto sei sicuro? Si possono aggiungere una nota e il provider.
4. **Ripartire dai totali.** Le tabelle strato × giurisdizione, strato × gruppo e livello × esito, per gli anni scelti, portano con un clic all'elenco dei contratti che compongono ogni cella.

## Che cosa contiene [V]

L'indice si costruisce da `lavoro/imbuto/ict.csv` (imbuto 0.3.4). Gli strati sono quelli che l'imbuto scrive: S0 (padri di accordo quadro), S2 ICT sotto soglia, S3-S6, dal 2020.

- **667.303 CIG**, di cui **289.192** negli strati S3-S6 dal 2024 (il perimetro della misura).
- **S1** (non ICT, circa 5 milioni di CIG) e S2 non ICT **non sono nell'indice**: l'imbuto li esclude e non li scrive.
- Esiti dei livelli: 175.175 righe su 167.701 CIG.

| livello | che cosa dice | CIG con esito | fonte |
|---|---|---:|---|
| L2 | regola su stampanti, consumabili, cablaggio: fuori dalla misura cloud | 6.980 | `esiti/2026-11-18/imbuto/raffinamento-l2.csv` |
| B1 | quadro economico: quota lavori ≥ 0,8, esce; oppure anomalia S3/S4 | 1.916 | `esiti/2026-11-19/imbuto/bdncp/segnali.csv` |
| B2 | in-house: classe dell'aggiudicatario (ipa, sa-non-ipa, non-sa, senza) | 962 | idem |
| B4 | PNRR: quali delle vie indipendenti lo segnalano | 148.378 | idem |
| L3 | lettura del testo con Claude Opus | 3.540 | `esiti/2026-11-18/imbuto/raffinamento-l3.csv` |
| via 6 | classificazione con ricerca degli atti (G1 e G3) | 1.242 | `dati/classificazioni/imbuto-g1g3.jsonl` |
| revisione | revisione C1-C4 dei casi discordi | 273 | `dati/classificazioni/imbuto-revisione.jsonl` |
| L4 | via 6 sul residuo di L3 (**in corso**) | 107 | `report/metodo/llm/raffinamento-l4/esiti/` |
| licenze | asse cloud delle licenze S4 | 3.889 | `esiti/2026-11-18/imbuto/licenze-cig.csv` |
| tetti | massimali e accordi quadro | 174 | `esiti/2026-11-18/imbuto/tetti-cig-v2.csv` |
| campione a cieco | annotazione alla cieca di Claude (campione v3) | 601 | `dati/classificazioni/campione-v3.jsonl` |
| atti cercati | che cosa ha trovato l'[acquisizione degli atti](/progetto/acquisizione-documenti/) | 7.113 | `esiti/2026-11-19/imbuto/residuo-s6-per-66.csv` |

1.966 esiti riguardano CIG che non sono nell'indice, per esempio CIG in S1 o del campione v3 di versioni precedenti dell'imbuto. Restano nei file di origine. Gli atti archiviati sono 4.463 righe su 1.479 CIG (`dati/atti/`).

**Nessun livello modifica l'imbuto.** La scheda mostra lo strato dell'imbuto e, accanto, gli esiti dei livelli. La tabella unica degli spostamenti per CIG (L1, B, L2, L3, L4), con lo stato finale di ogni contratto, è una voce a sé del rendiconto del risultato parziale (#78). Quando esisterà, entrerà nell'indice come colonna in più.

## I totali riproducono l'imbuto [V]

La verifica `tools/verifiche/cruscotto_riproduzione.py` ricalcola dall'indice CIG ed euro per anno, strato, sottoclasse, gruppo, giurisdizione e importo anomalo. Usa la stessa regola dell'imbuto: i padri S0 contano 0 €. Poi confronta il risultato riga per riga con il riepilogo pubblicato (`esiti/2026-11-18/imbuto/riepilogo-0.3.4.json`, sha256 `546e5ce4…`).

Esito del 19/11/2026: **341 righe su 341 uguali**, 667.303 CIG e 160.412.604.641 € da entrambe le parti, nessun esito senza contratto e nessun codice fiscale fra gli aggiudicatari (`esiti/2026-11-19/cruscotto/riproduzione.json`). I numeri delle tabelle del cruscotto sono quindi quelli dell'imbuto, e ogni cella porta ai CIG che la compongono.

## Annotazioni: a supporto e controllo, separate dal campione a cieco

Le annotazioni del cruscotto usano lo stesso servizio e lo stesso archivio delle [annotazioni dei volontari](/annotazioni/) (`tools/annotazioni/server.py`, `stato/annotazioni.sqlite`, esportazione oraria in `dati/annotazioni/annotazioni.jsonl`). Ogni riga ha due campi nuovi:

- `modo`: «cieco» per le letture indipendenti del campione (pagina delle annotazioni), «cruscotto» per le annotazioni libere fatte qui;
- `ict`: la risposta alla domanda «è spesa ICT?».

Nel cruscotto chi annota **vede** le nostre classificazioni, quindi le sue annotazioni non sono letture indipendenti. Non entrano nelle misure di precisione alla cieca: i campioni a cieco restano annotati da Claude (decisione di Fabio del 19/11/2026). Servono a segnalare errori e documenti: ogni annotazione con un documento indicato entra nella coda `dati/annotazioni/documenti-da-cercare.jsonl` per i crawler.

Le annotazioni sono pubbliche nella scheda del contratto **senza il nome** di chi annota. L'hash dell'IP resta sul server, solo contro gli abusi. Il servizio accetta al massimo 30 annotazioni e 120 ricerche al minuto per indirizzo.

## Dati personali

Il dataset ANAC «aggiudicatari» pubblica nome e codice fiscale anche delle persone fisiche: professionisti e imprenditori individuali. L'indice li tratta così:

- un aggiudicatario con codice fiscale personale (16 caratteri) diventa «[persona fisica]» nel campo aggiudicatari e, se il nome compare, anche nell'oggetto e nelle motivazioni dei livelli;
- nei CIG con almeno una persona fisica si oscurano anche gli aggiudicatari senza forma societaria (srl, spa, società, consorzio…), per non lasciare passare varianti del nome;
- i codici fiscali non entrano mai nell'indice.

Sono **15.585 CIG** [V], di cui 9.062 negli strati S3-S6 dal 2024. La verifica controlla che nessun aggiudicatario dell'indice contenga un codice fiscale.

**Limite:** l'oggetto del contratto è scritto dall'ente e può citare persone che non sono aggiudicatarie, per esempio il RUP o un consulente. Non lo filtriamo: il testo resta quello pubblicato da ANAC. Chi trova un dato personale può segnalarlo con un'annotazione, e lo togliamo.

## Architettura: perché una pagina statica più il servizio esistente

- **Pagina:** un file HTML senza dipendenze esterne (`tools/cruscotto/pagina.html`, copiato in `sito/static/contratti/`). Sta sul sito su GitHub Pages ed è servita anche da `/contratti` del servizio.
- **Dati:** l'indice SQLite con ricerca a testo pieno FTS5 pesa circa 500 MB. È troppo per GitHub Pages (limite di 100 MB per file) e per una ricerca nel browser (sql.js o DuckDB-WASM scaricherebbero centinaia di MB).
- **Servizio:** abbiamo esteso quello delle annotazioni, che è già pubblico in HTTPS. Non servono porte, domini o proxy nuovi: solo endpoint in sola lettura sull'indice.
  - `GET /api/cerca`: ricerca con filtri e CSV;
  - `GET /api/contratto`: la scheda di un CIG;
  - `GET /api/totali`: i totali per il drilldown.

  Le risposte arrivano in pochi centesimi di secondo; i totali in circa 1 s la prima volta, poi vengono dalla memoria.
- **Codice nuovo:** circa 180 righe nel servizio, 230 nello script dell'indice, 250 nella pagina e 65 nella verifica.

Datasette sarebbe stato un'alternativa senza codice per la ricerca. Però non ha l'annotazione integrata né il drilldown dai totali, e sarebbe un servizio in più da esporre.

## Come si rifà

Sul server, come `mxmap.it`, dopo ogni nuova versione dell'imbuto o di un livello:

```
nice -n 15 .venv/bin/python tools/cruscotto/indice_contratti.py              # ~70 s, ~450 MB di RAM
.venv/bin/python tools/verifiche/cruscotto_riproduzione.py --json esiti/<data>/cruscotto/riproduzione.json
```

Lo script prende l'esito più recente di ogni livello (`esiti/<data più alta>/…`). Scrive l'indice in un file temporaneo e lo sostituisce solo alla fine, quindi il servizio resta acceso e legge subito il nuovo indice. Registra lo sha256 di ogni ingresso in `esiti/<data>/cruscotto/indice.json`. L'indice non va in git: è derivato e si rifà da zero con lo stesso comando.

## Limiti e prossimi passi

- **L4 è in corso:** la scheda mostra gli esiti disponibili alla costruzione dell'indice. Oggi l'indice si ricostruisce a mano.
- **Proposta per Fabio:** ricostruire l'indice ogni notte con il cron, dopo i livelli, e aggiornare la pagina nel sito.
- **Stato finale per CIG:** arriverà con la tabella unica degli spostamenti (#78).
- **B3 (durate)** non è un esito: compare solo nella scheda, perché non sposta i contratti fra gli strati.
- **Indirizzo del servizio:** oggi è un nome sslip.io legato all'IP del server. **Proposta per Fabio:** un nome stabile sul dominio del progetto, per esempio `api.analisi-spesa-ict.mxmap.it`. Serve un record DNS e una riga nella configurazione di Caddy; non l'abbiamo fatto.

## Registro delle revisioni

| data | versione | modifica |
|---|---|---|
| 2026-11-19 | 0.1 | prima versione: indice di tutti i CIG dell'imbuto con gli esiti di 12 livelli, ricerca, scheda, annotazione libera (modo «cruscotto»), totali con drilldown riprodotti riga per riga dall'imbuto, persone fisiche oscurate |
