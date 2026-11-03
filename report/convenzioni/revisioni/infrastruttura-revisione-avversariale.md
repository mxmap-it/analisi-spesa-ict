# Revisione avversariale — system management, sicurezza da remoto, SPC2, reti locali, PC (#55)

Versione 1.0 — 2026-11-03. Revisore avversariale (DECISIONI.md, voce 2026-11-03). Oggetto: i dossier `7260902DDE-system-management-2.md`, `893944468E-system-management-3.md`, `B2094754F1-system-management-4.md`, `88846293CA-sicurezza-da-remoto-compliance.md`, `5133642F61-spc2-connettivita.md`, `9543706356-reti-locali-8-lotto-2.md`, `9158053868-pc-portatili-chromebook.md`, `9823936871-pc-desktop-workstation-3.md` e `tools/verifiche/attuativi_s5.py`. Non ho modificato i dossier né `config/iniziative_ict.yaml`. File di lavoro: `lavoro/rev-infra/` sul server. I documenti nuovi sono archiviati con `tools/archivia.py` (sha256 qui sotto). Righe degli attuativi lette da `lavoro/convenzioni/attuativi_s5.csv`, prodotto dallo script, senza ricaricare i CIG.

## Verdetti e classificazione difendibile per l'imbuto

| Iniziativa | Verdetto | Classificazione difendibile |
|---|---|---|
| Sicurezza da remoto L1 88846293CA | **Cadono** «giurisdizione IT» e «cloud incluso» come stato certo | Categoria «servizio gestito di sicurezza» (nuova, `decisione-fabio`). **Asse cloud: incerto/misto**: gli attuativi comprano anche realizzazione di componenti presso l'ente e formazione (Giustizia, 23,8 M€). **Giurisdizione, lente prodotto (primaria): EXTRA-UE** per la quota RTI Accenture (Fortinet, Splunk, Palo Alto, Tenable, Qualys: USA; Trend Micro: JP); **incerta** per la quota RTI TIM (offerta non trovata). Lente fornitore/erogazione: IT. Stato: identificazione verificata, contenuto da verificare. |
| Sicurezza da remoto L2 8884642E81 | **Regge** | S5 consulenza di sicurezza, escluso certo. |
| SPC2 5133642F61 | **Regge con riserva**; cadono gli aggiudicatari e la «proroga non documentata» | Connettività S5. Asse cloud **incerto** solo per l'IaaS del bando (contratto non trovato); gli attuativi «cloud» vanno riassegnati. Firmatari del 2016: Tiscali (60 %, poi Fastweb), BT Italia e Vodafone (20 % ciascuno). TIM ed Ericsson non risultano tra i firmatari. |
| System management 2 (1836) | **Regge con riserva** | S5. Escluso, con confidenza media; IFO «disaster recovery» (0,19 M€) incerto. |
| System management 3 (2275) | **Regge con riserva** | S5. Escluso certo per il catalogo; **12** attuativi con cloud/DC nell'oggetto (non 11) → «migrazione/gestione cloud», incerti; i 4 CIG LTF identici vanno contati una volta sola. |
| System management 4 (2710) | **Regge** | S5. Escluso certo (esclusione testuale nel CTS); 3 attuativi di migrazione incerti, di cui 2 doppioni (Siracusa). |
| Reti locali 8 L2 9543706356 | **Regge con riserva** | Hardware di rete in-house S5, escluso certo. Giurisdizione prodotto EXTRA-UE solo come **riferito** (campione di marchi). |
| PC portatili L1 9158053868 | **Regge**; la correzione dello YAML è confermata | Hardware in-house S5, escluso certo. SO Windows 11 Pro/Education a licenza perpetua (V, chiarimenti Consip) → prodotto EXTRA-UE. |
| Chromebook L3 91580749BC | **Regge con riserva** | Hardware con dipendenza Google. Licenza Chrome Upgrade **non accertata** per l'edizione 1; nell'edizione 2 (ID 2759) sarebbe inclusa (R). |
| PC desktop L2 9823936871 | **Regge con riserva** | Hardware in-house S5, escluso certo; marchio Lenovo R (dagli oggetti). |

