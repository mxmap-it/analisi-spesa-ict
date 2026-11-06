#!/usr/bin/env python3
"""Indice pubblico del mirror (#17): una riga per risorsa, generata dal manifest reale.

Per ogni URL delle fonti di risorse.yaml (ANAC, Consip, SIOPE, IndicePA, ...) riporta:
percorso originale, ultima versione (sha256, byte, Last-Modified), prima/ultima
acquisizione, numero di versioni distinte conservate e lo storico (sha256 + data).
Serve all'indice statico del sito e a dimensionare l'hosting; non pubblica dati.

    indice_mirror.py --out report/mirror            # scrive indice.json, indice.csv, sintesi.json
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
ROOT = Path(os.environ.get("ARCHIVIO_ROOT", BASE / "archivio"))
HOST = {
    "dati.anticorruzione.it": "anac",
    "dati.consip.it": "consip",
    "www.siope.it": "rgs",
    "indicepa.gov.it": "indicepa",
    "raw.githubusercontent.com": "agid_dtd",
    "api.github.com": "agid_dtd",
}
OK = ("nuovo", "invariato")


def dataset_di(url: str) -> str:
    m = re.search(r"/dataset/([^/]+)/", url)
    if m:
        d = m.group(1)
        return re.sub(r"-\d{4}$", "-annuale", d)
    if "/api/3/action/" in url:
        return "api-ckan"
    if "/superset/" in url or "?id=CIG" in url:
        return "pagine-cig"
    nome = url.rstrip("/").rsplit("/", 1)[-1].split("?")[0]
    nome = re.sub(r"\.(csv|json|xlsx|ttl|zip|txt)$", "", nome, flags=re.I)
    nome = re.sub(r"[-_.]?\d{4}$", "", nome)
    return nome[:50] or "indice"


def formato_di(url: str) -> str:
    u = url.lower()
    for f in ("csv", "json", "ttl", "xml", "xlsx"):
        if f"_{f}" in u or u.endswith("." + f) or f".{f}." in u:
            return f.upper()
    if "/api/" in u:
        return "API"
    return u.rsplit(".", 1)[-1][:5].upper()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=BASE / "report" / "mirror")
    a = ap.parse_args()
    per = defaultdict(list)
    tentativi = defaultdict(lambda: defaultdict(int))
    with (ROOT / "manifest.jsonl").open(encoding="utf-8") as f:
        for l in f:
            if not l.strip():
                continue
            r = json.loads(l)
            u = r.get("url", "")
            h = u.split("/")[2] if "://" in u else ""
            if h not in HOST:
                continue
            tentativi[u][r.get("esito")] += 1
            if r.get("esito") in OK and r.get("sha256"):
                per[u].append(r)
    righe = []
    for u in sorted(set(per) | set(tentativi)):
        rs = sorted(per.get(u, []), key=lambda r: r["acquisito"])
        storico, visti = [], set()
        for r in rs:
            if r["sha256"] not in visti:
                visti.add(r["sha256"])
                storico.append({"sha256": r["sha256"], "byte": r.get("dimensione"),
                                "acquisito": r["acquisito"], "last_modified": r.get("last_modified")})
        ult = rs[-1] if rs else {}
        h = u.split("/")[2]
        righe.append({
            "autorita": HOST[h], "dataset": dataset_di(u), "formato": formato_di(u),
            "url_originale": u, "percorso": u.split("/", 3)[3] if u.count("/") >= 3 else "",
            "sha256": ult.get("sha256"), "byte": ult.get("dimensione"),
            "last_modified": ult.get("last_modified"),
            "prima_acquisizione": rs[0]["acquisito"] if rs else None,
            "ultima_acquisizione": ult.get("acquisito"),
            "versioni": len(storico), "esiti": dict(tentativi[u]), "storico": storico,
        })
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "indice.json").write_text(json.dumps(
        {"schema": "spesaict.indice-mirror/1", "risorse": righe}, ensure_ascii=False, indent=1), encoding="utf-8")
    campi = ["autorita", "dataset", "formato", "url_originale", "sha256", "byte", "last_modified",
             "prima_acquisizione", "ultima_acquisizione", "versioni"]
    with (a.out / "indice.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, campi, extrasaction="ignore")
        w.writeheader()
        w.writerows(righe)
    sint = defaultdict(lambda: {"risorse": 0, "conservate": 0, "byte": 0, "byte_storico": 0,
                                "piu_versioni": 0, "formati": set()})
    for r in righe:
        s = sint[(r["autorita"], r["dataset"])]
        s["risorse"] += 1
        s["formati"].add(r["formato"])
        if r["sha256"]:
            s["conservate"] += 1
            s["byte"] += r["byte"] or 0
            s["byte_storico"] += sum(v["byte"] or 0 for v in r["storico"])
        if r["versioni"] > 1:
            s["piu_versioni"] += 1
    out = [{"autorita": k[0], "dataset": k[1], **{**v, "formati": sorted(v["formati"])}}
           for k, v in sorted(sint.items())]
    tot = {"risorse": len(righe), "conservate": sum(1 for r in righe if r["sha256"]),
           "byte_ultime": sum(r["byte"] or 0 for r in righe),
           "byte_storico": sum(sum(v["byte"] or 0 for v in r["storico"]) for r in righe),
           "risorse_con_piu_versioni": sum(1 for r in righe if r["versioni"] > 1)}
    (a.out / "sintesi.json").write_text(json.dumps({"totale": tot, "per_dataset": out},
                                                   ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(tot))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
