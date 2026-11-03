# Dossier — Consip Microsoft Enterprise Agreement 9 (ID 2755), CIG B1D4011AB2

Versione 1.0 — 3/11/2026 — ticket #55. Legenda: **V** = verificato da noi su documento archiviato; **R** = riferito o inferito.

## 1. Sintesi

1. **Legame CIG↔gara chiuso**: una determina MAECI scrive testualmente «edizione 9, ID 2755, Lotto unico CIG B1D4011AB2», e il record BDNCP di Consip coincide con il bando TED per data (27/05/2024), massimale (537,5 M€) e titolo del lotto (V).
2. Aggiudicata a Telecom Italia; convenzione attiva dal 31/01/2025 al 31/01/2026; contratti attuativi di 36 mesi (V).
3. Contiene licenze on-premise (es. SQL Server Enterprise Core con SA) e abbonamenti SaaS (es. M365 E3), divise in due famiglie con **peso 50/50** nella ponderazione di gara (V il dato; la composizione della Famiglia I è R).
4. L'avviso TED di aggiudicazione riporta 53.750.000 €, un decimo del massimale: probabile errore di un ordine di grandezza.
5. Classificazione proposta: asse A **misto** (~50 % SaaS, confidenza bassa); asse B **extra-UE** (alta).

## 2. Identificazione

