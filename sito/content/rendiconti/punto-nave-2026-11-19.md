---
title: "Punto nave al 19 novembre 2026"
subtitle: "Dove siamo arrivati nella misura della spesa cloud della PA: cosa è certo, cosa è incerto, cosa manca, se è ripetibile, cosa viene dopo"
date: 2026-11-19
lastmod: 2026-11-19
datiAl: 2026-11-19
description: "Fotografia datata del progetto: obiettivo e disegno, numeri dell'imbuto dal 2024, livelli di raffinamento, dataset usati e loro limiti, mancanze con gravità, test di ripetibilità, prossimi passi e decisioni aperte."
---

**Versione 1.1 del 19/11/2026.** Questa è una **fotografia datata**: non si aggiorna, se ne scrive una nuova al prossimo punto nave. La versione sempre aggiornata della stessa materia è la [Mappa dell'imbuto](/progetto/mappa-imbuto/), generata da [`config/mappa-imbuto.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/mappa-imbuto.yaml). Legenda: **[V]** verificato da noi con lo strumento indicato; **[R]** riferito da terzi; **[S]** stima.

## 1. In breve

- **Obiettivo.** Quanto spende la PA italiana in servizi cloud e infrastrutture informatiche, divisa per giurisdizione del prodotto (Italia, UE, extra-UE). Il processo deve rifarsi ogni anno con gli stessi comandi.
- **Universo.** Tutti i contratti ANAC (CIG) dal 2020. Dal 2024 sono **3.734.840 CIG** [V].
- **Esclusi con certezza.** L'85,9 % dei contratti non è informatica [V]. Questa esclusione non ha ancora una misura di precisione (mancanza M5, [#77](https://github.com/mxmap-it/analisi-spesa-ict/issues/77)).
- **Spesa ICT** (strati S3-S6, dal 2024): **289.192 CIG**. Valgono 114,4 miliardi dichiarati, **56,06 miliardi al netto dei massimali di accordo quadro** [V]. È il valore dei contratti, non la spesa di un anno: il pagato ICT del 2024 è circa 5,1 miliardi [V, SIOPE + BDAP].
- **Cloud certo**, dal 2024 [V]:
  - **1,21 miliardi** in 4.556 CIG di cloud;
  - **0,66 miliardi** di infrastruttura in-house.

  Sugli inclusi certi la giurisdizione è extra-UE 47 %, Italia 39 %, UE 14 %, misurata su campioni a cieco.
- **Incerto**, dal 2024 [V]:
  - 16,37 miliardi nel residuo S6;
  - 5,37 miliardi di licenze e software con marchio noto, per cui resta da capire se sono cloud.

  Per la maggior parte di questi contratti l'atto di gara che direbbe il prodotto non è pubblicato in modo raggiungibile.
- **Cosa è cambiato negli ultimi due giorni** (decisioni di Fabio del 18 e 19/11): l'imbuto resta largo e sopra si lavora per **livelli di raffinamento**, sempre più costosi e ciascuno registrato. I livelli sono:
  - L2: regole sul testo;
  - B: dataset della Banca dati nazionale dei contratti pubblici;
  - L3: Claude Opus sul testo;
  - L4: Claude Opus con gli atti.

  Insieme hanno già tolto dalla misura cloud circa **0,77 miliardi** di contratti che cloud non sono (somma delle tabelle di L2, B1 e L3, ancora da deduplicare: § 3).

## 2. Il disegno e i dati

![Il disegno dell'imbuto con i numeri dal 2024](/img/mappa-imbuto/imbuto.svg)

![Relazioni fra i dataset dell'imbuto](/img/mappa-imbuto/relazioni.svg)

Il **CIG** è il centro: ogni informazione su un contratto si attacca al suo codice.
- **Cinque dataset BDNCP** si collegano solo per CIG: aggiudicazioni, quadro economico, avvio e fine, stati di avanzamento, indicatori PNRR.
- **Quattro dataset BDNCP fanno da ponte** verso le fonti esterne:
  - aggiudicatari e stazioni appaltanti, per codice fiscale;
  - CUP, verso i finanziamenti;
  - pubblicazioni, verso TED.

Dataset, chiavi, coperture e limiti sono descritti uno per uno nella [Mappa](/progetto/mappa-imbuto/#2-i-dati-e-come-si-collegano). I limiti più pesanti sono quattro:
- l'importo è un valore, non una spesa;
- l'oggetto del contratto è troppo breve per dire il prodotto;
- i campi ANAC sulle società in-house sono vuoti (R84);
- gli atti di gara mancano per il residuo.

## 3. I livelli di raffinamento a oggi

| livello | cosa ha fatto | effetto sulla misura cloud | precisione misurata |
|---|---|---|---|
| L2 regole | stampanti, consumabili, cablaggio | 6.980 CIG / 470 M€ fuori | 40 su 40 [V] |
| B1 quadro economico | contratti che sono lavori (≥ 80 %) | 1.281 CIG / 132 M€ fuori | 37 su 40 su campione nuovo, Wilson 80-97 % [V] |
| B2 in-house | aggiudicatario confrontato con l'Indice PA | in-house certo da 298,5 a 77,6 M€; 150,4 M€ di privati tornano da attribuire | 40 su 40 [V] |
| B3 durate | date effettive di inizio e fine | misura, non cambia il totale: la quota 2024 sugli stessi CIG scende da 5,84 a 4,07 mld | copertura 13 % |
| B4 PNRR | flag, indicatori, CUP | gli indicatori coincidono col flag; un terzo dei CIG della Misura 1.2 non ha il flag | — |
| L3 Opus sul testo | 3.540 CIG a segnale debole | 2.260 ICT non cloud e 308 non ICT escono (167 M€); 972 vanno a L4 | esce solo con certezza alta |
| L4 Opus con gli atti | arbitro e incerti di L3 | 5 disaccordi risolti (2 con quota cloud); 95 su 977 letti | fonte primaria per ogni esito |

**Cosa manca ancora per avere un numero solo:**
- Le tabelle dei livelli vanno unite in una sola tabella di spostamenti per CIG. Così un contratto tolto da due livelli conta una volta sola. È il prossimo passo (§ 6).
- Per questo gli 0,77 miliardi del § 1 sono una somma lorda: dopo la deduplica saranno di meno.

## 4. Che cosa manca e quanto pesa

![Mancanze dell'imbuto per peso e gravità](/img/mappa-imbuto/mancanze.svg)

Le mancanze sono 11, con un criterio di gravità fisso. Le quattro **alte** che pesano di più sono:
- **M1, atti non raggiungibili** per il residuo incerto (16,37 mld): raffinamento a livelli; l'accesso civico solo alla fine;
- **M4, importi che sono massimali** (14,4 mld ancora incerti): regole dei tetti e revisione;
- **M3, licenze con marchio noto** (5,37 mld): regole per prodotto e censimento degli EA;
- **M2, PSN** (4,03 mld): servizio comprato non noto.

Una quinta mancanza alta non è ancora misurata: **M9, il cloud di un hyperscaler dentro un servizio italiano**.

Tabella completa, con il perché, il come e il ticket: [Mappa, § 4](/progetto/mappa-imbuto/#4-che-cosa-manca-quanto-pesa-come-lo-risolviamo).

## 5. Test di ripetibilità

<!-- RIPETIBILITA -->
Il test è in corso: rifà da zero, in una cartella separata, i passi deterministici e confronta ogni uscita con quella pubblicata. I passi sono:
- l'imbuto (`ict.csv`);
- strati, tetti, revisione e CIG ripetuti;
- il livello B;
- il livello L2.

L'esito sarà riportato qui.

## 6. Prossimi passi, in ordine

1. **Una sola tabella di spostamenti** con tutti i livelli (L2, B1, B2, L3, L4) e il numero della misura cloud al netto di tutto, deduplicato per CIG ([#71](https://github.com/mxmap-it/analisi-spesa-ict/issues/71)).
2. **B1 versione 0.2:** proteggere anche locali informatici, locali tecnologici e area server, poi misurare su un campione nuovo ([#74](https://github.com/mxmap-it/analisi-spesa-ict/issues/74)).
3. **Finire L4** sui 977 CIG. Riparte da solo dopo il tetto di spesa giornaliero.
4. **Misurare la precisione di S1** ([#77](https://github.com/mxmap-it/analisi-spesa-ict/issues/77)) e **portare SmartCIG nell'imbuto** ([#76](https://github.com/mxmap-it/analisi-spesa-ict/issues/76)).
5. **Hosting dei SaaS italiani** su hyperscaler ([#70](https://github.com/mxmap-it/analisi-spesa-ict/issues/70)).

**Traguardo prima dell'accesso civico** (decisione di Fabio, 19/11/2026): le richieste di accesso civico massivo ([#58](https://github.com/mxmap-it/analisi-spesa-ict/issues/58)) si fanno **solo alla fine**. Prima si fa tutto ciò che è possibile con le fonti aperte, e se ne pubblica un **rendiconto del risultato parziale** ([#78](https://github.com/mxmap-it/analisi-spesa-ict/issues/78)) con:
- risultati intermedi documentati estensivamente;
- metodologia dettagliata, ripetibile e riproducibile;
- tutte le mancanze evidenziate;
- grafici, pubblicazioni e integrazioni;
- open data definitivo;
- il processo per aggiornarlo ogni anno.

Solo allora gli atti che restano mancanti (M1, M2) diventano la lista delle richieste.

**Decisioni che restano a Fabio:**
- **Richieste ad ANAC** ([#54](https://github.com/mxmap-it/analisi-spesa-ict/issues/54), raccomandazioni R22, R84 e altre). Nessuna è stata inviata.

## Registro delle revisioni

| data | versione | modifica |
|---|---|---|
| 2026-11-19 | 1.1 | decisione di Fabio: accesso civico massivo solo alla fine, dopo il rendiconto del risultato parziale (#78) |
| 2026-11-19 | 1.0 | prima fotografia: richiesta di Fabio del 19/11 («punto nave, documentiamo bene tutto, test di ripetibilità») |
