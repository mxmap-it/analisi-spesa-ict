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
| 2026-10-26 | **Regola ristretta**: entrano solo le fonti che servono all'obiettivo finale, la spesa ICT e cloud per giurisdizione. Escono aiuti di Stato, INPS, AIFA, DAIT, NoiPA, Ministero della Salute e OpenCivitas | Fabio | Sostituisce la regola precedente: la spesa pubblica non ICT non serve all'obiettivo |
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

| 2026-10-26 | **La giurisdizione si attribuisce al prodotto, non al fornitore.** Due lenti separate: prodotto (dalla descrizione della gara) e fornitore (chi incassa). La rete dei rivenditori è un tema a sé | Fabio, su indicazione di Pietro Biase | Misurato su marzo 2026: le gare che nominano Microsoft 365, Azure, AWS e Google sono vinte dal produttore fra lo 0% e il 5% delle volte |
| 2026-10-26 | **Sottoinsieme prioritario: i fondi PNRR per il cloud** (Misura 1.2 e collegate): quanta parte è andata a prodotti delle big tech statunitensi | Fabio | Denaro pubblico destinato esplicitamente al cloud, e tracciabile per CUP |

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
| 2026-10-26 | **Il tetto vale a regime, non durante il setup**: fino al completamento di ANAC, che è il macro-obiettivo, si lavora senza tetto | Fabio | Oggi si costruisce |
| 2026-10-26 | Ogni lavoro è **legato a un ticket**; board di progetto nell'organizzazione | Fabio | — |

## Rapporti esterni

| Data | Decisione | Chi | Perché |
|---|---|---|---|
| 2026-10-26 | **AppaltIntel è commerciale: nessuna condivisione di metodo o lavorazioni.** Il loro documento interno resta riservato | Fabio | — |
| 2026-10-26 | Prima tornata di problemi da presentare **ad ANAC**, a stretto giro, attraverso contatti di Fabio | Fabio | — |
| 2026-09-23 | Il seme del registro delle giurisdizioni è il package di **aborruso**; proporgli di esternalizzare la lista in un file dati mantenuto da noi | Claude, da confermare con Fabio | Non partire da zero né in concorrenza |
| 2026-10-26 | **Cruscotto Italia di AgID: per ora lo lasciamo da parte.** Alla fine del percorso lo approfondiamo, ne raccogliamo ogni lezione appresa e lo usiamo per controvalidare i nostri risultati. Non è la base dell'analisi: niente fornitori, solo comuni, solo 12 mesi, dati aggregati | Fabio | Utile per controvalidare, non per misurare la giurisdizione |

## Comunicazione ad ANAC

