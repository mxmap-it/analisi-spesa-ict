# Database dei documenti PSN pubblicati dagli enti (#55)

Versione 1 — 3/11/2026. Database: [`documenti-psn.csv`](documenti-psn.csv) (una riga per documento).
Strumenti: `tools/psn_documenti.py` (archivia + estrae codici, CIG, CUP, tratti), `tools/psn_configuratore.py`
(OCR tesseract delle pagine "Configuratore"). Lavoro sul server in `lavoro/psn-db/` (estratti, testi, OCR).
Segue [psn-progetti-campione.md](../psn-progetti-campione.md); nessun contatto con enti, nessuna istanza.

## Sintesi

- **51 righe**: 41 documenti scaricati e archiviati (sha256) + 11 riferiti dal motore di ricerca ma non scaricabili
  dal server (timeout di connessione, 503, 404: probabile filtro sugli IP esteri; il download dal portatile è stato
  bloccato dalle regole di sessione e non è stato aggirato).
  - **17 Progetti del Piano dei Fabbisogni (PPdF) di PSN pubblicati per intero** (16 distinti), da **12 enti**
    (Difesa, ARES Sardegna, ASL Latina, AST Pesaro-Urbino, AORN Santobono ×5, ATS Brescia, ASL Roma 3, ESU Verona,
    Comune di Trento, USR Lazio, Commissario sisma 2009, Regione Calabria); altri **5 PPdF riferiti** (Provincia
    di Benevento, AORN Cardarelli, ULSS 9 Scaligera, Provincia di Padova, ESU Padova) → **17 enti** pubblicano il PPdF.
  - **17 determine/decreti** che citano il PPdF (di cui almeno 5 lo dichiarano "allegato" o "parte integrante" ma il
    PDF pubblicato non lo contiene: ASL VC, OGS, Firenze ×2, Calabria 5301), **4 contratti di utenza** (MEF-Consip,
    CONSOB, Difesa lettera, Turismo addendum), **2 piani dei fabbisogni degli enti** (Regione Sardegna, Mauriziano).
  - Enti distinti con almeno un documento archiviato: **30**.
- **Clausola di confidenzialità** ("informazioni confidenziali di proprietà esclusiva della società PSN S.p.A. …
  non possono essere pubblicate") **presente in 15 dei 16 PPdF distinti** (nel 16°, ASL Latina, non rilevata nel
  testo estratto). **Nessun PPdF è oscurato né ha omissis**: gli enti l'hanno pubblicato integralmente, prezzi
  inclusi, nonostante la clausola. Il Configuratore è sempre un'immagine (serve OCR).
- **Copertura sui contratti PSN 2024-2025** (base corretta: imbuto 0.3.1, sottoclasse `psn-servizio-da-determinare`,
  importo non "da verificare": **692 CIG, 1.918 M€**. La prima versione usava solo i CIG con provider PSN attribuito,
  586 CIG / 1.542,9 M€, e sovrastimava le percentuali; il numeratore non cambia):

  | collegamento al CIG | contratti | M€ | % valore | nel top-100 |
  |---|---|---|---|---|
  | PPdF con riepilogo prezzi (Difesa, ARES, Latina, Pesaro, Trento, Santobono P6) | 6 | 95,4 | 5,0 % | 3 (7,6 % del top-100) |
  | + determine/contratti senza prezzi per famiglia (MIM, ANPAL, Mauriziano, ISIN, ASL VC, BEIC) | 12 | 125,2 | 6,5 % | 4 (9,3 %) |
  | + documenti riferiti non scaricati (ASL VCO, Cardarelli, ULSS9, Padova ×2, Benevento) | 18 | 151,4 | 7,9 % | 6 (11,4 %) |

  Attenzione: per Difesa il PPdF letto è l'**estensione M1** (1,8 M€), non l'intero contratto (44 M€); per ARES
  è letta una scheda su ~10. Il **valore effettivamente ripartito per famiglia** è quindi molto minore del valore
  dei contratti collegati. Gli altri 10 PPdF letti riguardano contratti del 2023 o del 2026, o non sono collegabili
  a un CIG 2024-2025.
- **Ripartizione aggregata dei 15 riepiloghi letti** (IVA esclusa; OCR, varie righe "da riverificare"):
  - canone annuo **4,44 M€**: Industry Standard 2,21 (55 % dell'attribuito), **Secure Public Cloud 1,70 (42 %, tutto
    Azure, tutto Difesa)**, PSN Managed (Oracle) 0,13 (3 %), Hybrid 0; 0,40 non attribuibile per OCR;
  - una tantum **57,5 M€**: servizi professionali 47,0 (82 %), migrazione 5,8 (10 %), 4,6 non attribuibile (Latina).
  - Lettura: negli enti che pubblicano (sanità, enti locali, commissari) la spesa PSN è soprattutto **servizi
    professionali una tantum**; il canone infrastrutturale va su Industry Standard (IT). Big tech solo nella Difesa.
    **Campione non rappresentativo** dei grandi contratti ministeriali, che non pubblicano.
