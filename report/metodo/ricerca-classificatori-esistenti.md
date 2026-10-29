# Ricerca di classificatori e risorse esistenti riusabili (appalti ICT/cloud)

Data: 2026-10-29. Metodo: `gh api search/repositories`, lettura README/licenza/data ultimo push via API GitHub, API Hugging Face e Zenodo, due WebSearch. Legenda: **[V]** = verificato aprendo la risorsa; **[R]** = riferito (da risultati di ricerca o paper, non aperto). Non è stato contattato nessuno né aperto issue/PR.

## Executive summary

1. **Non esiste (trovato) un classificatore pubblico "appalto -> ICT/cloud -> prodotto/giurisdizione" per l'Italia.** Nessun repo cerca "spesa ICT PA" né normalizza fornitori cloud con giurisdizione. L'imbuto e la tassonomia prodotto/giurisdizione restano originali; le risorse esistenti coprono solo i pezzi a monte (CPV da testo, dati ANAC, fornitori).
2. **Risorsa più utile: dataset Zenodo 10007545** [V], 5M coppie (descrizione italiana ANAC -> CPV), CC-BY-4.0, già diviso train/dev/test. Permette di addestrare un classificatore testo->divisione CPV e, soprattutto, di costruire un **vocabolario di esclusione basato sui dati** (n-grammi che compaiono quasi solo in divisioni non ICT).
3. **Modello pronto: `sinceaihq/eurotender-cpv-baseline`** [V] (Apache-2.0, TF-IDF lineare su CPU, 22 lingue incl. italiano; dichiarato top-1 82,1% sulle 45 divisioni, top-5 94,2% [R: numeri degli autori]; dataset CC-BY-4.0). Utile come voto indipendente, non come verità. Addestrato su TED, da validare su campione ANAC.
4. **Avvertenza fondamentale sulle etichette:** il CPV nei dati ANAC è assegnato dalle stazioni appaltanti ed è spesso generico o sbagliato; i modelli predicono il CPV *dichiarato*. Il disaccordo testo-vs-CPV è esso stesso un segnale (incerto -> lavoro a fondo). Per ESCLUDERE con certezza serve l'accordo di più segnali indipendenti (CPV non-ICT + testo non-ICT + nessun termine ICT).
5. **Fornitori:** nessun catalogo SaaS/cloud con alias e giurisdizione trovato come progetto aperto riusabile. Utili solo ISO 20275 ELF / GLEIF per forme giuridiche e paese; il resto è da costruire (lista curata nostra).
6. **Licenze:** i repo accademici più noti sul CPV (oeg-upm, nextprocurement) **non hanno licenza sul codice** [V] -> codice non riusabile; i *dati* Zenodo Spagna (6554604) sono CC-BY-4.0 [V].

## Tabella ordinata per utilità

