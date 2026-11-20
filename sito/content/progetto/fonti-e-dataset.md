---
title: "Fonti e dataset: da dove viene ogni numero"
date: 2026-11-20
lastmod: 2026-11-20T21:00:00Z
description: "Registro unico delle fonti usate dalle verifiche pubblicate (mirror, file di lavoro, tabelle curate, rete, modello) e dei dataset che produciamo noi, con sha256 e il modo di rifarli da un clone pulito."
weight: 37
gruppo: dati
---

**Versione 0.1 del 2026-11-20** · ticket [#81](https://github.com/mxmap-it/analisi-spesa-ict/issues/81) · [registro delle revisioni](#registro-delle-revisioni)

## 1. Perché

Ogni numero pubblicato deve potersi rifare da un clone pulito del repository (AGENTS.md § 5). Finora lo avevamo
dimostrato per il mirror ANAC e per quattro file di lavoro ([RIPRODURRE.md](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/RIPRODURRE.md)).
Ma le verifiche leggono anche BDAP, SIOPE, Indice PA, TED, GLEIF, il censimento MEF delle partecipazioni, Developers
Italia, pagine raccolte dal vivo, e tabelle che curiamo noi. Questa pagina le elenca **tutte**, con lo stato di
ciascuna, ed è rigenerata da `python3 tools/fonti.py pagina`.

Esempio: la [vista sulle società ICT pubbliche](/rendiconti/societa-ict-pubbliche/) dipende dal censimento MEF (mirror,
sha256), dai CIG e dagli aggiudicatari ANAC (mirror), da un file di lavoro con i codici fiscali per CIG (congelato in
git con sha256) e da due tabelle curate a mano (siti e soci, con la fonte di ogni riga).

## 2. Come si legge

Ogni ingresso di uno strumento è di uno di questi tipi:

- **mirror**: file scaricato dalla fonte e conservato nell'archivio append-only, indirizzato per sha256; si ripristina dall'archivio;
- **lavoro**: file intermedio in `lavoro/` (fuori da git). Deve essere **congelato** (copia in git o nell'archivio con
  sha256), oppure essere un **intermedio** che un comando rifà da ingressi già congelati;
- **git**: tabelle curate, esiti e classificazioni versionati;
- **rete**: letto dal vivo (es. API di GitHub, DNS); le risposte usate si archiviano con sha256 dove possibile;
- **modello**: esiti di un modello linguistico, già versionati: non si rigenerano, si rileggono.

Modi di congelare un file di lavoro: **git** (copia compressa in `dati/ingressi/`), **archivio** (blob con sha256),
**archivio-tar** (cartella intera in un tar deterministico, più l'elenco degli sha256 di ogni file in git),
**impronta** (solo l'elenco degli sha256, per file enormi che si rifanno dal mirror: `lavoro/cig_completo`, 11 GB).

## 3. Sintesi della verifica

<!-- GEN:sintesi -->
Verifica del 2026-11-20: 92 strumenti esaminati, ingressi per tipo git 135, lavoro 84, mirror 54, modello 5, rete 6; 17 host del mirror; 22 ingressi di lavoro/ congelati; non registrati: 0; host senza acquisizioni: 0. Esito: **ok**.
<!-- /GEN:sintesi -->

## 4. Fonti esterne nel mirror

<!-- GEN:host -->
| host | strumenti che lo leggono | acquisizioni nel mirror |
|---|---:|---:|
| assets.innovazione.gov.it | 1 | 3 |
| bdap-opendata.rgs.mef.gov.it | 4 | 2.627 |
| dati.anticorruzione.it | 24 | 2.142 |
| ec.europa.eu | 1 | 23 |
| goldencopy.gleif.org | 1 | 8 |
| indicepa.gov.it | 5 | 107 |
| presidenza.governo.it | 1 | 379 |
| raw.githubusercontent.com | 1 | 15 |
| vari (41 host di enti. dagli URL in documenti-psn.csv) | 1 | 0 |
| vari (blob Libro PSN 2025) | 1 | 0 |
| vari (blob delle pagine AT) | 1 | 0 |
| vari (elenco host) | 2 | 0 |
| vari (tutti) | 1 | 0 |
| www.acn.gov.it | 2 | 265 |
| www.de.mef.gov.it | 1 | 74 |
| www.iss.it | 1 | 58 |
| www.siope.it | 3 | 33 |
<!-- /GEN:host -->

## 5. File di lavoro letti dalle verifiche

<!-- GEN:lavoro -->
| ingresso in lavoro/ | strumenti | stato | come si rifà |
|---|---:|---|---|
| `lavoro/attribuzione/<anno>.csv` | 10 | intermedio: registro: lavoro/attribuzione (archivio-tar) | python tools/analisi/attribuisci_provider.py 2024 2025 2026 |
| `lavoro/bdap-pagine/start-*.json` | 1 | intermedio: registro: lavoro/bdap-pagine (archivio-tar) | tools/acquisizione/bdap_metadati.sh (curl CKAN BDAP) |
| `lavoro/cig_completo/*.csv` | 10 | intermedio: registro: impronta di lavoro/cig_completo | tools/anac_integrita.py (estrai_tutti(CIG_COMPLETO, 'cig_completo')) |
| `lavoro/cig_delta/*.csv` | 2 | intermedio: registro: lavoro/cig_delta (archivio-tar) | origine sconosciuta |
| `lavoro/convenzioni/attuativi.csv` | 1 | congelato (git) | derivato del 3/11/2026 dai CIG ANAC con cig_accordo_quadro delle convenzioni ICT: si conserva |
| `lavoro/cruscotto/contratti.sqlite` | 1 | intermedio: tools/cruscotto/ (dagli esiti versionati e da lavoro/imbuto/ict.csv) | tools/cruscotto/indice_contratti.py |
| `lavoro/imbuto-prova-0.3.4/<V>/ict.csv` | 1 | intermedio: tools/verifiche/imbuto_prova_034.py <V> | tools/verifiche/imbuto_prova_034.py <V> |
| `lavoro/imbuto-prova-0.3.4/base.duckdb` | 1 | intermedio: tools/verifiche/imbuto_prova_034.py prepara (dal mirror ANAC) | tools/verifiche/imbuto_prova_034.py prepara |
| `lavoro/imbuto-revisione/` | 1 | intermedio: tools/verifiche/imbuto_revisione.py (lotti e log; la lettura del modello è negli esiti versionati) | tools/verifiche/imbuto_via6_revisione.py (prepara/leggi via tools/llm/giro_revisione_guardiano.sh) |
| `lavoro/imbuto/ict.csv` | 34 | congelato (archivio) | tools/analisi/imbuto.py (IMBUTO_OUT=lavoro/imbuto) dal mirror ANAC; la prova 0.3.4 lo rifà in tools/verifiche/ripetibilita.sh, passo a |
| `lavoro/imbuto/stati-finali.csv.gz` | 2 | congelato (git) | tools/verifiche/imbuto_spostamenti.py AAAA-MM-GG |
| `lavoro/inhouse/` | 1 | intermedio: tools/verifiche/inhouse_opensource.py (risposte archiviate con sha256 nel riepilogo) | tools/verifiche/inhouse_opensource.py (risposte API Developers Italia) |
| `lavoro/inhouse/cig-cf.csv.gz` | 2 | congelato (git) | tools/verifiche/inhouse_cf.py (da ict.csv, cig_completo e aggiudicatari del mirror) |
| `lavoro/l190-campione/stato.jsonl` | 1 | congelato (git) | raccolta dal vivo dei dataset L. 190 (pagine in archivio): si conserva |
| `lavoro/mirror-completamento/` | 1 | intermedio: registro: lavoro/mirror-completamento (archivio-tar) | tools/acquisizione/bdap_lista.py (da lavoro/bdap-pagine) e tools/acquisizione/consip_html.py > .../consip/html-elenco.tsv |
| `lavoro/pnrr12/ocds-1.2.jsonl` | 1 | congelato (git) | tools/verifiche/pnrr12_ocds.py dal mirror OCDS |
| `lavoro/pvl/cig_link.csv` | 1 | congelato (archivio) | tools/acquisizione/pvl_avvisi.py estrai > lavoro/pvl/link_cig.csv (dalle pagine API PVL archiviate, elenco con sha256 in dati/ingressi/pvl/indice.jsonl.gz), poi |
| `lavoro/residuo-s6/` | 1 | intermedio: registro: out/esiti.jsonl e l4-js/enti.jsonl congelati; ingresso.csv è intermedio (residuo_s6_ingresso.py) |  |
| `lavoro/residuo-s6/ingresso.csv` | 1 | intermedio: tools/acquisizione/residuo_s6_ingresso.py (da ict.csv e pvl/link_cig.csv) | tools/acquisizione/residuo_s6_ingresso.py lavoro/residuo-s6/ingresso.csv |
| `lavoro/residuo-s6/l4-js/enti.jsonl` | 1 | congelato (git) | tools/acquisizione/at_cig_js.py (raccolta dal vivo): si conserva |
| `lavoro/residuo-s6/out/esiti.jsonl` | 2 | congelato (archivio) | tools/acquisizione/residuo_s6.sh -> at_cig.py (raccolta dal vivo, pagine in archivio): si conserva |
| `lavoro/ripetibilita/<data>/` | 1 | intermedio: uscita della prova di ripetibilità, non un ingresso |  |
| `lavoro/rivenditori/gleif-it.json` | 1 | congelato (archivio) | estratto dalla golden copy GLEIF del mirror (goldencopy.gleif.org) |
| `lavoro/smartcig/ict.csv` | 1 | congelato (archivio) | tools/verifiche/imbuto_smartcig.py --rigenera dal mirror SmartCIG |
| `lavoro/ted-v2/pagine/*.json` | 2 | intermedio: registro: lavoro/ted-v2/pagine (archivio-tar) | tools/acquisizione/ted_mirror.py --dir lavoro/ted-v2 (API https://api.ted.europa.eu/v3/notices/search) |
| `lavoro/trasparenza/stato.sqlite` | 2 | congelato (archivio) | tools/trasparenza/censimento.py (raccolta dal vivo: non identica se rifatta, si conserva) |
| `lavoro/zenodo-10007545/cpv_5M.csv.gz` | 1 | congelato (archivio) | scaricato a mano da Zenodo (record 10007545): non si rigenera, si conserva |
| `lavoro/raffinamento/pacchetti` | 0 | congelato (git-tar) | raffinamento.py prepara-l3 (idempotente, aggiunge pacchetti): i pacchetti già letti dal modello non si rigenerano, si conservano |
<!-- /GEN:lavoro -->

## 6. Registro degli ingressi congelati

`config/ingressi-lavoro.yaml`, scritto da `python3 tools/ingressi_lavoro.py congela`; da un clone pulito
`python3 tools/ingressi_lavoro.py ripristina` rimette tutto in `lavoro/` e controlla gli sha256.

<!-- GEN:registro -->
| ingresso | via | sha256 | file / byte |
|---|---|---|---|
| `lavoro/pvl/cig_link.csv` | archivio | `0bfde73703099c9f…` |  406474879 |
| `lavoro/pvl/indice.jsonl` | git | `4b696600549d62de…` |  663384 |
| `lavoro/convenzioni/attuativi.csv` | git | `5d9bcf855e9c744f…` |  636284 |
| `lavoro/raffinamento/pacchetti` | git-tar | `6789a26f95c0f8e3…` | 355  |
| `lavoro/imbuto/ict.csv` | archivio | `9604940172cd6f80…` |  229616749 |
| `lavoro/imbuto/stati-finali.csv.gz` | git | `7aaa37e931a21f18…` |  8591278 |
| `lavoro/inhouse/cig-cf.csv.gz` | git | `1056ed9b76fac44c…` |  8449716 |
| `lavoro/smartcig/ict.csv` | archivio | `cbf7be2b24eaf2f0…` |  88087169 |
| `lavoro/zenodo-10007545/cpv_5M.csv.gz` | archivio | `8fa6b264f002a41e…` |  306566254 |
| `lavoro/rivenditori/gleif-it.json` | archivio | `e4df22c8ffb45d53…` |  31774058 |
| `lavoro/trasparenza/stato.sqlite` | archivio | `c04f90388794e37b…` |  230207488 |
| `lavoro/residuo-s6/out/esiti.jsonl` | archivio | `7f039007291f3afb…` |  26093587 |
| `lavoro/residuo-s6/l4-js/enti.jsonl` | git | `60dc9bc89fe7d028…` |  489271 |
| `lavoro/l190-campione/stato.jsonl` | git | `dccf61816bdabd44…` |  108680 |
| `lavoro/pnrr12/ocds-1.2.jsonl` | git | `e1a6d0e7ea8944d6…` |  2888715 |
| `lavoro/pvl/link_cig.csv` | archivio | `fa5b5f1f138b3c0b…` |  1174644447 |
| `lavoro/attribuzione` | archivio-tar | `7ef07c9c277f6c5b…` | 16  |
| `lavoro/cig_delta` | archivio-tar | `5fd65d66eb3faa3f…` | 1  |
| `lavoro/bdap-pagine` | archivio-tar | `5bb9f1dd46ae51b9…` | 16  |
| `lavoro/ted-v2/pagine` | archivio-tar | `b75b10231c681861…` | 34  |
| `lavoro/mirror-completamento` | archivio-tar | `560ece5c76bc6a4b…` | 15  |
| `lavoro/cig_completo` | impronta | impronte in `dati/ingressi/cig_completo.sha256` | 235 11176074597 |
<!-- /GEN:registro -->

## 7. Dataset prodotti da noi

Tabelle curate a mano (ogni riga con la fonte) e dataset derivati, tutti versionati in git e rilasciati con licenza
libera. Sono dataset a pieno titolo, non configurazione: la colonna sha256 permette di citarne la versione.

<!-- GEN:nostri -->
| tipo | file | versione | contenuto | sha256 |
|---|---|---|---|---|
| tabella curata | [`config/budget.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/budget.yaml) |  | Tetto di sforzo del progetto, deciso da Fabio il 2026-10-26: | `bbbea5a3d2d8…` |
| tabella curata | [`config/datacenter_proprio.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/datacenter_proprio.yaml) | 0.4 | Regole per riconoscere la spesa per datacenter propri («cloud in proprio», #52). | `d8c3622a1d7c…` |
| tabella curata | [`config/fonti-verifiche.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/fonti-verifiche.yaml) | 0.1 | Inventario STATICO delle fonti delle verifiche pubblicate (#81), 20/11/2026. | `e343604a19ae…` |
| tabella curata | [`config/ingressi-lavoro.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/ingressi-lavoro.yaml) |  | descrizione: Ingressi di lavoro/ letti dall'imbuto e fuori dal mirror ANAC (M12). Generato da tools/ingressi_lavoro.py congela. | `ab2629e11a92…` |
| tabella curata | [`config/inhouse_siti.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/inhouse_siti.yaml) | 0.1 | Siti web delle società ICT pubbliche non trovati nell'Indice PA (letto da tools/verifiche/inhouse_censimento.py). | `b0b8b93da2eb…` |
| tabella curata | [`config/inhouse_soci.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/inhouse_soci.yaml) | 0.1 | Quote pubbliche verificate a mano per le società ICT «da verificare» (letto da tools/verifiche/inhouse_censimento.py 0.3). | `489e2e5714fd…` |
| tabella curata | [`config/inhouse_verifica.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/inhouse_verifica.yaml) | 0.2 | Verifica per CIG della classe «in-house» dell'imbuto (#52, #71). Letta da tools/verifiche/inhouse_verifica.py. | `7a6ba61e04e0…` |
| tabella curata | [`config/iniziative_ict.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/iniziative_ict.yaml) |  | Base di conoscenza delle iniziative ICT (accordi quadro e convenzioni padre) per lo strato S3 dell'imbuto. | `756ec84ee1d8…` |
| tabella curata | [`config/lotti_cloud.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/lotti_cloud.yaml) |  | Lotti di accordi quadro e convenzioni che identificano il cloud provider (via 2 del metodo). | `522360dcecc4…` |
| tabella curata | [`config/mappa-imbuto.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/mappa-imbuto.yaml) | 0.11 | Mappa dell'imbuto: dataset, relazioni, livelli, limiti, mancanze (#71 #74, richiesta di Fabio 19/11/2026). | `41c4f15464fe…` |
| tabella curata | [`config/marchi_cloud.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/marchi_cloud.yaml) |  | Dizionario dei marchi (vie 3 e 5). Metodo: sito/content/progetto/metodo-cloud-provider.md | `7e62f8778b23…` |
| tabella curata | [`config/marchi_cloud_fonti.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/marchi_cloud_fonti.yaml) |  | 40 Fonte della giurisdizione per ogni provider del dizionario dei marchi (config/marchi_cloud.yaml). | `f371263df8c8…` |
| tabella curata | [`config/perimetro_cpv.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/perimetro_cpv.yaml) | perimetro-cpv-0.3 (2026-11-09) | Perimetro ICT per CPV (#44). Lista bianca: un CIG con CPV che inizia con uno di questi prefissi entra nel perimetro ICT | `f52159ffba56…` |
| tabella curata | [`config/risorse.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/risorse.yaml) | 1 | Registry delle risorse da monitorare e specchiare. | `3da634b726a7…` |
| tabella curata | [`config/rivenditori_capogruppo.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/rivenditori_capogruppo.yaml) |  | Capogruppo dei rivenditori di prodotti cloud (#41, v4 del 9/11/2026). Prevale su GLEIF (tools/verifiche/rivenditori_mappa.py). | `befbf4a01f77…` |
| tabella curata | [`config/saas_host.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/saas_host.yaml) |  | Domini dei servizi SaaS (front-end per ente) dei fornitori S2 della Misura 1.2, trovati fra gli host dell'archivio | `921066ed2fb8…` |
| tabella curata | [`config/saas_infrastruttura.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/saas_infrastruttura.yaml) | 0.4 | Infrastruttura sottostante dei SaaS qualificati ACN dei primi fornitori S2 della Misura PNRR 1.2 (#43, #45) | `ef952d14e32b…` |
| tabella curata | [`config/societa_inhouse_ict.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/societa_inhouse_ict.yaml) | 0.1 | Società ICT in-house della PA (#52, vista «cosa fanno le in-house»). Letta da tools/verifiche/inhouse_vista.py e | `9595d63f69ad…` |
| tabella curata | [`config/tipi_soggetto.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/tipi_soggetto.yaml) |  | 62: tipo di soggetto della stazione appaltante del CIG padre, per il filtro della sezione /convenzioni/. | `0a894318ba8e…` |
| tabella curata | [`config/usi-dataset.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/usi-dataset.yaml) | 1 | Usi dei dataset del mirror rispetto ai progetti dell'osservatorio (#17, #9). | `4e25a10ead8a…` |
| dataset derivato | [`dati/inhouse/catalogo-riuso.csv`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/dati/inhouse/catalogo-riuso.csv) |  | società ICT pubbliche (#82) | `413d153cb052…` |
| dataset derivato | [`dati/inhouse/opensource-riepilogo.json`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/dati/inhouse/opensource-riepilogo.json) |  | società ICT pubbliche (#82) | `fe79342111d4…` |
| dataset derivato | [`dati/inhouse/opensource.csv`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/dati/inhouse/opensource.csv) |  | società ICT pubbliche (#82) | `7405bc47164d…` |
| dataset derivato | [`dati/inhouse/riepilogo.json`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/dati/inhouse/riepilogo.json) |  | società ICT pubbliche (#82) | `111db66436b3…` |
| dataset derivato | [`dati/inhouse/societa-ict-pa.csv`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/dati/inhouse/societa-ict-pa.csv) |  | società ICT pubbliche (#82) | `76ce38dbb93b…` |
<!-- /GEN:nostri -->

## 8. Limiti

- L'inventario degli ingressi è **statico** (lettura del codice, `config/fonti-verifiche.yaml`): un percorso costruito
  a runtime può sfuggire. Il controllo dinamico è la prova da clone pulito (`tools/verifiche/ripetibilita.sh`).
- Le raccolte dal vivo (sezioni di Amministrazione trasparente, atti L4, dataset L. 190) non si rifanno identiche: si
  conserva lo stato raccolto e le pagine scaricate.
- `lavoro/cig_delta` non ha uno strumento che lo produca (estrazione a mano dei delta ANAC): congelato, origine da documentare.

## Registro delle revisioni

| versione | data | modifica |
|---|---|---|
| 0.1 | 2026-11-20 | prima versione: inventario di 92 strumenti, registro degli ingressi esteso a cartelle e impronte (#81) |
