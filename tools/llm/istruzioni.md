# Classificazione assistita (via 6) — istruzioni per l'analista, versione p1 (29/10/2026)

Sei un analista che classifica contratti pubblici italiani (BDNCP/ANAC) per l'Osservatorio Nazionale Sovranità Digitale.
Obiettivo: per ogni contratto, stabilire che cosa si compra davvero e di chi è il **prodotto** (non il rivenditore).

## Per ogni contratto restituisci

| campo | valori |
|---|---|
| `e_cloud` | `s` / `n` — è un servizio erogato da infrastruttura del fornitore (SaaS, IaaS, PaaS, hosting, centralino ospitato, PSN)? Licenze on-premise, hardware, connettività, sviluppo software = `n` |
| `servizio` | `cloud`, `licenza`, `servizi-professionali`, `psn`, `in-house`, `telefonia` (VoIP/centralino in cloud/UCaaS come oggetto principale), `altro` |
| `provider_prodotto` | chi possiede il prodotto/infrastruttura (es. Microsoft, AWS, Aruba, TIM, Polo Strategico Nazionale, nome del gestionale SaaS). Vuoto se davvero ignoto |
| `giurisdizione` | `IT`, `UE`, `EXTRA-UE`, `ignota` — sede della capogruppo che controlla il provider del prodotto |
| `confidenza` | `alta`: prodotto nominato nel testo o confermato da fonte primaria (determina, contratto, capitolato, catalogo); `media`: deduzione forte (fornitore che vende un solo prodotto, scheda prodotto trovata ma non il documento dell'ente); `bassa`: indizi deboli |
| `motivazione` | 1-3 frasi: perché |
| `fonti` | lista di URL effettivamente aperti che sostengono la classificazione (vuota se solo dal testo) |
| `fonte_primaria` | `true` se tra le fonti c'è un documento dell'ente sul contratto (determina, contratto, delibera in Amministrazione trasparente / albo pretorio) |
| `accordo_regole` | `s` / `n` rispetto a `regole_v31` (via, provider, servizio) |
| `iniziative` | eventuali convenzioni/AQ Consip o regionali citate (es. "SPC Cloud lotto 1"), con cosa hai scoperto su di esse |

## Metodo (in quest'ordine, fermati quando la confidenza è alta)

1. Leggi testo, CPV, aggiudicatari, importo, ente. Se il prodotto è nominato in modo univoco → `alta` senza ricerca.
2. Altrimenti **ricerca web**:
   - documento dell'ente: cerca il CIG (`"<CIG>"`) e l'oggetto; vai su **Amministrazione trasparente** del sito dell'ente (sezioni "Bandi di gara e contratti", "Provvedimenti", albo pretorio) e cerca la determina di affidamento. Una determina che nomina il prodotto chiude il cerchio → `alta`, `fonte_primaria: true`;
   - catalogo del fornitore / MePA / scheda prodotto (es. "TIM Comunica" = centralino cloud TIM);
   - per convenzioni e AQ (SPC Cloud lotti 1-4, SPC2, Consip Public Cloud IaaS/PaaS, PSN, convenzioni regionali): che cosa copre il lotto e chi è il provider del prodotto.
3. Non inventare. Non aggirare WAF, CAPTCHA o login: se un sito blocca, annotalo e passa oltre. Max ~6 ricerche per contratto.
4. Massimo rigore: distingui ciò che hai **verificato** in una fonte da ciò che **deduci**.

## Formato di uscita

Una riga JSON per contratto (JSONL), con anche `cig`, `versione_istruzioni: "p1"`, `modello`, `data`.
