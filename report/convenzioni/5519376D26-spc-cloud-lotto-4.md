# SPC Cloud lotto 4 — realizzazione e gestione di portali e servizi on-line (CIG 5519376D26) — dossier analitico

Versione 0.1 — 2026-11-03 — #55. Bozza per revisione avversariale.
Legenda: **V** verificato su documento archiviato; **V2** due fonti indipendenti di cui una della stazione appaltante; **R** riferito / da verificare.

## 1. Sintesi

- Contratto quadro Consip (gara SPC Cloud, ID SIGEF 1403) con lo stesso RTI del lotto 3: Almaviva (mandataria), Almawave, Indra Italia, Intellera Consulting (ex PwC).
- Oggetto: realizzazione e gestione di portali e servizi on-line (sviluppo, conduzione applicativa, assistenza specialistica): **sviluppo applicativo, non cloud**.
- In BDNCP **626 attuativi**, **763 M€** dichiarati (2017-2023); variante Consip «Lotto 4» +135 M€ (2021). Casi: INPS 37,0 + 27,6 M€, Sogei «nuovo sistema ERP per RGS» 17,3 M€, Banca d'Italia «assistenza specialistica» 13,3 M€.
- Asse A: **non cloud**. Asse B: non pertinente (lente fornitore IT/UE). Hosting accessorio: 2 CIG, 9,7 M€.

## 2. Identificazione

| Campo | Valore | Fonte | Livello |
|---|---|---|---|
| CIG | 5519376D26, «Lotto n. 4 – Servizi di realizzazione e gestione di portali e servizi on-line», SA Consip, 2014 | BDNCP; TED 248256-2021 (Regione Campania) | V2 |
| Aggiudicatario | RTI Almaviva (mandataria), Almawave, Indra Italia, Intellera Consulting | BDNCP aggiudicatari; contratto esecutivo PCM-Casa Italia (CIG 76399763A4); TED 248256-2021 | V2 |
| Massimale | 450.000.000 € (BDNCP); variante +135 M€ (CIG 8734381F34, Consip 2021) | BDNCP | V (fonte unica) |
| Scadenza CQ | 03/08/2022 (TED 248256-2021); proroga al 31/12/2022 (decreto Calabria 17588/2022) | TED; decreto | V2 |
| Gara | procedura ristretta in 4 lotti, bando GUUE S99 del 24/05/2013 | contratto esecutivo PCM | V |

## 3. Cosa contiene

- «Servizi di realizzazione e gestione di portali e servizi on-line» — TED 248256-2021 (Regione Campania, 2,9 M€). **V**
- Schema di contratto esecutivo (PCM – Dipartimento Casa Italia, CE 76399763A4, durata 3 mesi): servizi di «realizzazione e gestione di Portali e Servizi on-line» definiti nel Progetto dei Fabbisogni; nessuna voce di infrastruttura cloud nel testo letto. **V**
- Base di conoscenza (AgID, non archiviato qui): sviluppo, conduzione applicativa, supporto specialistico. **R**

## 4. Analisi degli attuativi

| Anno | n | € |
|---|---:|---:|
| 2017 | 30 | 60.635.952 |
| 2018 | 135 | 145.349.428 |
| 2019 | 129 | 143.474.538 |
| 2020 | 113 | 118.783.919 |
| 2021 | 77 | 121.095.982 |
| 2022 | 141 | 172.810.794 |
| 2023 | 1 | 925.553 |
| **Totale** | **626** | **763.076.166** |

Attuativi (763 M€) > massimale + variante (585 M€): stesse cautele dei lotti 1 e 3.
Anomali (≥ 20 M€): INPS 36,98 M€ (72517773B1, 2017) e 27,6 M€ (8856973D53, 2021).
Classi: sviluppo/manutenzione/portali 431 CIG / 507 M€; «cloud» 188 / 291 M€ (titolo); servizi professionali 64 / 78 M€; interoperabilità 38 / 39 M€; sicurezza 35 / 33 M€; **hosting 2 / 9,7 M€**; migrazione 5 / 4,4 M€. Nessun nome di hyperscaler.
Fuori tema: Acquedotto Lucano 12,1 M€ «rilievi, modellazione, ricerca perdite…» (9478338BF2): uso del lotto per servizi non ICT-portali, da segnalare.
Orfani: 5 CIG, 138,9 M€ di cui 135 M€ = variante Consip.

## 5. Classificazione proposta

- **Asse A**: **non cloud** (escluso certo dalla spesa cloud) per la convenzione; i 2 CIG «hosting» (9,7 M€) restano incerti. Confidenza alta.
- **Asse B**: non pertinente; lente fornitore IT (mandataria) con Indra (ES).
- **Risposta alla domanda «cloud o sviluppo applicativo?»: sviluppo applicativo.**

## 6. Assunzioni e limiti

1. Capitolato Consip non archiviato; contenuto ricostruito da un CE e da un avviso TED di aderenti.
2. L'hosting accessorio (se fornito nei CE) non è quantificato.

## 7. Fonti

| URL | sha256 | Cosa conferma | Tipo |
|---|---|---|---|
| https://ted.europa.eu/it/notice/248256-2021/xml | 2b4e2dba99569558dfce089c00a89f4a18ba01b53e1bf355f8528cabe1330081 | CIG master, RTI, oggetto, scadenza CQ 03/08/2022 | terzo (aderente) |
| https://presidenza.governo.it/AmministrazioneTrasparente/BandiContratti/ANAC_ALLEGATI_PUB/216293_216294_SPC-Cloud-L4_04_CONTRATTO-ESECUTIVO-signed-signed_24927.pdf | dd1b5407f0c704bddb1f124bd18b21ab13bbec28fae99604d055e2494e9c013d | schema CE lotto 4, RTI, oggetto, bando 2013 | terzo (aderente; schema Consip allegato D) |
| https://www.regione.calabria.it/wp-content/uploads/2023/01/decreto-n.-17588-del-30_12_2022.pdf | b527dddf71003875b65aa10528194a1b6da09324bdc60f68d1f347fcebd3416e | proroga lotti 1-4 al 31/12/2022 | terzo |
| BDNCP ANAC (cig, aggiudicatari) | per file in `archivio/manifest.jsonl` | padre Consip 450 M€, variante 135 M€, 626 attuativi | Consip/SA tramite ANAC |

## Proposta per iniziative_ict.yaml

```yaml
- cig: 5519376D26
  iniziativa: Consip SPC Cloud lotto 4, realizzazione di portali e servizi online (SIGEF 1403)
  categoria: servizi-applicativi
  stato: verificato
  asse_cloud: escluso-certo        # sviluppo e gestione applicativa; hosting accessorio in 2 CIG (9,7 M€) incerto
  asse_giurisdizione: n/a
  massimale: 450000000
  variante_cig: 8734381F34         # +135 M€ (2021)
  dossier: report/convenzioni/5519376D26-spc-cloud-lotto-4.md
  documenti_aggiuntivi:
  - url: https://presidenza.governo.it/AmministrazioneTrasparente/BandiContratti/ANAC_ALLEGATI_PUB/216293_216294_SPC-Cloud-L4_04_CONTRATTO-ESECUTIVO-signed-signed_24927.pdf
    sha256: dd1b5407f0c704bddb1f124bd18b21ab13bbec28fae99604d055e2494e9c013d
```
