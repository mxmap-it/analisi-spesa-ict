#!/usr/bin/env bash
# Sul server: committa gli output prodotti dai job (esiti, atti, consumi), poi pull --rebase e push.
# Evita che i job in corso blocchino gli aggiornamenti del codice. Idempotente.
cd "$(dirname "$0")/.." || exit 1
.venv/bin/python tools/annotazioni/esporta.py >/dev/null 2>&1
git add -A report/metodo/llm/giro2 dati esiti 2>/dev/null; git add -f stato/claude-consumi.jsonl 2>/dev/null
git diff --cached --quiet || git commit -qm "Server: output dei job in corso (#55)"
git diff --quiet || { git stash -q; S=1; }; git pull -q --rebase; git push -q; [ -n "${S:-}" ] && git stash pop -q
git log --oneline -1
