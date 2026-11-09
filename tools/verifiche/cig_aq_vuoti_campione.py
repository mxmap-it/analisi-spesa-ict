"""#50 (P15) campione dei CIG 2025 «discendenti da AQ/convenzione» con cig_accordo_quadro vuoto.

Scopo: distinguere adesioni del regime transitorio SIMOG (AQ/convenzioni con bando entro il 31/12/2023, CIG
acquisiti fuori dalla PCP) da un difetto dell'esportazione open data dei CIG PCP (la scheda PCP AD4 rende
obbligatorio il campo cig dell'AQ: anticorruzione/npa, modello-dati-schede-AD4.yaml, AppaltoAD4Type.required).
Indicatori, solo dai dati del mirror (lavoro/cig_completo):
  - serie del CIG: i CIG PCP iniziano per «B» (es. padri Consip 2024 B1457D87B0, B2B780C944), quelli SIMOG del
    2023 per cifra o «A» (es. A030E34F62);
  - STRUMENTO_SVOLGIMENTO valorizzato (tipico dei record SIMOG: vuoto nel 98,7 % dei CIG 2025);
  - presenza nell'oggetto di un CIG o del riferimento a convenzione/AQ (per capire se il padre è almeno citato).
Campione: 30 CIG con ordinamento deterministico hash(cig||SEME). Il file di uscita ha una colonna
classe_manuale da compilare/controllare a mano; classe_regola è la classificazione automatica della regola sopra.
Uso (server): nice .venv/bin/python tools/verifiche/cig_aq_vuoti_campione.py -> esiti/<oggi>/cig-aq/vuoti-2025-*.{json,csv}"""

import csv
import datetime
import json
import os
import re
from pathlib import Path

import duckdb

R = Path(__file__).resolve().parents[2]
BASE = Path(os.environ.get("SPESAICT_BASE", R))
SEME = "p15-campione-20261109"
N = 30


def classe(cig, strum):
    if not cig.startswith("B") or strum:
        return "simog-transitorio"
    return "pcp-difetto-esportazione"


def main():
    c = duckdb.connect()
    c.execute("set memory_limit='6GB'; set threads=2; set preserve_insertion_order=false")
    os.makedirs(BASE / "lavoro/duck/tmp", exist_ok=True)
    c.execute(f"set temp_directory='{BASE}/lavoro/duck/tmp'")
    fs = sorted(str(p) for p in (BASE / "lavoro/cig_completo").glob("*cig_csv*.csv"))
    c.execute(f"""create temp table v as select distinct on (cig) trim(cig) cig, data_pubblicazione dp,
        tipo_scelta_contraente sc, coalesce(STRUMENTO_SVOLGIMENTO, '') st, denominazione_amministrazione_appaltante sa,
        coalesce(oggetto_lotto, oggetto_gara, '') og, importo_lotto imp, cod_cpv cpv
        from read_csv({fs}, delim=';', header=true, all_varchar=true, ignore_errors=true, union_by_name=true)
        where anno_pubblicazione = '2025' and modalita_realizzazione like '%DISCENDENTE%'
        and coalesce(trim(cig_accordo_quadro), '') = ''""")
    tot = c.execute("""select count(*), count(*) filter (where cig like 'B%'), count(*) filter (where st <> ''),
        count(*) filter (where cig like 'B%' and st = '') from v""").fetchone()
    iniziale = dict(c.execute("select left(cig, 1), count(*) from v group by 1 order by 2 desc").fetchall())
    scelta = dict(c.execute("select sc, count(*) from v group by 1 order by 2 desc limit 8").fetchall())
    righe = c.execute(f"""select cig, dp, sa, sc, st, og, imp, cpv from v
        order by hash(cig || '{SEME}') limit {N}""").fetchall()
    camp = []
    for cig, dp, sa, sc, st, og, imp, cpv in righe:
        cig_testo = re.findall(r"\b[0-9A-Z]{10}\b", og.upper())
        cita = bool(re.search(r"CONVENZION|ACCORDO QUADRO|\bAQ\b|ADESION|ORDINATIV|MEPA|CONSIP", og.upper()))
        camp.append({"cig": cig, "data_pubblicazione": dp, "sa": sa, "scelta": sc, "strumento": st,
                     "oggetto": og[:160], "importo_lotto": imp, "cpv": cpv,
                     "cig_nel_testo": ";".join(x for x in cig_testo if any(ch.isdigit() for ch in x)),
                     "cita_adesione": cita, "classe_regola": classe(cig, st), "classe_manuale": ""})
    cont = {}
    for r in camp:
        cont[r["classe_regola"]] = cont.get(r["classe_regola"], 0) + 1
    out = {"generato": str(datetime.date.today()), "seme": SEME, "file": len(fs),
           "universo_2025_vuoti": {"cig": tot[0], "serie_B": tot[1], "strumento_valorizzato": tot[2],
                                   "serie_B_e_strumento_vuoto": tot[3]},
           "iniziale_cig": iniziale, "scelta_contraente": scelta, "campione_per_classe_regola": cont,
           "campione": camp}
    o = R / "esiti" / str(datetime.date.today()) / "cig-aq"
    o.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(o / "vuoti-2025-campione.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    with open(o / "vuoti-2025-campione.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(camp[0].keys()))
        w.writeheader()
        w.writerows(camp)
    print(json.dumps({k: v for k, v in out.items() if k != "campione"}, ensure_ascii=False))
    for r in camp:
        print(r["cig"], r["data_pubblicazione"], r["classe_regola"], "|", r["strumento"][:20], "|", r["scelta"][:40], "|",
              r["sa"][:40], "|", r["oggetto"][:90], "|", r["cig_nel_testo"])


if __name__ == "__main__":
    main()
