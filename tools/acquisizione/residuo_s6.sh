#!/usr/bin/env bash
# Acquisizione dei documenti per il residuo S6 non coperto dalla via 6 (#57): L3 (link PVL, piattaforme_cig.py),
# MePA con browser reale (mepa_cig.py), L4 per i CIG senza link (at_cig.py). Ripartibile e idempotente: se gira già
# esce; ogni fase lascia FINITO.txt (o STOP-disco.txt sotto 15 GB liberi) e non riparte.
# Ripresa automatica, riga da far mettere a Fabio nel crontab:
#   */30 * * * * cd ~/analisi-spesa-ict && bash tools/acquisizione/residuo_s6.sh >/dev/null 2>&1
# Il ripasso notturno degli host AT esclusi da robots.txt è tools/acquisizione/residuo_s6_at.sh.
set -u
cd "$(dirname "$0")/../.."
D=lavoro/residuo-s6; mkdir -p $D
exec 9>$D/lock; flock -n 9 || exit 0
ls $D/*/STOP-disco.txt >/dev/null 2>&1 && exit 0
[ -f $D/ingresso.csv ] || SPESAICT_BASE=$PWD nice .venv/bin/python tools/acquisizione/residuo_s6_ingresso.py $D/ingresso.csv
[ -f $D/out/FINITO.txt ] || nice -n 15 .venv/bin/python tools/acquisizione/piattaforme_cig.py $D/ingresso.csv $D/out >> $D/giro.log 2>&1
[ -f $D/out/FINITO.txt ] || exit 0
pgrep -f "[m]epa_cig.py" >/dev/null || nice -n 15 .venv/bin/python tools/acquisizione/mepa_cig.py $D/out >> $D/mepa.log 2>&1
pgrep -f "[a]t_cig.py" >/dev/null || [ -f $D/l4/FINITO.txt ] || SPESAICT_BASE=$PWD nice -n 15 .venv/bin/python tools/acquisizione/at_cig.py $D/ingresso.csv $D/l4 >> $D/l4.log 2>&1
