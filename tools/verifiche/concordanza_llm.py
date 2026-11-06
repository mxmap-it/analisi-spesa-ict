"""Concordanza fra due modelli sul pacchetto di riproduzione del prompt portabile (#55 #66).

  python tools/verifiche/concordanza_llm.py esiti-claude-via6 esiti-<modello> [--json OUT]
(cartelle in report/metodo/llm/riproduzione/v1/). Per asse A stato, servizio, asse B stato, giurisdizione:
accordo percentuale con intervallo di Wilson al 95 % e kappa di Cohen; più quota di uscite valide e di citazioni letterali.
"""
import json, math, sys, collections
from pathlib import Path

RIP = Path(__file__).resolve().parents[2] / "report/metodo/llm/riproduzione/v1"


def wilson(k, n, z=1.96):
    if not n: return None
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - m, 3), round(c + m, 3)]


def kappa(pares):
    n = len(pares)
    if not n: return None
    po = sum(a == b for a, b in pares) / n
    ca, cb = collections.Counter(a for a, _ in pares), collections.Counter(b for _, b in pares)
    pe = sum(ca[k] * cb[k] for k in ca) / (n * n)
    return round((po - pe) / (1 - pe), 3) if pe < 1 else 1.0


def carica(d):
    out = {}
    for f in (RIP / d).glob("*.json"):
        r = json.loads(f.read_text(encoding="utf-8"))
        o = r.get("uscita", r) if "uscita" in r else r
        if o: out[r["cig"]] = (o, r)
    return out


def main():
    A, B = carica(sys.argv[1]), carica(sys.argv[2])
    comuni = sorted(set(A) & set(B))
    campi = {"asse_a.stato": lambda o: (o.get("asse_a") or {}).get("stato"), "servizio": lambda o: (o.get("asse_a") or {}).get("servizio"),
             "asse_b.stato": lambda o: (o.get("asse_b") or {}).get("stato"), "giurisdizione": lambda o: (o.get("asse_b") or {}).get("giurisdizione")}
    T = {"a": sys.argv[1], "b": sys.argv[2], "cig_comuni": len(comuni), "campi": {}}
    for k, f in campi.items():
        p = [(f(A[c][0]), f(B[c][0])) for c in comuni]
        ok = sum(x == y for x, y in p)
        T["campi"][k] = {"accordo": ok, "n": len(p), "pct": round(100 * ok / len(p), 1) if p else None, "wilson95": wilson(ok, len(p)), "kappa": kappa(p),
                         "disaccordi": [{"cig": c, "a": f(A[c][0]), "b": f(B[c][0])} for c in comuni if f(A[c][0]) != f(B[c][0])]}
    rb = [B[c][1] for c in B]
    T["validita_b"] = {"uscite": len(rb), "valide": sum(bool(r.get("valida")) for r in rb),
                       "citazioni": sum(len(r.get("prove_letterali") or []) for r in rb), "citazioni_letterali": sum(sum(r.get("prove_letterali") or []) for r in rb)}
    for k, v in T["campi"].items(): print(f"{k}: {v['accordo']}/{v['n']} ({v['pct']} %, Wilson {v['wilson95']}, kappa {v['kappa']})")
    print("validità:", T["validita_b"])
    if "--json" in sys.argv: Path(sys.argv[sys.argv.index("--json") + 1]).write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
