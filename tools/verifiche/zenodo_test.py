"""Test del dataset Zenodo 10007545 (Siciliani et al., CLiC-it 2023, CC-BY-4.0) per l'imbuto (#59).
Criterio (STATE.md, todo #59): elenchi di esclusione certa ricavati da Zenodo: quanti contratti escludono IN PIÙ
rispetto a S1 e con quale precisione.

Metodo:
 1. lessico «puro non ICT»: parole (>=4 lettere) con almeno MIN_OCC occorrenze nel dataset e quota di righe
    con CPV ICT (stesso CPV_ICT di classifica.py) <= MAX_QUOTA_ICT;
 2. regola candidata: un CIG del residuo S6 (dal 2024) che contiene almeno K parole del lessico e nessuna parola
    del lessico ICT di imbuto.py «forte» (cloud, software, server, ...) si escluderebbe;
 3. precisione: sul campione v3 (611 CIG con riferimento, dati/classificazioni/campione-v3.jsonl) si contano i CIG
    che la regola escluderebbe e, fra questi, quanti il riferimento dà come cloud (errori);
 4. sovrapposizione: quanti CIG del dataset sono già nell'universo ANAC (sono descrizioni ANAC: stessa fonte).

Uso:  python tools/verifiche/zenodo_test.py             # stampa l'esito versionato
      python tools/verifiche/zenodo_test.py --rigenera  # SUL SERVER: lavoro/zenodo-10007545/cpv_5M.csv.gz
            (md5 dd68c3480819ff3065bb8dc49b053905 da https://zenodo.org/records/10007545) + lavoro/imbuto/ict.csv
"""
import csv, gzip, json, os, re, sys, collections, hashlib

RADICE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
ESITO = os.path.join(RADICE, "esiti/2026-11-06/zenodo/esito.json")
ZEN = os.path.join(RADICE, "lavoro/zenodo-10007545/cpv_5M.csv.gz")
ICT = os.path.join(RADICE, "lavoro/imbuto/ict.csv")
CAMP = os.path.join(RADICE, "dati/classificazioni/campione-v3.jsonl")
CPV_ICT = re.compile(r"^(48|72|302|3223|3224|3225|3226|50312|50320|51611|64216|64222|79342)")
FORTI = re.compile(r"cloud|software|server|hosting|saas|iaas|paas|datacent|data center|licenz|informatic|microsoft|oracle|aws|azure|google|backup|storage|digital|telematic|piattaform|applicativ|sistema informativ|rete|web|portale|app\b", re.I)
PAROLA = re.compile(r"[a-zàèéìòù]{4,}")
MIN_OCC, MAX_QUOTA_ICT, K = 500, 0.001, 2
csv.field_size_limit(10**8)


def parole(t):
    return set(PAROLA.findall((t or "").lower()))


def rigenera():
    occ, ict = collections.Counter(), collections.Counter()
    n = n_ict = 0; cig_zen = set(); anni = collections.Counter()
    with gzip.open(ZEN, "rt", encoding="utf-8", errors="replace") as f:
        for r in csv.reader(f):
            if len(r) < 5: continue
            n += 1; e = bool(CPV_ICT.match(r[4].replace("-", "")[:8])); n_ict += e
            cig_zen.add(r[0])
            for w in parole(r[1] + " " + r[2]):
                occ[w] += 1
                if e: ict[w] += 1
    lessico = {w for w, c in occ.items() if c >= MIN_OCC and ict[w] / c <= MAX_QUOTA_ICT}
    regola = lambda t: (len(parole(t) & lessico) >= K) and not FORTI.search(t or "")
    # residuo dal 2024 e strati ICT
    agg = collections.defaultdict(lambda: [0, 0.0]); sovr = collections.Counter()
    with open(ICT, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["cig"] in cig_zen: sovr[r["anno"]] += 1
            if int(r["anno"]) < 2024: continue
            if regola(r["testo"]):
                k = (r["strato"], r["gruppo"]); agg[k][0] += 1; agg[k][1] += float(r["importo"] or 0)
    # precisione sul campione v3
    escl = err = 0; esempi = []
    for line in open(CAMP, encoding="utf-8"):
        d = json.loads(line); t = d["ingresso"].get("oggetto", "")
        if regola(t):
            escl += 1
            if d["esito"].get("e_cloud") == "s":
                err += 1; esempi.append({"cig": d["cig"], "oggetto": t[:160]})
    out = {"dataset": "zenodo 10007545 cpv_5M.csv.gz", "md5": "dd68c3480819ff3065bb8dc49b053905",
           "sha256": hashlib.sha256(open(ZEN, "rb").read()).hexdigest(), "righe": n, "righe_cpv_ict": n_ict,
           "cig_distinti": len(cig_zen), "cig_zenodo_presenti_in_ict_csv_per_anno": dict(sorted(sovr.items())),
           "parametri": {"min_occ": MIN_OCC, "max_quota_ict": MAX_QUOTA_ICT, "k": K}, "lessico_parole": len(lessico),
           "lessico_esempi": sorted(lessico)[:60],
           "esclusi_in_piu_dal_2024": [{"strato": k[0], "gruppo": k[1], "cig": v[0], "euro": round(v[1])} for k, v in sorted(agg.items())],
           "campione_v3": {"n": 611, "esclusi_dalla_regola": escl, "di_cui_cloud_per_riferimento": err, "errori_esempi": esempi[:10]}}
    os.makedirs(os.path.dirname(ESITO), exist_ok=True)
    json.dump(out, open(ESITO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    if "--rigenera" in sys.argv: rigenera()
    print(json.dumps({k: v for k, v in json.load(open(ESITO, encoding="utf-8")).items() if k != "lessico_esempi"}, ensure_ascii=False, indent=1))
