# Sistema Cloud Toscana (SCT) - chi fa cosa nel RTI

Contratto quadro Regione Toscana, CIG 7154112FF8, stipulato il 30/09/2019 (Rep. 8788). Gara indetta con decreto 11103 del 26/07/2017.
Ultimo aggiornamento: 2026-10-29.

Legenda: **[V]** verificato su fonte primaria letta (file in `lavoro/ricerca_cloud/`, con riga o pagina); **[R]** riferito da terzi (stampa, sindacati, sito istituzionale non contrattuale, sentenza che cita il capitolato); **[D]** dedotto da chi scrive.

## 0. Esito in una riga

La ripartizione puntuale dei compiti tra i sei partner **non è pubblica**. Sta nell'offerta tecnica, nel Progetto Tecnico 17CE2693ATO e nel Progetto Esecutivo 17CE2693EXE (v1.10 del 09/02/2023), nella Guida al contratto quadro e nell'Allegato Tecnico di Compliance. Questi documenti sono dietro il login START o non indicizzati. Ciò che si può dire con certezza è:
- tutti i partner sono **esecutori** (non semplici fornitori di licenze), con quote di esecuzione dichiarate;
- il contratto prevede l'esercizio operativo (gestione sistemi, rete, sicurezza, backup, DR) e gli amministratori di sistema dell'Appaltatore;
- i singoli compiti di DXC, IBM e Kyndryl **non risultano** da nessun documento reperito.

## 1. Documenti cercati e stato

| Documento | Stato |
|---|---|
| Contratto quadro (cq.txt) | letto per intero [V] |
| Progetti dei fabbisogni Firenze 2025 (pf_fi), DSU 2023 (pf_dsu), Firenze Metrowide 2024 (mw_pf) | letti [V] |
| Determine (dd8446, dd5901, a*.txt), atto di adesione e nomina gruppo di lavoro Firenze Metrowide (mw_adesione, mw_nomina) | letti [V] |
| C.S.D.P. della gara (decreto 11103/2017) | **non trovato**. Il file "capitolato speciale.pdf" del sito Comune di Firenze (20200709) è di altra gara (piattaforma IRIS, CIG 755171505D) e **non va usato**: scartato |
| Offerta tecnica / Progetto Tecnico 17CE2693ATO | non pubblico (solo citato; ai §3.3.1 "Centri Servizi remoti") |
| Atto costitutivo del RTI | citato come allegato al CQ (cq.txt r. 183), non reperito |
| Guida al Contratto Quadro, Allegato Tecnico di Compliance (es. TLC25DODATC, TLC24EXFATC) | non reperiti (START richiede login; non aggirato) |
| Sentenza Consiglio di Stato (ricorso 7033/2019, provv. 202000378), `cds.txt` | letta; riporta stralci del C.S.D.P. [R] |
| Pagine cloud.toscana.it (`ct_chi-siamo.html`, home), presentazione Armanino 22/11/2021 (`armanino.txt`), agendadigitale.toscana.it | lette [V per il contenuto, R per il valore contrattuale] |

## 2. Struttura contrattuale [V]

- RTI, quote di esecuzione (cq art. 1 c. 3, r. 183-191): TIM (Telecom Italia) 41,27%, Enterprise Services 16,53%, IBM Italia 9,65%, Lutech 20,48%, Dedalus 11,71%. Le quote "potranno subire variazioni" in esecuzione (r. 193-197).
- Il CQ dice che "le società costituenti il Raggruppamento eseguiranno le prestazioni" come da domande di partecipazione e atto costitutivo (r. 182-185): sono **esecutori diretti**, non rivenditori.
- Oggetto (art. 1): progettazione, realizzazione, **gestione operativa** e sviluppo evolutivo del SCT, più lavori sugli impianti industriali del DC TIX.
- Enterprise Services Italia S.r.l. è indicata come "a DXC Technology Company" (pf_fi r. 124; dd8446 r. 99).
- **Kyndryl Italia S.p.A. compare già nel novembre 2021**, non dal 2024: elenco RTI nella presentazione di G. Armanino (Regione Toscana, 22/11/2021, slide 6) e sul sito cloud.toscana.it (chi-siamo) [V sulla presenza, non sul titolo giuridico]. Nei documenti 2024-2026 è mandante accanto a IBM (pf_fi, mw_pf, dd8446 r. 99-100).
- Pagamento: fattura la sola TIM mandataria (dd8446 r. 123-124) [V].

### 2.1 Dati personali: i mandanti sono Responsabili [V]

