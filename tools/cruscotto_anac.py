"""Cruscotto di disponibilità ANAC (#16): dalle metriche giornaliere I1-I9 (stato/metriche/AAAA-MM-GG.json,
scritte dal cron delle 06:40) e dal registro report/anac/problemi.yaml produce
  sito/static/dati/anac-cruscotto.json   (open data: esito per metrica e per giorno)
  sito/content/enti/anac-cruscotto.md    (pagina del sito)
Gira sul server dopo le metriche; idempotente. Uso: python tools/cruscotto_anac.py
"""

import json
import pathlib
import re

import yaml

R = pathlib.Path(__file__).resolve().parents[1]


def main():
    giorni = {}
    for f in sorted((R / "stato/metriche").glob("*.json")):
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", f.stem):
            giorni[f.stem] = json.loads(f.read_text(encoding="utf-8"))["metriche"]
    probl = yaml.safe_load((R / "report/anac/problemi.yaml").read_text(encoding="utf-8"))
    per_metrica = {}
    for p in probl:
        for mid in re.findall(r"\bI\d\b", str(p.get("metrica", ""))):
            per_metrica.setdefault(mid, []).append(p["id"])
    metriche = {}
    for g, ms in giorni.items():
        for m in ms:
            x = metriche.setdefault(m["id"], {"id": m["id"], "controllo": m["controllo"], "esiti": {}})
            x["esiti"][g] = m["esito"]
            x["controllo"] = m["controllo"]
    for x in metriche.values():
        e = x["esiti"]
        x["ultimo"] = e[max(e)]
        x["giorni"] = len(e)
        x["giorni_violato"] = sum(v == "violato" for v in e.values())
        x["problemi"] = per_metrica.get(x["id"], [])
    ultimo = max(giorni) if giorni else None
    out = {"generato_da": "tools/cruscotto_anac.py", "primo_giorno": min(giorni) if giorni else None,
           "ultimo_giorno": ultimo, "metriche": sorted(metriche.values(), key=lambda x: int(x["id"][1:])),
           "registro": [{k: p.get(k) for k in ("id", "titolo", "gravita", "stato", "pronto_per_anac")} for p in probl]}
    (R / "sito/static/dati").mkdir(parents=True, exist_ok=True)
    (R / "sito/static/dati/anac-cruscotto.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    viol = sum(m["ultimo"] == "violato" for m in out["metriche"])
    righe = [
        "---",
        'title: "ANAC: cruscotto di disponibilità"',
        f"date: {ultimo}",
        f'description: "Esito giornaliero delle metriche di non ricorrenza I1-I9 sui dati aperti ANAC e stato di ogni problema del registro. Ultima misura: {ultimo}."',
        "---",
        f"Ogni mattina alle 06:40 la sonda misura dal vivo il portale `dati.anticorruzione.it`. **Ultima misura: {ultimo}: "
        f"{viol} metriche violate su {len(out['metriche'])}.** Quando ANAC corregge un problema la sua metrica passa a *rispettata*.",
        "",
        "Dati aperti: [anac-cruscotto.json](/dati/anac-cruscotto.json). Metodo: `tools/metriche_anac.py`, pagina generata da `tools/cruscotto_anac.py`.",
        "",
        "## Metriche di non ricorrenza",
        "",
        "| Metrica | Controllo | Ultimo esito | Giorni violata / misurati | Problemi |",
        "|---|---|---|---|---|",
    ]
    for m in out["metriche"]:
        stato = "**violata**" if m["ultimo"] == "violato" else m["ultimo"].replace("rispettato", "rispettata")
        righe.append(f"| {m['id']} | {m['controllo']} | {stato} | {m['giorni_violato']} / {m['giorni']} | {', '.join(m['problemi']) or '—'} |")
    righe += ["", f"Serie dal {out['primo_giorno']} al {ultimo}; un giorno senza file significa che la sonda non ha girato.", "",
              "## Registro dei problemi", "", "Schede complete: [problemi e rimedi](/rendiconti/anac-2026-10-problemi/).", "",
              "| Id | Problema | Gravità | Stato | Pronto per ANAC |", "|---|---|---|---|---|"]
    for p in out["registro"]:
        righe.append(f"| {p['id']} | {p['titolo'].replace('|', '/')} | {p['gravita']} | {p['stato']} | {'sì' if p['pronto_per_anac'] else 'no, resta interno'} |")
    (R / "sito/content/enti/anac-cruscotto.md").write_text("\n".join(righe) + "\n", encoding="utf-8")
    print(f"{len(giorni)} giorni, {len(out['metriche'])} metriche, {viol} violate all'ultimo giorno ({ultimo})")


if __name__ == "__main__":
    main()
