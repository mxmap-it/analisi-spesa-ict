"""#62, passo 5: genera la sezione /convenzioni/ del sito dalla base dati (unica fonte: report/convenzioni/database/iniziative.json).

Non si modificano a mano le pagine generate: si cambia la base dati (o curate.yaml) e si rilancia.
Uso: python tools/convenzioni/pagine.py"""
import json
import shutil
from pathlib import Path

R = Path(__file__).resolve().parent.parent.parent
DB = R / "report/convenzioni/database"
OUT = R / "sito/content/convenzioni"
GH = "https://github.com/mxmap-it/analisi-spesa-ict/blob/main/"
TIPI = {"consip": "Consip", "psn": "PSN", "aggregatore-regionale": "Aggregatore regionale", "consorzio-unione": "Consorzio o unione", "altro": "Altro"}
STATI = {"archiviato": "archiviato", "pubblicato-non-archiviato": "pubblicato, non archiviato", "non-pubblicato": "non pubblicato", "da-verificare": "da verificare"}
AVVISO = "<!-- Generata da tools/convenzioni/pagine.py dalla base dati report/convenzioni/database/: non modificare a mano. -->\n\n"


def meur(v):
    return "–" if v is None else f"{v / 1e6:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")


def pct(x):
    return f"{round(x * 100)} %"


def esc(t):
    return (t or "").replace("|", "/").replace("\n", " ").strip()


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
           f"Censimento di **{len(voci)} iniziative** ({len(att)} attive, {len(st)} storiche) con i loro lotti, i documenti pubblici "
           f"archiviati e quelli che mancano. Copertura documentale media: **{pct(media)}** dei tipi di documento attesi.", "",
           "**Criterio.** Un'iniziativa è un ID Sigef Consip, o una gara (CIG padre) di un altro soggetto. È «attiva» se ha CIG derivati "
           "con CPV ICT nel 2024-2025 (o è nuova: PRINCO ID 2928, IaaS/PaaS 2 ID 2746). Si prendono le prime per valore dei derivati "
           "ICT 2024-2025 in ciascun tipo di soggetto (40 Consip, 25 aggregatori regionali, 15 consorzi o unioni, 10 altri; fuori Consip "
           "almeno 3 derivati e 1 M€), più il PSN. Le iniziative della base di conoscenza senza derivati recenti ma con almeno 100 M€ dal "
           "2020 sono elencate a parte come «storiche». Dettagli: "
           f"[README della base dati]({GH}report/convenzioni/database/README.md).", "",
           "Per il contesto cloud vedi [Iniziative Consip cloud](/progetto/iniziative-consip-cloud/).", "",
           '<p>Filtra per tipo di soggetto: <select id="filtro-tipo" onchange="(function(s){document.querySelectorAll(\'tr[data-tipo]\').forEach(function(r){r.style.display=(!s.value||r.dataset.tipo===s.value)?\'\':\'none\'})})(this)">'
           '<option value="">tutti</option>' + "".join(f'<option value="{k}">{n}</option>' for k, n in TIPI.items()) + "</select></p>", ""]

    def tabella(vs):
        t = ['<table class="table table-sm"><thead><tr><th>#</th><th>Iniziativa</th><th>Tipo</th><th>M€ ICT 2024-25</th><th>Derivati</th>'
             "<th>Archiviati</th><th>Mancanti</th><th>Copertura</th></tr></thead><tbody>"]
        for k, v in enumerate(vs, 1):
            arch = sum(1 for i in v["inventario"] if i["stato"] == "archiviato")
            t.append(f'<tr data-tipo="{v["tipo_soggetto"]}"><td>{k}</td><td><a href="/convenzioni/{v["id"].lower()}/">{esc(v["nome"])[:110]}</a></td>'
                     f'<td>{TIPI[v["tipo_soggetto"]]}</td><td>{meur(v["valore_ict_2024_2025"])}</td><td>{v["derivati_ict_2024_2025"]}</td>'
                     f'<td>{arch}</td><td>{len(v["mancanze"])}</td><td>{pct(v["copertura"])}</td></tr>')
        t.append("</tbody></table>")
        return t
    idx += ["## Iniziative attive", ""] + tabella(att) + ["", "## Iniziative storiche (ancora rilevanti)", ""] + tabella(st)
    idx += ["", "Fonte e ripetibilità: `tools/convenzioni/*.py`; numeri ricontrollati da `tools/verifiche/convenzioni_copertura.py`.", ""]
    (OUT / "_index.md").write_text("\n".join(idx), encoding="utf-8")
    for v in voci:
        (OUT / f"{v['id'].lower()}.md").write_text(pagina(v), encoding="utf-8")
    print(len(voci), "pagine")


if __name__ == "__main__":
    main()
