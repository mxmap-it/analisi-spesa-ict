# Revisione avversariale — PSN, SPC Cloud lotti 1/3/4, Trenitalia (#55)

Versione 1.0 — 2026-11-03. Revisore avversariale (DECISIONI.md, voce 2026-11-03). Oggetto: i dossier `9066973ECE-polo-strategico-nazionale.md`, `55187486EA-spc-cloud-lotto-1.md`, `55193442C1-spc-cloud-lotto-3.md`, `5519376D26-spc-cloud-lotto-4.md`, `7991036B82-trenitalia-servizi-ict.md` e `tools/verifiche/attuativi_convenzioni.py`. I dossier non sono stati modificati. File di lavoro: `lavoro/rev-psn/` sul server.

## Verdetti e classificazione difendibile per l'imbuto

| Iniziativa | Verdetto | Classificazione difendibile |
|---|---|---|
| PSN 9066973ECE | **Regge con riserva**; cade «quote non stimabili» | Padre = massimale, escluso. Attuativi: **prevalentemente servizi e infrastruttura PSN (IT)**; quota hyperscaler extra-UE **misurabile a livello aggregato**: Secure Public Cloud = 4,4 % dei ricavi 2025 (19,9 su 454,3 M€), PSN Managed 1,0 %; sui contratti firmati, canoni = 40 % del valore, di cui SPC 15 % (circa 6 % del valore totale) e «Soluzioni Oracle PSN» 14 % (circa 5,6 %, misto Industry Standard Oracle + PSN Managed). Per singolo CIG resta «incerto». |
| SPC Cloud lotto 1 55187486EA | **Regge con riserva** | Cloud (IaaS/PaaS/BaaS) + servizi; giurisdizione **IT con riserva** (Enterprise Services Italia/DXC mandante, ruolo esecutivo ignoto; PaaS SQL Server = prodotto Microsoft). «Verificato» solo sull'identificazione; il contenuto resta R finché manca un documento Consip. |
| SPC Cloud lotto 3 55193442C1 | **Regge** | Non cloud (servizi applicativi/interoperabilità). Nessun attuativo con hosting/IaaS/hyperscaler nell'oggetto. |
| SPC Cloud lotto 4 5519376D26 | **Regge con riserva** («escluso certo» va attenuato) | Non cloud per la convenzione; **hosting web accessorio** reale (Giustizia 9,5 M€ «hosting siti web e manutenzione», ENIT 0,2 M€): escluso al netto di questi CIG. |
| Trenitalia 7991036B82 | **Cade l'asse B «incerto, prodotti non identificabili»**; regge la decifrazione | AQ **intragruppo** → fuori dalla misura cloud (come in-house); il cloud pubblico di FSTechnology va contato **sul suo CIG proprio**: AQ Microsoft Azure MACC per il gruppo FS (CIG 9481341A1A, Microsoft Ireland Operations, TED 139007-2023) = EXTRA-UE (USA). Stato «da-verificare» resta. |

## Assunzioni cadute

1. PSN: «quote non stimabili» — il Bilancio integrato 2025 di PSN dà la ripartizione dei ricavi e del valore dei contratti per famiglia (A1).
2. PSN: «Industry Standard = IT con sole dipendenze tecnologiche» va riformulato: il 14 % dei canoni è «Soluzioni Oracle PSN», che **include i servizi Oracle Enterprise dell'Industry Standard**; il PEF indica licenze hypervisor **Red Hat e Microsoft SPLA** (non VMware) (A2).
3. Trenitalia: «prodotti sottostanti non identificabili» — FSTechnology compra Azure direttamente da Microsoft Ireland con un AQ dedicato (A9).
4. Lotto 4 «escluso certo» senza eccezioni (A6).
5. «L'eccedenza degli attuativi sui massimali si spiega con proroghe e doppi CIG»: proroghe e duplicati espliciti ne spiegano una parte minima (A8).

## Correzioni proposte (sintesi)

