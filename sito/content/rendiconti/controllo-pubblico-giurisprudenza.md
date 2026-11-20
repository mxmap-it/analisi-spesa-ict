---
title: "Controllo pubblico delle società: controllo in concreto e catene di quotate"
date: 2026-11-20
lastmod: 2026-11-20T22:00:00Z
description: "Ricerca sulla giurisprudenza del Consiglio di Stato, della Corte dei conti e sugli atti ANAC e MEF: quando una società è a controllo pubblico, se serve il controllo in concreto, come contano le quote che passano per società quotate; applicazione al Polo Strategico Nazionale. Bozza tecnica, non parere professionale."
---

**Versione 0.1 del 2026-11-20** · ticket [#82](https://github.com/mxmap-it/analisi-spesa-ict/issues/82) · **proposta per Fabio**: bozza tecnica di ricerca, non è un parere legale professionale. Testi delle pronunce archiviati con sha256 ([INDICE.tsv](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/metodo/prove-controllo-pubblico/INDICE.tsv)). Usata per la classe «controllata sostanzialmente» del [dataset delle società ICT pubbliche](/rendiconti/societa-ict-pubbliche/).

Data: 20/11/2026 · Redatto da agente (Claude) per il progetto analisi-spesa-ict · Stato: **bozza tecnica di ricerca, non è un parere legale professionale; da validare (proposta per Fabio)**. Le correzioni del § 9 riguardano una prima bozza interna, superata da questo testo.

Legenda dello stato di lettura: **[I]** testo integrale letto da fonte primaria (archiviato nel mirror con sha256: elenco in `report/metodo/prove-controllo-pubblico/INDICE.tsv`); **[IC]** testo integrale letto da copia non ufficiale; **[E]** letto in estratto (citato testualmente in un'altra pronuncia o atto letto integralmente); **[R]** riferito da commento (indicato); **[N]** non trovato.

---

## 1. Sommario

1. **Controllo in concreto.** Sul controllo congiunto di più amministrazioni non c'è un orientamento unico. Si contrappongono una tesi **formale/astratta** (basta la maggioranza dei voti in mano pubblica ex art. 2359 n. 1 c.c.: Corte dei conti SS.RR. controllo 11/2019 [R], Cons. Stato IV 5289/2025 [I]), una tesi **presuntiva** (la maggioranza è indice, salvo prova contraria: ANAC 859/2019 [IC]), una tesi **sostanziale intermedia** (serve un coordinamento effettivo, anche tacito o per comportamenti concludenti: orientamento MEF 15/2/2018 [IC], Cons. Stato V 2543/2023 [I], VI 3880/2023 [I], VI 436/2026 [I]) e una tesi **formale rigorosa** (servono patti o clausole scritte: Corte dei conti SS.RR. giur. 16/2019 e 25/2019 [E/R]). L'orientamento oggi più recente e motivato del Consiglio di Stato è quello **sostanziale** di VI 436/2026: il dato numerico basta nel controllo «solitario», non in quello «congiunto», dove serve la prova (anche indiziaria) di una concertazione. La IV sezione (5289/2025) resta però in contrasto e **436/2026 non la cita**. Nessuna rimessione all'Adunanza plenaria e nessuna norma di interpretazione trovate; ci sono solo proposte (ANAC, atto di segnalazione 3/2020; CNDCEC, dicembre 2025 [R]).
2. **Controllo tramite quotate.** Il TUSP vigente (art. 1 c. 5, testo Normattiva) esclude le quotate «nonché le società da esse **controllate**». La formula «partecipate, salvo che … non per il tramite di società quotate, controllate o partecipate da amministrazioni pubbliche» sopravvive **solo** nell'art. 2-bis c. 2 lett. b) d.lgs. 33/2013. La bozza `parere-psn.md` cita per il TUSP il testo superato: va corretta. **Nessuna pronuncia** decide se i voti che passano per una quotata contino per qualificare «a controllo pubblico» una società a valle. Gli atti trovati divergono: il MEF ammette in generale il controllo indiretto (art. 2359 c. 2); la relazione illustrativa del TUSP, citata dal MEF, tratta come «meramente partecipate» le società in cui partecipano quotate; il parere del Consiglio di Stato 968/2016 proponeva di contare solo il controllo diretto; ANAC (2020) considera **CDP una «società quotata»** per via delle obbligazioni, e ANAS esclusa dal d.lgs. 33/2013 perché controllata da FS, emittente di obbligazioni quotate.
3. **PSN.** Con il computo «trasparente» (art. 2359 c. 2 c.c. senza filtro) tutte le catene portano al MEF. Ne risulta un controllo **solitario** indiretto del MEF: 55 % prima di settembre 2026 (se si ammette il controllo di fatto su Leonardo) e **75 % senza Leonardo, 100 % con Leonardo** dopo il passaggio di TIM sotto Poste (~85,8 %). Con il filtro delle quotate resta solo Sogei (10 %), perché anche CDP Equity passa per CDP «quotata»: PSN è **partecipata, non controllata**. Per la trasparenza (art. 2-bis) il testo letterale favorisce il filtro: PSN sta nel c. 3, come lei stessa dichiara. Per il TUSP la questione è aperta, e dal 2026 l'argomento «controllata sostanzialmente» si rafforza molto.

## 2. Quadro normativo (testi verificati)

| Norma | Testo rilevante | Stato |
|---|---|---|
| TUSP art. 2 c. 1 lett. b) | «“controllo”: la situazione descritta nell'articolo 2359 del codice civile. Il controllo può sussistere anche quando, in applicazione di norme di legge o statutarie o di patti parasociali, per le decisioni finanziarie e gestionali strategiche relative all'attività sociale è richiesto il consenso unanime di tutte le parti che condividono il controllo» | [I] Normattiva, vigente al 20/11/2026 |
| TUSP art. 2 c. 1 lett. m) | «società in cui una o più amministrazioni pubbliche esercitano poteri di controllo ai sensi della lettera b)» | [I] |
| TUSP art. 2 c. 1 lett. n) | società a partecipazione pubblica = «le società a controllo pubblico, nonché le altre società partecipate direttamente da amministrazioni pubbliche o da società a controllo pubblico» | [I] |
| TUSP art. 2 c. 1 lett. p) | quotate = «le società a partecipazione pubblica che emettono azioni quotate in mercati regolamentati; le società che hanno emesso, alla data del 31 dicembre 2015, strumenti finanziari, diversi dalle azioni, quotati in mercati regolamentati» (termine portato al 31/12/2021 per il comparto energetico: art. 52 c. 1-bis d.l. 50/2022) | [I] |
| **TUSP art. 1 c. 5 (vigente)** | «Le disposizioni del presente decreto si applicano, solo se espressamente previsto, alle società quotate, come definite dall'articolo 2, comma 1, lettera p), nonché alle società da esse **((controllate))**» — la doppia parentesi di Normattiva segnala una modifica. Testo precedente (d.lgs. 100/2017): «…partecipate, salvo che queste ultime siano, non per il tramite di società quotate, controllate o partecipate da amministrazioni pubbliche». Fonte della modifica: L. 145/2018, art. 1 c. 721 | testo vigente [I]; fonte modifica [R] (self-entilocali, via segretaricomunalivighenzi.it 28/2/2019; testo del c. 721 non aperto) |
| TUSP art. 26 c. 3 | «Le pubbliche amministrazioni possono comunque mantenere le partecipazioni in società quotate detenute al 31 dicembre 2015» | [I] |
| TUSP art. 26 c. 5-bis | Per le emittenti di strumenti diversi dalle azioni lo status resta «in virtù della proroga dello strumento finanziario o di successive emissioni effettuate in sostanziale continuità» | [I] |
| d.lgs. 33/2013 art. 2-bis c. 2 lett. b) | società in controllo pubblico (TUSP lett. m) «ad esclusione delle società quotate … nonché delle società da esse partecipate, salvo che queste ultime siano, non per il tramite di società quotate, controllate o partecipate da amministrazioni pubbliche» | [V] in `parere-psn.md` (Normattiva); testo identico riportato da ANAC, atto di segnalazione 3/2020 [I] |
| d.lgs. 33/2013 art. 2-bis c. 3 | società a partecipazione pubblica: trasparenza «limitatamente ai dati e ai documenti inerenti all'attività di pubblico interesse» | [E] (Cons. Stato 2543/2023) |
| c.c. art. 2359 | n. 1 maggioranza dei voti; n. 2 voti sufficienti per l'influenza dominante; n. 3 vincoli contrattuali; c. 2: «si computano anche i voti spettanti a società controllate» | [E] (Cons. Stato 5289/2025, 436/2026) |

