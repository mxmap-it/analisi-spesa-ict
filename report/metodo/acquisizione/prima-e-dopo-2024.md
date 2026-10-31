# Documenti degli acquisti: cosa cambia prima e dopo il 2024

Stato: considerazione analitica (31/10/2026), **riferita, da verificare** sulle delibere ANAC 261, 263 e 264/2023 (e successive modifiche) e da misurare sul mirror ANAC. Ticket #57. Ogni affermazione normativa va passata a V aprendo la fonte prima di pubblicarla come fatto.

## 1. Il quadro normativo, in sintesi (R)

- **Fino al 31/12/2023** (d.lgs. 50/2016):
  - l'ente pubblica bandi, determine e contratti sul proprio sito (Amministrazione trasparente, albo pretorio), ciascuno con il proprio software;
  - ad ANAC arrivano dati strutturati parziali: SIMOG/SmartCIG e il file XML della legge 190/2012, art. 1 c. 32;
  - non c'è un collegamento obbligatorio, e leggibile da una macchina, tra CIG e documenti.
- **Dal 1/1/2024** (d.lgs. 36/2023, artt. 19-36, digitalizzazione del ciclo di vita):
  - ogni fase passa da **piattaforme di e-procurement certificate**, che trasmettono le schede alla **BDNCP** (art. 23): programmazione, indizione, aggiudicazione, esecuzione, conclusione;
  - la trasparenza (art. 28) si assolve trasmettendo i dati alla BDNCP; la sezione Amministrazione trasparente può limitarsi a un link, salvo gli atti elencati nell'allegato della delibera 264/2023;
  - i documenti di gara stanno sulla piattaforma dell'ente, e lo schema allineato agli eForms prevede il loro indirizzo;
  - gli affidamenti diretti entrano nel ciclo; sotto i 5.000 € tramite l'interfaccia ANAC (PCP). Regime transitorio da verificare.

## 2. Cosa possiamo fare di diverso

| | prima del 2024 | dal 2024 |
|---|---|---|
| dove sono i documenti | sito dell'ente (AT, albo), formati e software eterogenei | piattaforma certificata dell'ente; link attesi nei dati |
| come si trovano | ricerca o scraping del sito, riconoscimento del software di trasparenza, poi identificazione dell'atto che cita il CIG | lettura del puntatore nei dati BDNCP o eForms, poi scaricamento |
| affidamenti diretti | spesso solo determina in albo, a volte nulla | dovrebbero esserci scheda e documenti |
| esecuzione e importo pagato | quasi assenti | schede di esecuzione e conclusione dovute |
| livello di acquisizione tipico | L4-L5 (scraping o ricerca) e L7 (FOIA) | L1-L3 (puntatori strutturati e piattaforme), L4+ solo per il residuo |
| cosa resta comunque assente | prodotto, produttore, sede dei dati, giurisdizione (R16, R21), composizione PSN (R20) | idem: il Codice nuovo dà la tracciabilità (chi, quanto, quando), non cosa si compra né sotto quale giurisdizione |

## 3. La misura da fare (todo, dalla settimana del 2/11/2026)

Sul mirror ANAC, per i CIG dal 2024 (tutto l'universo e, separatamente, il sottoinsieme cloud/IT dell'imbuto):

1. **Presenza del puntatore:** quota di CIG con un link ai documenti, per fonte (dataset ANAC, OCDS, TED eForms), per fase (indizione, aggiudicazione, esecuzione), per tipo di procedura (affidamento diretto contro gara) e per piattaforma.
2. **Funzionamento del puntatore:** campione stratificato per piattaforma, con richieste rispettose (robots, niente aggiramenti), classificato in:
   - risponde 200 e porta al documento;
   - risponde ma è una pagina generica o di login;
   - errore 4xx/5xx o timeout;
   - dominio inesistente.
3. **Coerenza:** il documento scaricato cita quel CIG? È il documento giusto (bando, determina, contratto)? È leggibile da una macchina (testo contro scansione)?
4. **Completezza delle fasi:** quota di CIG con schede di esecuzione e conclusione popolate, rispetto a quelle dovute.
5. **Confronto con il prima:** stessi indicatori sul 2022-2023, dove ci si aspetta quasi zero puntatori. Misura dell'effetto della riforma.
6. **Costo per documento** a ogni livello, per decidere dove conviene salire.

Esito: rendiconto pubblicato (con la differenza tra dovuto e pubblicato), metriche in `tools/verifiche/` riproducibili, nuove voci di raccomandazione dove i puntatori mancano o non funzionano.

## 4. Il percorso multi-livello che ne deriva

Si sale di livello solo per il residuo che il livello precedente non ha risolto (principio a imbuto):

1. **Analisi dei dati strutturati** (L0-L1): oggetto, CPV, lotto, convenzione, base di conoscenza. Chiude il facile ed esclude il certo.
2. **Puntatori strutturati** (L1-L3, soprattutto dal 2024): link in BDNCP, OCDS ed eForms, poi scaricamento, archivio sha256 e parsing (testo o OCR).
3. **Scraping con identificazione** (L4, soprattutto prima del 2024 e per i link rotti): riconoscimento del software di trasparenza dell'ente, crawler per famiglia di software, identificazione dell'atto che cita il CIG, poi scaricamento e parsing.
4. **Ricerca assistita da modello** (L5): per i casi rimasti, a consumo di token, solo sui contratti significativi.
5. **Segnale umano** (L6): annotazioni, con la segnalazione «servono documenti esterni».
6. **Accesso civico puntuale e massivo** (L7, progetto a parte, #58): solo per ciò che è significativo e non pubblicato, con richiesta generata dai dati (ente, CIG, documento mancante).

Ogni documento registra il livello che l'ha trovato (`spesaict.atto/1`). Ogni livello ha copertura e costo misurati, e i buchi diventano richieste di policy.