| # | Progetto | Uso per noi | Licenza | Ultimo push | Verifica |
|---|---|---|---|---|---|
| 1 | Zenodo 10007545 "Automatic Generation of CPV Codes" (Siciliani et al., CLiC-it 2023) https://zenodo.org/records/10007545 | ADDESTRARE + ESCLUDERE: 5M descrizioni IT ANAC->CPV; lessico per divisione | CC-BY-4.0 | 2023-10 | V (metadati; cpv_5M.csv.gz 307 MB, train/dev/test json) |
| 2 | sinceaihq/eurotender + HF model e dataset https://github.com/sinceaihq/eurotender | Segnale: divisione CPV da testo, CPU, multilingue | Apache-2.0 (codice, modello), CC-BY-4.0 (dati) | 2026-10-19 | V (README, HF API); accuratezze R |
| 3 | HARISPAARTAN/anac-appalti-dbt https://github.com/HARISPAARTAN/anac-appalti-dbt | Ingest: CKAN ANAC -> Parquet, dbt+DuckDB, dim_cpv, nomi divisioni CPV, anagrafica aggiudicatari | MIT (dati derivati CC BY-SA 4.0) | 2026-10-25 | V README; non eseguito |
| 4 | nschevokin/appalti-observatory https://github.com/nschevokin/appalti-observatory | Idee: risoluzione entità su 562k gare >40k EUR OCDS ANAC, gate di qualità | NOASSERTION (non riusabile finché non chiarita) | 2026-10-19 | V README |
| 5 | open-contracting/cardinal-rs | Indicatori/red flags OCDS (non classifica ICT) | MIT | 2026-10-28 | V |
| 6 | open-contracting/kingfisher-collect, pelican-backend | Raccolta OCDS e controlli qualità | BSD-3-Clause | 2026-10-28 | V |
| 7 | MKaan/multilingual-cpv-sector-classifier (HF) | Alternativa mBERT 45 classi (F1 0,686 R) | Apache-2.0 | n/d | licenza V |
| 8 | DmitryMatv/classifast | Ricerca semantica UNSPSC/NAICS/CPV con mappature; ponte CPV<->UNSPSC | MIT | 2026-10-25 | V |
| 9 | Reg-Data/open-legal-forms; GLEIF (ISO 20275 ELF) | Forme giuridiche/paese dei fornitori | repo NOASSERTION; GLEIF CC0 [R] | 2026-08 | solo ricerca |
| 10 | ColinMaudry/decp-processing (Francia) | Pattern di arricchimento titolari | NOASSERTION | 2026-10-28 | V README |
| 11 | acourreg/spendlabel (UK, regole/ML/LLM) | Confronto metodi | senza licenza: non riusabile | 2026-06 | V |
| 12 | VaidehiTawde16/llm-spend-categorizer | Idea "regole prima, LLM sul residuo" (= nostro imbuto) | senza licenza: solo idea | 2026-06 | V |
| 13 | oeg-upm/cpv-classifier = nextprocurement/CPV-Classifier + Zenodo 6554604 | Confronti SVM/RoBERTa su PLACSP; dati ES | **codice senza licenza**; dati CC-BY-4.0 | 2022/2025 | V |
| 14 | alanbuxton/tbfy-cpv-classifier-poc | Solo benchmark (SVM 63%, DistilBERT 78%) | NOASSERTION | 2022 | V |
| 15 | tiktak6828/ProjectAI | Nulla di riusabile | senza licenza | 2026-02 | V |
| 16 | giacomogazzellone/anac_opendata_extractor (MIT), DavideFornari/openspesa (AGPL-3.0), GabriPaganelli/anac-pu-learning, SimonBerg255/anac-mcp, pipeworx-io/mcp-italy-tenders | Ecosistema ANAC: estrazione, link CIG-CUP; non classificano ICT | vari | 2026 | solo metadati |
| 17 | Extension OCDS tenderClassification / organizationClassification | Schema per allegare le nostre classificazioni | Apache-2.0 | 2026-09 | V |

Tesi PoliTo 2022 sulla classificazione gerarchica degli oggetti dei contratti pubblici italiani (https://webthesis.biblio.polito.it/22580/) [R, non aperta].

## Non trovato (ricerche GitHub con 0 risultati pertinenti)

- Spesa ICT PA, cloud/SaaS in gare, Cruscotto AgID, Team Digitale, openpolis/ondata/DataCivicLab su classificazione ICT. Non si esclude che esistano fuori dagli indici.
- Tassonomia aperta prodotti software/cloud con alias e giurisdizione.
- Dataset etichettato ICT/non-ICT esplicito (solo CPV dichiarato).
- USAspending PSC/NAICS, Contracts Finder UK: nessun classificatore ICT riusabile (spendlabel senza licenza).

## Come usarli (priorità)

**P1 - subito**
- Scaricare Zenodo 10007545 (attribuire, CC-BY-4.0). Per n-gramma/lemma calcolare la distribuzione per divisione CPV: (a) termini quasi mai ICT -> regole di esclusione ad alta precisione; (b) termini ICT ad alta precisione -> inclusione; (c) set di validazione per `classifica.py`.
- Eseguire EuroTender sui nostri oggetti e confrontare con le regole: i disaccordi vanno a "incerto". Solo come voto.

**P2 - presto**
- Addestrare TF-IDF + lineare sul 5M per predire la divisione CPV dall'oggetto; auditare i CIG con CPV generico/errato.
- Riusare da anac-appalti-dbt il flusso CKAN->Parquet e dim_cpv.
- Fornitori: ISO 20275/GLEIF per forme giuridiche e paese; alias prodotti e giurisdizione = lista curata da noi.

**P3 - poi**
- cardinal-rs/pelican per qualità dati; classifast per il ponte CPV<->UNSPSC.

## Cautele

- Etichette = CPV dichiarato dalle SA: rumore alto, entra nei modelli. Mai un modello CPV come verità per escludere.
- TED è diverso per registro e lunghezza dai CIG ANAC: misurare su un campione nostro etichettato a mano.
- Accuratezze citate = riferite dagli autori, non rimisurate.
- Repo senza licenza (oeg-upm, nextprocurement, spendlabel, llm-spend-categorizer, ProjectAI): non copiare codice; le idee si possono riscrivere.
