# Tabella unica degli spostamenti — 2026-11-19

Strumento `tools/verifiche/imbuto_spostamenti.py` 0.1. Spostamenti proposti 14.286, CIG toccati 14.040 (fuori dall'imbuto: 0).

Lo strato S1 (non ICT per CPV e testo) non è in `ict.csv` e non è contato qui: «escluso certo, non ICT» conta solo i CIG che i livelli tolgono dall'ICT.

## Asse A dal 2024, prima e dopo i livelli

| stato | CIG prima | CIG dopo | mld lordi prima | mld lordi dopo | mld netti tetti prima | mld netti tetti dopo |
|---|---:|---:|---:|---:|---:|---:|
| fuori misura (S0 padre AQ, S2 sotto soglia) | 94.061 | 94.062 | 391,70 | 391,70 | 391,70 | 391,70 |
| escluso certo, non ICT | 0 | 1.579 | 0,00 | 0,19 | 0,00 | 0,19 |
| ICT non cloud | 220.525 | 231.132 | 90,76 | 93,13 | 40,01 | 41,90 |
| incluso certo: cloud | 4.556 | 5.035 | 1,21 | 1,42 | 1,09 | 1,29 |
| incluso certo: infrastruttura in-house | 816 | 438 | 0,66 | 0,08 | 0,42 | 0,08 |
| incerto: marchio o lotto noto, da attribuire | 3.889 | 2.039 | 5,37 | 4,10 | 2,85 | 1,80 |
| incerto: residuo S6 | 59.406 | 48.968 | 16,37 | 15,09 | 11,70 | 10,67 |

## Flussi netti dal 2024 (livello decisivo)

| da | a | livello | CIG | M€ netti tetti |
|---|---|---|---:|---:|
| ict-non-cloud | escluso-non-ict | B1 | 417 | 20,0 |
| incerto-marchio | cloud-certo | LIC | 304 | 159,9 |
| incerto-marchio | ict-non-cloud | LIC | 1758 | 968,0 |
| incerto-s6 | cloud-certo | L4 | 2 | 1,6 |
| incerto-s6 | cloud-certo | V6R | 9 | 27,2 |
| incerto-s6 | escluso-non-ict | B1 | 863 | 111,4 |
| incerto-s6 | escluso-non-ict | L3 | 297 | 53,3 |
| incerto-s6 | escluso-non-ict | L4 | 2 | 7,3 |
| incerto-s6 | ict-non-cloud | L2 | 6913 | 466,3 |
| incerto-s6 | ict-non-cloud | L3 | 2259 | 112,4 |
| incerto-s6 | ict-non-cloud | L4 | 71 | 92,9 |
| incerto-s6 | ict-non-cloud | V6R | 22 | 152,5 |
| inhouse-certo | cloud-certo | MAN | 164 | 13,3 |
| inhouse-certo | fuori-misura | MAN | 1 | 0,0 |
| inhouse-certo | ict-non-cloud | MAN | 1 | 117,3 |
| inhouse-certo | incerto-marchio | B2 | 212 | 84,6 |

## Giurisdizione degli inclusi certi dal 2024 (netti tetti)

| stato | giurisdizione | M€ prima | M€ dopo |
|---|---|---:|---:|
| cloud-certo | EXTRA-UE | 828,4 | 964,4 |
| cloud-certo | IT | 67,2 | 83,0 |
| cloud-certo | UE | 190,9 | 239,5 |
| cloud-certo | non determinata | 0,0 | 1,6 |
| inhouse-certo | IT | 415,8 | 77,6 |

## Disaccordi fra livelli

- dal-2024: B1:escluso-non-ict vs L2:ict-non-cloud — 67 CIG
- dal-2024: B1:escluso-non-ict vs L3:ict-non-cloud — 1 CIG
- dal-2024: B1:escluso-non-ict vs L4:ict-non-cloud — 1 CIG
- dal-2024: B2:incerto-marchio vs MAN:cloud-certo — 164 CIG
- dal-2024: B2:incerto-marchio vs MAN:fuori-misura — 1 CIG
- dal-2024: B2:incerto-marchio vs MAN:ict-non-cloud — 1 CIG
