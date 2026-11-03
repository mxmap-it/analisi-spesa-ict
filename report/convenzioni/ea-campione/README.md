# Campione EA Microsoft: quota cloud e on-premise in euro (#55)

Versione 0.2, 3/11/2026. Lavoro in corso: tutti i 50 C1 cercati; C2, C3 ed E solo in parte.

## Sintesi
- **Atti trovati: 7 su 120.** Ricerche fatte su 62 contratti (50 C1, 8 C2, 4 C3; nessun E). **Carrello completo in euro: 1** (AIFA, C2). Carrello con quantità ma senza prezzi: 1 (MAECI, C1).
- **AIFA B9907C4EF3 (EA9, 737.500,14 € IVA esclusa, V):** cloud **726.183,00 €** (98,5 %), on-premise **11.317,14 €** (6 SQL Server Standard Core LSA). Il carrello è nella relazione tecnica: O365 E3/E1, EMS E3/E5, Advanced Data Residency Italy, M365 Copilot, Power Platform.
- **MAECI B89CF8349C (EA9, 9.408.828,36 € IVA inclusa, V):** 8.000 utenti M365 E3 (cloud) e 128 core SQL Server Enterprise SA (on-premise). Gli euro per riga non sono pubblicati, quindi gli euro certi sono tutti «non attribuibili». **Stima a listino (non verificata):** on-premise circa 0,9 M€ IVA esclusa (circa 12 %), il resto cloud.
- **Quota cloud per strato:** con 1 solo carrello completo **non si può calcolare nessun intervallo**: C1 n.d., C2 n.d. (1 contratto non fa una stima), C3 n.d., E n.d. Il dato AIFA (98,5 %) e la stima MAECI (circa 88 %) vanno nella stessa direzione dei casi già noti (Calabria EA6, ART e Archivi notarili EA8, tutti SaaS). Restano però indicazioni: nessuno dei due è una stima.
- **Importi C1, controllati sui dati ANAC (CIG e aggiudicazioni):** su 388,8 M€ del C1, circa **61,2 M€ sono doppioni o errori probabili**:
  - ANAS: 17,75 M€ registrati due volte con lo stesso oggetto.
  - ASL Caserta: 37,07 M€ = 10 × 3,71 M€, probabile errore di un ordine di grandezza; anche i due CIG da 3,71 M€ sono doppioni fra loro.
  - DTD Giustizia: 4,71 M€ registrati due volte.
  - Archivi notarili: 1,68 M€ registrati due volte.
- **Altri importi C1 da tenere a parte:**
  - Terna (47,9 M€ a base, 43,6 M€ aggiudicati) è una **gara propria con Microsoft Ireland**, non EA Consip.
  - ANCI (45 M€) è legato da ANAC all'EA6: come fabbisogno di un'associazione non è plausibile, va verificato.
- **Atti senza carrello: 5** (Consob, ARERA, Calabria, ISTAT, oltre a MAECI con i soli SKU). Danno l'importo ma non la composizione.
  - Consob distingue solo i capitoli di bilancio: 99,9 % sul capitolo «servizi informatici e cloud». È un indizio, non un carrello.

## Metodo
1. **Livelli L0-L1 (ANAC, deterministico):** per i 120 CIG si estraggono dai CIG 2024-2025 e dalle aggiudicazioni l'accordo quadro (EA6/7/8/9 o procedura propria) e l'importo aggiudicato (`anac.csv`). Risultato: 4 EA6, 4 EA7, 46 EA8, 33 EA9, 26 procedure proprie o affidamenti, 7 altri accordi quadro.
2. **Livello L5 (ricerca web):** circa 60 ricerche per CIG, per ente + oggetto + anno e per edizione EA. Gli atti trovati sono archiviati sul server con `tools/archivia.py` (sha256 in `risultati.csv`) e letti con pdftotext.
3. **Confine R-S5** (`../ea-quota-cloud-elaborazione.md` §1). Advanced Data Residency è un add-on cloud. SQL Server LSA/SA è on-premise.
4. **Stime a listino** (colonne `stima_*`): solo dove ci sono le quantità, con i prezzi EA9 letti nell'atto AIFA. Sono marcate come stima e non entrano negli euro certi.
5. Tutto il calcolo è in `node tools/verifiche/ea_campione.js`, che genera `risultati.csv` e `stime.txt` da `campione.csv`, `anac.csv` e `letture.json`. Le letture sono l'unico input manuale e sono il punto di ripresa.

## Tabella
`risultati.csv`: una riga per contratto (120). La colonna `stato_ricerca` vale «atto letto», «cercato … atto non trovato» oppure «non ancora cercato».

## Limiti (verificato e riferito)
- **Resa della ricerca web:** 7 atti su 62 contratti cercati (11 %), in linea con la misura del giro 2 (circa 1 su 10, `acquisizione-documenti.md`). Gli albi delle ASL e i portali delle società partecipate non sono indicizzati dai motori. Il sito dell'ASL Caserta era in timeout già il 29/10.
- **L'atto spesso non contiene il carrello:** su 7 atti trovati, il carrello completo c'è in 1 (AIFA, in un allegato zip della pagina «Lavori, servizi e forniture»). Il carrello sta nell'ordinativo MePA/acquistinretepa, che non leggiamo nel rispetto del robots.txt.
- **Stima MAECI:** usa il rapporto di listino pubblico Enterprise/Standard di SQL Server (3,83) applicato al prezzo EA9 AIFA. Non è verificata.
- **Strati C2, C3 ed E:** ancora in gran parte da cercare (58 contratti non cercati). Per E nessuna verifica dell'oggetto esplicito.

## Contratti senza carrello pubblicato (finora)
| cig | ente | perché l'atto online non basta |
|---|---|---|
| B89CF8349C | MAECI | SKU e quantità senza prezzi per riga |
| B84589CB74 | Regione Calabria | l'atto letto è una nomina; il decreto di adesione dell'aprile 2024 non è indicizzato |
| B76FB69827 | Consob | decisione a contrarre con solo importi per capitolo |
| B204DD6DAB | ARERA | determinazione con solo importo triennale |
| B6C1D27A41 | ISTAT | contratto indicizzato ma non scaricabile (404); EES education, non EA |
| altri 43 C1 cercati | vari | atto non trovato online con la ricerca web; prima di qualunque accesso civico serve il livello L4 (crawling di Amministrazione trasparente) |

L'accesso civico è l'ultima risorsa e richiede la decisione di Fabio. Prima vanno provati L4 sui siti degli enti C1 e la lettura del decreto DGSIA del 6/5/2024 (EA8 Giustizia, altro CIG).

## Registro delle revisioni
| data | versione | modifica |
|---|---|---|
| 2026-11-03 | 0.1 | avvio: 2 atti |
| 2026-11-03 | 0.2 | tutti i C1 cercati; AIFA con carrello completo; importi C1 controllati su ANAC; verifica ripetibile `tools/verifiche/ea_campione.js` |
