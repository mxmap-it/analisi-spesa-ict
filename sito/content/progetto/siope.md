---
title: "SIOPE, la spesa ICT pagata per ente"
date: 2026-11-09
description: "Che cosa c'è in SIOPE, quali codici gestionali sono ICT, quanto pagano in ICT gli enti non statali 2022-2025 e quanto dei loro pagamenti vedono i CIG ICT dell'imbuto."
---

**Versione 0.2 del 10/11/2026** ([#12](https://github.com/mxmap-it/analisi-spesa-ict/issues/12), [#67](https://github.com/mxmap-it/analisi-spesa-ict/issues/67), [#30](https://github.com/mxmap-it/analisi-spesa-ict/issues/30)).
Legenda: **[V]** verificato da noi su file archiviati con sha256; **[R]** riferito da altri o dalla
documentazione della fonte; **stima** quando c'è un'ipotesi in mezzo.

## In breve

- **Gli enti non statali (regioni, sanità, comuni, università, enti di ricerca, scuole...) hanno
  pagato in ICT 3,97 miliardi nel 2024** (2,99 nel 2022, 3,30 nel 2023, 4,62 nel 2025), più
  0,35 miliardi di telefonia [V]. Con lo Stato centrale da BDAP (1,14 miliardi) la **spesa ICT
  pubblica pagata nel 2024 è circa 5,1 miliardi** (5,5 con la telefonia) [V sulle due fonti, somma
  nostra].
- Gli stessi enti, abbinati per **codice fiscale** alle stazioni appaltanti ANAC, hanno pubblicato nel
  2024 CIG ICT (strati S3-S6) per **6,67 miliardi**: **1,68 euro di CIG per ogni euro pagato**; la
  quota 2024 dei contratti attivi (dal 2020) vale 8,79 miliardi, 2,2 volte il pagato [V].
- **L'imbuto non perde enti, sopravvaluta gli importi.** Degli enti con pagamenti ICT nel 2024, 740 su
  10.180 non hanno alcun CIG ICT: 16,8 milioni, lo 0,4 % del pagato [V]. Il rapporto CIG/pagato va da
  0,98 nei comuni sotto i 5.000 abitanti a 4 nella sanità.
- **Dove l'imbuto è cieco** (molto pagato, pochi CIG): la **Regione Lombardia** (gestione sanitaria
  accentrata) paga in ICT circa 300 milioni l'anno contro 7-14 milioni di CIG suoi: è la spesa verso la
  società in-house regionale, senza CIG proprio [V sui numeri, interpretazione da verificare]; poi
  Comune di Venezia, ARPAL Umbria, ARPEA Piemonte.
- La sanità SIOPE torna con il Conto economico SSN: assistenza informatica pagata 674 milioni nel
  2024 contro 720 milioni di costo (voce BA1620) [V].

## Ente, portale, accesso

| | |
|---|---|
| Ente | Ragioneria generale dello Stato e Banca d'Italia (SIOPE, art. 14 l. 196/2009; SIOPE+ dal 2018) |
| Portale | <https://www.siope.it/> (open data in `documenti/siope2/open/last/`) |
| File | `SIOPE_USCITE.<anno>.zip` (2017-2026, 70-77 MB ciascuno, CSV di 400 MB: codice ente, anno, mese, codice gestionale, importo in **centesimi**), `SIOPE_ANAGRAFICHE.zip` (enti con codice fiscale, comparti e sottocomparti, codici gestionali con descrizione) [V] |
| Archivio | `archivio/mirror/www.siope.it/documenti/siope2/open/last/` (11 file, 702 MB, 6/11/2026; file del 5/11/2026) [V] |
| Natura | **cassa** (pagamenti per mese), non competenza; tutti gli enti della PA tranne lo Stato centrale, che è in BDAP |

Il mirror è **completo** per quel che serve: tutte le annualità 2017-2026 e le anagrafiche. Il nome
`last` si sovrascrive alla fonte: le versioni restano nei blob dell'archivio (sha256 nell'esito).
SIOPE via BDAP (per regione) e diretto coincidono sull'ICT, ma BDAP **tronca il 2025** di Lombardia e
Friuli-Venezia Giulia a marzo (§ SIOPE via BDAP in [BDAP](/progetto/bdap/), R75): si usa il diretto.

