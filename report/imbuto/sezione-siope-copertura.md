### 4.13 Riscontro con la spesa pagata: SIOPE e BDAP (#12, #67; nuovo, 10/11/2026)

**Pronto da inserire nel rendiconto imbuto.** Verifica `tools/verifiche/siope_ict_enti.py` (sul server,
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
   pagati, quota CIG 0,03), Comune di Venezia, MEF e Sogei per lo Stato (BDAP: quota 0,25) [V sui
   numeri; l'in-house è un'ipotesi da verificare].
4. *Dove l'imbuto gonfia?* Sanità: 192 enti (quasi tutti ASL e AO) con quota CIG oltre 5 volte il
   pagato ICT; parte è hardware pagato su codici sanitari non ICT [stima].
5. *La sanità SIOPE è credibile?* Sì per i servizi: 674 M€ pagati (3212) contro 720 di costo nel CE SSN
   (BA1620) nel 2024 [V].

**Proposta.** Aggiungere all'imbuto uno **strato di riscontro R** (non sommato alla spesa) con, per ogni
ente abbinato per CF: pagato ICT SIOPE o BDAP dell'anno, quota annua CIG, indicatore di copertura e le
due bandiere «contratti mancanti» (< 0,2) e «CIG da rivedere» (> 5). Nel testo dell'imbuto, gli euro
dei CIG si presentano con accanto il pagato (≈ 5,1 mld nel 2024). Raccomandazione R83.
