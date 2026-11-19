#!/usr/bin/env python3
"""#74: precisione dei campioni annotati a cieco del livello B (report/metodo/bdncp/*.csv), con intervallo di Wilson al 95 %.
Giudizi: giusto / errore / dubbio. Precisione = giusti / tutti (i dubbi contano come non giusti) e, a parte, giusti / (giusti + errori).
Uso: python3 tools/verifiche/bdncp_campioni_misura.py [DATA]  -> esiti/<DATA>/imbuto/bdncp/campioni-misura.json
"""
import collections, csv, datetime, glob, json, math, os, sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]


def wilson(k, n, z=1.96):
    if not n:
        return None
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - h, 3), round(c + h, 3)]


def main():
    data = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
    out = {}
    for p in sorted(glob.glob(str(R / "report/metodo/bdncp/*.csv"))):
        g = collections.Counter((r.get("giudizio") or "").strip() for r in csv.DictReader(open(p, encoding="utf-8")))
        n, k, e = sum(g.values()), g["giusto"], g["errore"]
        out[os.path.relpath(p, R)] = {"n": n, "giudizi": dict(g), "precisione": round(k / n, 3) if n else None, "wilson95": wilson(k, n),
                                      "precisione_senza_dubbi": round(k / (k + e), 3) if k + e else None, "wilson95_senza_dubbi": wilson(k, k + e)}
    d = R / f"esiti/{data}/imbuto/bdncp"
    d.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(d / "campioni-misura.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
