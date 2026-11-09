# Scheda decisionale: CPV 3224 e sottoclasse «videosorveglianza» (#44)

**Per Fabio, 9/11/2026.** Decisione richiesta: cosa fare dei CIG con CPV 3224 («trasmettitori per televisione», in pratica telecamere). Prove: `tools/verifiche/cpv_rapporto.py` → `esiti/2026-11-09/cpv/rapporto-cpv.json` (C_videosorveglianza_3224); review del 7/11 in `report/cpv/review-79342-3224/`.

## Numeri (ict.csv dal 2024, un CIG una volta)

| Classe (regola sul testo) | CIG | M€ | M€ senza B139F77033 |
|---|---:|---:|---:|
| videosorveglianza (telecamere, ZTL, targhe, fototrappole, TVCC) | 996 | 4.739,3 | 35,9 |
| altro (camere televisive e scientifiche, controllo traffico, sensori) | 208 | 6,2 | 6,2 |
| ICT stretto (software, HW/SW) | 14 | 0,3 | 0,3 |
| **totale** | **1.218** | **4.745,8** | **42,4** |

- I 4,7 mld sono **un solo CIG con importo errato**: B139F77033, Università di Perugia, «telecamera con accessori», 4.703.401.002 €.
- 981 dei 996 sono già in S5 (ICT non cloud): **la misura cloud non cambia** in nessuna opzione.
- Enti: comuni 571, società partecipate 192 (autostrade, trasporti), università e ricerca 54, Stato 44.
- La regola sul testo, controllata sulle 123 etichette della review del 7/11: precisione 89 % (92 su 103), richiamo 91 % (92 su 101).

Esempi fra i più grandi:
- Comune di Arona, ampliamento della videosorveglianza, 1,94 M€ (B4460262FE);
- Comune di Montecchio Precalcino, videosorveglianza contro l'abbandono dei rifiuti, 1,41 M€ (B42B6169EC);
- Carabinieri, adesione alla convenzione Consip con 224 telecamere, 112 videoregistratori e 56 server, 0,82 M€ (B6B906E97C);
- ANM Napoli, nuovi impianti di videosorveglianza, 0,80 M€ (BAA0509071).

## Opzioni

| | Cosa | Effetto | Pro | Contro |
|---|---|---|---|---|
| **A (proposta)** | 3224 resta in lista; sottoclasse «videosorveglianza» in S5, fuori dalla misura cloud | nessun CIG cambia strato; i 996 ricevono l'etichetta | non si perde nulla; la videosorveglianza con archiviazione in cloud resta tracciabile | una regola in più |
| B | 3224 fuori lista, come 79342 | circa 1.200 CIG e 42 M€ passano in S1; i 14 ICT stretti rientrano per il testo | perimetro più pulito | si perde la videosorveglianza in cloud (video archiviati presso terzi), che è un tema di sovranità |
| C | lasciare tutto com'è | nessuno | nessun lavoro | S5 gonfiato da impianti di sicurezza fisica |

In tutte le opzioni va **corretto l'importo di B139F77033**, togliendolo dai totali e annotandolo fra gli errori d'importo.

**Raccomandazione: A.** Dopo la decisione: sottoclasse in `tools/analisi/imbuto.py` alla rigenerazione di `ict.csv` (dopo la via 6) e stato aggiornato in `config/perimetro_cpv.yaml` (`sottoclassi_proposte`).
