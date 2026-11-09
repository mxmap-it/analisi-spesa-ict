# Registro delle decisioni

Una riga per decisione, con data, chi l'ha presa e perché. Le decisioni non si ridiscutono senza
un fatto nuovo; se una cambia, si aggiunge una riga nuova che la sostituisce, non si cancella la
vecchia.

**Ultimo aggiornamento:** 2026-11-06

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
- 2026-11-03 — Fabio — **Conta anche che cosa fa l'erogatore.** L'esposizione al CLOUD Act (e normative extra-UE analoghe) riguarda chi **eroga direttamente l'infrastruttura o il servizio cloud** e quindi detiene o controlla i dati. Una società a controllo extra-UE che fa **consulenza o servizi professionali** (progettazione, migrazione, gestione) **su infrastruttura del cliente** non porta la spesa fuori dalla sovranità: la sovranità segue chi gestisce l'infrastruttura. Il revisore di sovranità valuta quindi, per ogni servizio: (a) ruolo dell'erogatore (eroga il servizio cloud / opera su infrastruttura del cliente o di terzi); (b) catena di controllo di chi eroga e gestisce l'infrastruttura; (c) l'origine del prodotto solo come dipendenza tecnologica.
- 2026-11-03 — Fabio — **Criteri di sovranità in un documento dedicato** della metodologia (`sito/content/progetto/criteri-sovranita.md`): sintesi, regole, eccezioni, cosa porta a incertezza; aperto a critiche (issue con etichetta `criteri-sovranita`) e aggiornato a ogni nuova eccezione. Inoltre:
  - **Svizzera = sovrana** (non soggetta al CLOUD Act); si registra il paese CH;
  - **PSN rivenditore di servizi hyperscaler**: se il servizio è erogato da Microsoft/Google/AWS/Oracle il controllo è dell'hyperscaler (extra-UE); i servizi erogati da PSN in proprio seguono il controllo italiano di PSN;
  - **niente richieste alla SEC** che richiedano di dichiarare un'email: le catene che ne dipendono restano incerte con un'azione alternativa.

## 2026-11-03 — Accesso civico solo come ultima risorsa; database dei documenti PSN; lettura dei contratti Microsoft (Fabio, #55)
- **Accesso civico** (PSN, DTD, enti): solo come **ultima risorsa**, documentato e giustificato come compromesso. Prima si raccoglie tutto ciò che è pubblicato.
- **PSN:** si costruisce un database ampio dei **piani dei fabbisogni** inviati dagli enti e dei **Progetti** inviati dal PSN, con ricerca estesa per parole chiave ricavate dai documenti già trovati. Scopo doppio: misurare quanto è ottenibile da fonti pubbliche e dimostrare che questi documenti sono già pubblicati spontaneamente, per prevenire dinieghi. Analisi avversariale dei possibili motivi di diniego (d.lgs. 33/2013 art. 5-bis, clausola di confidenzialità, sicurezza).
- **Licenze Microsoft:** sì alla lettura dei contratti (censimento dei primi 50 con oggetto generico, campioni casuali del resto, controllo degli espliciti).
- **No** alla forbice provvisoria 44-100 % nell'imbuto per ora.

## 2026-11-03 — Amministrazione trasparente: robots.txt e anti-bot non bloccano la raccolta (Fabio, #55)
- **Base:** art. 9 c. 1 d.lgs. 33/2013 (verificato su Normattiva il 3/11/2026). Le amministrazioni «non possono disporre filtri e altre soluzioni tecniche atte ad impedire ai motori di ricerca web di indicizzare ed effettuare ricerche all'interno della sezione "Amministrazione trasparente"».
- **Regola:** sulle sezioni obbligatorie robots.txt non vincola. Contro le protezioni anti-bot sono ammessi un client da browser identificato e un ritmo basso. Restano esclusi la soluzione di CAPTCHA, la rotazione di IP o proxy e l'accesso ad aree riservate.
- **Ogni blocco è un'evidenza di violazione** da registrare e segnalare come raccomandazione. L'accesso civico resta solo per il dato che sul sito non c'è.
- **Perché:** la catena è sito → (solo se assente) accesso civico. Un blocco tecnico non equivale a «dato assente».
- Regola operativa in AGENTS.md §3.

