# SPC2 Connettività — contratti quadro OPA/OPO, ID 1367 (CIG 5133642F61) — dossier analitico

Versione 0.1 — 2026-11-03 — #55. Bozza per revisione avversariale.
Legenda: **V** verificato su documento archiviato; **V2** due fonti indipendenti di cui una della stazione appaltante; **R** riferito / da verificare.
Numeri degli attuativi: `tools/verifiche/attuativi_s5.py` (sul server, esito in `lavoro/convenzioni/attuativi_s5.json`).

## 1. Sintesi

- Il CIG 5133642F61 è ora confermato da **fonte della stazione appaltante**: il Documento descrittivo Consip del 21/05/2013 lo riporta testualmente (V), oltre a BDNCP e agli avvisi TED degli aderenti → **V2**.
- Il bando prevedeva **quattro famiglie di servizi**: trasporto IP, **sicurezza perimetrale «as a service»** (VPN, firewall, IDS/IPS, antivirus, content filtering), **comunicazione** (VoIP/videoconversazione) e **calcolo e memorizzazione IaaS in community cloud** (V, Documento descrittivo). Se l'IaaS è rimasto nel contratto stipulato, SPC2 contiene cloud: da verificare sul capitolato tecnico del contratto quadro (non archiviato).
- BDNCP: 2.958 attuativi (2013-2026), 6,86 G€ lordi; 2 anomali per 4,1 G€ (CTM 2,4 G€; ANM 1,7 G€); al netto **2,74 G€** (1,09 del massimale 2,5 G€). Esteso per legge fino al 31/12/2025 (Consip), ma 482 attuativi nel 2026.
- Negli oggetti: 87 attuativi VoIP/telefonia (74,2 M€), 42 sicurezza/SOC (56,4 M€), 40 cloud/DC (64,4 M€, in parte adesioni a **SPC Cloud** agganciate per errore al CIG master SPC2).
- Proposta: resta **connettività (S5)** per la parte trasporto; VoIP e sicurezza erogati dall'operatore sono servizi «as a service» di rete, da tenere in S5-connettività per coerenza con le TLC; **asse cloud incerto** finché non si accerta se l'IaaS è stato contrattualizzato e ordinato.

## 2. Identificazione

| Campo | Valore | Fonte | Livello |
|---|---|---|---|
| CIG | 5133642F61 | Documento descrittivo Consip 2013 («Il codice identificativo della gara (CIG) è il seguente: 5133642F61»); BDNCP; TED 374672-2023 (CIG MASTER) | V2 |
| Gara | procedura ristretta, contratti quadro multifornitore (fino a 4 parti decrescenti), ID Sigef 1367 | pagina Consip gara-spc-connettivita; Documento descrittivo | V2 |
| Date | indizione 21/05/2013; aggiudicazione 28/04/2015 | pagina Consip | V (fonte unica SA) |
| Durata | 84 mesi dalla sottoscrizione; prorogato per legge (31/12/2023, 31/12/2024 +50 %, 31/12/2025) | pagina Consip; notizia Consip milleproroghe; TED 374672-2023, 397204-2023 | V2 |
| Massimale | 2.500.000.000 € | BDNCP | V fonte unica → R |
| Aggiudicatari | BDNCP: Fastweb, TIM, Vodafone, Ericsson Telecomunicazioni; attuativi anche con BT Italia (499) e Tiscali (51) | BDNCP | R (graduatoria non archiviata; Ericsson anomalo) |

## 3. Cosa contiene

Documento descrittivo (oggetto, §1): **V**
1. trasporto IP (wired, wireless/satellitare) negli ambiti Intranet, Infranet (QXN), Internet;
2. sicurezza perimetrale «as a service»: VPN, firewalling, IDS/IPS, antivirus, antispam, content filtering, application control;
3. servizi di comunicazione: video/conversazioni sullo stesso accesso IP (VoIP);
4. **calcolo e memorizzazione IaaS**, risorse fisiche dedicate alle PA aderenti a SPC («Community Cloud»), macchine virtuali e spazio disco «reso disponibile remotamente dal fornitore».