## Assunzioni cadute

1. **Sicurezza L1, giurisdizione «IT».** Contraddice il metodo (AGENTS.md §2: la giurisdizione si attribuisce al prodotto). IT vale solo per la lente fornitore/erogazione.
2. **Sicurezza L1, «cloud incluso» con confidenza media-alta.** L'attuativo Giustizia/DAP (il più grande, 23,8 M€, RTI TIM) compra «Realizzazione SOC – Componente DHCP IPAM», «Componente funzionale PAM», protezione endpoint, «Gestione Servizi di Sicurezza per i Portali in Cloud» e sensibilizzazione del personale. È un insieme di realizzazioni presso l'ente, servizi gestiti e formazione, non solo consumo di un servizio condiviso.
3. **Sicurezza L1, «somme oltre il massimale coerenti con +50 % non letti».** Ora le lettere sono lette. +50 % alla quota PAL Accenture (280,8 → 421,2 M€, art. 17 c.3 DL 13/2023) e alla quota PAC TIM (+50 %, art. 13-bis L. 170/2023), con proroga dell'AQ al 28/07/2025. Il massimale aggiornato del L1 è circa **702 M€**: i 492,6 M€ puliti ne valgono 0,70, non «1,05 ×». Il lotto 2 vale 175,5 M€ aggiornati (PAL 70,2 → 105,3 M€, più la quota PAC Intellera estesa): da ricalcolare.
4. **SPC2, aggiudicatari «Fastweb, TIM, Vodafone, Ericsson».** Il comunicato AgID/Consip del 24/05/2016 riporta i contratti firmati con Tiscali (60 %), BT Italia e Vodafone (20 % ciascuno). Il campo `aggiudicatari` BDNCP dei figli è la lista dei partecipanti copiata dall'ente (es. «ERICSSON | FASTWEB | TIM | VODAFONE» su attuativi Fastweb): **non usabile come esecutore**. Le 477 righe Ericsson sono quasi tutte 2016-2019 (adesioni iniziali); quelle TIM 2024-2026. Ruolo di Ericsson (forse mandante di un firmatario) e di TIM: da verificare.
5. **SPC2, «482 attuativi 2026 oltre scadenza, proroga non documentata».** L'art. 4 del D.L. 200 del 31/12/2025 estende il CQ OPA fino al 31/12/2026, in attesa di SPC ed. 3 (ID 2573, bando del 01/09/2025). Lo riporta la determina ARPA Piemonte 169/2026, che cita il CIG 5133642F61. Fonte unica di terzi più la norma: **R** finché non si archivia un comunicato Consip.
6. **System management 3, «11 attuativi cloud».** Dalle righe risultano 12 con cloud, data center o DR nell'oggetto, e 4 di questi sono lo **stesso ordine LTF** («Migrazione cloud e conduzione SAP», 1.632.350 € × 4).
7. **PC portatili L1, «SO non noto».** I chiarimenti Consip ID 2425 (II tranche) fissano per il lotto 1 licenze del SO «a tempo indeterminato», tra cui Microsoft Windows 11 Pro Education → on-premise, prodotto USA.

## Dettaglio per assunzione

### 1. Sicurezza da remoto L1 = «security-as-a-service = cloud, IT»

