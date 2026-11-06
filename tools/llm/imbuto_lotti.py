#!/usr/bin/env python3
"""Pacchetti della via 6 per il residuo S6 dell'imbuto (decisione di Fabio del 7/11/2026, #55 #66, top-5 punto 4).

Selezione (dal 2024, imbuto-0.3.1, lavoro/imbuto/ict.csv):
  G1 «mega»: tutti i 209 CIG (≥ 5 M€), 2 per pacchetto (uno per uno, con cura);
  G3 «incerti rilevanti»: i primi 1.000 per importo, 5 per pacchetto, in ordine d'importo decrescente;
  CTL: i CIG del campione 611 (dati/classificazioni/campione-v3.jsonl) che cadono in G1/G3 ma non nella selezione,
       per allargare il campione di controllo della precisione (senza il riferimento: classificazione cieca).
Ogni riga porta il link ai documenti dall'API PVL (lavoro/pvl/cig_link.csv, 4/11) e il flag `controllo` se il CIG è nel campione 611.
Scrive report/metodo/llm/imbuto-g1g3/lotti/{g1,g3,ctl}-NNN.jsonl e selezione.json (con sha256 degli ingressi). Idempotente.
Uso (sul server): nice .venv/bin/python tools/llm/imbuto_lotti.py
"""
import hashlib, json, os
from pathlib import Path
import duckdb

R = Path(__file__).resolve().parents[2]
ICT, LINK = R / "lavoro/imbuto/ict.csv", R / "lavoro/pvl/cig_link.csv"
RIF = R / "dati/classificazioni/campione-v3.jsonl"
OUT = R / "report/metodo/llm/imbuto-g1g3"
N_G3 = 1000


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


def main():
    rif = {json.loads(l)["cig"] for l in open(RIF, encoding="utf-8") if l.strip()}
    (R / "lavoro/imbuto/duck/tmp").mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    con.execute(f"SET memory_limit='6GB'; SET threads=2; SET temp_directory='{R}/lavoro/imbuto/duck/tmp'")
    con.execute(f"""CREATE TABLE s AS SELECT * FROM read_csv('{ICT}', header=true, types={{'importo':'DOUBLE','cig':'VARCHAR'}})
                    WHERE CAST(anno AS INT) >= 2024 AND (gruppo LIKE 'G1%' OR gruppo LIKE 'G3%')
                    QUALIFY row_number() OVER (PARTITION BY cig ORDER BY importo DESC, anno DESC) = 1""")  # ict.csv ha CIG ripetuti (più anni): uno per CIG
    con.execute(f"""CREATE TABLE l AS SELECT cig, first(link) link, first(dominio) dominio FROM read_csv('{LINK}', header=true, all_varchar=true)
                    WHERE coalesce(link,'') <> '' AND cig IN (SELECT cig FROM s) GROUP BY cig""")
    cols = ["anno", "cig", "gruppo", "sottoclasse", "via", "provider", "giurisdizione", "servizio", "cod_cpv", "importo",
            "importo_da_verificare", "stazione_appaltante", "aggiudicatari", "testo", "link"]
    rows = [dict(zip(cols, r)) for r in con.execute(
        f"SELECT {', '.join('s.'+c for c in cols[:-1])}, l.link FROM s LEFT JOIN l USING (cig) ORDER BY importo DESC, cig").fetchall()]
    g1 = [r for r in rows if r["gruppo"].startswith("G1")]
    g3 = [r for r in rows if r["gruppo"].startswith("G3")][:N_G3]
    sel = {r["cig"] for r in g1 + g3}
    ctl = [r for r in rows if r["cig"] in rif and r["cig"] not in sel]

    def riga(r, g):
        return {"cig": r["cig"], "gruppo": g, "anno": r["anno"], "sottoclasse": r["sottoclasse"], "cpv": r["cod_cpv"],
                "importo": r["importo"], "importo_da_verificare": bool(r["importo_da_verificare"]), "ente": r["stazione_appaltante"],
                "aggiudicatari": r["aggiudicatari"], "testo": r["testo"], "link_documenti": r["link"] or "",
                "regole_v31": {"via": r["via"], "provider": r["provider"], "giurisdizione": r["giurisdizione"], "servizio": r["servizio"]},
                "controllo": r["cig"] in rif}
    d = OUT / "lotti"; d.mkdir(parents=True, exist_ok=True)
    # gli esiti già scritti si ridistribuiscono per CIG nei nuovi pacchetti (ripartibile anche se la selezione cambia)
    E = OUT / "esiti"; vecchi = {}
    for f in sorted(E.glob("*.jsonl")) if E.exists() else []:
        for l in f.read_text(encoding="utf-8").splitlines():
            if l.strip():
                try: vecchi[json.loads(l)["cig"]] = l
                except (json.JSONDecodeError, KeyError): pass
        f.unlink()
    for f in d.glob("*.jsonl"): f.unlink()
    for nome, lst, n in (("g3", g3, 5), ("g1", g1, 2), ("ctl", ctl, 5)):
        g = nome.upper()
        for i in range(0, len(lst), n):
            pk = f"{nome}-{i // n + 1:03d}.jsonl"
            fatti = [vecchi[r["cig"]] for r in lst[i:i + n] if r["cig"] in vecchi]
            if fatti: E.mkdir(exist_ok=True); (E / pk).write_text("".join(x + "\n" for x in fatti), encoding="utf-8")
            (d / pk).write_text("".join(json.dumps(riga(r, g), ensure_ascii=False) + "\n" for r in lst[i:i + n]), encoding="utf-8")
    dup = con.execute(f"SELECT gruppo, count(*) - count(DISTINCT cig) FROM read_csv('{ICT}', header=true, types={{'importo':'DOUBLE','cig':'VARCHAR'}}) WHERE CAST(anno AS INT) >= 2024 AND (gruppo LIKE 'G1%' OR gruppo LIKE 'G3%') GROUP BY 1").fetchall()
    info = {"righe_ripetute_in_ict_csv": dict(dup), "decisione": "Fabio 7/11/2026: top-5 punto 4, primi 1.000 CIG G3 per importo + G1 uno per uno", "versione_imbuto": "imbuto-0.3.1",
            "ingressi": {"ict.csv": sha(ICT), "cig_link.csv": sha(LINK), "campione-v3.jsonl": sha(RIF)},
            "g1": {"cig": len(g1), "euro": sum(r["importo"] for r in g1), "con_link": sum(bool(r["link"]) for r in g1), "controllo": sum(r["cig"] in rif for r in g1)},
            "g3": {"cig": len(g3), "euro": sum(r["importo"] for r in g3), "importo_minimo": min(r["importo"] for r in g3),
                   "con_link": sum(bool(r["link"]) for r in g3), "controllo": sum(r["cig"] in rif for r in g3)},
            "ctl": {"cig": len(ctl), "euro": sum(r["importo"] for r in ctl), "con_link": sum(bool(r["link"]) for r in ctl)}}
    (OUT / "selezione.json").write_text(json.dumps(info, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(info, ensure_ascii=False))


if __name__ == "__main__":
    main()
