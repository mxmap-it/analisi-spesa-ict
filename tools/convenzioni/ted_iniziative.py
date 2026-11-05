"""#62: bandi e aggiudicazioni su TED per le iniziative non Consip (aggregatori, consorzi, altri), via API pubblica di ricerca.

Il CIG non è indicizzato nel testo pieno di TED: si cerca il codice di gara dell'aggregatore (es. «ARIA_2023_807») o, in mancanza,
una frase dell'oggetto di gara nel titolo, limitata ad avvisi italiani. L'abbinamento è per testo: ogni avviso trovato è
marcato «abbinamento per testo, da confermare» finché non si legge il CIG nell'XML (controllo fatto qui: se l'XML contiene
il CIG padre l'abbinamento è «verificato»). Gli XML si archiviano con tools/archivia.py.
Ripartibile: salta le iniziative già cercate. Uscita: report/convenzioni/database/ted/<iniziativa>.json
Uso: python tools/convenzioni/ted_iniziative.py [--rifai]"""
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

R = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(R / "tools"))
import archivia as A  # noqa: E402

A.PAUSA_S = 5.0
DB = R / "report/convenzioni/database"
OUT = DB / "ted"
API = "https://api.ted.europa.eu/v3/notices/search"
RE_CODICE = re.compile(r"\b([A-Z]{3,}_\d{4}_\d{2,4})\b")
VUOTE = {"procedura", "aperta", "per", "la", "il", "di", "dei", "delle", "del", "e", "ai", "sensi", "dell", "art", "gara", "telematica",
         "l", "affidamento", "lo", "un", "una", "conclusione", "accordo", "quadro", "stipula", "convenzione", "d", "lgs", "n", "comma"}


def frase(ogg):
    parole = [p for p in re.findall(r"[A-Za-zÀ-ú]+", ogg.split(" | ")[0]) if p.lower() not in VUOTE and len(p) > 2]
    return " ".join(parole[:5])


def cerca(q):
    time.sleep(3)
    r = requests.post(API, json={"query": q, "fields": ["publication-number", "notice-type", "publication-date"], "limit": 10}, timeout=120)
    return r.json().get("notices", []) if r.status_code == 200 else []


def main(rifai=False):
    OUT.mkdir(parents=True, exist_ok=True)
    voci = json.loads((DB / "iniziative.json").read_text(encoding="utf-8"))
    s = requests.Session()
    s.headers["User-Agent"] = A.UA
    for v in voci:
        if v["tipo_soggetto"] in ("consip", "psn"):
            continue
        dest = OUT / f"{v['id']}.json"
        if dest.exists() and not rifai:
            continue
        ogg = v["lotti"][0]["oggetto"]
        m = RE_CODICE.search(ogg)
        q = f'FT~"{m.group(1)}"' if m else f'notice-title~"{frase(ogg)}" AND buyer-country=ITA'
        esito = {"iniziativa": v["id"], "query": q, "data": datetime.now(timezone.utc).isoformat(timespec="seconds"), "avvisi": []}
        cig = {x["cig_padre"] for x in v["lotti"]}
        for n in cerca(q)[:6]:
            url = f"https://ted.europa.eu/it/notice/{n['publication-number']}/xml"
            rec = A.archivia(s, url, accetta_html=True)
            A.scrivi_manifest(rec)
            testo = ""
            if rec.get("sha256"):
                b = A.percorso_blob(rec["sha256"])
                testo = b.read_text(encoding="utf-8", errors="ignore") if b.exists() else ""
            trovati = sorted(c for c in cig if c in testo)
            esito["avvisi"].append({"numero": n["publication-number"], "tipo": n.get("notice-type"), "data": (n.get("publication-date") or "")[:10],
                                    "url": url, "sha256": rec.get("sha256"), "esito_archivio": rec.get("esito"), "cig_nell_xml": trovati,
                                    "abbinamento": "verificato (CIG nell'XML)" if trovati else "per testo, da confermare"})
        dest.write_text(json.dumps(esito, ensure_ascii=False, indent=1), encoding="utf-8")
        print(v["id"], len(esito["avvisi"]), sum(1 for a in esito["avvisi"] if a["cig_nell_xml"]), flush=True)


if __name__ == "__main__":
    main("--rifai" in sys.argv)
