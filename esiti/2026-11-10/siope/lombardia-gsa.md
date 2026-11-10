# Regione Lombardia e GSA: dove va la spesa ICT pagata in SIOPE (#12, 10/11/2026)

Verifica: `tools/verifiche/siope_lombardia_gsa.py` 0.1 → `lombardia-gsa.json` (codici gestionali, mesi, trasferimenti, CIG ARIA), `lombardia-gsa-mesi.csv` (una riga per codice ente, anno, mese, codice ICT). Ingressi con sha256 nel json (SIOPE_USCITE 2022-2025, SIOPE_ANAGRAFICHE, aggiudicatari ANAC). Fonti esterne archiviate con `tools/archivia.py`: tabella in fondo.

## 1. Correzione: i «≈300 M€ della GSA» sono la somma di due enti SIOPE [V]

Il CF 80050050154 ha due codici SIOPE: 000713218 Regione Lombardia (bilancio ordinario) e 800000616 gestione sanitaria accentrata (GSA). `siope_ict_enti.py` somma per CF, quindi la riga «GESTIONE SANITARIA REGIONE LOMBARDIA» di `ict-enti.csv` (263/297/332/395 M€) vale per entrambi.

| M€ ICT pagati (senza telefonia) | 2022 | 2023 | 2024 | 2025 |
|---|---:|---:|---:|---:|
| GSA (800000616) | 163,8 | 181,7 | 204,5 | 256,8* |
| Regione ordinaria (000713218) | 99,3 | 115,4 | 127,6 | 137,8 |
| totale CF | 263,2 | 297,2 | 332,1 | 394,6 |

\* GSA 2025: dicembre a zero, quindi il dato 2025 è probabilmente incompleto.

