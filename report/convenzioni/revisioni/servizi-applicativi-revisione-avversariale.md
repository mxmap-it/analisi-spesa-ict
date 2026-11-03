# Revisione avversariale dei dossier dei servizi applicativi (ID 2212, 2483, 2610, 2365, 2366, 2601, 2536)

Versione 1.0, 3/11/2026, ticket #55. Revisore: agente avversariale (Claude). Oggetto: i 7 dossier in `report/convenzioni/`, le prove in `prove-servizi-applicativi/` e `tools/analisi/attuativi_convenzioni.py`.
Regola applicata (DECISIONI 2026-11-03): «verificato» solo con almeno due fonti indipendenti, di cui una della stazione appaltante. I dossier non sono stati modificati.

## 0. Verdetto per iniziativa e classificazione difendibile per l'imbuto

| Iniziativa | Verdetto | Asse «è cloud?» difendibile | Asse giurisdizione | Note per l'imbuto |
|---|---|---|---|---|
| ID 2212 L1-L3 (8210577E78, 82106098E2, 8210615DD4) | **regge** | escluso come cloud diretto (V: chiarimenti Consip 7 e 93) | n/a (servizi professionali) | togliere i 3 attuativi SPC Cloud AO Moscati; quota migrazione come soglia minima |
| ID 2483 L1 (91918889EE) | **regge con riserva** | escluso *per la parte servizi*; **incerto** per gli attuativi che contengono licenze o servizi sistemistici (vedi A1.2) | per gli attuativi con prodotto: dal prodotto (es. Nutanix, USA) | lotto ufficiale «Servizi applicativi **e accessori**»: gli accessori non sono documentati; GSE B9A1514D57 dichiara «fornitura licenze software … Nutanix … hybrid cloud» (7,32 M) |
| ID 2483 L2 (9191898231) | regge | escluso | n/a | stato «da-verificare» corretto |
| ID 2610 L1 (A02590F330) | **regge con riserva** | escluso per continuità, non per documento | n/a | stato CIG↔lotto ora verificabile con fonte d'ente (Lazio, ASPAL) |
| ID 2610 L2 (A0259125A9) | **regge** | escluso | n/a | ASPAL: ipotesi ×1000 **confermata** sull'atto dell'ente |
| ID 2365 L2 (903054517C) | regge con riserva | escluso salvo componenti SaaS (vedi 2601) | da accertare per prodotto (Dedalus) | Lazio 150 M non verificato sull'atto |
| ID 2366 L2 (9188183878) | regge con riserva | **incerto** sugli attuativi con canone PSN/PNRR 1.1-1.2 | da accertare | stato «da-verificare» corretto |
| ID 2601 L2 (98209074D6) | **cade** la tesi «cloud escluso, nessuna licenza» | **incerto**: Consip ha progettato la 2ª edizione «con possibilità di erogazione anche tramite modalità SaaS» e chiede fatturato di «licenze on-premises e soluzioni SaaS» | da accertare per prodotto (Engineering, Dedalus, GPI: IT; Enterprise Services: USA) | serve il capitolato e gli attuativi con SaaS |
| ID 2536 L2/L6 (985365662A, 985369130D) | regge | escluso | n/a | anomalie InfoCamere non verificate sull'atto |

**Classificazione difendibile oggi.** Escluso certo dall'asse cloud: ID 2212 L1-L3 e i lotti PMO/demand (2483 L2, 2610 L2, 2536 L6) e la consulenza 2536 L2. Escluso «per la parte servizi» ma con riga incerta per attuativo: 2483 L1, 2610 L1, 2365 L2, 2366 L2. Incerto a livello d'iniziativa: 2601 L2 finché non si legge il capitolato.

## 1. Assunzioni cadute

