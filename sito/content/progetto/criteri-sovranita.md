---
title: "Criteri di sovranità: quando una spesa cloud è sovrana"
date: 2026-11-03
description: "Le regole con cui qualifichiamo come sovrana, europea o extra-UE una spesa cloud della PA: chi eroga il servizio, chi lo controlla, che ruolo ha. Eccezioni, casi particolari, incertezze. Documento aperto a critiche e proposte."
weight: 16
---

## In sintesi

1. **Extra-UE = servizio cloud delle big tech statunitensi.** Un servizio cloud erogato da **Microsoft, Google, Amazon o Oracle** (quando vendono cloud) è sempre soggetto al CLOUD Act, **chiunque lo rivenda**: PSN, TIM, un system integrator. Le misure tecniche (chiavi gestite dal rivenditore, region dedicate, gestione «managed») non danno immunità (vedi l'[analisi del PSN dell'Osservatorio](https://osservatorio.mxmap.it/psn/)).
2. **Il resto segue chi eroga il servizio in proprio.** Un operatore italiano o europeo che eroga cloud dalla propria infrastruttura è sovrano, anche se usa software statunitense (VMware, Microsoft…): il software si registra come **dipendenza tecnologica**, in un campo separato. Non contano il luogo dei data center né l'origine del prodotto.
3. **Conta il ruolo.** Chi fa consulenza, progettazione, migrazione o gestione **su infrastruttura del cliente o di terzi** non sposta la qualificazione: la sovranità segue chi gestisce l'infrastruttura.
4. **Niente spippolamenti societari.** Non contano la quotazione in borsa né i veicoli di investimento che detengono le quote. Una controllante statunitense conta solo se è **essa stessa un erogatore di servizi cloud**.
5. **Non si inferisce.** Ciò che non è certo su fonte resta **incerto**, con l'azione per accertarlo. Ogni qualificazione passa per un **agente di revisione** dedicato alla sovranità.

## Le regole

### R-S1. Erogatore e ruolo
Per ogni servizio si individua il ruolo di chi lo fornisce:
- **eroga il servizio cloud**: IaaS, PaaS, SaaS, hosting (anche dedicato), servizi gestiti a canone dai propri centri. In questo caso la sua catena di controllo decide la qualificazione;
- **opera su infrastruttura altrui**: consulenza, sviluppo, migrazione, system management. In questo caso decide chi gestisce l'infrastruttura su cui opera; il controllo del consulente si registra solo come lente fornitore.

### R-S2. Chi eroga davvero
La domanda decisiva è: **il servizio è un servizio cloud di Microsoft, Google, Amazon o Oracle?** Se sì, è extra-UE, qualunque sia il rivenditore o il gestore. Se no, conta il paese dell'operatore che lo eroga in proprio. Non si fanno ricostruzioni societarie: quotazione in borsa e fondi o veicoli di investimento non contano; una capogruppo statunitense conta solo se è essa stessa un fornitore di servizi cloud.

### R-S3. Esiti
| esito | quando |
|---|---|
| **IT** | servizio erogato in proprio da un operatore italiano |
| **UE** | servizio erogato in proprio da un operatore di un paese UE |
| **sovrano non UE** | operatore di un paese europeo non soggetto al CLOUD Act (es. **Svizzera**, Fabio 3/11/2026): conteggiato fra i sovrani, con il paese registrato (CH) |
| **extra-UE** | servizio cloud di Microsoft, Google, Amazon, Oracle (o di altro fornitore cloud statunitense), anche se rivenduto o gestito da un operatore italiano |
| **incerto** | non si sa quale servizio sia stato comprato o chi lo eroghi; si registra l'azione per accertarlo |

### R-S4. Prodotto
L'origine del prodotto (Microsoft, Oracle, VMware, Fortinet…) **non decide** la sovranità. Si registra come dipendenza tecnologica. Decide solo se il produttore è anche chi **eroga** il servizio.

### R-S5. Licenze
Una licenza installata nei sistemi dell'ente (on-premise) **non è spesa cloud**: si conta a parte. Un abbonamento SaaS (es. Microsoft 365) è cloud erogato dal produttore, quindi segue la catena di controllo del produttore.

## Eccezioni e casi particolari incontrati

| caso | regola | fonte della decisione |
|---|---|---|
| **PSN: offerte su big tech** (Secure Public Cloud su Azure, Google, AWS; PSN Managed su Oracle Alloy; Hybrid su Azure Stack/Arc) | **sempre extra-UE**, senza eccezioni: chiavi gestite da PSN, region dedicate e gestione «managed» non danno immunità dal CLOUD Act | Fabio, 3/11/2026; Osservatorio, pagina PSN |
| **PSN: servizi erogati in proprio** (Industry Standard: housing, hosting, IaaS/PaaS su infrastruttura PSN) | **IT** (operatore italiano); VMware, Red Hat ecc. sono dipendenze tecnologiche | Fabio, 3/11/2026 |
| **TIM e altri rivenditori di cloud big tech** | ciò che rivendono di Microsoft, Google, Amazon, Oracle è extra-UE; ciò che erogano in proprio segue il loro paese | Fabio, 3/11/2026 |
| **Controllo tramite fondi, veicoli d'investimento o quotazione** (Engineering, Retelit, Accenture plc, Tiscali/Jefferies) | **non conta**: conta solo se la controllante è essa stessa un fornitore di servizi cloud | Fabio, 3/11/2026 |
| **Hosting dedicato** | è cloud: ospita servizi per conto dell'ente | Fabio, 3/11/2026 |
| **Affidamenti intragruppo o in house** (es. Trenitalia → FSTechnology) | si qualificano solo sapendo che cosa usa l'affidatario e come eroga. Se usa un hyperscaler extra-UE, quella parte non è sovrana. Finché non è noto: **incerto** | Fabio, 3/11/2026 |
| **Software USA gestito in proprio da un operatore italiano** (es. Sistema Cloud Toscana su VMware/Microsoft; servizi di sicurezza a canone su tecnologie USA) | sovrano se l'operatore eroga e controlla il servizio; il software è dipendenza tecnologica | Fabio, 29/10 e 3/11/2026 |
| **Catena che termina in Svizzera** | sovrana (la Svizzera non è soggetta al CLOUD Act) | Fabio, 3/11/2026 |
| **Licenze miste** (es. Microsoft Enterprise Agreement: on-premise e SaaS insieme) | si separano le quote; finché non sono note, la quota cloud è un intervallo e il resto incerto | revisione, 3/11/2026 |
| **Servizi applicativi «in ottica cloud»** | servizi professionali, non cloud; gli attuativi con licenze, hosting o infrastruttura si valutano uno per uno | revisione, 3/11/2026 |

## Cosa si porta a incertezza
- non si sa quale servizio sia stato comprato (es. un'adesione al PSN senza piano dei fabbisogni: Industry Standard o Secure Public Cloud?);
- ruolo dell'erogatore non scritto negli atti;
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
| 2026-11-03 | semplificazione (Fabio): extra-UE = servizi cloud di Microsoft, Google, Amazon, Oracle, chiunque li rivenda (PSN Secure Public Cloud, Managed, Hybrid compresi); il resto segue l'operatore che eroga in proprio; quotazione e veicoli d'investimento non contano |
