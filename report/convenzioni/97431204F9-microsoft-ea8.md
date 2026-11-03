# Dossier — Consip Microsoft Enterprise Agreement 8 (ID 2615), CIG 97431204F9

Versione 1.0 — 3/11/2026 — ticket #55. Legenda: **V** = verificato da noi su documento archiviato; **R** = riferito o inferito, da verificare.

## 1. Sintesi

1. Il CIG 97431204F9 è la convenzione Consip «Microsoft Enterprise Agreement 8», ID 2615, lotto unico, procedura aperta, aggiudicata a Telecom Italia, massimale 430 M€ (V).
2. Contiene licenze Microsoft on-premise e abbonamenti SaaS (Microsoft 365, Dynamics 365, SharePoint, Copilot) nello stesso lotto (V da ordini reali).
3. Gli acquisti documentati dagli enti sono **in prevalenza Microsoft 365** (ART: Office 365 + spazio SharePoint + Copilot; Archivi notarili: Dynamics 365 F&O) (V su esempi, non quantificabile).
4. Gli attuativi BDNCP hanno **7 importi anomali per 2,1 G€** (ASL NA3 Sud 607 M€, InfoCamere 2×430 M€ = massimale…), cinque volte il massimale: vanno esclusi da ogni somma.
5. Classificazione proposta: asse A **misto** (quota SaaS ~40–50 %, confidenza bassa); asse B **extra-UE** (alta).

## 2. Identificazione

| Campo | Valore | Fonte | Stato |
|---|---|---|---|
| CIG | 97431204F9 | BDNCP CIG padre; bando TED 236254-2023 | V (2 fonti, Consip) |
| ID Sigef | 2615 | TED 236254-2023 e 272361-2024; oggetto BDNCP «ID 2615 … (8 EDIZIONE)» | V |
| Lotti | lotto unico | TED 236254-2023 | V |
| Procedura | aperta ex art. 60 d.lgs. 50/2016 | TED 272361-2024 | V |
| Bando | 21/04/2023 (TED e BDNCP) | TED, BDNCP | V |
| Aggiudicazione | 28/07/2023; Telecom Italia S.p.A. | TED 272361-2024 | V (+ determine ART, UCAN) |
| Massimale | 430.000.000 € | TED (VAL_ESTIMATED_TOTAL, TotalAmount) = BDNCP | V |
| Durata | convenzione 12 mesi (TED); contratti attuativi 36 mesi (es. ART dal 1/5/2024 al 30/4/2027) | TED; determina ART | V / R |
| Avviso Consip «acquisti successivi», «Lotto 1» | il Ministero della Giustizia scrive «EA 8, Lotto 1, acquisti successivi» fino al 30/4/2027 | UCAN 49/2026 | R |

## 3. Cosa contiene

