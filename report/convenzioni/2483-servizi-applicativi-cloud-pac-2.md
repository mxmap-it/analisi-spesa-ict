# Dossier: Consip «Servizi applicativi in ottica cloud e Demand/PMO per le PA centrali», 2ª edizione (ID 2483)

Versione 1.0, 3/11/2026, ticket #55. Lotti: **91918889EE** (lotto 1, servizi applicativi) e **9191898231** (lotto 2, demand e PMO).
Legenda: **V** = verificato da noi su documento archiviato (sha256 in §7); **R** = riferito o inferito, da verificare.

## 1. Sintesi

1. ID 2483 è un accordo quadro Consip a due lotti: lotto 1 servizi applicativi, base d'asta 3,0 mld e massimale 3,6 mld con il +20 %; lotto 2 demand e PMO, 300 M e 360 M. Il lotto 1 è stato aggiudicato a 10 RTI, tra cui Accenture, IBM ed Enterprise Services (V).
2. **«In ottica cloud» non vuol dire che si compra cloud.** Gli enti comprano servizi professionali: sviluppo e manutenzione evolutiva (SVI), supporto specialistico (SS) e gestione del portafoglio applicativo (GA). Li pagano a tariffa secondo il Piano dei fabbisogni (V da due contratti esecutivi). Né il bando né i contratti prevedono IaaS, PaaS o SaaS.
3. BDNCP: **556 attuativi dichiarano 31,26 mld**. Di questi, **28,32 mld (90,6 %) vengono da 23 attuativi da ≥50 M**. Fra questi, 9 sono della Banca d'Italia e valgono 27,21 mld: ciascuno vale 3,0–3,21 mld, cioè la base d'asta dell'intero lotto. Sono massimali, non spesa. Sotto i 50 M restano **2,94 mld in 533 attuativi** (V, misura nostra).
4. La migrazione al cloud c'è, ma è minoritaria: 4 attuativi su 556 la nominano esplicitamente, per 6,4 M (soglia minima). La quota reale è sconosciuta perché l'oggetto del CIG è generico (R).
5. Proposta per l'imbuto: S5, **consulenza IT applicativa**, con una sotto-quota di **consulenza-migrazione-cloud** da riconoscere per attuativo. Sull'asse cloud la spesa è **esclusa con certezza** come spesa cloud diretta. Confidenza media: manca il capitolato tecnico (§6).

## 2. Identificazione

