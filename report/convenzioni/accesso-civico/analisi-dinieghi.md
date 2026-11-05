# Accesso civico sulle convenzioni ICT: analisi avversariale dei dinieghi (#62)

Versione 0.1 — 5/11/2026. Stato: **bozza, nessuna istanza inviata** (le invia Fabio).

L'accesso civico generalizzato (art. 5 c. 2 d.lgs. 33/2013) qui è un **rimedio di breve periodo per carenze di policy**: i dati
sono stati cercati prima sulle pagine ufficiali (consip.it, TED, BDNCP, PVL) e non ci sono (inventario in
`report/convenzioni/database/iniziative.json`). È coerente con la regola «accesso civico come ultima risorsa» (DECISIONI.md, 5/11/2026).
Il rimedio strutturale sono le proposte di policy R37-R42.

Si ragiona come l'ufficio legale del destinatario che vuole negare. Livelli: [V] verificato sul testo (scheda
`report/metodo/accessibilita-documenti-normativa.md`); [R] riferito, da verificare sulla fonte. Il precedente del progetto è
l'analisi sui PPdF del PSN (`report/convenzioni/psn-database/README.md`).

## Motivi di diniego e come le richieste minime li neutralizzano

| Motivo | Forza | Su cosa | Neutralizzazione nella richiesta |
|---|---|---|---|
| **Segreto tecnico o commerciale** (art. 5-bis c. 2 lett. c d.lgs. 33/2013 [V]; art. 35 d.lgs. 36/2023 [R]) | forte sull'offerta tecnica integrale; debole su prodotti e prezzi di convenzione | C1, C2 | Non si chiede l'offerta integrale: solo le sezioni con prodotti, marchi, produttori, region e data center, subappaltatori. Si **accettano gli oscuramenti** delle parti che l'offerente ha dichiarato segrete in gara, con motivazione. I prezzi di una convenzione sono condizioni applicate a tutte le PA aderenti, non un'informazione riservata dell'offerente. |
| **Controinteressato** (art. 5 c. 5: notifica all'aggiudicatario, 10 giorni per opporsi [V]) | procedurale | C1, C2, C6 | Si mette in conto il ritardo. La richiesta minima rende difficile dimostrare un pregiudizio **concreto**, richiesto dalle Linee guida ANAC 1309/2016 [R]. |
| **Sicurezza pubblica o informatica** (art. 5-bis c. 1 lett. a-c [V]) | forte su indirizzi e architetture; nulla su paese e region | C6 | Si chiedono solo paese, città o region dichiarata del cloud provider, mai indirizzi, schemi di rete o misure di sicurezza. |
| **Non è un documento: è un'elaborazione** (l'accesso civico non obbliga a creare dati [R, Linee guida ANAC 1309/2016 §4.2]) | media | C3, C4, C7, C8 | Si chiede **copia dell'estrazione o del report già esistente** (report di monitoraggio, cruscotto interno, tabella di configurazione della gara), nel formato in cui è già detenuto. Non si chiede di calcolare nulla. |
| **Richiesta massiva o onere sproporzionato** [R] | media se si chiedono tutte le iniziative insieme | tutte | Un'istanza per iniziativa e carenza; si parte dalle iniziative di maggior valore. Periodo limitato (dal 1/1/2024). |
| **Soggetto non tenuto** (Consip è S.p.A.; art. 2-bis c. 2 lett. b d.lgs. 33/2013, «in quanto compatibile» [R]) | debole per Consip, media per i concessionari (PSN) | Consip, PSN S.p.A. | Per il PSN l'istanza va al **DTD-PCM** concedente o all'ente aderente. Per Consip, società interamente pubblica che svolge funzioni di centrale di committenza, si cita l'art. 2-bis c. 2. |
| **Interesse del richiedente non dichiarato** | nullo | tutte | L'istanza non va motivata (art. 5 c. 3 [V]); la motivazione è facoltativa e serve solo a rendere chiaro l'interesse pubblico. |
| **Dato già pubblicato** | nullo, anzi utile | — | Se il destinatario indica un link, il risultato equivale a una risposta positiva e lo archiviamo con sha256. |

## Richieste minime per carenza

| Carenza | Richiesta minima | In subordine |
|---|---|---|
| C1 offerte tecniche | sezioni dell'offerta tecnica con prodotti, marchi, produttori, region e data center, subappaltatori, con oscuramenti accettati | elenco di prodotti e marchi offerti per lotto |
| C2 listini offerti | listino prezzi o allegato economico applicato alle PA aderenti, per lotto | elenco di codici e descrizioni dei prodotti a listino |
| C3 transato | estrazione esistente del transato (o del valore degli ordinativi) per lotto e, dove c'è, per listino o marchio, per anno dal 2024 | totale per lotto |
| C4 ordinativi | estrazione esistente degli ordinativi: ente, data, lotto, importo, CIG derivato | numero e importo degli ordinativi per lotto e per ente |
| C5 progetti dei fabbisogni | tabella «Riepilogo prezzi» del PPdF (modello del PSN) | importo per famiglia di servizio |
| C6 region e data center | paese e region o città dei data center dichiarati per lotto | paese del trattamento |
| C7 erosione | valore del massimale eroso per lotto alla data della risposta | percentuale di erosione |
| C8 indice ID ↔ CIG | elenco dei lotti dell'iniziativa con il CIG di ciascuno | — |

## Dopo il diniego

Riesame dell'RPCT (art. 5 c. 7 [V]), poi ricorso al TAR (art. 116 c.p.a.) [R]. Ogni diniego diventa evidenza per la proposta
di policy corrispondente.
