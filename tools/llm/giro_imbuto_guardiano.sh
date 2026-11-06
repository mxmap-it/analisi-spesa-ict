#!/usr/bin/env bash
# Cron ogni 30 minuti: rilancia giro_imbuto.sh se non gira, mancano esiti e non c'è lo STOP; poi verifica e sincronizza.
cd "$(dirname "$0")/../.." || exit 1
# a ogni passaggio: verifica a regole e numeri aggiornati (versionati da sync_server.sh)
.venv/bin/python tools/llm/verifica_imbuto.py >/dev/null 2>&1 && .venv/bin/python tools/verifiche/imbuto_via6.py --json esiti/imbuto-via6/via6-g1g3.json >/dev/null 2>&1
S=; [ -f stato/imbuto-g1g3-STOP.txt ] && S=1
pgrep -f "[t]ools/llm/giro_imbuto.sh" >/dev/null && exit 0
B=report/metodo/llm/imbuto-g1g3
manca=$(for f in $B/lotti/*.jsonl; do [ -n "$S" ] && case $(basename "$f") in g3-*) continue;; esac; e=$B/esiti/$(basename "$f"); [ -f "$e" ] && [ "$(grep -c . "$e")" -ge "$(grep -c . "$f")" ] || echo x; done | wc -l)
[ "$manca" -eq 0 ] && exit 0
echo "$(date -Is) guardiano: $manca pacchetti da fare, rilancio" >> log/imbuto-g1g3/avanzamento.log
setsid nohup bash -c 'tools/llm/giro_imbuto.sh; .venv/bin/python tools/llm/verifica_imbuto.py; bash tools/sync_server.sh' >> log/imbuto-g1g3/esecuzione.log 2>&1 < /dev/null &
