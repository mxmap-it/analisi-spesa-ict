#!/bin/bash
# Catena dopo lo scaricamento PVL (#57): attende la fine di pvl_avvisi.py scarica,
# poi estrai -> analisi -> verifica a campione dei link. Ripartibile: ogni passo
# rigenera i suoi file; la verifica salta i domini già fatti.
set -euo pipefail
cd "$(dirname "$0")/../.."
while pgrep -f "[p]vl_avvisi.py scarica" >/dev/null; do sleep 300; done
if grep -q '"discrepanza"' lavoro/pvl/stato.jsonl; then
  echo "$(date -u +%FT%TZ) giorni in discrepanza: ripresa"; nice -n 15 .venv/bin/python tools/acquisizione/pvl_avvisi.py scarica --da 2024-01-01 --a "${PVL_A:-$(date +%F)}"
fi
nice -n 15 .venv/bin/python tools/acquisizione/pvl_avvisi.py estrai > lavoro/pvl/link_cig.csv.part && mv lavoro/pvl/link_cig.csv.part lavoro/pvl/link_cig.csv
nice -n 15 .venv/bin/python tools/acquisizione/pvl_analisi.py --data "$(date +%F)"
nice -n 15 .venv/bin/python tools/acquisizione/pvl_verifica_link.py --top 300 --casuali 100
echo "$(date -u +%FT%TZ) catena PVL finita"