## I codici ICT

Lista definita sulle descrizioni dell'anagrafica `ANAG_CODGEST_USCITE` (archiviata) [V]:

| Categoria | Piano dei conti armonizzato (tutti i comparti tranne SAN e STA) | Sanità (comparto SAN, codici a 4 cifre) |
|---|---|---|
| servizi | 1.03.02.19.001-011 e .999 (gestione applicazioni, assistenza utenti, interoperabilità, rete dati e VoIP, sistemi, sicurezza, documentale, monitoraggio, postazioni, consulenza ICT, processi trasversali, altri) | 3212 assistenza informatica e manutenzione software |
| licenze | 1.03.02.07.006 licenze d'uso per software | 5205 licenze software |
| noleggi | 1.03.02.07.004 noleggi di hardware | — |
| materiale | 1.03.01.02.006 materiale informatico | — |
| hardware | 2.02.01.07.* (server, postazioni, periferiche, apparati TLC, tablet, n.a.c.) e 2.02.04.07.* (in leasing) | **nessun codice proprio** |
| software (investimento) | 2.02.03.02.001/002 sviluppo e acquisto software, 2.02.06.01.001 in leasing | — |
| telefonia (a parte) | 1.03.02.05.001/002 telefonia fissa e mobile | 3208 telefonia e reti di trasmissione |
| misti, solo limite superiore | — | 2204 supporti informatici e cancelleria, 6200 immobilizzazioni immateriali |

Sono tutti codici di **acquisto**: i trasferimenti fra enti (1.04, 2.03, 41xx) non entrano, quindi non
c'è doppio conteggio da trasferimenti. Resta un doppio conteggio possibile quando un ente paga un altro
ente o una sua gestione per un servizio ICT (es. le centrali pagamenti regionali del SSN), non misurato.
Lo Stato (comparto STA) è escluso: si misura con BDAP.

## Le misure (verifica `tools/verifiche/siope_ict_enti.py`)

Esiti in `esiti/2026-11-10/siope/`: `ict-enti.json` (tabelle, sha256 di ogni ingresso, codici usati),
`ict-enti.csv` (un ente per codice fiscale, 2022-2025: pagato ICT, telefonia, totale, CIG, quota),
`ict-enti-scarti.csv` (enti fuori scala nei due sensi) [V].

**Pagato ICT degli enti non statali** (11.532 codici fiscali con pagamenti) [V]:

| Anno | ICT | di cui servizi | hardware | software inv. | licenze | telefonia (a parte) |
|---|---:|---:|---:|---:|---:|---:|
| 2022 | 2.993 M€ | 2.074 | 297 | 359 | 195 | 387 |
| 2023 | 3.297 M€ | 2.216 | 325 | 452 | 235 | 353 |
| 2024 | 3.975 M€ | 2.638 | 405 | 549 | 297 | 353 |
| 2025 | 4.618 M€ | 2.999 | 417 | 756 | 359 | 321 |

**2024 per comparto** (CIG = strati S3-S6 dell'imbuto, SA abbinata per CF; quota = parte 2024 dei
CIG attivi pubblicati dal 2020) [V]:

| Comparto | Enti | Pagato ICT | CIG pubblicati 2024 | Quota 2024 CIG attivi | quota / pagato |
|---|---:|---:|---:|---:|---:|
| Regioni (con gestioni sanitarie) | 43 | 1.372 M€ | 1.357 | 1.653 | 1,2 |
| Comuni, province, città metropolitane, unioni | 8.516 | 1.035 | 1.445 | 2.063 | 2,0 |
| Sanità | 238 | 659 | 2.623 | 3.380 | 5,1 |
| Università | 70 | 357 | 408 | 508 | 1,4 |
| Enti di ricerca | 30 | 170 | 303 | 398 | 2,3 |
| Comunità montane e altri enti locali | 726 | 103 | 144 | 190 | 1,8 |
| Scuole e altri enti in contabilità finanziaria | 1.671 | 79 | 80 | 158 | 2,0 |