- **Tesi:** catalogo erogato dai centri servizi del fornitore → cloud; DC Fastweb a Milano e Roma → IT.
- **Attacco:** (a) il metodo vuole la giurisdizione del prodotto, e i prodotti dell'offerta Accenture sono tutti USA/JP. (b) «Da remoto» non vuol dire infrastruttura condivisa per ogni voce: NGFW, EDR, PAM e IPAM possono essere apparati o agent presso l'ente, gestiti a distanza. (c) La quota PAC (TIM) non è stata letta. Ho tentato gli URL simmetrici dell'AQ firmato TIM: `…Accordo Quadro - Lotto 1 RTI Telecom.pdf` e `…RTI TIM.pdf` danno «assente». La pagina Consip non lo linka.
- **Prove:**
  - Lettera Consip DL 13/2023, +50 % PAL L1/L2 (zip `2296 - Sicurezza Remoto +50%.zip`), https://www.consip.it/sites/default/files/bandi/documentazione_firmata/2296%20-%20Sicurezza%20Remoto%20%2B50%25.zip — sha256 `b1cfcb29bc36fdbdca5e8310a33abc7003d89738bd8c985659a4e971c5ea62d9` (SA).
  - Lettere Consip L. 170/2023, estensione temporale e +50 % TIM e Intellera, https://www.consip.it/sites/default/files/bandi/documentazione_firmata/2296%20-%20Sicurezza%20Remoto%20%2B50%25%20%2B12mesi_2.zip — `84607deb913b00e39984221ab8a433109ed28e0ecc4b9d90c0f7e89573171dea` (SA).
  - Zip `2296.zip` firmata: contiene solo i rapporti sulle pari opportunità, nessun AQ TIM — `ea61446c23202af4490b52d5e922dda36cd7dd3fe5d11f7469eb6ff47a44d5ed`.
  - Decreti di pagamento Giustizia (CIG derivato 99026071D0, RTI TIM, 23.804.878,05 €), https://www.giustizia.it/cmsresources/cms/documents/dgsia_decpag_telecom_consiplotto1_21giu24.pdf — `36d039f36fe52bfbf89b0901ae2f149f9eb97616caf90f9c2aee920a56fa636a`; https://www.giustizia.it/cmsresources/cms/documents/dgsia_decpag_telecom_lotto1_6giu24.pdf — `2f28c946f1d259fcb6b97064d9bd49046b1a5bed8621fdc4018c37d1c189f771` (aderente).
  - Decisione Consob, adesione RTI TIM per 53.529,60 €, https://www.consob.it/documents/d/asset-library-1912910/0084967_decisione — `9a17f8e8ce295261a912e666bfd238400d02a064f6ccc3909fa3a3588db2d529` (aderente; non dà le tecnologie).
- **Esito:** **cade** (giurisdizione IT e cloud certo).
- **Correzione proposta:** `asse_cloud: incerto` (sottoclasse «servizio gestito di sicurezza»); `asse_giurisdizione: EXTRA-UE` per la lente prodotto sulla quota PAL Accenture, `incerto` per la quota PAC TIM; lente fornitore IT/UE. `produttori` va qualificato come «offerta RTI Accenture». Massimale aggiornato circa 702 M€. Nuova voce in `richieste-e-raccomandazioni.yaml` (proposta): Consip pubblichi gli AQ firmati di tutti gli aggiudicatari, non solo di uno.

### 2. SPC2: IaaS community cloud nel contratto firmato