**Difformità testuale.** Dal 2019 (L. 145/2018) il TUSP esclude solo le **controllate** dalle quotate, mentre il d.lgs. 33/2013 esclude anche le **partecipate**, salvo che siano controllate o partecipate da PA «non per il tramite di società quotate». Le due norme rinviano alla stessa definizione di quotata ma hanno perimetri diversi.

## 3. Tabella riassuntiva delle pronunce e degli atti

| # | Pronuncia / atto | Estremi | Tema | Criterio | Stato di lettura |
|---|---|---|---|---|---|
| P1 | Cons. Stato, Comm. speciale, parere sullo schema di TUSP | n. 968/2016, adunanza 16/3/2016, spedito 21/4/2016 (affare 438/2016) | quotate; controllo congiunto | — (consultivo); propone di limitare l'esclusione delle partecipate dalle quotate ai casi di controllo **diretto** | [I] |
| P2 | Cons. Stato, Comm. speciale, parere su LG ANAC | n. 1257/2017, adunanza 20/4/2017, data 29/5/2017 (affare 650/2017) | quotate e trasparenza | — ; esonero quotate giustificato dal regime di mercato; coinvolgere CONSOB | [I] |
| P3 | ANAC, Linee guida società e enti controllati/partecipati | delibera n. 1134 dell'8/11/2017 | controllo congiunto; quotate | prudente: controllo congiunto ex 2359 incluso; **parte sulle quotate espunta** | [I] (relazione AIR + testo, PDF anticorruzione.it) |
| P4 | MEF-DT, Struttura di monitoraggio TUSP, orientamento | 15/2/2018 | nozione di controllo pubblico | **sostanziale** (comportamenti concludenti, PA «soggetto unitario»; controllo indiretto ammesso) | [IC] copia dirittobancario.it |
| P5 | MEF-DT, Struttura di monitoraggio, orientamento | 22/6/2018 | nozione di mercato regolamentato (quotate) | definitorio | [IC] |
| P6 | Linee guida MEF-DT e Corte dei conti, revisione periodica | 2018 (rif. piani al 31/12/2019 [S]) | partecipazioni indirette; quotate; tipologie di controllo | sostanziale (controllo congiunto «anche tramite comportamenti concludenti») | [IC] |
| P7 | Cons. Stato, sez. V | 23/1/2019 n. 578 | partecipazioni «pulviscolari» (Asco Holding) | **non definitorio**: riguarda il mantenimento delle partecipazioni (artt. 4, 20, 24 TUSP); coordinamento di fatto «non istituzionalizzato» insufficiente | [I] |
| P8 | Corte dei conti, SS.RR. in sede di controllo | delib. n. 11/SSRRCO/QMIG/2019 (adunanza 4/4/2019; citata come «20 giugno 2019» da Cons. Stato 2543/2023, data di deposito [R]) | nozione di controllo pubblico | **formale/astratto** (maggioranza dei voti di una o più PA) | [R] (ANAC 859; Ardita 2026; commenti) — testo non raggiunto |
| P9 | Corte dei conti, SS.RR. in sede giurisdizionale in speciale composizione | sent. 22/5/2019 n. 16 | controllo congiunto | **formale rigoroso** (coordinamento formalizzato; no comportamenti concludenti) | [E] (citata in Cons. Stato 2543/2023 e 436/2026) + [R] |
| P10 | idem | sent. 29/7/2019 n. 25 | idem | idem | [R] (Ardita 2026, nota 18; ANAC 859) |
| P11 | ANAC | delibera n. 859 del 25/9/2019 | controllo congiunto | **presuntivo** (maggioranza pubblica «indice presuntivo», onere della prova sulla società) | [IC] testo riportato su segretaricomunalivighenzi.it |
| P12 | ANAC, atto di segnalazione n. 3 | 1/7/2020, delibera n. 541 | quotate e trasparenza; controllo congiunto | chiede una norma; CDP e ANAS citate come casi | [I] |
| P13 | Cons. Stato, sez. III | 3/3/2020 n. 1564 | controllo congiunto | formale (richiamata da 2543/2023) | [E] (solo citazione) |
| P14 | Cons. Stato, sez. VI | 11/4/2022 n. 2655 (Rai) | quotate e accesso civico | esclusione delle quotate «evidente»; questione di costituzionalità manifestamente infondata | [I] |
| P15 | Cons. Stato, sez. VI | 12/9/2022 n. 7896 (Rai) | idem | conferma P14 | [I] |
| P16 | Cons. Stato, sez. VII | 25/1/2023 n. 860 (ITA Airways) | controllo solitario MEF 100 % | formale (2359 n. 1) | [R] (eius.it) |
| P17 | Cons. Stato, sez. V | 10/3/2023 n. 2543 | controllo congiunto (accesso civico, Udine e Gorizia Fiere) | **sostanziale intermedio** (atti/accordi «o quanto meno un comportamento concludente») | [I] |
| P18 | Cons. Stato, sez. VI | 18/4/2023 n. 3880 (AGCM c. Comune di Rimini e altri; Rimini Congressi / IEG) | controllo congiunto; **quotate** (art. 1 c. 5) | **sostanziale**, con apertura alla tesi della PA «unitariamente intesa»; art. 1 c. 5 non tocca gli obblighi delle PA | [I] |
| P19 | Cons. Stato, sez. IV | 17/6/2025 n. 5289 (S.A.Pro.Di.R., Rieti) | controllo «frazionato» | **formale/astratto** («necessario, ed è anche sufficiente» la maggioranza dei voti) | [I] |
| P20 | Cons. Stato, sez. VI | 20/1/2026 n. 436 (Padova Hall c. MEF) | controllo congiunto | **sostanziale** (concertazione anche tacita, prova indiziaria) | [I] |
| P21 | Corte dei conti, sez. reg. controllo Lombardia | 16/3/2026 n. 84 | controllo congiunto | sostanziale/estensivo | [R] (Ardita 2026, nota 37) |
| P22 | Corte dei conti, sez. reg. controllo Emilia-Romagna | delib. n. 6 e n. 7 (anno non indicato dal commento) | controllo congiunto | «dissonanti» | [R] (Ardita 2026, nota 23) |
| P23 | Cass. SU | ord. 14/7/2026 n. 23220 | giurisdizione contabile sulle partecipate | non sul controllo pubblico | [R] (dirittobancario.it, snippet) |

