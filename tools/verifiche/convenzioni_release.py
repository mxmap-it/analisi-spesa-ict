"""#62: verifica che ogni documento presente (con sha256) nelle pagine /convenzioni/ abbia un asset nella release
dell'iniziativa su mxmap-it/convenzioni-ict-documenti con digest sha256 coincidente; scarica un campione e ricalcola lo sha256.

Uso: python tools/verifiche/convenzioni_release.py [--campione N]   (API GitHub pubblica; GH_TOKEN facoltativo)
Esce con 1 se qualcosa non coincide. I documenti senza blob nell'archivio sono elencati come esclusi nel manifest."""
import csv
import hashlib
import json
import os
import random
import sys
import urllib.request
from pathlib import Path

R = Path(__file__).resolve().parent.parent.parent
DB = R / "report/convenzioni/database"
REPO = "mxmap-it/convenzioni-ict-documenti"


def get(url, raw=False):
    h = {"User-Agent": "analisi-spesa-ict", "Accept": "application/vnd.github+json"}
    if os.environ.get("GH_TOKEN"):
        h["Authorization"] = f"Bearer {os.environ['GH_TOKEN']}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=300) as r:
        b = r.read()
    return b if raw else json.loads(b)


def main():
    n = int(sys.argv[sys.argv.index("--campione") + 1]) if "--campione" in sys.argv else 5
    voci = json.loads((DB / "iniziative.json").read_text(encoding="utf-8"))
    attesi = {(v["id"], d["sha256"]) for v in voci for i in v["inventario"] for d in i["documenti"] if d.get("sha256")}
    man = {(r["iniziativa"], r["sha256"]): r for r in csv.DictReader(open(DB / "documenti-release.csv", encoding="utf-8"))}
    esclusi = {(e["iniziativa"], e["sha256"]) for e in json.loads((DB / "documenti-release-esclusi.json").read_text(encoding="utf-8"))}
    dig = {}
    for ini in sorted({k[0] for k in man}):
        rel = get(f"https://api.github.com/repos/{REPO}/releases/tags/{ini}")
        p = 1
        while True:
            a = get(f"https://api.github.com/repos/{REPO}/releases/{rel['id']}/assets?per_page=100&page={p}")
            for x in a:
                dig[(ini, x["name"])] = x
            if len(a) < 100:
                break
            p += 1
    errori = 0
    senza = sorted(k for k in attesi if k not in man and k not in esclusi)
    for k in senza:
        print("SENZA ASSET:", k); errori += 1
    for k, r in man.items():
        x = dig.get((k[0], r["asset"]))
        if not x or x.get("digest") != f"sha256:{k[1]}" or x["browser_download_url"] != r["asset_url"]:
            print("NON COINCIDE:", k, r["asset"]); errori += 1
    random.seed(62)
    for k in random.sample(sorted(man), min(n, len(man))):
        h = hashlib.sha256(get(man[k]["asset_url"], raw=True)).hexdigest()
        ok = h == k[1]
        errori += not ok
        print("campione", k[0], man[k]["asset"], "OK" if ok else f"DIVERSO {h}")
    print(f"documenti presenti con sha256: {len(attesi)}; con asset coincidente: {len([k for k in attesi if k in man])}; "
          f"esclusi (blob assente): {len([k for k in attesi if k in esclusi])}; asset nel manifest: {len(man)}; errori: {errori}")
    sys.exit(1 if errori else 0)


if __name__ == "__main__":
    main()