- **Tesi:** il bando 2013 prevedeva l'IaaS; il contratto non è letto → asse cloud incerto.
- **Attacco:** non ho trovato capitolato, listini o contratto quadro firmato con voci IaaS. Il comunicato del 2016 parla di contratti di «connettività» e colloca il cloud nella gara SPC Cloud separata. È indizio, non prova, che l'IaaS non sia stato contrattato. Gli attuativi «cloud» trovati sono adesioni SPC Cloud mal agganciate o progetti DC.
- **Prove:** comunicato AgID/Consip 24/05/2016, https://www.agid.gov.it/sites/default/files/repository_files/ufficio_stampa/consip_e_agid_sottoscritti_i_contratti_per_la_connettivita_e_aggiudicati_i_primi_due_lotti_della_gara_per_i_servizi_cloud.pdf — `278b20daeb58962d5998556bf5f825bdc98b38ff98e9aa44b8a379965c0a963c` (SA + AgID); determina ARPA Piemonte 169/2026 (proroga al 31/12/2026, DL 200/2025, CIG 5133642F61, STDO 1 Gbps Fastweb), https://bandi.arpa.piemonte.it/sites/default/files/allegati/bandi-appalti/2026/362/Determina_Originale_169_18032026.pdf — `015b4d9a97b7497fa3367ff8ef141c46c4d66892c90d5a767e26cb96d258d718` (aderente).
- **Esito:** **regge con riserva** l'asse cloud «incerto»; **cadono** aggiudicatari e «proroga non documentata».
- **Correzione proposta:** aggiudicatari = Tiscali→Fastweb, BT Italia, Vodafone (fonte AgID/Consip); TIM/Ericsson «da verificare»; `scadenza_cq: 2026-12-31` (DL 200/2025 art. 4, R); in `attuativi_s5.py` non usare `aggiudicatari` BDNCP dei figli come esecutore. Prossimo passo: cercare sulla pagina Consip ID 1367 il capitolato tecnico del CQ firmato (sezione «calcolo e memorizzazione»). Se non esiste, l'asse diventa «escluso con riserva».

### 3. System management 1836 / 2275 / 2710 «cloud escluso»

