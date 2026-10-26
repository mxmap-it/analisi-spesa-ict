#!/bin/bash
# Riavvia il mirror se non e in esecuzione e non ha finito. Pensato per cron.
cd ~/analisi-spesa-ict || exit 0
# conta i processi python che eseguono il mirror, senza auto-colpirsi
n=$(ps -eo args | grep -c '[t]ools/mirror_anac.py')
[ "$n" -gt 0 ] && exit 0
# finito? l'ultima riga del log lo dice
tail -3 log/mirror-anac.log 2>/dev/null | grep -qE 'scaricati .* GB in questa sessione' && exit 0
echo "$(date -Is) riavvio il mirror" >> log/guardiano.log
setsid nohup ./tools/avvia.sh tools/mirror_anac.py >> log/mirror-anac.log 2>&1 < /dev/null &
