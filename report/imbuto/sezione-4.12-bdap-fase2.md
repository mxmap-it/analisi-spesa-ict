<!-- Sezione pronta per il rendiconto «Imbuto: dove siamo» (#66, consegna 12/11/2026), § 4.12 «BDAP fase 2».
     Non è ancora nel rendiconto: chi la inserisce sostituisce il segnaposto § 4.12, aggiorna § 1 (riga «Denominatore
     BDAP» e «In attesa») e § 4.10 (riga «Rapporto CIG ICT / pagato»), aggiunge le due verifiche al § 9 e una riga al
     registro delle revisioni. Cifre dal 9/11/2026, #67 e #30. -->

### 4.12 BDAP fase 2: codice fiscale, quota annua, Sogei, SIOPE (#67, #30, nuovo in 0.11)

Dalla pagina [BDAP](/progetto/bdap/) (versione 0.2, 9/11/2026). Verifiche, dal mirror: `tools/verifiche/bdap_ict_stato.py`
(esito `esiti/2026-11-09/bdap/ict-stato.json`), `tools/verifiche/bdap_cig_ministeri_cf.py` (`esiti/2026-11-09/bdap/cig-ministeri-cf.json`),
`tools/verifiche/siope_bdap_vs_diretto.py 2024` e `2025` (`esiti/2026-11-09/siope/bdap-vs-diretto-<anno>.json`), tutte con lo sha256 dei file.

- **Stazione appaltante → ministero per codice fiscale** (IndicePA: CF degli enti e degli uffici di fatturazione,
  2.661 CF ministeriali) invece che per nome: i CIG ICT ministeriali 2020-2026 passano da 10.758 a 23.644, da 5,0 a
  8,2 miliardi [V]. Per nome se ne perdevano 13.007 per 3,24 miliardi.
- **Giustizia:** il buco era un artefatto della regola sul nome. Nel 2024 i CIG ICT sono 359 per 213 M€ (erano 13 per
  9); la quota 2024 dei contratti attivi vale **0,96** volte il pagato ICT (304 contro 315 M€) [V sui conteggi, stima
  sull'interpretazione].
- **MEF:** il buco resta. Nel 2024 quota dei CIG attivi 97 M€ contro 388 pagati (**0,25**); 0,36 nel 2025 [V]. I
  contratti in-house con Sogei che hanno un CIG con SA del MEF (Dipartimento delle finanze 77 M€ sul triennio
  2024-2026, Giustizia tributaria 47 M€) spiegano circa 26 M€ l'anno [stima]. Ragioneria, Tesoro e Amministrazione
  generale non hanno contratti Sogei con CIG in ANAC [V sull'assenza nei dati] (R71). Peso della criticità 9 ridotto
  da circa 0,7 a circa **0,3 miliardi l'anno**.
- **Sogei come stazione appaltante:** quota 2024 dei suoi CIG ICT attivi circa 0,69 miliardi [V sui conteggi]. Sono
  acquisti per tutti i committenti (MEF e agenzie fiscali), non attribuibili a un ministero, e non vanno sommati al
  pagato del MEF: sarebbe un doppio conteggio della stessa catena in-house.
- **Quota annua dei contratti pluriennali:** ogni CIG si ripartisce sulla durata prevista ANAC. Dal 2024 la durata
  manca nel **90 % dei CIG** (0,1 % nel 2022) [V]: per i contratti 2024-2025 la quota è l'importo intero (R69).
  Rapporti sopra 1 (Difesa 9,1, Cultura 11,5) non sono coperture: per CF entrano uffici con bilancio proprio (musei e
  parchi autonomi, Agenzia industrie difesa).
- **Seconda via per anno** (rendiconto per piano di gestione, CE di 3° livello): 492, 740, 675, 452, 1.007, 979 M€ dal
  2019 al 2024 [V]. Il salto del 2023 è una riclassificazione (MEF da 18 a 297 M€): la controvalidazione vale dal 2023
  (84-86 % della via per gestionali), non prima.
- **SIOPE via BDAP contro SIOPE diretto** (#30; Lazio, Umbria, Basilicata, Molise, Liguria): sui codici ICT 99,4 %
  (2024) e 99,5 % (2025) delle coppie ente × codice uguali all'euro, totali 473,35 contro 473,36 M€ [V]; sul totale
  BDAP è più basso dello 0,7 % (2024) per i pagamenti da regolarizzare. Il **troncamento del 2025 a marzo** riferito da
  AgID [R] non si ripresenta sui file attuali di queste regioni: tutti i 1.507 enti abbinati arrivano a dicembre [V].
  Le altre 15 regioni non sono misurate. BDAP non ha il codice ente (R70): resta la fonte diretta.

Da aggiungere al § 9 (ripetibilità):

```
# sul server, dal mirror (giro 0.2 di BDAP)
nice .venv/bin/python tools/verifiche/bdap_ict_stato.py
nice .venv/bin/python tools/verifiche/bdap_cig_ministeri_cf.py
nice .venv/bin/python tools/verifiche/siope_bdap_vs_diretto.py 2024
nice .venv/bin/python tools/verifiche/siope_bdap_vs_diretto.py 2025
```

Riga per il registro delle revisioni: «§ 4.12 BDAP fase 2: abbinamento per codice fiscale (Giustizia 0,96, MEF 0,25
nel 2024), quota annua e durata mancante dal 2024 (R69), Sogei (R71), seconda via 2019-2024, SIOPE BDAP contro
diretto (#30, R70); criticità 9 a circa 0,3 miliardi».
