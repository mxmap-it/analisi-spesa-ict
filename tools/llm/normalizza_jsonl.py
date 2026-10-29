#!/usr/bin/env python3
"""Riscrive un file di esiti come JSONL vero (un oggetto per riga), anche se l'agente ha scritto JSON indentato o concatenato.
Tiene l'ultima versione di ogni CIG. Uso: normalizza_jsonl.py FILE"""
import json, sys
from pathlib import Path
f = Path(sys.argv[1]); s = f.read_text(encoding="utf-8"); dec = json.JSONDecoder(); i = 0; per_cig = {}
while i < len(s):
    while i < len(s) and s[i] in " \r\n\t,[]": i += 1
    if i >= len(s): break
    o, i = dec.raw_decode(s, i)
    per_cig[o.get("cig", len(per_cig))] = o
f.write_text("".join(json.dumps(o, ensure_ascii=False) + "\n" for o in per_cig.values()), encoding="utf-8")
print(f, len(per_cig))
