#!/usr/bin/env python3
"""Registro unico delle fonti e dei dataset (#81): verifica e pagina pubblica. Versione 0.1 (20/11/2026).

Domanda di Fabio del 20/11/2026: la riproducibilità non riguarda solo il mirror ANAC, ma tutte le fonti da cui
dipendono i numeri pubblicati e i dataset che produciamo noi. Questo strumento unisce:
  config/fonti-verifiche.yaml   inventario statico: per ogni strumento citato sul sito, i suoi ingressi
                                (mirror, lavoro, git, rete, modello) e, per i file di lavoro/, chi li produce;
  config/ingressi-lavoro.yaml   ingressi di lavoro/ congelati (git, archivio, archivio-tar, impronta) con sha256;
  archivio/manifest.jsonl       una riga per acquisizione del mirror (url, sha256);
  config/risorse.yaml           autorità delle fonti.
Comandi:
  python3 tools/fonti.py verifica   ogni host del mirror usato ha acquisizioni nel manifest; ogni file di lavoro/ letto
                                    da uno strumento è nel registro degli ingressi (o è un prodotto intermedio con
                                    ricetta); esce con 1 se qualcosa manca. Scrive esiti/<data>/fonti/verifica.json
  python3 tools/fonti.py pagina     riscrive sito/content/progetto/fonti-e-dataset.md fra i marcatori GEN
"""
import collections
import glob
import hashlib
import json
import os
import re
import sys
from datetime import date

import yaml

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INV = yaml.safe_load(open(os.path.join(R, "config/fonti-verifiche.yaml"), encoding="utf-8"))
REG = yaml.safe_load(open(os.path.join(R, "config/ingressi-lavoro.yaml"), encoding="utf-8"))
PAG = os.path.join(R, "sito/content/progetto/fonti-e-dataset.md")
OGGI = date.today().isoformat()

# Prodotti intermedi che si rigenerano con un comando da ingressi già registrati (non serve congelarli).
INTERMEDI = {
    "lavoro/imbuto-prova-0.3.4/base.duckdb": "tools/verifiche/imbuto_prova_034.py prepara (dal mirror ANAC)",
    "lavoro/imbuto-prova-0.3.4/<V>/ict.csv": "tools/verifiche/imbuto_prova_034.py <V>",
    "lavoro/cruscotto/contratti.sqlite": "tools/cruscotto/ (dagli esiti versionati e da lavoro/imbuto/ict.csv)",
    "lavoro/residuo-s6/ingresso.csv": "tools/acquisizione/residuo_s6_ingresso.py (da ict.csv e pvl/link_cig.csv)",
    "lavoro/inhouse/": "tools/verifiche/inhouse_opensource.py (risposte archiviate con sha256 nel riepilogo)",
    "lavoro/imbuto-revisione/": "tools/verifiche/imbuto_revisione.py (lotti e log; la lettura del modello è negli esiti versionati)",
    "lavoro/residuo-s6/": "registro: out/esiti.jsonl e l4-js/enti.jsonl congelati; ingresso.csv è intermedio (residuo_s6_ingresso.py)",
    "lavoro/ripetibilita/<data>/": "uscita della prova di ripetibilità, non un ingresso",
    "lavoro/cig_completo/*.csv": "registro: impronta di lavoro/cig_completo",
    "lavoro/cig_delta/*.csv": "registro: lavoro/cig_delta (archivio-tar)",
    "lavoro/attribuzione/<anno>.csv": "registro: lavoro/attribuzione (archivio-tar)",
    "lavoro/ted-v2/pagine/*.json": "registro: lavoro/ted-v2/pagine (archivio-tar)",
    "lavoro/bdap-pagine/start-*.json": "registro: lavoro/bdap-pagine (archivio-tar)",
    "lavoro/mirror-completamento/": "registro: lavoro/mirror-completamento (archivio-tar)",
}


def registrati():
    return {e["percorso"]: e for e in REG["ingressi"]}


def manifest_per_host():
    c = collections.Counter()
    with open(os.path.join(R, "archivio/manifest.jsonl"), encoding="utf-8") as f:
        for l in f:
            try:
                j = json.loads(l)
            except ValueError:
                continue
            if j.get("esito") in ("nuovo", "invariato") and j.get("url", "").startswith("http"):
                c[j["url"].split("/")[2]] += 1
    return c


def uso():
    host = collections.defaultdict(set)
    lav = collections.defaultdict(set)
    tipi = collections.Counter()
    for s, v in (INV.get("strumenti") or {}).items():
        for i in v.get("ingressi") or []:
            tipi[i["tipo"]] += 1
            if i["tipo"] == "mirror":
                h = i.get("host") or i.get("percorso", "").split("/")[2]
                if h.startswith("("):      # segnaposto: blob o host di enti elencati altrove
                    host["vari (" + h.strip("()") + ")"].add(s)
                    continue
                for x in re.split(r"\s*,\s*", h):
                    host[x].add(s)
            elif i["tipo"] == "lavoro":
                lav[pulisci(i["percorso"])].add(s)
    return host, lav, tipi


def pulisci(p):
    """L'inventario annota i percorsi fra parentesi: «lavoro/x.csv (confronto)» -> «lavoro/x.csv»."""
    return re.sub(r"\s*\(.*$", "", p).strip()


def stato_lavoro(p, reg):
    p = pulisci(p)
    if p in reg:
        return "congelato (" + reg[p]["via"] + ")"
    if p in INTERMEDI:
        return "intermedio: " + INTERMEDI[p]
    base = p.split("*")[0].split("<")[0].rstrip("/")
    for k in reg:
        if base and (base == k or base.startswith(k + "/")):
            return "congelato (" + reg[k]["via"] + ", in " + k + ")"
    return "NON REGISTRATO"


