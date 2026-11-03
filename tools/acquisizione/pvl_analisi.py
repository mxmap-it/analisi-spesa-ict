#!/usr/bin/env python3
"""Disponibilità del link ai documenti (PVL) sull'universo dei CIG 2024-2026 e
mappa dei sistemi di destinazione (#57).

Ingressi (sul server):
  lavoro/pvl/link_cig.csv            da `pvl_avvisi.py estrai`
  lavoro/cig_completo/*.csv          CIG BDNCP (mensili 2024-2025 + delta 2026)
  lavoro/stazioni_appaltanti/*.csv   anagrafica stazioni appaltanti

Uscite:
  lavoro/pvl/cig_link.csv     un CIG per riga: cig, cf_ente, link (primo), dominio, n_avvisi
  lavoro/pvl/sistemi.csv      un dominio per riga (formato in dettaglio-cig.md)
  esiti/pvl-link-cig/*.csv    statistiche aggregate versionate

DuckDB su disco, memory_limit 4 GB, 2 thread: niente CIG in memoria Python.

    pvl_analisi.py [--data AAAA-MM-GG]
"""
from __future__ import annotations

import argparse
import os
from datetime import date
from pathlib import Path

import duckdb

BASE = Path(__file__).resolve().parents[2]
L = BASE / "lavoro"

