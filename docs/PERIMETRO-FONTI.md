# Quali fonti entrano nel perimetro

**Ultimo aggiornamento:** 2026-10-26

## La regola

> Entrano nel perimetro **solo le fonti che riguardano, direttamente o indirettamente, la spesa
> pubblica.** Tutto il resto resta fuori, per quanto sia buon dato aperto.

Tre livelli:

| Livello | Significato | Esempi |
|---|---|---|
| **diretta** | Misura denaro pubblico che esce: impegni, pagamenti, aggiudicazioni, ordini, aiuti, stipendi | ANAC, Consip, SIOPE, BDAP, INPS |
| **indiretta** | Non misura la spesa, ma serve a **leggerla o ad attribuirla**: anagrafiche dei soggetti, classificazioni, denominatori di confronto | IndicePA, ISTAT per i conti della PA, catalogo cloud ACN, anagrafiche d'impresa |
| **fuori** | Qualunque altro dato aperto | ambiente, mobilità, elezioni, giustizia, sanità non finanziaria, cultura |

Una fonte **indiretta** entra solo se risponde a una domanda che ci serve davvero. L'anagrafe degli
enti entra perché senza di essa non si sa chi ha speso; il catalogo dei servizi cloud qualificati
entra perché serve ad attribuire la giurisdizione di un fornitore. Il parco veicoli no.

## Perché la regola serve

Il progetto riusa `source-observatory` di DataCivicLab, che monitora **36 fonti** pubbliche
italiane scelte con un criterio diverso dal nostro: loro fanno scouting di dati aperti in
generale, noi misuriamo la spesa. Senza un confine scritto, estendere il loro lavoro
significherebbe ereditare il loro perimetro — e trovarsi a specchiare la qualità dell'aria.

Vale anche nell'altro senso: quando contribuiremo a monte il livello per risorsa, contribuiremo
**solo le fonti di spesa**, lasciando a loro le altre.

## Le 36 fonti di DataCivicLab, classificate

Classificazione nostra, fatta sui nomi delle fonti e sui dataset che il loro registry dichiara in
uso. Le voci marcate *da verificare* non sono state controllate una per una: vanno confermate
prima di essere adottate.

### Diretta — entrano

| Fonte | Cosa dà |
|---|---|
| `anac` | Appalti e contratti pubblici. **Già nostra fonte principale** |
| `consip_open_data` | Acquisti centralizzati, ordini MePA e convenzioni. **Già nostra** |
| `openbdap` | Bilancio dello Stato, gestione delle spese, bilanci degli enti |
| `opencoesione` | Costo, impegni e pagamenti dei progetti di coesione |
| `opencivitas` | Spesa storica e fabbisogni standard dei comuni |
| `mimit_rna` | Registro Nazionale Aiuti di Stato: aiuti erogati alle imprese |
| `inps` | Spesa previdenziale e prestazioni |
| `aifa` | Spesa farmaceutica |
| `dait` *(da verificare)* | Finanza locale, certificati di bilancio dei comuni |
| `noipa_sparql` *(da verificare)* | Stipendi del personale pubblico. **Nessun dataset in uso da loro**: potrebbe essere un giacimento intatto sulla spesa per il personale |
| `ministero_salute` *(da verificare)* | Da distinguere: la spesa sanitaria entra, l'epidemiologia no |

### Indiretta — entrano solo per quello che servono

| Fonte | A cosa ci serve |
|---|---|
| `agid` | Catalogo nazionale dei dati aperti, Piano Triennale, spesa ICT |
| `istat_sdmx` | Conti delle amministrazioni pubbliche e COFOG: denominatori e confronti europei |
| `mef_irpef` | Base imponibile per rapportare la spesa al territorio. Sono entrate, non spesa |
| `unioncamere` *(da verificare)* | Anagrafiche d'impresa, per riconoscere i fornitori |
| `pagopa` *(da verificare)* | Pagamenti **verso** la PA: utile come controparte, non è spesa |
| `mit_opendata` *(da verificare)* | Opere pubbliche, se e quando serviranno |

### Fuori — non le prendiamo

`aci`, `adm_opendata`, `agcm`, `art_opendata`, `cortecostituzionale`, `dati_camera`,
`dati_cultura`, `dati_senato`, `eligendo`, `giustizia_statistiche`, `inail_opendata`,
`ispra_linked_data`, `lavoro_opendata`, `mim_opendata`, `ministero_interno`,
`ministero_turismo_opendata`, `mur_ustat`, `openga` *(sigla non chiarita)*, `terna_opendata`.

Sono ventidue fonti su trentasei: **più della metà del loro perimetro è fuori dal nostro**. È la
misura di quanto serviva scrivere questa regola.

## Il nostro perimetro oggi

Le fonti nel nostro registry, con il livello di relazione con la spesa:

| Fonte | Livello | Stato |
|---|---|---|
| ANAC | diretta | **in archiviazione**, 1.797 risorse, tutti i formati |
| Consip | diretta | nel registry, da archiviare |
| SIOPE (RGS) | diretta | nel registry, da archiviare |
| PA Digitale 2026 (DTD) | diretta, specifica ICT | nel registry |
| IndicePA | indiretta | nel registry |
| ACN, catalogo cloud qualificati | indiretta, serve alla giurisdizione | sondata, risponde 403 |

Da aggiungere, in ordine di utilità per l'obiettivo ICT: **BDAP** per la spesa di cassa e di
bilancio, **OpenCUP** e **ItaliaDomani** per i finanziamenti, **GLEIF** e le anagrafiche d'impresa
per l'attribuzione di giurisdizione, **CPT** e **ISTAT** come contesto.

## Casi limite già decisi

- **Le entrate non sono spesa.** IRPEF dichiarato, accise, pagamenti verso la PA via pagoPA:
  entrano solo come denominatore, e sempre marcati come tali.
- **La sanità va divisa.** Il conto economico del Servizio Sanitario Nazionale è spesa; i dati
  epidemiologici no.
- **Le anagrafiche entrano se identificano chi spende o chi incassa.** IndicePA sì, l'anagrafe
  delle scuole no, a meno che non serva a un'attribuzione specifica.
- **Un dato ICT non finanziario entra se serve all'attribuzione.** Il catalogo dei servizi cloud
  qualificati non misura spesa, ma dice chi è il fornitore e con quale qualificazione: è il ponte
  verso la giurisdizione.