def verifica():
    reg = registrati()
    host, lav, tipi = uso()
    man = manifest_per_host()
    h_out = {h: {"strumenti": len(s), "acquisizioni_nel_manifest": man.get(h, 0)} for h, s in sorted(host.items())}
    l_out = {p: {"strumenti": len(s), "stato": stato_lavoro(p, reg)} for p, s in sorted(lav.items())}
    for p, e in (INV.get("lavoro") or {}).items():
        p = pulisci(p)
        l_out.setdefault(p, {"strumenti": 0, "stato": stato_lavoro(p, reg)})
    mancano = [p for p, v in l_out.items() if v["stato"] == "NON REGISTRATO"]
    host_vuoti = [h for h, v in h_out.items() if not v["acquisizioni_nel_manifest"] and not h.startswith("vari (")]
    out = {"data": OGGI, "strumento": "tools/fonti.py verifica", "strumenti_esaminati": len(INV.get("strumenti") or {}),
           "ingressi_per_tipo": dict(tipi), "host_del_mirror": h_out, "ingressi_di_lavoro": l_out,
           "lavoro_non_registrati": mancano, "host_senza_acquisizioni": host_vuoti,
           "esito": "ok" if not mancano and not host_vuoti else "da completare"}
    d = os.path.join(R, "esiti", OGGI, "fonti")
    os.makedirs(d, exist_ok=True)
    json.dump(out, open(os.path.join(d, "verifica.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: out[k] for k in ("strumenti_esaminati", "ingressi_per_tipo", "lavoro_non_registrati", "host_senza_acquisizioni", "esito")}, ensure_ascii=False, indent=1))
    return out


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def nostri():
    """Dataset prodotti da noi: tabelle curate (config/), dataset derivati (dati/), registri."""
    righe = []
    for p in sorted(glob.glob(os.path.join(R, "config/*.yaml"))):
        try:
            y = yaml.safe_load(open(p, encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        testa = open(p, encoding="utf-8").readline().lstrip("# ").strip()
        righe.append(("tabella curata", os.path.relpath(p, R), str(y.get("versione", "")) if isinstance(y, dict) else "", testa[:150], sha(p)))
    for p in sorted(glob.glob(os.path.join(R, "dati/inhouse/*.csv")) + glob.glob(os.path.join(R, "dati/inhouse/*.json"))):
        righe.append(("dataset derivato", os.path.relpath(p, R), "", "società ICT pubbliche (#82)", sha(p)))
    return righe


def pagina(out):
    reg = registrati()
    G = {}
    tab = ["| host | strumenti che lo leggono | acquisizioni nel mirror |", "|---|---:|---:|"]
    for h, v in out["host_del_mirror"].items():
        tab.append(f"| {h} | {v['strumenti']} | {v['acquisizioni_nel_manifest']:,} |".replace(",", "."))
    G["host"] = "\n".join(tab)
    tab = ["| ingresso in lavoro/ | strumenti | stato | come si rifà |", "|---|---:|---|---|"]
    for p, v in out["ingressi_di_lavoro"].items():
        e = reg.get(p) or {}
        rif = (e.get("rigenera") or (INV.get("lavoro") or {}).get(p, {}).get("prodotto_da", "")).replace("|", "/")
        tab.append(f"| `{p}` | {v['strumenti']} | {v['stato']} | {rif[:160]} |")
    G["lavoro"] = "\n".join(tab)
    tab = ["| ingresso | via | sha256 | file / byte |", "|---|---|---|---|"]
    for e in REG["ingressi"]:
        h = e.get("sha256") or e.get("sha256_tar") or e.get("sha256_concatenati") or ("impronte in `" + e.get("impronte", "") + "`")
        h = f"`{h[:16]}…`" if re.fullmatch(r"[0-9a-f]{64}", h or "") else h
        tab.append(f"| `{e['percorso']}` | {e['via']} | {h} | {e.get('file', '')} {e.get('byte', '')} |")
    G["registro"] = "\n".join(tab)
    tab = ["| tipo | file | versione | contenuto | sha256 |", "|---|---|---|---|---|"]
    for t, p, v, d, s in nostri():
        tab.append(f"| {t} | [`{p}`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/{p}) | {v} | {d.replace('|', '/')} | `{s[:12]}…` |")
    G["nostri"] = "\n".join(tab)
    G["sintesi"] = (f"Verifica del {out['data']}: {out['strumenti_esaminati']} strumenti esaminati, ingressi per tipo "
                    + ", ".join(f"{k} {v}" for k, v in sorted(out["ingressi_per_tipo"].items()))
                    + f"; {len(out['host_del_mirror'])} host del mirror; {len(REG['ingressi'])} ingressi di lavoro/ congelati; "
                    + f"non registrati: {len(out['lavoro_non_registrati'])}; host senza acquisizioni: {len(out['host_senza_acquisizioni'])}. "
                    + f"Esito: **{out['esito']}**.")
    t = open(PAG, encoding="utf-8").read()
    for k, v in G.items():
        t = re.sub(rf"(<!-- GEN:{k} -->\n)(?:.*?\n)?(<!-- /GEN:{k} -->)", lambda m: m.group(1) + v + "\n" + m.group(2), t, flags=re.S)
    open(PAG, "w", encoding="utf-8").write(t)
    print("scritta", os.path.relpath(PAG, R))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "verifica"
    o = verifica()
    if cmd == "pagina":
        pagina(o)
    sys.exit(0 if o["esito"] == "ok" or cmd == "pagina" else 1)
