#!/usr/bin/env python3
"""#11 Elenco delle risorse open data Consip da specchiare, dal catalogo CKAN (dati.consip.it/api/3).

Per ogni dataset di package_list: package_show, poi le risorse. Si tengono le annualità dal 2024 in poi (le più a
rischio di sparire, ticket #11) e le risorse senza anno nel nome; si scrive l'elenco degli URL (uno per riga) che
tools/archivia.py --lista consuma, più un CSV con dataset, nome, formato, dimensione dichiarata (HEAD).
Idempotente: rifarlo riproduce l'elenco; archivia.py non riscarica ciò che non è cambiato.

    consip_elenco.py [--da 2024] > lavoro/consip/elenco.txt   (CSV in lavoro/consip/risorse.csv)
    consip_elenco.py --api https://indicepa.gov.it/ipa-dati/api/3/action/ --out lavoro/indicepa > lavoro/indicepa/elenco.txt
"""
import argparse, csv, json, os, re, sys, time, urllib.request

UA = "Mozilla/5.0 (compatible; analisi-spesa-ict; +https://analisi-spesa-ict.mxmap.it)"
API = "https://dati.consip.it/api/3/action/"  # --api per altri cataloghi CKAN (IndicePA, #13)


def get(u, metodo="GET"):
    req = urllib.request.Request(u, method=metodo, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read() if metodo == "GET" else r.headers


def main():
    global API
    ap = argparse.ArgumentParser(); ap.add_argument("--da", type=int, default=2024); ap.add_argument("--out", default="lavoro/consip")
    ap.add_argument("--api", default=API)
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    API = a.api
    righe = []
    for p in json.loads(get(API + "package_list"))["result"]:
        d = json.loads(get(API + "package_show?id=" + p))["result"]; time.sleep(1)
        for r in d.get("resources", []):
            u = r.get("url", ""); anni = [int(x) for x in re.findall(r"(?<!\d)(20\d\d)(?!\d)", u + " " + r.get("name", ""))]
            if anni and max(anni) < a.da: continue
            try:
                h = get(u, "HEAD"); dim = h.get("Content-Length", "")
            except Exception as e:
                dim = f"errore:{e}"
            time.sleep(1)
            righe.append({"dataset": p, "nome": r.get("name", ""), "formato": r.get("format", ""), "url": u, "byte_dichiarati": dim})
    with open(os.path.join(a.out, "risorse.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(righe[0])); w.writeheader(); w.writerows(righe)
    for r in righe:
        if not str(r["byte_dichiarati"]).startswith("errore"): print(r["url"])
    tot = sum(int(r["byte_dichiarati"]) for r in righe if str(r["byte_dichiarati"]).isdigit())
    print(f"{len(righe)} risorse, {tot/1e9:.2f} GB dichiarati", file=sys.stderr)


if __name__ == "__main__":
    main()