- PSN §1/§4/§5: sostituire «quote non stimabili» con i dati del Bilancio 2025 (sha256 sotto); `attuativo_default`: «IT prevalente, EXTRA-UE circa 5–12 % del valore aggregato, incerto per CIG».
- PSN §3: Industry Standard: registrare Oracle Enterprise (prodotto USA venduto a canone) come EXTRA-UE di prodotto, e Microsoft SPLA/Red Hat (PEF) accanto a VMware come software-infrastruttura; PSN Managed: «Oracle Alloy; la dicitura Google sopravvive nella grafica del Bilancio 2025 ma ricavi e certificazioni sono solo Oracle».
- PSN §2: il catalogo passa a **V2** grazie al PEF pubblicato dalla PCM (concedente).
- PSN §4: il CSV di lavoro dà 777 attuativi con legame (4,86 mld €) contro 786 (4,89 mld) del dossier: riallineare.
- PSN: totali presentati con e senza ARIA (BAFE270F81) finché manca l'atto.
- Trenitalia: categoria `affidamento-intragruppo`, fuori dal numeratore cloud; aggiungere all'imbuto CIG 9481341A1A (Azure MACC gruppo FS) come EXTRA-UE, verificando l'importo su BDNCP.
- Lotto 4: `asse_cloud: escluso` con eccezione esplicita dei CIG 7365232DB5 e 7429224596 (hosting).
- Lotti 1/3/4: archiviare una fonte Consip diretta (pagina iniziativa SPC Cloud ID 1403 o capitolato) prima di dichiarare V2 sul contenuto; scrivere «eccedenza non spiegata» invece di attribuirla a proroghe.

---

## A1. PSN — quote per famiglia «non stimabili»

- **Tesi**: dagli oggetti dei CIG la ripartizione Industry Standard / hyperscaler non si ricava; serve un dato PSN/DTD.
- **Attacco**: il dato aggregato esiste.
- **Prove**: Bilancio integrato PSN 2025, https://www.polostrategiconazionale.it/app/uploads/2026/07/Libro-PSN-2025.pdf, sha256 `b8fe9ec1b4becdbf07cf837cac4f5ef26621bda85c7bfa1162773bf9a7ed64ed`. Nota «Ricavi da contratti con clienti» (p. 105-106): totale 454.328.062 €; servizi migrazione/Rearchitect/Replatform/IT Infrastructure Service Operation 360.684.223 (79 %); IaaS 26.023.450; **Secure Public Cloud «Azure, Google e AWS» 19.861.529 (4,4 %)**; Data Protection/Security/OS/Connettività 15.715.534; Housing 8.650.981; Hosting 6.258.611; **Public Cloud on PSN Managed 4.529.341 (1,0 %)**; PaaS 7.067.249; coordinamento progettuale 4.171.898; CaaS 1.365.246. «Service mix» dei contratti firmati dall'inizio della convenzione (p. 71-72): servizi professionali 60 %, canoni infrastrutturali 40 %; dei canoni: IaaS 32 %, Soluzioni Oracle PSN 14 %, Backup 13 %, **Secure Public Cloud 15 % (PAC 24 %, PAL 6 %, ASL/AO 7 %)**, Housing & Hosting 13 %, PaaS 4 %, altro 9 %. Il PEF (proposta PSN pubblicata dalla PCM, sha256 `4134d48cbea43462cdaeb9e88aa85e70901cad97a5b241a0726ebfedcdf85b07`) prevedeva in 13 anni rivendita CSP Secure Public Cloud 439,6 M€ e PSN Managed 224,8 M€.
- **Esito**: **cade**.
- **Correzione**: usare il Bilancio 2025 come stima aggregata (fonte unica del concessionario, ma bilancio certificato e numerico). I ricavi sono contabili, non valori dichiarati in BDNCP; la quota extra-UE degli attuativi si colloca fra circa 5 % (ricavi 2025) e 6–12 % (valore dei contratti, a seconda di come si conta «Oracle PSN»). I «servizi di migrazione» al 79 % sono in gran parte finanziati PNRR e non sono cloud.

## A2. PSN — «Industry Standard = IT» malgrado VMware/Oracle/Red Hat

