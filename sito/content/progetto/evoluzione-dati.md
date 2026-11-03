---
title: "Come cambiano i dati negli anni, e con loro l'attendibilità"
date: 2026-11-03
description: "Dal 2020 a oggi i dati ANAC sugli acquisti cambiano struttura: due dataset (CIG e SmartCIG) fino al 2023, il ciclo digitale dal 2024. Cosa c'è in ogni anno, cosa manca e quale attendibilità si può raggiungere."
weight: 17
---

La misura della spesa cloud parte dai contratti pubblici registrati presso ANAC. **Quei dati non sono uguali in tutti gli anni.** Cambiano i dataset, i campi disponibili e la possibilità di arrivare ai documenti. Di conseguenza cambia l'attendibilità che possiamo raggiungere. Questa pagina spiega come, anno per anno, e si aggiorna a ogni nuova misura.

Legenda: **V** = misurato da noi sui file ANAC archiviati (sha256); **R** = riferito (norma o documentazione), da verificare.

## 1. Due dataset: CIG e SmartCIG

- **CIG** (codice identificativo di gara, procedura ordinaria). Ogni riga ha oggetto, importo, ente, **CPV**, procedura e **CIG dell'accordo quadro** da cui il contratto deriva. Gli **aggiudicatari** sono in un dataset collegato.
- **SmartCIG** (CIG semplificato, codice che di solito inizia per Z). È stato pensato per i contratti minori e le fattispecie particolari. Ha oggetto, importo, ente, tipo di fattispecie e procedura, ma **non ha CPV, non ha aggiudicatario e non ha il collegamento all'accordo quadro** (V, colonne dei file ANAC).

Per classificare un contratto SmartCIG resta quindi solo il **testo dell'oggetto**: nessun segnale strutturato aiuta, né per escludere né per includere.

## 2. Cosa c'è in ogni anno (V)

| anno | SmartCIG (contratti) | SmartCIG (euro dichiarati) | cosa contiene SmartCIG |
|---|---|---|---|
| 2020 | 4,68 milioni | 28,5 mld | affidamenti sotto 40.000 €, più fattispecie particolari |
| 2021 | 4,66 milioni | 29,3 mld | idem |
| 2022 | 4,42 milioni | 33,3 mld | sotto 40.000 € (15,2 mld), difesa e sicurezza (4,7 mld), **affidamenti in house** (2,6 mld), adesioni ad accordi quadro sotto 40.000 € (1,2 mld) |
| 2023 | 4,71 milioni | 48,4 mld | sotto 40.000 € (16,9 mld), difesa (7,0 mld), **servizi sociali e socio-sanitari** (11,4 mld), adesioni ad accordi quadro (2,4 mld) |
| 2024 | 3,39 milioni | 5,0 mld | **solo affidamenti diretti**, in media circa 1.500 € l'uno |
| 2025 | 2,99 milioni | 4,5 mld | idem |

Nel dataset **CIG** ordinario il numero di contratti esclusi come non ICT passa da circa 0,5 milioni (2023) a oltre 1 milione (2024) (V, [imbuto 0.2](https://github.com/mxmap-it/analisi-spesa-ict/tree/main/esiti/2026-11-02/imbuto)).

**Lettura.** Dal 2024, con il nuovo Codice dei contratti (d.lgs. 36/2023) e la digitalizzazione del ciclo, il grosso degli affidamenti passa nel CIG ordinario, con CPV e aggiudicatario. In SmartCIG restano solo affidamenti diretti molto piccoli, coerenti con il regime ANAC per gli importi sotto i 5.000 € (R, da verificare sulle delibere).

Due fatti contano per noi:
- **Prima del 2024 una quota rilevante di spesa sta in SmartCIG, senza CPV né aggiudicatario.** Contando solo il dataset CIG, il 2020-2023 risulta sottostimato rispetto al 2024 e oltre, e i due periodi non sono confrontabili.
- **Gli affidamenti in house stanno in SmartCIG** (2,6 mld nel 2022). Tra questi ci sono le società ICT in house di Stato e Regioni, che contano per la voce «datacenter e infrastrutture interne» dell'obiettivo finale.

## 3. Cosa si può sapere di un contratto, per periodo

| informazione | CIG 2020-2023 | SmartCIG 2020-2023 | CIG dal 2024 | SmartCIG dal 2024 |
|---|---|---|---|---|
| oggetto in testo libero | sì | sì | sì | sì |
| importo | sì | sì | sì | sì |
| CPV (categoria) | sì, spesso generico (vedi [CPV](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/cpv/letteratura.md)) | **no** | sì | **no** |
| aggiudicatario | sì | **no** | sì | **no** |
| collegamento all'accordo quadro | sì, quando compilato | **no** | sì, quando compilato | **no** |
| schede di esecuzione e conclusione | parziali | no | dovute (R), da misurare | no |
| link ai documenti | quasi mai (da misurare) | no | atteso nei dati (R), da misurare | da misurare |
| prodotto, produttore, giurisdizione | **mai** | **mai** | **mai** | **mai** |

## 4. Come cambia l'attendibilità

L'attendibilità di un contratto dipende da quanti **segnali indipendenti** abbiamo e da se possiamo arrivare a un **documento** che lo conferma ([definizione della confidenza](../formato-classificazione/)).

- **CIG dal 2024: attendibilità più alta.** Si possono usare CPV, testo, aggiudicatario, accordo quadro e, quando c'è, il link ai documenti. L'esclusione certa usa più segnali concordi, e l'inclusione si può confermare con l'atto. È il periodo della **prima statistica di sovranità** (11/11/2026).
- **CIG 2020-2023: attendibilità media.** Ci sono gli stessi campi strutturati, ma i documenti si raggiungono solo con scraping dei siti degli enti o con l'accesso civico.
- **SmartCIG 2020-2023: attendibilità bassa sul singolo contratto.** C'è solo il testo dell'oggetto. Si esclude con certezza solo ciò che il testo dice chiaramente (lavori, farmaci, servizi sociali). Per le cifre si usa una **stima statistica da campione**, con intervallo, e non la somma dei contratti classificati uno per uno. Fanno eccezione gli affidamenti **in house** e quelli con importo alto, che si trattano a parte.
- **SmartCIG dal 2024:** importi piccolissimi (circa 5 mld/anno in tutto, ogni settore). Si contano e si stimano, senza approfondire.

**Attendibilità complessiva di un anno** = quota della spesa dell'anno decisa con confidenza alta + forbice sul resto (quota extra-UE se il resto fosse tutto italiano o tutto extra-UE). Si pubblica anno per anno: così si vede quanto pesa la differenza fra i due periodi.

## 5. Cosa cambia nell'imbuto

- L'universo comprende **CIG e SmartCIG** dal 2020.
- In SmartCIG gli strati che usano CPV, aggiudicatario o accordo quadro non si applicano. Restano esclusione dal testo, marchio nel testo (S4), in house come gruppo a sé e stima da campione.
- Ogni cifra porta il periodo e il dataset da cui viene.

## 6. Cosa resta da misurare

- La quota di CIG con link ai documenti e la quota di link funzionanti, per anno ([prima e dopo il 2024](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/metodo/acquisizione/prima-e-dopo-2024.md)).
- La quota di spesa ICT in SmartCIG 2020-2023 (dal testo) e la sua stima da campione.
- Il regime SmartCIG dal 2024, da verificare sulle delibere ANAC.

## Registro delle revisioni

| data | modifica |
|---|---|
| 2026-11-03 | prima versione: SmartCIG per anno e per fattispecie (V), campi disponibili per periodo, attendibilità per periodo, effetti sull'imbuto |
