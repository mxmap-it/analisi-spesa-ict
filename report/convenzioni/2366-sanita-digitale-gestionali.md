# Dossier: Consip «Sanità digitale: sistemi informativi gestionali» (ID 2366), lotto 2

Versione 1.0, 3/11/2026, ticket #55. CIG **9188183878**, «Lotto 2: procedimenti amministrativi e contabili, Centro-Sud».
Legenda: **V** = verificato su documento archiviato; **R** = riferito o inferito.

## 1. Sintesi

1. Il CIG 9188183878 è il lotto 2 dell'AQ Consip ID 2366, «servizi applicativi e servizi di supporto in ambito Sanità digitale: sistemi informativi gestionali» per le PA del SSN. Importo lotto 252 M; gara 900 M; CPV 72211000-7; BDNCP 10/05/2022 (V, solo BDNCP).
2. Si comprano servizi applicativi su gestionali amministrativo-contabili delle aziende sanitarie: sviluppo, reingegnerizzazione, manutenzione. Non è cloud diretto. Un attuativo nomina un **canone cloud su piattaforma PSN** (Sardegna IT, 0,16 M): alcuni contratti possono includere canoni infrastrutturali (R).
3. BDNCP: **91 attuativi, 888 M**. **667 M sono un solo attuativo So.Re.Sa.** (B29E105589, «reingegnerizzazione SIAC/SURAFS»), 2,6 volte il lotto: anomalo. Senza: 90 attuativi per 221 M.
4. Due attuativi So.Re.Sa. da 7,47 M ciascuno citano il PNRR M1C1 1.1 «infrastrutture digitali» e 1.2 «abilitazione al cloud». Lì ci può essere migrazione.
5. Stato proposto: **da-verificare**. Non c'è ancora un documento Consip archiviato (TED di bando o esito) che leghi il CIG al lotto.

## 2. Identificazione

| Campo | Valore | Fonte | Stato |
|---|---|---|---|
| CIG / lotto | 9188183878, lotto 2 «procedimenti amministrativi e contabili – Centro-Sud» | BDNCP padre (numero gara 8525885) | R (fonte unica) |
| Iniziativa | ID 2366, «Sanità digitale – sistemi informativi gestionali» | oggetto_gara BDNCP | R |
| Importi | lotto 252 M; gara 900 M | BDNCP | R |
| Aggiudicatari | 47 operatori nell'elenco BDNCP (RTI con Accenture, Almaviva, Enterprise Services, Capgemini, Artexe…) | BDNCP aggiudicatari | R |
| Lotti noti da terzi | L1 procedure amministrativo-contabili Nord, L4 data governance Centro-Sud, L6 supporto Centro-Sud | stampa di settore (non archiviata) | R |

## 3. Cosa contiene

Servizi applicativi (CPV 72211000-7, programmazione) e di supporto. Le soluzioni sono gestionali dei fornitori (R), quindi potrebbero esserci licenze o canoni di prodotto. Non abbiamo il capitolato: non sappiamo se l'AQ preveda canoni SaaS o di hosting. Indizi:
- Sardegna IT, B9EE1FEF1F: «manutenzione correttiva, adeguativa ed evolutiva, **canone cloud su piattaforma PSN** del sistema informativo SIRMES» (0,16 M);
- So.Re.Sa.: due attuativi PNRR M1C1 1.1/1.2 da 7,47 M.

## 4. Analisi degli attuativi

| Anno | N | M€ |
|---|---|---|
| 2024 | 25 | 759,0 (667,1 So.Re.Sa.) |
| 2025 | 23 | 67,0 |
| 2026 | 43 | 62,1 |

Fasce: 100 k–1 M 39; 1–10 M 48 (163 M); 10–50 M 3 (39 M); ≥50 M 1 (667 M).

Classi:
- sviluppo/reingegnerizzazione 25 attuativi (741 M, quasi tutto So.Re.Sa.);
- manutenzione 15 (54,5 M);
- cloud specifico 3 (15,1 M);
- migrazione 0.

Fornitori: Enterprise Services 748 M (con So.Re.Sa.), Accenture 37 attuativi (57 M).

## 5. Classificazione proposta

Categoria servizi-applicativi (sanità). Asse cloud: **incerto per la minoranza** di attuativi che citano canoni cloud o PSN o la Misura 1.2, escluso per il resto. S5: consulenza IT applicativa. Confidenza **bassa**: manca qualsiasi documento Consip. Escludere B29E105589.

## 6. Assunzioni e limiti

- Fonte unica (BDNCP). Prossimo passo: archiviare il bando TED ID 2366 (2022) e l'esito, e un contratto esecutivo con l'elenco dei servizi (per esempio gli atti della Regione Siciliana citati in rete, DRA n. 836–837/2026).
- Non sappiamo se l'AQ includa licenze o SaaS dei prodotti gestionali: va accertato come per le convenzioni di licenze (DECISIONI 2026-11-03).

## 7. Fonti

| URL | sha256 | Cosa conferma | Tipo |
|---|---|---|---|
| BDNCP → `prove-servizi-applicativi/attuativi.csv`, `riepilogo.json` | 5d9bcf855e9c744fdef125d539a27bd51f909a88338c7aaf27657c1971349d2f; 7774cfbc0317bc685a8b8407b0d2f47399e6e614f6bc017faca64349a22ed381 | padre, lotto, attuativi | terzo (ANAC) |

## Proposta per iniziative_ict.yaml

```yaml
- cig: 9188183878
  iniziativa: Consip AQ Sanità digitale, sistemi informativi gestionali (ID 2366), lotto 2 procedimenti amministrativi e contabili Centro-Sud
  categoria: servizi-applicativi
  stato: da-verificare       # solo BDNCP; manca documento Consip
  s5: consulenza-it-applicativa
  cloud_diretto: incerto-minoritario   # canone cloud PSN (B9EE1FEF1F), PNRR 1.1/1.2 (A04D55DB8F, B056F820A5)
  attuativi_esclusi: [B29E105589]      # So.Re.Sa. 667 M > lotto 252 M
```