- **Riferimento verificato**: il bilancio PSN 2024 (archiviato, sha256 `5be1ea22…`) dichiara **473 PA** che hanno
  scelto PSN al 31/12/2024 e un portafoglio ordini di ~2,6 miliardi. 17 enti su 473 (~3,6 %) pubblicano il PPdF.

## Keyword e query (resa)

Stringhe distintive estratte dai PPdF letti: titolo «PROGETTO DEL PIANO DEI FABBISOGNI»; codice
`AAAA-<16 cifre con il codice fiscale dell'ente>-PPdF-PnRm[Mk]` (anche `PdF-`, `PPDF-`, `CdU-` per i contratti);
codice documento «PSN-SDE-CONV22-001»; capitolo «8 Configuratore»; tabella «RIEPILOGO PREZZI» con «Totale UT» e
«Totale Canone Annuale»; righe «Industry Standard», «Hybrid Cloud on PSN Site», «Secure Public Cloud», «Public
Cloud PSN Managed», «Servizi di Migrazione», «Servizi Professionali»; clausola «informazioni "confidenziali" di
proprietà esclusiva della società PSN S.p.A.»; nomi file «PSN_Progetto dei Fabbisogni_1.x», «Progetto_Piano_dei_
Fabbisogni-<ENTE>», «PSN_PianoDeiFabbisogni_<ENTE>»; CIG concessione 9066973ECE, CUP J51B21005710007 (presenti in
tutti i PPdF: chiave di ricerca robusta).

| query (WebSearch) | resa |
|---|---|
| "Progetto del Piano dei Fabbisogni" "Polo Strategico Nazionale" filetype:pdf | alta: 10 risultati, 7 nuovi (Latina, Calabria, BEIC, MEF, Padova, Cardarelli, ESU PD, Marche) |
| "PPdF" PSN … "Configuratore" "Riepilogo prezzi" | media: ULSS9, ESU VR, Padova |
| "informazioni confidenziali di proprietà esclusiva" PSN | alta: Trento, ASL Roma 3, ESU VR (la clausola è la stringa più selettiva) |
| "PSN-SDE-CONV22" | media: USR Lazio, sisma 2009, BUR Veneto |
| "PdF-P1R1" PSN determina | media: ISIN, ALER |
| "PPdF-P1R2" OR "PPdF-P2R1" OR "PPdF-P3R1" | bassa: Padova P3R1, PTV |
| "contratto di utenza" … determina | media: ASL Biella, CONSOB |
| "Polo Strategico Nazionale" "PPdF" determina CIG derivato | media: sisma 2016, ASL VC, ANPAL |
| codici PPdF presi dall'oggetto ANAC (ASL NA3, De Bellis, Portici, Preganziol, Acque Veronesi, Zetema, AOU Novara) | **nulla**: il motore non indicizza le cifre dei codici |
| per regione/tipologia (Lombardia, Emilia, Toscana, Puglia, Sicilia; università, comuni capoluogo, ministeri, camere di commercio) | quasi nulla oltre ai già noti; Puglia: delib. 455/2024 |
| Benevento, Abruzzo, Puglia, ASL VCO (download falliti) | URL riconfermati, ancora non scaricabili dal server |

Dopo ~25 query la ricerca satura: gli stessi ~30 documenti ritornano. Il "barile" raggiungibile col motore è
questo; il resto sta negli albi non indicizzati (L3-L4 di `acquisizione-documenti.md`).

## Chi pubblica e chi no

- **Pubblicano il PPdF integrale**: aziende sanitarie (Santobono pubblica tutti i suoi PPdF; ARES, ASL Latina, ASL
  Roma 3, AST Pesaro, ATS Brescia), enti locali (Trento, Provincia di Padova, Provincia di Benevento), enti regionali
  e commissari (Calabria, USR Lazio, sisma 2009, ESU Verona), un ministero (Difesa). Lo allegano all'atto di
  approvazione (delibera/decreto/determina) nell'albo o in "bandi di gara e contratti".
- **Pubblicano l'atto ma non il PPdF**: MIM, ANPAL, ISIN, BEIC, ALER, ARERA, INL, OGS, Firenze, ASL VC, Calabria
  5301 — spesso dichiarandolo "allegato" o "parte integrante".
- **Non pubblicano nulla di indicizzato**: la quasi totalità dei grandi contratti (PCM, MAECI se non per le
  liquidazioni, Turismo per i PPdF P2/P3, Interno, MIT, CSM, Consip, LazioCrea, Azienda Zero, RFI, INPS, Careggi).

## Analisi avversariale del diniego (accesso civico generalizzato)

Si ragiona come il legale di PSN o dell'ente che vuole negare. Le norme sono citate per contenuto; la
giurisprudenza è **riferita, da verificare** (non letta sulla fonte in questa sessione).

