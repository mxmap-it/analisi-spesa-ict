# Via 6, giro imbuto G1/G3 — istruzioni p3 (7/11/2026, #55 #66)

Valgono campi e definizioni di `istruzioni.md` (p1) e il metodo di ricerca di `istruzioni-p2.md` (p2, compresa l'aggiunta p2.1).
Leggi prima `report/metodo/llm/conoscenza-iniziative.yaml`. Cambia l'uscita: **due assi distinti, ciascuno con il suo stato**.

## Contesto

I contratti di questo giro sono nel residuo S6 dell'imbuto: le regole v3.1 non li chiudono. Gruppo G1 «mega» (≥ 5 M€, uno o due per
pacchetto: guardali uno per uno, con la massima cura) e G3 «incerti rilevanti» (≥ 40 k€, i primi 1.000 per importo).
Sottoclasse `cpv-non-ict-testo-ict`: CPV non ICT ma testo con parole ICT (spesso falsi positivi: lavori, sanità, «rete» idrica…).
Sottoclasse `cloud-provider-indeterminato`: c'è un indizio di cloud ma non il provider.

## Ordine di lavoro (fermati appena entrambi gli assi sono certi)

1. Leggi oggetto, CPV, ente, aggiudicatari, importo. Se l'oggetto basta a **escludere con certezza** (es. lavori stradali, farmaci,
   servizi di pulizia) chiudi l'asse A come `escluso-certo` senza ricerche: la certezza qui viene dal testo stesso.
2. Se c'è `link_documenti` (link ai documenti di gara dall'API PVL di ANAC): aprilo **per primo** con
   `.venv/bin/python tools/llm/atti.py <CIG> <URL> --livello L2 --metodo "link PVL" --tipo altro --ente "<ente>"`;
   nella pagina cerca determina, capitolato, contratto e aprili con atti.py (anche PDF).
3. Poi il metodo p2: ricerca web del CIG tra virgolette, Amministrazione trasparente / albo dell'ente, schede prodotto, convenzioni.
   Massimo ~8 chiamate per contratto (G1: fino a ~12).
4. Non aggirare WAF, CAPTCHA, login; non contattare nessuno. Ogni blocco va in `ostacoli`.

## Uscita: una riga JSON per contratto, su UNA riga

```
{"cig": "...", "gruppo": "G1|G3|CTL",
 "asse_a": {"stato": "escluso-certo|incluso-certo|incerto", "e_cloud": "s|n|?", "servizio": "<vocabolario p1 + connettivita, hardware, lavori-non-ict, sanitario-non-ict>", "ict": "s|n|?"},
 "asse_b": {"stato": "incluso-certo|incerto|non-applicabile", "provider_prodotto": "...", "giurisdizione": "IT|UE|EXTRA-UE|ignota|non-determinabile"},
 "confidenza": "alta|media|bassa", "fonte_primaria": true|false, "atto_ente": "URL o \"\"", "fonti": ["URL aperti"],
 "ricerche": N, "passaggi": [{"tipo": "ricerca|pagina|documento|deduzione", "query_o_url": "...", "risultato": "1 frase"}],
 "ostacoli": [{"url": "...", "tipo": "403|captcha|login|404|link-pvl-rotto|pdf-illeggibile|altro", "nota": "..."}],
 "motivazione": "1-3 frasi", "versione_istruzioni": "p3", "modello": "...", "data": "AAAA-MM-GG"}
```

Regole degli stati (il codice le ricontrolla con `tools/llm/verifica_imbuto.py`; uno stato certo senza prova diventa `incerto`):

- **asse A `escluso-certo`**: non è cloud né infrastruttura IT. Basta l'oggetto se è univoco (lavori, beni non ICT), altrimenti un documento aperto.
- **asse A `incluso-certo`**: è cloud (SaaS/IaaS/PaaS/hosting/PSN/centralino ospitato) provato da un documento aperto o dall'oggetto che nomina un servizio cloud univoco.
- **asse B**: `non-applicabile` se l'asse A è `escluso-certo` o non è cloud; `incluso-certo` solo se il **provider del prodotto** (non il rivenditore)
  è provato da un documento aperto o nominato in modo univoco nell'oggetto; giurisdizione = sede della capogruppo che controlla il provider del prodotto.
- Tutto il resto è `incerto`. Distingui sempre ciò che hai verificato in una fonte da ciò che deduci (`passaggi` di tipo `deduzione`).
