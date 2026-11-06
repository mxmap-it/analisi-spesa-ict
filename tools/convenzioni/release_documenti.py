"""#62: pubblica le copie dei documenti delle convenzioni come asset delle GitHub Release
del repository pubblico mxmap-it/convenzioni-ict-documenti (una release per iniziativa, tag = id).

Scelta Release e non LFS: DECISIONI.md (6/11/2026).

Uso (sul server, dove sta l'archivio content-addressed):
  python release_documenti.py piano  --radice DIR --archivio ~/analisi-spesa-ict/archivio --out DIR_LAVORO
  GH_TOKEN=... python release_documenti.py carica --out DIR_LAVORO        # ripartibile
  GH_TOKEN=... python release_documenti.py manifest --out DIR_LAVORO      # manifest.csv/json con asset_url

--radice = cartella che contiene report/convenzioni (clone o copia). Il token si passa solo per ambiente,
mai su file. Ripartibile: un asset con lo stesso nome e digest sha256 uguale si salta; ogni upload è
annotato in DIR_LAVORO/caricati.jsonl.

Inclusi: solo documenti scaricati da pagine pubbliche ufficiali (archiviati.jsonl e documenti dell'inventario
di iniziative.json con sha256). Esclusi: «reperiti altrove» (fonte non ufficiale), materiali interni
(es. PDF Proteggimi: non è nell'archivio delle convenzioni, e il filtro sui nomi lo esclude comunque)."""
import argparse
import csv
import glob
import hashlib
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

REPO = "mxmap-it/convenzioni-ict-documenti"
SITO = "https://analisi-spesa-ict.mxmap.it/convenzioni/"
ESCLUSI_NOME = re.compile(r"proteggimi", re.I)


def blob(arch, s):
    return Path(arch) / "blobs/sha256" / s[:2] / s[2:4] / s


def estensione(p):
    with open(p, "rb") as f:
        t = f.read(8)
    if t.startswith(b"%PDF"):
        return ".pdf"
    if t.startswith(b"PK"):
        return ".zip"
    if t[:1] == b"\x30":
        return ".p7m"
    if t.startswith(b"\xd0\xcf\x11\xe0"):
        return ".doc"
    if t.lstrip()[:1] in (b"<",):
        return ".xml"
    return ".bin"


def pulisci(n):
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode()
    n = re.sub(r"[^A-Za-z0-9._-]+", "_", n).strip("._-")
    n = re.sub(r"_+", "_", n)
    if len(n) > 150:
        base, dot, ext = n.rpartition(".")
        n = (base[:140] + "." + ext) if dot and len(ext) <= 8 else n[:150]
    return n or "documento"