| motivo di diniego | forza | cosa colpirebbe | come lo neutralizzano i documenti già pubblicati |
|---|---|---|---|
| **Clausola di confidenzialità** in copertina | debole | tutto il PPdF | Una clausola contrattuale non è un limite di legge (art. 5-bis d.lgs. 33/2013 elenca i limiti in modo tassativo; v. Linee guida ANAC 1309/2016, §§ 2 e 5). 15 PPdF su 16 la riportano e **sono stati pubblicati integralmente da 12 enti**, inclusa la Difesa: la prassi delle stesse PA la smentisce. |
| **Interessi economici e commerciali / segreto commerciale** (art. 5-bis c. 2 lett. c; artt. 35-36 d.lgs. 36/2023 per l'accesso agli atti di gara) | media sul dettaglio, debole sul riepilogo | configurazioni voce per voce, dimensionamenti, figure professionali, giorni-uomo | I prezzi unitari sono quelli del **listino pubblico** della convenzione (PSN pubblica listino e catalogo); il riepilogo per famiglia è quantità × listino, **non contiene know-how**. 15 riepiloghi sono già in rete con cifre. Non c'è gara in corso: il PPdF è esecuzione di una concessione già aggiudicata (Ad. Plen. CdS 10/2020 sull'accesso civico in fase esecutiva: riferito, da verificare). |
| **Sicurezza nazionale / pubblica** (art. 5-bis c. 1 lett. a-b) | forte sulle architetture, nulla sui totali | schemi di rete, VDC, region, piani di sicurezza, inventari di VM, IP | La richiesta minimale **esclude** tutto questo. Anche qui: la Difesa ha pubblicato il proprio PPdF con l'indicazione del Secure Public Cloud Azure. |
| **Sicurezza informatica** (misure ACN, MTMS) | media sulle configurazioni | policy, cifratura, DR | Escluse dalla richiesta. PSN pubblica il proprio Manuale tecnico misure di sicurezza. |
| **Richiesta massiva / onere sproporzionato** (Linee guida ANAC § 4.2) | media se rivolta a PSN per centinaia di contratti | tutto | Chiedere un **estratto** di dati già strutturati nel configuratore (una riga per contratto) o procedere per lotti (prima i top-30, 45 % del valore). |
| **PSN non soggetto** (S.p.A. concessionaria; art. 2-bis c. 2-3 d.lgs. 33/2013) | media | richiesta a PSN | Rivolgere la richiesta all'**ente** (sempre soggetto) e/o al **DTD concedente**, che riceve i PPdF per la rendicontazione PNRR. |
| **Dati inesistenti in forma aggregata** | media verso DTD | tabella riassuntiva | Chiedere copia dei documenti (pagina "Riepilogo prezzi"), non un'elaborazione. |
| **Controinteressato PSN** (art. 5 c. 5: notifica e opposizione) | procedurale | ritardo | L'opposizione deve indicare il pregiudizio concreto; la pubblicazione spontanea di 17 enti rende difficile dimostrarlo per i soli totali per famiglia. |

### Richiesta minimale proposta (bozza, NON inviata; decisione di Fabio)

> Ai sensi dell'art. 5 c. 2 d.lgs. 33/2013 chiedo copia della **sola tabella "Riepilogo prezzi"** (capitolo
> "Configuratore") dell'ultima versione approvata del Progetto del Piano dei Fabbisogni relativo al contratto di
> utenza CIG ……, con le colonne "Totale UT" e "Totale canone annuale" per famiglia di servizio (Industry Standard,
> Hybrid Cloud on PSN Site, Secure Public Cloud distinto per cloud provider, Public Cloud PSN Managed, Servizi di
> Migrazione, Servizi Professionali), oltre a codice del PPdF e durata. **Non chiedo** architetture, configurazioni,
> inventari, indirizzi, piani di sicurezza né il dettaglio voce per voce. In subordine chiedo l'accesso parziale con
> oscuramento delle parti eventualmente sottratte. Documenti analoghi sono pubblicati integralmente da almeno 12
> amministrazioni (elenco e sha256 allegati).

Allegato utile: l'elenco D01-D19 di questo database (ente, URL, sha256) come prova della pubblicazione spontanea.

## Limiti

- Riepiloghi letti con OCR tesseract: le righe marcate "da riverificare" vanno lette a vista; le somme sono state
  controllate dove possibile (UT = migrazione + professionali).
- 11 documenti trovati non sono stati scaricati (filtri di rete dei siti verso il server estero).
- Il collegamento ai CIG è per CIG esplicito, CUP o ente+oggetto; per ente con più contratti PSN (es. ASL Latina)
  il legame è probabile, non certo.
- Base corretta il 3/11: 692 CIG / 1.918 M€ (tutti i contratti PSN dell'imbuto, non solo quelli con provider PSN attribuito). Le percentuali sul top-100 vanno ricalcolate sulla stessa base.
- Ricerca limitata al motore di ricerca: "non trovato" ≠ "non pubblicato".
