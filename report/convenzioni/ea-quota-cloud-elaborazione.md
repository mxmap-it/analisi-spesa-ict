# Microsoft Enterprise Agreement e altre licenze Microsoft: come passare da «misto» a certo (3/11/2026, #55)

Misure **V** su imbuto 0.3.1 (`lavoro/imbuto/ict.csv`): contratti 2024-2025 di sottoclasse «licenza» con Microsoft nell'oggetto o come produttore attribuito (S3 convenzione + S4 marchio), esclusi gli importi ≥ 50 M€ «da verificare».

## Sintesi
- **611 M€ in 1.133 contratti.** Dall'oggetto: SaaS esplicito **88 M€** (175 contratti), on-premise esplicito **18 M€** (243), **generico 504 M€** (715, 482 enti).
- Il generico è **molto concentrato**: i primi 50 contratti fanno il 77 % del valore (soglia 1,5 M€), i primi 100 l'87 %, i primi 200 il 96 %. I 346 contratti sotto 40 k€ valgono 4,4 M€ in tutto.
- **Correzione rispetto all'approfondimento precedente** (`approfondimento-psn-ea.md` §2): i pesi di gara Consip (44 % EA6, 50 % EA9) **non** sono una stima centrale. La revisione avversariale (`revisioni/licenze-*.md` §1) li aveva già fatti cadere: sono coefficienti per lo sconto, e la Famiglia II contiene anch'essa prodotti cloud. Al più 0,44 è un **limite inferiore** per EA6. Inoltre la stima «on-premise esplicito 92 M€» contava come on-premise anche «rinnovo» e «manutenzione», che possono essere abbonamenti M365: con un criterio più stretto l'on-premise esplicito scende a 18 M€.
- **Proposta:** censimento dei primi 50 contratti generici e campione casuale stratificato del resto, letti fino al dettaglio SKU. Le vie «induttive» servono solo come forbice provvisoria, dichiarata come tale.

## 1. Perché l'oggetto non basta
Il CIG registra l'adesione («licenze Microsoft», «adesione EA9»), non il carrello. Il carrello (SKU, quantità, prezzi) sta nella determina dell'ente o nel suo allegato, e nell'ordinativo su acquistinretepa (non accessibile nel rispetto del robots.txt). La quota cloud vera è un fatto **per contratto**: va letta, non dedotta.

Confine da applicare nella lettura (R-S5): «cloud» = abbonamento a un servizio erogato da Microsoft (M365, O365, Dynamics 365, EMS/Intune, Copilot, Azure). Licenze perpetue, Software Assurance e subscription di prodotti installati presso l'ente (Windows Server, SQL Server, CAL, CIS Suite) = on-premise. M365 E3 resta cloud anche se include il diritto di installare Office: il servizio (posta, Teams, OneDrive, identità) lo eroga Microsoft.

## 2. Le vie possibili

### A. Lettura dei contratti (deduttiva, porta a «certo»)
Per ogni contratto letto si ottiene la quota cloud in euro dal carrello. Esito certo per quel contratto; la quota aggregata si stima sul resto.

**Disegno proposto:**
| strato | contratti | M€ | lettura | perché |
|---|---|---|---|---|
| C1: generico ≥ 1,5 M€ (top 50) | 50 | ~388 (77 %) | **censimento**, tutti | il valore è qui; ogni contratto letto passa a certo |
| C2: generico 200 k€–1,5 M€ | ~165 | ~97 | campione casuale **30** | stima della quota con errore misurabile |
| C3: generico < 200 k€ | ~500 | ~19 | campione casuale **20** | serve a sapere se i piccoli enti comprano diversamente (es. solo M365) |
| esplicito SaaS / on-premise | 418 | 106 | controllo a campione **20** | misura quanto è affidabile la parola nell'oggetto |

Errore atteso: con C1 letto per intero, l'incertezza residua riguarda solo il ~23 % del valore. Se nel campione di 30 la quota cloud fosse (per esempio) 80 % con dispersione ampia fra contratti, l'intervallo al 95 % su C2 sarebbe circa ±15 punti. Pesato sul 19 % del valore, sposta il totale di ±3 punti. **Il totale verrebbe noto con un margine di pochi punti, e per il 77 % in modo certo.**