| Campo | Valore | Fonte | Stato |
|---|---|---|---|
| CIG lotto 1 | 91918889EE, «LOTTO 1 - SERVIZI APPLICATIVI», CPV 72211000-7 | BDNCP (CIG padre); bando TED 221218-2022; contratto esecutivo ISTAT («CIG Accordo Quadro: 91918889EE») | V |
| CIG lotto 2 | 9191898231, «LOTTO 2 - SERVIZI DI DEMAND E PMO», CPV 72224000-1 | BDNCP (CIG padre, stesso numero gara 8526979 del lotto 1) | V (BDNCP) / R (manca il CIG nel TED) |
| Pubblicazione | GUUE S 082 del 27/04/2022, GURI n. 49 del 29/04/2022; BDNCP 27/04/2022 | TED 221218-2022; premesse dei contratti MiTur e ISTAT | V |
| Valori | totale 3,96 mld; lotto 1: base d'asta 3,0 mld, massimale **3,6 mld** (+20 %); lotto 2: 300 M, massimale **360 M** | TED 221218-2022 («Lotto 1: € 3.000.000.000,00 … incrementato fino al 20 %»); BDNCP importo_lotto 3.600.000.000 e 360.000.000 | V |
| Aggiudicatari lotto 1 | RTI Accenture (con Avanade, Engineering D.HUB, EY, InfoCert, BeSharp, Cloudmind…), RTI Enterprise Services Italia, RTI IBM Italia e altri (53 operatori nell'elenco aggiudicatari BDNCP) | TED 717702-2023; BDNCP aggiudicatari; contratto MiTur | V |
| Aggiudicatari lotto 2 | HSPI, Intellera, Deloitte, Advant, Business Changers, LUISS, PRS, S3K, SCS Azioninnova (BDNCP) | BDNCP aggiudicatari | R (TED da archiviare) |
| Durata | contratti esecutivi lotto 1 fino a **60 mesi**, compresi al massimo 12 di garanzia | TED 221218-2022; contratto MiTur: 24 mesi | V |
| Attivazione | lotto 1 attivo dal 21/12/2022 | R (ricerca web, non archiviata) | R |

## 3. Cosa contiene

- **Servizi a persone, non infrastruttura.** I contratti esecutivi archiviati elencano solo:
  - MiTur (CIG 959949490B): «Sviluppo e Manutenzione Evolutiva di Software (SVI); Supporto Tecnico-Specialistico ICT (SS); Gestione del Portafoglio Applicativo (GA)»;
  - ISTAT (contratto 73/2025): SVI e SS.

  I corrispettivi sono «calcolati sulla base del dimensionamento dei servizi indicato nel Piano dei fabbisogni», con le tariffe dell'allegato «Corrispettivi e Tariffe» (V).
- **Nessuna infrastruttura cloud nel perimetro.** Una ricerca testuale nel bando TED (hosting, licenze, infrastruttura, IaaS, PaaS, SaaS) non trova nulla oltre al nome della gara. Il lotto 1 ha CPV 72211000-7, programmazione di software (V, BDNCP). Il cloud su cui girano le applicazioni si compra altrove: per la 1ª edizione (ID 2212) Consip lo dice in chiaro, vedi il dossier 2212. Il re-hosting rientra nella gara Public Cloud ID 2213; gli applicativi vanno sui CSP qualificati AgID. Per ID 2483 la stessa architettura è **R per continuità**: lo dicono la denominazione identica e il «Cloud Enablement Kit» citato nelle rettifiche.
- **Migrazione.** Le rettifiche Consip (rettifica 2) rinviano ai servizi del «Capitolato Tecnico Speciale Lotto 1 – Servizi Applicativi» e citano una «soluzione con architettura a microservizi». Che esista un servizio di «Migrazione applicativa al cloud» nel lotto 1 è **R**: c'era nella 1ª edizione (§5.3 del capitolato speciale ID 2212, V) e alcuni attuativi BDNCP lo nominano (sotto). Il capitolato ID 2483 non è stato trovato in forma archiviabile (§6).
- **Chi fornisce il cloud.** Negli RTI ci sono partner di hyperscaler: Avanade (Microsoft), BeSharp e Cloudmind (AWS), secondo quanto è noto sul mercato (R). La loro presenza non dice quale cloud usi l'ente: lo dice il contratto cloud separato (PSN, ID 2213, SPC Cloud).

## 4. Analisi degli attuativi (BDNCP, 3/11/2026)

Script: `tools/analisi/attuativi_convenzioni.py`. Gira in streaming, con nice e ionice; picco di circa 20 MB di RSS. Esito in `report/convenzioni/prove-servizi-applicativi/`: attuativi.csv (sha256 5d9bcf85…), riepilogo.json (7774cfbc…). Per ogni CIG vale l'ultima versione, annuale o delta. Non c'è filtro per CPV: si contano tutti i figli che dichiarano `cig_accordo_quadro` uguale al padre.

### Lotto 1, 91918889EE: 556 attuativi, 31.258,8 M€ dichiarati

| Anno | N | M€ dichiarati |
|---|---|---|
| 2022 | 3 | 22,1 |
| 2023 | 82 | 669,0 |
| 2024 | 150 | **19.026,2** |
| 2025 | 207 | **10.895,1** |
| 2026 | 114 | 646,4 |

| Fascia d'importo | N | M€ |
|---|---|---|
| < 100 k | 29 | 1,1 |
| 100 k – 1 M | 129 | 65,6 |
| 1 – 10 M | 293 | 1.042,8 |
| 10 – 50 M | 82 | 1.827,9 |
| **≥ 50 M** | **23** | **28.321,4** |

**Perché 28,3 dei 31,3 mld sono massimali (R22).**
- Banca d'Italia: 9 attuativi per **27.210 M**. Due ne valgono uno l'intero massimale con il +20 %:
  - B5A2C1471F, «AQ12/24 servizi professionali SVI», 3.210 M;
  - B489E1897E, B48B805E83, B48AC2FA15, B49A5A7853, B49A8866DE, B49B512180, B5BE68B94E e B6438A7BB3, 3.000 M ciascuno, che è la **base d'asta dell'intero lotto 1** (TED: 3,0 mld).

  Insieme valgono 7,6 volte il massimale del lotto, 3,6 mld (V). Le sigle «AQ05/24 … AQ04/25» fanno pensare che la Banca d'Italia stipuli propri accordi quadro derivati e scriva in BDNCP il valore del lotto Consip (R).
- Gli altri 14 attuativi ≥50 M valgono 1.111 M. Sogei 8 per 627 M, poi Infratel 180 M, Cassa forense 67 M, Interno 63 M, MiC 62 M, ACN 58 M e MASE 54 M. Sono **plausibili** come contratti veri: il più alto resta sotto il 5 % del massimale (R).
- Sotto i 50 M: **533 attuativi, 2.937,5 M€**, mediana 2,44 M. È la stima difendibile della spesa contrattualizzata. Resta un tetto: l'importo del CIG è il valore del contratto esecutivo, non lo speso.
- **Riconciliazione con R22.** R22 riporta 647 attuativi, 35,2 mld, di cui 31,7 ≥50 M e 3,6 <50 M. **Non lo riproduciamo.** Sul mirror di oggi troviamo 556 / 31,26 / 28,32 / 2,94. Il CSV committed `padri-ict.csv` (filtro CPV ICT) dà 537 / 31,0 mld. La differenza va spiegata prima di pubblicare R22: snapshot diversi, doppi conteggi annuale+delta o altro (§6). La sostanza regge: oltre il 90 % del dichiarato sono massimali.

**Classi d'oggetto** (regex, un attuativo può stare in più classi):
- «cloud» compare in 177 attuativi (4.655 M), ma quasi sempre è il nome della convenzione («in ottica cloud»).
- Senza le formule generiche, **14 attuativi da 46,2 M** parlano davvero di cloud. Esempi:
  - Sogei «servizi applicativi per il PSN», 4,0 M e 0,66 M;
  - Consiglio di Stato «servizi cloud», 4,5 M;
  - CONSOB «passaggio al cloud dell'infrastruttura informatica», 2,47 M.
- **Migrazione esplicita: 4 attuativi, 6,4 M**:
  - ENAC «migrazione cloud perimetro TIME», 1,5 M;
  - PCM «re-architect e supporto migrazione al PSN», 0,88 M;
  - DTD «migrazione cloud native del parco applicativo civile», 3,0 M;
  - Studiare Sviluppo, 1,05 M.
- Nessuna classe: 225 attuativi. Per lo più «servizi applicativi per …» o «servizi professionali».
- Prodotti nominati: 19 attuativi (190,7 M), soprattutto SAP e Oracle in manutenzione.

Fornitori per importo (con i massimali): IBM 18,1 mld (gonfiato dai massimali Banca d'Italia), Accenture 4,0 mld, NTT Data 3,5 mld, Capgemini 3,1 mld.

### Lotto 2, 9191898231: 136 attuativi, 337,9 M€

- Per anno: 2023 11 / 17,9 M; 2024 32 / 55,5 M; 2025 48 / 193,9 M; 2026 45 / 70,5 M.
- Un solo attuativo ≥50 M: Banca d'Italia B5A874258D, «supporto alla misura del software applicativo», 120 M. È un terzo del massimale del lotto, quasi certamente un altro AQ derivato (R).
- Sotto i 50 M: 135 attuativi per 217,9 M.
- Classi: 102 attuativi sono PMO/demand; nessun attuativo cloud o migrazione al netto delle formule generiche.
- Fornitori: HSPI 80 attuativi (249 M), Intellera 40 (65,5 M).

## 5. Classificazione proposta per l'imbuto

| Lotto | Categoria | Asse «è cloud?» | S5 | Confidenza |
|---|---|---|---|---|
| 91918889EE | servizi-applicativi | **escluso** come spesa cloud diretta (servizi professionali; l'infrastruttura si compra altrove) | consulenza IT **applicativa**; sotto-quota **consulenza-migrazione-cloud** per attuativo (soglia minima misurata: 6,4 M su 2.937 M = 0,2 %; con i 14 attuativi cloud-specifici 46,2 M = 1,6 %) | media (manca il capitolato) |
| 9191898231 | pmo-demand | escluso | consulenza IT di governo e PMO (non infrastrutturale) | alta (CPV 72224000-1; contratti) |

Regole operative proposte:
1. Escludere dalle somme gli attuativi con importo ≥ massimale del lotto/10 (≥ 360 M per il lotto 1): sono i 9 della Banca d'Italia. Gli attuativi 50–360 M si tengono, marcati «da verificare».
2. Mandare in S5 migrazione gli attuativi il cui oggetto cita migrazione, PSN o passaggio al cloud. Tutto il resto va in S5 applicativa.

## 6. Assunzioni e limiti

- **Capitolato tecnico generale e speciale ID 2483 non archiviati.** Su consip.it non abbiamo trovato l'URL pubblico: la pagina di gara si genera via JavaScript e il percorso che avevamo indovinato risponde 404. L'elenco dei servizi del lotto 1, compresa un'eventuale «migrazione applicativa al cloud», resta R. Va recuperato da acquistinretepa.it o da allegati di enti aderenti.
- Il lotto 2 è legato al TED solo tramite il numero gara BDNCP: il CIG 9191898231 non compare nel testo TED estratto.
- L'importo BDNCP è un valore dichiarato, non pagato. Anche sotto i 50 M possono esserci quote di massimale.
- Le classi d'oggetto vengono da regex su oggetti brevi. Sono soglie minime, non stime della quota di migrazione.
- Numeri diversi da R22 (vedi §4): R22 va riallineato, oppure va documentata la sua base.
- Primo run del 3/11: lo script usava `righe_cig("delta")`, che tiene tutto il delta in memoria (circa 10 GB di RSS). È stato corretto in streaming. Il secondo run dà esiti identici, con circa 20 MB.

## 7. Fonti

| URL | sha256 | Cosa conferma | Tipo |
|---|---|---|---|
| https://ted.europa.eu/it/notice/221218-2022/xml | 3ebb9f0758307324992f5feef3164920ef1567fb2992258af961168b7e840e0b | bando: lotti, basi d'asta (3,0 mld / 300 M), massimale +20 %, durata 60 mesi | stazione appaltante (Consip via GUUE) |
| https://ted.europa.eu/it/notice/717702-2023/xml | 9959a0bcf12102c082b9cdb28d55f23eb3aec752d8855b1e49366377907a92cc | aggiudicazione lotto 1: RTI Accenture, Enterprise, IBM… | stazione appaltante |
| https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID%202483%20-%20Rettifiche%20alla%20documentazione%202.pdf | 6d390d72e0847e77f0aa9b83e918ba60f36c800faead525a8c0c40a99778bce6 | struttura lotti, Capitolato Tecnico Speciale lotto 1 «Servizi Applicativi», microservizi | stazione appaltante |
| https://www.ministeroturismo.gov.it/wp-content/uploads/2023/06/Contratto-Esecutivo_ODA-AQ-ID2483_signed.pdf | 71da1e744e253de8635a2715a863a150cf83d10a76795fe377139cf854199853 | servizi SVI/SS/GA, corrispettivo da Piano dei fabbisogni, 24 mesi, RTI Accenture | terzo (ente aderente) |
| https://www.istat.it/wp-content/uploads/2025/10/Contratto-73-del-16-06-2025.pdf | 142d6aa6a86407ed101325c8b19dc335ccaa10efed6c31ee01125b4007b9f01d | CIG AQ 91918889EE, servizi SVI e SS, RTI Enterprise Services | terzo (ente aderente) |
| https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID%202212%20-%20Servizi%20applicativi%20in%20ottica%20cloud%20-%20Risposte%20ai%20chiarimenti.pdf | 0ca7e99890c96b6c50e43d3cd2379787fa5a5dc7ac79c5012f790d56368d0b2b | (1ª ed.) re-hosting in ID 2213, CSP qualificati AgID: architettura per continuità | stazione appaltante |
| BDNCP CIG e aggiudicatari (mirror ANAC) → `report/convenzioni/prove-servizi-applicativi/attuativi.csv` | 5d9bcf855e9c744fdef125d539a27bd51f909a88338c7aaf27657c1971349d2f | attuativi, importi, oggetti, fornitori | terzo (ANAC, dati inseriti dagli enti) |

## Proposta per iniziative_ict.yaml

```yaml
- cig: 91918889EE
  iniziativa: Consip AQ Servizi applicativi in ottica cloud e Demand/PMO PA centrali, seconda edizione (ID Sigef 2483), lotto 1 Servizi applicativi
  categoria: servizi-applicativi
  stato: verificato            # CIG↔lotto: TED Consip + BDNCP + contratto ISTAT
  s5: consulenza-it-applicativa
  s5_quota_migrazione: per-attuativo   # oggetto con migrazione/PSN/passaggio al cloud -> consulenza-migrazione-cloud
  cloud_diretto: escluso       # servizi professionali; infrastruttura acquistata con altri contratti (PSN, ID 2213, SPC Cloud)
  massimale_lotto: 3600000000
  soglia_massimale_attuativo: 360000000   # >= massimale/10: escluso dalle somme (9 attuativi Banca d'Italia, 27,21 mld)
  nota: '556 attuativi / 31,26 mld dichiarati, di cui 28,32 mld in 23 attuativi >=50 M; sotto 50 M 2,94 mld (3/11/2026). Servizi SVI/SS/GA (contratti MiTur, ISTAT). Capitolato tecnico da archiviare'
  documenti: [... i due TED esistenti +]
  - url: https://www.istat.it/wp-content/uploads/2025/10/Contratto-73-del-16-06-2025.pdf
    sha256: 142d6aa6a86407ed101325c8b19dc335ccaa10efed6c31ee01125b4007b9f01d
    cosa_conferma: 'contratto esecutivo ISTAT: CIG Accordo Quadro 91918889EE, servizi SVI e SS'
  - url: https://www.ministeroturismo.gov.it/wp-content/uploads/2023/06/Contratto-Esecutivo_ODA-AQ-ID2483_signed.pdf
    sha256: 71da1e744e253de8635a2715a863a150cf83d10a76795fe377139cf854199853
    cosa_conferma: 'contratto esecutivo MiTur ID 2483 lotto 1: SVI, SS, GA a tariffa da Piano dei fabbisogni'
- cig: 9191898231
  iniziativa: Consip AQ Servizi applicativi in ottica cloud e Demand/PMO PAC, seconda edizione (ID 2483), lotto 2 Demand e PMO
  categoria: pmo-demand
  stato: da-verificare         # BDNCP (stesso numero gara del lotto 1) + bando TED che descrive il lotto 2, ma il CIG non è nel TED
  s5: consulenza-it-governance
  cloud_diretto: escluso
  massimale_lotto: 360000000
  nota: '136 attuativi / 337,9 M; Banca d''Italia B5A874258D 120 M probabile AQ derivato'
```