- Capitolato e listino EA8 non reperiti in forma pubblica. Il modello è quello delle edizioni 6–7 (V per EA6 dai chiarimenti Consip, V per EA7 dalla guida riprodotta dall'ARL Sardegna): **licenze on-premise in acquisto perpetuo**, **Subscription** (licenze online e on-premise a tempo), **Dual Use Rights**, servizio di aggiornamento evolutivo (Software Assurance); **Azure non previsto** in EA7 (per EA8: R).
- Esempi d'acquisto EA8 (V):
  - Autorità di regolazione dei trasporti: Microsoft Office 365 per 36 mesi (291.920,40 €), poi +1 TB SharePoint (2.600 €) e Microsoft 365 Copilot add-on + Copilot Studio (49.180 €): **tutto SaaS**.
  - Ministero della Giustizia, Archivi notarili: rinnovo licenze e **Dynamics 365 Finance & Operations** (653.777,10 € + IVA): **SaaS**.
- Oggetto «Fornitura di licenze di posta elettronica» (ASST, BDNCP): Exchange Online o Exchange Server, non distinguibile.

## 4. Attuativi in BDNCP

Stesso metodo del dossier EA6 (`prove-attuativi/`).

- **491 attuativi**, somma dichiarata 2.560,7 M€. **7 anomali** (importo ≥ 20 % del massimale o ≥ 100 M€), somma 2.107,4 M€:

| CIG | € | Ente | Lettura |
|---|---|---|---|
| B2D9920951 | 607.425.675 | ASL Napoli 3 Sud | oltre il massimale: errore |
| B24129F825 | 430.000.000 | InfoCamere | = massimale |
| B4DF298EDE | 430.000.000 | InfoCamere | = massimale (duplicato) |
| B16C905102 | 260.938.788 | Coninet | implausibile |
| B10AB5BA1F | 161.849.127 | ASST Santi Paolo e Carlo | «licenze di posta elettronica»: implausibile |
| A041C635CF | 117.393.918 | DTD Giustizia | plausibile, da verificare |
| B23BDB448F | 99.811.830 | AO Cosenza | implausibile |

- Senza anomali: 484 attuativi, 453,3 M€, mediana 136.100 €. Per anno: 2023 31 / 116,4 M€; 2024 288 / 320,3 M€; 2025 103 / 12,4 M€; 2026 62 / 4,2 M€.
- Classi di oggetto (senza anomali): generico 241 / 320,2 M€; SaaS 153 / 63,4 M€; on-premise esplicito 41 / 36,2 M€; SA/rinnovo 48 / 33,4 M€; Azure 1 / 6.555 €. Il 71 % degli euro ha oggetto generico.

## 5. Classificazione proposta

- **Asse A**: `misto`, quota SaaS stimata **~40–50 %**. Base: peso «Microsoft 365» nella ponderazione di gara 44 % in EA6 e 50 % in EA9 (EA8 è in mezzo, peso non letto); oggetti espliciti SaaS 63,4 M€ contro on-premise 36,2 M€. Confidenza **bassa**. Azure ~0.
- **Asse B**: `EXTRA-UE` (Microsoft). Confidenza **alta**.
- **Stato identificazione**: `verificato` (già in yaml; confermato).

## 6. Assunzioni e limiti

- Capitolato, listino e pesi di gara EA8 non letti (non trovati pubblici; acquistinretepa.it ammette solo alcuni percorsi in robots.txt).
- La quota SaaS è un'inferenza dai pesi di altre edizioni.
- La soglia per gli anomali (20 % del massimale / 100 M€) è una scelta nostra; A041C635CF potrebbe essere reale.
- Una M365 E3 include diritti d'installazione locale di Office: «SaaS» va inteso come abbonamento a servizio Microsoft.

## 7. Fonti

| URL | sha256 | Cosa conferma | Tipo |
|---|---|---|---|
| https://ted.europa.eu/it/notice/236254-2023/xml | db4481a7c597f45e2a68f9d2c05a59b3b941800af7c1c82fca25bd94ac67dd28 | bando: ID 2615, CIG, lotto unico, 430 M€ | stazione appaltante |
| https://ted.europa.eu/it/notice/272361-2024/xml | 2888fafcfb7f0af5f572312a3b42edc4ace529827151e5c5a6076891666381c3 | aggiudicazione Telecom Italia 28/07/2023, procedura aperta | stazione appaltante |
| BDNCP record CIG 97431204F9 (delta `20260401-cig_csv.zip`) | vedi manifest | oggetto, massimale | stazione appaltante via ANAC |
| https://www.autorita-trasporti.it/wp-content/uploads/2025/10/det_00130_03-10-2025.pdf | 728a027ad782af87236268ce346e5ee4a3b5fb7961c5d450c2c23867eb796933 | Office 365 + SharePoint in EA8, 36 mesi | terzo (ente aderente) |
| https://www.autorita-trasporti.it/wp-content/uploads/2026/06/det_00112_04-06-2026.pdf | 6963a4a0081d85c15f66c680aa21b0fe377b81a90f086cf0a50d3440ed6c2469 | Copilot add-on in EA8 | terzo |
| https://www.giustizia.it/cmsresources/cms/documents/UCAN_decisione_a_contrarre_49_2026.pdf | 4d2b8395bedc5fa79a751aae243ebb715e6043279e9053b0cde7cb39c2938a27 | Dynamics 365 F&O in EA8, scadenza 30/4/2027 | terzo |
| https://agenziaregionaleperillavoro.regione.sardegna.it/documenti/44_917_20230306122603.pdf | e8b6581982a1526e8f7bc047d620da85978f29e77575c8736241a7cad7b43d3c | modello EA7 (on-premise, subscription, dual use, no Azure) | terzo |
| `report/convenzioni/prove-attuativi/attuativi.csv` | 52affacafa04b492e3cc95a370bfd02f5a78f9f1f7345466a9d46fc78d9056a6 | attuativi | elaborazione nostra |

## Proposta per iniziative_ict.yaml

```yaml
# aggiunte alla voce esistente 97431204F9
  modello: misto            # on-premise + SaaS (M365, Dynamics 365, Copilot); Azure non risultante
  quota_cloud_stimata: 0.45 # inferita dai pesi di gara EA6 (0,44) ed EA9 (0,50); confidenza bassa
  dossier: report/convenzioni/97431204F9-microsoft-ea8.md
  attuativi_anomali: [B2D9920951, B24129F825, B4DF298EDE, B16C905102, B10AB5BA1F, B23BDB448F]  # A041C635CF da verificare
  documenti:  # aggiungere
  - url: https://www.autorita-trasporti.it/wp-content/uploads/2025/10/det_00130_03-10-2025.pdf
    sha256: 728a027ad782af87236268ce346e5ee4a3b5fb7961c5d450c2c23867eb796933
    cosa_conferma: 'ente aderente: Office 365 e SharePoint acquistati in EA8 (Telecom Italia)'
```
