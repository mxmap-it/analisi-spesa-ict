#!/usr/bin/env bash
# Cron giornaliero dopo le metriche (06:40): rigenera il cruscotto ANAC, ricostruisce il sito e pubblica SOLO i file
# del cruscotto (pagina, dati, HTML costruito). Le altre modifiche in corso nel clone non vengono committate.
cd "$(dirname "$0")/.." || exit 1
.venv/bin/python tools/cruscotto_anac.py || exit 1
hugo --source sito --minify --cleanDestinationDir >/dev/null 2>&1 || exit 1
git add sito/content/enti/anac-cruscotto.md sito/static/dati/anac-cruscotto.json docs/enti/anac-cruscotto docs/dati/anac-cruscotto.json 2>/dev/null
git diff --cached --quiet || git commit -qm "Cruscotto ANAC: misura del $(date +%F) (#23)"
git pull -q --rebase --autostash && git push -q