**GSA: solo due codici ICT**, entrambi servizi: 1.03.02.19.999 «altri servizi informatici n.a.c.» (87 / 125 / 138 / 159 M€) e 1.03.02.19.001 «gestione e manutenzione applicazioni» (29 / 43 / 66 / 98 M€). Nel 2022 compaiono anche .011 (44,8 M€) e .010 (1,7 M€). Mancano hardware, licenze e postazioni: per la GSA lo strumento di acquisto è un unico fornitore di servizi. I pagamenti mensili sono a blocchi (per esempio 2024: 49 M€ a maggio, 29 a ottobre, 0 a gennaio), compatibili con acconti e saldi di incarichi più che con fatture di tanti fornitori [stima, il beneficiario in SIOPE non c'è].

**Regione ordinaria:** codici articolati, con sviluppo software in conto capitale (2.02.03.02.001, 33-52 M€) e manutenzione applicazioni (44-66 M€). Pagamenti concentrati a febbraio (51-83 M€).

**Trasferimenti:** la GSA paga anche 47-55 M€ l'anno di «trasferimenti correnti a imprese controllate» (1.04.03.01.001); la Regione ordinaria 32-67 M€ correnti e 485-742 M€ in conto capitale a controllate (non solo ARIA). Sono fuori dall'ICT SIOPE e non vanno sommati.

## 2. Fonti pubbliche su ARIA S.p.A.

- **Bilancio ARIA 2023** (nota integrativa) [V, documento archiviato; i numeri sono di ARIA]: valore della produzione 450,3 M€ (2022: 399,6). Ricavi «servizi resi alla controllante Regione Lombardia» **307,3 M€** (2022: 302,2). Le voci ICT sono: Piano delle attività di interesse regionale 155,7 (161,2), Data Center delle aziende sanitarie 17,5 (9,5), network provider 5,9 (6,0), piattaforma regionale d'integrazione 6,7 (5,9), colocation 2,6 (0), campagna vaccinale 0,7 (6,2). **Totale ICT circa 189 M€ in entrambi gli anni**. A parte: contact center 34,4, lavori pubblici 62,5, condomini 8,9. ARIA riceve inoltre un contributo di funzionamento di 51,3 M€, che copre anche l'attività di centrale di committenza (DGR XI/2690/2019), e 23,0 M€ di ricavi diretti dalle ASST.
- **Relazione sulla gestione 2023** [V, documento archiviato]: elenca le adesioni e le gare ICT bandite da ARIA per la Regione e per il SSR (CUP unico regionale, DGR XII/514/2023; cybersecurity degli enti sanitari, DGR XII/1224/2023; migrazione dei 39 data center delle ASST). ARIA è presentata come «società strumentale in house providing» con «affidamenti diretti e/o convenzioni».
- **Convenzione quadro Regione-ARIA 2023-2025**, allegata alla DGR XI/7409/2022 [R: copia ripubblicata da Farmindustria, non dal BURL]: le attività del piano pluriennale diventano **incarichi approvati con decreto della Direzione committente** (art. 4-6). Per l'ICT la rendicontazione è annuale, con validazione dei servizi (art. 6 c. 6 g).
- **Regione Lombardia, Amministrazione trasparente** [R, letta il 10/11; archiviazione non riuscita, vedi sotto]: «Dati sui pagamenti del servizio sanitario nazionale» (art. 41 c. 1-bis d.lgs. 33/2013) dice «Non ci sono documenti, informazioni o dati di competenza della Regione Lombardia da pubblicare». La GSA paga però 24-32 mld l'anno.
- **Parifica della Corte dei conti** e bilancio ARIA 2024: non trovati in questo giro.

## 3. ANAC [V]

- **CIG con SA = Regione Lombardia e aggiudicataria ARIA: zero nel 2020-2026.** ARIA ha CIG come aggiudicataria solo da altri enti: 132 nel 2024 (37,0 M€), 70 nel 2025 (5,2 M€), tolta la regex larga della 0.1.
- **CIG ICT con SA = ARIA** (solo CF 05017630152, strati S3-S6 dell'imbuto), per anno di pubblicazione: 2022 118 CIG / 455 M€; 2023 134 / 331; 2024 85 / 1.068; 2025 134 / 543; 2026 82 / 664. I più grandi: SIR, il sistema informativo regionale (B1031AADD9, B1031A8C33, B1031A6A8D: 363 M€, 2024); i sotto-perimetri A/B (B313D081DE, B313D092B1, B313D06038, B313D0710B: 358 M€, 2024); il cloud e l'outsourcing infrastrutturale (BAFE270F81, 580 M€, 2026, affidamento diretto); i servizi infrastrutturali del CUP regionale (B7DF25AC93, 77,8 M€, 2025); la gestione del capitale umano degli enti sanitari (B9A495C22E, 53,6 M€, 2025); l'adesione PSN (A02216FBF5, 52,4 M€, 2023); l'appalto specifico per la cartella clinica (933914496D, 48,4 M€, 2022).
- La 0.1 di `siope_inhouse_4enti.py` contava come «SA in-house» anche i CF di IM.I.S.C.A. e di un'onlus, perché la regex `\bARIA\b` era larga. Il suo `c_cig_sa_inhouse` per la Lombardia (es. 22 mld di ICT nel 2022) va quindi sostituito con i numeri qui sopra.

## 4. Lettura

- [V] La spesa ICT della GSA e della Regione è registrata in SIOPE come **acquisto di servizi** (1.03.02.19), non come trasferimento. Verso ARIA non c'è nessun CIG della Regione.
- [R, bilancio ARIA] ARIA fattura alla Regione circa 189 M€ l'anno di servizi ICT (2022 e 2023), più 34 di contact center, su **incarichi in-house** della convenzione quadro (DGR XI/7409/2022). Contro i 263-297 M€ di ICT SIOPE (Regione + GSA) restano 75-110 M€ verso altri beneficiari o per sfasamenti di cassa, non attribuibili senza il beneficiario. La ripartizione GSA/ordinaria degli incarichi ARIA non è nel bilancio.
- **Risposta alla domanda:** **entrambi i modelli, a due livelli**. La Regione (GSA tramite la DG Welfare) paga ARIA **come in-house**: incarichi per decreto, senza CIG fino al 2023 compreso e anche nel 2024-2025 [V]. ARIA poi compra sul mercato **come stazione appaltante propria** (CIG intestati ad ARIA: SIR, SISS e servizi sanitari, CUP, cloud), in parte anche come centrale di committenza per gli enti del SSR (adesioni e appalti specifici).
- **Nell'imbuto, senza doppi conteggi:** (a) i CIG con SA = ARIA restano la spesa di mercato (strati S3-S6) e si attribuiscono con il **collegamento ente-centrale** R (ARIA → Regione Lombardia CF 80050050154, comparto regione/sanità). (b) Il pagato SIOPE della Regione verso ARIA è lo **stesso denaro un livello più su**: nello strato R si confronta con la quota annua dei CIG ARIA «per la Regione» (acquisti propri, non le convenzioni usate dalle ASST, che hanno CIG derivati delle ASST), e non si somma mai. (c) Il margine ARIA (personale interno, circa 51 M€ di contributo) è spesa ICT senza CIG per definizione: va indicato come quota in-house, fuori dall'imbuto dei contratti.
- **Quota di copertura rivista** (indicativa): pagato ICT Regione + GSA 2022-2025 = 1,29 mld, contro 2,40 mld di CIG ICT ARIA pubblicati nello stesso periodo. Con il collegamento ARIA → Regione il rapporto non è più 0,03 ma è nell'ordine dei contratti/pagato tipico (1-2). È una stima: la quota annua dei CIG ARIA non è calcolata qui, e una parte dei CIG ARIA serve enti diversi dalla Regione.

## 5. Documenti da chiedere (accesso civico, fonte C)

1. Regione Lombardia, DG Welfare e Direzione Trasformazione digitale: decreti di incarico ad ARIA 2022-2025 per ICT e sanità digitale, con importo e capitolo; piano delle attività ARIA approvato ogni anno.
2. Regione Lombardia: mandati di pagamento della GSA (codice SIOPE 800000616) e della Regione sui codici 1.03.02.19.* e 2.02.03.02.* per beneficiario, 2022-2025. Il dato è obbligatorio (art. 4-bis e 41 c. 1-bis d.lgs. 33/2013) ma la pagina risulta vuota.
3. ARIA S.p.A.: bilanci 2024 e 2025 e ricavi per incarico e per direzione committente (GSA o ordinario).

## Fonti archiviate

| documento | URL | sha256 |
|---|---|---|
| ARIA, Bilancio al 31.12.2023 | www.trasparenza.ariaspa.it/wps/wcm/connect/017d3b8f-…/Bilancio+al+31.12.2023.pdf | 187211c3e8e6e8d1a796ab0d13372dfe36f9b1cbf4d825b466d24caa75257e13 |
| ARIA, Relazione sulla gestione 2023 | www.trasparenza.ariaspa.it/wps/wcm/connect/a88bafb6-…/Relazione+Gestione+Bilancio+al+31.12.2023.pdf | a6258a753c21b6292fa796132d26af99189a04f332f37bb5d888b57465862f33 |
| Convenzione Regione-ARIA 2023-2025 (all. DGR XI/7409/2022, copia Farmindustria) | www.farmindustria.it/app/uploads/2022/12/DGR-7409_2022-Allegato-convenzione-con-ARIA-2023-2025.pdf | b3fd4225e104d5315084c84ff75a611d35e41cc26ca6a2f4df58a99bff21898c |
| Regione Lombardia AT, pagamenti SSN e dati pagamenti | www.regione.lombardia.it/amministrazione-trasparente/pagamenti-dell-amministrazione/… | **non archiviate**: `archivia.py` fallisce con NotADirectoryError, perché nel mirror esiste già un file dove servirebbe una cartella (stesso difetto su trasparenza.ariaspa.it/wps/wcm/connect, aggirato con www.) |
