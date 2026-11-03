# Convenzione PC desktop, workstation e monitor ed. 3 — ID 2631, lotto 2 (CIG 9823936871) — dossier analitico

Versione 0.1 — 2026-11-03 — #55. Bozza per revisione avversariale.
Legenda: **V** verificato su documento archiviato; **V2** due fonti indipendenti di cui una della stazione appaltante; **R** riferito / da verificare.
Numeri degli attuativi: `tools/verifiche/attuativi_s5.py` (sul server, esito in `lavoro/convenzioni/attuativi_s5.json`).

## 1. Sintesi

- Convenzione Consip in 6 lotti; il lotto 2 è **PC desktop small form factor**, aggiudicato a **Italware S.r.l.**, valore 89.045.000 € (Convenzione firmata, avviso di aggiudicazione Consip, TED, BDNCP: **V2**; passa a verificato).
- Sistema operativo obbligatorio **Microsoft Windows 11 Professional** preinstallato dal produttore, con alternativa Linux su richiesta per i lotti 1-3 (Capitolato tecnico, V): ogni PC porta con sé una licenza Microsoft (USA), on-premise, non cloud.
- Produttore del lotto 2: dagli oggetti degli attuativi **Lenovo** (37 menzioni, gruppo con sede a Hong Kong, Cina) (R); la Convenzione non nomina il marchio nelle parti lette.
- BDNCP: 498 attuativi, 449 M€ lordi di cui 401,5 M€ in 4 righe anomale; al netto **47,5 M€** (0,53 del valore). 243 attuativi con aggiudicatario «IMPRESA INESISTENTE».
- Proposta: **S5 hardware in-house**, asse cloud escluso certo; giurisdizione prodotto extra-UE (hardware Lenovo, SO Microsoft).

## 2. Identificazione

| Campo | Valore | Fonte | Livello |
|---|---|---|---|
| CIG | lotti 1-6: 9823924E88, **9823936871**, 9823953679, 9823965062, 9824002EE6, 9824017B48 | avviso di aggiudicazione Consip; Convenzione lotto 2 («LOTTO 2 CIG 9823936871»); TED 322210-2023; BDNCP | V2 |
| Gara | procedura aperta d.lgs. 50/2016, 6 lotti, ID Sigef 2631 | pagina Consip gara-pc-desktop-e-workstation-ed-3; TED | V2 |
| Date | GUUE S-102 30/05/2023; GURI n. 63 05/06/2023; aggiudicazione 17/10/2023; contratto 21/12/2023; esito GUUE S 11 16/01/2024 | pagina Consip; avviso di aggiudicazione | V2 |
| Valore lotto 2 | 89.045.000 € (totale gara 243.067.500 €) | avviso di aggiudicazione; TED; BDNCP | V2 |
| Aggiudicatario | Italware S.r.l. (Roma) | Convenzione lotto 2; BDNCP | V2 |
| Durata | 365 giorni (BDNCP); lettera di proroga per il lotto 6 (non letta per il lotto 2) | BDNCP; pagina Consip | R |

## 3. Cosa contiene

- Fornitura in acquisto di PC desktop SFF con servizi connessi (consegna, installazione, assistenza) e opzioni. **V**
- SO: Windows 11 Professional 64 bit «nuovo di fabbrica … installato dal produttore»; Linux in alternativa per i lotti 1, 2, 3 se richiesto (CT §5.1). TPM 2.0, requisiti ambientali (EPEAT/TCO). **V**
- Nessun servizio cloud nel capitolato (ricerca testuale «cloud»: nessuna occorrenza nei requisiti). **V**

## 4. Analisi degli attuativi (BDNCP)

| Misura | Valore |
|---|---|
| attuativi | 498 (2024: 473; 2025: 25) |
| anomali | 4 / 401,5 M€: ANBSC 243,1 M€ (= totale gara), ASL Roma G e ANBSC 52,8 M€ (3 righe) |
| euro puliti | 47.546.026 (2024 46,6 M€; 2025 1,0 M€) |
| mediana / p90 | 11.597 € / 138.910 € |
| doppioni | 21 / 4,5 M€ |
| sotto 500 € | 8 |
| maggiori | Carabinieri 1,99 M€ (3.292 PC) e 1,63 M€ (4.417 PC); Guardia di Finanza 1,72 M€ (3.474 PC) |
| marchi in oggetto | Lenovo 37; Windows 8, Linux 4 |
| aggiudicatario «IMPRESA INESISTENTE» | 243 su 494 |

