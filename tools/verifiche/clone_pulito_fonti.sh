#!/usr/bin/env bash
# Prova da clone pulito per TUTTE le fonti (#81, 20/11/2026), complementare a ripetibilita.sh (catena ANAC).
# 1. clona il repository (solo ciò che è in git) in lavoro/clone-fonti/<data>/repo; collega l'archivio del server
#    (append-only, content-addressed: si legge soltanto) e la .venv;
# 2. ripristina gli ingressi di lavoro/ dal registro (git, archivio, archivio-tar) e RIGENERA dal mirror quelli
#    registrati per impronta (lavoro/cig_completo, 11 GB, tools/anac_integrita.py), poi controlla tutti gli sha256;
# 3. controlla il registro unico delle fonti (tools/fonti.py verifica);
# 4. rifà la catena delle società ICT pubbliche e del cloud in proprio (#82) e confronta ogni uscita con quella
#    pubblicata (contenuto, non i byte del gzip): censimento MEF, codici fiscali per CIG, livello DC, tabella unica, vista.
# Uso (sul server, come mxmap.it, un job pesante alla volta): tools/verifiche/clone_pulito_fonti.sh
# Esito: lavoro/clone-fonti/<data>/esito.txt, copiato in esiti/<data>/fonti/clone-pulito.txt
set -u
O=$(cd "$(dirname "$0")/../.." && pwd)
DATA=${RIP_DATA:-$(date +%F)}
GIORNO=${GIORNO_ESITI:-2026-11-20}
D=$O/lavoro/clone-fonti/$DATA
E=$D/esito.txt
rm -rf "$D/repo"; mkdir -p "$D"
: > "$E"
riga() { echo "$*" | tee -a "$E"; }
riga "prova da clone pulito delle fonti, $(date -Is), commit $(git -C "$O" rev-parse --short HEAD)"
git clone -q "$O" "$D/repo" || exit 1
cd "$D/repo"
ln -s "$O/archivio" archivio
ln -s "$O/.venv" .venv
PY=.venv/bin/python
N="nice -n 15 ionice -c3"

riga "== 2. ingressi di lavoro/"
$N $PY tools/ingressi_lavoro.py ripristina > "$D/ripristina.log" 2>&1
grep -E "ripristinato|MANCA|DIVERSO" "$D/ripristina.log" | tee -a "$E"
riga "rigenero lavoro/cig_completo dal mirror ANAC (tools/anac_integrita.py, estrazione degli zip)"
$N $PY -c "import sys; sys.path.insert(0,'tools'); import anac_integrita as A; A.estrai_tutti(A.CIG_COMPLETO, 'cig_completo')" > "$D/cig_completo.log" 2>&1
$N $PY tools/ingressi_lavoro.py verifica > "$D/verifica.json" 2>&1 && riga "ingressi: tutti identici al registro (sha256)" \
  || { riga "ingressi: DIFFERENZE"; grep -v '"ok"' "$D/verifica.json" | tee -a "$E"; }

riga "== 3. registro unico delle fonti"
$PY tools/fonti.py verifica | grep -E '"esito"|non_registrati|senza_acq' | tee -a "$E"

riga "== 4. catena delle società ICT pubbliche e del cloud in proprio"
confronta() {  # confronta <file nel clone> <file pubblicato>: contenuto (decompresso se .gz)
  local a=$1 b=$O/$1
  if [[ $a == *.gz ]]; then cmp -s <(zcat "$a") <(zcat "$b"); else cmp -s "$a" "$b"; fi \
    && riga "identico  $1" || riga "DIVERSO   $1"
}
$N $PY tools/verifiche/inhouse_censimento.py > "$D/e1.log" 2>&1;            confronta dati/inhouse/societa-ict-pa.csv
cp lavoro/inhouse/cig-cf.csv.gz "$D/cig-cf-ripristinato.csv.gz"
$N $PY tools/verifiche/inhouse_cf.py > "$D/e2.log" 2>&1
cmp -s <(zcat lavoro/inhouse/cig-cf.csv.gz) <(zcat "$D/cig-cf-ripristinato.csv.gz") \
  && riga "identico  lavoro/inhouse/cig-cf.csv.gz (rigenerato dal mirror = congelato)" || riga "DIVERSO   lavoro/inhouse/cig-cf.csv.gz"
$N $PY tools/verifiche/datacenter_proprio.py $GIORNO > "$D/e3.log" 2>&1;    confronta esiti/$GIORNO/imbuto/datacenter/datacenter-cig.csv.gz
confronta esiti/$GIORNO/imbuto/datacenter/riepilogo.json
$N $PY tools/verifiche/imbuto_spostamenti.py $GIORNO > "$D/e4.log" 2>&1;   confronta esiti/$GIORNO/imbuto/spostamenti/riepilogo.json
confronta esiti/$GIORNO/imbuto/spostamenti/finale.csv.gz
cmp -s <(zcat lavoro/imbuto/stati-finali.csv.gz) <(zcat "$O/lavoro/imbuto/stati-finali.csv.gz") \
  && riga "identico  lavoro/imbuto/stati-finali.csv.gz" || riga "DIVERSO   lavoro/imbuto/stati-finali.csv.gz"
$N $PY tools/verifiche/inhouse_vista.py $GIORNO > "$D/e5.log" 2>&1;         confronta esiti/$GIORNO/inhouse/vista/vista.json
riga "fine $(date -Is)"
mkdir -p "$O/esiti/$DATA/fonti" && cp "$E" "$O/esiti/$DATA/fonti/clone-pulito.txt"
grep -q "DIVERSO\|DIFFERENZE\|MANCA" "$E" && exit 1 || exit 0
