#!/usr/bin/env bash
# Cron ogni 30 minuti (#71): rilancia il livello L4 del raffinamento (Opus con gli atti) se non gira e mancano esiti.
# Il tetto (claude_tetto.py, codice 75) ferma i pacchetti; qui si riparte quando la finestra di 24 h si libera.
cd "$(dirname "$0")/../.." || exit 1
B=report/metodo/llm/raffinamento-l4; L=log/raffinamento-l4
# lucchetto: il giro eredita il descrittore 9 e lo tiene finché gira
exec 9>lavoro/raffinamento/l4.lock; flock -n 9 || exit 0
manca=$(for f in $B/lotti/*.jsonl; do e=$B/esiti/$(basename "$f"); [ -f "$e" ] && [ "$(grep -c . "$e")" -ge "$(grep -c . "$f")" ] || echo x; done | wc -l)
[ "$manca" -eq 0 ] && exit 0
echo "$(date -Is) guardiano: $manca pacchetti L4 da fare, rilancio" >> $L/avanzamento.log
setsid nohup env GIRO_DIR=$B GIRO_LOG=$L MODELLO=opus PAR=2 bash tools/llm/giro_imbuto.sh >> $L/esecuzione.log 2>&1 < /dev/null &
