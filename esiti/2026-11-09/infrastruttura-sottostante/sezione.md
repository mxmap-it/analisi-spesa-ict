### Misura 1.2: su quale infrastruttura girano i «prodotti italiani» (v0.2, 9/11/2026, #43 #45)

**Verifiche** (nessuna rete; la seconda solo DNS):
- `nice .venv/bin/python tools/verifiche/infrastruttura_sottostante.py --data 2026-11-09` → `esiti/2026-11-09/infrastruttura-sottostante/infrastruttura.json`;
- `tools/verifiche/saas_infra_fornitori.py`, che estende il pilota DNS/AS `saas_infra_pilota.py`.

**Tabelle:** `config/saas_infrastruttura.yaml` (fornitori, v0.2), `config/saas_host.yaml` (domini dei servizi), `psn-ppdf.csv` (riepiloghi dei piani dei fabbisogni PSN).

**Terzo asse.** Accanto a prodotto e fornitore conta la giurisdizione di **chi gestisce l'infrastruttura** su cui gira il servizio: DC proprio in Italia, provider IT-UE oppure hyperscaler extra-UE.

#### 1. PSN (389,2 M€ della 1.2, di cui 368,6 M€ di ASL/AO)

**Fonte aggregata** [V, A]: *Libro PSN 2025*, bilancio integrato, sha256 b8fe9ec1…, p. 71-72 e 106.
- **Ricavi 2025:** 454,3 M€, di cui 360,7 M€ (79 %) da migrazione e servizi professionali.
- **Hyperscaler:** Secure Public Cloud (Azure, Google, AWS) 19,9 M€ + PSN Managed (Oracle Alloy / Exadata Cloud@Customer nei DC PSN) 4,5 M€. Insieme fanno **5,4 % dei ricavi e 27,3 % dei ricavi infrastrutturali** (2024: 2,6 % e 16,8 %).
- **Contratti firmati:** 3.853 M€, 60 % servizi professionali e 40 % canoni.
  - Il Secure Public Cloud è il 15 % dei canoni: PA centrali 24 %, PA locali 6 %, ASL/AO 7 %.
  - Le «Soluzioni Oracle PSN» sono il 14 % dei canoni, PA locali 20 %, ASL 24 %.

**Fonte per ente** [V, lettura visiva del Configuratore]: 12 schede del piano dei fabbisogni di ARES Sardegna (PDF sha256 524b568a…, p. 155-179) e USR Lazio (fef2aea8…).
- **Nessun Secure Public Cloud e nessun Hybrid.**
- In 11 ASL/AO su 12 c'è **Public Cloud PSN Managed Oracle** (Exadata Cloud@Customer, licenze BYOL): **34,9 % dei canoni** del SSR sardo, da 38 a 43 % per scheda.
- AREUS e USR Lazio sono a 0 %.
- È coerente con il Libro per le ASL: 7 % di SPC più 24 % di Oracle PSN fa 31 %.
- Contando la una tantum, l'hyperscaler pesa il 2,6 % del contratto ARES: la spesa è dominata dai servizi professionali.

**Quota hyperscaler sui canoni:**

| Enti | Basso | Centrale | Alto |
|---|---|---|---|
| ASL | 7 % (solo SPC, Libro) | **34,9 %** (misurata su ARES) | 43,3 % (scheda più alta) |
| Comuni e altri | 6 % | 13,2 % | 31 % |

**PSN 1.2 su hyperscaler:**
- se la migrazione segue l'infrastruttura (R-S1): **27 / 131 / 166 M€** (basso / centrale / alto);
- se la migrazione conta come servizio italiano: 5 / 53 / 99 M€.

**Avvertenze:**
- Il centrale estende **una sola regione (ARES, 12 schede)** a tutte le ASL.
- Il Managed Oracle gira **nei DC PSN in Italia**: è extra-UE per produttore e gestione (software, aggiornamenti, supporto Oracle), non per la collocazione dei dati.

