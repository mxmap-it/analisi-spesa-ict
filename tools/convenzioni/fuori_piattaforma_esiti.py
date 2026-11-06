"""#62 fuori piattaforma, passo 3: dagli allegati.jsonl/pagine.jsonl del passo 2 una riga per (iniziativa, documento_atteso) di criticità 3.
Abbinamento per categoria del documento atteso e parole trovate nel testo estratto dell'allegato; senza riscontro: non-trovato con le
fonti provate. Uscita: report/convenzioni/fuori-piattaforma/trovati-<data>.csv; blocchi in blocchi-nuovi.csv (da accodare a mano).
Uso: python tools/convenzioni/fuori_piattaforma_esiti.py <cartella con allegati.jsonl, pagine.jsonl, input/> <uscita.csv>"""
import csv, json, re, sys
from collections import defaultdict
from pathlib import Path

CAT = [  # (regex sul documento atteso, parole richieste nel testo, regex sul titolo del link)
    (r"ordinativ|contratti attuativi", ["contratto_esecutivo", "ordinativo"], r"contratt|ordin|oda|adesion|determin"),
    (r"flussi|transato|erosion", ["transato"], r"erosion|transat|massimal|monitoragg"),
    (r"fabbisogn", ["piano_fabbisogni", "progetto_fabbisogni"], r"fabbisogn|progett"),
    (r"offerta tecnica", ["offerta_tecnica"], r"offert.*tecnic|tecnic"),
    (r"offerta econom|listin|corrispettiv|tariff|prezz|ea per", ["offerta_economica", "listino", "prezzi"], r"offert|listin|prezz|preventiv|corrispett|econom"),
]


def cat(doc):
    return next((c for c in CAT if re.search(c[0], doc, re.I)), CAT[-1])


def main(d, out):
    d = Path(d)
    mancanti = [r for r in csv.DictReader(open(d / "input/documenti-mancanti.csv", encoding="utf-8")) if r["criticita"] == "3"]
    al = defaultdict(list)
    for l in open(d / "allegati.jsonl", encoding="utf-8"):
        x = json.loads(l); al[x["iniziativa"]].append(x)
    pg = defaultdict(list)
    for l in open(d / "pagine.jsonl", encoding="utf-8"):
        x = json.loads(l); pg[x["iniziativa"]].append(x)
    campi = ["iniziativa", "documento_atteso", "fonte_tipo", "ente", "url_pagina", "url_documento", "sha256", "data", "esito", "livello", "note"]
    with open(out, "w", newline="", encoding="utf-8") as fo:
        w = csv.DictWriter(fo, fieldnames=campi); w.writeheader()
        for m in mancanti:
            i, doc = m["iniziativa"], m["documento_atteso"]
            _, parole, rx_t = cat(doc)
            cand = []
            for a in al[i]:
                if not a.get("sha256") or not a.get("parole"):
                    continue
                s = sum(a["parole"].get(p, 0) for p in parole)
                if s and re.search(rx_t, a.get("testo", "") + " " + a["url"], re.I):
                    cand.append((s + 5 * bool(a["parole"].get("cig_padre")), a))
            cand.sort(key=lambda t: -t[0])
            if cand:
                for s, a in cand[:3]:
                    pz = {k: v for k, v in a["parole"].items() if v}
                    w.writerow({"iniziativa": i, "documento_atteso": doc, "fonte_tipo": "at-ente", "ente": a["ente"], "url_pagina": a["url_pagina"],
                                "url_documento": a["url"], "sha256": a["sha256"], "data": "2026-11-07", "esito": "trovato-parziale", "livello": "V",
                                "note": f"allegato «{a.get('testo','')[:80]}» del CIG derivato {a['cig']} nella pagina PVL dell'ente; parole nel testo estratto: {pz}; "
                                        "controllo automatico per parole (pdftotext, prime 30 pagine): atto del singolo aderente, non il documento dell'iniziativa"})
            else:
                p = pg[i]
                fonti = "; ".join(f"{x['ente'][:40]} {x['url'][:90]} (HTTP {x.get('http','')}{', ' + x['blocco'] if x.get('blocco') else ''}{', errore' if x.get('errore') else ''}, {len(x['link'])} link pertinenti)" for x in p[:6])
                na = sum(1 for a in al[i] if a.get("sha256"))
                w.writerow({"iniziativa": i, "documento_atteso": doc, "fonte_tipo": "at-ente" if p else "bdncp", "ente": "", "url_pagina": "", "url_documento": "",
                            "sha256": "", "data": "2026-11-07", "esito": "non-trovato", "livello": "V",
                            "note": (f"provate {len(p)} pagine PVL «documenti di gara» di CIG derivati: {fonti}; {na} allegati archiviati e letti, nessuno con il contenuto atteso"
                                     if p else "nessun CIG derivato con link PVL ai documenti (cig_completo 2022-2026 × lavoro/pvl/cig_link.csv)")})


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
