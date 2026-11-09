### 3.3 Su quale infrastruttura girano i «prodotti italiani»: terzo asse (v0.9)

**Domanda:** sotto i prodotti italiani della Misura 1.2 (PSN 389,2 M€, SaaS qualificati ACN 150,2 M€) ci sono infrastrutture delle big tech?

**Verifiche** (senza LLM; la seconda interroga solo il DNS):
- `nice .venv/bin/python tools/verifiche/infrastruttura_sottostante.py --data 2026-11-09` → `esiti/2026-11-09/infrastruttura-sottostante/infrastruttura.json`;
- `tools/verifiche/saas_infra_fornitori.py`, che estende il pilota del § 3.2 ai domini dei servizi di 11 fornitori (`config/saas_host.yaml`).

**Tabelle:** `config/saas_infrastruttura.yaml` (21 fornitori, con fonte, sha256 e attendibilità per riga) e `psn-ppdf.csv`.

**Terzo asse:** la giurisdizione di chi gestisce l'infrastruttura, accanto a prodotto e fornitore. Teniamo **due letture distinte**:
- **extra-UE per produttore o gestione**: conta anche Oracle Exadata Cloud@Customer nei DC PSN (hardware, software e aggiornamenti Oracle);
- **extra-UE per localizzazione dei dati**: conta solo ciò che gira nelle region degli hyperscaler (Secure Public Cloud, SaaS su AWS o Azure).

In entrambe le letture le region sono in Italia (Milano, Torino): «extra-UE» vuol dire controllo dell'operatore (CLOUD Act), non che i dati escano dall'UE.