## 2026-11-03 — Monitor dell'accessibilità di «Amministrazione trasparente» (Fabio, #61)
- **Byproduct deciso:** software autonomo e rieseguibile che censisce tutte le PA (registro ANAC art. 1 c. 32 L. 190/2012 + IndicePA) e misura se la sezione AT è indicizzabile (art. 9 c. 1 d.lgs. 33/2013), riconoscendo anche la piattaforma del portale (serve al dimensionamento dello scraping).
- **Pubblicazione nominativa: sì.** Open data con esito per ente (CSV + JSON, schema documentato, CC BY 4.0), una versione datata per giro mai sovrascritta più un «ultimo»; dashboard sul sito che legge l'open data (nessun numero copiato a mano), con ricerca, filtri per esito/tipo/regione/piattaforma e serie storica fra giri.
- **PEC:** saranno inviate da Fabio, non dagli agenti. Il modulo prepara le PEC (testo + allegati con sha256) e tiene un registro append-only degli eventi (invio, accettazione, consegna, risposta); la dashboard mostra lo stato degli invii e il giro successivo misura la risoluzione. L'invio automatico, se mai, va autorizzato a parte.
- **Architettura:** modulo separabile (`tools/trasparenza/`: README, METODO con versione e registro delle revisioni, schema, test, comando unico, licenza EUPL-1.2), senza dipendenze dal resto del repo salvo `requests` (e `playwright` facoltativo). Diventerà un progetto con GitHub e pagina propri; per ora è una sezione del sito (`/progetto/trasparenza-accessibilita/`).
- **Perché:** la catena sito → accesso civico richiede che il sito sia consultabile; un blocco tecnico è una violazione da misurare nel tempo, non un «dato assente».

## 2026-11-05 — Convenzioni ICT: carenze di trasparenza e accesso civico come rimedio di breve periodo (Fabio, #62)
- **Carenze in evidenza:** per ogni iniziativa e in sintesi per tipo di soggetto, la sezione `/convenzioni/` mostra cosa non viene pubblicato pur servendo a controllare spesa e sovranità (classi C1-C8 in `report/convenzioni/database/carenze.yaml`), con la base normativa o, se manca un obbligo, la ragione. «Verificato» = assenza constatata sulla pagina ufficiale con data; il resto è «da verificare».
- **Accesso civico generalizzato (art. 5 c. 2 d.lgs. 33/2013) come rimedio di breve periodo per carenze di policy.** È coerente con la regola del 3/11 («ultima risorsa»): si usa solo per dati che abbiamo cercato sulle fonti ufficiali e che le politiche di pubblicazione non prevedono, quindi non sono reperibili altrove. Le bozze con assenza ancora «da verificare» portano l'avviso di verificarla prima dell'invio.
- **Richieste minime** costruite sull'analisi avversariale dei dinieghi (`report/convenzioni/accesso-civico/analisi-dinieghi.md`): sezioni dell'offerta invece dell'offerta integrale, estrazioni già esistenti invece di elaborazioni, oscuramenti accettati.
- **Nessun invio:** le istanze le invia Fabio; registro `report/convenzioni/accesso-civico/registro.csv` (preparata / inviata / risposta / esito) mostrato sul sito; formato `spesaict.istanza/1` riusabile dal futuro sistema di invii massivi.
- **Rimedio strutturale:** una proposta di policy per classe di carenza (R08, R37-R42), così da non dover più ricorrere all'accesso civico.
- **Criterio del censimento:** iniziative ICT con CIG derivati dal 2024 (o nuove), quote per tipo di soggetto, soglie fuori Consip (3 derivati, 1 M€); storiche segnalate a parte (README della base dati).

