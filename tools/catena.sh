#!/bin/bash
# Attende la fine del censimento, poi avvia il mirror. Entrambi ripartibili.
cd ~/analisi-spesa-ict
until ! pgrep -f censisci_anac.py >/dev/null; do sleep 30; done
echo "censimento finito $(date -Is), avvio mirror"
exec .venv/bin/python tools/mirror_anac.py
