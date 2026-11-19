---
title: "Design metodologico e confronto europeo"
date: 2026-11-19
description: "Come è disegnata la misura della spesa cloud della PA italiana per giurisdizione (due assi, imbuto a strati, livelli di raffinamento, due lenti, valori) e come si confronta con le misure europee: quote di mercato, indici, studi sugli appalti, inchieste parlamentari e Corti dei conti. Ogni fonte esterna è verificata e archiviata con sha256, oppure marcata come riferita."
weight: 19
gruppo: misura
---

**Versione 1.0 del 19/11/2026** ([#48](https://github.com/mxmap-it/analisi-spesa-ict/issues/48)).
Questa pagina riassume il disegno e rimanda alle pagine che lo descrivono in dettaglio: non le sostituisce. I numeri italiani sono solo quelli già pubblicati, con il rimando alla pagina che li produce. La seconda parte confronta il disegno con le misure europee.

**Legenda.**
- **[V]**: abbiamo letto l'affermazione sulla fonte primaria, archiviata nel nostro archivio append-only (sha256 abbreviato fra parentesi; elenco completo in [`report/metodo/prove-design/fonti-europee.csv`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/metodo/prove-design/fonti-europee.csv)). Per le fonti esterne [V] vuol dire che **la fonte dice questo**, non che abbiamo rifatto il suo calcolo.
- **[R]**: riferito da un terzo, **da verificare**: la fonte primaria non era raggiungibile senza aggirare una protezione, oppure non l'abbiamo letta.
- **[S]**: stima o proposta nostra.

## 1. Il design attuale in breve

### 1.1 Che cosa misuriamo

Quanto spende la PA italiana in **servizi cloud esterni** e in **infrastrutture informatiche proprie**, diviso per **giurisdizione**: Italia, UE, extra-UE. Il processo si deve poter rifare ogni anno con gli stessi comandi.

L'unità è il **contratto**, identificato dal CIG (codice identificativo di gara) dell'Autorità nazionale anticorruzione (ANAC). Per ogni contratto ci sono due domande indipendenti:
1. **asse A: è cloud?**
2. **asse B: di quale giurisdizione?**

Su ciascun asse un contratto è *escluso con certezza*, *incluso con certezza* o *incerto*. Dettaglio: [L'imbuto](/progetto/imbuto/).

### 1.2 Il principio a imbuto e gli strati

Il principio (Fabio, 29/10/2026): escludere ciò che è certamente fuori, includere ciò che è certamente dentro, spendere lo sforzo costoso solo sull'incerto. Gli strati sono:

| strato | contenuto |
|---|---|
| S0 | accordi quadro e convenzioni «padre»: massimali, contati nei contratti attuativi |
| S1 | esclusi con certezza: non informatica |
| S2 | sotto 500 € |
| S3 | inclusi per convenzione o lotto noto |
| S4 | inclusi per marchio del prodotto nell'oggetto |
| S5 | informatica non cloud |
| S6 | residuo incerto |

La spesa ICT è S3-S6. I numeri dal 2024 sono nella pagina [L'imbuto](/progetto/imbuto/) e nel [punto nave del 19/11](/rendiconti/punto-nave-2026-11-19/): 289.192 CIG per 114,4 miliardi dichiarati, circa 56 miliardi al netto dei massimali [V]. Il perimetro ICT è una lista bianca di 12 prefissi del vocabolario comune degli appalti (CPV) più segnali nel testo: [Perimetro ICT](/progetto/perimetro-ict/).

### 1.3 Raffinamento a livelli

L'imbuto resta largo. Sopra si applicano livelli sempre più costosi, ciascuno solo sul residuo del precedente. Un livello non modifica l'imbuto: scrive una tabella per CIG con esito, motivo e via. Si esce solo con certezza.

| livello | mezzo |
|---|---|
| L1 | regole dell'imbuto: testo, CPV, lotti, marchi |
| B | segnali della Banca dati nazionale dei contratti pubblici (BDNCP): **B1** quadro economico (lavori o informatica), **B2** società in-house pubbliche o privati, **B3** durata effettiva, **B4** tre vie per i fondi del Piano nazionale di ripresa e resilienza (PNRR) |
| L2 | regola sul testo (stampanti, consumabili, cablaggio) |
| L3 | Claude Opus sul solo testo ANAC, senza strumenti |
| L4 | Claude Opus con ricerca e archiviazione degli atti di gara |

Regole, comandi e misure di precisione: [Raffinamento dell'imbuto](/progetto/raffinamento-imbuto/). Effetti a oggi: [punto nave, § 3](/rendiconti/punto-nave-2026-11-19/).

### 1.4 Due lenti: prodotto e fornitore

- **Lente prodotto (primaria).** La giurisdizione segue il prodotto comprato, riconosciuto dal testo, dal lotto della convenzione o dal marchio. Microsoft 365 venduto da un rivenditore italiano resta Microsoft.
- **Lente fornitore (secondaria).** La capogruppo di chi vince il contratto. Serve per confrontarsi con gli studi europei, che usano questa lente (§ 2).
- **Incrocio.** Una tabella incrocia le due lenti: misura quanta spesa verso prodotti extra-UE passa da vincitori italiani o europei.

Le vie di attribuzione e i sei campioni a cieco sono in [Come si riconosce il cloud provider](/progetto/metodo-cloud-provider/). I rivenditori sono un tema a sé.

### 1.5 Criteri di sovranità

In breve ([Criteri di sovranità](/progetto/criteri-sovranita/)):
- un servizio cloud di Microsoft, Google, Amazon o Oracle è **extra-UE chiunque lo rivenda**, compreso il Polo Strategico Nazionale (PSN);
- il resto segue **chi eroga il servizio in proprio**; il software statunitense usato da un operatore italiano è una *dipendenza tecnologica*, registrata a parte;
- la Svizzera conta fra i sovrani, con il paese registrato;
- ciò che non è certo su fonte resta **incerto**.

### 1.6 Valori: contratti e pagato

- **Valore dei contratti.** L'importo ANAC è un valore dichiarato, spesso pluriennale, a volte un massimale. Non è la spesa di un anno (mancanze M4 e M8 della [Mappa](/progetto/mappa-imbuto/)). Il livello B3 misura la quota annua con le date effettive.
- **Pagato.** È una serie separata: SIOPE (il sistema dei pagamenti degli enti non statali) e BDAP (la Banca dati delle amministrazioni pubbliche, per lo Stato centrale). Il pagato ICT 2024 è circa 5,1 miliardi [V]: [SIOPE](/progetto/siope/), [BDAP](/progetto/bdap/). Il pagato non ha un codice cloud: serve come vincolo di plausibilità, non per attribuire la giurisdizione.
- **Mai sommati.** Contratti e pagato non si sommano e non si correggono l'uno con l'altro senza dirlo.

### 1.7 Ripetibilità annuale

Ogni numero viene da una verifica in `tools/verifiche/`, eseguibile da un clone pulito ([RIPRODURRE.md](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/RIPRODURRE.md)). Il 19/11/2026 tutti i passi deterministici sono stati rifatti da zero e tutti i numeri pubblicati si sono riprodotti ([punto nave, § 5](/rendiconti/punto-nave-2026-11-19/)). Le letture del modello linguistico (L3, L4) non sono deterministiche: i loro esiti sono versionati in git e si rileggono. Il quadro sperimentale è in [Metodologia sperimentale](/progetto/metodologia-sperimentale/).

## 2. Confronto europeo

### 2.1 Da dove partiamo

Il punto di partenza sono due rapporti di ricerca dell'Osservatorio del 27/10/2026, «Misure europee sovranità digitale» e «Metodi europei spesa cloud pubblica», con una legenda simile alla nostra. Il 19/11/2026 abbiamo riaperto dal vivo le fonti primarie citate, le abbiamo archiviate e abbiamo riletto ogni cifra che riportiamo qui. Una richiesta per volta, robots.txt controllato. Tre fonti hanno risposto 403 (accesso negato): non abbiamo insistito né aggirato la protezione.

Il quadro che ne esce: **nelle fonti lette, nessuno misura la spesa pubblica per giurisdizione del prodotto**. Le misure si dividono in quattro famiglie:
- **quote di mercato**, sull'intera economia;
- **indici** per paese;
- **studi sugli appalti**, che classificano il vincitore o contano le menzioni di un marchio;
- **inchieste istituzionali** (parlamenti, Corti dei conti), su perimetri parziali.

Non abbiamo cercato in modo sistematico in tutti i paesi: l'assenza di risultati è un limite della ricerca, non una prova che il metodo non esista altrove.

### 2.2 Tabella comparata

| chi, paese, anno | che cosa misura | unità | giurisdizione attribuita a | limiti | verifica |
|---|---|---|---|---|---|
| Synergy Research Group, Europa, 24/7/2025 | quote di mercato: ricavi cloud infrastrutturale (IaaS, PaaS, cloud privato ospitato) in Europa | fornitore | sede del fornitore | intera economia, non la PA; dati proprietari, metodo non pubblico | [V] (b5b502ea) |
| Digital Dependence Index, Università di Bonn (CASSIS) e Vodafone Institute, 51 paesi, 2017-2023 | indice composito 0-1 su hardware, software, piattaforme, proprietà intellettuale | paese | paese | pesi e metodo non letti; nessuna spesa | [V] pagina (d65560eb), metodo da leggere |
| Studio «European Software and Cyber Dependencies», Parlamento europeo PE 778.576, Visionary Analytics per la commissione ITRE, dicembre 2025 | appalti: avvisi di aggiudicazione su TED (la gazzetta europea degli appalti) | vincitore | sede della capogruppo del vincitore | circa 315 avvisi; perimetro ambiguo (§ 2.3); un modello linguistico assegna la sede senza metriche di validazione | [V] (6429f4b5) |
| Compass Lexecon per Open Cloud Coalition, UE, luglio 2025 | menzioni del marchio Microsoft nei bandi TED | menzione | marchio | conta citazioni, non euro; committente sostenuto da un concorrente | [R] dallo studio PE, p. 62; fonte primaria 403 |
| Bundestag, Germania, risposta del governo 21/5413, 14/4/2026 | spesa per licenze, contratti quadro e singoli dei ministeri | contratto | gruppo controparte | tabelle in PDF; alcune risposte negate per la sicurezza dello Stato; il governo avverte di imprecisioni e lacune | [V] (6401171c) |
| Senato, Francia, rapporto n. 830, 8/7/2025 | appalti pubblici e sovranità economica: cifre per contratto e per fornitore | contratto, fornitore | non attribuita in modo sistematico | cifre parziali, alcune riferite in audizione; nessun totale | [V] (e9cb3a0f) |
| Assemblée nationale, Francia, rapporto n. 3054, 8/7/2026 | questionari agli enti; primi 50 fornitori UGAP | editore e gruppo | nazionalità del gruppo, verificata a mano | il totale nazionale è un'estrapolazione da una quota di mercato stimata | [V] (51435b16) |
| Cour des comptes, Francia, 22/10/2026 | spesa per suite d'ufficio e strumenti collaborativi dei ministeri | editore | editore | solo ministeri, solo produttività; contabilità ricostruita dalla Corte | [V] pagina (bd053f38), PDF non archiviato |
| Algemene Rekenkamer, Paesi Bassi, 15/1/2025 | inventario dei servizi cloud dello Stato | servizio | fornitore del servizio | nessuna cifra di spesa | [V] (9281ca1e) |
| Rigsrevisionen, Danimarca, nota 1123/23, 16/11/2023 | rischio di dipendenza nei contratti di gestione informatica | contratto | non attribuita | misura contrattuale, non spesa né giurisdizione | [V] (30d9759d) |
| Controllo federale delle finanze (EFK), Svizzera, 23740, 29/2/2024 | audit del progetto di migrazione a Microsoft 365 | progetto | — | un solo progetto | [V] (e51991ce) |
| Computer Weekly, Regno Unito, 2026 | ricognizione DNS dei domini di enti pubblici | dominio | fornitore del servizio | misura l'uso, non la spesa | [R] dal rapporto del 27/10; pagina 403 |
| AgID con Politecnico di Milano, Italia, 29/5/2025 | spesa ICT di un panel di 77 enti | ente | non attribuita | panel, non censimento | [V] comunicato (eb4ae5c6), rapporto non letto |
| Istat, Italia, 2022 | adozione del cloud nelle PA locali | ente | non attribuita | adozione, non spesa | [V] (cb003399) |
| Corte dei conti, Italia, delibera 30/2024/G | attuazione degli investimenti PNRR per il cloud e del PSN | progetto | — | stato di attuazione, non spesa per giurisdizione | [V] (713ea1ce) |

### 2.3 Che cosa dicono le fonti, e le verifiche aperte dei rapporti

**Synergy Research** [V] (b5b502ea). La quota dei fornitori cloud europei sul loro mercato è scesa dal 29 % del 2017 al 15 % del 2022 ed è stabile da allora; Amazon, Microsoft e Google valgono il 70 %. È l'unico ordine di grandezza europeo diffuso, ma riguarda tutta l'economia e attribuisce al fornitore. Non è confrontabile con una misura sulla PA: al più è un termine di paragone.

**Digital Dependence Index** [V] (d65560eb). La pagina pubblica dà all'Italia 0,78 nel 2023, livello «medio» (0,57-0,83). È un indice per paese: non scende al contratto.

**Studio del Parlamento europeo PE 778.576: il conflitto fra le note è risolto** [V] (6429f4b5). Le due note del primo rapporto si contraddicevano: una diceva che c'era un'analisi dei dati TED, l'altra che lo studio era solo ricerca documentale. Sul PDF archiviato:
- l'**Annesso 1 «TED data analysis» esiste**, pp. 175-179;
- l'estratto viene dalla sezione TED sui contratti **aggiudicati dalle istituzioni UE**, 2020-2025, con **13.238 avvisi**;
- filtro per parole chiave, dizionario di grandi fornitori e verifica con ChatGPT, con revisione manuale: restano **circa 315 avvisi**;
- le gare con più vincitori diventano una riga per vincitore (778 righe), con i dati della gara copiati su ogni riga;
- la sede è assegnata con il dizionario per il 41,3 % delle righe e con ChatGPT per il 58,7 %;
- risultato principale: solo il **59 % delle aziende vincitrici ha sede nell'UE**; quasi l'88 % del valore va a raggruppamenti con almeno un membro non europeo (p. 61).

Resta un'**ambiguità di perimetro**: la nota 168 (p. 60) descrive TED come la banca dati delle gare di tutti gli Stati membri, mentre l'annesso indica la sezione delle istituzioni UE. Lo studio stesso ammette che i vincitori più frequenti (Accenture, Deloitte, NTT Data) sono società di servizi «rather than software vendors» (p. 61-62): è il limite della lente vincitore. Il calcolo dell'88 % non è riproducibile dal testo: l'annesso dice che per le gare con più vincitori i valori sono stati riassunti con tabelle pivot «per evitare doppi conteggi», ma non pubblica dati né codice.

**Compass Lexecon / Open Cloud Coalition** [R]. Il comunicato e il rapporto hanno risposto 403. Lo studio del Parlamento europeo (p. 62) ne riporta il risultato: quota di «incidenza» delle menzioni di Microsoft nei bandi del 72-91 % nel 2023 e dell'89-100 % nel 2024. È una quota di **menzioni**, non di spesa. Il rapporto del 27/10 riferisce un conflitto di interessi del committente: da verificare.

**Germania, Bundestag 21/5413** [V] (6401171c).
- I 481,4 milioni di euro di licenze Microsoft nel 2025 stanno nella **premessa dei deputati che fanno la domanda** (Die Linke). La fonte citata è un articolo delle *Stuttgarter Nachrichten*, non della *Stuttgarter Zeitung* come scriveva il rapporto del 27/10. Il governo non conferma la cifra.
- Il governo avverte che possono esserci «Unschärfen und ggf. Datenlücken» (imprecisioni ed eventuali lacune).
- Per i contratti quadro il volume è «lediglich eine Höchstgrenze», soltanto un tetto massimo. È la stessa trappola dei nostri massimali (strato S0).
- Ancora aperto: l'estrazione completa delle tabelle allegate.

**Francia.**
- Senato, rapporto n. 830 [V] (e9cb3a0f): presidente Simon Uzenat, relatore Dany Wattebled. Non dà una spesa Microsoft complessiva dello Stato. Riporta cifre parziali:
  - vendite 2024 della centrale d'acquisto UGAP: 860 milioni di software multi-editore e 44 milioni di ospitalità cloud;
  - dei 44 milioni, 8,1 a Microsoft e 2,2 ad AWS, cifre riferite in audizione;
  - l'accordo quadro Microsoft del ministero dell'Istruzione: 74,72 milioni stimati in quattro anni, massimale 152 milioni. Due lotti su tre sono andati al rivenditore Crayon France. È un caso da manuale di prodotto extra-UE comprato da un rivenditore europeo.
- Assemblée nationale, rapporto n. 3054 (presidente Philippe Latombe, relatrice Cyrielle Chatelain) [V] (51435b16):
  - Microsoft vale 115 milioni nel 2025 sul perimetro della commissione;
  - gli acquisti UGAP verso gruppi statunitensi sono almeno 609 milioni, il 79 % dei primi 50 fornitori, con la nazionalità verificata a mano;
  - dividendo per una quota di mercato UGAP **stimata** al 40 % si arriva a circa 1,5 miliardi. È un'**estrapolazione**, non una misura.
- Cour des comptes, 22/10/2026 [V] (bd053f38):
  - circa 100 milioni nel 2025 per gli strumenti d'ufficio e collaborativi di circa 860.000 postazioni;
  - più della metà va a Microsoft;
  - fino a 130 milioni l'anno sono una spesa **evitata** in uno scenario, non un risparmio misurato;
  - la Corte scrive che la conoscenza dei crediti consumati soffre di un monitoraggio poco rigoroso.

**Paesi Bassi** [V] (9281ca1e). L'Algemene Rekenkamer conta 1.588 servizi cloud dello Stato. Del 26 % non si sa che tipo di cloud sia. Per 84 dei 126 servizi più importanti manca l'analisi dei rischi. Più della metà dei servizi più importanti è comprata da Amazon, Microsoft e Google: è un conteggio di servizi, non una spesa. La pubblicazione esplicita della **quota ignota** è un modello da seguire.

**Danimarca** [V] (30d9759d). In 24 dei 72 contratti di gestione informatica esaminati c'era rischio di dipendenza dal fornitore. È una misura contrattuale, senza giurisdizione.

**Svizzera** [V] (e51991ce). L'EFK ha esaminato il progetto di migrazione dell'amministrazione federale a Microsoft 365 collegato al cloud pubblico di Microsoft. Il volume del progetto è di 26,5 milioni di franchi. Al momento dell'audit i rischi residui della migrazione al cloud non erano ancora stati rilevati e accettati del tutto. È un audit di progetto, non una misura di spesa.

**Regno Unito** [R]. L'articolo di Computer Weekly ha risposto 403. Il rapporto del 27/10 lo descrive come una ricognizione DNS su 29 enti, parente di MxMap, e ritira le cifre di spesa (17,7 miliardi di sterline, 55 %) attribuite in precedenza: la loro fonte è ignota. Non le usiamo. I rapporti di Tussell sono a pagamento: non verificati.

**Italia.**
- AgID e Politecnico di Milano [V] (eb4ae5c6): panel di 77 enti; la spesa ICT del panel sale da circa 3,8 miliardi nel 2022 a quasi 5 miliardi nel 2025; l'innovazione vale in media il 44 %. Nessuna divisione per fornitore o giurisdizione. Il rapporto completo non è stato letto. Il nostro pagato ICT 2024 (circa 5,1 miliardi, § 1.6) viene da una fonte diversa, SIOPE più BDAP, e copre tutti gli enti: i due numeri **non si confrontano direttamente**.
- Istat [V] (cb003399): le PA locali che usano il cloud passano dal 34,3 % del 2018 al 54,2 % del 2022. È adozione, non spesa.
- Corte dei conti, delibera 30/2024/G [V] (713ea1ce): il PSN prevede un investimento di 723 milioni a carico del concessionario e una convenzione di 13 anni. Nel cronoprogramma di ReGIS (il sistema di monitoraggio del PNRR) «non si registrano pagamenti».
- Agenzia per la cybersicurezza nazionale (ACN), regolamento cloud [V] (577ec23b): i requisiti riguardano il luogo dei dati e dei metadati (nell'UE) e gli accessi da parte di entità extra-UE. Nelle occorrenze cercate non ci sono requisiti sulla nazionalità o sul controllo societario del fornitore. Per questo la qualificazione ACN non dice la giurisdizione nel nostro senso.

**Verifiche dei rapporti ancora aperte:** metodo del Digital Dependence Index; tabelle complete del Bundestag; PDF della Cour des comptes; rapporto di Compass Lexecon (403); rapporto completo AgID 2024; soglie di capitale di SecNumCloud (lo schema di qualificazione francese) e stato dello schema europeo EUCS, che quindi **non usiamo**.

### 2.4 Cosa prendiamo

- **Dalla Rekenkamer:** pubblicare sempre la **quota ignota**. Da noi è l'asse «incerto» e il residuo S6, mai imputato.
- **Dal Parlamento europeo:** la **lente capogruppo del vincitore**, per essere confrontabili. La teniamo come lente secondaria, con la tabella di incrocio verso la lente prodotto (§ 1.4).
- **Dal Bundestag:** separare **tetto** e **richiamato** nei contratti quadro. Da noi è lo strato S0, e i massimali si contano negli attuativi.
- **Dall'Assemblée nationale:** verificare a mano la nazionalità dei gruppi principali. Da noi lo fanno le tabelle curate in `config/` con la fonte di ogni riga.
- **Da Compass Lexecon (riferito):** il prodotto si riconosce dal testo. Da noi è la via del marchio (S4), misurata su campioni a cieco.
- **Dal Cloud Sovereignty Framework della Commissione** [V] (ac072d49): la regola **dell'anello più debole**. Il livello complessivo (SEAL, da 0 a 4) è il più basso fra gli otto obiettivi di sovranità. Coincide con la nostra regola: un servizio di un hyperscaler resta extra-UE chiunque lo rivenda.

### 2.5 Cosa evitiamo

1. **Classificare il vincitore come se fosse il prodotto.** È il limite dichiarato dallo studio del Parlamento europeo.
2. **Contare menzioni invece di euro**, come la quota di incidenza di Compass Lexecon.
3. **Sommare i massimali come spesa** (avvertenza del governo tedesco; da noi S0 e mancanza M4).
4. **Copiare il valore della gara su ogni vincitore** senza dichiarare come si deduplica. Da noi un CIG conta una volta (regola R53).
5. **Estrapolare da una quota di mercato stimata**, o chiamare risparmio un costo evitato. Se mai lo facessimo, lo marcheremmo come scenario [S].
6. **Usare un modello linguistico senza misurarne la precisione.** Da noi ogni regola e ogni livello ha un campione a seme fisso giudicato e pubblicato, e il modello esce solo con certezza alta.
7. **Usare cifre di seconda mano come fatti.** Tre cifre molto citate si sono rivelate non governative (Germania), di fonte ignota (Regno Unito, secondo il rapporto del 27/10) o ambigue nel perimetro (studio PE).

### 2.6 Scelte di compatibilità

- **CPV.** Pubblichiamo la lista bianca versionata e il suo effetto misurato ([Perimetro ICT](/progetto/perimetro-ict/)). Nessuno studio europeo letto pubblica una lista CPV di riferimento: la nostra si può riusare su TED o su altri dati nazionali.
- **Giurisdizione.** I nostri esiti sono IT, UE, sovrano non UE (Svizzera), extra-UE e incerto ([Criteri](/progetto/criteri-sovranita/#r-s3-esiti)). Per il confronto con lo studio del Parlamento europeo, che divide solo UE e non UE, IT e UE si sommano. Il sovrano non UE va dichiarato a parte, perché lì conterebbe come non UE.
- **Livelli SEAL.** Una corrispondenza indicativa fra i nostri esiti e i livelli SEAL è una **proposta per Fabio** [S], non adottata: per esempio extra-UE vicino a SEAL-0/1. Andrebbe dichiarata come stima dai dati di spesa, non come valutazione con il questionario del framework.
- **Qualificazione ACN.** Resta un asse di sicurezza, separato dalla giurisdizione (§ 2.3).
- **Dati e codice aperti.** Nessuno studio della tabella pubblica dati per contratto, codice e metriche di validazione insieme. Noi li pubblichiamo ([Mirror pubblico](/progetto/mirror-pubblico/), [Strumenti](/progetto/strumenti/)): è il nostro contributo riusabile.

**Nessun contatto con gli autori** è stato preso. I rapporti del 27/10 suggeriscono un elenco di controparti (autori dello studio PE, Open Contracting Partnership e altri): ogni contatto è una decisione di Fabio.

## 3. Fonti archiviate

Tutte acquisite il 19/11/2026 con `tools/archivia.py` (archivio append-only, indirizzato per contenuto). URL completi, date, sha256 e percorsi nel mirror: [`fonti-europee.csv`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/metodo/prove-design/fonti-europee.csv).

| fonte | sha256 |
|---|---|
| Synergy Research, comunicato 24/7/2025 | b5b502ea |
| Digital Dependence Index, pagina principale | d65560eb |
| Parlamento europeo, PE 778.576 (PDF) | 6429f4b5 |
| Bundestag, Drucksache 21/5413 (PDF) | 6401171c |
| Senato francese, rapporto n. 830 | e9cb3a0f |
| Assemblée nationale, rapporto n. 3054, tomo I (PDF) | 51435b16 |
| Cour des comptes, pagina della pubblicazione 22/10/2026 | bd053f38 |
| Algemene Rekenkamer, «Het Rijk in de cloud» | 9281ca1e |
| Rigsrevisionen, nota 1123/23 (PDF) | 30d9759d |
| EFK, rapporto 23740, sintesi (PDF) | e51991ce |
| AgID, comunicato del 29/5/2025 | eb4ae5c6 |
| Istat, comunicato «PA locale e ICT, anno 2022» | cb003399 |
| Corte dei conti, delibera 30/2024/G (PDF) | 713ea1ce |
| Commissione europea, Cloud Sovereignty Framework, guida all'attuazione (PDF) | ac072d49 |
| ACN, regolamento infrastrutture digitali e servizi cloud (PDF) | 577ec23b |

**Non raggiungibili (403, non aggirati):** comunicato e rapporto di Open Cloud Coalition; articolo di Computer Weekly. Sono registrati nel manifest come tentativi falliti.

## Registro delle revisioni

| data | versione | modifica |
|---|---|---|
| 2026-11-19 | 1.0 | prima versione (#48): sintesi del design con rimandi; confronto europeo dai rapporti del 27/10 con le fonti primarie riaperte e archiviate (15 [V], 2 [R] per 403); risolto il conflitto sulle note dello studio PE 778.576 (l'Annesso 1 esiste, perimetro ambiguo); corretta la testata della cifra tedesca (Stuttgarter Nachrichten); SEAL solo come proposta, EUCS e SecNumCloud non usati |
