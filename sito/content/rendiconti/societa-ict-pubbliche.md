---
title: "Società ICT pubbliche e in-house: il dataset"
subtitle: "Chi sono, chi le controlla, che sito hanno, se pubblicano software libero o in riuso"
date: 2026-11-20
lastmod: 2026-11-20T20:00:00Z
description: "Elenco per codice fiscale delle società ICT partecipate dalla PA, dal censimento MEF delle partecipazioni (dati al 31/12/2023), con classe in-house / controllata / partecipata, sito web e un'analisi minima di software libero e riuso. Scaricabile."
---

**Versione 0.4 del 2026-11-20** · ticket [#82](https://github.com/mxmap-it/analisi-spesa-ict/issues/82) (legato a [#52](https://github.com/mxmap-it/analisi-spesa-ict/issues/52)) · [registro delle revisioni](#registro-delle-revisioni)

Legenda: **[V]** misurato da noi, con il comando per rifarlo; **[S]** stima.

## 1. Perché questo dataset

Per misurare il [cloud in proprio](/rendiconti/cloud-in-proprio/) serve sapere quali sono le società ICT pubbliche:
quando un ente affida i suoi sistemi alla propria in-house, quella spesa è cloud o datacenter «in casa» della PA.
Finora le riconoscevamo dal nome, partendo dai soci di Assinter Italia più Sogei, CINECA e PagoPA (24 società).
Ma l'elenco ufficiale esiste: ogni anno le amministrazioni devono dichiarare al MEF le società che partecipano
(censimento delle partecipazioni, art. 17 del d.l. 90/2014 e art. 20 del d.lgs. 175/2016). Ora l'elenco viene da lì,
per **codice fiscale**.

Esempio: Venis (Comune di Venezia), Pasubio Tecnologia (comuni dell'Alto Vicentino) o SISPI (Comune di Palermo) non
sono soci Assinter e prima ci sfuggivano; nel censimento sono in-house ICT dichiarate.

## 2. Fonte e criteri

- **Fonte:** MEF, Dipartimento dell'Economia, [open data delle partecipazioni](https://www.de.mef.gov.it/it/attivita_istituzionali/partecipazioni_pubbliche/open_data_partecipazioni/),
  file dei dati al 31/12/2023 (pubblicato il 10/3/2026, 53.656 righe, licenza CC BY 4.0). Copia nel nostro mirror con
  sha256 `c3c29c9d982879248e5f8dfa49b5cf6b63f6703e8839245ed017afe2dd278d2b`; specchiati anche gli anni 2012-2022 e gli
  elenchi degli enti adempienti. Non specchiamo il file dei rappresentanti negli organi delle società: contiene nomi di persone.
- **Società ICT:** divisione ATECO 62 (software e consulenza informatica) o 63 (servizi d'informazione), come la
  dichiarano gli enti; in più i soci Assinter che gli enti dichiarano con un'altra attività (InnovaPuglia risulta
  «consulenza gestionale», SoReSa e Metis «supporto alle imprese»): restano con `ateco=altro`.
- **Classe**, da ciò che dichiarano gli enti soci:
  - **in-house**: almeno un ente dichiara il *controllo analogo* oppure un *affidamento diretto* di servizi (che a una
    società pubblica è possibile solo in-house);
  - **controllata**: almeno un ente dichiara un controllo, senza i segni dell'in-house. Qui finiscono Sogei e PagoPA:
    il MEF, unico socio, dichiara «controllo solitario» e non l'affidamento diretto;
  - **controllo pubblico congiunto** (dalla versione 0.2, decisione di Fabio del 20/11/2026): nessun ente dichiara il
    controllo, ma la **quota pubblica è almeno del 50 %**. È la presunzione relativa di controllo pubblico: il testo
    unico sulle società partecipate (art. 2, d.lgs. 175/2016) comprende il controllo esercitato da più amministrazioni
    insieme, e ANAC (delibere 1134/2017 e 859/2019, *riferite* da commenti pubblicati, testo ufficiale da archiviare)
    considera la partecipazione pubblica maggioritaria un indice presuntivo del controllo pubblico ai fini della
    trasparenza e dell'anticorruzione, salvo prova contraria della società. Conta come le controllate;
  - **controllata sostanzialmente** (dalla versione 0.3, decisione di Fabio del 20/11/2026): la quota pubblica «di
    diritto» è sotto il 50 %, ma supera il 50 % se si contano i soci **quotati** controllati dallo Stato. È controllata
    nei fatti, non ancora giuridicamente. Oggi un solo caso, il Polo Strategico Nazionale (vedi sotto, § 2bis);
  - **partecipata**: quota pubblica sotto il 50 % e nessun controllo dichiarato. Resta nel file, fuori dalla tabella.
- **Quota pubblica**, come si calcola:
  - somma delle quote **dirette** dichiarate al censimento da amministrazioni pubbliche e da società a loro volta
    pubbliche (in-house, controllate o con quota pubblica almeno del 50 %), calcolata **a catena** su tutte le
    53.656 righe del censimento: così conta, per esempio, la quota di Sogei in una società partecipata da Sogei;
  - le partecipazioni dichiarate solo come «indirette» non hanno una quota nel censimento: sono contate a parte;
  - **verifica a mano** dei soci, sul sito della società (Società trasparente), nei bilanci o in atti pubblici, per le
    società attive con quota pubblica fra 30 e 50 % o con partecipazione indiretta e fatturato da 1 M€: 13 casi,
    risolti 3 (`config/inhouse_soci.yaml`, con fonte e data). Esempi: Geoweb (Consiglio nazionale dei geometri e
    Sogei) risulta tutta pubblica e passa a controllo pubblico congiunto; il **Polo Strategico Nazionale** ha il 30 %
    pubblico certo (CDP Equity 20 %, Sogei 10 %) più Leonardo 25 %, su cui il MEF ha un controllo di fatto: con la
    regola attuale resta partecipata; se si contasse Leonardo arriverebbe al 55 % (**decisione per Fabio**). Le 10
    società non risolte restano «da verificare» nel file.
- **Sito web:** dall'[Indice PA](https://indicepa.gov.it/ipa-dati) per codice fiscale, quando la società vi è iscritta;
  gli altri cercati a mano e confermati sulla pagina stessa (denominazione o partita IVA), con la data, in
  `config/inhouse_siti.yaml`.
- **Controprova con Assinter** [V]: 22 dei 24 nomi del vecchio elenco si ritrovano nel censimento per codice fiscale;
  mancano Consorzio.IT (cremasco), Arsenàl.IT si ritrova con un'altra grafia.

### 2bis. Il Polo Strategico Nazionale: controllato sostanzialmente, non ancora di diritto

**Soci** (sezione «Società trasparente» di PSN, 20/11/2026): TIM 45 %, Leonardo 25 %, CDP Equity 20 %, Sogei 10 %.

**Perché è controllato nei fatti.** Tutte e quattro le catene risalgono al Ministero dell'economia: Sogei (100 % MEF),
CDP Equity (gruppo CDP, controllato dal MEF), Leonardo (circa 30 % del MEF, controllo di fatto) e, da settembre 2026,
TIM (circa 85,8 % a Poste Italiane dopo l'offerta pubblica di acquisto e scambio; Poste è controllata da MEF e CDP).
Quota pubblica di voto: 30 % senza quotate, 55 % con Leonardo (dal 2022), circa 100 % con TIM (da settembre 2026) [S:
quote di Leonardo, Poste e TIM da fonti secondarie, da riconfermare su fonte primaria Consob].

**Perché non lo è ancora giuridicamente** (ricerca sulla giurisprudenza: [Controllo pubblico delle società](/rendiconti/controllo-pubblico-giurisprudenza/), bozza tecnica):
1. *trasparenza e anticorruzione: le quote che passano per quotate non contano.* L'art. 2-bis c. 2 lett. b del d.lgs.
   33/2013 esclude le società partecipate da quotate, salvo che siano controllate o partecipate da amministrazioni
   «non per il tramite di società quotate». Per questa via resta solo Sogei (10 %); anche CDP Equity può cadere, perché
   ANAC (atto di segnalazione 3/2020) considera CDP «quotata» per le sue obbligazioni. PSN si colloca quindi fra le
   società a partecipazione pubblica (comma 3), come dichiara di sé nel modello organizzativo del 26/7/2023;
2. *testo unico sulle partecipate: la questione è aperta.* Dal 2019 l'art. 1 c. 5 del d.lgs. 175/2016 esclude solo le
   quotate e le società **da esse controllate**, e PSN non è controllata da nessuna singola quotata; il computo del
   controllo indiretto (art. 2359 c. 2 c.c.) non ha un filtro per le quotate. **Nessuna sentenza** decide se i voti che
   passano per una quotata contino; atti e pareri divergono (MEF 2018 sì; parere del Consiglio di Stato 968/2016 e
   relazione illustrativa del testo unico no);
3. *il controllo «in concreto».* Per il controllo **congiunto** di più enti il Consiglio di Stato più recente (VI,
   436/2026) chiede la prova di una concertazione effettiva, mentre la IV sezione (5289/2025) considera la maggioranza
   «necessaria e sufficiente»: contrasto non risolto, senza rimessione all'Adunanza plenaria. Per PSN però tutte le
   catene risalgono al **solo** MEF: è un controllo solitario indiretto, dove il dato numerico basta anche per la 436/2026;
4. *altri perimetri*: non è nell'elenco ISTAT delle amministrazioni pubbliche (2025 e 2026; Sogei sì) e, come
   concessionario a rischio d'impresa, non è amministrazione aggiudicatrice né organismo di diritto pubblico.

**Quote con i diversi metodi** [S per le quote di Leonardo, Poste e TIM, da riconfermare su fonte Consob]: computo
pieno lungo le catene 55 % fino ad agosto 2026 (solo con il controllo di fatto su Leonardo), da settembre 2026 75 %
senza Leonardo (maggioranza di diritto) e 100 % con Leonardo; con il filtro delle quotate 30 % (o 10 % se CDP conta come
quotata). Conclusione: per la trasparenza PSN resta **partecipata** (certezza media); per il testo unico, da settembre
2026, gli argomenti per il controllo pubblico sono più forti ma non decisi (certezza bassa-media). Da qui la classe
**controllata sostanzialmente**.

**Effetto sulla misura.** Nessuno sulla giurisdizione: i servizi PSN sono già cloud **IT**. Nella vista per società PSN
compare fra le società pubbliche; non entra fra i «servizi alle società ICT pubbliche» del cloud in proprio, perché i
suoi contratti sono già contati come cloud esterno sovrano. La regola vale per ogni società i cui soci siano verificati
a mano (`config/inhouse_soci.yaml`, campi `quota_pubblica_sostanziale` e `sostanziale_dal`): nel censimento MEF non ci
sono altri casi (le società controllate solo da quotate, come quelle dei gruppi TIM o Leonardo, non vi compaiono).

Comandi: `python3 tools/verifiche/inhouse_censimento.py`, `nice python3 tools/verifiche/inhouse_cf.py`, `python3 tools/verifiche/inhouse_vista.py`, `python3 tools/verifiche/inhouse_opensource.py`, `python3 tools/pagina_inhouse.py`.

## 3. Quante sono

<!-- GEN:conteggi -->
| classe | attive | non attive |
|---|---:|---:|
| in-house | 64 | 5 |
| controllata | 15 | 6 |
| controllo-pubblico-congiunto | 5 | 4 |
| controllata-sostanzialmente | 1 | 0 |
| partecipata | 94 | 24 |
<!-- /GEN:conteggi -->

Le in-house attive fatturano in tutto circa 2,8 miliardi (2023), quasi tutto nelle 20 socie Assinter; le altre 44
sono piccole società di comuni, province e camere di commercio (circa 130 M€ in tutto) [V]. Le controllate attive
fatturano 1,1 miliardi, quasi tutto Sogei.

## 4. Software libero e riuso

Due vie indipendenti, entrambe ripetibili:

1. il **catalogo del riuso** di [Developers Italia](https://developers.italia.it/it/software), dove la PA pubblica il
   software che mette a disposizione di altri enti (art. 69 del Codice dell'amministrazione digitale) con un file
   `publiccode.yml`. Contiamo il software di cui la società è **editrice** e quello pubblicato da un ente in cui la
   società compare come **manutentrice**;
2. la **home page** del sito (una sola pagina, nel rispetto del robots.txt, una richiesta ogni 5 secondi): cerchiamo le
   parole «open source», «software libero», «riuso» e i collegamenti a GitHub o GitLab. È un indizio, non una prova:
   un sito può citare l'open source senza pubblicare nulla, e una società può pubblicare codice senza dirlo in home.

<!-- GEN:opensource -->
- Società esaminate (in-house, controllate e soci Assinter attivi o no): **99**.
- Nel catalogo del riuso di Developers Italia (577 software, 153 editori, copia del 2026-11-20 con sha256 `7db646184800739e…`): **7** società hanno almeno un software, **35** software in tutto (come editrici o come manutentrici di software pubblicato da un ente) [V].
- Home page lette: **44**; con le parole «open source» o «software libero»: **6**; con «riuso»: **0**; con un collegamento a GitHub o GitLab: **0** [V, indizio da leggere a mano].
<!-- /GEN:opensource -->

## 5. La tabella (in-house, controllate, a controllo pubblico congiunto o sostanziale, attive, più i soci Assinter)

Ordine: in-house, poi controllate, per fatturato 2023. «Enti» = enti che dichiarano una partecipazione.
«Riuso (catalogo)» = software nel catalogo Developers Italia (ed. = editrice, man. = manutentrice).

<!-- GEN:tabella -->
| società | classe | regione | enti | fatturato 2023 (M€) | addetti | sito | riuso (catalogo) | open source in home | riuso in home |
|---|---|---|---:|---:|---:|---|---:|---|---|
| SOCIETA' REGIONALE PER LA SANITA' S.P.A.' IN BREVE SO.RE.SA.… | in-house | Campania | 1 | 1.445,2 | 160 | [www.soresa.it](https://www.soresa.it) | 0 | no | no |
| AZIENDA REGIONALE PER L'INNOVAZIONE E GLI ACQUISTI S.P.A., I… | in-house | Lombardia | 1 | 418,3 | 512 | [www.ariaspa.it](https://www.ariaspa.it) | 0 | no | no |
| LAZIOCREA S.P.A. | in-house | Lazio | 1 | 162,6 | 1676 | [www.laziocrea.it](https://www.laziocrea.it) | 1 (0 ed., 1 man.) | no | no |
| INFOCAMERE - SOCIETA' CONSORTILE DI INFORMATICA DELLE CAMERE… | in-house | Lazio | 75 | 116,4 | 1098 | [www.infocamere.it](https://www.infocamere.it) | 0 | no | no |
| INSIEL-INFORMATICA PER IL SISTEMA DEGLI ENTI LOCALI S.P.A. O… | in-house | Friuli Venezia Giulia | 1 | 99,0 | 681 | [www.insiel.it](https://www.insiel.it) | 0 | no | no |
| LIGURIA DIGITALE S.P.A. | in-house | Liguria | 37 | 94,2 | 448 | [www.liguriadigitale.it](https://www.liguriadigitale.it) | 5 (3 ed., 2 man.) | sì | no |
| INNOVAPUGLIA - S.P.A. | in-house | Puglia | 1 | 79,6 | 211 | [www.innova.puglia.it](https://www.innova.puglia.it) | 2 (2 ed., 0 man.) | sì | no |
| LEPIDA S.C.P.A. | in-house | Emilia Romagna | 435 | 70,3 | 657 | [www.lepida.net](https://www.lepida.net) | 0 | no | no |
| INFORMATICA ALTO ADIGE S.P.A. % SUEDTIROLER INFORMATIK AG | in-house | Trentino Alto Adige | 5 | 57,5 | 178 | [www.siag.it](https://www.siag.it) | 0 | no | no |
| TRENTINO DIGITALE S.P.A. | in-house | Trentino Alto Adige | 181 | 55,6 | 298 | [www.trentinodigitale.it](https://www.trentinodigitale.it) | 0 | no | no |
| PUNTOZERO S.C.A R.L. | in-house | Umbria | 86 | 40,4 | 532 | [puntozeroscarl.it](https://puntozeroscarl.it/) | 0 | no | no |
| SISPI - SISTEMA PALERMO INNOVAZIONE S.P.A. | in-house | Sicilia | 1 | 28,6 | 104 | [www.sispi.it](https://www.sispi.it) | 0 | no | no |
| IC OUTSOURCING SOCIETA' CONSORTILE A RESPONSABILITA' LIMITAT… | in-house | Veneto | 72 | 24,8 | 629 | [www.icoutsourcing.it](https://www.icoutsourcing.it) | 0 | no | no |
| IN.VA. S.P.A. | in-house | Valle D'Aosta | 89 | 22,7 | 250 | [www.invallee.it](https://www.invallee.it) | 0 | errore-ConnectTimeout |  |
| VENEZIA INFORMATICA E SISTEMI - VENIS S.P.A. - O IN BREVE - … | in-house | Veneto | 26 | 21,7 | 84 | [www.venis.it](https://www.venis.it) | 0 | no | no |
| ECOCERVED SOCIETA' CONSORTILE A RESPONSABILITA' LIMITATA', O… | in-house | Lazio | 64 | 12,0 | 175 | [www.ecocerved.it](https://www.ecocerved.it) | 0 | no | no |
| MOLISE DATI - SOCIETA' INFORMATICA MOLISANA S.P.A. | in-house | Molise | 1 | 11,3 | 30 | [www.molisedati.it](https://www.molisedati.it) | 0 | errore-ConnectionError |  |
| SIN - SISTEMA INFORMATIVO NAZIONALE PER LO SVILUPPO DELL'AGR… | in-house | Lazio | 2 | 9,5 | 80 | [www.sin.it](https://www.sin.it) | 0 | no | no |
| SICILIA DIGITALE S.P.A. | in-house | Sicilia | 1 | 8,1 | 106 | [www.siciliadigitale.it](https://www.siciliadigitale.it) | 0 | errore-ConnectTimeout |  |
| CASA ATC SERVIZI S.R.L. | in-house | Piemonte | 1 | 7,5 | 122 | [www.casaatcservizi.it](https://www.casaatcservizi.it) | 0 | HTTP 403 |  |
| ANCI DIGITALE SOCIETA' PER AZIONI | in-house | Lazio | 2 | 6,8 | 40 | [www.ancidigitale.it](https://www.ancidigitale.it/) | 0 | errore-ConnectTimeout |  |
| SARDEGNA IT S.R.L. | in-house | Sardegna | 1 | 6,0 | 111 | [www.sardegnait.it](https://www.sardegnait.it) | 0 | no | no |
| PASUBIO TECNOLOGIA S.R.L. | in-house | Veneto | 36 | 4,4 | 28 | [www.pasubiotecnologia.it](https://www.pasubiotecnologia.it) | 0 | errore-ConnectTimeout |  |
| SMACT SOCIETA' CONSORTILE PER AZIONI | in-house | Veneto | 13 | 3,3 | 11 |  | 0 |  |  |
| C.S.A. CONSORZIO SERVIZI AVANZATI SOCIETA' CONSORTILE A RESP… | in-house | Puglia | 7 | 3,2 | 97 |  | 0 |  |  |
| IT.CITY S.P.A | in-house | Emilia Romagna | 1 | 3,1 | 25 | [www.itcity.it](https://www.itcity.it) | 0 | sì | no |
| SOCIETA' INFORMATICA TERRITORIALE SRL | in-house | Veneto | 67 | 2,3 | 16 | [www.sitbelluno.it](https://www.sitbelluno.it/) | 0 | no | no |
| AGENZIA PER LO SVILUPPO E L'INNOVAZIONE ASI SRL | in-house | Veneto | 63 | 2,3 | 41 | [www.asi-srl.it](https://www.asi-srl.it/) | 0 | no | no |
| SISAM SERVIZI S.R.L. | in-house | Lombardia | 13 | 2,1 | 7 | [www.sisamspa.it](https://www.sisamspa.it) | 0 | errore-SSLError |  |
| S.E.D. SERVIZI ELABORAZIONE DATI S.P.A. CON SOCIO UNICO | in-house | Abruzzo | 1 | 1,8 | 22 | [www.sedaq.it](https://www.sedaq.it) | 0 | no | no |
| ORGANIZZAZIONE PROGETTI E SERVIZI S.P.A. IN SIGLA 'O.P.S'. S… | in-house | Abruzzo | 2 | 1,6 | 27 |  | 0 |  |  |
| SANNIO EUROPA SOCIETA' CONSORTILE A R.L. | in-house | Campania | 1 | 1,4 | 18 | [www.sannioeuropa.com](http://www.sannioeuropa.com/) | 0 | no | no |
| ESTEEM S.R.L.U. | in-house | Toscana | 1 | 1,3 | 31 | [www.esteemsrl.it](http://www.esteemsrl.it) | 0 | sì | no |
| CST - SISTEMI SUD - S.R.L. | in-house | Campania | 23 | 1,2 | 3 | [www.cstsistemisud.it](https://www.cstsistemisud.it) | 1 (1 ed., 0 man.) | no | no |
| INTER.CAM. SOCIETA' CONSORTILE A R.L. | in-house | Umbria | 37 | 1,1 | 25 |  | 0 |  |  |
| T.A.S.K. - TELEMATIC APPLICATIONS FOR SYNERGIC KNOWLEDGE S.R… | in-house | Marche | 63 | 1,1 | 16 |  | 0 |  |  |
| AFRAGOL@NET S.R.L. UNIPERSONALE | in-house | Campania | 1 | 0,8 | 20 |  | 0 |  |  |
| ASMENET CALABRIA SOC. CONS. A R.L. | in-house | Calabria | 213 | 0,6 | 5 | [www.asmenetcalabria.it](https://www.asmenetcalabria.it) | 0 | no | no |
| ASMENET SOC. CONS. A R. L. | in-house | Campania | 233 | 0,5 | 4 | [www.asmenet.it](https://www.asmenet.it) | 0 | no | no |
| AZIENDA SERVIZI STRUMENTALI PINEROLO S.R.L. | in-house | Piemonte | 1 | 0,3 | 5 |  | 0 |  |  |
| MONTEPULCIANO SERVIZI S.R.L. | in-house | Toscana | 1 | 0,2 |  |  | 0 |  |  |
| TELEPHARMATEC S.R.L. | in-house | Marche | 1 | 0,1 |  |  | 0 |  |  |
| CITIMAP SOCIETA' CONSORTILE A R.L. | in-house | Emilia Romagna | 1 | 0,1 | 1 | [www.citimap.it](http://www.citimap.it) | 0 | no | no |
| TERRE D'AMORE IN ABRUZZO SCARL | in-house | Abruzzo | 45 | 0,0 |  |  | 0 |  |  |
| 3-I S.P.A. | in-house | Lazio | 3 | 0,0 |  | [www.3-i.gov.it](https://www.3-i.gov.it) | 0 | no | no |
| PESCARAINNOVA S.R.L. | in-house | Abruzzo | 17 |  |  |  | 0 |  |  |
| CONSORZIO METIS | in-house | Toscana | 11 |  | 110 | [www.consorziometis.it](https://www.consorziometis.it) | 0 | no | no |
| FONDAZIONE TICHE -FONDAZIONE DI PARTECIPAZIONE | in-house | Campania | 22 |  |  |  | 0 |  |  |
| CONSORZIO INTERUNIVERSITARIO ALMA LAUREA | in-house | Emilia Romagna | 60 |  | 38 | [www.almalaurea.it](https://www.almalaurea.it) | 0 | no | no |
| CINECA CONSORZIO INTERUNIVERSITARIO | in-house | Emilia Romagna | 77 |  | 1136 | [www.cineca.it](https://www.cineca.it) | 0 | HTTP 403 |  |
| CONSORZIO PER IL SISTEMA INFORMATIVO (CSI PIEMONTE) | in-house | Piemonte | 96 |  | 1047 | [www.csipiemonte.it](https://www.csipiemonte.it) | 16 (15 ed., 1 man.) | sì | no |
| CO.SE.A. - CONSORZIO SERVIZI AMBIENTALI | in-house | Emilia Romagna | 15 |  | 10 |  | 0 |  |  |
| TRADIZIONE DELLE TERRE OCCITANE SOCIETA' CONSORTILE A RESPON… | in-house | Piemonte | 15 |  | 2 | [www.tradizioneterreoccitane.com](https://www.tradizioneterreoccitane.com) | 0 | no | no |
| CONSORZIO TOPIX - TORINO E PIEMONTE EXCHANGE POINT | in-house | Piemonte | 9 |  | 28 | [www.top-ix.org](https://www.top-ix.org) | 0 | no | no |
| ARSENA'L.IT - CENTRO VENETO RICERCA E INNOVAZIONE PER LA SAN… | in-house | Veneto | 13 |  | 56 | [www.consorzioarsenal.it](https://www.consorzioarsenal.it/) | 0 | no | no |
| PNICUBE | in-house | Piemonte | 12 |  |  | [www.pnicube.it](https://www.pnicube.it) | 0 | no | no |
| SISTEMI PER I SERVIZI DI PAGAMENTO S.R.L. - SIMPLYCITY | in-house | Emilia Romagna | 1 |  |  |  | 0 |  |  |
| TESIP S.R.L. - TECNOLOGIE E SISTEMI INFORMATIVI PREVIDENZIALI | in-house | Lazio | 1 |  | 6 |  | 0 |  |  |
| CONSORZIO SANNIO.IT | in-house | Campania | 4 |  | 1 | [www.cstsannio.it](https://www.cstsannio.it/) | 0 | errore-ConnectTimeout |  |
| PROMOCAMERA PERUGIA - AZIENDA SPECIALE DELLA CCIAA DELL'UMBR… | in-house | Umbria | 1 |  | 7 |  | 0 |  |  |
| CONSORZIO GE-DIX - GENOVA DATA INTERNET EXCHANGE | in-house | Liguria | 5 |  |  |  | 0 |  |  |
| GRUPPO AZIONE LOCALE CASTELL'UMBERTO NEBRODI SOCIETA' CONSOR… | in-house | Sicilia | 3 |  |  |  | 0 |  |  |
| A.C. SERVICE ESTENSE S.R.L. | in-house | Emilia Romagna | 1 |  | 4 |  | 0 |  |  |
| ACI INFORMATICA SOCIETA' PER AZIONI' IN BREVE 'ACI INFORMATI… | in-house | Lazio | 1 |  | 546 | [www.informatica.aci.it](https://www.informatica.aci.it/) | 0 | sì | no |
| SOGEI - SOCIETA' GENERALE D'INFORMATICA - S.P.A. E IN FORMA … | controllata | Lazio | 1 | 1.009,2 | 2768 | [www.sogei.it](https://www.sogei.it) | 1 (0 ed., 1 man.) | HTTP 403 |  |
| PAGOPA S.P.A. | controllata | Lazio | 1 | 78,8 | 319 | [www.pagopa.it](https://www.pagopa.it) | 9 (9 ed., 0 man.) | no | no |
| CONINET SOCIETA' PER AZIONI IN BREVE CONINET S.P.A. | controllata | Lazio | 1 | 5,5 | 41 | [www.coninet.it](https://www.coninet.it) | 0 | no | no |
| SAIM - SUEDTIROL ALTO ADIGE INFORMATICA MEDICA SRL IN LIQUID… | controllata | Trentino Alto Adige | 1 | 1,1 | 2 | [www.saim.bz.it](https://www.saim.bz.it/) | 0 | errore-ConnectionError |  |
| TECNOBORSA - CONSORZIO PER LO SVILUPPO DEL MERCATO IMMOBILIA… | controllata | Lazio | 8 | 1,1 | 7 | [www.tecnoborsa.com](https://www.tecnoborsa.com/) | 0 | no | no |
| EHEALTHNET SOCIETA' CONSORTILE A RESPONSABILITA' LIMITATA | controllata | Campania | 7 | 0,3 |  | [www.ehealthnet.it](http://www.ehealthnet.it) | 0 | no | no |
| DRIVING ADVANCES OF ICT IN SOUTH ITALY - NET SOCIETA' CONSOR… | controllata | Puglia | 4 | 0,1 |  |  | 0 |  |  |
| PATTO TERRITORIALE DELLA PROVINCIA DI BENEVENTO SOC. CONS. A… | controllata | Campania | 2 | 0,0 | 1 |  | 0 |  |  |
| TAG S.R.L. IN LIQUIDAZIONE | controllata | Veneto | 3 | 0,0 |  |  | 0 |  |  |
| AGENZIA RADIO TRAFFIC SOCIETA' PER AZIONI | controllata | Lombardia | 1 |  | 12 |  | 0 |  |  |
| SERVIZI ALLA MOBILITA' METROPOLITANA S.A.M.M. S.R.L. | controllata | Toscana | 1 |  | 4 |  | 0 |  |  |
| CITYLINK S.R.L. - SMART MOBILITY BY ATM | controllata | Lombardia | 1 |  | 5 |  | 0 |  |  |
| LUTECH DIGITAL AIRPORT S.R.L. | controllata | Lombardia | 1 |  | 40 |  | 0 |  |  |
| FONDAZIONE 'SISTEMA TOSCANA | controllata | Toscana | 1 |  | 78 | [www.fondazionesistematoscana.it](https://www.fondazionesistematoscana.it) | 0 | no | no |
| SARA SERVICES S.R.L. | controllata | Lazio | 1 |  |  |  | 0 |  |  |
| GEOWEB S.P.A IN FORMA ABBREVIATA GEOWEB | controllo-pubblico-congiunto | Lazio | 2 | 6,9 | 27 |  | 0 |  |  |
| CONSORTIUM GARR (GESTIONE AMPLIAMENTO RETE RICERCA) | controllo-pubblico-congiunto | Lazio | 6 |  | 80 |  | 0 |  |  |
| CONSORZIO T3 LAB | controllo-pubblico-congiunto | Emilia Romagna | 1 |  | 9 |  | 0 |  |  |
| LABORATORIO DI MONITORAGGIO E MODELLISTICA AMBIENTALE PER LO… | controllo-pubblico-congiunto | Toscana | 2 |  | 27 | [www.lamma.toscana.it](https://www.lamma.toscana.it) | 0 | no | no |
| CONSORZIO PER LE TECNOLOGIE DELL'INFORMAZIONE E COMUNICAZION… | controllo-pubblico-congiunto | Toscana | 1 |  |  |  | 0 |  |  |
| POLO STRATEGICO NAZIONALE S.P.A. | controllata-sostanzialmente | Lazio | 2 | 78,3 | 24 |  |  |  |  |
<!-- /GEN:tabella -->

## 5bis. Che cosa comprano e che cosa ricevono

La [vista per società](/dati/inhouse/vista.md) incrocia il dataset con i CIG ANAC per **codice fiscale o partita IVA**
(la partita IVA viene dall'anagrafica ANAC delle stazioni appaltanti: i consorzi come CINECA ne hanno una diversa dal
codice fiscale): per ogni società, gli acquisti per stato dell'imbuto (cloud esterno per giurisdizione, cloud in
proprio, ICT non cloud, incerto) e gli affidamenti ricevuti dagli enti, dal 2024. Compaiono nei CIG 61 delle 99
società ICT pubbliche. Il riconoscimento per codice fiscale trova 1.273 CIG da datacenter che il vecchio elenco per
nome non vedeva, e ne perde 53 (da controllare) [V].

## 6. File scaricabili

Licenza CC BY 4.0 (citare il MEF per il censimento e questo progetto per le colonne aggiunte).

<!-- GEN:file -->
| file | contenuto | sha256 |
|---|---|---|
| [societa-ict-pa.csv](/dati/inhouse/societa-ict-pa.csv) | una riga per società ICT nel censimento MEF: classe, ATECO, enti, quote, fatturato, addetti, sito | `b7b6417f88207b65…` |
| [opensource.csv](/dati/inhouse/opensource.csv) | per in-house e controllate: catalogo del riuso (editore, manutentore) e indizi dalla home page | `3db4383e3d58d76d…` |
| [catalogo-riuso.csv](/dati/inhouse/catalogo-riuso.csv) | i software del catalogo Developers Italia legati a ciascuna società | `413d153cb0522ac9…` |
| [vista.md](/dati/inhouse/vista.md) | che cosa comprano e che cosa ricevono dagli enti, per società (CIG ANAC dal 2024, per codice fiscale) | `f0e908fff8f584bb…` |
| [riepilogo.json](/dati/inhouse/riepilogo.json) | conteggi, fonte con sha256, controprova con l'elenco Assinter | `b1f4d2219026ca11…` |
| [opensource-riepilogo.json](/dati/inhouse/opensource-riepilogo.json) | conteggi dell'analisi open source e sha256 delle copie del catalogo | `b4914727234cce92…` |
<!-- /GEN:file -->

## 7. Limiti

- **Dati del 2023:** il censimento esce con più di due anni di ritardo; società nate o fuse dopo non ci sono.
- **ATECO dichiarato dagli enti:** una società ICT dichiarata con un'altra attività sfugge, se non è socia Assinter.
- **Tipo di controllo spesso vuoto** per i consorzi (CSI Piemonte, CINECA): li riconosciamo dall'affidamento diretto.
- **Home page:** un solo sguardo, senza seguire i collegamenti.
- **Quote pubbliche indirette:** il censimento non le quantifica; 10 società restano da verificare a mano.
- **Soci quotati controllati dallo Stato:** contano solo per la classe «controllata sostanzialmente»; le quote di Leonardo, Poste e TIM sono da riconfermare su fonte primaria.

## Registro delle revisioni

| versione | data | modifica |
|---|---|---|
| 0.4 | 2026-11-20 | § 2bis corretto con la ricerca sulla giurisprudenza: l'esclusione «per il tramite di quotate» è nel d.lgs. 33/2013, non più nel testo unico; contrasto sul controllo in concreto; 75 % senza Leonardo da settembre 2026 |
| 0.3 | 2026-11-20 | classe «controllata sostanzialmente» (soci quotati controllati dallo Stato); PSN: argomenti di fatto e di diritto (§ 2bis) |
| 0.2 | 2026-11-20 | classe «controllo pubblico congiunto» (quota pubblica ≥ 50 %, calcolata a catena, verifiche a mano dei soci); partita IVA dall'anagrafica ANAC; vista per società per codice fiscale (#82) |
| 0.1 | 2026-11-20 | prima versione: censimento MEF 2023, siti, catalogo del riuso, home page (#82) |