1. **2601 «non è cloud diretto; licenze e SaaS da accertare»** → la componente SaaS/licenze è prevista dalla stazione appaltante fin dalla consultazione di mercato. *Cade* la classificazione «cloud escluso, confidenza media»: va «incerto».
2. **2483 «né il bando né i contratti prevedono IaaS, PaaS o SaaS» / nessuna licenza** → *cade nella forma assoluta*: il lotto si chiama «Servizi applicativi **e accessori**» (decisione a contrarre del Ministero della Giustizia) e almeno un attuativo BDNCP dichiara una fornitura di licenze Nutanix per hybrid cloud (GSE, 7,32 M). O il padre è sbagliato o gli accessori includono prodotti: in entrambi i casi la frase va riscritta.
3. **Riproducibilità (AGENTS §5, #47)** → *cade*: i numeri dei 7 dossier non sono prodotti da una verifica in `tools/verifiche/`. `tools/verifiche/attuativi_convenzioni.py` contiene solo PSN, SPC Cloud e FS; i dossier usano `tools/analisi/attuativi_convenzioni.py` che scrive in `lavoro/`. Il CSV si riproduce identico, il riepilogo no (vedi A7).

## 2. Assunzioni una per una

### A1. «"In ottica cloud" = servizi professionali, non cloud»

**A1.1 ID 2212.** Tesi: chiarimenti Consip 7 (re-hosting in ID 2213) e 93 (CSP qualificati AgID). Attacco: rilette le citazioni nel dossier; nessuna prova contraria trovata. **Esito: regge.**

**A1.2 ID 2483 (estensione per continuità).** Attacco: cercati capitolato tecnico generale e speciale (consip.it, acquistinretepa, copie su siti di enti aderenti, lawinsider). **Capitolato non trovato in forma archiviabile** (solo copie lawinsider di schemi, non archiviate perché copia di terzi). Prove nuove:
- Schema di contratto esecutivo ID 2483 L1 (pubblicato dal MiTur, 2026): rinvia a «Capitolato Tecnico Generale e Speciale» e ai «servizi … come riportati nel Piano Operativo»; nessuna voce di canone o infrastruttura. Sostiene la tesi.
  `https://www.ministeroturismo.gov.it/wp-content/uploads/2026/08/Schema-di-Contratto-Esecutivo.pdf` — sha256 `66953589a7d1676eadc66404576059c60aa9a5c084aac8c0b67238234e8710d8`
- Ministero della Giustizia, decisione a contrarre 474 del 6/6/2025: aderisce a «ID 2483 … Lotto 1 – **Servizi applicativi e accessori**», per «servizi professionali» (26,78 M IVA incl.). Sostiene la natura di servizi, ma introduce gli «accessori», non documentati nel dossier.
  `https://www.giustizia.it/cmsresources/cms/documents/dit_decisione_a_contrarre_474_06giu2025.pdf` — `b757dabbc849c375c3e741dffd5507a52515c40097326845434591fd346e153c`
- CONSOB, decisione 0109694: adesione a ID 2483 L1 (RTI IBM) per «servizi di sviluppo software e supporto specialistico per il **setup e la migrazione dell'infrastruttura**» verso il cloud; 2,47 M, di cui 0,465 M imputati al capitolo «Noleggio, manutenzione e assistenza prodotti hardware e software». Sono servizi, ma con componente sistemistica/infrastrutturale.
  `https://www.consob.it/documents/d/asset-library-1912910/0109694_decisione` — `921c6427c1848eef876b6958e1291016a67726b6ff8a85d81dc782a75818d45f`
- ARERA, determina 51/2026 DAGR: ID 2483 L1, CIG 91918889EE, RTI Enterprise Services, 1,15 M + IVA per cybersicurezza (servizi).
  `https://www.arera.it/fileadmin/allegati/docs/26/51-26dagr.pdf` — `a155316005da2e24e95c311c3fe96d2d66194009902a7eeed13b45a202ba603b`
- BDNCP (`attuativi.csv`, sha256 `5d9bcf85…`): GSE **B9A1514D57**, oggetto lotto «FORNITURA LICENZE SOFTWARE DELLA SOLUZIONE NUTANIX PER LA GESTIONE DI AMBIENTI HYBRID CLOUD», 7.319.940 €, padre 91918889EE; PCM 9847671B2E «conduzione applicativa **e sistemistica** … in ambiente cloud», 2,0 M; Studiare Sviluppo «gestione sistemistica». Atto GSE non trovato (R).

**Esito: regge con riserva.** La sostanza (si comprano giornate di professionisti a tariffa) regge su 5 atti di enti diversi; non regge l'affermazione assoluta «nessun prodotto/licenza». **Correzione:** riscrivere §1.2 e §3 del dossier 2483 così: «servizi professionali a tariffa; il lotto comprende servizi accessori non documentati (capitolato non archiviato); almeno un attuativo dichiara licenze di prodotto (GSE, Nutanix)». Nell'imbuto: asse cloud «escluso» per default, «incerto» per gli attuativi con classe `prodotti` o parole «licenz|sistemistic|infrastruttur|setup». Recuperare il capitolato speciale L1 (Allegato 13A) e la «Guida all'AQ» da acquistinretepa.

**A1.3 ID 2610.** Prove nuove d'ente: Regione Lazio DD G04481 del 9/4/2025 (ID 2610 L2, CIG A0259125A9, «servizi di supporto specialistici», 389.546 €) e ASPAL Piano operativo (ID 2610 L2, tariffe a giornata 210-220 €). Entrambe sul lotto 2; sul lotto 1 nessun capitolato nuovo. Gli oggetti BDNCP del L1 contengono InfoCamere «assistente virtuale» (AI) e altre realizzazioni, compatibili con servizi.
`https://regione.lazio.it/sites/default/files/documentazione/2025/SOC-DD-G04481-09-04-2025.pdf` — `6848bdc9ca2aafaba345abdea621317af8b0826a79594648c51aaf4099690150`
`https://agenziaregionaleperillavoro.regione.sardegna.it/documenti/44_915_20241230081350.pdf.p7m` — `6e6b89dc13c23ae1fe3bf4065befdf4f1819d6c8e957fa8509fea9b026a76512`
**Esito: regge con riserva** (L1 sempre per continuità). Correzione: come 2483.

### A2. Quote di migrazione (soglie minime da regex)

Tesi: 2483 L1 6,4 M (0,2 %) espliciti, 46,2 M (1,6 %) con il cloud specifico; 2212 18,6 M; 2610 4,6 M.
Attacco 1 — oggetti generici: tra gli attuativi < 50 M, quelli con classe `pnrr` ma senza `migrazione` valgono 49,1 M (11) su 2483 L1, 36,6 M (20) su 2610 L1, 95,3 M (3, AgID SDG/INAIL) su 2212 L1, 16,9 M (4) su 2366. È il margine minimo di sottostima per i soli progetti PNRR non descritti (misura nostra sul CSV).
Attacco 2 — oggetti che nascondono migrazione: CONSOB «evoluzione al cloud» (2,47 M) e PCM «conduzione … in ambiente cloud» non hanno la parola «migrazione»; il dossier li conta solo nel gruppo «cloud specifico». Corretto, ma conferma che la soglia «migrazione esplicita» è molto bassa.
Attacco 3 — PNRR 1.2 Comuni: due enti verificati (Firenze DD 9667/2024, 4,79 M PNRR; Verona det. 6144 e 6514/2024) migrano **con PSN o affidamenti propri**, non con questi AQ. Il caso Carrara (2212 L1) è l'eccezione documentata. Non ho trovato migrazioni 1.2 eseguite con 2483/2610 oltre a quelle già nel dossier.
`https://affidamenti.comune.fi.it/sites/affidamenti.comune.fi.it/files/profilo/determina-a-contrattare/20241217/DDcontrarre_09667.pdf` — `215ef485091f56ce776a90211662e1751ada4209a4115536481df5b6ccc2402c`
`https://www.comune.verona.it/content/download/21681/505062/file/det_06144_09-12-2024.stamped.pdf` — `485e150b6294752492d59b488e09e039c2e85e76e9c8367fbcb1a8fc4209830b`
`https://www.comune.verona.it/content/download/16152/351903/file/det_06514_20-12-2024.stamped.pdf` — `d17b45c76ae22616359a376d09be845d3837326d0b1a83893e6ab9c4688dca9e`
**Esito: regge con riserva.** Le cifre sono corrette come soglie minime, ma le percentuali (0,2 %, 1,6 %) non vanno pubblicate come «quota»: suggeriscono un ordine di grandezza che la regex non può dare. **Correzione:** pubblicare un intervallo «da soglia minima a soglia minima + attuativi PNRR/oggetto generico» (2483 L1: 6,4–95 M circa, cioè 0,2–3,2 %) e marcare il resto «incerto»; campionare 20 piani dei fabbisogni per stimare la quota vera.

### A3. Letture degli importi anomali

Controllo preliminare: i valori grezzi ANAC (`importo_lotto` nei CSV mensili, letti in streaming con `lavoro/rev-servizi/grezzo.py`) sono già interi senza separatori: B4FCA078F0 `'2213114754'`, B5A2C1471F `'3210000000'`, B489E1897E `'3000000000'`, B76198E668 `'1605000000'`, B76199E39D `'400000000'`, B785C1D778 `'250000000'`, B78F306070 `'150000000'`, B29E105589 `'667087403'`. L'errore non è del nostro parser.

- **ASPAL ×1000 (2610 L2)**: il Piano operativo ASPAL (sha256 `6e6b89dc…` sopra) chiude a «€ 2.700.000,00 (IVA inclusa)»; 2.700.000 / 1,22 = 2.213.114,754 €. Il valore BDNCP 2.213.114.754 è l'imponibile con tre decimali senza virgola. **Regge, ed è ora verificato** (atto d'ente + BDNCP). Correzione: valore 2,21 M, non escluso ma corretto. Nota: il Piano operativo cita il CIG dell'AQ, non il CIG derivato B4FCA078F0; il legame è per ente, lotto, fornitore (Intellera) e importo esatto.
- **Banca d'Italia «AQ derivati con massimale» (2483 L1, 9+1 attuativi)**: nessun atto trovato (ricerche su TED e bancaditalia.it senza esito). **Ipotesi alternativa non esclusa:** lo stesso errore ×1000 di ASPAL. 3.000.000.000 → 3,0 M e 3.210.000.000 → 3,21 M sono importi plausibili per singoli contratti SVI. La lettura «base d'asta del lotto» e la lettura «×1000» danno lo stesso effetto (escludere), ma non lo stesso numero se si vuole reintegrare. **Regge con riserva**: «massimale» resta R; scrivere «importo implausibile (> massimale del lotto), lettura da accertare».
- **Regione Lazio su 2601 (B785C1D778, 250 M, «digital upskilling FSE 2.0»)**: atto non trovato; la DD Lazio trovata riguarda FSE+ su ID 2610 L2 (0,39 M), non questo CIG. Anche qui 250.000.000/1000 = 250 k è plausibile per una piattaforma e-learning. **Non verificabile oggi**: la lettura «padre sbagliato» non ha prova; resta R.
- **InfoCamere (2610 L1 2×1.605 M; 2536 L6 400 M)**: atto non trovato. Ipotesi ×1000 (1,605 M; 400 k) plausibile quanto «quota di massimale». R.
- **Lazio 2365 (B78F306070, 150 M)**: non controllato sull'atto; 150 k plausibile. R.

