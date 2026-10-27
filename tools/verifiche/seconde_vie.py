"""Seconde vie indipendenti per le schede del registro ANAC (#33).

Codice scritto da capo, diverso da quello che ha prodotto i numeri pubblicati, e dove possibile
su dati diversi (un altro mese OCDS). Uso: python tools/verifiche/seconde_vie.py
Esito: lavoro/seconde_vie.json
"""
import csv
import io
import json
import os
import zipfile
from datetime import datetime
from pathlib import Path

import ijson

BASE = Path(__file__).resolve().parents[2]
ROOT = Path(os.environ.get("ARCHIVIO_ROOT", BASE / "archivio"))
D = ROOT / "mirror" / "dati.anticorruzione.it" / "opendata" / "download" / "dataset"
MESE = "2024/10"  # mese OCDS con contenuto unico (non fa parte dei gruppi duplicati di P01)
csv.field_size_limit(1 << 30)


def p11_dimensioni():
    """Dimensione dichiarata dal catalogo e Content-Length contro i byte effettivamente archiviati."""
    archiviati = {}
    for riga in (ROOT / "manifest.jsonl").read_text(encoding="utf-8").splitlines():
        d = json.loads(riga)
        if d.get("sha256"):
            archiviati[d["url"]] = d.get("byte")
    dich = serv = arch = n = 0
    for riga in (BASE / "config" / "anac-risorse.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(riga)
        b = archiviati.get(r["url"])
        if b and r.get("dim_dichiarata") and r.get("dim_reale"):
            dich += r["dim_dichiarata"]; serv += r["dim_reale"]; arch += b; n += 1
    return {"risorse": n, "dichiarati_gb": round(dich / 1e9, 2), "content_length_gb": round(serv / 1e9, 2),
            "archiviati_gb": round(arch / 1e9, 2), "rapporto_dichiarato_su_archiviato": round(dich / arch, 2)}


def p16_csv_rigoroso():
    """Lettore csv di Python in modalità strict sui delta CIG 2026."""
    out = {}
    for z in sorted((D / "cig" / "filesystem").glob("*-cig_csv.zip")):
        zf = zipfile.ZipFile(z)
        testo = io.TextIOWrapper(zf.open(next(i for i in zf.namelist() if i.endswith(".csv"))), encoding="utf-8")
        con_escape = sum(1 for l in testo if '\\"' in l)
        testo = io.TextIOWrapper(zf.open(next(i for i in zf.namelist() if i.endswith(".csv"))), encoding="utf-8")
        rd = csv.reader(testo, delimiter=";", quotechar='"', strict=True)
        errori = righe = 0
        while True:
            try:
                riga = next(rd)
            except StopIteration:
                break
            except csv.Error:
                errori += 1
                continue
            righe += 1
            if len(riga) != 61 and righe > 1:
                errori += 1
        out[z.name] = {"righe_lette": righe, "errori_o_colonne_sbagliate": errori, "righe_con_escape": con_escape}
    return out


def p14_cup_nd():
    """Valori 'ND' nel campo CUP, contati con il modulo csv."""
    zf = zipfile.ZipFile(D / "cup" / "filesystem" / "cup_csv.zip")
    rd = csv.DictReader(io.TextIOWrapper(zf.open(next(i for i in zf.namelist() if i.endswith(".csv"))), encoding="utf-8-sig"), delimiter=";")
    tot = nd = 0
    for r in rd:
        tot += 1
        if (r.get("CUP") or r.get("cup") or "").strip().upper() == "ND":
            nd += 1
    return {"righe": tot, "cup_nd": nd}


def data_valida(s):
    try:
        datetime.fromisoformat(s.replace("Z", "+00:00"))
        return "T" in s and " " not in s
    except (ValueError, AttributeError):
        return False


def p03_p04_p05_ocds():
    """Un altro mese OCDS: quota di award con fornitore, date valide, copertura rispetto ai tabellari."""
    award, con_forn, rel, date_ok, vuote = set(), 0, 0, 0, 0
    with (D / "ocds" / "filesystem" / "bulk" / f"{MESE}.json").open("rb") as f:
        for r in ijson.items(f, "releases.item"):
            rel += 1
            d = r.get("date")
            if not d:
                vuote += 1
            elif data_valida(d):
                date_ok += 1
            for a in r.get("awards") or []:
                award.add(str(a.get("id")))
                if a.get("suppliers"):
                    con_forn += 1
    mese = MESE.replace("/", "-")
    zf = zipfile.ZipFile(D / "aggiudicazioni" / "filesystem" / "aggiudicazioni_csv.zip")
    rd = csv.DictReader(io.TextIOWrapper(zf.open(next(i for i in zf.namelist() if i.endswith(".csv"))), encoding="utf-8-sig"), delimiter=";")
    tab = {r["id_aggiudicazione"] for r in rd if (r.get("data_aggiudicazione_definitiva") or "").startswith(mese)}
    return {"mese": MESE, "release": rel, "release_data_valida": date_ok, "release_data_vuota": vuote,
            "award": len(award), "award_con_fornitore": con_forn,
            "pct_award_con_fornitore": round(con_forn / len(award) * 100, 1) if award else None,
            "tabellari_aggiudicati_nel_mese": len(tab), "di_cui_in_ocds": len(tab & award),
            "pct_copertura": round(len(tab & award) / len(tab) * 100, 1) if tab else None}


if __name__ == "__main__":
    esito = {}
    for nome, f in [("P11", p11_dimensioni), ("P16", p16_csv_rigoroso), ("P14", p14_cup_nd), ("P03_P04_P05", p03_p04_p05_ocds)]:
        try:
            esito[nome] = f()
        except Exception as e:  # una verifica rotta non deve fermare le altre
            esito[nome] = {"errore": repr(e)}
        print(nome, json.dumps(esito[nome], ensure_ascii=False)[:400], flush=True)
    (BASE / "lavoro").mkdir(exist_ok=True)
    (BASE / "lavoro" / "seconde_vie.json").write_text(json.dumps(esito, indent=1, ensure_ascii=False), encoding="utf-8")
