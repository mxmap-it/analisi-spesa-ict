#!/bin/bash
# Giro completo (metodo 1.1.0-beta), ripartibile: rilanciarlo riprende dal punto in cui si era fermato.
#   tools/trasparenza/giro.sh [AAAA-MM]
# Passi: fonti -> indice CIG -> sonda (tutti) -> diagnosi giro 1 (dubbi, 5 identità + browser reale)
#        -> caratterizzazione (campione: due vie + ricerca per CIG) -> diagnosi giro 2 (>= 60 min dopo: conferma)
#        -> esporta (open data, indici, storico, cambiamenti).
# Il punto di osservazione desktop si aggiunge a parte (README, «Origine desktop») e poi si riesporta.
set -u
cd "$(dirname "$0")/../.."
RUN="${1:-$(date +%Y-%m)}"
PY=.venv/bin/python
T=tools/trasparenza/censimento.py
CAMPIONE_CARATTERI="${CAMPIONE_CARATTERI:-300}"
echo "$(date -u +%FT%TZ) inizio giro $RUN"
nice -n 10 $PY $T fonti || exit 1
nice -n 10 $PY $T indice-cig || echo "indice CIG non aggiornato (si prosegue con il precedente)"
nice -n 10 $PY $T sonda --run "$RUN" --paralleli 24 || exit 1
until nice -n 10 $PY $T diagnosi --run "$RUN" --giro-conferma 1 --paralleli 24 --max-per-host 25; do [ $? -eq 3 ] || exit 1; done
nice -n 10 $PY $T caratterizza --run "$RUN" --campione "$CAMPIONE_CARATTERI" || echo "caratterizzazione incompleta (si prosegue)"
# giro di conferma: ripete finché tutti i dubbi hanno il secondo passaggio a >= 60 minuti dal primo
for i in $(seq 1 30); do
  OUT=$(nice -n 10 $PY $T diagnosi --run "$RUN" --giro-conferma 2 --paralleli 24 --max-per-host 25 2>&1 | tee -a /dev/stderr)  # codice 3 = ente saltato: il ciclo rilancia
  echo "$OUT" | grep -q "in attesa della distanza: 0)" && break
  sleep 600
done
nice -n 10 $PY $T esporta --run "$RUN" || exit 1
echo "$(date -u +%FT%TZ) fine giro $RUN"
