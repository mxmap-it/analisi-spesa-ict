#!/usr/bin/env python3
"""Genera la pagina «Mappa dell'imbuto» e i suoi grafici (#71 #74, richiesta di Fabio 19/11/2026).

Ingressi:  config/mappa-imbuto.yaml (dataset, relazioni, livelli, mancanze: la fonte unica, si aggiorna a mano)
           esiti più recenti dell'imbuto e dei livelli (percorsi nella sezione `esiti` del YAML)
Uscite:    sito/content/progetto/mappa-imbuto.md
           sito/static/img/mappa-imbuto/{imbuto,relazioni,mancanze}.svg
Deterministico: stessi ingressi, stessi file. Solo libreria standard + PyYAML, nessun programma esterno.
Uso:  python3 tools/pagina_mappa_imbuto.py   poi   hugo --source sito --minify --cleanDestinationDir
"""
import collections, glob, html, json, os, textwrap
from pathlib import Path

import yaml

R = Path(__file__).resolve().parents[1]
CFG = yaml.safe_load(open(R / "config/mappa-imbuto.yaml", encoding="utf-8"))
IMG = R / "sito/static/img/mappa-imbuto"
PAGINA = R / "sito/content/progetto/mappa-imbuto.md"
FONT = "'Titillium Web', 'Segoe UI', Arial, sans-serif"
GRAV = {"alta": "#b3261e", "media": "#e69138", "bassa": "#6aa84f"}
STATO = {"aperta": "aperta", "in-corso": "in corso", "mitigata": "mitigata", "risolta": "risolta", "decisione-fabio": "decisione di Fabio"}


def ultimo(pat):
    f = sorted(glob.glob(str(R / pat)))
    return f[-1] if f else None


def leggi(pat):
    p = ultimo(pat)
    return (json.load(open(p, encoding="utf-8")), os.path.relpath(p, R)) if p else (None, None)


def it(n, dec=0):
    s = f"{n:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def e(s):
    return html.escape(str(s), quote=True)


# ------------------------------------------------------------------ numeri dagli esiti
def numeri():
    n = {"fonti": {}}
    st, p = leggi(CFG["esiti"]["strati"]); n["fonti"]["strati"] = p
    tot = {r["chiave"]: r for r in st["totale"]}["dal-2024"]
    n["universo"] = (tot["cig"], tot["euro"] / 1e9)
    s = collections.defaultdict(lambda: [0, 0.0])
    for r in st["strati"]:
        if r["chiave"][0] == "dal-2024":
            s[r["chiave"][1][:2]][0] += r["cig"]; s[r["chiave"][1][:2]][1] += r["euro"] / 1e9
    n["strati"] = s
    a = {r["chiave"][1]: (r["cig"], r["euro"] / 1e9) for r in st["asse_a"] if r["chiave"][0] == "dal-2024"}
    def trova(prefisso):
        return next(v for k, v in a.items() if k.startswith(prefisso))
    n["asse_a"] = {"cloud": trova("incluso certo (cloud)"), "inhouse": trova("incluso certo (infrastruttura"),
                   "marchio": trova("incerto (marchio"), "s5": trova("ICT non cloud"), "s6": trova("incerto (residuo")}
    n["fonti"]["l2"] = leggi(CFG["esiti"]["raffinamento_l2"])[1]
    l3, p = leggi(CFG["esiti"]["raffinamento_l3"]); n["fonti"]["l3"] = p
    if l3:
        es = l3["esiti"]
        n["l3"] = {k: (v["cig"], v["euro"] / 1e9) for k, v in es.items()}
    b, p = leggi(CFG["esiti"]["bdncp"]); n["fonti"]["bdncp"] = p
    n["b1"] = (b["b1_quadro_economico"]["esce_lavori"]["cig"], b["b1_quadro_economico"]["esce_lavori"]["importo"] / 1e3)
    n["b2"] = b["b2_inhouse"]
    n["ict_dal_2024"] = b["cig_ict_dal_2024"]
    lotti = sum(1 for f in glob.glob(str(R / CFG["esiti"]["l4_lotti"])) for l in open(f, encoding="utf-8") if l.strip())
    letti = collections.Counter()
    for f in glob.glob(str(R / CFG["esiti"]["l4_esiti"])):
        for l in open(f, encoding="utf-8"):
            try:
                x = json.loads(l)
            except json.JSONDecodeError:
                continue
            letti[x["asse_a"].get("stato", "?")] += 1
    n["l4"] = (lotti, letti)
    rip, p = leggi("esiti/*/ripetibilita/esito.json"); n["ripetibilita"] = (rip, p)
    return n


