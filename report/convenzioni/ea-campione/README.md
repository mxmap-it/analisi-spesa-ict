# Campione EA Microsoft: quota cloud vs on-premise in euro (#55) — STATO PARZIALE

**Sintesi (3/11/2026, sessione 1, lavoro in corso):** dei 120 contratti del campione (`lavoro/ea-campione.csv`) **2 hanno l'atto letto**, 4 sono stati cercati per CIG senza esito, 114 non ancora cercati. **Nessuna stima di quota cloud per strato è ancora calcolabile**: zero contratti con carrello completo in euro. Nessun intervallo pubblicabile.

- MAECI B89CF8349C (EA9): importo ANAC 9.408.828,35 = atto 7.712.154,39 + IVA (**importo confermato**, V). Carrello solo con SKU e quantità: 8.000 utenti M365 E3 (cloud) + 128 core SQL Server Enterprise SA (on-premise). Euro per riga non pubblicati → tutto «non attribuibile» in euro; per quantità prevalenza cloud (R sulla ripartizione in euro).
- Regione Calabria B84589CB74 (EA9, 1.732.295,86, importo confermato, V): l'atto trovato (decreto 15468/2025) è una nomina; il carrello sta nel decreto di adesione dell'aprile 2024, non ancora trovato.
- Importi sospetti di C1 (Terna 48 M€, ANCI 45 M€, ASL Caserta 37 M€, ANAS 17,75 M€ ×2): **non verificati**. La ricerca web per CIG non restituisce atti per ANCI, ASL Caserta, ANAS; vanno cercati negli albi/trasparenza degli enti (passo successivo).

## Metodo
Confine R-S5 (vedi `../ea-quota-cloud-elaborazione.md` §1). Per ogni CIG: ricerca del CIG sul web, poi albo/amministrazione trasparente dell'ente; archiviazione con `tools/archivia.py` sul server (sha256 in `risultati.csv`); nessuna inferenza: senza carrello in euro, l'importo va in `euro_non_attribuibile`. Stime previste a lavoro finito: C1 esatto sui letti; C2/C3 bootstrap sulla quota per contratto; E = concordanza oggetto↔carrello con Wilson.

## Tabella
`risultati.csv` (120 righe, colonna `stato_ricerca`: atto letto / cercato, atto non trovato / non ancora cercato). Il file è il punto di ripresa.

## Limiti
- La ricerca web generica per CIG ha resa bassa (1 su 5 tentativi): i CIG compaiono nei PDF ma i motori indicizzano poco gli albi.
- Anche quando l'atto c'è, il carrello può avere SKU senza prezzi (MAECI): serve allora il listino EA9 per ripartire, che non è pubblico.

## Contratti senza carrello pubblicato (finora)
| cig | ente | perché l'atto online non basta |
|---|---|---|
| B89CF8349C | MAECI | SKU e quantità senza prezzi per riga |
| B84589CB74 | Regione Calabria | atto trovato è una nomina; adesione 2024 non ancora cercata (non è ancora candidato ad accesso civico) |

Accesso civico: solo come ultima risorsa, decisione di Fabio.