# Famiglie software/piattaforma riconosciute con certezza dal dominio o dal
# percorso (pattern, piattaforma, gestore). Tutto il resto: «ignota».
FAMIGLIE = [
    (r"\.tuttogare\.it$", "TuttoGare", "Studio Amica"),
    (r"maggiolicloud\.it$", "Appalti e Contratti e-Procurement", "Maggioli"),
    (r"(^|\.)acquistinretepa\.it$", "MePA / Acquisti in rete", "Consip"),
    (r"(sintel\.regione\.lombardia\.it|ariaspa\.it)$", "Sintel", "ARIA (Regione Lombardia)"),
    (r"start\.toscana\.it$", "START", "Regione Toscana"),
    (r"(^|\.)empulia\.it$", "EmPULIA", "InnovaPuglia (Regione Puglia)"),
    (r"intercenter\.regione\.emilia-romagna\.it$", "SATER", "Intercent-ER"),
    (r"centraleacquisti\.regione\.lazio\.it$", "STELLA", "Regione Lazio"),
    (r"(^|\.)soresa\.it$", "Piattaforma Soresa", "So.Re.Sa. (Regione Campania)"),
    (r"(^|\.)asmecomm\.it$", "ASMECOMM", "ASMEL"),
    (r"(^|\.)net4market\.com$", "Net4market", "Net4market-CSAmed"),
    (r"\.traspare\.com$", "Traspare", "Traspare"),
    (r"servizipubblicaamministrazione\.it$", "SaturnWeb", "Saturn"),
    (r"eappalti\.regione\.fvg\.it$", "eAppaltiFVG", "Regione FVG"),
    (r"(bandi-altoadige|ausschreibungen-suedtirol)\.it$", "Portale appalti Alto Adige", "Provincia di Bolzano"),
    (r"(^|\.)acquistiretepa\.it$|(^|\.)portaleappalti\.mit\.gov\.it$", "Portale appalti MIT", "MIT"),
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=date.today().isoformat())
    a = ap.parse_args()
    esiti = BASE / "esiti" / "pvl-link-cig" / a.data
    esiti.mkdir(parents=True, exist_ok=True)
    db = L / "pvl" / "analisi.duckdb"
    con = duckdb.connect(str(db))
    con.execute("SET memory_limit='4GB'; SET threads=2; SET preserve_insertion_order=false;")
    con.execute(f"SET temp_directory='{L / 'pvl' / 'duckdb_tmp'}'")

    # avvisi PVL (una riga per avviso x CIG)
    con.execute(f"""CREATE OR REPLACE TABLE pvl AS SELECT * FROM read_csv('{L/'pvl'/'link_cig.csv'}',
        header=true, all_varchar=true) WHERE cig <> ''""")
    con.execute(r"""CREATE OR REPLACE TABLE cig_link AS
        SELECT cig, any_value(cf_sa) cf_ente, count(DISTINCT id_avviso) n_avvisi,
          string_agg(DISTINCT codice_scheda, ',') schede,
          min(data_pubblicazione) prima_pubblicazione,
          any_value(trim(split_part(documenti_di_gara_link,' | ',1))) FILTER (WHERE documenti_di_gara_link<>'') link,
          any_value(indirizzo_internet_sa) FILTER (WHERE indirizzo_internet_sa<>'') sito_ente
        FROM pvl GROUP BY cig""")
    con.execute(r"""ALTER TABLE cig_link ADD COLUMN dominio VARCHAR;
        UPDATE cig_link SET dominio = regexp_replace(lower(regexp_extract(
          CASE WHEN link LIKE '%://%' THEN link ELSE 'http://'||link END, '^[a-z]+://([^/:?#]+)', 1)), '^www\.', '')
        WHERE link IS NOT NULL""")

    # universo BDNCP 2024-2026: ultima versione per CIG
    files = [str(p) for p in sorted((L / "cig_completo").glob("cig_csv_202[4-9]_*.csv"))] + \
            [str(p) for p in sorted((L / "cig_completo").glob("2026*-cig_csv.csv"))]
    con.execute(f"""CREATE OR REPLACE TABLE bdncp AS
        SELECT cig, any_value(cf_amministrazione_appaltante) cf_ente,
          any_value(denominazione_amministrazione_appaltante) ente,
          max(TRY_CAST(anno_pubblicazione AS INT)) anno, max(TRY_CAST(mese_pubblicazione AS INT)) mese,
          any_value(tipo_scelta_contraente) procedura, any_value(sezione_regionale) regione,
          max(TRY_CAST(replace(importo_lotto, ',', '.') AS DOUBLE)) importo,
          any_value(oggetto_principale_contratto) oggetto
        FROM read_csv({files}, delim=';', header=true, all_varchar=true, union_by_name=true, ignore_errors=true)
        WHERE TRY_CAST(anno_pubblicazione AS INT) >= 2024 GROUP BY cig""")
    con.execute(f"""CREATE OR REPLACE TABLE sa AS SELECT codice_fiscale, any_value(natura_giuridica_descrizione) natura
        FROM read_csv('{L/'stazioni_appaltanti'/'stazioni-appaltanti_csv.csv'}', delim=';', header=true, all_varchar=true)
        GROUP BY codice_fiscale""")
    con.execute("""CREATE OR REPLACE TABLE u AS
        SELECT b.*, s.natura, c.cig IS NOT NULL in_pvl, c.link IS NOT NULL ha_link, c.dominio, c.schede,
          CASE WHEN importo IS NULL THEN 'n.d.' WHEN importo < 5000 THEN 'a <5k' WHEN importo < 40000 THEN 'b 5-40k'
               WHEN importo < 140000 THEN 'c 40-140k' WHEN importo < 221000 THEN 'd 140-221k'
               WHEN importo < 1000000 THEN 'e 221k-1M' WHEN importo < 5538000 THEN 'f 1-5,5M' ELSE 'g >5,5M' END classe
        FROM bdncp b LEFT JOIN cig_link c USING (cig) LEFT JOIN sa s ON s.codice_fiscale = b.cf_ente""")

    agg = "count(*) cig, sum(in_pvl::INT) in_pvl, sum(ha_link::INT) con_link, " \
          "round(100.0*sum(in_pvl::INT)/count(*),1) pct_in_pvl, round(100.0*sum(ha_link::INT)/count(*),1) pct_link, " \
          "round(sum(importo)/1e6,1) importo_mln, round(100.0*sum(CASE WHEN ha_link THEN importo END)/nullif(sum(importo),0),1) pct_importo_link"
    for nome, chiave in [("totale", "'tutti'"), ("anno-mese", "anno, mese"), ("procedura", "procedura"),
                         ("classe-importo", "classe"), ("tipo-ente", "natura"), ("regione", "regione"),
                         ("oggetto", "oggetto")]:
        con.execute(f"COPY (SELECT {chiave} AS chiave_{nome.replace('-', '_')}, {agg} FROM u GROUP BY ALL ORDER BY 1) "
                    f"TO '{esiti / (nome + '.csv')}' (HEADER)")
    con.execute(f"""COPY (SELECT cf_ente, any_value(ente) ente, {agg} FROM u GROUP BY cf_ente ORDER BY cig DESC)
        TO '{esiti / 'stazione-appaltante.csv'}' (HEADER)""")
    con.execute(f"""COPY (SELECT split_part(schede, ',', 1) scheda, count(*) cig, sum((link IS NOT NULL)::INT) con_link,
        round(100.0*sum((link IS NOT NULL)::INT)/count(*),1) pct_link FROM cig_link GROUP BY 1 ORDER BY 2 DESC)
        TO '{esiti / 'scheda-pvl.csv'}' (HEADER)""")
    # CIG in PVL ma non nel BDNCP 2024+ (es. CIG precedenti o mancanti nei mensili)
    con.execute(f"""COPY (SELECT count(*) cig_pvl, sum((b.cig IS NULL)::INT) non_in_bdncp_2024
        FROM cig_link c LEFT JOIN bdncp b USING (cig)) TO '{esiti / 'pvl-vs-bdncp.csv'}' (HEADER)""")

    # mappa dei sistemi
    con.execute("CREATE OR REPLACE TABLE famiglie (pat VARCHAR, piattaforma VARCHAR, gestore VARCHAR)")
    con.executemany("INSERT INTO famiglie VALUES (?,?,?)", FAMIGLIE)
    con.execute(r"""CREATE OR REPLACE TABLE sistemi AS
        WITH d AS (
          SELECT c.dominio, c.link, c.cig, c.cf_ente, b.importo,
            CASE WHEN regexp_matches(lower(c.link), '\.(pdf|p7m|zip|docx?|xlsx?|rar|odt)(\?|$)') THEN 'documento diretto'
                 WHEN regexp_matches(c.link, '[?&][^=]+=[^&]+|/(gare|bandi|bando|gara|procedur|dettaglio|tender|auction|rdo)[^/]*/.+')
                   THEN 'pagina di gara'
                 ELSE 'home o profilo committente' END tipo_link
          FROM cig_link c LEFT JOIN bdncp b USING (cig) WHERE c.dominio IS NOT NULL AND c.dominio <> '')
        SELECT dominio,
          coalesce((SELECT piattaforma FROM famiglie f WHERE regexp_matches(d.dominio, f.pat) LIMIT 1),
                   CASE WHEN any_value(link) ILIKE '%saturnweb%' THEN 'SaturnWeb' END, 'ignota') piattaforma,
          coalesce((SELECT gestore FROM famiglie f WHERE regexp_matches(d.dominio, f.pat) LIMIT 1), 'ignoto') gestore,
          count(DISTINCT cf_ente) n_enti, count(*) n_cig, round(sum(importo)) importo,
          sum((tipo_link='pagina di gara')::INT) n_pagina_gara, sum((tipo_link='documento diretto')::INT) n_documento,
          sum((tipo_link='home o profilo committente')::INT) n_home_profilo,
          mode(tipo_link) tipo_link_prevalente, min(link) link_esempio, string_agg(DISTINCT cf_ente, ' ') FILTER (WHERE true) cf_enti
        FROM d GROUP BY dominio""")
    con.execute(f"COPY (SELECT * EXCLUDE cf_enti FROM sistemi ORDER BY n_cig DESC) TO '{L/'pvl'/'sistemi.csv'}' (HEADER)")
    con.execute(f"COPY (SELECT * EXCLUDE (cf_enti) FROM sistemi ORDER BY n_cig DESC) TO '{esiti/'sistemi.csv'}' (HEADER)")
    con.execute(f"""COPY (SELECT piattaforma, gestore, count(*) domini, sum(n_enti) enti, sum(n_cig) cig, round(sum(importo)) importo
        FROM sistemi GROUP BY ALL ORDER BY cig DESC) TO '{esiti/'piattaforme.csv'}' (HEADER)""")
    # chiave per il monitor della trasparenza: ente -> sistemi
    con.execute(f"""COPY (SELECT c.cf_ente, c.dominio, s.piattaforma, count(*) n_cig, min(c.link) link_esempio
        FROM cig_link c JOIN sistemi s USING (dominio) WHERE c.cf_ente IS NOT NULL GROUP BY ALL ORDER BY 1, 4 DESC)
        TO '{L/'pvl'/'enti_sistemi.csv'}' (HEADER)""")
    con.execute(f"""COPY (SELECT cig, cf_ente, link, dominio, sito_ente, schede, n_avvisi, prima_pubblicazione FROM cig_link)
        TO '{L/'pvl'/'cig_link.csv'}' (HEADER)""")
    print(con.execute(f"SELECT {agg} FROM u").fetchall())
    print(con.execute("SELECT count(*), count(DISTINCT piattaforma) FROM sistemi").fetchall())


if __name__ == "__main__":
    main()
