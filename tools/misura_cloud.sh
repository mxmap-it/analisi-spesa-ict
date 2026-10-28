#!/usr/bin/env bash
# Riproduce da zero la misura della spesa in servizi cloud (attribuzione del provider). Istruzioni: RIPRODURRE.md
# Prerequisito: i file ANAC scaricati e verificati con tools/verifica_anac.sh ambiente | scarica | snapshot
#
#   tools/misura_cloud.sh test          casi di riferimento del classificatore (tests/casi_classifica.yaml)
#   tools/misura_cloud.sh attribuisci   attribuisce provider, giurisdizione, tipo e canale a ogni contratto ICT 2024, 2025, 2026
#   tools/misura_cloud.sh rivenditori   mappa dei rivenditori dei prodotti cloud, PSN compreso
#   tools/misura_cloud.sh campione      ri-estrae il campione di misura (seme fisso: stesso campione se i dati sono gli stessi)
#   tools/misura_cloud.sh misura A.csv [B.csv]   precisione e accordo sulle annotazioni alla cieca
#   tools/misura_cloud.sh confronta     confronta i numeri con quelli pubblicati in report/metodo/
#   tools/misura_cloud.sh tutto         test + attribuisci + rivenditori + campione + confronta
set -euo pipefail
cd "$(dirname "$0")/.."
PY=.venv/bin/python
OGGI=$(date +%F)
ESITI=esiti/$OGGI/cloud
mkdir -p "$ESITI"

test_()       { "$PY" tests/test_classifica.py; }
attribuisci() { nice -n 10 "$PY" tools/analisi/attribuisci_provider.py 2024 2025 delta >/dev/null && cp lavoro/attribuzione/riepilogo.json "$ESITI/attribuzione-riepilogo.json"; echo "esito: $ESITI/attribuzione-riepilogo.json"; }
rivenditori() { nice -n 10 "$PY" tools/analisi/rivenditori.py >/dev/null && cp lavoro/attribuzione/rivenditori.json "$ESITI/rivenditori.json"; echo "esito: $ESITI/rivenditori.json"; }
campione()    { "$PY" tools/analisi/campione_riferimento.py 700 20261028 campione-misura-v3 && cp lavoro/attribuzione/campione-misura-v3*.csv "$ESITI/"; }
misura()      { "$PY" tools/analisi/misura_campione.py report/metodo/campione-misura-v3.csv "$@" | tee "$ESITI/misura.json"; }
confronta()   { "$PY" tools/verifiche/confronta.py "$ESITI/.." cloud/; }

case "${1:-}" in
  test) test_ ;;
  attribuisci) attribuisci ;;
  rivenditori) rivenditori ;;
  campione) campione ;;
  misura) shift; misura "$@" ;;
  confronta) confronta ;;
  tutto) test_; attribuisci; rivenditori; campione; confronta ;;
  *) sed -n '2,11p' "$0"; exit 1 ;;
esac
