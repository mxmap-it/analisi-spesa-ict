> **Attenzione (3/11/2026):** la revisione di sovranità (`revisioni/sovranita-revisione.md`) ha trovato affermazioni non presenti nelle fonti citate: Tiscali/Jefferies dopo il 2025 e quota 57,14%; revoca della quotazione TIM; citazioni FSTechnology e scissione 5/8/2025; frase Swisscom su Fastweb; «controllante ultimo MEF» di Poste (somma fatta da noi, non scritta nella fonte); data della scheda Leonardo; data di acquisizione del bilancio PSN (30/10). Fino alla correzione queste righe valgono come **non accertate**. N1 e N8 superate dalle decisioni di Fabio del 3/11 (niente SEC; Svizzera sovrana).

# Catena di controllo degli erogatori (#55)

Versione 0.1, 3/11/2026. Rilevazione di un agente, **non ancora passata per la revisione avversariale** (DECISIONI 3/11/2026).

Criterio (Fabio, DECISIONI 29/10 e 3/11/2026): la sovranità dipende dal **controllo giuridico di chi eroga il servizio**, cioè dall'immunità rispetto al CLOUD Act e a normative extra-UE analoghe. Non contano il luogo dei data center né l'origine del software.

Regola: **non inferire**. In tabella c'è solo ciò che sta scritto in un documento archiviato (`archivio/manifest.jsonl`, sha256 qui sotto). Il resto è «non accertato», con l'azione per accertarlo nell'ultima sezione.

**Cosa non decide questa tabella.** Il valore «esposizione CLOUD Act» registra solo un fatto documentato: un controllante o una capogruppo con sede, quotazione o controllo negli USA (o in un altro paese extra-UE). Se una società italiana controllata ricada davvero nel CLOUD Act (18 U.S.C. §2713, «possession, custody, or control» di un fornitore soggetto alla giurisdizione USA) è una **qualificazione giuridica** che nessuna fonte archiviata contiene. Per questo la colonna distingue:
- **sì (fatto)**: catena con un soggetto USA documentata;
- **extra-UE non USA**: catena che termina fuori dall'UE ma non negli USA;
- **no (fatto)**: catena interamente italiana o UE, fino al controllante ultimo, documentata;
- **non accertato**: manca almeno un anello.

Data di consultazione di tutte le fonti: 3/11/2026 (campo `acquisito` del manifest).

## Tabella sintetica

