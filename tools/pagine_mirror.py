#!/usr/bin/env python3
"""Rigenera le tabelle delle pagine sul mirror (#17) dai file dati versionati.

- sito/content/progetto/mirror-pubblico.md  <- report/mirror/sintesi.json (da tools/indice_mirror.py)
- sito/content/progetto/usi-dei-dataset.md  <- config/usi-dataset.yaml
Scrive solo fra i marcatori <!-- GEN:nome --> ... <!-- /GEN:nome -->; copia indice e sintesi in sito/static/dati/mirror/.

    python tools/pagine_mirror.py
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parent.parent
PAG = BASE / "sito" / "content" / "progetto"
LIV = {"C": "**C**", "Ci": "C·i", "P": "P", "Pi": "P·i", "-": "–"}


def sostituisci(p: Path, nome: str, testo: str) -> None:
    s = p.read_text(encoding="utf-8")
    rx = re.compile(rf"(<!-- GEN:{nome} -->\n).*?(<!-- /GEN:{nome} -->)", re.S)
    if not rx.search(s):
        raise SystemExit(f"marcatore GEN:{nome} assente in {p}")
    p.write_text(rx.sub(lambda m: m.group(1) + testo + "\n" + m.group(2), s), encoding="utf-8")


def gb(b: float) -> str:
    return f"{b / 1e9:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def tabella_mirror() -> None:
    d = json.loads((BASE / "report/mirror/sintesi.json").read_text(encoding="utf-8"))
    agg: dict = {}
    for r in d["per_dataset"]:
        k = r["autorita"]
        a = agg.setdefault(k, {"dataset": 0, "risorse": 0, "conservate": 0, "byte": 0, "formati": set()})
        a["dataset"] += 1
        a["risorse"] += r["risorse"]
        a["conservate"] += r["conservate"]
        a["byte"] += r["byte"]
        a["formati"].update(r["formati"])
    righe = ["| Autorità | Gruppi | Risorse viste | Conservate (sha256) | GB (ultima versione) | Formati |",
             "|---|---:|---:|---:|---:|---|"]
    for k, a in sorted(agg.items(), key=lambda x: -x[1]["byte"]):
        righe.append(f"| {k} | {a['dataset']} | {a['risorse']} | {a['conservate']} | {gb(a['byte'])} | "
                     f"{', '.join(sorted(f for f in a['formati'] if f.isalpha()))} |")
    t = d["totale"]
    righe.append(f"| **totale** | | **{t['risorse']}** | **{t['conservate']}** | **{gb(t['byte_ultime'])}** | |")
    righe.append("")
    righe.append("ANAC per dataset (GB): " + "; ".join(
        f"{r['dataset']} {gb(r['byte'])}" for r in sorted(d["per_dataset"], key=lambda r: -r["byte"])
        if r["autorita"] == "anac" and r["byte"] > 1e8) + ".")
    sostituisci(PAG / "mirror-pubblico.md", "mirror", "\n".join(righe))
    dst = BASE / "sito/static/dati/mirror"
    dst.mkdir(parents=True, exist_ok=True)
    for f in ("indice.csv", "sintesi.json"):
        shutil.copyfile(BASE / "report/mirror" / f, dst / f)


def tabella_usi() -> None:
    u = yaml.safe_load((BASE / "config/usi-dataset.yaml").read_text(encoding="utf-8"))
    pr = list(u["progetti"])
    righe = ["| Dataset | " + " | ".join(pr) + " | Conservazione |", "|---|" + "---|" * len(pr) + "---|"]
    for d in u["dataset"]:
        righe.append(f"| [{d['id']}](#{d['id'].replace('/', '-')}) | " +
                     " | ".join(LIV[d["usi"].get(p, "-")] for p in pr) + f" | {d['priorita_conservazione']} |")
    sostituisci(PAG / "usi-dei-dataset.md", "tabella", "\n".join(righe))
    sch = []
    for d in u["dataset"]:
        sch.append(f"### {d['id']}\n")
        sch.append(f"{d['nome']}. Campi chiave: `{'`, `'.join(d['campi'])}`.\n")
        sch.append(f"- **Uso certo:** {d['certo']}")
        for p, t in (d.get("potenziale") or {}).items():
            sch.append(f"- **Potenziale, {u['progetti'][p]['nome']}:** {t}")
        if d.get("limiti"):
            sch.append(f"- **Limiti noti:** {'; '.join(d['limiti'])}.")
        sch.append(f"- **Conservazione: {d['priorita_conservazione']}.** {d['perche_priorita']}\n")
    sostituisci(PAG / "usi-dei-dataset.md", "schede", "\n".join(sch))


if __name__ == "__main__":
    tabella_mirror()
    tabella_usi()
