#!/usr/bin/env python3
"""Rigenera la pagina pubblica del dataset delle società ICT pubbliche (#82) e copia i file scaricabili.

Ingressi: dati/inhouse/{societa-ict-pa.csv, riepilogo.json, opensource.csv, catalogo-riuso.csv, opensource-riepilogo.json}
Uscite:   sito/content/rendiconti/societa-ict-pubbliche.md (solo fra i marcatori GEN), sito/static/dati/inhouse/*

    python3 tools/pagina_inhouse.py
"""
import csv
import hashlib
import json
import os
import re
import shutil

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(R, "dati/inhouse")
ST = os.path.join(R, "sito/static/dati/inhouse")
PAG = os.path.join(R, "sito/content/rendiconti/societa-ict-pubbliche.md")
FILE = ["vista.md", "societa-ict-pa.csv", "opensource.csv", "catalogo-riuso.csv", "riepilogo.json", "opensource-riepilogo.json"]


def it(x, dec=1):
    return f"{x:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def nome(s):
    s = s.strip("' ").replace("*", " ")
    s = re.sub(r"\s+", " ", s)
    return (s[:60] + "…") if len(s) > 61 else s


def main():
    os.makedirs(ST, exist_ok=True)
    sha = {}
    vista = sorted(__import__("glob").glob(os.path.join(R, "esiti/*/inhouse/vista/vista.md")))[-1]
    for f in FILE:
        src = vista if f == "vista.md" else os.path.join(D, f)
        shutil.copyfile(src, os.path.join(ST, f))
        sha[f] = hashlib.sha256(open(src, "rb").read()).hexdigest()
    soc = list(csv.DictReader(open(os.path.join(D, "societa-ict-pa.csv"), encoding="utf-8")))
    os_ = {r["cf"]: r for r in csv.DictReader(open(os.path.join(D, "opensource.csv"), encoding="utf-8"))}
    rp = json.load(open(os.path.join(D, "riepilogo.json"), encoding="utf-8"))
    ro = json.load(open(os.path.join(D, "opensource-riepilogo.json"), encoding="utf-8"))
    G = {}
    G["file"] = "\n".join(["| file | contenuto | sha256 |", "|---|---|---|"] + [
        f"| [{f}](/dati/inhouse/{f}) | {d} | `{sha[f][:16]}…` |" for f, d in (
            ("societa-ict-pa.csv", "una riga per società ICT nel censimento MEF: classe, ATECO, enti, quote, fatturato, addetti, sito"),
            ("opensource.csv", "per in-house e controllate: catalogo del riuso (editore, manutentore) e indizi dalla home page"),
            ("catalogo-riuso.csv", "i software del catalogo Developers Italia legati a ciascuna società"),
            ("vista.md", "che cosa comprano e che cosa ricevono dagli enti, per società (CIG ANAC dal 2024, per codice fiscale)"),
            ("riepilogo.json", "conteggi, fonte con sha256, controprova con l'elenco Assinter"),
            ("opensource-riepilogo.json", "conteggi dell'analisi open source e sha256 delle copie del catalogo"))])
    pc = rp["per_classe"]
    G["conteggi"] = "\n".join(["| classe | attive | non attive |", "|---|---:|---:|"] + [
        f"| {c} | {pc.get(c, 0)} | {pc.get(c + ' (non attiva)', 0)} |" for c in ("in-house", "controllata", "controllo-pubblico-congiunto", "partecipata")])
    righe = ["| società | classe | regione | enti | fatturato 2023 (M€) | addetti | sito | riuso (catalogo) | open source in home | riuso in home |",
             "|---|---|---|---:|---:|---:|---|---:|---|---|"]
    for s in soc:
        if s["stato"] != "Attiva" or (s["classe"] == "partecipata" and not s["assinter"]):
            continue
        o = os_.get(s["cf"], {})
        fat = float(s["fatturato_2023"]) / 1e6 if s["fatturato_2023"] else None
        sito = f"[{re.sub(r'^https?://(www\\.)?', '', s['sito']).rstrip('/')}]({s['sito']})" if s["sito"] else ""
        cat = o.get("software_nel_catalogo_riuso", "")
        cat = f"{cat} ({o.get('come_editore', 0)} ed., {o.get('come_manutentore', 0)} man.)" if cat not in ("", "0") else ("0" if cat == "0" else "")
        hos = "sì" if o.get("home_open_source") else ("no" if o.get("home_sha256") else (o.get("home_esito", "") or "").replace("http-", "HTTP "))
        hri = "sì" if o.get("home_riuso") else ("no" if o.get("home_sha256") else "")
        righe.append(f"| {nome(s['denominazione'])} | {s['classe']} | {s['regione'].title()} | {s['enti_dichiaranti']} | "
                     f"{it(fat) if fat is not None else ''} | {int(float(s['addetti'])) if s['addetti'] else ''} | {sito} | {cat} | {hos} | {hri} |")
    G["tabella"] = "\n".join(righe)
    G["opensource"] = "\n".join([
        f"- Società esaminate (in-house, controllate e soci Assinter attivi o no): **{ro['societa_esaminate']}**.",
        f"- Nel catalogo del riuso di Developers Italia ({ro['fonti']['developers_italia_software']['n']} software, {ro['fonti']['developers_italia_publishers']['n']} editori, copia del {ro['data']} con sha256 `{ro['fonti']['developers_italia_software']['sha256'][:16]}…`): "
        f"**{ro['con_software_nel_catalogo']}** società hanno almeno un software, **{ro['software_totali']}** software in tutto (come editrici o come manutentrici di software pubblicato da un ente) [V].",
        f"- Home page lette: **{ro['home_lette']}**; con le parole «open source» o «software libero»: **{ro['home_con_open_source']}**; con «riuso»: **{ro['home_con_riuso']}**; con un collegamento a GitHub o GitLab: **{ro['home_con_github_o_gitlab']}** [V, indizio da leggere a mano]."])
    t = open(PAG, encoding="utf-8").read()
    for k, v in G.items():
        t = re.sub(rf"(<!-- GEN:{k} -->\n)(?:.*?\n)?(<!-- /GEN:{k} -->)", lambda m: m.group(1) + v + "\n" + m.group(2), t, flags=re.S)
    open(PAG, "w", encoding="utf-8").write(t)
    print("ok", len(righe) - 2, "righe")


if __name__ == "__main__":
    main()