- **Tesi:** servizi professionali su infrastrutture dell'ente.
- **Attacco:** ricerca nelle righe di regex su cloud, hosting, housing, IaaS, data center, DR e colocation. 1836: Roma Capitale 23,1 M€ «system management per il data center ed il sito di DR di Roma Capitale» (conduzione di DC dell'ente, regge); IFO 186.066 € «acquisizione servizio di disaster recovery» (formulazione da fornitura: incerto). 2275: 12 righe, tra cui ASL FG «migrazione al cloud PNRR 1.2» 0,9 M€, LTF ×4, ENAV 9,6 M€ «progettazione… e conduzione… ambiti tecnologici: cloud…», Firenze «abilitazione al cloud» 1,07 M€, AOU «monitoraggio… on premise e in cloud» 0,5 M€, InnovaPuglia «supporto… datacenter» 0,9 M€. Nessun oggetto parla di fornitura di risorse cloud o di hosting presso il fornitore. 2710: Siracusa «migrazione al cloud» 442.903 € ×2 (doppione), CDP «technology & cloud» 15,7 M€.
- **Prove:** `lavoro/convenzioni/attuativi_s5.csv` (BDNCP, file del mirror per sha256 in `archivio/manifest.jsonl`); CTS 2710 già citato nel dossier.
- **Esito:** **regge** (escluso per la convenzione); gli attuativi di migrazione restano incerti come servizi, non come consumo cloud.
- **Correzione proposta:** in 2275 portare il conteggio a 12, deduplicare LTF (−4,9 M€) e Siracusa in 2710 (−0,44 M€); IFO DR «incerto» finché non si legge l'atto. Nota per l'imbuto: la migrazione PNRR 1.2 è spesa *verso* il cloud, non spesa cloud. Va contata a parte, coerente col sottoinsieme PNRR.

### 4. Pulizia degli importi: criterio unico

- **Tesi:** anomalo se ≥ 25 % del massimale; doppioni solo segnalati.
- **Attacco:** (a) Tradate 480.000.000 € («proroga CE OPA 2024», CIG B12C4DB93C) passa la soglia (19 % di 2,5 G€) ed è da solo il 72 % del 2024 SPC2. (b) Il massimale di riferimento ignora le estensioni (+50 %, quinto d'obbligo), quindi la soglia è sbagliata in entrambe le direzioni. (c) I doppioni identici (LTF ×4, Siracusa ×2) gonfiano i puliti.
- **Esito:** **cade** la regola attuale come regola unica.
- **Correzione proposta (criterio unico per tutte le convenzioni):**
  1. *massimale di riferimento* = massimale aggiornato dalle comunicazioni Consip archiviate (estensioni comprese), altrimenti BDNCP, dichiarato nel dossier;
  2. *escluso automatico* se l'importo è ≥ 25 % del massimale di riferimento, oppure se è uguale (±1 %) al massimale, a una quota d'aggiudicazione o al valore del lotto;
  3. *in revisione manuale* se l'importo è ≥ 50 × la mediana dell'iniziativa e non è già escluso. Con questa regola Tradate (mediana SPC2 123 k€ → soglia 6,2 M€) entra in revisione. Lo stesso vale per i grandi legittimi (es. Sardegna 26,4 M€), che restano dopo la revisione;
  4. *doppioni*: stessa SA, stesso importo e stesso oggetto normalizzato → si conta una volta sola (sottratti, non segnalati); le proroghe restano separate e marcate;
  5. si pubblica una **forbice** [puliti − in revisione; puliti] e il rapporto con il massimale di riferimento.

  Vanno integrati in `attuativi_s5.py` e nello script delle altre convenzioni con un'unica funzione condivisa.

### 5. Marchi hardware e giurisdizione

- **Tesi:** Lenovo HK/CN, HP/Dell/Cisco USA, Acer TW, Huawei CN, dal campione degli oggetti.
- **Attacco:** (a) campione di circa 50 oggetti su 800 e oltre: frequenza, non quota di spesa. (b) `config/marchi_cloud.yaml` non ha **alcuna voce hardware** e usa solo i bucket IT/UE/EXTRA-UE: le etichette «HK/CN» e «TW» dei dossier non hanno un codice nella configurazione. (c) Per la convenzione PC desktop L2 il marchio dovrebbe venire dalla Convenzione o dalla guida (aggiudicatario unico Italware, rivenditore).
- **Esito:** **regge con riserva**: tutti i marchi citati sono EXTRA-UE in qualunque codifica, quindi il bucket non cambia. Il paese di dettaglio resta R.
- **Correzione proposta:** codificare EXTRA-UE con paese come metadato; aggiungere una sezione hardware in `config/` (marchio → paese, con fonte) prima di usarla (AGENTS.md §5); prendere il marchio dal listino o dalla guida Consip della convenzione, non dagli oggetti. Chromebook: licenza non accertata per ID 2425. Il capitolato L3 resta da archiviare; il ricercatore web indica «licenza Chrome Upgrade» inclusa nell'ed. 2 ID 2759 (R, fonte non archiviata).

### 6. Correzione YAML PC 2425

- **Esito:** **regge**. BDNCP `padre_oggetto`: 9158053868 = «LOTTO 1 (PERSONAL COMPUTER PORTATILI)», 91580749BC = «LOTTO 3 (CHROMEBOOK)», 9158062FD3 = «LOTTO2 (MOBILE WORKSTATION)». Con il bando TED Consip già citato fa V2.
- **Prove nuove:** Chiarimenti ID 2425 II tranche, https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID2425%20-%20AQ%20PC%20Portatili%201%20-%20II%20tranche%20Chiarimenti.pdf — `2ee41d4c33f4de848c7b424e99a361d9eefceb5cff64094ed8ea6e9b385e7b6c` (SO lotto 1); Rettifiche ID 2425, https://www.consip.it/sites/default/files/bandi/documentazione_non_firmata/ID%202425%20-%20Rettifiche%20alla%20documentazione.pdf — `d5d053f5d2b185f320f9f6c5fb940b426ac136f7949b119666886b4a9052cc32` (3 lotti; nulla su Chrome).

### 7. «Verificato» = due fonti indipendenti, una della SA

- **Esito:** **regge con riserva**. L'identificazione (CIG, gara, massimale) ha quasi sempre la fonte Consip/TED più BDNCP. Tre punti però non tengono:
  - lo stato `verificato` proposto per L1 sicurezza copre anche classificazione e giurisdizione, che invece si appoggiano a una sola offerta (Accenture) e lasciano la quota TIM non letta;
  - per SPC2, date, massimale e aggiudicatari sono a fonte unica (lo dichiara il dossier stesso), mentre la riga YAML dice `verificato` senza riserve;
  - i marchi di reti locali e PC sono R.
- **Correzione proposta:** separare nello YAML `stato_identificazione` da `stato_classificazione`; «verificato» solo quando entrambi hanno V2.

### 8. `archivia(..., accetta_html=True)` sulle pagine Consip

- **Fatti:** `tools/archivia.py` scarta le risposte HTML quando ci si aspetta un file («probabile blocco WAF»). `accetta_html=True` è previsto per «pagine web vere» (docstring). Le pagine Consip archiviate sono `text/html` da 64-90 kB e contengono i link reali ai documenti, quindi non sono pagine di blocco. `robots.txt` di consip.it vieta solo `/core/`, `/profiles/` e file di installazione; `/bandi/` e `/sites/default/files/` sono permessi. Nessun header o cookie aggirato.
- **Attacco:** l'opzione disattiva l'unico controllo anti-WAF. Una pagina di blocco HTML verrebbe archiviata come «nuovo» senza segnalazione. L'uso non è documentato nei dossier né in DECISIONI.md. `archivia.py` non legge robots.txt: il rispetto è affidato all'operatore.
- **Esito:** **regge con riserva** (legittimo, ma non documentato).
- **Correzione proposta:** con `accetta_html=True`, verificare almeno una stringa attesa (es. «ID 2296» o il titolo) e registrare nel manifest `accetta_html: true`; una riga in DECISIONI.md o in `acquisizione-documenti.md`; controllo robots.txt dentro `archivia.py`.

## Note minori

- Reti locali L2: massimale BDNCP 217 M€ contro aggiudicazione 145,2 M€ (174,2 con il sesto quinto): la soglia del 25 % va calcolata sul massimale di riferimento del punto 4.
- `attuativi_s5.json`: il campo `doppioni` è un oggetto a 2 chiavi, non un numero; le tabelle dei dossier sono corrette, ma il JSON è fuorviante per chi lo riusa.

## Fonti nuove archiviate in questa revisione

| URL | sha256 |
|---|---|
| consip.it …/documentazione_firmata/2296.zip | ea61446c23202af4490b52d5e922dda36cd7dd3fe5d11f7469eb6ff47a44d5ed |
| consip.it …/2296 - Sicurezza Remoto +50%.zip | b1cfcb29bc36fdbdca5e8310a33abc7003d89738bd8c985659a4e971c5ea62d9 |
| consip.it …/2296 - Sicurezza Remoto +50% +12mesi_2.zip | 84607deb913b00e39984221ab8a433109ed28e0ecc4b9d90c0f7e89573171dea |
| giustizia.it dgsia_decpag_telecom_consiplotto1_21giu24.pdf | 36d039f36fe52bfbf89b0901ae2f149f9eb97616caf90f9c2aee920a56fa636a |
| giustizia.it dgsia_decpag_telecom_lotto1_6giu24.pdf | 2f28c946f1d259fcb6b97064d9bd49046b1a5bed8621fdc4018c37d1c189f771 |
| consob.it 0084967_decisione | 9a17f8e8ce295261a912e666bfd238400d02a064f6ccc3909fa3a3588db2d529 |
| agid.gov.it comunicato 24/05/2016 SPC | 278b20daeb58962d5998556bf5f825bdc98b38ff98e9aa44b8a379965c0a963c |
| arpa.piemonte.it Determina 169/2026 | 015b4d9a97b7497fa3367ff8ef141c46c4d66892c90d5a767e26cb96d258d718 |
| consip.it ID 2425 Rettifiche | d5d053f5d2b185f320f9f6c5fb940b426ac136f7949b119666886b4a9052cc32 |
| consip.it ID 2425 II tranche Chiarimenti | 2ee41d4c33f4de848c7b424e99a361d9eefceb5cff64094ed8ea6e9b385e7b6c |

Tentativi falliti («assente»): AQ firmato L1 RTI Telecom/TIM agli URL simmetrici a quello Accenture.
