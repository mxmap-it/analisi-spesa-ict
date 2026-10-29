---
title: "Iniziative Consip e PSN: cosa significano negli oggetti dei contratti"
date: 2026-10-29
description: "Tavola di lettura delle iniziative di acquisto centralizzato ICT (SPC Cloud, AQ IaaS/PaaS, PSN, SaaS PRINCO, Microsoft EA, LAN 8, Centralini, telefonia): prodotto, provider, giurisdizione e fonti."
weight: 16
---
**Stato: bozza del 29 ottobre 2026.** Le voci marcate *controvalidata* hanno due fonti
indipendenti concordi. Le altre sono **da verificare** e non vanno usate come fatto.
Base dati: `report/metodo/llm/conoscenza-iniziative.yaml`; tabella dei lotti usata dal
codice: `config/lotti_cloud.yaml`. Metodo generale:
[come si riconosce il cloud provider](../metodo-cloud-provider/).

Regola: la giurisdizione è quella della **capogruppo del produttore**, non del rivenditore
aggiudicatario (es. AWS venduto da Fastweb resta extra-UE).

## Cloud

| Negli oggetti | Cosa è | Prodotto / provider | Giurisdizione | Stato |
|---|---|---|---|---|
| "Cloud IaaS e PaaS 2", ID 2746, lotto 1 (CIG B6A19F425E) | AQ Consip 2025, rivendita crediti | Amazon Web Services (aggiudicatario Fastweb) | extra-UE | controvalidata ([avviso Consip][2746], [ARERA 76/DAGR/2026][arera76]) |
| ID 2746 lotto 2 (B6A19F5331) | idem | Google Cloud | extra-UE | controvalidata ([avviso Consip][2746], oggetti CIG BDNCP); aggiudicatario da verificare |
| ID 2746 lotto 3 (B6A19F6404) | idem | Microsoft Azure (aggiudicatario SoftwareOne) | extra-UE | controvalidata ([avviso Consip][2746], [Giustizia UCAN 32/2026][ucan]) |
| ID 2746 lotti 4, 5, 6 | idem | Oracle, IBM, Aruba | extra-UE, extra-UE, IT | controvalidata ([avviso Consip][2746], oggetti CIG BDNCP); aggiudicatari da verificare |
| "Public Cloud IaaS e PaaS", ID 2213 | AQ Consip 2021-22, 11 lotti: lotti CSP + lotti di servizi di migrazione | lotto 1 (CIG 81283942ED): AWS, RTI Almaviva-Engineering; lotti 5, 8, 10: servizi professionali | lotto 1 extra-UE; servizi: n/a | **da verificare** ([Engineering][eng], [AgID][agid6754], [CE Regione Lazio][lazio]) |
| "Public Cloud SaaS", PRINCO, ID 2297 (CIG 89910186C4) | AQ multifornitore, 10 aggiudicatari (Aruba, TIM, Fastweb, Engineering, Lutech…) | dipende dal prodotto a catalogo: il lotto **non** identifica il provider | dall'oggetto del CIG derivato | verificata ([esito Consip][2297]) |
| "SPC Cloud lotto 1" | Contratto quadro SPC 2016, IaaS/PaaS/SaaS | DC del RTI TIM-Poste-Postel-Postecom-HPE; non hyperscaler | IT (erogazione); tecnologia sottostante da verificare | controvalidata (riferita: [AgID][agidspc], [CorCom][corcom]) |
| "SPC Cloud lotto 2" | Servizi di sicurezza (assessment, servizi professionali, sicurezza gestita); CQ fino al 20/07/2022 | RTI Leonardo-IBM-Fastweb-Sistemi Informativi | servizi, non cloud IaaS/PaaS/SaaS; eventuali prodotti di sicurezza di terzi: da verificare per CIG | verificata ([AgID 123/2017][agid123], [AgID 494/2021][agid494]) |
| "SPC Cloud lotto 3" | Interoperabilità dei dati e cooperazione applicativa (web services, orchestrazione, Open Data, analisi Big Data); CQ stipulato 20/07/2016, prorogato fino al 31/12/2022 | RTI Almaviva (mandataria)-Almawave-Indra-PwC (ora Intellera); quote da verificare | servizi professionali: **non** spesa in prodotto cloud | verificata ([AgID 293/2022][agid293], [AgID 194/2017][agid194]) |
| "SPC Cloud lotto 4" | Realizzazione di portali e servizi online (sviluppo, conduzione applicativa) | stesso RTI del lotto 3 | servizi applicativi: **non** spesa cloud di prodotto | verificata ([CE lotto 4 AgID][agid2160]) |
| "Cloud Toscana", "Sistema Cloud Toscana", SCT | Contratto quadro Regione Toscana (soggetto aggregatore), stipula 30/09/2019, 60 mesi dal 3/10/2019, prorogato dal 3/10/2024 fino a 270 giorni dopo il nuovo accordo quadro; CIG quadro 7154112FF8, CIG derivato Regione 8006383443; massimale 68,97 M EUR | RTI TIM (mandataria, 41,27%), Enterprise Services/DXC (16,53%), IBM (9,65%), Lutech (20,48%), Dedalus (11,71%); Kyndryl mandante almeno dal 2021, Accenture solo subappaltatore CMP. Catalogo IaaS/PaaS/SaaS/housing/DR; stack OpenStack + VMware, Guest OS Microsoft, SAS | **cloud sovrano IT, condizionato** (criterio del 29/10/2026): DC in Italia (TIX regionale + DC TIM Acilia e Firenze), mandataria italiana; VMware, Microsoft e SAS sono dipendenze tecnologiche. Condizione aperta: ruolo e accessi dei mandanti a capogruppo USA (DXC, IBM, Kyndryl), non pubblici ([scheda di analisi](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/metodo/analisi-infrastrutture/cloud-toscana.md)) | contratto quadro **verificato** ([contratto][ctq], [Comune di Firenze][fi8446], [Progetto dei Fabbisogni][pfdsu]); stack e quota extra-UE da verificare |
| "PSN" + Housing / Hosting / Industry Standard | Convenzione PSN 24/08/2022 (CIG 9066973ECE), DC Rozzano, Santo Stefano, Acilia, Pomezia | Polo Strategico Nazionale (TIM, Leonardo, CDP, Sogei) | IT | controvalidata ([Guida PSN][psn], [ARERA][arera34]) |
| "PSN" + Secure Public Cloud (AWS, Microsoft, Google) | region pubbliche degli hyperscaler + chiavi su HSM nei DC PSN e backup mensile su PSN; qualifica ACN livello 2 | Amazon Web Services, Microsoft Azure, Google Cloud | extra-UE | controvalidata ([Guida PSN][psn], [analisi dell'Osservatorio](https://osservatorio.mxmap.it/psn/)) |
| "PSN" + Secure Public Cloud Oracle | region pubblica Oracle, per i servizi non erogabili con Alloy | Oracle | extra-UE | [analisi dell'Osservatorio](https://osservatorio.mxmap.it/psn/) (listino PSN 04/2026) |
| "PSN" + Public Cloud PSN Managed | due architetture: Google (Assured Workloads sulle region Google di Milano e Torino, operate da Google) e Oracle Alloy (realm dedicato nei DC PSN, operato e aggiornato da Oracle) | Google Cloud, Oracle | extra-UE | [analisi dell'Osservatorio](https://osservatorio.mxmap.it/psn/) |
| "PSN" + Hybrid Cloud on PSN site | HCI dedicata gestita col control plane Azure (Arc) | Microsoft | extra-UE | [Guida PSN][psn]; non presente nell'analisi dell'Osservatorio: **da verificare** sul listino |

"PSN" da solo non basta: va letto il servizio.

## Licenze, servizi, reti e telefonia (non cloud)

| Negli oggetti | Cosa è | Prodotto / fornitore | Stato |
|---|---|---|---|
| "Microsoft Enterprise Agreement 7", EA7 | Convenzione licenze Microsoft (incl. M365), venduta da TIM | Microsoft, extra-UE | controvalidata ([Regione Abruzzo][abruzzo], [AGCOM 70/23][agcom]) |
| "Licenze software multibrand" | Convenzione a lotti per brand | dal brand del lotto | **da verificare** |
| "Servizi applicativi in ottica cloud", ID 2212 | sviluppo applicativo | servizi professionali, non prodotto | **da verificare** |
| "Sanità digitale", ID 2202 | sistemi clinico-assistenziali (RTI Engineering e altri) | servizi applicativi | controvalidata (riferita) |
| "Reti locali 8", LAN 8, ID 2223 | apparati e servizi di rete LAN; RTI Vodafone-Converge-Lisa (lotto 1 CIG 95436927C7, lotto 2 CIG 9543706356) | non cloud; vendor apparati da verificare | lotto 1 controvalidato ([Giustizia][giust], [AgID][agid9569]) |
| "Centrali telefoniche 8", Centralini, CT8 | apparati telefonici | RTI Sielte-Vodafone; TIM citata da Regione Piemonte | **da verificare** |
| "Telefonia mobile 9" | convenzione TM9, Vodafone (ora Fastweb) | telefonia | **da verificare** (scadenza) |
| "SPC2", connettività | contratti quadro 2016: Fastweb (subentrata a Tiscali), BT, Vodafone | connettività | controvalidata (riferita: [Agenda Digitale][ad], [CorCom][corcomspc]) |

Le altre convenzioni regionali (Lepida, CSI Piemonte, ARIA, Liguria Digitale, LAZIOcrea) e il Sistema Gestionale Integrato non sono ancora mappati: **da verificare**. Cloud Toscana: l'esito del nuovo accordo quadro e la qualifica ACN non sono stati trovati.

[agid123]: https://trasparenza.agid.gov.it/download/1629.html
[agid494]: https://trasparenza.agid.gov.it/download/2357.html
[agid293]: https://trasparenza.agid.gov.it/download/5924.html
[agid194]: https://trasparenza.agid.gov.it/download/1327.html
[agid2160]: https://trasparenza.agid.gov.it/download/2160.html
[ctq]: https://affidamenti.comune.fi.it/sites/affidamenti.comune.fi.it/files/profilo/documenti-di-gara/20210108/Contratto%20quadro.pdf
[fi8446]: https://affidamenti.comune.fi.it/sites/affidamenti.comune.fi.it/files/profilo/aggiudicazione-definitiva/20251120/20251120-DD8446-Affidamento.pdf
[pfdsu]: https://www.dsu.toscana.it/documents/4390857/15562343/DETERM_724_20203_progetto+dei+fabbisogni_sct_ards.pdf

[2746]: https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID%202746%20AVVISO%20DI%20PROROGA%20DEL%2028-05-25%20S%20102_0.pdf
[arera76]: https://www.arera.it/fileadmin/allegati/docs/26/76-26-dagr.pdf
[ucan]: https://www.giustizia.it/cmsresources/cms/documents/UCAN_decisione_a_contrarre_32_2026.pdf
[eng]: https://www.eng.it/en/news/press-releases/2022/07/engineering-wins-two-new-lots-of-the-consip-framework-agreement-on-cloud-services
[agid6754]: https://trasparenza.agid.gov.it/download/6754.html
[lazio]: https://regione.lazio.it/sites/default/files/amministrazione-trasparente/atti-procedure-affidamento/Contratto-Esecutivo-ID2213.pdf
[2297]: https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID%202297%20-%20Public%20Cloud%20Saas%20Princo%20-%20Avviso%20di%20esito.pdf
[agidspc]: https://www.agid.gov.it/sites/default/files/repository_files/ufficio_stampa/consip_e_agid_sottoscritti_i_contratti_per_la_connettivita_e_aggiudicati_i_primi_due_lotti_della_gara_per_i_servizi_cloud.pdf
[corcom]: https://www.corrierecomunicazioni.it/telco/spc-consip-detta-i-tempi-di-attivazione-dei-servizi
[psn]: https://www.polostrategiconazionale.it/app/uploads/2025/08/PSN_Guida-alla-Convenzione_.pdf
[arera34]: https://www.arera.it/fileadmin/allegati/docs/25/34-25dagr.pdf
[abruzzo]: https://regione.abruzzo.it/system/files/bandi-di-gara-e-contratti/delibere-contrarre/dpb012-046-del-29-03-23-prenotazione-impegno-di-spesa.pdf
[agcom]: https://www.agcom.it/sites/default/files/migration/delibera/Delibera%2070-23-CONS.pdf
[giust]: https://www.giustizia.it/cmsresources/cms/documents/DIT_Determina3309_31ott2025.pdf
[agid9569]: https://trasparenza.agid.gov.it/download/9569.html
[ad]: https://www.agendadigitale.eu/procurement/sistema-pubblico-di-connettivita-spc-2-cosa-e-cambiato/
[corcomspc]: https://www.corrierecomunicazioni.it/pa-digitale/consip-aggiudicata-la-gara-spc-previsti-risparmi-per-due-miliardi/