Costo: ~120 contratti da cercare. Dall'esperienza sui dossier, la determina con il carrello si trova online per una parte degli enti (Calabria, ART, ARPA Piemonte, MAECI, Archivi notarili sì; molti altri danno solo l'importo). Per quelli non trovati: **accesso civico mirato**, con decisione di Fabio (stessa logica dei progetti PSN, `psn-progetti-campione.md`).

Avvertenze: alcuni dei primi 50 vanno verificati prima come importi (ASL Caserta 37 M€, ANCI 45 M€, Terna 48 M€ sono valori sospetti di massimale o di contratto pluriennale: regola unica sugli importi anomali, incertezza I13).

### B. Vie induttive (forbice provvisoria, mai «certo»)
| via | base | cosa dà | limite |
|---|---|---|---|
| B1. Pesi di gara Consip | chiarimenti EA6 (0,44), EA9 (0,50) | **minimo** per EA6 | non sono spesa; la Famiglia II contiene cloud (revisione avversariale) |
| B2. Oggetti espliciti | 88 M€ SaaS contro 18 M€ on-premise | 83 % SaaS fra gli espliciti | chi scrive il prodotto non è un campione casuale (chi compra M365 lo scrive più spesso) |
| B3. Ordini con SKU letti finora | Calabria, ART, ARPA Piemonte (96 %), MAECI, Archivi notarili | prevalenza SaaS | 5 enti, auto-selezionati: indicazione, non stima |
| B4. Transato Consip per famiglia | raccomandazione R23 | quota aggregata vera per EA | non pubblico; dipende da Consip |
| B5. Rapporti di Microsoft | quota cloud dei ricavi | contesto | globale, non PA italiana: non usabile |

**Forbice provvisoria proposta per il generico (504 M€), finché A non è fatta:** da 44 % (minimo da B1) a 100 %, con l'indicazione di B2-B3 che la realtà sta verso l'alto. Non si pubblica un valore centrale.

## 3. Raccomandazione
1. **Subito:** forbice 44-100 % sul generico nell'imbuto; SaaS esplicito = cloud extra-UE certo (88 M€); on-premise esplicito = licenze (18 M€).
2. **Lettura dei contratti C1** (50, 77 % del valore): ricerca degli atti come per il PSN; ogni contratto letto passa a certo.
3. **Campioni C2-C3 e controllo degli espliciti** (70 contratti).
4. In parallelo **R23 a Consip** (decisione di Fabio): chiude il dato per tutte le edizioni EA in una volta.
5. Gli enti che non pubblicano il carrello vanno nella lista per l'accesso civico, insieme ai progetti PSN.

## 4. Aggiornamento del 6/11/2026: primo censimento degli atti (#66, imbuto 0.7)

Fonte: `tools/verifiche/ea_censimento.py`, atti in `esiti/2026-11-06/imbuto/ea-campione.csv` (URL e sha256). Confine R-S5 del § 1.

- **C1, i primi 50 EA per importo:**
  - 1 atto letto su 50: MAECI, EA9, 9,41 M€ con IVA. Il carrello è M365 E3 per 8.000 utenti più CIS Suite, SQL Server e RDS CAL; quota cloud ~92 %, stimata con i prezzi unitari EA8 di un altro atto [V-quantità, prezzi da EA02];
  - per gli altri 49 non è stato trovato in rete nessun atto con il carrello. Le vie tentate sono le ricerche per ente e oggetto (10); i link PVL portano alla home delle piattaforme.
- **Atti trovati per edizione (EA7-EA9), di enti più piccoli:** 7 con il dettaglio dei prodotti, 6 con i prezzi unitari dell'ordinativo. Le quote cloud sono 92, 100, 100, 100, 57, 100 e 100 %.
- **Campione complessivo:**
  - 8 atti, quota pesata **92 %**;
  - 8 su 8 a prevalenza cloud: intervallo di Wilson **68-100 %**.
- **Forbice aggiornata:**
  - sul generico, cioè il residuo Microsoft incerto di 819 M€ in imbuto 0.7, si passa dal **44-100 %** della raccomandazione 1 al **68-100 %**, cioè **0,55-0,81 mld cloud extra-UE**;
  - è una forbice provvisoria: il campione non è casuale (atti trovabili in rete, enti piccoli e autorità). La sua distorsione possibile va verso il cloud, se i grandi enti, che non pubblicano il carrello, comprano più licenze on premises;
  - la raccomandazione 2 (lettura di C1) resta aperta, con 49 contratti; restano anche R23 e R54.
