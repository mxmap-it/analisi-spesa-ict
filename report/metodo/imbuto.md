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
