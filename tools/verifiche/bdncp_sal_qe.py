#!/usr/bin/env python3
"""#74, due punti aperti del rendiconto report/metodo/bdncp-e-l190-inventario.md (§ 3.9 e proposte 1):
  1. stati-avanzamento: `importo_sal` è l'importo del singolo SAL o il totale progressivo? Se fosse progressivo, la somma
     delle righe (19,17 mld € sui CIG ICT il 18/11) conterebbe più volte la stessa spesa.
     Prove, sui CIG ICT S3-S6 dal 2020 con almeno due SAL (ordinati per progressivo_sal, poi data):
       a) successioni non decrescenti (un progressivo lo è sempre; importi singoli lo sono per caso);
       b) somma delle righe e massimo per CIG contro l'importo del lotto (ict.csv): se progressivo, la somma supera
          spesso l'importo mentre il massimo no; se singolo, la somma resta vicina o sotto l'importo;
       c) righe ripetute identiche (stesso CIG, progressivo, data e importo): doppioni da togliere in ogni caso;
       d) il SAL «finale» (denominazione con FINALE/ULTIMO/CONTO FINALE) contro la somma dei precedenti.
  2. quadro-economico: somme per componente (forniture, servizi, lavori, progettazione, sicurezza, oneri, somme a
     disposizione) per evento (BASE_ASTA, VARIANTE, CONSUNTIVO, ...) sui CIG ICT, e importo del quadro per CIG (ultimo
     evento: consuntivo, poi variante, poi base d'asta) con percentili e rapporto con l'importo del lotto.
Ingresso: lavoro/imbuto/ict.csv (IMBUTO_ICT) e gli zip «pieni» del mirror ANAC (come imbuto_bdncp.py), in streaming.
Uso (server, nice, dopo free -g): flock lavoro/pesante.lock nice .venv/bin/python tools/verifiche/bdncp_sal_qe.py
  -> esiti/<oggi>/bdncp/sal-qe.json
"""
import collections, csv, datetime, hashlib, io, json, os, re, statistics, zipfile
from pathlib import Path

R = Path(__file__).resolve().parents[2]
D = R / "archivio/mirror/dati.anticorruzione.it/opendata/download/dataset"
ICT = R / os.environ.get("IMBUTO_ICT", "lavoro/imbuto/ict.csv")
OGGI = os.environ.get("ESITI_DATA", datetime.date.today().isoformat())
OUT = R / f"esiti/{OGGI}/bdncp"
csv.field_size_limit(1 << 30)
RX_FINALE = re.compile(r"finale|ultimo|conto\s+final|saldo", re.I)
COMP = ["importo_forniture", "importo_servizi", "importo_lavori", "importo_progettazione", "importo_sicurezza",
        "ulteriori_oneri_non_soggetti_ribasso"]
ORDINE_EVENTO = {"CONSUNTIVO": 3, "VARIANTE": 2, "BASE_ASTA": 1}
ingressi = {}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def num(x):
    try:
        return float((x or "").replace(",", "."))
    except ValueError:
        return 0.0


def righe(ds):
    z = D / ds / "filesystem" / f"{ds}_csv.zip"
    ingressi[str(z.relative_to(R))] = {"sha256": sha(z), "byte": z.stat().st_size}
    zf = zipfile.ZipFile(z)
    m = next(n for n in zf.namelist() if n.endswith(".csv"))
    return csv.DictReader(io.TextIOWrapper(zf.open(m), encoding="utf-8-sig", errors="replace"), delimiter=";")


def q(v, ps=(.1, .25, .5, .75, .9, .99)):
    v = sorted(v)
    return {f"p{int(p * 100)}": round(v[int(p * (len(v) - 1))], 3) for p in ps} if v else {}


def mld(x):
    return round(x / 1e9, 3)


