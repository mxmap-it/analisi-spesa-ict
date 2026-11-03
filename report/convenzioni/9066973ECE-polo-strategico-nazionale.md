# Polo Strategico Nazionale (CIG 9066973ECE) — dossier analitico

Versione 0.1 — 2026-11-03 — #55. Stato: bozza, da sottoporre a revisione avversariale (DECISIONI.md, 2026-11-03).
Legenda: **V** = verificato su documento archiviato (sha256 in §7); **V2** = verificato con due fonti indipendenti di cui una della stazione appaltante/concedente; **R** = riferito (terzi o fonte unica), da verificare.

## 1. Sintesi

- Concessione in PPP (13 anni, dal 24/08/2022) fra DTD-PCM e Polo Strategico Nazionale S.p.A.; le PA aderiscono con Contratti di Utenza (max 10 anni) **(V2)**.
- Il catalogo ha quattro famiglie: **Industry Standard** (housing, hosting, IaaS, PaaS, CaaS nei 4 DC PSN), **Hybrid Cloud on PSN site** (Azure Stack HCI + Azure Arc), **Secure Public Cloud** (region italiane di Azure, Google Cloud, poi AWS e Oracle), **Public Cloud PSN Managed** (Oracle Alloy nei DC PSN; Google nella Guida 2024) **(V)**, più servizi di migrazione e professionali.
- In BDNCP: **786 CIG attuativi** collegati al padre, **4,89 mld €** di importi dichiarati (2022-2026), più 585 CIG «orfani» che citano il PSN senza legame al padre; un CIG riporta per errore l'intero valore della concessione (723,3 M€).
- Asse A (cloud): **misto**. Housing (non cloud), hosting dedicato (infrastruttura, non cloud in senso NIST), IaaS/PaaS/CaaS (cloud), migrazione (servizi professionali). Quote **non stimabili** dagli oggetti dei CIG: solo 4 su 786 nominano il Secure Public Cloud.
- Asse B (giurisdizione del prodotto): **IT** per Industry Standard, con dipendenze tecnologiche extra-UE (VMware Tanzu, Oracle DB, Red Hat); **EXTRA-UE (USA)** per Secure Public Cloud, PSN Managed e Hybrid. A livello di singolo CIG il bucket resta **incerto** finché non si legge il Progetto del Piano dei Fabbisogni.

## 2. Identificazione

| Campo | Valore | Fonte | Livello |
|---|---|---|---|
| CIG | 9066973ECE | Guida alla Convenzione (PSN); bando TED 57802-2022; delibera ARERA 34/2025; BDNCP | V2 |
| CUP | J51B21005710007 | Guida alla Convenzione | V |
| Stazione appaltante / concedente | Bando pubblicato da Difesa Servizi S.p.A. per la PCM; concedente DTD-PCM. In BDNCP la SA del CIG è «Presidenza del Consiglio dei Ministri» | TED 57802-2022; Guida; BDNCP | V2 |
| Oggetto | PPP per la realizzazione e gestione del Polo Strategico Nazionale (art. 33-septies d.l. 179/2012) | TED 57802-2022; BDNCP; Guida | V2 |
| Aggiudicatario | RTI TIM (mandataria), CDP Equity, Leonardo, Sogei (BDNCP, aggiudicatari); poi la società di progetto Polo Strategico Nazionale S.p.A. (Guida) | BDNCP aggiudicatari; Guida; TED 492519-2022 | V2 |
| Stipula convenzione | 24/08/2022 | Guida alla Convenzione | V (fonte unica, del concessionario per conto del concedente) |
| Durata | 13 anni (3 di allestimento + 10 di esercizio); Contratti di Utenza fino a 10 anni | Guida | V |
| Valore in BDNCP | 723.300.000 € (importo del lotto del CIG padre) | BDNCP | V (fonte unica); il valore dei Contratti di Utenza non è un massimale contrattuale chiuso |
| Data center | Region Nord: Rozzano, Santo Stefano; Region Sud: Acilia, Pomezia | Guida; Presentazione 04/2026 («4 DC in doppia region Milano e Roma») | V2 (stesso autore: PSN) |

Nota: la Guida e la Presentazione sono entrambe di PSN S.p.A. (concessionario). Per il «verificato» della regola 2026-11-03 servirebbe un documento del DTD (es. convenzione e allegati su innovazione.gov.it): non archiviato in questa sessione → i campi «solo Guida» restano V a fonte unica.

## 3. Cosa contiene

Dalla Guida alla Convenzione (ed. luglio 2024) e dall'Allegato B – Annesso 3 «Descrizione nuovi servizi» (atto aggiuntivo, marzo 2025) e dalla Presentazione dei servizi a listino (04/2026):

