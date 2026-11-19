#!/usr/bin/env python3
"""M12 (19/11/2026): ict.csv in ordine canonico (tools/analisi/imbuto.py, ordina_ict) rende la rigenerazione identica
byte per byte. Prova senza rigenerare l'imbuto di produzione: si copiano in una cartella di prova (IMBUTO_PROVA_DIR,
default lavoro/ripetibilita/ordina-<oggi>) due ict.csv con lo stesso contenuto e ordine diverso (quello di produzione
e quello rifatto dalla prova di ripetibilità del 19/11), si ordinano con la stessa funzione usata da imbuto.py e si
confrontano: stesso sha256 dopo l'ordinamento, stesse righe (multinsieme) prima e dopo, CIG in ordine crescente.

Uso (server): nice .venv/bin/python tools/verifiche/ripetibilita_ordina_ict.py [ict_A] [ict_B]
  -> esiti/<oggi>/ripetibilita/ordina-ict.json
"""
import collections, csv, datetime, hashlib, json, os, shutil, sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/analisi"))
from imbuto import ordina_ict  # noqa: E402

csv.field_size_limit(1 << 30)
OGGI = os.environ.get("ESITI_DATA", datetime.date.today().isoformat())
PROVA = R / os.environ.get("IMBUTO_PROVA_DIR", f"lavoro/ripetibilita/ordina-{OGGI}")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def righe(p):
    with open(p, encoding="utf-8", newline="") as fh:
        r = list(csv.reader(fh))
    return r[0], collections.Counter(map(tuple, r[1:])), [x[1] for x in r[1:]]


def main():
    a = sys.argv[1] if len(sys.argv) > 1 else "lavoro/imbuto/ict.csv"
    b = sys.argv[2] if len(sys.argv) > 2 else "lavoro/ripetibilita/2026-11-19/prova/A/ict.csv"
    PROVA.mkdir(parents=True, exist_ok=True)
    out = {"data": OGGI, "cartella_prova": str(PROVA.relative_to(R)), "file": {}}
    ordinati = []
    for nome, src in (("A", a), ("B", b)):
        dst = PROVA / f"ict-{nome}.csv"
        shutil.copyfile(R / src, dst)
        h0, c0, _ = righe(dst)
        s0 = sha(dst)
        ordina_ict(str(dst))
        h1, c1, cig = righe(dst)
        out["file"][nome] = {"sorgente": src, "sha256_prima": s0, "sha256_ordinato": sha(dst), "righe": sum(c1.values()),
                             "stesse_righe_dopo_ordinamento": h0 == h1 and c0 == c1, "cig_in_ordine": cig == sorted(cig)}
        ordinati.append(c1)
    fa, fb = out["file"]["A"], out["file"]["B"]
    out["stesso_contenuto"] = ordinati[0] == ordinati[1]
    out["ordine_diverso_prima"] = fa["sha256_prima"] != fb["sha256_prima"]
    out["stesso_sha256_dopo"] = fa["sha256_ordinato"] == fb["sha256_ordinato"]
    out["ok"] = out["stesso_contenuto"] and out["stesso_sha256_dopo"] and all(
        f["stesse_righe_dopo_ordinamento"] and f["cig_in_ordine"] for f in (fa, fb))
    d = R / f"esiti/{OGGI}/ripetibilita"
    d.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(d / "ordina-ict.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(out, indent=1, ensure_ascii=False))
    sys.exit(0 if out["ok"] else 1)


if __name__ == "__main__":
    main()
