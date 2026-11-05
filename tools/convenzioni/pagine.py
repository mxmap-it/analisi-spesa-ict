"""#62, passo 5: genera la sezione /convenzioni/ del sito dalla base dati (unica fonte: report/convenzioni/database/iniziative.json).

Non si modificano a mano le pagine generate: si cambia la base dati (o curate.yaml) e si rilancia.
Uso: python tools/convenzioni/pagine.py"""
import json
import sys
import yaml
import shutil
from pathlib import Path

R = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from griglia_pagina import GRIGLIA  # noqa: E402
DB = R / "report/convenzioni/database"
OUT = R / "sito/content/convenzioni"
GH = "https://github.com/mxmap-it/analisi-spesa-ict/blob/main/"
TIPI = {"consip": "Consip", "psn": "PSN", "aggregatore-regionale": "Aggregatore regionale", "consorzio-unione": "Consorzio o unione", "altro": "Altro"}
STATI = {"archiviato": "archiviato", "pubblicato-non-archiviato": "pubblicato, non archiviato", "non-pubblicato": "non pubblicato", "da-verificare": "da verificare"}
DATA_FONTI = "05/11/2026"
DATA_BDNCP = "05/11/2026"
AVVISO = "<!-- Generata da tools/convenzioni/pagine.py dalla base dati report/convenzioni/database/: non modificare a mano. -->\n\n"


def meur(v):
    return "–" if v is None else f"{v / 1e6:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")


def pct(x):
    return f"{round(x * 100)} %"


def esc(t):
    return (t or "").replace("|", "/").replace("\n", " ").strip()


CAR = yaml.safe_load(open(DB / "carenze.yaml", encoding="utf-8"))
CAR_ID = {c["id"]: c for c in CAR["carenze"]}
STATO_C = {"verificato": "accertato (non trovato sulle fonti consultate)", "da-verificare": "da verificare"}


def blocco_carenze(v):
    if not v.get("carenze"):
        return []
    r = ["## Carenze di trasparenza di questa iniziativa", "",
         f"Pagina del bando su consip.it consultata il {DATA_FONTI}; open data Consip, campione di enti aderenti e ricerca web del {DATA_FONTI}.", "",
         "| Carenza | Stato | Base (norma o ragione) | Proposta |", "|---|---|---|---|"]
    for k in v["carenze"]:
        c = CAR_ID[k["id"]]
        nota = f" ({esc(k['nota'])})" if k.get("nota") else ""
        r.append(f"| **{k['id']}** {c['titolo']} | {STATO_C[k['stato']]}{nota} | {esc(c['base'])} | {k['raccomandazione']} |")
    r += ["", "Rimedio di breve periodo: [bozze di accesso civico generalizzato](/convenzioni/accesso-civico/) (non inviate).", ""]
    return r


