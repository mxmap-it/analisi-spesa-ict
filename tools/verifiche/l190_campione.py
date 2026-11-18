#!/usr/bin/env python3
"""Verifica «dataset art. 1 c. 32 L. 190/2012» (#74): registro ANAC e campione degli XML degli enti.

Fase 1 (offline, dall'archivio): ricostruisce il registro ANAC `rest/legge190/ricerca` dalle 354 pagine JSON
già archiviate il 3/11 (lavoro/trasparenza/stato.sqlite -> blobs sha256): righe per anno, enti, esiti ANAC.
Fase 2 (dal vivo, ripartibile): campione casuale (seme fisso) di N enti del registro 2023 (= dati 2022);
per ciascuno archivia l'indice (tools/archivia.py, accetta_html) e fino a MAXF file dataset linkati,
con una pausa >= 5 s fra due richieste qualsiasi (quindi anche per host). Progresso in
lavoro/l190-campione/stato.jsonl (un ente per riga): si riparte saltando gli enti fatti.
Fase 3 (offline): misura validità XML, anni, lotti, CIG, importi di aggiudicazione e somme liquidate,
copertura dei CIG ICT dell'imbuto (lavoro/imbuto/ict.csv) -> esiti/<data>/l190/campione.json + campione-file.csv.

Uso (SUL SERVER, nice): .venv/bin/python tools/verifiche/l190_campione.py [--n 200] [--solo-misura]"""
import argparse, csv, json, os, random, re, sqlite3, sys, time, collections
import xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlsplit
from pathlib import Path
import requests

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / "tools"))
import archivia as A  # noqa: E402

_vista = A.aggiorna_vista


def _vista_sicura(url, sha):
    """Alcuni portali usano lo stesso percorso come file e come cartella (es. .../32/datasets e .../32/datasets/x.xml):
    la vista mirror/ non può contenerli entrambi. Il blob e la riga di manifest restano; manca solo l'hardlink."""
    try:
        _vista(url, sha)
    except OSError as e:
        print("vista non creata:", url, e, flush=True)


A.aggiorna_vista = _vista_sicura

OUT = BASE / "lavoro" / "l190-campione"
PAUSA = 5.0
MAXF = 3          # file dataset scaricati per ente (il primo, il secondo, l'ultimo)
SEME = 190


def blob(sha):
    return (BASE / "archivio" / "blobs" / "sha256" / sha[:2] / sha[2:4] / sha).read_bytes()


def registro():
    c = sqlite3.connect(BASE / "lavoro" / "trasparenza" / "stato.sqlite")
    righe, visti = [], set()  # le pagine sono archiviate da più giri: si deduplica per contenuto della riga
    for url, sha in c.execute("select url, sha256 from fonti_scaricate where url like '%legge190/ricerca%' order by ts"):
        anno = url.split("#anno=")[1]
        for x in json.loads(blob(sha))["result"]:
            k = (anno, json.dumps(x, sort_keys=True))
            if k in visti:
                continue
            visti.add(k)
            x["_anno"] = anno
            righe.append(x)
    return righe


def tag(e):
    return e.tag.rsplit("}", 1)[-1]


def num(s):
    try:
        return float((s or "").strip().replace(",", "."))
    except ValueError:
        return None


def leggi_xml(b):
    """-> dict con tipo (indice/dataset/non-xml), link, anno, lotti."""
    try:
        r = ET.fromstring(b)
    except ET.ParseError as e:
        return {"tipo": "non-xml", "errore": str(e)[:120], "html": b[:600].lower().find(b"<html") >= 0}
    link = [x.text.strip() for x in r.iter() if tag(x) == "linkDataset" and x.text]
    anno = next((x.text for x in r.iter() if tag(x) == "annoRiferimento"), None)
    lotti = []
    for l in r.iter():
        if tag(l) != "lotto":
            continue
        d = {tag(x): x for x in l}
        lotti.append({"cig": (d["cig"].text or "").strip().upper() if "cig" in d else "",
                      "agg": num(d["importoAggiudicazione"].text) if "importoAggiudicazione" in d else None,
                      "liq": num(d["importoSommeLiquidate"].text) if "importoSommeLiquidate" in d else None,
                      "tempi": "tempiCompletamento" in d,
                      "aggiudicatari": "aggiudicatari" in d})
    return {"tipo": "indice" if link else ("dataset" if lotti or tag(r) == "pubblicazione" else "xml-altro"),
            "radice": tag(r), "link": link, "anno": anno, "lotti": lotti}


def scarica(sess, url):
    rec = A.archivia(sess, url, accetta_html=True)
    A.scrivi_manifest({**rec, "nota": "l190_campione.py #74"})
    time.sleep(PAUSA)
    return rec


