# Via 6, secondo giro: verifica sulle fonti — istruzioni p2 (29/10/2026)

Valgono i campi e le definizioni di `istruzioni.md` (p1). Cambia il metodo: il primo giro ha classificato dal solo testo; questo giro **deve cercare le fonti**.

Leggi prima `report/metodo/llm/conoscenza-iniziative.yaml` (cosa significano SPC Cloud lotti 1-4, AQ 2213/2746, PSN, LAN 8, EA7…).

## Per ogni contratto (5 per pacchetto), obbligatorio

1. `WebSearch` del CIG tra virgolette (`"B1234ABCD"`), poi CIG + nome dell'ente.
2. Trova il sito istituzionale dell'ente e la sezione **Amministrazione trasparente → Bandi di gara e contratti / Provvedimenti** o l'albo pretorio; cerca la determina di affidamento (per CIG, oggetto, aggiudicatario, anno). Aprila con `WebFetch`.
3. Se non trovi l'atto: scheda prodotto/catalogo del fornitore, MePA, documenti della convenzione.
4. Almeno 2 ricerche e almeno 1 `WebFetch` per contratto prima di concludere. Massimo ~8 chiamate.

## Regole di confidenza (vincolanti)

- `alta` solo se: atto dell'ente aperto che nomina il prodotto (`fonte_primaria: true`), oppure prodotto nominato in modo univoco nel testo **e** confermato da una fonte aperta.
- Altrimenti `media` (deduzione forte) o `bassa`.
- `fonti`: solo URL **aperti con WebFetch** e pertinenti a **questo** CIG o a questo prodotto. Mai URL visti solo nei risultati di ricerca.
- Per i contratti con `controllo: true` (campione di controllo dell'alta confidenza) verifica comunque.

## Uscita

Una riga JSON per contratto in `report/metodo/llm/giro2/esiti/<pacchetto>.jsonl`, scritta appena finito il contratto (ripartibile: salta i CIG già presenti). Campi p1 più: `ricerche` (numero), `atto_ente` (URL della determina o ""), `cambia_rispetto_giro1` (s/n), `versione_istruzioni: "p2"`, `modello`, `data`.
Se un sito blocca (WAF, CAPTCHA, login) annota e passa oltre: non aggirare. Non contattare nessuno.
