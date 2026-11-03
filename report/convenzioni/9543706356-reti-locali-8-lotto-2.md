# Convenzione Reti locali 8 — ID 2223, lotto 2 PAL (CIG 9543706356) — dossier analitico

Versione 0.1 — 2026-11-03 — #55. Bozza per revisione avversariale.
Legenda: **V** verificato su documento archiviato; **V2** due fonti indipendenti di cui una della stazione appaltante; **R** riferito / da verificare.
Numeri degli attuativi: `tools/verifiche/attuativi_s5.py` (sul server, esito in `lavoro/convenzioni/attuativi_s5.json`).

## 1. Sintesi

- Convenzione (art. 26 L. 488/1999) per **cablaggio, switch, SD-WAN, wireless, UPS, sistema di management** e servizi di installazione/gestione on-site: hardware di rete installato presso l'ente. CIG confermato da Consip (esito gara), TED e BDNCP: passa da «da verificare» a **verificato** (V2).
- Aggiudicatario lotto 2: RTI **Vodafone Italia** (mandataria), Converge, Studio Ing. Umberto Lisa; valore di aggiudicazione 145.154.513,82 €, portato a 174.185.416,58 € con il «sesto quinto» (TED modifica 2024).
- Cloud: solo clausola generale (qualificazione ACN per servizi «erogati in modalità cloud» offerti come minimo o miglioria); il management può essere «con o senza piattaforma hardware». Nessun servizio cloud a listino nel capitolato. Asse cloud: **escluso** (confidenza alta).
- Produttori: gara **multibrand** (5 marchi di switch, 3 di SD-WAN, scelti in offerta, non letti). Negli oggetti degli attuativi: Cisco (29), HPE Aruba (14), Juniper (5), Huawei (2), Fortinet, Extreme — tutti extra-UE (USA; Huawei CN) (R).
- BDNCP: 817 attuativi, importi pesantemente gonfiati (somma lorda 9,9 × il valore): al netto degli anomali 475,4 M€, ancora 2,7 × il valore aggiornato → dato BDNCP **non utilizzabile** come spesa senza correzione.

## 2. Identificazione

| Campo | Valore | Fonte | Livello |
|---|---|---|---|
| CIG | lotto 1 PAC 95436927C7; **lotto 2 PAL 9543706356** | Esito gara Consip; TED 60365-2023, 787004-2023; BDNCP | V2 |
| Gara | procedura aperta d.lgs. 50/2016, ID Sigef 2223, Reti locali ed. 8 | pagina Consip gara-reti-locali-8; esito | V2 |
| Date | indizione 25/01/2023; GUUE S-21 30/01/2023; stipula 14/11/2023 | pagina Consip; esito | V2 |
| Valore | stimato 217 M€; aggiudicato 145.154.513,82 €; dopo modifica 174.185.416,58 € (sesto quinto, PNRR M6C2) | esito Consip; TED 671042-2024; BDNCP (217 M€) | V2 |
| Aggiudicatario | RTI Vodafone Italia – Converge – Studio Tecnico Ing. Umberto Lisa | esito Consip; BDNCP | V2 |
| Durata | 548 giorni (BDNCP); nulla osta subentro Fastweb 2026 sulla pagina Consip | BDNCP; pagina Consip | R |

## 3. Cosa contiene (Capitolato tecnico)

- Forniture: cablaggio strutturato, apparati attivi (switch tipi 1-9, SD-WAN, wireless), UPS, «sistema centralizzato di management (con o senza piattaforma hardware)». **V**
- Servizi connessi: progettazione, installazione e configurazione, collaudo, help desk, dismissione; a richiesta: manutenzione, opere civili, **gestione on-site della rete**. **V**
- §2.1.2: per i servizi «erogati in modalità cloud», minimi o migliorativi, si applicano le norme di qualificazione AgID/ACN. **V** — clausola condizionale, nessun servizio cloud specifico a listino.
- Multibrand: 5 brand di switch e 3 di SD-WAN (CT §2.3). **V**; quali brand: nell'offerta, non letta. **R**

## 4. Analisi degli attuativi (BDNCP)

| Misura | Valore |
|---|---|
| attuativi | 817 (2023: 21; 2024: 785; 2025: 11) |
| anomali (≥ 54 M€) | 9 righe, 1.680 M€ (Bari Uniba 380 M€, ASL BA 343 e 115 M€, ASL Frosinone 243 M€, 3 righe = valore del lotto 145,15 M€…) |
| euro puliti | 475.444.504 (2,19 × 217 M€; 2,73 × 174 M€) |
| mediana / p90 | 54.926 € / 967.963 € |
| possibili doppioni | 64 / 22,5 M€ |
| sotto 500 € | 23 |
| oggetti fuori tema | telefonia mobile «Convenzione Consip TM9» (CIG agganciati al master sbagliato) |
| data center in oggetto | 7 / 9,4 M€ (switch per DC regionali: Marche, Campania, ATAC) → infrastruttura in-house |
| marchi in oggetto | Cisco 29, Aruba 14, Juniper 5, Huawei 2, Fortinet 1, Extreme 1 |

