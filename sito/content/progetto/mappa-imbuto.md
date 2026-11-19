---
title: "Mappa dell'imbuto: dati, relazioni, limiti e mancanze"
date: 2026-11-19
lastmod: 2026-11-19
description: "Il punto di riferimento sempre aggiornato: quali dataset usa l'imbuto e come si collegano, il disegno dei livelli con i numeri, i limiti di ogni fonte, le mancanze con gravità e piano per risolverle, cosa è ripetibile."
weight: 17
---

<!-- PAGINA GENERATA da tools/pagina_mappa_imbuto.py da config/mappa-imbuto.yaml e dagli esiti: non modificarla a mano. -->

**Versione 0.1, aggiornata il 2026-11-19.** Questa pagina è il **punto di riferimento** del progetto: si rigenera a ogni avanzamento. Testi, dataset, relazioni e mancanze stanno in [`config/mappa-imbuto.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/mappa-imbuto.yaml); i numeri si leggono dagli esiti più recenti, con il file indicato sotto ogni figura. I dettagli stanno nel rendiconto [«Imbuto: dove siamo»](/rendiconti/imbuto-dove-siamo/) e nella pagina di metodo [Raffinamento dell'imbuto a livelli](/progetto/raffinamento-imbuto/).

**Obiettivo:** misurare quanto spende la PA italiana in servizi cloud e infrastrutture informatiche, per giurisdizione del prodotto (Italia, UE, extra-UE), con un processo che si rifà ogni anno. **Unità:** il contratto (CIG). **Due domande per ogni contratto:** è cloud? di quale giurisdizione?

## 1. Il disegno dell'imbuto

![Il disegno dell'imbuto con i numeri dal 2024](/img/mappa-imbuto/imbuto.svg)

<small>Numeri dal 2024. Fonti: `esiti/2026-11-18/imbuto/strati.json`, `esiti/2026-11-19/imbuto/bdncp/riepilogo.json`, `esiti/2026-11-18/imbuto/raffinamento-l3.json`, esiti L4 in `report/metodo/llm/raffinamento-l4/esiti/`. Gli importi sono **dichiarati** (valore dei contratti): il totale al netto dei massimali di accordo quadro è nel rendiconto, § 2.7.</small>

Come funziona:
- **L1, gli strati.** Ogni contratto passa per gli strati in ordine:
  - S0 padri di accordo quadro, contati negli attuativi;
  - S1 non ICT, escluso con certezza;
  - S2 sotto 500 €;
  - S3 convenzione o lotto noto;
  - S4 marchio nel testo;
  - S5 ICT non cloud;
  - S6 incerto.
- **Il principio:** prima si esclude ciò che è certamente fuori, poi si include ciò che è certamente dentro, e lo sforzo costoso va solo sull'incerto.
- **I livelli di raffinamento** stanno **sopra** gli strati e non li modificano. Ognuno scrive una tabella per CIG, con il motivo e la via che ha deciso.

| livello | mezzo | ingresso | uscita | strumento | ripetibile |
|---|---|---|---|---|---|
| **L1** Imbuto a regole | testo, CPV, lotti di convenzione, marchi | tutti i CIG ANAC dal 2020 | strati S0-S6 | `tools/analisi/imbuto.py, tools/verifiche/imbuto_strati.py` | sì, identico |
| **B** Segnali BDNCP | quadro economico, aggiudicatari + Indice PA, avvio/fine, indicatori PNRR | CIG ICT S3-S6 | lavori fuori dalla misura cloud; in-house ristretta; durate; PNRR | `tools/verifiche/imbuto_bdncp.py` | sì, identico |
| **L2** Regole sul testo | stampanti, consumabili, cablaggio, salvo testo cloud | residuo S6 dal 2024 | fuori dalla misura cloud | `tools/llm/raffinamento.py l2` | sì, identico |
| **L3** Lettura del testo con Claude Opus | solo dati ANAC, senza web | S6 entrato per «sw» o «connettività» | non ICT / ICT non cloud con certezza alta; il resto a L4 | `tools/llm/raffinamento.py prepara-l3, leggi-l3, esito` | esiti versionati (modello linguistico) |
| **L4** Atti di gara con Claude Opus | ricerca e archiviazione degli atti (sha256) | incerti di L3, disaccordi sull'asse cloud | cloud sì/no e prodotto, con fonte primaria | `tools/llm/giro_imbuto.sh (GIRO_DIR raffinamento-l4)` | esiti versionati (modello linguistico) |

## 2. I dati e come si collegano

![Relazioni fra i dataset dell'imbuto](/img/mappa-imbuto/relazioni.svg)

<small>Una freccia è un collegamento: la chiave (CIG, codice fiscale, CUP) e, dove misurata, la quota dei CIG ICT dal 2024 che il collegamento copre. Il CIG è il centro: tutto ciò che sappiamo di un contratto si attacca al suo codice.</small>

| dataset | chiave | cosa usiamo | a che cosa serve | stato |
|---|---|---|---|---|
| **CIG ANAC (annuali 2020-2025 e mensili)** | CIG | oggetto gara e lotto, CPV, importo del lotto, CF della stazione appaltante, CIG dell'accordo quadro, data, durata prevista, flag PNRR | Universo dell'imbuto: ogni contratto dal 2020 entra da qui. | usato |
| **SmartCIG (affidamenti semplificati)** | CIG | oggetto, importo, CF della stazione appaltante, fattispecie | Spesa sotto soglia (canoni, licenze, piccoli SaaS). Non ancora nell'imbuto. | **da usare** |
| **OCDS ANAC (73,8 GB)** | CIG (ocid) | fasi della gara, periodi, parti | Seconda via sul CIG; periodi e PNRR 1.2. | usato |
| **Aggiudicatari** | CIG → codice fiscale | CF, denominazione, ruolo nel raggruppamento | Chi vince: lente fornitore, canale diretto/rivenditore, in-house (B2). | usato |
| **Aggiudicazioni** | CIG | importo di aggiudicazione, data | Seconda via sull'importo: tetti contro spesa. | usato |
| **Quadro economico** | CIG | importo per natura (forniture, servizi, lavori) e per evento | B1: contratti che sono lavori; tetti sopra 50 M€. | usato |
| **Avvio e fine contratto** | CIG | stipula, inizio effettivo, termine, ultimazione | B3: durata effettiva, quota annua di spesa. | usato |
| **Stati di avanzamento (SAL)** | CIG | importo SAL, certificati di pagamento | Unica spesa eseguita in BDNCP: controvalidazione. | usato poco |
| **Indicatori PNRR/PNC** | CIG | quote di genere e giovani | B4: candidata terza via PNRR. | usato |
| **CUP** | CIG ↔ CUP | codice unico di progetto | Ponte verso i finanziamenti (PNRR) e le opere. | usato |
| **Pubblicazioni** | CIG | date GURI e GUUE | Aggancio a TED. | usato |
| **Stazioni appaltanti** | codice fiscale | denominazione, natura giuridica, flag in-house e partecipata | Anagrafica dei committenti; B2. | usato |
| **Indice PA (AgID)** | codice fiscale | ente, tipologia, URL istituzionale e trasparenza | Chi è pubblico (B2), abbinamento enti, URL delle sezioni Amministrazione trasparente. | usato |
| **Atti di gara: link PVL, MePA, sezioni Amministrazione trasparente** | CIG nel testo dell'atto | determine, capitolati, contratti (archiviati con sha256) | La prova del prodotto comprato: livelli L3-L4 dell'acquisizione e via 6. | usato |
| **TED (Gazzetta UE)** | numero di avviso, CIG nel testo | aggiudicatari, lotti | Seconda fonte degli aggiudicatari sopra soglia UE. | usato |
| **PA Digitale 2026 (finanziamenti PNRR)** | CUP | misura, ente, importo finanziato | Sottoinsieme prioritario: Misure 1.1 e 1.2 (catena v3 CUP → CIG). | usato |
| **SIOPE e BDAP (pagamenti)** | codice fiscale dell'ente / ministero | pagato per codice gestionale ICT | Riscontro con la spesa pagata (strato R, non si somma). | usato |
| **Dataset L. 190/2012 degli enti** | CIG | importo aggiudicato e liquidato per lotto | Unica spesa effettiva per CIG: campione di 200 enti. | a campione |
| **Tabelle curate (lotti, marchi, iniziative, perimetro CPV)** | lotto di AQ, marchio, CPV | provider, giurisdizione, fonte di ogni riga | Regole dell'imbuto (S3, S4) e dei livelli. | usato |
| **Imbuto (ict.csv) e tabelle dei livelli** | CIG | strato, sottoclasse, provider, giurisdizione, esito di ogni livello | Risultato: una riga per CIG con chi ha deciso cosa. | usato |

## 3. I limiti di ogni fonte

Ogni limite è un motivo per cui un numero potrebbe essere sbagliato. Dove c'è un codice (P, R) il problema è documentato con evidenza in [`richieste-e-raccomandazioni.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/metodo/richieste-e-raccomandazioni.yaml) o nelle [schede dei problemi](/problemi/).

