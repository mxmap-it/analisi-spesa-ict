# AQ PC portatili, mobile workstation e Chromebook ed. 1 — ID 2425 (CIG 9158053868, 9158062FD3, 91580749BC) — dossier analitico

Versione 0.1 — 2026-11-03 — #55. Bozza per revisione avversariale.
Legenda: **V** verificato su documento archiviato; **V2** due fonti indipendenti di cui una della stazione appaltante; **R** riferito / da verificare.
Numeri degli attuativi: `tools/verifiche/attuativi_s5.py` (sul server, esito in `lavoro/convenzioni/attuativi_s5.json`).

## 1. Sintesi

- **Correzione**: il CIG 9158053868 in `iniziative_ict.yaml` è il **lotto 1 – PC portatili**, non i Chromebook. I Chromebook sono il **lotto 3, CIG 91580749BC**; il lotto 2 (mobile workstation) è 9158062FD3 (bando TED Consip + BDNCP, **V2**).
- AQ multi-operatore (lett. b) di sola fornitura in acquisto di hardware con servizi connessi. Hardware = infrastruttura in-house (S5).
- Chromebook (lotto 3): 42 attuativi, **1,03 M€** in tutto (scuole PNRR 2023-24): irrilevante in euro. Il ChromeOS implica la dipendenza da servizi Google (account, aggiornamenti; la console di gestione richiede la licenza Chrome Education/Enterprise Upgrade): **non verificato** se la licenza è nel listino del lotto (capitolato non archiviato).
- Produttori negli oggetti: Lenovo (gruppo con sede a Hong Kong, Cina), HP (USA), Acer (Taiwan); Dell (USA) non misurabile per collisione con «dell'». Tutti extra-UE (R).
- BDNCP lotto 1: 729 attuativi, 1.673 M€ lordi di cui 1.552 M€ in 5 righe anomale; al netto **120,6 M€** (0,58 del valore del lotto).

## 2. Identificazione

| Campo | Valore | Fonte | Livello |
|---|---|---|---|
| CIG | L1 9158053868 PC portatili; L2 9158062FD3 mobile workstation; L3 91580749BC Chromebook | TED 176721-2022 («CIG lotto 1 9158053868; lotto 2 9158062FD3; lotto 3 91580749BC»); BDNCP | V2 |
| Gara | procedura aperta, AQ per lotto art. 54 c.4 lett. b, ID 2425 | TED 176721-2022, 564730-2023; BDNCP | V2 |
| Pubblicazione | bando 2022/S 067-176721 (05/04/2022); BDNCP 03/06/2022 | TED; BDNCP | V2 |
| Valori | base L1 207.749.000 €, L2 58.891.000 €, L3 30.840.000 €; massimo stimato L1 249,3 M€, L2 70,7 M€, L3 37,0 M€; quantità L1 220.000, L2 20.000, L3 60.000 | TED 176721-2022; BDNCP | V2 |
| Durata | 18 mesi (TED); 540 giorni (BDNCP) | TED; BDNCP | V2 |
| Aggiudicatari L1 | 9 operatori (BSistemi, Converge, Eurome, Finbuc, Infordata, Italware, …) con quote | TED 564730-2023; BDNCP (21 imprese su tutti i lotti) | V2 |
| Aggiudicatari L3 | BDNCP: A.G. Informatica, Bellucci, …; attuativi a Posdata, C2, IM Direct | BDNCP | R |

Pagina iniziativa Consip non trovata (slug ignoto); fonte della stazione appaltante = avvisi TED Consip.

## 3. Cosa contiene

