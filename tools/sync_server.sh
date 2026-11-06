#!/usr/bin/env bash
# Sul server: committa gli output prodotti dai job (esiti, atti, consumi), poi pull --rebase e push.
# Evita che i job in corso blocchino gli aggiornamenti del codice. Idempotente.
cd "$(dirname "$0")/.." || exit 1
.venv/bin/python tools/annotazioni/esporta.py >/dev/null 2>&1
git add -A report/metodo/llm/giro2 dati esiti 2>/dev/null; git add -f stato/claude-consumi.jsonl 2>/dev/null
git diff --cached --quiet || git commit -qm "Server: output dei job in corso (#55)"
git diff --quiet || { git stash -q; S=1; }
if git pull -q --rebase && git push -q; then
  rm -f stato/sync-ERRORE.txt
else
  # 7/11/2026: per giorni il rebase falliva (file non tracciati sul server già committati altrove) e il clone divergeva in silenzio.
  git rebase --abort 2>/dev/null
  { date -Is; git status -sb | head -1; echo "pull/push falliti: riallineare a mano (mai stash -u/clean)"; } > stato/sync-ERRORE.txt
fi
[ -n "${S:-}" ] && git stash pop -q
git log --oneline -1
