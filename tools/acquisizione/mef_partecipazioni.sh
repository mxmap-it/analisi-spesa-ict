#!/bin/bash
# Mirror del censimento MEF delle partecipazioni. Elenca pagine e file del censimento MEF (partecipazioni 2012-2022, adempienti 2014-2023) e li archivia. #52
cd "$(dirname "$0")/../.." && mkdir -p lavoro/inhouse
UA0="Mozilla/5.0 (X11; Linux x86_64) analisi-spesa-ict.mxmap.it"
curl -sL -m 60 -A "$UA0" -o lavoro/inhouse/mef_od_indice.html https://www.de.mef.gov.it/it/attivita_istituzionali/partecipazioni_pubbliche/open_data_partecipazioni/
B=https://www.de.mef.gov.it; P=/it/attivita_istituzionali/partecipazioni_pubbliche/open_data_partecipazioni
UA="Mozilla/5.0 (X11; Linux x86_64) analisi-spesa-ict.mxmap.it"
: > lavoro/inhouse/mef_urls.txt
echo "$B$P/" >> lavoro/inhouse/mef_urls.txt
for p in $(grep -oE 'dati_(partecipazioni|amministrazioni_adempienti)_[0-9]{4}\.html' lavoro/inhouse/mef_od_indice.html | sort -u); do
  echo "$B$P/$p" >> lavoro/inhouse/mef_urls.txt
  curl -sL -m 60 -A "$UA" "$B$P/$p" | grep -oE 'href="[^"]+\.(csv|CSV|zip|pdf|xlsx)"' | sed -E 's/href="//;s/"$//' | sed "s#^/#$B/#" >> lavoro/inhouse/mef_urls.txt
  sleep 5
done
sort -u lavoro/inhouse/mef_urls.txt -o lavoro/inhouse/mef_urls.txt
wc -l lavoro/inhouse/mef_urls.txt
.venv/bin/python tools/archivia.py --lista lavoro/inhouse/mef_urls.txt
