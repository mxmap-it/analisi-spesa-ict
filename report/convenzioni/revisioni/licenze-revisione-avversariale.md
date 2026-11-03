# Revisione avversariale — dossier convenzioni di licenze (#55)

Versione 1.0 — 3/11/2026. Oggetto: `report/convenzioni/8335254532-microsoft-ea6.md`, `97431204F9-microsoft-ea8.md`, `B1D4011AB2-microsoft-ea9.md`, `9660108D4B-multibrand6-oracle.md` e `prove-attuativi/`. Regola applicata: DECISIONI.md, voce 2026-11-03 («verificato» = almeno due fonti indipendenti, una della stazione appaltante; licenze ≠ cloud).

Metodo del revisore: i testi dei documenti già archiviati sono stati rilavorati da zero sul server (`pdftotext` dei blob, in `lavoro/rev55/`), più quattro documenti nuovi archiviati con `tools/archivia.py` (§ Fonti nuove). Nessun contatto con terzi.

## Verdetti in testa

| Convenzione | Verdetto | Classificazione difendibile per l'imbuto |
|---|---|---|
| **EA6** 8335254532 | Identificazione regge; **quota 0,44 cade** come stima (è un limite inferiore, non una stima); «Azure assente» regge solo per il consumo IaaS/PaaS | asse A `misto` con **prevalenza SaaS non quantificata** (quota ≥ 0,44, intervallo dichiarato 0,44–0,9, confidenza bassa); asse B `EXTRA-UE` (alta); stato `verificato` per CIG↔iniziativa, aggiudicatario `da verificare` |
| **EA8** 97431204F9 | Identificazione regge; **quota 0,45 cade** (inferita da pesi di altre edizioni, a loro volta non stime) | asse A `misto`, prevalenza SaaS, quota ≥ 0,45 non puntuale; asse B `EXTRA-UE`; stato `verificato` |
| **EA9** B1D4011AB2 | Legame CIG↔ID 2755 **regge, rafforzato** (secondo ente aderente indipendente); **quota 0,50 cade** (definizione delle famiglie non letta; esempio MAECI riportato in modo incompleto) | asse A `misto`, prevalenza SaaS; asse B `EXTRA-UE`; stato `verificato` (con riserva: nessun documento Consip scrive il CIG, solo BDNCP) |
| **Multibrand 6 lotto 1 Oracle** 9660108D4B | «Solo on-premise» **regge per l'oggetto della convenzione**, **regge con riserva per la spesa**: i due attuativi DTD «cloud» (13,4 M€, un terzo del massimale) non sono stati aperti e il loro aggancio al lotto è dubbio | asse A `on-premise` per la convenzione (alta); quota cloud della spesa **non dichiarabile = 0** finché gli atti DTD non sono letti; asse B `EXTRA-UE`; stato `verificato` |

**Assunzioni cadute:** (1) i pesi di ponderazione degli sconti come stima della quota SaaS, in tutte e tre le EA; (2) «Famiglia II = on-premise» implicita nella lettura 44/56; (3) «nessun Azure» in senso lato (in EA6/EA8 si comprano licenze a marchio Azure, es. Azure Active Directory); (4) l'aggiudicatario EA6 è sostenuto da un solo ente aderente (due determine dello stesso Consiglio regionale non sono fonti indipendenti); (5) la descrizione dell'ordine MAECI in EA9 (omette 904 core CIS Suite Datacenter, Visual Studio, Visio, RDS CAL); (6) l'esclusione automatica degli «anomali» nel lotto Oracle (soglia 20 % = 8 M€ esclude due ordini plausibili e tra i più rilevanti per la domanda cloud).

---

## 1. Quote SaaS dai pesi di ponderazione (EA6 44 %, EA8 40–50 %, EA9 50 %)

**Tesi.** La quota SaaS di ciascuna EA è stimata con il peso della Famiglia I («Microsoft 365») nello sconto ponderato di gara.

