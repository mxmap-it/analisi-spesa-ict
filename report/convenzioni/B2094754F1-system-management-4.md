# AQ System Management ed. 4 — ID 2710 (CIG B2094754F1) — dossier analitico

Versione 0.1 — 2026-11-03 — #55. Bozza per revisione avversariale.
Legenda: **V** verificato su documento archiviato; **V2** due fonti indipendenti di cui una della stazione appaltante; **R** riferito / da verificare.
Numeri degli attuativi: `tools/verifiche/attuativi_s5.py` (sul server, nice, streaming; esito in `lavoro/convenzioni/attuativi_s5.json`).

## 1. Sintesi

- **Legame CIG↔gara chiuso**: il Capitolato d'oneri Consip dell'ID 2710 riporta testualmente «CIG B2094754F1» (V); BDNCP concorda (oggetto «… ID 2710», 720.051.840 €, pubblicazione 11/06/2024 = data GUUE, aggiudicatari = membri dei 4 RTI dell'avviso di esito). **V2**.
- Servizi professionali di conduzione di infrastrutture **dell'amministrazione** (presidio, supporto specialistico, monitoraggio H24 da remoto). Il CTS **esclude** espressamente hosting/housing presso il fornitore e fornitura di risorse cloud IaaS/PaaS/SaaS (V).
- Componente cloud marginale e **senza prezzo separato**: lo strumento di monitoraggio può essere SaaS di un CSP qualificato ACN (QC1/QI1) a scelta del fornitore; la «gestione sistemi» comprende anche risorse cloud **acquistate altrove** dall'ente (V).
- BDNCP: 112 attuativi (2025-2026), 431,7 M€ dichiarati, nessun importo anomalo; 3 attuativi con «cloud» nell'oggetto (16,6 M€: migrazioni PNRR 1.2 e «technology & cloud» CDP).
- Proposta: **S5 confermata** (consulenza IT infrastrutturale in-house); asse cloud **escluso certo**, salvo gli attuativi di migrazione da riesaminare.

## 2. Identificazione

| Campo | Valore | Fonte | Livello |
|---|---|---|---|
| CIG | B2094754F1, lotto unico | Capitolato d'oneri ID 2710 (zip Consip «DOC NON UFF»): «codice NUTS IT, CIG B2094754F1»; BDNCP | V2 |
| Gara | procedura aperta d.lgs. 36/2023, AQ System Management ed. 4 | TED 342482-2024; pagina Consip aq-system-management-ed4; BDNCP | V2 |
| Pubblicazione | GUUE S 112 del 11/06/2024; PVL ANAC 12/06/2024 | pagina Consip (cronologia); TED | V2 |
| Massimale | 720.051.840 € (incrementabile del 20 %); «valore massimo AQ» nell'avviso di esito 1.540.201.600 € | TED 342482-2024 e 605358-2025; avviso di esito Consip; BDNCP | V2 (il 1.540 M€ non riconciliato) |
| Aggiudicatari | 4 RTI: Telecom Italia (offerta 448,05 M€), Almaviva (406,05 M€), Fastweb (364,05 M€), Engineering D.Hub (322,05 M€) | TED 605358-2025; avviso di esito Consip; BDNCP aggiudicatari (34 imprese coerenti) | V2 |
| Date | selezione 29/05/2025; aggiudicazione efficace 11/06/2025; conclusione AQ 08/08/2025 | pagina Consip; TED 605358-2025 | V2 |
| Durata | non letta | — | R |

Gli avvisi eForms non riportano il CIG: il legame viene dal documento della stazione appaltante, controvalidato da BDNCP.

## 3. Cosa contiene (CTS ID 2710)

- Servizi base: presidio operativo, supporto specialistico, monitoraggio H24 da remoto; opzionali tra cui reperibilità e manutenzione hardware accessoria. **V**
- Esclusione (CTS §2): la fornitura «non prevede la fornitura di apparecchiature hardware o prodotti software, l'hosting/housing delle infrastrutture tecnologiche presso la sede del Fornitore o la fornitura di risorse cloud (IaaS, PaaS, SaaS, etc.)». **V**
- Ambito: infrastrutture dell'ente tradizionali o cloud (privato, pubblico, ibrido); la gestione sistemi include «risorse elaborative acquisite da Cloud Service Provider esterni» (CTS §5.1.1). **V** — il cloud è oggetto di gestione, non di fornitura.
- Centro Servizi del fornitore nell'**UE**, oppure monitoraggio in **SaaS di CSP** qualificato ACN (QC1 su QI1), «senza oneri aggiuntivi»; exit strategy di 30 giorni (CTS §4.3, §6.4). **V**
- Personale presso le sedi dell'ente, salvo il monitoraggio da remoto (CTS §4.4). **V**

## 4. Analisi degli attuativi (BDNCP)

| Misura | Valore |
|---|---|
| attuativi (ultima versione, non cancellati) | 112 |
| euro dichiarati | 431.706.957 (0,60 del massimale) |
| per anno | 2025: 49 / 145,4 M€; 2026: 63 / 286,3 M€ |
| mediana / p90 | 1,88 M€ / 11,2 M€ |
| anomali (≥ 25 % del massimale) | 0 |
| possibili doppioni (stessa SA e importo) | 5 righe, 40,7 M€ |
| sotto 500 € | 1 |
| CPV prevalenti | gestione connessa all'informatica (68), consulenza in sistemi (18) |
| aggiudicatari più frequenti | TIM (56), Almaviva (17), Engineering D.Hub (16), Fastweb (14) |
| oggetto con «cloud» | 3 / 16,6 M€: Siracusa migrazione al cloud PNRR (2 CIG da 442.903 €, probabile doppione), CDP «technology & cloud» (15,7 M€) |
| oggetto con SOC/monitoraggio | 7 / 15,6 M€ |

## 5. Classificazione proposta

- Categoria system-management; **S5 – consulenza IT infrastrutturale per infrastrutture in-house**. Confidenza **alta** (esclusione testuale nel CTS).
- Asse cloud: **escluso certo** come spesa cloud; i 3 attuativi di migrazione → sottoclasse «migrazione», incerti.
- Componente cloud interna: strumento di monitoraggio eventualmente SaaS (nessun prezzo separato): dipendenza da registrare, non spesa.
- Lente fornitore: mandatarie italiane; mandanti di gruppi USA (Kyndryl, IBM, Accenture, Avanade). Centro servizi in UE (V).

## 6. Assunzioni e limiti

- CTS e C.d.O. letti nella versione non firmata dello zip Consip; si assume identica a quella firmata.
- Offerte tecniche non lette: non sappiamo se il monitoraggio è SaaS e di quale CSP.
- Importi BDNCP = importo dichiarato al CIG derivato, non speso; doppioni non sottratti.
- Il «valore massimo» 1.540 M€ dell'avviso di esito non è riconciliato con 720 M€ (+20 %).

## 7. Fonti

| URL | sha256 | Cosa conferma | Tipo |
|---|---|---|---|
| https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID%202710%20DOC%20NON%20UFF.zip | 5cd1f43729f0fb5c3958205d77a6e41debf2a324fb21b4de08c176594db23a67 | C.d.O. (file interno 875fb607ef2806183b1fcecfe2dec8d34b41b454b0c144f073bc6b267babfa80): CIG; CTS (b27fc7a7fcdd96489a13cbfe83d1c83dbaa51f7b57c6bd71d4758f9a7201e985): esclusione cloud/hosting, centro servizi UE, SaaS | stazione appaltante |
| https://www.consip.it/bandi/aq-system-management-ed4 | ef3d231599a30c2e7ae9f535c6c10abe5eb253b63020ebb2108557c6993789ba | cronologia, aggiudicazione | stazione appaltante |
| https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID%202710%20AVVISO%20DI%20ESITO%20GUUE%20S%20177%2016-09-2025.pdf | 88d49e788bf70df3a19bc28a5acebbcf69f79c88e7f26dc794aa5538633414b6 | valori e 4 RTI | stazione appaltante |
| https://ted.europa.eu/it/notice/342482-2024/xml | b7fe91c2486ad3a5fe0b3152894ff61eafe74ae943e2644040c41a0a32497459 | bando, 720.051.840 € | stazione appaltante (TED) |
| https://ted.europa.eu/it/notice/605358-2025/xml | 7ee2cb429bc8d6e1cdc8ab5b7561430aded312a49cf42ff9d755a95b42542234 | aggiudicazione | stazione appaltante (TED) |
| BDNCP ANAC (cig, aggiudicatari) nel mirror | per file in `archivio/manifest.jsonl` | padre e attuativi | ANAC (dato della SA) |

## Proposta per iniziative_ict.yaml

```yaml
- cig: B2094754F1
  iniziativa: Consip AQ System management ed. 4, ID 2710 (lotto unico)
  categoria: system-management
  stato: verificato               # CIG nel Capitolato d'oneri Consip + BDNCP (oggetto, importo, data, aggiudicatari)
  sottoclasse_s5: consulenza-it-infrastrutturale
  asse_cloud: escluso-certo       # CTS §2: esclusi hosting/housing e risorse IaaS/PaaS/SaaS
  massimale: 720051840
  dossier: report/convenzioni/B2094754F1-system-management-4.md
  documenti:
  - url: https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID%202710%20DOC%20NON%20UFF.zip
    sha256: 5cd1f43729f0fb5c3958205d77a6e41debf2a324fb21b4de08c176594db23a67
    cosa_conferma: "Capitolato d'oneri: CIG B2094754F1; CTS: esclusi hosting e risorse cloud"
  - url: https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID%202710%20AVVISO%20DI%20ESITO%20GUUE%20S%20177%2016-09-2025.pdf
    sha256: 88d49e788bf70df3a19bc28a5acebbcf69f79c88e7f26dc794aa5538633414b6
    cosa_conferma: esito, 4 RTI aggiudicatari
```
