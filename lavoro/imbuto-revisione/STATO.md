# Revisione delle proposte via 6 (#55 #66) — stato ripartibile

Aggiornato: 2026-11-09 12:15 CET.

## Cosa
Revisione indipendente delle 176 proposte via 6 di passaggio a «certo» (S5 161, cloud certo 15; S1 escluso),
criteri C1-C4 in `tools/verifiche/imbuto_via6_revisione.py` (docstring). Seconda lettura cieca: Claude Opus,
`report/metodo/llm/imbuto-revisione/istruzioni-revisione.md`, solo estratti degli atti archiviati, etichetta consumi «imbuto-revisione».

## Fatto
- `prepara`: 30 pacchetti ciechi da 6 CIG (importo decrescente) in `lavoro/imbuto-revisione/pacchetti/` (rigenerabili, deterministici).
- `esito 2026-11-09` con 0 letture: C1/C2/C3 calcolati; `esiti/2026-11-09/imbuto/revisione-via6.json`, `revisione-per-66.md`, coda vuota.

## Dove si è fermato
- Tetto giornaliero condiviso raggiunto alle 12:07 CET (24 h: 104/100 USD-eq, tutto giro imbuto-g3 dell 8/11): NESSUNA lettura fatta.
- Il tetto scende sotto 90 verso le 14:30 CET del 9/11.
- Avviato `tools/llm/giro_revisione_guardiano.sh` (nohup setsid, PID nel `pgrep -af giro_revisione`): riprova ogni 30 min,
  legge i pacchetti mancanti, a fine giro riscrive `esito $(date +%F)`. Log: `lavoro/imbuto-revisione/log/guardiano.log`.

## Per riprendere
1. `pgrep -af giro_revisione` — se non gira: `nohup setsid tools/llm/giro_revisione_guardiano.sh >/dev/null 2>&1 &`
2. avanzamento: `ls report/metodo/llm/imbuto-revisione/esiti/ | wc -l` (30 = finito); pacchetti con 2 tentativi incompleti: `lavoro/imbuto-revisione/log/*.tentativi`
3. a fine giro: `python tools/verifiche/imbuto_via6_revisione.py esito <data>`, commit di esiti/<data>/imbuto/revisione-*, report/metodo/llm/imbuto-revisione/esiti, dati/classificazioni/imbuto-revisione.jsonl; commento su #55 e #66 coi numeri.
4. se il giro G3 aggiunge proposte: rieseguire `prepara` (i pacchetti cambiano: ripartire con esiti vuoti o tenere quelli fatti, i CIG sono la chiave).