**PSN in generale (#45):**
- circa **8 % del valore ordinato** su hyperscaler (~0,3 mld su 3,85);
- 5,4 % dei ricavi 2025 e 27 % dell'infrastruttura venduta nel 2025, in crescita.

#### 2. SaaS dei fornitori S2

**Prove per 101,2 dei 150,2 M€ di S2.** Le fonti sono atti e offerte pubblicati dagli enti, schede ACN e DNS/AS. Il DNS/AS dice dove **risponde** il servizio pubblico, non dove stanno i dati; i CDN sono marcati.

**Hyperscaler extra-UE accertato** [A + B]:
- **Datamanagement Italia, 15,1 M€: AWS Milano.**
  - Relazione tecnica, Comune di Firenze, CIG B519664052: «Il provider … è Amazon AWS».
  - akropolis.cloud: 3 host su 3 in AWS.
  - Esiste anche una variante su Unimatica (IT).
- **Deda Next, 4,7 M€: Microsoft Azure.**
  - Offerta Avviso 1.2 al Comune di Tramonti.
  - soluzionipa.it: 5 host su 5 in Microsoft.
- **Parsec 3.26, 2,0 M€: AWS** (front-end) [B].

**Misto: APKappa, 7,1 M€.**
- DC proprio a Magenta più Aruba (IN-54).
- Varianti qualificate su **AWS** (SA-1740) e su Liguria Digitale.
- hypersicapp.net risponde da AWS, hypersic.net da Fastweb.

**Infrastruttura italiana:**
- **Maggioli, 37,9 M€**: DNS 10/10 host su reti Maggioli e Dinova [B]. Ma l'offerta PNRR (Ferno) lascia la scelta «private cloud (Data Center Maggioli, DATA4) oppure public cloud (Google, Microsoft o AWS)» [A].
- **PA Digitale: DC TIM** di Acilia e Pomezia [A].
- **Halley**: rete propria e Retelit [B].
- Siscom, ADS e Boxxapps con DC proprio [B]; Kibernetes su Aruba [B]; TIM, Fastweb, IAA ed Engineering D.HUB con IaaS proprio [B].

**Senza prove: 49,0 M€** (svic 8,6, Almaviva 4,1, We-Com 3,8, Municipia dietro Cloudflare, 3PItalia, BIP, coda S2), più S3-S4 55,7 M€.
- Prendono la **quota media dei fornitori con prove: 23,9 % in euro**.
- È un dato misurato, al posto dell'ipotesi fissa del 25 % della v0.1.

#### 3. Misura 1.2 con il terzo asse (818,9 M€; lettura «la migrazione segue la destinazione»)

| Scenario | Big tech prodotto | PSN su hyperscaler | SaaS con prove | SaaS senza prove + S3-S4 | S5 | S6 | **Totale infra extra-UE** |
|---|---|---|---|---|---|---|---|
| basso | 13,6 | 27,0 | 9,9 | 0 | 0 | 0 | **50,6 M€ (6,2 %)** |
| centrale | 13,6 | 131,5 | 24,1 | 25,0 | 28,5 | 55,0 | **277,8 M€ (33,9 %)** |
| alto | 13,6 | 165,9 | 57,2 | 104,7 | 28,5 | 162,3 | **532,2 M€ (65,0 %)** |

- **Lettura stretta** (migrazione PSN = servizio italiano): centrale circa **180 M€ (22 %)**.
- **La soglia basso sale** da 4,7 % a **6,2 %**, perché sono accertati AWS (Datamanagement) e Azure (Deda Next).
- **Lo scenario centrale sale** da 20,6 % a **33,9 %**, perché i dati sostituiscono le ipotesi.
  - Il peso maggiore è il PSN delle ASL: Oracle Managed misurato in Sardegna, 131,5 M€ di cui ~124 sulle ASL.
  - Seguono i SaaS: AWS e Azure documentati, 24 M€.
- **Incertezze principali:**
  - un solo SSR misurato nei piani dei fabbisogni PSN;
  - Oracle Managed è in DC italiani;
  - DNS ≠ collocazione dei dati;
  - Maggioli: 37,9 M€ con la scelta lasciata all'ente;
  - S6 (162 M€) resta senza aggiudicatario.
- **Prossime prove utili:**
  - piani dei fabbisogni PSN di ASL di altre regioni (Azienda Zero Veneto, Lazio, Campania);
  - quante adesioni Maggioli hanno scelto il public cloud.
