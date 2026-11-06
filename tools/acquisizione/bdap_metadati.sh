#!/usr/bin/env bash
# BDAP (#25): metadati CKAN package_search a pagine da 250, con tentativi ripetuti (il backend va in timeout a caso,
# verificato 7/11/2026 dal server e dal portatile: non è un blocco per IP). Ripartibile: salta le pagine già scaricate.
cd ~/analisi-spesa-ict
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36 analisi-spesa-ict (+https://github.com/mxmap-it/analisi-spesa-ict)"
B="https://bdap-opendata.rgs.mef.gov.it/SpodCkanApi/api/3/action/package_search?rows=250&start="
s=-250
while :; do s=$((s+250))
  f=lavoro/bdap-pagine/start-$s.json
  [ -s $f ] && python3 -c "import json,sys;json.load(open(sys.argv[1]))" $f 2>/dev/null && continue
  for k in 1 2 3 4 5 6 7 8; do
    c=$(curl -s -o $f.tmp -m 300 -A "$UA" -w "%{http_code}" "$B$s")
    if [ "$c" = 200 ] && python3 -c "import json,sys;json.load(open(sys.argv[1]))" $f.tmp 2>/dev/null; then mv $f.tmp $f; echo "start=$s ok al tentativo $k"; break; fi
    echo "start=$s tentativo $k: $c"; sleep $((30*k))
  done
  sleep 6
  n=$(python3 -c "import json,sys;print(len(json.load(open(sys.argv[1]))[\"result\"][\"results\"]))" $f 2>/dev/null || echo 0)
  [ "$n" -lt 250 ] && break
done
python3 - <<"P"
import json,glob
n=0;ids=set()
for f in sorted(glob.glob("lavoro/bdap-pagine/start-*.json")):
    r=json.load(open(f))["result"]; tot=r["count"]; ids|={p["name"] for p in r["results"]}
print(f"dataset dichiarati {tot}, raccolti {len(ids)}")
P
