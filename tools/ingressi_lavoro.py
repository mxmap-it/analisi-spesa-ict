#!/usr/bin/env python3
"""Ingressi di lavoro/ che l'imbuto legge ma che non stanno nel mirror ANAC (M12, ripetibilità da un clone pulito).

Registro: config/ingressi-lavoro.yaml (percorso, sha256, byte, chi lo usa, come si ripristina, come si rigenera).
Due vie di conservazione, scelte per dimensione:
  git       file piccoli, compressi in modo deterministico in dati/ingressi/ (gzip senza nome né data; i pacchetti L3
            come tar ordinato con data, proprietario e permessi fissi), quindi presenti in ogni clone;
  archivio  file grandi (lavoro/pvl/cig_link.csv, 406 MB): blob content-addressed in archivio/blobs/sha256/ (append-only,
            riga nel manifest, vista in archivio/mirror/_derivati/<percorso>), più la ricetta per rigenerarlo dalle
            pagine dell'API PVL già archiviate (indice delle pagine con sha256 versionato in dati/ingressi/).

Estensione del 20/11/2026 (#81, riproducibilità di TUTTE le fonti, inventario statico in config/fonti-verifiche.yaml):
  archivio-tar  cartelle (attribuzioni, delta ANAC estratti, pagine BDAP e TED, completamento mirror): tar deterministico
                di tutti i file in ordine di percorso, conservato come blob content-addressed; si ripristina estraendo;
  impronta      file o cartelle troppo grandi da duplicare e rigenerabili dal mirror con una ricetta (cig_completo,
                11 GB, da tools/anac_integrita.py): si registra lo sha256 di ogni file in dati/ingressi/<percorso>.sha256,
                così la verifica dice se il file rigenerato è identico.

Uso:
  python3 tools/ingressi_lavoro.py verifica     # ogni ingresso c'è e ha lo sha256 del registro (esce con 1 se no)
  python3 tools/ingressi_lavoro.py ripristina   # rimette in lavoro/ ciò che manca (da git o dall'archivio), poi verifica
  python3 tools/ingressi_lavoro.py congela [percorsi]  # (server) copia gli ingressi attuali (o solo quelli indicati) e riscrive il registro
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
                                "elenco con sha256 in dati/ingressi/pvl/indice.jsonl.gz), poi tools/acquisizione/pvl_analisi.py "
                                "(legge anche lavoro/cig_completo e l'anagrafica delle stazioni appaltanti): lo sha256 può cambiare se "
                                "cambiano i dataset ANAC, quindi per riprodurre i numeri si ripristina il blob"),
    "lavoro/pvl/indice.jsonl": ("git", "tools/acquisizione/pvl_avvisi.py (indice delle pagine API PVL, una riga per pagina con sha256 del blob)",
                                "scaricamento del 3-4/11/2026 (pvl_avvisi.py scarica): non si rigenera, si conserva"),
    "lavoro/convenzioni/attuativi.csv": ("git", "tools/verifiche/imbuto_licenze.py (attuativi delle convenzioni)",
                                         "derivato del 3/11/2026 dai CIG ANAC con cig_accordo_quadro delle convenzioni ICT: si conserva"),
    "lavoro/raffinamento/pacchetti": ("git-tar", "tools/llm/raffinamento.py esito (ingresso di L3: importo e oggetto)",
                                      "raffinamento.py prepara-l3 (idempotente, aggiunge pacchetti): i pacchetti già letti dal modello "
                                      "non si rigenerano, si conservano"),
    # ---- #81 (20/11/2026): ingressi critici dall'inventario config/fonti-verifiche.yaml
    "lavoro/imbuto/ict.csv": ("archivio", "circa 45 strumenti di tools/verifiche/ (imbuto 0.3.4, una riga per CIG ICT)",
                              "tools/analisi/imbuto.py (IMBUTO_OUT=lavoro/imbuto) dal mirror ANAC; la prova 0.3.4 lo rifà in tools/verifiche/ripetibilita.sh, passo a"),
    "lavoro/imbuto/stati-finali.csv.gz": ("git", "tools/verifiche/inhouse_vista.py e pagine del cloud in proprio",
                                          "tools/verifiche/imbuto_spostamenti.py AAAA-MM-GG"),
    "lavoro/inhouse/cig-cf.csv.gz": ("git", "tools/verifiche/datacenter_proprio.py, inhouse_vista.py (#82)",
                                     "tools/verifiche/inhouse_cf.py (da ict.csv, cig_completo e aggiudicatari del mirror)"),
    "lavoro/smartcig/ict.csv": ("archivio", "tools/verifiche/imbuto_smartcig.py (M6)", "tools/verifiche/imbuto_smartcig.py --rigenera dal mirror SmartCIG"),
    "lavoro/zenodo-10007545/cpv_5M.csv.gz": ("archivio", "tools/verifiche/zenodo_test.py",
                                             "scaricato a mano da Zenodo (record 10007545): non si rigenera, si conserva"),
    "lavoro/rivenditori/gleif-it.json": ("archivio", "tools/verifiche/rivenditori_*.py", "estratto dalla golden copy GLEIF del mirror (goldencopy.gleif.org)"),
    "lavoro/trasparenza/stato.sqlite": ("archivio", "pagine sulla trasparenza (censimento delle sezioni AT)",
                                        "tools/trasparenza/censimento.py (raccolta dal vivo: non identica se rifatta, si conserva)"),
    "lavoro/residuo-s6/out/esiti.jsonl": ("archivio", "tools/verifiche/residuo_s6_*.py (livello L4)",
                                          "tools/acquisizione/residuo_s6.sh -> at_cig.py (raccolta dal vivo, pagine in archivio): si conserva"),
    "lavoro/residuo-s6/l4-js/enti.jsonl": ("git", "tools/verifiche/l4js_url_at.py", "tools/acquisizione/at_cig_js.py (raccolta dal vivo): si conserva"),
    "lavoro/l190-campione/stato.jsonl": ("git", "tools/verifiche/l190_campione.py", "raccolta dal vivo dei dataset L. 190 (pagine in archivio): si conserva"),
    "lavoro/pnrr12/ocds-1.2.jsonl": ("git", "tools/verifiche/pnrr12_prodotto.py", "tools/verifiche/pnrr12_ocds.py dal mirror OCDS"),
    "lavoro/pvl/link_cig.csv": ("archivio", "tools/acquisizione/residuo_s6_ingresso.py, pvl_analisi.py",
                                "tools/acquisizione/pvl_avvisi.py estrai (dalle pagine API PVL archiviate)"),
    "lavoro/attribuzione": ("archivio-tar", "lente_cieco5-7, regole_v4x_confronto (attribuzioni per anno)",
                            "tools/analisi/attribuisci_provider.py <anni> (dipende dalla versione delle regole)"),
    "lavoro/cig_delta": ("archivio-tar", "tools/verifiche/ted_cig.py, pnrr_flag.py",
                         "estrazione dei delta mensili ANAC dal mirror (strumento non ritrovato: origine da documentare)"),
    "lavoro/bdap-pagine": ("archivio-tar", "tools/verifiche/mirror_fonti.py (via lavoro/mirror-completamento)",
                           "tools/acquisizione/bdap_metadati.sh (curl dal vivo, non archiviato: si conserva)"),
    "lavoro/ted-v2/pagine": ("archivio-tar", "tools/verifiche/ted_*.py", "tools/acquisizione/ted_l2.py (risposte API TED, anche in archivio)"),
    "lavoro/mirror-completamento": ("archivio-tar", "tools/verifiche/mirror_fonti.py", "da lavoro/bdap-pagine e dal manifest"),
    "lavoro/cig_completo": ("impronta", "imbuto 0.3.4 (prepara), inhouse_cf.py, attuativi",
                            "tools/anac_integrita.py (estrae i CSV dagli zip del mirror ANAC): 11 GB, si rigenera e si confronta con le impronte"),
}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def tutti(d):
    return sorted(p for p in Path(d).rglob("*") if p.is_file() and p.suffix != ".log")  # i log non sono ingressi


def tar_tutti(cartella, dst):
    """tar deterministico di tutti i file della cartella (percorsi relativi, ordine di nome, metadati fissi), gzip senza data."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(dst, "wb") as fo, gzip.GzipFile(filename="", mode="wb", fileobj=fo, mtime=0, compresslevel=6) as g, \
            tarfile.open(fileobj=g, mode="w|", format=tarfile.PAX_FORMAT) as t:
        for p in tutti(cartella):
            ti = tarfile.TarInfo(str(p.relative_to(cartella)))
            ti.size, ti.mtime, ti.mode, ti.uid, ti.gid, ti.uname, ti.gname = p.stat().st_size, 0, 0o644, 0, 0, "", ""
            with open(p, "rb") as f:
                t.addfile(ti, f)


