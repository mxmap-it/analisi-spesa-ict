#!/bin/bash
# Coda di mirror (#12 #13 #25 #26 #28 #29): un URL per riga (righe vuote e # ignorate), ognuno con tools/archivia.py.
# Guardia disco: si ferma sotto GUARDIA_GB (default 45) liberi. Ripartibile: archivia.py non riscarica ciò che non è cambiato.
#   tools/acquisizione/coda_mirror.sh LISTA [LOG]
cd "$(dirname "$0")/../.." || exit 1
LISTA=$1; G=${GUARDIA_GB:-45}
grep -v '^\s*\(#\|$\)' "$LISTA" | while read -r u; do
  libero=$(df --output=avail -BG . | tail -1 | tr -dc 0-9)
  if [ "$libero" -lt "$G" ]; then echo "STOP disco ${libero}G < ${G}G prima di $u"; exit 3; fi
  nice -n 15 .venv/bin/python tools/archivia.py "$u"; sleep 3
done
echo FATTO