- **Tesi**: Industry Standard IT (operatore italiano, DC in Italia), con dipendenze tecnologiche USA.
- **Attacco**: il metodo (`sito/content/progetto/metodo-cloud-provider.md`) attribuisce la giurisdizione al **prodotto comprato**; il software con cui si costruisce un cloud in casa (VMware) non è un cloud provider ma va marcato `software-infrastruttura`. Coerente per hypervisor e CaaS. Non coerente per **Oracle Enterprise DB/PaaS venduto a canone**: è un prodotto Oracle rivenduto, che per la regola «Microsoft 365 venduto da TIM resta Microsoft» seguirebbe il produttore.
- **Prove**: Bilancio 2025 p. 71: «le soluzioni Oracle PSN, che includono sia i servizi Oracle Enterprise dell'Industry Standard sia i servizi PSN Managed» = 14 % dei canoni (sha256 `b8fe9ec1…`). PEF, voce costi software: «licenze per virtualizzatori/hypervisor Red Hat e Microsoft SPLA» (sha256 `4134d48c…`): il PEF non nomina VMware; il dossier cita solo VMware vCloud (Annesso 3).
- **Esito**: **regge con riserva** per IaaS/CaaS (IT + marcatura software-infrastruttura); **cade** per i servizi Oracle Enterprise a canone.
- **Correzione**: Industry Standard = IT **esclusa** la componente Oracle Enterprise (EXTRA-UE come prodotto, canale PSN). Elencare Microsoft SPLA e Red Hat accanto a VMware.

## A3. PSN — catalogo e giurisdizione per servizio (PSN Managed = solo Oracle?)

