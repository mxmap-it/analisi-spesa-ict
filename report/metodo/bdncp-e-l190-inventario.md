# BDNCP e dataset L. 190/2012: inventario e utilità per la spesa ICT

Versione 0.2, 18/11/2026 (#74), pubblicata il 18/11/2026. Scritta solo dagli esiti già versionati. I numeri «ICT» vengono dagli esiti del 18/11/2026 sull'imbuto 0.3.4, con il filtro corretto (strati S3-S6); gli altri numeri sono gli stessi del 10/11. Nessuno scaricamento.

Domanda di Fabio (10/11): «la banca dati contratti pubblici come dataset è clonata e l'abbiamo analizzata per trovarne utilità?»

Legenda: **[V]** verificato da noi, con il comando che rifà il numero; **[R]** riferito da terzi; **[S]** stima, con il calcolo.

## In breve

- **Sì, è clonata:** 62 cartelle di dataset BDNCP nel mirror ANAC, 1.796 file, 128,7 GB (OCDS 73,8 GB, SmartCIG annuali 38,7 GB, CIG annuali 8,6 GB, gli altri 7,6 GB) [V].
- **Ne usiamo poco:** 14 dataset su 62 compaiono nel codice di `tools/` secondo il grep dell'inventario. Con le correzioni di § 3 (falsi positivi e negativi) l'imbuto si regge su CIG, SmartCIG, aggiudicatari, aggiudicazioni, CUP, pubblicazioni, stazioni appaltanti e OCDS [V].
- **Potenziale non sfruttato** (quote sui 443.331 CIG ICT S3-S6 dell'imbuto 0.3.4):
  - quadro economico 54,7 %;
  - indicatori PNRR/PNC 21,1 %;
  - avvio e fine contratto 17,5 % e 7,1 %;
  - stati di avanzamento 2,2 %;
  - varianti e subappalti, con coperture piccole.

  Si usano oggi solo per i 2.130 CIG sopra i 50 M€ (#66) o per niente [V].
- **L. 190/2012:** il registro ANAC ha 27.045 enti distinti (2015-2023). Nel campione di 200 enti del registro 2023, 97 enti hanno un XML con lotti (48,5 %); ANAC dichiara «successo» per l'85,0 % degli URL del 2023 [V].
- I 200 enti del campione pubblicano 34.592 lotti, 8,15 mld € aggiudicati e 0,94 mld € liquidati. Sui 198 CIG ICT: 103,4 M€ aggiudicati, 20,6 M€ liquidati [V]. Le **somme liquidate** sono l'unico dato di spesa effettiva per CIG che oggi l'imbuto non ha.
- **Il mirror completo** di un anno di riferimento peserebbe circa 4 GB di XML [S] e richiederebbe circa 30 ore a 5 s fra le richieste [S]. I dati vanno ripuliti: 2.800 coppie con liquidato maggiore dell'aggiudicato (8,5 %) e anni di riferimento malformati.
- **Correzione rispetto alla v0.1:** gli esiti del 10/11 contavano come ICT anche i padri di accordo quadro (S0). Il filtro è corretto dal 18/11 e i numeri ICT di questa versione vengono dagli esiti del 18/11 (§ 3, punto 1).

## Fonti e comandi

| esito | sha256 | prodotto da | insieme ICT |
|---|---|---|---|
| `esiti/2026-11-18/bdncp/inventario.json` | `280a613e…5c60` | `tools/verifiche/bdncp_inventario.py` | imbuto 0.3.4, S3-S6 |
| `esiti/2026-11-18/bdncp/inventario.csv` | `41df9db8…af94` | idem | idem |
| `esiti/2026-11-18/l190/campione.json` | `cc6e431f…58cd` | `tools/verifiche/l190_campione.py` | idem |
| `esiti/2026-11-18/l190/campione-file.csv` | `4d64f4f4…bf37` (identico al 10/11) | idem | — |
| `esiti/2026-11-10/…` (stessi quattro file) | `4c3b6a05…807a`, `6969288a…f306`, `e213fb8b…54f5`, `4d64f4f4…bf37` | versioni precedenti | imbuto 0.3.1, tutto tranne S1-S2: filtro sbagliato, superato |

Insieme ICT del 18/11: `lavoro/imbuto/ict.csv`, imbuto 0.3.4, sha256 `9604940172cd6f80b52617cf302fcaa7c7002fd06a1162ea93c782c9f8a2fd5c`. Ha 443.331 CIG distinti negli strati S3-S6, lo stesso valore `ict_cig` dell'esito [V].

Per rifare i numeri, sul server come `mxmap.it`, con `nice`, dopo `free -g` e un job pesante alla volta:

```
nice .venv/bin/python tools/verifiche/bdncp_inventario.py              # scrive esiti/<oggi>/bdncp/
nice .venv/bin/python tools/verifiche/l190_campione.py --solo-misura   # offline: stato.jsonl + blob archiviati
```

Le quote e i rapporti sono calcolati con `python3` sui JSON e CSV, per esempio:

```
python3 -c "import json;d=json.load(open('esiti/2026-11-18/l190/campione.json'))['campione']['lotti'];print(d['liq_gt_agg']/d['coppie'])"
```

Fra il 10/11 e il 18/11 tutti i campi non ICT degli esiti coincidono: righe, CIG distinti, byte, file, CSV letto, registro L.190, lotti e importi totali del campione [V]. Cambiano solo `ict_cig`, `cig_ict`, `quota_ict_coperti`, `somme_ict` e gli importi `ict_*`. Cambiano anche alcuni `usato_da`, per strumenti aggiunti a `tools/` nel frattempo.

## 1. BDNCP nel mirror ANAC

### 1.1 Volumi [V]

| gruppo | cartelle | GB | letto dall'inventario |
|---|---|---|---|
| `ocds` | 1 (96 file) | 73,84 | no, solo file e byte |
| `smartcig-2011` … `smartcig-2025` | 15 | 38,65 | no, solo file e byte |
| `cig-2007` … `cig-2025` | 19 | 8,60 | no, solo file e byte |
| tutti gli altri | 27 | 7,63 | sì, l'ultimo CSV |
| **totale** | **62** | **128,72** | |

Per i dataset mensili il mirror ha 7 aggiornamenti datati, da `20260401` a `20261001`. Fa eccezione `smartcig`, che ne ha 5: mancano `20260601` e `20260701` (§ 3, punto 6).

### 1.2 Dataset per dataset

La colonna «CIG ICT (quota)» conta i CIG del dataset presenti nell'insieme ICT dell'imbuto 0.3.4 (S3-S6) e li divide per 443.331. «Usato da» viene dal grep dei nomi in `tools/`, corretto a mano dove indicato.

| dataset | righe | CIG distinti | CIG ICT (quota) | usato | a cosa serve o servirebbe per la spesa ICT e cloud per giurisdizione |
|---|---:|---:|---:|---|---|
| `cig` + `cig-AAAA` | 565.864 (solo il mensile 20261001) | 544.422 | 36.919 (8,3 %, non significativa) | **sì**: imbuto, attribuzione, tetti, SIOPE (136 file per `cig`; gli annuali via `glob("cig-20*")`) | universo: oggetto, CPV, importo, ente, FLAG_PNRR_PNC, collegamento AQ |
| `smartcig` + `smartcig-AAAA` | 683.756 (mensile) | 683.756 | 0 | **sì**: `smartcig_profilo.py`, `metriche_anac.py` | affidamenti minori; non entrano nell'insieme ICT dell'imbuto (0 codici che iniziano per X/Y/Z in `ict.csv` 0.3.4 [V]) |
| `aggiudicatari` | 5.437.334 | 4.818.810 | 254.716 (57,5 %) | **sì**: 50 file (imbuto, rivenditori, lenti, SIOPE) | lente fornitore |
| `aggiudicazioni` | 4.862.077 | 4.849.388 | 255.922 (57,7 %) | **sì**: 9 file (tetti, seconde vie, metriche) | importo aggiudicato, ribasso, offerte. Somma sui CIG ICT: 111,39 mld € (§ 3, punto 9) |
| `partecipanti` | 8.044.052 | 4.746.047 | 246.541 (55,6 %) | no | composizione dei raggruppamenti (ruolo): lente fornitore secondaria; utilità bassa per la misura |
| `quadro-economico` | 5.515.313 | 4.580.650 | 242.374 (54,7 %) | solo `imbuto_qe_sal.py` (2.130 CIG > 50 M€, #66) | **alta**: importi per forniture / servizi / lavori / progettazione e per evento (base d'asta, variante, consuntivo). Separa i servizi dalle forniture e aggiorna l'importo dopo varianti e chiusura. L'inventario non ne calcola le somme (§ 3, punto 4) |
| `stati-avanzamento` | 1.274.801 | 343.824 | 9.807 (2,2 %) | `imbuto_qe_sal.py`, `inhouse_datacenter.py` | **spesa eseguita**: importo dei SAL e certificati di pagamento con data. Somme sui CIG ICT: SAL 19,17 mld €, certificati di pagamento 1,86 mld € su 12.396 righe (§ 3, punto 9) |
| `avvio-contratto` | 1.925.829 | 1.922.826 | 77.719 (17,5 %) | no | date di stipula, inizio e termine contrattuale: durata, quindi ripartizione annua dell'importo |
| `fine-contratto` | 1.070.254 | 1.068.186 | 31.271 (7,1 %) | no | data effettiva di ultimazione (31.000 righe ICT la hanno), risoluzioni, proroghe in giorni |
| `collaudo` | 648.862 | 648.674 | 16.553 (3,7 %) | no | regolare esecuzione (10.430 righe ICT la hanno): contratto eseguito |
| `varianti` | 321.294 | 220.976 | 2.832 (0,6 %) | no (il grep trova la parola «varianti» in `imbuto_prova_034*.py`: falso positivo) | proroghe (`CIG_PROROGA`) e atti aggiuntivi: rinnovi di contratti cloud |
| `subappalti` | 334.301 | 121.030 | 862 (0,2 %) | no | CF e CPV del subappaltatore: chi eroga davvero (es. data center in subappalto); copertura piccola |
| `sospensioni` | 227.747 | 126.325 | 135 (0,03 %) | no | trascurabile |
| `fonti-finanziamento` | 2.449.736 | 2.436.528 | 87.289 (19,7 %) | no | quota da fondi comunitari, di bilancio, mutui: controllo del sottoinsieme PNRR e fondi UE |
| `indicatori-pnrrpnc` | 385.097 | 385.097 | 93.438 (21,1 %) | no | seconda via per riconoscere i CIG PNRR/PNC (oggi FLAG_PNRR_PNC e CUP); da verificare se contiene solo CIG PNRR/PNC |
| `misurepremiali-pnrrpnc` | **0** | 0 | 0 | no | dataset vuoto (§ 3, punto 5) |
| `cup` | 7.228.216 | 7.103.635 | 146.721 (33,1 %) | **sì**: 21 file (PNRR 1.1 e 1.2, PSN). Il grep ne conta 22, ma `archivia.py` è un falso positivo («oc*cup*ato») | collegamento CIG-CUP, sottoinsieme PNRR |
| `pubblicazioni` | 11.417.220 | 11.417.220 | 359.093 (81,0 %) | **sì**: `acquisizione/ted_l2.py` | date GURI/GUCE: aggancio a TED |
| `categorie-opera` | 12.204.598 | 11.416.840 | 359.090 (81,0 %) | no | categoria e classe d'importo; da verificare quali categorie hanno i CIG ICT (lavori su impianti di rete e data center) |
| `categorie-dpcm-aggregazione` | 2.751.379 | 2.730.689 | 111.551 (25,2 %) | no | categoria DPCM dei soggetti aggregatori e deroghe; utilità per l'ICT da verificare |
| `lavorazioni` | 1.008.701 | 893.992 | 1.248 (0,3 %) | no | tipo di lavorazione; utilità bassa |
| `stazioni-appaltanti` | 48.040 | — | — | **sì**: 7 file (anagrafica, CF segnaposto) | ha `flag_inHouse` e `flag_partecipata`, che nessuno strumento legge oggi: servirebbero per la classe in-house (S5, data center interni) |
| `centri-di-costo` | 158.645 | — | — | no | anagrafica; utilità bassa |
| `ocds` | non letto (96 file, 73,8 GB) | | | **sì**: 11 file (periodi, PNRR 1.2, seconde vie) | seconda via per il CIG |
| `attestazioni-soa-v2` | non letto (2 file, 160,6 MB, nessun CSV riconosciuto) | | | no | imprese di lavori: fuori perimetro |
| `bandi-cig-modalita-realizzazione`, `bandi-cig-tipo-scelta-contraente`, `smartcig-tipo-fattispecie-contrattuale` | 23, 47, 77 | — | — | no (le stesse decodifiche sono già nei CSV dei CIG) | tabelle di decodifica |

Pubblicazioni e categorie-opera coprono l'81,0 % dei CIG ICT: il restante 19 % dei CIG dell'imbuto non compare nei due dataset. Il perché è da verificare: mesi recenti, CIG cancellati, ritardi di pubblicazione.

### 1.3 Dataset con potenziale non sfruttato, in ordine di utilità per l'obiettivo

1. **`quadro-economico`**: copre il 54,7 % dei CIG ICT. Dà l'importo per natura (servizi / forniture / lavori) e per evento, cioè la seconda via sull'importo che l'imbuto oggi usa solo per i tetti.
2. **`stati-avanzamento`**: è l'unica spesa eseguita in BDNCP (SAL e certificati di pagamento), ma copre poco (9.807 CIG ICT, il 2,2 %). Per l'ICT servirebbe da controvalidazione, non da misura.
3. **`avvio-contratto` + `fine-contratto` + `collaudo`**: danno la durata effettiva, quindi la quota annua di spesa per CIG pluriennale (oggi la quota annua è stimata). Coprono il 17,5 %, il 7,1 % e il 3,7 %.
4. **`indicatori-pnrrpnc` (21,1 %) + `fonti-finanziamento` (19,7 %)**: il sottoinsieme prioritario PNRR (Misure 1.1 e 1.2) per una via indipendente dal CUP (33,1 %).
5. **`stazioni-appaltanti.flag_inHouse`**: per restringere la classe in-house, oggi contaminata da privati (STATE.md, #66).
6. **`varianti`** e **`subappalti`**: proroghe e catena di fornitura; coperture piccole (0,6 % e 0,2 %).

## 2. Dataset art. 1 c. 32 L. 190/2012

### 2.1 Registro ANAC (`rest/legge190/ricerca`, 354 pagine archiviate il 3/11) [V]

| anno del registro | righe (= enti) | esito ANAC «successo» | quota |
|---|---:|---:|---:|
| 2015 | 18.030 | 8.823 | 48,9 % |
| 2016 | 17.534 | 12.014 | 68,5 % |
| 2017 | 18.093 | 13.709 | 75,8 % |
| 2018 | 19.031 | 15.141 | 79,6 % |
| 2019 | 19.349 | 15.726 | 81,3 % |
| 2020 | 19.024 | 15.248 | 80,2 % |
| 2021 | 19.807 | 16.569 | 83,7 % |
| 2022 | 20.204 | 17.131 | 84,8 % |
| 2023 | 19.889 | 16.897 | 85,0 % |
| **totale** | **170.961** | | |

- Enti distinti nei nove anni: **27.045**. Per ogni anno righe = enti, cioè una comunicazione per ente.
- Campi del registro: codice fiscale, ragione sociale, PEC, URL, data ed esito dell'ultimo tentativo di accesso di ANAC. Il registro non ha né importi né il contenuto dei file: il dato sta presso gli enti.
- Il registro si interroga solo per API di ricerca e si ferma al 2023: già oggetto di R29.

### 2.2 Campione: 200 enti del registro 2023 (dati 2022), seme 190 [V]

Il campione è casuale con seme fisso, preso fra gli enti con URL http. Per ogni ente si sono scaricati l'indice e al massimo 3 file del dataset (il primo, il secondo e l'ultimo), con almeno 5 s fra due richieste. Gli host distinti sono 122.

| esito del file indicato ad ANAC | enti |
|---|---:|
| scaricato (nuovo 111 + già archiviato 10) | 121 |
| — XML dataset in un solo file | 89 |
| — XML indice (link ad altri file) | 8 |
| — non XML (HTML, pagine d'errore…) | 24 |
| assente (HTTP 404) | 26 |
| errore (rete, HTTP, timeout) | 53 |
| **enti con almeno un lotto leggibile** | **97 (48,5 %)** |

- Dagli 8 indici si sono scaricati 18 file, tutti XML dataset validi. Due indici hanno almeno 50 link: per quegli enti il campione legge 3 file su ≥ 50.
- Nel 2023 ANAC ha registrato «successo» per l'85,0 % degli URL; noi a novembre 2026 troviamo un XML con lotti nel 48,5 % dei casi. I due numeri misurano cose diverse (data, criterio di ANAC non documentato), ma lo scarto va spiegato prima di usarlo (§ 3, punto 7).
- I 107 file letti (89 dataset diretti + 18 da indice) pesano 40.790.733 byte: mediana 119.708, massimo 5.155.554. I 18 file da indice pesano 21.490.598 byte e hanno 17.725 lotti.

**Lotti** (somme su tutti i file letti, senza deduplica fra file):

| misura | valore |
|---|---:|
| lotti | 34.592 |
| con CIG di 10 caratteri | 34.419 (99,5 %) |
| CIG nell'insieme ICT dell'imbuto 0.3.4 (S3-S6) | 198 (0,58 % dei CIG) |
| con importo di aggiudicazione | 34.520 — somma 8.154.344.676,69 € |
| con somme liquidate | 34.543 — somma 943.548.677,56 € |
| liquidato > 0 | 27.311 (79,1 % dei lotti con il campo) |
| coppie con aggiudicato > 0 e liquidato presente | 32.987 — aggiudicato 8.154.207.528,55 €, liquidato 811.780.537,29 € (9,96 %) |
| **coppie con liquidato > aggiudicato** | **2.800 (8,5 %)** |
| CIG ICT: aggiudicato / liquidato | 103.411.209,04 € / 20.556.878,54 € (19,9 %) |

Con la correzione del filtro, nel campione restano 198 CIG ICT invece di 294 (−96). L'aggiudicato ICT scende di 49,8 M€, mentre il liquidato ICT cambia poco (−0,38 M€). Ne segue che i padri di accordo quadro esclusi pesavano soprattutto come aggiudicato, non come spesa liquidata.

### 2.3 Anomalie viste nei dati degli enti [V]

1. **Liquidato maggiore dell'aggiudicato** in 2.800 coppie su 32.987 (8,5 %). Le cause possibili, da verificare sui file, sono importi cumulati su più anni, varianti, aggiudicato a zero o simbolico, oppure errori di unità.
2. **Liquidato senza aggiudicato:** 34.543 − 32.987 = 1.556 lotti hanno le somme liquidate ma l'aggiudicato mancante o pari a zero. Valgono 943.548.677,56 − 811.780.537,29 = **131.768.140,27 €** (14,0 % del liquidato).
3. **Anno di riferimento malformato o fuori anno:** su 107 file, 104 dichiarano «2022». Gli altri tre:
   - Eni SpA dichiara `01/26/2022 00:00:00`, una data in formato USA al posto dell'anno;
   - un file dichiara 2021;
   - il Comune di Monastier di Treviso, nell'indice 2023, linka anche `dataset.2013.2172.xml`, con anno 2013.
4. **Possibili doppioni:** ASL AL pubblica due file generati a 10 s di distanza (`dataset_20230127_105735.xml` e `_105745.xml`), di 5,10 e 5,12 MB, con 3.738 e 3.781 lotti. La misura somma i lotti di tutti i file senza deduplicare i CIG, quindi questi sono probabilmente contati due volte. Gli esiti non permettono di quantificarlo (§ 3, punto 8).
5. **Aggiudicato implausibile in scala:** 8,15 mld € da 200 enti, riportati a 19.889 enti, danno circa 811 mld € l'anno [S]. È un valore poco plausibile per un anno: indica massimali di accordi quadro, importi pluriennali ripetuti ogni anno, doppioni o errori. L'aggiudicato del file L.190 non è utilizzabile senza pulizia. Il liquidato riportato alla stessa scala fa 93,8 mld € [S].

### 2.4 Stima del mirror completo e di cosa darebbe [S]

Calcolo dal campione, con 19.889 enti nel registro 2023:

| voce | calcolo | stima |
|---|---|---:|
| byte per anno di riferimento | 40.790.733 B / 200 enti × 19.889 | **≈ 4,1 GB** di XML non compresso (per difetto: due indici letti in parte) |
| tutti gli anni 2015-2023 | 203.954 B × 170.961 righe | ≈ 35 GB, per eccesso: i file invariati fra un anno e l'altro si archiviano una volta sola (sha256) |
| richieste per anno | (200 indici + 18 file) / 200 × 19.889 | ≈ 21.700, più i file degli indici lunghi |
| tempo, 5 s fra due richieste in sequenza | 21.700 × 5 s | **≈ 30 ore** per anno; meno con pause per host (122 host su 200 enti) |
| lotti per anno | 34.592 / 200 × 19.889 | ≈ 3,4 milioni |
| CIG ICT (S3-S6) per anno | 198 / 200 × 19.889 | ≈ 19.700 (v0.1: ≈ 29.000 con gli S0) |
| liquidato sui CIG ICT per anno | 20.556.879 € / 200 × 19.889 | ≈ 2,0 mld € (v0.1: ≈ 2,1). Incertezza alta: pochi CIG ICT nel campione, spesa concentrata |

Spazio libero sul disco del server il 18/11/2026: 355 GB (`df -h /home`) [V]. Il volume non è un vincolo.

**Cosa darebbe:**

- **Somme liquidate per CIG nell'anno:** è la spesa effettiva per contratto, che l'imbuto oggi non ha. Oggi la spesa effettiva si ha solo per ente (SIOPE e BDAP) o per pochi CIG (SAL).
- **Una seconda via sull'aggiudicato e sull'aggiudicatario,** con il codice fiscale.
- **Un ordine di grandezza da confrontare:** il liquidato ICT stimato (≈ 2,0 mld € per i dati 2022) è dello stesso ordine del pagato ICT degli enti non statali da SIOPE per il 2022, 2,99 mld € (STATE.md). Il confronto è grezzo e non controvalida nulla: campione piccolo, possibili doppioni, perimetri diversi (SIOPE per ente, L.190 per CIG nell'insieme dell'imbuto).

**Cosa non darebbe:** non copre gli anni dopo il 2023, perché il registro si ferma lì. Dal 2024 gli obblighi di pubblicazione dei contratti passano per la BDNCP (d.lgs. 36/2023): **da verificare** la norma esatta e la decorrenza, prima di scriverlo in pubblico. Il dato è prezioso per 2015-2023 e per misurare la continuità, non per gli anni correnti.

## 3. Punti aperti: incoerenze negli esiti

1. **Risolto il 18/11: l'insieme «ICT» comprendeva gli S0.** Fino al 10/11 entrambe le verifiche escludevano solo gli strati S1 e S2, mentre la docstring e il ticket parlano di S3-S6. Nella 0.3.1 i 661.633 CIG erano 445.937 in S3-S6 e 215.696 S0 «padre-aq»; delle 215.817 righe S0, 212.660 avevano `cpv_ict = 0` e un importo S0 di 807,17 mld € [V]. Il conteggio si rifà con:

   ```
   nice python3 -c "import csv,collections;c=collections.Counter(r['strato'][:2] for r in csv.DictReader(open('lavoro/imbuto/versioni/0.3.1-20261103/ict.csv',encoding='utf-8')));print(c)"
   ```

   Il 18/11 il filtro è stato corretto in tutte e due le verifiche (tiene solo S3-S6, commento nel codice) e gli esiti sono stati rifatti sull'imbuto 0.3.4. I principali numeri, prima → dopo:

   | misura | 10/11 | 18/11 |
   |---|---:|---|
   | insieme ICT | 661.633 | 443.331 |
   | aggiudicato ICT in `aggiudicazioni` | 553,99 mld € | 111,39 mld € |
   | SAL ICT | 23,18 mld € | 19,17 mld € |
   | certificati di pagamento | 2,09 mld € | 1,86 mld € |
   | CIG ICT nel campione L.190 | 294 | 198 |
   | aggiudicato / liquidato ICT L.190 | 153,2 / 20,9 M€ | 103,4 / 20,6 M€ |
2. **Ripetibilità.** Gli esiti del 18/11 sono legati all'imbuto 0.3.4, `lavoro/imbuto/ict.csv` con sha256 `9604940172cd6f80b52617cf302fcaa7c7002fd06a1162ea93c782c9f8a2fd5c` (443.331 CIG S3-S6, verificato il 18/11). Quelli del 10/11 erano sull'imbuto 0.3.1 (`lavoro/imbuto/versioni/0.3.1-20261103/ict.csv`, sha256 `a814e318…bd4`), con il filtro sbagliato: sono superati, ma restano in git per traccia. Due cose restano aperte:
   - gli esiti non registrano né la versione né lo sha256 dell'insieme ICT: il legame è scritto solo qui;
   - l'insieme sta in `lavoro/`, che non è versionato. Quando l'imbuto cambia, rieseguire non rifà questi numeri (regola #47).

   Correzione proposta: scrivere `imbuto_versione` e `ict_sha256` nell'esito, e far fallire la verifica se lo sha256 non è quello atteso, salvo un parametro esplicito.
3. **`cig` e `smartcig` sono letti solo nel mensile `20261001`** (565.864 e 683.756 righe), perché manca uno zip «pieno». La quota dell'8,3 % non dice nulla sulla copertura dei CIG. Gli annuali `cig-AAAA` e `smartcig-AAAA` non sono letti.
4. **Il campo `usato_da` viene da un grep sul nome e sbaglia in tutte e due le direzioni:**
   - falsi negativi: `cig-2007`…`cig-2023` risultano quasi tutti non usati, ma `imbuto.py`, `attribuisci_provider.py` e `imbuto_tetti.py` li leggono con `glob("cig-20*")`; `smartcig-AAAA` è letto da `smartcig_profilo.py` con `f"smartcig-{y}"`;
   - falsi positivi: `varianti` (parola nel testo), `cup` in `archivia.py`, e probabilmente parte dei 136 file per `cig` e dei 50 per `aggiudicatari`.

   Altri due difetti: il campo `formati` degli annuali contiene i nomi dei file invece dei formati, perché la regex non riconosce `cig_csv_AAAA_MM.zip`; la docstring promette somme anche per `quadro-economico`, che il codice non calcola (anche il 18/11 l'esito non ha `somme_ict` per quel dataset).
5. **`misurepremiali-pnrrpnc` ha 0 righe** nell'ultimo CSV archiviato: è un dataset pubblicato vuoto. È da segnalare come voce in `richieste-e-raccomandazioni.yaml` dopo aver controllato che il file non sia troncato.
6. **SmartCIG mensile:** mancano gli aggiornamenti `20260601` e `20260701` (5 su 7). Non si sa se è una lacuna del mirror o una mancata pubblicazione: va controllato nel `manifest.jsonl`.
7. **Lo scarto fra il registro ANAC e il nostro campione** (85,0 % di «successo» nel 2023 contro 48,5 % di XML con lotti nel 2026) non è spiegato. Servono una tabella per esito (404, errore, HTML) e il confronto con l'esito ANAC ente per ente. Il dato è già in `lavoro/l190-campione/stato.jsonl`.
8. **La misura L.190 non deduplica i CIG fra file dello stesso ente** (caso ASL AL) e legge 3 file su ≥ 50 per due enti. Gli esiti non hanno le somme per ente: non si può dire quanto pesino i primi enti sugli 8,15 mld €.
9. **Somme ICT in BDNCP ancora da controllare.** Anche senza S0, le somme vanno guardate prima di usarle:
   - l'aggiudicato ICT in `aggiudicazioni` è 111,39 mld € su 255.922 CIG (media 435 mila €);
   - l'importo dei CIG S3-S6 nell'imbuto 0.3.4 è 160,41 mld € su 443.331 CIG (media 362 mila €) [V, somma della colonna `importo` di `ict.csv`]. L'ordine di grandezza è coerente, ma senza la distribuzione non si escludono valori anomali;
   - i SAL ICT valgono 19,17 mld € su 9.807 CIG, 1,95 M€ per CIG, e i certificati di pagamento solo il 9,7 % dei SAL. Va verificato se `importo_sal` è cumulativo, cioè se ogni SAL riporta il totale progressivo: in quel caso la somma delle righe conta più volte.

   Nessuna di queste somme è una misura della spesa ICT.

## Cosa proponiamo (per Fabio: proposte, non decisioni)

1. **Completare le due verifiche** (il filtro S3-S6 è fatto il 18/11):
   - scrivere versione e sha256 dell'imbuto nell'esito;
   - aggiungere le somme del quadro economico e le distribuzioni (percentili) degli importi;
   - per i SAL, prendere l'ultimo progressivo per CIG invece della somma delle righe, se risulta cumulativo;
   - per `cig` e `smartcig`, leggere gli annuali o dichiararne l'esclusione;
   - per L.190, deduplicare per CIG dentro l'ente, aggiungere le somme per ente e la tabella esito ANAC contro esito nostro.

   Costo: due giri in streaming sul server, uno alla volta.
2. **Usare `quadro-economico` sull'intero insieme ICT** come seconda via sull'importo (servizi o forniture, importo dopo le varianti), estendendo `imbuto_qe_sal.py` oltre i 2.130 CIG sopra i 50 M€.
3. **Usare avvio, fine contratto e collaudo per la durata,** quindi per la quota annua dei CIG pluriennali (coperture S3-S6: 17,5 %, 7,1 %, 3,7 %).
4. **Provare `stazioni-appaltanti.flag_inHouse`** per ripulire la classe in-house (S5).
5. **L.190: mirror completo del solo 2023 (dati 2022),** a 5 s fra le richieste e con pause per host. Costa circa 4 GB e circa 30 ore [S]. Si fa solo dopo la pulizia (doppioni, liquidato > aggiudicato, anni malformati) e solo come fonte di **somme liquidate per CIG**, da confrontare con SIOPE per ente. Gli anni 2015-2022 si valutano dopo l'esito del 2023.
6. **Nuove voci in `richieste-e-raccomandazioni.yaml`** (da approvare):
   - ANAC: `misurepremiali-pnrrpnc` pubblicato vuoto;
   - ANAC: validare alla ricezione il file L.190 (anno di riferimento nel formato previsto, liquidato coerente con l'aggiudicato), e conservare e pubblicare in blocco i file raccolti, non solo il registro degli URL (estensione di R29).

## Limiti

- I numeri ICT vengono dagli esiti del 18/11 sull'imbuto 0.3.4: cambiano a ogni nuova versione dell'imbuto (§ 3, punto 2).
- Il campione L.190 ha 200 enti: per i 198 CIG ICT l'incertezza è alta, e le stime di § 2.4 sono ordini di grandezza.
- Gli esiti non contengono distribuzioni (per ente, per lotto, per importo): le anomalie sono contate, non spiegate.
- L'utilità dei dataset non usati è dedotta dai campi e dalla copertura, non provata su un caso: va misurata prima di entrare nella metodologia (`metodo-cloud-provider.md`).
- L'OCDS (73,8 GB) e gli annuali non sono stati letti dall'inventario.

## Registro delle revisioni

| versione | data | autore | modifiche |
|---|---|---|---|
| 0.1 | 18/11/2026 | Claude (agente), per Fabio Pietrosanti | prima stesura dagli esiti `esiti/2026-11-10/bdncp/` e `esiti/2026-11-10/l190/` (#74) |
| 0.2 | 18/11/2026 | Claude (agente), per Fabio Pietrosanti | numeri ICT dagli esiti `esiti/2026-11-18/` (filtro S3-S6, imbuto 0.3.4, `ict.csv` sha256 `96049401…d5c`); verificato che i numeri non ICT coincidono con il 10/11. § 3.1 risolto, § 3.2 riformulato, nuovo § 3.9 (somme ICT da controllare); aggiornati «In breve», fonti, § 1.2-1.3, § 2.2, § 2.4, proposte, limiti (#74) |