pf_fi r. 380-381 e mw_pf: l'Ente nomina TIM Responsabile ex art. 28 GDPR e le conferisce mandato (art. 1704 c.c.) "al fine di nominare Responsabili del trattamento le società mandanti". Quindi DXC, IBM e Kyndryl (se nominate) sono Responsabili che trattano dati degli enti [V]; il fatto che serva nominarle implica che trattino dati [D, solido].
CQ art. 38 c. 4 punto 3 (r. 1529-1534): l'Appaltatore deve nominare gli "amministratori di sistema" (provvedimenti Garante 2008/2009), conservarne gli estremi, e comunicare al Titolare l'elenco nominativo con gli ambiti di operatività [V]. L'elenco **non è pubblico**. Punto 5 (r. 1556ss): subappaltatori che trattano dati devono essere nominati sub-responsabili.

## 3. Sedi e chi le gestisce

| Nodo | Proprietà / messa a disposizione | Gestione operativa |
|---|---|---|
| **TIX** (Firenze, nodo primario) | Regione Toscana: "messo a disposizione da Regione Toscana" [R: sentenza CdS cita il C.S.D.P. art. 2]. Locali consegnati alla Regione con verbale, impianti già presenti (CQ art. 30 c. 7, r. 1050; sentenza) [V/R] | L'**Appaltatore** (RTI) assicura "manutenzione, gestione ed esercizio delle infrastrutture IT presenti presso il DC TIX", esercizio e manutenzione ordinaria degli impianti, rete locale, sicurezza perimetrale [R: stralci C.S.D.P. nella sentenza, `cds.txt`]. Appaltatore "Datore di lavoro della struttura" ex art. 26 D.Lgs. 81/2008 (CQ art. 30 c. 8) [V]. A fine contratto l'infrastruttura va rimossa dal TIX a cura dell'Appaltatore, con affiancamento (art. 21, r. 530-554) [V]. **Quale membro del RTI faccia il presidio fisico/logico al TIX: non documentato.** |
| **Firenze-Bruni** (continuità applicativa, BC) | "Data center TIM" [V: Armanino slide 3; R: sito] | TIM, per proprietà del DC [D]. |
| **Roma-Acilia** (disaster recovery, DR) | "Data center TIM" [V: Armanino slide 3, cloud.toscana.it servizi: "DR su sito secondario (Acilia), continuità applicativa su sito secondario (Firenze Bruni)"] | TIM [D]. |

Nota: l'unica gestione del TIX prima del SCT era del consorzio HyperTIX (Almaviva, CDC, TD Group), 2011-2014 [R: zerounoweb, ilcorrieredellasicurezza]. Nessun legame documentato con l'attuale RTI.
Localizzazione dati: slide Armanino "tutela dei dati: presso il datacenter regionale (Italia/UE)" [R]; non c'è nel CQ una clausola esplicita di residenza dei dati in UE (grep su cq.txt) [V come assenza nel solo CQ].

## 4. Subappalti [V]

CQ art. 28 (r. 942-976): subappalto fino al 30% dell'importo, per le prestazioni indicate in offerta, con terne di subappaltatori (autorizzazione ex art. 105 D.Lgs. 50/2016):

| Prestazione | Terna indicata |
|---|---|
| Gestione sistemi di calcolo, storage | T.T. Tecnosistemi, BV Tech, Axiom.IT |
| Gestione sistemi di rete | Maticmind, BV Tech, TBS.IT |
| Gestione della sicurezza | Sistemi Informativi, BV Tech, Maticmind |
| Dispiegamento/assistenza specialistica CMP | Accenture, ClouDesire.com, BV Tech |
| Servizi SaaS | Extra Red, BV Tech, I.S.E.D. |
| Gestione istanze PaaS fully-managed | BV Tech, Eustema, I.S.E.D. |
| Altri servizi (videoconferenza, streaming) | BV Tech, T.T. Tecnosistemi, Sime Telecomunicazioni |
| Servizi professionali | Project, BV Tech, T.T. Tecnosistemi |
| Progettazione/lavori/manutenzione impianti | West Systems, Carani e Pieroni, Chiti, La Rinascita, Estracom, Control |

Terne = possibili, non subappalti effettivi. **Lista effettiva dei sub-responsabili alla data 24/08/2022** (cloud.toscana.it/chi-siamo, ex art. 38 c. 4 p. 6) [R, pubblicazione istituzionale]: **BV Tech S.p.A. (Milano), Sistemi Informativi S.r.l. (Roma), Axiom.IT (Firenze), Moongy Italia S.r.l.**
- Accenture, ClouDesire, Extra Red **non figurano** nella lista 2022 [V come assenza in quella pagina; la lista può essere cambiata dopo il 2022] [D: non risultano sub-responsabili effettivi a quella data].
- Sistemi Informativi è società del gruppo IBM in Italia [R: sindacati USB parlano di "IBM, Sistemi Informativi e altre aziende del gruppo"; a1629 la cita insieme a IBM in RTI Consip]. Quindi la sicurezza (terna del CQ) può passare per una società IBM [D].
- BV Tech copre tutte le aree (calcolo, rete, sicurezza, CMP, SaaS, PaaS): se è il subappaltatore effettivo, è un attore operativo rilevante [D].
- Ruolo di Moongy Italia: non documentato.

