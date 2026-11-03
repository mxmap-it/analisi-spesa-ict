# AQ Servizi di sicurezza da remoto, compliance e controllo — ID 2296 (CIG 88846293CA, 8884642E81) — dossier analitico

Versione 0.1 — 2026-11-03 — #55. Bozza per revisione avversariale.
Legenda: **V** verificato su documento archiviato; **V2** due fonti indipendenti di cui una della stazione appaltante; **R** riferito / da verificare.
Numeri degli attuativi: `tools/verifiche/attuativi_s5.py` (sul server, esito in `lavoro/convenzioni/attuativi_s5.json`).

## 1. Sintesi

- **Lotto 1 (88846293CA) non è sicurezza in-house**: è un catalogo di servizi di sicurezza **erogati dai Centri Servizi del fornitore** (SOC, NGFW, WAF, protezione navigazione/posta, endpoint, IAM, firma remota, sigillo, marca temporale), a canone, con migrazione dei servizi «on premise» dell'ente verso quelli in fornitura. È di fatto **security-as-a-service**: per il nostro asse cloud va trattato come cloud esterno (incluso certo come modello di erogazione), con giurisdizione dei centri servizi **UE obbligatoria** e **IT** nell'offerta del RTI Accenture-Fastweb (DC Fastweb Milano e Roma) (V).
- Tecnologie del RTI Accenture-Fastweb: Fortinet (NGFW, WAF, SWG), Splunk (SIEM), Palo Alto Cortex XSOAR, Tenable/Qualys, Trend Micro Apex One — produttori USA e Giappone (V, offerta tecnica allegata all'AQ).
- **Lotto 2 (8884642E81)**: servizi professionali di compliance e controllo (VA/PT, security strategy, audit): consulenza IT di sicurezza, **S5**, nessun cloud.
- BDNCP: L1 306 attuativi puliti, 492,6 M€ (1 anomalo 280,8 M€); L2 171 puliti, 208,2 M€ (1 anomalo 117 M€). Somme superiori al massimale (proroghe +50 % e +12 mesi pubblicate da Consip).
- Proposta: **togliere il lotto 1 da S5** e classificarlo come servizio gestito erogato dal fornitore (cloud, sottoclasse sicurezza-as-a-service), IT; lotto 2 resta S5.

## 2. Identificazione

| Campo | Valore | Fonte | Livello |
|---|---|---|---|
| CIG | L1 88846293CA, L2 8884642E81 | TED 463974-2021 e 485060-2022; Bando GURI nello zip Consip; BDNCP | V2 |
| Gara | procedura aperta d.lgs. 50/2016, AQ lett. a per lotto, ID Sigef 2296 | TED; pagina Consip | V2 |
| Date | indizione 09/09/2021; GUUE S 178 14/09/2021; aggiudicazione efficace L2 16/03/2022, L1 24/05/2022; esito GUUE S-171 06/09/2022 | pagina Consip; TED | V2 |
| Massimali | L1 468 M€: RTI Accenture-Fincantieri NexTech-Fastweb-DEAS 280,8 M€ (solo PAL), RTI Telecom Italia-Netgroup-Reevo-KPMG-Almaviva 187,2 M€ (solo PAC); L2 117 M€: RTI Deloitte-EY-Teleco 70,2 M€ (PAL), RTI Intellera-Capgemini-… (PAC) | TED 485060-2022; BDNCP | V2 |
| Durata | AQ 24 mesi; contratti esecutivi fino a 48 mesi | Bando GURI (zip Consip); BDNCP 1460 giorni | V2 |
| Estensioni | «Sicurezza Remoto +50 %» e «+50 % +12 mesi» (zip firmati sulla pagina Consip, non letti) | pagina Consip | R |

## 3. Cosa contiene

Lotto 1 (CTS lotto 1, §3-4; bando TED):
- servizi L1.S1-S15: SOC, NGFW, WAF, gestione continua delle vulnerabilità, threat intelligence, protezione navigazione e posta, endpoint (EDR), certificati SSL, formazione, IAM, firma digitale remota, sigillo e timbro elettronico, validazione temporale, servizi specialistici. **V**
- «L'erogazione dei servizi in modalità "da remoto" … richiede che il Fornitore dovrà disporre obbligatoriamente di Centri Servizi», «dislocati su sedi ubicate sul territorio comunitario»; il centro servizi è «la struttura complessiva all'interno della quale è ritagliata dal Fornitore l'infrastruttura dedicata alle Amministrazioni» (CTS L1 §4). **V** → infrastruttura condivisa del fornitore, prezzata a canone: modello as-a-service.
- servizi specialistici per la «migrazione dei servizi di sicurezza dell'Amministrazione di tipo "on premise" verso i servizi oggetto di fornitura» (CTS L1). **V**
- Continuità dichiarata con SPC Cloud lotto 2 (CTG). **V**
- RTI Accenture (AQ firmato con offerta tecnica): Centro Servizi Fastweb Caracciolo e Bernina (Milano), Polo Tiburtino (Roma, DR); tecnologie Fortinet, Splunk, Palo Alto, Tenable, Qualys, Trend Micro; clausola dati personali: trattamento nell'UE. **V**
- RTI Telecom (PAC): centro servizi e tecnologie **non letti** (sito aqsicurezzadaremoto.tim.it archiviato ma senza contenuto utile in HTML). **R**

Lotto 2: servizi di compliance e controllo (VA, PT, security strategy, supporto normativo), CPV 72810000 audit informatico. **V** (bando). CTS L2 non analizzato in dettaglio.

## 4. Analisi degli attuativi (BDNCP)

| Misura | Lotto 1 | Lotto 2 |
|---|---|---|
| attuativi | 307 | 172 |
| anomali | ASR Abruzzo 280,8 M€ (= quota RTI Accenture) | Acquedotto Pugliese 117 M€ (= massimale) |
| euro puliti | 492.634.114 (1,05 × massimale) | 208.150.473 (1,78 ×) |
| per anno | 2022 27,7; 2023 202,0; 2024 161,4; 2025 100,7; 2026 0,8 M€ | 2022 37,1; 2023 60,1; 2024 58,0; 2025 52,9 M€ |
| mediana / p90 | 0,61 / 3,63 M€ | 0,46 / 2,85 M€ |
| possibili doppioni | 6 / 3,0 M€ | 6 / 4,8 M€ |
| SOC/monitoraggio in oggetto | 29 / 69,5 M€ | 2 / 8,8 M€ |
| cloud in oggetto | 4 / 3,7 M€ (es. GSE «WAF e API protection in cloud») | 1 / 0,8 M€ |
| maggiori | DAP 23,7 M€ (SOC, IPAM, PAM), INPS 22,5, Sogei 21,6, ARES Sardegna 18,0, Banca d'Italia 16,0 | ARIA 20,0; ARIA 10,9; Calabria 7,0; INAIL 6,5 |

Le somme oltre il massimale sono coerenti con gli aumenti (+50 %) pubblicati da Consip ma non letti: da verificare.

## 5. Classificazione proposta

- **Lotto 1**: fuori da S5. Categoria «sicurezza-as-a-service» (servizio gestito da infrastruttura condivisa del fornitore). Asse cloud: **incluso** (confidenza media-alta: il CTS non usa la parola cloud per l'erogazione; la qualificazione è nostra, sul modello: risorse del fornitore, condivise, a canone, accesso remoto). Asse giurisdizione: erogazione **IT** per il RTI Accenture-Fastweb (V), **UE** garantita per entrambi (V), **IT probabile** per RTI Telecom (R); lente prodotto: tecnologie extra-UE (Fortinet, Splunk, Palo Alto, Tenable, Qualys USA; Trend Micro JP) gestite in DC italiani.
- Parte del L1 è comunque in-house (servizi specialistici a giornate, apparati NGFW eventualmente installati presso l'ente): quota non stimabile dagli oggetti.
- **Lotto 2**: **S5 – consulenza IT di sicurezza**, asse cloud escluso certo.

## 6. Assunzioni e limiti

- «Cloud» per il L1 è un'interpretazione di metodo da sottoporre a Fabio (`decisione-fabio`): un SOC gestito o un firewall erogato da centro servizi è servizio esterno, non infrastruttura dell'ente.
- Letta solo l'offerta del RTI Accenture (quota PAL); quella del RTI Telecom (PAC: INPS, Sogei, DAP…) no.
- Gli attuativi non dicono quali servizi del catalogo acquistano: la quota as-a-service vs giornate professionali è ignota.

## 7. Fonti

| URL | sha256 | Cosa conferma | Tipo |
|---|---|---|---|
| https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID%202296%20-%20Documentazione%20di%20gara%20-%20NEW.zip | 7170e78b9569e9aa0e5afc05756e9607bf1004f25c861c22062f83178466bdba | CTS L1 (file interno 97be26b4c747ea8161737566b1b3fb0cc51cb20ac13c890562687b51088b8c17): servizi, centri servizi UE, migrazione da on-premise; CTG (af5f3bfd6365256ad35e48e5e94c7fd2507e4c291d126879b71242a822e077ed): continuità SPC Cloud L2; Bando GURI: CIG, durata | stazione appaltante |
| https://www.consip.it/sites/default/files/ID%202296_Gara%20Sicurezza%20da%20remoto%20-%20Accordo%20Quadro%20-%20Lotto%201%20RTI%20Accenture.pdf | ffd1a2f0e9d95b64b78f52763be58b0fcb0696c0c17e4ac0e3967d1aecb74de7 | AQ firmato con offerta tecnica: DC Fastweb Milano/Roma, Fortinet, Splunk, Palo Alto, Trend Micro; dati in UE | stazione appaltante |
| https://www.consip.it/bandi/gara-servizi-di-sicurezza-da-remoto-di-compliance-e-controllo-per-le-pa | a337d313b42577af29aa9e88d36c891988827609b78c5f7f63a1a3f80138774e | cronologia, estensioni +50 % | stazione appaltante |
| https://ted.europa.eu/it/notice/463974-2021/xml | 239ea5516dc821fccf3e9d3f6c6a06abdc43d6934b83c51fa5bc8761f71efddf | bando, CIG, servizi lotto 1 | stazione appaltante (TED) |
| https://ted.europa.eu/it/notice/485060-2022/xml | a1029f10b18c1096657cd3435771d3f25593048c2ec2850ce0af661c7ec5f9de | aggiudicazione, quote PAL/PAC | stazione appaltante (TED) |
| BDNCP ANAC nel mirror | per file in `archivio/manifest.jsonl` | padri e attuativi | ANAC (dato della SA) |

## Proposta per iniziative_ict.yaml

```yaml
- cig: 88846293CA
  iniziativa: Consip AQ Servizi di sicurezza da remoto, compliance e controllo, ID 2296, lotto 1 sicurezza da remoto
  categoria: sicurezza-as-a-service   # nuova: servizio gestito da centri servizi del fornitore (decisione-fabio)
  stato: verificato
  asse_cloud: incluso                 # erogazione da infrastruttura condivisa del fornitore, a canone; quota a giornate ignota
  asse_giurisdizione: IT              # centri servizi UE obbligatori; RTI Accenture-Fastweb: DC Fastweb Milano/Roma (V); RTI Telecom: R
  produttori: [Fortinet, Splunk, Palo Alto Networks, Tenable, Qualys, Trend Micro]   # offerta RTI Accenture
  dossier: report/convenzioni/88846293CA-sicurezza-da-remoto-compliance.md
  documenti_aggiuntivi:
  - url: https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID%202296%20-%20Documentazione%20di%20gara%20-%20NEW.zip
    sha256: 7170e78b9569e9aa0e5afc05756e9607bf1004f25c861c22062f83178466bdba
    cosa_conferma: CTS lotto 1, centri servizi in UE, migrazione da on-premise
  - url: https://www.consip.it/sites/default/files/ID%202296_Gara%20Sicurezza%20da%20remoto%20-%20Accordo%20Quadro%20-%20Lotto%201%20RTI%20Accenture.pdf
    sha256: ffd1a2f0e9d95b64b78f52763be58b0fcb0696c0c17e4ac0e3967d1aecb74de7
    cosa_conferma: DC Fastweb e tecnologie del RTI Accenture
- cig: 8884642E81
  iniziativa: Consip AQ Servizi di sicurezza da remoto, compliance e controllo, ID 2296, lotto 2 compliance e controllo
  categoria: sicurezza
  stato: verificato
  sottoclasse_s5: consulenza-it-sicurezza
  asse_cloud: escluso-certo
  dossier: report/convenzioni/88846293CA-sicurezza-da-remoto-compliance.md
```
