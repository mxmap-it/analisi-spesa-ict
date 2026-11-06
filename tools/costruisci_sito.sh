#!/usr/bin/env bash
# Costruisce il sito dal registro dei problemi e produce il PDF del documento per ANAC.
#   tools/costruisci_sito.sh          sito
#   tools/costruisci_sito.sh pdf      sito + PDF (serve pip install typst)
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p sito/data sito/static/pdf
cp report/anac/problemi.yaml sito/data/anac_problemi.yaml   # unica fonte per web, PDF e presentazione
python3 tools/pagina_scheda_normativa.py 2>/dev/null || PYTHONUTF8=1 /c/Users/admin/AppData/Local/Python/bin/python.exe tools/pagina_scheda_normativa.py
python3 tools/convenzioni/pagine.py 2>/dev/null || PYTHONUTF8=1 /c/Users/admin/AppData/Local/Python/bin/python.exe tools/convenzioni/pagine.py   # sezione /convenzioni/ (#62)
hugo --source sito --minify --cleanDestinationDir
if [ "${1:-}" = "pdf" ]; then
  # impaginazione dedicata con typst dal registro (#34), non la stampa del sito
  python3 tools/documento_anac/genera.py 2>/dev/null || PYTHONUTF8=1 /c/Users/admin/AppData/Local/Python/bin/python.exe tools/documento_anac/genera.py
  hugo --source sito --minify --cleanDestinationDir
fi
