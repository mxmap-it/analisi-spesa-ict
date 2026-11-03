# PSN: dove sono pubblicati i "Progetti del piano dei fabbisogni"? Verifica a campione (#55)

Data: 2026-11-03. Fonte del campione: `lavoro/psn-top100.csv` (primi 100 contratti PSN 2024-2025 per importo, da ANAC).
Metodo: ricerca web (motore + siti degli enti), download con `tools/archivia.py` sul server, `pdftotext`, OCR
`tesseract` delle pagine-immagine e **lettura visiva** delle tabelle di riepilogo. Nessun contatto, nessuna FOIA.
Testi estratti e OCR: server `~/analisi-spesa-ict/lavoro/psn-txt/` e `lavoro/psn-ocr/`.

## Sintesi

- **Il documento giusto esiste e ha la struttura che serve.** Il *Progetto del piano dei fabbisogni* (PPdF), firmato
  dall'AD di PSN S.p.A., chiude sempre con il capitolo **"8 Configuratore"**: una tabella **"Riepilogo prezzi"** con
  una riga per famiglia (*Industry Standard, Hybrid Cloud on PSN Site, Secure Public Cloud, Public Cloud PSN Managed,
  Servizi di Migrazione, Servizi Professionali*; nelle versioni 2025 compaiono anche *Secure Public Cloud Azure
  Confidential* e *Secure Public Cloud OCI*), divise in **Totale UT** (una tantum) e **Totale canone annuale**, seguita
  dal dettaglio voce per voce. È esattamente il dato per la domanda di sovranità. **Verificato** su 5 PPdF.
- **Ma il Configuratore è un'immagine incollata nel PDF**: `pdftotext` non lo vede; serve OCR (tesseract legge male le
  celle colorate) o lettura visiva / un modello multimodale. Il resto del PPdF è PDF testuale.
- **Copertura del campione top-100: bassa.** Su 22 contratti del top-100 cercati, ho trovato un PPdF collegabile per
  **2** (Difesa, ARES Sardegna) e un atto contrattuale parziale per **1** (Ministero del Turismo, addendum al contratto
  di utenza). Per gli altri 19 la ricerca web non restituisce né la determina né gli allegati (non significa che non
  esistano negli albi: molti albi non sono indicizzati o sono a scadenza).
- **Valore coperto:** i contratti top-100 toccati valgono 151,3 M€ (Difesa 43,96 + ARES 36,63 + Turismo 46,20 + 24,67),
  ma il dettaglio per famiglia **letto** copre solo una parte piccola di quel valore (vedi tabella): Difesa 1,80 M€
  dell'estensione SPC; ARES il riepilogo della sola componente CRESSAN (3,23 M€ UT).
- **Ripartizione per famiglia (solo dove letta, 5 PPdF, valori IVA esclusa):**

| Ente / PPdF | Industry Standard (IT) | Secure Public Cloud (extra-UE) | PSN Managed (Oracle, extra-UE) | Hybrid | Migrazione (UT) | Servizi professionali (UT) |
|---|---|---|---|---|---|---|
| Difesa, 2023-…0589-PPdF-P1R2M1 (config. 2025-…-PdF-P2R1) | 0 | **1.700.232,77** canone (Azure; = 3 × 566.744,26: 1 anno + 2 lotti opzionali) | 0 | 0 | 0 | 98.353,40 |
| ARES Sardegna, 2023-0000003990570925-PPdF-P1R1 — solo scheda CRESSAN | 134.424,34 canone (OCR, da riverificare) | 0 | 58.531,59 canone (OCR) | 0 | 306.647,08 | 2.925.105,49 |
| ATS Brescia, 2025-0000003775430980-PdF-P1R1 | 134.445,96 (tot. infrastruttura) | 0 (anche Azure Confidential e OCI vuote) | 0 | 0 | 44.508,31 | 487.673,04 |
| AORN Santobono, 2025-…0630-PPdF-P9R1 | 0 | 0 | **31.825,96** canone | 0 | 0 | 3.088,60 |
| AORN Santobono, 2023-…0630-PPdF-P6R2 | 15.005,42 canone | 0 | 0 | 0 | 387.453,60 | 1.497.952,12 (somma UT 1.885.405,72 − migraz.; OCR) |

  Lettura qualitativa: nei PPdF sanitari letti la spesa è dominata da **servizi professionali e migrazione** (una
  tantum, pagati dal PNRR); il canone infrastrutturale è piccolo e va su Industry Standard (IT) o PSN Managed (Oracle
  Alloy). L'unico caso con big tech pubblica dichiarata è la **Difesa: Secure Public Cloud su Microsoft Azure**
  (verificato nel testo: "spazio Azure sul Secure Public Cloud del PSN"). Campione minuscolo: **non generalizzabile**.

