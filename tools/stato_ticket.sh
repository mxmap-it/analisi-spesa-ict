#!/bin/bash
# uso: stato_ticket.sh <numero> <Todo|In Progress|Done>
N=$1; S=$2; P=1; O=mxmap-it
F=PVTSSF_lADOEYrgLM4Bo0y9zhnTFWw
case "$S" in Todo) OPT=f75ad846;; "In Progress") OPT=47fc9ee4;; Done) OPT=98236657;; esac
PID=$(gh project view $P --owner $O --format json --jq .id)
ITEM=$(gh project item-list $P --owner $O --limit 200 --format json --jq ".items[]|select(.content.number==$N)|.id")
gh project item-edit --id "$ITEM" --project-id "$PID" --field-id $F --single-select-option-id $OPT >/dev/null && echo "#$N -> $S"
