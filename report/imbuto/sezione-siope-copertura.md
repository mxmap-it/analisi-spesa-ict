### 4.13 Riscontro con la spesa pagata: SIOPE e BDAP (#12, #67; nuovo, 10/11/2026)

**Inserita nel rendiconto imbuto 0.16.** Verifica `tools/verifiche/siope_ict_enti.py` (sul server,
circa 10 minuti, un job alla volta); esiti `esiti/2026-11-10/siope/` (`ict-enti.json`, `ict-enti.csv`,
`ict-enti-scarti.csv`); pagina [SIOPE](/progetto/siope/) [V].

**Quanto si paga davvero in ICT.** Enti non statali (SIOPE, codici gestionali ICT del piano dei conti,
senza telefonia): 2,99 / 3,30 / 3,97 / 4,62 mld nel 2022-2025. Stato centrale (BDAP, gestionali ICT):
0,99 / 1,20 / 1,14 / 1,29 mld. **Totale pagato: 4,0 / 4,5 / 5,1 / 5,9 mld** (più 0,3-0,4 di telefonia)
[V sulle fonti; somma nostra]. È un minimo: la sanità non ha codici per l'hardware; le società
pubbliche e in-house non sono in SIOPE.

**Quanto ne vede l'imbuto.** CIG ICT S3-S6 pubblicati (tutte le stazioni appaltanti): 9,47 / 12,16 /
14,02 / 15,31 mld nel 2022-2025 [V]. I 56,06 mld S3-S6 «dal 2024» al netto dei tetti sono circa 2,9
annualità, quindi circa 19 mld l'anno: **l'imbuto è tre volte e mezzo il pagato**. Non è un errore
dell'imbuto, è la natura dei due numeri:

| | 2024 |
|---|---:|
| CIG ICT pubblicati (S3-S6) | 14,02 mld |
| di cui stazioni appaltanti enti SIOPE (per CF) | 6,71 |
| di cui Stato | 1,69 |
| di cui fuori SIOPE (società pubbliche, in-house, centrali di committenza) | 5,62 |
| pagato ICT enti SIOPE | 3,97 |
| pagato ICT Stato (BDAP) | 1,14 |

A parità di enti (SIOPE, abbinati per codice fiscale) il rapporto CIG pubblicati / pagato è **1,68**;
la quota annua dei contratti attivi / pagato è **2,2** [V]. I CIG sono importi di lotto (base d'asta,
valore stimato con opzioni, pluriennali), il pagato è cassa dell'anno: il rapporto va letto come
«euro di contratti per euro pagato», non come copertura.

**Dubbi che si tolgono.**
1. *L'imbuto perde enti?* No: nel 2024 solo 740 enti su 10.180 con pagamenti ICT non hanno alcun CIG
   ICT, per 16,8 M€ (0,4 % del pagato) [V].
2. *Gli importi CIG sono spesa?* No: sovrastimano la spesa annua da 1 (comuni < 5.000 abitanti, CIG/pagato
   0,98) a 4 volte (sanità); le cifre in euro dell'imbuto vanno dette «valore dei contratti», non «spesa».
3. *Dove l'imbuto è cieco?* Dove la spesa va a in-house senza CIG: Regione Lombardia (≈ 300 M€ l'anno
   pagati, quota CIG 0,03, nessun CIG verso ARIA), MEF e Sogei per lo Stato (BDAP: quota 0,25); per
   Venezia, ARPAL Umbria e ARPEA gli affidamenti in-house hanno CIG solo dal 2024-2025 (sotto) [V].
4. *Dove l'imbuto gonfia?* Sanità: 192 enti (quasi tutti ASL e AO) con quota CIG oltre 5 volte il
   pagato ICT; parte è hardware pagato su codici sanitari non ICT [stima].
5. *La sanità SIOPE è credibile?* Sì per i servizi: 674 M€ pagati (3212) contro 720 di costo nel CE SSN
   (BA1620) nel 2024 [V].

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

**Proposta.** Aggiungere all'imbuto uno **strato di riscontro R** (non sommato alla spesa) con, per ogni
ente abbinato per CF: pagato ICT SIOPE o BDAP dell'anno, quota annua CIG, indicatore di copertura e le
due bandiere «contratti mancanti» (< 0,2) e «CIG da rivedere» (> 5). Nel testo dell'imbuto, gli euro
dei CIG si presentano con accanto il pagato (≈ 5,1 mld nel 2024). Raccomandazione R83.
