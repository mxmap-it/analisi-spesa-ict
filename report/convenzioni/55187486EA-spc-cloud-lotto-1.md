# SPC Cloud lotto 1 — servizi di cloud computing (CIG 55187486EA) — dossier analitico

Versione 0.1 — 2026-11-03 — #55. Bozza per revisione avversariale.
Legenda: **V** verificato su documento archiviato; **V2** due fonti indipendenti di cui una della stazione appaltante; **R** riferito / da verificare.

## 1. Sintesi

- Contratto quadro Consip (gara SPC Cloud, ID SIGEF 1403, 4 lotti) col RTI TIM (mandataria), Enterprise Services Italia (ex HPE, gruppo DXC), Poste Italiane, Postel, Postecom; stipulato il 20/05/2016, prorogato fino al 31/12/2022 e con plafond esaurito nel 2022.
- Contiene servizi IaaS (Virtual Data Center), PaaS (DB, es. SQL Server), BaaS (backup), SaaS e servizi professionali di «Cloud Enabling» (porting, reingegnerizzazione).
- In BDNCP **1.372 attuativi**, **961 M€** dichiarati (picco 2021: 291 M€); variante Consip «Lotto 1 – variante SPC Cloud» +150 M€ (2021).
- Asse A: **cloud prevalente con quota di servizi professionali**; quota non stimabile dagli oggetti CIG (gli enti scrivono «cloud computing» anche per lo sviluppo).
- Asse B: **IT** per l'erogazione (DC del RTI in Italia, mandataria italiana); dipendenze tecnologiche USA (Microsoft SQL Server nel PaaS; stack di virtualizzazione non letto); un mandante (Enterprise Services Italia) appartiene a un gruppo USA (lente fornitore).

## 2. Identificazione

| Campo | Valore | Fonte | Livello |
|---|---|---|---|
| CIG | 55187486EA, «Lotto 1 – Servizi di cloud computing», SA Consip, pubblicato 2014 | BDNCP; det. Ministero dell'Interno 2022; det. ART 138/2021 | V2 (Consip in BDNCP + atti di aderenti) |
| Gara | procedura ristretta in 4 lotti «servizi di Cloud Computing, di Sicurezza, di Realizzazione di Portali e Servizi on-line e di Cooperazione Applicativa», bando GUUE S99 del 24/05/2013 | schema di Contratto esecutivo lotto 4 (PCM) | V (bando non archiviato) |
| Aggiudicatario | RTI TIM (mandataria), Enterprise Services Italia S.r.l. (ex HPE Services Italia), Poste Italiane, Postel, Postecom | BDNCP aggiudicatari (Postecom assente); det. Interno; TED 647656-2021 | V2 |
| Stipula CQ | 20/05/2016 | TED 647656-2021 (ARNAS Garibaldi) | V a fonte unica di terzo → R |
| Massimale | 500.000.000 € (importo lotto in BDNCP); variante +150 M€ (CIG 8734352748, Consip, 2021, «Lotto 1 – variante SPC Cloud – ID 1403») | BDNCP | V (fonte unica: Consip in BDNCP) |
| Durata / scadenza | proroga 24 mesi a 20/07/2021 (com. Consip 17/01/2018), addendum a 20/07/2022, poi 31/12/2022 | det. ART 138/2021; delibera AGCOM 282/22/CONS; decreto Regione Calabria 17588/2022 | V2 (atti di aderenti che citano comunicazioni Consip) |
| Esaurimento | «erosione totale del plafond» del CQ lotto 1 | delibera AGCOM 282/22/CONS | V a fonte unica → R |

## 3. Cosa contiene

Dagli atti degli aderenti (manca il capitolato tecnico Consip, non archiviato):