## 2026-11-06 — Copie dei documenti delle convenzioni: repository pubblico con GitHub Release, non LFS (Fabio approva il repo; scelta Release verificata da Claude, #62)

- Fabio ha approvato un repository GitHub **pubblico** dedicato, `mxmap-it/convenzioni-ict-documenti`, per le copie dei documenti archiviati (~1.770 file, ~4,7 GB per iniziativa; 1.447 file distinti, 4,1 GB).
- **Release, non Git LFS.** Fatti dalla documentazione GitHub consultata il 6/11/2026:
  - LFS (docs.github.com, «About storage and bandwidth usage»): GitHub Free e Free for organizations hanno **10 GiB di spazio e 10 GiB di banda** LFS; la banda dei download, anche di terzi su repo pubblici, **conta sul proprietario**; superata la banda senza metodo di pagamento LFS si **disattiva fino al mese dopo**; superato lo spazio non si possono più caricare file (i cloni ricevono solo i puntatori). Con 4,1 GB, bastano 2-3 download completi al mese per bloccare tutto, oppure si paga.
  - Release (docs.github.com, «About releases»): ogni file **sotto 2 GiB**, **fino a 1.000 asset per release**, **nessun limite** sulla dimensione totale né sulla banda.
  - Quindi: una release per iniziativa (max 1.000 file; la più grande ne ha meno), nessun file oltre 2 GiB. GitHub espone il digest sha256 di ogni asset: verifica completa senza riscaricare.