| Data | Decisione | Chi | Perché |
|---|---|---|---|
| 2026-10-26 | A chiusura di ANAC: **sito aggiornato, un documento e una presentazione** per comunicare i problemi specifici | Fabio | — |
| 2026-10-26 | **Ogni problema ha un'azione correttiva e una metrica di non ricorrenza**: come risolverlo, e il controllo che dimostra che non si ripresenta | Fabio | Un problema senza soluzione proposta è una lamentela |
| 2026-10-26 | **Ogni affermazione è validata e controvalidata** per una via indipendente prima di uscire | Fabio | Evitare figuracce davanti all'autorità |

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
| 2026-10-28 | **Prima la misura cloud** (big tech USA, provider UE, provider italiani su datacenter propri) con la mappa dei rivenditori, PSN compreso; **in-house e datacenter propri dopo**, come punto aperto (#52) | Fabio | Chiudere bene una misura prima di aprirne un'altra |
| 2026-10-28 | Classificatore **robusto, riusabile e testabile**: funzione pura (`tools/analisi/classifica.py`), tabelle in `config/`, ogni errore trovato diventa un caso in `tests/casi_classifica.yaml` che non si toglie | Fabio, implementato da Claude | Rendere le regole verificabili da terzi e portabili ad altri strumenti |
| 2026-10-28 | Il metodo pubblicato dichiara **difficoltà, vie di analisi, verifica umana alla cieca a campione e raccomandazioni** per semplificare il monitoraggio | Fabio | Il metodo è parte del risultato |
| 2026-10-28 | Le righe lette per scrivere una versione delle regole diventano **campione di sviluppo**; ogni misura si fa su un campione nuovo che esclude tutti quelli già visti, con copia cieca per gli annotatori | Claude | Non misurare la precisione sulle righe usate per tararla |
| 2026-10-28 | **Registro unico delle richieste e raccomandazioni** (ANAC, Consip, PSN, Sogei, DTD, ACN) in `report/metodo/richieste-e-raccomandazioni.yaml`, aggiornato man mano | Fabio | Rendere l'analisi più facile e manutenibile e dare capacità di monitoraggio al DTD e ai progetti indipendenti |
| 2026-10-28 | **Codice nostro al minimo:** a fine lavoro il metodo si propone come miglioramento degli strumenti esistenti (anac-pl-pp-cli di aborruso, #22), almeno per la parte ben gestita e manutenibile | Fabio | Ridurre la manutenzione e ampliare la capacità di analisi di terzi |
| 2026-10-29 | **Cloud sovrano = controllo giuridico dell'operatore, non origine del software.** Un servizio con data center in Italia, gestito da un'azienda italiana a controllo italiano non soggetta al CLOUD Act (immunità giuridica sul modello SecNumCloud 3.2) è cloud sovrano (IT), anche se usa software extra-UE (es. Sistema Cloud Toscana con VMware/Microsoft). Il software extra-UE si registra come *dipendenza tecnologica*, campo separato. Da applicare caso per caso a PSN Managed / Hybrid (stack hyperscaler gestito da PSN) | Fabio | Distinguere il cloud sovrano dal cloud delle big tech USA, coerente con i quadri europei (SecNumCloud, EUCS) |
| 2026-10-29 | **Classificazione via 6 costi quel che costi**, con attendibilità, ripetibilità e basi dati; ogni ostacolo diventa raccomandazione di policy (#55) | Fabio | È il cuore della misura e deve diventare ripetibile ogni anno con meno sforzo |
| 2026-10-29 | **Artefatti intermedi riusabili da terzi:** dataset CIG → atti (URL, sha256, testo estratto) e registro di classificazione per CIG con tutti i passaggi (come, perché, con quali strumenti), in formato strutturato con schema, documentato nella metodologia e tenuto aggiornato. Anche le conversazioni con gli agenti si versionano in git | Fabio | Riprendibilità da terzi con altri software; trasparenza del metodo |

## Decisioni aperte, che spettano a Fabio

1. ~~Valore del tetto~~: 20% del settimanale su 7 giorni. Resta da tarare quanti token vale un punto percentuale (#20).
2. ~~Permesso per la board~~: fatto, board su https://github.com/orgs/mxmap-it/projects/1
3. Da dove servire il **mirror pubblico** (#17).
4. Quando contattare **DataCivicLab** (#21) e **aborruso** (#22).
5. L'**invio del rapporto ad ANAC** e a chi (#19).

- 2026-10-26 — Fabio — Tolte dal perimetro mef_irpef e pagopa: sono entrate, non spesa ICT.
- 2026-10-26 — Fabio — Regole di progetto per persone e agenti AI in AGENTS.md (CLAUDE.md rimanda lì), per permettere ad altri di unirsi con i propri agenti.
- 2026-10-27 — Fabio — La pipeline di verifica dev'essere ripetibile da zero da ANAC o tecnici terzi, come sotto-consegna documentata (#47); è criterio di chiusura di ANAC.
- 2026-10-27 — Fabio — Documento e presentazione per ANAC contengono una sezione «Come riprodurre tutto» con pochi comandi copiabili (#34, #35, #47).
- 2026-10-27 — Fabio — Il cloud provider si rileva con più processamenti differenziati (lotto di convenzione, lotto nel testo, marchio, PSN, fornitore-provider, modello linguistico, indeterminato), ciascuno documentato come metodo; ogni contratto porta la via di attribuzione (#48, #50).
- 2026-10-31 — Fabio — **Imbuto a strati con livelli di attendibilità** (anche da confronto con un esperto esterno):
  1. classificare il facile;
  2. escludere con certezza ciò che è ben classificato come altro;
  3. escludere gli importi troppo piccoli, con soglia documentata e quota di spesa esclusa misurata;
  4. raggruppare il residuo in gruppi da approfondire, ciascuno con il suo metodo: mega contratti a mano; significativi con informazione mancante (es. PSN) tramite documenti e richieste di pubblicazione; significativi ma incerti tramite modello linguistico più revisione;
  5. fondo del barile: lettura con AI dell'Amministrazione trasparente e accesso civico automatizzato.

  I buchi misurati diventano richieste di policy, per esempio la pubblicazione dei piani dei fabbisogni PSN da parte del DTD (R20).

  Riferito dall'esperto, da verificare: le classificazioni dei dati di spesa pubblica in UE «non superano il 40-50%»; EuroTender e Zenodo usati in pipeline per le esclusioni.
- 2026-11-02 — Fabio — Imbuto (`report/metodo/imbuto.md`):
  - **universo dai CIG pubblicati dal 2020**, con vista per annualità e attendibilità per anno. I mondi attesi, 2020-2023 e dal 2024, sono da validare misurando la disponibilità dei link ai documenti; per il 2020-2023 eventualmente solo un sottoinsieme utile. Prima statistica di sovranità (11/11) sul 2024 e oltre;
  - **soglia d'importo 500 €**;
  - in **S5** anche la **consulenza IT riconducibile a infrastrutture in-house**, distinguendo consulenza IT da non IT e, nell'IT, infrastrutturale, migrazione e applicativa.
- 2026-11-03 — Fabio — Convenzioni e accordi quadro (`config/iniziative_ict.yaml`):
  - **«verificato» richiede più fonti indipendenti** (almeno due, di cui una dell'ente che ha bandito la gara: Consip, PCM, ecc.). Una sola fonte, o solo l'avviso di un ente aderente che cita il CIG, resta «da verificare».
  - **Licenze ≠ cloud.** Il produttore extra-UE dà la giurisdizione, ma una licenza installata on-premise non è spesa cloud: per ogni convenzione di licenze (es. Microsoft EA) va accertato cosa contiene (licenze on-premise, abbonamenti SaaS come Microsoft 365, consumo Azure) e in che proporzione.
  - **Ogni convenzione grossa ha un dossier analitico** (`report/convenzioni/`): documenti originali archiviati con sha256, cosa abbiamo compreso, dettaglio analitico, limiti. Ogni dossier passa poi per un **agente avversariale** che cerca di smontarne le assunzioni; si pubblica solo ciò che regge.
- 2026-11-03 — Fabio — Chiarimenti sui casi aperti dalle revisioni dei dossier delle convenzioni:
  1. **L'hosting dedicato è cloud** (ospita servizi per conto dell'ente).
  2. **Affidamenti intragruppo o a società in house** (es. Trenitalia → FSTechnology): si contano solo quando si sa **che cosa usa l'affidatario e come eroga i servizi**. Se usasse un hyperscaler extra-UE (es. solo AWS) non sarebbe sovrano. Finché non lo sappiamo: **incerto**, con l'azione per accertarlo.
  3. **PSN:** il bilancio 2025 non basta, perché lo sviluppo principale avviene nel 2026; serve il **bilancio 2026**. Fino ad allora la ripartizione PSN resta incerta.
  4. **Sovranità = controllo giuridico di chi eroga il servizio** (criterio di immunizzazione giuridica, già deciso il 29/10/2026), non il luogo dei dati o dei data center e non l'origine del software. Un prodotto USA gestito e offerto come servizio da un soggetto italiano a controllo italiano, in Italia, non è soggetto al CLOUD Act ed è sovrano; il software extra-UE è una *dipendenza tecnologica* separata. Vale per la sicurezza da remoto ID 2296 e per tutti i casi analoghi: decide la **catena di controllo** del fornitore che eroga.
  5. **Non inferire.** Ciò che non è accertato su fonte si marca **incerto**, con le azioni per portarlo a certezza (registro `report/convenzioni/incertezze.md`).
- 2026-11-03 — Fabio — **Sostituisce la regola «verificato = due fonti indipendenti»** (stessa data): non servono due fonti archiviate, **basta esserne sicuri** su fonte, senza forzature interpretative. In cambio ogni qualificazione di sovranità passa **sempre per un agente di revisione** che stabilisce se la sovranità è qualificabile **in base alla catena di controllo di chi eroga il servizio cloud**, non in base all'origine del prodotto (un prodotto extra-UE può essere gestito in proprio in modo pienamente sovrano). Se il revisore non è sicuro, resta incerto con l'azione per accertarlo.