def pagina(v):
    righe = ["---", f'title: "{esc(v["nome"])[:150].replace(chr(34), chr(39))}"', "date: 2026-11-05",
             f'description: "Iniziativa {v["id"]}: dati, documenti archiviati e mancanti."', "---", "", AVVISO]
    righe += ["| Campo | Valore |", "|---|---|",
              f"| Identificativo | `{v['id']}` |", f"| Tipo di soggetto | {TIPI[v['tipo_soggetto']]} |",
              f"| Stato | {v['stato_iniziativa']} |", f"| Stazione appaltante | {esc(v['stazione_appaltante'])} |",
              f"| Valore ICT dei CIG derivati 2024-2025 | {meur(v['valore_ict_2024_2025'])} M€ ({v['derivati_ict_2024_2025']} CIG) |",
              f"| Valore ICT dei CIG derivati 2020-2026 | {meur(v['valore_ict_2020_2026'])} M€ |",
              f"| Categoria (base di conoscenza) | {', '.join(v['categoria']) or 'non classificata'} |"]
    for k, nome in (("aggiudicatari", "Aggiudicatari"), ("massimali", "Massimali e tetti"), ("durata", "Durata"),
                    ("listini_marchi_prodotti", "Listini, marchi e prodotti"), ("regola_giurisdizione", "Regola di giurisdizione")):
        righe.append(f"| {nome} | {esc(v.get(k)) or 'da ricavare dai documenti'} |")
    righe.append(f"| Copertura documentale | {pct(v['copertura'])} dei tipi di documento attesi |")
    righe += [""] + blocco_carenze(v)
    righe += ["", "Gli importi sono la somma dell'importo dichiarato in BDNCP per i CIG derivati con CPV ICT: alcuni attuativi riportano il "
              "massimale dell'accordo quadro invece del valore del contratto, quindi sono un ordine di grandezza (verificato: "
              "`tools/analisi/padri_ict.py`; anomalie in `report/convenzioni/incertezze.md`).", ""]
    if v["dossier"]:
        righe += ["## Rendiconti esistenti", ""] + [f"- [{d.rsplit('/', 1)[-1]}]({GH}{d})" for d in v["dossier"]] + [""]
    if v["pagina_consip"]:
        righe += ["## Pagina pubblica", ""] + [f"- <{u}> (HTML sha256 `{h[:16]}…`)" for u, h in zip(v["pagina_consip"], v["pagina_consip_sha256"])] + [""]
    righe += ["## Lotti (CIG padre)", "", "| CIG padre | Anno | Derivati ICT 2024-25 | M€ 2024-25 | M€ 2020-26 | Oggetto |", "|---|---|---|---|---|---|"]
    for x in v["lotti"]:
        righe.append(f"| {x['cig_padre']} | {x['anno_padre']} | {x['derivati_ict_2024_2025']} | {meur(x['euro_ict_2024_2025'])} | "
                     f"{meur(x['euro_ict_2020_2026'])} | {esc(x['oggetto'])[:140]} |")
    righe += ["", "## Inventario dei documenti", "", "| Documento | Stato | Dove | Nota |", "|---|---|---|---|"]
    for i in v["inventario"]:
        righe.append(f"| {i['descrizione']} | **{STATI[i['stato']]}** | {i['dove_di_norma']} | {esc(i['nota'])} |")
    docs = [(i["descrizione"], d) for i in v["inventario"] for d in i["documenti"]]
    if docs:
        righe += ["", "### Documenti trovati", "", "| Tipo | Documento | Originale | Copia (sha256) |", "|---|---|---|---|"]
        for desc, d in docs:
            sha = f"`{d['sha256'][:16]}…`" if d.get("sha256") else "non archiviato"
            righe.append(f"| {desc} | {esc(d['nome'])[:90]} | [link]({d['url'].replace(' ', '%20')}) | {sha} |")
    altrove = [(i["descrizione"], d) for i in v["inventario"] for d in i.get("reperiti_altrove", [])]
    if altrove:
        righe += ["", "### Reperiti da fonte non ufficiale", "",
                  "Documenti che la centrale non pubblica, trovati con la ricerca online complementare. **La carenza resta**: il dato "
                  "esiste altrove, ma la politica di pubblicazione non lo garantisce.", "",
                  "| Tipo | Documento | Dove | Affidabilità | Copia (sha256) |", "|---|---|---|---|---|"]
        for desc, d in altrove:
            righe.append(f"| {desc} | [{esc(d['nome'])[:110]}]({d['url']}) | non pubblicato dalla centrale; reperito su {esc(d.get('fonte'))} il {d.get('data')} | "
                         f"{d.get('affidabilita') or '–'} | `{(d.get('sha256') or '')[:16]}…` |")
    if v.get("evidenze_dato_esistente"):
        righe += ["", "### Il dato esiste, ma non è pubblico", ""]
        for e in v["evidenze_dato_esistente"]:
            righe.append(f"- **{e['carenza']}** ({e['livello']}): {e['testo']}. Documento: [{esc(e['documento'])[:90]}]({e['url'].replace(' ', '%20')}), "
                         f"sha256 `{(e['sha256'] or '')[:16]}…`.")
    ex = v.get("estratti")
    if ex and ex["documenti_letti"]:
        TEMI_N = {"prodotti_marchi": "Prodotti e marchi", "tetti_erosione": "Massimali, tetti ed erosione", "region_datacenter": "Region, data center e trasferimenti", "reporting": "Reporting e monitoraggio"}
        righe += ["", "## Estratti dai documenti (automatici, da leggere)", "",
                  f"Ricerca per parole chiave su {ex['documenti_letti']} documenti chiave archiviati (`tools/convenzioni/estrai_documenti.py`). "
                  "Un estratto orienta la lettura: **non è un'analisi** e non va citato come accertato.", ""]
        for t, n in TEMI_N.items():
            es = ex["esempi"].get(t) or []
            righe.append(f"**{n}** ({ex['conteggi'].get(t, 0)} occorrenze)")
            righe.append("")
            for x in es:
                righe.append(f"> «…{esc(x['testo'])}…» — {esc(x['documento'])[:80]} (sha256 `{(x['sha256'] or '')[:12]}…`)")
                righe.append("")
    if v.get("analisi"):
        righe += ["", "## Analisi dei documenti chiave", ""]
        for a in v["analisi"]:
            righe.append(f"- **{esc(a['documento'])}.** {a['sintesi']}")
    righe += ["", "## Mancanze e via per colmarle", "", "| Documento | Stato | Fonte possibile | Via |", "|---|---|---|---|"]
    for m in v["mancanze"]:
        righe.append(f"| {m['descrizione']} | {STATI[m['stato']]} | {m['fonte']} | {m['via']} |")
    if v.get("note"):
        righe += ["", f"*Nota:* {v['note']}"]
    righe += ["", "Legenda: «archiviato» = copia nel nostro archivio content-addressed con sha256 (verificato); i campi descrittivi "
              "senza fonte archiviata sono «riferiti» e marcati R in `report/convenzioni/database/curate.yaml`.", ""]
    return "\n".join(righe)


