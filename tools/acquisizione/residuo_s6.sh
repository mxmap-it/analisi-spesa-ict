#!/usr/bin/env bash
# Acquisizione L3 del residuo S6 non coperto dalla via 6 (#57). Ripartibile e idempotente: se gira già esce;
# se c'è FINITO.txt o STOP-disco.txt non riparte. Per la ripresa automatica (riga da far mettere a Fabio nel crontab):
#   */30 * * * * cd ~/analisi-spesa-ict && bash tools/acquisizione/residuo_s6.sh >/dev/null 2>&1
set -u
cd "$(dirname "$0")/../.."
D=lavoro/residuo-s6; mkdir -p $D
[ -f $D/FINITO.txt ] || [ -f $D/STOP-disco.txt ] && exit 0
exec 9>$D/lock; flock -n 9 || exit 0
[ -f $D/ingresso.csv ] || SPESAICT_BASE=$PWD nice .venv/bin/python tools/acquisizione/residuo_s6_ingresso.py $D/ingresso.csv
nice -n 15 .venv/bin/python tools/acquisizione/piattaforme_cig.py $D/ingresso.csv $D/out >> $D/giro.log 2>&1
