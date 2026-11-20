---
title: "Cloud in proprio: datacenter della PA e società in-house"
subtitle: "Quanto spende la PA per i propri datacenter e che cosa comprano le società ICT in-house"
date: 2026-11-20
lastmod: 2026-11-20T12:00:00Z
description: "Spesa per datacenter propri (server, storage, virtualizzazione, impianti, calcolo scientifico) e servizi affidati alle in-house ICT, dai CIG ANAC, con precisione misurata su tre campioni a cieco."
---

**Versione 0.1 del 2026-11-20** · ticket [#52](https://github.com/mxmap-it/analisi-spesa-ict/issues/52) · [registro delle revisioni](#registro-delle-revisioni)

Legenda: **[V]** misurato da noi, con il comando per rifarlo; **[S]** stima.

## 1. Sintesi

- **Cosa è.** Il «cloud in proprio» è la spesa della PA per far girare in casa i propri sistemi: datacenter come luogo e impianti, server e storage, software di virtualizzazione, backup, calcolo scientifico; più i servizi di datacenter e cloud affidati alle società ICT in-house pubbliche. Si affianca al cloud esterno.
- **Giurisdizione (decisione di Fabio, 20/11/2026).** Un datacenter di proprietà dell'ente e gestito da lui è **sovrano (IT)** anche se usa tecnologia extra-UE come VMware: il produttore non può accedere giuridicamente ai dati né ai sistemi.
- **Numeri dal 2024, al netto dei massimali** [V, regole 0.4]:

| voce | CIG | M€ |
|---|---:|---:|
| cloud esterno certo (per confronto) | 5.036 | 1.288 |
| **datacenter dell'ente** | 7.851 | 1.938 |
| — server e storage | 4.133 | 643 |
| — il datacenter come luogo e i suoi impianti | 1.950 | 499 |
| — virtualizzazione | 965 | 464 |
| — calcolo scientifico (voce separata) | 638 | 316 |
| — backup | 165 | 16 |
| **servizi affidati alle in-house** (infrastruttura in-house certa) | 711 | 138 |

- **Precisione** [V, terzo campione a cieco]: 74,7 % dei contratti (Wilson 63,8-83,1 %), **85,7 % degli euro** (73,3-92,9 %). Stima corretta del datacenter proprio dal 2024 **[S]: circa 1,66 mld (1,42-1,80)**. Dal 2020 al 2023 le regole danno 1,64 mld.
- **Cosa sfugge.** Dei contratti lasciati incerti perché misti, il 44 % è da datacenter (26,7-62,9 %): il numero è prudente da quel lato.

## 2. Come si riconosce

Regole su testo e CPV in `config/datacenter_proprio.yaml`, applicate da `tools/verifiche/datacenter_proprio.py` e unite alla [tabella unica degli spostamenti](/rendiconti/imbuto-dove-siamo/) come livello **DC**:

- famiglie con peso: luogo del datacenter, server e storage (solo con contesto hardware), virtualizzazione, backup, calcolo scientifico; rete e gestione dei sistemi solo se la gara nomina il datacenter;
- **prevalenza** (decisione di Fabio): il contratto conta solo se il punteggio da datacenter supera quello di postazioni, stampanti, telefonia, videosorveglianza, assistenza generica;
- esclusi i segni di servizio esterno (cloud, hosting, housing, PSN, server a noleggio o virtuali, servizi a consumo) e i contratti madre di convenzioni e accordi quadro (massimali);
- si applica solo a contratti oggi ICT non cloud o incerti, mai sopra il cloud certo né sopra una verifica manuale;
- servizi a in-house: aggiudicatario nell'elenco `config/societa_inhouse_ict.yaml` (22 soci di Assinter Italia, pagina archiviata con sha256, più Sogei, CINECA, PagoPA) e testo da datacenter o cloud. Dal 20/11/2026 l'elenco ufficiale per codice fiscale viene dal censimento MEF delle partecipazioni: [Società ICT pubbliche e in-house](/rendiconti/societa-ict-pubbliche/) (64 in-house ICT attive, 44 non socie Assinter); il passaggio dei CIG dal nome al codice fiscale è in [#82](https://github.com/mxmap-it/analisi-spesa-ict/issues/82).

## 3. Precisione: tre campioni a cieco

Un agente (Claude Sonnet) etichetta i testi senza vedere la nostra classificazione; ogni versione delle regole è misurata su un campione nuovo.

| regole | contratti a caso | estratti in proporzione agli euro | servizi in-house | incerti misti che sono DC |
|---|---:|---:|---:|---:|
| 0.2 | 70,9 % | 77,5 % | — | 66,7 % |
| 0.3 | 74,1 % | 77,5 % | 68,4 % | — |
| 0.4 | 74,7 % | 85,7 % | 84,0 % | 44,0 % |

Gli errori residui sono soprattutto contratti misti (luogo del datacenter con lavori o licenze d'ufficio) e server per applicativi.

## 4. Le società ICT in-house: che cosa comprano e che cosa ricevono

`tools/verifiche/inhouse_vista.py`, dal 2024, M€ netti. Tabella completa in `esiti/2026-11-20/inhouse/vista/vista.md`. Esempi:

- **CINECA:** 230 M€ di cloud in proprio (calcolo scientifico e impianti del datacenter del Tecnopolo di Bologna); riceve 160 M€ da 144 enti.
- **Lepida:** 29 M€ di cloud in proprio, 17 M€ di cloud esterno extra-UE; riceve 281 M€ da 181 enti.
- **CSI Piemonte:** 38 M€ di cloud in proprio; riceve 423 M€ da 118 enti.
- **Sogei:** 77 M€ di cloud in proprio; riceve 2,38 mld da 50 enti, ma i testi quasi mai dicono «datacenter»: restano ICT non cloud.
- **ARIA e So.Re.Sa.** sono anche centrali d'acquisto: i loro acquisti includono quelli per la sanità regionale.

Il riconoscimento è sul nome (0.1); il passaggio al codice fiscale è il prossimo passo.

## Limiti

- Precisione 75-86 %: la cifra è una stima con forbice, non un conto.
- Valore dei contratti, non pagato; duplicati di procedura (due CIG per la stessa gara) non ancora tolti.
- Servizi affidati alle in-house senza parole da datacenter (Sogei) non riconosciuti; affidamenti senza CIG fuori (M7).
- Elenco dei datacenter per ente di AgID non pubblicato (M14).

## Rifare i numeri

```
python3 tools/verifiche/datacenter_proprio.py 2026-11-20
python3 tools/verifiche/inhouse_verifica.py 2026-11-20
python3 tools/verifiche/imbuto_spostamenti.py 2026-11-20
python3 tools/verifiche/inhouse_vista.py 2026-11-20
python3 tools/verifiche/datacenter_cieco.py esiti/2026-11-20/imbuto/datacenter/cieco3
```

## Registro delle revisioni

| versione | data | modifica |
|---|---|---|
| 0.1 | 2026-11-20 | Prima versione: capitolo aperto su richiesta di Fabio; decisioni del 20/11; regole 0.4; tre campioni a cieco; vista sulle in-house. |