- Il repo contiene solo README, licenza CC0 del manifest e `manifest.csv/json`; i documenti restano delle amministrazioni (riuso ex art. 7 d.lgs. 33/2013 e art. 52 CAD, citando la fonte). Esclusi: fonti non ufficiali e materiali interni (es. PDF Proteggimi, che comunque non è nell'archivio delle convenzioni).
- Caricamento dal portatile (il token GitHub non si porta sul server), con i blob copiati dal server.

## 2026-11-06 — DECISIONE (approvata da Fabio il 7/11/2026, «andiamo avanti su tutto»): destinatario dell'accesso civico per le gare Consip su delega (#62)

Stato: **approvata** come regola di instradamento; nessuna istanza inviata (ogni invio resta da approvare). Casi: ID 1774 SIAN (AGEA, `consip-1774`) e ID 2748 INAIL (`cig-B2FB115279`): in BDNCP la stazione
appaltante del CIG padre è l'ente, la pagina con i documenti è su consip.it (Consip centrale di committenza su delega).

- **Norma.** Art. 5 c. 3 d.lgs. 33/2013: l'istanza si presenta «all'ufficio che detiene i dati, le informazioni o i documenti» (in alternativa
  all'URP o all'ufficio indicato in AT); art. 5 c. 2: il diritto vale verso il soggetto che detiene il documento. Linee guida ANAC del. 1309/2016
  §5 e circolare FP 2/2017 §3: l'amministrazione che riceve un'istanza per documenti che non detiene la trasmette a quella che li detiene [R:
  testi da riarchiviare con sha256 prima dell'invio]. Il d.lgs. 36/2023 (art. 62-63) separa la fase di affidamento, svolta dalla centrale
  delegata, dall'esecuzione, che resta all'ente stipulante [R].
- **Atti** [V]: le pagine consip.it delle due gare pubblicano bando, disciplinare, capitolato e aggiudicazione a nome di Consip; il contratto
  si stipula fra ente e aggiudicatario (schema di contratto/AQ fra i documenti di gara).
- **Proposta di instradamento** (implementata in `tools/convenzioni/documenti_mancanti.py`, funzione `detentore`):
  - documenti della procedura (offerte, allegati di gara, verbali, aggiudicazione, chiarimenti) → **Consip** (bozza `mancanti-consip-s-p-a`);
  - atti di esecuzione (contratto stipulato, ordinativi/contratti esecutivi, flussi di monitoraggio, piani dei fabbisogni, proroghe e modifiche,
    listini applicati) → **ente delegante** (bozze `mancanti-agenzia-per-le-erogazioni-in-agricoltura`, `mancanti-istituto-nazionale-…`);
  - nei casi dubbi istanza a Consip con richiesta esplicita di trasmissione all'ente ex art. 5 c. 3 se non detiene il documento.
- Da decidere: approvare l'instradamento; se inviare a entrambi in parallelo per i documenti dubbi.

## 2026-11-07 — RUP: niente accesso civico ad ANAC (Fabio)
I RUP servono solo per i CIG da notificare e si raccolgono con due metodi:
1. navigazione web sulla pagina ANAC che indicherà Fabio, in Chrome vero, a ritmo basso, con gli eventuali CAPTCHA risolti a mano da Fabio;
2. analisi degli atti.

Il metodo è in visibilita-pa `METODO-RUP.md`. La bozza `anac-incaricati-bdncp` è annullata e non cancellata. R47 resta come raccomandazione (dato pubblico senza open data e dietro CAPTCHA), non come istanza. Il prototipo si fa con Fabio.

## 2026-11-07 — Via 6 su G1 e G3 «ad oltranza» (Fabio)
Il giro su G1 (196 CIG) e sui primi 1.000 di G3 continua senza lo stop sul totale, prima fissato a 360 USD-eq +20 %, perché «ci serve conoscenza». Resta il tetto giornaliero del giro. Lo stop si ripristina con `IMBUTO_STOP=1` (`tools/llm/imbuto_budget.py`). Approvato anche il costo di G1, circa 140 USD-eq.

## 2026-11-07 — Perimetro CPV: 79342 fuori, RX_ICT più largo, 3224 rinviato (Fabio, #44)
- **79342 marketing:** tolto da `CPV_ICT` (`tools/analisi/classifica.py`) e da `config/perimetro_cpv.yaml`. Prima c'è stata la review delle descrizioni: campione stratificato per importo, con tutti i CIG sopra 1 M€. Risultato: 3,0 % di ICT veri stimati, nessuno sopra 1 M€, tutti recuperati dal testo. Effetto: 5.706 CIG e 539 M€ dal 2024 passano in S1.
- **3224 telecamere/TV:** resta in lista. La review dà 79 % di videosorveglianza e 2,4 % di ICT stretto. Proposta: una sottoclasse «videosorveglianza» in S5, fuori dalla misura cloud. Decide Fabio.
- **RX_ICT:** aggiunti «sw» e «connettività» (imbuto 0.3.3). Effetto calcolato a parte: 3.593 CIG in più nel residuo S6, 4,1 mld, di cui 29 G1 per 3,8 mld. `ict.csv` si rigenera quando la via 6 sarà finita.
- Prove in `tools/verifiche/perimetro_cpv_effetto.py`, `esiti/2026-11-06/cpv/perimetro-effetto.json` e `report/cpv/review-79342-3224/`.

## 2026-11-09 — Accesso civico: destinatario = PEC istituzionale (protocollo)
**Chi:** Fabio. **Decisione:** le istanze di accesso civico generalizzato si inviano via PEC alla casella istituzionale dell ente (protocollo informatico / URP, da IndicePA), indirizzandole nel testo all ufficio preposto (ufficio che detiene i dati, art. 5 c. 3 d.lgs. 33/2013). Non serve individuare la PEC dedicata né il nome dell RPCT per l invio.
**Perché:** semplicità e robustezza: la PEC istituzionale è sempre presente in IndicePA ed è canale valido di presentazione; lo smistamento interno spetta all ente.
**Effetti:** il giro rpct_destinatari.py serve solo per (a) i 434 enti senza PEC in IndicePA, (b) RPCT come destinatario del riesame, (c) registro degli accessi e moduli online come contesto. Il nome RPCT resta campo C, non usato per l invio.
