#!/usr/bin/env bash
# Riproduce da zero le verifiche del rendiconto ANAC. Istruzioni complete: RIPRODURRE.md
#
#   tools/verifica_anac.sh ambiente    crea .venv con le versioni bloccate di requirements.txt
#   tools/verifica_anac.sh dal-vivo    misura ORA il server ANAC (metriche I1-I9), pochi minuti, nessun download pesante
#   tools/verifica_anac.sh scarica     scarica i file che servono alle verifiche (~95 GB, ore)
#   tools/verifica_anac.sh snapshot    confronta gli sha256 dei file scaricati con quelli usati per il rendiconto
#   tools/verifica_anac.sh verifiche   esegue tutte le verifiche sui file scaricati
#   tools/verifica_anac.sh confronta   confronta i risultati con quelli pubblicati in report/anac/
#   tools/verifica_anac.sh tutto       ambiente + scarica + snapshot + verifiche + confronta
set -euo pipefail
cd "$(dirname "$0")/.."
PY=.venv/bin/python
OGGI=$(date +%F)
ESITI=esiti/$OGGI
# I dataset che le verifiche leggono (gli altri restano nel mirror completo, non servono a riprodurre i numeri)
DATASET=('ocds-appalti-ordinari-*' 'cig-20*' 'cig' 'aggiudicazioni' 'aggiudicatari' 'cup' 'stazioni-appaltanti')

ambiente() {
  python3 -m venv .venv
  "$PY" -m pip install --quiet --upgrade pip
  "$PY" -m pip install --quiet -r requirements.txt
  "$PY" -c "import duckdb, requests, ijson, yaml; print('ambiente pronto, duckdb', duckdb.__version__)"
}

dal_vivo() {
  mkdir -p "$ESITI"
  "$PY" tools/metriche_anac.py --oggi "$OGGI"
  cp "stato/metriche/$OGGI.json" "$ESITI/metriche-dal-vivo.json"
  echo "esito: $ESITI/metriche-dal-vivo.json (I1-I9: violata / rispettata, con le prove)"
}

scarica() {
  "$PY" tools/mirror_anac.py --formati CSV JSON --dataset "${DATASET[@]}"
}

snapshot() {
  "$PY" tools/verifiche/snapshot.py controlla report/anac/snapshot-2026-10-27.tsv
}

verifiche() {
  mkdir -p "$ESITI" lavoro
  nice -n 10 "$PY" tools/verifiche/ocds_mesi_duplicati.py >/dev/null && cp lavoro/verifica_ocds_mesi_duplicati.json "$ESITI/"
  nice -n 10 "$PY" tools/verifiche/verifica_38_42.py      >/dev/null && cp lavoro/verifica_38_42.json "$ESITI/"
  nice -n 10 "$PY" tools/verifiche/cig_accordo_quadro.py  >/dev/null && cp lavoro/verifica_cig_accordo_quadro.json "$ESITI/"
  nice -n 10 "$PY" tools/verifiche/seconde_vie.py       >/dev/null && cp lavoro/seconde_vie.json "$ESITI/"
  nice -n 10 "$PY" tools/anac_integrita.py --completo --oggi 2026-10-27 --out "$ESITI/integrita-completo.json"
  echo "esiti in $ESITI/"
}

confronta() {
  "$PY" tools/verifiche/confronta.py "$ESITI"
}

case "${1:-}" in
  ambiente) ambiente ;;
  dal-vivo) dal_vivo ;;
  scarica) scarica ;;
  snapshot) snapshot ;;
  verifiche) verifiche ;;
  confronta) confronta ;;
  tutto) ambiente; scarica; snapshot; verifiche; confronta ;;
  *) sed -n '2,11p' "$0"; exit 1 ;;
esac