**Esito complessivo A3: regge con riserva** (1 su 5 verificata, e confermata; le altre 4 hanno una spiegazione alternativa ugualmente plausibile). **Correzione:** nei dossier sostituire le interpretazioni (massimale / padre sbagliato / quota RTI) con «importo implausibile; ipotesi: massimale o errore ×1000; da verificare sull'atto»; annotare in `richieste-e-raccomandazioni.yaml` (ANAC) il controllo di coerenza importo-derivato ≤ massimale del padre.

### A4. Regola «escludere attuativi ≥ massimale/10»

Attacco:
- Non coglie gli errori ×1000 su contratti piccoli: un affidamento da 50 k inserito ×1000 vale 50 M, sotto la soglia di 360 M del lotto 1 di 2483 (e sotto 216 M di 2610 L1). ASPAL è stato colto solo perché il lotto 2 ha un massimale piccolo.
- Dipende dal massimale del lotto, che per alcuni padri è incerto (TED vs BDNCP, +20 %).
- Esclude anche eventuali derivati veri di grandi enti (Sogei, Interno) se il lotto è piccolo.

Alternative, in ordine di robustezza:
1. **Controllo di coerenza a più livelli**: escludere se importo > massimale del lotto (impossibile); marcare «sospetto» se importo > 10× la mediana del lotto **e** > 5 % del massimale; per i sospetti verificare l'atto.
2. **Controllo ×1000**: se importo/1000 cade nella fascia interquartile del lotto e l'importo è multiplo di 1000 o ha la forma «imponibile con 3 decimali», marcare «probabile ×1000».
3. **Seconda via sull'importo**: confrontare con `importo_aggiudicazione` (dataset aggiudicazioni ANAC) e con l'OCDS; la discrepanza > 10× è un segnale indipendente dall'ente.
4. Somma di controllo: la somma dei derivati per lotto non può superare il massimale; se lo supera, si scartano in ordine decrescente i sospetti finché rientra.
**Esito: regge con riserva** come prima barriera; non è sufficiente da sola. **Correzione:** adottare 1+3 e tenere la regola massimale/10 solo come soglia «da verificare», non di esclusione automatica.