def l2_totale():
    """raffinamento-l2.json: somma dei gruppi se non c'è un totale esplicito."""
    d, _ = leggi(CFG["esiti"]["raffinamento_l2"])
    if not d:
        return None
    righe = [r for r in d.get("per_gruppo", []) if r.get("livello") == "L2"]
    return (sum(r["cig"] for r in righe), sum(r["euro"] for r in righe) / 1e9) if righe else None


# ------------------------------------------------------------------ SVG
def svg(w, h, corpo, titolo):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{e(titolo)}" '
            f'font-family="{FONT}"><title>{e(titolo)}</title><rect width="{w}" height="{h}" fill="#ffffff"/>{corpo}</svg>\n')


def testo(x, y, s, size=13, peso="normal", colore="#1a1a1a", anchor="start"):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{peso}" fill="{colore}" text-anchor="{anchor}">{e(s)}</text>'


def svg_imbuto(n):
    W, H = 1000, 700
    o = []
    righe = [
        ("Universo ANAC dal 2024", f"{it(n['universo'][0])} CIG · {it(n['universo'][1])} mld € dichiarati", 960, "#5b6770"),
        ("Esclusi: non ICT (S1), padri di accordo quadro (S0), sotto 500 € (S2)",
         f"S1 {it(n['strati']['S1'][0])} CIG ({it(100 * n['strati']['S1'][0] / n['universo'][0], 1)} %) · S0 {it(n['strati']['S0'][0])} · S2 {it(n['strati']['S2'][0])}", 860, "#9aa5ad"),
        ("Spesa ICT: strati S3-S6", f"{it(n['ict_dal_2024'])} CIG · {it(sum(n['strati'][k][1] for k in ('S3', 'S4', 'S5', 'S6')), 1)} mld dichiarati (56,06 al netto dei tetti)", 760, "#0b5394"),
    ]
    y = 20
    for i, (t, sub, w, c) in enumerate(righe):
        x = (W - w) / 2
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="62" rx="6" fill="{c}"/>')
        o.append(testo(W / 2, y + 26, t, 16, "bold", "#ffffff", "middle"))
        o.append(testo(W / 2, y + 47, sub, 13, "normal", "#ffffff", "middle"))
        o.append(f'<path d="M{W/2} {y+64} l0 14" stroke="#5b6770" stroke-width="2" marker-end="url(#fr)"/>')
        y += 88
    o.insert(0, '<defs><marker id="fr" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#5b6770"/></marker></defs>')
    # barra degli assi: S3-S6 per esito sull'asse A
    aa = n["asse_a"]
    parti = [("cloud certo", aa["cloud"], "#2e7d32"), ("in-house certo", aa["inhouse"], "#66bb6a"),
             ("marchio noto, cloud da accertare", aa["marchio"], "#f6b26b"), ("residuo incerto S6", aa["s6"], "#e06666"),
             ("ICT non cloud S5", aa["s5"], "#9fc5e8")]
    tot = sum(p[1][1] for p in parti)
    x0, bw = 40, 920
    o.append(testo(40, y + 6, "Come si dividono i 114 mld dichiarati di S3-S6 (larghezza proporzionale agli euro)", 14, "bold"))
    y += 18
    x = x0
    for nome, (c, eu), col in parti:
        w = max(bw * eu / tot, 3)
        o.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="34" fill="{col}"/>')
        x += w
    y += 52
    for i, (nome, (c, eu), col) in enumerate(parti):
        cx = 40 + (i % 3) * 320; cy = y + (i // 3) * 40
        o.append(f'<rect x="{cx}" y="{cy - 12}" width="14" height="14" fill="{col}"/>')
        o.append(testo(cx + 20, cy, f"{nome}", 13, "bold"))
        o.append(testo(cx + 20, cy + 16, f"{it(c)} CIG · {it(eu, 2)} mld", 12, "normal", "#444"))
    y += 96
    # raffinamento
    o.append(testo(40, y, "Raffinamento sopra l'imbuto: escono dalla misura cloud (restano spesa ICT salvo «non ICT»)", 14, "bold"))
    y += 14
    liv = []
    l2 = l2_totale()
    if l2:
        liv.append(("L2 regole: stampanti, consumabili, cablaggio", l2))
    liv.append(("B1 quadro economico: contratti di lavori", n["b1"]))
    if n.get("l3"):
        l3 = n["l3"]
        out = [l3.get("esce-ict-non-cloud", (0, 0)), l3.get("esce-non-ict", (0, 0))]
        liv.append(("L3 Opus sul testo: escono con certezza alta", (sum(c for c, _ in out), sum(v for _, v in out))))
        liv.append(("L3 → L4: incerti mandati agli atti", l3.get("resta-incerto-L4", (0, 0))))
    mx = max(v for _, (c, v) in liv)
    for nome, (c, v) in liv:
        y += 30
        o.append(testo(40, y + 4, nome, 13))
        w = 420 * v / mx
        o.append(f'<rect x="440" y="{y - 10}" width="{w:.1f}" height="18" fill="#3d85c6"/>')
        o.append(testo(448 + w, y + 4, f"{it(c)} CIG · {it(v * 1000)} M€", 12, "normal", "#333"))
    lotti, letti = n["l4"]
    y += 36
    o.append(testo(40, y, f"L4 Opus con gli atti: {it(sum(letti.values()))} letti su {it(lotti)} "
                         f"({it(letti.get('escluso-certo', 0))} non cloud, {it(letti.get('incluso-certo', 0))} cloud, {it(letti.get('incerto', 0))} ancora incerti)", 13, "normal", "#333"))
    H = y + 24
    return svg(W, H, "".join(o), "Il disegno dell'imbuto con i numeri dal 2024")


def wrap(s, n=28):
    return textwrap.wrap(s, n)[:2]


def svg_relazioni():
    ds = {d["id"]: d for d in CFG["dataset"]}
    gr = CFG["gruppi"]
    est = {d["id"] for d in CFG["dataset"] if d["gruppo"] == "esterni"}
    ponte = {r["da"] for r in CFG["relazioni"] if r["a"] in est and ds[r["da"]]["gruppo"] == "bdncp"}
    col = {}
    for d in CFG["dataset"]:
        g = d["gruppo"]
        col[d["id"]] = 1 if g in ("anac", "nostri") else 3 if g == "esterni" else 2 if d["id"] in ponte else 0
    X = {0: 20, 1: 330, 2: 640, 3: 950}; NW, NH, GAP = 220, 58, 18
    ordine = collections.defaultdict(list)
    for d in CFG["dataset"]:
        ordine[col[d["id"]]].append(d["id"])
    # anac in alto, nostri in basso nella colonna 1
    ordine[1].sort(key=lambda i: ds[i]["gruppo"] == "nostri")
    pos = {}
    for c, ids in ordine.items():
        if c == 3:  # esterni: prima quelli collegati ai ponti, nell'ordine dei ponti
            yp = {}
            for r in CFG["relazioni"]:
                if r["a"] in ids and r["da"] in ordine[2]:
                    yp.setdefault(r["a"], ordine[2].index(r["da"]))
            ids.sort(key=lambda i: yp.get(i, 99))
        y = 60 + (40 if c == 0 else 0)
        for i in ids:
            pos[i] = (X[c], y); y += NH + GAP
    H = max(p[1] for p in pos.values()) + NH + 100
    W = 1300
    o = ['<defs><marker id="fr2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="#7a7a7a"/></marker></defs>']
    for c, t in ((0, "BDNCP collegati solo per CIG"), (1, "CIG: il centro"), (2, "BDNCP che fanno da ponte"), (3, "Fonti esterne")):
        o.append(testo(X[c] + NW / 2, 30, t, 14, "bold", "#333", "middle"))
    # archi: ogni arco esce ed entra da un lato del riquadro; le porte sullo stesso lato si distribuiscono in altezza,
    # le etichette stanno vicino all'arrivo (non al centro, dove si accavallerebbero)
    def lati(r):
        c1, c2 = col[r["da"]], col[r["a"]]
        if c1 == c2:
            return "d", "d"
        return ("s", "d") if c2 < c1 else ("d", "s")
    porte = collections.defaultdict(list)
    for k, r in enumerate(CFG["relazioni"]):
        ls, la = lati(r)
        porte[(r["da"], ls)].append((pos[r["a"]][1], k, "da"))
        porte[(r["a"], la)].append((pos[r["da"]][1], k, "a"))
    yporta = {}
    for (nodo, lato), lst in porte.items():
        lst.sort()
        for i, (_, k, ruolo) in enumerate(lst):
            yporta[(k, ruolo)] = pos[nodo][1] + NH * (i + 1) / (len(lst) + 1)
    etichette = []
    for k, r in enumerate(CFG["relazioni"]):
        (x1, _), (x2, _) = pos[r["da"]], pos[r["a"]]
        c1, c2 = col[r["da"]], col[r["a"]]
        sy, ty = yporta[(k, "da")], yporta[(k, "a")]
        ls, la = lati(r)
        sx = x1 + NW if ls == "d" else x1
        tx = x2 + NW if la == "d" else x2
        if c1 == c2:  # stessa colonna: arco sul lato destro
            d = f"M{sx} {sy} C{sx + 45} {sy} {tx + 45} {ty} {tx + 2} {ty}"
            lx, ly, an = sx + 40, (sy + ty) / 2 + 4, "start"
        elif ls == "s":  # verso sinistra
            d = f"M{sx} {sy} C{sx - 40} {sy} {tx + 40} {ty} {tx + 2} {ty}"
            lx, ly, an = tx + 8, ty - 5, "start"
        elif c2 - c1 == 2:  # salta la colonna dei ponti: passa sotto
            yb = H - 52
            d = f"M{sx} {sy} C{sx + 40} {yb} {tx - 60} {yb} {tx - 2} {ty}"
            lx, ly, an = (sx + tx) / 2 - 10, 0.125 * (sy + ty) + 0.75 * yb - 6, "middle"
        else:
            d = f"M{sx} {sy} C{sx + 40} {sy} {tx - 40} {ty} {tx - 2} {ty}"
            lx, ly, an = tx - 8, ty - 5, "end"
        o.append(f'<path d="{d}" fill="none" stroke="#9a9a9a" stroke-width="1.4" marker-end="url(#fr2)"/>')
        et = r["chiave"] + (f" · {r['copertura']}" if r.get("copertura") else "")
        if r["chiave"] != "CIG" or r.get("copertura"):
            etichette.append((lx, ly, et, an))
    for d in CFG["dataset"]:
        x, y = pos[d["id"]]; g = gr[d["gruppo"]]
        trat = ' stroke-dasharray="5 3"' if d["stato"] in ("da-usare", "campione", "usato-poco") else ""
        o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" fill="#ffffff" stroke="{g["colore"]}" stroke-width="2.2"{trat}/>')
        o.append(f'<rect x="{x}" y="{y}" width="6" height="{NH}" rx="2" fill="{g["colore"]}"/>')
        nome = d["nome"].split(" (")[0]
        for k, riga in enumerate(wrap(nome, 30)):
            o.append(testo(x + 14, y + 20 + k * 15, riga, 13, "bold"))
        o.append(testo(x + 14, y + NH - 8, "chiave: " + d["chiave"], 11, "normal", "#555"))
    for lx, ly, et, an in etichette:
        w = 6.0 * len(et) + 8
        x0 = lx - w / 2 if an == "middle" else lx - 4 if an == "start" else lx - w + 4
        o.append(f'<rect x="{x0:.1f}" y="{ly - 11:.1f}" width="{w:.1f}" height="15" rx="3" fill="#ffffff" fill-opacity="0.95"/>')
        o.append(testo(lx, ly, et, 11, "normal", "#333", an))
    # legenda su due righe
    ly = H - 24; lx = 20
    for g in gr.values():
        o.append(f'<rect x="{lx}" y="{ly - 11}" width="14" height="14" fill="{g["colore"]}"/>')
        o.append(testo(lx + 20, ly, g["nome"], 12)); lx += 20 + 6.2 * len(g["nome"]) + 28
    o.append(f'<rect x="20" y="{H - 13}" width="14" height="14" fill="none" stroke="#555" stroke-dasharray="4 2"/>')
    o.append(testo(40, H - 1, "bordo tratteggiato: da usare, usato a campione o poco usato", 12, "normal", "#555"))
    return svg(W, H + 8, "".join(o), "Relazioni fra i dataset dell'imbuto")


def svg_mancanze():
    ms = sorted(CFG["mancanze"], key=lambda m: (["alta", "media", "bassa"].index(m["gravita"]), -(m["peso_mld"] or 0)))
    mx = max((m["peso_mld"] or 0) for m in ms)
    W, RH = 1060, 34
    o = [testo(20, 24, "Peso in miliardi di euro dichiarati (dove misurato), colore = gravità", 14, "bold")]
    y = 50
    for m in ms:
        o.append(testo(20, y + 15, f"{m['id']} {m['titolo']}"[:88], 13))
        if m["peso_mld"]:
            w = 380 * m["peso_mld"] / mx
            o.append(f'<rect x="600" y="{y + 2}" width="{w:.1f}" height="20" fill="{GRAV[m["gravita"]]}"/>')
            o.append(testo(606 + w, y + 17, f"{it(m['peso_mld'], 2)} mld", 12, "normal", "#333"))
        else:
            o.append(f'<rect x="600" y="{y + 2}" width="60" height="20" fill="none" stroke="{GRAV[m["gravita"]]}" stroke-width="2" stroke-dasharray="4 3"/>')
            o.append(testo(668, y + 17, "non misurato", 12, "normal", "#555"))
        y += RH
    lx = 20; y += 12
    for g, c in GRAV.items():
        o.append(f'<rect x="{lx}" y="{y - 11}" width="14" height="14" fill="{c}"/>'); o.append(testo(lx + 20, y, f"gravità {g}", 12)); lx += 130
    return svg(W, y + 12, "".join(o), "Mancanze dell'imbuto per peso e gravità")


# ------------------------------------------------------------------ pagina
def pagina(n):
    v = CFG["versione"]; agg = CFG["aggiornato"]
    L = []
    a = L.append
    a(f'''---
title: "Mappa dell'imbuto: dati, relazioni, limiti e mancanze"
date: 2026-11-19
lastmod: {agg}
description: "Il punto di riferimento sempre aggiornato: quali dataset usa l'imbuto e come si collegano, il disegno dei livelli con i numeri, i limiti di ogni fonte, le mancanze con gravità e piano per risolverle, cosa è ripetibile."
weight: 17
---

<!-- PAGINA GENERATA da tools/pagina_mappa_imbuto.py da config/mappa-imbuto.yaml e dagli esiti: non modificarla a mano. -->

**Versione {v}, aggiornata il {agg}.** Questa pagina è il **punto di riferimento** del progetto: si rigenera a ogni avanzamento. Testi, dataset, relazioni e mancanze stanno in [`config/mappa-imbuto.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/mappa-imbuto.yaml); i numeri si leggono dagli esiti più recenti, con il file indicato sotto ogni figura. I dettagli stanno nel rendiconto [«Imbuto: dove siamo»](/rendiconti/imbuto-dove-siamo/) e nella pagina di metodo [Raffinamento dell'imbuto a livelli](/progetto/raffinamento-imbuto/).

**Obiettivo:** misurare quanto spende la PA italiana in servizi cloud e infrastrutture informatiche, per giurisdizione del prodotto (Italia, UE, extra-UE), con un processo che si rifà ogni anno. **Unità:** il contratto (CIG). **Due domande per ogni contratto:** è cloud? di quale giurisdizione?

## 1. Il disegno dell'imbuto

![Il disegno dell'imbuto con i numeri dal 2024](/img/mappa-imbuto/imbuto.svg)

<small>Numeri dal 2024. Fonti: `{n['fonti']['strati']}`, `{n['fonti']['bdncp']}`, `{n['fonti']['l3']}`, esiti L4 in `report/metodo/llm/raffinamento-l4/esiti/`. Gli importi sono **dichiarati** (valore dei contratti): il totale al netto dei massimali di accordo quadro è nel rendiconto, § 2.7.</small>

Come funziona:
- **L1, gli strati.** Ogni contratto passa per gli strati in ordine:
  - S0 padri di accordo quadro, contati negli attuativi;
  - S1 non ICT, escluso con certezza;
  - S2 sotto 500 €;
  - S3 convenzione o lotto noto;
  - S4 marchio nel testo;
  - S5 ICT non cloud;
  - S6 incerto.
- **Il principio:** prima si esclude ciò che è certamente fuori, poi si include ciò che è certamente dentro, e lo sforzo costoso va solo sull'incerto.
- **I livelli di raffinamento** stanno **sopra** gli strati e non li modificano. Ognuno scrive una tabella per CIG, con il motivo e la via che ha deciso.

| livello | mezzo | ingresso | uscita | strumento | ripetibile |
|---|---|---|---|---|---|''')
    for l in CFG["livelli"]:
        a(f"| **{l['id']}** {l['nome']} | {l['mezzo']} | {l['ingresso']} | {l['uscita']} | `{l['strumento']}` | {'sì, identico' if l['deterministico'] else 'esiti versionati (modello linguistico)'} |")
    a('''
## 2. I dati e come si collegano

![Relazioni fra i dataset dell'imbuto](/img/mappa-imbuto/relazioni.svg)

<small>Una freccia è un collegamento: la chiave (CIG, codice fiscale, CUP) e, dove misurata, la quota dei CIG ICT dal 2024 che il collegamento copre. Il CIG è il centro: tutto ciò che sappiamo di un contratto si attacca al suo codice.</small>

| dataset | chiave | cosa usiamo | a che cosa serve | stato |
|---|---|---|---|---|''')
    st = {"usato": "usato", "usato-poco": "usato poco", "da-usare": "**da usare**", "campione": "a campione"}
    for d in CFG["dataset"]:
        a(f"| **{d['nome']}** | {d['chiave']} | {d['campi']} | {d['ruolo']} | {st.get(d['stato'], d['stato'])} |")
    a('''
## 3. I limiti di ogni fonte

Ogni limite è un motivo per cui un numero potrebbe essere sbagliato. Dove c'è un codice il problema è documentato con evidenza: **P** nelle [schede dei problemi dei dati ANAC](/rendiconti/anac-2026-10-problemi/), **R** nelle [raccomandazioni agli enti](/progetto/raccomandazioni/).
''')
    for d in CFG["dataset"]:
        if d["limiti"]:
            a(f"- **{d['nome']}**")
            for x in d["limiti"]:
                a(f"  - {x}")
    a('''
## 4. Che cosa manca, quanto pesa, come lo risolviamo

![Mancanze dell'imbuto per peso e gravità](/img/mappa-imbuto/mancanze.svg)

<small>I pesi **non si sommano**: una mancanza può stare dentro un'altra. Per esempio il PSN (M2) è una parte del residuo S6 (M1). Gli importi da verificare (M4) toccano contratti di tutti gli strati.</small>

**Gravità**, con un criterio fisso per poterla confrontare nel tempo:
- **alta:** può spostare la quota cloud o la giurisdizione di oltre 1 miliardo, oppure riguarda oltre il 10 % della spesa ICT senza misura;
- **media:** pesa fra 0,1 e 1 miliardo, oppure tocca un passo intermedio senza cambiare il risultato finale;
- **bassa:** pesa sotto 0,1 miliardi, oppure è un problema di qualità del dato già aggirato.

| | mancanza | peso | gravità | perché conta | come la risolviamo | ticket | stato |
|---|---|---|---|---|---|---|---|''')
    for m in sorted(CFG["mancanze"], key=lambda m: (["alta", "media", "bassa"].index(m["gravita"]), -(m["peso_mld"] or 0))):
        tk = ", ".join(f"[{t}](https://github.com/mxmap-it/analisi-spesa-ict/issues/{t[1:]})" for t in m["ticket"])
        a(f"| {m['id']} | **{m['titolo']}** | {m['peso']} | {m['gravita']} | {m['perche']} | {m['come']} | {tk} | {STATO[m['stato']]} |")
    rip, rp = n["ripetibilita"]
    a('''
## 5. Ripetibilità

- **Deterministici: L1, B, L2.** Con gli stessi file d'ingresso (sha256 nel manifest dell'archivio e nei riepiloghi) danno lo stesso risultato, byte per byte.
- **Non deterministici: L3 e L4.** Usano un modello linguistico, che riletto da capo dà risposte vicine ma non identiche. Per questo i loro esiti sono versionati in git e si **rileggono**, non si rigenerano; lo scarto si misura sui campioni a cieco.
- **I comandi in ordine** sono nella pagina [Raffinamento dell'imbuto a livelli](/progetto/raffinamento-imbuto/#rifarlo-ogni-anno) e in [RIPRODURRE.md](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/RIPRODURRE.md).''')
    if rip:
        a(f"\n**Ultimo test di ripetibilità** (`{rp}`): {rip.get('sintesi', 'vedi il file')}\n")
        if isinstance(rip.get("passi"), list):
            a("| passo | esito | nota |\n|---|---|---|")
            for p in rip["passi"]:
                a(f"| {p.get('passo', '')} | {p.get('esito', '')} | {p.get('nota', '')} |")
    else:
        a("\nIl test di ripetibilità di questa versione è in corso: l'esito comparirà qui alla prossima rigenerazione.")
    a(f'''
## 6. Come si aggiorna questa pagina

1. **Quando cambia qualcosa, si aggiorna il file dati.** È [`config/mappa-imbuto.yaml`](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/config/mappa-imbuto.yaml). Per esempio:
   - un dataset nuovo, con la sua chiave e i suoi limiti;
   - una relazione nuova;
   - una mancanza che cambia stato;
   - un livello nuovo.

   Ogni numero scritto lì deve essere già pubblicato in un rendiconto, con la sua fonte.
2. **Si rigenera:** `python3 tools/pagina_mappa_imbuto.py`. I numeri dell'imbuto si rileggono dagli esiti più recenti.
3. **Si costruisce il sito e si pubblica:** `hugo --source sito --minify --cleanDestinationDir`, poi commit di sorgente e `docs/`, poi push.
4. **Si annota la modifica** nel registro qui sotto, nel YAML, alla voce `registro`.

## Registro delle revisioni

| data | versione | modifica |
|---|---|---|''')
    for r in CFG.get("registro", []):
        a(f"| {r['data']} | {r['versione']} | {r['modifica']} |")
    return "\n".join(L) + "\n"


def main():
    n = numeri()
    IMG.mkdir(parents=True, exist_ok=True)
    for nome, f in (("imbuto", lambda: svg_imbuto(n)), ("relazioni", svg_relazioni), ("mancanze", svg_mancanze)):
        (IMG / f"{nome}.svg").write_text(f(), encoding="utf-8")
    PAGINA.write_text(pagina(n), encoding="utf-8")
    print("scritti", PAGINA.relative_to(R), "e", len(list(IMG.glob("*.svg"))), "grafici")


if __name__ == "__main__":
    main()