**Attacco.**
1. *Il peso è un coefficiente per il calcolo della soglia di sconto*, non una dichiarazione di spesa attesa. Nei chiarimenti EA6 il 0,44 compare solo nell'esempio di un concorrente («0,44*24,500%+0,56*23,500%», 4dda75e5…, p. 4); il capitolato d'oneri non è letto. In EA9 il peso 0,50/0,50 (6c93217a…, domanda 6) è appunto un pari-e-patta: un peso 50/50 con sconti minimi quasi uguali non contiene informazione sulla composizione della spesa.
2. *La Famiglia II contiene anch'essa prodotti cloud.* Nei chiarimenti EA6 (4dda75e5…, domanda 2) un operatore scrive che il listino prevede prodotti «Famiglia II di tipo Dual Use Rights» e che l'aggiornamento mensile consente di inserire «nuovi prodotti di tipo Cloud Microsoft»; Consip risponde (domanda 3) confermando che, «All'interno della famiglia di prodotti di tipo II», le «dual use right» sono acquistabili da chi aveva già licenze Cloud. Quindi Famiglia II ≠ on-premise e **0,44 è al più un limite inferiore** della componente online, non una stima centrale. Il dossier EA6 lo accenna (§5 «la Famiglia II comprende anch'essa prodotti online») ma poi propone `quota_cloud_stimata: 0.44`: incoerente.
3. *I dati di dettaglio SKU disponibili puntano molto più in alto.* Ordini letti con prezzi o quantità:
   - Consiglio reg. Calabria (EA6): M365 E3, M365 F3, O365 E1 → 100 % SaaS (9f970e05…, c9f22bb6…).
   - ART (EA8): Office 365, SharePoint, Copilot → 100 % SaaS (728a027a…, 6963a4a0…).
   - **ARPA Piemonte (EA9, nuovo, 1afb2932…)**: per anno 267.268,20 €, di cui O365 E1/E3 + EMS E3 + Intune = 256.876,80 € (**96,1 % SaaS**), Server Datacenter Core 7.582,40 € (2,8 %), un codice «6VC» non decodificato 2.809 € (1,1 %).
   - MAECI (EA9, 9c57dba2…): 8.000 M365 E3 contro 904 core CIS Suite Datacenter + 128 core SQL Server Enterprise SA + Visual Studio/Visio/RDS CAL; senza prezzi unitari la quota in € non è calcolabile, ma con prezzi di listino tipici M365 E3 pesa la maggioranza.
   - Archivi notarili (EA8): Dynamics 365 F&O → SaaS.
   Nessun ordine documentato con SKU è a prevalenza on-premise. Il campione è piccolo e auto-selezionato (enti che pubblicano il dettaglio), quindi non è una stima, ma **contraddice** una quota del 44–50 %.
4. *Fonti migliori cercate e non trovate*: relazioni annuali Consip sul transato per singola iniziativa, referti Corte dei conti o dati AgID con ripartizione EA per famiglia non individuati in questa sessione. Gli ordinativi (ODA) di acquistinretepa non sono accessibili nel rispetto del robots.txt. Resta da chiedere a Consip il transato per famiglia (I/II) e per tipologia (online/on-premise) — è la raccomandazione di policy naturale.

**Esito: cade.** Il peso di gara non è una stima difendibile della spesa.

**Correzione proposta.** Togliere `quota_cloud_stimata` puntuale; sostituire con `quota_cloud_min: 0.44` (EA6) e una nota «prevalenza SaaS negli ordini con SKU letti (n=5 enti); quota non stimabile dai dati pubblici». Se l'imbuto richiede un numero, usare un intervallo (es. 0,44–0,95) e propagare l'incertezza; in nessun caso 0,44/0,45/0,50 come valori centrali. Aggiungere il campione SKU (Calabria, ART, ARPA Piemonte, MAECI, Archivi notarili) come tabella nei dossier.

