---
title: "Analisi della spesa ICT della PA"
heroTitle: "Verso quale giurisdizione va l'euro che la PA spende in cloud?"
heroLead: "Quanto spendono gli enti pubblici italiani in servizi cloud e infrastrutture digitali, e quanta parte va a fornitori italiani, europei o alle big tech statunitensi. Ma prima bisogna sapere in che stato sono i dati pubblici che servono a misurarlo — ed è da lì che partiamo."
---

Questo è il secondo asse dell'[Osservatorio Nazionale Sovranità Digitale](https://osservatorio.mxmap.it/),
accanto alla posta elettronica degli enti misurata da [mxmap.it](https://mxmap.it/). La
definizione di sovranità è la stessa: conta la **giurisdizione giuridica del fornitore e del suo
gruppo**, non dove stanno fisicamente i server. Un servizio di un gruppo statunitense resta
soggetto al CLOUD Act anche se ospitato in un datacenter europeo.

<div class="callout note"><div class="callout-title">Lavori in corso, pubblicati man mano</div>
<p>I risultati escono quando li produciamo, non a lavoro finito. Ogni numero è riproducibile: file
originali con il loro <code>sha256</code>, script e verifiche sono nel
<a href="https://github.com/mxmap-it/analisi-spesa-ict">repository pubblico</a>.</p></div>

## Sei obiettivi, in quest'ordine

L'obiettivo vero è l'ultimo. Gli altri cinque vengono prima perché senza di essi l'ultimo non si
raggiunge in modo onesto: non si misura la spesa su dati di cui non si conoscono i buchi. Ma non
sono passaggi di servizio: ciascuno produce un risultato pubblico e utile da solo, e ciascuno è
pensato perché i problemi trovati vengano **corretti alla fonte** invece di essere aggirati ogni
volta.

<div class="obiettivo">
<h3><span class="ob-num">1</span> <a href="mirror/">Mirror dei dati di spesa pubblica</a> <span class="ob-stato in-corso">in corso</span></h3>

Una copia fedele, completa e sempre aggiornata di **tutti i dataset che riguardano, direttamente o
indirettamente, la spesa pubblica**: quelli già mappati da
[DataCivicLab](https://github.com/dataciviclab/source-observatory) e quelli che aggiungiamo noi.
Tutti i formati, tutte le versioni, usabile da chiunque con gli stessi percorsi della fonte
originale.

Serve perché **i dati pubblici spariscono**: Consip cancella oltre i tre anni, ANAC rimuove i file
mensili senza una regola scritta. Un archivio che conserva ogni versione con il suo `sha256` è
anche l'unico modo di dimostrare cosa era stato pubblicato e quando.

<div class="ob-risultati">

Finora

- ANAC: **1.801 risorse** censite in 70 dataset, in CSV, JSON e TTL; archiviazione in corso.
- Nel registro anche Consip, SIOPE, PA Digitale 2026, IndicePA e il catalogo cloud di ACN.
- [Perimetro delle fonti](progetto/perimetro-fonti/): delle 36 fonti di DataCivicLab, 14
  riguardano la spesa.

</div>
</div>

<div class="obiettivo">
<h3><span class="ob-num">2</span> <a href="disponibilita/">Disponibilità, accesso e integrità dei dati</a> <span class="ob-stato avviato">avviato</span></h3>

Due domande distinte. **I dati si possono prendere?** Ci sono tutti, con la cadenza promessa, senza
blocchi, con una documentazione che corrisponde a ciò che il server serve davvero? **I dati presi
sono corretti?** Identificativi validi, date plausibili, importi coerenti, collegamenti fra
dataset che si chiudono.

E una terza che le tiene insieme: **ciò che viene dichiarato corrisponde a ciò che viene
pubblicato?** Le difformità fra catalogo e file, fra un formato e l'altro, fra due vie di accesso
allo stesso dato, sono spesso il problema più grave e il meno visibile.

<div class="ob-risultati">

Finora

- [Rapporto ANAC, ottobre 2026](rendiconti/anac-2026-10/): 18 problemi di disponibilità e 33
  controlli di integrità.

</div>
</div>

<div class="obiettivo">
<h3><span class="ob-num">3</span> <a href="enti/">Un rendiconto per ogni ente, misurato nel tempo</a> <span class="ob-stato avviato">avviato</span></h3>

Per ogni autorità che produce i dati: **cosa va sistemato**, con la prova, e una misura ripetuta che
dice **se è stato sistemato oppure no**. Un problema segnalato una volta e poi dimenticato non
migliora nulla; un problema misurato ogni mese e pubblicato finché non è risolto, sì.

Ogni problema entra in un registro con un identificativo stabile e un ciclo di vita: aperto,
segnalato, risposta ricevuta, risolto oppure cronico. I problemi cronici restano in evidenza a
tempo indeterminato.

<div class="ob-risultati">

Finora

- [Cosa ogni autorità dovrebbe garantire](progetto/attese-autorita/), con lo stato atteso,
  confermato o smentito, e i contatti verificati.
- La misura nel tempo parte con le prossime sonde mensili.

</div>
</div>

<div class="obiettivo">
<h3><span class="ob-num">4</span> <a href="rendiconti/">Rapporti, presentazioni ed evidenze empiriche</a> <span class="ob-stato avviato">avviato</span></h3>

Per ogni ente e per ogni dataset problematico: un rapporto leggibile da chi deve intervenire, con
gli **allegati che dimostrano il problema** — i file analizzati con il loro hash, le richieste fatte
al server con le risposte ottenute, gli script che riproducono ogni numero.

Non sono giudizi sul lavoro delle amministrazioni: sono l'elenco delle cose che, se corrette,
renderebbero i loro dati pienamente utilizzabili. Per questo ogni rapporto dice anche cosa
funziona bene.

<div class="ob-risultati">

Finora

- [Rapporto ANAC](rendiconti/anac-2026-10/) con
  [gli allegati](https://github.com/mxmap-it/analisi-spesa-ict/tree/main/report/anac): manifest
  dei file, esiti dei controlli, esiti della sonda.

</div>
</div>

<div class="obiettivo">
<h3><span class="ob-num">5</span> <a href="strumenti/">Gli strumenti: quali usiamo, quali no, e perché</a> <span class="ob-stato fatto">prima stesura</span></h3>

Esistono già molti strumenti per scaricare e analizzare i dati aperti italiani, pubblici, civici e
commerciali. Li abbiamo censiti per dire **quali riusiamo, quali scartiamo, e con quale motivo**.

**Principio di progetto: scrivere meno codice possibile.** Riusiamo tutto ciò che è libreria o
servizio invocabile — il motore di pipeline di DataCivicLab, le CLI di onData, i moduli di
ingestione di AgID, i validatori europei — e scriviamo solo ciò che non esiste. Il codice che non
si scrive non va mantenuto.

</div>

<div class="obiettivo finale">
<h3><span class="ob-num">6</span> <a href="spesa-ict/">La spesa ICT in cloud, per giurisdizione</a> <span class="ob-stato da-fare">alla fine</span></h3>

L'obiettivo per cui il progetto esiste. **Quanto spendono gli enti pubblici italiani in servizi
cloud esterni e in datacenter e infrastrutture proprie**, e quanta parte va a:

<p><span class="bucket" style="background:#2E7D32"></span>fornitori italiani
<span class="bucket" style="background:#003DA5"></span>fornitori europei
<span class="bucket" style="background:#CE1126"></span>big tech extra-europee
<span class="bucket" style="background:#607d8b"></span>non attribuibile</p>

Con la stessa classificazione e la stessa definizione di sovranità di mxmap.it. Come **processo
ripetibile**: ricostruito sugli anni passati, aggiornato nell'anno in corso, rieseguibile negli
anni successivi senza rifare il lavoro.

Non ci sono altri obiettivi di analisi: **solo la spesa ICT che incide sulla sovranità**. Questo
punto si elabora per ultimo, perché è l'unico che dipende da tutti gli altri.

</div>

## ANAC in quattro numeri

<div class="cifre">
  <div class="cifra"><b>11 su 23</b><span>mesi OCDS con contenuto distinto: gli altri servono un file identico a quello di un altro mese</span></div>
  <div class="cifra"><b>4,1×</b><span>sovrastima delle dimensioni dichiarate dal catalogo, su 1.797 risorse</span></div>
  <div class="cifra"><b>1.951.844</b><span>righe del dataset dei CUP con «ND» al posto del codice</span></div>
  <div class="cifra"><b>17</b><span>CIG non validi su 4,8 milioni: ciò che funziona bene, funziona molto bene</span></div>
</div>

Il dettaglio è nel [rapporto ANAC](rendiconti/anac-2026-10/).
