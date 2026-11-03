# Approfondimento: PSN per servizio ed Enterprise Agreement Microsoft (3/11/2026, #55)

Misure **V** sul file di lavoro dell'imbuto 0.3 (`lavoro/imbuto/ict.csv`, contratti 2024-2025, esclusi gli importi ≥ 50 M «da verificare»). Criteri: [criteri-sovranita](../../sito/content/progetto/criteri-sovranita.md).

## 1. PSN: si può applicare la regola per servizio?

**No, non dai dati ANAC.** 692 contratti, 1.918 M€. Classificando l'oggetto:

| l'oggetto dice | contratti | M€ |
|---|---|---|
| solo «adesione PSN / contratto di utenza» | 492 | 1.332 |
| migrazione o servizi professionali | 163 | 566 |
| Industry Standard (housing, hosting, IaaS, backup…) | 26 | 16 |
| un hyperscaler (Azure, Google, AWS, Oracle, «Secure Public Cloud», hybrid) | 11 | 5 |

Il servizio comprato è scritto nell'oggetto per l'1 % del valore. La regola per servizio non può essere applicata dall'imbuto: servono i **progetti dei piani dei fabbisogni** (codici `…-PPDF-PnRn`, citati nell'oggetto di 70 contratti).

**Concentrazione** (dove conviene cercare gli atti): i primi 30 contratti fanno il 45 % del valore, i primi 100 il 75 %, i primi 200 il 90 %.

**Correzione necessaria (difetto):** l'imbuto oggi scrive giurisdizione «IT» su 1.575 M€ di PSN indeterminato, perché il classificatore attribuisce la giurisdizione dell'operatore PSN. È fuorviante: va scritto «incerto (servizio non noto)», finché il servizio non è accertato.

### Azioni proposte (in ordine di costo)
1. **Correggere l'etichetta** (codice, subito).
2. **Atti dei primi 30-100 contratti PSN** (livelli L1-L3 di acquisizione: amministrazione trasparente degli enti, determine con allegato il progetto del piano dei fabbisogni). Per ogni contratto: servizi e importi per famiglia (Industry Standard, Secure Public Cloud per hyperscaler, PSN Managed, Hybrid, migrazione). Copre il 45-75 % del valore.
3. **Ripartizione aggregata** come forbice di riserva: bilancio PSN 2026 (Fabio, 3/11), richiesta R26 a DTD.
4. I servizi di **migrazione** (566 M€) sono servizi professionali: la loro sovranità segue l'infrastruttura di destinazione (R-S1), quindi restano legati al punto 2.

## 2. Microsoft Enterprise Agreement: quanto è cloud?

Licenze Microsoft 2024-2025 (S3 convenzione + S4 marchio), classificate dall'oggetto:

| oggetto | S3 (EA) M€ | S4 M€ |
|---|---|---|
| generico («licenze Microsoft», «adesione EA») | 273,1 | 158,5 |
| SaaS esplicito (M365, O365, Dynamics, Copilot…) | 86,7 | 0,7 |
| on-premise esplicito (Windows/SQL Server, CAL, Software Assurance, rinnovi) | 83,2 | 8,6 |
| Azure | ~0 | 0,2 |
| **totale** | **~443** | **~168** |

Dove l'oggetto è esplicito, **SaaS e on-premise si dividono circa a metà** (87 contro 92 M€). È coerente con i pesi di gara Consip (44 % «Microsoft 365» in EA6, 50 % in EA9). Gli ordini con dettaglio SKU letti (Calabria, ART, MAECI, Archivi notarili) sono in prevalenza M365/Dynamics, ma sono un campione piccolo.

> **Superato** da `ea-quota-cloud-elaborazione.md`: i pesi di gara non sono una stima centrale (revisione avversariale), e «rinnovo»/«manutenzione» non indicano on-premise.

### Regola proposta (decisione Fabio, superata)
- **Cloud extra-UE certo:** solo il SaaS esplicito (~87 M€).
- **On-premise certo:** solo l'on-premise esplicito (~92 M€): licenze, non cloud.
- **Generico (~430 M€): intervallo.** Valore centrale 44-50 % cloud (pesi di gara); estremi 0 % e 100 %, nella forbice dell'incerto.
- Avvertenza (dossier EA6/EA9): M365 E3 include il diritto di installare Office in locale, e il MAECI contabilizza le licenze come software installato. «SaaS» significa abbonamento a servizio erogato da Microsoft (R-S5).

### Azioni per restringere l'intervallo
1. Transato per famiglia di prodotto da Consip (raccomandazione R23).
2. Campione di ordini con dettaglio SKU fra gli aderenti EA8/EA9 (determine in amministrazione trasparente), stratificato per importo.

## 3. Effetto atteso sulla forbice
Le due regole spostano dall'incerto al certo poco valore: ~87 M€ di SaaS Microsoft e ~5 M€ di PSN su hyperscaler. La forbice del 12-96 % si stringe davvero solo con gli atti dei contratti PSN (azione 1.2) e con il transato EA (R23).
