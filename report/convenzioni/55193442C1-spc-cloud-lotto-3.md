# SPC Cloud lotto 3 — interoperabilità per i dati e cooperazione applicativa (CIG 55193442C1) — dossier analitico

Versione 0.1 — 2026-11-03 — #55. Bozza per revisione avversariale.
Legenda: **V** verificato su documento archiviato; **V2** due fonti indipendenti di cui una della stazione appaltante; **R** riferito / da verificare.

## 1. Sintesi

- Contratto quadro Consip (gara SPC Cloud, ID SIGEF 1403) con il RTI Almaviva (mandataria), Almawave, Indra Italia, PwC Public Sector (ora Intellera Consulting).
- Oggetto: servizi di interoperabilità per i dati (integrazione dati e metadati, open data, big data) e di cooperazione applicativa: **sviluppo e servizi professionali, non cloud**. Il nome «SPC Cloud» viene dal titolo della gara, comune ai 4 lotti.
- In BDNCP **421 attuativi**, **718 M€** dichiarati (2015-2023); INPS da solo ~142 M€ in 4 CIG; variante Consip «Lotto 3» +120 M€ (2021).
- Asse A: **non cloud** (servizi applicativi); possibile hosting accessorio non quantificato. Asse B: non applicabile come prodotto cloud; lente fornitore IT/UE (Indra è spagnola).

## 2. Identificazione

| Campo | Valore | Fonte | Livello |
|---|---|---|---|
| CIG | 55193442C1, «Lotto n. 3 – Servizi di interoperabilità per i dati e di cooperazione applicativa», SA Consip, 2014 | BDNCP; TED 248255-2021 (Regione Campania) | V2 |
| Aggiudicatario | RTI Almaviva (mandataria), Almawave, Indra Italia, Intellera Consulting (ex PwC Public Sector) | BDNCP aggiudicatari; TED 248255-2021 | V2 |
| Massimale | 400.000.000 € (BDNCP); variante +120 M€ (CIG 87343673AA, Consip 2021) | BDNCP | V (fonte unica) |
| Scadenza CQ | 30/03/2022 secondo Regione Campania (TED 248255-2021); 31/12/2022 secondo AgID det. 293/2022 (base di conoscenza) e decreto Calabria 17588/2022 | TED; decreto Calabria | V2 sulla proroga al 31/12/2022 |
| Bando | GUUE S99 del 24/05/2013 (procedura ristretta, 4 lotti) | schema CE lotto 4 PCM | V |

## 3. Cosa contiene

- «Acquisto di servizi di interoperabilità per i dati finalizzati a garantire l'integrazione dei dati e dei metadati, la gestione di dati di tipo aperto, nonché la gestione dei Big Data» — TED 248255-2021 (Regione Campania, 5,3 M€, progetto «Move to cloud ecosistema digitale per la cultura»). **V**
- Base di conoscenza (AgID det. 194/2017, 293/2022, letti il 29/10 ma **non archiviati**: gli URL trasparenza.agid.gov.it oggi danno «assente»): web services, orchestrazione, open data, supporto big data (voce L3.S7). **R** in questo dossier.
- Nessun prodotto cloud a listino nei documenti letti. AgID 194/2017 parla di «ambienti di sviluppo e di esercizio» acquisiti col CE (R): possibile componente infrastrutturale accessoria.

## 4. Analisi degli attuativi

| Anno | n | € |
|---|---:|---:|
| 2015 | 1 | 475.115 |
| 2017 | 32 | 35.750.228 |
| 2018 | 42 | 75.451.431 |
| 2019 | 61 | 94.179.477 |
| 2020 | 74 | 99.684.343 |
| 2021 | 116 | 224.578.783 |
| 2022 | 94 | 187.382.693 |
| 2023 | 1 | 127.900 |
| **Totale** | **421** | **717.629.970** |

