---
title: "Metodo: documenti pubblicati e mancanti delle convenzioni ICT"
date: 2026-11-06
lastmod: 2026-11-06
description: "Come censiamo, file per file, i documenti pubblicati e mancanti delle convenzioni e degli accordi quadro ICT: fonti, tre metodi, criticità 1-3, livelli [V]/[R], ricontrollo dal vivo, blocchi, accesso civico."
weight: 25
---

Versione 1.0 del 6/11/2026 (#62). Si applica alla [base dati delle convenzioni](/convenzioni/), al
[rapporto sulla trasparenza](/rendiconti/convenzioni-trasparenza/) e all'inventario
[`documenti-mancanti.csv`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/database/documenti-mancanti.csv).

## In sintesi

- Per ogni convenzione o accordo quadro ICT della base dati elenchiamo **i documenti pubblicati** (con copia archiviata e sha256) e
  **quelli che mancano**, uno per riga.
- Un documento è «mancante» per uno di tre motivi: **numerazione** (manca l'Allegato 12 fra l'11 e il 13), **rimando** (un atto
  pubblicato lo cita ma non è allegato), **atteso** (la legge o la prassi lo prevedono: aggiudicazione, offerte, listini, flussi di monitoraggio…).
- Ogni mancante ha una **criticità** da 1 a 3 (3 = decisivo per stabilire la giurisdizione del prodotto o per controllare la spesa)
  e un **livello**: [V] se abbiamo ricontrollato la pagina ufficiale dal vivo e il file non c'è, [R] se è dedotto o da verificare.
- Non aggiriamo login, CAPTCHA o registrazioni: i blocchi si registrano e si provano a mano.
- Per i mancanti di criticità 2 e 3 prepariamo **bozze di accesso civico** raggruppate per destinatario; nessuna parte senza l'approvazione di Fabio Pietrosanti.

## Fonti e livelli di acquisizione

1. **BDNCP ANAC** (nostro mirror): CIG padre e derivati, valori dichiarati.
2. **Pagina ufficiale dell'iniziativa** (consip.it, piattaforme degli aggregatori): l'elenco dei file linkati, con sha256 dell'HTML.
   I file e il contenuto degli zip si archiviano nell'archivio content-addressed (sha256, data di acquisizione).
3. **Acquistinretepa** (schede pubbliche, senza login) e **open data Consip** (ordinato per anno e lotto).
4. **Fonti non ufficiali** (atti di enti aderenti, ricerca web): mostrate a parte, non cancellano la mancanza.
5. **Accesso civico generalizzato** (art. 5 c. 2 d.lgs. 33/2013): ultima risorsa.

I livelli L0-L7 dell'acquisizione sono descritti in [Acquisizione dei documenti](/progetto/acquisizione-documenti/).

## I tre metodi

| Metodo | Come | Evidenza registrata |
|---|---|---|
| numerazione | Si leggono i nomi dei file pubblicati (pagina e contenuto degli zip) e si cercano i numeri saltati in ciascuna serie: «Allegato», «Appendice … al Capitolato», «Annesso», sub-allegati con lettera. | numeri presenti, file vicini con sha256; se il numero è citato in un testo, anche la citazione |
| rimando | Si estrae il testo dei PDF archiviati pagina per pagina (`tools/convenzioni/rimandi_documenti.py`) e si cercano i rimandi ad allegati, appendici e annessi; si scartano i rimandi a norme (allegati del codice, decreti). Il rimando non pubblicato diventa una riga. | citazione, documento, pagina, sha256, numero di citazioni |
| atteso | Per ogni tipo di documento atteso per legge o prassi (classi [C1-C8](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/database/carenze.yaml) e inventario della base dati), se non c'è sulla pagina ricontrollata. Si aggiungono gli atti di proroga, incremento del massimale o modifica (art. 120 d.lgs. 36/2023), la cui esistenza però non è accertata. | stato dell'inventario, classe di carenza, esito del ricontrollo |

I tre metodi si sommano: una riga può avere metodo «numerazione;rimando» quando il numero saltato è anche citato.
Limite noto: il metodo «rimando» trova anche allegati che per natura non si pubblicano (gli allegati dell'offerta del concorrente):
restano nell'inventario con la nota «parte dell'offerta» perché sono proprio i documenti che servono (listini, elenchi di prodotti).

## Criticità

| Criticità | Criterio | Esempi |
|---|---|---|
| 3 | decisivo per la giurisdizione del prodotto o per controllare la spesa | listini, offerte economiche e tecniche, elenco prodotti e marchi, flussi di transato/erogato, ordinativi, Piani dei fabbisogni, region e data center |
| 2 | utile al controllo, non decisivo | capitolato, convenzione stipulata, aggiudicazione, livelli di servizio, atti di modifica, flussi di monitoraggio non economici |
| 1 | formale | moduli di dichiarazione, garanzie, determina, bando, chiarimenti |

La criticità si assegna per regole sul titolo (`tools/convenzioni/documenti_mancanti.py`): è una classificazione automatica, da rivedere caso per caso prima di ogni richiesta.

## Livelli [V] e [R]

- **[V] verificato**: la pagina ufficiale è stata riscaricata dal vivo alla data indicata (`ricontrollo-pagine.json`, sha256 dell'HTML) e il file non c'è.
- **[R] riferito o da verificare**: pagina non individuata, non ricontrollata, oppure mancanza dedotta (es. atti di modifica la cui esistenza non è nota).

## Ricontrollo dal vivo e blocchi

Prima di dichiarare un mancante si riscarica la pagina ufficiale (`tools/convenzioni/ricontrollo_pagine.py`) con User-Agent da browser
più l'URL del progetto, almeno 5 secondi fra le richieste, al massimo 10 in parallelo. **Mai** CAPTCHA, login, registrazioni, proxy.
Una risposta 401/403/429, un errore o una maschera di login si registra in
[`blocchi-accesso.csv`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/database/blocchi-accesso.csv) con data e codice;
la colonna `dietro_login` dell'inventario vale «sì» solo se il blocco è stato osservato, «ignoto» se il documento potrebbe stare in un'area
riservata (es. prezzi e residuo su acquistinretepa) ma non l'abbiamo provato. I casi «ignoto» si provano a mano in un giro assistito.

## Ciclo dell'accesso civico

bozza → approvazione di Fabio Pietrosanti → inviata (data, protocollo) → risposta (data) → esito (accolta, parziale, diniego, silenzio).
Lo stato sta in [`registro.csv`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/accesso-civico/registro.csv),
una riga per istanza; il legame con il singolo documento sta nella colonna `bozza_accesso_civico` dell'inventario. Le pagine delle
convenzioni mostrano una bozza non approvata solo come «in preparazione». Le bozze per i documenti mancanti sono raggruppate per destinatario
e contengono l'elenco analitico dei mancanti.

## Contributi

Chi ha uno dei documenti mancanti può segnalarlo sul [gruppo Telegram](https://t.me/+Ot-M_g0dkh1kMGI0) o aprendo una
[issue su GitHub](https://github.com/mxmap-it/analisi-spesa-ict/issues/new). Servono il file, la fonte (dove e quando è stato
ottenuto) e, se possibile, l'atto che lo accompagna. Verifichiamo l'autenticità (sha256, confronto con la fonte, firma digitale se presente) e lo
pubblichiamo come «fonte non ufficiale» finché la centrale non lo pubblica.

## Ripetibilità

`python tools/verifiche/convenzioni_mancanti.py` da un clone pulito rigenera l'inventario, controlla che non cambi e ricalcola i buchi di
numerazione per seconda via.

## Registro delle revisioni

| Versione | Data | Cosa è cambiato |
|---|---|---|
| 1.0 | 6/11/2026 | prima versione: tre metodi, criticità, livelli, ricontrollo, blocchi, ciclo dell'accesso civico, contributi |