Pronunce cercate ma **non trovate** su: controllo di fatto del MEF su Leonardo; società a valle di quotate pubbliche (Poste/TIM, CDP Equity); PSN.

## 4. Schede

### P1 — Cons. Stato, Commissione speciale, parere n. 968/2016 (schema di TUSP) [I]
- **Contesto**: parere sullo schema del decreto. Nello schema la lettera o) definiva quotate anche «le società partecipate dalle une o dalle altre, salvo che le stesse siano anche controllate o partecipate da amministrazioni pubbliche».
- **Massima utile**: sul comma 5 dell'art. 1 il parere osserva che «per le società quotate in mercati regolamentati opera interamente un regime di mercato». Sulla definizione suggerisce di limitare l'esclusione «ai soli casi di controllo diretto e non anche indiretto da parte di amministrazioni pubbliche», con la formula «salvo che le stesse siano direttamente controllate o partecipate da amministrazioni pubbliche».
- **Rilievo**: è il solo testo autorevole trovato che affronti il **conteggio del controllo tramite quotate**. Propone di non contare il controllo indiretto. Il legislatore ha poi scelto un'altra formula («non per il tramite di società quotate», d.lgs. 100/2017), che porta allo stesso risultato. Dal 2019 il TUSP l'ha abbandonata (solo «controllate»); il d.lgs. 33/2013 la conserva.
- Sul controllo congiunto il parere nota che la nozione è recepita «in termini non molto chiari».

### P2 — Cons. Stato, Comm. speciale, parere n. 1257/2017 (LG ANAC) [I]
- Critica la scelta dello schema ANAC di collocare le quotate nel terzo ambito (c. 3). Secondo il parere, la scelta è coerente con la lettera ma meno con la ratio dell'esonero: le quotate «sono sottoposte ad un sistema di obblighi, di controlli e di sanzioni autonomo». Suggerisce di coinvolgere la CONSOB.
- Ricorda che la determinazione ANAC 8/2015 aveva sospeso le linee guida «per le società con azioni quotate e per le società con strumenti finanziari quotati in mercati regolamentati **e per le loro controllate**».

### P3 — ANAC, delibera n. 1134/2017 [I]
- La relazione AIR riferisce che la parte sulle quotate è stata **espunta** per «un ulteriore approfondimento da svolgersi con il Mef e la CONSOB». Su proposta del MEF il § 2.1 si limita a precisare che fra le società a controllo pubblico rientrano quelle in cui il controllo ex art. 2359 c.c. «è esercitato da una pluralità di amministrazioni congiuntamente».
- **Rilievo per PSN**: PSN richiama la 1134 per collocarsi nel c. 3 (MOG 231, nota 3). Le LG però non trattano le società a valle delle quotate.

### P4 — MEF-DT, orientamento 15/2/2018 [IC]
- **Massima**: rientrano nel controllo pubblico anche le ipotesi in cui l'art. 2359 c.c. si riferisce a più PA «le quali esercitano tale controllo congiuntamente e mediante comportamenti concludenti, pure a prescindere dall'esistenza di un coordinamento formalizzato». La PA è intesa «come soggetto unitario».
- **Punto decisivo per le catene** (nota 1): «rientra nella nozione di controllo … anche il controllo indiretto e, cioè, quello esercitato tramite una società controllata o soggetto diverso». **Nessuna eccezione per le quotate.**
- Criterio: sostanziale. Citato da Cons. Stato 2543/2023 e 3880/2023, e dalla 436/2026 attraverso l'appellante.

### P5 — MEF-DT, orientamento 22/6/2018 (mercato regolamentato) [IC]
- «Mercato regolamentato» ai sensi del TUF: ne restano fuori i sistemi multilaterali (ExtraMot, AIM).
- **Passaggio rilevante**: riporta la relazione illustrativa al TUSP, secondo cui «le società meramente partecipate da amministrazioni pubbliche, in cui le società quotate abbiano una partecipazione (di controllo o meno), saranno soggette solo alle poche disposizioni del testo unico relative alle società meramente partecipate». La relazione si riferisce al testo originario del 2016.
- Ratio dell'esenzione: «evitare distorsioni del mercato di negoziazione dei titoli già quotati».

### P6 — Linee guida MEF-DT e Corte dei conti sulla revisione periodica [IC]
- Società «partecipata indirettamente» = partecipazione detenuta «per il tramite di società o altri organismi soggetti al controllo» di una o più PA.
- Controllo congiunto esemplificato: una pluralità di soci «dispone della maggioranza assoluta dei voti … ed esercita il controllo, anche tramite comportamenti concludenti».
- Quotate (§ 4.3): «se le società partecipate dalla società “tramite” quotata sono controllate o partecipate da Amministrazioni pubbliche, a tali società si applicano comunque le disposizioni del TUSP» (formulazione legata al testo 2017). Una società emittente di strumenti diversi dalle azioni «cesserà di essere considerata “quotata” dal momento della scadenza dei predetti strumenti» (ma vedi art. 26 c. 5-bis su proroghe e nuove emissioni).

### P7 — Cons. Stato, sez. V, 23/1/2019 n. 578 [I]
- **Fatti**: Comuni soci di Asco Holding (partecipazioni ≤ 2,74 % ciascuno), contro il socio privato Plavisgas. Il caso riguarda le delibere comunali sul mantenimento delle partecipazioni e sulla fusione con Asco TLC. Ascopiave, controllata della holding, è quotata.
- **Massima**: le partecipazioni «pulviscolari» senza strumenti di coordinamento non consentono di incidere sulle decisioni strategiche. Si rende «nei fatti necessario … la stipulazione di adeguati patti parasociali ovvero anche la previsione … di un organo speciale». Il coordinamento di fatto (delibere identiche) è «non istituzionalizzato».
- **Correzione importante**: la sentenza **non definisce** la «società a controllo pubblico» ai sensi della lett. m). Decide la legittimità del mantenimento delle partecipazioni (artt. 4, 20, 24). Ne viene usata in seguito come precedente sul controllo (2543/2023, 436/2026). La stessa appellante nel caso 436/2026 la definisce pronuncia sulla «differenza tra “società a controllo pubblico” e “società a capitale prevalentemente pubblico”».
- Criterio: formale-funzionale (patti o organo statutario).

