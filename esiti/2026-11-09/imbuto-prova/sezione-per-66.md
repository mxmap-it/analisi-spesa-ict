# Prova a secco della rigenerazione dell'imbuto 0.3.4 — sezione pronta per #66

Data: 9/11/2026. Ticket #71 (sotto #66). **Non applicata:** `lavoro/imbuto/ict.csv` (0.3.1, 3/11) e il rendiconto 0.12 restano come sono. Questa sezione serve a scrivere il § 2.6 del rendiconto alla rigenerazione vera, dopo la via 6.

**Executive summary.** Con le tre modifiche insieme (R53 «una riga per CIG col CPV ICT», perimetro CPV 0.3.3, lente v4.3) gli strati ICT **S3-S6 dal 2024, al netto dei tetti, passano a 56,06 mld** [V]. La stima 0.12 era «circa 55,7»: la stessa misura sulla base 0.3.1 dà 55,70 [V], quindi la stima era giusta. Lo scarto di +0,36 mld viene quasi tutto dal perimetro 0.3.3 (+0,48 mld). I CIG ripetuti scendono da 1.016 a **0** [V]. Il residuo S6/G1 cresce di 31 CIG e 3,83 mld dichiarati: sono i 29 CIG nuovi (connettività SPC Consip, ASI, multiutility) più 3 che arrivano da S5. Della selezione via 6 (1.196 CIG G1+G3) **cambiano strato 5 CIG** (27 M€). Nessuno esce dall'imbuto [V].

## Metodo

Quattro varianti calcolate sul mirror ANAC (fonti 2020-2025 + delta), una alla volta. Ogni variante cambia una sola cosa rispetto alla successiva:

| variante | DEDUP_CPV (R53) | perimetro CPV | lente (classifica + config) |
|---|---|---|---|
| A = imbuto 0.3.4 | sì (CPV ICT minimo) | 0.3.3 (79342 fuori, RX_ICT con sw e connettività) | v4.3 |
| B | no (prima riga, 0.3.2) | 0.3.3 | v4.3 |
| C | no | 3/11 (79342 dentro) | v4.3 |
| D | no | 3/11 | 3/11 (commit 4820e09d) |

- Effetto R53 = A − B, effetto perimetro = B − C, effetto lente = C − D.
- «Al netto dei tetti» si calcola come nel rendiconto: per i CIG da 50 M€ in su vale `euro_netti` di `esiti/2026-11-06/imbuto/tetti-cig-v2.csv`, con una riga per CIG.
- Controllo: la variante A riproduce la base CIG per CIG dove non deve cambiare nulla. Anni 2020-2023 e 2026 identici. Nel 2024-2025 mancano 11.043 righe, cioè i doppioni noti della 0.3.2.

Verifica: `tools/verifiche/imbuto_prova_034.py tutto` (sul server, ~2,5 h in sequenza), poi `tools/verifiche/imbuto_prova_034_confronto.py 2026-11-09`. Uscite: `esiti/2026-11-09/imbuto-prova/{confronto.json,g1-nuovi.csv,via6-cambi.csv}`.

## Strati e gruppi dal 2024 (CIG / mld dichiarati) [V]

| strato | base 0.3.1 (tutte le righe) | D | C | B | **A (0.3.4)** |
|---|---|---|---|---|---|
| S0 padre AQ | 88.913 / 0 | 88.792 / 0 | 88.792 / 0 | 88.792 / 0 | **88.792 / 0** |
| S1 escluso non ICT | 3.216.533 / 1.286,32 | 3.207.753 / 1.278,25 | 3.207.752 / 1.278,25 | 3.209.744 / 1.274,53 | **3.209.583 / 1.274,46** |
| S2 sotto soglia | 147.715 / 0,00 | 147.273 / 0,00 | 147.273 / 0,00 | 147.273 / 0,00 | **147.273 / 0,00** |
| S3 convenzione-lotto | 897 / 4,83 | 893 / 3,61 | 891 / 3,61 | 891 / 3,61 | **891 / 3,61** |
| S4 marchio | 8.049 / 3,61 | 8.016 / 3,61 | 8.370 / 3,63 | 8.370 / 3,63 | **8.370 / 3,63** |
| S5 ICT non cloud | 227.830 / 92,40 | 226.459 / 91,12 | 226.004 / 91,09 | 220.279 / 90,68 | **220.525 / 90,76** |
| S6 residuo | 55.946 / 12,50 | 55.654 / 12,25 | 55.758 / 12,26 | 59.491 / 16,39 | **59.406 / 16,37** |
| — G1 mega | 209 / 4,88 | 196 / 4,71 | 196 / 4,71 | 228 / 8,55 | **227 / 8,53** |
| — G2 informazione mancante | 884 / 4,08 | 872 / 4,03 | 867 / 4,03 | 867 / 4,03 | **867 / 4,03** |
| — G3 incerti significativi | 12.615 / 2,94 | 12.542 / 2,91 | 12.569 / 2,92 | 13.451 / 3,17 | **13.437 / 3,16** |
| — G4 coda | 42.238 / 0,61 | 42.044 / 0,60 | 42.126 / 0,61 | 44.945 / 0,65 | **44.875 / 0,65** |

## S3-S6 dal 2024 al netto dei tetti [V]

