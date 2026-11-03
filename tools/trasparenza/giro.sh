#!/bin/bash
# Giro mensile completo, ripartibile: rilanciarlo riprende dagli enti mancanti.
#   tools/trasparenza/giro.sh [AAAA-MM]
set -u
cd "$(dirname "$0")/../.."
RUN="${1:-$(date +%Y-%m)}"
PY=.venv/bin/python
T=tools/trasparenza/censimento.py
echo "$(date -u +%FT%TZ) inizio giro $RUN"
nice -n 10 $PY $T fonti || exit 1
nice -n 10 $PY $T sonda --run "$RUN" --paralleli 24 || exit 1
nice -n 10 $PY $T browser --run "$RUN" || echo "seconda prova con browser non riuscita (si prosegue)"
nice -n 10 $PY $T esporta --run "$RUN" || exit 1
echo "$(date -u +%FT%TZ) fine giro $RUN"
