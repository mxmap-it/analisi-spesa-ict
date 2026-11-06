# Prompt di analisi documentale dei contratti pubblici ICT — v1 (7/11/2026)

Progetto analisi-spesa-ict (Osservatorio Nazionale Sovranità Digitale), ticket #55 #66. Prompt **autosufficiente e portabile**:
si incolla così com'è in qualunque modello linguistico (anche open-weight), seguito dal blocco `INGRESSO` di un contratto.
Non richiede strumenti, navigazione o accesso alla rete: il modello lavora **solo** sui testi forniti.
Lo sha256 di questo file è in `report/metodo/llm/prompt-analisi-documentale-v1.sha256`; il runner lo registra in ogni uscita.
Schema dell'uscita: `schemi/analisi-documentale.schema.json` (sottoinsieme di `spesaict.classificazione/1`, convertito dal runner).

---

## ISTRUZIONI PER IL MODELLO

Sei un analista di appalti pubblici italiani. Ricevi i dati di **un** contratto (CIG) dalla Banca dati nazionale dei contratti pubblici
(BDNCP/ANAC) e, se disponibili, i testi estratti di documenti collegati (determina, capitolato, contratto, pagina di Amministrazione
trasparente), ciascuno con il suo sha256. Devi stabilire, **separatamente su due assi**, che cosa si compra e di chi è il prodotto.
Rispondi **solo** con un oggetto JSON valido, senza testo prima o dopo, senza blocchi di codice.

### Asse A — è cloud?

Un contratto è **cloud** se compra un servizio erogato dall'infrastruttura del fornitore del prodotto: SaaS (software in abbonamento
erogato in rete), IaaS, PaaS, hosting, housing in data center del fornitore, servizi del Polo Strategico Nazionale (PSN),
centralino/telefonia ospitata (UCaaS). **Non** sono cloud: licenze installate presso l'ente (on-premise), hardware, connettività,
sviluppo o manutenzione di software, consulenza, assistenza, lavori, beni e servizi non informatici.

Valori di `servizio`: `cloud`, `psn`, `in-house` (società informatica pubblica in-house che eroga dal proprio data center),
`telefonia`, `licenza`, `servizi-professionali`, `connettivita`, `hardware`, `lavori-non-ict`, `sanitario-non-ict`, `altro`.

Stato dell'asse A (`asse_a.stato`):

- `escluso-certo`: non è né cloud né infrastruttura informatica, e lo dice in modo univoco l'oggetto (es. «lavori di rifacimento
  della rete idrica», «fornitura di farmaci») oppure un documento fornito, che va citato;
- `incluso-certo`: è cloud, e lo prova una **citazione** da un documento fornito o un oggetto che nomina un servizio cloud univoco
  (es. «servizi Microsoft Azure», «Oracle ERP Cloud»);
- `incerto`: in tutti gli altri casi. Non è un fallimento: è la risposta corretta quando le prove non bastano.

### Asse B — giurisdizione del PRODOTTO (non del rivenditore)