### A5. Sanità digitale: licenze, SaaS, giurisdizione

Prove nuove:
- Consip, documento di consultazione del mercato «Sanità Digitale Clinico-Assistenziale 2» (14/7/2022, la gara che è diventata ID 2601): «servizi applicativi e di supporto … con possibilità di erogazione anche tramite modalità software as a service (SaaS)»; i SaaS devono essere qualificati AgID; richiama la strategia di migrazione «re-purchase»; chiede il fatturato per «licenze on-premises e soluzioni SaaS» (CCE, ADT, RIS, LIS, PACS, telemedicina).
  `https://www.consip.it/sites/default/files/Sanit%C3%A0%20Digitale%20Clinico-Assistenziale%202%20-%20Questionario%20generale.docx` — `8971e5afb92021e8a16fa8431411debae845bf51602886356d85430392a6c702`
- Avviso di esito GUUE ID 2601 (Consip): CPV 72211000 per i lotti 1-4, 72222000/72224000 per 5-6; nessun CPV di licenze o SaaS (48xxxxxx / 72416000). Il CPV quindi non smentisce, ma non esclude: i SaaS possono essere «accessori».
  `https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/AVVISO%20DI%20ESITO%20GUUE%20ID%202601.pdf` — `059b04a8dd22679a58292386faf1432d5aef40f60f20a2812c9538bf14cf172d`
