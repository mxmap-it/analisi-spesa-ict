---
title: "Metodologia sperimentale in corso"
date: 2026-10-29
description: "Stato del lavoro sperimentale sulla classificazione dei contratti cloud: regole, modelli linguistici con ricerca delle fonti, verifica della confidenza, base di conoscenza, analisi delle infrastrutture, modelli tabulari, tetto di computazione."
weight: 15
---

Questa pagina descrive **il lavoro in corso**: metodi in sperimentazione, cosa abbiamo misurato finora e cosa resta da decidere. I numeri pubblicati nei rendiconti usano solo i metodi già consolidati ([metodo di attribuzione](../metodo-cloud-provider/)). Si aggiorna a ogni passo, con il registro delle revisioni in fondo.

## 1. Il problema

Vogliamo sapere, contratto per contratto (CIG), se si compra cloud, quale **prodotto** e sotto quale **giurisdizione** (IT, UE, extra-UE). Detta così sembra una domanda semplice. Non lo è, e conviene dire perché.

## 2. Perché non è facile: le criticità

**Nei dati pubblici l'informazione che serve non c'è**

- **Il prodotto non è un campo.** Nella banca dati nazionale dei contratti pubblici (BDNCP/ANAC) ci sono l'oggetto in testo libero, il CPV, l'importo e l'aggiudicatario. Nessun campo dice quale prodotto si compra e chi lo produce (R16).
- **L'aggiudicatario spesso non è il produttore.** Licenze Microsoft o storage Pure Storage passano da rivenditori italiani come TIM o Fastweb. Attribuire per fornitore darebbe "IT" a prodotti statunitensi.
- **Il collegamento al contratto attuativo manca.** Spesso il contratto attuativo non è collegato alla convenzione o all'accordo quadro da cui deriva (R01). Così si perde l'informazione sul lotto, e quindi sul provider.
- **Gli atti degli enti sono difficili da raggiungere.** Le determine sono PDF, spesso scansioni. I siti rispondono con errori. Cercando il CIG l'atto quasi mai esce. Anche con l'agente migliore si trova l'atto che cita il CIG in circa 1 contratto su 10 (R17).

**Il testo dei contratti inganna**

- **Parole ambigue:** "AWS" significa anche Automatic Weather Stations; "Azure S DR" è un pacemaker; "PSN" nel testo non vuol dire acquisto di servizi PSN; "lotto 1" non indica per forza un accordo quadro cloud; "cloud" compare in nomi di prodotti installati presso l'ente (IBM Cloud Pak).
- **Sigle delle convenzioni:** "SPC Cloud" copre quattro lotti molto diversi, di cui solo il primo è cloud. "PSN Managed" comprende due architetture diverse. Per decifrarle serve una conoscenza costruita a parte.
- **Ruoli invertiti:** l'ente acquirente (ARIA, Sogei, CINECA) viene scambiato per il fornitore.

**La giurisdizione non è un'etichetta semplice**

- **Conta chi controlla il servizio, non dove sono i server.** Un data center in Italia gestito da un operatore soggetto al CLOUD Act non è sovrano.
- **I raggruppamenti sono misti.** Ci sono membri italiani e statunitensi, e il riparto dei compiti non è pubblico (caso Cloud Toscana, R19).
- **Lo stesso nome copre cose diverse.** Il PSN ha servizi nativi italiani e servizi su tecnologia di hyperscaler USA.

**Il costo**

- Leggere e verificare ogni contratto con un modello linguistico costa calcolo e tempo, e i contratti sono centinaia di migliaia ogni anno. Serve un metodo che riduca la parte costosa anno dopo anno.

## 3. La strategia: più approcci indipendenti che convergono

Nessuna via da sola dà una confidenza elevata. La otteniamo **incrociando vie indipendenti** e **misurando** quanto ciascuna sbaglia.

1. **Regole deterministiche:** gratuite, ripetibili, coprono i casi chiari (lotti di convenzione, marchi univoci). Ogni errore trovato dalle altre vie diventa un caso di test e una regola corretta.
2. **Base di conoscenza delle iniziative:** convenzioni, lotti e servizi PSN decifrati una volta per tutte, con fonti controvalidate. Un contratto attuativo eredita prodotto e giurisdizione dalla convenzione.
3. **Modello linguistico con ricerca degli atti (via 6):** legge il contratto e cerca l'atto dell'ente. Ogni documento letto viene archiviato con sha256, così la prova resta verificabile.
4. **Verifica della confidenza da parte del codice:** il modello dichiara una confidenza, il codice la accetta solo se la prova c'è davvero.
5. **Revisione umana alla cieca:** misura la precisione di ogni via e di ogni livello. È l'unica cosa che trasforma «alta» in un numero, per esempio «precisione 97%, intervallo 94-99%».
6. **Secondo classificatore tabulare (TabICL, da sperimentare):** se si dimostra utile, filtra i casi facili senza consumare token e segnala quelli in cui le vie non concordano.
7. **Analisi caso per caso delle infrastrutture dubbie:** un modello in 8 domande, con esito ed elenco dei punti aperti.

**Concordanza come segnale.** Quando regole, base di conoscenza e modello concordano, ed esiste un documento archiviato, la classificazione è affidabile. Quando non concordano, il caso va in revisione: è lì che si impara.