**PSN, aggregato** [V, fonte A del concessionario]. Fonte: *Libro PSN 2025*, sha256 b8fe9ec1…, p. 71-72 e 106.
- **Ricavi 2025:** 454,3 M€, di cui il 79 % da migrazione e servizi professionali.
- **Hyperscaler sui ricavi:** Secure Public Cloud (Azure, Google, AWS) 19,9 M€ + PSN Managed Oracle 4,5 M€, cioè **5,4 % dei ricavi e 27,3 % dei ricavi infrastrutturali** (2024: 2,6 % e 16,8 %).
- **Contratti firmati:** 3.853 M€, 60 % servizi professionali e 40 % canoni. Il Secure Public Cloud vale il 15 % dei canoni: PA centrali 24 %, PA locali 6 %, ASL/AO 7 %.
- **PSN in generale (#45):** circa **8 % del valore ordinato** su hyperscaler (~0,3 mld).

**PSN, per ente: piani dei fabbisogni** [V, Riepilogo prezzi del Configuratore letto nel testo o a vista]. Campione: 9 enti sanitari in 6 regioni (Sardegna come un ente; Piemonte, Lazio, Campania, Marche, Lombardia).

| Ente | Hyperscaler sul canone annuo | Cosa |
|---|---|---|
| ARES Sardegna (12 schede) | 34,4 % | Oracle Managed (Exadata C@C) |
| AIC3 Piemonte (5 aziende) | 37,7 % | **Secure Public Cloud Azure** |
| ASL Latina | 17,0 % | Oracle Managed |
| ASL Roma 3 | 15,5 % | Oracle Managed |
| AORN Cardarelli | 10,5 % | Oracle Managed (inferito) |
| AORN Santobono | 68,0 % (canone piccolo) | Oracle Managed |
| AO Mauriziano, AST Pesaro-Urbino, ATS Brescia | 0 % | solo Industry Standard |

- **Media pesata dei canoni** nelle ASL:
  - **23,3 % per produttore o gestione** (soprattutto Oracle Managed nei DC PSN);
  - **7,4 % per localizzazione** (solo Azure dell'AIC3), coerente con il 7 % del Libro.
- Contando la una tantum, l'hyperscaler pesa pochi punti: i piani sono dominati da servizi professionali e migrazione.

**SaaS dei fornitori S2** [V/R per riga]. Ci sono prove per 122,9 dei 150,2 M€. Fonti: offerte e relazioni pubblicate dagli enti (A); schede ACN, documenti del fornitore e DNS/AS (B, cioè dove *risponde* il servizio, non dove stanno i dati); indizi (C).

- **Hyperscaler accertato:**
  - **Datamanagement Italia**, 15,1 M€: AWS Milano. Fonte A, relazione tecnica, Comune di Firenze, CIG B519664052: «Il provider che verrà utilizzato per il servizio cloud è Amazon AWS».
  - **Deda Next**, 4,7 M€: Microsoft Azure. Fonte A, offerta Avviso 1.2 al Comune di Tramonti; soluzionipa.it risponde da Microsoft.
  - Parsec 3.26, 2,0 M€: AWS [B].
  - Almaviva, 4,1 M€: front-end Giotto su AWS [B].
- **Misto:**
  - **Maggioli**, 37,9 M€. Delle 33 varianti ACN con l'IaaS nel nome, 12 sono su hyperscaler (Google 6, Azure 5, AWS 1) e 21 su DC Maggioli/DATA4, Dinova, CSI Nivola, Lepida e altri.
    - L'offerta PNRR (Ferno) lascia all'ente la scelta fra private e public cloud [A].
    - Il prodotto PNRR Sicraweb EVO è orientato a Google [B].
    - Nei 4 atti comunali 1.2 trovati: 1 Lepida, 3 senza indicazione, 0 public.
    - **Quanti Comuni abbiano scelto il public cloud non è misurabile dagli atti pubblicati.**
  - **APKappa**, 7,1 M€: DC proprio più Aruba, con una variante su AWS.
  - **Municipia**: jEnte su Engineering, altre varianti «su AMAZON».
- **Infrastruttura italiana:**
  - PA Digitale: DC TIM [A];
  - Halley (e svic, che la rivende), Siscom, ADS, Boxxapps, Kibernetes (Aruba), We-Com (Fastweb), TIM, Fastweb, IAA, Engineering D.HUB [B].
- **Senza prove:** 27,3 M€ di S2 e 55,7 M€ di S3-S4. Prendono la quota media in euro dei fornitori con prove, **34,3 %**.

**Misura 1.2 con il terzo asse** (818,9 M€; il PSN segue la destinazione della migrazione, R-S1):

| Scenario | Big tech prodotto | PSN su hyperscaler | SaaS con prove | SaaS senza prove + S3-S4 | S5 | S6 | **Produttore/gestione** | **Localizzazione** |
|---|---|---|---|---|---|---|---|---|
| basso | 13,6 | 27,0 | 11,4 | 0 | 0 | 0 | **52,0 M€ (6,3 %)** | 24,9 M€ (3,0 %) |
| centrale | 13,6 | 88,5 | 42,1 | 28,4 | 28,5 | 49,7 | **250,9 M€ (30,6 %)** | **176,1 M€ (21,5 %)** |
| alto | 13,6 | 145,5 | 76,6 | 83,0 | 28,5 | 162,3 | 509,4 M€ (62,2 %) | 417,8 M€ (51,0 %) |

- **Risposta:** sì. Sotto i prodotti italiani della 1.2 c'è infrastruttura degli hyperscaler, ben oltre l'1,7 % della lente prodotto. Lo **stimiamo nel 20-30 % dei contratti collegati** (centrale), con una forbice dal 3-6 % accertato al 51-62 %.
- **Accertato con fonte A o B:**
  - Datamanagement su AWS e Deda Next su Azure (19,8 M€);
  - Oracle Managed in 6 aziende sanitarie su 9;
  - Azure in un consorzio di 5 aziende piemontesi.
- **Pesano sull'incertezza:**
  - la scelta di infrastruttura dei Comuni Maggioli (37,9 M€);
  - il campione PSN di 9 enti, contro 368,6 M€ di PSN nelle ASL 1.2;
  - il residuo S6 (162,3 M€, senza aggiudicatario);
  - il fatto che il DNS non dice dove stanno i dati.
- **Raccomandazione R78:** infrastruttura dichiarata per ogni SaaS nella scheda ACN, servizi migrati in PA Digitale 2026, Riepilogo prezzi PSN per Contratto di Utenza in open data. Aggiorna R73.
