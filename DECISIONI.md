# Registro delle decisioni

Una riga per decisione, con data, chi l'ha presa e perché. Le decisioni non si ridiscutono senza
un fatto nuovo; se una cambia, si aggiunge una riga nuova che la sostituisce, non si cancella la
vecchia.

**Ultimo aggiornamento:** 2026-10-26

## Obiettivo e perimetro

| Data | Decisione | Chi | Perché |
|---|---|---|---|
| 2026-09-23 | L'obiettivo è la spesa ICT della PA **per giurisdizione del fornitore**, con i quattro bucket di mxmap.it (`it`, `eu_non_it`, `extra_eu`, `unknown`) | Fabio | È il secondo asse dell'Osservatorio, accanto alla posta |
| 2026-10-26 | L'obiettivo si restringe alla spesa in **servizi cloud esterni e datacenter/infrastrutture interne**: quanto in totale e quanto a fornitori nazionali, europei e big tech statunitensi. **Nessun altro obiettivo di analisi** | Fabio | È la spesa che incide sulla sovranità |
| 2026-10-26 | L'analisi della spesa deve essere un **processo ripetibile**: anni passati, anno in corso, anni futuri | Fabio | Va aggiornata, non rifatta |
| 2026-10-26 | Sei obiettivi in quest'ordine: mirror · disponibilità e integrità · stato per ente nel tempo · rendiconti con evidenze · strumenti · **spesa ICT, per ultima** | Fabio | Non si misura la spesa su dati di cui non si conoscono i buchi |
| 2026-10-26 | Nel mirror entrano **solo fonti che riguardano, direttamente o indirettamente, la spesa pubblica** | Fabio | Estendere DataCivicLab non significa ereditarne il perimetro |
| 2026-10-26 | **Prima ANAC, fino in fondo.** Poi la roadmap con tutti gli altri dataset mappati | Fabio | Concentrazione; ANAC è la spina dorsale |

## Mirror

| Data | Decisione | Chi | Perché |
|---|---|---|---|
| 2026-10-26 | ANAC **in tutti i formati** (CSV, JSON, TTL) e **da tutte le fonti** | Fabio | Poter confermare e approfondire i rendiconti |
| 2026-10-26 | **Anche l'OCDS bulk**, nonostante i 90 GB: l'archivio per contenuto fa collassare i mesi duplicati, e il risparmio diventa una misura pubblicabile | Fabio (opzione 1) | Sostituisce la proposta di escluderlo |
| 2026-10-26 | **Niente Wayback Machine e nessun recupero retroattivo**: ciò che è sparito si registra come perduto | Fabio | File grandi, copertura casuale |
| 2026-10-26 | Archivio **append-only, indirizzato per contenuto** (`sha256`), con una vista che replica i percorsi originali | Claude, approvato | Prova di cosa era pubblicato e quando; usabile da altri cambiando solo l'URL base |
| 2026-10-26 | Il mirror si ferma se lo spazio libero scende sotto **40 GB** | Claude | Sullo stesso server gira la produzione di mxmap.it |
| 2026-10-26 | Dati **sul VPS di mxmap.it per ora**, forse una macchina dedicata in seguito. Layout trasferibile con un `rsync` | Fabio | — |
| 2026-10-26 | SIOPE: via principale il bulk di `siope.it`; **anche la via BDAP va specchiata e confrontata** | Claude, su domanda di Fabio | Il difetto di BDAP è riferito da AgID, non verificato da noi |

## Lavoro e strumenti