## 2. Confine SaaS / on-premise (M365 E3, Dual Use Rights, Software Assurance)

**Tesi.** M365/O365/Dynamics = SaaS; il resto = on-premise; la linea «non è netta» (EA6 §3 nota).

**Attacco.** Con il nostro metodo (cloud = servizio erogato da infrastruttura del provider), la domanda è *dove gira il servizio per cui si paga*:
- **M365 E3 / O365 E3**: il corrispettivo è un abbonamento per utente a servizi erogati dai data center Microsoft (Exchange Online, SharePoint/OneDrive, Teams, Entra ID); il diritto di installare le app Office è accessorio e le app stesse richiedono l'attivazione periodica online. → **cloud (SaaS) per intero**. Non ha senso ripartire il prezzo: Microsoft non lo scompone. Il fatto che il MAECI scriva che le licenze «sono installate sugli apparati hardware di proprietà dell'Amministrazione» (9c57dba2…) è una motivazione contabile (spesa in conto capitale) e **non** prova di natura on-premise; il dossier EA9 la presenta come se la PA «trattasse l'EA come software installato»: lettura da togliere o ridimensionare.
- **EMS E3, Intune, Azure Active Directory / Entra ID**: servizi online → **cloud**, anche se il marchio «Azure» li farebbe confondere con il consumo IaaS.
- **Dual Use Rights**: diritto di usare il prodotto o in locale o nella versione online. La spesa non è attribuibile per natura del contratto; va classificata come **cloud potenziale** ⇒ categoria propria «ambivalente», non sommata né a SaaS né a on-premise.
- **Software Assurance** su prodotti server (SQL Server, CIS Suite, RDS CAL): manutenzione/diritti di aggiornamento di software installato → **on-premise**. «Subscription on-premise» (licenza a tempo di prodotto installato) → **on-premise**: abbonamento ≠ cloud. Le classi regex «SA / rinnovo / supporto» mescolano invece rinnovi M365 (es. «M365 E3 … Renewal») e SA server: classe non interpretabile.

**Esito: regge con riserva** l'impostazione; **cade** la nota MAECI come prova di uso installato.

**Correzione proposta.** Nel metodo (e nei dossier) fissare: M365/O365/EMS/Entra/Intune/Dynamics 365/Copilot = cloud SaaS integrale; Dual Use = «ambivalente»; SA e subscription on-premise = on-premise. Riclassificare «SA/rinnovo» separando rinnovi SaaS da SA server.

## 3. Assenza di Azure nelle EA6/8/9