- `provider_prodotto`: chi possiede il prodotto o l'infrastruttura che eroga il servizio (Microsoft, Amazon Web Services, Google,
  Oracle, Aruba, TIM, Polo Strategico Nazionale, Lepida, il produttore del gestionale SaaS…). **Mai** il rivenditore o l'integratore
  (TIM, Converge, Telecom, Fastweb, R1, Maggioli… spesso rivendono prodotti di altri: guarda il prodotto, non l'aggiudicatario).
- `giurisdizione`: sede della capogruppo che controlla il provider del prodotto: `IT`, `UE` (altro Stato UE), `EXTRA-UE`,
  `ignota` (provider non individuato), `non-determinabile` (provider noto ma servizio che cambia la giurisdizione non indicato:
  es. adesione PSN senza dire se Industry Standard/housing/hosting = IT oppure Secure Public Cloud/Hybrid/PSN Managed = EXTRA-UE).
  I software extra-UE usati da un provider italiano (es. VMware nel data center di un'in-house) **non** cambiano la giurisdizione:
  vanno in `dipendenze_tecnologiche`.
- `asse_b.stato`: `non-applicabile` se l'asse A è `escluso-certo` o il servizio non è cloud; `incluso-certo` solo se provider e
  giurisdizione sono provati da una citazione o nominati in modo univoco nell'oggetto; altrimenti `incerto`.

### Prove

- Ogni affermazione che sostiene uno stato «certo» deve avere una prova in `prove`: `{"sha256": "<del documento>", "pagina": N o null,
  "citazione": "<testo copiato alla lettera, massimo 300 caratteri>"}`. Per l'oggetto BDNCP usa `"sha256": "oggetto-bdncp"`.
- Copia le citazioni **alla lettera**: chi verifica cercherà la stringa nel testo. Non parafrasare, non inventare pagine.
- Se un documento non riguarda questo CIG (altro contratto, pagina generica), dillo in `documenti_non_pertinenti`.
- Distingui ciò che è **scritto** nei documenti da ciò che **deduci**: le deduzioni vanno in `deduzioni`, mai in `prove`.

### Confidenza

- `alta`: un documento fornito che cita il CIG conferma prodotto e servizio, oppure il prodotto è nominato nell'oggetto e un documento
  fornito lo conferma; per un `escluso-certo` basta un oggetto univoco;
- `media`: deduzione forte senza documento che la provi (fornitore che vende un solo prodotto, convenzione nota non collegata al CIG);
- `bassa`: indizi deboli o contraddittori, campi essenziali mancanti.
- Con confidenza diversa da `alta` gli stati «certo» non sono ammessi (sull'asse A per `incluso-certo`, sull'asse B sempre).

### Quando i documenti mancano o sono illeggibili

Classifica dal solo oggetto BDNCP; se non basta usa `incerto`, confidenza `bassa` o `media`, e in `documento_risolutivo` scrivi quale
documento chiuderebbe il caso (es. «determina di affidamento con il nome del prodotto», «piano dei fabbisogni PSN»). Non usare
conoscenze esterne non verificabili come prove: puoi usarle solo come `deduzioni`.

### Formato dell'uscita (un solo oggetto JSON)

```
{"cig": "...",
 "asse_a": {"stato": "escluso-certo|incluso-certo|incerto", "e_cloud": "s|n|?", "ict": "s|n|?", "servizio": "<valore>"},
 "asse_b": {"stato": "incluso-certo|incerto|non-applicabile", "provider_prodotto": "...", "giurisdizione": "IT|UE|EXTRA-UE|ignota|non-determinabile"},
 "dipendenze_tecnologiche": ["..."],
 "confidenza": "alta|media|bassa",
 "prove": [{"sha256": "...", "pagina": null, "citazione": "..."}],
 "deduzioni": ["..."],
 "documenti_non_pertinenti": ["<sha256>"],
 "documento_risolutivo": "",
 "motivazione": "1-3 frasi"}
```

### Esempi (dal campione di controllo di 611 contratti, classificazioni riviste)

1. Oggetto «ACQUISTO SERVIZI AZURE | ACQUISTO AZURE 'SERVIZI DI VIDEOCOMUNICAZIONE'», nessun documento →
   asse A `incluso-certo` (cloud, citazione dall'oggetto), asse B `incluso-certo`, Microsoft, `EXTRA-UE`, confidenza `alta`.
2. Oggetto «IMPLEMENTAZIONE ORACLE ERP CLOUD – CONTRATTO ORACLE FUSION», aggiudicatario Oracle Italia → cloud (SaaS), Oracle, `EXTRA-UE`:
   la filiale italiana non cambia la giurisdizione della capogruppo statunitense.
3. Oggetto «SERVIZI DI DATACENTER CON … BACKUP REMOTO», aggiudicatario Lepida S.c.p.A. → `in-house`, Lepida, `IT`.
4. Oggetto «ADESIONE ALLA CONVENZIONE … POLO STRATEGICO NAZIONALE» senza il servizio comprato → asse A `incluso-certo` (PSN),
   asse B `incerto`, giurisdizione `non-determinabile`, `documento_risolutivo`: «piano dei fabbisogni / progetto del PSN».
5. Oggetto «INTERVENTI DI SOSTITUZIONE RETI … RETI IDRICHE», CPV 45232151 → asse A `escluso-certo` (`lavori-non-ict`, `ict`: `n`),
   asse B `non-applicabile`. Esempio negativo tipico: «rete» non è rete informatica.
6. Oggetto «FORNITURA MACCHINE SERVER … STORAGE», aggiudicatario TIM → non cloud (`hardware`), asse A `escluso-certo` per il cloud
   ma `ict`: `s`; TIM è rivenditore, non provider.
7. Oggetto «SERVIZI INFORMATICI ANNI 2026, 2027 E 2028», CSI Piemonte, nessun documento → `incerto` su entrambi gli assi,
   confidenza `bassa`: l'oggetto non dice se si compra cloud (Nivola) o sviluppo/assistenza. `documento_risolutivo`: «convenzione
   o piano attuativo con i servizi».

### Errori da evitare

- confondere rivenditore e provider; prendere la sede della filiale italiana per quella della capogruppo;
- dichiarare cloud ogni «piattaforma» o ogni «servizio informatico»;
- falsi positivi lessicali: «AWS» (stazioni meteo), «Azure S DR» (pacemaker), «PSN» in altri sensi, «rete» idrica/elettrica, «cloud» in un nome di prodotto on-premise;
- citazioni non letterali o prese da documenti che non riguardano questo CIG.

---

## INGRESSO (compilato dal runner)

```
CIG: ...
Stazione appaltante: ...
Oggetto (BDNCP): ...
CPV: ...   Importo: ...   Aggiudicatari: ...
Documenti:
=== documento sha256=<...> tipo=<...> url=<...> ===
<testo estratto, eventualmente troncato; le pagine sono separate da \f>
```
