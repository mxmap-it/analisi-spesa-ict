#!/usr/bin/env python3
"""#57 Sostituzione delle regole proprie con visibilita_pa: le decisioni cambiano? Confronto su un campione già fatto.

A. blocco: per i CIG già elaborati (lavoro/residuo-s6/out/esiti.jsonl) con una pagina archiviata, si rilegge la prima
   pagina dall'archivio e si confronta blocco_v1 (regole proprie) con blocco (visibilita_pa extended.riconosci_blocco).
   Lo stato HTTP è quello registrato (HTTP xxx) o 200; le intestazioni non sono archiviate (limite del confronto).
B. robots.txt: per N host del campione si confronta robots_ok_v1 (urllib.robotparser) con robots_ok
   (visibilita_pa.core.robots) sullo stesso URL. Richiede rete (una richiesta per host, 5 s per host).
Uso (server): SPESAICT_BASE=$PWD .venv/bin/python tools/verifiche/blocchi_vpa_confronto.py [N_HOST] [DATA] -> esiti/<DATA>/acquisizione/blocchi-vpa-confronto.json
"""
import collections, datetime, json, os, sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/acquisizione"))
import piattaforme_cig as P  # noqa: E402

BASE = Path(os.environ.get("SPESAICT_BASE", R))


class Finta:
    def __init__(self, url, testo, status):
        self.url, self.text, self.status_code, self.headers = url, testo, status, {}


def main():
    n_host = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    ultimo = {}
    for l in open(BASE / "lavoro/residuo-s6/out/esiti.jsonl", encoding="utf-8"):
        x = json.loads(l); ultimo[x["cig"]] = x
    conf = collections.Counter(); diversi = []
    for x in ultimo.values():
        if not x["pagine"]: continue
        s = x["pagine"][0]["sha256"]; p = BASE / f"archivio/blobs/sha256/{s[:2]}/{s[2:4]}/{s}"
        if not p.exists(): continue
        t = p.read_bytes().decode("utf-8", "replace")
        st = int(x["blocco"].split()[1]) if x.get("blocco", "").startswith("HTTP") else 200
        r = Finta(x["pagine"][0]["url"], t, st)
        import html as H, re
        testo = re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", t)))
        a, b = P.blocco_v1(r, testo), P.blocco(r, testo)
        conf[(a or "-", b or "-")] += 1
        if a != b and len(diversi) < 30: diversi.append({"cig": x["cig"], "url": r.url, "v1": a, "vpa": b})
    host = {}
    for x in ultimo.values():
        if x.get("link", "").startswith("http") and x["famiglia"] != "js":
            host.setdefault(x["link"].split("/")[2], x["link"])
    rob = collections.Counter(); rdiv = []
    for h, u in list(host.items())[:n_host]:
        try:
            a, b = P.robots_ok_v1(u), P.robots_ok(u)
        except Exception as e:
            rob["errore"] += 1; continue
        rob[f"v1={a} vpa={b}"] += 1
        if a != b: rdiv.append({"url": u, "v1": a, "vpa": b})
    out = {"generato": sys.argv[2] if len(sys.argv) > 2 else str(datetime.date.today()), "blocco": {"pagine": sum(conf.values()),
           "concordi": sum(v for (a, b), v in conf.items() if a == b), "matrice": {f"{a} -> {b}": v for (a, b), v in conf.most_common()},
           "diversi": diversi}, "robots": {"host": sum(rob.values()), "esiti": dict(rob), "diversi": rdiv}}
    d = R / f"esiti/{out['generato']}/acquisizione"; d.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(d / "blocchi-vpa-confronto.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "diversi"} for k, v in out.items() if k != "generato"}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
