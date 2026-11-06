---
title: "Obiettivo 6: prodotti, rivenditori, PNRR, PSN"
subtitle: "Lente prodotto misurata sul campione, chi rivende i prodotti esteri, quota big tech nei contratti PNRR, catalogo ACN"
date: 2026-11-06
lastmod: 2026-11-06
datiAl: 2026-10-28
description: "Precisione e richiamo del dizionario dei marchi cloud sul campione di 611 CIG; quota della spesa in prodotti extra-UE intermediata da rivenditori; quota dei prodotti delle big tech USA nei contratti collegati alle Misure PNRR 1.1 e 1.2; stato del catalogo ACN dei servizi qualificati."
sitemap:
  disable: true
build:
  list: never
---

**Versione 0.1 del 2026-11-06 · BOZZA non annunciata: la pubblicazione la decide Fabio Pietrosanti** · ticket [#40](https://github.com/mxmap-it/analisi-spesa-ict/issues/40), [#41](https://github.com/mxmap-it/analisi-spesa-ict/issues/41), [#43](https://github.com/mxmap-it/analisi-spesa-ict/issues/43), [#45](https://github.com/mxmap-it/analisi-spesa-ict/issues/45), parte di [#24](https://github.com/mxmap-it/analisi-spesa-ict/issues/24)

Legenda: **[V]** misurato da noi, con il comando per rifarlo; **[R]** riferito da terzi, non verificato. La giurisdizione è quella del **prodotto** ([metodo](/progetto/metodo-cloud-provider/)).

## 1. Lente prodotto (#40)

Dizionario: `config/marchi_cloud.yaml` (regex ed esclusioni, vie 3), con la fonte della giurisdizione di ogni provider in `config/marchi_cloud_fonti.yaml` (capogruppo e sede; tutte [R] tranne PSN, SPC Cloud e in-house). Misura sul campione v3 di 611 CIG (riferimento: via 6 con atti e revisione, `dati/classificazioni/campione-v3.jsonl`), guardando **solo il testo della gara** [V]:

| Insieme | Precisione | Richiamo |
|---|---|---|
| Prodotti big tech USA (Microsoft, AWS, Google, Oracle, IBM, Salesforce, ServiceNow, Adobe, VMware, Cisco, Zoom, Cloudera) | 168/175 = **96 %** (92-98) | 168/186 = **90 %** (85-94) |
| Tutti i provider del dizionario, provider esatto | 286/336 = 85 % (81-89) | 286/455 = 63 % (58-67) |

Intervalli di Wilson al 95 %. Per provider: Microsoft 97 % / 94 %, VMware 95 % / 100 %, Oracle 100 % / 83 %, SAP 100 % / 74 %, PSN 84 % / 97 %. Il richiamo complessivo basso viene da TIM (0/62), Fastweb (0/15) e in-house (27/84): il riferimento li attribuisce dal fornitore o dagli atti, non dal testo; per la lente prodotto non è un errore ma il limite atteso. **Menzioni in negativo** («migrazione da», «in sostituzione», «dismissione»): 0 falsi positivi su 50.

Limiti: il campione è stratificato, non casuale; il riferimento è stato prodotto anche guardando le vie 3 (possibile circolarità, che gonfia la precisione); per una misura indipendente serve un campione nuovo etichettato a cieco.

Rifare: `python tools/verifiche/lente_prodotto.py` → `esiti/2026-11-06/lente-prodotto/` (errori uno per uno in `errori.csv`).

## 2. Rivenditori dei prodotti esteri (#41)

Dalla mappa v3 (`report/metodo/rivenditori-v3.*`, contratti attuativi 2022-2026, padri di AQ e importi da verificare esclusi) [V]:

| Giurisdizione del prodotto | Totale | Rivenditore | Diretto | Ignoto | Rivenditore sul noto |
|---|---|---|---|---|---|
| EXTRA-UE | 2,95 mld | 1,82 mld | 0,45 mld | 0,67 mld | **80 %** |
| UE | 0,35 mld | 0,20 mld | 0,07 mld | 0,08 mld | 75 % |
| IT | 2,15 mld | 0,09 mld | 1,53 mld | 0,54 mld | 5 % |

- **1.180 rivenditori** hanno venduto prodotti extra-UE; i primi 5 fanno il **66 %**. TIM da sola 1,07 mld (Microsoft 0,87 mld), poi Eurolink 94 M (Oracle), Fastweb 78 M (AWS, IBM), Postel 61 M (Microsoft), Var Group 48 M, SoftwareOne 48 M.
- Il 7° «rivenditore» per importo è il segnaposto ANAC **«IMPRESA INESISTENTE»** (46,5 M€): nuova **R56**.
- La nazionalità dei rivenditori non è misurata (manca il CF nel file): i nomi in testa sono società italiane [R], da verificare sui CF ANAC. Il totale per rivenditore (2,04 mld) supera quello per canale (1,82 mld) perché il file per rivenditore conta anche i contratti con più provider: da riconciliare.
- Esclusi perché l'importo è da verificare: Microsoft 2,50 mld, PSN 2,16 mld, Oracle 0,52 mld.

Rifare: `python tools/verifiche/rivenditori_esteri.py` → `esiti/2026-11-06/rivenditori/`.

## 3. PNRR cloud (#43)

Catena PA Digitale 2026 → CUP → dataset ANAC cup → CIG → attribuzione v3 (`report/metodo/pnrr-contratti-v3.csv`, 26/10/2026) [V]:

| Misura | Contratti collegati | Big tech USA | Quota sul totale | Quota sull'attribuito |
|---|---|---|---|---|
| 1.2 (migrazione al cloud) | 818,9 M€ | **13,6 M€** (Microsoft 10,0; Oracle 2,3; AWS 0,5; Google 0,4) | **1,7 %** | 3,2 % |
| 1.1 (infrastrutture, PSN) | 270,3 M€ | 0 | 0 % | 0 % |

- In 1.2 il resto attribuito è IT (408,6 M€, soprattutto SaaS di fornitori italiani e in-house); 396,7 M€ senza provider. Della quota big tech, 6,6 M€ passano da rivenditori e 6,9 M€ hanno canale ignoto; nessuno diretto.
- Sono **importi dei contratti collegati al CUP**, non la quota del finanziamento: un CUP può avere CIG fuori dal progetto e il 47,8 % dei CUP 1.2 non porta a nessun CIG.
- In 1.1 l'assenza di big tech è nel **contratto** (adesioni PSN); quale tecnologia eroga il PSN (Secure Public Cloud su hyperscaler) non si vede dai CIG: vedi § 4 e R50.
- 1.1 con i decreti: 16 decreti spogliati, 537,6 M€ ([imbuto 0.5](/rendiconti/imbuto-dove-siamo/), `tools/verifiche/pnrr11_decreti.py`); la catena v3 qui sopra parte invece dalle candidature open data (206). Da riallineare sui CUP dei decreti (`esiti/2026-11-06/pnrr11/cup-cig.csv`).

Rifare: `python tools/verifiche/pnrr_bigtech.py` → `esiti/2026-11-06/pnrr/pnrr-bigtech.json`.

## 4. PSN e catalogo ACN (#45)

- **Catalogo ACN non specchiabile:** `catalogocloud.acn.gov.it/opendata` e `/robots.txt` rispondono **403** (Akamai) anche con User-Agent da browser e URL del progetto, dal server, il 6/11/2026 [V]. Non è una sezione di Amministrazione trasparente: vale la regola generale, non si aggira. Nuova **R55**: pubblicazione in open data scaricabile.
- **PSN dai CIG** (già misurato, [imbuto 0.5](/rendiconti/imbuto-dove-siamo/)): impegni ANAC 4,38 mld al netto dei tetti certi, contro un portafoglio di 3,8 mld e ricavi 2023-25 di 0,79 mld [R, bilanci PSN]. Contratti PSN con un prodotto big tech nel testo: 12 per 9,2 M€ [V, mappa v3].
- Senza catalogo né contratti di utenza per ente (R50) la quota del PSN erogata su tecnologia di hyperscaler non è misurabile.

## 5. Prossimi passi

1. #40: campione nuovo a cieco (casuale nello strato S3-S4) per una precisione senza circolarità; regole per TIM/Fastweb come prodotto (Microsoft via TIM).
2. #41: CF degli aggiudicatari dal dataset ANAC per la giurisdizione del rivenditore; riconciliare 2,04 contro 1,82 mld.
3. #43: rifare la catena 1.1 dai 312 CUP dei decreti; FLAG_PNRR_PNC e openpnrr come controvalidazione.
4. #45: catalogo ACN a mano con Fabio (consultazione da browser, non automatica) o richiesta ad ACN (R55).

## Registro delle revisioni

| Versione | Data | Modifica |
|---|---|---|
| 0.1 | 2026-11-06 | Prima bozza: tre verifiche nuove (`lente_prodotto.py`, `rivenditori_esteri.py`, `pnrr_bigtech.py`), R55-R56 |