def pagina_registro(voci):
    """/convenzioni/accesso-civico/: registro delle istanze (report/convenzioni/accesso-civico/registro.csv)."""
    import csv
    reg_p = R / "report/convenzioni/accesso-civico/registro.csv"
    if not reg_p.exists():
        return
    reg = list(csv.DictReader(open(reg_p, encoding="utf-8")))
    nomi = {v["id"]: v["nome"] for v in voci}
    from collections import Counter
    st = Counter(r["stato"] for r in reg)
    t = ["---", 'title: "Accesso civico sulle convenzioni ICT"', "date: 2026-11-05",
         'description: "Registro delle istanze di accesso civico generalizzato preparate per le carenze di trasparenza: stato ed esito."', "---", "", AVVISO,
         "L'accesso civico generalizzato (art. 5 c. 2 d.lgs. 33/2013) è qui un **rimedio di breve periodo** per dati che le politiche di "
         "pubblicazione non prevedono e che abbiamo cercato prima sulle pagine ufficiali. Il rimedio strutturale sono le proposte di policy "
         "(R37-R42). **Nessuna istanza è inviata senza l'approvazione di Fabio Pietrosanti.**", "",
         f"Stato: " + ", ".join(f"{k} {n}" for k, n in sorted(st.items())) + f" (totale {len(reg)}).", "",
         f"Analisi dei possibili dinieghi e richieste minime: [analisi-dinieghi.md]({GH}report/convenzioni/accesso-civico/analisi-dinieghi.md). "
         f"Bozze riusabili (JSON `spesaict.istanza/1`) in [report/convenzioni/accesso-civico/bozze/]({GH.replace('/blob/', '/tree/')}report/convenzioni/accesso-civico/bozze).", "",
         "| Istanza | Iniziativa | Carenza | Destinatario | Stato | Inviata | Risposta | Esito | Note |", "|---|---|---|---|---|---|---|---|---|"]
    for r in reg:
        t.append(f"| [{r['id']}]({GH}report/convenzioni/accesso-civico/bozze/{r['id']}.md) | [{esc(nomi.get(r['iniziativa'], r['iniziativa']))[:60]}]"
                 f"(/convenzioni/{r['iniziativa'].lower()}/) | {r['carenza']} {CAR_ID[r['carenza']]['titolo']} | {esc(r['destinatario'])} | {r['stato']} | "
                 f"{r['inviata']} | {r['risposta']} | {esc(r['esito'])} | {esc(r['note'])} |")
    (OUT / "accesso-civico.md").write_text("\n".join(t) + "\n", encoding="utf-8")


