"""#12 Verifica dell'ipotesi in-house sui 4 enti SIOPE «molto pagato ICT, pochi CIG» (siope_ict_enti.py, esiti 2026-11-10).

Enti (CF SIOPE) e in-house candidate (regex sul nome dell'aggiudicatario ANAC):
  Regione Lombardia / gestione sanitaria (80050050154)  -> ARIA S.p.A. (ex Lombardia Informatica)
  Comune di Venezia (00339370272)                        -> Venis S.p.A.
  ARPAL Umbria (03630270548)                             -> Umbria Digitale S.c.a r.l. (ora PuntoZero)
  ARPEA Piemonte (97694170016)                           -> CSI-Piemonte
Misure, dai CIG ANAC 2020-2025 + delta (ultima versione) e dagli aggiudicatari ANAC:
  a) tutti i CIG con SA = ente (ICT o no, per anno): quanti e quanto verso l'in-house come aggiudicataria;
  b) tutti i CIG con aggiudicataria = in-house: per stazione appaltante (quanto viene dall'ente, quanto da altri);
  c) CIG con SA = in-house (centrale di committenza o acquisti propri) per anno.
Uso (server): nice -n 19 ionice -c3 .venv/bin/python tools/verifiche/siope_inhouse_4enti.py -> esiti/<oggi>/siope/inhouse-4enti.json"""
import collections, csv, datetime, glob, io, json, os, re, sys, zipfile
from pathlib import Path

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/verifiche")); sys.path.insert(0, str(R / "tools/analisi"))
import bdap_cig_ministeri_cf as M  # noqa: E402

D = M.D
ENTI = {"80050050154": ("REGIONE LOMBARDIA", r"\bARIA\b|AZIENDA REGIONALE PER L.INNOVAZIONE E GLI ACQUISTI|LOMBARDIA INFORMATICA"),
        "00339370272": ("COMUNE DI VENEZIA", r"\bVENIS\b|VENEZIA INFORMATICA"),
        "03630270548": ("ARPAL UMBRIA", r"UMBRIA DIGITALE|PUNTO ?ZERO"),
        "97694170016": ("ARPEA PIEMONTE", r"\bCSI.?PIEMONTE\b|CONSORZIO PER IL SISTEMA INFORMATIVO")}


