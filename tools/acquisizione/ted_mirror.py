#!/usr/bin/env python3
"""#27 Mirror degli avvisi TED italiani ICT (API v3 anonima, POST /v3/notices/search).

Perimetro: buyer-country=ITA, CPV 72000000 (servizi IT), 48000000 (software), 30200000 (apparecchiature
informatiche), discendenti compresi; un mese di pubblicazione alla volta, pagine da 250 (`--da 2024-01`).
Ogni pagina grezza va in lavoro/ted/pagine/AAAA-MM-pNNN.json e poi nell'archivio content-addressed con
tools/archivia.py --da-file (URL convenzionale con la query, per ritrovarla). Un mese è «fatto» quando le notizie
raccolte coincidono con totalNoticeCount; lo stato è in lavoro/ted/stato.jsonl. Ripartibile e idempotente.
Pausa 2 s fra richieste.

    ted_mirror.py [--da 2024-01] [--a 2026-10] [--dir lavoro/ted-v2]

Filtro CPV verificato il 6/11/2026 sul marzo 2024: classification-cpv (tutti i CPV, anche aggiuntivi) 143 avvisi,
main-classification-proc (solo il principale) 132; IN (…) equivale a 72* OR 48* OR 302*. Totale IT nel mese: 2.012.
"""
import argparse, datetime, json, os, subprocess, sys, time, urllib.parse
from pathlib import Path
import requests

R = Path(__file__).resolve().parents[2]
D = R / "lavoro/ted"
API = "https://api.ted.europa.eu/v3/notices/search"
UA = "analisi-spesa-ict (+https://analisi-spesa-ict.mxmap.it)"
CAMPI = ["publication-number", "notice-type", "publication-date", "buyer-name", "buyer-identifier", "notice-title",
         "classification-cpv", "total-value", "total-value-cur", "winner-name", "winner-identifier", "procedure-type",
         # v2 (6/11/2026): testi e identificativi interni, dove le stazioni italiane scrivono spesso il CIG
         "internal-identifier-lot", "internal-identifier-proc", "title-lot", "description-lot", "title-proc", "description-proc",
         "organisation-identifier-tenderer", "organisation-name-tenderer"]


def mesi(da, a):
    y, m = map(int, da.split("-")); y2, m2 = map(int, a.split("-"))
    while (y, m) <= (y2, m2):
        yield y, m
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--da", default="2024-01")
    ap.add_argument("--a", default=(datetime.date.today().replace(day=1) - datetime.timedelta(days=1)).strftime("%Y-%m"))
    ap.add_argument("--dir", default="lavoro/ted-v2")
    a = ap.parse_args(); global D; D = R / a.dir; (D / "pagine").mkdir(parents=True, exist_ok=True)
    fatti = set()
    if (D / "stato.jsonl").exists():
        fatti = {json.loads(l)["mese"] for l in open(D / "stato.jsonl", encoding="utf-8") if json.loads(l).get("completo")}
    for y, m in mesi(a.da, a.a):
        mese = f"{y}-{m:02d}"
        if mese in fatti: continue
        fine = (datetime.date(y + (m == 12), m % 12 + 1, 1))
        q = (f"buyer-country=ITA AND publication-date>={y}{m:02d}01<{fine:%Y%m%d} "
             "AND classification-cpv IN (72000000 48000000 30200000)")
        visti, totale, p = set(), None, 1
        while True:
            body = {"query": q, "fields": CAMPI, "limit": 250, "page": p, "paginationMode": "PAGE_NUMBER"}
            r = requests.post(API, json=body, headers={"User-Agent": UA}, timeout=120)
            if r.status_code != 200:
                print(mese, p, r.status_code, r.text[:200], file=sys.stderr); break
            f = D / "pagine" / f"{mese}-p{p:03d}.json"; f.write_bytes(r.content)
            url = API + "?" + urllib.parse.urlencode({"q": q, "page": p, "limit": 250})
            subprocess.run([sys.executable, str(R / "tools/archivia.py"), "--da-file", str(f), "--url", url,
                            "--data", datetime.datetime.now(datetime.timezone.utc).isoformat(), "--nota", "TED API v3 #27"],
                           check=False, stdout=subprocess.DEVNULL)
            d = r.json(); totale = d.get("totalNoticeCount", totale)
            n = d.get("notices", [])
            visti |= {x["publication-number"] for x in n}
            time.sleep(2)
            if not n or len(visti) >= (totale or 0) or p * 250 >= 15000: break
            p += 1
        riga = {"mese": mese, "totale": totale, "raccolti": len(visti), "pagine": p, "completo": totale is not None and len(visti) == totale,
                "data": datetime.datetime.now(datetime.timezone.utc).isoformat()}
        with open(D / "stato.jsonl", "a", encoding="utf-8") as fo: fo.write(json.dumps(riga) + "\n")
        print(json.dumps(riga))


if __name__ == "__main__":
    main()
