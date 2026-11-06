# Aggregatori regionali: convenzioni e AQ ICT (ticket #62)

Data della ricognizione: 5-6 novembre 2026. Elenco completo dei documenti: `aggregatori-2026-11-06.csv`. Blocchi di accesso: righe con data 2026-11-05/06 in `../blocchi-accesso.csv`.

Legenda: **V** = visto (letto da noi sulla pagina o nel documento); **R** = dedotto da noi, non scritto dalla fonte.

## Metodo

- Abbiamo consultato solo le parti pubbliche delle piattaforme: niente login, niente registrazione, niente CAPTCHA. Lo user-agent era dichiarato e fra due richieste allo stesso host passavano almeno 3 s.
- **Intercent-ER**: il sito è un Plone/Volto. L'elenco dei file viene dall'API JSON pubblica `++api++/<pagina>/@search`. I documenti di gara sono i link `DisplayAttach.ASP` di SATER che compaiono nella pagina del bando. File archiviati con `tools/archivia.py`.
- **EmPULIA**: è raggiungibile solo in `http://` (la 443 va in timeout, sia dal PC sia dal server). Pagine trovate con la ricerca SharePoint del sito (`_layouts/OSSSearchResults.aspx`). File archiviati con `tools/archivia.py`.
- **Sintel (ARIA)**: la procedura si trova con la ricerca pubblica `arcaSearch.xhtml` (codice gara), aperta con Chrome headless sul server. Gli allegati sono link JSF che scaricano in POST e non hanno un URL GET stabile. Li abbiamo scaricati senza login con il browser del server (`lavoro/convenzioni/aggregatori/sintel_ARIA_2023_807/`, sha256 nel CSV). Non sono in `archivio/`.
- **START (ESTAR)**: è una SPA Angular. La pagina della procedura l'abbiamo letta con Chrome headless e gli allegati li abbiamo scaricati con un click. Gli URL `documents-api/documents/?access-code=…` valgono una volta sola: un secondo GET risponde 404. Per questo i file stanno solo sul server (`lavoro/convenzioni/aggregatori/start_*`, sha256 nel CSV).
- Abbiamo archiviato anche le pagine HTML (bando, convenzione, schede), con `archivia()` e `accetta_html=True`, perché la CLI rifiuta l'HTML ("probabile blocco WAF").

## Esiti per iniziativa (sintesi)

| Iniziativa | Piattaforma | Trovato |
|---|---|---|
| cig-A008DB40BA | Intercent-ER | V convenzione "Sviluppo sistemi informativi 2": attiva dal 28/05/2024, scade il 28/05/2027, RTI Almaviva. Allegati (convenzione, listino, capitolato, CIG) e documenti di gara SATER (bando, disciplinare, capitolato, schema di convenzione, aggiudicazione) |
| cig-97219284C8 | Intercent-ER | V convenzione ITSM 2 + Sicurezza informatica 2: rinnovo di 24 mesi fino al 17/11/2028 e al 05/02/2029; det. 848/2026 "Lotto 1 – Estensione del quinto" |
| cig-9845010742 | Intercent-ER | V PC Desktop e Notebook 11, Team Memores: rinnovi; det. 511/2025 "Lotto 2 – Estensione del quinto" |
| cig-993049146A | EmPULIA | V pagina "Telemedicina": AS SDAPA in 3 lotti con importi, CIG e RTI; convenzioni firmate, capitolato, listini "Prodotti corrispettivi SLA" (7 revisioni) |
| cig-8637686BF8 | EmPULIA | V pagina AQ RUPAR-SPC: 30 M€, estendibili a 33 M€; 48 mesi dal 16/03/2022; 5 operatori; AQ firmato e zip della documentazione |
| cig-989984280E | Sintel | V ARIA_2023_807 è l'**AQ Infrastruttura Regionale di Telemedicina**, non un AQ ICT generico. 16 allegati pubblici, fra cui chiarimenti e comunicazione di aggiudicazione (det. 446 dell'08/05/2024) |
| cig-81636687F2 | START | V ESTAR, Area Vasta Sud Est, 11,3 M€: 10 documenti scaricati (bando, disciplinare, capitolati, bozza di convenzione) |
| cig-84163618CE | START | V ESTAR, Area Vasta Centro, 20 M€: 9 documenti elencati ma **non più scaricabili** (disponibili solo fino alla scadenza delle offerte, 17/10/2020) |

## Dati di consumo/erosione

