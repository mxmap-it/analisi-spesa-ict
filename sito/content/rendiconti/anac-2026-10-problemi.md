---
title: "I dati aperti di ANAC: problemi e rimedi"
subtitle: "Sintesi e schede tecniche per la correzione · rilevazione di ottobre 2026"
date: 2026-10-27
layout: problemi
pdf: "/pdf/anac-problemi-e-rimedi-2026-10.pdf"
description: "I problemi dei dati aperti della Banca Dati Nazionale dei Contratti Pubblici, ciascuno con prova riproducibile, conferma indipendente, rimedio atteso da ANAC e metrica di non ricorrenza."
---
**Osservatorio Nazionale Sovranità Digitale** · progetto
[analisi-spesa-ict](https://github.com/mxmap-it/analisi-spesa-ict) · versione del 27 ottobre 2026

## Perché questo documento

ANAC pubblica sul portale `dati.anticorruzione.it` uno dei patrimoni di dati sugli appalti pubblici
più ampi d'Europa: oltre dodici milioni di contratti dal 2007, in tre formati e nello standard
internazionale OCDS. Per misurare la spesa pubblica in servizi cloud abbiamo scaricato e verificato
tutto il portale: 1.797 risorse, 77 GB di file usati per le verifiche.

Abbiamo trovato problemi che impediscono di usare quei dati in modo affidabile. Questo documento li
elenca **con un solo scopo: che vengano corretti.** Per ognuno indica la conseguenza per chi usa i
dati, il rimedio che chiediamo ad ANAC e il controllo automatico con cui verificheremo, nel tempo,
che il problema sia risolto e non si ripresenti.

I problemi sono noti anche ad **AgID**, che ne ha documentati diversi, in modo indipendente da noi,
nel codice pubblico di Cruscotto Italia (ottobre 2026).

## Come leggerlo

- La **sintesi** elenca i problemi pronti per la comunicazione, con conseguenza e rimedio atteso.
- Le **schede** sono scritte per il gruppo tecnico: cosa abbiamo misurato, come rifarlo, come lo
  abbiamo confermato, cosa chiediamo, come verificheremo.
- L'**analisi completa**, con tutti i controlli e il registro delle revisioni, è nel
  [rendiconto tecnico](/rendiconti/anac-2026-10/).

## Come riprodurre tutto

Ogni numero si può rifare da zero, su qualunque macchina, con pochi comandi. Il dettaglio
(requisiti, tempi, cosa controlla ogni script) è in
[RIPRODURRE.md](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/RIPRODURRE.md).

```bash
git clone https://github.com/mxmap-it/analisi-spesa-ict.git && cd analisi-spesa-ict
tools/verifica_anac.sh ambiente     # ambiente con versioni bloccate
tools/verifica_anac.sh dal-vivo     # stato attuale del server ANAC, pochi minuti
tools/verifica_anac.sh scarica      # i file usati per le verifiche, ~77 GB
tools/verifica_anac.sh snapshot     # sono gli stessi file del 27 ottobre 2026? (sha256)
tools/verifica_anac.sh verifiche    # tutte le verifiche
tools/verifica_anac.sh confronta    # ogni numero confrontato con quelli pubblicati
```

Il controllo **dal vivo** gira ogni mattina sul nostro server: quando ANAC corregge un problema, la
sua metrica passa da *violata* a *rispettata*, e lo pubblichiamo.

## Il nostro impegno

Se un nostro numero è sbagliato lo correggiamo e lo registriamo, come abbiamo già fatto
più volte nel registro delle revisioni del rendiconto tecnico. Le segnalazioni si aprono su
[GitHub](https://github.com/mxmap-it/analisi-spesa-ict/issues).