def main():
    ict = {}
    ingressi[str(ICT.relative_to(R))] = {"sha256": sha(ICT)}
    for r in csv.DictReader(open(ICT, encoding="utf-8")):
        if r["strato"][:2] in ("S3", "S4", "S5", "S6") and int(r["anno"] or 0) >= 2020:
            ict[r["cig"]] = (num(r["importo"]), r["importo_da_verificare"] == "1")
    out = {"versione": "bdncp-sal-qe 0.1", "data": OGGI, "cig_ict_s3s6_dal_2020": len(ict)}

    # --- 1. SAL ---
    sal = collections.defaultdict(list)
    n_righe = 0
    for r in righe("stati-avanzamento"):
        if r["cig"] in ict:
            n_righe += 1
            sal[r["cig"]].append((int(num(r["progressivo_sal"])), r["data_emissione_sal"][:10], num(r["importo_sal"]),
                                  r["denominazione_sal"], num(r["IMPORTO_CERT_PAGAMENTO"]), r["id_aggiudicazione"]))
    somma_righe = sum(x[2] for v in sal.values() for x in v)
    doppie = 0
    dedup = {}
    for c, v in sal.items():
        u = sorted(set((p, d, i) for p, d, i, *_ in v))
        doppie += len(v) - len(u)
        dedup[c] = u
    multi = {c: v for c, v in dedup.items() if len(v) >= 2}
    nondecr = sum(all(a[2] <= b[2] for a, b in zip(v, v[1:])) for v in multi.values())
    # attesa per caso: con importi singoli indipendenti la quota di successioni non decrescenti cala con la lunghezza
    perm = sum(1 / __import__("math").factorial(len(v)) for v in multi.values())
    rap_somma, rap_max, sopra_somma, sopra_max = [], [], 0, 0
    for c, v in multi.items():
        imp, dv = ict[c]
        if imp <= 0 or dv:
            continue
        s, m = sum(x[2] for x in v), max(x[2] for x in v)
        rap_somma.append(s / imp); rap_max.append(m / imp)
        sopra_somma += s > 1.2 * imp; sopra_max += m > 1.2 * imp
    finale_vs_prec = []
    for c, v in sal.items():
        fin = [x for x in v if RX_FINALE.search(x[3] or "")]
        prec = [x for x in dedup[c] if not any(f[0] == x[0] for f in fin)]
        if fin and prec:
            finale_vs_prec.append(max(f[2] for f in fin) / max(sum(x[2] for x in prec), 1))
    somma_dedup = sum(x[2] for v in dedup.values() for x in v)
    somma_max = sum(max(x[2] for x in v) for v in dedup.values())
    cert = sum(x[4] for v in sal.values() for x in v)
    out["sal"] = {
        "righe_ict": n_righe, "cig_ict": len(sal), "cig_con_almeno_2_sal": len(multi),
        "somma_righe_mld": mld(somma_righe), "somma_senza_doppioni_mld": mld(somma_dedup), "somma_massimi_per_cig_mld": mld(somma_max),
        "righe_doppie_identiche": doppie, "certificati_pagamento_mld": mld(cert),
        "successioni_non_decrescenti": {"cig": nondecr, "quota": round(nondecr / len(multi), 3) if multi else None,
                                        "attese_per_caso_se_importi_singoli": round(perm, 1)},
        "somma_su_importo_lotto": {"n": len(rap_somma), **q(rap_somma), "cig_oltre_1_2": sopra_somma},
        "massimo_su_importo_lotto": {"n": len(rap_max), **q(rap_max), "cig_oltre_1_2": sopra_max},
        "sal_finale_su_somma_precedenti": {"n": len(finale_vs_prec), **q(finale_vs_prec)},
    }
    # classificazione per CIG (due o più SAL, importo del lotto noto): «progressivo» se la successione non decresce, la
    # somma supera 1,2 volte l'importo del lotto e il massimo no; «singolo» se la somma resta entro 1,2 volte l'importo;
    # «incerto» il resto. Stima della spesa SAL: massimo per i progressivi, somma per gli altri.
    cl, stima = collections.Counter(), collections.Counter()
    for c, v in dedup.items():
        imp, dv = ict[c]
        s_, m_ = sum(x[2] for x in v), max(x[2] for x in v)
        if len(v) < 2:
            k = "un-solo-sal"
        elif imp <= 0 or dv:
            k = "senza-importo-lotto"
        elif all(a[2] <= b[2] for a, b in zip(v, v[1:])) and s_ > 1.2 * imp and m_ <= 1.2 * imp:
            k = "progressivo"
        elif s_ <= 1.2 * imp:
            k = "singolo"
        else:
            k = "incerto"
        cl[k] += 1
        stima[k] += m_ if k == "progressivo" else s_
    vv = out["sal"]
    vv["classi_cig"] = {k: {"cig": cl[k], "stima_mld": mld(stima[k])} for k in sorted(cl)}
    vv["stima_spesa_sal_mld"] = mld(sum(stima.values()))
    vv["forbice_mld"] = {"minimo_massimi_per_cig": vv["somma_massimi_per_cig_mld"], "massimo_somma_righe": vv["somma_senza_doppioni_mld"]}
    vv["conclusione"] = ("importo_sal è MISTO: per molti CIG è l'importo del singolo SAL, per una parte è il totale progressivo "
                         "(successioni non decrescenti oltre l'atteso per caso, somma oltre 1,2 volte il lotto con il massimo "
                         "entro): la somma delle righe sovrastima, il massimo per CIG sottostima; usare la stima per classe")

    # --- 2. quadro economico ---
    per_ev = collections.defaultdict(lambda: collections.Counter())
    ult = {}
    for r in righe("quadro-economico"):
        c = r["cig"]
        if c not in ict:
            continue
        ev = (r["descrizione_evento"] or "").upper() or "?"
        v = {k: num(r[k]) for k in COMP + ["somme_a_disposizione"]}
        per_ev[ev]["righe"] += 1
        for k, x in v.items():
            per_ev[ev][k] += x
        tot = sum(v[k] for k in COMP)
        key = (ORDINE_EVENTO.get(ev, 0), r["dettaglio_evento"])
        if c not in ult or key > ult[c][0]:
            ult[c] = (key, ev, tot, v)
    out["quadro_economico"] = {
        "per_evento_mld": {ev: {"righe": int(cn["righe"]), **{k: mld(cn[k]) for k in COMP + ["somme_a_disposizione"]}}
                           for ev, cn in sorted(per_ev.items())},
        "cig_ict_con_quadro": len(ult),
        "ultimo_evento_per_cig": dict(collections.Counter(x[1] for x in ult.values()).most_common()),
        "importo_ultimo_quadro_mld": mld(sum(x[2] for x in ult.values())),
        "importo_lotto_stessi_cig_mld": mld(sum(ict[c][0] for c in ult if not ict[c][1])),
        "importo_ultimo_quadro_stessi_cig_senza_da_verificare_mld": mld(sum(x[2] for c, x in ult.items() if not ict[c][1])),
        "percentili_importo_quadro_euro": q([x[2] for x in ult.values()]),
        "rapporto_quadro_su_lotto": q([x[2] / ict[c][0] for c, x in ult.items() if ict[c][0] > 0 and not ict[c][1]]),
        "quadro_zero": sum(1 for x in ult.values() if x[2] <= 0),
        # valori anomali: quadro oltre 10 volte l'importo del lotto (errori di unità o di compilazione)
        "anomali_oltre_10x_lotto": {"cig": sum(1 for c, x in ult.items() if ict[c][0] > 0 and x[2] > 10 * ict[c][0]),
                                    "importo_mld": mld(sum(x[2] for c, x in ult.items() if ict[c][0] > 0 and x[2] > 10 * ict[c][0])),
                                    "primi": [(c, x[1], round(x[2]), round(ict[c][0])) for c, x in sorted(ult.items(), key=lambda t: -t[1][2])[:8]]},
        "somme_a_disposizione_prime": [(c, x[1], round(x[3]["somme_a_disposizione"]), round(ict[c][0])) for c, x in
                                        sorted(ult.items(), key=lambda t: -t[1][3]["somme_a_disposizione"])[:5]],
        "somme_a_disposizione_senza_oltre_10x_lotto_mld": mld(sum(x[3]["somme_a_disposizione"] for c, x in ult.items()
                                                                  if ict[c][0] > 0 and x[3]["somme_a_disposizione"] <= 10 * ict[c][0])),
        "importo_ultimo_quadro_coerente_mld": mld(sum(x[2] for c, x in ult.items() if not ict[c][1] and ict[c][0] > 0 and x[2] <= 10 * ict[c][0])),
        "importo_lotto_coerente_mld": mld(sum(ict[c][0] for c, x in ult.items() if not ict[c][1] and ict[c][0] > 0 and x[2] <= 10 * ict[c][0])),
        "composizione_ultimo_quadro_coerente_mld": {k: mld(sum(x[3][k] for c, x in ult.items() if not ict[c][1] and ict[c][0] > 0 and x[2] <= 10 * ict[c][0]))
                                                    for k in COMP + ["somme_a_disposizione"]},
        "composizione_ultimo_quadro_mld": {k: mld(sum(x[3][k] for x in ult.values())) for k in COMP + ["somme_a_disposizione"]},
    }
    out["ingressi"] = ingressi
    OUT.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(OUT / "sal-qe.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in out.items() if k != "ingressi"}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