**Comuni per dimensione** (popolazione dell'anagrafica SIOPE), quota / pagato: sotto 5.000 abitanti 1,4
(CIG pubblicati / pagato 0,98), 5-20 mila 1,8, 20-100 mila 2,6, oltre 100 mila 2,2 [V]. Nei piccoli
comuni l'imbuto e la cassa si somigliano; più l'ente è grande, più pesano i contratti pluriennali e
gli importi a base d'asta.

**Per regione** la quota / pagato va da 1,1 (Valle d'Aosta) e 1,4 (Trentino-Alto Adige) a 3,0-3,4
(Sicilia, Calabria, Campania, Basilicata) [V]: dove l'imbuto pesa di più rispetto al pagato ci sono
più CIG sanitari e più contratti pluriennali.

**Sanità contro Conto economico SSN** (BDAP, voce BA1620 «servizi di assistenza informatica»,
consolidato regionale «999»): 530, 604, 720 M€ nel 2022-2024; SIOPE codice 3212 sugli enti sanitari
e le gestioni sanitarie regionali 2024: 674 M€ [V]. Cassa e competenza si avvicinano: SIOPE sanità è
affidabile per i servizi; manca l'hardware, che il piano dei conti sanitario non separa.

## Abbinamento con i CIG e scarti

- CIG ICT S3-S6 dell'imbuto 2020-2025 con CF della stazione appaltante dal CIG ANAC: 445.709.
- Nel 2024 i CIG ICT (14,02 miliardi in tutto) vanno per **6,71 miliardi a enti SIOPE**, 1,69 a
  stazioni appaltanti statali (CF in IndicePA dei ministeri o comparto STA), **5,62 a soggetti che non
  sono in SIOPE** (società pubbliche e in-house, centrali di committenza, enti non tenuti a SIOPE) [V].
- **Enti con pagato ICT e nessun CIG ICT**: 740 su 10.180 nel 2024, 16,8 M€ (0,4 %); 1.416 nel 2023
  (48 M€); 5.993 nel 2022 (253 M€), quando i CIG sotto 40.000 euro non erano ancora nell'open data [V].
- **Molto pagato, pochi CIG** (pagato 2023-24 ≥ 2 M€, quota CIG < 20 %): 4 enti. Regione Lombardia
  (gestione sanitaria accentrata, CF 80050050154): 297 e 332 M€ pagati in ICT, 7 e 14 M€ di quota CIG
  (rapporto 0,03); Comune di Venezia (CF 00339370272): 19 e 16 M€ contro 1-2; ARPAL Umbria; ARPEA
  Piemonte [V]. L'ipotesi è la spesa verso le società in-house (ARIA, Venis), affidata senza CIG o con
  CIG intestati alla società: **da verificare** sui loro bilanci.
- **Molti CIG, poco pagato** (quota CIG > 5 volte il pagato, ≥ 2 M€): 192 enti, quasi tutti ASL e
  aziende ospedaliere (ARES Sardegna, ASL Napoli 3 Sud, ASST Bergamo Ovest, ASL Caserta...) [V]. Cause
  probabili: hardware e apparecchiature con componente ICT pagati su codici sanitari non ICT (6103,
  6104); importi a base d'asta o massimali; pagamenti accentrati su un altro CF (centrali pagamenti
  regionali, gestioni liquidatorie).

## Verifica in-house (giro 0.2)

**Verifica dell'ipotesi in-house sui 4 enti «molto pagato, pochi CIG»** (`tools/verifiche/siope_inhouse_4enti.py`,
esito `esiti/2026-11-10/siope/inhouse-4enti.json`: tutti i CIG ANAC 2020-2026 con SA = ente, con aggiudicataria = in-house,
con SA = in-house):

