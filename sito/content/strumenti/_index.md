---
title: "Strumenti: quali usiamo, quali no, e perché"
---
**Principio di progetto: scrivere meno codice possibile.** Riusiamo tutto ciò che è libreria o servizio invocabile e scriviamo solo ciò che non esiste: il codice che non si scrive non va mantenuto.

**Riusati.** Il motore di pipeline `toolkit` e il radar `source-observatory` di DataCivicLab; le CLI di onData per la Pubblicità a Valore Legale, il catalogo BDAP e IndicePA — inclusi la validazione del CIG e il classificatore di giurisdizione; i moduli di ingestione di Cruscotto Italia di AgID per SIOPE e PNRR; `frictionless-py` e il validatore SHACL europeo per la qualità; GLEIF e `nomenklatura` per l'identità dei fornitori.

**Scartati, con il motivo.** Il canale OCDS di ANAC come fonte primaria (mesi duplicati, fermo da marzo 2026); l'API REST di ANAC (non funzionante); SIOPE attraverso BDAP (annualità troncate); i ventitré portali regionali (dal 2024 confluiscono in ANAC); gli XML della Legge 190 per ente; un aggregatore generalista (esiste già due volte); la normalizzazione di tutto in un unico schema (competenza, cassa e aggiudicato non sono sommabili).

L'analisi completa, con le prove, è nel [README del progetto](https://github.com/mxmap-it/analisi-spesa-ict#3-le-strade-che-non-abbiamo-seguito).
