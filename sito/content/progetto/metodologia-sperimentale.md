---
title: "Metodologia sperimentale in corso"
date: 2026-10-29
description: "Stato del lavoro sperimentale sulla classificazione dei contratti cloud: regole, modelli linguistici con ricerca delle fonti, verifica della confidenza, base di conoscenza, analisi delle infrastrutture, modelli tabulari, tetto di computazione."
weight: 15
---

Questa pagina descrive **il lavoro in corso**: metodi in sperimentazione, cosa abbiamo misurato finora e cosa resta da decidere. I numeri pubblicati nei rendiconti usano solo i metodi già consolidati ([metodo di attribuzione](../metodo-cloud-provider/)). Si aggiorna a ogni passo, con il registro delle revisioni in fondo.

## 1. Il problema

Vogliamo sapere, contratto per contratto (CIG), se si compra cloud, quale **prodotto**, e sotto quale **giurisdizione** (IT, UE, extra-UE). Le regole sul testo dei contratti non bastano:

- il testo spesso nomina il **rivenditore** (TIM, Fastweb) e non il prodotto;
- le sigle delle convenzioni ("SPC Cloud lotto 4", "LAN 8", "PSN") vanno interpretate;
- alcune parole ingannano: "AWS" in un contratto di stazioni meteo, "Azure" in un pacemaker.

## 2. Le vie di classificazione

| via | cosa fa | stato |
|---|---|---|
| regole (vie 1-5, 7) | lotti di convenzione, marchi, fornitore = provider | in uso (v3.1); v3.2 in preparazione con gli errori trovati dalla via 6 |
| **via 6: modello linguistico + fonti** | un agente legge il contratto, cerca la determina dell'ente in Amministrazione trasparente, la scarica, la archivia (sha256), ne estrae il testo (anche OCR) e classifica | **in sperimentazione** |
| revisione umana | annotazione alla cieca di un campione | in preparazione |
| modelli fondazionali tabulari (TabICL) | secondo classificatore senza token, addestrato sui casi etichettati | protocollo scritto ([#56](https://github.com/mxmap-it/analisi-spesa-ict/issues/56)) |

## 3. Cosa abbiamo misurato (campione di 611 contratti)

- **Giro 1** (modello linguistico solo sul testo, 611 contratti): 404 confidenza alta, 161 media, 46 bassa. Il modello non concorda con le regole v3.1 in **204 casi**: da qui l'elenco degli errori delle regole.
- **Giro 2** (verifica sulle fonti, 337 contratti dubbi + 31 di controllo):
  - lo strumento web generico dell'agente non legge i PDF: 0 atti in 45 contratti; per questo abbiamo scritto `tools/llm/atti.py` (scarica, archivia, estrae il testo);
  - **confronto tra modelli sugli stessi contratti:**

    | | Haiku | Sonnet |
    |---|---|---|
    | documenti archiviati | 3 su 25 contratti | 22 su 10 contratti |
    | «fonte primaria» dichiarata senza prova | 4 su 6 | 0 |
    | righe malformate | 10 su 80 | 0 |

    Haiku è stato scartato; il giro prosegue con Sonnet, poi Opus sui casi rimasti incerti;
  - **limite strutturale:** anche con Sonnet un atto dell'ente che cita il CIG si trova in circa 1 contratto su 10. Molti siti degli enti rispondono con errori, molti atti sono scansioni, la ricerca del CIG non li restituisce. Questo è un limite di come si pubblica, non del metodo: ne nasce la raccomandazione R17.

## 4. La confidenza: definita, poi verificata dal codice, poi misurata

La definizione operativa è nel [formato della classificazione](../formato-classificazione/). In breve:

- **alta, media, bassa** sono definite da condizioni ricontrollabili;
- il codice (`verifica_esiti.py`) corregge la confidenza dichiarata dal modello quando manca la prova. Nel giro 2 ha corretto 16 esiti su 70 di Haiku e 4 su 10 di Sonnet;
- la **precisione** di ogni livello si misura su un campione rivisto alla cieca. Nei numeri pubblicati come fatti entra solo ciò che ha precisione misurata di almeno il 95%.

## 5. Base di conoscenza e analisi delle infrastrutture

- **Iniziative** (Consip, PSN, regionali): lotti, aggiudicatari, prodotti, giurisdizione, con stato verificato, riferito o controvalidato (due fonti indipendenti). Vedi [iniziative Consip e PSN](../iniziative-consip-cloud/) (in bozza).
- **Criterio di cloud sovrano** (deciso il 29/10/2026): data center in Italia/UE e operatore a controllo UE non soggetto a leggi extraterritoriali (modello SecNumCloud 3.2). Il software extra-UE si registra come dipendenza tecnologica.
- **Infrastrutture dubbie:** si analizzano con un modello in 8 domande: dati, operatore, catena di controllo, ruoli e accessi, CLOUD Act, dipendenze, qualifiche, esito. Primo caso svolto: Sistema Cloud Toscana, esito «sovrano IT condizionato», perché il ruolo dei partner USA non è pubblico.
- **PSN:** allineato all'[analisi dell'Osservatorio](https://osservatorio.mxmap.it/psn/). I servizi nativi sono IT; Secure Public Cloud e PSN Managed sono su tecnologia extra-UE.

## 6. Artefatti intermedi e riproducibilità

Pubblichiamo in formati aperti, con schema:

- il **registro di classificazione** per CIG, con tutti i passaggi;
- i **collegamenti CIG → atti**, con sha256 e testo estratto;
- la base di conoscenza;
- le istruzioni date ai modelli (versionate);
- le conversazioni di lavoro con gli agenti.

Vedi il [formato della classificazione](../formato-classificazione/).

## 7. Costo e tetto di computazione

I compiti automatici di Claude sul server passano da un tetto (`tools/llm/claude_tetto.py`). Ogni chiamata registra token e costo equivalente; oltre il tetto giornaliero o settimanale il lavoro si ferma e riparte da dov'era. Il tetto si tara confrontando il registro con il contatore del piano.

## 8. Cosa resta da decidere

- annotatori e campione per la revisione alla cieca; pagina pubblica per volontari;
- soglia di precisione per usare l'«alta» del modello nei numeri;
- esito della sperimentazione TabICL;
- per Cloud Toscana, se chiedere l'accesso agli atti all'offerta tecnica;
- invio delle raccomandazioni R16-R19 (dopo approvazione).

## Registro delle revisioni

| data | modifica |
|---|---|
| 2026-10-29 | prima versione: giri 1-2 della via 6, confronto Haiku/Sonnet, confidenza verificata, cloud sovrano, Cloud Toscana, TabICL, tetto |
