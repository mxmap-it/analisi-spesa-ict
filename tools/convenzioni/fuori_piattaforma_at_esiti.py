"""#62 fuori piattaforma, passo 5: dagli at-visite.jsonl del passo 4 produce
- report/convenzioni/fuori-piattaforma/at-enti-2026-11-07.csv (una riga per ente visitato);
- l'aggiornamento di trovati-2026-11-07.csv: righe non-trovato -> trovato-parziale se un allegato archiviato di un CIG derivato
  dell'iniziativa contiene le parole del documento atteso (controllo automatico, livello V-auto da rileggere), e nota con le fonti AT provate;
- at-blocchi-nuovi.csv (righe da accodare a report/convenzioni/blocchi-accesso.csv).
Uso: python fuori_piattaforma_at_esiti.py <dir con at-visite.jsonl, derivati.csv> <cartella report/convenzioni>"""
import csv, json, re, sys
from collections import defaultdict
from pathlib import Path

CAT = [(r"ordinativ|contratti attuativi", ["ordinativo", "contratto_esecutivo"]), (r"flussi|transato|erosion", ["transato"]),
       (r"fabbisogn", ["piano_fabbisogni", "progetto_fabbisogni"]), (r"offerta tecnica", ["offerta_tecnica"]),
       (r".", ["offerta_economica", "listino", "prezzi"])]
CRIT3 = ["ordinativo", "contratto_esecutivo", "piano_fabbisogni", "progetto_fabbisogni", "offerta_economica", "offerta_tecnica", "listino", "transato"]


def main(d, rep):
    d, rep = Path(d), Path(rep)
    vis = {}
    for l in open(d / "at-visite.jsonl", encoding="utf-8"):
        x = json.loads(l); vis[x["cf_ente"]] = x
    cig_ini = defaultdict(set)
    for r in csv.DictReader(open(d / "derivati.csv", encoding="utf-8")):
        cig_ini[r["cig"]].add(r["iniziativa"])
    ente_ini = defaultdict(set)
    for r in csv.DictReader(open(d / "derivati.csv", encoding="utf-8")):
        if r["cf_ente"] in vis:
            ente_ini[r["iniziativa"]].add(r["cf_ente"])
    campi = ["cf_ente", "ente", "sito_ipa", "url_sezione_at", "data", "http", "esito_sezione", "n_cig_cercati", "n_atti_trovati", "n_allegati_crit3", "blocco"]
    trov_ini = defaultdict(list)
    with open(rep / "fuori-piattaforma/at-enti-2026-11-07.csv", "w", newline="", encoding="utf-8") as fo:
        w = csv.DictWriter(fo, fieldnames=campi); w.writeheader()
        for cf, x in vis.items():
            crit = [a for a in x["allegati"] if a.get("sha256") and (a.get("cig_nel_testo") or a.get("padri_nel_testo"))
                    and any(a["parole"].get(p) for p in CRIT3)]
            for a in crit:
                for c in a.get("cig_nel_testo") or a.get("cig_pagina") or []:
                    for i in cig_ini[c]:
                        trov_ini[i].append((x, a, c))
            w.writerow({"cf_ente": cf, "ente": x["ente"], "sito_ipa": x["sito_ipa"], "url_sezione_at": x.get("url_sezione_at", ""), "data": x["data"][:10],
                        "http": x.get("http", ""), "esito_sezione": x["esito_sezione"], "n_cig_cercati": x["n_cig"],
                        "n_atti_trovati": len(x["cig_trovati"]), "n_allegati_crit3": len(crit), "blocco": x["blocco"]})
    # trovati
    p = rep / "fuori-piattaforma/trovati-2026-11-07.csv"
    righe = list(csv.DictReader(open(p, encoding="utf-8")))
    out = []
    for r in righe:
        if r["esito"] != "non-trovato":
            out.append(r); continue
        i = r["iniziativa"]
        parole = next(c[1] for c in CAT if re.search(c[0], r["documento_atteso"], re.I))
        enti = ente_ini.get(i, set())
        prov = "; ".join(f"{vis[c]['ente'][:35]} ({vis[c]['esito_sezione']}{', ' + vis[c]['blocco'] if vis[c]['blocco'] else ''}, {len(vis[c]['cig_trovati'])} CIG nelle pagine)"
                         for c in sorted(enti)[:8])
        nota_at = f" | AT enti aderenti (#62, 7/11): visitate {len(enti)} sezioni" + (f": {prov}" + (" …" if len(enti) > 8 else "") if enti else "")
        hit = [(x, a, c) for x, a, c in trov_ini.get(i, []) if any(a["parole"].get(q) for q in parole)]
        if hit:
            for x, a, c in hit[:3]:
                pz = {k: v for k, v in a["parole"].items() if v}
                out.append({**r, "fonte_tipo": "at-ente", "ente": x["ente"], "url_pagina": a["url_pagina"], "url_documento": a["url"], "sha256": a["sha256"],
                            "esito": "trovato-parziale", "livello": "V-auto",
                            "note": f"atto del CIG derivato {c} nella sezione AT dell'ente; parole nel testo (pdftotext, 30 pp.): {pz}; atto del singolo aderente, da rileggere a mano"})
        else:
            out.append({**r, "note": r["note"] + (nota_at if enti else "")})
    with open(p, "w", newline="", encoding="utf-8") as fo:
        w = csv.DictWriter(fo, fieldnames=list(righe[0].keys())); w.writeheader(); w.writerows(out)
    with open(d / "at-blocchi-nuovi.csv", "w", newline="", encoding="utf-8") as fo:
        w = csv.writer(fo)
        for cf, x in vis.items():
            if x["blocco"] and x["blocco"] != "login":
                w.writerow([x.get("url_blocco", ""), "#62-at", f"sezione AT/Bandi di gara di {x['ente']}", x["blocco"], x["data"], x.get("http_blocco", ""),
                            x.get("sha_blocco", ""), f"lavoro/convenzioni/fuori-piattaforma/at-html/{x.get('sha_blocco','')}.html (server)", "Chrome headless, UA dichiarato; non aggirato"])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
