# Trenitalia «Affidamento di servizi ICT» (CIG 7991036B82) — dossier analitico

Versione 0.1 — 2026-11-03 — #55. Bozza per revisione avversariale.
Legenda: **V** verificato su documento archiviato; **V2** due fonti indipendenti di cui una della stazione appaltante; **R** riferito / da verificare.

## 1. Sintesi

- **Decifrato (da BDNCP)**: non è la gara Ferservizi 2019 (TED 358459-2019, CIG 7963682E45), ma un **accordo quadro intragruppo** con cui Trenitalia affida i propri servizi ICT a **FSTechnology S.p.A.** (società ICT del gruppo FS), con «affidamento diretto a società raggruppate/consorziate o controllate», 850 M€, pubblicato il 26/07/2019, settori speciali.
- Gli attuativi sono i «contratti applicativi FST» annuali: 540 CIG, 426 M€ (2019: 49,8; 2020: 66,0; 2021: 308,3; 2024: 2,1 M€), tutti aggiudicati a FSTechnology.
- Contenuto: servizi ICT generali (sviluppo applicativo, gestione sistemi, apparati di bordo, migrazioni SAP/HANA «al cloud»): **misto, prevalentemente non cloud** dagli oggetti; il cloud eventuale è acquistato a valle da FSTechnology (anche tramite la gara Ferservizi 2019, che prevedeva IaaS e «orchestrazione di cloud di terze parti IaaS/PaaS/SaaS»).
- Asse B: **incerto** — FSTechnology è un fornitore interno (IT); i prodotti sottostanti non sono identificabili dalle fonti.
- Nota di perimetro: Trenitalia è società pubblica in settori speciali; un affidamento intragruppo è spesa ICT «interna» al gruppo FS più che spesa verso il mercato.

## 2. Identificazione

| Campo | Valore | Fonte | Livello |
|---|---|---|---|
| CIG | 7991036B82 | BDNCP | V (fonte unica) |
| SA | Trenitalia S.p.A. | BDNCP | V |
| Oggetto | «Affidamento di servizi ICT» | BDNCP | V |
| Tipo | accordo quadro; «affidamento diretto a società raggruppate/consorziate o controllate nelle concessioni e nei partenariati»; settori speciali; procedura in modalità tradizionale | BDNCP | V |
| Importo | 850.000.000 € | BDNCP | V |
| Pubblicazione | 26/07/2019 | BDNCP | V |
| Aggiudicatario | FSTechnology S.p.A. (CF 15032391003) | BDNCP aggiudicatari | V |
| CPV | servizi software di gestione di rete | BDNCP | V |
| Durata | non valorizzata in BDNCP | — | ignota |

**Nessuna fonte della stazione appaltante fuori da BDNCP**: niente su TED (affidamento intragruppo, non soggetto a pubblicazione) né sul web indicizzato (nota già in config). Stato: **da-verificare** secondo la regola dei 2026-11-03; ma la decifrazione dell'oggetto è solida (5 campi BDNCP coerenti + 540 attuativi con lo stesso aggiudicatario).

**Candidato precedente escluso**: TED 358459-2019 è una procedura negoziata Ferservizi «in nome e per conto» di FSTechnology, Trenitalia e altre società FS, CIG 7963682E45, AQ 48 mesi, 318,86 M€ (558 M€ valore stimato complessivo), per «gestione sistemistica e infrastrutture hardware, hosting, housing, IaaS, orchestrazione di cloud di terze parti IaaS/PaaS/SaaS, DR/BC, service desk, rete TLC». In BDNCP il CIG 7963682E45 (Ferservizi, 558 M€) **non ha attuativi collegati**. È un'altra procedura: probabilmente il fornitore a valle di FSTechnology per infrastruttura (R, non provato).

## 3. Cosa contiene

