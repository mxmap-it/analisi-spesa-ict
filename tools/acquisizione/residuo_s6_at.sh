#!/usr/bin/env bash
# Ripasso notturno degli host «Amministrazione trasparente» esclusi da robots.txt (config/at_robots_esenti.txt,
# AGENTS.md §3, art. 9 d.lgs. 33/2013): aspetta le 21, poi rifà i CIG con ultimo esito «robots» su quegli host.
# robots.txt archiviato come evidenza (campo robots_escluso_at). Ripartibile: rilanciarlo rifà solo ciò che manca.
set -u
cd "$(dirname "$0")/../.."
D=lavoro/residuo-s6
exec 8>$D/lock-at; flock -n 8 || exit 0
while h=$(date +%-H); [ "$h" -ge 7 ] && [ "$h" -lt 21 ]; do sleep 600; done
RIPASSA=robots FINE_FILE=FINITO-at.txt nice -n 15 .venv/bin/python tools/acquisizione/piattaforme_cig.py $D/ingresso.csv $D/out >> $D/giro-at.log 2>&1