## 5. Ruolo di ciascun partner

| Partner | Verificato [V] | Dedotto [D] / ignoto |
|---|---|---|
| **TIM** (41,27%) | Mandataria, fattura, interfaccia verso gli enti e DPA (pf_fi r. 380; dd8446). Nodi BC (Firenze-Bruni) e DR (Acilia) sono DC TIM (Armanino slide 3) | Gestisce quei due DC e presumibilmente cuore dei servizi IaaS/rete (maggiore quota). Il "Team di Presidio dedicato" (pf_fi r. 279) non è attribuito a un'azienda |
| **Enterprise Services Italia / DXC** (16,53%) | Esecutore con quota, "a DXC Technology Company"; Responsabile del trattamento via mandato TIM | Ruolo tecnico preciso ignoto. DXC è fornitore di managed services/IT outsourcing, ma questo è generale, non sul SCT. Gestione operativa plausibile (sistemi, infrastruttura), non verificata |
| **IBM Italia** (9,65%) | Esecutore con quota, Responsabile via mandato | Ruolo ignoto. Dal 2021 il ramo "Managed Infrastructure Services" è passato a Kyndryl [R] quindi in IBM Italia è rimasto presumibilmente software/hardware maintenance/consulenza [D] |
| **Kyndryl Italia** (quota non pubblica) | Mandante, presente nell'RTI almeno dal 22/11/2021 (Armanino slide 6). Ricevuto dal sito cloud.toscana.it e dalle adesioni 2024-2026 | Spin-off da IBM del ramo MIS, trasferimento ex art. 47 L. 428/1990 con accordo 21/06/2021, circa 1.083 lavoratori [R: UILM, USB, RSU IBM]. **Dedotto**: Kyndryl ha rilevato la parte infrastrutturale (gestione sistemi) di IBM nel RTI. Quota non pubblicata; "subentro a IBM" non documentato in nessun atto che abbiamo letto |
| **Lutech** (20,48%) | Esecutore con quota | Integratore; ruolo ignoto (secondo maggiore quota: plausibile gestione di una parte dei servizi gestiti) |
| **Dedalus** (11,71%) | Esecutore con quota | Software sanitario; probabile area sanità/applicativo, ignoto |

CMP (Cloud Management Platform): piattaforma "ibrida", per quanto possibile open source (cloud.toscana.it/servizi). Il portale mostra un avviso su "sistema Morpheus" [R]. Hypervisor: OpenStack e VMware (pf_dsu r. 314) [V].
Servizi: IaaS (VM, storage, VDC, rete, **backup**), PaaS, SaaS, DRaaS, FWaaS, housing, "gestione fully-managed" delle istanze fisiche e logiche (pf_fi r. 106; Armanino slide 5) [V]. "Team di Presidio dedicato" per attività extra-time FM-ET (pf_fi r. 279) [V].
Backup: standard 1 full settimanale + 1 incrementale giornaliero, 30 giorni (pf_dsu r. 297); "copia remota dei backup" (pf_dsu r. 280) [V].
Certificazione ISO/IEC 27001:2013 con linee guida 27017/27018 su "gestione dell'infrastruttura fisica e informatica del DC SCT", servizi cloud, housing/hosting, backup remoto, DR, gestione e monitoraggio sistemi e rete (cloud.toscana.it) [R].

## 6. Chi ha accesso root/admin ai dati degli enti

**Verificato**: nessun documento nominativo/aziendale. Il contratto impone la nomina di amministratori di sistema dell'Appaltatore con elenco al Titolare (art. 38 c. 4 p. 3) [V]. I servizi sono "fully-managed" (pf_fi) e l'Appaltatore gestisce l'esercizio dell'infrastruttura IT al TIX [R]. Ne consegue che **personale dell'RTI e dei subappaltatori ha accesso amministrativo a sistemi e storage** su cui risiedono i dati [D, solido]. Chi precisamente (TIM, DXC, IBM, Kyndryl, Lutech, BV Tech, Axiom.IT, Sistemi Informativi...) dipende dall'offerta tecnica: **ignoto**. Nei servizi IaaS "self-managed" l'ente gestisce guest OS e applicazioni, l'RTI il livello infrastruttura/hypervisor (cfr. pf_dsu r. 314-317) [V sul modello], con possibilità di accesso fisico/ipervisore ai dati non cifrati [D].
Criptazione dei dati con chiavi detenute dall'ente: non risulta (art. 38 elenca "pseudonimizzazione e crittografia" come misura generale) [V].