Schema di contratto esecutivo OPA (2013): rinvia al Progetto dei fabbisogni e al Contratto quadro; non elenca i servizi. **V**
Non letto: capitolato tecnico del contratto quadro e listini (decidono se l'IaaS è stato mantenuto). **R**

## 4. Analisi degli attuativi (BDNCP)

| Misura | Valore |
|---|---|
| attuativi | 2.958 |
| anomali | CTM S.p.A. 2,4 G€ (2024); ANM 1,73 G€ (2017) |
| euro puliti | 2.736.583.968; picchi 2017 (756,7 M€, adesioni iniziali) e 2024 (664,0 M€, contiene ancora valori dubbi: Comune di Tradate 480 M€ per una proroga annuale) |
| per anno (puliti, M€) | 2016 65,8; 2017 756,7; 2018 127,8; 2019 132,2; 2020 130,3; 2021 138,2; 2022 132,0; 2023 225,8; 2024 664,0; 2025 195,1; 2026 167,0 |
| mediana / p90 | 123.494 € / 1,50 M€ |
| possibili doppioni | 183 righe, 24,7 M€ (impegni annuali ripetuti, es. Roma Capitale) |
| sotto 500 € | 15 |
| VoIP/telefonia | 87 / 74,2 M€ (Roma Capitale «connettività, servizi VoIP e professionali») |
| sicurezza/SOC | 42 / 56,4 M€ |
| cloud/DC | 40 / 64,4 M€ — tra questi adesioni a «SPC Cloud lotto 1/lotto 2» con CIG master SPC2 (ARPA 86.434 €, ASL Rieti 329.790 €, Acquirente Unico 329.066 €) e progetti DC regionali (LazioCrea, Sardegna «infrastrutturazione cloud edge» 26,4 M€) |
| aggiudicatari | Fastweb (1.324), Vodafone (681+136), TIM (513), BT Italia (499), Ericsson (477) |

Valori 2024 sospetti: Tradate 480 M€ è sotto la soglia anomali (25 % = 625 M€) ma palesemente errato; la soglia è troppo larga per un master da 2,5 G€.

## 5. Classificazione proposta

- Categoria connettività, **S5 – connettività**; confidenza alta per il trasporto.
- VoIP e sicurezza perimetrale «as a service» erogati dall'operatore: in senso stretto servizi esterni di rete; li lasciamo in S5-connettività (proposta) perché inseparabili dall'accesso e non sono «cloud ICT» nel senso dell'obiettivo; da confermare con Fabio.
- Asse cloud: **incerto** — IaaS community cloud previsto nel bando (V), contrattualizzazione e ordini ignoti; gli attuativi «cloud» trovati sono in gran parte SPC Cloud mal agganciati (da riassegnare a 55187486EA/lotto 2).
- Giurisdizione: operatori con sede in Italia; Vodafone (gruppo UK fino al 2024, poi Swisscom/Fastweb, CH), BT Italia (UK), Ericsson (SE): lente fornitore UE/extra-UE mista.

## 6. Assunzioni e limiti

- Il Documento descrittivo descrive la gara bandita, non il contratto firmato.
- Massimale e aggiudicatari solo da BDNCP; Ericsson tra gli aggiudicatari è da spiegare (graduatoria non letta).
- BDNCP mescola ordini pluriennali, impegni annuali e proroghe: la somma non è spesa annua.
- 482 attuativi 2026 oltre la scadenza del 31/12/2025 comunicata da Consip: ulteriore proroga non documentata qui.

## 7. Fonti

| URL | sha256 | Cosa conferma | Tipo |
|---|---|---|---|
| https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/7871DocumentazioneNO.zip | 47b7f2ece54dfc48d8487ec311b4b900ba723f21a9b97a7865330e8e2ec21f09 | Documento descrittivo (file interno d60c1c910ab04c0e7d8311188f0b5638ef458c631f6cef846a774b15ae160111): CIG, 4 famiglie di servizi incluso IaaS | stazione appaltante |
| https://www.consip.it/bandi/gara-spc-connettivita | b6db1f5eb48f4db7657c8c6b8920f34f8edfe36ab1d7900523027d4cff4a1a15 | ID 1367, 84 mesi, cronologia, proroghe | stazione appaltante |
| https://www.consip.it/notizie-e-comunicati/milleproroghe-esteso-al-31-dicembre-2025-il-contratto-quadro-spc-2-connettivita | 97444124cf77bdf62158f7388f743625ea5540b8802e3e7568e1600a5a193895 | estensione al 31/12/2025 | stazione appaltante |
| https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID%201367%20Schema%20di%20contratto.zip | 2ecc88579f5cd576aac1bdfe6fcb1953a5c5a94e28608f26edc5a463692ca2a9 | schema CE OPA (5108ff1a4dcc78ee43279782d8124d2fbcfd6e261639cd28dff339f8b2f1ff66) | stazione appaltante |
| https://ted.europa.eu/it/notice/374672-2023/xml | 11016c0f2fd9c668d700d736dff0dc2d1af55faa873e6376f5b1af30110fb390 | CIG MASTER, «connettività e sicurezza», Fastweb | terzo (aderente) |
| https://ted.europa.eu/it/notice/397204-2023/xml | e8271625d7fbdcddbad048eb3d65fb33dfab1f0c5bced3349ccc028444f57c10 | estensione al 31/12/2023 del CQ ID 1367 | terzo (aderente) |
| https://ted.europa.eu/it/notice/204682-2017/xml | f463f1e6e8f53ee13adea379fad1cd7db40f1b063fcb7242dcac8296527ad10f | IPZS, migrazione verso SPC2 | terzo (aderente) |
| BDNCP ANAC nel mirror | per file in `archivio/manifest.jsonl` | massimale, aggiudicatari, attuativi | ANAC (dato della SA) |

## Proposta per iniziative_ict.yaml

```yaml
- cig: 5133642F61
  iniziativa: Consip SPC2 Connettività, contratti quadro OPA/OPO, ID 1367
  categoria: connettivita
  stato: verificato               # ora anche fonte Consip (Documento descrittivo 2013)
  sottoclasse_s5: connettivita
  asse_cloud: incerto             # bando con IaaS community cloud; contratto/ordini da verificare; attuativi SPC Cloud mal agganciati
  componenti: [trasporto, sicurezza-as-a-service, voip, iaas-community-cloud-da-verificare]
  massimale: 2500000000
  scadenza_cq: 2025-12-31         # attuativi 2026 presenti: verificare ulteriore proroga
  dossier: report/convenzioni/5133642F61-spc2-connettivita.md
  documenti_aggiuntivi:
  - url: https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/7871DocumentazioneNO.zip
    sha256: 47b7f2ece54dfc48d8487ec311b4b900ba723f21a9b97a7865330e8e2ec21f09
    cosa_conferma: Documento descrittivo Consip con CIG 5133642F61 e quattro famiglie di servizi
  - url: https://www.consip.it/bandi/gara-spc-connettivita
    sha256: b6db1f5eb48f4db7657c8c6b8920f34f8edfe36ab1d7900523027d4cff4a1a15
    cosa_conferma: pagina iniziativa ID 1367
```
