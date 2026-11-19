"""Prova leggera dei modelli fondazionali tabulari (TabICL) come via di classificazione (#56).

Protocollo: report/metodo/sperimentazione-tfm.md. Comando (dalla radice del repo, sul server, come mxmap.it):

  python3 -m venv lavoro/tfm/.venv && lavoro/tfm/.venv/bin/pip install torch==2.5.1 \
      --index-url https://download.pytorch.org/whl/cpu && lavoro/tfm/.venv/bin/pip install tabicl==2.2.0 \
      scikit-learn==1.9.1 skrub==0.11.0 pandas==3.1.1 scipy==1.18.1          # una volta
  HF_HOME=$PWD/lavoro/tfm/hf OMP_NUM_THREADS=4 flock lavoro/pesante.lock nice -n 15 \
      lavoro/tfm/.venv/bin/python tools/sperimentazioni/tfm/prova_leggera.py

Uscita: report/metodo/sperimentazioni/tfm-2026-11-19.json (versioni, semi, sha256 degli ingressi e dei pesi).

Etichette (tutte prodotte da Claude: via 6 con ricerca delle fonti, e campioni a cieco 4-6 per la giurisdizione):
  - dati/classificazioni/campione-v3.jsonl (611, via 6 giri 1-2), imbuto-g1g3.jsonl (1.242, via 6 p3, residuo S6),
    imbuto-revisione.jsonl (273, sottoinsieme di g1g3 rivisto il 18/11).
  - Dedup per CIG: prevale l'esito con fonte_primaria=true; a parità il più recente (revisione > g1g3 > v3).
    e_cloud '?' escluso. Sui CIG in comune le etichette coincidono quasi sempre (vedi «dedup» nell'uscita).
  - Giurisdizione: IT / UE / EXTRA-UE dagli stessi esiti più report/metodo/lente-cieco-{4,5,6} (etichette a cieco
    sul testo dell'oggetto); se un CIG è in entrambi prevale la via 6 (ha cercato le fonti).
Caratteristiche: oggetto (testo), CPV (divisione, gruppo, classe, codice), log importo, tipo di stazione appaltante
(regola sul nome), stazione appaltante, primo aggiudicatario. Colonne delle regole (variante «+regole»): via, servizio,
provider, giurisdizione delle regole e sottoclasse dell'imbuto, tutte dal passaggio 1 (regola) dei record.
Confronti: regole (passaggio 1), via 6 giro 1 sul solo testo (campione v3), revisione cieca Opus (273 CIG),
skrub TableVectorizer + HistGradientBoosting, TabICL (stesso vettorizzatore) senza e con colonne delle regole.
"""
import collections, hashlib, json, math, os, platform, re, sys, time, warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
RADICE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
USCITA = os.path.join(RADICE, os.environ.get("TFM_USCITA", "report/metodo/sperimentazioni/tfm-2026-11-19.json"))
SEME = 20261119
N_FOLD = 5
N_RIP = int(os.environ.get("TFM_RIPETIZIONI", "3"))
SOGLIA_PREC = 0.95
TABICL_STIMATORI = 8
THREADS = 4

FILE = {
    "v3": "dati/classificazioni/campione-v3.jsonl",
    "g1g3": "dati/classificazioni/imbuto-g1g3.jsonl",
    "revisione": "dati/classificazioni/imbuto-revisione.jsonl",
}
CIECHI = ["report/metodo/lente-cieco-4", "report/metodo/lente-cieco-5", "report/metodo/lente-cieco-6"]
PRIORITA = {"revisione": 3, "g1g3": 2, "v3": 1, "cieco": 0}
GIUR = ["IT", "UE", "EXTRA-UE"]


