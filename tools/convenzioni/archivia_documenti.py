"""#62, passo 3b: archivia i documenti pubblici delle iniziative, in ordine di valore, con tools/archivia.py.

Legge report/convenzioni/database/censimento.csv (ordine) e consip/<iniziativa>.json (URL dei documenti).
Idempotente e ripartibile: archivia.py salta cio' che e' invariato. Alla fine (e ogni 20 file) riscrive l'indice
versionato report/convenzioni/database/archiviati.jsonl dal manifest dell'archivio (url, sha256, data, dimensione, e
per gli zip l'elenco dei file contenuti), cosi' la base dati si ricostruisce da un clone pulito senza l'archivio.
Uso: python tools/convenzioni/archivia_documenti.py [--max-mb 200] [--solo-indice]"""
import csv, json, sys, zipfile
from pathlib import Path
import requests

R = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(R / "tools"))
import archivia as A  # noqa: E402
A.PAUSA_S = 5.0  # ritmo basso (#62)

DB = R / "report/convenzioni/database"


def urls_da_archiviare():
    ordine = []
    for r in csv.DictReader(open(DB / "censimento.csv", encoding="utf-8")):
        if r["iniziativa"] not in ordine:
            ordine.append(r["iniziativa"])
    for ini in ordine:
        p = DB / "consip" / f"{ini}.json"
        if not p.exists():
            continue
        e = json.loads(p.read_text(encoding="utf-8"))
        for pg in e.get("pagine", []):
            if pg.get("cita_chiave"):
                for d in pg["documenti"]:
                    yield ini, d["url"]


def indice(url_validi):
    ultimi = {}
    if A.MANIFEST.exists():
        for l in open(A.MANIFEST, encoding="utf-8"):
            try:
                m = json.loads(l)
            except ValueError:
                continue
            if m.get("url") in url_validi and m.get("sha256") and m.get("esito") in ("nuovo", "invariato", "aggiornato"):
                ultimi[m["url"]] = m
    with open(DB / "archiviati.jsonl", "w", encoding="utf-8") as f:
        for u in sorted(ultimi):
            m = ultimi[u]
            rec = {"url": u, "sha256": m["sha256"], "acquisito": m.get("acquisito"), "byte": m.get("dimensione")}
            b = A.percorso_blob(m["sha256"])
            if u.lower().endswith(".zip") and b.exists():
                try:
                    rec["contenuto"] = [i.filename for i in zipfile.ZipFile(b).infolist() if not i.is_dir()]
                except zipfile.BadZipFile:
                    rec["contenuto"] = None
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return len(ultimi)


def main():
    args = sys.argv[1:]
    max_mb = float(args[args.index("--max-mb") + 1]) if "--max-mb" in args else 200.0
    lista = list(urls_da_archiviare())
    validi = {u for _, u in lista}
    if "--solo-indice" not in args:
        s = requests.Session(); s.headers["User-Agent"] = A.UA
        tot = 0.0
        for k, (ini, u) in enumerate(lista):
            if tot > max_mb:
                print("tetto di MB raggiunto: si riprende al prossimo giro"); break
            r = A.archivia(s, u)
            tot += (r.get("dimensione") or 0) / 1e6 if r.get("esito") == "nuovo" else 0
            print(ini, r.get("esito"), u[-90:], flush=True)
            if k % 20 == 19:
                indice(validi)
    print(indice(validi), "documenti nell'indice")


if __name__ == "__main__":
    main()