| Ente (CF SIOPE) | In-house (CF) | CIG ente → in-house | Lettura |
|---|---|---|---|
| Regione Lombardia, gestione sanitaria (80050050154) | ARIA S.p.A. (05017630152) | **nessuno, 2020-2026** [V] | ARIA riceve CIG solo da altri enti (202 nel 2024, 154 nel 2025); la Regione le affida senza CIG o con un CF diverso. Che i ≈ 300 M€ ICT pagati vadano ad ARIA è **ipotesi** [R, non verificata: bilancio ARIA non archiviato] |
| Comune di Venezia (00339370272) | Venis S.p.A. (02396850279) | 0 fino al 2023; 1 nel 2024 (27 k€); **17 nel 2025 per 42,7 M€** [V] | Il contratto di servizio 2024-2027 per il sistema informativo comunale (CIG B5F1633320, 27,2 M€, «affidamento diretto a società in house») ha il CIG solo dal 2025: **ipotesi confermata** [V] |
| ARPAL Umbria (03630270548) | PuntoZero S.c.a r.l., ex Umbria Digitale (02915750547) | 2 nel 2024 (0,9 M€), 5 nel 2025 (3,9 M€) [V] | piano d'esercizio e SIL affidati in-house; prima del 2024 nessun CIG: **confermata** [V] |
| ARPEA Piemonte (97694170016) | CSI-Piemonte (01995120019) | 2 nel 2025 (1,2 M€) [V] | servizi applicativi in convenzione in-house; prima del 2025 nessun CIG: **confermata** [V]. Il CSI lavora per gli enti consorziati con convenzioni in esenzione IVA [R, determina ARPA Piemonte 2026] |

Conclusione: per 3 enti su 4 lo scarto è spesa verso la in-house che **fino al 2023 non aveva CIG** e dal
2024-2025 compare come «affidamento diretto a società in house», spesso con durata vuota (quindi tutta
nell'anno di pubblicazione). Per la Regione Lombardia il buco resta anche nel 2024-2025. Gli anni prima
del 2024 sottostimano quindi sistematicamente gli enti con in-house ICT (regioni, grandi comuni). Il bilancio
di Venis 2023 riporta circa 21,7 M€ di valore della produzione [R, ricerca web, non archiviato]; archiviata
la relazione di revisione 2024 (`www.venis.it/.../RelazioneRevinet_14-04-2025.pdf`, senza cifre).

## Avvertenze

1. **Cassa contro contratto.** SIOPE è il pagato dell'anno; il CIG è l'importo del lotto (base d'asta o
   valore stimato, spesso pluriennale, con opzioni). La quota annua spalma l'importo sulla durata; i CIG
   prima del 2020 non ci sono, quindi la quota 2022 è sottostimata.
2. **Abbinamento per CF.** Un CF raccoglie più codici SIOPE (articolazioni, gestioni); l'ente è il CF.
   Le gestioni sanitarie regionali hanno il CF della regione.
3. **La sanità non ha codici hardware**: l'ICT sanitario SIOPE è un minimo.
4. **Telefonia** a parte, perché il perimetro CPV dell'imbuto la tratta in modo diverso a seconda dei
   servizi.

## Come entra nell'imbuto

Strato di **riscontro** (non uno strato di spesa): per ogni ente con CF in SIOPE, accanto ai CIG ICT
si pubblica il pagato ICT SIOPE dell'anno e l'indicatore di copertura *quota annua CIG / pagato ICT*,
con soglie: < 0,2 «contratti mancanti» (in-house, convenzioni intestate ad altri, affidamenti senza
CIG), > 5 «CIG da rivedere» (importi a base d'asta, hardware fuori codici ICT, pagamenti accentrati).
Proposta nel rendiconto imbuto (`report/imbuto/sezione-siope-copertura.md`) e R83.