- Stampa di settore (corrierecomunicazioni.it) riferisce che la 2ª edizione aggiunge la fruizione SaaS e servizi accessori con «prodotti software, SaaS e soluzioni di mercato» fino al 50 % della base dell'appalto specifico. **Non archiviabile**: archivia.py riceve una pagina di blocco WAF (non aggirata). R.
- ID 2366: rettifiche Consip archiviate, nessuna occorrenza di SaaS/licenze/canone/cloud.
  `https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID%202366%20-%20Rettifiche%20alla%20documentazione_0.pdf` — `dcc05fa0629ee198ca0eee371b116df6b9dbb07e24bffd55d2fffcddf33713d3`

Giurisdizione: aggiudicatari 2601 L2 Engineering, Dedalus, GPI (capogruppo italiane, R da verificare con la tabella capogruppo in `config/`) ed Enterprise Services Italia (gruppo DXC, USA). I prodotti CCE di Dedalus e GPI sono italiani; il SaaS può però girare su hyperscaler: la giurisdizione dell'infrastruttura va letta per contratto (qualificazione ACN del servizio). R.
**Esito: cade** per 2601 («cloud escluso»), **regge con riserva** per 2365 e 2366. **Correzione:** 2601 L2 asse cloud «incerto», con sotto-voce «SaaS di prodotto» da quantificare sui piani dei fabbisogni; archiviare capitolato e listino; per 2366 trattare come incerti gli attuativi con canone PSN o PNRR 1.1/1.2 (Sardegna IT, So.Re.Sa.).

### A6. «Verificato» e regola delle due fonti

| Voce proposta «verificato» | Fonti nei dossier | Fonte d'ente indipendente da Consip | Esito |
|---|---|---|---|
| 2483 L1 91918889EE | TED + BDNCP (entrambi Consip) + contratto ISTAT | ISTAT, e ora ARERA, Giustizia, CONSOB | **regge** |
| 2483 L2 9191898231 | solo BDNCP (numero gara) | nessuna | «da-verificare» corretto |
| 2212 L1-L3 | TED + chiarimenti Consip + comunicato Consip su sito AgID | il comunicato è Consip, non AgID: **nessuna fonte d'ente** nei dossier per il legame CIG↔lotto; solo oggetti BDNCP (dati inseriti dagli enti) | **regge con riserva**: aggiungere un contratto esecutivo d'ente con CIG AQ (es. Carrara, Roma Capitale) |
| 2610 L1/L2 | TED + BDNCP | Lazio DD G04481 (L2, CIG A0259125A9), ASPAL (L2) | L2 **ora verificabile**; L1 serve un atto d'ente |
| 2365, 2601, 2536 | TED + BDNCP | nessuna nei dossier | restano «da-verificare» per la regola, anche se il dossier li presenta come V |
| 2366 | solo BDNCP | nessuna | «da-verificare» corretto |

