#!/usr/bin/env python3
"""Le in-house ICT offrono software libero o in riuso? (#52) Versione 0.1 (20/11/2026).

Richiesta di Fabio del 20/11/2026: arricchire il dataset delle in-house e fare un minimo di analisi dei loro siti
per capire se offrono soluzioni open source e/o in riuso. Due vie indipendenti:

  1. catalogo del riuso (con il ruolo: «editore» del software o «manutentore», cioè nominata fra i
     maintenance.contractors del publiccode.yml di software pubblicato da un ente) (Developers Italia, api.developers.italia.it, la fonte ufficiale dell'art. 69 CAD): editori
     (publishers) e software con publiccode.yml. La società si riconosce per codice IPA (alternativeId dell'editore =
     cod_amm dell'Indice PA trovato per codice fiscale) o per nome; il software per organisation.uri
     (urn:x-italian-pa:<codice IPA>) o per URL del repository sotto i codeHosting dell'editore;
  2. home page del sito (una sola pagina per società, robots.txt rispettato, 5 s fra richieste): parole «open source»,
     «riuso», collegamenti a GitHub / GitLab / Developers Italia. È un indizio, non una prova: si legge a mano.

Ingressi: dati/inhouse/societa-ict-pa.csv (tools/verifiche/inhouse_censimento.py), Indice PA (amministrazioni.txt).
Le risposte scaricate si conservano in archivio (tools/archivia.py --da-file), con sha256 nel riepilogo.
Uso: python3 tools/verifiche/inhouse_opensource.py [--senza-siti]
Uscite: dati/inhouse/opensource.csv, dati/inhouse/catalogo-riuso.csv, dati/inhouse/opensource-riepilogo.json
"""
import csv
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.robotparser
from datetime import datetime, timezone
from urllib.parse import urljoin, urlsplit

import requests

VERSIONE = "0.1"
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(R, "dati/inhouse")
LAV = os.path.join(R, "lavoro/inhouse")
API = "https://api.developers.italia.it/v1"
UA = "Mozilla/5.0 (compatible; analisi-spesa-ict; +https://analisi-spesa-ict.mxmap.it)"
S = requests.Session()
S.headers["User-Agent"] = UA
OGGI = datetime.now(timezone.utc).isoformat(timespec="seconds")


def archivia(path, url):
    subprocess.run([sys.executable, os.path.join(R, "tools/archivia.py"), "--da-file", path, "--url", url,
                    "--data", OGGI, "--nota", "inhouse_opensource.py"], capture_output=True)
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def tutto(risorsa):
    out, nxt = [], f"?page[size]=100"
    while nxt:
        j = S.get(f"{API}/{risorsa}{nxt}", timeout=60).json()
        out += j["data"]
        nxt = (j.get("links") or {}).get("next")
        time.sleep(0.5)
    p = os.path.join(LAV, f"developers-italia-{risorsa}.json")
    json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False)
    return out, archivia(p, f"{API}/{risorsa}#tutte-le-pagine")


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


PAROLE = {"open_source": r"open[\s-]?source|software\s+libero|opensource",
          "riuso": r"\briuso\b|\briusabil|a\s+riuso|catalogo\s+del\s+riuso",
          "github": r"github\.com/[\w.-]+", "gitlab": r"gitlab\.[\w.]+/[\w.-]+|gitlab\.com/[\w.-]+",
          "developers_italia": r"developers\.italia\.it", "publiccode": r"publiccode"}


def home(url):
    """Una pagina, se robots.txt lo consente. Restituisce (esito, testo)."""
    try:
        rp = urllib.robotparser.RobotFileParser()
        rr = S.get(urljoin(url, "/robots.txt"), timeout=20)
        if rr.status_code == 200:
            rp.parse(rr.text.splitlines())
            if not rp.can_fetch(UA, url):
                return "robots-vieta", ""
        r = S.get(url, timeout=30)
        return f"http-{r.status_code}", r.text if r.ok else ""
    except requests.RequestException as e:
        return "errore-" + type(e).__name__, ""