### P8 — Corte dei conti, SS.RR. controllo, delib. 11/SSRRCO/QMIG/2019 [R]
- Secondo ANAC 859 [IC] e Ardita 2026: sono a controllo pubblico le società in cui «una o più amministrazioni dispongono della maggioranza dei voti esercitabili in assemblea ordinaria». Il controllo può essere escluso solo provando l'influenza dominante di soci privati per patti parasociali o clausole statutarie o contrattuali.
- Per Donativi (riferito da Ardita, nota 17) è una presunzione «assoluta».
- **Date**: Ardita indica «delibera 4 aprile 2019, n. 11»; Cons. Stato 2543/2023 la cita come «20 giugno 2019, n. 11» (verosimilmente adunanza e deposito; da verificare sul testo).
- Testo integrale **non raggiunto**: `banchedati.corteconti.it` ha robots.txt «Disallow: /» per tutti gli agenti; non l'abbiamo interrogata. Il link nella bozza era in 404.

### P9-P10 — Corte dei conti, SS.RR. giurisdizionali in speciale composizione, n. 16 del 22/5/2019 e n. 25 del 29/7/2019 [E/R]
- Citate testualmente da Cons. Stato 2543/2023 e 436/2026 come «Corte dei Conti, Sezioni riunite, 22 maggio 2019, n. 16» [E]. Secondo 436/2026 la n. 16 esclude il ricorso a «una presunzione di controllo derivante dalla partecipazione maggioritaria».
- Secondo Ardita [R]: gli accordi fra PA devono «risultare da atto scritto». Per ANAC 859 [IC]: «il socio privato non può concorrere in modo determinante alla governance della società».
- La n. 16 ha annullato deliberazioni di una sezione regionale sul numero dei componenti del CdA di una partecipata [R] (snippet). Testi integrali non raggiunti, per lo stesso motivo indicato in P8.
- Criterio: formale rigoroso. Commenti del 2019 riferiscono un **contrasto interno alla Corte dei conti** fra controllo (11/2019) e giurisdizione (16 e 25/2019).

### P11 — ANAC, delibera n. 859 del 25/9/2019 [IC]
- Massima: «la partecipazione pubblica maggioritaria al capitale sociale quale indice presuntivo della situazione di controllo pubblico». La società deve «dimostrare l'assenza di un coordinamento formalizzato tra i soci pubblici» e l'eventuale influenza dominante del privato. ANAC «auspica un intervento urgente del legislatore».
- Non menziona le quotate. Il testo ufficiale su anticorruzione.it non è stato trovato (URL in 404); la copia della Regione Emilia-Romagna è servita da un'app e non scaricabile.

### P12 — ANAC, atto di segnalazione n. 3 del 1/7/2020 (delibera 541) [I]
- **Quotate**: secondo ANAC la nozione di quotata del TUSP comprende le emittenti di strumenti diversi dalle azioni, e la deroga produce esclusioni anomale. Esempi testuali:
  - **CDP**: «società detenuta dal MEF all'82,77% che rientra nella nozione di società in controllo pubblico», emette obbligazioni «fin dal 2014 nell'ambito del mercato regolamentato del Lussemburgo». Per ANAC è quindi «da ascrivere nella categoria delle “società quotate”», esente dal d.lgs. 33/2013.
  - **ANAS**, «per il solo fatto di essere entrata a far parte del Gruppo Ferrovie dello Stato Italiane», «rimarrebbe esclusa dal d.lgs. 33/2013» perché FSI emette strumenti quotati (Dublino) dal 2013. È il caso più vicino a PSN: **una controllata pubblica esce dal regime perché la catena passa per una quotata.**
- Proposte: limitare l'esenzione dal c. 2 alle emittenti di **azioni**; portare le altre quotate nel c. 3; includere per legge fra le società a controllo pubblico quelle «partecipate da più amministrazioni con capitale pubblico maggioritario». Ricorda le «posizioni non univoche … della giurisprudenza amministrativa e contabile». Al 20/11/2026 non risulta (da ricerche web) che le proposte siano state recepite [N].

### P14-P15 — Cons. Stato, sez. VI, 11/4/2022 n. 2655 e 12/9/2022 n. 7896 (Rai) [I]
- Rai è quotata per via delle obbligazioni. Massima (2655): «è evidente la scelta del legislatore di voler sottrarre all'accesso civico le società in controllo pubblico quotate». La tesi del nucleo minimo ex c. 3 per tutte le partecipate è respinta, e la questione di costituzionalità dell'art. 2-bis c. 2 lett. b) è manifestamente infondata. La 7896 conferma.
- **Rilievo**: il giudice applica l'esclusione per le emittenti di obbligazioni **alla lettera**. Le due sentenze confermano che CDP (se emittente qualificata) è fuori dal c. 2, e così le sue «partecipate» salvo la clausola «non per il tramite». Nessuna delle due tratta le società a valle.

### P16 — Cons. Stato, sez. VII, 25/1/2023 n. 860 (ITA) [R]
- Controllo solitario del MEF (100 %) = controllo pubblico ex 2359 n. 1; il rinvio dell'art. 2-bis al TUSP è un rinvio alle sole definizioni (riferito da eius.it). Non riguarda le quotate.

### P17 — Cons. Stato, sez. V, 10/3/2023 n. 2543 [I]
- **Fatti**: CCIAA Venezia Giulia (5 %) chiede accesso a Udine e Gorizia Fiere s.p.a.; nessun socio pubblico ha la maggioranza assoluta e c'è un istituto di credito privato fra i soci.
- **Massima**: «non è sufficiente a tali fini una semplice sommatoria delle partecipazioni di soggetti pubblici … ma occorrono piuttosto, in assenza di un controllo monocratico ex art. 2359 Cod. civ., atti o accordi che vincolino i soggetti pubblici all'esercizio congiunto delle loro prerogative … o quanto meno un comportamento concludente dei soci pubblici orientato in tal senso». Dà atto del contrasto: «cfr., in senso diverso, Corte conti, SS.RR. contr., 20 giugno 2019, n. 11; Anac, delibera 25 settembre 2019, n. 859».
- Criterio: sostanziale intermedio (concreto).

### P18 — Cons. Stato, sez. VI, 18/4/2023 n. 3880 [I] — rilevante anche per le quotate
- **Fatti**: AGCM contro Comune e Provincia di Rimini e CCIAA. Rimini Congressi s.r.l. (100 % pubblica) controlla Italian Exhibition Group (IEG, **quotata dal giugno 2019**; 55,86 % dei voti), che ha acquisito società di allestimento stand.
- **Controllo congiunto**: per «comportamenti concludenti paralleli» (documenti della Provincia, voto coordinato in assemblea), senza prova contraria («come, riprendendo le indicazioni di Anac … sarebbe stato onere di controparte fare»). Che il controllo debba tradursi in atti formali «appare più che dubbio»: vale la libertà delle forme (art. 2341-bis c.c.). Obiter: la PA intesa «unitariamente», per cui «basterebbe allora che il soggetto “Pubblica amministrazione” unitariamente inteso disponga della maggioranza dei voti». Cita anche il parere Cons. Stato, sez. I, 4/6/2014 n. 1801 sui «comportamenti paralleli» [E].
- **Quotate**: l'eccezione fondata sull'art. 1 c. 5 è «manifestamente infondata». La previsione riguarda le norme che hanno «come destinatario diretto le società, e non già le amministrazioni pubbliche». Per gli obblighi delle PA (art. 4) la quotazione della partecipata non consente di eludere i limiti. Inoltre IEG si è quotata dopo il 31/12/2015.
- **Rilievo**: è l'unica pronuncia trovata che applica l'art. 1 c. 5 a una catena PA → controllata non quotata → quotata → partecipate a valle. Non decide se le società **a valle della quotata** siano «a controllo pubblico». Afferma però che gli obblighi delle PA azioniste (razionalizzazione, art. 4/20) seguono la catena anche attraverso la quotata.

