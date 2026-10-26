# analisi-spesa-ict

**Quanta parte della spesa ICT della Pubblica Amministrazione italiana va a fornitori sotto
giurisdizione italiana, europea o extra-europea.**

Secondo asse dell'[Osservatorio Nazionale Sovranità Digitale](https://osservatorio.mxmap.it/),
accanto alla posta elettronica misurata da [mxmap.it](https://mxmap.it/). Stessa definizione di
sovranità — **giurisdizione giuridica del fornitore e del suo gruppo**, non collocazione fisica
dei server — e stessa classificazione a quattro categorie: `it`, `eu_non_it`, `extra_eu`,
`unknown`.

La domanda non è *quanto* spende la PA in digitale, ma **verso quale giurisdizione va l'euro
speso**.

## Obiettivo

**Misurare quanto spendono gli enti pubblici italiani in servizi cloud esterni e in datacenter e
infrastrutture proprie, e quanta parte di quella spesa va a fornitori italiani, europei o
extra-europei** — le big tech statunitensi esposte al CLOUD Act in primo luogo. Un processo
ripetibile: gli anni passati, l'anno in corso, quelli futuri. Non ci sono altri obiettivi di
analisi oltre alla spesa ICT che incide sulla sovranità.

È **l'ultimo risultato a uscire**. Prima vengono cinque passi intermedi, ciascuno pubblico e utile
da solo, e ciascuno pensato perché i problemi trovati vengano corretti alla fonte:

1. **Mirror** di tutti i dataset che riguardano, direttamente o indirettamente, la spesa pubblica:
   completo, aggiornato, usabile da chiunque.
2. **Disponibilità e integrità**: i dati ci sono tutti, sono corretti, corrispondono a ciò che
   viene dichiarato?
3. **Stato per ente**: cosa va sistemato, con la prova, e se viene sistemato, misurato nel tempo.
4. **Rendiconti** con le evidenze, presentati alle autorità che producono i dati.
5. **Strumenti**: riusare quelli esistenti e scrivere meno codice possibile.

Il dettaglio è nella [roadmap](https://analisi-spesa-ict.mxmap.it/progetto/roadmap/).

---

## Dove sono le cose

| Cosa | Dove |
|---|---|
| Il sito, con i rendiconti pubblicati | https://analisi-spesa-ict.mxmap.it/ |
| **Analisi tecnica**: fonti, accesso, strade scartate, strumenti, architettura | [sito/content/progetto/analisi-tecnica.md](sito/content/progetto/analisi-tecnica.md) · [sul sito](https://analisi-spesa-ict.mxmap.it/progetto/analisi-tecnica/) |
| **Decisioni prese**, con data e motivo | [DECISIONI.md](DECISIONI.md) |
| **Stato del lavoro** e punto di ripresa | [STATE.md](STATE.md) |
| Roadmap, perimetro delle fonti, attese verso le autorità | [sito/content/progetto/](sito/content/progetto/) |
| Ticket e avanzamento | [Board](https://github.com/orgs/mxmap-it/projects/1) · [Issues](https://github.com/mxmap-it/analisi-spesa-ict/issues) |
| Strumenti | [tools/](tools/) |

Il lavoro gira sul server di mxmap.it: ANAC respinge gli user-agent non-browser, i file sono
grandi e i job lunghi. Il sito è generato con Hugo da `sito/` in `docs/`, con lo stesso tema di
[osservatorio.mxmap.it](https://osservatorio.mxmap.it/).

## Licenze

- **Codice**: libero. I pacchetti che vogliamo far accettare a monte in progetti permissivi restano
  MIT e scritti come libreria pura; il resto può essere AGPL dove solleviamo codice AGPL.
- **Dati e documentazione**: **CC BY-SA 4.0**, come il resto dell'Osservatorio.
- **Dati di origine**: ANAC CC BY-SA 4.0, Consip CC BY 4.0, SIOPE CC BY 4.0, GLEIF CC0, IndicePA
  CC BY 4.0. Ogni dataset derivato cita la fonte e la data di acquisizione.

