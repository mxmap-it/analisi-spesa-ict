---
title: "Perimetro ICT: lista bianca dei CPV"
date: 2026-11-09
description: "La lista bianca dei codici CPV che definisce il perimetro ICT, le esclusioni verificate, le decisioni prese e il loro effetto misurato."
---

**Versione 0.3 del 2026-11-09** · configurazione [`config/perimetro_cpv.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/perimetro_cpv.yaml) · ticket [#44](https://github.com/mxmap-it/analisi-spesa-ict/issues/44) · misure nel rendiconto [Perimetro ICT e attendibilità del CPV](/rendiconti/perimetro-cpv/) (bozza)

Un CIG entra nel perimetro ICT se **almeno uno** dei suoi CPV comincia con un prefisso della lista, oppure se il testo dell'oggetto ha segnali ICT (`RX_ICT` in `tools/analisi/imbuto.py`). Gli altri vanno in S1 (esclusi). La lista è la stessa di `CPV_ICT` in `tools/analisi/classifica.py`: la verifica `tools/verifiche/perimetro_cpv.py` controlla che coincidano.

## Lista bianca (12 prefissi)

| Prefisso | Denominazione (Reg. CE 213/2008) |
|---|---|
| 48 | Pacchetti software e sistemi di informazione |
| 72 | Servizi informatici |
| 302 | Apparecchiature informatiche e forniture |
| 3223 | Apparecchi trasmittenti radio con apparecchi riceventi |
| 3224 | Trasmettitori per televisione (telecamere): sottoclasse videosorveglianza **proposta** |
| 3225 | Telefoni mobili e accessori |
| 3226 | Apparecchiature per la trasmissione di dati e voce |
| 50312 | Manutenzione e riparazione di attrezzature informatiche |
| 50320 | Riparazione e manutenzione di personal computer |
| 51611 | Installazione di computer |
| 64216 | Messaggeria e informazione elettroniche |
| 64222 | Telelavoro |

## Esclusioni verificate

- **79342 marketing**: tolto il 7/11/2026 dopo una review di 177 CIG (3 % ICT veri stimati, nessuno sopra 1 M€).
- **642 telecomunicazioni** (salvo 64216 e 64222), **50000000 e 50800000** manutenzione generica, **99999999** segnaposto ANAC, **30121** fotocopiatrici, **32323500** videosorveglianza, **80500** formazione: fuori lista. Entrano solo per il testo.

## Effetto della versione 0.3.3 dell'imbuto rispetto alla 0.3.2

Base: `ict.csv` dal 2024. Gli importi sono quelli dichiarati, comprese le basi d'asta e i tetti degli accordi quadro: valgono per il confronto, non come spesa.

| Passo | CIG | M€ |
|---|---:|---:|
| 0.3.2, una riga per CPV | 386.911 righe | 505.159 |
| 0.3.2 con R53 (un CIG una volta, imbuto 0.3.4) | 385.249 | 502.470 |
| escono: 79342 senza altri CPV in lista né testo ICT | −5.694 | −538 |
| restano: 79342 con testo ICT / con un altro CPV in lista | 152 / 13 | 28 / 0,6 |
| entrano: nuovo `RX_ICT` («sw», «connettività») | +3.593 | +4.100 |
| **0.3.3 con R53** | **383.148** | **506.031** |

Degli ingressi, 29 CIG valgono 3,8 mld (lotti SPC Connettività, missioni ASI): si rivedono a mano nel gruppo G1. `ict.csv` si rigenera con la 0.3.4 quando la via 6 sarà finita.

Comando: `python tools/verifiche/cpv_rapporto.py` → `esiti/2026-11-09/cpv/rapporto-cpv.json` (B_effetto_perimetro).

## Registro delle revisioni

- 0.1 (2026-11-06): lista di 13 prefissi misurata sui campioni (precisione 83 %, 93 % con i dubbi; falsi esclusi 1 %).
- 0.2 (2026-11-07): 79342 fuori; `RX_ICT` con «sw» e «connettività» (decisione di Fabio); 3224 rinviato.
- 0.3 (2026-11-09): effetto 0.3.3 contro 0.3.2 con R53; proposta di sottoclasse videosorveglianza per 3224 (in attesa di decisione); lacune del vocabolario e raccomandazioni nel yaml.