### P19 — Cons. Stato, sez. IV, 17/6/2025 n. 5289 [I]
- **Fatti**: S.A.Pro.Di.R. s.r.l., società mista dei rifiuti (Rieti). Soci pubblici frazionati ~51 % (Provincia ~19 %), socio privato Rieco ~44 % che nomina l'AD. Il ricorso mirava a sottrarla all'art. 17 TUSP.
- **Massima**: sono a controllo pubblico anche le società «a controllo pubblico frazionato in cui i soci pubblici dispongono complessivamente, in assemblea ordinaria, della maggioranza dei voti … anche se mancano specifici patti parasociali o vincoli statutari e anche se il socio privato nomina l'amministratore delegato»; «è necessario, ed è anche sufficiente» disporre dei voti ex 2359. Ratio: evitare che le società a capitale pubblico frazionato «possano strumentalmente sottrarsi» al TUSP.
- **Motivo concorrente**: lo statuto attribuisce al socio pubblico di maggioranza relativa la nomina della maggioranza del CdA e del presidente. Ne deriva un controllo ex 2359 n. 3 («in luogo di un patto parasociale ricorre … una espressa previsione statutaria»).
- **Note**: non cita 578/2019, 2543/2023, le SS.RR. 16/2019 né ANAC 859. Sul diverso tema UE afferma l'«assenza, allo stato, di orientamenti giurisprudenziali divergenti». Nessuna rimessione all'Adunanza plenaria. La bozza la descrive con «salvo prova contraria»: l'inciso non è nel testo, che parla di condizione «necessari[a] ed … anche sufficiente» (l'inciso viene dal commento Ardita).
- Criterio: **formale/astratto**, con un argomento concreto (statuto) in sussidio.

### P20 — Cons. Stato, sez. VI, 20/1/2026 n. 436 [I]
- **Fatti**: Padova Hall s.p.a. (Comune di Padova 49,20 %, CCIAA 49,20 %, Provincia 1,60 %), già in house. La RGS-IGF (verifica 2022) la qualifica a controllo pubblico; il TAR Lazio 6983/2024 respinge il ricorso. L'appello è respinto **con diversa motivazione**.
- **Massime**:
  - non sovrapponibilità fra partecipazione e controllo pubblico (richiama 2543/2023, 578/2019, Corte conti 16/2019);
  - il rinvio della lett. m) alla lett. b) comprende l'art. 2359 anche con più PA (no «interpretatio abrogans»): è possibile «un potere di influenza dominante imputato ad un determinato numero di enti»;
  - ma «il mero computo numerico delle partecipazioni … non è, ex se, indice del controllo»: «se il dato numerico è ex se significativo nel caso di dominanza solitario, lo stesso non è, necessariamente, tale in caso di pluralità di partecipazioni»;
  - occorre verificare se i soci «risultino, in concreto e al di là del mero dato numerico, allineati nella gestione»;
  - la concertazione non richiede un patto espresso: sono possibili «forme tacite o attuate mediante comportamenti concludenti», da provare anche con indizi «gravi, precisi e concordanti», «senza dover ricorrere ad una presunzione di controllo derivante dalla partecipazione maggioritaria»;
  - nel caso concreto le decisioni strategiche (bilanci, nomine) sono votate all'unanimità o con il solo voto contrario della Provincia. Ne risulta un'«intesa tacita e duratura», non un «mero “allineamento accidentale”»; il gruppo di controllo non deve comprendere tutti i soci pubblici.
- **Note**: **non cita la 5289/2025** né la smentisce espressamente. Il «superamento» è una lettura del commento (Ardita), non un'affermazione della sentenza. Nessuna rimessione all'Adunanza plenaria (art. 99 c.p.a.), benché il contrasto fra la IV e la V/VI sezione sia evidente. Le spese sono compensate per la «complessità delle questioni».
- Criterio: **sostanziale/concreto** (posizione intermedia).

### P21-P23
- Corte conti Lombardia 84/2026 [R]: «in caso di partecipazioni pubbliche condivise il controllo in forma congiunta tra i soci pubblici è ben possibile attraverso un compendio di strumenti normativi e contrattuali». Corte conti Emilia-Romagna 6 e 7 [R]: definite «dissonanti», non lette. Cass. SU 23220/2026 [R]: la qualità di socio pubblico non basta per la giurisdizione contabile; non riguarda la nozione di controllo.

## 5. Contrasti sul controllo in concreto

| Tesi | Contenuto | Chi la sostiene | Ultimo atto |
|---|---|---|---|
| A. Formale/astratta | Maggioranza dei voti in mano pubblica (anche frammentata) = controllo, senza ulteriori verifiche (prova contraria solo per l'influenza dominante del privato) | Corte conti SS.RR. contr. 11/2019 [R]; Cons. Stato IV 5289/2025 [I]; obiter VI 3880/2023 (PA «unitariamente intesa») | 17/6/2025 |
| B. Presuntiva | Maggioranza = indice presuntivo; la società prova l'assenza di coordinamento | ANAC 859/2019 [IC]; richiamata da VI 3880/2023 | 2023 |
| C. Sostanziale intermedia | Serve concertazione effettiva, anche tacita o per comportamenti concludenti, provata anche per indizi | MEF 15/2/2018 [IC]; LG MEF-CdC [IC]; Cons. Stato V 2543/2023 [I], VI 3880/2023 [I], **VI 436/2026 [I]**; Corte conti Lombardia 84/2026 [R] | **20/1/2026** |
| D. Formale rigorosa | Servono legge, statuto o patti parasociali scritti; non bastano comportamenti concludenti | Corte conti SS.RR. giur. 16 e 25/2019 [E/R]; Cons. Stato V 578/2019 (in tema di mantenimento) [I]; III 1564/2020 [E] | 2020 |

**Oscillazioni.** Nel Consiglio di Stato: V (2019: D) → V (2023: C) → VI (2023: C con aperture ad A/B) → IV (2025: A) → VI (2026: C). Nella Corte dei conti: controllo (A) contro giurisdizione (D) già nel 2019.

**Orientamento prevalente oggi** (con cautela): la tesi **C** è maggioritaria per numero di pronunce del Consiglio di Stato (V 2543/2023, VI 3880/2023, VI 436/2026) e coincide con la prassi del MEF e con la Corte dei conti in sede regionale (Lombardia 2026). La tesi A (IV 5289/2025) resta un precedente recente, non smentito in modo espresso e confermativo di un TAR.

**Rimessione o norma.** Nessuna rimessione all'Adunanza plenaria trovata (né nelle sentenze lette né nelle ricerche web; la ricerca testuale su giustizia-amministrativa.it per «controllo pubblico congiunto» non dà pronunce del Consiglio di Stato successive alla 436/2026 sul tema, ma è limitata ai primi 60 risultati). Nessuna norma di interpretazione: ci sono solo proposte (ANAC 3/2020; CNDCEC, Osservatorio enti pubblici, dicembre 2025, con presunzione per le società a capitale pubblico maggioritario [R, via Ardita]).

**Rilievo per PSN.** La disputa riguarda **più amministrazioni distinte**. Tutte le tesi, compresa la 436/2026, riconoscono che nel controllo **solitario** il dato numerico basta («ex se significativo»). Se le catene di PSN si ricompongono in capo al **solo MEF**, il controllo congiunto non serve: il nodo è il conteggio dei voti tramite quotate (§ 6).

## 6. Controllo indiretto tramite quotate

### 6.1 Le domande e le risposte disponibili

1. **Le controllate dalle quotate sono escluse?**
   - *TUSP*: sì, per il testo vigente dell'art. 1 c. 5 («società da esse controllate»), salvo norma espressa. Secondo Cons. Stato 3880/2023 l'esclusione vale solo per le norme rivolte alle società, non per gli obblighi delle PA azioniste (art. 4, 20).
   - *d.lgs. 33/2013*: l'esclusione è più ampia (anche le «partecipate» dalle quotate), ma cade se la società è «non per il tramite di società quotate, controllata **o partecipata**» da PA.
   - Casi applicativi: ANAS esclusa perché nel gruppo FS (ANAC 2020, critica). Nessuna pronuncia su una controllata di Poste, Leonardo o CDP.
2. **Una società partecipata a maggioranza da quotate a loro volta controllate dallo Stato è a controllo pubblico?** **Nessuna pronuncia lo decide.**
   - *Argomenti per il sì* (computo trasparente): art. 2359 c. 2 c.c. («si computano anche i voti spettanti a società controllate») richiamato senza eccezioni dalla lett. b); orientamento MEF 15/2/2018 sul controllo indiretto; LG MEF-CdC sulle partecipazioni indirette; Cons. Stato 3880/2023 (la quotazione intermedia non sottrae la catena agli obblighi delle PA); ratio antielusiva di 5289/2025.
   - *Argomenti per il no* (filtro delle quotate): la clausola «non per il tramite di società quotate» dell'art. 2-bis (testo vigente) presuppone che ciò che passa per una quotata non valga a far scattare il regime; parere Cons. Stato 968/2016 (solo controllo diretto); relazione illustrativa del TUSP citata dal MEF il 22/6/2018 (partecipate da quotate «di controllo o meno» = «meramente partecipate»); ratio di mercato delle quotate (pareri 968/2016 e 1257/2017; Cons. Stato 2655/2022).
