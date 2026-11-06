#!/usr/bin/env bash
# Via 6 sul residuo S6 dell'imbuto, G1 + primi 1.000 G3 (decisione di Fabio 7/11/2026, #55 #66).
# Un `claude -p` (abbonamento, mai API) per pacchetto; ripartibile (salta i pacchetti completi), nice, PAR <= 10.
# Budget: consumo per etichetta (TETTO_ETICHETTA in stato/claude-consumi.jsonl). G3: stima 360 USD-eq, STOP oltre +20 %
# (432) o se la proiezione sui 1.000 CIG lo supera dopo 10 pacchetti: scrive stato/imbuto-g1g3-STOP.txt e non riparte.
#   tools/llm/giro_imbuto.sh            # ordine: g1, ctl, g3
set -u
cd "$(dirname "$0")/../.."
unset CLAUDE_CODE_OAUTH_TOKEN
PAR=${PAR:-4}; MODELLO=${MODELLO:-sonnet}; B=report/metodo/llm/imbuto-g1g3
mkdir -p log/imbuto-g1g3 $B/esiti
# lo STOP (stato/imbuto-g1g3-STOP.txt) ferma solo i pacchetti g3
pacchetti=("$@")
[ ${#pacchetti[@]} -eq 0 ] && pacchetti=($(ls $B/lotti | sed 's/\.jsonl$//' | sort -t- -k1,1 -s | awk '/^g1/{a=a" "$0} /^ctl/{b=b" "$0} /^g3/{c=c" "$0} END{print a,b,c}'))

uno() {
  p=$1; e=$B/esiti/$p.jsonl; g=${p%%-*}
  [ "$g" = g3 ] && [ -f stato/imbuto-g1g3-STOP.txt ] && return 0
  n=$( [ -f "$e" ] && grep -c . "$e" || echo 0 ); t=$(grep -c . $B/lotti/$p.jsonl)
  [ "$n" -ge "$t" ] && return 0
  if [ "$g" = g3 ]; then .venv/bin/python tools/llm/imbuto_budget.py || return 0; fi
  cat > "log/imbuto-g1g3/$p.prompt" <<PROMPT
Sei un analista del progetto analisi-spesa-ict. Leggi e segui alla lettera tools/llm/istruzioni-p3.md (e, da lì, istruzioni.md e istruzioni-p2.md); leggi report/metodo/llm/conoscenza-iniziative.yaml.
Pacchetto: $B/lotti/$p.jsonl. Uscita: $e (una riga JSON per contratto, su UNA riga, aggiunta appena finito il contratto; salta i CIG già presenti). modello "claude-$MODELLO", data "$(date +%F)".
WebFetch non legge i PDF: per ogni documento candidato (link PVL, determina, capitolato, contratto) usa
  .venv/bin/python tools/llm/atti.py <CIG> <URL> --livello <L2 se link PVL, altrimenti L5> --metodo "<come l'hai trovato>" --query "<query>" --tipo <determina|contratto|capitolato|altro> --ente "<ente>"
che archivia con sha256, estrae il testo (anche OCR) e lo stampa. Non aggirare blocchi, non contattare nessuno. Scrivi SOLO nel file di uscita: non modificare nessun altro file.
PROMPT
  TETTO_ETICHETTA=imbuto-$g nice -n 15 timeout 36000 .venv/bin/python tools/llm/claude_tetto.py --progetto analisi-spesa-ict -- \
    claude -p --model "$MODELLO" \
    --allowedTools "WebSearch,WebFetch,Read,Write,Edit,Bash(.venv/bin/python tools/llm/atti.py:*),Bash(grep:*),Bash(head:*)" \
    < "log/imbuto-g1g3/$p.prompt" > "log/imbuto-g1g3/$p.log" 2>&1
  c=$?
  [ $c -eq 75 ] && { echo "$(date -Is) $p TETTO" >> log/imbuto-g1g3/avanzamento.log; return 0; }
  .venv/bin/python tools/llm/normalizza_jsonl.py "$e" >/dev/null 2>&1
  echo "$(date -Is) $p codice=$c esiti=$( [ -f "$e" ] && grep -c . "$e" || echo 0 )/$t" >> log/imbuto-g1g3/avanzamento.log
}
export -f uno; export MODELLO B
printf '%s\n' "${pacchetti[@]}" | xargs -P "$PAR" -I{} bash -c 'uno {}'
