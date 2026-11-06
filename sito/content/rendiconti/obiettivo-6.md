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

**Versione 0.3 del 2026-11-06 · BOZZA non annunciata: la pubblicazione la decide Fabio Pietrosanti** · ticket [#40](https://github.com/mxmap-it/analisi-spesa-ict/issues/40), [#41](https://github.com/mxmap-it/analisi-spesa-ict/issues/41), [#43](https://github.com/mxmap-it/analisi-spesa-ict/issues/43), [#45](https://github.com/mxmap-it/analisi-spesa-ict/issues/45), parte di [#24](https://github.com/mxmap-it/analisi-spesa-ict/issues/24)

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

### 1.1 Campione nuovo a cieco (v0.2)

Per togliere la circolarità: 240 CIG estratti a caso, 40 per ciascuno dei 6 strati dell'imbuto (S0, S2, S3, S4, S5, S6) dal 2024, esclusi i 611 del v3. Il seme è 20261106 (`report/metodo/lente-cieco/disegno.json`). Le etichette sono date leggendo il solo oggetto, senza vedere l'uscita della lente (`etichette.csv`; una riga corretta dopo per un'omissione di trascrizione, annotata). Il riferimento dice **quale prodotto nomina il testo**, non quale prodotto è stato comprato: gli atti non sono stati aperti [V].

| Insieme | Precisione (campione) | Richiamo (campione) | Pesato sull'universo (P / R) |
|---|---|---|---|
| Big tech USA | 54/54 = **100 %** (93-100) | 54/67 = **81 %** (70-88) | 100 % / 94 % |
| Tutti i provider | 64/65 = 98 % (92-100) | 64/80 = 80 % (70-87) | 99 % / 59 % |

- **Mancati** (13 big tech, tutti in S3): sigle delle convenzioni Consip Microsoft (MS EA8, EA9, «Consip Microsoft Agreement»), «Win 10», «licenze SQL - Teams», adesioni all'AQ IaaS/PaaS 2746 con il marchio ma senza lotto. Nell'imbuto questi CIG sono già presi da altre vie (lotto, convenzione), ma la lente da sola li perde.
- **Regole applicate (v0.3).** La via 6 non legge `config/marchi_cloud.yaml` (verificato in `tools/llm/`), quindi le regole sono nel dizionario, con commento e riga nel [metodo](/progetto/metodo-cloud-provider/):
  - aggiunte: sigle MS EA8/EA9, `consip microsoft`, licenze SQL, licenze ed ESU di Windows 10/11, IaaS/PaaS Google e Microsoft;
  - scartata «win 10/11» da sola: sull'universo dal 2024 prendeva 242 CIG di PC con Windows preinstallato;
  - effetto: circa 40 CIG in più sull'universo dal 2024, controllati su un estratto;
  - campione v3 invariato (96 % / 90 %);
  - sul campione a cieco il richiamo big tech sale a 66/67 (98 %), ma è una misura sullo stesso campione usato per scrivere le regole: **non vale come misura**, e il campione diventa di sviluppo. La misura indipendente resta 81 %.
- **Sottocampione sugli atti (v0.3):** 9 CIG positivi con link PVL più specifico (pagine di dettaglio dei portali), scaricati con `tools/llm/atti.py`:
  - 1 atto pertinente (B96E3295BB, licenze Microsoft VDA, R1 S.p.A.): conferma l'etichetta;
  - 2 pagine generiche dei portali, senza il CIG;
  - 6 non trovati o illeggibili.
  Resa 1/9, come nei giri precedenti (R53, R54): fermato. Il confronto «prodotto nominato contro prodotto comprato» resta senza misura.
- Il richiamo pesato di tutti i provider (59 %) è basso per gli strati S2: Aruba firma digitale, in-house Lepida, Google nominato come piattaforma di un SaaS italiano. Gli strati S0 e S5 (315 mila CIG) hanno 0 menzioni su 80, quindi la stima pesata è molto incerta.

Rifare: `python tools/verifiche/lente_cieco.py` → `esiti/2026-11-06/lente-prodotto/lente-cieco.json`.

## 2. Rivenditori dei prodotti esteri (#41)

Dalla mappa v3 (`report/metodo/rivenditori-v3.*`, contratti attuativi 2022-2026, padri di AQ e importi da verificare esclusi) [V]:

| Giurisdizione del prodotto | Totale | Rivenditore | Diretto | Ignoto | Rivenditore sul noto |
|---|---|---|---|---|---|
| EXTRA-UE | 2,95 mld | 1,82 mld | 0,45 mld | 0,67 mld | **80 %** |
| UE | 0,35 mld | 0,20 mld | 0,07 mld | 0,08 mld | 75 % |
| IT | 2,15 mld | 0,09 mld | 1,53 mld | 0,54 mld | 5 % |

- **1.180 rivenditori** hanno venduto prodotti extra-UE; i primi 5 fanno il **66 %**. TIM da sola 1,07 mld (Microsoft 0,87 mld), poi Eurolink 94 M (Oracle), Fastweb 78 M (AWS, IBM), Postel 61 M (Microsoft), Var Group 48 M, SoftwareOne 48 M.
- Il 7° «rivenditore» per importo è il segnaposto ANAC **«IMPRESA INESISTENTE»** (46,5 M€): nuova **R56**.
- **Nazionalità (v0.2), dai codici fiscali del dataset ANAC aggiudicatari** del mirror (`tools/verifiche/rivenditori_cf.py`, sul server) [V]. Dei contratti di prodotti extra-UE via rivenditore con aggiudicatari ANAC (1,41 mld), il **99,9 %** va a soggetti con CF italiano (11 cifre o CF di persona). Restano 1,5 M€ a CF esteri o non validi: P.IVA estere (FR, AT, CH, Zoom «EU…») e CF italiani con lo zero iniziale perso (es. «1682521008» per P.S.N.). Ci sono 1.104 CF distinti. Altri 0,41 mld di CIG via rivenditore non hanno righe nel dataset aggiudicatari: il nome viene da altra fonte del file di attribuzione.
- **Riconciliazione 2,04 contro 1,82 mld** [V]: nessun CIG è ripetuto su più anni (9.580 righe, 9.580 CIG). La differenza di 215 M€ viene dal file per rivenditore, che somma l'importo intero del CIG a **ogni membro dell'RTI**. Il totale corretto è 1,82 mld. Ripartito (alla mandataria, o in parti uguali) fa 1,41 mld con aggiudicatari ANAC più 0,41 mld senza.
- **Rigenerazione v3.1 (v0.3):** `tools/analisi/rivenditori.py` ora divide l'importo degli RTI in parti uguali fra i membri. Rigenerato sul server, è pubblicato come `report/metodo/rivenditori-v3.1.*`; la v3 resta per confronto. Il file per rivenditore ora somma **1,824 mld**, uguale al totale per canale. I primi 5 fanno il 70 %: TIM 1,05 mld, Eurolink 78 M, Fastweb 64 M, SoftwareOne 48 M, Var Group 45 M, Postel 43 M; «IMPRESA INESISTENTE» 40 M. `python tools/verifiche/rivenditori_esteri.py v3.1`.
- **Primi per CF** (ripartito): TIM 874 M, Eurolink 62 M, Fastweb 44 M, «IMPRESA INESISTENTE» 42 M, Var Group 42 M, Italware 32 M.
- **«IMPRESA INESISTENTE»** ha un CF valido (02102821002, 24 CIG, 74,8 M€ in tutto). Il nome è un segnaposto su un CF reale: R56 aggiornata.
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
- **1.1 dai decreti (v0.2)** [V]: 16 decreti, 312 CUP, 537,6 M€ finanziati. 238 CUP hanno almeno un CIG, per 197 CIG distinti (`tools/verifiche/pnrr11_prodotto.py`, attribuzione v3 per prodotto):
  - PSN: 111 CIG, 732,5 M€, pari all'**89 %** dell'ICT contato (819,5 M€);
  - big tech USA: **5 CIG, 0,61 M€ (0,07 %)**. Google 0,28 M€ in 2 CIG di servizi professionali; Microsoft 0,33 M€ in 3 CIG cloud e licenze;
  - senza provider: 47 CIG, 85,8 M€;
  - padri di AQ o importi da verificare: 9 CIG, 361,9 M€, fuori dal conto;
  - fuori dal perimetro ICT: 20 CIG.
  Il contratto 1.1 è quasi tutto PSN. La tecnologia erogata dentro il PSN resta invisibile (§ 4).
- **Controvalidazione con FLAG_PNRR_PNC (v0.3)** [V], `tools/verifiche/pnrr_flag.py` (server, 229 file CIG ANAC mensili e delta, DuckDB su disco). Il flag lo dichiara la stazione appaltante, la catena nasce da PA Digitale 2026 e dal dataset cup: sono due vie indipendenti.

  | Catena | CIG | Con flag PNRR | Senza flag | Assenti dai file CIG |
  |---|---|---|---|---|
  | 1.2 (v3) | 12.504 | **11.306 (90 %)**, 733,5 M€ | 1.064, 93,1 M€ | 134, 13,5 M€ |
  | 1.1 (v3) | 61 | 48 (79 %), 344,1 M€ | 10, 14,6 M€ | 3, 19,5 M€ |
  | 1.1 (decreti) | 197 | 136 (69 %), 1.048,1 M€ | 26, 90,2 M€ | 35, 43,0 M€ |

  Gli importi qui sono lordi: comprendono padri di AQ e importi da verificare. Il 10 % di CIG 1.2 senza flag va guardato: CIG collegati al CUP ma pagati con altri fondi, oppure flag omesso.
- **Ponte ufficiale CUP → CIG di Italia Domani (gare ReGiS):** la pagina del catalogo c'è (PNRR_Gare.csv, v11, 13/06/2026), ma il file risponde 403 (Akamai) e il pulsante di scaricamento è solo JavaScript. Nuova **R57**. openpnrr: nell'archivio ci sono solo 3 pagine di progetto, nessun file ponte.

Rifare: `python tools/verifiche/pnrr_bigtech.py` → `esiti/2026-11-06/pnrr/pnrr-bigtech.json`.

## 4. PSN e catalogo ACN (#45)

- **Catalogo ACN non specchiabile:** `catalogocloud.acn.gov.it/opendata` e `/robots.txt` rispondono **403** (Akamai) anche con User-Agent da browser e URL del progetto, dal server, il 6/11/2026 [V]. Non è una sezione di Amministrazione trasparente: vale la regola generale, non si aggira. Nuova **R55**: pubblicazione in open data scaricabile.
- **PSN dai CIG** (già misurato, [imbuto 0.5](/rendiconti/imbuto-dove-siamo/)): impegni ANAC 4,38 mld al netto dei tetti certi, contro un portafoglio di 3,8 mld e ricavi 2023-25 di 0,79 mld [R, bilanci PSN]. Contratti PSN con un prodotto big tech nel testo: 12 per 9,2 M€ [V, mappa v3].
- Senza catalogo né contratti di utenza per ente (R50) la quota del PSN erogata su tecnologia di hyperscaler non è misurabile.

## 5. Mirror Consip (#11) e TED/FTS (#27)

Con gli strumenti esistenti: `tools/archivia.py` (content-addressed, idempotente) e `config/risorse.yaml`, con guardia sul disco (stop sotto 45 GB liberi).

- **Consip:** `tools/acquisizione/consip_elenco.py` legge il catalogo CKAN (16 dataset, 151 risorse dal 2024 in poi, 8,3 GB dichiarati in tutti i formati). Si specchiano per ora le **49 CSV (1,59 GB)**; JSON, XLSX e TTL sono gli stessi dati in altri formati e restano da decidere, per lo spazio. Lanciatore ripartibile `lavoro/consip/specchia.sh`. Esito: **49/49 archiviate** (43 nuove, 6 già presenti e invariate), disco da 60 a 58 GB liberi; elenco in `esiti/2026-11-06/mirror/consip-risorse.csv`.
- **TED:** `tools/acquisizione/ted_mirror.py`, API v3 anonima. Avvisi con acquirente italiano e CPV 72/48/302 dal 2024-01, un mese alla volta, pagine grezze in archivio, mese «completo» quando i raccolti sono pari al totale dichiarato. Esito: **33 mesi (2024-01 → 2026-10), 5.254 avvisi, 33/33 mesi completi**; stato in `esiti/2026-11-06/mirror/ted-stato.jsonl`. Il numero (circa 160 al mese) è basso rispetto alle gare ICT sopra soglia attese: il filtro CPV prende il CPV principale, da controllare.
- **FTS** (beneficiari del bilancio UE): 19 file annuali 2007-2025: **19/19 archiviati** (circa 270 MB).

## 6. Prossimi passi

1. #40: un campione a cieco nuovo (il secondo) per misurare le regole v0.3; atti con browser reale solo su decisione di Fabio.
2. #41: aggiudicatari dei 0,41 mld senza righe ANAC.
3. #43: i 1.064 CIG 1.2 senza flag; i 74 CUP 1.1 senza CIG; il file ReGiS quando sarà raggiungibile (R57).
4. #11 e #27: altri formati Consip; incrocio TED → CIG (`tools/acquisizione/ted_l2.py`) e FTS → aggiudicatari per P.IVA.
4. #45: catalogo ACN a mano con Fabio (consultazione da browser, non automatica) o richiesta ad ACN (R55).

## Registro delle revisioni

| Versione | Data | Modifica |
|---|---|---|
| 0.3 | 2026-11-06 | Regole della lente applicate (non misurate); sottocampione sugli atti 1/9; rivenditori v3.1 con RTI ripartiti; FLAG_PNRR_PNC; R57; mirror Consip, TED e FTS |
| 0.2 | 2026-11-06 | Campione a cieco di 240 CIG (`lente_cieco.py`); CF e nazionalità dei rivenditori, riconciliazione 2,04/1,82 mld (`rivenditori_cf.py`); 1.1 dai 312 CUP dei decreti (`pnrr11_prodotto.py`) |
| 0.1 | 2026-11-06 | Prima bozza: tre verifiche nuove (`lente_prodotto.py`, `rivenditori_esteri.py`, `pnrr_bigtech.py`), R55-R56 |