| soggetto | controllante diretto | controllante ultimo | paese del controllante ultimo | quotazione | esposizione CLOUD Act / extra-UE | fonti (sha256, 12 caratteri) |
|---|---|---|---|---|---|---|
| Polo Strategico Nazionale S.p.A. | nessun socio di maggioranza: TIM 45%, Leonardo 25%, CDP Equity 20%, Sogei 10% | non accertato (patti parasociali e controllo congiunto non pubblicati) | Italia per tutti i soci, vedi sotto | no | non accertato a livello PSN; i soci risultano italiani a controllo pubblico (TIM via Poste; Leonardo, CDP via MEF); Sogei non accertata | 5be1ea22301b |
| TIM S.p.A. | Poste Italiane S.p.A., 85,823% del capitale dopo l'OPAS (regolamento 2/10/2026) | MEF, attraverso Poste (vedi riga sotto) | Italia | Euronext Milan; la revoca dalla quotazione non scatta secondo il comunicato | no (fatto, per la catena di controllo) | d20d92aee844, 59e9a310d64b |
| Poste Italiane S.p.A. (controllante di TIM) | CDP S.p.A. 35,000%, MEF 29,696% (Consob, situazione all'8/10/2024) | MEF; Consob qualifica CDP come «società controllata dal Ministero dell'Economia e delle Finanze» | Italia | Euronext Milan | no (fatto) | b7b47c1e5c40 |
| CDP Equity S.p.A. | Cassa Depositi e Prestiti S.p.A. (PSN: «attraverso la controllata CDP Equity») | MEF (Consob, scheda Poste) | Italia | no | no (fatto) | 5be1ea22301b, b7b47c1e5c40 |
| Leonardo S.p.A. | MEF 30,204% (Consob, situazione al 10/3/2025; confermato dalla lista MEF del 16/4/2026) | MEF, socio di maggioranza relativa; il controllo di diritto non è dichiarato nelle fonti | Italia | Euronext Milan | no per la catena di controllo; secondo azionista e flottante non analizzati | daecda0b64f5, 129ffd4c0d96 |
| Sogei S.p.A. | non accertato su fonte archiviata | non accertato | non accertato | no | non accertato | (nessuna: il PDF Consip «Consip e Sogei» non è più online) |
| Fastweb S.p.A. (dal 1/1/2026 fusa con Vodafone Italia S.p.A.) | Swisscom Ltd: Fastweb S.p.A. è una delle due «strategic subsidiaries» | Confederazione Svizzera, 51% del capitale di Swisscom | Svizzera (extra-UE) | Swisscom: SIX Swiss Exchange | **extra-UE non USA**: nessun anello USA documentato; l'esposizione al diritto svizzero è un fatto, la sua equivalenza al CLOUD Act non è accertata | 7182b2549239 |
| Vodafone Italia S.p.A. | dal 31/12/2024 Swisscom (acquisizione completata), poi fusa in Fastweb il 1/1/2026 | come sopra | Svizzera | — | extra-UE non USA dal 2025; prima (Vodafone Group plc, Regno Unito) non accertato su fonte archiviata | 7182b2549239 |
| Accenture S.p.A. (Italia) | non accertato (l'Exhibit 21 del 10-K non è stato archiviato, SEC risponde 403) | Accenture plc, Irlanda, azioni di classe A quotate al New York Stock Exchange, registrante presso la SEC (10-K esercizio al 31/8/2026) | Irlanda (UE) con quotazione e consistente presenza negli USA (es. Accenture LLP) | NYSE | **sì (fatto)**: capogruppo registrante SEC e quotata a New York, controllate USA; resta da accertare l'anello Accenture S.p.A. → capogruppo e la qualificazione giuridica | c19f8c647bba |
| Almaviva S.p.A. | non accertato | non accertato | non accertato | no (Almawave, controllata, revocata dalla quotazione: riferito, non archiviato) | non accertato; riferito da Business Wire 31/10/2024 (non archiviato, 403): Almaviva ha acquisito il 100% della statunitense Iteris. È una controllata USA, non un controllante USA | — |
| Enterprise Services Italia S.r.l. | non accertato (catena con DXC non documentata da fonte archiviata) | DXC Technology Company, Nevada/Ashburn (USA), secondo la scheda SEC: riferito, non archiviato | USA (riferito) | NYSE (riferito) | **non accertato** (l'anello ESI → DXC manca; se confermato, sì) | — |
| Tiscali Italia S.p.A. | Tessellis S.p.A., 100% («società totalitariamente controllata da Tessellis») | Jefferies Financial Group Inc. (USA): controllo indiretto dal 19/4/2024, tramite BEI Italia Wireless LLC → ShellNet S.p.A. (già OpNet; 56,5%-57,14% di Tessellis secondo la data) | USA | Tessellis: Euronext Milan; Jefferies: non archiviato | **sì (fatto) dal 19/4/2024**; prima (OpNet/Linkem 2022-2024) non accertato | ea8f180d5e97, e780a47eec4f, 52ce9d63bd4c |
| BT Italia S.p.A. / rami ceduti | ramo domestico e asset italiani ceduti a Retelit-X S.p.A. (100% Retelit) con closing al 1/10/2025 | Retelit: azionista Asterion (dal comunicato); paese e struttura di Asterion non accertati | non accertato | no | dal 1/10/2025 non accertato (Asterion); prima: BT Group plc (Regno Unito) non accertato su fonte archiviata | 2f19bd5c22e8 |
| FSTechnology S.p.A. | Ferrovie dello Stato Italiane S.p.A. («directly controlled by FS SpA») | MEF, «sole shareholder» di FS S.p.A. | Italia | no (FS emette obbligazioni EMTN) | no (fatto) per la catena di controllo; **come eroga** resta da accertare (vedi I7) | 1c355d4f628f |
| Aruba S.p.A. | non accertato | titolare effettivo Giorgio Cecconi **al 16/11/2017** (dichiarazione Consob di Aruba, a proposito di un'altra società) | Italia (al 2017) | no | no al 2017; dato attuale non accertato | fa911c4b3780 |
| Engineering Ingegneria Informatica S.p.A. | Centurion Newco S.p.A. («parent company», comunicato del 30/3/2026) | controllo congiunto NB Renaissance Partners (braccio italiano di Neuberger Berman) e Bain Capital Private Equity (accordo del 2020; i due fondi sono indicati come soci anche nel 2026) | non accertato nel documento; il gestore Neuberger Berman e Bain Capital non sono qualificati per paese nelle fonti archiviate | no | **non accertato**: i fondi sono comunemente noti come statunitensi, ma nessuna fonte archiviata lo dice e la qualificazione dei fondi (veicoli, sede, gestore) non è nota | 52cfee1508f1, 8464ec34091c |
| Dedalus (Dedalus Italia S.p.A. / Dedalus Holding) | non accertato | riferito dalla stampa: Ardian (Francia) maggioranza, quota di ADIA (Emirati); nessun documento primario archiviato | non accertato | no | non accertato | — |
| GPI S.p.A. | FM S.p.A., 60,571% dei diritti di voto («its parent company, FM S.p.A.») | Fausto Manzana (Consob indica Manzana come soggetto al vertice della catena); CDP Equity 23,820%; patto parasociale FM-CDP Equity firmato il 19/12/2025 | Italia | Euronext Milan | no (fatto) | 7c1317806ed2, 5b76558a1595 |

### Ruolo nelle convenzioni (griglia del revisore, Fabio 3/11/2026)

Il CLOUD Act riguarda chi **eroga direttamente** l'infrastruttura o il servizio cloud. Una società a controllo USA che fa consulenza o gestione su infrastruttura del cliente non rende la spesa non sovrana: si registra solo come lente fornitore. Qui si indica il ruolo solo se una fonte archiviata lo rende certo.

| soggetto | ruolo accertato | fonte | se non accertato, come accertarlo |
|---|---|---|---|
| Polo Strategico Nazionale | **erogatore a canone** di servizi infrastrutturali e applicativi in cloud alla PA (Convenzione con il DTD, agosto 2022). Una parte, il Secure Public Cloud, è erogata «con Google e Azure» (AWS in arrivo) | 5be1ea22301b | per l'SPC/hybrid resta da stabilire chi sia il fornitore giuridico verso la PA (N4) |
| FSTechnology | «technology Service Provider» del gruppo FS, incaricata della strategia ICT. Non risulta se per Trenitalia eroghi infrastruttura propria o gestisca servizi di terzi (Microsoft e Oracle sono in uso nel gruppo) | 1c355d4f628f | contratto 7991036B82 e relazione FSTechnology (I7) |
| TIM, Fastweb, Accenture, Almaviva, Enterprise Services Italia, Tiscali, BT Italia, Vodafone, Aruba, Engineering, Dedalus, GPI | **non accertato in questa rilevazione**: nessuna fonte archiviata qui descrive il loro ruolo dentro le singole convenzioni (ID 2296, SPC Cloud L1, SPC2, ID 2601) | — | capitolato tecnico e contratto quadro di ciascuna convenzione (ripartizione delle attività nel RTI, servizi a canone e servizi professionali); i dossier in `report/convenzioni/` vanno incrociati con questa tabella |

Nota sulla priorità: la catena di controllo pesa solo per chi risulta erogatore. Per Accenture, Enterprise Services Italia, Engineering e Tiscali conviene accertare **prima il ruolo** (capitolati) e solo dopo, se sono erogatori, chiudere N1, N10, N11 e N18.

La regola «due fonti» è stata sostituita (Fabio, 3/11/2026): basta una fonte che renda il fatto certo, senza forzature interpretative. Le righe sopra seguono già questo criterio.

### Variazioni 2020-2026 accertate

- **TIM**: Poste sale al 27,315% dei diritti di voto il 15/12/2025 (Consob); poi 85,823% del capitale con l'OPAS (risultati definitivi 29/9/2026, regolamento 2/10/2026). Prima del 2025 la catena (Vivendi, CDP) non è stata accertata su fonte archiviata. Per le statistiche 2020-2024, quindi, TIM resta «non accertato» sulla catena di controllo.
- **Fastweb e Vodafone Italia**: Fastweb è sotto Swisscom per tutto il periodo (riferito; il rapporto 2025 lo documenta per il 2025). Vodafone Italia passa a Swisscom a fine 2024 e si fonde con Fastweb il 1/1/2026.
- **Tiscali**: dal 19/4/2024 il controllo indiretto è di Jefferies (USA). Nel 2022-2024 il controllante (OpNet/Linkem) e la sua catena non sono accertati.
- **BT Italia**: i rami domestici passano a Retelit dal 1/10/2025.
- **GPI**: CDP Equity entra nel 2022 (patto del 22/6/2022 citato nel comunicato del 22/12/2025); nuovo patto dal 19/12/2025.

## Poteri speciali (golden power) e qualificazioni ACN

- **PSN, qualificazioni ACN** (bilancio 2024-25, sha256 5be1ea22301b): ad aprile 2024 PSN «ha qualificato i servizi Secure Public Cloud erogati con Google e Azure al livello 2», per dati fino al livello «critico». A maggio 2024 ha rinnovato le qualificazioni dell'infrastruttura per i dati «strategici». È inoltre prevista «l'introduzione del quarto Cloud Service Provider AWS». È un fatto rilevante per I4: una parte dei servizi PSN è erogata **con** hyperscaler USA. Chi eroga giuridicamente il servizio (PSN o l'hyperscaler) e con quali garanzie contrattuali contro il CLOUD Act non risulta dal bilancio: non accertato.
- **Swisscom/Vodafone Italia, golden power**: la stampa (Swisscom citata da più testate, 21/5/2024) riferisce un'approvazione senza prescrizioni. Il provvedimento PCM non è stato trovato e il comunicato Swisscom non è stato archiviato (marketscreener risponde 403): non accertato.
- **TIM/Poste, PSN, Tiscali/Jefferies, Engineering**: nessun provvedimento golden power trovato. Non accertato.
- Le **qualificazioni ACN** degli altri erogatori non sono state cercate in questa passata. Non accertato.

## FSTechnology: elementi per I7

Nella relazione finanziaria 2025 di FS (sha256 1c355d4f628f):
- FSTechnology è definita «the FS Group's technology Service Provider, appointed to manage its ICT strategy»;
- il 5/8/2025 è stato firmato l'atto di scissione parziale di FSTechnology a favore di FS Security;
- tra gli investimenti 2025 figurano «higher capitalisations … with specific regard to Microsoft's cloud services (+€23 million)»;
- i dati KPI sono estratti da «Oracle Cloud Enterprise».

Il gruppo FS usa dunque, documentalmente, servizi cloud Microsoft e Oracle. **Non** risulta quali servizi FSTechnology eroghi a Trenitalia con il contratto 7991036B82 né su quale infrastruttura: resta incerto.

## Non accertato e come accertarlo

| # | cosa manca | azione (in ordine di costo) | fonte risolutiva |
|---|---|---|---|
| N1 | Exhibit 21 di Accenture plc e di DXC Technology (elenco delle controllate: Accenture S.p.A., Enterprise Services Italia S.r.l.) | 1) archiviare da EDGAR con uno User-Agent che contenga un contatto email del progetto, come chiede la policy SEC (oggi `archivia.py` riceve 403 e nella stringa non c'è un'email: decisione di Fabio su quale indirizzo dichiarare); 2) in alternativa, bilancio depositato delle due società italiane (nota integrativa: «direzione e coordinamento», socio unico) | SEC EDGAR 10-K FY2026: `acn-20260831` ex. 21.1; `dxc-20260331` ex. 21 |
| N2 | Sogei → MEF | archiviare lo statuto o il bilancio Sogei dal sito sogei.it (Società trasparente) | bilancio Sogei 2025 |
| N3 | Controllo di PSN (congiunto? patti?) e golden power alla costituzione | 1) nota integrativa del bilancio PSN, sezione parti correlate e patti; 2) bilancio TIM 2025 (PSN consolidata o collegata?); 3) relazioni annuali PCM al Parlamento sul golden power 2022-2025 | bilancio TIM 2025; relazione golden power PCM |
| N4 | Ripartizione tra servizi PSN «industry standard» (erogati da PSN) e «Secure Public Cloud» / «hybrid» erogati con Google, Azure e AWS; garanzie contrattuali contro l'accesso extra-UE | 1) Convenzione PSN e allegati; 2) bilancio PSN 2026 (DECISIONI 3/11/2026, punto 3); 3) richiesta al DTD di pubblicare i piani dei fabbisogni (R20) | Convenzione PSN; bilancio 2026 |
| N5 | Catena TIM 2020-2024 (Vivendi, CDP) | archiviare gli snapshot storici Consob di TIM e le relazioni sul governo societario TIM 2020-2024 | Consob; relazioni di governance TIM |
| N6 | Quote attuali MEF/CDP in Poste dopo l'aumento di capitale al servizio dell'OPAS (5,544% di azioni nuove) | archiviare la scheda Consob aggiornata di Poste o la relazione sul governo societario 2026 | Consob |
| N7 | Swisscom/Vodafone: provvedimento golden power e prescrizioni | relazione PCM al Parlamento sull'esercizio dei poteri speciali 2024; comunicato Swisscom del 21/5/2024 dal sito swisscom.ch | PCM; swisscom.ch |
| N8 | Diritto svizzero equivalente al CLOUD Act per Fastweb | analisi giuridica (non è un fatto documentale): decide Fabio se una catena che termina in Svizzera, Stato terzo con decisione di adeguatezza UE, valga come «extra-UE» ai fini del bucket | decisione di metodo (Fabio) |
| N9 | Almaviva: controllante diretto e ultimo | bilancio consolidato Almaviva 2025 (il PDF «Gruppo Almaviva 2025» risponde con errore all'archiviazione); prospetto del bond 2030 alla Borsa del Lussemburgo | bilancio depositato; prospetto LuxSE |
| N10 | Enterprise Services Italia: socio unico e direzione e coordinamento | bilancio depositato (Registro imprese, a pagamento) o Exhibit 21 DXC (N1) | come N1 |
| N11 | Engineering: sede e natura dei fondi Bain Capital e NB Renaissance; Centurion Newco → Centurion Bidco → fondi | bilancio consolidato Engineering 2025 (nota sulle parti correlate e sulla controllante); documenti dei bond Engineering | bilancio Engineering 2025 |
| N12 | Dedalus: catena Ardian / ADIA e società italiane erogatrici | bilancio Dedalus Italia S.p.A. o comunicati Ardian archiviabili | bilancio depositato; ardian.com |
| N13 | Aruba: soci attuali (il dato 2017 è vecchio) | bilancio Aruba S.p.A. (nota integrativa) o visura | Registro imprese |
| N14 | Retelit / Asterion: paese e veicolo di controllo | sito Retelit (governance) e Asterion Industrial Partners | retelit.it; asterionindustrial.com |
| N15 | BT Italia ante 2025 e Vodafone Italia ante 2025: capogruppo nel Regno Unito | annual report BT Group plc e Vodafone Group plc (elenco delle controllate) | annual report |
| N16 | Tiscali 2022-2024: catena OpNet/Linkem prima di Jefferies | relazioni finanziarie Tessellis 2022 e 2023 | emarketstorage |
| N17 | Qualificazioni ACN degli erogatori diversi da PSN | catalogo ACN dei servizi cloud qualificati, archiviato per data | catalogo ACN |
| N18 | Qualificazione giuridica «soggetto al CLOUD Act» per le controllate italiane di gruppi USA (Tiscali/Jefferies, Accenture, DXC, eventualmente Engineering) | parere giuridico o riferimento a quadri esistenti (SecNumCloud 3.2 §19.6, EUCS): decisione di metodo di Fabio | — |

## Proposte di aggiornamento per `incertezze.md` (da approvare, il file non è stato toccato)

- **I1 (sicurezza da remoto 2296)**: Accenture ha capogruppo quotata al NYSE e registrante SEC (fatto, c19f8c647bba). L'anello Accenture S.p.A. → Accenture plc manca (N1). Fastweb è controllata da Swisscom, cioè dalla Confederazione Svizzera, extra-UE non USA (7182b2549239). TIM è controllata da Poste e quindi dal MEF (d20d92aee844, b7b47c1e5c40). Stato proposto: resta **incerto** per la quota PAL (Accenture: N1, N18; Fastweb: N8) e diventa **IT accertato sulla catena di controllo** per il RTI TIM, quota PAC, dal 2/10/2026. Per le annualità precedenti TIM resta incerta (N5), e restano da accertare le mandanti del RTI TIM.
- **I4 (PSN)**: compagine 45/25/20/10 accertata; TIM, Leonardo e CDP Equity sono italiani a controllo pubblico (MEF); Sogei non accertata (N2); controllo di PSN non accertato (N3). Fatto nuovo: servizi Secure Public Cloud «erogati con Google e Azure», AWS in arrivo (5be1ea22301b). Proposta: separare nel registro la riga «catena di controllo PSN» (quasi chiusa) dalla riga «chi eroga i servizi SPC/hybrid e con quali garanzie» (N4, aperta, dipende anche dal bilancio 2026).
- **I5 (SPC Cloud L1)**: TIM è italiana a controllo pubblico solo dal 2025-2026 (N5 per gli anni precedenti, rilevanti per un contratto del 2016). Per Enterprise Services Italia la catena con DXC (USA) è riferita ma non archiviata (N1, N10). Resta **incerto**.
- **I6 (SPC2 Connettività)**: Tiscali Italia è controllata indirettamente da Jefferies (USA) dal 19/4/2024 (ea8f180d5e97). Fastweb, compresa l'ex Vodafone, è svizzera. I rami domestici di BT Italia sono passati a Retelit dal 1/10/2025 (2f19bd5c22e8). Il controllo dipende quindi dall'anno: proposta di registrare la catena per annualità. Resta **incerto** (N8, N14, N15, N16) e resta aperto il dubbio sull'IaaS.
- **I7 (Trenitalia → FSTechnology)**: catena **IT accertata** (FS S.p.A., poi il MEF socio unico, 1c355d4f628f). Nuovo elemento: il gruppo capitalizza «Microsoft's cloud services» (+€23 mln nel 2025) e usa Oracle Cloud. Per il criterio del 3/11 (punto 2) resta **incerto** finché non si sa come FSTechnology eroghi i servizi del contratto 7991036B82.
- **I10 (Sanità digitale 2601)**: GPI è **IT accertata** (FM, cioè Manzana, più CDP Equity; 7c1317806ed2, 5b76558a1595). Engineering è controllata da Centurion Newco (fondi Bain Capital e NB Renaissance), con natura e paese dei fondi non accertati (N11). Dedalus non è accertata (N12). Resta **incerto**, ma per la quota GPI si può chiudere la catena.

## Ostacoli emersi (candidati per `richieste-e-raccomandazioni.yaml`)

- SEC EDGAR respinge (403) gli scaricamenti senza un contatto email nello User-Agent: per archiviare gli Exhibit 21 serve dichiarare un indirizzo del progetto.
- Le pagine Consob «Partecipazioni rilevanti» sono archiviabili, ma il loro aggiornamento è in ritardo rispetto ai fatti: per TIM, il 3/11/2026 la scheda era ferma al 18/12/2025 e non mostrava l'esito dell'OPAS.
- Non esiste un registro pubblico gratuito della catena di controllo delle società non quotate (Registro imprese a pagamento). Questo è il limite principale per ESI, Accenture S.p.A., Aruba, Almaviva e Dedalus.

## Registro delle revisioni

| versione | data | modifica |
|---|---|---|
| 0.1 | 3/11/2026 | prima rilevazione: 21 documenti archiviati, file di lavoro in `lavoro/controllo/` sul server |
