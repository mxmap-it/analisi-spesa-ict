#!/usr/bin/env python3
"""Ingressi di lavoro/ che l'imbuto legge ma che non stanno nel mirror ANAC (M12, ripetibilità da un clone pulito).

Registro: config/ingressi-lavoro.yaml (percorso, sha256, byte, chi lo usa, come si ripristina, come si rigenera).
Due vie di conservazione, scelte per dimensione:
  git       file piccoli, compressi in modo deterministico in dati/ingressi/ (gzip senza nome né data; i pacchetti L3
            come tar ordinato con data, proprietario e permessi fissi), quindi presenti in ogni clone;
  archivio  file grandi (lavoro/pvl/cig_link.csv, 406 MB): blob content-addressed in archivio/blobs/sha256/ (append-only,
            riga nel manifest, vista in archivio/mirror/_derivati/<percorso>), più la ricetta per rigenerarlo dalle
            pagine dell'API PVL già archiviate (indice delle pagine con sha256 versionato in dati/ingressi/).

Uso:
  python3 tools/ingressi_lavoro.py verifica     # ogni ingresso c'è e ha lo sha256 del registro (esce con 1 se no)
  python3 tools/ingressi_lavoro.py ripristina   # rimette in lavoro/ ciò che manca (da git o dall'archivio), poi verifica
  python3 tools/ingressi_lavoro.py congela      # (server) copia gli ingressi attuali in git/archivio e riscrive il registro
"""
import gzip, hashlib, io, json, os, shutil, sys, tarfile
from datetime import datetime, timezone
from pathlib import Path

import yaml

R = Path(__file__).resolve().parents[1]
REG = R / "config/ingressi-lavoro.yaml"
GIT = R / "dati/ingressi"
sys.path.insert(0, str(R / "tools"))

# percorso in lavoro/ -> (via, chi lo usa, come si rigenera)
INGRESSI = {
    "lavoro/pvl/cig_link.csv": ("archivio", "tools/verifiche/imbuto_strati.py --rigenera (link PVL per strato)",
                                "tools/acquisizione/pvl_avvisi.py estrai > lavoro/pvl/link_cig.csv (dalle pagine API PVL archiviate, "
                                "elenco con sha256 in dati/ingressi/lavoro/pvl/indice.jsonl.gz), poi tools/acquisizione/pvl_analisi.py "
                                "(legge anche lavoro/cig_completo e l'anagrafica delle stazioni appaltanti): lo sha256 può cambiare se "
                                "cambiano i dataset ANAC, quindi per riprodurre i numeri si ripristina il blob"),
    "lavoro/pvl/indice.jsonl": ("git", "tools/acquisizione/pvl_avvisi.py (indice delle pagine API PVL, una riga per pagina con sha256 del blob)",
                                "scaricamento del 3-4/11/2026 (pvl_avvisi.py scarica): non si rigenera, si conserva"),
    "lavoro/convenzioni/attuativi.csv": ("git", "tools/verifiche/imbuto_licenze.py (attuativi delle convenzioni)",
                                         "derivato del 3/11/2026 dai CIG ANAC con cig_accordo_quadro delle convenzioni ICT: si conserva"),
    "lavoro/raffinamento/pacchetti": ("git-tar", "tools/llm/raffinamento.py esito (ingresso di L3: importo e oggetto)",
                                      "raffinamento.py prepara-l3 (idempotente, aggiunge pacchetti): i pacchetti già letti dal modello "
                                      "non si rigenerano, si conservano"),
}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def sha_cartella(d):
    """sha256 dei file della cartella concatenati in ordine di nome (come ripetibilita_confronta.py)."""
    h = hashlib.sha256()
    for p in sorted(Path(d).glob("d*.jsonl")):
        h.update(p.read_bytes())
    return h.hexdigest(), len(list(Path(d).glob("d*.jsonl")))