- L1: «fornitura in acquisto di Personal computer portatili (15", 14", 13") e dei servizi connessi»; L2 mobile workstation; L3 «fornitura in acquisto di chromebook e dei servizi connessi»; opzioni descritte nella documentazione (TED 564730-2023). **V**
- CPV del lotto 1 include 48624000 (pacchetti software di sistemi operativi). **V**
- Capitolato tecnico, sistema operativo dei PC, licenze di gestione ChromeOS: **non letti**. **R**

## 4. Analisi degli attuativi (BDNCP)

| Misura | L1 PC portatili | L2 mobile WS | L3 Chromebook |
|---|---|---|---|
| attuativi | 729 | 53 | 42 |
| anomali | 5 / 1.552 M€ (Prefettura Milano 862 M€ per 55 notebook; Ferrara, InfoCamere = valore AQ) | 0 | 0 |
| euro puliti | 120.592.578 (0,58 × lotto) | 6.313.966 (0,11) | 1.025.202 (0,03) |
| per anno | 2023 53,2; 2024 57,0; 2025 10,4 M€ | 2023 0,6; 2024 5,7 M€ | 2023 0,86; 2024 0,16 M€ |
| mediana | 29.408 € | 25.937 € | 13.926 € |
| doppioni | 38 / 11,8 M€ | 3 / 0,08 M€ | 0 |
| aggiudicatario «IMPRESA INESISTENTE» | 41 | 0 | 0 |
| marchi in oggetto | Lenovo 36, HP 7, Acer 2 | Lenovo 4, HP 1 | Lenovo 6, Acer 1 |

Nel lotto 1, 110 oggetti contengono «Chromebook» solo perché ripetono il titolo dell'AQ: nessun acquisto di Chromebook sul lotto 1.

## 5. Classificazione proposta

- Categoria hardware; **S5 – infrastruttura in-house (postazioni di lavoro)**; confidenza alta.
- Asse cloud: escluso certo per L1 e L2. L3: hardware in-house con **dipendenza** da servizi cloud Google (ChromeOS); la spesa per licenze di gestione, se presente, sarebbe cloud extra-UE, ma vale al massimo una frazione di 1 M€: proposta di classificare L3 come hardware con nota «dipendenza cloud Google», non come spesa cloud.
- Produttori e giurisdizione: Lenovo (HK/CN), HP e Dell (USA), Acer (TW): **extra-UE** per la voce infrastrutture interne (R, dagli oggetti).

## 6. Assunzioni e limiti

- Senza capitolato non sappiamo né il SO dei portatili (verosimilmente Windows, Microsoft USA) né se il lotto 3 include licenze Chrome Education Upgrade.
- «IMPRESA INESISTENTE» negli aggiudicatari BDNCP (41 righe): difetto di qualità ANAC da segnalare.
- Marchi negli oggetti su circa 50 attuativi su 824: campione non rappresentativo.

## 7. Fonti

| URL | sha256 | Cosa conferma | Tipo |
|---|---|---|---|
| https://ted.europa.eu/it/notice/176721-2022/xml | 0152855caa6d496f035e9708be478610a2d004ed9598f8fde1a09b3bb9c6b39d | bando: 3 lotti, 3 CIG, valori, quantità | stazione appaltante (TED) |
| https://ted.europa.eu/it/notice/564730-2023/xml | e4a17818478a92aae348cc344d67f651ba1fe18f3b244e9ce4b4756e291f96f5 | aggiudicazione, oggetto dei lotti | stazione appaltante (TED) |
| BDNCP ANAC nel mirror | per file in `archivio/manifest.jsonl` | padri, attuativi, marchi | ANAC (dato della SA) |

## Proposta per iniziative_ict.yaml

```yaml
- cig: 9158053868
  iniziativa: Consip AQ PC portatili, mobile workstation e Chromebook ed. 1, ID 2425, lotto 1 PC portatili   # non Chromebook
  categoria: hardware
  stato: verificato               # TED Consip (CIG per lotto) + BDNCP
  sottoclasse_s5: postazioni-di-lavoro
  asse_cloud: escluso-certo
  produttori: [Lenovo, HP, Dell, Acer]    # R: dagli oggetti degli attuativi
  giurisdizione_prodotto: EXTRA-UE
  dossier: report/convenzioni/9158053868-pc-portatili-chromebook.md
  documenti:
  - url: https://ted.europa.eu/it/notice/176721-2022/xml
    sha256: 0152855caa6d496f035e9708be478610a2d004ed9598f8fde1a09b3bb9c6b39d
    cosa_conferma: bando TED ID 2425 con i CIG dei 3 lotti
  - url: https://ted.europa.eu/it/notice/564730-2023/xml
    sha256: e4a17818478a92aae348cc344d67f651ba1fe18f3b244e9ce4b4756e291f96f5
    cosa_conferma: aggiudicazione TED ID 2425
- cig: 91580749BC                 # nuovo: lotto 3 Chromebook
  iniziativa: Consip AQ PC portatili, mobile workstation e Chromebook ed. 1, ID 2425, lotto 3 Chromebook
  categoria: hardware
  stato: verificato
  asse_cloud: escluso-certo       # hardware; nota: dipendenza da servizi Google (ChromeOS), licenze di gestione da verificare
  produttori: [Lenovo, Acer]
  dossier: report/convenzioni/9158053868-pc-portatili-chromebook.md
```