- **IaaS**: Virtual Data Center (VDC) — det. ART 138/2021 (voce «IaaS VDC», canone mensile). **V**
- **PaaS**: database (es. «PaaS L1.S2 SQL Server») — det. ART 138/2021. **V**
- **BaaS**: backup remoto — det. ART 138/2021; det. Interno 2022. **V**
- **Hosting** di siti web — delibera AGCOM 282/22 («gestione delle piattaforme di Hosting del sito web»). **V**
- **Cloud Enabling** (servizi professionali: adattamento, reingegnerizzazione, porting) — det. Interno 2022. **V**
- SaaS: citato nella base di conoscenza (riferito), non visto negli atti letti. **R**
- Data center: del RTI (TIM/Poste) in Italia — base di conoscenza, **R** (nessun documento letto elenca i siti).
- Prodotti: SQL Server (Microsoft, USA) a listino PaaS **V**; hypervisor/stack (VMware? HPE?) **non verificato**.

Nessun hyperscaler extra-UE risulta a listino nei documenti letti (assenza di prova, non prova di assenza).

## 4. Analisi degli attuativi (BDNCP)

Script `tools/verifiche/attuativi_convenzioni.py` (streaming, `nice`), esiti in `lavoro/convenzioni-55/`.

| Anno | n | € |
|---|---:|---:|
| 2012-2014 | 3 | 588.277 (date di pubblicazione anteriori al CQ: errori o CIG riusati) |
| 2016 | 20 | 11.858.589 |
| 2017 | 131 | 72.508.712 |
| 2018 | 174 | 80.236.789 |
| 2019 | 223 | 146.831.214 |
| 2020 | 261 | 170.259.217 |
| 2021 | 353 | 290.691.306 |
| 2022 | 196 | 183.241.114 |
| 2023-2025 | 11 | 4.966.617 (dopo la scadenza: proroghe tecniche o errori) |
| **Totale** | **1.372** | **961.181.836** |

Il totale degli attuativi (961 M€) supera il massimale (500 M€ + 150 M€ di variante = 650 M€) di ~48 %: gli importi dichiarati sono valori di contratto, includono proroghe registrate come nuovi CIG e probabili doppi conteggi (CE + addendum). Da non sommare come spesa.

Importi anomali (≥ 20 M€): Regione Puglia 29,2 M€ (8100621BE9, 2019), MIT 21,0 M€ (9133998D96, 2022). Nessun massimale copiato.

Classi (regex): «cloud» 1.134 CIG / 751 M€; sviluppo/manutenzione 260 / 204 M€; sicurezza 143 / 113 M€ (spesso è il titolo della gara); interoperabilità 126 / 98 M€; servizi professionali 101 / 52 M€; IaaS/PaaS/SaaS 42 / 20 M€; migrazione 31 / 14 M€; hosting 6; menzioni oracle/azure/hybrid 6 CIG, ~7 M€ (da leggere: probabilmente licenze o PaaS DB).
Orfani (oggetto «SPC cloud … lotto 1» senza legame al padre): 102 CIG, 175,7 M€ di cui 150 M€ = la variante Consip.

## 5. Classificazione proposta

- **Asse A**: padre = massimale (escluso). Attuativi: **cloud (IaaS/PaaS/BaaS) con componente di servizi professionali** («Cloud Enabling»). Quota servizi non stimabile dagli oggetti; esempio letto: Interno 2022 mette in un unico importo (1,47 M€) canoni e servizi professionali. Proposta: stato «incluso certo» per l'asse cloud a livello di convenzione, con avvertenza «quota servizi ignota». Confidenza media.
- **Asse B**: **IT** (erogazione da DC italiani di RTI a mandataria italiana), dipendenze USA (Microsoft SQL Server; stack di virtualizzazione da verificare). Lente fornitore: Enterprise Services Italia (gruppo DXC, USA) mandante, quote di esecuzione ignote. Confidenza media.
- Stato proposto: resta **verificato** (identificazione).

## 6. Assunzioni e limiti

1. Capitolato tecnico e listino Consip non archiviati: il contenuto è ricostruito dagli atti di tre aderenti.
2. Data center del RTI: riferiti, non letti.
3. La lente prodotto assume che il «cloud SPC» sia infrastruttura del RTI e non rivendita di cloud pubblico: nessun atto letto la contraddice, ma nessun atto Consip la conferma.
4. Importi BDNCP non deduplicati per proroghe/addendum.

## 7. Fonti

