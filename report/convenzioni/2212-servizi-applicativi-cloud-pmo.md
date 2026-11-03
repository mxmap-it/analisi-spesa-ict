# Dossier: Consip «Servizi applicativi in ottica cloud e servizi di PMO per le PA», 1ª edizione (ID 2212)

Versione 1.0, 3/11/2026, ticket #55. Lotti analizzati: **8210577E78** (lotto 1, PAC dimensioni rilevanti), **82106098E2** (lotto 2, PAL dimensioni rilevanti), **8210615DD4** (lotto 3, PAC medio-piccole). La gara ha 9 lotti: 1-5 applicativi, 6-9 PMO.
Legenda: **V** = verificato su documento archiviato; **R** = riferito o inferito.

## 1. Sintesi

1. ID 2212 è la gara strategica del Piano triennale AgID del 2020: base d'asta 1,2 mld, 9 lotti (5 applicativi multifornitore e 4 PMO), accordo quadro di 18 mesi, contratti fino a 48 mesi (V).
2. **Qui la domanda centrale ha una risposta documentale.** Il capitolato prevede un «Servizio di Migrazione Applicativa al Cloud» (§5.3 del capitolato speciale). Consip però chiarisce che la strategia re-hosting «è invece oggetto della gara Id 2213 Public Cloud Lotto 1», e che le competenze cloud richieste riguardano solo IaaS, PaaS e SaaS «gestite dai Cloud Service Provider qualificati da AgID» (V). Si comprano persone, non cloud.
3. Il team medio è fatto di profili professionali, con percentuali fissate da Consip: Developer/Cloud Developer 25 %, Digital/Mobile Media Specialist 13 %, Business Analyst e Systems Analyst 10 % ciascuno… (V).
4. BDNCP: lotto 1 65 attuativi / 1.042 M; lotto 2 36 / 308 M; lotto 3 141 / 357 M. Non ci sono massimali anomali evidenti (V). Migrazione esplicita: 6 attuativi per 18,6 M (soglia minima).
5. Proposta: S5, consulenza IT applicativa, con sotto-quota consulenza-migrazione-cloud per attuativo. Cloud diretto escluso. Confidenza **alta**.

## 2. Identificazione

