# Revisione di sovranità delle convenzioni (#55)

Versione 0.1, 3/11/2026. Revisore di sovranità (agente), secondo la griglia di `incertezze.md` e le decisioni di Fabio del 29/10 e del 3/11/2026, comprese quelle comunicate in corso di revisione:

1. una catena che termina in **Svizzera** non è soggetta al CLOUD Act: è **sovrana**, con giurisdizione registrata come **CH**;
2. PSN è a controllo italiano, ma quando **rivende un servizio erogato direttamente dall'hyperscaler** (es. Azure erogato da Microsoft) l'erogatore giuridico è l'hyperscaler e la qualificazione è **extra-UE (USA)**. I servizi che PSN eroga in proprio seguono il controllo di PSN;
3. nessuna richiesta alla SEC e nessun uso di email: le catene che richiederebbero EDGAR restano **incerte**, con un'azione alternativa.

Metodo: ho lavorato solo sulle fonti archiviate (`archivio/manifest.jsonl`, testi in `lavoro/controllo/txt/` sul server), senza ricerche web nuove. Ho controllato con ricerche testuali ogni affermazione di `controllo-erogatori.md` sulla fonte citata. Una qualificazione è data solo se il **ruolo** e la **catena** di chi eroga sono entrambi certi su fonte; altrimenti l'esito è «incerto», con l'azione.

Esiti: **IT**, **UE**, **CH** (sovrano, decisione 1), **extra-UE**, **incerto**, **n.a.** (non è servizio cloud: licenza on-premise, hardware, servizi professionali su infrastruttura del cliente; si registra solo la lente fornitore e la dipendenza tecnologica).

## Tabella per servizio

