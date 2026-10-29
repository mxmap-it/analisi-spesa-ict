#!/usr/bin/env bash
# Secondo giro della via 6 sul server: un `claude -p` (Haiku, abbonamento) per pacchetto da 5 contratti,
# con WebSearch/WebFetch e tools/llm/atti.py per scaricare e leggere gli atti (anche PDF e scansioni).
# Ripartibile: salta i pacchetti con 5 esiti; idempotente; parallelismo PAR (default 4); nice.
#   tools/llm/giro2.sh            # tutti i pacchetti mancanti
#   PAR=2 tools/llm/giro2.sh g2-010 g2-011
set -u
cd "$(dirname "$0")/../.."
unset CLAUDE_CODE_OAUTH_TOKEN
PAR=${PAR:-4}; MODELLO=${MODELLO:-haiku}
mkdir -p log/giro2 report/metodo/llm/giro2/esiti
pacchetti=("$@")
[ ${#pacchetti[@]} -eq 0 ] && pacchetti=($(ls report/metodo/llm/giro2/lotti | sed 's/\.jsonl$//'))
uno() {
  p=$1; e=report/metodo/llm/giro2/esiti/$p.jsonl
  n=$( [ -f "$e" ] && grep -c . "$e" || echo 0 ); t=$(grep -c . report/metodo/llm/giro2/lotti/$p.jsonl)
  [ "$n" -ge "$t" ] && return 0
  nice -n 15 timeout 1800 claude -p --model "$MODELLO" \
    --allowedTools "WebSearch" "WebFetch" "Read" "Write" "Edit" "Bash(.venv/bin/python tools/llm/atti.py:*)" "Bash(grep:*)" "Bash(head:*)" \
    "Sei un analista del progetto analisi-spesa-ict. Leggi e segui alla lettera tools/llm/istruzioni-p2.md e, per campi e definizioni, tools/llm/istruzioni.md; leggi report/metodo/llm/conoscenza-iniziative.yaml e report/metodo/analisi-infrastrutture/MODELLO.md.
Pacchetto: report/metodo/llm/giro2/lotti/$p.jsonl. Uscita: $e (una riga JSON per contratto, aggiunta appena finito; salta i CIG già presenti). modello \"claude-$MODELLO\", data \"$(date +%F)\".
IMPORTANTE: WebFetch non legge i PDF. Per ogni documento candidato (determina, contratto, capitolato), anche PDF, usa
  .venv/bin/python tools/llm/atti.py <CIG> <URL> --metodo \"<come l'hai trovato>\" --query \"<query>\" --tipo <determina|contratto|...> --ente \"<ente>\"
che lo archivia con sha256, ne estrae il testo (anche OCR) e ti stampa il testo. Metti in fonti gli URL così letti e in atto_ente quello dell'atto che cita il CIG. Non aggirare blocchi, non contattare nessuno." \
    > log/giro2/$p.log 2>&1
  echo "$(date -Is) $p esiti=$( [ -f "$e" ] && grep -c . "$e" || echo 0 )/$t" >> log/giro2/avanzamento.log
}
export -f uno; export MODELLO
printf '%s\n' "${pacchetti[@]}" | xargs -P "$PAR" -I{} bash -c 'uno {}'
