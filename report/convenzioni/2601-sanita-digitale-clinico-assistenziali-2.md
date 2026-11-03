# Dossier: Consip «Sanità digitale: sistemi informativi clinico-assistenziali 2» (ID 2601), lotto 2

Versione 1.0, 3/11/2026, ticket #55. CIG **98209074D6**, «Lotto 2: cartella clinica elettronica, Centro-Sud».
Legenda: **V** = verificato su documento archiviato; **R** = riferito o inferito.

## 1. Sintesi

1. AQ Consip ID 2601, bando del 12/06/2023: 6 lotti, 880 M. Lotti 1-2 cartella clinica elettronica (CCE), 3-4 enterprise imaging, 5-6 supporto. Lotto 2: 252 M, massimale 302,4 M con il +20 %. Aggiudicato a 4 RTI: Engineering, Dedalus, GPI ed Enterprise (V).
2. Oggetto: servizi applicativi (CPV 72211000-7) per la CCE. Non è cloud diretto. Nel TED non ci sono voci di infrastruttura (V, ricerca testuale).
3. BDNCP: **84 attuativi, 361,1 M**. **250 M sono un solo attuativo della Regione Lazio**, «piattaforma digital upskilling FSE 2.0 / e-learning»: pari a circa il lotto e fuori tema rispetto alla CCE. Probabile padre sbagliato o massimale. Senza: 83 attuativi per 111,1 M (mediana 0,65 M).
4. Né cloud né migrazione negli oggetti.
5. Proposta: S5, consulenza IT applicativa (sanità), cloud escluso; confidenza media.

## 2. Identificazione

| Campo | Valore | Fonte | Stato |
|---|---|---|---|
| CIG / lotto | 98209074D6 = lotto 2 CCE Centro-Sud | TED 347073-2023; TED 336340-2024; BDNCP | V |
| Valori | gara 880 M; lotto 2 **252 M** (302,4 M con +20 %) | TED bando e aggiudicazione; BDNCP | V |
| Pubblicazione | GUUE 2023/S 111-347073 (12/06/2023) | TED | V |
| Aggiudicatari lotto 2 | RTI Engineering, RTI Dedalus, RTI GPI, RTI Enterprise | TED 336340-2024 | V |

## 3. Cosa contiene

Servizi applicativi per la CCE (lotti 1-4 plurifornitore) e servizi di supporto alla digitalizzazione (lotti 5-6). Ammessi contratti finanziati dal PNRR (V, TED). Le CCE sono prodotti dei fornitori: licenze e SaaS nel perimetro non verificati (R).

## 4. Analisi degli attuativi

| Anno | N | M€ |
|---|---|---|
| 2024 | 23 | 20,6 |
| 2025 | 35 | 302,5 (250 Lazio) |
| 2026 | 26 | 38,0 |

Fasce: < 100 k 8; 100 k–1 M 42; 1–10 M 32 (79 M); 10–50 M 1 (AOU Messina 15,4 M); ≥50 M 1.

Classi: sviluppo 20 attuativi (27,7 M), manutenzione 15 (17,2 M), PNRR 13; cloud 0; migrazione 0.

Fornitori: Engineering (265 M con Lazio), Dedalus 16 attuativi (41,6 M), GPI 16 (13,9 M).

## 5. Classificazione proposta

servizi-applicativi; cloud diretto **escluso**; S5 consulenza IT applicativa; migrazione 0. Escludere B785C1D778 (Regione Lazio 250 M). Confidenza media.

## 6. Assunzioni e limiti

Capitolato non archiviato; licenze e SaaS dei prodotti CCE da accertare. L'oggetto del Lazio («digital upskilling FSE 2.0») va confrontato con l'atto: potrebbe essere un CIG agganciato al padre sbagliato.

## 7. Fonti

| URL | sha256 | Cosa conferma | Tipo |
|---|---|---|---|
| https://ted.europa.eu/it/notice/347073-2023/xml | 483c7f5ef482c30f7db5d3f689a3289b0fc064beeeb245335d54a182ccf1a700 | lotti, valori, CPV | stazione appaltante |
| https://ted.europa.eu/it/notice/336340-2024/xml | f17420b3a7d9101ecce1b9078a5fb57388df4328d0c7c8a9c7ca6924eee2a2f5 | aggiudicatari lotto 2, massimale 302,4 M | stazione appaltante |
| BDNCP → `prove-servizi-applicativi/attuativi.csv` | 5d9bcf855e9c744fdef125d539a27bd51f909a88338c7aaf27657c1971349d2f | attuativi | terzo (ANAC) |

## Proposta per iniziative_ict.yaml

```yaml
# 98209074D6 (stato invariato: verificato)
  s5: consulenza-it-applicativa
  cloud_diretto: escluso
  massimale_lotto: 252000000
  attuativi_esclusi: [B785C1D778]   # Regione Lazio 250 M, oggetto e-learning FSE: padre errato o massimale
```