def main():
    os.makedirs(LAV, exist_ok=True)
    soc = [r for r in csv.DictReader(open(os.path.join(D, "societa-ict-pa.csv"), encoding="utf-8"))
           if r["classe"] in ("in-house", "controllata", "controllo-pubblico-congiunto") or r["assinter"]]
    ipa = {}
    for p in glob.glob(os.path.join(R, "archivio/mirror/indicepa.gov.it/ipa-dati/dataset/*/resource/*/download/amministrazioni.txt"))[:1]:
        for a in csv.DictReader(open(p, encoding="utf-8-sig", newline=""), delimiter="\t"):
            ipa[re.sub(r"\D", "", a["cf"]).zfill(11)] = a["cod_amm"].lower()
    pubs, sha_p = tutto("publishers")
    sw, sha_s = tutto("software")
    per_ipa = {(p.get("alternativeId") or "").lower(): p for p in pubs if p.get("alternativeId")}
    catalogo, righe = [], []
    for s in soc:
        cod = ipa.get(s["cf"], "")
        pub = per_ipa.get(cod)
        if not pub:   # per nome: la descrizione dell'editore contiene la parte distintiva della denominazione
            chiave = norm(re.split(r"\s+-\s+|\s+S\.?P\.?A|\s+S\.?R\.?L|\s+SOC", s["denominazione"].strip("' "))[0])
            if len(chiave) >= 5:
                pub = next((p for p in pubs if chiave in norm(p.get("description"))), None)
        host = [h["url"].rstrip("/").lower() for h in (pub or {}).get("codeHosting", [])]
        cod_pub = (pub or {}).get("alternativeId", cod).lower() if pub else cod
        mie = []
        chiave_c = norm(re.split(r"\s+-\s+|\s+S\.?P\.?A|\s+S\.?R\.?L|\s+SOC|\s+CONSORZIO", s["denominazione"].strip("' ").replace("CONSORZIO PER IL SISTEMA INFORMATIVO*(CSI PIEMONTE)", "CSI PIEMONTE"))[0])
        chiave_c = chiave_c if len(chiave_c) >= 5 else ""
        for x in sw:
            y = x.get("publiccodeYml") or ""
            m = re.search(r"uri:\s*['\"]?urn:x-italian-pa:([\w-]+)", y)
            u = (x.get("url") or "").lower()
            ruolo = ("editore" if (cod_pub and m and m.group(1).lower() == cod_pub) or any(u.startswith(h) for h in host) else
                     "manutentore" if chiave_c and chiave_c in norm(" ".join(re.findall(r"^\s+-?\s*name:\s*(.+)$", re.split(r"\n\S", y.split("contractors:", 1)[1])[0], re.M)) if "contractors:" in y else "") else "")
            if ruolo:
                nome = re.search(r"^name:\s*(.+)$", y, re.M)
                lic = re.search(r"^\s+license:\s*(.+)$", y, re.M)
                mie.append(x)
                catalogo.append({"cf": s["cf"], "societa": s["denominazione"], "ruolo": ruolo, "software": (nome.group(1).strip() if nome else ""),
                                 "url": x.get("url"), "licenza": lic.group(1).strip() if lic else "",
                                 "usato_da": len(re.findall(r"^usedBy:\s*\n((?:\s*-.*\n)+)", y, re.M)[0].strip().splitlines()) if re.search(r"^usedBy:", y, re.M) else 0})
        riga = {"cf": s["cf"], "denominazione": s["denominazione"], "classe": s["classe"], "sito": s["sito"],
                "codice_ipa": cod, "editore_developers_italia": (pub or {}).get("description", ""),
                "repository_editore": "|".join(host), "software_nel_catalogo_riuso": len(mie),
                "come_editore": sum(1 for c in catalogo if c["cf"] == s["cf"] and c["ruolo"] == "editore"),
                "come_manutentore": sum(1 for c in catalogo if c["cf"] == s["cf"] and c["ruolo"] == "manutentore")}
        if "--senza-siti" not in sys.argv and s["sito"]:
            esito, testo = home(s["sito"])
            riga["home_esito"] = esito
            if testo:
                p = os.path.join(LAV, "home-" + s["cf"] + ".html")
                open(p, "w", encoding="utf-8").write(testo)
                riga["home_sha256"] = archivia(p, s["sito"])
                t = testo.lower()
                for k, rx in PAROLE.items():
                    trov = sorted(set(re.findall(rx, t)))
                    riga["home_" + k] = "|".join(trov[:5])
            time.sleep(5)
        righe.append(riga)
        print(riga["denominazione"][:40], riga["software_nel_catalogo_riuso"], riga.get("home_esito", ""), flush=True)
    campi = sorted({k for r in righe for k in r}, key=lambda k: list(righe[0]).index(k) if k in righe[0] else 99)
    with open(os.path.join(D, "opensource.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campi)
        w.writeheader()
        w.writerows(righe)
    with open(os.path.join(D, "catalogo-riuso.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["cf", "societa", "ruolo", "software", "url", "licenza", "usato_da"])
        w.writeheader()
        w.writerows(catalogo)
    att = [r for r in righe]
    riep = {"versione": VERSIONE, "strumento": "tools/verifiche/inhouse_opensource.py", "data": OGGI[:10],
            "fonti": {"developers_italia_publishers": {"url": f"{API}/publishers", "n": len(pubs), "sha256": sha_p},
                      "developers_italia_software": {"url": f"{API}/software", "n": len(sw), "sha256": sha_s}},
            "societa_esaminate": len(att),
            "editori_nel_catalogo": sum(1 for r in att if r["editore_developers_italia"]),
            "con_software_nel_catalogo": sum(1 for r in att if r["software_nel_catalogo_riuso"]),
            "software_totali": len(catalogo),
            "home_lette": sum(1 for r in att if r.get("home_sha256")),
            "home_con_open_source": sum(1 for r in att if r.get("home_open_source")),
            "home_con_riuso": sum(1 for r in att if r.get("home_riuso")),
            "home_con_github_o_gitlab": sum(1 for r in att if r.get("home_github") or r.get("home_gitlab"))}
    json.dump(riep, open(os.path.join(D, "opensource-riepilogo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(riep, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
