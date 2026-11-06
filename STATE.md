# STATE — punto di ripresa

Per chiunque riprenda il lavoro, umano o Claude. Si aggiorna a ogni avanzamento.

**Ultimo aggiornamento:** 2026-11-06


## MIRROR CONGELATI il 7/11/2026 (Fabio): punto di ripresa
Si fermano per il disco: 44 GB liberi, sotto la soglia di 45 della guardia. Le scelte sullo storage (object storage UE, pulizia degli altri progetti) spettano a Fabio. Tutto il resto del lavoro va avanti.
- **ANAC:** completo, 1.796 risorse su 1.800 (le altre 4 rispondono 404 alla fonte). Il mirror quotidiano (cron) resta attivo, ma senza spazio la guardia lo ferma.
- **Consip (#11):** completo, 151 risorse in tutti i formati. I 7 file grandi sono archiviati con scaricamento a riprese (`tools/acquisizione/scarica_ripresa.sh`, log `lavoro/consip/grandi.log`).
- **OpenCUP (#26):** completo, compreso `OpendataComplessivo.zip` da 3,4 GB (`lavoro/opencup-grande.log`).
- **TED (#27):** 34 mesi, da 2024-01 a 2026-10. FTS dal 2007 al 2025.
- **SIOPE (#12), IndicePA e PA Digitale (#13), GLEIF (#28), OpenCoesione (#26), CPT ed Eurostat COFOG (#29):** archiviati.
- **Da riprendere:**
  1. BDAP (#25): circa 750 righe di metadati CKAN, `package_search?rows=1000&start=1000`, che cadono sempre. È l'ultima riga di `lavoro/consip/riprova.txt` e va riprovata in orari di poco carico.
  2. Italia Domani/ReGiS (403, R57) e catalogo ACN (403 Akamai, R55): bloccati, decide Fabio.
  3. Gli scaricamenti delle prossime annualità.
- **Come riprendere:** liberare spazio, cioè avere almeno 45 GB liberi, poi `bash tools/acquisizione/coda_mirror.sh config/coda-mirror-2026-11.txt` (ripartibile: `archivia.py` salta ciò che è invariato) e `tools/archivia.py --lista lavoro/consip/riprova.txt`.
- **Scaricamenti propedeutici all'analisi** (atti, documenti dietro i link PVL, pagine AT): continuano, piccoli e con una guardia propria a 40 GB.
## #57 DOCUMENTI L3 PER IL RESIDUO S6 FUORI DALLA VIA 6 — punto di ripresa 7/11/2026
- **7/11 notte:** L4 181 enti, 735 CIG trovati (6,7 mld); L3 4.075/12.180; MePA finito (582, 0 pagine pubbliche); blocchi/robots/piattaforme da visibilita_pa (confronto: 44 differenze, tutte falsi blocchi delle regole vecchie, ripassati); ariaspa ripassato. Proposta per visibilita-pa: CAPTCHA nell'URL (pagina-cancello ANAC /superset/recaptcha/) in riconosci_blocco; host cloud.urbi.it e sicopat2 nelle REGOLE delle piattaforme.
- **Stato 7/11 sera e RIPRESA A MANO (Fabio: niente cron).** In corso sul server: L3 (`piattaforme_cig.py`, 3.358 su 12.180 CIG con link), MePA (`mepa_cig.py`, 315 su 591: 0 pagine pubbliche), L4 (`at_cig.py`, 66 enti, 338 CIG trovati per 6,2 mld) e il ripasso AT notturno (`residuo_s6_at.sh`).
  - Rilancio, ripartibile: `cd ~/analisi-spesa-ict && (HOST_PARALLELI=5 setsid nohup bash tools/acquisizione/residuo_s6.sh >/dev/null 2>&1 &) ; (HOST_PARALLELI=4 SPESAICT_BASE=$PWD setsid nohup nice -n 15 .venv/bin/python tools/acquisizione/at_cig.py lavoro/residuo-s6/ingresso.csv lavoro/residuo-s6/l4 >> lavoro/residuo-s6/l4.log 2>&1 &) ; (setsid nohup bash tools/acquisizione/residuo_s6_at.sh >/dev/null 2>&1 &)`.
  - Ripassi mirati: `RIPASSA=errore SOLO_HOST=ariaspa` (ariaspa: la porta 80 non risponde, ora si passa in https); `RIPASSA=cig-non-trovato` per riprovare con la ricerca interna.
  - www.difesa.it ed esercito.difesa.it non rispondono dal server (timeout): vanno provati da un'altra origine, con il monitoraggio AT.
  - Misura: `.venv/bin/python tools/verifiche/residuo_s6_copertura.py <data>`.
- **Riuso di visibilita-pa (indicazione di Fabio).** at_cig.py importa `visibilita_pa.core.probes`: `locate.link_at` (sezione AT), `extended._cerca` (ricerca con browser), `checks.browser_playwright`.
  - Doppioni da sostituire in analisi-spesa-ict: `piattaforme_cig.blocco/SEGNI_BLOCCO` → `extended.riconosci_blocco` e `basic.firme`; `robots_ok` → `visibilita_pa.core.robots` (doppio parser); `config/at_robots_esenti.txt` → `platforms.riconosci` più la tabella enti AT.
  - **Proposte per visibilita-pa (da fare là, non qui):**
    - rendere pubbliche `_cerca` e `CAMPI_RICERCA`;
    - aggiungere una ricerca senza browser sui moduli GET (oggi `piattaforme_cig.modelli_ricerca/cerca_cig`), da far importare a noi;
    - aggiungere una funzione che restituisca la sezione «Bandi di gara e contratti», oltre alla AT.
- **In corso sul server** (`lavoro/residuo-s6/`, `giro.log`, stato in `out/esiti.jsonl`): `bash tools/acquisizione/residuo_s6.sh` (lock, ripartibile; `FINITO.txt` a fine giro, `STOP-disco.txt` se il disco scende sotto 15 GB, guardia decisa da Fabio il 7/11).
- **Ripresa automatica, RIGA DA METTERE NEL CRONTAB (Fabio):** `*/30 * * * * cd ~/analisi-spesa-ict && bash tools/acquisizione/residuo_s6.sh >/dev/null 2>&1`
- **Ingresso** `tools/acquisizione/residuo_s6_ingresso.py`: 28.583 CIG (P1 70 ICT incerti, P2 21.525 G3 oltre la via 6, P3 2.395 G2, P4 3.593 nuovi «sw»/«connettività», P5 1.000 G4 a campione); 16.403 senza link PVL (pre-2024).
- **Misure parziali** (2.093 CIG con link su 12.180): CIG citato 137, con documenti 62, con documento che cita il CIG 20; robots 317, blocchi 19. Documenti che citano il CIG in `dati/atti/atti-server.jsonl` (livello L3): la via 6 li trova per CIG. Rimisurare con `tools/verifiche/residuo_s6_copertura.py <data>` e aggiornare `acquisizione-documenti.md`.
- **Aggiornamento 7/11 (decisioni già in AGENTS §3):** host AT esclusi da robots.txt ripassati di notte (`tools/acquisizione/residuo_s6_at.sh` in attesa delle 21, `config/at_robots_esenti.txt`, robots.txt archiviato come evidenza). MePA con Playwright (`mepa_cig.py`): 0 su 85 CIG con pagina pubblica, R62. L4 avviato (`at_cig.py`, `lavoro/residuo-s6/l4/`): 79 enti e 3 CIG trovati. `residuo_s6.sh` concatena L3, poi MePA, poi L4 (la riga cron è sopra). **Prossimo:** adattatori per i software AT (ricerca interna per CIG o elenchi per anno), poi Playwright per le pagine AT in JavaScript.

## #40 #41 #43 #45 #11 #27 #12 #13 #25 #26 #28 #29 OBIETTIVO 6 E MIRROR — punto di ripresa 6/11/2026 (rendiconto 0.5)
- **Aggiornamento 0.5.1 (6/11, sera):**
  - **OpenCUP:** il bulk sta su `/portale/web/opencup/accesso-agli-open-data` e `dettaglio-opendata-complessivo`. Archiviati metadati, decodifiche e file CUP PNRR; `OpendataComplessivo.zip` (3,4 GB) in coda con `tools/acquisizione/scarica_ripresa.sh` dopo i file grandi di Consip. La guardia a 45 GB può fermarlo: con circa 50 GB liberi e circa 3 GB di Consip prima, controllare `lavoro/opencup-grande.log`.
  - **CPT:** 36 file di spesa del catalogo Open CPT archiviati.
  - **ISTAT COFOG:** coperto da Eurostat.
  - **Consip:** il server taglia i file sopra circa 350 MB, quindi curl con ripresa e poi `archivia.py --da-file`. `cataloghi2024.json` è archiviato, gli altri 6 sono in corso (`lavoro/consip/grandi.log`).
  - **BDAP:** la pagina `package_search start=1000` cade sempre (il server chiude dopo 120 s), anche in pagine da 250: da riprovare in orari di poco carico.
  - **Vincitori TED per l'imbuto (#66):** `esiti/2026-11-06/imbuto/ted-vincitori.csv` (`tools/verifiche/ted_imbuto.py`). 84 CIG con vincitore TED e senza aggiudicatari ANAC; 72 nell'imbuto, di cui 7 in S6 (19 M€) e 55 in S5. Da integrare a cura di chi gestisce l'imbuto: il rendiconto imbuto-dove-siamo non è stato toccato.
- **Rendiconto** bozza non elencata `sito/content/rendiconti/obiettivo-6.md` v0.5.
- **#40:** tre campioni a cieco (`report/metodo/lente-cieco{,-2,-3}/`; `tools/verifiche/lente_cieco.py CARTELLA`). Misure indipendenti big tech: R 81 % → 89 % → 89 %, P 100 % / 95 % / 100 %. Regole v0.5 in `config/marchi_cloud.yaml`; il terzo campione le misura. La lente testuale è al limite: non aggiungere regole senza un quarto campione.
- **#41 / #43:** invariati rispetto a 0.4 (rivenditori v3.1; FLAG_PNRR_PNC 90 %; R57, R58).
- **#11 Consip:** 151 risorse, 94 nuove, 50 invariate, 7 errori (JSON e TTL grandi, connessione interrotta). Nuovo tentativo in coda: `lavoro/consip/riprova.txt` (più BDAP start=1000), parte da solo dopo IndicePA.
- **#27:** TED v2 di 34 mesi, 5.348 avvisi; TED → CIG 6,6 %; TED come fonte di esiti: 112 righe senza aggiudicatari ANAC, 88 con vincitore e P.IVA TED, 298 M€ (`esiti/2026-11-06/mirror/ted-esiti.csv`). R59.
- **Coda mirror** (`config/coda-mirror-2026-11.txt`, `tools/acquisizione/coda_mirror.sh`, guardia 45 GB). Archiviati: PA Digitale 2026, SIOPE uscite 2017-2026 e anagrafiche, BDAP (4/5 pagine del catalogo), Eurostat COFOG, GLEIF (LEI2, RR, REPEX), OpenCoesione. IndicePA: 54 risorse in corso (`lavoro/indicepa/mirror.log`).
- **Da fare:** OpenCUP (URL 404, da ritrovare), CPT e ISTAT (URL), ItaliaDomani (R57). Registrazioni in `config/risorse.yaml`. Disco 52 GB liberi.
## #17 #9 MIRROR PUBBLICO ANAC — punto di ripresa 6/11/2026 (indicazione di Fabio del 7/11)
- **Stato [V]:** ANAC 1.796/1.800 risorse del catalogo con sha256 (128,7 GB; OCDS 96 file 73,8 GB); le 4 mancanti sono 404 alla fonte (P10). Totale mirror fonti di risorse.yaml 2.024 risorse, 134,1 GB. Nessuna risorsa ha ancora cambiato sha256 dal 26/10. 13 file > 2 GiB (max OCDS 2025/10, 5,25 GB). Server: 51 GB liberi.
- **Indice:** `tools/indice_mirror.py` (manifest → `report/mirror/indice.{json,csv}`, `sintesi.json`; sul server con `ARCHIVIO_ROOT`), `tools/pagine_mirror.py` (rigenera le tabelle fra i marcatori GEN e copia in `sito/static/dati/mirror/`; serve PyYAML → .venv del server).
- **Bozze non elencate:** `/progetto/mirror-pubblico/` (requisiti, 7 opzioni di hosting, proposta), `/progetto/perche-un-mirror/` (evidenze [V]/[R]; Consip ordini-mepa 2022 e 2023 → 404 il 6/11), `/progetto/usi-dei-dataset/` (dati in `config/usi-dataset.yaml`, 25 schede × 5 progetti).
- **DECISIONE A FABIO (#17):** hosting. Proposta: bucket S3-compatibile UE (Hetzner/Scaleway, ~5-10 €/mese [R]) con percorsi originali + frontale nginx su mxmap.it per le risposte CKAN statiche, dominio mirror.mxmap.it; Zenodo per snapshot annuali con DOI; GitHub solo indice/manifest. Nessun GB caricato in pubblico.
- **Prossimi passi:** archiviare con sha256 la prova Consip 404 nella sonda; confronto sha256 fra versioni come metrica quando ci saranno cambi; SIOPE «last» e IndicePA: verificare la sovrascrittura [R].

## #40 #41 #43 #45 #11 #27 OBIETTIVO 6 — punto di ripresa 6/11/2026 (rendiconto 0.4)
- **Rendiconto** bozza non elencata `sito/content/rendiconti/obiettivo-6.md` v0.4. Verifiche in `tools/verifiche/` (lente_prodotto, lente_cieco [arg: cartella del campione], rivenditori_esteri, pnrr_bigtech locali; rivenditori_cf, pnrr11_prodotto, pnrr_flag, ted_cig, fts_piva sul server).
- **#40:** il secondo campione a cieco (`report/metodo/lente-cieco-2/`, 120 CIG S2-S4) misura le regole v0.3: big tech P 56/59 = 95 %, R 56/63 = 89 %. Falsi positivi: backup di M365, collocation AWS, corso AWS. Mancati: Microsoft senza le parole chiave (EA9, CP-PILOT, Windows XP…). Regole nuove NON applicate: andrebbero misurate su un terzo campione.
- **#41:** v3.1 con RTI ripartiti (1,824 mld), CF italiani 99,9 %.
- **#43:** FLAG_PNRR_PNC sul 90 % dei CIG 1.2. Dei 1.064 senza flag, 627 nominano il PNRR nell'oggetto → R58. ReGiS 403 → R57.
- **#11:** Consip in tutti i formati, `lavoro/consip/specchia-tutti.sh` sul server (in corso al commit, circa 90/151, ripartibile, guardia 45 GB): alla fine contare nuovo/invariato in `lavoro/consip/specchia-tutti.log` e aggiornare il rendiconto § 5.
- **#27:** filtro TED verificato (classification-cpv = tutti i CPV, 143 contro 132 del solo principale sul marzo 2024). TED v2 (`lavoro/ted-v2/`): 34 mesi, 5.348 avvisi (la v0.3 diceva 33/5.254: corretto). TED → CIG 355/5.348 (6,6 %), P.IVA coincidente 157/177 → R59. FTS: 90 aggiudicatari cloud su 1.018 ricevono fondi UE diretti.
- **Prossimo:** terzo campione a cieco per esclusioni e regole Microsoft; chiusura del mirror Consip; TED come fonte di esiti per i CIG ANAC senza aggiudicazione; catalogo ACN (Fabio).

## #44 #59 #46 #50 #52 PERIMETRO, CPV, OCDS, AQ, IN-HOUSE — punto di ripresa 6/11/2026
- **#44 perimetro ICT:**
  - lista bianca in `config/perimetro_cpv.yaml` (13 prefissi, uguale a `CPV_ICT`, la verifica lo controlla);
  - verifica `tools/verifiche/perimetro_cpv.py` (campioni da `perimetro_cpv_campiona.py`, etichette in `report/cpv/campione-*/`) → `esiti/2026-11-06/cpv/perimetro-cpv.json`;
  - precisione **83 %** (93 % con i dubbi) su 200; falsi esclusi in S1 **1,0 %** (2/200, 3,5 % con i dubbi);
  - **proposte per Fabio:** togliere 79342 marketing (0/5 ICT, 5.859 CIG e 567 M€ dal 2024); rivedere 3224; aggiungere `\bsw\b` e `connettivit` a `RX_ICT`. Non applicate.
- **#44, decisione di Fabio del 7/11:**
  - 79342 tolto da CPV_ICT e dal yaml, dopo la review di 177 CIG (3,0 % ICT veri stimati, 0 sopra 1 M€): 5.706 CIG e 539 M€ dal 2024 passano in S1;
  - 3224 resta in lista: la review dice 79 % videosorveglianza, 2,4 % ICT stretto; una sottoclasse videosorveglianza da decidere. Il CIG B139F77033 ha un importo errato di 4,7 mld;
  - RX_ICT con sw e connettività (imbuto 0.3.3): 3.593 CIG in più nel residuo S6, di cui G1 29 per 3,8 mld (SPC Connettività, ASI);
  - prove: tools/verifiche/perimetro_cpv_effetto.py, report/cpv/review-79342-3224/;
  - **DA FARE a via 6 finita:** rigenerare ict.csv con imbuto 0.3.3 (python tools/analisi/imbuto.py sul server), poi rifare imbuto_strati e perimetro_cpv. Non è stato rigenerato perché la via 6 legge ict.csv.
- **#59 CPV:**
  - sui 543 ICT del campione 611: 74 % specifico, 17 % generico, 9 % fuori lista (25 con il segnaposto 99999999);
  - cloud con codice di servizio erogato: 30 % (contro l'11 % dei non cloud);
  - base dal 2024: 99999999 o vuoto 8,3 %, codice di gruppo 16,2 %;
  - ECA SR 28/2023 aperta e archiviata: **il 49,8 % non c'è** (valori mancanti circa 30 %);
  - Ramboll/BME 2012 trovato: 405 avvisi, 23 % di codici inesatti;
  - rendiconto bozza `sito/content/rendiconti/perimetro-cpv.md` (non elencato); R21 aggiornata, R60 nuova (segnaposto).
  - **Prossimo:** uscita di riclassificazione `dati/classificazioni/cpv-riclassificazione.csv`; etichette umane su L e S1; includere `lente-cieco-3` quando sarà versionato.
- **#46 OCDS release.date** (`tools/verifiche/ocds_release_date.py`, `esiti/2026-11-06/ocds/`, 96 mesi):
  - le due vie concordano su 4.751.105 date;
  - conformi solo 2018/01-2019/11; **da 2019/12 zero conformi** (la scheda P04 diceva «fra il 2021 e il 2023»: corretta);
  - 3.594.570 release senza data. P04 aggiornata con sha256 e metrica.
- **#50 cig_accordo_quadro** (`tools/verifiche/cig_aq_modalita.py`, `esiti/2026-11-06/cig-aq/`):
  - con modalità «discendente» il campo è compilato nel 98,6-100 %: mancano 4.130 CIG nel 2024 e 3.946 nel 2025;
  - il «20 % vuoto» era l'espressione sul testo: precisione 3/60 (5 %), quasi tutti appalti specifici di SDA;
  - **decisione:** P15 resta interno (esito nella scheda) e R01 è ridimensionata. Se Fabio vuole, il difetto piccolo («discendente senza CIG padre», circa 4.000 l'anno) può diventare una scheda pronta: è verificato su campo strutturato.
- **#52 in-house/datacenter** (`tools/verifiche/inhouse_datacenter.py`, `esiti/2026-11-06/inhouse/`), punto aperto:
  - in-house dal 2024: 943 CIG, 774 M€, 446 enti. La classe è **contaminata da privati** (Accenture 91 M€, HTDI 48, TAI 31, DGS, TIM, Fastweb): va ristretta alle società pubbliche;
  - SAL su 17 CIG su 943;
  - infrastruttura propria: hardware 31.677 CIG e 4,5 mld; consulenza su infrastruttura 3.527 e 2,7 mld; software di infrastruttura 663 e 0,8 mld (VMware 651); testo datacenter/CED 10.991 e 3,1 mld (importi del lotto, con i tetti).

## #66 #55 VIA 6 SU G1 + PRIMI 1.000 G3 (top-5 punto 4) — punto di ripresa 6/11/2026 (decisione di Fabio)
- **Gira sul server, da solo:** `tools/llm/giro_imbuto.sh` (Sonnet in abbonamento, istruzioni `tools/llm/istruzioni-p3.md`, due assi con stato; PAR 4; ordine g1 → ctl → g3), rilanciato ogni 30 min dal cron `tools/llm/giro_imbuto_guardiano.sh`, che a ogni passaggio rifà la verifica (`tools/llm/verifica_imbuto.py`) e i numeri (`esiti/imbuto-via6/via6-g1g3.json`, da `tools/verifiche/imbuto_via6.py`). Il tetto di 100 USD-eq al giorno ferma e riprende da sé (codice 75).
- **Selezione:** `report/metodo/llm/imbuto-g1g3/selezione.json`: G1 196 CIG unici (4,70 mld), G3 1.000 (1,55 mld), CTL 15 dal campione 611. ict.csv ha CIG ripetuti (G1 13, G3 52): R53.
- **Budget G3:** stima 360, guardia a 432 USD-eq (`tools/llm/imbuto_budget.py`, etichetta `imbuto-g3` in `stato/claude-consumi.jsonl`). Se scatta, scrive `stato/imbuto-g1g3-STOP.txt`, che ferma solo g3: chiedere a Fabio. Misurato: G3 0,32 per CIG (proiezione 320), G1 circa 0,70 per CIG.
- **Uscite:** proposte da revisionare in `dati/classificazioni/imbuto-g1g3.jsonl` (`spesaict.classificazione/1`) e `report/metodo/llm/imbuto-g1g3/verificati.jsonl`. Rendiconto imbuto 0.4 § 4.3 e § 9.1.
- **Riproducibilità (richiesta di Fabio):**
  - prompt portabile `report/metodo/llm/prompt-analisi-documentale-v1.md` (sha256 accanto), schema `schemi/analisi-documentale.schema.json`;
  - runner neutro `tools/llm/analisi_documentale.py` (stampa / openai / ollama / claude-cli / importa), confronto `tools/verifiche/concordanza_llm.py`;
  - `tools/llm/riproduzione.sh`, lanciato dal guardiano, congela il pacchetto da 50 CIG, fa girare Haiku e qwen3-vl:8b (Ollama già installato, solo CPU, lento) e scrive le concordanze in `esiti/imbuto-via6/`;
  - pilota su 12 CIG: asse B 10/12, asse A 6/12.
- **Al termine:**
  - rivedere i numeri del § 4.3 dal JSON e aggiornare il rendiconto;
  - revisione umana a campione delle proposte (tutte le «certo» di G1 e un 10 % di G3);
  - deduplicare per CIG in `tools/analisi/imbuto.py`;
  - chiave per un modello cloud gratuito: decide Fabio.

## #66 IMBUTO: DOVE SIAMO — punto di ripresa 6/11/2026 (consegna del 12/11)
- **0.9:** § 4.8, vincitori TED (`ted-vincitori.csv`, altro agente) come seconda fonte degli aggiudicatari: 72 CIG nell'imbuto, precisione P.IVA 89 % (riferita da #27); strati invariati (integratori, non produttori).
- **0.8:**
  - `tools/acquisizione/piattaforme_cig.py`: adattatori portaleappalti/esop/generico; CINECA Oracle B90DB64041 scaricato da anonimo (ULA, nessun cloud); Banca d'Italia non in elenco pubblico; Terna = login (rimando JS non riconosciuto: da correggere); Calabria, CSI, Hera non trovati.
  - Oracle: 5 atti (CINECA, ISTAT, MAECI, Giustizia DIT, Lepida), 0 con cloud (Wilson 0-43 %). EA: 3 ricerche in più, 0 atti.
  - **Rigenerazione imbuto 0.3.2 da fare a mano** a fine via 6 (`pgrep -f giro_imbuto.sh` vuoto e guardiano senza pacchetti mancanti): `nice .venv/bin/python tools/analisi/imbuto.py 2020`, poi copiare `lavoro/imbuto/riepilogo.json` in `esiti/…/riepilogo-0.3.2.json`. La regola cron automatica non è stata autorizzata.
- **0.7:**
  - `ea_censimento.py`: 8 atti EA con prodotti (MAECI fra i primi 50, 9,4 M€), quota cloud pesata 92 %, 8/8 a prevalenza cloud (Wilson 68-100 %); forbice sul residuo MS 819 M€: 0,55-0,81 mld cloud; `ea-quota-cloud-elaborazione.md` § 4 aggiornato.
  - Oracle: i primi 20 incerti (261 M€) sono supporto e rinnovi, on premises probabile (nessun atto letto).
  - `imbuto.py` 0.3.2: dedup per fonte (CIG ripetuti nello stesso file annuale); NON rigenerato finché gira la via 6 (`tools/llm/giro_imbuto.sh`).
  - Da fare: ricerca del CIG dentro le piattaforme di e-procurement da anonimo (per i primi 30 link PVL), 49 EA C1 senza atto.
- **0.6:**
  - `imbuto_doppioni.py`: 11.043 righe duplicate nei file annuali 2024/2025 (conti che tornano: 5.713.798 righe − 11.043 = 5.702.755 CIG); correzione sui totali, `ict.csv` non toccato (via 6 in corso). S3-S6 dal 2024 a 55,3 mld.
  - `imbuto_licenze.py`: 3.508 CIG di licenze/marchi, 2,76 mld netti; cloud 168 M€ (extra-UE 141), non cloud 892 M€, incerto 1,68 mld (MS 799, Oracle 401, ? 396, SAP 83).
  - Prossimo: censimento SKU dei primi 50 EA (atti), correzione dei doppioni in `imbuto.py` alla prossima rigenerazione, dopo la via 6.
- **0.5 (chiusura del giro tetti/PNRR):**
  - visita AT dei 79 CIG ICT incerti (`fuori_piattaforma_at.py`, ingresso `lavoro/imbuto/at79/`): 40 enti, 0 atti, fermata per resa zero; 4 blocchi aggiunti a `report/convenzioni/blocchi-accesso.csv` (SOGEI, CINECA 403; UniBa Radware; ASL Pescara → reCAPTCHA ANAC), da validare in R45/R46;
  - E4: dichiarato errato 14/15 (70-99 %), quadro economico plausibile 9/15 (36-80 %), 46/115 rapporti potenza di 10;
  - PNRR chiuso a 16 decreti, 537,6 M€.
  - **Chiuso per ora:** 79 CIG / 14,4 mld incerti, solo accesso agli atti (non autorizzato).
- **0.4, parte tetti/PNRR (6/11 notte):**
  - secondo campione T4 concessione: 9/15, totale 20/30 (67 %, 49-81); con la regola I6 (concessioni energia/TPL/impianti → incerto) 17/18 (94 %, 74-99);
  - `imbuto_qe_sal.py`: quadro economico e SAL ANAC per 442 e 41 dei 2.130 CIG; regola E4; gli 8 errori d'importo con QE valgono 70.150 €; SAL 0,40 mld (ICT 0,15);
  - atti degli incerti: 0 su 10 ricerche, ricerca fermata → R54;
  - PNRR: decreto fin 3.1 (iss.it), 16 decreti per 537,6 M€; `pnrr11_cup_cig.py`: 238/312 CUP con CIG; 431 M€ finanziati contro 2,20 mld di contratti PSN collegati;
  - S3-S6 58,3 mld, 14,4 incerti in 79 CIG.
- **0.3 (6/11 notte):**
  - `tools/verifiche/imbuto_revisione.py`: precisione sul campione stratificato (15 per gruppo, giudizi sugli atti in `esiti/2026-11-06/imbuto/campione-tetti-giudizi.csv`): T3 tondo 8/15 (53 %, 30-75), T3 non tondo 15/15 (80-100), T4 AQ 15/15 (80-100), T4 concessione 11/15 (73 %, 48-89); T4 su PVL 191/192.
  - Regole v2: T3 tondo solo se discendente; T5 e E2 dal PVL (`pvl-percig.csv`); revisione degli incerti ICT con 10 errori d'importo (14,1 mld) e 9 tetti. S3-S6 dal 2024 scende a **58,2 mld** (incerti 14,4 mld in 80 CIG).
  - `tools/verifiche/pnrr11_decreti.py`: 15 decreti PNRR 1.1 archiviati, 15/15 coerenti al loro interno, 524,2 M€ su 298 CUP e 274 enti (75 % dei ~700 M€ [R]). Nuova R51.
  - Prossimo: atti degli 80 incerti ICT; decreti PNRR mancanti; CUP → CIG.
- **0.2 (6/11 sera), top-5 punti 2 e 3 fatti:**
  - `tools/verifiche/imbuto_tetti.py`: i 2.160 «da verificare» sono 2.130 CIG distinti (30 righe duplicate nei file annuali). Esito: 781 tetti per 178,0 mld (vie T1 padre copiato 78, T2 oltre l'ordinato Consip 14, T3 importo ripetuto 187, T4 modalità AQ/concessione 502); 32 spesa effettiva (E1, aggiudicato); 1.317 incerti per 612,8 mld. S3-S6 dal 2024 da 113,3 a 76,5 mld (incerti ancora dentro 33,6). Esiti in `esiti/2026-11-06/imbuto/tetti*`.
  - `tools/verifiche/imbuto_psn.py`: impegni ANAC PSN 5,10 → 4,38 mld (tetto Taranto 723 M€), contro un portafoglio di 3,8 mld [R] e ricavi 2023-25 di 0,79 mld [R] (Libro PSN 2025 e bilancio 2024 archiviati, sha256 in `esiti/2026-11-06/psn/bilanci-psn.json`); PPdF pubblicati da 20 PA su 617. Nuove R49 (ordinato per CIG) e R50 (contratti di utenza PSN e PNRR 1.1 per ente).
  - Prossimi passi: controllo a campione di T3/T4; importo dell'ordinativo dagli atti per i ~114 CIG ICT incerti; spoglio dei decreti PNRR 1.1 (presidenza.governo.it, PDF).
- **Fatto:** rendiconto bozza `sito/content/rendiconti/imbuto-dove-siamo.md` v0.1 (non elencato, non in sitemap; pubblicazione da decidere con Fabio). Verifiche `tools/verifiche/imbuto_strati.py` (strati, assi, soglia, gruppi, link PVL per strato; `--rigenera` sul server) e `tools/verifiche/zenodo_test.py`; esiti in `esiti/2026-11-06/{imbuto,zenodo}/`. R48 (censimento AgID) nuova.
- **Numeri dal 2024 (imbuto-0.3.1):** 3.745.883 CIG; S1 escluso certo 3.216.533 (85,9 %); incluso certo cloud 4.537 CIG/1,21 mld + in-house 894/0,72 mld (asse B: extra-UE 45 %, IT 41 %, UE 14 %); incerto con marchio/lotto 3.515/6,51 mld; residuo S6 55.946/12,50 mld (G1 209/4,88; G2 884/4,08 di cui PSN 864/4,07; G3 12.615/2,94; G4 42.238/0,61). Link PVL: S3 0,1 %, G2 19,6 %, G3 73,1 %.
- **#59:** Zenodo fuori (+245 CIG S6, 0,44 %, stessa fonte ANAC); EuroTender non testato (installazione del pacchetto negata dal permesso), fuori per ora; clone in `lavoro/eurotender/repo`.
- **#60:** ricerca fatta (§7 del rendiconto), nessun contatto. **Prossimo:** top-5 del rendiconto §8 (primo: precisione di S1 su campione casuale).

## ANAC (macro-obiettivo §8quater) — punto di ripresa 6/11/2026
- **Chiusi:** #31 (riconfermato), #32, #33, #18, #16, #47. **Aperti in attesa di Fabio:** #34 documento, #35 presentazione, #36 sito.
- **Registro:** 18 problemi, **17 pronti**; P17 controvalidato sull'anagrafica stazioni-appaltanti JSON (`tools/verifiche/cf_segnaposto.py`: 1.282 segnaposto CFAVCP-); **P15 resta interno** (`motivo_interno` nel registro).
- **Pipeline da clone pulito** (server, `lavoro/clone-pulito-2026-11-06`): snapshot 349/349 identici, **335 numeri uguali, 0 diversi** (i 3 «MANCA cloud/*» sono di `misura_cloud.sh`, #48).
- **PDF per ANAC** con typst: `python tools/documento_anac/genera.py` → `sito/static/pdf/anac-problemi-e-rimedi-2026-10.pdf` (11 pagine). Presentazione: `node tools/presentazione/build.js`. Bozze, NESSUN INVIO.
- **Cruscotto:** `/enti/anac-cruscotto/` da `tools/cruscotto_anac.py` (sul server, dopo le metriche). Cron `55 6 * * *` da aggiungere (non aggiunto: permessi).
- **Build:** errore da `sito/content/rendiconti/imbuto-dove-siamo.md` non committato (altro lavoro, `_build` → `build`).

## #62 DOCUMENTI MANCANTI PER FILE — punto di ripresa 6/11/2026
- **Fatto (6/11 sera, rapporto 0.10 bozza):** pagine ufficiali delle 7 iniziative Consip/PSN mai cercate tutte trovate (la ricerca del 5/11 per CIG padre dava pagine sbagliate; ora per ID Sigef/titolo su consip.it/imprese/bandi, CIG o ID verificati nell'HTML): consip-2556 PEC-REM 2, consip-2453 SaaS ITSM, cig-8898059E90 Sicurezza on premises (ID 2367), cig-B0DA5C472C Tecnologie Server 5 (ID 2714), cig-5133642F61 SPC Connettività, cig-91881762B3 Sanità digitale gestionali (ID 2366), psn = AT Presidenza del Consiglio (bando, disciplinare, allegati). 196 documenti linkati, **195 archiviati** (130 nuovi, 65 già presenti; 1 errore: zip «ID 2453 DOC RIPUBBLICATI NON UFF»); CSV `report/convenzioni/aggregatori/aggregatori-ricerca-consip-2026-11-06.csv` da `tools/convenzioni/zip_aggregatori/ricerca_consip_psn.py`; lavoro sul server in `lavoro/convenzioni/aggregatori/r1109/`. Schede acquistinretepa (8898059E90, 2556, 2453) aperte da anonimo: nessun «VAI AL CATALOGO», nessun login. Inventario: righe **782 → 757**, dietro_login **ignoto 234 → 155**, no 480 → 534, sì 68; nuova bozza accesso civico per la Presidenza (PSN, 31 istanze preparate, nessuna inviata). Residuo ignoto = le 15 iniziative senza pagina. `docs/` NON rigenerato.
- **Fatto (6/11 pomeriggio, rapporto 0.9 bozza):** (1) «Allegato 6 WebRT18» di cig-94252656BA riscaricato da START (allegato 690934, `lavoro/convenzioni/aggregatori/start_dl_uno.py`), sha256 7c7b3567… verificato, archiviato; CSV 7/11 «scaricato-perso» → «archiviato»; corretto `archivia.py --da-file` (perdeva `--url`) e pausa configurabile `ARCHIVIA_PAUSA_S`. (2) 17 iniziative senza pagina: **2 trovate** su Azienda Zero via API jsonws pubblica (cig-949554539F GIP 2^ ed., CIG nel disciplinare e nella delibera di aggiudicazione 641/2023; cig-B736423C63 = CIG master Arsenàl.IT, citato nel DDG 370/2026), 25 documenti archiviati; 15 negative con vie provate (web, TED, PVL, portali) in `report/convenzioni/aggregatori/aggregatori-ricerca-2026-11-06.csv` (`tools/convenzioni/zip_aggregatori/ricerca_senza_pagina.py`); 4 documenti collegati per oggetto archiviati (capitolato ECM Marche, comunicato ANAS SHM, decreto CR Toscana 266/2022, ATS Bergamo del. 643); blocchi CAPTCHA SUAM Marche e AT Provincia di Brescia in `blocchi-accesso.csv`. (3) dietro_login: **ignoto 308 → 234**, sì 36 → 68, no 444 → 480 (782 righe): 25 schede acquistinretepa aperte da anonimo (`r1108/cat_*`): 15 con «VAI AL CATALOGO» → login SPID/CNS [V] (listini/offerte sì), 10 AQ senza catalogo né login (no); transato = sì [R] (residuo vuoto da anonimo); file `report/convenzioni/database/dietro-login-verifiche.csv` letto da `documenti_mancanti.py`. Residuo ignoto: 15 iniziative senza pagina + 7 Consip/PSN senza pagina individuata (cig-8898059E90, 91881762B3, B0DA5C472C, 5133642F61, consip-2556, 2453, psn). Registro accesso civico: riga anac-incaricati-bdncp riparata (virgola non quotata). **Da provare con Fabio:** CAPTCHA SUAM e Brescia, filtro Jaggaer ANAS, login SAP PAT e HERA, catalogo acquistinretepa. `docs/` NON rigenerato (lavoro release).
- **Fatto:** inventario analitico `report/convenzioni/database/documenti-mancanti.csv` (886 righe, 86 iniziative; criticità 3: 431, 2: 167, 1: 288; [V] 272, [R] 614) da `tools/convenzioni/documenti_mancanti.py` (metodi numerazione / rimando / atteso; righe a mano in `documenti-mancanti-curati.yaml`). Ingressi nuovi: `rimandi.jsonl` (1.555 rimandi estratti pagina per pagina dai PDF archiviati, `tools/convenzioni/rimandi_documenti.py`, gira sul server in `lavoro/convenzioni`, cache `lavoro/rimandi-cache/`), `ricontrollo-pagine.json` (44 pagine consip.it riscaricate dal vivo il 6/11, tutte 200, nessun blocco: `blocchi-accesso.csv` vuoto). Verifica: `python tools/verifiche/convenzioni_mancanti.py`.
- **Allegato 12 della 2928:** pubblicato solo come facsimile vuoto; l'Appendice 3 al CT (Listino Open Source) rinvia ai prodotti «presentati … conformemente all'allegato 12»: manca l'Allegato 12 compilato da Converge (criticità 3, [V]).
- **Sito:** pagine per convenzione con sintesi, documenti presenti, mancanti, accesso civico, invito a contribuire (Telegram/issue), JSON-LD Dataset+BreadcrumbList, breadcrumb; indice con presenti/mancanti/FOIA; metodo `/progetto/metodo-convenzioni-trasparenza/`; rapporto **0.6 bozza** (§ 5bis). Nessuna release pubblica.
- **Accesso civico:** nuova bozza raggruppata `bozze/mancanti-consip-s-p-a.{md,json}` (41 iniziative, solo criticità 2-3 [V] o da numerazione/rimando, non coperte), NON inviata.
- **Aperti:** (1) copie scaricabili: ~4,3 GB di documenti archiviati, troppo per Pages: **decisione di Fabio** (server mxmap.it con nginx, release GitHub, o solo i file < 5 MB ≈ 0,9 GB); (2) giro assistito con Fabio per i 53 mancanti Consip probabilmente dietro login su acquistinretepa (offerte economiche/listini/flussi, 26 iniziative); (3) aggregatori: pagine non ricontrollate (righe [R], dietro_login «ignoto»); (4) criticità per regole sul titolo: rivedere a mano prima di inviare; (5) overflow orizzontale di 13 px su mobile in tutto il sito (`.row`), preesistente.

- **Fatto (7/11, rapporto 0.8 bozza):** inventario 797 → **788** righe (criticità 3: 415, 2: 133, 1: 240; [V] 403, [R] 385; dietro_login ignoto 308, no 444, sì 36). Zip del 7/11 letti (`report/convenzioni/aggregatori/zip-letti-2026-11-07.csv`, 111 file; listini Intercent-ER con prezzi offerti e marchi; nessuna offerta dell'aggiudicatario), strumenti spostati in `tools/convenzioni/zip_aggregatori/` (#47); 119/120 copie START/Sintel in `archivio/` (`tools/archivia.py --da-file`; perso «Allegato 6 WebRT18» di cig-94252656BA, da riscaricare). Ricerca fuori piattaforma (`report/convenzioni/fuori-piattaforma/`): 5 parziali (determine di adesione Min. Giustizia 2483, Comune di Trieste 2610, …), 411 non trovati; sezioni AT di 60 enti aderenti visitate (IndicePA CKAN), resa 1/20, 1/20, 0/20 → stop, 12 blocchi (403/428/perfdrive) in `blocchi-accesso.csv`, R46. Conclusione: i criticità 3 non sono pubblicati in rete; resta l'accesso civico (bozze preparate, NESSUN INVIO). `docs/` ricostruito con la versione committata di `pagine.py` e del metodo (sezione «Copie» lasciata all'agente delle release).
- **Fatto (6/11, revisione, rapporto 0.7 bozza):** inventario 886 → **797** righe; criticità 3: 431 → 415, 2: 167 → 139, 1: 288 → 243; [V] 272 → 412, [R] 614 → 385; dietro_login: ignoto 557 → 308, no 329 → 453, sì 0 → 36. 89 righe scartate con motivazione in `documenti-mancanti-scartati.csv`: 28 dalla revisione a mano delle 175 righe rimando/numerazione (`revisione-mancanti.yaml`, criteri R1-R7 nel metodo §«Revisione delle righe»), 61 «attesi» trovati dal vivo sulle piattaforme degli aggregatori (`report/convenzioni/aggregatori/aggregatori-2026-11-0{6,7}.csv`; ricontrollo del 7/11: 14 pagine trovate su 31, 17 non trovate; listini Intercent-ER archiviati). `tools/convenzioni/allegati_nei_contratti.py` (server, cache `lavoro/allegati-contratti-cache/` nella copia `lavoro/convenzioni/rev/tree`): offerte tecniche/economiche e corrispettivi **dentro gli AQ firmati dell'ID 2296** (L1 Accenture, L2 Deloitte e Intellera, es. Security Strategy 250 €/gg); in nessun altro contratto stipulato. Gare su delega (AGEA 1774, INAIL 2748): instradamento proposto in DECISIONI.md (procedura → Consip, esecuzione → ente), bozze rigenerate (29 preparate, NESSUN INVIO). Commit 1dc2884f.
- **Da fare dopo la revisione:** ricerca fuori piattaforma (AT degli enti aderenti, delibere di adesione con listini, albi) per i criticità 3 delle 17 iniziative senza pagina; estrarre e leggere gli zip archiviati nel giro del 7/11; portare in `archivio/` le copie START/Sintel (`lavoro/convenzioni/aggregatori/r0711/`); giro assistito con Fabio: login SAP PAT (cig-95643027B0), portale HERA, acquistinretepa (righe dietro_login «ignoto» delle schede con prezzi), NECA residuo; ricostruire `docs/` (non ricostruito: altre modifiche non committate di un agente parallelo).
- **Fatto (6/11):** 36 allegati «flussi dati» letti per intero (`report/convenzioni/database/flussi-dati-letti.yaml`, applicato da `leggi_flussi.py`, anche `--solo-letti`; testi sul server in `lavoro/convenzioni/flussi/`): 35 sono solo commissioni (fattura, ID ordine o appalto specifico, imponibile; nessun ente, prodotto, marchio, CIG); solo l'ID 2275 (monitoraggio «Erogato», v1.4 del 15/5/2019) ha sede/ente, prodotto, marchio, lotto e quantità. Quantità fatturata anche in 2213 (secondo tracciato, senza prodotto) e 2638 (kWh, non ICT). Correzioni alle parole chiave: lotto falso positivo in 16, marchio e ordine nel 2275, ordine nel 2174.

## #62 CONVENZIONI ICT — punto di ripresa 5/11/2026
- **Fatto:** sezione `/convenzioni/` (indice con filtro per tipo di soggetto + 86 mini-pagine) generata da `tools/convenzioni/pagine.py` dalla base dati `report/convenzioni/database/iniziative.json` (README, schema.json, PROGRESSO.md lì). 86 iniziative (82 attive, 4 storiche; 45 Consip, 1 PSN, 25 aggregatori regionali, 4 consorzi/unioni, 11 altro), 295 lotti. Criterio nel README (derivati ICT 2024-2025; quote per tipo). PRINCO 2928 archiviato (16 file, copertura 69 %). Pagine Consip trovate per 44 iniziative (1.503 documenti linkati). Raccomandazioni R37-R40. Verifica: `python tools/verifiche/convenzioni_copertura.py`.
- **Gira sul server (riavviato alle 16:40 del 5/11 dopo la correzione del manifest):** archiviazione dei 1.503 documenti Consip, ripartibile: `cd ~/analisi-spesa-ict/lavoro/convenzioni && nohup nice -n 15 ../../.venv/bin/python tools/convenzioni/archivia_documenti.py --max-mb 20000 > archivia-documenti.log 2>&1 &` (5 s fra richieste, ~2,5 h; idempotente, si rilancia uguale). Archivio = `~/analisi-spesa-ict/archivio` (symlink). Disco: 54 GB liberi al 5/11, guardia a 40 GB.
- **Al termine:** `scp` di `lavoro/convenzioni/report/convenzioni/database/archiviati.jsonl` nel clone, poi `base_dati.py`, `pagine.py`, `bash tools/costruisci_sito.sh`, verifica, commit (solo file della sezione).
- **Fatto (2° giro, 5/11):** carenze di trasparenza C1-C8 (`report/convenzioni/database/carenze.yaml`) in evidenza nell'indice e in ogni mini-pagina; 127 bozze di accesso civico generalizzato (NON inviate) in `report/convenzioni/accesso-civico/` con `analisi-dinieghi.md` e `registro.csv`, pagina `/convenzioni/accesso-civico/`; R08 e R37-R40 aggiornate, R41-R42 nuove; DECISIONI 5/11; atti PRINCO riletti (tetto ~62 M€ per Brand, art. 68 CAD, QC1, trasferimenti extra-UE con autorizzazione: ora V).
- **Fatto (3° giro, 5/11):** cruscotto `/convenzioni/griglia/` (dati `sito/static/dati/convenzioni-griglia.json` da `base_dati.py`; pagina da `tools/convenzioni/griglia_pagina.py`), link da indice e home; ricerca online complementare con documenti «fonte non ufficiale» in `curate.yaml` (`ufficiale: false`), mostrati nelle pagine senza cambiare la carenza.
- **Fatto (4° giro, 5/11):** job sul server finito (1.360 documenti nell'indice); estratti per parole chiave (`estrai_documenti.py`, sul server); open data Consip degli ordini come seconda misura (`consip_opendata.py`, `consip-ordinato.csv`); rapporto `sito/content/rendiconti/convenzioni-trasparenza.md` v0.1 (generato da `tools/convenzioni/rapporto.py VERSIONE DATA NOTA`, verifica `tools/verifiche/convenzioni_rapporto.py`, storico `report/convenzioni/rapporto/versioni.jsonl`), dopo revisione avversariale. **Bozza: da presentare a Fabio prima di ogni diffusione.**
- **Fatto (5° giro, 5/11):** fonti online prima dell'accesso civico: campione di 48 righe di enti aderenti (`report/convenzioni/enti-campione/`, formato riusabile dal monitor AT), centrali e aggregatori (`centrali-2026-11-05.csv`), ricerca web non ufficiale (`report/convenzioni/fonti-non-ufficiali/`, tutto [R]); AT di Consip consultata; allegato 4E «flussi dati» di EA8 letto; abbinamenti open data confermati per testo (V-testo); bozze ridotte a 19 (114 ritirate con motivo per istanza); R43-R44; rapporto v0.2 dopo revisione avversariale (12 punti); tabelle Markdown, `lastmod`/`datiAl` nel front matter.
- **Fatto (5/11, sera):** archivio locale copiato sul server in modo append-only: 89 blob (67 MB) con `tar --skip-old-files` verso `~/analisi-spesa-ict/archivio/blobs`, **sha256 verificati 89/89**; 119 righe del manifest locale aggiunte al manifest del server (copia del manifest precedente in `lavoro/convenzioni/sync/manifest-server-prima.jsonl`), 58 viste `mirror/` create come hardlink. Script: `lavoro/convenzioni/sync/unisci_manifest.py`.
- **Fatto (6/11, notte):** acquistinretepa con browser reale (Playwright + Chrome headless sul server): vetrina 663 iniziative via `publicservices/vetrineservices/getIniziative` (chiamate in `report/convenzioni/aretepa/chiamate.jsonl` con sha256, risposte in `lavoro/convenzioni/aretepa/risposte/`), schede pubbliche di 26 iniziative del censimento, 259 documenti `getDocument` archiviati sul server (indice 1.612); sezione «Massimale residuo» vuota per utente anonimo (resa forse incompleta, da riverificare); 36 allegati flussi dati analizzati (`flussi-dati.csv`, `leggi_flussi.py`); open data Consip 2026; siti AT e R44 in browser (`siti-browser-2026-11-05.csv`); `report/convenzioni/blocchi-accesso.csv` (32 righe) per le prove a mano di Fabio; rapporto v0.3 con consumato per convenzione, revisione avversariale 10 punti. Script: `tools/convenzioni/aretepa_browser.py`, `verifica_siti_browser.py`. Non serve cron: job brevi, ripartibili (saltano le schede già scritte).
- **Fatto (6/11, notte):** massimale residuo riprovato (attesa esplicita XHR + browser visibile con Xvfb all'01:00): 26/26 vuoti, `getDettaglioLotti` con payload null per utente anonimo (`report/convenzioni/aretepa/residuo-*.jsonl`); allegato 18 dell'ID 2275 letto per intero (flusso di monitoraggio «Erogato» mensile per ordine, lotto, sede, prodotto); piattaforme degli aggregatori (Intercent-ER, EmPULIA, Sintel/NECA, START) in `report/convenzioni/aggregatori/`; blob locali copiati sul server (147/147 sha256 OK); rapporto v0.4.
- **Fatto (6/11):** allegati di monitoraggio letti per intero: ID 2452 (All. B Telefonia mobile 9, flusso «Erogato» come l'ID 2275, versione non indicata) e ID 2648 (solo commissioni, non monitoraggio); rapporto v0.5 dopo revisione avversariale (10 punti: obbligo contrattuale con allegato e versione, nessuna generalizzazione ai 35 allegati non letti, residuo «causa non accertata», ID non formattati, date 5-6/11).
- **In attesa di Fabio:** invio delle 19 istanze e ripresa di acquistinretepa con browser reale (non avviare senza sua decisione).
- **Da fare:** acquistinretepa con browser reale (su decisione di Fabio) (schede in JS, listini; prima di inviare C1/C3); ripetere e documentare i blocchi AT (R44) prima di ogni rilievo; aggregatori regionali e consorzi via mappa piattaforme #57 (inventario oggi «da verificare»); controvalidare `config/tipi_soggetto.yaml` con l'elenco ANAC dei soggetti aggregatori (la pagina anticorruzione.it/-/soggetti-aggregatori non espone un file scaricabile: cercarlo fra i documenti ANAC); curare aggiudicatari/massimali/durata in `curate.yaml` partendo dai rendiconti; rileggere gli atti PRINCO archiviati per passare da R a V; ricostruire tutto `docs/` per il menu «Convenzioni» (le altre pagine di docs/ hanno modifiche non nostre, non committate).


## PUNTO DI RIPRESA 4/11/2026 (sessione principale; scritto prima di un possibile stop per i limiti dei token)
Per riprendere: leggi questa sezione, poi i ticket citati. Nulla gira in locale; i job lunghi sono sul server.
- **Fatto oggi:**
  - #57 chiuso nella sostanza: link PVL per il 65,1 % dei CIG, esiti in `esiti/pvl-link-cig/2026-11-04/`; P18 nel registro ANAC, presentazione e rendiconto rigenerati; R30 aggiornata.
  - #62 convenzioni (prima PRINCO 2928).
  - #63 accessibilità link per link: pagina del sito `/progetto/normativa-documenti-gara/`, generata da `report/metodo/accessibilita-documenti-normativa.md`, con giurisprudenza §6.
  - #64 specifica «Visibilità PA» 0.2 in `progetti/visibilita-pa/SPECIFICA.md`.
- **In corso:** monitor trasparenza beta (#61). Lo porta avanti un agente; il suo stato è nella sezione «Monitor trasparenza» qui sotto.
- **Prossimi passi:**
  - fare approvare a Fabio la specifica #64 (decisioni aperte nel §10);
  - #63: verificare gli estremi delle pronunce riferite e scaricare la delibera ANAC 968/2019;
  - #62: database delle convenzioni;
  - aggiungere il cron giornaliero PVL;
  - riallineare il server a origin quando finisce il censimento della trasparenza.
- **Regola:** nessun `git stash` sul clone locale mentre il monitor scrive file. Il 4/11 uno stash accidentale è stato ripristinato; backup in `scratchpad/bk-1793784376`.

## Aggiornamento 4/11/2026 — link ai documenti di gara (#57) e convenzioni (#62)
- **Il link ai documenti di gara è un ingresso obbligato dell'imbuto** (Fabio, 4/11). Sta solo nell'API PVL (`documenti_di_gara_link`), dal 1/1/2024. Non è in nessun dataset bulk.
- Statistiche sull'universo 2024-2026 (`esiti/pvl-link-cig/2026-11-04/`):
  - CIG: 3.734.845; il 69,9 % ha un avviso PVL, il 65,1 % ha il link (43,7 % dell'importo, che contiene anomalie);
  - **0 link per le adesioni a convenzioni e accordi quadro** (93.485 CIG, nessun avviso) e per gli in house (30.214 CIG);
  - gennaio-febbraio 2024: link nell'1,5-3,2 % dei CIG;
  - affidamenti diretti AD3: 96 %; bandi P1_16: 99 %;
  - 174.834 CIG PVL assenti da BDNCP;
  - 36.888 domini, 16 famiglie di piattaforme attribuite.

  Metodo in `report/metodo/acquisizione/dettaglio-cig.md`, pagina `sito/content/progetto/sistemi-documenti.md`. Per rifare tutto: `pvl_avvisi.py scarica` + `pvl_dopo.sh`. Manca il cron giornaliero.
- Il problema è nel registro ANAC come **P18** (gravità alta, pronto) e quindi nella presentazione e nel rendiconto «problemi e rimedi». **R30** è aggiornata con i numeri definitivi.
  - Obiettivo: con un dataset bulk cig -> link completo non servirebbero accessi civici per trovare gli atti.
  - R30 resta una proposta fino al sistema di invii massivi.
- **Accessibilità dei documenti di gara, link per link (#63)**, sotto-progetto a priorità medio-bassa (Fabio, 4/11). È una misura diversa dal monitor #61: un campione e poi il censimento dei 2,4 milioni di link PVL, con la tassonomia degli esiti (login, JS, errori, nessun documento…), una doppia via, open data e cruscotto, e una campagna di azione dedicata con PEC ed esposti ad ANAC preparati e inviati da Fabio. Primo campione su 400 domini: documenti visibili solo su 44.
- **Convenzioni (#62):** database delle principali convenzioni, documenti mancanti tramite accesso civico, una mini-sezione con l'analisi di ogni documento.
  - Prima convenzione: Consip **PRINCO** ID 2928 (CIG BAFCF54A81, 105 M€). Listini: Microsoft/Postel, Google/TIM, Open Source/Converge.
  - Tetto di ~62 M€ per marchio; requisito ACN QC1; trasferimenti fuori SEE ammessi.

## Aggiornamento 4/11/2026 — Monitor trasparenza 1.1.0-beta (#61) — verso la beta

**Aggiornamento 4/11, 15:00 UTC — beta completa pubblicata.** Fase 2 finita sul server (giro 2 di conferma su 3.459 enti, 12:52 UTC); pacchetto desktop b importato (3.213 tentativi); export finale con `--forza`. Numeri: 30.701 enti; violazioni art. 9: 5.546 (robots 4.592, WAF/anti-bot 759, noindex 195); accessibili 14.327; accesso negato a tutti 439; blocchi confermati in due giri 1.786. Il cron `riprendi-fase2.sh` non ha più nulla da fare (fase 2 finita) e si può togliere. Open data ~150 MB (prove 73 MB): da spostare in un repository dati per la stabile.

**Stato esatto (4/11, 11:30 UTC):**
- FATTO: giro 2026-11 (sonda 1.0.0) su 30.701 enti; diagnosi estesa giro 1 su 6.543 dubbi (max 25 per host); caratterizzazione di 300 enti; controllo falsi positivi (53 enti); **beta pubblicata** (commit 3e989b9: open data in `sito/static/dati/trasparenza/`, pagina `/progetto/trasparenza-accessibilita/`).
- IN CORSO sul server: `lavoro/trasparenza/fase2-dopo-giro.sh` (log `log/trasparenza-fase2-2026-11.log`) sta facendo la **diagnosi giro 2** (conferma), poi farà da solo `esporta --run 2026-11 --forza` e scriverà «fase 2 finita».
- IN CORSO sul portatile: diagnosi desktop dei WAF restanti (`lavoro/trasparenza-desktop-waf-b.log`, pacchetto `lavoro/trasparenza-fp/pacchetto-waf-b`).
- PROSSIMO PASSO: a «fase 2 finita» → (facoltativo) `tar czf` del pacchetto desktop, copia sul server, `TRASPARENZA_RADICE=$PWD .venv/bin/python lavoro/trasparenza/fase2-codice/censimento.py importa --pacchetto <dir>` ed `esporta --run 2026-11 --forza`; poi dal portatile: `rm -rf sito/static/dati/trasparenza; ssh mxmap.it@51.158.36.151 'cd ~/analisi-spesa-ict && tar czf - sito/static/dati/trasparenza esiti/2026-11-03/trasparenza' | tar xzf -`, `hugo --source sito --minify --cleanDestinationDir` (con il server di anteprima Hugo fermo), commit solo di `tools/trasparenza sito/content/progetto/trasparenza-accessibilita.md esiti/2026-11-03/trasparenza sito/static/dati/trasparenza docs/dati/trasparenza docs/progetto/trasparenza-accessibilita`, push.
- RIPRESA se il job sul server si ferma: rilanciare `nohup lavoro/trasparenza/fase2-dopo-giro.sh >> log/trasparenza-fase2-2026-11.log 2>&1 &` (ripartibile: salta ciò che è nel database, il sorvegliante esce con codice 3 sugli enti bloccati e il ciclo riparte); un cron ogni 30 minuti lo rilancia se non gira e non è finito (`lavoro/trasparenza/riprendi-fase2.sh`).
- Allineamento del server a origin: NON fatto. Il rebase si ferma su un conflitto in `esiti/pvl-link-cig/2026-11-04/verifica-link.csv` (file della sessione #57: commit locale del server contro origin). Va risolto da chi segue #57; i file PSN/PVL sono salvati in `lavoro/backup-psn/<data>/`.
- Da fare per la stabile: repository dati dedicato (l'open data pesa ~100 MB a giro, raddoppiato in docs/), desktop su tutti i dubbi, caratterizzazione su tutti, PEC da preparare dopo il giro 2 (`pec-prepara --giro 2026-11-03`).
- Codice 1.1.0-beta in `tools/trasparenza/` (commit 1eca969 e successivi): identità oneste, tassonomia, due giri di conferma, curl, origine desktop, schede, cambiamenti, catalogo con test, aggancio PVL (#57: `lavoro/pvl/*.csv`, non nostri).
- Sul server il giro 2026-11 gira ancora con il codice 1.0.0 (`tools/trasparenza/giro.sh`, non toccare). La fase 2 gira da una copia: `lavoro/trasparenza/fase2-codice/` con `TRASPARENZA_RADICE=$PWD`, stesso database.
  - diagnosi giro 1 sui dubbi già sondati: `log/trasparenza-diagnosi-2026-11-g1a.log` (`--solo-host-completati`); da rilanciare a sonda finita per gli host mancanti, poi giro 2 a ≥ 60 min (`--giro-conferma 2`), poi `caratterizza --campione 300`, poi `esporta --run 2026-11 --forza` (correzione documentata: aggiunta della diagnostica 1.1.0-beta sul giro pubblicato dalla 1.0.0).
  - desktop: `lavoro/trasparenza-desktop/` sul portatile (pilota2 in corso); per il giro: `elenco` sul server → `diagnosi --origine desktop` sul portatile → rsync del pacchetto → `importa`.
- A giro finito: backup `tools/psn_*.py` in `lavoro/backup-psn/`, spostarli, `git pull --rebase` (mai stash -u/clean); `lavoro/trasparenza/fase2-codice/` allora non serve più.
- Controllo dei falsi positivi FATTO (53 enti dal portatile): `report/metodo/trasparenza-falsi-positivi.md` (robots 15/15, noindex 8/8, WAF 13/30 → regole corrette).
- **Catena automatica sul server:** `lavoro/trasparenza/fase2-dopo-giro.sh` (log `log/trasparenza-fase2-2026-11.log`) aspetta la fine di `giro.sh`, poi diagnosi giro 1 (solo WAF, irraggiungibili, TLS), elenco per il desktop, caratterizzazione di 300 enti, giro 2 di conferma, `esporta --forza`. Se si interrompe: rilanciarlo (è ripartibile).
- Poi: dal portatile `diagnosi --origine desktop --elenco elenco-2026-11.json` (attenzione: Bitdefender intercetta HTTPS), `importa`, `esporta --forza`; copia dell'open data dal server, build Hugo, commit e push.

## Aggiornamento 3/11/2026 — Monitor «Amministrazione trasparente» (#61)

Modulo autonomo `tools/trasparenza/` (README, METODO 1.0.0, schema, test, EUPL-1.2). Fonte degli URL: registro ANAC L.190 art. 1 c. 32 (API `dati.anticorruzione.it/rest/legge190`, anni 2015-2023) + IndicePA (CKAN JSON) + anagrafica ANAC; 30.701 enti, 27.045 con URL L.190.

- **Giro completo 2026-11 in corso sul server** (lanciato 3/11 20:44 UTC): `tools/trasparenza/giro.sh 2026-11` → fonti, sonda (24 host in parallelo, 1 richiesta/host ogni 5 s), browser (Chromium headless sui bloccati), esporta. Log: `log/trasparenza-giro-2026-11.log`. Stima 8-12 h, collo di bottiglia avcp.trasparenza-pa.net (2.834 enti in serie).
- **Ripresa:** se si interrompe, rilanciare `nohup tools/trasparenza/giro.sh 2026-11 > log/trasparenza-giro-2026-11.log 2>&1 &`: riprende dagli enti mancanti (stato in `lavoro/trasparenza/stato.sqlite`).
- **Dopo il giro:** (il clone sul server è indietro e ha file non tracciati di altre sessioni — tools/psn_*.py — quindi non fare git pull lì finché non sono sistemati; pubblicare dal portatile: `rsync -a mxmap.it@51.158.36.151:analisi-spesa-ict/sito/static/dati/trasparenza/ sito/static/dati/trasparenza/` e `rsync -a ...:analisi-spesa-ict/esiti/<data>/trasparenza/ esiti/<data>/trasparenza/`). l'open data finisce in `sito/static/dati/trasparenza/giri/<data>/` + `ultimo/`, `indice.json`, `storico.json`, `invii.json`; aggregati in `esiti/<data>/trasparenza/`. Poi `hugo --source sito --minify --cleanDestinationDir`, commit, push. La pagina `/progetto/trasparenza-accessibilita/` legge i JSON (senza dati mostra «primo giro in corso»).
- **Pilota:** `lavoro/trasparenza/pilota/pilota2-2026-11-03/` (200 enti: 99 accessibili, 18 robots, 4 WAF, 29 sezione non individuata, 25 irraggiungibili, 22 URL non validi, 3 TLS).
- **PEC:** `censimento.py pec-prepara --run 2026-11 --giro <data>` → `lavoro/trasparenza/pec/<giro>/<cf>/`; invii registrati con `pec-registra` in `dati/trasparenza/invii.csv`. **Nessun invio fatto; li fa Fabio.**
- **Cron proposto (da attivare):** mensile, `0 1 2 * * cd ~/analisi-spesa-ict && tools/trasparenza/giro.sh >> log/trasparenza-giro-$(date +\%Y-\%m).log 2>&1`.
- **Fase 2 sospesa (3/11, priorità a #57):** requisiti futuri di Fabio elencati in `tools/trasparenza/README.md` §«Requisiti futuri» (progetto e repo autonomi con GitHub Pages, giri mensili o quotidiani con log dei cambiamenti, resilienza con backoff e conferma dei blocchi in momenti diversi, tassonomia dei blocchi per identità del client, due origini server/desktop, diagnostica estesa con log grezzi, doppio accesso ANAC/home, test di ricerca CIG, catalogo delle problematiche, mirror opzionale). Codice sperimentale già scritto (`diagnosi.py`, comandi `diagnosi/elenco/importa/caratterizza/indice-cig`), non usato nel giro. Lasciati in esecuzione sul pilota: diagnosi server (`log/trasparenza-diagnosi-pilota2.log`, copia del codice in `lavoro/trasparenza/fase2-codice/`), indice CIG (`log/trasparenza-indice-cig.log`), diagnosi desktop sul portatile (`lavoro/trasparenza-desktop.log`, pacchetto `lavoro/trasparenza-desktop/pacchetto-pilota2` da importare con `importa`).
- **Allineamento del server a origin solo a giro finito:** prima copiare `tools/psn_configuratore.py` e `tools/psn_documenti.py` in `lavoro/backup-psn/`, poi spostarli e `git pull --rebase`; mai `git stash -u` né `git clean`.

## Aggiornamento 29/10/2026 — via 6, classificazione con modello e fonti (#55) — PUNTO DI RIPRESA

Indicazione di Fabio (29/10): la classificazione va portata avanti **costi quel che costi**, con metodo scientifico, attendibilità, ripetibilità, basi dati; ogni ostacolo va registrato come raccomandazione di policy (`report/metodo/richieste-e-raccomandazioni.yaml`, nuove R16-R18).

- **Giro 1 (p1, Opus, 611 contratti):** `report/metodo/llm/esiti/`. Quasi solo dal testo: 404 alta / 161 media / 46 bassa, 204 disaccordi con regole v3.1, 0 atti dell'ente. Istruzioni `tools/llm/istruzioni.md`.
- **Giro 2 (p2, Haiku, 337 contratti in 68 pacchetti da 5):** `report/metodo/llm/giro2/`. Fatti g2-001..009 (45): 1 solo atto dell'ente, quasi tutto declassato. Causa: WebFetch non legge i PDF delle determine; siti degli enti 403/404/502. **Sospeso** fino allo strumento server di scaricamento + estrazione testo. Istruzioni `tools/llm/istruzioni-p2.md`.
- **Architettura proposta (da decidere):** `report/metodo/via6-architettura.md` — deterministico (regole, tabelle iniziative, scaricamento + pdftotext/tesseract con sha256) + modello solo per trovare l'URL e leggere il testo estratto + revisione umana sui dubbi e a campione.
- **Base di conoscenza iniziative:** `report/metodo/llm/conoscenza-iniziative.yaml` (21 voci, 15 controvalidate) e pagina in bozza `sito/content/progetto/iniziative-consip-cloud.md` (draft). In corso: SPC Cloud lotti 2-4 e Sistema Cloud Toscana (mandataria TIM o Accenture: fonti discordanti).
- **Errori delle regole dal giro 1, da trasformare in test (v3.2):** falsi positivi lessicali ("AWS" stazioni meteo, "Azure S DR" pacemaker, "lotto N" fuori AQ); "PSN" nel testo ≠ servizio PSN; rivenditore ≠ provider (TIM/Fastweb su Pure Storage, Oracle, Microsoft EA); committente ≠ fornitore (ARIA, Sogei, CINECA marcati in-house); Cloud Toscana non in-house; "Google Suite"/Workspace; consumo Azure in Enrollment; Oracle Fusion Cloud.
- **Server:** CLI `claude` autenticata per mxmap.it (login /login del 29/10). Annotazioni: servizio `tools/annotazioni/server.py` su 127.0.0.1:8790 (cron @reboot), API esposta da Caddy su https://annotazioni.51-158-36-151.sslip.io (il sito resta su GitHub Pages, DNS invariato). Trascrizione completa della sessione, fuori da git perché il repo è pubblico: `~/analisi-spesa-ict/lavoro/sessioni/2026-10-29-via6.jsonl`.
- **Aggiornamento 29/10 pomeriggio:** giro 2 su **Sonnet** (Haiku scartato, esiti in `giro2/esiti-haiku/`), passa da `tools/llm/claude_tetto.py` (tetto + attesa del reset del limite) e da `tools/llm/verifica_esiti.py` (R1-R4); guardiano cron `tools/llm/giro2_guardiano.sh` ogni 30 min lo rilancia finché i 68 pacchetti sono completi. Annotazioni volontari: https://annotazioni.51-158-36-151.sslip.io/ (servizio `tools/annotazioni/`, export orario in `dati/annotazioni/`, coda documenti da cercare). Acquisizione documenti a livelli L0-L7 (`sito/content/progetto/acquisizione-documenti.md`); pilota L2 TED in corso (`tools/acquisizione/ted_l2.py`, #57): solo 16/611 CIG del campione hanno data GUCE. Principio a imbuto in AGENTS.md. Ricerca di classificatori esistenti su GitHub in corso → `report/metodo/ricerca-classificatori-esistenti.md`.
- **Prossimi passi:** 1) `tools/llm/atti.py` (scarica nell'archivio, estrae testo, OCR); 2) runner server `claude -p` con Haiku, ripartibile, per i 59 pacchetti restanti; 3) regole v3.2 con i test sopra; 4) pagina di revisione con proposta del modello, confidenza e fonti.

## Aggiornamento 28/10/2026 — misura della spesa cloud v3

- **Rendiconto pubblico** `/rendiconti/cloud-metodo-2026-10/` (v1.0), per la revisione pubblica.
  Riproduzione: `tools/misura_cloud.sh` (test, attribuisci, rivenditori, pnrr, campione, misura,
  confronta). Il 28/10 sono stati riprodotti 1.449 numeri su 1.449.
- **Classificatore** `tools/analisi/classifica.py` (funzione pura). Regole in `config/`, 58 casi
  in `tests/casi_classifica.yaml`. Contratti 2022-2026; un CIG si conta una volta sola (ultima
  versione, il delta vince).
- **Pubblicati** `report/metodo/*-v3.*`:
  - riepilogo, rivenditori, PNRR, importi da verificare (84 contratti, 9,8 miliardi);
  - campione v3 di 611 contratti, con la copia cieca;
  - `fonti-v3.sha256`.
- **Registri:**
  - `report/metodo/REGISTRO-PROCEDIMENTI.md`, il racconto peritale del lavoro;
  - `report/metodo/richieste-e-raccomandazioni.yaml`, con R01-R15 per ANAC, Consip, PSN, DTD,
    ACN, Sogei. Va aggiornato sempre (AGENTS.md §3). Nulla è stato inviato.
- **Pagina di revisione** (privata, claude.ai): https://claude.ai/artifact/1wcRRvBGz6u2H5D8kbWPVq . Annotazione cieca
  A/B, verifica importi, decisioni R01-R15, lacune. Si ricostruisce con `node tools/revisione/costruisci.js`;
  le risposte stanno nel db della pagina (collezioni campione, importi, richieste) e si leggono con ArtifactData.
- **Prossimo:**
  1. Annotazione alla cieca del campione v3 da parte di due persone. **Serve sapere da Fabio chi
     la fa.**
  2. Verifica degli 84 importi da verificare.
  3. Via 4 (PSN) e catalogo ACN.
- **Ticket:** #48 metodo, #41 rivenditori, #43 PNRR, #52 in-house e datacenter (dopo), #53
  interfaccia di drilldown (dopo), #54 richieste ad ANAC, #22 proposta ad aborruso a fine lavoro.

## Aggiornamento 27/10/2026 (sera)

- **Mirror ANAC completo** (#9 chiuso): 1.793 risorse servite tutte archiviate; 4 rispondono 404 da ANAC.
- **Rendiconto ANAC 1.5**: mesi OCDS duplicati provati byte per byte (24 mesi in 8 gruppi su 96); OCDS vs tabellari (§3.5); controlli CIG su tutto il mirror (12.079.473 CIG); nuovo reperto CD-CSV.
- **Registro problemi** `report/anac/problemi.yaml`: 17 schede, 6 pronte per ANAC (P01 P02 P07 P08 P10 P12); le altre hanno il campo `manca` (quasi sempre la seconda via).
- **Contatti ANAC**: li ha Fabio, non cercarli (#51 chiuso).
- **Metodo cloud provider (#48)**: `tools/analisi/attribuisci_provider.py` (vie 1,2,3,5,7), dizionari in `config/`; campione di sviluppo e campione di misura in `report/metodo/`; prima misura v2 (non cieca): precisione provider 94,6%, provider+servizio 86,6%. Prossimo: regole v3 (sviluppo/sandbox, PSN omonimi, GCP clinico, SAP, in-house pubblico e telco IT), nuovo campione, annotazione umana cieca.
- **#50** `cig_accordo_quadro` vuoto nel 20% (2025) delle adesioni dichiarate: in validazione.
- **Server condiviso**: duckdb con memory_limit 6 GB e nice (il 27/10 un job ha reso il server irraggiungibile).

Prossimi passi ANAC: seconde vie per le 11 schede non pronte (#33), controlli su smartcig, poi documento, presentazione e sito (#34-#36) con la sezione «Come riprodurre tutto» (#47).

## Dove sta cosa

| Cosa | Dove |
|---|---|
| Repository | `mxmap-it/analisi-spesa-ict`, pubblico |
| Sito | https://analisi-spesa-ict.mxmap.it/ — sorgenti Hugo in `sito/`, build in `docs/`: `hugo --source sito --minify --cleanDestinationDir` |
| Server | `mxmap.it@51.158.36.151`, cartella `~/analisi-spesa-ict` (clone del repo, push con la deploy key `~/.ssh/id_ed25519_spesaict`, alias `github-spesaict`) |
| Archivio | `~/analisi-spesa-ict/archivio/` sul server, fuori da git: `blobs/` per contenuto, `mirror/` con i percorsi originali, `manifest.jsonl` |
| Clone locale | `C:\Users\admin\Claude\analisi-spesa-ict` |
| Decisioni | [DECISIONI.md](DECISIONI.md) |
| Analisi tecnica | [sito/content/progetto/analisi-tecnica.md](sito/content/progetto/analisi-tecnica.md) |
| Ticket | https://github.com/mxmap-it/analisi-spesa-ict/issues |

## In esecuzione sul server

- **Mirror completo di ANAC** (`tools/mirror_anac.py`, ticket #9): 1.797 risorse, tutti i formati,
  OCDS bulk incluso. Alle 18 del 26/10 era a 719 risorse e 13,1 GB. Si ferma da solo sotto i 40 GB
  liberi.
- **Sonda** ogni giorno alle 06:10 e **metriche di non ricorrenza ANAC** (I1-I9) alle 06:40, esiti in `stato/sonda/` e `stato/metriche/`. Al 26/10: 7 violate su 9; I6 rispettata solo perché l'archivio è nato oggi.
- **Guardiano** in cron ogni 15 minuti (`tools/guardiano.sh`): riavvia il mirror se muore e non ha
  finito.

Controllare con:

```
ssh mxmap.it@51.158.36.151 'cd ~/analisi-spesa-ict && tail -2 log/mirror-anac.log && .venv/bin/python tools/stato_mirror.py | head -9'
```

## Fatto

- Analisi di fonti e strumenti, con le strade scartate → analisi tecnica.
- Roadmap, perimetro delle fonti, attese verso le autorità, registro delle decisioni.
- Censimento ANAC completo: 70 dataset, 1.801 risorse, 128,9 GB reali.
- **Rapporto ANAC pubblicato** e versionato (1.1): https://analisi-spesa-ict.mxmap.it/rendiconti/anac-2026-10/
- Registry delle risorse e sonda; prima sonda su 125 risorse.
- Sito con il tema di osservatorio.mxmap.it.
- 31 ticket, i completati chiusi.

## Prossimo passo

1. **Chiudere ANAC**, macro-obiettivo del setup: criteri nella [roadmap](sito/content/progetto/roadmap.md#8quater-quando-anac-è-finito). Ogni problema con prova, controvalidazione indipendente, azione correttiva e metrica di non ricorrenza (#32, #33); poi documento, presentazione e sito (#34-#36). Prima: lasciar finire il mirror e **riverificare il rapporto su tutte le risorse** (#31) e
   misurare la deduplicazione dell'OCDS (#10).
2. Poi i dataset nell'ordine della [roadmap](sito/content/progetto/roadmap.md#8ter-i-dataset-in-ordine-prima-anac-poi-gli-altri):
   **Consip per primo**, perché cancella oltre i tre anni.

### Todo dalla settimana del 2/11/2026 — puntatori ai documenti prima e dopo il 2024 (#57)

Piano in `report/metodo/acquisizione/prima-e-dopo-2024.md`.
- [ ] Verificare sulle delibere ANAC 261, 263 e 264/2023 il quadro normativo (oggi R) e passarlo a V.
- [ ] Misurare sul mirror ANAC, per i CIG dal 2024 (tutto l'universo e il sottoinsieme cloud/IT):
  - presenza del puntatore ai documenti, per fonte, fase, procedura e piattaforma;
  - funzionamento, su un campione stratificato;
  - coerenza con il CIG e leggibilità;
  - completezza delle schede di esecuzione;
  - confronto con il 2022-2023;
  - costo per documento.
- [ ] Pubblicare il rendiconto, la differenza tra dovuto e pubblicato e le nuove raccomandazioni; mettere le verifiche in `tools/verifiche/`.
- [ ] Comporre il percorso multi-livello (dati strutturati, puntatori, scraping con identificazione, modello, annotazioni, FOIA) con la copertura e il costo misurati di ogni livello.

### Riproducibilità e riuso degli strumenti (Fabio, 3/11/2026)
- Ogni script dell'imbuto (`tools/analisi/imbuto.py`, `padri_ict.py`) deve entrare in `tools/verifiche/` e in `tools/misura_cloud.sh`: un comando da un clone pulito, stessi numeri dallo snapshot sha256.
- [ ] Inventario: per ogni funzione nostra (lettura CSV ANAC, deduplica delta, classificazione, archivio sha256, estrazione testo, crawler) quale strumento esistente la fa già (anac-pl-pp-cli di aborruso, source-observatory di DataCivicLab, anac-appalti-dbt, kingfisher/cardinal di OCP, `sito/content/progetto/strumenti.md`).
- [ ] Dove uno strumento esistente basta con una modifica, preparare la **patch da proporre upstream**, invece di tenere codice nostro. Nessuna PR su repo altrui senza l'ok di Fabio.

## Piano fino al 12/11/2026 — fattibilità dell'imbuto (Fabio, 2/11)

Obiettivo per il 12/11:
1. aver scalfito la superficie di ciò che è **facile** da escludere o includere, con numeri;
2. una **top-5** delle cose ancora da fare, e come farle, per arrivare alla completezza dei dati.

Lo stato di partenza al 2/11:
- giro 2 della via 6 completato (68/68 pacchetti), da verificare e confrontare; negli ultimi pacchetti atti=0, da capire;
- pilota TED L2 fallito (JSONDecodeError dall'API) prima di scrivere risultati.

| giorni | lavoro | esito |
|---|---|---|
| 2-3/11 | chiudere il giro 2: verifica_esiti, registro.js, confronto con il giro 1, perché atti=0; correggere e rilanciare il pilota TED | numeri della via 6 |
| 3-5/11 | **pipeline dettaglio-cig → pagina dell'ente → documenti**: link nei dataset?, copertura per anno e piattaforma, pilota sul campione | fattibilità L2-L3 misurata |
| 4-6/11 | **strati facili dell'imbuto sull'universo ANAC**: esclusione certa con più segnali, inclusione certa (convenzioni e lotti, marchi), distribuzione degli importi per proporre la soglia, conteggio del residuo per gruppo (mega, PSN-like, incerti) | dimensione di ogni strato, in numero e importo |
| 5-6/11 | test di Zenodo ed EuroTender (dentro o fuori) | rendiconto |
| 6-9/11 | puntatori ai documenti prima e dopo il 2024 (presenza, funzionamento, coerenza); censimento ICT AgID (questionari, disponibilità) | fattibilità L1 e fonte di controprova |
| 10-11/11 | rendiconto «Imbuto: dove siamo» + **top-5** con metodo, costo stimato e chi deve agire (noi, enti, AgID/ANAC/DTD) | consegna del 12/11 |

In parallelo, senza bloccare: annotazioni umane (la verità di riferimento serve per tutte le precisioni), CPV (#59, bassa priorità).

### Todo PRIORITARIO dalla ripresa — pipeline dettaglio-cig → link dell'ente → documenti (#57, Fabio 1/11/2026)

Esempio: https://dettaglio-cig.anticorruzione.it/cig/B320E66854 ha in fondo un link alla pagina di pubblicazione dell'ente, https://www.servizipubblicaamministrazione.it/servizi/saturnweb/Pubblicazioni.aspx?Tipo=26&CE=lnmtrn203, da cui dovrebbero scaricarsi altri documenti dell'acquisto. Pipeline da valutare, validare come fattibile e scomporre in tutti i passaggi:

**Esito 4/11/2026:** scaricamento PVL completo; link per il 65,1 % dei 3,73 M CIG 2024-2026 (69,9 % con avviso); mappa di 36.888 domini in `esiti/pvl-link-cig/2026-11-04/` e pagina `progetto/sistemi-documenti`; file per il monitor trasparenza in `lavoro/pvl/` (chiave `cf_ente`, formato in `dettaglio-cig.md`). Prossimo: attribuire le famiglie «ignote» più grandi (halleyweb, trasparenza-pa.net, albofornitori, spaggiari, madisoft), verifica con browser reale, pilota L3; capire i 174.834 CIG PVL assenti dai file BDNCP 2024+; aggiornamento giornaliero via cron. **Nota:** il clone sul server ha un commit locale (590a5d2) non pushato perché i file non tracciati di `tools/trasparenza/` (altra sessione) impediscono il pull --rebase.

**Esito 3/11/2026 (sera):** il link c'è in open data via **API PVL** (`pubblicitalegale.anticorruzione.it/api/v0/avvisi`, campo `documenti_di_gara_link`, senza CAPTCHA, dal 1/1/2024; verificato sul CIG d'esempio). dettaglio-cig usa un'API con CAPTCHA mosparo: non si usa in massa. Pre-2024: nessuna fonte aperta → R30. Scaricamento completo (2,75 M avvisi) in corso sul server: `log/pvl_avvisi.log`, stato `lavoro/pvl/stato.jsonl`, ripresa in `report/metodo/acquisizione/dettaglio-cig.md`. Prima misura (gen-feb 2024): 15 % dei CIG con link; bandi 70-95 %, affidamenti diretti AD3 0,3 %. Prossimo: copertura sull'universo e sul campione ICT, censimento domini, esito versionato, pilota L3.
- [ ] Il link c'è anche nei dataset che scarichiamo già (ANAC, BDNCP, OCDS)? Con quale campo? Se c'è solo nella pagina, vale la pena leggerla, rispettando robots e senza aggirare blocchi?
- [ ] Copertura: quota di CIG con il link, per anno (prima e dopo il 2024), per tipo di procedura, per ente e per piattaforma.
- [ ] Censire le piattaforme e i software di destinazione (es. SaturnWeb) e capire se un crawler per ogni famiglia copre molti enti.
- [ ] Scomporre i passaggi:
  1. CIG;
  2. link;
  3. pagina dell'ente;
  4. elenco dei documenti;
  5. identificazione dei documenti pertinenti;
  6. scaricamento con archivio sha256;
  7. estrazione del testo, con OCR se serve;
  8. interpretazione con regole o modello;
  9. classificazione con il livello registrato (`spesaict.atto/1`).
- [ ] Misurare per ogni passaggio successo, errori e costo. Fare un pilota sul campione di 611, poi decidere se adottarla.
- [ ] Documentarla in `acquisizione-documenti.md` (probabile livello L2-L3).

### Todo — censimento del patrimonio ICT della PA (AgID) (#60, 1/11/2026)

Fonte: https://padigitale2026.gov.it/guide-e-risorse/censimento-del-patrimonio-ict-della-pubblica-amministrazione
- [ ] Analizzare il censimento: chi lo compila, in quali anni, quali dati di spesa ICT, datacenter e cloud raccoglie.
- [ ] Verificare come sono fatti i questionari: domande, granularità, voci di spesa.
- [ ] Capire se i dati sono pubblicati (aggregati o per ente). Se non lo sono, stabilire come ottenerli:
  - accesso civico ad AgID per il dataset completo, oppure ai singoli enti per il questionario compilato;
  - a chi indirizzare la richiesta (ufficio e responsabile).

  Nessuna richiesta parte senza l'ok di Fabio.
- [ ] Inserirlo nella metodologia come fonte di controvalidazione della spesa misurata dagli appalti.

### Todo a bassa priorità — rapporto CPV (#59, 30/10/2026)

Esito atteso: **misura dell'attendibilità del CPV** sui contratti cloud e IT e **raccomandazione di policy per AgID, ANAC e ACN** (R21). Piano in `report/cpv/PIANO.md`, letteratura in `report/cpv/letteratura.md` (nessuna misura di correttezza esistente).
- [ ] Aprire il PDF della Corte dei conti europea 28/2023 (p. 37) e passare la cifra del 49,8% da R a V.
- [ ] Cercare il rapporto finale Ramboll/BME 2012 (450 documenti).
- [ ] Misurare il CPV dichiarato contro la classe vera sul campione, appena ci sono le annotazioni umane.
- [ ] **Dalla settimana del 2/11/2026 (ok di Fabio del 30/10):** scaricare sul server il dataset Zenodo 10007545 ed EuroTender e fare un **test di valutazione con rendiconto**: aiutano la metodologia o no? Possono anche non servire a niente. Criteri:
  - elenchi di esclusione certa ricavati da Zenodo: quanti contratti escludono in più e con quale precisione;
  - EuroTender come voto indipendente: quanto concorda con le nostre classi sul campione e se segnala errori veri.

  Si includono nella pipeline solo se il guadagno misurato giustifica la complessità; altrimenti si scartano, con il motivo scritto.
- [ ] Mappare le lacune del vocabolario, riclassificare, scrivere la proposta di policy, poi il rapporto.

## Bloccanti, che dipendono da Fabio

- ~~**Board di progetto**~~ creata: https://github.com/orgs/mxmap-it/projects/1
- **Tetto**: 20% del limite settimanale su 7 giorni, 2,86% al giorno (`config/budget.yaml`). Da tarare la conversione in token prima di avviare compiti automatici (#20).

## Vincoli da ricordare

- **ANAC respinge gli user-agent non-browser** rispondendo 200 con una pagina HTML: `archivia.py`
  lo riconosce e non lo salva come file. Il blocco degli IP cloud è riferito da altri, non verificato.
- **Il catalogo dichiara dimensioni 4,1 volte quelle vere**: per lo spazio contano gli `HEAD`.
- **I delta ANAC spariscono** senza regola; il file annuale dell'anno in corso non esiste.
- **Consip cancella oltre i tre anni**: il 2023 è già perso.
- **BDAP** in manutenzione straordinaria, segnalata con HTTP 200.
- Importi **SIOPE** in centesimi e mensili puri; join per codice fiscale.
- Sul server **non usare `/tmp`** per file di lavoro: è condiviso con altri progetti. E un `pkill -f`
  con un pattern presente nel proprio comando uccide la propria sessione: usare `tools/avvia.sh`.
- Distinguere sempre **verificato da noi** e **riferito da altri**.