| Famiglia | Servizi | Dove gira | Tecnologia / produttore | Cloud? | Giurisdizione del prodotto | Livello |
|---|---|---|---|---|---|---|
| Industry Standard – Housing | spazio fisico nei DC PSN, server della PA | DC PSN | — | **No** (colocation) | IT (erogazione) | V |
| Industry Standard – Hosting | server dedicati a noleggio, rack condivisi o privati | DC PSN | hardware non specificato | **No/parziale** (infrastruttura dedicata, non servizio cloud NIST) | IT | V |
| Industry Standard – IaaS (Private, Shared, Storage, GPU, DR) | VM, storage, BC/DR fra AZ e region | DC PSN | VMware vCloud citato nell'Annesso 3 («console tecnica VMware vCloud»); hypervisor non elencato per intero | Sì | IT con dipendenza tecnologica USA (VMware/Broadcom) | V (presenza VMware) / R (quota) |
| Industry Standard – PaaS (DB, IAM, Big Data, AI) | Oracle DB, MySQL, PostgreSQL, MariaDB, MongoDB…; AI «basato su opensource» | DC PSN | Oracle (USA), MongoDB (USA), open source | Sì | IT con dipendenze USA per i DB commerciali | V |
| Industry Standard – CaaS | Licensed CaaS (VMware Tanzu), CaaS «Opensource» (Red Hat OpenShift) | DC PSN | Broadcom/VMware (USA), Red Hat/IBM (USA) | Sì | IT con dipendenza USA | V |
| Hybrid Cloud on PSN site | HCI dedicata nei DC PSN, registrata nelle subscription Azure della PA, gestita col control plane Azure (Azure Arc), parte del management plane su servizi cloud Azure | DC PSN + cloud Azure | Microsoft (USA) | Sì | **EXTRA-UE (USA)** | V |
| Secure Public Cloud | servizi pubblici degli hyperscaler da region italiane + chiavi esterne (HSM nei DC PSN) + backup nel cloud privato PSN | region italiane degli hyperscaler | Guida 2024: Microsoft Azure e Google Cloud; Annesso 3 (03/2025): introduzione di **AWS** «come quarto Hyperscaler»; Presentazione 04/2026: Azure, Google Cloud, AWS, Oracle | Sì | **EXTRA-UE (USA)** | V |
| Public Cloud PSN Managed | region dedicate nei DC PSN | DC PSN | Guida 2024: «Google ed Oracle» erogati da DC PSN; Annesso 3 e Presentazione 2026: **Oracle Alloy** (prima OCI Dedicated Region/DRCC), «hardware e software sviluppati da Oracle» ospitati nei DC PSN | Sì | **EXTRA-UE (USA)** (software e aggiornamenti del produttore) | V |
| Migrazione e servizi professionali | piano di migrazione, «servizi professionali» opzionali a listino | — | — | No (servizi) | segue il fornitore (IT) | V |

Region degli hyperscaler citate (Annesso 3): Google europe-west8 (Milano) ed europe-west12 (Torino); Azure Italy North (Milano). Region AWS e Oracle: non citate con nome nei documenti letti → R.

