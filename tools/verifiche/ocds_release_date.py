"""#46 (P04) OCDS: release.date conforme? Misura su tutto il mirror bulk (ogni mese archiviato), due vie indipendenti.

Via 1: espressione regolare dello schema OCDS 1.1 (date-time RFC 3339: AAAA-MM-GGThh:mm:ss[.frazione](Z|±hh:mm)).
Via 2: parser standard di Python (datetime.fromisoformat, che dal 3.11 accetta ISO 8601), con «T» e fuso obbligatori.
Per ogni mese: release, release.date vuota/assente, conformi per via 1 e via 2, forme più frequenti (cifre -> 9),
sha256 del file dal manifest dell'archivio (nessun ricalcolo: il file è un hardlink al blob content-addressed).
Il risultato per mese si scrive man mano (ripartibile: i mesi già fatti si saltano).
Uso (server): nice python tools/verifiche/ocds_release_date.py -> esiti/<oggi>/ocds/release-date.json"""
import json, os, re, sys, glob, datetime, collections
from pathlib import Path
import ijson

R = Path(__file__).resolve().parents[2]
BASE = Path(os.environ.get("SPESAICT_BASE", R))
URL = "https://dati.anticorruzione.it/opendata/download/dataset/ocds/filesystem/bulk/"
B = BASE / "archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/ocds/filesystem/bulk"
RX = re.compile(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d+)?(Z|[+-]\d\d:\d\d)")
O = R / "esiti" / str(datetime.date.today()) / "ocds"; O.mkdir(parents=True, exist_ok=True)
PARZ = O / "release-date-mesi.jsonl"


def via2(s):
    if "T" not in s: return False
    try: d = datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError: return False
    return d.tzinfo is not None


def sha():
    m = {}
    for l in open(BASE / "archivio/manifest.jsonl", encoding="utf-8"):
        if "/ocds/filesystem/bulk/" in l:
            j = json.loads(l)
            if j.get("sha256"): m[j["url"]] = j["sha256"]
    return m


def mese(p):
    c = collections.Counter(); forme = collections.Counter(); es = {}
    with open(p, "rb") as f:
        for pre, ev, v in ijson.parse(f):
            if pre == "releases.item" and ev == "start_map": c["release"] += 1; c["_d"] = 0
            elif pre == "releases.item.date":
                c["_d"] = 1; s = v or ""
                if not s: c["vuota"] += 1; continue
                a, b = bool(RX.fullmatch(s)), via2(s)
                c["via1_ok"] += a; c["via2_ok"] += b; c["discordi"] += a != b
                fm = re.sub(r"\d", "9", s); forme[fm] += 1; es.setdefault(fm, s)
            elif pre == "releases.item" and ev == "end_map" and not c["_d"]: c["assente"] += 1
    c.pop("_d", None)
    return {**c, "forme": [[f, n, es[f]] for f, n in forme.most_common(5)]}


def main():
    fatti = {json.loads(l)["mese"] for l in open(PARZ, encoding="utf-8")} if PARZ.exists() else set()
    hs = sha()
    for p in sorted(glob.glob(str(B / "*/*.json"))):
        m = p[len(str(B)) + 1:-5]
        if m in fatti: continue
        r = {"mese": m, "url": URL + m + ".json", "sha256": hs.get(URL + m + ".json"), **mese(p)}
        open(PARZ, "a", encoding="utf-8").write(json.dumps(r, ensure_ascii=False) + "\n"); print(m, r["release"], r.get("via1_ok", 0), flush=True)
    rr = [json.loads(l) for l in open(PARZ, encoding="utf-8")]
    tot = collections.Counter()
    for r in rr:
        for k in ("release", "vuota", "assente", "via1_ok", "via2_ok", "discordi"): tot[k] += r.get(k, 0)
    per_anno = collections.defaultdict(collections.Counter)
    for r in rr:
        for k in ("release", "vuota", "assente", "via1_ok"): per_anno[r["mese"][:4]][k] += r.get(k, 0)
    out = {"generato": str(datetime.date.today()), "mesi": len(rr), "totale": dict(tot),
           "quota_conforme_via1": round(tot["via1_ok"] / tot["release"], 6) if tot["release"] else None,
           "per_anno": {a: dict(v) for a, v in sorted(per_anno.items())},
           "primo_mese_non_conforme": next((r["mese"] for r in sorted(rr, key=lambda x: x["mese"]) if r.get("via1_ok", 0) < r["release"] - r.get("vuota", 0) - r.get("assente", 0)), None),
           "mesi_dettaglio": sorted(rr, key=lambda x: x["mese"])}
    json.dump(out, open(O / "release-date.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({k: out[k] for k in ("mesi", "totale", "quota_conforme_via1", "per_anno", "primo_mese_non_conforme")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
