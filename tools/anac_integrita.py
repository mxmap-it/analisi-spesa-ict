#!/usr/bin/env python3
"""Controlli di integrità sui dataset tabellari ANAC, letti dal mirror.

Ogni controllo produce un conteggio e alcuni esempi, così che ogni affermazione
del rapporto sia riproducibile: si rilancia lo script sulla stessa versione
(stesso sha256 nel manifest) e si ottiene lo stesso numero.

I file vengono estratti in `lavoro/`, che è derivato e rigenerabile: la copia
di riferimento resta il blob nell'archivio.

    anac_integrita.py [--oggi 2026-10-26] [--out report/anac/integrita.json]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import zipfile
from datetime import date
from pathlib import Path

import duckdb

BASE = Path(__file__).resolve().parent.parent
ROOT = Path(os.environ.get("ARCHIVIO_ROOT", BASE / "archivio"))
MIRROR = ROOT / "mirror" / "dati.anticorruzione.it" / "opendata" / "download" / "dataset"
LAVORO = Path(os.environ.get("LAVORO_ROOT", BASE / "lavoro"))

DATASET = {
    "stazioni_appaltanti": "stazioni-appaltanti/filesystem/stazioni-appaltanti_csv.zip",
    "aggiudicazioni": "aggiudicazioni/filesystem/aggiudicazioni_csv.zip",
    "aggiudicatari": "aggiudicatari/filesystem/aggiudicatari_csv.zip",
    "cup": "cup/filesystem/cup_csv.zip",
    "cig_delta": "cig/filesystem/20261001-cig_csv.zip",
}

# --------------------------------------------------------------------------
# Validatori. Il CIG segue l'algoritmo pubblicato da ANAC in anticorruzione/npa,
# come implementato in aborruso/anac-pl-pp-cli (internal/cig, Apache-2.0).
# --------------------------------------------------------------------------
HEXSET = set("0123456789ABCDEF")


def _hex(n: int, w: int) -> str:
    return format(n, "X").zfill(w)


def cig_valido(s: str | None) -> tuple[bool, str]:
    if not s:
        return False, "vuoto"
    c = s.strip().upper()
    if len(c) != 10:
        return False, "lunghezza"
    a = c[0]
    if a.isdigit():
        if not c[:7].isdigit() or not set(c[7:]) <= HEXSET:
            return False, "struttura"
        if c[1:7] == "000000":
            return False, "progressivo nullo"
        return (_hex(int(c[:7]) * 211 % 4091, 3) == c[7:]), "cifra di controllo"
    if "A" <= a <= "U":
        if not set(c[1:]) <= HEXSET:
            return False, "struttura"
        n = int(c[1:7], 16)
        return (_hex((n + ord(a) - ord("A") + 1) * 211 % 4091, 3) == c[7:]), "cifra di controllo"
    if a in "XYZ":
        if not set(c[1:]) <= HEXSET:
            return False, "struttura"
        n = int(c[3:], 16)
        if n == 0:
            return False, "progressivo nullo"
        return (_hex(n * 211 % 251, 2) == c[1:3]), "cifra di controllo"
    return False, "primo carattere"


def piva_valida(s: str) -> bool:
    if len(s) != 11 or not s.isdigit():
        return False
    d = [int(x) for x in s]
    tot = sum(d[0:10:2])
    for x in d[1:10:2]:
        y = 2 * x
        tot += y - 9 if y > 9 else y
    return (10 - tot % 10) % 10 == d[10]


_DISP = dict(zip("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                 [1, 0, 5, 7, 9, 13, 15, 17, 19, 21, 1, 0, 5, 7, 9, 13, 15, 17, 19, 21,
                  2, 4, 18, 20, 11, 3, 6, 8, 12, 14, 16, 10, 22, 25, 24, 23]))
_PARI = {c: (int(c) if c.isdigit() else ord(c) - ord("A")) for c in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"}


def cf_persona_valido(s: str) -> bool:
    if len(s) != 16 or not re.fullmatch(r"[A-Z0-9]{16}", s):
        return False
    tot = sum(_DISP[c] if i % 2 == 0 else _PARI[c] for i, c in enumerate(s[:15]))
    return chr(ord("A") + tot % 26) == s[15]


def cf_valido(s: str | None) -> tuple[bool, str]:
    if not s:
        return False, "vuoto"
    c = s.strip().upper()
    if c.isdigit() and len(c) == 11:
        if c == "00000000000":
            return False, "segnaposto 00000000000"
        return piva_valida(c), "cifra di controllo (11 cifre)"
    if len(c) == 16:
        return cf_persona_valido(c), "carattere di controllo (16)"
    return False, f"lunghezza {len(c)}"


# --------------------------------------------------------------------------
# --completo: il CIG su tutti i file annuali 2007-2025 più gli aggiornamenti mensili 2026
CIG_COMPLETO = ["cig-20*/filesystem/cig_csv_*.zip", "cig/filesystem/*-cig_csv.zip"]


def estrai_tutti(pattern: list[str], nome: str) -> list[Path]:
    out = []
    for pat in pattern:
        for z in sorted(MIRROR.glob(pat)):
            out.append(_estrai_zip(z, LAVORO / nome))
    return out


def estrai(nome: str) -> Path | None:
    z = MIRROR / DATASET[nome]
    if not z.exists():
        return None
    return _estrai_zip(z, LAVORO / nome)


def _estrai_zip(z: Path, dest: Path) -> Path:
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(z) as zf:
        membro = next(i for i in zf.infolist() if i.filename.lower().endswith(".csv"))
        out = dest / Path(membro.filename).name
        if not out.exists() or out.stat().st_size != membro.file_size:
            zf.extract(membro, dest)
            estratto = dest / membro.filename
            if estratto != out:
                os.replace(estratto, out)
    return out


def leggi_completo(con, nome: str, csvs: list[Path]) -> None:
    """Unione di più file con le stesse colonne; per ogni CIG resta la versione più recente
    (gli aggiornamenti mensili, il cui nome inizia con la data, prevalgono sui file annuali)."""
    elenco = ", ".join(f"'{c.as_posix()}'" for c in csvs)
    con.execute(f"""
        CREATE OR REPLACE TABLE {nome} AS
        SELECT * EXCLUDE (filename) FROM read_csv([{elenco}], delim=';', quote='"', header=true,
                               all_varchar=true, encoding='utf-8',
                               union_by_name=true, filename=true,
                               ignore_errors=true, store_rejects=true,
                               rejects_scan='rifiuti_scan', rejects_table='rifiuti_righe')
        QUALIFY row_number() OVER (PARTITION BY cig ORDER BY
            CASE WHEN regexp_matches(filename, '/[0-9]{{8}}-') THEN '2' || filename ELSE '1' || filename END DESC) = 1
    """)


def leggi(con, nome: str, csv: Path) -> None:
    con.execute(f"""
        CREATE OR REPLACE TABLE {nome} AS
        SELECT * FROM read_csv('{csv.as_posix()}', delim=';', quote='"', header=true,
                               all_varchar=true, ignore_errors=false, encoding='utf-8')
    """)


def q1(con, sql: str):
    return con.execute(sql).fetchone()[0]


def esempi(con, sql: str, n: int = 5) -> list:
    return [list(r) for r in con.execute(sql + f" LIMIT {n}").fetchall()]


def controllo(ris: list, ds: str, id_: str, descrizione: str, n: int, totale: int, es=None, nota=None):
    ris.append({"dataset": ds, "id": id_, "controllo": descrizione, "anomalie": int(n),
                "su": int(totale), "pct": round(100 * n / totale, 3) if totale else None,
                "esempi": es or [], "nota": nota})


def valida_colonna(con, tab: str, col: str, fn) -> tuple[int, int, dict, list]:
    valori = [r[0] for r in con.execute(f"SELECT DISTINCT {col} FROM {tab}").fetchall()]
    motivi: dict[str, int] = {}
    esempi_ = []
    cattivi = set()
    for v in valori:
        ok, motivo = fn(v)
        if not ok:
            cattivi.add(v)
            motivi[motivo] = motivi.get(motivo, 0) + 1
            if len(esempi_) < 5:
                esempi_.append(v)
    return len(cattivi), len(valori), motivi, esempi_


# --------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--oggi", default=date.today().isoformat())
    ap.add_argument("--out", type=Path, default=BASE / "report" / "anac" / "integrita.json")
    ap.add_argument("--completo", action="store_true",
                    help="CIG su tutti gli anni 2007-2025 più gli aggiornamenti 2026, non sul solo delta di ottobre")
    a = ap.parse_args()
    oggi = a.oggi
    # server condiviso: database su disco, memoria e thread limitati (il caricamento di tutti i CIG
    # dal 2007 in memoria ha esaurito la RAM il 27/10/2026)
    LAVORO.mkdir(parents=True, exist_ok=True)
    db = LAVORO / "integrita.duckdb"
    if db.exists():
        db.unlink()
    con = duckdb.connect(str(db))
    con.execute(f"SET memory_limit='{os.environ.get('DUCKDB_MEMORIA', '6GB')}'")
    con.execute(f"SET threads={os.environ.get('DUCKDB_THREAD', '4')}")
    con.execute(f"SET temp_directory='{(LAVORO / 'duckdb_tmp').as_posix()}'")
    con.execute("SET preserve_insertion_order=false")
    ris: list = []
    presenti = {}

    for nome in DATASET:
        if nome == "cig_delta" and a.completo:
            csvs = estrai_tutti(CIG_COMPLETO, "cig_completo")
            leggi_completo(con, nome, csvs)
            presenti[nome] = q1(con, f"SELECT count(*) FROM {nome}")
            rif = q1(con, "SELECT count(*) FROM rifiuti_righe")
            controllo(ris, nome, "CD-CSV", "righe non conformi al CSV standard (RFC 4180), scartate dal lettore rigoroso",
                      rif, presenti[nome] + rif,
                      esempi(con, """SELECT s.file_path, e.line, e.error_type, left(e.csv_line, 160)
                                    FROM rifiuti_righe e JOIN rifiuti_scan s USING (scan_id) ORDER BY 1, 2""", 10),
                      nota="per file: " + json.dumps(dict(con.execute("""SELECT regexp_extract(s.file_path, '[^/]+$'), count(*)
                           FROM rifiuti_righe e JOIN rifiuti_scan s USING (scan_id) GROUP BY 1 ORDER BY 1""").fetchall())))
            continue
        csv = estrai(nome)
        if csv:
            leggi(con, nome, csv)
            presenti[nome] = q1(con, f"SELECT count(*) FROM {nome}")
            print(f"letto {nome}: {presenti[nome]:,} righe", flush=True)

    # ---------------- stazioni appaltanti
    if "stazioni_appaltanti" in presenti:
        t = "stazioni_appaltanti"; N = presenti[t]
        dup = q1(con, f"SELECT count(*) FROM (SELECT codice_fiscale FROM {t} GROUP BY 1 HAVING count(*)>1)")
        controllo(ris, t, "SA-01", "codice fiscale ripetuto su più righe", dup, N,
                  esempi(con, f"SELECT codice_fiscale, count(*) n FROM {t} GROUP BY 1 HAVING n>1 ORDER BY n DESC"))
        nbad, nval, motivi, es = valida_colonna(con, t, "codice_fiscale", cf_valido)
        controllo(ris, t, "SA-02", "codice fiscale non valido (cifra di controllo o formato)", nbad, nval, es,
                  nota=f"motivi: {motivi}; conteggio su valori distinti")
        n = q1(con, f"SELECT count(*) FROM {t} WHERE partita_iva='00000000000'")
        controllo(ris, t, "SA-03", "partita IVA segnaposto 00000000000", n, N)
        n = q1(con, f"SELECT count(*) FROM {t} WHERE coalesce(trim(codice_ausa),'')=''")
        controllo(ris, t, "SA-04", "codice AUSA mancante", n, N)
        n = q1(con, f"SELECT count(*) FROM {t} WHERE data_fine LIKE '2099-%'")
        controllo(ris, t, "SA-05", "data di fine convenzionale 2099 (valore sentinella)", n, N,
                  nota="non è un errore in sé, ma va documentato come convenzione")

    # ---------------- aggiudicazioni
    if "aggiudicazioni" in presenti:
        t = "aggiudicazioni"; N = presenti[t]
        dup = q1(con, f"SELECT count(*) FROM (SELECT cig,id_aggiudicazione FROM {t} GROUP BY 1,2 HAVING count(*)>1)")
        controllo(ris, t, "AG-01", "coppia (cig, id_aggiudicazione) ripetuta", dup, N,
                  esempi(con, f"SELECT cig,id_aggiudicazione,count(*) n FROM {t} GROUP BY 1,2 HAVING n>1 ORDER BY n DESC"))
        nbad, nval, motivi, es = valida_colonna(con, t, "cig", cig_valido)
        controllo(ris, t, "AG-02", "CIG non valido secondo l'algoritmo ANAC", nbad, nval, es,
                  nota=f"motivi: {motivi}; conteggio su CIG distinti")
        for col, idc in (("data_aggiudicazione_definitiva", "AG-03"), ("data_comunicazione_esito", "AG-04")):
            n = q1(con, f"SELECT count(*) FROM {t} WHERE coalesce({col},'')<>'' AND try_cast({col} AS DATE) IS NULL")
            controllo(ris, t, idc + "a", f"{col}: data non interpretabile", n, N,
                      esempi(con, f"SELECT {col} FROM {t} WHERE coalesce({col},'')<>'' AND try_cast({col} AS DATE) IS NULL"))
            n = q1(con, f"SELECT count(*) FROM {t} WHERE try_cast({col} AS DATE) < DATE '2000-01-01'")
            controllo(ris, t, idc + "b", f"{col}: data anteriore al 2000", n, N,
                      esempi(con, f"SELECT cig,{col} FROM {t} WHERE try_cast({col} AS DATE) < DATE '2000-01-01' ORDER BY {col}"))
            n = q1(con, f"SELECT count(*) FROM {t} WHERE try_cast({col} AS DATE) > DATE '{oggi}'")
            controllo(ris, t, idc + "c", f"{col}: data nel futuro rispetto al {oggi}", n, N,
                      esempi(con, f"SELECT cig,{col} FROM {t} WHERE try_cast({col} AS DATE) > DATE '{oggi}' ORDER BY {col} DESC"))
            n = q1(con, f"SELECT count(*) FROM {t} WHERE coalesce({col},'')=''")
            controllo(ris, t, idc + "d", f"{col}: mancante", n, N)
        n = q1(con, f"""SELECT count(*) FROM {t} WHERE try_cast(data_comunicazione_esito AS DATE)
                        < try_cast(data_aggiudicazione_definitiva AS DATE)""")
        controllo(ris, t, "AG-05", "esito comunicato prima dell'aggiudicazione definitiva", n, N)
        imp = "try_cast(importo_aggiudicazione AS DOUBLE)"
        n = q1(con, f"SELECT count(*) FROM {t} WHERE coalesce(importo_aggiudicazione,'')<>'' AND {imp} IS NULL")
        controllo(ris, t, "AG-06", "importo non numerico", n, N)
        n = q1(con, f"SELECT count(*) FROM {t} WHERE {imp} < 0")
        controllo(ris, t, "AG-07", "importo di aggiudicazione negativo", n, N,
                  esempi(con, f"SELECT cig,importo_aggiudicazione FROM {t} WHERE {imp}<0 ORDER BY {imp}"))
        n = q1(con, f"SELECT count(*) FROM {t} WHERE {imp} = 0")
        controllo(ris, t, "AG-08", "importo di aggiudicazione pari a zero", n, N)
        n = q1(con, f"SELECT count(*) FROM {t} WHERE {imp} >= 1e9")
        controllo(ris, t, "AG-09", "importo di aggiudicazione pari o superiore a un miliardo", n, N,
                  esempi(con, f"SELECT cig,importo_aggiudicazione FROM {t} WHERE {imp}>=1e9 ORDER BY {imp} DESC"),
                  nota="non necessariamente errori: da verificare uno per uno")
        rib = "try_cast(ribasso_aggiudicazione AS DOUBLE)"
        n = q1(con, f"SELECT count(*) FROM {t} WHERE {rib} < 0 OR {rib} > 100")
        controllo(ris, t, "AG-10", "ribasso fuori dall'intervallo 0-100", n, N,
                  esempi(con, f"SELECT cig,ribasso_aggiudicazione FROM {t} WHERE {rib}<0 OR {rib}>100 ORDER BY {rib} DESC"))
        n = q1(con, f"""SELECT count(*) FROM {t} WHERE try_cast(numero_offerte_ammesse AS BIGINT)
                        > try_cast(num_imprese_offerenti AS BIGINT)""")
        controllo(ris, t, "AG-11", "più offerte ammesse che imprese offerenti", n, N,
                  esempi(con, f"""SELECT cig,numero_offerte_ammesse,num_imprese_offerenti FROM {t}
                        WHERE try_cast(numero_offerte_ammesse AS BIGINT) > try_cast(num_imprese_offerenti AS BIGINT)"""))
        n = q1(con, f"""SELECT count(*) FROM {t} WHERE upper(esito) LIKE '%NON%ANCORA%SELEZIONATO%'
                        AND {imp} > 0 AND coalesce(data_aggiudicazione_definitiva,'')<>''""")
        controllo(ris, t, "AG-12", "esito 'vincitore non ancora selezionato' ma con data e importo di aggiudicazione", n, N,
                  esempi(con, f"""SELECT cig,esito,data_aggiudicazione_definitiva,importo_aggiudicazione FROM {t}
                        WHERE upper(esito) LIKE '%NON%ANCORA%SELEZIONATO%' AND {imp}>0
                        AND coalesce(data_aggiudicazione_definitiva,'')<>''"""))
        n = q1(con, f"""SELECT count(*) FROM {t} WHERE upper(criterio_aggiudicazione) LIKE '%PIÙ VANTAGGIOSA%'
                        AND upper(criterio_aggiudicazione) LIKE '%MINOR PREZZO%'""")
        controllo(ris, t, "AG-13", "criterio di aggiudicazione con due criteri alternativi nella stessa etichetta", n, N,
                  esempi(con, f"""SELECT criterio_aggiudicazione, count(*) n FROM {t}
                        WHERE upper(criterio_aggiudicazione) LIKE '%PIÙ VANTAGGIOSA%'
                        AND upper(criterio_aggiudicazione) LIKE '%MINOR PREZZO%' GROUP BY 1 ORDER BY n DESC"""),
                  nota="se l'etichetta è una voce di codelist, il problema è nella codelist e non nei record")

    # ---------------- aggiudicatari
    if "aggiudicatari" in presenti:
        t = "aggiudicatari"; N = presenti[t]
        nbad, nval, motivi, es = valida_colonna(con, t, "codice_fiscale", cf_valido)
        controllo(ris, t, "AT-01", "codice fiscale dell'aggiudicatario non valido", nbad, nval, es,
                  nota=f"motivi: {motivi}; conteggio su valori distinti")
        n = q1(con, f"SELECT count(*) FROM {t} WHERE coalesce(trim(denominazione),'')=''")
        controllo(ris, t, "AT-02", "denominazione dell'aggiudicatario mancante", n, N)
        nbad, nval, motivi, es = valida_colonna(con, t, "cig", cig_valido)
        controllo(ris, t, "AT-03", "CIG non valido secondo l'algoritmo ANAC", nbad, nval, es,
                  nota=f"motivi: {motivi}; conteggio su CIG distinti")
        if "aggiudicazioni" in presenti:
            n = q1(con, f"""SELECT count(*) FROM (SELECT DISTINCT cig,id_aggiudicazione FROM {t}) a
                            ANTI JOIN aggiudicazioni g USING (cig,id_aggiudicazione)""")
            tot = q1(con, f"SELECT count(*) FROM (SELECT DISTINCT cig,id_aggiudicazione FROM {t})")
            controllo(ris, t, "AT-04", "aggiudicatario che rimanda a un'aggiudicazione inesistente", n, tot,
                      nota="confronto fra i file full dello stesso rilascio")
            n = q1(con, """SELECT count(*) FROM (SELECT DISTINCT cig,id_aggiudicazione FROM aggiudicazioni
                           WHERE try_cast(importo_aggiudicazione AS DOUBLE) > 0) g
                           ANTI JOIN aggiudicatari a USING (cig,id_aggiudicazione)""")
            tot = q1(con, """SELECT count(*) FROM (SELECT DISTINCT cig,id_aggiudicazione FROM aggiudicazioni
                             WHERE try_cast(importo_aggiudicazione AS DOUBLE) > 0)""")
            controllo(ris, t, "AT-05", "aggiudicazione con importo positivo ma senza alcun aggiudicatario", n, tot)

    # ---------------- cup
    if "cup" in presenti:
        t = "cup"; N = presenti[t]
        nbad, nval, motivi, es = valida_colonna(con, t, "CIG", cig_valido)
        controllo(ris, t, "CU-01", "CIG non valido secondo l'algoritmo ANAC", nbad, nval, es,
                  nota=f"motivi: {motivi}; conteggio su CIG distinti")
        n = q1(con, f"SELECT count(*) FROM {t} WHERE NOT regexp_full_match(coalesce(CUP,''), '[A-Z0-9]{{15}}')")
        controllo(ris, t, "CU-02", "CUP con formato diverso da 15 caratteri alfanumerici", n, N,
                  esempi(con, f"SELECT CIG,CUP FROM {t} WHERE NOT regexp_full_match(coalesce(CUP,''), '[A-Z0-9]{{15}}')"))
        n = q1(con, f"SELECT count(*) FROM (SELECT CIG,CUP FROM {t} GROUP BY 1,2 HAVING count(*)>1)")
        controllo(ris, t, "CU-03", "coppia (CIG, CUP) ripetuta", n, N)

    # ---------------- delta cig: struttura e anagrafica dell'appalto
    if "cig_delta" in presenti:
        t = "cig_delta"; N = presenti[t]
        cols = [r[0] for r in con.execute(f"DESCRIBE {t}").fetchall()]
        nbad, nval, motivi, es = valida_colonna(con, t, "cig", cig_valido)
        controllo(ris, t, "CD-01", "CIG non valido secondo l'algoritmo ANAC", nbad, nval, es,
                  nota=f"motivi: {motivi}; conteggio su CIG distinti")
        if "cod_cpv" in cols:
            n = q1(con, f"""SELECT count(*) FROM {t} WHERE coalesce(cod_cpv,'')=''
                            OR NOT regexp_full_match(cod_cpv, '[0-9]{{8}}(-[0-9])?') OR cod_cpv LIKE '00000000%'""")
            controllo(ris, t, "CD-02", "codice CPV mancante, malformato o tutto zeri", n, N,
                      esempi(con, f"""SELECT cig,cod_cpv FROM {t} WHERE coalesce(cod_cpv,'')<>''
                            AND (NOT regexp_full_match(cod_cpv, '[0-9]{{8}}(-[0-9])?') OR cod_cpv LIKE '00000000%')"""))
        if "importo_lotto" in cols:
            n = q1(con, f"SELECT count(*) FROM {t} WHERE try_cast(importo_lotto AS DOUBLE) <= 0")
            controllo(ris, t, "CD-03", "importo del lotto nullo o negativo", n, N)
        cf_col = next((c for c in ("cf_amministrazione_appaltante", "codice_fiscale_sa") if c in cols), None)
        if cf_col:
            nbad, nval, motivi, es = valida_colonna(con, t, cf_col, cf_valido)
            controllo(ris, t, "CD-04", "codice fiscale della stazione appaltante non valido", nbad, nval, es,
                      nota=f"motivi: {motivi}; conteggio su valori distinti")
        if "data_pubblicazione" in cols:
            n = q1(con, f"SELECT count(*) FROM {t} WHERE try_cast(data_pubblicazione AS DATE) > DATE '{oggi}'")
            controllo(ris, t, "CD-05", f"data di pubblicazione nel futuro rispetto al {oggi}", n, N)
        ris.append({"dataset": t, "id": "CD-00", "controllo": "colonne del file", "anomalie": 0,
                    "su": len(cols), "esempi": [cols], "nota": None})

    out = {"generato": oggi, "righe": presenti, "controlli": ris}
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print()
    for r in ris:
        if r["id"].endswith("-00"):
            continue
        print(f"{r['id']:7s} {r['anomalie']:>10,} / {r['su']:>11,} ({r['pct']}%)  {r['controllo']}")
    print(f"\nscritto {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