| # | servizio | ruolo erogatore | erogatore | catena di controllo | periodo | esito | fonte che lo rende certo | azione se incerto |
|---|---|---|---|---|---|---|---|---|
| 1 | PSN (9066973ECE), servizi **Industry Standard** (infrastruttura PSN) | eroga a canone su infrastruttura propria | Polo Strategico Nazionale S.p.A. | soci TIM 45%, Leonardo 25%, CDP (tramite CDP Equity) 20%, Sogei 10% (certo); soggetto che controlla PSN non pubblicato; TIM→Poste dal 2/10/2026, CDP e Leonardo con MEF socio rilevante, Sogei non accertata | 2022-2026 | **incerto, con propensione IT**: tutti i soci noti sono italiani e nessun anello extra-UE emerge, ma il controllo di PSN (congiunto? patti?) e Sogei non sono documentati; TIM prima del 2025 non accertata | 5be1ea22301b (compagine e servizi Industry Standard qualificati ACN liv. 4) | N2 (bilancio Sogei), N3 (nota integrativa PSN, parti correlate e patti); poi chiudere IT. Fabio ha detto «PSN è a controllo italiano»: se lo assume come decisione, l'esito diventa IT (vedi decisioni) |
| 2 | PSN, **Hybrid / PSN Managed** (stack di terzi gestito da PSN, es. «PSN Managed Oracle») | PSN gestisce e eroga lo stack in proprio sulla sua infrastruttura (se così: segue PSN); se è infrastruttura del vendor, segue il vendor | PSN o vendor | come riga 1 | 2024-2026 | **incerto** | il bilancio 5be1ea22301b cita «PSN Managed Oracle» in qualificazione, non dice dove gira | Convenzione PSN e allegati (N4): chi gestisce l'infrastruttura del servizio Managed |
| 3 | PSN, **Secure Public Cloud** Azure e Google (AWS dal 2024-25) | servizio «erogato con Google e Azure»: per decisione 2, se rivenduto, erogatore giuridico è l'hyperscaler | Microsoft / Google / AWS | gruppi USA (catena non archiviata) | 2024-2026 | **extra-UE (USA) per decisione 2**, con riserva sul fatto: il bilancio non dice se PSN rivende il servizio dell'hyperscaler o lo eroga in proprio su region dedicate | 5be1ea22301b («servizi Secure Public Cloud erogati con Google e Azure»; «quarto CSP AWS») | N4: contratto/Convenzione PSN su chi è il fornitore verso la PA; quota di spesa (I3) dal bilancio 2026 |
| 4 | SPC Cloud L1 (55187486EA), IaaS/PaaS a canone | eroga a canone (RTI) | TIM mandataria; Enterprise Services Italia (gruppo DXC, riferito) con ruolo non accertato | TIM: Poste/MEF solo dal 15/12/2025-2/10/2026; prima non accertata; ESI→DXC non archiviata | 2016-2026 | **incerto** per tutte le annualità fino al 2025; per il 2026 **incerto** finché non è chiaro chi del RTI eroga (se solo TIM: IT dal 2/10/2026) | 59e9a310d64b, d20d92aee844 (TIM→Poste) | contratto quadro e ripartizione nel RTI; N5 (TIM 2016-2024: relazioni di governance TIM); N10 (bilancio depositato ESI, senza EDGAR) |
| 5 | SPC Cloud L1, PaaS SQL Server Microsoft | prodotto Microsoft gestito dal RTI | come riga 4 | come riga 4 | — | segue riga 4; Microsoft è **dipendenza tecnologica**, non erogatore, salvo prova di servizio Azure rivenduto | — | come riga 4 |
| 6 | SPC Cloud L3 (55193442C1), L4 (5519376D26) | servizi applicativi/professionali | RTI aggiudicatari | non analizzata | — | **n.a. / incerto per attuativo**: servizi professionali; cloud solo se un attuativo include hosting del fornitore | — | I11: aprire gli attuativi con hosting |
| 7 | SPC2 Connettività (5133642F61), connettività | non cloud | TIM, Fastweb, BT, Vodafone, Tiscali | — | — | **n.a.** (connettività) | — | — |
| 8 | SPC2, **IaaS community cloud** (se nel contratto) | eroga a canone | Tiscali / Fastweb / BT / Vodafone (da accertare chi) | Tiscali: Jefferies (USA) dal 19/4/2024; Fastweb: Swisscom, Confederazione 51%; Vodafone Italia: Swisscom dal 31/12/2024, fusa in Fastweb dal 1/1/2026; BT Italia: Retelit dal 1/10/2025 | per annualità | **incerto** (non è certo che l'IaaS sia nel contratto firmato). Se c'è: Tiscali **extra-UE (USA) dal 19/4/2024**, incerto prima (N16); Fastweb **CH** per tutto il periodo coperto dal rapporto Swisscom 2025, incerto prima; Vodafone **CH** dal 31/12/2024, incerto prima (N15); BT incerto (N14, N15) | ea8f180d5e97 (Jefferies), 7182b2549239 (Swisscom, Confederazione 51%, fusione 1/1/2026), 2f19bd5c22e8 (Retelit) | I6: contratto quadro firmato e atti con IaaS; poi N14-N16 |
| 9 | Sicurezza da remoto ID 2296 (88846293CA), **servizi a canone dai Centri Servizi**, quota PAL | eroga a canone da Centri Servizi del fornitore | RTI Accenture-Fastweb (chi gestisce i Centri Servizi non accertato) | Accenture plc (Irlanda, NYSE) – anello Accenture S.p.A. mancante; Fastweb: CH | 2022-2026 | **incerto**: se i Centri Servizi sono di Fastweb, **CH (sovrano)**; se di Accenture, incerto (N1 senza EDGAR, N18) | 7182b2549239; c19f8c647bba (solo capogruppo) | AQ firmato e capitolato: chi gestisce i Centri Servizi; per Accenture S.p.A. bilancio depositato (nota «direzione e coordinamento») invece di EDGAR |
| 10 | ID 2296, servizi a canone, quota PAC | eroga a canone | RTI TIM (mandanti non accertate) | TIM→Poste→(CDP+MEF) dal 2/10/2026; prima non accertata | dal 2/10/2026 / prima | **IT dal 2/10/2026 se TIM è l'unico erogatore dei Centri Servizi**: non è certo (mandanti ignote) → **incerto**; prima **incerto** (N5) | d20d92aee844, b7b47c1e5c40 | AQ firmato RTI TIM; N5 |
| 11 | ID 2296, **realizzazione / servizi professionali su infrastruttura dell'ente** | opera su infrastruttura del cliente | Accenture, Fastweb, TIM | irrilevante (griglia, punto 3) | — | **n.a.**: la sovranità segue l'infrastruttura dell'ente; lente fornitore | DECISIONI 3/11 | I2: separare canone e realizzazione negli attuativi (es. DAP 99026071D0) |
| 12 | Trenitalia → FSTechnology (7991036B82) | non accertato se eroga su infrastruttura propria o su Azure | FSTechnology S.p.A. | FS S.p.A., socio unico MEF (certo) | — | **incerto** (I7): catena IT certa, ruolo no; la parte su Azure MACC sarebbe extra-UE (Microsoft eroga direttamente) | 1c355d4f628f (FS «wholly owned by the State through the sole shareholder, the MEF»; FSTechnology controllata direttamente da FS); TED 139007-2023 (MACC) | quota dei servizi a Trenitalia su Azure vs data center propri: bilanci FSTechnology, avvisi TED |
| 13 | Microsoft EA6/EA8/EA9 (8335254532, 97431204F9, B1D4011AB2), **SaaS** (M365, Dynamics) e consumo Azure | Microsoft eroga direttamente | Microsoft (Microsoft Ireland Operations per l'UE) | gruppo Microsoft Corp. (USA): catena non archiviata | — | **extra-UE (USA)** per la quota SaaS/Azure (stesso principio della decisione 2), ma **quota incerta** (I8) | catena: nessuna fonte archiviata (il fatto è pacifico ma va archiviato) | archiviare l'annual report Microsoft da microsoft.com (non EDGAR); R23 transato per famiglia |
| 14 | Microsoft EA, **licenze on-premise** | licenza installata presso l'ente | — | — | — | **n.a.**: dipendenza tecnologica USA | DECISIONI 3/11 («licenze ≠ cloud») | — |
| 15 | Oracle multibrand 6 L1 (9660108D4B), licenze | licenza | RTI TIM-Eurolink (rivenditore) | — | — | **n.a.** per le licenze; **incerto** per A02A0C832A e B41CBAFA94 (possibile OCI/Oracle Analytics Cloud, che sarebbe extra-UE: Oracle eroga direttamente) | — | I9: atti DGSIA |
| 16 | Sanità digitale ID 2601 (98209074D6), **SaaS** | eroga in SaaS (prevista dalla consultazione) | Dedalus, GPI, Engineering (chi eroga cosa non accertato) | GPI: FM S.p.A. 60,571% (Manzana) + CDP Equity 23,820%: IT certo; Engineering: Centurion Newco, controllo congiunto NBRP/Bain, paese non accertato; Dedalus: non accertato | 2023-2026 | quota **GPI in SaaS su infrastruttura propria: IT** solo se si accerta l'infrastruttura (se gira su hyperscaler, segue l'hyperscaler) → **incerto**; Engineering e Dedalus **incerti** | 7c1317806ed2, 5b76558a1595 (GPI); 8464ec34091c, 52cfee1508f1 (Engineering) | I10: capitolato e contratti esecutivi (chi eroga, dove); N11, N12 |
| 17 | ID 2601, servizi professionali / on-premise | opera su infrastruttura dell'ente | come sopra | irrilevante | — | **n.a.** | DECISIONI 3/11 | — |
| 18 | Servizi applicativi ID 2212, 2483, 2610, 2365, 2366, 2536 | servizi professionali | RTI vari | irrilevante salvo hosting | — | **n.a.**; **incerto per attuativo** dove compaiono hosting, licenze cloud o canoni (I11: Roma Servizi Mobilità SAP S/4HANA Public Cloud → SAP eroga direttamente, catena SAP non archiviata; Sardegna IT canone PSN → segue righe 1-3) | — | I11 |
| 19 | System management 2/3/4 (7260902DDE, 893944468E, B2094754F1) | gestione su infrastruttura dell'ente | RTI vari | irrilevante | — | **n.a.**; **incerto** per gli 11 attuativi di ID 2275 con cloud/data center (I12) | — | I12: atti degli enti |
| 20 | Reti locali 8 L2 (9543706356), PC desktop (9823936871) | hardware/connettività | — | — | — | **n.a.** (dipendenza tecnologica Cisco, HPE, Juniper, Huawei) | — | — |
| 21 | Chromebook ID 2425 L3 (91580749BC) | hardware con Chrome OS | — | — | — | **n.a.** se nessuna licenza di gestione Google; altrimenti la console Google è servizio erogato da Google (extra-UE) | capitolato tecnico ID 2425 (approfondimento-incertezze-1) | I14: catalogo aggiudicato |
| 22 | Aruba (dove compare come erogatore) | eroga cloud/hosting | Aruba S.p.A. | titolare effettivo Giorgio Cecconi **al 2017** | — | **incerto** (dato vecchio di 9 anni) | fa911c4b3780 | N13 |
| 23 | I13 importi anomali | — | — | — | — | non è un tema di sovranità | — | — |

### Sintesi per il registro I1-I14

| # | esito del revisore |
|---|---|
| I1 | incerto; Fastweb sarebbe CH (sovrano), TIM IT solo dal 2/10/2026 e solo se unico erogatore; Accenture incerto |
| I2 | incerto (quota canone vs realizzazione); la realizzazione su infrastruttura dell'ente è n.a. |
| I3 | incerto (quote per famiglia) |
| I4 | catena PSN: incerto con propensione IT (controllo di PSN e Sogei mancanti) |
| I5 | incerto |
| I6 | incerto; per annualità vedi riga 8 |
| I7 | incerto (catena IT certa, ruolo no) |
| I8 | SaaS extra-UE; quota incerta |
| I9 | licenze n.a.; due attuativi incerti |
| I10 | incerto; GPI catena IT certa |
| I11, I12 | incerto per attuativo |
| I13 | fuori dal perimetro di sovranità |
| I14 | n.a. salvo licenze Google |

## Errori e debolezze in `controllo-erogatori.md` (verificati sulle fonti archiviate)

1. **Tiscali, fonti e quote**: la catena Jefferies → BEI Italia Wireless LLC → ShellNet → Tessellis è documentata **solo** in ea8f180d5e97 (relazione 2024, «detiene il 56,5%»). In e780a47eec4f (semestrale 30/6/2025) e 52ce9d63bd4c (comunicato 10/10/2025) **Jefferies non compare**; il 52ce9d63bd4c parla del socio «Shellnet S.A.p.A. di Shellnet GP srl», cioè una forma societaria diversa da ShellNet S.p.A. La quota «57,14%» non si trova in nessuna delle tre fonti. Il controllo Jefferies **dopo** la trasformazione in S.A.p.A. (2025) non è quindi dimostrato: va scritto «sì (fatto) dal 19/4/2024, da riverificare dopo la riorganizzazione ShellNet 2025».
2. **TIM, delisting**: la frase «la revoca dalla quotazione non scatta secondo il comunicato» non trova riscontro nel testo di d20d92aee844 (nessuna occorrenza di «quotazione» o «delisting»). Togliere o citare la fonte giusta.
3. **FSTechnology**: le citazioni «technology Service Provider, appointed to manage its ICT strategy» e la scissione del 5/8/2025 a favore di FS Security **non si trovano** in 1c355d4f628f con ricerca testuale. Si trovano invece: FS «wholly owned by the State through the sole shareholder, the MEF» e FSTechnology fra le società «directly controlled by FS SpA». Il ruolo di FSTechnology va quindi riscritto senza la citazione, o citando la pagina esatta.
4. **Swisscom**: la frase «Fastweb S.p.A. è una delle due "strategic subsidiaries"» non si trova come tale; il rapporto parla di «strategic subsidiaries» senza elencarle nel passaggio trovato. Restano certi: Confederazione 51%, acquisizione di Vodafone Italia il 31/12/2024, fusione legale il 1/1/2026, Fastweb S.p.A. come entità del gruppo. Il controllo di Fastweb da parte di Swisscom è certo nel 2025; per gli anni precedenti è riferito.
5. **Poste**: la scheda Consob (situazione all'8/10/2024) mostra CDP 35,000% e MEF 29,696% come azionisti distinti e qualifica CDP come controllata dal MEF. Che il **controllante ultimo sia il MEF** è una somma fatta dall'agente, non scritta nella fonte: andrebbe formulato «CDP e MEF, entrambi riconducibili al MEF» (fatto) senza dichiarare un controllo di diritto.
6. **Leonardo**: la «situazione al 10/3/2025» non è leggibile nel testo estratto della scheda Consob (si legge la data 04/03/2025 della dichiarazione Capital Research); il 30,204% del MEF è confermato da daecda0b64f5 e 129ffd4c0d96.
7. **Data di consultazione**: non è vero che tutte le fonti sono del 3/11/2026: il bilancio PSN 5be1ea22301b è stato acquisito il 30/10/2026.
8. **PSN, qualificazione SPC**: la fonte dice «Secure Public Cloud erogati con Google e Azure» e «servizi SPC Google e Azure»; il resto della lettura (I4, N4) è corretto. Va però aggiunto che la fonte cita anche il servizio «PSN Managed Oracle» in qualificazione (livello 3), assente dalla tabella.
9. **Ruolo nelle convenzioni**: l'impostazione è coerente con la griglia; la nota sulla priorità (accertare prima il ruolo) è condivisa.
10. **N1/N8**: superati dalle decisioni di Fabio (niente SEC; Svizzera sovrana). N1 va riscritto con l'azione alternativa (bilanci depositati, annual report dal sito della società).

Affermazioni verificate e corrette: compagine PSN 45/25/20/10 e CDP tramite CDP Equity; Poste 85,823% di TIM; Poste 27,315% al 15/12/2025 (Consob TIM); Accenture plc irlandese, azioni classe A al NYSE; Jefferies dal 19/4/2024 via BEI Italia Wireless e ShellNet 56,5% (ea8f180d5e97); Tiscali Italia «totalitariamente controllata da Tessellis»; Retelit completa l'acquisizione il 1/10/2025 con «our shareholder Asterion»; Aruba, titolare effettivo Cecconi al 16/11/2017; Engineering, controllante Centurion Newco, controllo congiunto NBRP e Bain Capital (2020), soci citati nel 2026; GPI, FM 60,571% (Manzana) e CDP Equity 23,820%, patto del 19/12/2025.

## Decisioni di metodo per Fabio

Già decise (3/11, applicate qui): catena svizzera = sovrana (CH); PSN che rivende un hyperscaler = erogatore l'hyperscaler, extra-UE; niente SEC né email.

Ancora aperte:

1. **PSN «a controllo italiano»**: le fonti archiviate danno soci tutti italiani ma non chi controlla PSN (né Sogei). Fabio lo assume come dato di metodo (allora le righe 1-2 diventano IT) o resta incerto fino a N2/N3?
2. **TIM prima del 2025**: la catena Vivendi/CDP non è documentata. Per le annualità 2020-2024 TIM resta incerta; serve decidere se cercare le fonti storiche (N5) o dichiarare la statistica 2020-2024 incerta per la quota TIM.
3. **Hybrid / PSN Managed** su stack di un vendor extra-UE: se lo stack gira su infrastruttura PSN gestita da PSN, è IT (decisione 29/10); se gira su region dell'hyperscaler gestita da PSN, chi è l'erogatore? Proposta: decide chi gestisce l'infrastruttura fisica e logica del servizio.
4. **Fondi di private equity** (Engineering: NBRP/Bain; Retelit: Asterion; Dedalus: Ardian/ADIA): in che modo si determina la giurisdizione di un controllo tramite fondi (sede del veicolo, del gestore, del GP)?
5. **Capogruppo UE quotata negli USA** (Accenture plc, Irlanda, NYSE): la sola quotazione/registrazione SEC basta a dire «extra-UE», o conta la catena societaria verso entità USA?
6. **Controllo indiretto USA di società italiana quotata** (Tiscali/Jefferies): basta il controllo indiretto documentato per «extra-UE (USA)», senza qualificazione giuridica sul §2713? Proposta: sì, è il caso tipo del CLOUD Act.
7. **Erogatore il cui SaaS gira su hyperscaler** (es. GPI o Dedalus su Azure): segue l'hyperscaler (coerente con decisione 2) o l'erogatore contrattuale?
8. **Catene che cambiano in corso d'anno**: attribuire l'annualità pro rata per giorni o secondo la catena alla data del contratto/fattura?

## Eccezioni e particolarità incontrate, con la regola proposta (per `criteri-sovranita.md`)

| particolarità | caso | regola proposta |
|---|---|---|
| catena che termina in uno Stato extra-UE non USA con adeguatezza UE | Fastweb, Vodafone Italia (Svizzera) | sovrano, giurisdizione registrata col codice del paese (CH); deciso da Fabio |
| intermediario sovrano che rivende un hyperscaler | PSN Secure Public Cloud | l'erogatore giuridico è chi eroga direttamente il servizio; extra-UE; deciso da Fabio |
| catena che cambia nel periodo | TIM (Poste dal 2/10/2026), Tiscali (Jefferies dal 19/4/2024), Vodafone (Swisscom dal 31/12/2024), BT (Retelit dal 1/10/2025) | qualificare per annualità; da decidere il criterio dentro l'anno (decisione 8) |
| fusione dell'erogatore | Vodafone Italia in Fastweb dal 1/1/2026 | la qualificazione segue l'entità risultante dalla data di efficacia |
| RTI con membri di catene diverse | ID 2296, SPC Cloud L1 | qualificare per membro che eroga il servizio a canone; senza ripartizione nel RTI, incerto |
| stessa convenzione con servizi a canone e servizi professionali | ID 2296, ID 2601, servizi applicativi | separare per servizio: canone → erogatore; realizzazione su infrastruttura dell'ente → n.a. |
| affidamento intragruppo | Trenitalia → FSTechnology | catena certa non basta: serve sapere su che infrastruttura eroga (DECISIONI 3/11) |
| licenze in convenzione con componente SaaS | Microsoft EA, Oracle | licenza on-premise n.a. (dipendenza); SaaS/consumo cloud extra-UE con erogatore il produttore |
| prodotto extra-UE gestito in proprio | SPC Cloud L1 con PaaS SQL Server, PSN Managed | segue chi gestisce; il prodotto è dipendenza tecnologica |
| hardware con possibile servizio di gestione del produttore | Chromebook (console Google) | n.a. salvo licenza di gestione cloud, che è servizio del produttore |
| controllo tramite fondi di investimento | Engineering, Retelit, Dedalus | incerto finché non c'è una regola (decisione 4) |
| capogruppo UE con quotazione USA | Accenture plc | incerto finché non c'è una regola (decisione 5) |
| dato di controllo datato | Aruba (2017) | un dato di catena vale solo per il periodo che la fonte attesta; oltre, incerto |
| fonte che documenta il controllo, fonti successive che non lo ripetono | Tiscali dopo la riorganizzazione ShellNet 2025 | la qualificazione vale fino alla data della fonte; si estende solo con una fonte successiva |
| catena ricostruibile solo da EDGAR | Accenture S.p.A., ESI/DXC | incerto; azione alternativa: bilancio depositato, annual report dal sito della società |
| soci tutti pubblici ma controllo non pubblicato | PSN | da decidere (decisione 1) |

## Registro delle revisioni

| versione | data | modifica |
|---|---|---|
| 0.1 | 3/11/2026 | prima revisione di sovranità; verifica di `controllo-erogatori.md` v0.1 sulle fonti archiviate |
