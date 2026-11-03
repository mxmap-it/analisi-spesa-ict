# AQ System Management ed. 3 — ID 2275 (CIG 893944468E) — dossier analitico

Versione 0.1 — 2026-11-03 — #55. Bozza per revisione avversariale.
Legenda: **V** verificato su documento archiviato; **V2** due fonti indipendenti di cui una della stazione appaltante; **R** riferito / da verificare.
Numeri degli attuativi: `tools/verifiche/attuativi_s5.py` (sul server, esito in `lavoro/convenzioni/attuativi_s5.json`).

## 1. Sintesi

- Due AQ (art. 54 c.4 lett. a «condizioni tutte fissate» e lett. c «con rilancio») su un unico CIG 893944468E, massimale 500 M€ (TED + BDNCP, **V2**).
- Catalogo (Condizioni di fornitura Consip): presidio sistemistico, supporto specialistico, **monitoraggio H24 remoto per server logico dell'ente**, service management a ticket, reperibilità, interventi extra orario. Nessuna voce di hosting, housing o risorse cloud nel listino (V).
- BDNCP: 226 attuativi (2023-2025); 1.495 M€ dichiarati, di cui **1.131 M€ in 6 righe anomale** (massimale copiato o quasi); al netto 364,3 M€ (0,73 del massimale).
- 11 attuativi citano il cloud (22,9 M€): soprattutto **migrazione** (PNRR 1.2, SAP in cloud per LTF) e gestione di sistemi «on premise e in cloud».
- Proposta: **S5 confermata**, asse cloud escluso certo per il catalogo; incerti i soli attuativi di migrazione.

## 2. Identificazione

| Campo | Valore | Fonte | Livello |
|---|---|---|---|
| CIG | 893944468E, «CIG Lotto 1» | TED 565879-2022 (II.1.1); BDNCP | V2 |
| Gara | procedura aperta d.lgs. 50/2016, due AQ, ID Sigef 2275, bando 2021/S 211-553938 | TED 565879-2022; Condizioni di fornitura Consip | V2 |
| Pubblicazione | 29/10/2021 (BDNCP) | BDNCP | V (fonte unica) |
| Massimale | 500.000.000 €; quote lett. a: RTI Fastweb-Accenture-Atos-Consielte 125 M€, RTI Enterprise Services-Engineering D.Hub-Eustema-DGS 75 M€; lett. c: 300 M€ | TED 565879-2022; Condizioni di fornitura (125 M€/75 M€) | V2 |
| Aggiudicatari lett. c | anche RTI Almaviva-Leonardo-SMI-Net Service-Eurolink-Telecom Italia | TED 565879-2022; BDNCP aggiudicatari | V2 |
| Aggiudicazione | 13/09/2022 | TED 565879-2022 | V (Consip via TED) |
| Durata AQ | 730 giorni (BDNCP «DURATA_PREVISTA») | BDNCP | V fonte unica → R |

## 3. Cosa contiene

Dalle Condizioni di fornitura (Tab. 2.3): PRS presidio sistemistico (FTE/anno: ICT operations manager, security manager, system/DB/network administrator, service desk agent…), SSR supporto specialistico (giornate), MON monitoraggio H24 remoto (canone per **server logico** dell'amministrazione, fasce 1-300/301-600/>600), SMA service management (change standard a ticket), RPR reperibilità, EXT intervento extra orario. Servizi accessori nel rilancio: monitoraggio H24 on-site, manutenzione hardware, supporto ambienti client. **V**
Nessuna voce di prezzo per hosting, housing, IaaS/PaaS/SaaS. **V** (assenza nel listino; il capitolato tecnico non è stato letto).

## 4. Analisi degli attuativi (BDNCP)

| Misura | Valore |
|---|---|
| attuativi | 226 (2023: 79; 2024: 132; 2025: 15) |
| euro dichiarati lordi | 1.495.058.708 |
| anomali (≥ 125 M€) | 6 righe, 1.130,7 M€: ZES/Agenzia attrazione investimenti 274,8 M€, ASL Avellino 229,5 M€, ASL NA3 Sud 2×181,2 M€, Policlinico Bari 2×131,9 M€ |
| euro puliti | 364.336.258 (0,73 del massimale); 2023 125,0 M€, 2024 215,9 M€, 2025 23,4 M€ |
| mediana / p90 | 1,13 M€ / 2,67 M€ |
| possibili doppioni | 40 righe, 39,5 M€ (es. LTF «migrazione cloud e conduzione SAP» 4 CIG da 1,63 M€) |
| oggetto con «cloud» | 11 / 22,9 M€ |
| oggetto con SOC/monitoraggio | 4 / 5,0 M€ |
| aggiudicatari più frequenti | Fastweb (103), Enterprise Services Italia (76), Nexthera (28), Accenture (26), Lutech (26) |

Le righe anomale sono quasi certamente l'importo dell'AQ o di una quota trascritto dall'ente: la somma lorda (2,99 volte il massimale) è impossibile.

## 5. Classificazione proposta

- **S5 – consulenza IT infrastrutturale in-house**; confidenza **alta** sul catalogo, **media** sul totale degli attuativi (oggetti generici).
- Asse cloud: escluso certo; sottoclasse «migrazione» per gli 11 attuativi con cloud nell'oggetto (incerti).
- Lente fornitore: mandatarie italiane (Fastweb, Enterprise Services Italia — gruppo DXC, USA — Almaviva).

## 6. Assunzioni e limiti

- Il capitolato tecnico dell'ID 2275 non è archiviato: l'assenza di hosting/cloud è dedotta dal listino delle Condizioni di fornitura e dalla continuità con l'ed. 4 (dove è esplicita).
- Soglia degli anomali (25 % del massimale) arbitraria; doppioni non sottratti.
- BDNCP indica un solo CIG per due AQ: la ripartizione tra lett. a e lett. c degli attuativi non è ricostruibile.

## 7. Fonti

| URL | sha256 | Cosa conferma | Tipo |
|---|---|---|---|
| https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID%202275%20AQ%20System%20Management%203%20-%20Condizioni%20di%20fornitura.pdf | 9d3ade94c344e1ecfeba3f46919aa59204a099ef21e2c3899b748c373bfb0f9b | catalogo e quote 125/75 M€ | stazione appaltante |
| https://ted.europa.eu/it/notice/565879-2022/xml | 7d5c92766e20b0461f86683e99cdbc171b4bae4aa72234ea9f19e73817f50d1e | CIG lotto 1, aggiudicatari, 500 M€ | stazione appaltante (TED) |
| BDNCP ANAC nel mirror | per file in `archivio/manifest.jsonl` | padre e 226 attuativi | ANAC (dato della SA) |

## Proposta per iniziative_ict.yaml

```yaml
- cig: 893944468E
  iniziativa: Consip AQ System management ed. 3, ID 2275 (due AQ, lett. a e c)
  categoria: system-management
  stato: verificato
  sottoclasse_s5: consulenza-it-infrastrutturale
  asse_cloud: escluso-certo       # listino senza hosting/cloud; attuativi di migrazione da riesaminare
  massimale: 500000000
  dossier: report/convenzioni/893944468E-system-management-3.md
  documenti_aggiuntivi:
  - url: https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID%202275%20AQ%20System%20Management%203%20-%20Condizioni%20di%20fornitura.pdf
    sha256: 9d3ade94c344e1ecfeba3f46919aa59204a099ef21e2c3899b748c373bfb0f9b
    cosa_conferma: catalogo servizi (presidio, supporto, monitoraggio per server logico), quote massimale
```
