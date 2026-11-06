---
title: "Mirror pubblico ANAC: progetto (bozza)"
date: 2026-11-06
description: "Stato del mirror sul server, requisiti per renderlo usabile da terzi, opzioni di hosting con costi e limiti, scelta proposta. Decisione a Fabio."
build:
  list: never
---

**Bozza 0.1 del 6/11/2026, non elencata (#17).** Nessun dato è stato caricato in pubblico: l'hosting lo
decide Fabio. Perché serve un mirror: [Perché un mirror](../perche-un-mirror/). A che cosa servono i
dataset: [Usi dei dataset](../usi-dei-dataset/).

## 1. Stato del mirror (misurato il 6/11/2026 dal manifest reale)

Archivio append-only e indirizzato per contenuto sul server di mxmap.it (`archivio/blobs/sha256/…`,
vista per percorso originale `archivio/mirror/<host>/<path>`). Indice generato da
`tools/indice_mirror.py` dal `manifest.jsonl`: [indice.csv](/dati/mirror/indice.csv) (una riga per
risorsa: URL originale, sha256, byte, Last-Modified, prima e ultima acquisizione, numero di versioni) e
[sintesi.json](/dati/mirror/sintesi.json).

<!-- GEN:mirror -->
| Autorità | Gruppi | Risorse viste | Conservate (sha256) | GB (ultima versione) | Formati |
|---|---:|---:|---:|---:|---|
| anac | 32 | 1807 | 1805 | 128,72 | CSV, JSON, TTL |
| consip | 18 | 150 | 143 | 4,45 | CSV, JSON, TTL, XLSX |
| rgs | 2 | 11 | 11 | 0,74 | ZIP |
| indicepa | 27 | 54 | 54 | 0,15 | JSON, TXT, XLSX |
| agid_dtd | 11 | 11 | 11 | 0,05 | CSV |
| **totale** | | **2033** | **2024** | **134,11** | |

ANAC per dataset (GB): ocds 73,84; smartcig-annuale 38,65; cig-annuale 8,60; cig 1,54; aggiudicazioni 0,98; quadro-economico 0,82; partecipanti 0,75; smartcig 0,74; pubblicazioni 0,47; aggiudicatari 0,41; categorie-opera 0,38; cup 0,24; stati-avanzamento 0,23; avvio-contratto 0,23; fonti-finanziamento 0,18; attestazioni-soa-v2 0,16; subappalti 0,12.
<!-- /GEN:mirror -->

- **ANAC [V]:** 1.796 delle 1.800 risorse elencate dal catalogo CKAN sono conservate con sha256
  (128,7 GB compressi, CSV + JSON + TTL, OCDS bulk 2018-2026 compreso: 96 file, 73,8 GB). Le 4 che
  mancano rispondono 404 alla fonte (OCDS 2025/12, 2026/01, 2026/02 e `smartcig-2025_csv_logCsv.csv`,
  problema P10): non sono recuperabili da nessuna parte. Il ticket #9 è chiuso su questa base.
- **File grandi:** 13 file superano i 2 GiB; il più grande è l'OCDS 2025/10 (5,25 GB).
- **Storico delle versioni:** il mirror esiste dal 26/10/2026; finora **nessuna risorsa ha cambiato
  sha256** fra un'acquisizione e l'altra (0 su 2.033). La storicizzazione è pronta (ogni versione resta
  un blob), ma ancora non ha nulla da conservare: le sovrascritture che motivano il mirror sono quelle
  *già avvenute prima* (delta rimossi, file full fermi, mesi OCDS spariti), documentate nel
  [Perché](../perche-un-mirror/).
- **Spazio:** 136 GB di blob; sul server restano 51 GB liberi (soglia di guardia 40 GB). Raddoppiare
  l'archivio sullo stesso disco non è possibile.

## 2. Requisiti (roadmap §1F)

1. **Percorsi originali** sotto un prefisso nostro: chi usa `https://dati.anticorruzione.it/opendata/…`
   cambia solo l'URL di base.
2. **Endpoint compatibili CKAN** minimi: `package_list`, `package_show`, `package_search`, generati dal
   nostro indice, con gli `url` delle risorse riscritti verso il mirror.
3. **Manifest** `index.json` + `manifest.jsonl` + `SHA256SUMS` per dataset; `datapackage.json` dove lo
   schema è noto.
4. **Licenza:** quella della fonte, invariata (ANAC CC BY-SA 4.0; Consip CC BY 4.0; per l'OCDS la licenza è
   incoerente alla fonte, P07: si ripubblica con CC BY-SA 4.0, la più restrittiva, e la nota).
   Attribuzione e avviso «copia non ufficiale» in ogni dataset.
5. **Cadenza:** stessa della sonda (giornaliera per l'elenco, mensile per i file), pubblicazione entro 24 h
   dall'acquisizione.
6. **Storicizzazione:** l'ultima versione al percorso originale; le precedenti a
   `…/versioni/<sha256>/<nome>` e nel manifest; mai cancellate. Snapshot annuale congelato con DOI.
7. **HTTP corretto:** `Last-Modified`, `ETag` (= sha256), `Accept-Ranges`, nessun WAF né filtro sullo
   user-agent, limite di banda dichiarato.
8. **Compatibilità** con `kingfisher-collect`, `cruscotto-italia/etl`, DoveVannoINostriSoldi, toolkit
   DataCivicLab (prova da fare prima dell'annuncio).

## 3. Opzioni di hosting

Costi e limiti sono **[R] riferiti dalle pagine dei fornitori**, da riverificare al momento della scelta.
Volume: ~129 GB oggi per ANAC (~135 GB con le altre fonti), +~10-15 GB l'anno di nuove versioni stimate.

| Opzione | Costo | Limiti rilevanti | Percorsi originali + CKAN | Storico | Giurisdizione |
|---|---|---|---|---|---|
| GitHub Releases | gratis | file ≤ 2 GiB (13 file la superano: andrebbero spezzati); niente percorsi | no | per release | USA |
| Zenodo | gratis | 50 GB per record (estendibile su richiesta); caricamento lento | no | versioni con DOI | UE (CERN) |
| Internet Archive | gratis | nessun limite rigido; lento; nessuna garanzia di servizio | no | sì, per item | USA |
| Software Heritage | gratis | archivia codice (repository git), non dataset di 100 GB | no | sì | UE (Inria) |
| Server mxmap.it | 0 € in più | 51 GB liberi, disco al 95 %; condiviso con la produzione di mxmap.it; banda condivisa | sì (nginx sull'archivio, hardlink: zero copie) | sì | UE (Scaleway, FR) |
| Hugging Face datasets | gratis (pubblico) | file grandi via Xet; politiche di spazio «best effort» | no (percorsi propri) | sì (commit git) | USA |
| Object storage S3-compatibile UE (Hetzner, Scaleway, OVH) | ~5-10 €/mese per ~150 GB più traffico (Hetzner: quota base con 1 TB di spazio e 1 TB di traffico) [R] | serve un piccolo frontale per le query CKAN | sì (chiavi = percorsi originali) | sì (prefisso versioni) | UE |

## 4. Scelta proposta (decide Fabio)

**Proposta: tre livelli.**

1. **Servizio vivo** su object storage S3-compatibile in UE (Hetzner o Scaleway), con le chiavi uguali ai
   percorsi originali e un frontale minimo sul server di mxmap.it (nginx: le risposte CKAN sono file
   JSON statici generati dall'indice; i file si servono per redirect al bucket). Dominio
   `mirror.mxmap.it` (DNS su TopDNS, niente Cloudflare). **Perché:** è l'unica opzione che soddisfa insieme
   i percorsi originali, gli header HTTP e lo storico senza toccare il disco della produzione; costa
   pochi euro al mese; e un osservatorio sulla sovranità digitale non può servire i dati della PA da un
   fornitore extra-UE.
2. **Conservazione** con **Zenodo**: uno snapshot congelato l'anno (e a ogni evento rilevante, come la
   chiusura di ANAC) con DOI, citabile nei rapporti e nelle comunicazioni ad ANAC. OCDS diviso in record per
   anno per stare nei 50 GB.
3. **GitHub** solo per indice, manifest e SHA256SUMS (già nel repository), così che chiunque verifichi le
   copie.

Alternativa a costo zero: servire subito dal server di mxmap.it (hardlink, nessuna copia) con limite di
banda, finché lo spazio regge; migrare poi al bucket. Sconsigliata come soluzione stabile per disco e
carico condivisi.

**Da decidere:** fornitore del bucket e budget; dominio; se annunciare il mirror e a chi; se includere le
fonti non ANAC fin dall'inizio.
