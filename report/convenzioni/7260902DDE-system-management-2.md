# AQ System Management ed. 2 — ID 1836 (CIG 7260902DDE) — dossier analitico

Versione 0.1 — 2026-11-03 — #55. Bozza per revisione avversariale.
Legenda: **V** verificato su documento archiviato; **V2** due fonti indipendenti di cui una della stazione appaltante; **R** riferito / da verificare.
Numeri degli attuativi: `tools/verifiche/attuativi_s5.py` (sul server, esito in `lavoro/convenzioni/attuativi_s5.json`).

## 1. Sintesi

- AQ multi-operatore con **appalti specifici** (art. 54 c.4 lett. c), ID Sigef 1836, CIG 7260902DDE, valore stimato 302.120.512 € (TED + pagina Consip + BDNCP, **V2**).
- Oggetto: servizi di System Management (CPV 72250000, 72510000, 72600000); contratti da 12 a 60 mesi.
- BDNCP: 31 appalti specifici (2020-2025), 554 M€ lordi; 1 anomalo (INPS 145,3 M€); al netto 408,9 M€ (1,35 del valore stimato: gli AS possono superarlo per ricalcolo dei ribassi, ma il dato va letto con cautela).
- Due AS riguardano data center e disaster recovery (Roma Capitale 23,1 M€; IFO 0,19 M€): conduzione di DC dell'ente, non hosting presso il fornitore (da verificare per IFO).
- Proposta: **S5** (consulenza IT infrastrutturale); asse cloud escluso, con confidenza **media** (capitolato non letto).

## 2. Identificazione

| Campo | Valore | Fonte | Livello |
|---|---|---|---|
| CIG | 7260902DDE | TED 455199-2017 («ID Sigef 1836 — CIG: 7260902DDE»); BDNCP | V2 |
| Gara | procedura aperta d.lgs. 50/2016, AQ lett. c | TED 455199-2017; pagina Consip aq-system-management-2 | V2 |
| Date | indizione 10/11/2017; GUUE S 219 15/11/2017; aggiudicazione 16/07/2019; avviso di esito 09/05/2024 | pagina Consip | V (fonte unica SA) |
| Valore stimato | 302.120.512 € | TED; BDNCP | V2 |
| Durata AQ | 24 mesi + proroga max 12; AS 12-60 mesi | TED 455199-2017 | V (Consip via TED) |
| Aggiudicatari | 17 imprese in BDNCP (Accenture, Almaviva, Enterprise Services Italia, Fastweb, HP Italiana, Kyndryl, Leonardo, Lutech, Present, Reply…) | BDNCP aggiudicatari | V fonte unica → R (avviso di esito non archiviato) |

## 3. Cosa contiene

Dal bando (TED): «prestazione di servizi di System Management per le Pubbliche Amministrazioni», luogo di esecuzione «presso gli uffici delle Pubbliche Amministrazioni». **V**. Capitolato tecnico non archiviato: il dettaglio (presidio, monitoraggio, gestione sistemi) è **R** per analogia con le ed. 3 e 4.

## 4. Analisi degli attuativi (BDNCP)

| Misura | Valore |
|---|---|
| appalti specifici | 31 (2020: 5; 2021: 14; 2022: 11; 2025: 1) |
| euro lordi / puliti | 554.191.470 / 408.877.190 |
| anomalo | INPS 88089141CC, 145,3 M€ «conduzione operativa e supporto specialistico» (plausibile come importo reale: AS grande; escluso solo per regola) |
| mediana / p90 | 10,3 M€ / 34,2 M€ |
| per anno (puliti) | 2020 53,6 M€; 2021 160,8 M€; 2022 191,2 M€; 2025 3,3 M€ |
| oggetto con «cloud»/DC | 2 / 23,3 M€ (Roma Capitale DC e sito DR; IFO «servizio di disaster recovery») |
| SOC/monitoraggio | 5 / 91,1 M€ (gestione, assistenza e monitoraggio ICT: ULSS 3, ULSS 7, ASP Catanzaro, Regione Veneto, USL Umbria 1) |
| aggiudicatari più frequenti | Fastweb (12), HP Italiana (11), Present (9), Lutech (8) |

## 5. Classificazione proposta

- **S5 – consulenza IT infrastrutturale in-house**; confidenza media.
- Asse cloud: escluso (nessun elemento di fornitura cloud); IFO «servizio di disaster recovery» va letto: un DR erogato da sito del fornitore sarebbe hosting.
- Lente fornitore: presenti HP Italiana (USA) e Kyndryl (USA) tra gli esecutori.

## 6. Assunzioni e limiti

- Capitolato e avviso di esito non archiviati in questa sessione (lo zip documentazione è sulla pagina Consip); l'assenza di hosting è un'inferenza.
- Rapporto puliti/valore stimato > 1: o il valore BDNCP degli AS include opzioni/rinnovi, o restano importi gonfiati.

## 7. Fonti

| URL | sha256 | Cosa conferma | Tipo |
|---|---|---|---|
| https://ted.europa.eu/it/notice/455199-2017/xml | 9f87a64642df50b36752e8f320d165f1e76fa0aefb02254af771be3069327f5b | CIG, oggetto, durata, valore | stazione appaltante (TED) |
| https://www.consip.it/bandi/aq-system-management-2 | b031db92f7eeaa999cc479760be7b3712a593a790b0deb3386274bca21ce2a88 | ID 1836 ed. 2, cronologia | stazione appaltante |
| BDNCP ANAC nel mirror | per file in `archivio/manifest.jsonl` | padre, 17 aggiudicatari, 31 AS | ANAC (dato della SA) |

## Proposta per iniziative_ict.yaml

```yaml
- cig: 7260902DDE
  iniziativa: Consip AQ System management ed. 2, ID 1836 (appalti specifici)
  categoria: system-management
  stato: verificato
  sottoclasse_s5: consulenza-it-infrastrutturale
  asse_cloud: escluso-certo       # confidenza media: capitolato non letto; IFO disaster recovery da verificare
  massimale: 302120512
  dossier: report/convenzioni/7260902DDE-system-management-2.md
  documenti_aggiuntivi:
  - url: https://www.consip.it/bandi/aq-system-management-2
    sha256: b031db92f7eeaa999cc479760be7b3712a593a790b0deb3386274bca21ce2a88
    cosa_conferma: pagina iniziativa ID 1836, cronologia
```