def main():
    csv.field_size_limit(10 ** 8)
    rx = {cf: re.compile(p, re.I) for cf, (_, p) in ENTI.items()}
    agg = collections.defaultdict(set); cf_inh = collections.defaultdict(collections.Counter)
    z = sorted(glob.glob(str(D / "aggiudicatari/filesystem/aggiudicatari_csv.zip")))[0]
    ing = {"aggiudicatari": {"file": os.path.relpath(z, M.ARC), "sha256": M.sha(z)}}
    zf = zipfile.ZipFile(z); m = next(i for i in zf.namelist() if i.endswith(".csv"))
    for r in csv.DictReader(io.TextIOWrapper(zf.open(m), encoding="utf-8-sig", errors="replace"), delimiter=";"):
        n = r.get("denominazione") or ""
        for cf, x in rx.items():
            if x.search(n): agg[r["cig"]].add(cf); cf_inh[cf][(n.strip()[:80], (r["codice_fiscale"] or "").strip())] += 1
    print("aggiudicatari", len(agg), flush=True)
    ict = set()
    for r in csv.DictReader(open(R / "lavoro/imbuto/ict.csv", encoding="utf-8")): ict.add(r["cig"])
    # CF delle in-house come SA: i CF più frequenti fra gli aggiudicatari trovati
    inh_cf = {cf: {k[1] for k, v in c.most_common(3) if k[1]} for cf, c in cf_inh.items()}
    cig = {}; files = []
    zz = [z for a in range(2020, 2026) for z in sorted(glob.glob(str(D / f"cig-{a}/filesystem/cig_csv_*.zip")))]
    zz += sorted(glob.glob(str(D / "cig/filesystem/*-cig_csv.zip")))
    tutti_inh = set().union(*inh_cf.values()) if inh_cf else set()
    for z in zz:
        files.append(os.path.relpath(z, M.ARC)); zf = zipfile.ZipFile(z)
        m = next(i for i in zf.namelist() if i.endswith(".csv"))
        for r in csv.DictReader(io.TextIOWrapper(zf.open(m), encoding="utf-8-sig", errors="replace"), delimiter=";"):
            cf = (r["cf_amministrazione_appaltante"] or "").strip()
            if r["cig"] in agg or cf in ENTI or cf in tutti_inh:
                cig[r["cig"]] = {"cf": cf, "sa": r["denominazione_amministrazione_appaltante"], "anno": r["data_pubblicazione"][:4],
                                 "importo": M.B.num(r["importo_lotto"]), "oggetto": r["oggetto_lotto"][:150], "cpv": r["cod_cpv"],
                                 "scelta": r["tipo_scelta_contraente"], "durata": M.B.num(r.get("DURATA_PREVISTA"))}
    ing["cig_anac"] = {"file": files}
    out = {"versione": "siope-inhouse-4enti 0.1 (2026-11-10)", "ingressi": ing, "enti": {}}
    for cf, (nome, _) in ENTI.items():
        a = collections.defaultdict(collections.Counter); b = collections.defaultdict(collections.Counter); c = collections.defaultdict(collections.Counter)
        el = []
        for k, v in cig.items():
            y = v["anno"]
            if v["cf"] == cf:
                a[y]["n"] += 1; a[y]["importo"] += v["importo"]
                if k in ict: a[y]["n_ict"] += 1; a[y]["imp_ict"] += v["importo"]
                if cf in agg.get(k, ()): a[y]["n_inhouse"] += 1; a[y]["imp_inhouse"] += v["importo"]; el.append((k, v))
            if cf in agg.get(k, ()):
                chi = "ente" if v["cf"] == cf else "altri"
                b[y]["n_" + chi] += 1; b[y]["imp_" + chi] += v["importo"]
            if v["cf"] in inh_cf.get(cf, ()):
                c[y]["n"] += 1; c[y]["importo"] += v["importo"]
                if k in ict: c[y]["n_ict"] += 1; c[y]["imp_ict"] += v["importo"]
        el.sort(key=lambda t: -t[1]["importo"])
        r2 = lambda d: {y: {kk: round(vv) for kk, vv in x.items()} for y, x in sorted(d.items()) if "2020" <= y <= "2026"}
        out["enti"][cf] = {"nome": nome, "inhouse_denominazioni_cf": [[k[0], k[1], n] for k, n in cf_inh[cf].most_common(6)],
                           "cf_inhouse_usati_come_sa": sorted(inh_cf.get(cf, ())),
                           "a_cig_ente": r2(a), "b_cig_aggiudicati_inhouse": r2(b), "c_cig_sa_inhouse": r2(c),
                           "elenco_ente_a_inhouse": [{"cig": k} | {kk: v[kk] for kk in ("anno", "importo", "oggetto", "cpv", "scelta", "durata")} for k, v in el[:40]]}
    o = R / f"esiti/{datetime.date.today().isoformat()}/siope"; os.makedirs(o, exist_ok=True)
    json.dump(out, open(o / "inhouse-4enti.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=str)
    for cf, e in out["enti"].items():
        print(e["nome"], e["inhouse_denominazioni_cf"][:3], e["cf_inhouse_usati_come_sa"])
        for k in ("a_cig_ente", "b_cig_aggiudicati_inhouse", "c_cig_sa_inhouse"): print(" ", k, json.dumps(e[k], ensure_ascii=False))
        for x in e["elenco_ente_a_inhouse"][:8]: print("   ", x)


if __name__ == "__main__":
    main()