- **Tesi**: PSN Managed oggi solo Oracle Alloy; Google della Guida 2024 superato.
- **Attacco**: il Bilancio 2025 (luglio 2026) intesta ancora nella grafica «PUBLIC CLOUD PSN MANAGED (PSN + Oracle/Google Cloud)» e cita partnership «con Azure, Oracle e Google Cloud e, dal 2024, Amazon Web Services».
- **Prove**: Libro PSN 2025 (sha256 `b8fe9ec1…`): testo «Public Cloud PSN Managed è un servizio cloud basato sulla tecnologia Oracle Alloy»; certificazioni «Public Cloud PSN Managed Oracle»; portafoglio 2025 «PSN Managed: Oracle»; region «PSN Managed Oracle a nord». Ricavi Secure Public Cloud: «Azure, Google e AWS» (Oracle non citato, contro la Presentazione 04/2026 che mette Oracle nel Secure Public Cloud). PEF (concedente): PSN Managed = «portfolio dei servizi Hyperscaler erogato da Region dedicata al PSN» senza nome del CSP.
- **Esito**: **regge con riserva** (Google in PSN Managed: residuo grafico, nessun ricavo né certificazione; la giurisdizione è EXTRA-UE in ogni caso, l'imbuto non cambia). Oracle nel Secure Public Cloud = R.
- **Correzione**: annotare la contraddizione residua. Il catalogo a famiglie diventa **V2** con il PEF pubblicato dalla PCM + documenti PSN; il listino XLS resta da archiviare. Nessun documento DTD/Corte dei conti con ripartizione per famiglia trovato in questa sessione.

## A4. PSN — «hosting dedicato = non cloud»

- **Tesi**: l'hosting dedicato è infrastruttura esterna, non cloud NIST.
- **Attacco**: il PEF include Housing e Hosting fra i «Servizi Core»; il bilancio li conta nei canoni infrastrutturali.
- **Prove**: PEF punto 15 (sha256 `4134d48c…`); Bilancio 2025 (Housing 8,65 M€, Hosting 6,26 M€).
- **Esito**: **regge** come scelta di metodo dichiarata (decisione di Fabio); la qualificazione commerciale del concessionario non è un criterio NIST. Peso: 13 % dei canoni, 3,3 % dei ricavi 2025.
- **Correzione**: nessuna; indicare la quota.

## A5. SPC lotto 1 — «IT» malgrado Enterprise Services Italia (DXC) e SQL Server

- **Tesi**: IT per l'erogazione; dipendenze USA.
- **Attacco**: per il metodo conta il prodotto. Se i Virtual Data Center del lotto 1 fossero erogati su DC/piattaforma di Enterprise Services Italia (gruppo DXC, USA), il prodotto sarebbe di un gruppo USA. Nessun documento letto dice quale mandante eroghi l'IaaS. Il PaaS SQL Server è licenza Microsoft rivenduta: per il metodo è Microsoft.
- **Prove**: solo atti di aderenti (det. ART 138/2021, sha256 `86de164f727a099baa625ecf7d930135d94f8a5519abd5eea499b2b833665998`; det. Interno 2022, `c4d4f217e9442135f84fb4ce796260427cabff5e9615595d41db53868e569c22`); nessuna fonte Consip; nessuna fonte nuova sulla ripartizione dei ruoli nel RTI.
- **Esito**: **regge con riserva**.
- **Correzione**: asse B «IT prevalente, con componente prodotto USA (SQL Server PaaS) e ruolo DXC ignoto»; cercare capitolato e listino Consip SPC Cloud lotto 1 (ID 1403).

## A6. SPC lotti 3 e 4 — «cloud escluso con certezza»

- **Tesi**: sviluppo/servizi; «cloud» è solo nel titolo della gara.
- **Attacco**: ricerca di hosting/housing/IaaS/PaaS/infrastruttura/data center/canone/migrazione/hyperscaler negli oggetti dei 1.047 attuativi (`lavoro/convenzioni-55/attuativi.csv`).
- **Prove**: lotto 4: 7365232DB5 Ministero della Giustizia 9,5 M€ «hosting siti web e manutenzione evolutiva e correttiva»; 7429224596 ENIT 0,2 M€ «hosting, conduzione e manutenzione correttiva dei portali»; 8262536C65 ISTAT 0,66 M€ «progetto migrazione portali». Lotto 3: nessun hosting/IaaS; «infrastruttura» solo come oggetto applicativo (MyData Verona, catasto infrastrutture Sardegna). Nessun hyperscaler in nessuno dei due lotti. Nessun contratto esecutivo con canoni cloud trovato.
- **Esito**: lotto 3 **regge**; lotto 4 **regge con riserva** (hosting web reale, misto a manutenzione).
- **Correzione**: lotto 4 «escluso, salvo hosting accessorio ~9,7 M€ in 2 CIG misti».

## A7. Anomalie — Taranto 723 M€ e ARIA 580 M€

- **Tesi**: Taranto = valore del padre copiato; ARIA plausibile da verificare.
- **Prove**: Taranto B280091A05: `oggetto_lotto` = testo della convenzione DTD-PSN, importo 723.300.000 identico al padre → errore materiale. ARIA BAFE270F81 (2026, CPV 72260000-5, «messa a disposizione delle risorse cloud e della gestione infrastrutturale (c.d. servizi di outsourcing infrastrutturale)»): **nessun atto ARIA/Regione Lombardia trovato** (ricerche web e TED); TED 344848-2026 (sha256 `460f8a3f731850b4590d4128352f89fc93196db99cf00becff2c29f48373ff63`) è un'altra gara ARIA (supporto alla Direzione acquisti, 5,15 M€), prova negativa. Atti ASST Mantova 2023 (non archiviati) indicano la migrazione della sanità lombarda sul «multi-cloud ibrido» di ARIA: rende plausibile un outsourcing pluriennale ARIA→PSN, non lo prova. Termine di paragone: 580 M€ = 128 % dei ricavi PSN 2025.
- **Esito**: Taranto **regge**; ARIA **non verificato** (resta R).
- **Correzione**: escludere ARIA dalle somme finché non c'è l'atto (decreto ARIA o DGR sul Contratto di Utenza); presentare i totali PSN con e senza.

## A8. Somme degli attuativi oltre i massimali

- **Tesi**: eccedenza dovuta a proroghe, addendum, doppi CIG.
- **Attacco**: misura sul CSV di lavoro di (a) duplicati stessa SA + stesso importo e (b) oggetti con proroga/addendum/estensione/integrazione/quinto/rinnovo.
- **Prove** (script inline, streaming sul CSV, `nice`): lotto 1: eccedenza 311 M€ (961 vs 650); duplicati 3,8 M€; proroghe/estensioni 106 CIG, 44,4 M€. Lotto 3: eccedenza 198 M€; duplicati 1,4; proroghe 10,3. Lotto 4: eccedenza 178 M€; duplicati 2,4; proroghe 7,2. Trenitalia: duplicati 4,9; proroghe 3,6. PSN: duplicati 3,8; proroghe 6,4.
- **Esito**: la spiegazione **cade in gran parte**: proroghe e duplicati espliciti coprono al massimo ~15 % dell'eccedenza del lotto 1 e ~6 % dei lotti 3/4. Restano ipotesi non provate: importi dichiarati comprensivi di opzioni, contratti non eseguiti per intero, plafond rimodulati, CIG di adesione + CIG del contratto esecutivo.
- **Correzione**: nei dossier «eccedenza non spiegata»; usare il massimale (+ variante) come tetto per qualsiasi somma.

## A9. Trenitalia → FSTechnology e cloud pubblico

- **Tesi**: AQ intragruppo; cloud acquistato a valle, prodotti ignoti.
- **Attacco**: FSTechnology ha un AQ diretto con Microsoft per Azure.
- **Prove**: TED 139007-2023, https://ted.europa.eu/it/notice/139007-2023/xml, sha256 `5cdbfebd0c71a27ac362e4542412e5341be712bd240a8245ad45e738315eb238`: «Microsoft Azure Committed To Consume (MACC) per le Società del Gruppo Ferrovie dello Stato Italiane», LIN FST 97/2022, CIG 9481341A1A, aggiudicato il 10/02/2023 a Microsoft Ireland Operations Limited, acquisto diretto senza reseller; proroga di 12 mesi legata al trasferimento in Azure degli ambienti di produzione. Riferiti, non archiviati: migrazione in cloud SAP di oltre 30 sistemi (news SAP Italia, 2026); Microsoft 365 Copilot per oltre 50.000 dipendenti FS (stampa).
- **Esito**: «prodotti non identificabili» **cade** come affermazione generale; trattare l'AQ Trenitalia come intragruppo **regge** e si rafforza (FSTechnology compra dal mercato con CIG propri). Nessun atto FS sull'AQ 7991036B82 trovato: «da-verificare» corretto.
- **Correzione**: escludere 7991036B82 dal numeratore cloud (intragruppo); contare a parte CIG 9481341A1A come Azure EXTRA-UE (importo da BDNCP); evitare il doppio conteggio fra contratti applicativi FST e ordini puntuali.

## A10. Regola «due fonti indipendenti, una della stazione appaltante»

- PSN: identificazione V2 **regge** (TED Difesa Servizi per PCM + BDNCP + Guida). Catalogo: prima solo concessionario; ora **V2** col PEF pubblicato da presidenza.governo.it. Stipula 24/08/2022: fonte unica PSN → V a fonte unica, come scritto.
- SPC lotti 1/3/4: la «fonte della SA» è solo BDNCP (dati dichiarati da Consip all'ANAC); le altre fonti sono aderenti. Per CIG/aggiudicatario è difendibile; per il **contenuto no**: nessun documento Consip. «Verificato» va limitato all'identificazione (**regge con riserva**). Lotto 3: fonte AgID non archiviata → R, corretto nel dossier.
- Trenitalia: «da-verificare» corretto.
- `attuativi_convenzioni.py`: il CSV prodotto ha 777 attuativi PSN con legame contro 786 nel dossier: riallineare prima di pubblicare (**regge con riserva**).

## Fonti nuove archiviate (server, `archivio/manifest.jsonl`)

| URL | sha256 | Tipo |
|---|---|---|
| https://www.polostrategiconazionale.it/app/uploads/2026/07/Libro-PSN-2025.pdf | b8fe9ec1b4becdbf07cf837cac4f5ef26621bda85c7bfa1162773bf9a7ed64ed | concessionario (bilancio integrato 2025) |
| https://presidenza.governo.it/AmministrazioneTrasparente/BandiContratti/Procedure_LavoriFornitureServizi/AvvisiBandiInviti/PoloStrategicoNazionale/Allegato_3___sub_3___Proposta_PSN_Relazione_illustrativa_PEF_2.0.pdf | 4134d48cbea43462cdaeb9e88aa85e70901cad97a5b241a0726ebfedcdf85b07 | proposta del promotore pubblicata dal concedente (PCM) |
| https://ted.europa.eu/it/notice/139007-2023/xml | 5cdbfebd0c71a27ac362e4542412e5341be712bd240a8245ad45e738315eb238 | stazione appaltante (gruppo FS) |
| https://ted.europa.eu/it/notice/344848-2026/xml | 460f8a3f731850b4590d4128352f89fc93196db99cf00becff2c29f48373ff63 | ARIA, non pertinente (prova negativa) |

Nota operativa: sul server `git pull` è bloccato da un `tools/verifiche/attuativi_convenzioni.py` non tracciato che sarebbe sovrascritto; non toccato.