- **Nessuna** delle quattro piattaforme pubblica l'erosione delle iniziative esaminate.
- Sintel/NECA (V): la scheda pubblica di una convenzione mostra MASSIMALE ed ESTENSIONE. Per il RESIDUO la nota dice che è "consultabile accedendo a NECA con le proprie credenziali", quindi sta dietro login.
- Intercent-ER (V): gli open data su dati.emilia-romagna.it contengono solo i listini degli ordinativi SATER, senza le quantità ordinate. R: le determine di "estensione del quinto" (ITSM 2 lotto 1, PC 11 lotto 2) indicano un massimale vicino all'esaurimento.
- START (V): la scheda di aggiudicazione è dietro login.

## Limiti

- In `archivio/manifest.jsonl` restano alcune righe con URL che finiscono in `\r`. Sono un errore del primo giro: il file di elenco aveva i fine riga CRLF. Gli URL Intercent-ER corrispondenti sono stati riarchiviati con l'URL corretto. Il manifest è append-only e non è stato corretto.
- Non abbiamo scaricato le determine di autorizzazione al subappalto di Intercent-ER (circa 120): sono elencate nel CSV come `pubblicato-non-archiviato`.
- Non abbiamo letto i chiarimenti START (scheda "Chiarimenti" della SPA) né i chiarimenti in testo di SATER, se non dentro la pagina archiviata.
- Le copie dei file Sintel e START stanno sul server, fuori da `archivio/`. Per portarle nell'archivio content-addressed serve un'estensione di `archivia.py` che accetti file locali.

## Ricontrollo del 7/11

Elenco dei documenti: `aggregatori-2026-11-07.csv` (239 righe, stesse colonne del file del 6/11). Riguarda le 31 iniziative non Consip di `../database/iniziative.json` che il 6/11 non erano state guardate. C'è una riga `(pagina)` per iniziativa, con `dietro_login=sì/no` nelle note. Script, log e copie dei file stanno sul server in `lavoro/convenzioni/aggregatori/r0711/`. Per ricostruire il CSV si lancia `costruisci_csv.py`.

### Metodo

- **Dal CIG alla procedura** (V): prima la ricerca full-text dell'API TED (`api.ted.europa.eu/v3/notices/search`, `FT~"<CIG>"`). Trova 16 CIG su 30. Poi la ricerca della piattaforma, se ne ha una pubblica:
  - START: `initiatives/list/?keyword=<CIG>`;
  - Intercent-ER: `++api++/@search` sul titolo, perché i CIG non sono indicizzati. Il CIG l'abbiamo poi verificato nel PDF «Importi e codici CIG» della convenzione;
  - CSI Piemonte: la pagina «Gare concluse» rimanda a Sintel;
  - ACP: `bandi-altoadige.it`.
  Come ultima strada, la ricerca web.
- **Scaricamento**:
  - Intercent-ER, ACP e avvisi CSI con `tools/archivia.py`, nell'archivio content-addressed;
  - START e Sintel con Chrome headless (`start_dl.py`, `sintel_dl.py`), perché gli URL degli allegati valgono una volta sola o sono POST JSF. I file sono in `r0711/<piattaforma>_<cig>_<id>/` con sha256 in `_scaricati.json` e nel CSV.
  Ritmo: almeno 5 s fra due richieste allo stesso host, al massimo 3 processi insieme. Niente login, registrazioni o CAPTCHA.
- Le determine di subappalto di Intercent-ER sono elencate ma non scaricate (`pubblicato-non-archiviato`).

### Esiti per iniziativa

