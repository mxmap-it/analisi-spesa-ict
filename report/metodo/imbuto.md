# L'imbuto: disegno (2/11/2026, bozza da approvare con Fabio)

Obiettivo all'11/11:
- prime statistiche di sovranità sui contratti **dal 2024** facili da identificare;
- la **roadmap delle difficoltà**, con numeri di tutto ciò che resta incerto: quanti contratti, quanti euro, perché sono incerti e quanto può pesare.

## Universo e assi
- **Universo:** CIG ANAC **pubblicati dal 1/1/2020** (decisione di Fabio, 2/11). Si attendono due mondi da validare:
  - **2020-2023:** link ai documenti scarsi, quindi attendibilità complessiva più bassa e probabilmente solo un sottoinsieme di informazioni utili;
  - **dal 2024:** ciclo digitale, schede BDNCP e puntatori ai documenti.

  Il confine e la sua nettezza vanno misurati. La prima statistica pubblicata (11/11) è sul **2024 e oltre**. Il 2020-2023 entra come vista separata, con la sua attendibilità e l'elenco di ciò che manca.
- **Cifra di riferimento:** importo di aggiudicazione, altrimenti importo a base d'asta, dichiarato.
- **Vista per annualità** (prodotto obbligatorio). Per ogni anno dal 2020:
  - contratti ed euro in ogni strato;
  - fonti e livelli di acquisizione disponibili (dati strutturati, link, documenti);
  - quota con documento raggiungibile;
  - attendibilità complessiva dell'anno, cioè la quota di spesa decisa con confidenza alta e la forbice sul resto.
- **Asse A, è cloud o infrastruttura IT?** Escluso certo / incluso certo / incerto.
- **Asse B, giurisdizione e sovranità** (solo per gli inclusi): IT sovrano / UE / extra-UE / non determinabile / incerto.
- Ogni contratto porta lo **strato** che l'ha deciso e la **confidenza** (`spesaict.classificazione/1`).

## Strati (in ordine, ciascuno sul residuo del precedente)

| # | strato | regola | costo | confidenza attesa |
|---|---|---|---|---|
| S0 | perimetro | dal 2024; contratti annullati o duplicati fuori | zero | dato |
| S1 | esclusione certa non ICT | CPV non ICT **e** oggetto senza termini ICT **e** nessun lotto o convenzione ICT (più segnali concordi) | zero | alta, da misurare sul campione |
| S2 | soglia d'importo | **sotto 500 €** (Fabio, 2/11): fuori dalla misura ma conteggiati, con la quota di spesa esclusa riportata | zero | dato |
| S3 | inclusione certa da convenzione o lotto | contratto attuativo di un'iniziativa nota (AQ 2746 lotti, SPC Cloud lotto 1, PSN, Cloud Toscana…), che eredita prodotto e giurisdizione dalla base di conoscenza | zero | alta (salvo PSN: servizio da determinare) |
| S4 | inclusione certa da marchio univoco | prodotto nominato nell'oggetto (Microsoft 365, AWS, Azure, Google Workspace, Oracle Cloud, Aruba…), con le parole ambigue gestite | zero | alta o media, da misurare |
| S5 | ICT non cloud, incluse le infrastrutture in-house | hardware, datacenter interni, telefonia; **consulenza e servizi professionali IT riconducibili all'implementazione o gestione di infrastrutture in-house** (Fabio, 2/11). Distinguere: consulenza IT o non IT (organizzativa, legale, formazione); se IT, se infrastrutturale (in-house), di migrazione al cloud o applicativa. Conteggiato a parte nella voce «datacenter e infrastrutture interne» dell'obiettivo finale | zero (regole), via 6 per i casi dubbi | media, da misurare |
| S6 | residuo, in gruppi | **G1 mega** (sopra la soglia alta): a mano. **G2 informazione mancante ma significativi** (PSN senza piano dei fabbisogni, convenzioni non decifrate): documenti e richieste di pubblicazione. **G3 incerti significativi**: modello con ricerca degli atti (via 6). **G4 coda incerta sotto la media**: stima statistica dal campione | da token a FOIA | variabile |

## Prodotti per l'11/11
1. **Tabella dell'imbuto:** contratti ed euro per strato e per gruppo, dal 2024.
2. **Statistiche di sovranità** sugli inclusi certi (S3, S4, più la via 6 con confidenza alta): spesa per IT sovrano / UE / extra-UE, con intervallo dove la precisione è misurata.
3. **Roadmap delle difficoltà:** per ogni gruppo G1-G4:
   - quanti contratti ed euro;
   - perché sono incerti (manca il prodotto, PSN, RTI misti, atto irraggiungibile…);
   - quanto può pesare: forbice della quota extra-UE se il gruppo fosse tutto IT o tutto extra-UE;
   - metodo per risolverlo e costo;
   - chi deve agire (noi, enti, AgID, ANAC, DTD), con il collegamento alle raccomandazioni R16-R21.
