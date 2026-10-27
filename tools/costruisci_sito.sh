#!/usr/bin/env bash
# Costruisce il sito dal registro dei problemi e produce il PDF del documento per ANAC.
#   tools/costruisci_sito.sh          sito
#   tools/costruisci_sito.sh pdf      sito + PDF (serve Chrome o Chromium)
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p sito/data sito/static/pdf
cp report/anac/problemi.yaml sito/data/anac_problemi.yaml   # unica fonte per web, PDF e presentazione
hugo --source sito --minify --cleanDestinationDir
if [ "${1:-}" = "pdf" ]; then
  CHROME=${CHROME:-$(command -v chromium || command -v google-chrome || command -v chrome || echo "/c/Program Files/Google/Chrome/Application/chrome.exe")}
  PAGINA="$(pwd)/docs/rendiconti/anac-2026-10-problemi/index.html"
  command -v cygpath >/dev/null && PAGINA=$(cygpath -m "$PAGINA")
  OUT="$(pwd)/sito/static/pdf/anac-problemi-e-rimedi-2026-10.pdf"
  PROFILO=$(mktemp -d)
  command -v cygpath >/dev/null && OUT=$(cygpath -m "$OUT") && PROFILO=$(cygpath -m "$PROFILO")
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --user-data-dir="$PROFILO" --print-to-pdf="$OUT" "file:///${PAGINA#/}" 2>/dev/null
  hugo --source sito --minify --cleanDestinationDir   # ricostruisce per pubblicare anche il PDF
  echo "PDF: $OUT"
fi
