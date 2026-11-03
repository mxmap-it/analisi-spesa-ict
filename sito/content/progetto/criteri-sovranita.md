---
title: "Criteri di sovranità: quando una spesa cloud è sovrana"
date: 2026-11-03
description: "Le regole con cui qualifichiamo come sovrana, europea o extra-UE una spesa cloud della PA: chi eroga il servizio, chi lo controlla, che ruolo ha. Eccezioni, casi particolari, incertezze. Documento aperto a critiche e proposte."
weight: 16
---

## In sintesi

1. **Conta chi eroga il servizio, e chi lo controlla.** La sovranità dipende dal **controllo giuridico** del soggetto che **eroga direttamente** l'infrastruttura o il servizio cloud: è sovrana se quel soggetto non è esposto al CLOUD Act statunitense o a normative extra-UE analoghe (criterio di immunizzazione giuridica, sul modello SecNumCloud).
2. **Non contano il luogo dei data center né l'origine del software.** Un prodotto statunitense gestito e offerto come servizio da un soggetto italiano a controllo italiano, in Italia, è sovrano. Il software extra-UE si registra come **dipendenza tecnologica**, in un campo separato.
3. **Conta il ruolo.** Chi fa consulenza, progettazione, migrazione o gestione **su infrastruttura del cliente o di terzi** non sposta la qualificazione: la sovranità segue chi gestisce l'infrastruttura.
4. **Non si inferisce.** Ciò che non è accertato su una fonte che lo renda certo resta **incerto**, con l'azione per accertarlo. Ogni qualificazione passa per un **agente di revisione** dedicato alla sovranità.

## Le regole

### R-S1. Erogatore e ruolo
Per ogni servizio si individua il ruolo di chi lo fornisce:
- **eroga il servizio cloud**: IaaS, PaaS, SaaS, hosting (anche dedicato), servizi gestiti a canone dai propri centri. In questo caso la sua catena di controllo decide la qualificazione;
- **opera su infrastruttura altrui**: consulenza, sviluppo, migrazione, system management. In questo caso decide chi gestisce l'infrastruttura su cui opera; il controllo del consulente si registra solo come lente fornitore.

### R-S2. Catena di controllo
Si risale fino al controllante ultimo, per ogni anno: il controllo può cambiare nel tempo (esempi accertati: TIM sotto Poste Italiane, e quindi sotto il MEF, dal 2/10/2026; Tiscali sotto Jefferies, USA, dal 2024). La qualificazione vale per il periodo in cui la catena è accertata.

### R-S3. Esiti
| esito | quando |
|---|---|
| **IT** | erogatore a controllo italiano, non esposto a normative extra-UE |
| **UE** | erogatore a controllo di un paese UE, non esposto a normative extra-UE |
| **sovrano non UE** | erogatore a controllo di un paese europeo non soggetto al CLOUD Act (es. **Svizzera**, Fabio 3/11/2026): conteggiato fra i sovrani, con il paese registrato (CH) |
| **extra-UE** | erogatore esposto al CLOUD Act o a normative extra-UE analoghe |
| **incerto** | ruolo, erogatore o catena non accertati; si registra l'azione per accertarli |

### R-S4. Prodotto
L'origine del prodotto (Microsoft, Oracle, VMware, Fortinet…) **non decide** la sovranità. Si registra come dipendenza tecnologica. Decide solo se il produttore è anche chi **eroga** il servizio.

### R-S5. Licenze
Una licenza installata nei sistemi dell'ente (on-premise) **non è spesa cloud**: si conta a parte. Un abbonamento SaaS (es. Microsoft 365) è cloud erogato dal produttore, quindi segue la catena di controllo del produttore.

## Eccezioni e casi particolari incontrati

| caso | regola | fonte della decisione |
|---|---|---|
| **Rivendita di servizi hyperscaler** (es. PSN che offre Azure erogato da Microsoft) | l'erogatore giuridico è l'hyperscaler: **extra-UE**, anche se il rivenditore è italiano. I servizi che il rivenditore eroga in proprio seguono il suo controllo | Fabio, 3/11/2026 |
| **Hosting dedicato** | è cloud: ospita servizi per conto dell'ente | Fabio, 3/11/2026 |
| **Affidamenti intragruppo o in house** (es. Trenitalia → FSTechnology) | si qualificano solo sapendo che cosa usa l'affidatario e come eroga. Se usa un hyperscaler extra-UE, quella parte non è sovrana. Finché non è noto: **incerto** | Fabio, 3/11/2026 |
| **Software USA gestito in proprio da un operatore italiano** (es. Sistema Cloud Toscana su VMware/Microsoft; servizi di sicurezza a canone su tecnologie USA) | sovrano se l'operatore eroga e controlla il servizio; il software è dipendenza tecnologica | Fabio, 29/10 e 3/11/2026 |
| **Società italiana controllata da un gruppo USA** | l'esposizione al CLOUD Act della controllata è una qualificazione giuridica: si considera solo quando la società **eroga** il servizio. Se non è accertata, resta incerto | revisione, 3/11/2026 |
| **Catena che termina in Svizzera** | sovrana (la Svizzera non è soggetta al CLOUD Act) | Fabio, 3/11/2026 |
| **Licenze miste** (es. Microsoft Enterprise Agreement: on-premise e SaaS insieme) | si separano le quote; finché non sono note, la quota cloud è un intervallo e il resto incerto | revisione, 3/11/2026 |
| **Servizi applicativi «in ottica cloud»** | servizi professionali, non cloud; gli attuativi con licenze, hosting o infrastruttura si valutano uno per uno | revisione, 3/11/2026 |

## Cosa si porta a incertezza
- ruolo dell'erogatore non scritto negli atti;
- catena di controllo senza fonte (società non quotate, fondi di investimento di paese non accertato);
- quote di servizi diversi dentro uno stesso contratto (es. PSN: servizi propri e servizi hyperscaler);
- importi dichiarati implausibili (massimali copiati, errori di un fattore mille).

Ogni incertezza ha una riga nel [registro delle incertezze](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/incertezze.md) con l'azione per chiuderla.

## Cosa non facciamo
- Non contattiamo enti, autorità o fornitori senza decisione di Fabio, e non facciamo richieste che richiedono di dichiarare indirizzi personali (es. le API della SEC).
- Non deduciamo la sovranità dalla sede dei data center, dal marchio del prodotto o dalla nazionalità del consulente.

## Critiche e proposte
Questi criteri sono aperti a critiche e proposte di miglioramento. Si commentano con una issue sul [repository del progetto](https://github.com/mxmap-it/analisi-spesa-ict/issues) (etichetta `criteri-sovranita`). Ogni modifica accolta entra nel registro delle revisioni qui sotto e in [DECISIONI.md](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/DECISIONI.md).

## Registro delle revisioni
| data | modifica |
|---|---|
| 2026-10-29 | sovranità = controllo giuridico dell'operatore, non origine del software |
| 2026-11-03 | prima versione del documento: ruolo dell'erogatore, catena di controllo per anno, licenze, eccezioni (rivendita di servizi hyperscaler, hosting dedicato, intragruppo, Svizzera sovrana), regola «non inferire» con revisore di sovranità |
