---
title: "Usi dei dataset (bozza)"
date: 2026-11-06
description: "A che cosa servono, con certezza e potenzialmente, i dataset del mirror per i progetti dell'Osservatorio Nazionale Sovranità Digitale."
build:
  list: never
---

**Bozza 0.1 del 6/11/2026, non elencata (#17, #9).** Tabella e schede sono generate da
[`config/usi-dataset.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/usi-dataset.yaml)
con `tools/pagine_mirror.py`: si aggiorna il file dati, non la pagina.

**Progetti:** ASI = analisi-spesa-ict (spesa ICT cloud per giurisdizione); MXM = mxmap.it (provider di
posta delle PA); PVL = Monitoraggio PVL e Amministrazione trasparente; ROB = osservatorio robots.txt
(#64); OSS = Osservatorio Nazionale Sovranità Digitale (rapporti di sintesi).

**Legenda:** **C** uso certo e diretto (script nel repository con uscita versionata, verificato il
6/11/2026); C·i certo ma indiretto (attraverso un altro progetto o un derivato); P potenziale diretto;
P·i potenziale indiretto (ipotesi motivate nelle schede); – nessuno.

## Sintesi

<!-- GEN:tabella -->
| Dataset | ASI | MXM | PVL | ROB | OSS | Conservazione |
|---|---|---|---|---|---|---|
| [anac/cig](#anac-cig) | **C** | P | C·i | – | C·i | alta |
| [anac/smartcig](#anac-smartcig) | **C** | P | P·i | – | P·i | alta |
| [anac/aggiudicatari](#anac-aggiudicatari) | **C** | P | – | – | C·i | alta |
| [anac/aggiudicazioni](#anac-aggiudicazioni) | **C** | – | – | – | P·i | alta |
| [anac/cup](#anac-cup) | **C** | – | – | – | C·i | media |
| [anac/stazioni-appaltanti](#anac-stazioni-appaltanti) | **C** | P | **C** | P | C·i | media |
| [anac/ocds](#anac-ocds) | **C** | – | – | – | P | alta |
| [anac/quadro-economico](#anac-quadro-economico) | **C** | – | – | – | P·i | media |
| [anac/stati-avanzamento](#anac-stati-avanzamento) | **C** | – | – | – | P·i | media |
| [anac/pubblicazioni](#anac-pubblicazioni) | **C** | – | P | – | – | media |
| [anac/fonti-finanziamento](#anac-fonti-finanziamento) | P | – | – | – | P·i | media |
| [anac/subappalti](#anac-subappalti) | P | – | – | – | P·i | media |
| [anac/partecipanti](#anac-partecipanti) | P·i | – | – | – | P | bassa |
| [anac/avvio-contratto](#anac-avvio-contratto) | P | – | – | – | – | bassa |
| [anac/fine-contratto](#anac-fine-contratto) | P | – | – | – | – | bassa |
| [anac/varianti](#anac-varianti) | P | – | – | – | – | bassa |
| [anac/minori](#anac-minori) | P·i | – | – | – | – | bassa |
| [consip/ordini](#consip-ordini) | **C** | – | – | – | C·i | alta |
| [consip/gare](#consip-gare) | P | – | P·i | – | – | alta |
| [consip/mepa-rdo](#consip-mepa-rdo) | P | – | – | – | P·i | media |
| [consip/anagrafiche](#consip-anagrafiche) | P | P·i | – | – | – | media |
| [rgs/siope](#rgs-siope) | P | P·i | – | – | P | alta |
| [agid_dtd/padigitale2026](#agid_dtd-padigitale2026) | **C** | P | C·i | – | C·i | media |
| [indicepa/enti](#indicepa-enti) | **C** | **C** | **C** | P | C·i | alta |
| [acn/catalogo-cloud](#acn-catalogo-cloud) | P | P·i | – | – | P | media |
<!-- /GEN:tabella -->

Lettura: i dataset ANAC dei CIG, degli aggiudicatari, del CUP e i file Consip degli ordini sono già il
motore dell'imbuto di ASI; IndicePA e l'anagrafe delle stazioni appaltanti sono la chiave di join comune
a tutti i progetti; SIOPE, subappalti e fonti di finanziamento sono il potenziale più alto non ancora
usato. Tutto ciò che ha conservazione **alta** è insieme usato e a rischio alla fonte.

## Schede

<!-- GEN:schede -->
### anac/cig

CIG (file annuali cig-AAAA e delta mensili). Campi chiave: `cig`, `cig_accordo_quadro`, `oggetto_gara`, `oggetto_lotto`, `cod_cpv`, `importo_lotto`, `cf_amministrazione_appaltante`, `denominazione_amministrazione_appaltante`, `data_pubblicazione`, `tipo_scelta_contraente`.

- **Uso certo:** Universo dell'imbuto: tools/analisi/imbuto.py e attribuisci_provider.py leggono cig-AAAA e i delta; producono gli strati S1-S6 (cloud certo ~594 M€ 2024-2025, residuo incerto ~6,4 mld, /progetto/imbuto/). Verifiche: cig_accordo_quadro.py (P15), attuativi_s5.py, ted_cig.py; acquisizione/pvl_analisi.py misura il link PVL su 3.734.845 CIG 2024-2026 (P18).
- **Potenziale, Monitoraggio PVL e Amministrazione trasparente:** universo dei CIG contro cui misurare il link PVL (oggi via file di lavoro di ASI): diventa uso diretto quando PVL legge il mirror
- **Potenziale, Osservatorio Nazionale Sovranità Digitale:** serie annuale della spesa ICT per giurisdizione, indicatore di testata
- **Potenziale, mxmap.it:** contratti di posta/collaboration (M365, Google Workspace) per ente: seconda via, indipendente dai record MX, per il provider di posta
- **Limiti noti:** P08 delta gennaio-marzo 2026 rimossi; P15 cig_accordo_quadro vuoto in parte degli attuativi; P16 righe CSV non conformi nei delta 2026; R22 importi pari al massimale dell'accordo quadro.
- **Conservazione: alta.** I delta sono rimossi senza regola (P08): senza mirror lo stato 2026 non è ricostruibile.

### anac/smartcig

SmartCIG (affidamenti semplificati, annuali e delta). Campi chiave: `cig`, `oggetto`, `importo`, `cf_amministrazione_appaltante`, `tipo_fattispecie_contrattuale`, `tipo_scelta_contraente`, `data_pubblicazione`.

- **Uso certo:** tools/analisi/smartcig_profilo.py: profilo per fattispecie 2022-2025; metriche_anac.py I5 (mesi mancanti, P09).
- **Potenziale, analisi-spesa-ict:** la spesa ICT corrente sotto soglia (licenze, canoni SaaS) passa in gran parte qui: va portata nell'imbuto
- **Potenziale, mxmap.it:** piccoli affidamenti di caselle/PEC per i comuni
- **Potenziale, Osservatorio Nazionale Sovranità Digitale:** quota del sotto soglia nella spesa cloud
- **Limiti noti:** P09 giugno e luglio 2026 mancanti, JSON interrotto.
- **Conservazione: alta.** Mesi già mancanti alla fonte; 38,7 GB, la parte più pesante dopo l'OCDS.

### anac/aggiudicatari

Aggiudicatari. Campi chiave: `cig`, `codice_fiscale`, `denominazione`, `ruolo`, `tipo_soggetto`.

- **Uso certo:** Lente fornitore e canale diretto/rivenditore: classifica.py, attribuisci_provider.py, imbuto.py, rivenditori.py, pnrr_cloud.py; controprova di ted_cig.py.
- **Potenziale, mxmap.it:** fornitore del servizio di posta per ente (contratto) da confrontare con il provider misurato
- **Potenziale, Osservatorio Nazionale Sovranità Digitale:** concentrazione dei fornitori ICT e loro giurisdizione
- **Limiti noti:** file full fermo al 23/01/2026: lo stato corrente richiede i delta.
- **Conservazione: alta.** Full non aggiornato e delta mensili soggetti alla stessa rimozione di P08.

### anac/aggiudicazioni

Aggiudicazioni. Campi chiave: `cig`, `data_aggiudicazione_definitiva`, `importo_aggiudicazione`, `ribasso`, `numero_offerte`.

- **Uso certo:** verifiche/verifica_38_42.py (copertura OCDS, P05: 67% a marzo 2026), seconde_vie.py, imbuto_tetti.py (tetti d'importo).
- **Potenziale, analisi-spesa-ict:** importo aggiudicato come valore alternativo all'importo del lotto
- **Potenziale, Osservatorio Nazionale Sovranità Digitale:** ribassi e concorrenza nelle gare cloud
- **Limiti noti:** file full fermo al 15/01/2026.
- **Conservazione: alta.** Come aggiudicatari: full fermo, stato corrente solo nei delta.

### anac/cup

CUP (ponte CIG-CUP). Campi chiave: `cig`, `cup`.

- **Uso certo:** analisi/pnrr_cloud.py e verifiche/pnrr11_cup_cig.py: catena candidatura PNRR (PA Digitale 2026) → CUP → CIG per le misure 1.1 e 1.2.
- **Potenziale, Osservatorio Nazionale Sovranità Digitale:** quota PNRR della spesa cloud e dove è finita
- **Limiti noti:** P14 'ND' al posto del CUP in 1.951.844 righe.
- **Conservazione: media.** Usato, ma file unico rigenerato: conservarne le versioni misura i miglioramenti di P14.

### anac/stazioni-appaltanti

Stazioni appaltanti (anagrafe, AUSA). Campi chiave: `codice_fiscale`, `denominazione`, `codice_ausa`, `natura_giuridica`, `comune`, `provincia`.

- **Uso certo:** trasparenza/fonti.py (censimento enti del monitor AT: natura giuridica e comune per chi non è in IndicePA); pvl_analisi.py; verifiche/cf_segnaposto.py (P17).
- **Potenziale, mxmap.it:** aggancio CF ente → dominio per gli enti non in IndicePA (partecipate)
- **Potenziale, Osservatorio robots.txt (#64):** elenco degli enti e dei loro siti da sondare
- **Potenziale, Osservatorio Nazionale Sovranità Digitale:** denominatore comune degli enti fra progetti
- **Limiti noti:** P17 codici fiscali segnaposto (902 su 39.486).
- **Conservazione: media.** Piccolo (10 MB) e chiave di join fra progetti: costa niente tenerne tutte le versioni.

### anac/ocds

OCDS bulk mensile 2018-2026. Campi chiave: `ocid`, `tender.id (CIG)`, `parties`, `awards.suppliers`, `release.date`, `value`.

- **Uso certo:** verifiche/ocds_mesi_duplicati.py (P01: 96 mesi, 80 contenuti distinti), ocds_periodo.py (P02), verifica_38_42.py (P03-P05), metriche I1-I4 del cruscotto.
- **Potenziale, Osservatorio Nazionale Sovranità Digitale:** formato standard internazionale: confronti con altri paesi UE nell'osservatorio
- **Potenziale, analisi-spesa-ict:** non fonte primaria (deciso), resta seconda via
- **Limiti noti:** P01 mesi duplicati; P02 fermo a marzo 2026; P03 fornitore assente nell'80% degli award 2026; P04 date non conformi; P05 copertura parziale; P06 API REST non funzionante; P07 licenza incoerente.
- **Conservazione: alta.** 74 GB; mesi già spariti (2025/12, 2026/01-02 in 404): è la prova di P01-P02 e l'unica copia di quei mesi in forma OCDS.

### anac/quadro-economico

Quadro economico. Campi chiave: `cig`, `tipo_evento`, `importo_base_asta`, `importo_consuntivo`.

- **Uso certo:** verifiche/imbuto_qe_sal.py: seconda fonte d'importo per gli incerti dell'imbuto (esiti/2026-11-06/imbuto/anac-qe-sal.csv).
- **Potenziale, Osservatorio Nazionale Sovranità Digitale:** scostamento fra importo bandito e consuntivo nei contratti cloud
- **Limiti noti:** copertura parziale: riguarda soprattutto i lavori.
- **Conservazione: media.** Unico proxy pubblico del liquidato insieme agli stati di avanzamento.

### anac/stati-avanzamento

Stati di avanzamento (SAL). Campi chiave: `cig`, `data`, `importo_sal`.

- **Uso certo:** verifiche/imbuto_qe_sal.py (somma dei SAL per CIG).
- **Potenziale, analisi-spesa-ict:** spesa effettiva (non solo bandita) per i contratti pluriennali PSN
- **Limiti noti:** poco compilato per servizi e forniture.
- **Conservazione: media.** Proxy del liquidato; full+delta come gli altri.

### anac/pubblicazioni

Pubblicazioni (avvisi e bandi). Campi chiave: `cig`, `data_pubblicazione`, `tipo_pubblicazione`.

- **Uso certo:** Solo censimento e controlli (censisci_anac.py); acquisizione/ted_l2.py lo usa per le date di pubblicazione.
- **Potenziale, Monitoraggio PVL e Amministrazione trasparente:** data di pubblicazione attesa da confrontare con l'avviso PVL e con la sezione AT
- **Conservazione: media.** Serve alla serie temporale della pubblicità legale.

### anac/fonti-finanziamento

Fonti di finanziamento. Campi chiave: `cig`, `fonte_finanziamento`, `importo`.

- **Uso certo:** Solo censimento (censisci_anac.py).
- **Potenziale, analisi-spesa-ict:** marca PNRR/fondi UE senza passare dal CUP (seconda via a pnrr_cloud.py, utile con P14)
- **Potenziale, Osservatorio Nazionale Sovranità Digitale:** spesa cloud finanziata con fondi UE
- **Conservazione: media.** Seconda via al CUP, che ha il 27% di ND.

### anac/subappalti

Subappalti. Campi chiave: `cig`, `subappaltatore`, `importo`.

- **Uso certo:** Solo censimento.
- **Potenziale, analisi-spesa-ict:** chi eroga davvero il servizio cloud quando l'aggiudicatario è un integratore (lente fornitore)
- **Conservazione: media.** Potenziale alto per la lente fornitore, nessuna copia altrove.

### anac/partecipanti

Partecipanti. Campi chiave: `cig`, `codice_fiscale`, `denominazione`, `ruolo`.

- **Uso certo:** Solo censimento.
- **Potenziale, Osservatorio Nazionale Sovranità Digitale:** concorrenza nelle gare ICT/cloud (numero di offerenti)
- **Conservazione: bassa.** Contesto.

### anac/avvio-contratto

Avvio contratto. Campi chiave: `cig`, `data_stipula`, `data_esecutivita`.

- **Uso certo:** Solo censimento.
- **Potenziale, analisi-spesa-ict:** data di stipula per attribuire la spesa all'anno giusto
- **Conservazione: bassa.** Raffinamento temporale.

### anac/fine-contratto

Fine contratto. Campi chiave: `cig`, `data_fine`, `importo_finale`.

- **Uso certo:** Solo censimento.
- **Potenziale, analisi-spesa-ict:** durata reale e importo finale dei contratti cloud pluriennali
- **Conservazione: bassa.** Raffinamento.

### anac/varianti

Varianti. Campi chiave: `cig`, `motivo`, `importo`.

- **Uso certo:** Solo censimento.
- **Potenziale, analisi-spesa-ict:** estensioni dei contratti cloud oltre l'importo iniziale
- **Conservazione: bassa.** Contesto.

### anac/minori

Dataset minori: categorie-opera, lavorazioni, sospensioni, collaudo, centri-di-costo, categorie-dpcm-aggregazione, attestazioni-soa, indicatori-pnrrpnc, misurepremiali-pnrrpnc, bandi-cig-*, smartcig-tipo-fattispecie. Campi chiave: `cig`, `codici di classificazione`.

- **Uso certo:** Solo censimento e integrità (censisci_anac.py, anac_integrita.py); le tabelle bandi-cig-* e smartcig-tipo-* decodificano i codici.
- **Potenziale, analisi-spesa-ict:** categorie-dpcm-aggregazione: obbligo di aggregazione per le categorie ICT; indicatori-pnrrpnc: marcatura PNRR
- **Conservazione: bassa.** Piccoli; si conservano perché il mirror è completo per costruzione (#9).

### consip/ordini

Ordini MePA, convenzione, accordi quadro (ordini-mepa, ordini-convenzione, ordini-aq, consumi-in-convenzione). Campi chiave: `anno`, `iniziativa`, `lotto`, `tipologia_amministrazione`, `provincia`, `importo_ordinato`.

- **Uso certo:** convenzioni/consip_opendata.py: seconda via, indipendente da BDNCP, al valore delle iniziative ICT (report/convenzioni/database/consip-ordinato.csv).
- **Potenziale, Osservatorio Nazionale Sovranità Digitale:** quota della spesa ICT che passa dal canale centralizzato
- **Limiti noti:** nessun CIG né ente: solo aggregati per anno e lotto; finestra mobile di tre anni (2022 e 2023 in 404).
- **Conservazione: alta.** Consip cancella gli anni oltre la finestra: ogni anno non specchiato è perso.

### consip/gare

Gare e bandi (gareasp, bandiegare, bandi_gare_rdf, as-aq-banditi, as-sda-banditi). Campi chiave: `cig`, `oggetto`, `data`, `importo`, `strumento`.

- **Uso certo:** Nessuno script lo legge ancora; specchiato (#11).
- **Potenziale, analisi-spesa-ict:** CIG padre delle iniziative Consip: completa config/iniziative_ict.yaml
- **Potenziale, Monitoraggio PVL e Amministrazione trasparente:** pagina della gara su consip.it per i CIG su delega
- **Limiti noti:** finestra mobile di tre anni.
- **Conservazione: alta.** Stessa finestra mobile; hanno il CIG, quindi si legano a ANAC.

### consip/mepa-rdo

RdO e trattative dirette MePA (bandite e stipulate, beni-servizi). Campi chiave: `anno`, `categoria`, `importo`, `tipologia_amministrazione`.

- **Uso certo:** Nessuno script.
- **Potenziale, analisi-spesa-ict:** categorie MePA ICT come controllo dei CPV del sotto soglia
- **Limiti noti:** finestra mobile di tre anni.
- **Conservazione: media.** Finestra mobile; uso solo potenziale.

### consip/anagrafiche

Amministrazioni, operatori economici, cataloghi, partecipazioni. Campi chiave: `codice_fiscale`, `denominazione`, `categoria`, `abilitazioni`.

- **Uso certo:** Il nome «amministrazioni» compare in convenzioni/ e trasparenza/ ma riferito ad altre fonti: nessun uso certo del dataset Consip.
- **Potenziale, analisi-spesa-ict:** cataloghi MePA: prodotti e marchi cloud offerti (lente prodotto)
- **Potenziale, mxmap.it:** operatori abilitati alla posta elettronica sul MePA
- **Limiti noti:** alcune distribuzioni JSON/TTL in errore alla fonte (cataloghi 2024, partecipazioni 2024-2026, operatori_economici_rdf).
- **Conservazione: media.** Finestra mobile; cataloghi pesanti (~1 GB).

### rgs/siope

SIOPE uscite e anagrafiche. Campi chiave: `codice_ente`, `anno`, `mese`, `codice_gestionale`, `importo`.

- **Uso certo:** Specchiato (2017-2026); nessuno script lo legge ancora.
- **Potenziale, analisi-spesa-ict:** unica misura di cassa per ente: codici gestionali ICT come tetto della spesa ICT e controllo dell'imbuto
- **Potenziale, Osservatorio Nazionale Sovranità Digitale:** spesa ICT pagata per ente e territorio
- **Limiti noti:** cartella open/last: il file dell'anno corrente è sovrascritto a ogni aggiornamento.
- **Conservazione: alta.** Percorso «last»: le versioni intermedie dell'anno in corso non restano alla fonte.

### agid_dtd/padigitale2026

PA Digitale 2026 (candidature finanziate, avvisi). Campi chiave: `cup`, `codice_ipa`, `misura`, `importo_finanziamento`, `stato`.

- **Uso certo:** analisi/pnrr_cloud.py (misure 1.1 e 1.2); trasparenza/test_trasparenza.py.
- **Potenziale, mxmap.it:** enti finanziati per la migrazione cloud: confronto prima/dopo dei provider
- **Potenziale, Osservatorio Nazionale Sovranità Digitale:** esito del PNRR cloud per ente
- **Conservazione: media.** Repository git pubblico: la storia c'è alla fonte, ma il mirror ne fissa gli sha256 usati.

### indicepa/enti

IndicePA (enti, unità organizzative, domicili digitali, RTD). Campi chiave: `codice_ipa`, `codice_fiscale`, `denominazione`, `sito_istituzionale`, `categoria`, `pec`, `codice_comune_istat`.

- **Uso certo:** trasparenza/fonti.py e sonda.py (censimento enti e siti del monitor AT); convenzioni/fuori_piattaforma_at.py. mxmap.it lo usa come universo degli enti e dei domini.
- **Potenziale, Osservatorio robots.txt (#64):** elenco dei siti istituzionali da sondare per robots.txt
- **Potenziale, Osservatorio Nazionale Sovranità Digitale:** anagrafe comune di tutti i progetti
- **Conservazione: alta.** Aggiornato ogni giorno sovrascrivendo: le versioni passate non restano alla fonte, ed è la base di join di tutti i progetti.

### acn/catalogo-cloud

Catalogo dei servizi cloud qualificati ACN. Campi chiave: `servizio`, `fornitore`, `livello`, `data_qualifica`.

- **Uso certo:** Solo sondato (specchia: false).
- **Potenziale, analisi-spesa-ict:** servizio qualificato → fornitore → giurisdizione: via di attribuzione
- **Potenziale, Osservatorio Nazionale Sovranità Digitale:** quanti servizi qualificati sono extra-UE
- **Limiti noti:** non specchiato: da decidere.
- **Conservazione: media.** Le qualifiche scadono e vengono tolte dal catalogo.

<!-- /GEN:schede -->