Solo dagli oggetti degli attuativi (nessun documento contrattuale):
- tre contratti applicativi annuali grandi: 2019 «Contratto applicativo anno 2019 su AQ servizi ICT» 45,5 M€; «2° contratto applicativo FST – 2020» 125,6 M€; «3° contratto applicativo FST – 2021» 140,0 M€;
- ~537 ordini puntuali «FST …»: es. «SIREV2 – upgrade HANA 2 e migrazione al cloud» 4,26 M€; «offerta modale trasporto regionale-bus» 4,24 M€; «fornitura Network Box NB3N per flotta ETR500 per TVCC» 3,6 M€ (hardware di bordo).

## 4. Analisi degli attuativi

| Anno | n | € |
|---|---:|---:|
| 2019 | 44 | 49.840.800 |
| 2020 | 290 | 66.047.382 |
| 2021 | 195 | 308.252.511 |
| 2024 | 11 | 2.087.542 |
| **Totale** | **540** | **426.228.234** |

Anomali (≥ 20 M€): i tre contratti applicativi annuali (311 M€ = 73 % del totale). Sono «contenitori»: gli ordini puntuali FST potrebbero esserne parte (rischio di doppio conteggio).
Classi: nessuna parola chiave 400 CIG / 79 M€; sviluppo/manutenzione 111 / 335 M€; servizi professionali 23 / 4,3 M€; migrazione 9 / 6,8 M€; «cloud» 3 / 7,8 M€; housing 1 / 1,2 M€. Nessun hyperscaler nominato.
Vuoto 2022-2023: nessun attuativo registrato; da capire (nuovo AQ? dati mancanti?).

## 5. Classificazione proposta

- **Asse A**: **misto, prevalentemente non cloud** dagli oggetti (sviluppo, gestione, hardware di bordo); cloud ≥ 7,8 M€ dichiarato in 3 CIG. Quota non stimabile. Confidenza bassa.
- **Asse B**: **incerto**. Lente fornitore: FSTechnology, società italiana a controllo pubblico (gruppo FS). Lente prodotto: ignota (SAP HANA = SAP, DE/UE, per il caso SIREV2; il «cloud» di destinazione non è nominato).
- Perimetro: proporre a Fabio se gli affidamenti intragruppo FS vadano contati come «datacenter/infrastrutture interne» anziché come «servizi cloud esterni» (etichetta `decisione-fabio`).

## 6. Assunzioni e limiti

1. Unica fonte BDNCP: nessun atto di Trenitalia/FSTechnology archiviato.
2. Il legame Ferservizi 2019 → FSTechnology come fornitore di infrastruttura è un'ipotesi.
3. Rischio di doppio conteggio fra contratti applicativi annuali e ordini FST.

## 7. Fonti

| URL | sha256 | Cosa conferma | Tipo |
|---|---|---|---|
| BDNCP ANAC, cig-2019 e successivi + aggiudicatari (mirror `archivio/mirror/dati.anticorruzione.it/`) | per file in `archivio/manifest.jsonl` | padre 850 M€, affidamento diretto intragruppo, FSTechnology, 540 attuativi | SA tramite ANAC |
| https://ted.europa.eu/it/notice/358459-2019/xml | 2931682e5db4621d3e294a4e9d898a5f36bf13f00ea5cce96b1ce9668afa6f59 | candidato escluso: gara Ferservizi CIG 7963682E45, oggetto IaaS/hosting/housing | stazione appaltante (Ferservizi) |

## Proposta per iniziative_ict.yaml

```yaml
- cig: 7991036B82
  iniziativa: Trenitalia, AQ intragruppo di servizi ICT affidato a FSTechnology S.p.A.
  categoria: affidamento-intragruppo   # nuova categoria proposta
  stato: da-verificare                  # decifrato su BDNCP (fonte unica); manca un atto Trenitalia/FS
  aggiudicatario: FSTechnology S.p.A.
  importo: 850000000
  asse_cloud: misto-incerto
  asse_giurisdizione: incerto           # fornitore interno IT; prodotti ignoti
  nota: 'NON corrisponde a TED 358459-2019 (Ferservizi, CIG 7963682E45, senza attuativi in BDNCP). Attuativi = contratti applicativi FST 2019-2021.'
  dossier: report/convenzioni/7991036B82-trenitalia-servizi-ict.md
```
