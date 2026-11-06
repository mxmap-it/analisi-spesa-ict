"""Seconda via per P17 (#33): codici fiscali segnaposto delle stazioni appaltanti.

Via indipendente da tools/anac_integrita.py: altro dataset (anagrafica stazioni-appaltanti, formato JSON,
non i CSV cig_delta), altro lettore (json della libreria standard, non duckdb), validatore del codice
fiscale riscritto da zero qui sotto. Uso:
  python tools/verifiche/cf_segnaposto.py ZIP_JSON ESITO.json
"""
import collections, hashlib, json, re, sys, zipfile

DISP = {c: v for c, v in zip("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        [1, 0, 5, 7, 9, 13, 15, 17, 19, 21] + [1, 0, 5, 7, 9, 13, 15, 17, 19, 21, 2, 4, 18, 20, 11, 3, 6, 8, 12, 14, 16, 10, 22, 25, 24, 23])}

def ok11(s):
    t = 0
    for i, ch in enumerate(s[:10]):
        d = int(ch)
        if i % 2:
            d *= 2
            d = d - 9 if d > 9 else d
        t += d
    return (10 - t % 10) % 10 == int(s[10])

def ok16(s):
    t = sum(DISP[c] if i % 2 == 0 else (int(c) if c.isdigit() else ord(c) - 65) for i, c in enumerate(s[:15]))
    return chr(65 + t % 26) == s[15]

def motivo(cf):
    cf = (cf or "").strip().upper()
    if not cf: return "vuoto"
    if cf.startswith("CFAVCP"): return "segnaposto CFAVCP"
    if re.fullmatch(r"\d{11}", cf): return None if ok11(cf) else "cifra di controllo (11)"
    if re.fullmatch(r"[A-Z0-9]{16}", cf): return None if ok16(cf) else "carattere di controllo (16)"
    return f"lunghezza {len(cf)}"

def main(zp, out):
    h = hashlib.sha256(open(zp, "rb").read()).hexdigest()
    z = zipfile.ZipFile(zp)
    n, mot, es, attivi, ausa = 0, collections.Counter(), collections.defaultdict(list), collections.Counter(), 0
    for nome in z.namelist():
        for riga in z.open(nome):
            if not riga.strip(): continue
            r = json.loads(riga); n += 1
            m = motivo(r.get("codice_fiscale"))
            if m:
                mot[m] += 1; attivi[(m, r.get("stato"))] += 1
                if r.get("codice_ausa"): ausa += 1
                if len(es[m]) < 5: es[m].append([r.get("codice_fiscale"), r.get("denominazione"), r.get("stato")])
    bad = sum(mot.values())
    ris = {"file": zp, "sha256": h, "righe": n, "non_validi": bad, "pct": round(100 * bad / n, 3),
           "motivi": dict(mot), "per_stato": {f"{a}|{b}": c for (a, b), c in attivi.items()},
           "non_validi_con_codice_ausa": ausa, "esempi": es}
    json.dump(ris, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: ris[k] for k in ("sha256", "righe", "non_validi", "pct", "motivi")}, ensure_ascii=False))

if __name__ == "__main__":
    main(*sys.argv[1:3])
