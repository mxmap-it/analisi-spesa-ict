#!/usr/bin/env bash
# Ricerca mirata degli atti per i CIG via 6 fermi a C1 (#55 #66): L3 link PVL, L2 avvisi TED, L4 sezioni AT.
# Riusa piattaforme_cig.py e at_cig.py; un solo job pesante (AGENTS §4): at_cig parte quando nessun altro at_cig gira.
# Ripartibile: ogni passo salta i CIG/enti già fatti.
set -u
cd "$(dirname "$0")/../.."
D=lavoro/c1-mirata
exec 8>$D/lock; flock -n 8 || exit 0
nice -n 15 .venv/bin/python tools/acquisizione/piattaforme_cig.py $D/ingresso.csv $D/l3 >> $D/l3.log 2>&1
# L2: il link ai documenti dell avviso TED (eForms) passato come link alla stessa ricerca
.venv/bin/python - <<PY
import csv
r=[x for x in csv.DictReader(open("$D/ingresso.csv",encoding="utf-8")) if x["link_ted"]]
for x in r: x["link"]=x["link_ted"]
w=csv.DictWriter(open("$D/ingresso-ted.csv","w",encoding="utf-8",newline=""),fieldnames=list(r[0].keys()) if r else ["cig","link"]); w.writeheader(); w.writerows(r)
PY
nice -n 15 .venv/bin/python tools/acquisizione/piattaforme_cig.py $D/ingresso-ted.csv $D/l2-ted >> $D/l2-ted.log 2>&1
while pgrep -f "[a]t_cig.py lavoro/residuo" >/dev/null; do sleep 60; done
SPESAICT_BASE=$PWD nice -n 15 .venv/bin/python tools/acquisizione/at_cig.py $D/ingresso.csv $D/l4 >> $D/l4.log 2>&1
date -u +%FT%TZ > $D/FINITO.txt