## 7. CLOUD ACT (18 U.S.C. § 2713) - valutazione

Testo: il provider di servizi di comunicazione elettronica o di *remote computing service* deve rendere i contenuti "within such provider's possession, custody, or control", **a prescindere dalla localizzazione** dei dati. Valutazione giuridica, non fatto verificato.

- **Soggetti**: Enterprise Services Italia = DXC Technology Company (USA, NYSE) [V: pf_fi "a DXC Technology Company"]; IBM Italia = IBM Corp.; Kyndryl Italia = Kyndryl Holdings Inc. (USA) [D, notorio; Kyndryl ceduta da IBM, fonte R]. Sono tutte società con capogruppo USA soggetta a giurisdizione federale.
- **Possession/custody**: il personale italiano con accesso admin ha, di fatto, custodia dei dati o dei sistemi che li ospitano (D, se tali partner hanno ruoli di gestione sistemi: **non provato per il SCT**).
- **Control**: la giurisprudenza USA (test "legal right to obtain" / "practical ability") tende a includere la capacità di una capogruppo di ottenere dalle controllate dati sotto il loro controllo; è la tesi più forte per DXC, IBM e Kyndryl **se** le controllate italiane hanno accesso. Non c'è una pronuncia definitiva su capogruppo USA / dati di una controllata UE.
- **Plausibilità**: **alta per Kyndryl e DXC *se* hanno ruolo di gestione sistemi; media-bassa per IBM** (il ramo infrastrutturale è andato a Kyndryl, R). Oggi: *plausibile ma non dimostrato* per tutti e tre.
- **Dubbi residui**:
  1. Mancano le prove sul ruolo effettivo (offerta tecnica, elenco amministratori di sistema, lista sub-responsabili aggiornata, Allegato Tecnico di Compliance).
  2. La nozione di "provider of ECS/RCS" (18 U.S.C. § 2711) richiede un servizio "to the public": è discutibile per un community cloud riservato alla PA e per un integratore che opera su commessa.
  3. La giurisdizione personale sulla controllata italiana o sulla capogruppo e il conflitto con GDPR art. 48 (trasferimenti non autorizzati dal diritto UE) restano questioni aperte; il CLOUD Act prevede comity challenge solo per Stati con executive agreement (UE non lo ha concluso al momento di questa ricerca [D, non verificato]).
  4. TIM, Lutech, Dedalus e i subappaltatori italiani (BV Tech, Axiom.IT, Moongy) non risultano controllati da gruppi USA [D, non verificato].

## 8. Cosa serve per chiudere i dubbi (senza contattare nessuno)

1. C.S.D.P. + allegati del decreto 11103/2017 nella banca dati atti Regione Toscana (cercare Allegati del decreto n. 11103 del 26-07-2017): non indicizzati dai motori; si può provare l'accesso diretto alla bancadati senza login.
2. Offerta tecnica / Progetto Tecnico: richiedibile via accesso agli atti o FOIA civico (azione per il responsabile del progetto, non per questa ricerca).
3. Altri enti che pubblicano l'Allegato Tecnico di Compliance (con elenco sub-responsabili e sedi di trattamento) nelle proprie adesioni (Comune di Firenze: TLC25DODATC, TLC24EXFATC; ESTAR, ARPAT, Comuni).
4. Atto di adesione Kyndryl all'RTI (modifica soggettiva) nei decreti regionali di autorizzazione.

## Fonti principali

- `cq.txt` (contratto quadro), `pf_fi.txt`, `pf_dsu.txt`, `dd8446.txt`, `mw_pf.txt`, `mw_adesione.txt`, `mw_nomina.txt` in `lavoro/ricerca_cloud/`.
- `armanino.txt`: G. Armanino, Regione Toscana, "SCT", 22/11/2021 (agendadigitale.toscana.it).
- cloud.toscana.it/chi-siamo e /servizi (`ct_chi-siamo.html`, `ct_servizi.html`).
- Consiglio di Stato, ricorso 7033/2019, provv. 202000378 (mdp.giustizia-amministrativa.it) -> `cds.txt`.
- GU 14/10/2019 avviso di aggiudicazione (`gu.txt`); CQ pubblicato dal Comune di Firenze.
- Kyndryl/IBM MIS: UILM, USB, RSU IBM Segrate (ricerca web 2026-10-29; fonti sindacali = riferito).