- **CIG ANAC (annuali 2020-2025 e mensili)**
  - L'importo del lotto è valore del contratto, non spesa; negli attuativi è spesso il massimale dell'accordo quadro copiato (R22).
  - L'oggetto è testo libero breve: il prodotto comprato spesso non c'è.
  - Delta mensili rimossi e righe non conformi (P08, P16): li conserva il mirror.
- **SmartCIG (affidamenti semplificati)**
  - Mesi mancanti alla fonte (P09).
- **OCDS ANAC (73,8 GB)**
  - Pesante; usato solo a campione o per sottoinsiemi.
- **Aggiudicatari**
  - Manca per una parte dei CIG (177 CIG in-house su 816 dal 2024).
- **Quadro economico**
  - Copre il 62,4 % dei CIG ICT dal 2024.
  - A volte servizi compilati come lavori (siti web, pagoPA).
- **Avvio e fine contratto**
  - Copre il 13,4 % dei CIG ICT dal 2020: solo misura, non sostituisce la stima.
- **Stati di avanzamento (SAL)**
  - Copre il 2,2 % dei CIG ICT; importi progressivi da non sommare due volte.
- **Indicatori PNRR/PNC**
  - Coincide con il flag del CIG: non è una via indipendente.
- **CUP**
  - Il CUP c'è anche per investimenti non PNRR: da solo non dice PNRR.