def sha256(p):
    h = hashlib.sha256()
    with open(os.path.join(RADICE, p), "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def tipo_sa(nome):
    n = (nome or "").upper()
    for t, rx in [
        ("sanita", r"AZIENDA (SANITARIA|OSPEDALIER|USL|ULSS|SOCIO)|\bASL\b|\bASST\b|\bULSS\b|\bAUSL\b|OSPEDAL|IRCCS|ESTAR|POLICLINICO|\bATS\b|SANITARI"),
        ("universita-ricerca", r"UNIVERSIT|POLITECNICO|\bCNR\b|CONSIGLIO NAZIONALE DELLE RICERCHE|ISTITUTO NAZIONALE DI|\bINFN\b|SCUOLA (NORMALE|SUPERIORE)"),
        ("scuola", r"ISTITUTO COMPRENSIVO|LICEO|ISTITUTO (TECNICO|PROFESSIONALE|D.ISTRUZIONE)|DIREZIONE DIDATTICA|\bI\.?C\.?\b|SCUOLA"),
        ("comune", r"^COMUNE|COMUNE DI|UNIONE (DEI|DEL|DI) COMUNI|UNIONE COMUNI|COMUNITA.? MONTANA"),
        ("provincia-citta-metro", r"PROVINCIA|CITTA.? METROPOLITANA"),
        ("regione", r"^REGIONE|GIUNTA REGIONALE|CONSIGLIO REGIONALE"),
        ("centrale", r"MINISTERO|PRESIDENZA DEL CONSIGLIO|AGENZIA|CONSIP|INPS|INAIL|\bISTAT\b|CORTE DEI CONTI|AUTORITA|GUARDIA|CARABINIERI|POLIZIA|ESERCITO|MARINA|AERONAUTICA|DIFESA"),
        ("societa", r"S\.?P\.?A\.?|S\.?R\.?L\.?|SOCIETA|S\.C\.?A\.?R\.?L|CONSORZIO"),
    ]:
        if re.search(rx, n):
            return t
    return "altro"


def riga_da_record(r, sorgente):
    i, e = r["ingresso"], r["esito"]
    p1 = r["passaggi"][0] if r.get("passaggi") else {}
    res, par = p1.get("risultato") or {}, p1.get("parametri") or {}
    giro1 = next((p["risultato"] for p in r.get("passaggi", []) if p.get("tipo") == "modello"), None)
    rev = next((p["risultato"] for p in r.get("passaggi", []) if p.get("tipo") == "revisione"), None)
    agg = i.get("aggiudicatari") or []
    return {
        "cig": r["cig"], "sorgente": sorgente,
        "oggetto": i.get("oggetto") or "", "cpv": str(i.get("cpv") or ""), "importo": i.get("importo"),
        "stazione_appaltante": i.get("stazione_appaltante") or "", "aggiudicatario": agg[0] if agg else "",
        "regola_via": str(res.get("via") or par.get("via") or ""), "regola_servizio": str(res.get("servizio") or ""),
        "regola_provider": str(res.get("provider") or ""), "regola_giurisdizione": str(res.get("giurisdizione") or ""),
        "regola_sottoclasse": str(par.get("sottoclasse") or ""),
        "e_cloud": e.get("e_cloud"), "servizio": e.get("servizio"), "giurisdizione": e.get("giurisdizione"),
        "fonte_primaria": bool(e.get("fonte_primaria")),
        "giro1_e_cloud": (giro1 or {}).get("e_cloud"), "giro1_giurisdizione": (giro1 or {}).get("giurisdizione"),
        "revisione_e_cloud": (rev or {}).get("e_cloud"),
    }


def carica():
    righe = []
    for k, f in FILE.items():
        with open(os.path.join(RADICE, f), encoding="utf-8") as fh:
            righe += [riga_da_record(json.loads(l), k) for l in fh if l.strip()]
    cieco = []
    for d in CIECHI:
        et = pd.read_csv(os.path.join(RADICE, d, "etichette.csv"), dtype=str).fillna("")
        cc = pd.read_csv(os.path.join(RADICE, d, "campione-cieco.csv"), dtype=str).fillna("")
        m = et.merge(cc, on="cig", how="left")
        for _, x in m.iterrows():
            cieco.append({"cig": x["cig"], "sorgente": "cieco", "oggetto": x.get("testo", ""), "cpv": x.get("cod_cpv", ""),
                          "importo": float(x["importo"]) if x.get("importo") else None,
                          "stazione_appaltante": x.get("stazione_appaltante", ""),
                          "aggiudicatario": (x.get("aggiudicatari", "") or "").split("|")[0].strip(),
                          "regola_via": "", "regola_servizio": "", "regola_provider": "", "regola_giurisdizione": "",
                          "regola_sottoclasse": "", "e_cloud": None, "servizio": None,
                          "giurisdizione": x.get("giurisdizione", ""), "fonte_primaria": False,
                          "giro1_e_cloud": None, "giro1_giurisdizione": None, "revisione_e_cloud": None})
    return pd.DataFrame(righe), pd.DataFrame(cieco)


def dedup(df, col):
    """Una riga per CIG: prevale fonte_primaria, poi la sorgente più recente. Conserva i confronti più informativi."""
    df = df.assign(_p=df["fonte_primaria"].astype(int) * 10 + df["sorgente"].map(PRIORITA))
    stat = {"righe": int(len(df)), "cig_distinti": int(df["cig"].nunique())}
    multipli = df[df.duplicated("cig", keep=False)]
    stat["cig_in_piu_sorgenti"] = int(multipli["cig"].nunique())
    stat["etichetta_discorde_fra_sorgenti"] = int((multipli.groupby("cig")[col].nunique() > 1).sum())
    # i confronti (giro 1, revisione) si recuperano da qualsiasi sorgente dello stesso CIG
    extra = df.groupby("cig").agg(giro1_e_cloud=("giro1_e_cloud", "first"), giro1_giurisdizione=("giro1_giurisdizione", "first"),
                                  revisione_e_cloud=("revisione_e_cloud", "first"))
    out = df.sort_values("_p", ascending=False).drop_duplicates("cig").drop(columns=["_p", "giro1_e_cloud", "giro1_giurisdizione", "revisione_e_cloud"])
    out = out.join(extra, on="cig")
    stat["sorgente_prevalsa"] = {k: int(v) for k, v in out["sorgente"].value_counts().items()}
    return out.reset_index(drop=True), stat


def caratteristiche(df, con_regole):
    cpv = df["cpv"].str.replace(r"[^0-9]", "", regex=True).str.ljust(8, "0")
    X = pd.DataFrame({
        "oggetto": df["oggetto"].str.slice(0, 600),
        "cpv2": "c" + cpv.str[:2], "cpv3": "c" + cpv.str[:3], "cpv5": "c" + cpv.str[:5], "cpv8": "c" + cpv.str[:8],
        "log_importo": np.log1p(pd.to_numeric(df["importo"], errors="coerce").fillna(0).clip(lower=0)),
        "tipo_sa": df["stazione_appaltante"].map(tipo_sa),
        "stazione_appaltante": df["stazione_appaltante"], "aggiudicatario": df["aggiudicatario"],
    })
    if con_regole:
        for c in ["regola_via", "regola_servizio", "regola_provider", "regola_giurisdizione", "regola_sottoclasse"]:
            X[c] = df[c].replace("", "nessuna")
    return X


def vettorizzatore():
    from skrub import StringEncoder, TableVectorizer
    return TableVectorizer(high_cardinality=StringEncoder(n_components=30, random_state=SEME), cardinality_threshold=40)


def modello(nome):
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.pipeline import make_pipeline
    if nome.startswith("hgb"):
        return make_pipeline(vettorizzatore(), HistGradientBoostingClassifier(random_state=SEME))
    from tabicl import TabICLClassifier
    return make_pipeline(vettorizzatore(), TabICLClassifier(n_estimators=TABICL_STIMATORI, device="cpu", random_state=SEME, n_jobs=THREADS))


def ece(prob, y, bins=10):
    conf, pred = prob.max(1), prob.argmax(1)
    e = 0.0
    for lo in np.linspace(0, 1, bins + 1)[:-1]:
        m = (conf > lo) & (conf <= lo + 1 / bins)
        if m.any():
            e += m.mean() * abs((pred[m] == y[m]).mean() - conf[m].mean())
    return float(e)


def soglia_auto(prob, y, target=SOGLIA_PREC):
    """Soglia minima sulla confidenza tale che i CIG sopra soglia abbiano accuratezza >= target (decisione automatica)."""
    conf = prob.max(1); ok = prob.argmax(1) == y
    ordine = np.argsort(-conf); acc = np.cumsum(ok[ordine]) / np.arange(1, len(y) + 1)
    validi = np.where(acc >= target)[0]
    validi = validi[validi >= 19]  # almeno 20 CIG
    if not len(validi):
        return None
    return float(conf[ordine][validi.max()])


def copertura(prob, y, s, maschera=None):
    if s is None:
        return {"copertura": 0.0, "precisione": None, "n": 0}
    m = prob.max(1) >= s
    if maschera is not None:
        m, prob, y = m[maschera], prob[maschera], y[maschera]
    return {"copertura": float(m.mean()), "precisione": float((prob.argmax(1)[m] == y[m]).mean()) if m.any() else None, "n": int(m.sum())}


def mcnemar(a_ok, b_ok):
    from scipy.stats import binomtest
    b = int((a_ok & ~b_ok).sum()); c = int((~a_ok & b_ok).sum())
    p = float(binomtest(b, b + c, 0.5).pvalue) if b + c else 1.0
    return {"solo_modello_giusto": b, "solo_altra_via_giusta": c, "p": p, "n": int(len(a_ok))}


def metriche_pred(y, pred, classi):
    from sklearn.metrics import f1_score
    return {"n": int(len(y)), "accuratezza": float((y == pred).mean()),
            "macro_f1": float(f1_score(y, pred, average="macro", labels=list(range(len(classi))))),
            "f1_per_classe": dict(zip(classi, map(float, f1_score(y, pred, average=None, labels=list(range(len(classi)))))))}


def esperimento(df, col, classi, confronti, gruppo_s6):
    from sklearn.model_selection import RepeatedStratifiedKFold
    y = df[col].map({c: i for i, c in enumerate(classi)}).to_numpy()
    cv = list(RepeatedStratifiedKFold(n_splits=N_FOLD, n_repeats=N_RIP, random_state=SEME).split(df, y))
    out = {"n": int(len(y)), "classi": {c: int((y == i).sum()) for i, c in enumerate(classi)}, "confronti": {}, "modelli": {}}
    for nome, pred in confronti.items():
        m = pred.notna().to_numpy()
        p = pred[m].map({c: i for i, c in enumerate(classi)}).fillna(-1).astype(int).to_numpy()
        out["confronti"][nome] = metriche_pred(y[m], p, classi)
    for nome in ["hgb", "hgb+regole", "tabicl", "tabicl+regole"]:
        X = caratteristiche(df, nome.endswith("+regole"))
        probs, t0, tempi = [], time.time(), []
        for r in range(N_RIP):
            P = np.zeros((len(y), len(classi)))
            for k in range(N_FOLD):
                tr, te = cv[r * N_FOLD + k]
                t = time.time(); m = modello(nome).fit(X.iloc[tr], y[tr]); P[te] = m.predict_proba(X.iloc[te]); tempi.append(time.time() - t)
            probs.append(P)
            print(f"  {col} {nome} ripetizione {r+1}/{N_RIP}: {time.time()-t0:.0f}s", flush=True)
        rip = []
        s0 = soglia_auto(probs[0], y)  # soglia scelta sulla ripetizione 1, misurata sulle altre
        for r, P in enumerate(probs):
            d = metriche_pred(y, P.argmax(1), classi); d["ece"] = ece(P, y)
            d["auto_soglia_rip1"] = copertura(P, y, s0); d["auto_soglia_rip1_residuo_s6"] = copertura(P, y, s0, gruppo_s6)
            rip.append(d)
        agg = {k: [float(np.mean([d[k] for d in rip])), float(np.std([d[k] for d in rip]))] for k in ["accuratezza", "macro_f1", "ece"]}
        altre = rip[1:] or rip
        agg["soglia_auto"] = s0
        for chiave in ["auto_soglia_rip1", "auto_soglia_rip1_residuo_s6"]:
            agg[chiave] = {"copertura_media": float(np.mean([d[chiave]["copertura"] for d in altre])),
                           "precisione_media": float(np.nanmean([d[chiave]["precisione"] or np.nan for d in altre]))}
        ok = probs[0].argmax(1) == y
        mc = {}
        for cn, pred in confronti.items():
            m = pred.notna().to_numpy()
            p = pred[m].map({c: i for i, c in enumerate(classi)}).fillna(-1).astype(int).to_numpy()
            mc[cn] = mcnemar(ok[m], p == y[m])
        out["modelli"][nome] = {"media_dev_std": agg, "per_ripetizione": rip, "mcnemar_rip1": mc,
                                "tempo_s": {"totale": float(sum(tempi)), "per_fold_medio": float(np.mean(tempi))}}
    return out


def main():
    import torch
    torch.set_num_threads(THREADS)
    t_inizio = time.time()
    df, cieco = carica()
    ingressi = {f: sha256(f) for f in list(FILE.values()) + [f"{d}/{n}" for d in CIECHI for n in ("etichette.csv", "campione-cieco.csv")]}
    ris = {"schema": "spesaict.sperimentazione-tfm/1", "ticket": 56, "data": "2026-11-19", "script": "tools/sperimentazioni/tfm/prova_leggera.py",
           "seme": SEME, "convalida": f"StratifiedKFold {N_FOLD} fold × {N_RIP} ripetizioni (RepeatedStratifiedKFold, random_state={SEME})",
           "soglia_precisione": SOGLIA_PREC, "tabicl": {"n_estimators": TABICL_STIMATORI, "device": "cpu", "threads": THREADS},
           "ingressi_sha256": ingressi, "versioni": {}, "obiettivi": {}}
    import sklearn, skrub, scipy, tabicl
    from importlib.metadata import version
    ris["versioni"] = {"python": platform.python_version(), "torch": torch.__version__, "scikit-learn": sklearn.__version__,
                       "skrub": skrub.__version__, "tabicl": version("tabicl"), "pandas": pd.__version__, "numpy": np.__version__, "scipy": scipy.__version__}
    hf = os.environ.get("HF_HOME", os.path.expanduser("~/.cache/huggingface"))
    pesi = [os.path.join(dp, f) for dp, _, fs in os.walk(os.path.join(hf, "hub", "models--jingang--TabICL", "blobs")) for f in fs if len(f) == 64]
    ris["pesi_tabicl"] = {"repo": "jingang/TabICL", "checkpoint": "tabicl-classifier-v2-20260212.ckpt",
                          "sha256_blob": [os.path.basename(p) for p in pesi]}

    # --- obiettivo 1: e_cloud ---
    d1, st1 = dedup(df[df["e_cloud"].isin(["s", "n"])], "e_cloud")
    regole = np.where(d1["regola_servizio"].isin(["cloud", "psn"]) | (d1["regola_via"] == "7-indeterminato-cloud"), "s", "n")
    conf1 = {"regole (passaggio 1)": pd.Series(regole, index=d1.index),
             "via 6 giro 1 sul solo testo (campione v3)": d1["giro1_e_cloud"].where(d1["giro1_e_cloud"].isin(["s", "n"])),
             "revisione cieca Opus (273 CIG S6)": d1["revisione_e_cloud"].where(d1["revisione_e_cloud"].isin(["s", "n"]))}
    s6 = (d1["sorgente"] != "v3").to_numpy()
    print(f"e_cloud: {len(d1)} CIG", flush=True)
    ris["obiettivi"]["e_cloud"] = {"dedup": st1, "regola_e_cloud_regole": "s se servizio delle regole in {cloud, psn} o via 7-indeterminato-cloud, altrimenti n",
                                   "n_residuo_s6": int(s6.sum()), **esperimento(d1, "e_cloud", ["n", "s"], conf1, s6)}

    # --- obiettivo 2: giurisdizione (IT/UE/EXTRA-UE) ---
    g = pd.concat([df, cieco], ignore_index=True)
    g = g[g["giurisdizione"].isin(GIUR)]
    d2, st2 = dedup(g, "giurisdizione")
    conf2 = {"regole (passaggio 1)": d2["regola_giurisdizione"].where(d2["regola_giurisdizione"].isin(GIUR)),
             "via 6 giro 1 sul solo testo (campione v3)": d2["giro1_giurisdizione"].where(d2["giro1_giurisdizione"].isin(GIUR))}
    s6b = d2["sorgente"].isin(["g1g3", "revisione"]).to_numpy()
    print(f"giurisdizione: {len(d2)} CIG", flush=True)
    ris["obiettivi"]["giurisdizione"] = {"dedup": st2, "n_residuo_s6": int(s6b.sum()), **esperimento(d2, "giurisdizione", GIUR, conf2, s6b)}
    ris["tempo_totale_s"] = time.time() - t_inizio
    os.makedirs(os.path.dirname(USCITA), exist_ok=True)
    with open(USCITA, "w", encoding="utf-8") as f:
        json.dump(ris, f, ensure_ascii=False, indent=1)
    print("scritto", USCITA, f"{ris['tempo_totale_s']:.0f}s")


if __name__ == "__main__":
    main()