3. **Come si conta la partecipazione tramite quotate?** Mancano prassi e giurisprudenza su un metodo. Due letture coerenti: (a) **trasparente**, ex 2359 c. 2, con voti risaliti per ogni anello controllato (controllo di diritto o di fatto); (b) **con filtro**, che azzera ogni anello quotato (azioni o obbligazioni ex lett. p). Una terza, intermedia, filtra solo le quotate azionarie, come proposto da ANAC 2020 *de iure condendo*: oggi non ha base testuale.

### 6.2 Difformità fra le fonti

| Fonte | Posizione sul controllo tramite quotate | Stato |
|---|---|---|
| TUSP art. 1 c. 5 vigente | Esclude le quotate e le loro **controllate** | [I] |
| d.lgs. 33/2013 art. 2-bis c. 2 lett. b) | Esclude le quotate e le loro **partecipate**, salvo controllo o partecipazione pubblica «non per il tramite di società quotate» | [V]/[I] |
| Parere CdS 968/2016 | Escludere anche il controllo indiretto: contare solo quello diretto | [I] |
| Relazione illustrativa TUSP (via MEF 22/6/2018) | Partecipate da quotate «di controllo o meno» = meramente partecipate | [IC] (citazione in atto MEF) |
| MEF 15/2/2018 | Controllo indiretto sempre computabile ex 2359 c. 2 (nessuna eccezione per le quotate) | [IC] |
| LG MEF-CdC (2018) | Le partecipate dalla «tramite» quotata, se anche controllate o partecipate da PA, restano soggette al TUSP | [IC] |
| ANAC 2017 (LG 1134) | Questione rinviata (tavolo MEF-CONSOB), parte sulle quotate espunta | [I] |
| ANAC 2020 (segnalazione 3) | Esclusione anche per le emittenti di obbligazioni (CDP, FS); la ritiene incoerente e chiede di modificare la norma | [I] |
| Cons. Stato 2655 e 7896/2022 | Esclusione delle quotate (anche per obbligazioni) applicata alla lettera | [I] |
| Cons. Stato 3880/2023 | L'art. 1 c. 5 non protegge le PA; la catena PA → quotata → partecipata resta rilevante per gli obblighi delle PA | [I] |

Le fonti divergono: il MEF e le LG MEF-CdC contano i voti attraverso la catena, la lettera dell'art. 2-bis e il parere 968/2016 li filtrano. Il TUSP del 2019 ha ristretto l'esclusione alle sole controllate dalle quotate, senza toccare l'art. 2-bis.

### 6.3 Le catene concrete (dati da verificare, vedi `parere-psn.md` F6-F10)

| Anello | Quota | Natura | Status ex lett. p) |
|---|---|---|---|
| MEF → Sogei | 100 % | controllo di diritto | Sogei non quotata [S: nessuna emissione nota] |
| MEF → CDP | ~82,77 % (ANAC 2020) | controllo di diritto | **quotata per ANAC** (obbligazioni su mercato regolamentato del Lussemburgo dal 2014; status mantenuto da nuove emissioni ex art. 26 c. 5-bis) [I ANAC; R per il 2026] |
| CDP → CDP Equity | 100 % | controllo di diritto | non quotata (controllata da quotata → esclusa dal TUSP ex art. 1 c. 5) [S] |
| MEF (29,7 %) + CDP (35 %) → Poste | 64,7 % | controllo di diritto del MEF (diretto + tramite CDP) | quotata (azioni) |
| Poste → TIM | ~85,8 % da settembre 2026 | controllo di diritto | quotata (azioni; delisting non avvenuto) |
| MEF → Leonardo | ~30,2 % | **controllo di fatto** ex 2359 n. 2 (lista di maggioranza in assemblea) | quotata (azioni) |

## 7. Applicazione al PSN

Soci: TIM 45 %, Leonardo 25 %, CDP Equity 20 %, Sogei 10 %. Dal 2026 TIM è a maggioranza Poste.

### 7.1 Quote di voto «pubbliche» secondo il metodo

| Metodo | Fino ad agosto 2026 | Da settembre 2026 |
|---|---|---|
| Trasparente con controllo di fatto su Leonardo | 10 + 20 + 25 = **55 %** | 10 + 20 + 25 + 45 = **100 %** |
| Trasparente senza Leonardo (solo controllo di diritto) | 10 + 20 = 30 % | 10 + 20 + 45 = **75 %** |
| Filtro sulle quotate azionarie (CDP non filtrata) | 10 + 20 = 30 % | 30 % |
| Filtro su tutte le quotate ex lett. p) (anche CDP) | **10 %** | **10 %** |

Dopo settembre 2026 il computo trasparente dà la maggioranza **anche senza** il controllo di fatto su Leonardo. Resta però decisivo che CDP Equity e TIM siano contate, cioè che non si applichi il filtro.