| Data | Decisione | Chi | Perché |
|---|---|---|---|
| 2026-10-26 | **Ricostruzione da zero** nel repository `mxmap-it/analisi-spesa-ict`, pubblico | Fabio | — |
| 2026-10-26 | Tutto il lavoro gira **sul server di mxmap.it**, con l'account `mxmap.it` e il Claude installato lì | Fabio | Job lunghi e ripartibili; ANAC respinge gli user-agent non-browser |
| 2026-10-26 | Push dal server con una **deploy key dedicata** a questo repository | Fabio | La chiave esistente era già legata a un altro repository |
| 2026-10-26 | Prima del codice, l'**analisi di strumenti e dataset nel README**, con le strade scartate | Fabio | Ora spostata in un documento a parte |
| 2026-10-26 | **Riusare il più possibile e scrivere meno codice possibile**; estendere DataCivicLab, ma prima costruire il nostro | Fabio | Il codice non scritto non va mantenuto |
| 2026-09-23 | **Qualunque licenza libera va bene**, si mescola tutto; fuori solo il non libero e i repo senza licenza | Fabio | Rilasciamo tutto |
| 2026-09-23 | Il backend di Biase **non si riusa** | Claude, condiviso | Licenza non commerciale; classificatore che si addestra sulle proprie predizioni |
| 2026-10-26 | **Tetto di sforzo in token al giorno**, non in tempo | Fabio | — |
| 2026-10-26 | Il tetto è **il 20% del limite settimanale dell'account, diviso per 7 giorni**: 2,86% al giorno. Conta il lavoro interattivo e quello automatico | Fabio | Il limite è condiviso con gli altri progetti |
| 2026-10-26 | Ogni lavoro è **legato a un ticket**; board di progetto nell'organizzazione | Fabio | — |

## Rapporti esterni

| Data | Decisione | Chi | Perché |
|---|---|---|---|
| 2026-10-26 | **AppaltIntel è commerciale: nessuna condivisione di metodo o lavorazioni.** Il loro documento interno resta riservato | Fabio | — |
| 2026-10-26 | Prima tornata di problemi da presentare **ad ANAC**, a stretto giro, attraverso contatti di Fabio | Fabio | — |
| 2026-09-23 | Il seme del registro delle giurisdizioni è il package di **aborruso**; proporgli di esternalizzare la lista in un file dati mantenuto da noi | Claude, da confermare con Fabio | Non partire da zero né in concorrenza |

## Sito

| Data | Decisione | Chi | Perché |
|---|---|---|---|
| 2026-10-26 | Sito su **analisi-spesa-ict.mxmap.it**, GitHub Pages dalla cartella `docs/` di `main` | Fabio | — |
| 2026-10-26 | **Stesso framework, layout e grafica di osservatorio.mxmap.it** (Hugo, Bootstrap Italia) | Fabio | — |
| 2026-10-26 | Sito **conciso**, home **centrata sulla spesa ICT** anche se esce per ultima, **meno sezioni**, nessuna barra con la citazione di Microsoft | Fabio | La prima versione era troppo lunga |
| 2026-10-26 | I rendiconti si **pubblicano man mano**, non a lavoro finito | Fabio | — |

## Metodo

| Data | Decisione | Chi | Perché |
|---|---|---|---|
| 2026-10-26 | **Separare sempre ciò che abbiamo verificato noi da ciò che riportiamo da altri** | Claude, dopo l'errore su BDAP | Avevo scritto come fatto un difetto di BDAP riferito da AgID, e un blocco degli IP cloud riferito da DataCivicLab |
| 2026-10-26 | Un conteggio anomalo non è sempre un errore: si classifica come **errore, incongruenza, convenzione o assenza di schema** | Claude | I codici `CFAVCP-…` e le partite IVA estere sembravano errori e non lo erano |

## Decisioni aperte, che spettano a Fabio

1. ~~Valore del tetto~~: 20% del settimanale su 7 giorni. Resta da tarare quanti token vale un punto percentuale (#20).
2. ~~Permesso per la board~~: fatto, board su https://github.com/orgs/mxmap-it/projects/1
3. Da dove servire il **mirror pubblico** (#17).
4. Quando contattare **DataCivicLab** (#21) e **aborruso** (#22).
5. L'**invio del rapporto ad ANAC** e a chi (#19).
