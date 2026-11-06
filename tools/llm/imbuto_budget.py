#!/usr/bin/env python3
"""Guardia di budget del giro imbuto G3 (decisione di Fabio 7/11/2026): stima 360 USD-eq per 1.000 CIG, stop oltre +20 %.
Legge stato/claude-consumi.jsonl (righe con etichetta imbuto-g3) e gli esiti; esce 1 e scrive stato/imbuto-g1g3-STOP.txt
se il consumo supera 432 USD-eq o se, dopo almeno 50 CIG, la proiezione su 1.000 lo supera. Stampa sempre lo stato."""
import json, sys
from datetime import datetime, timezone
from pathlib import Path
R = Path(__file__).resolve().parents[2]
STIMA, MARGINE, N = 360.0, 1.20, 1000
spesa = sum((json.loads(l).get("costo_usd_equivalente") or 0) for l in (R / "stato/claude-consumi.jsonl").read_text(encoding="utf-8").splitlines()
            if l.strip() and '"imbuto-g3"' in l)
fatti = sum(1 for f in (R / "report/metodo/llm/imbuto-g1g3/esiti").glob("g3-*.jsonl") for l in f.read_text(encoding="utf-8").splitlines() if l.strip())
proiezione = spesa / fatti * N if fatti else None
print(json.dumps({"spesa_g3_usd_eq": round(spesa, 2), "cig_g3_fatti": fatti, "proiezione_1000": proiezione and round(proiezione, 1), "limite": STIMA * MARGINE}))
motivo = None
if spesa >= STIMA * MARGINE: motivo = f"consumo G3 {spesa:.1f} USD-eq oltre {STIMA*MARGINE:.0f}"
elif fatti >= 50 and proiezione > STIMA * MARGINE: motivo = f"proiezione {proiezione:.0f} USD-eq su {N} CIG (dopo {fatti}) oltre {STIMA*MARGINE:.0f}"
if motivo:
    (R / "stato/imbuto-g1g3-STOP.txt").write_text(f"{datetime.now(timezone.utc).isoformat(timespec='seconds')} STOP: {motivo}. Chiedere a Fabio.\n", encoding="utf-8")
    sys.exit(1)