### 7.2 Argomenti per «non ancora controllata di diritto»
1. **Lettera dell'art. 2-bis c. 2 lett. b)**: PSN è partecipata da quotate (TIM, Leonardo). La salvezza vale solo per il controllo o la partecipazione pubblica «non per il tramite di società quotate». Per questa via c'è solo Sogei (10 %), che basta per la partecipazione: PSN resta nel regime ma come società a **partecipazione** (c. 3). Coincide con l'autoqualificazione di PSN (MOG 231) e con il censimento MEF 2023 (Sogei: «nessun» controllo).
2. **CDP quotata** (ANAC 2020, giudice amministrativo 2022 sulle emittenti di obbligazioni): con il filtro anche i 20 % di CDP Equity non contano.
3. **Ratio di mercato** (pareri 968/2016 e 1257/2017; MEF 22/6/2018): il regime pubblicistico non deve risalire dentro i gruppi quotati; la relazione illustrativa tratta come «meramente partecipate» le società in cui partecipano quotate.
4. **Controllo di fatto su Leonardo non accertato**: nessuna pronuncia o atto lo accerta. Senza Leonardo, prima del 2026 la maggioranza non c'è con nessun metodo.
5. **Controllo pubblico congiunto non provato**: non risultano patti parasociali pubblici fra TIM, Leonardo, CDP Equity e Sogei. Con la 436/2026 l'onere di provare una concertazione tacita è di chi afferma il controllo. Il potere del concedente (DTD) sui nuovi soci è contrattuale (convenzione), non societario. Andrebbe valutato come possibile «vincolo contrattuale» ex 2359 n. 3 [S, non trovata giurisprudenza].
6. **ISTAT**: PSN fuori da S13 (dato della bozza).

### 7.3 Argomenti per «controllata sostanzialmente» (e forse di diritto ai fini TUSP)
1. **Controllo solitario, non congiunto**: tutte le catene risalgono al MEF. Per la 436/2026 il dato numerico nel controllo solitario è «ex se significativo», e la disputa sul controllo congiunto non si pone.
2. **Art. 2359 c. 2 c.c. e MEF 15/2/2018**: il controllo indiretto è parte della nozione di controllo e il TUSP non prevede un filtro per le quotate **nel computo** (lett. b, m). Il filtro dell'art. 1 c. 5 riguarda l'applicabilità del decreto alle quotate e alle loro *controllate*, e PSN non è controllata da una singola quotata (nessuna supera il 50 %).
3. **Dal settembre 2026**: con TIM sotto Poste la quota pubblica trasparente è 75 % senza Leonardo, dunque una maggioranza **di diritto** (2359 n. 1 con c. 2), che non dipende dal controllo di fatto.
4. **Antielusione** (Cons. Stato 5289/2025; 3880/2023): la quotazione dell'anello intermedio non deve sottrarre alle regole pubbliche un veicolo detenuto in ultima istanza dallo Stato; gli obblighi delle PA azioniste seguono la catena (3880/2023).
5. **Comportamenti concludenti** (se servissero): il MEF esprime le liste di maggioranza in Leonardo e controlla Poste e CDP. PSN è il veicolo di una politica pubblica (art. 33-septies d.l. 179/2012) e i soci sono legati dal PEF e dalla convenzione. Sono indizi da documentare, non prove.

### 7.4 Sintesi per ambito
- **TUSP**: almeno *società a partecipazione pubblica* (lett. n: partecipata da Sogei, a controllo pubblico) — certezza alta. *Società a controllo pubblico*: fino ad agosto 2026 **dubbio, prevalente il no** (55 % solo con Leonardo, senza accertamento); da settembre 2026 **dubbio, con argomenti per il sì ora più forti** (75 % di diritto con il computo trasparente), ma senza giurisprudenza sul conteggio tramite quotate.
- **Trasparenza / L. 190/2012**: la lettera dell'art. 2-bis c. 2 lett. b) («non per il tramite di società quotate») sostiene la collocazione nel **c. 3** — certezza media. Il passaggio di TIM sotto Poste non cambia la conclusione letterale, perché anche quel controllo passa per quotate (Poste, TIM).
- **Dataset del progetto**: si conferma la proposta della bozza («partecipata» come classe giuridica, più un campo di sostanza «controllo indiretto MEF tramite quotate», datato). Si aggiunge che dal settembre 2026 il computo trasparente dà il 75 % **senza** Leonardo.

## 8. Grado di certezza

| Affermazione | Certezza | Perché |
|---|---|---|
| Testo vigente dell'art. 1 c. 5 TUSP = «controllate» | alta | Normattiva [I]; fonte della modifica (L. 145/2018 c. 721) solo [R] |
| Orientamento CdS più recente = controllo congiunto in concreto (436/2026) | alta sul contenuto, media sulla «prevalenza» | contrasto con IV 5289/2025 non risolto |
| Nessuna rimessione all'Adunanza plenaria né norma di interpretazione al 20/11/2026 | media | assenza di prova (ricerca web + ricerca testuale GA limitata) |
| Nessuna pronuncia sul conteggio del controllo tramite quotate | media | assenza di prova |
| CDP è «quotata» ex lett. p) | media | ANAC 2020 [I]; status 2026 da verificare (art. 26 c. 5-bis, emissioni) |
| PSN partecipata (TUSP lett. n) | alta | Sogei, controllata dal MEF, ne è socia diretta |
| PSN fuori dall'art. 2-bis c. 2 lett. b) | media | lettera chiara; prassi ANAC sulle catene assente |
| PSN a controllo pubblico TUSP da settembre 2026 | bassa-media | dipende dal metodo di computo, non deciso |

## 9. Correzioni a `parere-psn.md`

1. § 3.1: il testo dell'art. 1 c. 5 TUSP citato («partecipate, salvo che … non per il tramite di società quotate…») è **superato**. Vigente: «nonché alle società da esse controllate» (Normattiva). La formula «non per il tramite» resta solo nell'art. 2-bis d.lgs. 33/2013. Il ragionamento della bozza va spostato sull'art. 2-bis, e per il TUSP va riformulato (§ 6-7 qui).
2. § 4, riga Cons. Stato 5289/2025: «salvo prova contraria» non è nel testo; la sentenza dice «necessario, ed è anche sufficiente».
3. § 4, riga 436/2026: la sentenza **non cita** né «supera» espressamente la 5289/2025 (lettura del commentatore). La citazione testuale nella bozza è corretta; nel testo si legge «dominanza solitario», non «in solitario».
4. § 4, riga 578/2019: la sentenza non riguarda la definizione di controllo pubblico ex lett. m), ma il mantenimento di partecipazioni pulviscolari. La massima («servono patti parasociali o organo statutario») è corretta come obiter.
5. § 4, riga Corte conti 11/2019: date divergenti (4/4/2019 secondo Ardita; 20/6/2019 secondo Cons. Stato 2543/2023). La bozza dice «adottata 4/4/2019, depositata 20/6/2019»: plausibile, non verificato sul testo.
6. § 3.1, punto 4: CDP «quotata» non è più solo [R]. ANAC (atto di segnalazione 3/2020) la qualifica tale per le obbligazioni; resta da verificare lo status al 2026.
7. § 4, ultima riga («Società quotate … Nessuna pronuncia trovata»): resta vero per Leonardo, Poste e PSN. Vanno aggiunti Cons. Stato 3880/2023 (art. 1 c. 5 e catene con IEG quotata), Cons. Stato 2655 e 7896/2022 (Rai), ANAC 3/2020 (CDP, ANAS-FS) e il parere 968/2016.