Nota di metodo: TED, BDNCP del CIG padre, rettifiche e comunicati vengono tutti da Consip: contano come **una** fonte. Gli oggetti BDNCP dei derivati sono dell'ente, ma «deboli» (lo dice già il dossier 2212).
**Esito: regge con riserva.** **Correzione:** in `iniziative_ict.yaml` «verificato» solo per 2483 L1 e 2610 L2; gli altri restano «da-verificare» finché non si archivia un atto d'ente con il CIG dell'AQ.

### A7. Riproducibilità

Prova: rieseguito `tools/analisi/attuativi_convenzioni.py` sui 12 CIG padre, sul server, con nice/ionice, in `lavoro/rev-servizi/run/` (stesso mirror).
- `attuativi.csv`: sha256 `5d9bcf855e9c744fdef125d539a27bd51f909a88338c7aaf27657c1971349d2f`, **identico** a quello committato. Totali per padre identici (es. 91918889EE 556 / 31.258.827.817 €).
- `riepilogo.json`: sha256 `5490396e…` contro `7774cfbc…` committato. Differenze solo nella lista «fornitori» del riepilogo: a parità di importo (membri dello stesso RTI) l'ordine dipende dall'iterazione di un `set`, quindi i primi N cambiano a ogni run (es. 903054517C: Accenture vs Onit/Appocrate).
- Lo script non è in `tools/verifiche/` (quello omonimo copre solo PSN/SPC/FS) e scrive in `lavoro/`, contro AGENTS §5 (#47). Da clone pulito serve il mirror ANAC sul server: non c'è uno snapshot sha256 dichiarato dell'input.
- Limite già dichiarato e confermato nel codice: un CIG il cui `cig_accordo_quadro` è stato corretto nel delta resta contato dalla versione annuale o da una versione delta precedente (il dizionario `att` non rimuove chiavi).
- R22: i dossier dicono di non riprodurla (647/35,2 mld vs 556/31,26). Non risolto in questa revisione.
**Esito: cade** sul requisito formale, **regge** sui numeri. **Correzione:** spostare i padri dei servizi applicativi in `tools/verifiche/attuativi_convenzioni.py` (o farla parametrica), uscita in `report/convenzioni/prove-servizi-applicativi/`, ordinamento deterministico (importo, poi nome), sha256 dei file di input nel riepilogo; togliere le chiavi da `att` quando l'ultima versione di un CIG non punta più al padre.

## 3. Correzioni proposte (riepilogo operativo)

1. 2601 L2: asse cloud da «escluso» a **incerto** (SaaS/licenze previsti da Consip); archiviare capitolato e guida.
2. 2483 L1 e 2610 L1: «escluso» solo per la parte servizi; attuativi con licenze/sistemistica/infrastruttura → incerti (GSE B9A1514D57 Nutanix 7,32 M; PCM 9847671B2E; CONSOB B49210B98C). Riscrivere «né il bando né i contratti prevedono…» e documentare i «servizi accessori».
3. ASPAL B4FCA078F0: correggere a 2.213.114,75 € (verificato) invece di escluderlo.
4. Banca d'Italia, Lazio (2601, 2365), InfoCamere: togliere le interpretazioni non provate; scrivere «implausibile, massimale o ×1000, da verificare».
5. Regola di esclusione: impossibile (> massimale) → escluso; sospetto (> 10× mediana e > 5 % del massimale) → da verificare; confronto con importo di aggiudicazione; controllo somma ≤ massimale.
6. Quote di migrazione come intervallo, non come percentuale puntuale.
7. «Verificato» solo 2483 L1 e 2610 L2; per 2212 aggiungere un atto d'ente.
8. Riproducibilità: verifica in `tools/verifiche/`, ordinamento deterministico, snapshot degli input.
9. Raccomandazioni da annotare (non fatto qui: fuori dal file assegnato): ANAC, controllo importo derivato ≤ massimale del padre e formato decimale; Consip, pubblicare capitolati in URL stabili (la pagina 2483 si genera via JavaScript).

## 4. Limiti di questa revisione

- Nessun capitolato 2483/2610/2601 trovato in forma archiviabile; lawinsider non usato come fonte (copia di terzi).
- 4 anomalie su 5 non verificate sull'atto (atti non trovati con ricerca web).
- Pagina corrierecomunicazioni.it non archiviabile (WAF, non aggirato): l'informazione sui servizi accessori SaaS al 50 % è R.
- Nessun contatto con enti. File di lavoro: `lavoro/rev-servizi/` sul server (`grezzo.py`, `grezzo.log`, `run/`, testi estratti).