**Contraddizione da segnalare.** La Guida (2024) scrive che il PSN Managed è basato su Google e Oracle «erogati da Data Center del PSN»; la base di conoscenza (allineata all'Osservatorio, 29/10/2026) scrive che Google gira nelle region Google e solo Oracle Alloy nei DC PSN; la Presentazione 04/2026 intesta il PSN Managed «PSN + Oracle» e mette Google nel Secure Public Cloud. Lettura proposta: nel listino attuale il PSN Managed è solo Oracle Alloy; la dicitura Google della Guida 2024 è superata. Da far confermare sul listino XLS.

**Hybrid Cloud on PSN site** compare nella Guida e nella Presentazione 2026 (verificato: la nota «da verificare sul listino» della base di conoscenza si può chiudere sulla presenza nel catalogo, non sui volumi venduti).

## 4. Analisi degli attuativi (BDNCP)

Script: `tools/verifiche/attuativi_convenzioni.py` (sul server, `nice`, streaming con `righe_cig`, ultima versione per CIG fra file annuali 2007-2025 e delta mensile). Esito in `lavoro/convenzioni-55/`. Importi = `importo_lotto` dichiarato (valore del contratto, non spesa liquidata).

| Anno | CIG attuativi | € dichiarati |
|---|---:|---:|
| 2022 | 9 | 20.496.685 |
| 2023 | 165 | 932.548.705 |
| 2024 | 272 | 2.026.643.399 |
| 2025 | 241 | 1.065.423.052 |
| 2026 (delta) | 99 | 849.296.097 |
| **Totale** | **786** | **4.894.407.938** |

**Importi anomali.**
- `B280091A05` (Museo archeologico nazionale di Taranto, 2024): 723.300.000 € = valore del CIG padre copiato nell'attuativo. Errore materiale da escludere.
- `BAFE270F81` (ARIA S.p.A., 2026): 580.384.124 €, «messa a disposizione delle risorse cloud e della gestione infrastrutturale (outsourcing infrastrutturale)», aggiudicatario PSN S.p.A. Plausibile ma fuori scala (11,9 % del totale): da verificare sull'atto ARIA.
- 45 attuativi ≥ 20 M€ per 3,22 mld € (66 % del totale). Senza i due casi sopra: 784 CIG, ~3,59 mld €.
- Ripetizioni: lo stesso ente compare con più CIG (Difesa, Turismo, MAECI, ARIA, Azienda Zero) perché ogni Progetto dei Fabbisogni/Wave ha un CIG. Non sono doppi conteggi, ma neanche spesa annua: sono valori pluriennali fino a 10 anni.

**Classi di oggetto** (regex sull'oggetto gara+lotto; un CIG può stare in più classi):

| Classe | n | € |
|---|---:|---:|
| sviluppo/manutenzione/realizzazione (spesso è solo il titolo della convenzione: «realizzazione e gestione di una nuova infrastruttura…») | 341 | 1,88 mld |
| nessuna parola chiave (es. «adesione PSN») | 248 | 1,47 mld |
| «cloud» | 231 | 1,26 mld |
| migrazione | 153 | 0,90 mld |
| servizi professionali | 32 | 126 M |
| hosting | 4 | 53 M |
| housing | 3 | 9,9 M |
| secure public cloud | 4 | 9,8 M |
| azure/microsoft | 4 | 14,8 M |
| PSN managed | 1 | 8,4 M |
| AWS | 1 | 0,9 M |
| google | 0 | 0 |

Conclusione: **l'oggetto del CIG non dice quale famiglia di servizi si compra**. Meno dell'1 % dei CIG nomina un hyperscaler. La ripartizione Industry Standard / hyperscaler si può ottenere solo dai Progetti dei Piani dei Fabbisogni (allegati ai Contratti di Utenza) o da un dato aggregato PSN/DTD.

**Orfani**: 585 CIG con «PSN/Polo strategico/secure public cloud» nell'oggetto ma senza `cig_accordo_quadro` = 9066973ECE (276,9 M€). Contengono falsi positivi (es. «PSN 2023-2027» = Piano Strategico Nazionale PAC, Regione Campania 32 M€) e veri attuativi senza legame (AGCOM 14,8 M€, Carabinieri forestali 11,8 M€, Regione Abruzzo 17,9 M€). Non sommabili senza revisione.

## 5. Classificazione proposta

- **Asse A (è cloud?)**: CIG padre = massimale, non spesa (escluso dal conteggio). Attuativi = **misto, incerto per singolo CIG**. Housing = non cloud; hosting dedicato = infrastruttura esterna (datacenter esterno, non cloud); IaaS/PaaS/CaaS/SPC/Managed/Hybrid = cloud; migrazione = servizi. Quote: **non stimabili** con le fonti lette. Confidenza: alta sulla composizione del catalogo, nulla sulle quote.
- **Asse B (giurisdizione del prodotto)**:
  - Industry Standard: **IT** (criterio del 29/10/2026: DC in Italia, operatore italiano a controllo italiano), con dipendenze tecnologiche USA (VMware/Broadcom, Oracle, Red Hat, MongoDB) da registrare come tali. Confidenza media-alta.
  - Secure Public Cloud (Azure, Google, AWS, Oracle), Public Cloud PSN Managed (Oracle Alloy), Hybrid (Azure Arc): **EXTRA-UE (USA)**. Confidenza alta.
  - Attuativo senza Progetto dei Fabbisogni letto: **incerto** (bucket «IT o EXTRA-UE»), non IT per default.
- Stato proposto per il padre: resta **verificato** (identificazione); nuovo campo «composizione: misto, quote ignote».

## 6. Assunzioni esplicite e limiti

1. Documenti PSN (Guida, Annesso 3, Presentazione) sono del concessionario; non ho archiviato la convenzione firmata né il listino XLS del DTD/PSN.
2. «Hosting dedicato» classificato non cloud: è una scelta di metodo (decisione di Fabio), non un fatto.
3. Il criterio «IT» per Industry Standard dipende dalla decisione del 29/10/2026 (operatore italiano a controllo italiano); il socio TIM ha azionisti esteri, non valutato qui.
4. Importi BDNCP = valore dichiarato pluriennale, non pagato; nessuna deduplica fra CIG di Wave successive dello stesso ente oltre al CIG.
5. Regex delle classi grezze (la parola «realizzazione» cattura il titolo della convenzione).
6. Le region AWS/Oracle non sono nominate nei documenti letti.

## 7. Fonti

| URL | sha256 | Cosa conferma | Tipo |
|---|---|---|---|
| https://www.polostrategiconazionale.it/app/uploads/2025/08/PSN_Guida-alla-Convenzione_.pdf | 8b7e7ef454cb4679a8737e77c441a72836b240332e5d49f090b25e75e54575f6 | CIG, CUP, stipula 24/08/2022, durata, 4 DC, 4 famiglie di servizi, Hybrid Azure Arc, SPC Azure+GCP | concessionario (per il concedente) |
| https://www.polostrategiconazionale.it/app/uploads/2025/08/Listino-descrizione-.pdf | bd605cf7287cb1dd27e841212e5aa529822ee1479fb9cabb62b9d815cb804f34 | Allegato B Annesso 3 (03/2025): Oracle Alloy nei DC PSN, AWS quarto hyperscaler, region Milano/Torino, VMware vCloud, Red Hat | concessionario (allegato all'atto aggiuntivo) |
| https://www.polostrategiconazionale.it/app/uploads/2026/04/Presentazione-servizi-a-listino-Polo-Strategico-Nazionale-1.pdf | 70344b74f2eab896aeba2e26622ba0858f30fd17ef00f99b2c20291eca7461ef | PSN Managed = PSN+Oracle; SPC = Azure/Google/AWS/Oracle; Hybrid = Azure | concessionario |
| https://www.polostrategiconazionale.it/app/uploads/2025/06/PSN_Bilancio_esercizio_2024-25-LowRes.pdf | 5be1ea22301b05d11e17428b3320bb74e367c78b547c7ad9e924d8c7834a3937 | finanziamenti PNRR per la migrazione; nessuna ripartizione dei ricavi per famiglia | concessionario |
| https://ted.europa.eu/it/notice/57802-2022/xml | 05c72e72723c6256ea040092ccb14b31f01985a6357b2d9c478c5a48812915e3 | bando PPP PSN, CIG 9066973ECE | stazione appaltante (Difesa Servizi per PCM) |
| https://ted.europa.eu/it/notice/492519-2022/xml | aec5af83743e3e0843949b1f0fc1997fed5ff47550466058f8a0c57bd57a0f55 | aggiudicazione, stesso CIG | stazione appaltante |
| https://www.arera.it/fileadmin/allegati/docs/25/34-25dagr.pdf | a5b662e2f14948a8ab4a5f1deab72f39e78895e058fbac0037b6e3fd820efeb2 | adesione di un ente, CIG 9066973ECE | terzo (ente aderente) |
| https://cloud.italia.it/strategia-cloud-pa/polo-strategico-nazionale/ | 1cba25c36f82f845ee4e0b8de656ba04b4281eac132f99ec40a16f6baf00dd84 | pagina DTD sul PSN | concedente |
| BDNCP ANAC, dataset cig-2007…2025 + delta, aggiudicatari (mirror in `archivio/mirror/dati.anticorruzione.it/`) | per file in `archivio/manifest.jsonl` | 786 attuativi, importi, RTI aggiudicatario | terzo (ANAC, dichiarazioni delle SA) |

## Proposta per iniziative_ict.yaml

```yaml
- cig: 9066973ECE
  iniziativa: Polo Strategico Nazionale (PPP, Presidenza del Consiglio)
  categoria: psn
  stato: verificato            # identificazione; composizione: misto
  asse_cloud: misto-incerto     # housing non cloud; hosting dedicato non cloud; IaaS/PaaS/CaaS/SPC/Managed/Hybrid cloud
  asse_giurisdizione: per-servizio   # Industry Standard IT (dip. USA: VMware, Oracle, Red Hat); SPC/Managed/Hybrid EXTRA-UE
  attuativo_default: incerto    # serve il Progetto del Piano dei Fabbisogni
  dossier: report/convenzioni/9066973ECE-polo-strategico-nazionale.md
  documenti_aggiuntivi:
  - url: https://www.polostrategiconazionale.it/app/uploads/2025/08/PSN_Guida-alla-Convenzione_.pdf
    sha256: 8b7e7ef454cb4679a8737e77c441a72836b240332e5d49f090b25e75e54575f6
  - url: https://www.polostrategiconazionale.it/app/uploads/2025/08/Listino-descrizione-.pdf
    sha256: bd605cf7287cb1dd27e841212e5aa529822ee1479fb9cabb62b9d815cb804f34
  anomalie_bdncp: [B280091A05 (723,3 M€ = valore padre), BAFE270F81 (580 M€ ARIA, da verificare)]
```