def main():
    voci = json.loads((DB / "iniziative.json").read_text(encoding="utf-8"))
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    media = sum(v["copertura"] for v in voci) / len(voci)
    att = [v for v in voci if v["stato_iniziativa"] == "attiva"]
    st = [v for v in voci if v["stato_iniziativa"] != "attiva"]
    idx = ["---", 'title: "Convenzioni e accordi quadro ICT"', "date: 2026-11-05",
           'description: "Le principali iniziative ICT (Consip, PSN, soggetti aggregatori, consorzi): valore, documenti archiviati e mancanti."',
           "---", "", AVVISO,
           "**[Apri la griglia di tutte le iniziative](/convenzioni/griglia/)**: documenti archiviati, reperiti altrove, mancanti e richiesti, in una vista sola. Rapporto: [Trasparenza delle convenzioni ICT](/rendiconti/convenzioni-trasparenza/) (bozza).", "",
           f"Censimento di **{len(voci)} iniziative** ({len(att)} attive, {len(st)} storiche) con i loro lotti, i documenti pubblici "
           f"archiviati e quelli che mancano. Copertura documentale media: **{pct(media)}** dei tipi di documento attesi.", "",
           "**Criterio.** Un'iniziativa è un ID Sigef Consip, o una gara (CIG padre) di un altro soggetto. È «attiva» se ha CIG derivati "
           "con CPV ICT nel 2024-2025 (o è nuova: PRINCO ID 2928, IaaS/PaaS 2 ID 2746). Si prendono le prime per valore dei derivati "
           "ICT 2024-2025 in ciascun tipo di soggetto (40 Consip, 25 aggregatori regionali, 15 consorzi o unioni, 10 altri; fuori Consip "
           "almeno 3 derivati e 1 M€), più il PSN. Le iniziative della base di conoscenza senza derivati recenti ma con almeno 100 M€ dal "
           "2020 sono elencate a parte come «storiche». Dettagli: "
           f"[README della base dati]({GH}report/convenzioni/database/README.md).", "",
           "Per il contesto cloud vedi [Iniziative Consip cloud](/progetto/iniziative-consip-cloud/).", "",
           "Le tabelle si possono ordinare e filtrare (anche per tipo di soggetto, colonna «Tipo»).", ""]

    def tabella(vs):
        t = [f"Valori: BDNCP, derivati ICT 2024-2025 (mirror ANAC, elaborazione del {DATA_BDNCP}); documenti al {DATA_FONTI}.", "",
             "| # | Iniziativa | Tipo | M€ ICT 2024-25 | Derivati | Archiviati | Mancanti | Copertura |", "|---|---|---|---|---|---|---|---|"]
        for k, v in enumerate(vs, 1):
            arch = sum(1 for i in v["inventario"] if i["stato"] == "archiviato")
            t.append(f"| {k} | [{esc(v['nome'])[:110]}](/convenzioni/{v['id'].lower()}/) | {TIPI[v['tipo_soggetto']]} | {meur(v['valore_ict_2024_2025'])} | "
                     f"{v['derivati_ict_2024_2025']} | {arch} | {len(v['mancanze'])} | {pct(v['copertura'])} |")
        return t
    # riquadro «Carenze di trasparenza»: carenza -> iniziative colpite -> valore coinvolto
    idx += ["## Carenze di trasparenza", "",
            "Dati che non vengono pubblicati pur servendo a controllare la spesa e la sovranità. «Accertato» = non trovato sulla pagina "
            f"del bando su consip.it, negli open data Consip né nel campione di enti (consultati il {DATA_FONTI}; tipo dedotto dal nome dei file); "
            "«da verificare» = fonti non ancora consultate. Valore = somma dei derivati ICT 2024-2025 delle iniziative colpite "
            f"(BDNCP, elaborazione del {DATA_BDNCP}; ordine di grandezza, non transato).", "",
            "| Carenza | Iniziative colpite (accertato / da verificare) | M€ coinvolti (accertato) | Obbligo di pubblicare? | Proposta |", "|---|---|---|---|---|"]
    for c in CAR["carenze"]:
        ver = [v for v in voci if any(k["id"] == c["id"] and k["stato"] == "verificato" for k in v["carenze"])]
        dv = [v for v in voci if any(k["id"] == c["id"] and k["stato"] != "verificato" for k in v["carenze"])]
        idx.append(f"| **{c['id']}** {c['titolo']} | {len(ver)} / {len(dv)} | {meur(sum(v['valore_ict_2024_2025'] or 0 for v in ver))} | "
                   f"{ {'no': 'no', 'parziale': 'in parte'}[c['obbligo']] } | {c['raccomandazione']} |")
    idx += ["", "Per tipo di soggetto (iniziative colpite / iniziative del tipo):", "",
            "| Carenza | " + " | ".join(TIPI.values()) + " |", "|---|" + "---|" * len(TIPI)]
    for c in CAR["carenze"]:
        cel = []
        for t in TIPI:
            vs = [v for v in voci if v["tipo_soggetto"] == t]
            cel.append(f"{sum(1 for v in vs if any(k['id'] == c['id'] for k in v['carenze']))}/{len(vs)}")
        idx.append(f"| {c['id']} {c['titolo']} | " + " | ".join(cel) + " |")
    idx += ["", f"Basi normative e ragioni: [carenze.yaml]({GH}report/convenzioni/database/carenze.yaml) e "
            "[scheda normativa](/progetto/normativa-documenti-gara/). Rimedio di breve periodo: "
            "[bozze di accesso civico generalizzato](/convenzioni/accesso-civico/) (preparate, non inviate). "
            "Proposte di policy: R08, R37-R43 in richieste-e-raccomandazioni.yaml.", ""]
    idx += ["## Iniziative attive", ""] + tabella(att) + ["", "## Iniziative storiche (ancora rilevanti)", ""] + tabella(st)
    idx += ["", "Fonte e ripetibilità: `tools/convenzioni/*.py`; numeri ricontrollati da `tools/verifiche/convenzioni_copertura.py`.", ""]
    (OUT / "_index.md").write_text("\n".join(idx), encoding="utf-8")
    for v in voci:
        (OUT / f"{v['id'].lower()}.md").write_text(pagina(v), encoding="utf-8")
    pagina_registro(voci)
    (OUT / "griglia.md").write_text(GRIGLIA, encoding="utf-8")
    print(len(voci), "pagine")


if __name__ == "__main__":
    main()
