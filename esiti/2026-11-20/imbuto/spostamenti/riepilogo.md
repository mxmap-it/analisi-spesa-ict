# Tabella unica degli spostamenti — 2026-11-20

Strumento `tools/verifiche/imbuto_spostamenti.py` 0.2.0. Spostamenti proposti 14.421, CIG toccati 14.172 (fuori dall'imbuto: 0).

Lo strato S1 (non ICT per CPV e testo) non è in `ict.csv` e non è contato qui: «escluso certo, non ICT» conta solo i CIG che i livelli tolgono dall'ICT.

## Asse A dal 2024, prima e dopo i livelli

| stato | CIG prima | CIG dopo | mld lordi prima | mld lordi dopo | mld netti tetti prima | mld netti tetti dopo |
|---|---:|---:|---:|---:|---:|---:|
| fuori misura (S0 padre AQ, S2 sotto soglia) | 94.061 | 94.062 | 391,70 | 391,70 | 391,70 | 391,70 |
| escluso certo, non ICT | 0 | 1.591 | 0,00 | 0,19 | 0,00 | 0,19 |
| ICT non cloud | 220.525 | 224.526 | 90,76 | 91,51 | 40,01 | 40,42 |
| incluso certo: cloud | 4.556 | 5.036 | 1,21 | 1,42 | 1,09 | 1,29 |
| incluso certo: infrastruttura in-house | 816 | 711 | 0,66 | 0,14 | 0,42 | 0,14 |
| incluso certo: cloud in proprio (datacenter dell'ente) | 0 | 7.851 | 0,00 | 2,09 | 0,00 | 1,94 |
| incerto: marchio o lotto noto, da attribuire | 3.889 | 1.765 | 5,37 | 3,95 | 2,85 | 1,66 |
| incerto: residuo S6 | 59.406 | 47.711 | 16,37 | 14,71 | 11,70 | 10,29 |

## Flussi netti dal 2024 (livello decisivo)

| da | a | livello | CIG | M€ netti tetti |
|---|---|---|---:|---:|
| ict-non-cloud | dc-proprio | DC | 5941 | 1.006,0 |
| ict-non-cloud | escluso-non-ict | B1 | 417 | 20,0 |
| ict-non-cloud | inhouse-certo | DC | 91 | 14,3 |
| incerto-marchio | cloud-certo | LIC | 304 | 159,9 |
| incerto-marchio | dc-proprio | DC | 740 | 410,5 |
| incerto-marchio | ict-non-cloud | LIC | 1083 | 617,6 |
| incerto-marchio | inhouse-certo | DC | 33 | 13,2 |
| incerto-s6 | cloud-certo | L4 | 3 | 1,6 |
| incerto-s6 | cloud-certo | V6R | 9 | 27,2 |
| incerto-s6 | dc-proprio | DC | 1117 | 361,9 |
| incerto-s6 | escluso-non-ict | B1 | 853 | 110,0 |
| incerto-s6 | escluso-non-ict | L3 | 297 | 53,3 |
| incerto-s6 | escluso-non-ict | L4 | 24 | 8,9 |
| incerto-s6 | ict-non-cloud | L2 | 6895 | 466,0 |
| incerto-s6 | ict-non-cloud | L3 | 2255 | 112,2 |
| incerto-s6 | ict-non-cloud | L4 | 195 | 102,3 |
| incerto-s6 | ict-non-cloud | V6R | 22 | 152,5 |
| incerto-s6 | inhouse-certo | DC | 25 | 1,3 |
| inhouse-certo | cloud-certo | MAN | 164 | 13,3 |
| inhouse-certo | dc-proprio | DC | 52 | 42,6 |
| inhouse-certo | dc-proprio | MAN | 1 | 117,3 |
| inhouse-certo | fuori-misura | MAN | 1 | 0,0 |
| inhouse-certo | incerto-marchio | B2 | 36 | 10,2 |

## Giurisdizione degli inclusi certi dal 2024 (netti tetti)

| stato | giurisdizione | M€ prima | M€ dopo |
|---|---|---:|---:|
| cloud-certo | EXTRA-UE | 828,4 | 964,4 |
| cloud-certo | IT | 67,2 | 83,0 |
| cloud-certo | UE | 190,9 | 239,5 |
| cloud-certo | non determinata | 0,0 | 1,6 |
| dc-proprio | IT | 0,0 | 1.938,3 |
| inhouse-certo | IT | 415,8 | 138,2 |

## Cloud in proprio dal 2024: datacenter dell'ente per famiglia (netti tetti)

| famiglia | CIG | M€ lordi | M€ netti tetti |
|---|---:|---:|---:|
| backup | 165 | 16,4 | 16,4 |
| calcolo-scientifico | 638 | 315,9 | 315,9 |
| server-storage | 4.133 | 643,3 | 643,3 |
| servizio-inhouse | 273 | 60,6 | 60,6 |
| sito | 1.950 | 569,3 | 499,3 |
| virtualizzazione | 965 | 542,1 | 463,5 |

## Disaccordi fra livelli

- dal-2024: B1:escluso-non-ict vs L2:ict-non-cloud — 67 CIG
- dal-2024: B1:escluso-non-ict vs L3:ict-non-cloud — 1 CIG
- dal-2024: B1:escluso-non-ict vs L4:ict-non-cloud — 3 CIG
- dal-2024: B2:incerto-marchio vs MAN:cloud-certo — 164 CIG
- dal-2024: B2:incerto-marchio vs MAN:dc-proprio — 1 CIG
- dal-2024: B2:incerto-marchio vs MAN:fuori-misura — 1 CIG
