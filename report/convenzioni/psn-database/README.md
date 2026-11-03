# Database dei documenti PSN pubblicati dagli enti (#55)

Versione 2 — 3/11/2026 (v1 stesso giorno). Database: [`documenti-psn.csv`](documenti-psn.csv) (una riga per documento).
Strumenti: `tools/psn_documenti.py` (archivia + estrae codici, CIG, CUP, tratti), `tools/psn_configuratore.py`
(OCR tesseract delle pagine "Configuratore"). Lavoro sul server in `lavoro/psn-db/` (estratti, testi, OCR; i 5 PDF
scaricati dalla rete del portatile, su autorizzazione di Fabio, in `lavoro/psn-db/locale/`).
Segue [psn-progetti-campione.md](../psn-progetti-campione.md); nessun contatto con enti, nessuna istanza.

**Registro revisioni.** v1: 41 documenti, 15 riepiloghi (molti da OCR). v2: +6 documenti (5 scaricati dal
portatile, PTV via Phoca dal server); tutti i riepiloghi letti **a vista**; ARES letto sul totale complessivo
(§8.14) invece della sola scheda CRESSAN; corretti sisma 2009 (UT 16,12 e non 18,12 M€) e Latina (famiglie lette);
Calabria 9370 riclassificato: il PPdF **non è pubblicato per la clausola di confidenzialità**; base 692 righe /
1.918 M€ (680 CIG distinti, 1.871,7 M€).

## Sintesi

- **51 righe**: 47 documenti scaricati e archiviati (sha256), 4 ancora non ottenibili (Benevento: DNS; Cardarelli:
  503; ULSS 9: connessione rifiutata; ASL BT e Abruzzo "Fascicolo edificio": 404, URL attuale non trovato).
  - **19 Progetti del Piano dei Fabbisogni (PPdF) pubblicati per intero, da 15 enti**: Difesa, ARES Sardegna,
    ASL Latina, AST Pesaro-Urbino, AORN Santobono (×5), ATS Brescia, ASL Roma 3, ESU Verona, ESU Padova, Comune di
    Trento, Provincia di Padova, ASL Biella, Policlinico Tor Vergata, USR Lazio, Commissario sisma 2009. **Tutti e 19
    i riepiloghi prezzi sono letti** (a vista o con somme coerenti). Altri 3 PPdF riferiti e non ottenuti
    (Benevento, Cardarelli, ULSS 9) → **18 enti** pubblicano il PPdF.
  - **18 determine/decreti** che citano il PPdF senza riportarlo (ASL VC, OGS, Firenze ×2, Calabria 5301 lo dichiarano
    "allegato" o "parte integrante"); **4 contratti di utenza**; **2 piani dei fabbisogni degli enti**.
  - **Controprova del diniego di fatto: Regione Calabria** (decreto 9370/2023, PPdF SIS da 35,8 M€) approva il PPdF
    "parte integrante e sostanziale del presente atto, ma riservato e non pubblicato, in quanto trattasi di documento
    che contiene informazioni 'confidenziali'" di PSN. È l'unico caso trovato in cui la clausola è invocata.
- **Clausola di confidenzialità**: presente in **18 dei 19 PPdF** pubblicati (nel 19°, ASL Latina, non rilevata nel
  testo). **Nessun PPdF è oscurato né ha omissis**. Il Configuratore è sempre un'immagine.
- **Copertura sui contratti PSN 2024-2025** (base: imbuto 0.3.1, sottoclasse `psn-servizio-da-determinare`, importo
  non "da verificare": 692 righe / 1.918 M€ = **680 CIG distinti, 1.871,7 M€**; top-100 = 1.420,0 M€):

  | collegamento al CIG | contratti | M€ | % valore | nel top-100 |
  |---|---|---|---|---|
  | PPdF con riepilogo prezzi (Difesa, ARES, Latina, Pesaro, Trento, Santobono P6, **ASL Biella**) | 7 | 98,9 | 5,3 % | 3 (6,5 %) |
  | + atti senza prezzi per famiglia (MIM, ANPAL, Mauriziano, ISIN, ASL VC, BEIC) | 13 | 128,7 | 6,9 % | 4 (8,0 %) |
  | + documenti riferiti non ottenuti (Cardarelli, ULSS 9, Padova P2R1 ×2, Benevento) | 18 | 135,0 | 7,2 % | 5 (8,3 %) |

  (ASL VCO esce: l'URL indicato dal motore era una delibera sulla logistica.) Per Difesa il PPdF letto è
  l'**estensione M1** (1,8 M€) di un contratto da 44 M€; ARES invece è ora letto per intero (20,2 M€ UT + 1,6 M€/anno
  su un CIG da 36,6 M€). Gli altri 12 PPdF riguardano contratti 2023 o 2026, o non sono collegabili a un CIG 2024-2025.