## Tabella per contratto (campione top-100)

Legenda documento: D = determina/delibera/decreto; P = PPdF (progetto PSN); C = contratto di utenza/addendum.
"Non trovato" = nessun risultato con ricerca web mirata (nome ente + PSN/contratto di utenza/CUP/codice PdF); albo non esplorato a mano.

| CIG | Ente | Importo € | Documento trovato | URL | sha256 | Servizi per famiglia | Note |
|---|---|---|---|---|---|---|---|
| A06D509A47 | Stato Maggiore Difesa | 43.957.402,61 | P (estensione M1) + lettera di attivazione | difesa.it/assets/allegati/87186/1_annesso_progetto_piano.pdf ; …/87186/lettera_attivazione_servizi.pdf | 1aea8a9c7a626469b6653d79e6821d16febec1244280513844c1e15e8bc0916b ; 5538351b3c7038895f535140f07b4ef1f3d9827a2f46f58bea217a1f6d705bbc | SPC Azure 1.700.232,77 (canone, 3 anni) + prof. 98.353,40 | Collegamento al CIG per **CUP D81C23001300006** (identico nell'oggetto ANAC); il PPdF cita il contratto CIG A04AE447E0. La lettera di attivazione riporta un onere complessivo del contratto di 18.812.799,83 €. Configuratore = immagine (p. 26). PDF testuale. |
| B06937F577 | ARES Sardegna | 36.634.866,96 | P (214 pp., allegato 1 a delibera DG 40/2024) | aressardegna.it/wp-content/uploads/2024/02/PDELDG-40-allegato-1-2024.pdf | 524b568aebbf59b79d79faef32dcc02e6badfd868b54d2f155edfd66c9199231 | CRESSAN: v. sopra. Le altre ~9 schede (ASL1-8, AOU, AREUS…) hanno lo stesso riepilogo, **non lette** per tempo | Dettaglio per azienda sanitaria, inventario VM, tabelle figure professionali in testo. Collegamento al CIG per oggetto (Multimisura 1.1), non per codice. |
| A06E068C82 / A06E158293 | Ministero del Turismo | 46.200.181,44 / 24.671.472,75 | C (addendum 31/7/2025 al CdU CIG A02114987A) | ministeroturismo.gov.it/wp-content/uploads/2026/05/Addendum31lug25_2023-0000096480590585-CdU-P1R1M2_marcato.pdf | a73a20f731ffa47897cc1f6a5c811c0f6974a6706ab28dab7a9fd4ae637f079b | Solo integrazione servizi professionali (figure e quantità); famiglie infrastrutturali non indicate | Stesso codice amministrazione (…0096480590585) dei PPdF P2R1/P3R1 dei CIG top-100, ma i PPdF P2/P3 **non trovati**. |
| A06256ACEF | Presidenza Consiglio | 45.068.257,14 | non trovato | — | — | non indicato | |
| A05EAC57D2 | LazioCrea | 41.804.921,85 | non trovato | — | — | non indicato | |
| A05F245841, A04C7D8376 | Azienda Zero (Veneto) | 41.273.133,01 + 26.653.581,90 | non trovato | — | — | non indicato | sito azero.veneto.it indicizzato ma nessun atto PSN emerso |
| B84A909A09 | MAECI | 41.000.000,00 | non trovato | — | — | non indicato | |
| B4BFE36112 | MIT | 34.193.483,45 | non trovato | — | — | non indicato | |
| A0497FC4CA | CSM | 33.186.692,00 | non trovato | — | — | non indicato | |
| B2BD6503A1 | Consip | 32.232.794,67 | non trovato | — | — | non indicato | |
| A06DFA7D3D | Min. Interno – VVF | 29.713.973,25 | non trovato | — | — | non indicato | |
| B7E800BA01 | Roma Servizi per la Mobilità | 23.691.988,13 | non trovato | — | — | non indicato | |
| B918859AC7 | PCM – Protezione civile | 22.920.690,70 | non trovato (codice PPdF 2024-0000080188230587-PPDF-P2R4 nell'oggetto ANAC, zero risultati) | — | — | non indicato | |
| A04FA8DBB6 | Fondazione PTV Tor Vergata | 22.536.254,04 | non trovato | — | — | non indicato | |
| A04FC2E3D7 | ASL VCO | 20.000.000,00 | D riferita (revoca delib. 638/2023 + approvazione PPdF AIC n. 3) | aslvco.it/wp-content/uploads/2023/08/2583293.pdf | — (download in errore) | non indicato | esistenza riferita dal motore di ricerca, non letta |
| B201CBEA3B | Formez PA | 19.494.024,76 | non trovato | — | — | non indicato | |
| B0AE019439 | Fond. Pascale | 19.342.169,00 | non trovato | — | — | non indicato | |
| B2298FA3C4 | ASL Roma 1 | 18.716.105,79 | non trovato (CUP J81C23000670006 senza risultati) | — | — | non indicato | delibere ASL Roma 1 sono online in PDF, ricerca a mano possibile |
| A04FB9BA86 | ASL Roma 6 | 14.958.258,09 | non trovato | — | — | non indicato | |
| A06658648E | Regione Siciliana | 14.262.721,45 | non trovato | — | — | non indicato | |
| B5516CBC5E | Roma Capitale | 8.432.115,70 | non trovato | — | — | non indicato | |
| B0637C0F5E | ASP Reggio Calabria | 10.278.287,40 | non trovato | — | — | non indicato | |

### Documenti utili fuori dal top-100 (archiviati)

| Ente | Documento | URL | sha256 | Contenuto |
|---|---|---|---|---|
| AORN Santobono (NA) | P, P9R1 2025 | santobonopausilipon.it/wp-content/uploads/PSN_Progetto dei Fabbisogni_1.12 2025-…-PPdF-P9R1 AORN SANTOBONO-signed.pdf | 4234ec1150119c0d47dcc2f7a9d359806d117d04afa70dd1f8d9b5d4f5064ca7 | PSN Managed 31.825,96/anno; prof. 3.088,60 |
| AORN Santobono | P, P6R2 2023 (Smart Control Room) | santobonopausilipon.it/wp-content/uploads/2023-…-PPdF-P6R2-…pdf | 9f42ea10cd5e88b3045a5ff050636514f9fdd6aceec188c5da3bd3281dd1129f | IS 15.005,42/anno; migraz. 387.453,60; UT tot. 1.885.405,72 (OCR) — l'ente pubblica **tutti** i suoi PPdF (P1, P4, P6, P9) |
| ATS Brescia | D + P allegato A (decreto 172/2026, 43 pp.) | ats-brescia.it/…/Decreto%20172-2026.pdf | 332457d9cc0ec83de9b09b084f2ca4f0a31c2718187575511f89d0beb5f2b977 | IS 134.445,96; migraz. 44.508,31; prof. 487.673,04 (lettura visiva) |
| Comune di Firenze | D (DD 2933/2026, CIG derivato BB1DDD8915) | affidamenti.comune.fi.it/…/20260417-DD2933.pdf | 920aaa41fa7125348a1ac4dbecdc97636368b690b43ed7c44c62a61c83d25e57 | cita PPdF 2026-…0484-PPdF-P2R1 e Industry Standard; PPdF non allegato al PDF |
| ARERA | D (34/2025 DAGR) | arera.it/fileadmin/allegati/docs/25/34-25dagr.pdf | a5b662e2f14948a8ab4a5f1deab72f39e78895e058fbac0037b6e3fd820efeb2 | totale 230.683,16 € /10 anni, servizi di conservazione; famiglie non indicate |
| OGS | D (DFP 1045/2025) | ogs.it/sites/default/files/2025-03/DFP%201045.pdf | 4c48b4fa40c52283ea93f1a7381a7ab2de05d1286f21e46d7b1219d0a97ba08a | cita PPdF P1R2 "allegato"; allegato non nel PDF |
| Regione Sardegna (SIL) | Piano dei fabbisogni dell'ente (non il progetto) | files.regione.sardegna.it/…/psn-pianodeifabbisogni-sil-ras-signed-1-.pdf | 50d36c9c65b00ac247449a0a43b9de49746357f72747239b29312546fd00e4c8 | richiesta dell'ente, senza importi PSN |
| Regione Calabria | DCA 171/2023 | regione.calabria.it/wp-content/uploads/2023/06/dca-n.-171-del-27062023.pdf | 9858e7d316bd22579c0cd7a76f231acee15b00d334493739885f3483dc43238f | approva PPdF SIS per 35.763.258,44 € + IVA (riferito dal motore; famiglie non indicate nel decreto) |
| Difesa | atti a contrarre (ad 660/2024 e altro) | difesa.it/assets/allegati/55662/ad_660_04042024.pdf ; …/205/4b5bda55-…pdf | d78d1108b6bab5345bd67398025bc7f6d47e54b17d2653396baa8020258cba31 ; eafc5317faf01ed4f398a2b0fc8b45d828dd2b4e9d88db2bfb1d48dba528fa9c | nessuna famiglia di servizio |

Download falliti (errore HTTP dal server, non ritentati): Provincia di Benevento PPdF, Regione Abruzzo determina dpb012,
delibera ASL/Regione Puglia 455/2024 (sanita.puglia.it), ASL VCO 2583293.pdf, Abruzzo dpf01935 (404).

## Cosa si impara sulla pubblicazione

1. **Chi pubblica il PPdF:** soprattutto aziende sanitarie e regioni che lo approvano con atto proprio e lo allegano
   (ARES Sardegna, ATS Brescia, Santobono, Calabria, Abruzzo), più il caso della Difesa (annesso pubblicato nella
   sezione bandi). Formato: PDF nativo firmato digitalmente da PSN, testo estraibile, **Configuratore come immagine**.
2. **Chi omette:** la maggior parte dei grandi contratti (ministeri, PCM, in-house, Consip) non ha atti PSN indicizzati;
   diverse determine citano il PPdF "allegato" o "agli atti" ma il PDF pubblicato non lo contiene (OGS, Firenze, ARERA).
3. **Clausola di confidenzialità:** ogni PPdF reca in copertina "informazioni confidenziali di proprietà esclusiva della
   società PSN S.p.A. … non possono essere pubblicate". Probabile ragione delle omissioni; non impedisce l'accesso
   civico (eventuali limiti ex art. 5-bis d.lgs. 33/2013 da valutare caso per caso, ma i prezzi da listino di una
   concessione pubblica difficilmente sono segreto commerciale).
4. **Il collegamento CIG ANAC ↔ PPdF non è diretto:** i PPdF riportano il CIG della concessione (9066973ECE) e il codice
   PdF; il CIG derivato compare solo nelle determine. Chiave di aggancio utile: **CUP** e codice
   `AAAA-<codice fiscale ente>-PPdF-PxRy`.
5. **Raccolte/analisi esistenti:** non trovata alcuna raccolta pubblica dei PPdF né analisi per famiglia di servizio
   (Corte dei conti, AgID, DTD, stampa). Gli avvisi PA digitale 2026 (Misura 1.1) chiedono all'ente un piano di
   migrazione per servizio/rack, ma **non** risulta un open data con il dettaglio dei servizi PSN acquistati
   (verificato solo via motore di ricerca; da riverificare su padigitale2026.gov.it).

## Implicazioni

- **Scraping:** fattibile solo come integrazione (stima a campione: PPdF reperibile per ~10% dei grandi contratti).
  Dove c'è, l'estrazione si automatizza: individuare la pagina "Configuratore", ritagliare il "Riepilogo prezzi"
  e leggerlo con OCR robusto o modello multimodale (tesseract puro **non** basta), con verifica umana a campione.
- **Accesso civico / FOIA massivo: necessario.** Destinatario più efficiente: **PSN S.p.A.** (soggetto in controllo
  pubblico tramite concessione; tiene i configuratori di tutti gli enti) e il **Dipartimento per la trasformazione
  digitale** (concedente, riceve la rendicontazione PNRR e il monitoraggio della convenzione). In subordine i singoli
  enti (centinaia di richieste).
- **Formulazione proposta (da validare, non inviata):**
  > "Per ciascun Contratto di utenza stipulato in attuazione della Convenzione di concessione PSN (CIG 9066973ECE)
  > dal 2022 a oggi, chiedo copia della tabella 'Riepilogo prezzi' del Configuratore allegato all'ultima versione
  > approvata del Progetto del Piano dei Fabbisogni (codice PPdF), con: amministrazione utente e codice fiscale, codice
  > PPdF e versione, CIG derivato, importi 'Totale UT' e 'Totale canone annuale' per ciascuna famiglia di servizio
  > (Industry Standard, Hybrid Cloud on PSN Site, Secure Public Cloud distinto per cloud provider — Azure, Google Cloud,
  > AWS, Azure Confidential, OCI —, Public Cloud PSN Managed, Servizi di Migrazione, Servizi Professionali) e durata
  > contrattuale; in formato elettronico aperto (CSV/XLSX), anche come estrazione dai sistemi del Concessionario."

## Limiti

Ricerca limitata a ~2-3 ore e al motore di ricerca: "non trovato" ≠ "non pubblicato". ARES letto solo per la scheda
CRESSAN. Valori marcati OCR non riverificati a vista. Il legame CIG ANAC ↔ documento per Difesa e ARES è per CUP/oggetto,
non per CIG esplicito.
