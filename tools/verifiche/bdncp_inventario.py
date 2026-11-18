#!/usr/bin/env python3
"""Inventario dei dataset BDNCP nel mirror ANAC (#74): per ogni dataset file, formati, byte, ultimo CSV,
campi, righe, CIG distinti, copertura dei CIG ICT dell'imbuto (lavoro/imbuto/ict.csv, strati S3-S6) e, per i
dataset con importi (stati-avanzamento, quadro-economico, aggiudicazioni), somme sui CIG ICT.
Uso dello strumento: grep sui sorgenti di tools/ (nome del dataset nel codice).
Lettura in streaming (zip -> csv), un dataset alla volta: niente caricamento di tutti i CIG in memoria
(solo l'insieme dei CIG ICT, ~0,6 M stringhe). Annuali cig-AAAA/smartcig-AAAA: solo file e byte.

Uso (SUL SERVER, nice, dopo free -g): .venv/bin/python tools/verifiche/bdncp_inventario.py
  -> esiti/<data>/bdncp/inventario.json + inventario.csv"""
import csv, glob, io, json, os, re, subprocess, time, zipfile, collections
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
D = BASE / "archivio/mirror/dati.anticorruzione.it/opendata/download/dataset"
csv.field_size_limit(1 << 30)


def f(x):
    try:
        return float((x or "").replace(",", "."))
    except ValueError:
        return 0.0


def ultimo_csv(d):
    z = sorted(glob.glob(str(d / "filesystem" / "*csv*.zip")), key=lambda p: (re.match(r"\d{8}", os.path.basename(p)) is not None, os.path.basename(p)))
    # preferisce l'ultimo mensile datato; se non ce ne sono, lo zip «pieno» senza data
    dat = [p for p in z if re.match(r"\d{8}", os.path.basename(p))]
    piena = [p for p in z if not re.match(r"\d{8}", os.path.basename(p))]
    return piena[-1] if piena else (dat[-1] if dat else None), dat


def main():
    ict = set()
    with open(BASE / "lavoro/imbuto/ict.csv", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["strato"].startswith(("S3", "S4", "S5", "S6")):  # 18/11: prima escludeva solo S1-S2, contando i padri AQ (S0)
                ict.add(r["cig"])
    uso = {}
    sorgenti = [p for p in glob.glob(str(BASE / "tools/**/*.py"), recursive=True) + glob.glob(str(BASE / "tools/**/*.sh"), recursive=True)
                if "__pycache__" not in p and "bdncp_inventario" not in p and "l190_campione" not in p]
    testi = {os.path.relpath(p, BASE / "tools"): open(p, encoding="utf-8", errors="replace").read() for p in sorgenti}
    out = {"ict_cig": len(ict), "dataset": {}}
    for d in sorted(D.iterdir()):
        nome = d.name
        files = [p for p in d.rglob("*") if p.is_file()]
        rec = {"file": len(files), "byte": sum(p.stat().st_size for p in files),
               "formati": sorted({re.sub(r".*_(csv|json|ttl|xml)(_logCsv)?\.(zip|csv)$", r"\1", p.name) for p in files if re.search(r"_(csv|json|ttl)", p.name)})}
        chiave = nome.replace("-v2", "")
        rec["usato_da"] = sorted(k for k, t in testi.items() if chiave in t and k not in ("censisci_anac.py", "mirror_anac.py", "stato_mirror.py", "indice_mirror.py", "pagine_mirror.py"))
        if re.match(r"(smart)?cig-\d{4}$", nome) or nome == "ocds":
            out["dataset"][nome] = rec
            continue
        z, mensili = ultimo_csv(d)
        rec["mensili_datati"] = [os.path.basename(p)[:8] for p in mensili]
        if not z:
            out["dataset"][nome] = rec
            continue
        rec["letto"] = os.path.basename(z)
        zf = zipfile.ZipFile(z)
        m = [n for n in zf.namelist() if n.endswith(".csv")][0]
        R = csv.DictReader(io.TextIOWrapper(zf.open(m), encoding="utf-8-sig", errors="replace"), delimiter=";")
        rec["campi"] = R.fieldnames
        n, cig, cig_ict = 0, set(), set()
        somme = collections.Counter()
        for r in R:
            n += 1
            c = (r.get("cig") or r.get("CIG") or "").strip().upper()
            if c:
                cig.add(c)
                if c in ict:
                    cig_ict.add(c)
                    if nome == "stati-avanzamento":
                        somme["importo_sal"] += f(r["importo_sal"])
                        somme["IMPORTO_CERT_PAGAMENTO"] += f(r["IMPORTO_CERT_PAGAMENTO"])
                        somme["righe_con_cert_pagamento"] += f(r["IMPORTO_CERT_PAGAMENTO"]) > 0
                    elif nome == "aggiudicazioni":
                        somme["importo_aggiudicazione"] += f(r["importo_aggiudicazione"])
                    elif nome == "fine-contratto":
                        somme["con_data_ultimazione"] += bool(r["data_effettiva_ultimazione"])
                    elif nome == "collaudo":
                        somme["con_regolare_esecuzione"] += bool(r["data_regolare_esec"])
        rec.update(righe=n, cig_distinti=len(cig), cig_ict=len(cig_ict),
                   quota_ict_coperti=round(len(cig_ict) / len(ict), 4) if ict else None)
        if somme:
            rec["somme_ict"] = {k: round(v, 2) for k, v in somme.items()}
        out["dataset"][nome] = rec
        print(nome, n, len(cig), len(cig_ict), flush=True)
    oggi = time.strftime("%Y-%m-%d")
    o = BASE / "esiti" / oggi / "bdncp"
    o.mkdir(parents=True, exist_ok=True)
    (o / "inventario.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(o / "inventario.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["dataset", "file", "byte", "righe", "cig_distinti", "cig_ict", "quota_ict", "usato_da", "campi"])
        for k, v in out["dataset"].items():
            w.writerow([k, v["file"], v["byte"], v.get("righe", ""), v.get("cig_distinti", ""), v.get("cig_ict", ""),
                        v.get("quota_ict_coperti", ""), " ".join(v["usato_da"]), "|".join(v.get("campi") or [])])


if __name__ == "__main__":
    main()
