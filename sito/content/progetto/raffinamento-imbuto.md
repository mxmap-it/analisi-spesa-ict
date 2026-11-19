---
title: "Raffinamento dell'imbuto a livelli"
date: 2026-11-19
description: "Come i contratti rimasti nell'imbuto vengono esclusi o confermati con passaggi sempre più costosi: regole, segnali della Banca dati nazionale dei contratti pubblici, lettura con un modello linguistico, ricerca degli atti. Ogni passaggio è registrato e si rifà ogni anno con gli stessi comandi."
weight: 12
gruppo: inizio
---

**Versione 0.2, 19/11/2026** ([#71](https://github.com/mxmap-it/analisi-spesa-ict/issues/71), [#74](https://github.com/mxmap-it/analisi-spesa-ict/issues/74)).
Il quadro d'insieme (dataset, relazioni, mancanze) è nella [Mappa dell'imbuto](/progetto/mappa-imbuto/). I numeri di ogni livello stanno nel rendiconto [«Imbuto: dove siamo»](/rendiconti/imbuto-dove-siamo/) (§ 2.8 e § 2.9); questa pagina dice **come** si ottengono e come si rifanno.

## Il principio

L'[imbuto](/progetto/imbuto/) assegna ogni contratto (CIG) a uno strato con regole sul testo, sul codice CPV, sui lotti delle convenzioni e sui marchi. Per decisione di Fabio (18/11/2026) l'imbuto resta **largo**: un contratto che nomina «software» o «connettività» con un CPV non informatico entra nel perimetro ICT invece di essere escluso a regola.

Sopra l'imbuto si applicano **livelli di raffinamento**, dal più economico al più costoso. Valgono quattro regole:

1. **Nessun livello modifica l'imbuto.** Ogni livello scrive una tabella per CIG (`esiti/<data>/imbuto/…`) con l'esito, il motivo e la via che ha deciso. Il numero finale si ottiene applicando le tabelle in ordine, quindi ogni spostamento si può scomporre e rifare.
2. **Ogni livello lavora solo sul residuo del precedente.** Un CIG già deciso non si rilegge con un mezzo più costoso.
3. **Si esce solo con certezza.** Chi non è sicuro lascia il CIG al livello successivo: «incerto» è una risposta corretta.
4. **Ogni regola nuova ha la sua misura.** È un campione a seme fisso giudicato a mano, pubblicato con il giudizio riga per riga.

Due esiti vanno tenuti distinti:
- **fuori dalla misura cloud:** il contratto resta spesa ICT ma non è un servizio cloud (asse A del [principio a imbuto](/progetto/imbuto/));
- **non ICT:** il contratto esce anche dalla spesa ICT.

## I livelli

| livello | mezzo | ingresso | esce se… | strumento |
|---|---|---|---|---|
| **L1** | regole dell'imbuto (testo, CPV, lotti, marchi) | tutti i CIG ANAC | regole di strato | `tools/analisi/imbuto.py`, `tools/verifiche/imbuto_strati.py` |
| **B** | segnali della Banca dati nazionale dei contratti pubblici (BDNCP) | CIG ICT S3-S6 | vedi sotto: B1 esclude, B2 restringe l'in-house, B3 e B4 misurano | `tools/verifiche/imbuto_bdncp.py` |
| **L2** | regola sul testo | residuo incerto (S6) dal 2024 | stampanti, multifunzione, toner e consumabili, cablaggio, **salvo** che il testo nomini un servizio cloud | `tools/llm/raffinamento.py l2` |
| **L3** | Claude Opus, solo il testo ANAC, senza strumenti né web | CIG S6 entrati solo per «sw» o «connettività», non presi da L2 | categoria «non-ict» o «ict-non-cloud» con certezza **alta** ([istruzioni](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/metodo/llm/raffinamento/istruzioni-l3.md)) | `raffinamento.py prepara-l3 / leggi-l3 / esito` |
| **L4** | Claude Opus con ricerca e archiviazione degli atti (via 6, [acquisizione a livelli](/progetto/acquisizione-documenti/)) | ciò che L3 lascia incerto; i disaccordi sull'asse cloud della revisione | l'atto dell'ente prova che cosa si compra | `raffinamento.py prepara-l4`, `tools/llm/giro_imbuto.sh` |

Il livello B viene prima di L2 perché costa solo una lettura dei dati già archiviati e non legge testo.

## Livello B: i dataset BDNCP

La BDNCP è nel [mirror ANAC](/progetto/mirror-pubblico/): 62 dataset, 129 GB ([inventario](/rendiconti/bdncp-l190/)). L'imbuto ne usava già otto: CIG, SmartCIG, aggiudicatari, aggiudicazioni, CUP, pubblicazioni, stazioni appaltanti e OCDS. Il livello B ne aggiunge cinque. Si legge sempre l'ultimo zip completo di ciascun dataset (`<dataset>_csv.zip`), e il riepilogo registra lo sha256 di ogni file letto.

### B1. Quadro economico: lavori o informatica?

- **Dataset:** `quadro-economico`, importi per natura (forniture, servizi, lavori) e per evento (base d'asta, variante, consuntivo).
- **Calcolo:** quota lavori = lavori / (forniture + servizi + lavori), sull'evento «base d'asta». Se manca, si usa il primo evento con importi.
- **Regola:** un CIG degli strati S5 (ICT non cloud) o S6 (incerto) con quota lavori **≥ 0,8** esce dalla misura cloud. Resta ICT, come per L2. La regola non si applica in due casi:
  - il testo parla di cloud, hosting, data center, CED, sala o locale server, locali informatici o tecnologici, area server: costruire o attrezzare un data center è infrastruttura interna, che è nell'obiettivo (le ultime tre voci dalla regola 0.2);
  - il testo nomina siti web, pagoPA o licenze: sono servizi con il quadro economico compilato male.
- **Strati S3 e S4** (inclusi per convenzione o marchio): nessuna esclusione automatica. I casi con quota lavori alta si elencano come anomalie da rivedere.
- **Misura:** due campioni di 40, con il giudizio in [`report/metodo/bdncp/`](https://github.com/mxmap-it/analisi-spesa-ict/tree/main/report/metodo/bdncp):
  - un campione di sviluppo, da cui sono venute le protezioni;
  - un campione di misura con seme nuovo, a regola ferma: 37 su 40 giusti, Wilson 80-97 % (regola 0.1);
  - regola **0.2** (19/11): protezione estesa a «locali informatici», «locali tecnologici» e «area server», gli errori e i dubbi del campione di misura 0.1. Esclusi 1.274 CIG / 130,6 M€ dal 2024 (erano 1.281 / 131,9); restano nella misura 142 CIG / 34,2 M€ con lavori ma cloud o data center (erano 135 / 33,0). Nuovo campione di misura di 40 CIG mai visti (seme 202611192), annotato a cieco da Claude: **34 giusti, 2 errori, 4 dubbi**, Wilson 71-93 % (82-99 % senza i dubbi). I due errori sono una «stanza server» e il «canone dei siti comunali», non coperti dalla protezione: proposta per la regola 0.3, da misurare su un campione nuovo. Esiti in `esiti/2026-11-19/imbuto/bdncp/v0.2/`, misure dei campioni con `tools/verifiche/bdncp_campioni_misura.py`.

### B2. In-house: società pubbliche o privati?

- **Problema:** la classe «in-house» (contratti affidati a società informatiche pubbliche come Lepida, CSI Piemonte, Insiel) conta come infrastruttura pubblica italiana, ma il dizionario dei nomi vi fa entrare anche dei privati.
- **Dataset:** `aggiudicatari` (codice fiscale di chi vince), `stazioni-appaltanti` e l'Indice PA (`amministrazioni.txt` archiviato). I campi `flag_inHouse` e `flag_partecipata` dell'anagrafica ANAC sarebbero la fonte naturale, ma valgono «false» su tutte le 48.040 righe (raccomandazione R84).
- **Classi**, dalla più forte, in base al codice fiscale dell'aggiudicatario:
  - **ipa:** soggetto pubblico censito nell'Indice PA;
  - **sa-non-ipa:** registrato come stazione appaltante ma non in IPA, quindi può essere privato (TIM, DGS);
  - **non-sa:** privato;
  - **senza aggiudicatario**.
- **Regola:** la classe in-house regge solo con «ipa». Gli altri CIG tornano al residuo da attribuire, senza uscire dalla misura: alcuni sono acquisti per i data center delle in-house, cioè infrastruttura interna.
- **Misura:** campione di 40 «non-sa», con il giudizio in `report/metodo/bdncp/b2-campione-misura.csv`: 40 su 40 aggiudicatari privati.

### B3. Durata effettiva dei contratti

- **Dataset:** `avvio-contratto` (stipula, esecutività, inizio effettivo, termine contrattuale) e `fine-contratto` (ultimazione effettiva).
- **Calcolo:**
  - inizio = inizio effettivo, altrimenti stipula, altrimenti esecutività;
  - fine = ultimazione effettiva, altrimenti termine contrattuale.
- **Uso:** oggi la quota annua di un contratto pluriennale si stima distribuendo l'importo dalla data di pubblicazione per la durata prevista (`bdap_cig_ministeri_cf.quote`). Con le date effettive la stessa quota si ricalcola sui contratti che le hanno. Il livello misura la differenza sugli anni 2024 e 2025, senza sostituire la regola: copre solo una parte dei contratti.

### B4. PNRR: tre vie indipendenti

Per lo stesso CIG ci sono tre segnali candidati, tutti dichiarati dalla stazione appaltante in momenti diversi:
- il campo `FLAG_PNRR_PNC` del CIG;
- la presenza nel dataset `indicatori-pnrrpnc` (quote di genere e giovani, obbligatorie per i contratti PNRR/PNC);
- il CUP nel dataset `cup`.

A questi si aggiunge la catena del progetto, dai finanziamenti PA Digitale 2026 ai CIG (`report/metodo/pnrr-contratti-v3.csv`). La tabella incrociata dice quanto si sovrappongono le vie: è la controvalidazione del sottoinsieme prioritario PNRR (Misure 1.1 e 1.2).

Risultato del 19/11/2026: gli indicatori coincidono con il flag e quindi non sono una via indipendente. Il CUP non distingue il PNRR dagli altri investimenti. Restano due vie indipendenti: il flag e la catena v3.

## Rifarlo ogni anno

Il processo è lo stesso ogni anno. Gira sul server come `mxmap.it`, con `nice`, un job pesante alla volta. Dopo aver aggiornato il mirror ANAC (`tools/verifica_anac.sh scarica`) e rigenerato l'imbuto (`lavoro/imbuto/ict.csv`, [RIPRODURRE.md](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/RIPRODURRE.md)):

```bash
nice .venv/bin/python tools/verifiche/imbuto_strati.py            # L1: strati e numeri dell'imbuto
nice .venv/bin/python tools/verifiche/imbuto_bdncp.py             # B: quadro economico, in-house, durate, PNRR
nice .venv/bin/python tools/llm/raffinamento.py l2                # L2: regola stampanti/consumabili/cablaggio
.venv/bin/python tools/llm/raffinamento.py prepara-l3 tutti       # L3: pacchetti ciechi
nohup setsid tools/llm/raffinamento_catena.sh &                   # L3 (lettura) poi L4 (atti), ripartibile
.venv/bin/python tools/llm/raffinamento.py esito                  # tabella L3 e riepilogo dei livelli
```

- **L3 e L4** usano Claude in abbonamento (`claude -p`) attraverso il tetto di spesa `tools/llm/claude_tetto.py`. Quando il tetto è raggiunto il lavoro si ferma (codice 75). Il guardiano `tools/llm/raffinamento_guardiano.sh`, nel cron ogni 30 minuti, lo fa ripartire da dove era.
- **Riproducibilità:** le istruzioni del modello sono versionate. L3 e L4 non sono deterministici, quindi i loro esiti si conservano in git (`report/metodo/llm/raffinamento*/esiti/`) e si rileggono invece di rigenerarli. Rifarli da zero dà numeri vicini ma non identici, e lo scarto si misura sui campioni.
- **Livelli B e L2** sono deterministici: stessi file (sha256), stesso risultato.

## Registro delle revisioni

| data | versione | modifica |
|---|---|---|
| 2026-11-19 | 0.2 | B1 regola 0.2 (locali informatici e tecnologici, area server) e nuovo campione di misura a cieco: 34/40, Wilson 71-93 % ([#74](https://github.com/mxmap-it/analisi-spesa-ict/issues/74)) |
| 2026-11-19 | 0.1 | prima versione: livelli L1-L4 (decisione di Fabio del 18/11) e livello B con i quattro segnali BDNCP (decisione di Fabio del 19/11) |