| Campo | Valore | Fonte | Stato |
|---|---|---|---|
| CIG | B1D4011AB2 | BDNCP CIG padre (oggetto «FORNITURA DI LICENZE D'USO», Consip) + determina MAECI 1019/2025 | V |
| ID Sigef | 2755 | TED 309756-2024 e 251426-2025; determina MAECI; decisione Consob | V |
| Legame CIG↔ID | esplicito nella determina MAECI; coincidenza BDNCP–TED su data (bando TED emesso 24/05/2024, CIG pubblicato 27/05/2024), importo (537.500.000) e titolo del lotto unico | MAECI; BDNCP; TED | **V** (fonte della stazione appaltante per data/importo/titolo + ente aderente per il CIG) |
| Lotti | lotto unico «Fornitura di licenze d'uso» | TED | V |
| Base d'asta | 430 M€, incrementabile a 537,5 M€ | chiarimenti Consip ID 2755; TED | V |
| Aggiudicazione | 09/12/2024 (AwardDate), Telecom Italia S.p.A. | TED 251426-2025 | V (+ MAECI, Consob) |
| Valore in avviso di aggiudicazione | 53.750.000 € (PayableAmount/TotalAmount) | TED 251426-2025 | V il dato; anomalo |
| Attivazione | 31/01/2025 – 31/01/2026 (periodo ordinabile) | determina MAECI | R |
| Durata attuativi | 36 mesi | determina MAECI | R |

## 3. Cosa contiene

- **Famiglie di prodotto e pesi** (chiarimenti Consip ID 2755, V): sconti minimi Famiglia I ≥ 24,50 %, Famiglia II ≥ 23,50 %, sconto ponderato 0,50×I + 0,50×II. Per EA6 Consip definiva Famiglia I = «Microsoft 365» e II = il resto; per EA9 la definizione non è nel testo archiviato (R).
- **Requisito**: dichiarazione di Microsoft entro i termini; la fornitura «prevede esclusivamente licenze Microsoft» (chiarimenti, V).
- **Esempio d'acquisto MAECI, 36 mesi dal 01/11/2025, 7.712.154,39 € + IVA** (V):
  - 5.943 «M365 E3 Original FSA Renewal Sub Per User» + 2.057 «M365 E3 … Sub Per User» → **SaaS**;
  - 128 «SQL Server Enterprise Core ALng SA 2L» → **on-premise** (Software Assurance).
  - Il MAECI motiva la spesa come investimento perché le licenze «sono installate sugli apparati hardware di proprietà dell'Amministrazione»: la PA stessa tratta l'EA come software installato, anche quando compra M365.
- **Consob** (V): 1.004.747,82 € in EA9, imputati anche al capitolo «… cloud».
- Azure: nessuna menzione nei documenti EA9 archiviati (R).

## 4. Attuativi in BDNCP

- **296 attuativi** (2025: 187; 2026: 109), somma dichiarata 775,0 M€.
- **1 anomalo**: B7377A7739, Banca d'Italia, 430.000.000 € («P002/25 rinnovo licenze Microsoft») = base d'asta di EA9: errore.
- Senza anomali: 345,0 M€ (2025: 261,8 M€; 2026: 83,2 M€), mediana 345.983 €.
- Maggiori: INPS 54,8 M€, Difesa 18,8 M€, Roma Capitale 16,0 M€, ENAV 13,7 M€ («subscription e servizi di Software Assurance»), Insiel 12,7 M€.
- Classi (senza anomali): generico 180 / 241,6 M€; SA/rinnovo 31 / 67,8 M€; SaaS 76 / 34,0 M€; on-premise esplicito 8 / 1,6 M€; Azure 0.

## 5. Classificazione proposta

- **Asse A**: `misto`, quota SaaS stimata **~50 %** (peso Famiglia I 0,50, se Famiglia I = Microsoft 365 come in EA6). Confidenza **bassa**. Azure ~0.
- **Asse B**: `EXTRA-UE` (Microsoft). Confidenza **alta**.
- **Stato**: da `da-verificare` a **`verificato`**.

## 6. Assunzioni e limiti

- La definizione delle famiglie EA9 è presa per analogia con EA6.
- Il legame CIG↔ID usa un ente aderente per il CIG; dal lato Consip conferma per data/importo/titolo, non per il CIG scritto.
- Il valore 53,75 M€ nell'avviso TED resta non spiegato: da segnalare come raccomandazione (qualità dei dati eForms).
- Capitolato e listino non letti.

## 7. Fonti

| URL | sha256 | Cosa conferma | Tipo |
|---|---|---|---|
| https://ted.europa.eu/it/notice/309756-2024/xml | e4992b21e0b68e60b4a3a7ec4c97ca2fc7d106bd12576ef73fe97000f451f6b2 | bando ID 2755, nona edizione, 537,5 M€, lotto unico | stazione appaltante |
| https://ted.europa.eu/it/notice/251426-2025/xml | 265a0ef68464dbcd4754b12cada171e3d7baa781aeda60beebc1c57b289ffc31 | aggiudicazione Telecom Italia; valore 53,75 M€ (anomalo) | stazione appaltante |
| https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID-2755-EA9-Risposte-chiarimenti.pdf | 6c93217abf038c81429a51cf78403859031d9d80ad2fb7ae165cb52d15c1b3e5 | base 430 → 537,5 M€; pesi 50/50; solo licenze Microsoft | stazione appaltante |
| https://www.esteri.it/wp-content/uploads/2025/10/Determina-n.-1019-del-10.10.2025-Microsoft-EA9_Firmato.pdf | 9c57dba2cd3e31a1b7a7ef7707f48e0f7f3005122eadae5f6e4842efb4a33256 | «ID 2755, Lotto unico CIG B1D4011AB2», Telecom, attiva 31/01/2025–31/01/2026; M365 E3 + SQL Server | terzo (ente aderente) |
| https://www.consob.it/documents/d/asset-library-1912910/0064086_decisione | 528c29118b9f8e828c114cb9ad429c7e6d5b12f459c27b0522abc2cf79c29d67 | adesione EA9, lotto unico Telecom | terzo |
| BDNCP record CIG B1D4011AB2 (delta `20260601-cig_csv.zip`) | vedi manifest | data, importo 537,5 M€ | stazione appaltante via ANAC |
| `report/convenzioni/prove-attuativi/attuativi.csv` | 52affacafa04b492e3cc95a370bfd02f5a78f9f1f7345466a9d46fc78d9056a6 | attuativi | elaborazione nostra |

## Proposta per iniziative_ict.yaml

```yaml
- cig: B1D4011AB2
  iniziativa: Consip Licenze Microsoft Enterprise Agreement 9, ID 2755, lotto unico
  categoria: licenza-prodotto
  produttore: Microsoft
  giurisdizione: EXTRA-UE
  stato: verificato
  modello: misto            # on-premise (SQL Server, SA) + SaaS (M365); Azure non risultante
  quota_cloud_stimata: 0.50 # peso Famiglia I nella ponderazione di gara; confidenza bassa
  fonte: 'oggetto CIG padre (BDNCP): ''FORNITURA DI LICENZE D''USO''; determina MAECI 1019/2025'
  dossier: report/convenzioni/B1D4011AB2-microsoft-ea9.md
  attuativi_anomali: [B7377A7739]
  documenti:
  - url: https://ted.europa.eu/it/notice/309756-2024/xml
    sha256: e4992b21e0b68e60b4a3a7ec4c97ca2fc7d106bd12576ef73fe97000f451f6b2
    cosa_conferma: bando TED Consip ID 2755, lotto unico 'Fornitura di licenze d'uso', 537,5 M€ (= BDNCP)
  - url: https://www.esteri.it/wp-content/uploads/2025/10/Determina-n.-1019-del-10.10.2025-Microsoft-EA9_Firmato.pdf
    sha256: 9c57dba2cd3e31a1b7a7ef7707f48e0f7f3005122eadae5f6e4842efb4a33256
    cosa_conferma: 'determina MAECI: «edizione 9, ID 2755, Lotto unico CIG B1D4011AB2», Telecom Italia'
  - url: https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID-2755-EA9-Risposte-chiarimenti.pdf
    sha256: 6c93217abf038c81429a51cf78403859031d9d80ad2fb7ae165cb52d15c1b3e5
    cosa_conferma: 'chiarimenti Consip ID 2755: base d''asta 430/537,5 M€, famiglie I/II pesate 50/50'
```