**Tesi.** Azure non risulta (verificato solo sulla guida EA7 riprodotta dall'ARL Sardegna, e8b65819…, riga «Non è, invece, prevista … la presenza di prodotti / servizi Azure»).

**Attacco.**
- Prove contrarie *parziali* nei dati BDNCP dell'estratto stesso: `9321874DC4` (ATS Val Padana, EA6) «FORNITURA LICENZE AZURE-ACTIVE-DIRECTORY» 19.620,72 €; `B7F5D30888` (Polizia di Stato, EA8) «FORNITURA LICENZE AZURE» 6.554,74 €. Licenze a marchio Azure si comprano dunque in EA6 ed EA8. Azure AD è un servizio d'identità SaaS, non consumo IaaS; per la seconda («licenze Azure») il contenuto non è noto.
- Prove *a favore* dell'assenza di consumo IaaS/PaaS: gli enti comprano i crediti Azure **fuori dalle EA** — Comune di Firenze DD2941/2026 (840fd375…): crediti Azure «Server and Cloud Enrollment» e poi adesione all'AQ Consip «Cloud IaaS e PaaS 2», ID 2746, lotto 3 Microsoft; ARERA 2023 (5356c987…): «Azure Monetary Commit» comprati su MEPA da SoftwareOne. Il canale separato è coerente con l'assenza di Azure consumo nelle EA, ma non la prova per EA6/8/9 (nessun capitolato EA6/8/9 letto).

**Esito: regge con riserva** per il consumo IaaS/PaaS; **cade** la formulazione «Azure ~0» se intesa come «nessun prodotto Azure».

**Correzione proposta.** Scrivere «consumo Azure IaaS/PaaS: non previsto in EA7 (guida), canali alternativi documentati (AQ ID 2746, SCE, MEPA); licenze a marchio Azure (Azure AD) presenti in EA6/EA8 → classificate SaaS». Stato per EA6/8/9: R, non V.

## 4. Legame B1D4011AB2 = EA9 e aggiudicatario EA6

**EA9 — tesi.** CIG↔ID 2755 verificato (determina MAECI + coincidenza BDNCP/TED per data, importo, titolo).
**Attacco.** Nessun documento Consip archiviato scrive il CIG: il lato «stazione appaltante» è il record BDNCP (dichiarazione Consip ad ANAC) che però è generico («FORNITURA DI LICENZE D'USO»); il legame passa per coincidenza di importo/data. Cercata una seconda fonte indipendente: **ARPA Piemonte, determina 146/2026 (1afb2932…)** scrive «Convenzione Consip "Microsoft Enterprise Agreement 9" – lotto1 – Codice iniziativa 4344111 – CIG B1D4011AB2», Telecom Italia. Due enti aderenti indipendenti + record Consip in BDNCP coerente con TED.
**Esito: regge** (rafforzato). Riserva: «lotto 1» in ARPA vs «lotto unico» nel TED è solo nomenclatura.
**Correzione.** Aggiungere ARPA Piemonte (sha256 1afb293267f85a9ceb86563e4e6e01dd9b92169a801382480c9f17f0945e1337) ai `documenti` della voce.

**EA6 — tesi.** Aggiudicatario Telecom Italia (R nel dossier, ma lo stato complessivo proposto è `verificato`).
**Attacco.** Le due fonti sono due determine *dello stesso ente* (Consiglio reg. Calabria 306/2022 e 301/2023): non indipendenti tra loro; nessuna fonte Consip (non c'è TED: appalto specifico SDAPA). Il legame CIG↔ID 2187 invece regge (BDNCP Consip + chiarimenti Consip per l'ID + Calabria per il CIG).
**Esito: regge** l'identificazione; **cade** l'aggiudicatario come dato verificato.
**Correzione.** Mantenere `stato: verificato` solo per CIG↔iniziativa; campo `aggiudicatario` con stato `da-verificare` finché non si trova un secondo ente aderente o il dataset ANAC aggiudicatari per il CIG.

## 5. Oracle multibrand 6 lotto 1 «solo on-premise»

**Tesi.** Il CT ID 2599 (copia Sapienza, c7bd3e20…) parla di «prodotti software on premises», licenze perpetue, MySQL/Java, download da edelivery: nessun OCI/SaaS.
**Attacco.**
- Il CT regge per l'**oggetto** del lotto (letto nel testo). Ma è una copia di terzi: rispetto alla regola delle due fonti l'«on-premise» è sostenuto da un documento Consip in copia Sapienza e dall'esempio Consob (edizione non indicata): una fonte e mezza.
- I due attuativi DTD Giustizia — `A02A0C50B1` 8.254.028 € «FORNITURA DI LICENZE E SERVIZI DI SUPPORTO E CLOUD ORACLE» e `A02A0C832A` 5.186.877 € «… SERVIZI PROFESSIONALI DI CONSULENZA E DI SUPPORTO ORACLE», stessa gara da 13.440.905 € — **non sono stati aperti** (nessun atto DTD trovato pubblico in questa sessione). Due fatti li rendono sospetti come attuativi del lotto 1: (a) CIG pubblicati il **10/11/2023**, quattro giorni dopo l'aggiudicazione del lotto (06/11/2023, TED 702067-2023), quando la convenzione verosimilmente non era ancora attiva; (b) «servizi professionali di consulenza» e «cloud» non sono nell'oggetto del lotto 1 secondo il CT. Indizio indipendente: Digital Value annuncia il 31/05/2023 (a00c11d5…) un contratto «Cloud Oracle SaaS-PaaS Services and specialist support» da ~8 M€ con «a well-known public body», RT Italware–Eurolink, per migrare in cloud applicazioni su piattaforma Oracle on-premise. Importo e periodo compatibili con A02A0C50B1, ma aggiudicatario diverso da quello del lotto 1 (TIM–Eurolink) e ente non nominato: **non** prova il legame, prova che nel 2023 un ente pubblico ha comprato Oracle cloud per ~8 M€ con Eurolink in RT.
- Nel `riepilogo2.json` A02A0C832A cade nella classe «Azure / consumo cloud» (per «cloud oracle» nell'oggetto gara), A02A0C50B1 tra gli anomali: la componente cloud potenziale è invisibile nel conteggio.
**Esito: regge** «on-premise» per la convenzione; **regge con riserva** per la spesa: 13,4 M€ (≈ un terzo del massimale) con «cloud» nell'oggetto sono un'ipotesi contraria aperta.
**Correzione.** Nella yaml: `quota_cloud_stimata: 0.0` → `quota_cloud_convenzione: 0.0` + `attuativi_da_verificare: [A02A0C50B1, A02A0C832A]` con nota «possibile CIG agganciato per errore o acquisti cloud fuori listino»; non pubblicare «spesa cloud Oracle = 0». Cercare la copia del CT su consip.it.

## 6. Metodo sugli attuativi

**Tesi.** Estrazione BDNCP per `cig_accordo_quadro`, anomali = importo ≥ 20 % del massimale o ≥ 100 M€, classi per regex.
**Attacco.**
- *Soglia anomali scelta a mano e non coerente con la propria logica*: EA6 ha 0 anomali ma la somma 422,7 M€ supera il massimale di 280 M€ di oltre il 50 %; il criterio non rileva l'eccesso. Per Oracle, il 20 % di 40 M€ = 8 M€ esclude CNPADC 13,7 M€ e DTD 8,25 M€, plausibili, mentre in EA9 il 20 % sono 107 M€. Un'unica soglia relativa produce esclusioni non confrontabili tra convenzioni.
- *ANCI 45 M€ (B2FCEA46F4) in EA6 pubblicato dopo l'avvio di EA8*: segnalato «da controllare» ma incluso nella somma.
- *Regex*: l'ordine «SaaS prima» attribuisce a SaaS un oggetto misto (es. MAECI: M365 + SQL + CIS); «posta elettronica» non distingue Exchange Online/Server (ammesso); «server», «core», «database» classificano come on-premise testi generici; «SA/rinnovo» raccoglie anche rinnovi M365 (vedi §2); «consumo» manda in «Azure» oggetti non Azure; l'Oracle «cloud» finisce in «Azure». Il 71–83 % degli euro resta «generico»: le classi non pesano nulla e il dossier lo dice correttamente; vanno usate solo come numero di oggetti, non in €.
- *smartCIG esclusi*: gli ordini sotto soglia (es. ARERA, Firenze) mancano; distorsione verso i grandi enti, che tendono ad avere più SA server.
- *Somme oltre il massimale*: gli importi BDNCP sono valori a base/stimati e includono rinnovi e duplicati (InfoCamere 2×430 M€). Le somme «senza anomali» (453,3 M€ EA8, 345,0 M€ EA9) sono ancora valori dichiarati, non spesa: vanno sempre etichettate come tali.
- *«Ultima versione per CIG»* dipende dall'ordine di lettura dei file (annuali poi delta): corretto se i delta seguono gli annuali, non verificato nello script pubblicato (`analizza2.py` legge il CSV già estratto).
**Esito: regge con riserva** come descrizione; **cade** come base di qualunque ripartizione in €.
**Correzione.** Anomalo = importo > massimale residuo o duplicato esatto del massimale, più revisione manuale motivata per ogni CIG > 5 % del massimale; riportare sempre la somma con e senza gli esclusi; non usare le classi regex in euro.

## 7. Stati «verificato» proposti e regola delle due fonti

| Voce | Fonte stazione appaltante | Seconda fonte indipendente | Esito |
|---|---|---|---|
| EA6 CIG↔ID 2187 | BDNCP (Consip) + chiarimenti Consip (ID) | Calabria (CIG) | regge |
| EA6 aggiudicatario TIM | nessuna | Calabria (unico ente) | **cade** → da verificare |
| EA6 massimale 280 M€ | BDNCP | nessuna | regge con riserva (una fonte; dossier lo dice) |
| EA8 CIG↔ID 2615, TIM | TED ×2 + BDNCP | ART, UCAN | regge |
| EA9 CIG↔ID 2755 | BDNCP + TED (per coincidenza) | MAECI + **ARPA Piemonte** | regge |
| Oracle 9660108D4B | TED ×2 + BDNCP | CT (copia Sapienza), Consob | regge |
| Oracle «on-premise» | CT (copia di terzi) | — | regge con riserva |
| EA6/8/9 «Azure assente» | nessuna per EA6/8/9 | guida EA7 | **non verificato** (R) |
| EA9 Famiglia I = Microsoft 365 | nessuna (analogia EA6) | — | **non verificato** (R) |

## Fonti nuove archiviate (server, `archivio/manifest.jsonl`)

| URL | sha256 | Uso |
|---|---|---|
| https://bandi.arpa.piemonte.it/sites/default/files/allegati/bandi-appalti/2026/338/Determina_n.%20146%20del%2013.03.2026.pdf | 1afb293267f85a9ceb86563e4e6e01dd9b92169a801382480c9f17f0945e1337 | EA9: CIG B1D4011AB2 (secondo ente), dettaglio SKU e prezzi: 96 % SaaS |
| https://affidamenti.comune.fi.it/sites/affidamenti.comune.fi.it/files/profilo/aggiudicazione-definitiva/20260420/20260417-DD2941.pdf | 840fd37589af3e7a5573183842842ab243376a8679b786ba8fccb445ba8fae69 | Azure consumo comprato fuori EA (SCE, AQ ID 2746 lotto 3) |
| https://www.arera.it/fileadmin/allegati/gare/2023/Atto_di_affidamento_SoftwareOne_signed.pdf | 5356c98739101d660afefb741c5c18295ca00d91603de66029e06864748abc51 | Azure Monetary Commit via MEPA, fuori EA |
| https://www.digitalvalue.it/wp-content/uploads/2024/03/PR_Strategic-contract-Cloud.pdf | a00c11d5111c94703694847b51ac7e9b439beddf4af95bf2433111a1ed0cd21a | Oracle SaaS-PaaS ~8 M€ a ente pubblico, RT Italware–Eurolink, 31/05/2023 (indizio, fonte di parte) |

Documenti già archiviati riletti: 4dda75e5… (chiarimenti EA6), 6c93217a… (chiarimenti EA9), 9c57dba2… (MAECI; nota: nel manifest il tipo è `text/html` ma il blob è un PDF valido di 4 pagine), 9f970e05… (Calabria), e8b65819… (guida EA7), c7bd3e20… (CT ID 2599), 528c2911… (Consob EA9). Estratto attuativi: `prove-attuativi/attuativi.csv` (righe 9321874DC4, B7F5D30888, A02A0C50B1, A02A0C832A citate sopra).

## Cosa resta aperto

1. Transato per famiglia/tipologia delle EA: chiederlo a Consip (o FOIA); senza, nessuna quota puntuale è pubblicabile.
2. Atti DTD Giustizia per A02A0C50B1/A02A0C832A.
3. Capitolati EA6/8/9 per Azure e definizione delle famiglie EA8/EA9.
4. Secondo ente aderente per l'aggiudicatario EA6.
