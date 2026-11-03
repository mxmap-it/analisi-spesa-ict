# Dossier: Consip «Servizi specialistici di supporto alla Digital Transformation per la PA», ed. 2 (ID 2536)

Versione 1.0, 3/11/2026, ticket #55. Lotti analizzati: **985365662A** (lotto 2, digitalizzazione dei processi) e **985369130D** (lotto 6, PMO Nord).
Legenda: **V** = verificato su documento archiviato; **R** = riferito o inferito.

## 1. Sintesi

1. AQ Consip ID 2536, bando del 13/06/2023: 8 lotti, 400 M. Valori massimi con il +20 %: lotto 2 «digitalizzazione dei processi» 180 M (216 M); lotto 6 «PMO Nord» 10 M (12 M). Sono AQ monofornitore (art. 54 c. 3):
   - lotto 2: RTI Accenture, LUISS, EY, Digit'Ed, Deloitte…;
   - lotto 6: RTI BIP, Advant, Arthur D. Little, Business Changers, BV Tech, Digitalia (V).
2. È **consulenza**, non cloud. CPV del lotto 2: 79411000-8 (consulenza gestionale generale) + 79420000-4. CPV del lotto 6: 72224000-1. Il TED dichiara che l'aggiudicatario può subappaltare «tutte le attività del lotto» nei limiti di legge (V).
3. BDNCP, lotto 2: **49 attuativi, 857,9 M**, quattro volte il massimale. **627 M sono 3 attuativi**: Regione Sardegna «PATER» 394 M, Agenzia per i giovani 180 M (= importo del lotto), MiTur 53 M. Senza i primi due: 47 attuativi per 283 M.
4. Lotto 6: **14 attuativi, 422 M**. **400 M sono un solo attuativo InfoCamere**, 33 volte il massimale. Senza: 13 attuativi per 22,2 M.
5. Proposta: S5, consulenza (lotto 2 non infrastrutturale, mista IT e non IT; lotto 6 governance IT); cloud escluso; nessuna migrazione. Confidenza alta.

## 2. Identificazione

| Campo | Valore | Fonte | Stato |
|---|---|---|---|
| CIG | lotto 2 985365662A; lotto 6 985369130D (lotto 1 9853648F8D) | TED 351960-2023 e 557722-2024; BDNCP | V |
| Valori | gara 400 M (480 M con +20 %); L2 180 M (216 M); L6 10 M (12 M) | TED | V |
| CPV | L2 79411000-8, 79420000-4; L6 72224000-1 | TED; BDNCP | V |
| Pubblicazione | GUUE 2023/S 112-351960 (13/06/2023) | TED | V |
| Aggiudicatari | L2 RTI Accenture e altri; L6 RTI Business Integration Partners e altri | TED 557722-2024; BDNCP | V |

## 3. Cosa contiene

Servizi specialistici di supporto:
- strategia (L1);
- digitalizzazione dei processi (L2);
- gestione della transizione al digitale (L3-5, con CPV di formazione 80420000-4 e 72600000-6);
- PMO (L6-8).

Nessuna componente infrastrutturale, applicativa di prodotto o cloud (V da CPV e titoli).

## 4. Analisi degli attuativi

**Lotto 2.** 2024: 48 attuativi per 857,7 M; 2025: 1 per 0,2 M. Fasce: 1–10 M 22 (69,9 M); 10–50 M 9 (155 M); ≥50 M 3 (627,4 M).
- Anomali:
  - Regione Sardegna B2C11B9A7C «PATER», 394,2 M: 1,8 volte il massimale con il +20 %, impossibile;
  - Agenzia nazionale per i giovani B2AFEF4B41, 180 M, pari all'importo del lotto: è un massimale;
  - MiTur B2BF1E7832, 53,2 M: plausibile, da verificare.
- Classi: sviluppo/digitalizzazione 22 attuativi; cloud 1 (1,6 M, formula generica); migrazione 0.
- Fornitori: Accenture 43 attuativi.

**Lotto 6.** 2024: 6 attuativi per 16,8 M; 2025: 8 per 405,4 M.
- Anomalo: InfoCamere B76199E39D, 400 M («PMO assistente virtuale CdC Roma»). Lo stesso ente dichiara 1.605 M su ID 2610: InfoCamere scrive in BDNCP importi non legati all'affidamento (R).
- Il resto sono preordini ARIA Lombardia da 0,4 a 3,5 M.

## 5. Classificazione proposta

| Lotto | Categoria | Asse cloud | S5 | Confidenza |
|---|---|---|---|---|
| 985365662A | pmo-demand (consulenza di processo) | escluso | consulenza: quota IT e non IT da separare (CPV 79411000-8 = consulenza gestionale) | alta |
| 985369130D | pmo-demand | escluso | consulenza IT governance | alta |

Esclusioni: B2C11B9A7C, B2AFEF4B41, B76199E39D.

## 6. Assunzioni e limiti

Capitolato non archiviato. La ripartizione fra IT e non IT del lotto 2 non è misurabile dagli oggetti: proposta 100 % consulenza di processo, «IT» solo dove l'oggetto lo dice.

## 7. Fonti

| URL | sha256 | Cosa conferma | Tipo |
|---|---|---|---|
| https://ted.europa.eu/it/notice/351960-2023/xml | 3964268d7a6bd8ac74bdd8dd9ca0be8075fbf4f20745b94308af4d842d9cea48 | lotti, valori, massimali +20 % | stazione appaltante |
| https://ted.europa.eu/it/notice/557722-2024/xml | d05ca65247409d90922e2177e767bce393db7875f492f03b82e113a83814402f | aggiudicatari, CPV, subappalto | stazione appaltante |
| BDNCP → `prove-servizi-applicativi/attuativi.csv` | 5d9bcf855e9c744fdef125d539a27bd51f909a88338c7aaf27657c1971349d2f | attuativi | terzo (ANAC) |

## Proposta per iniziative_ict.yaml

```yaml
# 985365662A (stato invariato: verificato)
  s5: consulenza-processo   # IT/non IT da separare per attuativo
  cloud_diretto: escluso
  massimale_lotto: 216000000
  attuativi_esclusi: [B2C11B9A7C, B2AFEF4B41]
# 985369130D (stato invariato: verificato)
  s5: consulenza-it-governance
  cloud_diretto: escluso
  massimale_lotto: 12000000
  attuativi_esclusi: [B76199E39D]
```
