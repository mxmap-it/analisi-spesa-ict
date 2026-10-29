#!/usr/bin/env python3
"""Tetto di computazione per i compiti automatici di Claude sul server (abbonamento, `claude -p`).

Ogni chiamata passa da qui: prima controlla il consumo del progetto negli ultimi 7 giorni (registro
`stato/claude-consumi.jsonl`), e se il tetto è superato NON chiama Claude ed esce con codice 75 (da riprovare
più tardi: i runner sono ripartibili). Dopo la chiamata registra consumo in token e costo equivalente stimato
dalla CLI (`--output-format json`: `total_cost_usd`, `usage`).

    claude_tetto.py --progetto analisi-spesa-ict -- claude -p --model sonnet ... < prompt

Il tetto sta in config/budget.yaml (`tetto_settimanale_usd_equivalenti`, `tetto_giornaliero_usd_equivalenti`):
il piano Max misura in percentuale del limite settimanale; il costo equivalente della CLI è l'unità che vediamo
da qui. La taratura (USD equivalenti per 1% del limite settimanale) si aggiorna confrontando il registro con il
contatore del piano (ticket #20). Uso: tetto_stato.py per vedere a che punto si è.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

R = Path(__file__).resolve().parents[2]
REGISTRO = R / "stato/claude-consumi.jsonl"


def consumo(progetto: str, giorni: float) -> float:
    if not REGISTRO.exists():
        return 0.0
    limite = datetime.now(timezone.utc) - timedelta(days=giorni)
    tot = 0.0
    for l in REGISTRO.read_text(encoding="utf-8").splitlines():
        try:
            r = json.loads(l)
        except json.JSONDecodeError:
            continue
        if r.get("progetto") == progetto and datetime.fromisoformat(r["quando"]) >= limite:
            tot += r.get("costo_usd_equivalente") or 0.0
    return tot


def main() -> int:
    argv = sys.argv[1:]
    progetto = argv[argv.index("--progetto") + 1] if "--progetto" in argv else "analisi-spesa-ict"
    cmd = argv[argv.index("--") + 1:]
    b = yaml.safe_load(open(R / "config/budget.yaml", encoding="utf-8"))
    sett, gior = b.get("tetto_settimanale_usd_equivalenti"), b.get("tetto_giornaliero_usd_equivalenti")
    c7, c1 = consumo(progetto, 7), consumo(progetto, 1)
    if (sett is not None and c7 >= sett) or (gior is not None and c1 >= gior):
        print(f"TETTO RAGGIUNTO {progetto}: 7g {c7:.2f}/{sett} 24h {c1:.2f}/{gior} USD-eq; riprovare più tardi", file=sys.stderr)
        return 75
    if "--output-format" not in cmd:
        cmd += ["--output-format", "json"]
    t0 = time.time()
    ingresso = sys.stdin.read()
    for tentativo in range(6):
        p = subprocess.run(cmd, input=ingresso, capture_output=True, text=True)
        # limite dell'abbonamento ("You've hit your session limit · resets 3:40pm"): si aspetta il reset e si riprova
        m = re.search(r"limit.{0,40}resets\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)", p.stdout + p.stderr, re.I)
        if not m:
            break
        h = int(m.group(1)) % 12 + (12 if m.group(3).lower() == "pm" else 0)
        ora = datetime.now()
        reset = ora.replace(hour=h, minute=int(m.group(2) or 0), second=0, microsecond=0)
        if reset <= ora:
            reset += timedelta(days=1)
        attesa = (reset - ora).total_seconds() + 120
        print(f"limite dell'abbonamento: attendo il reset ({reset:%H:%M}, {attesa/60:.0f} min)", file=sys.stderr, flush=True)
        time.sleep(attesa)
    rec = {"quando": datetime.now(timezone.utc).isoformat(timespec="seconds"), "progetto": progetto,
           "secondi": round(time.time() - t0), "codice": p.returncode, "comando": " ".join(cmd[:4])}
    try:
        j = json.loads(p.stdout)
        rec.update(costo_usd_equivalente=j.get("total_cost_usd"), usage=j.get("usage"), modello=j.get("modelUsage") and list(j["modelUsage"]),
                   turni=j.get("num_turns"))
        print(j.get("result", ""))
    except json.JSONDecodeError:
        print(p.stdout)
    print(p.stderr, file=sys.stderr, end="")
    REGISTRO.parent.mkdir(parents=True, exist_ok=True)
    with REGISTRO.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return p.returncode


if __name__ == "__main__":
    sys.exit(main())
