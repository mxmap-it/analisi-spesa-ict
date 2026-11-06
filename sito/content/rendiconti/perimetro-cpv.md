---
title: "Perimetro ICT e attendibilità del CPV"
subtitle: "Lista bianca dei codici CPV misurata sui campioni, falsi esclusi, CPV dichiarato contro classe vera, lacune del vocabolario"
date: 2026-11-06
lastmod: 2026-11-07
datiAl: 2026-11-03
description: "Precisione della lista bianca CPV (83 %, 93 % con i dubbi), falsi esclusi in S1 (1 %), esiti del CPV sugli ICT accertati (74 % specifico, 17 % generico, 9 % fuori lista), cloud esprimibili col CPV (30 %), letteratura verificata (Ramboll 2012: 23 % inesatti), proposte di policy."
sitemap:
  disable: true
build:
  list: never
---

**Versione 0.2 del 2026-11-07 · BOZZA non annunciata: la pubblicazione la decide Fabio Pietrosanti** · ticket [#44](https://github.com/mxmap-it/analisi-spesa-ict/issues/44), [#59](https://github.com/mxmap-it/analisi-spesa-ict/issues/59) · piano `report/cpv/PIANO.md`

Legenda: **[V]** misurato da noi, con il comando per rifarlo; **[R]** riferito da terzi, non verificato.

## 1. Sintesi

- **Lista bianca** (`config/perimetro_cpv.yaml`, 13 prefissi, uguale a `CPV_ICT` di `classifica.py`, controllato dalla verifica) [V]:
  - **precisione** su 200 CIG casuali con CPV in lista dal 2024: **83 %** ICT certi (IC 77-88), **93 %** contando i dubbi (89-96);
  - **79342 «servizi di marketing»** ha 0 contratti ICT su 5. Fa entrare 5.859 CIG e 567 M€ dal 2024: **proposta di toglierlo**;
  - **3224** (telecamere, trasmettitori TV) dà 2 dubbi su 2, per 1.218 CIG e 4,7 mld: **proposta di rivederlo**.
- **Falsi esclusi in S1** (CPV fuori lista e nessun termine ICT nell'oggetto): su 200 CIG casuali dal 2024, **2 ICT certi (1,0 %, IC 0,3-3,6)** e 5 dubbi (3,5 % con i dubbi) [V]. I due casi:
  - manutenzione del software JIride scritta «SW», con CPV 50000000;
  - telefonia fissa e connettività con CPV segnaposto 99999999.

  Entrambi si recuperano aggiungendo a `RX_ICT` «sw» e «connettività» (proposta).
- **Il CPV sugli ICT accertati** (543 ICT del campione 611, via 6 con atti) [V]:
  - **74 % specifico** (70-78);
  - **17 % generico** (codice di gruppo, es. 72000000; 14-20);
  - **9 % fuori dalla lista ICT** (7-12). Di questi 50, 25 hanno il segnaposto 99999999.

  Sui campioni a cieco (159 ICT con prodotto riconosciuto) il fuori lista è all'11 % (7-16).
- **Cloud e CPV:** dei 308 cloud del campione 611, solo il **30 % (25-35)** porta un codice di servizio erogato da terzi (hosting, ASP, storage, Internet, gestione). L'11 % degli ICT non cloud porta gli stessi codici. Il CPV **non distingue il cloud** e **non dice nulla** di prodotto, produttore, sede dei dati e giurisdizione [V].
- **Nella base ANAC dal 2024** (3.734.845 CIG) [V]:
  - 8,3 % ha CPV 99999999 o vuoto;
  - 16,2 % ha un codice di livello gruppo (xxx00000).
- **Letteratura (aperta il 6/11)** [V]:
  - Ramboll/BME 2012 per la Commissione: su **405 avvisi TED il codice era inesatto nel 23 %** (10 % non descrive l'oggetto, 8 % troppo generico, 4 % troppo specifico);
  - Corte dei conti europea SR 28/2023: valori mancanti nel 30 % circa dei contratti TED. **Il 49,8 % che OCP le attribuisce non c'è nel testo**: la cifra non va usata.

## 2. Metodo e campioni

| Campione | Universo | n | Riferimento |
|---|---|---|---|
| L (lista bianca) | `ict.csv` dal 2024, CPV in lista: 254.571 CIG | 200 | etichetta ICT s/n/dubbio data sul solo oggetto senza vedere il CPV (Claude, 6/11) |
| S1 (esclusi) | file CIG 2024-2025 con importo ≥ 500 €, assenti da `ict.csv`: 2.282.585 CIG | 200 | come sopra |
| V3 | campione 611 (`dati/classificazioni/campione-v3.jsonl`) | 611 | via 6 con atti: ICT = servizio diverso da «altro», cloud = `e_cloud` |
| Cieco 1-2 | `report/metodo/lente-cieco{,-2}` | 159 con prodotto | prodotto etichettato = ICT certo |

Comandi (sul server):
- `python tools/verifiche/perimetro_cpv_campiona.py` (S1);
- `python tools/verifiche/perimetro_cpv.py` → `esiti/2026-11-06/cpv/perimetro-cpv.json`.

Limiti:
- le etichette di L e S1 sono di un solo annotatore (l'agente) e leggono solo l'oggetto: servono le annotazioni umane alla cieca già previste;
- «generico» è una regola meccanica sul codice (5 zeri finali);
- il terzo campione a cieco (`lente-cieco-3`) non è ancora versionato e non è incluso.

## 3. Lacune del vocabolario (parte C del piano)

- **Cloud contro on-premise:** nessun codice. 72415 (hosting) e 72416 (ASP) sono del 2008 e coprono il 30 % dei cloud veri; il resto è su 72410 (provider), 72500, 48xxxx (licenze) o 99999999.
- **PSN, hyperscaler e in-house:** indistinguibili. L'operatore e la sua capogruppo non sono un campo.
- **Prodotto, produttore, sede dei dati, giurisdizione, qualificazione ACN:** assenti. È per questo che la lente prodotto legge il testo.
- **Segnaposto 99999999:** accettato da ANAC come «CPV prevalente non disponibile», usato nell'8,3 % dei CIG.

## 4. Proposta di riclassificazione

Ogni CIG ICT già classificato in `dati/classificazioni/` ha la classe spesaict (servizio, modello cloud, giurisdizione del prodotto). La tabella CPV dichiarato → classe spesaict → CPV proposto si genera dal 611 e dal giro della via 6. Prossimo passo: aggiungere a `perimetro_cpv.py` l'uscita `dati/classificazioni/cpv-riclassificazione.csv`.

## 5. Proposte di policy (in `richieste-e-raccomandazioni.yaml`)

- **R21** (aggiornata con questi numeri): controllo di coerenza CPV-oggetto al rilascio del CIG; campi strutturati per gli acquisti ICT.
- **R60** (nuova): non accettare il segnaposto 99999999 al rilascio del CIG.

## 6. Decisioni del 7/11/2026 (Fabio) e loro effetto

Comando: `python tools/verifiche/perimetro_cpv_effetto.py` → `esiti/2026-11-06/cpv/perimetro-effetto.json`. L'effetto è calcolato a parte, senza rigenerare `ict.csv`, perché la via 6 è in corso.

**1. 79342 marketing: tolto, dopo la review** [V]
- Campione di 177 CIG: tutti i 57 sopra 1 M€ e 40 per ciascuno degli altri strati d'importo.
- Sopra 1 M€: 0 ICT (IC 0-6). Sono call center, promozione turistica e acquisto di spazi media.
- Stima sull'universo: 174 ICT veri su 5.859 (3,0 %), tutti sotto 100 k€ (licenza software, sito web). I 3 del campione tornano dentro col testo.
- Effetto: **5.706 CIG e 539 M€ dal 2024 passano in S1**.

**2. 3224 telecamere/TV: review fatta, decisione rinviata** [V]
- Campione di 123 CIG.
- Videosorveglianza, ZTL, lettura targhe: 79 % stimato. ICT stretto (software di videosorveglianza, interoperabilità PNRR): 2,4 %.
- I 4,7 mld del gruppo sono un solo CIG, **B139F77033**: Università di Perugia, «telecamera con accessori», 4.703.401.002 €. È un errore d'importo.
- Proposta: una sottoclasse «videosorveglianza» in S5, fuori dalla misura cloud.

**3. RX_ICT con «sw» e «connettività»: applicato** (imbuto 0.3.3) [V]
- **3.593 CIG** dal 2024 escono da S1 ed entrano nel residuo S6:
  - G4: 2.709;
  - G3: 855 (241 M€);
  - G1: 29 (3,8 mld: lotti SPC Connettività per 3,2 mld, missioni spaziali ASI con «HW/SW», contatori intelligenti).
- Su 40 esempi casuali: 29 ICT, 8 dubbi, 3 non ICT.
- I falsi positivi più grossi stanno in G1, che si rivede a mano.

## Registro delle revisioni

- 0.1 (2026-11-06): prima misura; letteratura ECA e Ramboll aperte e archiviate (sha256 in `report/cpv/letteratura.md`).
- 0.2 (2026-11-07): decisioni di Fabio su 79342, 3224 e RX_ICT, con review stratificata ed effetto misurato.
