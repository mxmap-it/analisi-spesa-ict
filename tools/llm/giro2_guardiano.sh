#!/usr/bin/env bash
# Cron ogni 30 minuti: se il giro 2 non è in corso e mancano esiti, lo rilancia (ripartibile, salta i pacchetti completi).
cd "$(dirname "$0")/../.." || exit 1
pgrep -f "[t]ools/llm/giro2.sh" >/dev/null && exit 0
fatti=$(for f in report/metodo/llm/giro2/lotti/*.jsonl; do p=$(basename "$f"); e=report/metodo/llm/giro2/esiti/$p; [ -f "$e" ] && [ "$(grep -c . "$e")" -ge "$(grep -c . "$f")" ] && echo x; done | wc -l)
tot=$(ls report/metodo/llm/giro2/lotti/*.jsonl | wc -l)
[ "$fatti" -ge "$tot" ] && exit 0
echo "$(date -Is) guardiano: $fatti/$tot pacchetti, rilancio" >> log/giro2/avanzamento.log
MODELLO=sonnet PAR=4 setsid nohup bash -c 'tools/llm/giro2.sh; .venv/bin/python tools/llm/verifica_esiti.py; bash tools/sync_server.sh' >> log/giro2/esecuzione-sonnet.log 2>&1 < /dev/null &