def impronte(d):
    return {str(p.relative_to(d)): sha(p) for p in tutti(d)}


def archivia_blob(src, perc, data, usato, A):
    s256 = sha(src)
    blob = A.percorso_blob(s256)
    if not blob.exists():
        part = A.ROOT / "tmp" / (s256 + ".part")
        part.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, part)
        blob.parent.mkdir(parents=True, exist_ok=True)
        os.replace(part, blob)
        esito = "nuovo"
    else:
        esito = "invariato"
    vista = A.collega_vista(blob, A.ROOT / "mirror/_derivati" / perc)
    A.scrivi_manifest({"acquisito": data, "archiviato": A.adesso(), "url": "derivato:" + perc, "via": "derivato-locale",
                       "nota": "ingresso fuori dal mirror (M12, #81): " + usato, "esito": esito, "sha256": s256,
                       "dimensione": src.stat().st_size, "verifica": "hash", "mirror": str(vista.relative_to(A.ROOT))})
    return s256, blob, vista


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


def congela(solo=()):
    """solo: percorsi da ricongelare (gli altri restano come nel registro): per gli ingressi che cambiano spesso,
    come lavoro/imbuto/stati-finali.csv.gz mentre il raffinamento L4 aggiunge esiti."""
    import archivia as A
    vecchi = {e["percorso"]: e for e in yaml.safe_load(REG.read_text(encoding="utf-8"))["ingressi"]} if solo and REG.exists() else {}
    reg = {"descrizione": "Ingressi di lavoro/ letti dall'imbuto e fuori dal mirror ANAC (M12). Generato da tools/ingressi_lavoro.py congela.",
           "ingressi": []}
    for perc, (via, usato, rigenera) in INGRESSI.items():
        if solo and perc not in solo and perc in vecchi:
            reg["ingressi"].append(vecchi[perc])
            continue
        src = R / perc
        e = {"percorso": perc, "via": via, "usato_da": usato, "rigenera": rigenera}
        if via == "archivio-tar":
            e["impronte"] = str((GIT / (perc.removeprefix("lavoro/") + ".sha256")).relative_to(R))
            imp = impronte(src)
            (R / e["impronte"]).parent.mkdir(parents=True, exist_ok=True)
            (R / e["impronte"]).write_text("".join(f"{v}  {k}\n" for k, v in imp.items()), encoding="utf-8")
            e["file"] = len(imp)
            tmp = R / "lavoro/ingressi-tar" / (perc.removeprefix("lavoro/").replace("/", "_") + ".tar.gz")
            tar_tutti(src, tmp)
            e["sha256_tar"], blob, vista = archivia_blob(tmp, perc + ".tar.gz", datetime.now(timezone.utc).date().isoformat(), usato, A)
            e["blob"] = str(blob.relative_to(R)); e["vista"] = str(vista.relative_to(R))
            tmp.unlink()
        elif via == "impronta":
            e["impronte"] = str((GIT / (perc.removeprefix("lavoro/") + ".sha256")).relative_to(R))
            imp = impronte(src)
            (R / e["impronte"]).parent.mkdir(parents=True, exist_ok=True)
            (R / e["impronte"]).write_text("".join(f"{v}  {k}\n" for k, v in imp.items()), encoding="utf-8")
            e["file"], e["byte"] = len(imp), sum(p.stat().st_size for p in tutti(src))
        elif via == "git-tar":
            e["sha256_concatenati"], e["file"] = sha_cartella(src)
            dst = GIT / (perc.removeprefix("lavoro/") + ".tar.gz")  # non «lavoro/»: .gitignore la esclude a ogni livello
            tar_deterministico(src, dst)
            e["copia"] = str(dst.relative_to(R)); e["sha256_copia"] = sha(dst)
        else:
            e["sha256"], e["byte"] = sha(src), src.stat().st_size
            e["data_file"] = datetime.fromtimestamp(src.stat().st_mtime, timezone.utc).date().isoformat()
            if via == "git":
                dst = GIT / (perc.removeprefix("lavoro/") + ".gz")
                gz_deterministico(src, dst)
                e["copia"] = str(dst.relative_to(R)); e["sha256_copia"] = sha(dst)
            else:  # archivio content-addressed, mai sovrascritto
                _, blob, vista = archivia_blob(src, perc, e["data_file"], usato, A)
                e["blob"] = str(blob.relative_to(R)); e["vista"] = str(vista.relative_to(R))
        reg["ingressi"].append(e)
        print(via, perc, e.get("sha256") or e.get("sha256_concatenati") or e.get("sha256_tar") or e.get("file"), flush=True)
    REG.write_text(yaml.safe_dump(reg, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")


def stato(e):
    p = R / e["percorso"]
    if e["via"] in ("archivio-tar", "impronta"):
        if not p.is_dir(): return "manca"
        att = {l.split("  ", 1)[1].rstrip("\n"): l.split("  ", 1)[0] for l in (R / e["impronte"]).read_text(encoding="utf-8").splitlines(True)}
        return "ok" if impronte(p) == att else "diverso"
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
        if e["via"] == "impronta":
            print("MANCA", e["percorso"], "-> rigenerare:", e["rigenera"]); continue
        if e["via"] == "archivio-tar":
            blob = R / e["blob"]
            if not blob.exists():
                print("MANCA il blob", e["blob"]); continue
            p.mkdir(parents=True, exist_ok=True)
            with tarfile.open(blob, mode="r:gz") as t:
                t.extractall(p, filter="data")
        elif e["via"] == "git-tar":
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
        congela(tuple(sys.argv[2:])); sys.exit(0 if verifica() else 1)
    sys.exit(0 if {"verifica": verifica, "ripristina": ripristina}[cmd]() else 1)
