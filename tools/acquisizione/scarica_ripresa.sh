#!/bin/bash
# File grandi che il server interrompe a metà (Consip: tagli a circa 330-380 MB, #11): curl con ripresa (-C -) fino alla
# dimensione dichiarata, poi tools/archivia.py --da-file (sha256, blob, vista, manifest). Guardia disco GUARDIA_GB (45).
#   tools/acquisizione/scarica_ripresa.sh LISTA_URL CARTELLA_LAVORO
cd "$(dirname "$0")/../.." || exit 1
LISTA=$1; D=$2; G=${GUARDIA_GB:-45}; mkdir -p "$D"
UA="Mozilla/5.0 (X11; Linux x86_64) Chrome/130 analisi-spesa-ict (+https://analisi-spesa-ict.mxmap.it)"
grep -v '^\s*\(#\|$\)' "$LISTA" | while read -r u; do
  libero=$(df --output=avail -BG . | tail -1 | tr -dc 0-9); [ "$libero" -lt "$G" ] && { echo "STOP disco ${libero}G"; exit 3; }
  f="$D/$(basename "${u%%\?*}")"
  atteso=$(curl -sI -A "$UA" "$u" | tr -d '\r' | awk -F': ' 'tolower($1)=="content-length"{print $2}')
  for i in $(seq 1 20); do
    nice -n 15 curl -s -C - -o "$f" -A "$UA" "$u"
    [ -n "$atteso" ] && [ "$(stat -c%s "$f" 2>/dev/null || echo 0)" -ge "$atteso" ] && break; sleep 10
  done
  if [ -n "$atteso" ] && [ "$(stat -c%s "$f")" -eq "$atteso" ]; then
    nice -n 15 .venv/bin/python tools/archivia.py --da-file "$f" --url "$u" --data "$(date -u +%FT%TZ)" --nota "curl con ripresa: il server interrompe i file grandi (#11)" && rm -f "$f"
    echo "archiviato $u"
  else echo "incompleto $u $(stat -c%s "$f") / $atteso"; fi
done
echo FATTO