def piano(a):
    R = Path(a.radice) / "report/convenzioni"
    arch = {}
    for l in open(R / "database/archiviati.jsonl", encoding="utf-8"):
        r = json.loads(l)
        x = arch.setdefault(r["sha256"], {"urls": [], "byte": r["byte"], "data": r["acquisito"]})
        x["urls"].append(r["url"])
        x["data"] = min(x["data"], r["acquisito"])
    u2s = {u: s for s, x in arch.items() for u in x["urls"]}
    it = json.load(open(R / "database/iniziative.json", encoding="utf-8"))
    nomi = {v["id"]: v.get("nome") or v["id"] for v in it}
    righe = defaultdict(dict)   # iniziativa -> sha -> riga

    def aggiungi(ini, s, titolo, url, data=None, byte=None):
        if ini not in nomi:
            return
        r = righe[ini].setdefault(s, {"iniziativa": ini, "sha256": s, "titolo": titolo, "url_originale": url,
                                      "byte": byte, "data_acquisizione": data})
        if not r["titolo"] and titolo:
            r["titolo"] = titolo

    for v in it:
        for i in v["inventario"]:
            for d in i["documenti"]:
                if d.get("sha256"):
                    x = arch.get(d["sha256"], {})
                    aggiungi(v["id"], d["sha256"], d.get("nome"), d["url"], x.get("data") or d.get("data"), x.get("byte"))
    for f in sorted(glob.glob(str(R / "database/consip/*.json"))):
        j = json.load(open(f, encoding="utf-8"))
        for p in j["pagine"]:
            if not p.get("cita_chiave", True):
                continue
            for d in p["documenti"]:
                s = u2s.get(d["url"])
                if s:
                    aggiungi(j["iniziativa"], s, d.get("nome") or d.get("testo"), d["url"], arch[s]["data"], arch[s]["byte"])
    for f in sorted(glob.glob(str(R / "aretepa/schede/*.json"))):
        j = json.load(open(f, encoding="utf-8"))
        for d in j.get("documenti", []):
            s = u2s.get(d.get("url"))
            if s and j.get("cdSigef"):
                aggiungi(f"consip-{j['cdSigef']}", s, d.get("nome"), d["url"], arch[s]["data"], arch[s]["byte"])
    out, esclusi = [], []
    for ini in sorted(righe):
        usati = set()
        for s, r in sorted(righe[ini].items(), key=lambda kv: (kv[1]["titolo"] or "", kv[0])):
            p = blob(a.archivio, s)
            tit = r["titolo"] or urllib.parse.unquote(r["url_originale"].rsplit("/", 1)[-1])
            if ESCLUSI_NOME.search(tit + r["url_originale"]):
                esclusi.append({**r, "motivo": "materiale interno/riservato"}); continue
            if not p.exists():
                esclusi.append({**r, "motivo": "blob assente dall'archivio"}); continue
            r["byte"] = p.stat().st_size
            if r["byte"] >= 2 * 1024 ** 3:
                esclusi.append({**r, "motivo": "oltre 2 GiB (limite asset)"}); continue
            base = urllib.parse.unquote(r["url_originale"].split("?")[0].rsplit("/", 1)[-1])
            if "getDocument" in r["url_originale"] or "." not in base or r["url_originale"].startswith("https://ted.europa.eu"):
                base = (r["titolo"] or base) + estensione(p)
            n = pulisci(base)
            if n.lower() in usati:
                n = f"{s[:12]}_{n}"
            usati.add(n.lower())
            r["titolo"] = tit
            r["asset"] = n
            out.append(r)
    Path(a.out).mkdir(parents=True, exist_ok=True)
    json.dump({"righe": out, "esclusi": esclusi, "nomi": {k: nomi[k] for k in righe}}, open(Path(a.out) / "piano.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"piano: {len(out)} asset in {len(righe)} release, {sum(r['byte'] for r in out)/1e9:.2f} GB; esclusi {len(esclusi)}")


def api(metodo, url, dati=None, tipo="application/json", tentativi=6):
    tok = os.environ["GH_TOKEN"]
    for k in range(tentativi):
        corpo = dati if isinstance(dati, (bytes, type(None))) else json.dumps(dati).encode()
        rq = urllib.request.Request(url, data=corpo, method=metodo, headers={
            "Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json", "Content-Type": tipo,
            "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "analisi-spesa-ict"})
        try:
            with urllib.request.urlopen(rq, timeout=600) as r:
                b = r.read()
                return json.loads(b) if b else None
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            msg = e.read()[:300]
            if e.code in (403, 429, 500, 502, 503, 504) and k < tentativi - 1:
                time.sleep(30 * (k + 1)); continue
            raise RuntimeError(f"{metodo} {url}: {e.code} {msg}")
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if k < tentativi - 1:
                time.sleep(30 * (k + 1)); continue
            raise RuntimeError(f"{metodo} {url}: {e}")


def assets(rid):
    tutti, p = [], 1
    while True:
        b = api("GET", f"https://api.github.com/repos/{REPO}/releases/{rid}/assets?per_page=100&page={p}") or []
        tutti += b
        if len(b) < 100:
            return tutti
        p += 1


def release(ini, nome):
    r = api("GET", f"https://api.github.com/repos/{REPO}/releases/tags/{ini}")
    if r:
        return r
    return api("POST", f"https://api.github.com/repos/{REPO}/releases", {
        "tag_name": ini, "target_commitish": "main", "name": f"{ini} — {nome}"[:200], "make_latest": "false",
        "body": (f"Copie dei documenti pubblici dell'iniziativa **{ini}** ({nome}), scaricate dalle pagine ufficiali.\n\n"
                 f"Per ogni file: fonte originale, sha256 e data di acquisizione in `manifest.csv` del repository. "
                 f"Scheda: {SITO}{ini}/")})


def carica(a):
    P = json.load(open(Path(a.out) / "piano.json", encoding="utf-8"))
    log = open(Path(a.out) / "caricati.jsonl", "a", encoding="utf-8")
    per = defaultdict(list)
    for r in P["righe"]:
        per[r["iniziativa"]].append(r)
    for ini in sorted(per):
        rel = release(ini, P["nomi"].get(ini, ini))
        ci = {x["name"]: x for x in assets(rel["id"])}
        for r in per[ini]:
            x = ci.get(r["asset"])
            if x and x.get("digest") == f"sha256:{r['sha256']}" and x.get("state") == "uploaded":
                continue
            if x:   # parziale o diverso: si rifà
                api("DELETE", f"https://api.github.com/repos/{REPO}/releases/assets/{x['id']}")
            p = blob(a.archivio, r["sha256"])
            dati = p.read_bytes()
            if hashlib.sha256(dati).hexdigest() != r["sha256"]:
                print("SHA LOCALE NON COINCIDE", p, file=sys.stderr); continue
            u = (rel["upload_url"].split("{")[0] + "?name=" + urllib.parse.quote(r["asset"]))
            y = api("POST", u, dati, "application/octet-stream")
            log.write(json.dumps({"iniziativa": ini, "asset": r["asset"], "sha256": r["sha256"], "digest": y.get("digest"),
                                  "id": y["id"], "t": time.strftime("%Y-%m-%dT%H:%M:%S")}) + "\n"); log.flush()
            print(ini, r["asset"], y.get("digest") == f"sha256:{r['sha256']}", flush=True)
            time.sleep(1)


def manifest(a):
    P = json.load(open(Path(a.out) / "piano.json", encoding="utf-8"))
    idx = {}
    for ini in sorted({r["iniziativa"] for r in P["righe"]}):
        rel = api("GET", f"https://api.github.com/repos/{REPO}/releases/tags/{ini}")
        for x in assets(rel["id"]) if rel else []:
            idx[(ini, x["name"])] = x
    righe, mancano = [], 0
    for r in P["righe"]:
        x = idx.get((r["iniziativa"], r["asset"]))
        ok = bool(x) and x.get("digest") == f"sha256:{r['sha256']}"
        mancano += not ok
        righe.append({"iniziativa": r["iniziativa"], "titolo": r["titolo"], "url_originale": r["url_originale"], "sha256": r["sha256"],
                      "byte": r["byte"], "data_acquisizione": r["data_acquisizione"], "asset": r["asset"],
                      "asset_url": x["browser_download_url"] if ok else ""})
    with open(Path(a.out) / "manifest.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(righe[0]))
        w.writeheader(); w.writerows(righe)
    json.dump({"repository": f"https://github.com/{REPO}", "generato": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "documenti": righe, "esclusi": [{k: e.get(k) for k in ("iniziativa", "sha256", "url_originale", "motivo")} for e in P["esclusi"]]},
              open(Path(a.out) / "manifest.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"manifest: {len(righe)} righe, senza asset coincidente {mancano}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("passo", choices=["piano", "carica", "manifest"])
    ap.add_argument("--radice", default=str(Path(__file__).resolve().parent.parent.parent))
    ap.add_argument("--archivio", default=os.path.expanduser("~/analisi-spesa-ict/archivio"))
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    {"piano": piano, "carica": carica, "manifest": manifest}[a.passo](a)