| Iniziativa | Pagina | dietro_login | Note |
|---|---|---|---|
| cig-9936839AF1 | V Intercent-ER «SIL 3» | no | CIG nel PDF importi; listino |
| cig-9923894067 | V Intercent-ER «Business Analytics e Data Management 2» | no | 23,66 M€; listino, rinnovo det. 107/2026 |
| cig-9580558E8E | V Intercent-ER «Sanzioni amministrative 4» | no | listini.zip, rinnovi, revisione prezzi det. 62/2026 |
| cig-9482392D69 | V Intercent-ER «Applicativi in licenza d'uso AA.SS. – 2ª ed.» | no | listini completi, 3 determine di estensione del quinto |
| cig-9481064585 | R stessa pagina | no | il CIG non è nel riepilogo: attribuzione dedotta |
| cig-9016294130 | V Intercent-ER «Telefonia 4», lotto 1 | no | 6 listini e dettagli prezzi |
| cig-9216207E99 | V START 009511-2022 (ESTAR, conservazione a norma) | no | 7 documenti di gara |
| cig-9837572D38 | V START 012406-2023 (ESTAR, prescrizioni farmaceutiche) | no | 6 documenti di gara |
| cig-94252656BA | V START 020546-2022 (Regione Toscana, SaaS su SCT) | no | 39 documenti, contratto quadro compreso |
| cig-B1FFB3098A | V Sintel 184471406, CSI GA24_006 (fondi SIE) | no | R: CIG attribuito per oggetto; 13 allegati + avviso di aggiudicazione |
| cig-9769148BF3 | V Sintel 167850541, CSI GA23_006 | no | 19 allegati + 4 avvisi di aggiudicazione |
| cig-A02B1C8A8A | V Sintel 176835696, CSI GA23_011 | no | 11 allegati + avviso di aggiudicazione |
| cig-8664818204 | V bandi-altoadige 804135, ACP SF 009/2021 | no | V: il CIG è il **Lotto 1**, mentre iniziative.json scrive «Lotto 2»; bandi, rettifiche ed esiti archiviati; i decreti su acp.provincia.bz.it rispondono HTML |
| cig-B2FB115279 | V Consip ID 2748 (per INAIL) | no | fuori perimetro: la gara è Consip |
| cig-95643027B0 | V TED 731004-2022 → `acquistionline.pat.provincia.tn.it/nwbc` | **sì** | maschera SAP «Logon», registrata in `blocchi-accesso.csv` |
| cig-A0260B3155 | V TED 706023-2023 → portale fornitori HERA | sì (R) | l'elenco pubblico risponde HTTP 500; procedura negoziata |
| cig-9777818EA8 | TED 661555-2023 (esito) | ? | pagina della Provincia di Brescia non individuata |
| cig-7930885557, cig-7812108376, cig-759453695C | TED (2018-2019) | ? | la vecchia piattaforma `start.e.toscana.it` non risponde più; la ricerca START non le trova |
| cig-87332390D0, cig-8716552642, cig-B715929978, cig-9603457F68 | non trovata | ? | ESTAR, procedure negoziate senza bando: R, non sono tra i «Bandi e avvisi» pubblici di START |
| cig-7246653F38 | TED 426575-2017 (ARCA gara 7/2017/LI) | ? | la ricerca ARIA per CIG non dà risultati |
| cig-88556834CB, cig-945403654F, cig-99617296D3, cig-B736423C63, cig-949554539F, cig-7991036B82 | non trovata | ? | Masaf, ANAS, Marche, Azienda Zero (2), Trenitalia: nessun avviso TED e nessun risultato web utile |

### Cosa abbiamo trovato di criticità 3

- **Listini** (V, archiviati, sha256 nel CSV), tutti da Intercent-ER:
  - SIL 3 (`d10115c4…`);
  - BA&DM 2 (`be1afc72…`);
  - Sanzioni 4 (`059f7755…`);
  - Licenza d'uso 2 (`98944639…`);
  - Telefonia 4: listino lotti 1-2 `559dbc81…`, dettaglio prezzi `874898a5…`, servizi aggiuntivi `0bbc517a…`, riscatto `5c5fbbef…`, accessori `2855dbcd…`, lotto 3 `ff8b6ed3…`.
- **Progetti dei fabbisogni / allegati economici** (V, START 94252656BA): «Piano dei Fabbisogni Servizi SCT» (pdf `2a8c038e…`, xlsx `a2fe7c78…`) e «Dettaglio Economico.ods» (`926a8341…`). R: sono **modelli di gara**, non l'offerta né il piano di un ente aderente.
- **Offerte tecniche ed economiche degli aggiudicatari, elenco degli ordinativi, transato/erosione**: **non trovati** su nessuna piattaforma (V). L'unico indizio indiretto dell'erosione sono le determine di estensione del quinto e di rinnovo di Intercent-ER (R).

### Limiti

- Non abbiamo ancora cercato i documenti mancanti fuori dalle piattaforme: Amministrazione trasparente delle centrali e degli enti aderenti, delibere di adesione, albi pretori. Resta da fare per le 17 iniziative senza pagina e per le offerte e il transato di tutte.
- Abbiamo aperto solo il bando e l'esito TED. Non abbiamo esplorato i portali Brescia, SUAM Marche, Azienda Zero, ANAS e FS.
- Gli zip («Documentazione su Sintel.zip», «listini.zip», ecc.) sono archiviati ma non ancora estratti né letti.
- Come il 6/11, i file START e Sintel sono sul server fuori da `archivio/`.
