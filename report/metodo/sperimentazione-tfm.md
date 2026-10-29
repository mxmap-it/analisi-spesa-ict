# Sperimentazione: modelli fondazionali tabulari (TabICL) come via di classificazione — protocollo

Stato: **approvata da Fabio** come valutazione empirica (29/10/2026, #56). Esito possibile: entra nella pipeline come via a sé, oppure resta fuori perché aggiunge complessità senza valore. Riferimento: https://www.probabl.ai/blog/demystifying-tfms (blog del produttore, non neutrale).

## Domanda
Un modello tabulare pre-addestrato (TabICL; TabPFN solo se la licenza lo consente), addestrato sui CIG già etichettati, porta **valore misurabile** rispetto a regole v3.x e modello linguistico (via 6)?

## Dati
- Caratteristiche: CPV (livelli 2-5), importo (log), tipo di stazione appaltante, aggiudicatari (codifica), oggetto (vettori di testo con skrub `TextEncoder`), esito delle regole (via, servizio, provider) come colonne opzionali.
- Etichette di riferimento: annotazioni umane alla cieca del campione v3 + CIG chiusi con fonte primaria (`verificati.jsonl`). Senza le annotazioni di Fabio si fa solo la prova tecnica.
- Obiettivi: `e_cloud`, `servizio`, giurisdizione (IT/UE/EXTRA-UE).

## Confronti
1. regole v3.x; 2. via 6 giro 1 (testo) e giro 2 (fonti); 3. baseline classica skrub `TableVectorizer` + HistGradientBoosting; 4. TabICL senza e con le colonne delle regole.

## Metriche (convalida incrociata stratificata ripetuta, 5×5)
- F1 per classe e macro-F1; precisione alla soglia di probabilità che dà ≥ 95% di precisione e relativa **copertura**;
- calibrazione (errore di calibrazione atteso, curva di affidabilità): la probabilità del modello deve poter diventare un livello di confidenza;
- tempo di calcolo e risorse sul server condiviso;
- **complementarietà**: matrice degli errori condivisi con regole e via 6, test di McNemar; guadagno dell'insieme; quota di CIG che non serve più mandare al modello linguistico.

## Criterio di decisione (da confermare con Fabio)
Entra nella pipeline solo se, a precisione ≥ regole, (a) riduce di ≥ 30% i CIG da mandare alla via 6, **oppure** (b) intercetta errori che le altre vie non vedono (McNemar p < 0,05), con calibrazione accettabile. Altrimenti resta fuori e l'esito si documenta nella metodologia.

## Riproducibilità
Script in `tools/sperimentazioni/tfm/`, versioni di librerie e pesi fissate, semi casuali dichiarati, risultati in `report/metodo/sperimentazioni/tfm-<data>.json`.
