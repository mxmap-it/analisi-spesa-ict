#!/usr/bin/env bash
# Pacchetto di riproduzione del prompt portabile (#55 #66): quando il giro G1/G3 ha almeno 50 esiti verificati, congela il
# pacchetto (50 CIG, una sola volta), esegue Claude Haiku (abbonamento, senza strumenti) e qwen3-vl:8b (Ollama locale, già
# installato, solo CPU, nice 19), poi scrive la concordanza in esiti/imbuto-via6/. Ripartibile; chiamato dal guardiano.
cd "$(dirname "$0")/../.." || exit 1
pgrep -f "[t]ools/llm/riproduzione.sh" | grep -vq "^$$\$" && exit 0
V=report/metodo/llm/riproduzione/v1; unset CLAUDE_CODE_OAUTH_TOKEN
n=$(grep -c . report/metodo/llm/imbuto-g1g3/verificati.jsonl 2>/dev/null || echo 0)
if [ ! -f $V/CONGELATO ]; then
  [ "$n" -lt 50 ] && exit 0
  rm -rf $V/ingressi $V/esiti-* $V/prompt
  .venv/bin/python tools/llm/analisi_documentale.py pacchetto --n 50 && date -Is > $V/CONGELATO
fi
mkdir -p esiti/imbuto-via6
nice -n 15 .venv/bin/python tools/llm/analisi_documentale.py esegui --fornitore claude-cli --modello haiku
.venv/bin/python tools/verifiche/concordanza_llm.py esiti-claude-via6 esiti-haiku --json esiti/imbuto-via6/concordanza-haiku.json
MAX_DOC=6000 MAX_TOT=12000 NUM_CTX=8192 nice -n 19 .venv/bin/python tools/llm/analisi_documentale.py esegui --fornitore ollama --modello qwen3-vl:8b
.venv/bin/python tools/verifiche/concordanza_llm.py esiti-claude-via6 esiti-qwen3-vl_8b --json esiti/imbuto-via6/concordanza-qwen3-vl_8b.json
.venv/bin/python tools/verifiche/concordanza_llm.py esiti-haiku esiti-qwen3-vl_8b --json esiti/imbuto-via6/concordanza-haiku-qwen3-vl_8b.json
