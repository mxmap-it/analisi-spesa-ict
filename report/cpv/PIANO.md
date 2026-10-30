# Rapporto CPV: attendibilità, lacune del vocabolario, riclassificazione e proposta di policy

Stato: piano (30/10/2026, richiesta di Fabio). Ticket: vedi STATE.md. Pubblicazione solo con approvazione di Fabio.

## Obiettivo
Un rapporto finale che, su tutto ciò che noi classifichiamo come **cloud e infrastrutture IT**:
1. misura **quanto è sbagliato o inutile il CPV** dichiarato dagli enti (BDNCP/ANAC);
2. descrive le **mancanze del vocabolario CPV 2008** per misurare cloud e sovranità;
3. dice **chi** dovrebbe aggiornarlo e con quale procedura (Commissione UE – DG GROW, revisione del Reg. 2195/2002 / 213/2008; in Italia ANAC per i campi BDNCP, AgID/ACN per le tipizzazioni ICT);
4. propone una **riclassificazione** dei contratti con i nostri codici (tassonomia spesaict);
5. propone una **modifica di policy del procurement**: campi strutturati obbligatori su tipologia IT e caratteristiche di sovranità.

## Parti e metodo

### A. Letteratura (verificata, non da memoria)
Chi ha già misurato la qualità del CPV: Corte dei conti europea (relazioni speciali appalti), DIGIWHIST/Opentender, OCSE, Single Market Scoreboard, studi di classificazione testo→CPV (incluso il dataset Zenodo 10007545), eventuali studi nazionali. Per ciascuno: cosa misura (compilazione vs correttezza), su quali dati, risultato. Etichetta V/R.

### B. Misura sul nostro campione (risultato originale)
- Unità: i CIG classificati (campione 611, poi l'universo ICT del funnel), con verità di riferimento = classificazione umana o "alta" con precisione misurata ≥95%.
- Esiti per CIG, confrontando CPV dichiarato e oggetto reale:
  - **corretto-specifico**; **corretto-generico** (es. 72000000); **divisione sbagliata** (ICT dichiarato non ICT o viceversa); **non esprimibile** (nessun CPV distingue ciò che serve, es. SaaS vs on-prem, PSN vs hyperscaler).
- Metriche: tasso per esito con intervallo di Wilson 95%; precisione e richiamo del filtro "CPV ICT" (divisioni 30, 32, 48, 50.3, 64.2, 72) rispetto alla nostra classe ICT/cloud; quota di spesa (importo) mal codificata; distribuzione per tipo di ente e per stazione appaltante centrale vs locale.
- Su scala: confronto CPV dichiarato vs classificatore indipendente (EuroTender) sull'universo ANAC, come stima di larga scala da calibrare sul campione verificato.
- Riproducibile da `tools/verifiche/` (#47).

### C. Lacune del vocabolario
Mappa delle nostre categorie (cloud IaaS/PaaS/SaaS, PSN, housing/hosting, licenze, servizi professionali, connettività, datacenter interni) sui codici CPV esistenti: cosa non ha codice, cosa è ambiguo, cosa è indistinguibile. Nessun codice esprime prodotto, produttore, sede dei dati, giurisdizione dell'operatore.

### D. Riclassificazione
Ogni CIG ICT con: CPV dichiarato, CPV corretto proposto, classe spesaict (servizio, modello di erogazione), giurisdizione del prodotto e sovranità (criterio DECISIONI 29/10). Pubblicato come dataset aperto (`dati/classificazioni/`).

### E. Proposta di policy
- Campi strutturati obbligatori al CIG/contratto per acquisti ICT: tipologia (tassonomia controllata), modello cloud, prodotto/marca e produttore, sede dei dati, operatore e capogruppo, qualificazione ACN, esposizione a leggi extraterritoriali.
- Controllo di coerenza CPV↔oggetto al rilascio del CIG (ANAC).
- Proposta di aggiornamento del CPV (DG GROW) o, in attesa, di un vocabolario supplementare nazionale/UE per ICT e cloud.
- Collegamento con R16–R20.

## Dipendenze
Annotazioni umane (verità di riferimento), secondo giro via 6, dataset Zenodo ed EuroTender (da scaricare, ~300 MB + modello).
