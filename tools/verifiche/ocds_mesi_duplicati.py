"""Verifica D14: mesi OCDS diversi che servono lo stesso contenuto. Confronto byte per byte dell intero file
fra ogni mese e il primo del suo gruppo (stessa dimensione). Uso: python tools/verifiche/ocds_mesi_duplicati.py"""
import glob, os, json, collections, itertools
B = "archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/ocds/filesystem/bulk/"
def diff(a, b, blocco=1 << 20):
    n = 0; pos = []
    with open(a, "rb") as fa, open(b, "rb") as fb:
        off = 0
        while True:
            x, y = fa.read(blocco), fb.read(blocco)
            if not x and not y: break
            if x != y:
                for i, (c, d) in enumerate(zip(x, y)):
                    if c != d: n += 1; pos.append(off + i) if len(pos) < 10 else None
            off += len(x)
    return n, pos
per_dim = collections.defaultdict(list)
for p in sorted(glob.glob(B + "*/*.json")):
    per_dim[os.path.getsize(p)].append(p)
gruppi = []
for dim, ps in sorted(per_dim.items()):
    if len(ps) < 2: continue
    ref = ps[0]
    confronti = []
    for p in ps[1:]:
        n, pos = diff(ref, p)
        confronti.append({"mese": p[len(B):-5], "byte_diversi": n, "posizioni": pos})
    gruppi.append({"byte": dim, "riferimento": ref[len(B):-5], "confronti": confronti})
mesi = len(glob.glob(B + "*/*.json"))
out = {"mesi_archiviati": mesi, "dimensioni_distinte": len(per_dim), "gruppi": gruppi}
json.dump(out, open("lavoro/verifica_ocds_mesi_duplicati.json", "w"), indent=1)
print(json.dumps(out, indent=1))