4. **Top-5** delle cose da fare per la completezza.

## Misure di qualità
- Precisione di S1, S3 e S4 sul campione di 611 e sulle annotazioni (Wilson 95%). Finché non è misurata, la statistica si pubblica come «provvisoria».
- La **forbice** (minimo e massimo della quota extra-UE) è il modo onesto di mostrare quanto pesa l'incerto.

## SmartCIG e i due periodi (3/11/2026)

Spiegazione completa in `sito/content/progetto/evoluzione-dati.md`. In sintesi (V, file ANAC archiviati):
- SmartCIG non ha CPV, aggiudicatario né collegamento all'accordo quadro;
- 2020-2023: 4,4-4,7 milioni di contratti l'anno, 28-48 mld, con affidamenti sotto 40.000 €, difesa, servizi sociali e **in house**;
- dal 2024: solo affidamenti diretti piccolissimi (~1.500 € in media, 4,5-5 mld l'anno).

Effetti sull'imbuto:
- l'universo è CIG + SmartCIG;
- su SmartCIG si applicano solo l'esclusione dal testo, il marchio nel testo, l'in house come gruppo a sé e la stima da campione;
- il 2020-2023 senza SmartCIG non è confrontabile con il 2024 e oltre.

Profilo: `esiti/2026-11-03/smartcig/profilo.json`.

## Criticità: CIG ripetuti con strati diversi (R53, 9/11/2026)

Verifica ripetibile: `tools/verifiche/imbuto_cig_ripetuti.py` (`--mirror` sul server), esiti in `esiti/2026-11-09/imbuto/cig-ripetuti.json` e `cig-ripetuti.csv`. Dati [V].
- **Causa.** Nei file annuali ANAC 2024 e 2025 un CIG ha una riga per ogni CPV. Nel mirror 7.862 CIG hanno più righe (18.905 righe), nessuno sta in due file annuali, 510 hanno insieme un CPV ICT e uno non ICT. Non sono lotti né un join: anno, importo e testo sono identici fra le righe, cambia solo il CPV (982 CIG su 1.016 in `ict.csv`; gli altri 34 sono righe identiche).
- **In `ict.csv` (0.3.1, 3/11).** 671.540 righe, 669.878 CIG: 1.016 CIG ripetuti, 1.662 righe in eccesso. Dal 2024 in S3-S6 l'eccesso è di 1.509 righe e 2,565 mld (S3 1,216, S4 0,005, S5 1,065, S6 0,278).
- **Strati incoerenti.** 152 CIG ripetuti stanno insieme in S5 e in S6 «cpv-non-ict-testo-ict»: lo strato dipende dal CPV della riga tenuta, cioè dall'ordine del file. Con la prima riga (0.3.2) o con l'ultima (`imbuto_doppioni.py`) il risultato cambia.
- **Il 55,3 mld va corretto.** `imbuto_doppioni.py` ha tolto da S3-S6 2,99 mld invece di 2,565. Ha contato come eccesso anche le righe che la 0.3.1 metteva in S1 (285 CIG con una sola riga in `ict.csv`, 0,267 mld) e le copie in più di 87 CIG (0,159 mld). Il totale S3-S6 dal 2024 una riga per CIG è quindi **circa 55,7 mld** (+0,43 mld, quasi tutto S5). La cifra esatta si avrà alla rigenerazione, perché c'è da tener conto dei tetti.
- **La 0.3.2 perderebbe CIG ICT.** Tenendo la prima riga, 162 CIG oggi in S5 (0,345 mld) finirebbero in S1, perché la loro prima riga ha un CPV non ICT e il testo non ha segnali ICT (stima).
- **Regola (imbuto 0.3.4, `DEDUP_CPV` in `tools/analisi/imbuto.py`, si applica alla prossima rigenerazione, dopo la via 6).** Una riga per CIG e per fonte. Se il CIG ha almeno un CPV ICT, si classifica con il più basso dei suoi CPV ICT; altrimenti con la prima riga. Il risultato non dipende più dall'ordine del file, e un CIG che ha un CPV ICT resta nel perimetro.
- **Effetto stimato oggi sugli strati dal 2024**, rispetto all'ultima riga. In S3-S6 i CIG (291.213) e gli euro (110,77 mld lordi, prima dei tetti) non cambiano. Fra S6 e S5 si spostano 47 CIG e 23,2 M€. Rispetto alla 0.3.2 si spostano 84 CIG, più i 162 CIG recuperati da S1.
- **Elenco accesso civico (#58).** `elenco_mancanti.py` ora usa la stessa regola, mentre prima prendeva l'ultima riga. 65 CIG dell'elenco sono ripetuti. Per 32 (P2-g3 30, P5 2; 4,2 M€) con la regola 0.3.4 lo strato diventa S5: la nota della voce lo segnala, la priorità si rivede alla rigenerazione.
