#!/usr/bin/env bash
# Seconda lettura della revisione via 6 (#55 #66): ripartibile; con il tetto condiviso raggiunto (codice 75)
# attende 30 minuti e riprova; a fine lettura riscrive l'esito del giorno. Avvio: nohup setsid tools/llm/giro_revisione_guardiano.sh &
cd "$(dirname "$0")/../.."
mkdir -p lavoro/imbuto-revisione/log
while :; do
  nice -n 15 .venv/bin/python tools/verifiche/imbuto_via6_revisione.py leggi >> lavoro/imbuto-revisione/log/guardiano.log 2>&1
  c=$?
  echo "$(date -Is) leggi codice=$c" >> lavoro/imbuto-revisione/log/guardiano.log
  [ $c -eq 75 ] && { sleep 1800; continue; }
  nice -n 15 .venv/bin/python tools/verifiche/imbuto_via6_revisione.py esito "$(date +%F)" >> lavoro/imbuto-revisione/log/guardiano.log 2>&1
  break
done