## 5. Classificazione proposta

- Categoria hardware; **S5 – postazioni di lavoro in-house**; confidenza alta.
- Asse cloud: escluso certo.
- Giurisdizione (lente prodotto): hardware **Lenovo** (HK/CN, R), SO **Microsoft** (USA, V da capitolato salvo opzione Linux) → extra-UE.

## 6. Assunzioni e limiti

- Il marchio del lotto 2 viene dagli oggetti degli attuativi (37 su 494), non dalla Convenzione: da confermare con la guida alla Convenzione o il listino.
- La somma BDNCP richiede pulizia: con le regole adottate resta 0,53 del valore, plausibile.
- La quota delle licenze Windows non è separabile dal prezzo del PC.

## 7. Fonti

| URL | sha256 | Cosa conferma | Tipo |
|---|---|---|---|
| https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID2631_PCDWM%203%20-%20Lotto%202%20-%20Convenzione.pdf | aeebf9e8c139aa97e94d9b097f825be4af5f280845bc4847e3f342dec738309f | CIG lotto 2, Italware | stazione appaltante |
| https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID%202631%20-%20PC%20Desktop%20Workstation%20e%20Monitor%20ed%203%20-%20Avviso%20di%20aggiudicazione.pdf | 9e028ac403e5caaa0b9e35708d5528ad51c2e97829ca92aa659610e739ca8e6b | CIG dei 6 lotti, valori, denominazioni | stazione appaltante |
| https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID%202631%20-%20DOC%20NON%20UFF.zip | 1b2d2223d9b56177158e580804e62fe8454b9f2e5cc8808013acaef159fc0786 | Capitolato tecnico (file interno 218f6927b5130af60803f41301d03838d909a9b16e150382fe21a01911c37ea3): Windows 11 Pro / Linux | stazione appaltante |
| https://www.consip.it/bandi/gara-pc-desktop-e-workstation-ed-3 | 54b09ef453757ce2ea2169c060365b7e00bbc51f49830e86ea6054fe836dd039 | cronologia | stazione appaltante |
| https://ted.europa.eu/it/notice/322210-2023/xml | c436c95b10444d6197b33d3f89b354a68b4453201ddf812218a75b571bd8aa05 | bando | stazione appaltante (TED) |
| https://ted.europa.eu/it/notice/28396-2024/xml | dc37c2e37b66e285fd04098c98fd062e551c91b11dae69b5bf7d228a89d712f9 | aggiudicazione | stazione appaltante (TED) |
| BDNCP ANAC nel mirror | per file in `archivio/manifest.jsonl` | attuativi, marchi | ANAC (dato della SA) |

## Proposta per iniziative_ict.yaml

```yaml
- cig: 9823936871
  iniziativa: Consip PC desktop e workstation 3, ID 2631, lotto 2 PC desktop small form factor
  categoria: hardware
  stato: verificato               # Convenzione e avviso Consip + TED + BDNCP
  sottoclasse_s5: postazioni-di-lavoro
  asse_cloud: escluso-certo
  aggiudicatario: Italware S.r.l.
  produttori: [Lenovo, Microsoft]  # Lenovo R (oggetti attuativi); Windows 11 Pro V (capitolato)
  giurisdizione_prodotto: EXTRA-UE
  dossier: report/convenzioni/9823936871-pc-desktop-workstation-3.md
  documenti:
  - url: https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID2631_PCDWM%203%20-%20Lotto%202%20-%20Convenzione.pdf
    sha256: aeebf9e8c139aa97e94d9b097f825be4af5f280845bc4847e3f342dec738309f
    cosa_conferma: Convenzione lotto 2, CIG 9823936871, Italware
  - url: https://ted.europa.eu/it/notice/28396-2024/xml
    sha256: dc37c2e37b66e285fd04098c98fd062e551c91b11dae69b5bf7d228a89d712f9
    cosa_conferma: aggiudicazione TED ID 2631
```