| | CIG | mld dichiarati | **mld netti** |
|---|---|---|---|
| rendiconto 0.11 (base 55,3) | | | 55,3 |
| rendiconto 0.12 (stima) | | | circa 55,7 |
| base 0.3.1, una riga per CIG | 291.213 | 110,77 | **55,70** |
| D | 291.022 | 110,59 | 55,51 |
| C | 291.023 | 110,59 | 55,52 |
| B | 289.031 | 114,31 | 56,00 |
| **A = imbuto 0.3.4** | **289.192** | **114,38** | **56,06** |

Netti per strato in A: S3 1,32, S4 3,03, S5 40,01, S6 11,70 mld.

## Effetto separato di ogni cambiamento (dal 2024) [V]

| cambiamento | S3-S6 netti | dettaglio |
|---|---|---|
| **R53** (A − B) | +161 CIG, **+0,064 mld** | 161 CIG da S1 a S5 (+246 S5 / −85 S6, di cui 1 G1 −14 M€ e 14 G3). |
| **perimetro 0.3.3** (B − C) | −1.992 CIG, **+0,479 mld** | 79342 fuori: S5 −5.725 CIG (−0,41 mld dichiarati). RX_ICT con sw e connettività: S6 +3.733 CIG (+4,13 mld dichiarati; G1 +32 CIG/+3,84, G3 +882, G4 +2.819). |
| **lente v4.3** (C − D) | +1 CIG, **+0,004 mld** | 354 CIG da S5 a S4 (marchi, +25 M€), +104 S6 (G3 +27). |
| totale (A − D) | −1.830 CIG, **+0,547 mld** | |
| 0.3.2 prima riga contro base una riga (D − base) | −191 CIG, −0,184 mld | CIG con la prima riga del file in S1: è il difetto che R53 corregge in parte. |

- **Perché R53 vale meno dei +0,43 stimati.** Lo 0,43 misurava la sottostima del metodo `imbuto_doppioni.py` (ultima riga). Qui si confronta con la 0.3.2 (prima riga).
- **Confronto finale.** Contro la base una riga per CIG, la 0.3.4 vale +0,36 mld: R53 e perimetro, meno il difetto della prima riga.

## CIG ripetuti in ict.csv [V]

- Base 0.3.1: 1.016 CIG ripetuti, 1.662 righe in eccesso.
- Varianti A, B, C, D: **0**. Per A la verifica esce con errore se ne trova.

## I 29 CIG G1 nuovi (perimetro 0.3.3) [V]

- **Totale:** 29 CIG dal 2024, per **3,82 mld dichiarati**: sono in S6/G1 in B e fuori dall'imbuto ICT in C. Dal 2020 sono 59 CIG (5,22 mld). Elenco in `g1-nuovi.csv`.
- **Consip SPC/connettività:** 8 CIG, i maggiori. Valgono 1.002, 588, 420, 350, 280, 244, 180 e 175 M€ (CPV 64210000).
- **ASI:** 6 CIG «HW/SW» di missioni spaziali (CPV 73300000), da 129,5 M€ in giù.
- **Altri:** E-Distribuzione 6, Padania Acque 2, Sorical 2, A2A Smart City 1. Sono probabilmente falsi ICT di «connettività» o telecontrollo, da rivedere.
- **Effetto dei tetti:** contano poco sul netto. Il perimetro aggiunge +3,7 mld dichiarati ma solo +0,48 netti, perché i tetti delle convenzioni SPC sono già classificati.
- **Via 6:** questi CIG non sono nella selezione via 6 (presa da ict.csv 0.3.1). Vanno aggiunti alla coda G1 alla rigenerazione.

## Selezione via 6: CIG che cambierebbero strato [V]

Dei 1.196 CIG della selezione via 6 (G1 196 + G3 1.000, `report/metodo/llm/imbuto-g1g3/lotti/`), con la 0.3.4 **cambiano strato 5 CIG** per 27 M€. Tutti passano da S6 a S5. Nessuno esce dall'imbuto e nessuno cambia gruppo dentro S6. Elenco in `via6-cambi.csv`:

| CIG | gruppo via 6 | strato 0.3.4 | importo |
|---|---|---|---|
| B28545AE4A | G1 | S5 hardware-infrastruttura (convenzione LAN 8) | 14,4 M€ |
| B592E9888C | G3 | S5 ict-altro (in-house InfoCamere) | 4,8 M€ |
| B69C602C3F | G3 | S5 ict-altro (centrale unica di risposta) | 4,4 M€ |
| B29D40C0F7 | G3 | S5 consulenza-it-altra (AQ Digital Transformation 2) | 2,0 M€ |
| B85D617A36 | G3 | S5 ict-altro (Cyber Security 2) | 1,4 M€ |

Le risposte via 6 su questi CIG restano valide come verifica, ma alla rigenerazione non contano più nel residuo S6.

## Per il rendiconto (alla rigenerazione, non ora)

- § 2.6: sostituire «circa 55,7 mld (stima)» con **56,06 mld** (S3-S6 dal 2024 al netto dei tetti, imbuto 0.3.4), con la scomposizione degli effetti riportata sopra.
- S6/G1 dal 2024: 227 CIG per 8,53 mld dichiarati (oggi 196 / 4,71 nella selezione).
- I 29 G1 nuovi vanno in coda alla via 6. Prima va fatta la revisione dei falsi ICT delle multiutility.
- Limite: le varianti C e D ricostruiscono il perimetro e la lente del 3/11 sostituendo regex e moduli. D non è identica alla base 0.3.1, per la deduplica della 0.3.2 (−191 CIG, −0,18 mld netti).
