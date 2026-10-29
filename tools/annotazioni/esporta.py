#!/usr/bin/env python3
"""Esporta le annotazioni dei volontari dal database del servizio a un file versionato in git.

dati/annotazioni/annotazioni.jsonl: una riga per annotazione, ordinata per id, senza l'hash dell'IP
(serve solo contro gli abusi e resta sul server). Deterministico: stesso database, stesso file.
Lanciato ogni ora dal cron del server insieme a tools/sync_server.sh, così ogni annotazione è in git."""
import json
import sqlite3
from pathlib import Path

R = Path(__file__).resolve().parents[2]
DB, OUT = R / "stato/annotazioni.sqlite", R / "dati/annotazioni/annotazioni.jsonl"
if DB.exists():
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row
    righe = [{k: r[k] for k in r.keys() if k != "ip_hash"} | {"schema": "spesaict.annotazione/1"}
             for r in c.execute("SELECT * FROM annotazioni ORDER BY id")]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in righe), encoding="utf-8")
    print(len(righe), "annotazioni esportate")