| Campo | Valore | Fonte | Stato |
|---|---|---|---|
| CIG lotto 1 | 8210577E78, «PAC per contratti di dimensioni rilevanti», importo 495 M, CPV 72211000-7 | TED 536035-2023 (aggiudicazione); BDNCP padre | V |
| CIG lotto 2 | 82106098E2, «PAL per contratti di dimensioni rilevanti», 176 M | TED 536035-2023; BDNCP | V |
| CIG lotto 3 | 8210615DD4, «PAC medio-piccole», 209 M | TED 536035-2023; BDNCP | V |
| Bando | GUUE 2020/S 038-090219; BDNCP 24/02/2020; comunicato del 26/02/2020 | TED 536035-2023 (rif. bando); BDNCP; comunicato AgID/Consip | V |
| Valore totale | 1.202 M (base d'asta «1,2 miliardi») | TED; BDNCP importo_complessivo_gara; comunicato | V |
| Aggiudicatari lotto 1 | 4 RTI: Accenture (con Avanade, ESRI, SMC, BIP), IBM (con Deda Next, EY, Pagile), Enterprise Services (con Eustema, Net Service, Claranet…), Almaviva (con Apkappa, Inmatica, Reply…) | TED 536035-2023 | V |
| Durata | AQ 18 mesi; contratti esecutivi fino a 48 mesi | comunicato Consip (repository AgID) | V (una fonte Consip) |

## 3. Cosa contiene

- **Servizi applicativi** (capitolato speciale lotti applicativi):
  - sviluppo;
  - evoluzione e manutenzione;
  - §5.3 **Migrazione applicativa al cloud** («Servizio MI»): come input l'ente porta la Roadmap di migrazione e le schede di assessment del **Cloud Enablement Kit** AgID;
  - supporto e co-working.

  Il team si paga a mix di profili (rettifica Tabella 5.7) (V).
- **Confine con l'infrastruttura** (risposta Consip n. 7): fanno parte di questa iniziativa le strategie «che comprendono interventi di natura applicativa, di migrazione dei dati e di integrazione e/o validazione funzionale». La strategia «Re-hosting, che non implica interventi applicativi, è invece oggetto della gara Id 2213 "Public Cloud" Lotto 1» (V).
- **Quale cloud** (risposta n. 93): le competenze devono riguardare «esclusivamente le soluzioni IaaS, PaaS e/SaaS gestite dai Cloud Service Provider qualificati da AgID» (V). L'infrastruttura cloud è **di terzi**, comprata con contratti separati (SPC Cloud, ID 2213, oggi PSN). Il dossier non dice quale CSP usi ciascun ente: va visto contratto per contratto.
- L'unica infrastruttura a carico del fornitore è il **portale della fornitura**, cioè lo strumento di governo del contratto (risposta sul §6.1 del capitolato generale). Non è un servizio per l'ente.

## 4. Analisi degli attuativi (BDNCP, 3/11/2026)

Metodo e prove come nel dossier 2483: `tools/analisi/attuativi_convenzioni.py`, CSV in `prove-servizi-applicativi/`.

| Lotto | N | M€ | Anni (N / M€) | ≥50 M | Fascia modale |
|---|---|---|---|---|---|
| 8210577E78 (L1) | 65 | 1.042,0 | 2021: 36 / 745,1; 2022: 23 / 295,9; 2023: 2 / 0,5; 2024: 4 / 0,4 | 2 per 142,7 M (Interno, P.S., 82,7 M; ACN 60 M) | 10–50 M: 31 attuativi per 765 M |
| 82106098E2 (L2) | 36 | 307,7 | 2023: 35 / 305,9; 2025: 1 / 1,8 | 0 | 1–10 M: 25 |
| 8210615DD4 (L3) | 141 | 357,1 | 2022: 88 / 254,6; 2023: 51 / 102,1; 2024-25: 2 / 0,5 | 0 (massimo 5 M: tetto dimensionale del lotto, V da oggetti «ordine diretto») | 1–10 M: 98 |

- **Importi anomali.** Nessuno supera un decimo del massimale del lotto. Il massimo del lotto 1, 82,7 M, è il 17 % di 495 M. Plausibile per un ministero, ma da verificare (R).
- **Cloud e migrazione nell'oggetto**, al netto delle formule «in ottica cloud»:
  - L1: 5 attuativi per 13,8 M. Tre sono liquidazioni «SPC Cloud lotto 1» dell'AO Moscati agganciate per errore a questo AQ: errore di `cig_accordo_quadro` (V da oggetto). Migrazione: 1, cioè Carrara, Misura 1.2, 0,36 M.
  - L2: Roma Capitale, «servizi di migrazione applicativa al cloud dei sistemi centrali», 5,01 M.
  - L3: 4 di migrazione per 13,2 M. Sono ENAC 5,0 M, Sogei 3,84 M, MISE «piano di migrazione in cloud» 3,28 M e Infratel 1,09 M. In più c'è Sogei «Cloudify NoiPA» 4,99 M.
- Altre classi:
  - L1: sviluppo 16 attuativi / 291 M, PMO 14 / 167 M;
  - L3: sviluppo 39 / 97 M, PMO 40 / 85 M, manutenzione 26 / 58 M.
- Fornitori principali:
  - L1: Accenture, Avanade, ESRI, SMC e BIP (RTI Accenture, 460–480 M ciascuno, in quota RTI);
  - L3: Reply Public Sector 103 M, Maggioli, Accenture TS e Almaviva Digitaltec circa 88 M ciascuno.

## 5. Classificazione proposta

| Lotto | Categoria | Asse cloud | S5 | Quota migrazione (soglia minima) | Confidenza |
|---|---|---|---|---|---|
| 8210577E78 | servizi-applicativi | escluso (diretto) | consulenza IT applicativa | 0,4 M / 1.042 M (0,03 %) | alta |
| 82106098E2 | servizi-applicativi | escluso | idem | 5,0 M / 308 M (1,6 %) | alta |
| 8210615DD4 | servizi-applicativi | escluso | idem | 13,2 M / 357 M (3,7 %) | alta |

Gli attuativi SPC Cloud dell'AO Moscati agganciati al lotto 1 vanno riassegnati al loro padre SPC Cloud: lì sono cloud diretto.

## 6. Assunzioni e limiti

- Il capitolato tecnico non è archiviato per intero. Archiviati: rettifiche e risposte ai chiarimenti di Consip, che ne citano i paragrafi. Le citazioni sono V, il resto del capitolato no.
- La «seconda fonte indipendente» per il contenuto sono gli oggetti degli attuativi BDNCP inseriti dagli enti: ENAC e Sogei, per esempio, nominano la «migrazione applicativa al cloud». Indipendente sì, ma debole.
- Lotti 4-9 non analizzati: fuori dal mandato.
- Gli importi sono valori dichiarati, non pagati.

## 7. Fonti

| URL | sha256 | Cosa conferma | Tipo |
|---|---|---|---|
| https://ted.europa.eu/it/notice/536035-2023/xml | abcd74941a45b085eeefeaa7f0814889ea20fc02292c4410ab5d70f4908ee8c1 | 9 lotti, CIG L1/L2/L3, aggiudicatari, valori | stazione appaltante |
| https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID%202212%20-%20Servizi%20applicativi%20in%20ottica%20cloud%20-%20Risposte%20ai%20chiarimenti.pdf | 0ca7e99890c96b6c50e43d3cd2379787fa5a5dc7ac79c5012f790d56368d0b2b | Servizio MI §5.3; re-hosting in ID 2213; CSP qualificati AgID; portale | stazione appaltante |
| https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID%202212%20-%20Gara%20Servizi%20Applicativi%20in%20ottica%20cloud%20-%20Rettifiche%20alla%20documentazione.pdf | ed307689e87a230f1f80f55af8530511b8548c2c4c1a3eb722494ae73962faa2 | mix di profili professionali (Tabella 5.7) | stazione appaltante |
| https://www.agid.gov.it/sites/default/files/repository_files/cs_gara_strategica_servizi_applicativi_in_ottica_cloud.pdf | 3d3f62d291957fb923236682f5d9094f16a86006ea726780f556d928e0a6e25a | 1,2 mld, 9 lotti, 18/48 mesi, contenuto dei lotti | stazione appaltante (comunicato Consip ospitato da AgID) |
| BDNCP → `prove-servizi-applicativi/attuativi.csv` | 5d9bcf855e9c744fdef125d539a27bd51f909a88338c7aaf27657c1971349d2f | attuativi e oggetti | terzo (ANAC) |

## Proposta per iniziative_ict.yaml

```yaml
# per 8210577E78, 82106098E2, 8210615DD4 (aggiunte alle voci esistenti, stato invariato: verificato)
  s5: consulenza-it-applicativa
  s5_quota_migrazione: per-attuativo
  cloud_diretto: escluso
  documenti (+):
  - url: https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID%202212%20-%20Servizi%20applicativi%20in%20ottica%20cloud%20-%20Risposte%20ai%20chiarimenti.pdf
    sha256: 0ca7e99890c96b6c50e43d3cd2379787fa5a5dc7ac79c5012f790d56368d0b2b
    cosa_conferma: 'Consip: migrazione applicativa al cloud nel perimetro (§5.3), re-hosting in ID 2213 Public Cloud, IaaS/PaaS/SaaS dei CSP qualificati AgID'
  nota (L1): '3 attuativi SPC Cloud (AO Moscati, B17E726FFA, B17EAF43C3, B17EBB0EE4) con cig_accordo_quadro errato'
```