def gz_deterministico(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(src, "rb") as fi, open(dst, "wb") as fo:
        with gzip.GzipFile(filename="", mode="wb", fileobj=fo, mtime=0, compresslevel=9) as g:
            shutil.copyfileobj(fi, g)


def tar_deterministico(cartella, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w", format=tarfile.PAX_FORMAT) as t:
        for p in sorted(Path(cartella).glob("d*.jsonl")):
            ti = tarfile.TarInfo(p.name)
            dati = p.read_bytes()
            ti.size, ti.mtime, ti.mode, ti.uid, ti.gid, ti.uname, ti.gname = len(dati), 0, 0o644, 0, 0, "", ""
            t.addfile(ti, io.BytesIO(dati))
    with open(dst, "wb") as fo, gzip.GzipFile(filename="", mode="wb", fileobj=fo, mtime=0, compresslevel=9) as g:
        g.write(buf.getvalue())


def congela():
    import archivia as A
    reg = {"descrizione": "Ingressi di lavoro/ letti dall'imbuto e fuori dal mirror ANAC (M12). Generato da tools/ingressi_lavoro.py congela.",
           "ingressi": []}
    for perc, (via, usato, rigenera) in INGRESSI.items():
        src = R / perc
        e = {"percorso": perc, "via": via, "usato_da": usato, "rigenera": rigenera}
        if via == "git-tar":
            e["sha256_concatenati"], e["file"] = sha_cartella(src)
            dst = GIT / (perc + ".tar.gz")
            tar_deterministico(src, dst)
            e["copia"] = str(dst.relative_to(R)); e["sha256_copia"] = sha(dst)
        else:
            e["sha256"], e["byte"] = sha(src), src.stat().st_size
            e["data_file"] = datetime.fromtimestamp(src.stat().st_mtime, timezone.utc).date().isoformat()
            if via == "git":
                dst = GIT / (perc + ".gz")
                gz_deterministico(src, dst)
                e["copia"] = str(dst.relative_to(R)); e["sha256_copia"] = sha(dst)
            else:  # archivio content-addressed, mai sovrascritto
                blob = A.percorso_blob(e["sha256"])
                if not blob.exists():
                    part = A.ROOT / "tmp" / (e["sha256"] + ".part")
                    part.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(src, part)
                    blob.parent.mkdir(parents=True, exist_ok=True)
                    os.replace(part, blob)
                    esito = "nuovo"
                else:
                    esito = "invariato"
                vista = A.collega_vista(blob, A.ROOT / "mirror/_derivati" / perc)
                A.scrivi_manifest({"acquisito": e["data_file"], "archiviato": A.adesso(), "url": "derivato:" + perc,
                                   "via": "derivato-locale", "nota": "ingresso dell'imbuto fuori dal mirror (M12): " + usato,
                                   "esito": esito, "sha256": e["sha256"], "dimensione": e["byte"], "verifica": "hash",
                                   "mirror": str(vista.relative_to(A.ROOT))})
                e["blob"] = str(blob.relative_to(R)); e["vista"] = str(vista.relative_to(R))
        reg["ingressi"].append(e)
        print(via, perc, e.get("sha256") or e.get("sha256_concatenati"))
    REG.write_text(yaml.safe_dump(reg, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")


def stato(e):
    p = R / e["percorso"]
    if e["via"] == "git-tar":
        if not p.is_dir(): return "manca"
        s, n = sha_cartella(p)
        return "ok" if (s, n) == (e["sha256_concatenati"], e["file"]) else "diverso"
    if not p.exists(): return "manca"
    return "ok" if sha(p) == e["sha256"] else "diverso"


def verifica():
    reg = yaml.safe_load(REG.read_text(encoding="utf-8"))
    esiti = {e["percorso"]: stato(e) for e in reg["ingressi"]}
    print(json.dumps(esiti, indent=1, ensure_ascii=False))
    return all(v == "ok" for v in esiti.values())


def ripristina():
    reg = yaml.safe_load(REG.read_text(encoding="utf-8"))
    for e in reg["ingressi"]:
        s = stato(e)
        if s == "ok": continue
        p = R / e["percorso"]
        if s == "diverso":  # mai sovrascrivere un file di lavoro diverso: si segnala
            print("DIVERSO, non tocco:", e["percorso"]); continue
        if e["via"] == "git-tar":
            p.mkdir(parents=True, exist_ok=True)
            with gzip.open(R / e["copia"]) as g, tarfile.open(fileobj=g, mode="r|") as t:
                t.extractall(p, filter="data")
        elif e["via"] == "git":
            p.parent.mkdir(parents=True, exist_ok=True)
            with gzip.open(R / e["copia"]) as g, open(p, "wb") as fo:
                shutil.copyfileobj(g, fo)
        else:
            blob = R / e["blob"]
            if not blob.exists():
                print("MANCA il blob", e["blob"], "-> rigenerare:", e["rigenera"]); continue
            p.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(blob, p)
        print("ripristinato", e["percorso"])
    return verifica()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "verifica"
    if cmd == "congela":
        congela(); sys.exit(0 if verifica() else 1)
    sys.exit(0 if {"verifica": verifica, "ripristina": ripristina}[cmd]() else 1)