- **Ripartizione aggregata dei riepiloghi** (IVA esclusa). 16 PPdF hanno "Totale canone annuale"; 3 PPdF del
  template 2025-2026 (ATS Brescia, Provincia di Padova P3R1, PTV) riportano invece "Totale infrastruttura" per
  l'intera durata (es. 108 mesi) e sono tenuti a parte (Industry Standard 1,22 M€, nessun hyperscaler).
  - canone annuo **5,91 M€**: Industry Standard 3,41 (**59 %** dell'attribuito), **Secure Public Cloud 1,70 (29 %,
    tutto Azure, tutto Difesa)**, PSN Managed 0,68 (**12 %**, in ARES e Latina è Oracle Exadata "SQL instances BYOL"),
    Hybrid 0; 0,11 non attribuito (Santobono P1);
  - una tantum **74,6 M€**: servizi professionali 65,8 (**88 %**), migrazione 8,8 (12 %).
  - Lettura: negli enti che pubblicano (sanità, enti locali, commissari) la spesa PSN è soprattutto **servizi
    professionali una tantum**; il canone va per lo più su Industry Standard (IT); extra-UE: Azure (Difesa) e Oracle
    (PSN Managed, sanità). **Campione non rappresentativo** dei grandi contratti ministeriali, che non pubblicano.
- **Riferimento verificato**: il bilancio PSN 2024 (archiviato, sha256 `5be1ea22…`) dichiara **473 PA** che hanno
  scelto PSN al 31/12/2024 e un portafoglio ordini di ~2,6 miliardi. 18 enti su 473 (~3,8 %) pubblicano il PPdF.

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
| **Clausola di confidenzialità** in copertina | debole | tutto il PPdF | Una clausola contrattuale non è un limite di legge (art. 5-bis d.lgs. 33/2013 elenca i limiti in modo tassativo; v. Linee guida ANAC 1309/2016, §§ 2 e 5). 18 PPdF su 19 la riportano e **sono stati pubblicati integralmente da 15 enti**, inclusa la Difesa: la prassi delle stesse PA la smentisce. Rischio concreto: la Regione Calabria (decreto 9370/2023) ha invece omesso il PPdF proprio citando la clausola; la risposta è che lo stesso tipo di documento è in rete, senza omissis, per 15 enti. |
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

Allegato utile: le righe con tipo P di questo database (19 PPdF, 15 enti) (ente, URL, sha256) come prova della pubblicazione spontanea.

## Limiti

- Riepiloghi: 12 letti a vista sulla pagina renderizzata, 7 da OCR con somme coerenti (UT = migrazione + professionali); sisma 2009 letto a 130 dpi, da riconfermare a risoluzione maggiore. Le ~11 schede ARES per azienda non sono trascritte singolarmente (si usa il totale §8.14).
- 4 documenti trovati restano non ottenibili (Benevento, Cardarelli, ULSS 9, ASL BT; Abruzzo "Fascicolo edificio" e il suo allegato B non sono più online). 5 PDF sono stati scaricati dalla rete del portatile (autorizzazione di Fabio, 3/11): i siti filtrano il server estero.
- Il collegamento ai CIG è per CIG esplicito, CUP o ente+oggetto; per ente con più contratti PSN (es. ASL Latina)
  il legame è probabile, non certo.
- Base corretta il 3/11: 692 CIG / 1.918 M€ (tutti i contratti PSN dell'imbuto, non solo quelli con provider PSN attribuito). Le percentuali sul top-100 vanno ricalcolate sulla stessa base.
- Ricerca limitata al motore di ricerca: "non trovato" ≠ "non pubblicato".
