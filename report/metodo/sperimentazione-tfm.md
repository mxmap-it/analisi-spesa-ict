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

## Esito della prova leggera del 19/11/2026

Prova **leggera**, non la 5×5 del protocollo: convalida incrociata stratificata 5 fold × 3 ripetizioni (seme 20261119), TabICL v2 (`tabicl` 2.2.0, checkpoint `tabicl-classifier-v2-20260212.ckpt`, 8 stimatori, CPU a 4 thread). Script `tools/sperimentazioni/tfm/prova_leggera.py` (comando in testa, venv separato `lavoro/tfm/.venv`), risultati completi con versioni e sha256 degli ingressi e dei pesi in `report/metodo/sperimentazioni/tfm-2026-11-19.json`. Le etichette sono annotate da Claude, come deciso da Fabio il 19/11/2026 (DECISIONI.md).

**Dati.** `e_cloud`: 1.728 CIG distinti (510 cloud, 1.218 non cloud) da campione v3 (611), via 6 sui gruppi G1/G3 (1.242) e revisione del 18/11 (273); 1.141 CIG sono del residuo S6. Dedup: prevale l'esito con fonte primaria, a parità il più recente (revisione > G1/G3 > v3); 291 CIG stanno in più file, con etichetta discorde solo in 3. Esclusi i 101 «?». Giurisdizione (IT/UE/EXTRA-UE): 1.039 CIG (396 / 49 / 594), dagli stessi esiti più i campioni a cieco 4-6 (351 CIG; se un CIG è in entrambi prevale la via 6). Caratteristiche: oggetto (skrub `StringEncoder`, 30 componenti, al posto di `TextEncoder` per non scaricare un modello linguistico), CPV a 2/3/5/8 cifre, log dell'importo, tipo di stazione appaltante (regola sul nome), stazione appaltante, primo aggiudicatario; nella variante «+regole» anche via, servizio, provider, giurisdizione delle regole e sottoclasse dell'imbuto.

**Risultati `e_cloud`** (media su 3 ripetizioni; «copertura» = quota di CIG con confidenza sopra la soglia che dà ≥ 95% di precisione, soglia scelta sulla ripetizione 1 e misurata sulle ripetizioni 2-3):

| via | macro-F1 | ECE | copertura a ≥95% (tutti / residuo S6) | precisione sopra soglia (tutti / S6) | tempo per fold |
|---|---|---|---|---|---|
| regole (passaggio 1) | 0,764 | – | – | accuratezza 0,806 | – |
| via 6 giro 1, solo testo (611 CIG v3) | 0,966 | – | – | – | – |
| revisione cieca Opus (267 CIG S6) | 0,950 | – | – | – | – |
| skrub + HGB | 0,864 | 0,056 | 78,6% / 87,0% | 0,947 / 0,968 | 2 s |
| skrub + HGB + regole | 0,894 | 0,043 | 85,5% / 91,3% | 0,954 / 0,967 | 2 s |
| TabICL | 0,884 | 0,015 | 86,0% / 92,2% | 0,952 / 0,973 | 96 s |
| **TabICL + regole** | **0,915** | **0,011** | **93,6% / 96,1%** | 0,954 / 0,969 | 112 s |

Deviazione standard fra ripetizioni ≤ 0,004 sul macro-F1. Complementarietà (McNemar sulla ripetizione 1, TabICL + regole): contro le regole il modello ha ragione da solo in 254 casi, le regole in 45 (p ≈ 10⁻³⁶); contro la via 6 giro 1 il modello ha ragione da solo in 13 casi, la via 6 in 61 (p ≈ 10⁻⁸, a favore della via 6); contro la revisione cieca 2 contro 7 (p = 0,18). Il modello **non intercetta errori che la via 6 non veda**.

**Risultati giurisdizione:** TabICL + regole macro-F1 0,861 (ECE 0,013) contro 0,923 delle regole (sui 459 CIG in cui le regole danno una giurisdizione) e 0,962 della via 6 giro 1; la classe UE (49 casi) resta debole (F1 0,76). Sul residuo S6 la precisione sopra soglia scende a 0,84: la soglia del 95% non regge.

**Costo:** 83 minuti per tutta la prova (60 addestramenti TabICL), picco di **11 GB di RAM**: va sotto il lucchetto dei job pesanti. HGB fa lo stesso lavoro in 2 secondi per fold.

**Criterio di decisione.** (a) Sulla carta è soddisfatto per `e_cloud`: a precisione ≥ regole, TabICL + regole deciderebbe da solo il 96% del residuo S6 con precisione 0,97, ben oltre il 30% richiesto. (b) Non è soddisfatto: nessun guadagno significativo contro la via 6 o la revisione. Per la giurisdizione nessuno dei due: resta fuori.

**Decisione proposta (proposta per Fabio, da approvare):**
1. **Giurisdizione: TabICL resta fuori.** Regole e via 6 sono migliori.
2. **`e_cloud`: niente ingresso nella pipeline come via che decide.** Il numero del 96% è misurato su etichette prodotte dalla stessa via 6 che dovrebbe sostituire, e su CIG già scelti per la via 6: dice solo che il modello imita bene la via 6, non che sia esatto. Si propone invece una **prova prospettica**: prima del prossimo giro della via 6 (livello L4 del raffinamento) si congelano le previsioni del modello sui CIG in coda, poi le si confronta con l'esito della via 6. Se la precisione resta ≥ 95% su CIG nuovi, il modello entra come **filtro di priorità** (ordina la coda e segnala i disaccordi), non come esclusione.
3. Per la prova prospettica basta **skrub + HGB + regole** (91% di copertura sul residuo S6, 2 s invece di 112 s, pochi MB invece di 11 GB). TabICL conviene solo se serve la sua calibrazione (ECE 0,011 contro 0,043), cioè se la probabilità deve diventare un livello di confidenza pubblicato.

**Limiti.**
- **Etichette non indipendenti:** tutte prodotte da Claude (via 6, revisione e campioni a cieco); nessuna annotazione umana. L'accuratezza è «accordo con la via 6», non verità.
- **Leakage:** la via 6 è insieme etichetta e via di confronto, quindi il confronto «via 6» è possibile solo con il giro 1 sul testo (campione v3) e con la revisione cieca. Le colonne delle regole (sottoclasse dell'imbuto) rivelano anche da quale file viene il CIG, e i file hanno quote di cloud diverse (50% nel v3, 19% in G1/G3). 77 CIG (4,5%) hanno lo stesso oggetto di un altro CIG (lotti della stessa gara) e possono cadere in fold diversi.
- **Campione piccolo e non casuale:** il residuo S6 etichettato sono i gruppi G1/G3 scelti per la via 6, non un campione del residuo; la classe UE ha 49 casi.
- **Soglia ottimistica:** scelta sulla ripetizione 1 e misurata sulle ripetizioni 2-3 degli stessi dati.
- Prova leggera: 5×3 invece di 5×5, `StringEncoder` invece di `TextEncoder`, nessun TabPFN, nessuna prova su `servizio`.

## Registro delle revisioni

| data | modifica |
|---|---|
| 2026-11-19 | esito della prova leggera (5 fold × 3 ripetizioni, `e_cloud` e giurisdizione): giurisdizione fuori; `e_cloud` criterio (a) soddisfatto solo sulla carta, proposta di prova prospettica come filtro di priorità (#56) |
| 2026-10-29 | protocollo approvato da Fabio (#56) |
