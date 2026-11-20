#!/usr/bin/env bash
# Prova di ripetibilità dell'imbuto «per dove siamo» (richiesta di Fabio del 19/11/2026, #71 #74).
# Rifà DA ZERO, in lavoro/ripetibilita/<data>/ (mai sugli esiti pubblicati), i passi deterministici della catena e
# confronta ogni uscita con quella pubblicata (tools/verifiche/ripetibilita_confronta.py):
#   a  ict.csv e riepilogo dall'archivio ANAC: imbuto_prova_034.py prepara + A (imbuto 0.3.4, DEDUP_CPV, lente v4.5)
#   b  imbuto_strati (--rigenera, --json), imbuto_tetti (--rigenera, --json), imbuto_revisione, imbuto_licenze, imbuto_cig_ripetuti
#   c  imbuto_bdncp (livello B)
#   d  raffinamento.py l2 ed esito (L3 riletto dagli esiti versionati: il modello linguistico non si rigenera)
# Variabili d'ambiente usate (tutte opzionali negli script, default = comportamento pubblicato):
#   IMBUTO_PROVA_DIR, IMBUTO_ICT, IMBUTO_RIEP, IMBUTO_ESITI_OUT, IMBUTO_ESITI, IMBUTO_VERSIONE, ESITI_DATA.
# Uso (SUL SERVER, come mxmap.it, un job pesante alla volta; ~1,5 h):
#   tools/verifiche/ripetibilita.sh [passi]      # passi: abcde (e: società ICT pubbliche, #82); default abcd — i passi già fatti si saltano (file .fatto)
#   poi: .venv/bin/python tools/verifiche/ripetibilita_confronta.py lavoro/ripetibilita/<data> esiti/<data>/ripetibilita
set -u
cd "$(dirname "$0")/../.."
PY=.venv/bin/python
DATA=${RIP_DATA:-$(date +%F)}
D=lavoro/ripetibilita/$DATA
PASSI=${1:-abcd}
mkdir -p "$D/esiti/bdncp" "$D/log"
T=$D/tempi.tsv

passo() {  # passo <nome> <comando...>: esegue, registra durata e codice, salta se già fatto
  local n=$1; shift
  [ -f "$D/log/$n.fatto" ] && { echo "salto $n (già fatto)"; return 0; }
  local t0=$(date +%s); echo "$(date -Is) inizio $n: $*" | tee -a "$D/log/catena.log"
  nice -n 15 ionice -c3 "$@" > "$D/log/$n.log" 2>&1; local c=$?
  echo -e "$n\t$t0\t$(date +%s)\t$c\t$*" >> "$T"
  echo "$(date -Is) fine $n codice=$c" | tee -a "$D/log/catena.log"
  [ $c -eq 0 ] && touch "$D/log/$n.fatto"
  return $c
}

memoria() {  # attende >= 12 GB disponibili (regola dell'incidente del 9/11)
  while [ "$(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo)" -lt 12 ]; do
    echo "$(date -Is) attesa memoria" >> "$D/log/catena.log"; sleep 120; done
}

# M12: gli ingressi di lavoro/ fuori dal mirror (registro config/ingressi-lavoro.yaml) devono esserci con lo sha256 del
# registro; da un clone pulito si rimettono con «ripristina» (da git e, per cig_link.csv, dall'archivio content-addressed)
$PY tools/ingressi_lavoro.py ripristina > "$D/log/ingressi.log" 2>&1 || { echo "ingressi di lavoro/ mancanti o diversi: $D/log/ingressi.log"; exit 1; }
# #81: registro unico di tutte le fonti (inventario statico + ingressi congelati + manifest del mirror)
$PY tools/fonti.py verifica > "$D/log/fonti.log" 2>&1 || { echo "fonti non tutte registrate: $D/log/fonti.log"; exit 1; }
export IMBUTO_VERSIONE=0.3.4
if [[ $PASSI == *a* ]]; then
  memoria
  export IMBUTO_PROVA_DIR=$D/prova
  # come lancia() di imbuto_prova_034.py: limite di memoria virtuale 8 GB, nice 19
  # 19/11: con 8 GB di memoria virtuale la creazione della tabella delta in duckdb è andata in Out of Memory (il 9/11 no);
  # la prova usa 12 GB di memoria virtuale per «prepara» (memory_limit di duckdb invariato a 4 GB). Variabile RIP_VMEM_PREPARA.
  passo a1-prepara bash -c "ulimit -v ${RIP_VMEM_PREPARA:-12582912}; exec $PY tools/verifiche/imbuto_prova_034.py prepara" || exit 1
  memoria
  passo a2-imbuto-A bash -c "ulimit -v 8388608; exec $PY tools/verifiche/imbuto_prova_034.py A" || exit 1
fi
export IMBUTO_ICT=$D/prova/A/ict.csv IMBUTO_RIEP=$D/prova/A/riepilogo.json IMBUTO_ESITI_OUT=$D/esiti
if [[ $PASSI == *b* ]]; then
  passo b1-strati-rigenera $PY tools/verifiche/imbuto_strati.py --rigenera
  passo b2-strati $PY tools/verifiche/imbuto_strati.py --json $D/esiti/strati.json
  passo b3-tetti-rigenera $PY tools/verifiche/imbuto_tetti.py --rigenera
  passo b4-tetti $PY tools/verifiche/imbuto_tetti.py --json $D/esiti/tetti.json
  passo b5-revisione $PY tools/verifiche/imbuto_revisione.py --json $D/esiti/revisione.json
  passo b6-licenze-rigenera $PY tools/verifiche/imbuto_licenze.py --rigenera
  passo b7-licenze $PY tools/verifiche/imbuto_licenze.py --json $D/esiti/licenze.json
  passo b8-cig-ripetuti env IMBUTO_ESITI=$D/esiti $PY tools/verifiche/imbuto_cig_ripetuti.py
fi
if [[ $PASSI == *c* ]]; then
  memoria
  passo c1-bdncp env IMBUTO_ESITI_OUT=$D/esiti/bdncp ESITI_DATA=2026-11-19 $PY tools/verifiche/imbuto_bdncp.py
fi
if [[ $PASSI == *d* ]]; then
  passo d1-l2 $PY tools/llm/raffinamento.py l2 2026-11-18
  passo d2-esito-l3 $PY tools/llm/raffinamento.py esito 2026-11-18
fi
if [[ $PASSI == *e* ]]; then
  # #82: società ICT pubbliche (censimento MEF dal mirror) e vista per codice fiscale
  mkdir -p "$D/inhouse"
  passo e1-censimento $PY tools/verifiche/inhouse_censimento.py
  passo e2-vista $PY tools/verifiche/inhouse_vista.py $(date +%F)
fi
echo "$(date -Is) catena finita" | tee -a "$D/log/catena.log"
touch "$D/FINITO"