## 5. Classificazione proposta

- Categoria hardware di rete; **S5 – infrastruttura in-house (rete locale)**; confidenza alta. Il valore in YAML «connettivita» andrebbe distinto da SPC2: è hardware, non servizio TLC.
- Asse cloud: escluso certo (nessun servizio cloud a listino; eventuali controller cloud dei vendor sarebbero miglioria non quantificabile).
- Produttori e giurisdizione (lente prodotto): Cisco, HPE Aruba, Juniper (HPE dal 2025), Extreme, Fortinet → **USA**; Huawei → **CN**. Fonte: oggetti degli attuativi (R); da confermare con l'offerta tecnica o le Convenzioni firmate (listino per brand).

## 6. Assunzioni e limiti

- BDNCP sovrastima in modo grossolano: molte SA scrivono il valore del lotto o importi non coerenti. Per la spesa servono le Convenzioni/ordinativi o i dati Consip sugli ordinato (la pagina Consip pubblica «Dati ordinato RL7», non RL8).
- I marchi negli oggetti sono un campione (circa 50 su 817).

## 7. Fonti

| URL | sha256 | Cosa conferma | Tipo |
|---|---|---|---|
| https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID%202223%20-%20RL8%20-%20Esito%20gara%20v2.pdf | 83396a8f20438fe5bdd4b5bd11b47ec1e2a1168050c9b934c027043de522051f | CIG lotti, RTI Vodafone, valori | stazione appaltante |
| https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID2223%20-%20DOC%20NON%20UFF.zip | e33413b8b82cf6d74b9638cec3d3f2806a2a314caefbc6e352aa88445a36279a | Capitolato tecnico (file interno 2c627861dddf22909a92f9d92ef6a6997f9acef2a815c75ed7d5067e83646a83): oggetto, clausola cloud, multibrand | stazione appaltante |
| https://www.consip.it/bandi/gara-reti-locali-8 | 8e8637f3ea47f1a2b1c24ed043b77dbb589da113c36b11b48c2de0f3aba0fbdd | cronologia, documenti | stazione appaltante |
| https://ted.europa.eu/it/notice/60365-2023/xml | c2e4a06e81d36b5f473fd2e4e17c3fa598f99d282ba76d3341649d982206b901 | bando | stazione appaltante (TED) |
| https://ted.europa.eu/it/notice/787004-2023/xml | 3d5781209eccbca28d8ebdcbd136ddd1c897e0342c0ab0ebf379536c805a292c | aggiudicazione | stazione appaltante (TED) |
| https://ted.europa.eu/it/notice/671042-2024/xml | ff1b5dfcff732855e9681aec6830b7abdbd8c3f7d928ae3ffdcb32a28043eff5 | modifica: 145,15 → 174,19 M€ | stazione appaltante (TED) |
| BDNCP ANAC nel mirror | per file in `archivio/manifest.jsonl` | attuativi, marchi negli oggetti | ANAC (dato della SA) |

## Proposta per iniziative_ict.yaml

```yaml
- cig: 9543706356
  iniziativa: Consip Reti locali 8, ID 2223, lotto 2 PAL
  categoria: hardware-rete        # oggi 'connettivita': è fornitura di apparati e cablaggi, non servizio TLC
  stato: verificato               # esito Consip + TED + BDNCP
  sottoclasse_s5: infrastruttura-rete-locale
  asse_cloud: escluso-certo
  produttori: [Cisco, HPE Aruba, Juniper, Huawei, Fortinet, Extreme]   # R: dagli oggetti degli attuativi
  giurisdizione_prodotto: EXTRA-UE  # USA; Huawei CN
  valore_aggiudicato: 145154513.82
  valore_dopo_modifica: 174185416.58
  dossier: report/convenzioni/9543706356-reti-locali-8-lotto-2.md
  documenti:
  - url: https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID%202223%20-%20RL8%20-%20Esito%20gara%20v2.pdf
    sha256: 83396a8f20438fe5bdd4b5bd11b47ec1e2a1168050c9b934c027043de522051f
    cosa_conferma: esito Consip con CIG lotto 2 9543706356 e RTI Vodafone
  - url: https://ted.europa.eu/it/notice/787004-2023/xml
    sha256: 3d5781209eccbca28d8ebdcbd136ddd1c897e0342c0ab0ebf379536c805a292c
    cosa_conferma: aggiudicazione TED ID 2223
```