- **Pubblicazioni**
  - Manca per il 19 % dei CIG ICT.
- **Stazioni appaltanti**
  - flag_inHouse e flag_partecipata «false» su tutte le 48.040 righe (R84).
- **Indice PA (AgID)**
  - URL della sezione trasparenza spesso errato (R82).
- **Atti di gara: link PVL, MePA, sezioni Amministrazione trasparente**
  - Per il residuo S6 solo 535 CIG su 59.406 hanno un atto che cita il CIG.
- **TED (Gazzetta UE)**
  - Solo gare sopra soglia UE.
- **PA Digitale 2026 (finanziamenti PNRR)**
  - Il 32 % dei CIG della Misura 1.2 non ha il flag PNRR nel CIG.
- **SIOPE e BDAP (pagamenti)**
  - Nessun CIG nei dati aperti: abbinamento solo per ente e anno (R83).
- **Dataset L. 190/2012 degli enti**
  - XML con lotti per il 48,5 % degli enti del campione; dati da ripulire.
- **Tabelle curate (lotti, marchi, iniziative, perimetro CPV)**
  - Vanno mantenute a mano: ogni riga ha la fonte.

## 4. Che cosa manca, quanto pesa, come lo risolviamo

![Mancanze dell'imbuto per peso e gravità](/img/mappa-imbuto/mancanze.svg)

<small>I pesi **non si sommano**: una mancanza può stare dentro un'altra. Per esempio il PSN (M2) è una parte del residuo S6 (M1). Gli importi da verificare (M4) toccano contratti di tutti gli strati.</small>

**Gravità**, con un criterio fisso per poterla confrontare nel tempo:
- **alta:** può spostare la quota cloud o la giurisdizione di oltre 1 miliardo, oppure riguarda oltre il 10 % della spesa ICT senza misura;
- **media:** pesa fra 0,1 e 1 miliardo, oppure tocca un passo intermedio senza cambiare il risultato finale;
- **bassa:** pesa sotto 0,1 miliardi, oppure è un problema di qualità del dato già aggirato.

| | mancanza | peso | gravità | perché conta | come la risolviamo | ticket | stato |
|---|---|---|---|---|---|---|---|
| M1 | **Atti non raggiungibili per il residuo incerto** | S6 dal 2024: 59.406 CIG, 16,37 mld dichiarati; con un atto che cita il CIG solo 535 CIG / 304,7 M€ | alta | Senza l'atto non si sa quale prodotto si compra: il contratto resta incerto su entrambi gli assi. | Raffinamento a livelli (L2-L4) per togliere ciò che non è cloud; per il resto accesso civico massivo. | [#57](https://github.com/mxmap-it/analisi-spesa-ict/issues/57), [#58](https://github.com/mxmap-it/analisi-spesa-ict/issues/58), [#71](https://github.com/mxmap-it/analisi-spesa-ict/issues/71) | in corso |
| M4 | **Importi che sono massimali, non spesa** | S3-S6 dal 2024: 56,06 mld al netto dei tetti; ancora incerti 14,4 mld in 80 CIG (misura della 0.3.1) | alta | Gli attuativi riportano spesso il massimale dell'accordo quadro: contarli gonfia la spesa. | Regole dei tetti v2 misurate su campione, quadro economico e aggiudicazioni come seconda via, revisione sugli atti; raccomandazione R22. | [#66](https://github.com/mxmap-it/analisi-spesa-ict/issues/66) | mitigata |
| M3 | **Licenze e software con marchio noto ma cloud da accertare (Microsoft EA, Oracle)** | 3.889 CIG, 5,37 mld dal 2024 | alta | Lo stesso contratto Microsoft o Oracle può essere licenza on premises o abbonamento cloud. | Regole per prodotto (L1-L4 delle licenze), censimento dei prodotti negli EA, transato per famiglia da Consip (R23). | [#66](https://github.com/mxmap-it/analisi-spesa-ict/issues/66), [#40](https://github.com/mxmap-it/analisi-spesa-ict/issues/40) | in corso |
| M2 | **PSN: servizio comprato non noto** | 847 CIG, 4,03 mld dal 2024 | alta | Il PSN eroga sia cloud sovrano sia servizi su hyperscaler: senza il piano dei fabbisogni la giurisdizione non si attribuisce. | Progetti dei piani dei fabbisogni sui siti degli enti; accesso civico a PSN S.p.A. e DTD; bilancio PSN come controllo aggregato. | [#58](https://github.com/mxmap-it/analisi-spesa-ict/issues/58), [#45](https://github.com/mxmap-it/analisi-spesa-ict/issues/45) | decisione di Fabio |
| M9 | **Cloud di un hyperscaler dentro il servizio di un fornitore italiano** | non misurato | alta | Un SaaS italiano che gira su AWS o Azure è giurisdizione extra-UE per l'infrastruttura, ma il contratto non lo dice. | Tabella dei SaaS e del loro hosting (config/saas_host.yaml) da documentazione pubblica dei fornitori; via 6 sugli atti. | [#70](https://github.com/mxmap-it/analisi-spesa-ict/issues/70) | aperta |
| M7 | **Spesa in-house senza CIG (Regione Lombardia → ARIA, MEF → Sogei)** | ARIA circa 189 M€ l'anno [R]; MEF circa 0,3 mld l'anno [stima] | media | Gli affidamenti alle società in-house spesso non hanno CIG: la spesa c'è nei pagamenti ma non nei contratti. | Strato di riscontro R con SIOPE e BDAP per ente; bilanci delle in-house; raccomandazione R83. | [#67](https://github.com/mxmap-it/analisi-spesa-ict/issues/67), [#52](https://github.com/mxmap-it/analisi-spesa-ict/issues/52) | in corso |
| M5 | **Precisione dell'esclusione non ICT (S1) non misurata** | 3,21 milioni di CIG, l'85,9 % dell'universo dal 2024 | media | Se l'esclusione sbaglia anche lo 0,1 %, qualche migliaio di contratti ICT sparisce senza traccia. | Campione casuale di circa 400 CIG di S1 annotato da volontari: con 0 errori il limite superiore è circa 1 %. | [#77](https://github.com/mxmap-it/analisi-spesa-ict/issues/77), [#66](https://github.com/mxmap-it/analisi-spesa-ict/issues/66) | aperta |
| M6 | **SmartCIG fuori dall'imbuto** | non misurato: affidamenti sotto soglia (canoni, licenze, piccoli SaaS) | media | Molta spesa cloud corrente dei piccoli enti passa per affidamenti semplificati. | Portare SmartCIG nell'imbuto con le stesse regole; prima un profilo per fattispecie. | [#76](https://github.com/mxmap-it/analisi-spesa-ict/issues/76) | aperta |
| M8 | **Valore dei contratti, non spesa annua** | il valore dei CIG è circa 3,5 volte il pagato; date effettive solo per il 13 % dei CIG | media | La misura finale è la spesa per anno: va ripartita sulla durata e confrontata col pagato. | Quota annua dalla durata (B3 dove c'è la data effettiva), SIOPE/BDAP per il pagato, liquidato L. 190 a campione. | [#74](https://github.com/mxmap-it/analisi-spesa-ict/issues/74), [#12](https://github.com/mxmap-it/analisi-spesa-ict/issues/12) | in corso |
| M10 | **Giurisdizione degli inclusi certi misurata solo a campione** | cloud certo 1,21 mld + in-house 0,66 mld dal 2024 | bassa | La precisione in euro pesata è circa 99 % sui campioni a cieco, ma il campione definitivo non è ancora fatto. | Settimo campione a cieco, una sola volta, prima del rendiconto finale. | [#40](https://github.com/mxmap-it/analisi-spesa-ict/issues/40), [#72](https://github.com/mxmap-it/analisi-spesa-ict/issues/72) | aperta |
| M11 | **Qualità dei dati ANAC: campi vuoti o compilati male** | flag in-house vuoto su 48.040 righe; PNRR senza flag sul 32 % dei CIG 1.2; quadro economico a volte sbagliato | bassa | Ogni campo vuoto obbliga a una via indiretta (Indice PA, catena CUP, lettura del testo). | Vie indirette documentate; raccomandazioni ad ANAC (R22, R84) con metrica, nessuna inviata senza Fabio. | [#74](https://github.com/mxmap-it/analisi-spesa-ict/issues/74), [#54](https://github.com/mxmap-it/analisi-spesa-ict/issues/54) | mitigata |

## 5. Ripetibilità

- **Deterministici: L1, B, L2.** Con gli stessi file d'ingresso (sha256 nel manifest dell'archivio e nei riepiloghi) danno lo stesso risultato, byte per byte.
- **Non deterministici: L3 e L4.** Usano un modello linguistico, che riletto da capo dà risposte vicine ma non identiche. Per questo i loro esiti sono versionati in git e si **rileggono**, non si rigenerano; lo scarto si misura sui campioni a cieco.
- **I comandi in ordine** sono nella pagina [Raffinamento dell'imbuto a livelli](/progetto/raffinamento-imbuto/#rifarlo-ogni-anno) e in [RIPRODURRE.md](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/RIPRODURRE.md).

Il test di ripetibilità di questa versione è in corso: l'esito comparirà qui alla prossima rigenerazione.

## 6. Come si aggiorna questa pagina

1. **Quando cambia qualcosa, si aggiorna il file dati.** È [`config/mappa-imbuto.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/mappa-imbuto.yaml). Per esempio:
   - un dataset nuovo, con la sua chiave e i suoi limiti;
   - una relazione nuova;
   - una mancanza che cambia stato;
   - un livello nuovo.

   Ogni numero scritto lì deve essere già pubblicato in un rendiconto, con la sua fonte.
2. **Si rigenera:** `python3 tools/pagina_mappa_imbuto.py`. I numeri dell'imbuto si rileggono dagli esiti più recenti.
3. **Si costruisce il sito e si pubblica:** `hugo --source sito --minify --cleanDestinationDir`, poi commit di sorgente e `docs/`, poi push.
4. **Si annota la modifica** nel registro qui sotto, nel YAML, alla voce `registro`.

## Registro delle revisioni

| data | versione | modifica |
|---|---|---|
| 2026-11-19 | 0.1 | Prima versione (punto nave chiesto da Fabio il 19/11): dataset e relazioni, disegno con L1-L4 e livello B, limiti, 11 mancanze con gravità e piano, ripetibilità. |