## 10. Fonti (URL, data di accesso 20/11/2026, stato)

File archiviati in `lavoro/inhouse/giurisprudenza/` con sha256 in `INDICE.tsv`. Script di ricerca: `ga_cerca.sh` e `ga_scarica.sh`. Ritmo di almeno 5 s fra le richieste e User-Agent da browser con l'URL del progetto. giustizia-amministrativa.it non ha robots.txt (404).

**Testo integrale letto [I]**
- Cons. Stato VI 436/2026 — https://mdp.giustizia-amministrativa.it/visualizza/?nodeRef=&schema=cds&nrg=202408846&nomeFile=202600436_11.html&subDir=Provvedimenti — `CdS_VI_2026_436.html`
- Cons. Stato IV 5289/2025 — https://mdp.giustizia-amministrativa.it/visualizza/?nodeRef=&schema=cds&nrg=202401061&nomeFile=202505289_11.html&subDir=Provvedimenti — `CdS_IV_2025_5289.html`
- Cons. Stato V 2543/2023 — https://mdp.giustizia-amministrativa.it/visualizza/?nodeRef=&schema=cds&nrg=202205957&nomeFile=202302543_11.html&subDir=Provvedimenti — `CdS_V_2023_2543.html`
- Cons. Stato VI 3880/2023 — https://mdp.giustizia-amministrativa.it/visualizza/?nodeRef=&schema=cds&nrg=202102936&nomeFile=202303880_11.html&subDir=Provvedimenti — `CdS_VI_2023_3880.html`
- Cons. Stato V 578/2019 — https://mdp.giustizia-amministrativa.it/visualizza/?nodeRef=&schema=cds&nrg=201805502&nomeFile=201900578_11.html&subDir=Provvedimenti — `CdS_V_2019_578.html`
- Cons. Stato VI 2655/2022 — https://mdp.giustizia-amministrativa.it/visualizza/?nodeRef=&schema=cds&nrg=202106876&nomeFile=202202655_11.html&subDir=Provvedimenti — `CdS_VI_2022_2655_Rai.html`
- Cons. Stato VI 7896/2022 — https://mdp.giustizia-amministrativa.it/visualizza/?nodeRef=&schema=cds&nrg=202200534&nomeFile=202207896_11.html&subDir=Provvedimenti — `CdS_VI_2022_7896_Rai.html`
- Cons. Stato, Comm. spec., parere 968/2016 — https://mdp.giustizia-amministrativa.it/visualizza/?nodeRef=&schema=consul&nrg=201600438&nomeFile=201600968_27.html&subDir=Provvedimenti — `CdS_CommSpec_parere_2016_968_schema_TUSP.html`
- Cons. Stato, Comm. spec., parere 1257/2017 — https://mdp.giustizia-amministrativa.it/visualizza/?nodeRef=&schema=consul&nrg=201700650&nomeFile=201701257_27.html&subDir=Provvedimenti — `CdS_CommSpec_parere_2017_1257_LG_ANAC.html`
- ANAC, delibera 1134/2017 (relazione AIR e LG) — https://www.anticorruzione.it/documents/91439/d75727a4-03de-0dc7-9b26-9d07078ba604
- ANAC, atto di segnalazione 3/2020 (delibera 541) — https://www.anticorruzione.it/documents/91439/cbe018f2-4847-07ee-6be8-2fc43bd46ab8 (pagine 2-7 lette come immagine: il testo estratto è lacunoso)
- ANAC, bozza di aggiornamento delle LG 1134 (consultazione; scaricata, non analizzata) — https://www.anticorruzione.it/documents/91439/6dbfc870-9a66-423e-67e5-71f7f1f41b89
- TUSP artt. 1, 2, 26 vigenti — https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2016-08-19;175~art1!vig= (e ~art2, ~art26)
- M.E. Ardita, commento alla 436/2026, Amministrazione in cammino, 27/7/2026 — https://www.amministrazioneincammino.luiss.it/wp-content/uploads/2026/07/Ardita_forum_27_07_26.pdf (commento, letto integralmente)

**Testo integrale da copia non ufficiale [IC]**
- MEF-DT, orientamento 15/2/2018 — https://www.dirittobancario.it/wp-content/uploads/sites/default/files/allegati/orientamento_struttura_di_monitoraggio_mef-dt_15_febbraio_2018.pdf
- MEF-DT, orientamento 22/6/2018 — https://www.dirittobancario.it/wp-content/uploads/sites/default/files/allegati/orientamento_22_giugno_2018.pdf
- LG MEF-DT e Corte dei conti sulla revisione periodica — https://www.dirittobancario.it/wp-content/uploads/sites/default/files/allegati/linee_guida_tusp.pdf
- ANAC, delibera 859/2019 (testo riportato) — https://www.segretaricomunalivighenzi.it/01-11-2019-obbligo-di-applicare-la-normativa-anticorruzione-per-la-societa-a-partecipazione-pubblica-maggioritaria-salvo-dimostrazione-contraria/

**Riferito [R] / non raggiunto**
- Corte conti SS.RR. contr. 11/2019, SS.RR. giur. 16 e 25/2019: testo non raggiunto. `banchedati.corteconti.it/robots.txt` = «Disallow: /», non interrogata. Commenti: segretaricomunalivighenzi.it (1/7/2019, 24/6/2019), Sipotra (nota alla 16/2019, PDF non scaricabile: risposta HTML).
- Cons. Stato VII 860/2023 (ITA) — https://www.eius.it/giurisprudenza/2023/036 (sintesi)
- Cons. Stato III 1564/2020; sez. I parere 1801/2014 — solo citazioni in 2543/2023 e 3880/2023
- Corte conti Lombardia 84/2026; Emilia-Romagna 6 e 7 — via Ardita
- Cass. SU ord. 23220/2026 — https://www.dirittobancario.it/art/azione-di-responsabilita-nelle-partecipate-e-giurisdizione-della-corte-dei-conti/ (snippet)
- L. 145/2018 art. 1 c. 721 — https://www.segretaricomunalivighenzi.it/28-02-2019-t-u-societa-a-partecipazione-pubblica-le-modifiche-apportate-dalla-legge-di-bilancio-2019/28/02/2019
- Proposta CNDCEC di modifica del TUSP (dicembre 2025) — https://commercialisti.it/wp-content/uploads/2025/12/Tusp2025_12_10_def.pdf (citata da Ardita, non aperta)

**Non trovato [N]**
- Pronunce o atti sul controllo di fatto del MEF su Leonardo, su società a valle di Poste/TIM o CDP Equity, su PSN; rimessioni all'Adunanza plenaria sul controllo pubblico; norme di interpretazione 2019-2026.
- Testo ufficiale della delibera ANAC 859/2019 su anticorruzione.it (l'URL della pagina dà 404).


## Registro delle revisioni

| versione | data | modifica |
|---|---|---|
| 0.1 | 2026-11-20 | prima versione, richiesta da Fabio: controllo in concreto, controllo tramite quotate, PSN |
