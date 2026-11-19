# Bozze di contatto verso terzi — DA APPROVARE DA FABIO

Stato: **bozze, nessun invio** (19/11/2026). Regola: AGENTS.md § 7, nessuna comunicazione verso enti o terzi senza
l'approvazione di Fabio. Numeri: solo quelli del [punto nave del 19/11/2026](https://analisi-spesa-ict.mxmap.it/rendiconti/punto-nave-2026-11-19/)
(versione 1.2), con il rimando invece di ricopiarli dove possibile, così la bozza non invecchia.

Cifre di riferimento [V] (punto nave 1.2, imbuto 0.3.4 con raffinamento a livelli e livello B):
- universo: 3.734.840 contratti (CIG) ANAC dal 2024; spesa ICT 289.192 CIG, 56,06 miliardi al netto dei massimali di accordo quadro;
- cloud certo dal 2024: 1,21 miliardi in 4.556 CIG; sugli inclusi certi la giurisdizione del prodotto è extra-UE 47 %, Italia 39 %, UE 14 % (campioni a cieco);
- incerto: 16,37 miliardi nel residuo; 5,37 miliardi di licenze con marchio noto da accertare;
- pagato ICT 2024 (SIOPE + BDAP): circa 5,1 miliardi.

---

## 1. AgID, team di Cruscotto Italia (#37) — canale pubblico: dati@agid.gov.it

**Oggetto:** Archivio dei dati ANAC e problemi già documentati da Cruscotto Italia: proposta di coordinamento

Buongiorno,

siamo il progetto aperto «Analisi della spesa ICT della PA» dell'Osservatorio nazionale sulla sovranità digitale
(https://analisi-spesa-ict.mxmap.it/). Misuriamo quanta spesa pubblica va in servizi cloud e infrastrutture, per
giurisdizione del prodotto, partendo dai contratti ANAC.

Nel vostro lavoro su Cruscotto Italia avete documentato in modo indipendente alcuni problemi dei dati ANAC che anche noi
abbiamo misurato (pacchetti OCDS duplicati e fermi, finestra limitata dei mensili, pagina di blocco che risponde 200).
Le nostre schede, ciascuna con prova riproducibile (sha256), azione correttiva e metrica, sono qui:
https://analisi-spesa-ict.mxmap.it/rendiconti/anac-2026-10-problemi/

Vi proponiamo:
1. di non duplicare l'archivio giornaliero dei mensili BDNCP: il nostro mirror è pubblico, content-addressed e con
   manifest (https://analisi-spesa-ict.mxmap.it/progetto/mirror-pubblico/);
2. di confrontare a fine percorso alcuni totali su un campione di comuni, usando Cruscotto Italia come controprova;
3. di sapere se è prevista la pubblicazione, per ente, degli esiti del Censimento del patrimonio ICT 2026 (la nostra
   raccomandazione R48).

Restiamo a disposizione per una breve chiamata.

---

## 2. DataCivicLab, source-observatory (#21) — canale: issue o discussione pubblica sul repository

**Titolo:** Proposta: monitoraggio per singola risorsa (oltre al livello di portale) per le fonti di spesa pubblica

Ciao, usiamo `source-observatory` come riferimento per il registro delle risorse
(`config/risorse.yaml` di https://github.com/mxmap-it/analisi-spesa-ict, formato compatibile).
Nel nostro mirror misuriamo ogni giorno, **per singola risorsa**, disponibilità, sha256, freschezza e persistenza
(risorse sparite dalla fonte ma conservate da noi), per ANAC, SIOPE, BDAP, IndicePA, PA Digitale 2026.
Ci piacerebbe portare questo livello nel vostro strumento, limitato alle fonti di spesa: vi interessa?
Se sì, apriamo una PR piccola con lo schema dei campi e un adattatore di esempio.

---

## 3. Enti, think tank e ricercatori europei (#49) — modello unico, un invio per soggetto

Elenco dei soggetti con canale pubblico verificato: rapporto dell'Osservatorio
«Misure europee sovranità digitale» (§ «Contatti da attivare tramite canali pubblici»), da riallineare con la pagina
[Design metodologico](https://analisi-spesa-ict.mxmap.it/progetto/design-metodologico/) (#48) prima dell'invio.
Ordine proposto: Open Contracting Partnership; Government Transparency Institute; autori dello studio del Parlamento
europeo PE 778.576; Università di Bonn (Digital Dependence Index); EDRIX/EuroStack; Nextcloud DSI.

**Oggetto (EN):** Measuring Italian public cloud spending by product jurisdiction — open method and data

Dear …,

we run an open project that measures how much the Italian public administration spends on cloud services and IT
infrastructure, attributing jurisdiction (Italy / EU / non-EU) to the **product** bought, not to the contractor or
reseller. Everything is reproducible from public procurement data (ANAC), with a published method and open results:
https://analisi-spesa-ict.mxmap.it/rendiconti/punto-nave-2026-11-19/

We read your work on [specific item] and would like to (a) align classifications where possible (CPV perimeter,
jurisdiction buckets), (b) share our product-level lists (cloud lots of framework agreements, brands) under a free
licence, (c) hear your criticism of the method. Would you be open to a short call?

---

## Non preparate di proposito

- **#19 report trimestrale e notifica alle autorità** e **#22 metodo in anac-pl-pp-cli**: per decisione, a fine
  percorso (dopo il rendiconto del risultato parziale, #78).
- **#34 #35 #36 ANAC**: il documento (v1.1) e la presentazione (1.1) esistono già e riguardano la qualità dei dati,
  non i numeri dell'imbuto; le richieste di capacità analitica (#54) stanno nel registro
  `report/metodo/richieste-e-raccomandazioni.yaml` (R84 compresa).
- **#58 #69 accesso civico**: solo dopo #78 (decisione di Fabio del 19/11/2026).
