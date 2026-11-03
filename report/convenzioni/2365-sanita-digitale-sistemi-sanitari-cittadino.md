# Dossier: Consip «Sanità digitale: sistemi informativi sanitari e servizi al cittadino» (ID 2365), lotto 2

Versione 1.0, 3/11/2026, ticket #55. CIG **903054517C**, «Lotto 2: CUP e interoperabilità dati sanitari, Centro-Sud».
Legenda: **V** = verificato su documento archiviato; **R** = riferito o inferito.

## 1. Sintesi

1. AQ Consip ID 2365, bandito il 31/12/2021: 6 lotti, 540 M. I lotti 1-4 sono applicativi multifornitore, i lotti 5-6 di supporto monofornitore. Il lotto 2 vale 150 M ed è aggiudicato nel 2023 (V, TED Consip + BDNCP).
2. Oggetto: servizi applicativi (CPV 72211000-7 e 72220000-3) per CUP e interoperabilità dei dati sanitari. Non è cloud diretto. Nel bando non ci sono voci di infrastruttura (V, ricerca testuale).
3. BDNCP: **94 attuativi, 338,9 M**. **221,5 M sono due attuativi**: Regione Lazio 150 M, pari al massimale del lotto, e ASL Viterbo 71,5 M. Senza quei due restano 117,5 M in 92 attuativi (mediana 0,58 M).
4. Cloud e migrazione: AOU «adeguamento SIO al cloud» 0,79 M; ASL Teramo «migrazione dati» 2 × 0,18 M. Trascurabili.
5. Proposta: S5, consulenza IT applicativa (sanità), cloud escluso; confidenza media.

## 2. Identificazione

| Campo | Valore | Fonte | Stato |
|---|---|---|---|
| CIG / lotto | 903054517C = lotto 2 (CIG dei 6 lotti: 9030521DAA, 903054517C, 9030563057, 90305727C2, 9030580E5A, 90305884F7) | TED 674881-2021; BDNCP | V |
| Valori | gara 540 M; lotto 2 **150 M** | TED; BDNCP | V |
| Pubblicazione | GUUE 2021/S 255-674881 (31/12/2021) | TED | V |
| Durata | AQ 18 mesi + 12 di proroga | TED | V |
| Aggiudicazione | TED 557162-2023 (15/09/2023). Fra gli RTI: GPI (con Almaviva, Postel, CGM, IQVIA…), Engineering (con Leonardo, TIM, Xenia Reply…), Dedalus (con IBM, Vodafone…) | TED 557162-2023; BDNCP aggiudicatari | V |

## 3. Cosa contiene

Servizi applicativi su CUP e interoperabilità: sviluppo, adeguamento, manutenzione. Tipo di AQ: «a condizioni tutte fissate e senza rilancio» (V, TED). I prodotti CUP sono dei fornitori (Dedalus, GPI…): canoni di licenza o SaaS nel perimetro non verificati (R).

## 4. Analisi degli attuativi

| Anno | N | M€ |
|---|---|---|
| 2021 | 1 | 0,7 |
| 2023 | 26 | 42,7 |
| 2024 | 38 | 122,1 |
| 2025 | 29 | 173,4 |

Anomali:
- Regione Lazio B78F306070, 150 M = massimale del lotto;
- ASL Viterbo B2F5991A19, 71,5 M (interoperabilità, message broker), metà del lotto: da verificare.

Classi: sviluppo 31 attuativi (258 M, gonfiato), manutenzione 8 (21 M), PNRR 19 (19 M), cloud 1, migrazione 2.

Fornitori: Dedalus 50 attuativi, GPI 22.

## 5. Classificazione proposta

servizi-applicativi; cloud diretto **escluso**; S5 consulenza IT applicativa; migrazione trascurabile (soglia minima 0,36 M). Esclusioni: B78F306070 (= massimale). B2F5991A19 resta marcato «da verificare». Confidenza media: manca il capitolato, incertezza su licenze e SaaS.

## 6. Assunzioni e limiti

Capitolato non archiviato. Una sola fonte per il contenuto (TED, che riporta solo i titoli dei lotti). Licenze e SaaS dei prodotti CUP da accertare.

## 7. Fonti

| URL | sha256 | Cosa conferma | Tipo |
|---|---|---|---|
| https://ted.europa.eu/it/notice/674881-2021/xml | a169d12bca3f1feff333d4de37e354e8818a979435e4deb2c2b6b7aa385759e0 | lotti, CIG, valori, CPV, durata | stazione appaltante |
| https://ted.europa.eu/it/notice/557162-2023/xml | da5bc144788f65d27c0968c3cbe4106da50ecddba683642d81a4821d9a9bc0d1 | aggiudicatari | stazione appaltante |
| BDNCP → `prove-servizi-applicativi/attuativi.csv` | 5d9bcf855e9c744fdef125d539a27bd51f909a88338c7aaf27657c1971349d2f | attuativi | terzo (ANAC) |

## Proposta per iniziative_ict.yaml

```yaml
# 903054517C (stato invariato: verificato)
  s5: consulenza-it-applicativa
  cloud_diretto: escluso
  massimale_lotto: 150000000
  attuativi_esclusi: [B78F306070]   # Regione Lazio 150 M = massimale
  attuativi_da_verificare: [B2F5991A19]
```