def campione(n):
    OUT.mkdir(parents=True, exist_ok=True)
    reg = [x for x in registro() if x["_anno"] == "2023" and (x.get("url") or "").startswith("http")]
    per_cf = {}
    for x in reg:
        per_cf.setdefault((x.get("codiceFiscale") or "").strip().upper(), x)
    cfs = sorted(per_cf)
    random.Random(SEME).shuffle(cfs)
    st = OUT / "stato.jsonl"
    fatti = {json.loads(l)["cf"] for l in st.open(encoding="utf-8")} if st.exists() else set()
    sess = requests.Session()
    for cf in cfs[:n]:
        if cf in fatti:
            continue
        x = per_cf[cf]
        url = x["url"].strip()
        ent = {"cf": cf, "denominazione": x.get("ragioneSociale"), "url": url,
               "esito_anac": x.get("esitoUltimoTentativoAccessoUrl"), "file": []}
        rec = scarica(sess, url)
        ent["file"].append({"url": url, "ruolo": "indice", **{k: rec.get(k) for k in ("esito", "errore", "http", "sha256", "dimensione", "tipo")}})
        if rec.get("sha256"):
            info = leggi_xml(blob(rec["sha256"]))
            link = [urljoin(url, u) for u in info.get("link", [])]
            ent["n_link"] = len(link)
            scelti = list(dict.fromkeys(link[:2] + link[-1:]))[:MAXF]
            for u in scelti:
                r2 = scarica(sess, u)
                ent["file"].append({"url": u, "ruolo": "dataset", **{k: r2.get(k) for k in ("esito", "errore", "http", "sha256", "dimensione", "tipo")}})
        with st.open("a", encoding="utf-8") as f:
            f.write(json.dumps(ent, ensure_ascii=False) + "\n")
        print(cf, rec.get("esito"), ent.get("n_link"), flush=True)


def misura(n):
    reg = registro()
    per_anno = collections.defaultdict(lambda: {"righe": 0, "enti": set(), "successo": 0})
    for x in reg:
        p = per_anno[x["_anno"]]
        p["righe"] += 1
        p["enti"].add((x.get("codiceFiscale") or "").strip().upper())
        p["successo"] += x.get("esitoUltimoTentativoAccessoUrl") == "successo"
    out = {"registro": {a: {"righe": v["righe"], "enti": len(v["enti"]), "esito_anac_successo": v["successo"]}
                        for a, v in sorted(per_anno.items())},
           "registro_enti_distinti": len({(x.get("codiceFiscale") or "").strip().upper() for x in reg}),
           "registro_campi": sorted(reg[0].keys()) if reg else []}
    ict = set()
    with open(BASE / "lavoro" / "imbuto" / "ict.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["strato"].startswith(("S3", "S4", "S5", "S6")):  # 18/11: prima escludeva solo S1-S2, contando i padri AQ (S0)
                ict.add(r["cig"])
    ents = [json.loads(l) for l in (OUT / "stato.jsonl").open(encoding="utf-8")][:n]
    c = collections.Counter()
    host = set()
    righe_file = []
    tot = collections.Counter()
    anni = collections.Counter()
    dim = []
    for e in ents:
        c["enti"] += 1
        host.add(urlsplit(e["url"]).netloc.lower())
        idx = e["file"][0]
        c["indice_" + str(idx.get("esito"))] += 1
        if not idx.get("sha256"):
            continue
        ii = leggi_xml(blob(idx["sha256"]))
        c["indice_tipo_" + ii["tipo"]] += 1
        dati = [ii] if ii["tipo"] == "dataset" else []
        if ii["tipo"] == "dataset":
            dim.append(idx.get("dimensione") or 0)
        for fd in e["file"][1:]:
            c["dataset_scaricati"] += 1
            if not fd.get("sha256"):
                c["dataset_errore"] += 1
                continue
            d = leggi_xml(blob(fd["sha256"]))
            c["dataset_tipo_" + d["tipo"]] += 1
            dim.append(fd.get("dimensione") or 0)
            dati.append(d)
            righe_file.append([e["cf"], fd["url"], fd["sha256"], fd.get("dimensione"), d["tipo"], d.get("anno"), len(d.get("lotti", []))])
        if any(d["lotti"] for d in dati):
            c["enti_con_lotti"] += 1
        for d in dati:
            if d.get("anno"):
                anni[d["anno"]] += 1
            for l in d.get("lotti", []):
                tot["lotti"] += 1
                tot["cig_valorizzato"] += bool(re.fullmatch(r"[0-9A-Z]{10}", l["cig"]))
                tot["cig_ict"] += l["cig"] in ict
                if l["agg"] is not None:
                    tot["con_agg"] += 1
                    tot["somma_agg"] += l["agg"]
                if l["liq"] is not None:
                    tot["con_liq"] += 1
                    tot["somma_liq"] += l["liq"]
                    tot["liq_pos"] += l["liq"] > 0
                if l["agg"] and l["liq"] is not None:
                    tot["coppie"] += 1
                    tot["coppie_agg"] += l["agg"]
                    tot["coppie_liq"] += l["liq"]
                    tot["liq_gt_agg"] += l["liq"] > l["agg"] * 1.0001
                if l["cig"] in ict:
                    tot["ict_agg"] += l["agg"] or 0
                    tot["ict_liq"] += l["liq"] or 0
    out["campione"] = {"enti": len(ents), "host_distinti": len(host), "conteggi": dict(c),
                       "lotti": {k: round(v, 2) for k, v in tot.items()}, "anni_riferimento": dict(anni),
                       "dimensione_file_dataset_byte": {"n": len(dim), "somma": sum(dim),
                                                         "mediana": sorted(dim)[len(dim) // 2] if dim else 0, "max": max(dim or [0])},
                       "n_link_per_indice": collections.Counter(min(e.get("n_link", 0), 50) // 5 * 5 for e in ents)}
    oggi = time.strftime("%Y-%m-%d")
    d = BASE / "esiti" / oggi / "l190"
    d.mkdir(parents=True, exist_ok=True)
    (d / "campione.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    with open(d / "campione-file.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["cf", "url", "sha256", "byte", "tipo", "anno", "lotti"])
        w.writerows(righe_file)
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--solo-misura", action="store_true")
    a = ap.parse_args()
    if not a.solo_misura:
        campione(a.n)
    misura(a.n)