Attuativi (718 M€) > massimale + variante (520 M€): stesse cautele del lotto 1 (valori di contratto, proroghe, doppi CIG).
Anomali (≥ 20 M€): INPS 57,3 M€ (957101074E, 2022), 37,3 M€ (8962347AB4, 2021), 24,7 M€ (86210099AD, 2021), 22,3 M€ (8031950ECE, 2019).
Classi: sviluppo/manutenzione 247 CIG / 360 M€; interoperabilità 163 / 247 M€; «cloud» 134 / 358 M€ (quasi sempre il titolo «SPC Cloud»); servizi professionali 53 / 70 M€; migrazione 3 / 18 M€. Nessun CIG con housing, hosting, IaaS/PaaS/SaaS o nomi di hyperscaler.
Orfani: 6 CIG, 131,5 M€ di cui 120 M€ = variante Consip.

## 5. Classificazione proposta

- **Asse A**: **non cloud** (escluso certo dalla spesa cloud): servizi di sviluppo/integrazione/professionali. Confidenza alta per la convenzione; media per i singoli CIG con «migrazione» (3 CIG, 18 M€: da leggere).
- **Asse B**: non pertinente (nessun prodotto cloud). Lente fornitore: RTI a mandataria italiana; Indra Italia controllata da Indra Sistemas (Spagna, UE). Da registrare come spesa ICT in servizi, giurisdizione fornitore IT/UE.
- **Risposta alla domanda «cloud o sviluppo applicativo?»: sviluppo applicativo e servizi professionali.**
- Stato proposto: verificato (identificazione); da ricategorizzare `servizi-applicativi` (già così).

## 6. Assunzioni e limiti

1. Capitolato Consip non archiviato; atti AgID letti in passato ora non scaricabili (URL «assente»): la descrizione dettagliata resta R finché non si archivia una copia.
2. «Non cloud» è una classificazione per prevalenza: eventuali ambienti di esercizio forniti col CE non sono quantificati.
3. Discrepanza sulla scadenza (30/03/2022 vs 31/12/2022) dovuta a proroghe successive.

## 7. Fonti

| URL | sha256 | Cosa conferma | Tipo |
|---|---|---|---|
| https://ted.europa.eu/it/notice/248255-2021/xml | ac4f6ebff2f1a8937041e2566df1bca832aa5cfd3c2172730e29b128b6e95f15 | CIG master, RTI, oggetto (integrazione dati, open data, big data), CE 77407057D6 5,3 M€ | terzo (aderente) |
| https://www.regione.calabria.it/wp-content/uploads/2023/01/decreto-n.-17588-del-30_12_2022.pdf | b527dddf71003875b65aa10528194a1b6da09324bdc60f68d1f347fcebd3416e | proroga lotti 1-4 al 31/12/2022 | terzo (aderente) |
| https://presidenza.governo.it/AmministrazioneTrasparente/BandiContratti/ANAC_ALLEGATI_PUB/216293_216294_SPC-Cloud-L4_04_CONTRATTO-ESECUTIVO-signed-signed_24927.pdf | dd1b5407f0c704bddb1f124bd18b21ab13bbec28fae99604d055e2494e9c013d | titolo della gara a 4 lotti, bando GUUE S99/2013 | terzo (aderente) |
| BDNCP ANAC (cig, aggiudicatari) | per file in `archivio/manifest.jsonl` | padre Consip 400 M€, variante 120 M€, 421 attuativi, RTI | Consip/SA tramite ANAC |

## Proposta per iniziative_ict.yaml

```yaml
- cig: 55193442C1
  iniziativa: Consip SPC Cloud lotto 3, interoperabilità e cooperazione applicativa (SIGEF 1403)
  categoria: servizi-applicativi
  stato: verificato
  asse_cloud: escluso-certo        # sviluppo/integrazione/servizi professionali; «cloud» è solo nel titolo della gara
  asse_giurisdizione: n/a          # lente fornitore: RTI Almaviva (IT) con Indra (ES)
  massimale: 400000000
  variante_cig: 87343673AA         # +120 M€ (2021)
  dossier: report/convenzioni/55193442C1-spc-cloud-lotto-3.md
```