| URL | sha256 | Cosa conferma | Tipo |
|---|---|---|---|
| https://www.interno.gov.it/sites/default/files/2022-05/9184438600_determina_servizi_contratto_quadro_spc_cloud_lotto1_rti_telecom-signed.pdf | c4d4f217e9442135f84fb4ce796260427cabff5e9615595d41db53868e569c22 | RTI, CIG 55187486EA, IaaS/PaaS/BaaS, Cloud Enabling, 1,47 M€ | terzo (aderente) |
| https://autorita-trasporti.it/wp-content/uploads/2021/07/det_00138_05-07-2021.pdf | 86de164f727a099baa625ecf7d930135d94f8a5519abd5eea499b2b833665998 | voci IaaS VDC, PaaS SQL Server, BaaS; proroghe 20/07/2021 e 20/07/2022 | terzo (aderente) |
| https://www.agcom.it/sites/default/files/migration/delibera/Delibera%20282-22-CONS.pdf | 476955c9684ac57f7a4a7fc81876ac1f5dcbf851534f148080eed8b4ab616517 | proroga CQ a 31/12/2022; erosione plafond; hosting sito web | terzo (aderente) |
| https://www.regione.calabria.it/wp-content/uploads/2023/01/decreto-n.-17588-del-30_12_2022.pdf | b527dddf71003875b65aa10528194a1b6da09324bdc60f68d1f347fcebd3416e | RTI; proroga lotti 1-4 al 31/12/2022 | terzo (aderente) |
| https://ted.europa.eu/it/notice/647656-2021/xml | 5a714d721b26ec28a3ccbed98c8fdb720ada8c5617e4e6ae9ec8f5cba3320430 | CIG master, stipula 20/05/2016, RTI | terzo (aderente) |
| https://www.regione.sicilia.it/istituzioni/servizi-informativi/decreti-e-direttive/liquidazione-allestimento-museale-espositivo-multimediale-servizi-cloud-computing-spc-cloud-lotto-1-ditta-telecom-spa | d18506605a62778c33a5713fbcbb1b08e49b6e6dc4072ef0024270d0a9d49f7a | uso del lotto 1 per un allestimento museale (esempio di oggetto improprio) — non letto per intero | terzo |
| BDNCP ANAC (cig, aggiudicatari) | per file in `archivio/manifest.jsonl` | padre Consip 500 M€, variante 150 M€, 1.372 attuativi | Consip/SA tramite ANAC |

Manca una fonte Consip diretta (pagina iniziativa o capitolato): la stazione appaltante compare solo tramite BDNCP.

## Proposta per iniziative_ict.yaml

```yaml
- cig: 55187486EA
  iniziativa: Consip SPC Cloud lotto 1, servizi di cloud computing (SIGEF 1403)
  categoria: cloud-multi
  stato: verificato
  asse_cloud: incluso-certo        # IaaS VDC, PaaS DB, BaaS; quota servizi professionali (Cloud Enabling) ignota
  asse_giurisdizione: IT           # erogazione RTI TIM/Poste in Italia; dipendenze USA (SQL Server); mandante Enterprise Services Italia (DXC, USA)
  massimale: 500000000
  variante_cig: 8734352748         # +150 M€ (2021)
  scadenza_cq: 2022-12-31
  dossier: report/convenzioni/55187486EA-spc-cloud-lotto-1.md
  documenti_aggiuntivi:
  - url: https://autorita-trasporti.it/wp-content/uploads/2021/07/det_00138_05-07-2021.pdf
    sha256: 86de164f727a099baa625ecf7d930135d94f8a5519abd5eea499b2b833665998
  - url: https://www.interno.gov.it/sites/default/files/2022-05/9184438600_determina_servizi_contratto_quadro_spc_cloud_lotto1_rti_telecom-signed.pdf
    sha256: c4d4f217e9442135f84fb4ce796260427cabff5e9615595d41db53868e569c22
  - url: https://www.agcom.it/sites/default/files/migration/delibera/Delibera%20282-22-CONS.pdf
    sha256: 476955c9684ac57f7a4a7fc81876ac1f5dcbf851534f148080eed8b4ab616517
```