## 4. Capitalizzare la conoscenza: ogni anno costa meno

- **Le correzioni diventano regole.** Ogni errore scoperto (dal modello, dalla revisione, da un atto) diventa un caso di test e una regola. Il residuo da affidare al modello cala ogni anno.
- **Le convenzioni si decifrano una volta.** Ogni convenzione o infrastruttura analizzata entra nella base di conoscenza e serve a tutti i contratti che vi aderiscono, negli anni successivi.
- **Gli atti si cercano una volta.** Ogni atto trovato entra nel dataset CIG → atti, con il suo sha256. Non va più cercato, ed è riutilizzabile da terzi.
- **Ogni ostacolo diventa una richiesta di policy** (R01–R19) ad ANAC, Consip, AgID e agli enti, perché il dato nasca già strutturato. È la via più efficace per rendere la misura facile negli anni a venire.
- **Tutto è aperto e versionato:** codice, istruzioni ai modelli, dataset intermedi, conversazioni. Chi viene dopo, noi compresi, riparte da dove siamo arrivati.

## 5. Le vie di classificazione

| via | cosa fa | stato |
|---|---|---|
| regole (vie 1-5, 7) | lotti di convenzione, marchi, fornitore = provider | in uso (v3.1); v3.2 in preparazione con gli errori trovati dalla via 6 |
| **via 6: modello linguistico + fonti** | un agente legge il contratto, cerca la determina dell'ente in Amministrazione trasparente, la scarica, la archivia (sha256), ne estrae il testo (anche OCR) e classifica | **in sperimentazione** |
| revisione umana | annotazione alla cieca di un campione | in preparazione |
| modelli fondazionali tabulari (TabICL) | secondo classificatore senza token, addestrato sui casi etichettati | protocollo scritto ([#56](https://github.com/mxmap-it/analisi-spesa-ict/issues/56)) |

## 6. Cosa abbiamo misurato (campione di 611 contratti)

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

## 7. La confidenza: definita, poi verificata dal codice, poi misurata

La definizione operativa è nel [formato della classificazione](../formato-classificazione/). In breve:

- **alta, media, bassa** sono definite da condizioni ricontrollabili;
- il codice (`verifica_esiti.py`) corregge la confidenza dichiarata dal modello quando manca la prova. Nel giro 2 ha corretto 16 esiti su 70 di Haiku e 4 su 10 di Sonnet;
- la **precisione** di ogni livello si misura su un campione rivisto alla cieca. Nei numeri pubblicati come fatti entra solo ciò che ha precisione misurata di almeno il 95%.

## 8. Base di conoscenza e analisi delle infrastrutture

- **Iniziative** (Consip, PSN, regionali): lotti, aggiudicatari, prodotti, giurisdizione, con stato verificato, riferito o controvalidato (due fonti indipendenti). Vedi [iniziative Consip e PSN](../iniziative-consip-cloud/) (in bozza).
- **Criterio di cloud sovrano** (deciso il 29/10/2026): data center in Italia/UE e operatore a controllo UE non soggetto a leggi extraterritoriali (modello SecNumCloud 3.2). Il software extra-UE si registra come dipendenza tecnologica.
- **Infrastrutture dubbie:** si analizzano con un modello in 8 domande: dati, operatore, catena di controllo, ruoli e accessi, CLOUD Act, dipendenze, qualifiche, esito. Primo caso svolto: Sistema Cloud Toscana, esito «sovrano IT condizionato», perché il ruolo dei partner USA non è pubblico.
- **PSN:** allineato all'[analisi dell'Osservatorio](https://osservatorio.mxmap.it/psn/). I servizi nativi sono IT; Secure Public Cloud e PSN Managed sono su tecnologia extra-UE.

## 9. Artefatti intermedi e riproducibilità

Pubblichiamo in formati aperti, con schema:

- il **registro di classificazione** per CIG, con tutti i passaggi;
- i **collegamenti CIG → atti**, con sha256 e testo estratto;
- la base di conoscenza;
- le istruzioni date ai modelli (versionate);
- le conversazioni di lavoro con gli agenti.

Vedi il [formato della classificazione](../formato-classificazione/).

## 10. Costo e tetto di computazione

I compiti automatici di Claude sul server passano da un tetto (`tools/llm/claude_tetto.py`). Ogni chiamata registra token e costo equivalente; oltre il tetto giornaliero o settimanale il lavoro si ferma e riparte da dov'era. Il tetto si tara confrontando il registro con il contatore del piano.

## 11. Cosa resta da decidere

- annotatori e campione per la revisione alla cieca; pagina pubblica per volontari;
- soglia di precisione per usare l'«alta» del modello nei numeri;
- esito della sperimentazione TabICL;
- per Cloud Toscana, se chiedere l'accesso agli atti all'offerta tecnica;
- invio delle raccomandazioni R16-R19 (dopo approvazione).

## Registro delle revisioni

| data | modifica |
|---|---|
| 2026-10-29 | criticità, strategia a più vie, capitalizzazione della conoscenza |
| 2026-10-29 | prima versione: giri 1-2 della via 6, confronto Haiku/Sonnet, confidenza verificata, cloud sovrano, Cloud Toscana, TabICL, tetto |
