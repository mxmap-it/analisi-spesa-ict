---
title: "Perché un mirror (bozza)"
date: 2026-11-06
description: "Le ragioni, con evidenze datate, per cui teniamo e proponiamo di rendere pubblica una copia integrale e versionata dei dati aperti di ANAC, Consip e delle altre fonti."
build:
  list: never
---

**Bozza 0.1 del 6/11/2026, non elencata (#17).** **[V]** = verificato da noi, con prova nel repository;
**[R]** = riferito o dedotto, da verificare. Progetto tecnico: [Mirror pubblico](../mirror-pubblico/).

## In breve

Una misura ripetibile ogni anno (l'obiettivo del progetto) richiede che i dati misurati restino
disponibili e identici. Per le fonti principali oggi non è così: file rimossi senza regola, file fermi a
mesi fa, finestre mobili che cancellano gli anni vecchi, mesi serviti con il contenuto di un altro mese.
Nessuna delle fonti dichiara una politica di conservazione.

## ANAC

| Evidenza | Data | Stato | Prova |
|---|---|---|---|
| Aggiornamenti mensili CIG di gennaio, febbraio e marzo 2026 rimossi (404), nessun file annuale 2026: lo stato 2026 di quei mesi non è più scaricabile | 26/10/2026 | [V] | P08; metriche I5-I6 |
| OCDS: 96 mesi serviti, solo 80 contenuti distinti; 24 mesi in 8 gruppi sono lo stesso file con il campo `uri` riscritto | 27/10/2026 | [V] | P01; `report/anac/verifica-ocds-mesi-duplicati-2026-10-27.json` |
| OCDS fermo a marzo 2026; 2025/12, 2026/01 e 2026/02 elencati ma in 404 | 27/10/2026 | [V] | P02, P10 |
| File full di aggiudicazioni e aggiudicatari fermi al 15 e 23/01/2026: lo stato corrente esiste solo nei delta, che vengono rimossi | 26/10/2026 | [V] | `config/anac-risorse.jsonl` (Last-Modified) |
| SmartCIG: giugno e luglio 2026 mancanti, distribuzione JSON interrotta | 26/10/2026 | [V] | P09 |
| Dimensioni dichiarate dal catalogo 4,1 volte quelle servite (524,78 GB contro 128,92 GB) | 26/10/2026 | [V] | P11 |
| Nessun ETag; HEAD da programmi non-browser restituisce una pagina HTML invece dei metadati: chi aggiorna in automatico non sa se il file è cambiato | 26-27/10/2026 | [V] | P12, P13 |
| Il WAF respinge IP cloud e user-agent non-browser: molti strumenti di terzi non possono scaricare | 26/10/2026 | [V] | nota d'accesso in `config/risorse.yaml` |
| Cruscotto giornaliero: **8 metriche su 9 violate** il 6/11/2026; 7 di esse violate in tutti i 12 giorni misurati | 26/10-6/11/2026 | [V] | [/enti/anac-cruscotto/](/enti/anac-cruscotto/) |
| AgID ha rilevato a sua volta che «i 12 file OCDS usati erano 4 file distinti» | — | [R] AgID, Cruscotto Italia `etl/sources/anac.py` | P01, controvalidazione |

Che cosa aggiunge il mirror: le 1.796 risorse oggi disponibili, con sha256, data e intestazioni HTTP
viste, conservate anche quando ANAC le sostituisce o le toglie; una via di accesso senza WAF; la prova
riproducibile di ogni problema comunicato.

## Consip

| Evidenza | Data | Stato | Prova |
|---|---|---|---|
| Finestra mobile di tre anni senza politica dichiarata: `ordini-mepa-2022.csv` e `ordini-mepa-2023.csv` rispondono 404, `ordini-mepa-2024.csv` 206 (il file c'è) | 6/11/2026 | [V] | richiesta HTTP del 6/11/2026; da archiviare con sha256 nella sonda |
| Alcune distribuzioni JSON/TTL in errore alla fonte (cataloghi 2024, partecipazioni 2024-2026, operatori economici RDF) | ottobre-novembre 2026 | [V] | `manifest.jsonl`, esito «errore» |
| Gli ordini sono aggregati per anno e lotto, senza CIG né ente | — | [V] | `tools/convenzioni/consip_opendata.py` |

Il 2023 è già perso per chi non l'ha scaricato prima: è la ragione più semplice per specchiare **ogni
anno prima che esca dalla finestra**. Il mirror Consip copre 2024-2026 in CSV, JSON e XLSX (#11).

## Altre fonti

| Fonte | Rischio | Stato |
|---|---|---|
| SIOPE (`siope.it/…/open/last/`) | il percorso «last» fa pensare che il file dell'anno in corso sia sostituito a ogni aggiornamento, senza versioni intermedie | [R] da verificare confrontando gli sha256 nel tempo |
| IndicePA | anagrafe aggiornata di continuo: gli stati passati (enti soppressi, domini cambiati) non restano alla fonte | [R] da verificare |
| PA Digitale 2026 | repository git pubblico: la storia resta alla fonte | [V] basso rischio; il mirror fissa solo gli sha256 usati |
| Catalogo cloud ACN | le qualifiche scadute escono dal catalogo | [R]; oggi solo sondato, non specchiato |

## Che cosa non diciamo

Non diciamo che i dati siano «spariti per sempre» se non lo abbiamo misurato; per ANAC non conosciamo il
motivo delle rimozioni. Le differenze fra versioni dello stesso URL non sono ancora misurabili sul nostro
mirror: in 12 giorni nessuna risorsa ha cambiato sha256. Il confronto fra versioni diventerà una metrica
quando ci saranno almeno due acquisizioni diverse.
