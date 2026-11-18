#!/usr/bin/env bash
# Catena del raffinamento a livelli (#71, decisione di Fabio 18/11/2026): L3 (Opus, testo) su G3 e poi G4, quindi L4
# (via 6 con Opus e atti) su ciò che L3 lascia incerto o dice cloud. Ripartibile: ogni passo salta il già fatto;
# con il tetto condiviso raggiunto (codice 75) attende 30 minuti e riprova. Avvio: nohup setsid tools/llm/raffinamento_catena.sh &
cd "$(dirname "$0")/../.." || exit 1
P=".venv/bin/python tools/llm/raffinamento.py"
leggi() { while :; do nice -n 15 $P leggi-l3; c=$?; echo "$(date -Is) leggi-l3 codice=$c"; [ $c -eq 75 ] && { sleep 1800; continue; }; break; done; }
D=$(date +%F)
while pgrep -f "[r]affinamento.py leggi-l3" >/dev/null; do sleep 60; done   # un solo lettore alla volta
leggi; $P esito "$D"
$P prepara-l3 G4; leggi; $P esito "$D"
$P prepara-l4 "$D"
GIRO_DIR=report/metodo/llm/raffinamento-l4 GIRO_LOG=log/raffinamento-l4 MODELLO=opus PAR=2 bash tools/llm/giro_imbuto.sh
echo "$(date -Is) catena finita"
