"""#62, passo 5: genera la sezione /convenzioni/ del sito dalla base dati (unica fonte: report/convenzioni/database/iniziative.json).

Non si modificano a mano le pagine generate: si cambia la base dati (o curate.yaml) e si rilancia.
Uso: python tools/convenzioni/pagine.py"""
import json
import yaml
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


CAR = yaml.safe_load(open(DB / "carenze.yaml", encoding="utf-8"))
CAR_ID = {c["id"]: c for c in CAR["carenze"]}
STATO_C = {"verificato": "verificato (assenza constatata)", "da-verificare": "riferito / da verificare"}


def blocco_carenze(v):
    if not v.get("carenze"):
        return []
    r = ['<div class="callout warning" style="border-left:6px solid #a66300;padding:.8em 1em;background:#fff6e5;margin:1.5em 0">',
         '<div class="callout-title"><strong>Carenze di trasparenza di questa iniziativa</strong></div>',
         '<table class="table table-sm"><thead><tr><th>Carenza</th><th>Stato</th><th>Base (norma o ragione)</th><th>Proposta</th></tr></thead><tbody>']
    for k in v["carenze"]:
        c = CAR_ID[k["id"]]
        nota = f" ({esc(k['nota'])})" if k.get("nota") else ""
        r.append(f"<tr><td><strong>{k['id']}</strong> {c['titolo']}</td><td>{STATO_C[k['stato']]}{nota}</td><td>{esc(c['base'])}</td>"
                 f"<td>{k['raccomandazione']}</td></tr>")
    r += ["</tbody></table>", '<p>Rimedio di breve periodo: <a href="/convenzioni/accesso-civico/">bozze di accesso civico generalizzato</a> (non inviate).</p>', "</div>", ""]
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
    # riquadro «Carenze di trasparenza»: carenza -> iniziative colpite -> valore coinvolto
    idx += ['<div class="callout danger" style="border-left:6px solid #b00020;padding:.8em 1em;background:#fdecee;margin:1.5em 0">',
            "<h2>Carenze di trasparenza</h2>",
            "<p>Dati che non vengono pubblicati pur servendo a controllare la spesa e la sovranità. «Verificato» = assenza constatata da noi "
            "sulla pagina ufficiale dell'iniziativa (con data); «da verificare» = pagina non ancora consultata o dato riferito. "
            "Valore = somma dei derivati ICT 2024-2025 delle iniziative colpite (ordine di grandezza, non transato).</p>",
            '<table class="table table-sm"><thead><tr><th>Carenza</th><th>Iniziative colpite (verificato / da verificare)</th>'
            "<th>M€ coinvolti (verificato)</th><th>Obbligo di pubblicare?</th><th>Proposta</th></tr></thead><tbody>"]
    for c in CAR["carenze"]:
        ver = [v for v in voci if any(k["id"] == c["id"] and k["stato"] == "verificato" for k in v["carenze"])]
        dv = [v for v in voci if any(k["id"] == c["id"] and k["stato"] != "verificato" for k in v["carenze"])]
        idx.append(f"<tr><td><strong>{c['id']}</strong> {c['titolo']}</td><td>{len(ver)} / {len(dv)}</td>"
                   f"<td>{meur(sum(v['valore_ict_2024_2025'] or 0 for v in ver))}</td><td>{ {'no': 'no', 'parziale': 'in parte'}[c['obbligo']] }</td>"
                   f"<td>{c['raccomandazione']}</td></tr>")
    idx += ["</tbody></table>", "<p><strong>Per tipo di soggetto</strong> (iniziative colpite, verificato + da verificare):</p>",
            '<table class="table table-sm"><thead><tr><th>Carenza</th>' + "".join(f"<th>{n}</th>" for n in TIPI.values()) + "</tr></thead><tbody>"]
    for c in CAR["carenze"]:
        cel = []
        for t in TIPI:
            vs = [v for v in voci if v["tipo_soggetto"] == t]
            cel.append(f"{sum(1 for v in vs if any(k['id'] == c['id'] for k in v['carenze']))}/{len(vs)}")
        idx.append(f"<tr><td>{c['id']} {c['titolo']}</td>" + "".join(f"<td>{x}</td>" for x in cel) + "</tr>")
    idx += ["</tbody></table>",
            f'<p>Basi normative e ragioni: <a href="{GH}report/convenzioni/database/carenze.yaml">carenze.yaml</a> e '
            '<a href="/progetto/normativa-documenti-gara/">scheda normativa</a>. Rimedio di breve periodo: '
            '<a href="/convenzioni/accesso-civico/">bozze di accesso civico generalizzato</a> (preparate, non inviate). '
            "Proposte di policy: R37-R42 in richieste-e-raccomandazioni.yaml.</p>", "</div>", ""]
    idx += ["## Iniziative attive", ""] + tabella(att) + ["", "## Iniziative storiche (ancora rilevanti)", ""] + tabella(st)
    idx += ["", "Fonte e ripetibilità: `tools/convenzioni/*.py`; numeri ricontrollati da `tools/verifiche/convenzioni_copertura.py`.", ""]
    (OUT / "_index.md").write_text("\n".join(idx), encoding="utf-8")
    for v in voci:
        (OUT / f"{v['id'].lower()}.md").write_text(pagina(v), encoding="utf-8")
    pagina_registro(voci)
    print(len(voci), "pagine")


if __name__ == "__main__":
    main()
