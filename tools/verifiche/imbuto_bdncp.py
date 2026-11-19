#!/usr/bin/env python3
"""Imbuto, livello B (BDNCP): quattro segnali dalla Banca dati nazionale dei contratti pubblici sui CIG ICT (#74, #71).
Decisione di Fabio 19/11/2026: «fai tutto, falli tutti e quattro, pubblica e integra la metodologia, tutto ripetibile».

Ingresso: lavoro/imbuto/ict.csv (imbuto IMBUTO_VERSIONE, strati S3-S6, CIG dal 2020) e i dataset BDNCP del mirror ANAC
(archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/<ds>/filesystem/<ds>_csv.zip, l'ultimo zip «pieno»,
come bdncp_inventario.py), letti in streaming, un dataset alla volta. sha256 di ogni ingresso nel riepilogo.

B1 quadro economico: quota lavori = lavori / (forniture + servizi + lavori) dell'evento BASE_ASTA (se manca, il primo
   evento con importi). Regola di esclusione dalla misura cloud (come L2, il CIG resta ICT): strato S5/S6, quota lavori
   >= 0,8 e il testo non parla di cloud né di data center (RX_CLOUD_DC: un data center costruito è infrastruttura interna,
   che è nell'obiettivo). Su S3/S4 nessuna esclusione: i casi si elencano come anomalie da rivedere.
B2 in-house: per i CIG S4-marchio/in-house, i codici fiscali degli aggiudicatari contro l'Indice PA e l'anagrafica delle
   stazioni appaltanti (i flag_inHouse/flag_partecipata ANAC sono tutti «false», non compilati). Classi: ipa (soggetto
   pubblico), sa-non-ipa (registrato come stazione appaltante, può essere privato), non-sa (privato), senza-aggiudicatario.
   Regola: la classe in-house regge solo con «ipa».
B3 durate: inizio effettivo (avvio-contratto: data_inizio_effettiva, poi stipula, poi esecutività) e fine (fine-contratto:
   data_effettiva_ultimazione, poi avvio-contratto: data_termine_contrattuale). Quota annua 2024 e 2025 con le date
   effettive contro la regola attuale (data di pubblicazione + DURATA_PREVISTA, bdap_cig_ministeri_cf.quote).
B4 PNRR: tre vie indipendenti sullo stesso CIG: FLAG_PNRR_PNC del CIG, presenza in indicatori-pnrrpnc, CUP (dataset cup);
   più la catena v3 (report/metodo/pnrr-contratti-v3.csv). Tabella incrociata su tutti i CIG ICT e sul cloud.

Uso (SUL SERVER, come mxmap.it, nice, dopo free -g, un job pesante alla volta):
  flock lavoro/pesante.lock nice .venv/bin/python tools/verifiche/imbuto_bdncp.py   -> esiti/<oggi>/imbuto/bdncp/v<VERSIONE>/{segnali.csv.gz,riepilogo.json,campione-*.csv}
"""
import collections, csv, datetime, glob, gzip, hashlib, io, json, os, random, re, sys, zipfile
from pathlib import Path

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/verifiche"))
import bdap_cig_ministeri_cf as M  # noqa: E402  quote(): regola attuale della quota annua

D = R / "archivio/mirror/dati.anticorruzione.it/opendata/download/dataset"
ICT = R / os.environ.get("IMBUTO_ICT", "lavoro/imbuto/ict.csv")  # IMBUTO_ICT / IMBUTO_ESITI_OUT: prova di ripetibilità
VERSIONE = "0.2"  # 0.1 (19/11 notte): esiti in esiti/2026-11-19/imbuto/bdncp/; dalla 0.2 una sottocartella per versione
OGGI = os.environ.get("ESITI_DATA", datetime.date.today().isoformat())
OUT = R / (os.environ.get("IMBUTO_ESITI_OUT") or f"esiti/{OGGI}/imbuto/bdncp/v{VERSIONE}")
RX_CLOUD_DC = re.compile(r"cloud|saas|iaas|paas|hosting|data\s*cent|datacent|\bced\b|sala\s+(?:server|macchine)|server\s+farm|"
                         r"(?:sala|locale|locali)\s+(?:server|macchine|ced)|piattaforma\s+(?:web|online)|in\s+remoto|\bpsn\b|"
                         r"pago\s*pa|siti?\s+(?:web|internet|istituzional)|licenz|"
                         r"locali?\s+(?:informatic|tecnologic|tecnic[oi]\s+informatic)|\bare[ae]\s+server", re.I)
# 0.1 (19/11): dal campione di sviluppo B1. 0.2 (19/11): + «locali informatici», «locali tecnologici», «area server»
# (errori e dubbi del campione di misura 0.1, report/metodo/bdncp/b1-campione-misura.csv).
# Campioni B1 già annotati: i CIG si escludono dal nuovo campione di misura (misura a cieco su casi mai visti).
VISTI_B1 = ["report/metodo/bdncp/b1-campione-sviluppo.csv", "report/metodo/bdncp/b1-campione-misura.csv"]
SOGLIA_LAVORI = 0.8
ANNI_QUOTA = (2024, 2025)
ORDINE = ["ipa", "sa-non-ipa", "non-sa"]
csv.field_size_limit(1 << 30)
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


def righe(z):
    ingressi[os.path.relpath(z, R)] = {"sha256": sha(z), "byte": os.path.getsize(z)}
    zf = zipfile.ZipFile(z)
    m = next(n for n in zf.namelist() if n.endswith(".csv"))
    return csv.DictReader(io.TextIOWrapper(zf.open(m), encoding="utf-8-sig", errors="replace"), delimiter=";")


def pieno(ds):
    return D / ds / "filesystem" / f"{ds}_csv.zip"


def data(s):
    try:
        return datetime.date.fromisoformat((s or "")[:10])
    except ValueError:
        return None


def carica_ict():
    ict = {}
    ingressi[os.path.relpath(ICT, R)] = {"sha256": sha(ICT)}
    for r in csv.DictReader(open(ICT, encoding="utf-8")):
        if not r["strato"].startswith(("S3", "S4", "S5", "S6")) or int(r["anno"] or 0) < 2020:
            continue
        ict[r["cig"]] = {"anno": int(r["anno"]), "strato": r["strato"], "sottoclasse": r["sottoclasse"], "importo": num(r["importo"]),
                         "da_verificare": r["importo_da_verificare"] == "1", "cloud_dc": bool(RX_CLOUD_DC.search(r["testo"])),
                         "aggiudicatari": r["aggiudicatari"][:120], "ente": r["stazione_appaltante"][:120], "testo": r["testo"][:300]}
    return ict


def cig_anac(ict):
    """data di pubblicazione, DURATA_PREVISTA e FLAG_PNRR_PNC: file annuali 2020-2025, poi mensili (vince l'ultimo)."""
    zz = [z for a in range(2020, 2026) for z in sorted(glob.glob(str(D / f"cig-{a}/filesystem/cig_csv_*.zip")))]
    zz += sorted(glob.glob(str(D / "cig/filesystem/*-cig_csv.zip")))
    for z in zz:
        for r in righe(z):
            c = ict.get(r["cig"])
            if c is not None:
                c["data_pub"] = r["data_pubblicazione"][:10]
                c["durata_prevista"] = num(r.get("DURATA_PREVISTA"))
                c["flag_pnrr"] = (r.get("FLAG_PNRR_PNC") or "").strip()


def b1_quadro(ict):
    ev = {}
    for r in righe(pieno("quadro-economico")):
        c = r["cig"]
        if c not in ict:
            continue
        f, s, l = num(r["importo_forniture"]), num(r["importo_servizi"]), num(r["importo_lavori"])
        if f + s + l <= 0:
            continue
        base = (r["descrizione_evento"] or "").upper() == "BASE_ASTA"
        if c not in ev or (base and not ev[c][0]):
            ev[c] = (base, f, s, l, r["descrizione_evento"])
    for c, (base, f, s, l, e) in ev.items():
        x = ict[c]
        x["qe_evento"], x["qe_forniture"], x["qe_servizi"], x["qe_lavori"] = e, f, s, l
        x["qe_quota_lavori"] = l / (f + s + l)
        x["b1"] = ("esce-lavori" if x["strato"][:2] in ("S5", "S6") and x["qe_quota_lavori"] >= SOGLIA_LAVORI and not x["cloud_dc"]
                   else "anomalia-lavori-S3S4" if x["qe_quota_lavori"] >= SOGLIA_LAVORI and x["strato"][:2] in ("S3", "S4")
                   else "")


def b2_inhouse(ict):
    """flag_inHouse e flag_partecipata dell'anagrafica ANAC sono «false» per tutte le 48.040 stazioni appaltanti (19/11/2026):
    il campo non è compilato. Si usa quindi l'Indice PA (amministrazioni.txt archiviato): un aggiudicatario con codice
    fiscale in IPA è un soggetto pubblico; uno registrato solo come stazione appaltante può essere privato (TIM, DGS)."""
    sa, ipa, flag = set(), {}, collections.Counter()
    for r in righe(pieno("stazioni-appaltanti")):
        flag[(r["flag_inHouse"], r["flag_partecipata"])] += 1
        sa.update({(r["codice_fiscale"] or "").strip(), (r["partita_iva"] or "").strip()} - {"", "00000000000"})
    p = sorted(glob.glob(str(R / "archivio/mirror/indicepa.gov.it/ipa-dati/dataset/*/resource/*/download/amministrazioni.txt")))[-1]
    ingressi[os.path.relpath(p, R)] = {"sha256": sha(p)}
    for r in csv.DictReader(open(p, encoding="utf-8-sig", newline=""), delimiter="\t"):
        if (r.get("cf") or "").strip():
            ipa[r["cf"].strip()] = (r["des_amm"], r.get("tipologia_istat") or "")
    inh = {c for c, x in ict.items() if x["strato"] == "S4-marchio" and x["sottoclasse"] == "in-house"}
    agg = collections.defaultdict(list)
    for r in righe(pieno("aggiudicatari")):
        if r["cig"] in inh:
            agg[r["cig"]].append((r["codice_fiscale"] or "").strip().upper().removeprefix("IT"))
    for c in inh:
        cl = ["ipa" if cf in ipa else "sa-non-ipa" if cf in sa else "non-sa" for cf in agg.get(c, [])]
        ict[c]["b2"] = min(cl, key=ORDINE.index) if cl else "senza-aggiudicatario"
        ict[c]["b2_cf"] = "|".join(sorted(set(agg.get(c, []))))[:120]
        ict[c]["b2_ipa"] = "|".join(sorted({ipa[cf][1] for cf in agg.get(c, []) if cf in ipa}))[:120]
    ingressi["flag_stazioni_appaltanti"] = {f"{a}/{b}": n for (a, b), n in flag.items()}


def b3_durate(ict):
    for r in righe(pieno("avvio-contratto")):
        x = ict.get(r["cig"])
        if x is None:
            continue
        d0 = data(r["data_inizio_effettiva"]) or data(r["data_stipula_contratto"]) or data(r["data_esecutivita_contratto"])
        if d0 and (x.get("d0") is None or d0 < x["d0"]):
            x["d0"] = d0
        t = data(r["data_termine_contrattuale"])
        if t:
            x["d1_termine"] = max(t, x.get("d1_termine") or t)
    for r in righe(pieno("fine-contratto")):
        x = ict.get(r["cig"])
        u = data(r["data_effettiva_ultimazione"]) if x is not None else None
        if u:
            x["d1_fine"] = max(u, x.get("d1_fine") or u)
    for x in ict.values():
        d1 = x.get("d1_fine") or x.get("d1_termine")
        if x.get("d0") and d1 and d1 > x["d0"]:
            x["d1"], x["durata_eff"] = d1, (d1 - x["d0"]).days


def b4_pnrr(ict):
    for r in righe(pieno("indicatori-pnrrpnc")):
        if r["cig"] in ict:
            ict[r["cig"]]["ind_pnrr"] = True
    for r in righe(pieno("cup")):
        c = (r.get("CIG") or r.get("cig") or "").strip()
        if c in ict:
            ict[c]["cup"] = True
    v3 = R / "report/metodo/pnrr-contratti-v3.csv"
    ingressi[os.path.relpath(v3, R)] = {"sha256": sha(v3)}
    for r in csv.DictReader(open(v3, encoding="utf-8")):
        if r["cig"] in ict:
            ict[r["cig"]]["v3"] = r["misura"]


def flag_si(v):
    v = (v or "").upper()
    return v not in ("", "N", "NO", "0", "FALSE") and not v.startswith("NESSUN")


def cloud(x):
    return x["sottoclasse"] in ("cloud", "psn", "in-house") or x["strato"].startswith("S6")


def riepilogo(ict):
    dal24 = {c: x for c, x in ict.items() if x["anno"] >= 2024}
    E = lambda it: round(sum(x["importo"] for x in it if not x["da_verificare"]) / 1e6, 1)  # noqa: E731
    out = {"versione": f"imbuto-bdncp {VERSIONE}", "data": OGGI, "imbuto": os.environ.get("IMBUTO_VERSIONE", "0.3.4"),
           "cig_ict_dal_2020": len(ict), "cig_ict_dal_2024": len(dal24), "soglia_lavori": SOGLIA_LAVORI,
           "rx_cloud_dc": RX_CLOUD_DC.pattern, "nota_importi": "M€, importo del lotto, senza importi da verificare"}
    # B1
    qe = [x for x in dal24.values() if "qe_quota_lavori" in x]
    fasce = collections.defaultdict(list)
    for x in qe:
        q = x["qe_quota_lavori"]
        fasce["0" if q == 0 else "<0,2" if q < .2 else "0,2-0,5" if q < .5 else "0,5-0,8" if q < .8 else ">=0,8"].append(x)
    out["b1_quadro_economico"] = {
        "cig_con_qe": len(qe), "copertura": round(len(qe) / len(dal24), 3), "importo_con_qe": E(qe),
        "fasce_quota_lavori": {k: {"cig": len(v), "importo": E(v)} for k, v in sorted(fasce.items())},
        "esce_lavori": {"cig": sum(x.get("b1") == "esce-lavori" for x in dal24.values()), "importo": E(x for x in dal24.values() if x.get("b1") == "esce-lavori"),
                        "per_strato": {s: {"cig": len(v), "importo": E(v)} for s, v in sorted(_per(dal24, "b1", "esce-lavori", "strato").items())},
                        "per_sottoclasse": {s: {"cig": len(v), "importo": E(v)} for s, v in sorted(_per(dal24, "b1", "esce-lavori", "sottoclasse").items())}},
        "lavori_ma_cloud_dc_restano": {"cig": sum(1 for x in qe if x["qe_quota_lavori"] >= SOGLIA_LAVORI and x["cloud_dc"] and x["strato"][:2] in ("S5", "S6")),
                                       "importo": E(x for x in qe if x["qe_quota_lavori"] >= SOGLIA_LAVORI and x["cloud_dc"] and x["strato"][:2] in ("S5", "S6"))},
        "anomalie_S3S4": {"cig": sum(x.get("b1") == "anomalia-lavori-S3S4" for x in dal24.values()), "importo": E(x for x in dal24.values() if x.get("b1") == "anomalia-lavori-S3S4")}}
    # B2
    inh = [x for x in dal24.values() if "b2" in x]
    cl = collections.defaultdict(list)
    for x in inh:
        cl[x["b2"]].append(x)
    top = {k: collections.Counter() for k in cl}
    for k, v in cl.items():
        for x in v:
            if not x["da_verificare"]:
                top[k][x["aggiudicatari"][:60]] += x["importo"]
    out["b2_inhouse"] = {"cig": len(inh), "importo": E(inh), "classi": {k: {"cig": len(v), "importo": E(v),
                         "primi_aggiudicatari": [(a, round(i / 1e6, 1)) for a, i in top[k].most_common(8)]} for k, v in sorted(cl.items())}}
    # B3
    cop = [x for x in ict.values() if "durata_eff" in x]
    rapp = sorted(x["durata_eff"] / x["durata_prevista"] for x in cop if x.get("durata_prevista", 0) > 0)
    q_att, q_eff = collections.Counter(), collections.Counter()
    for x in cop:
        if x["da_verificare"] or "data_pub" not in x:
            continue
        for y, v in M.quote(x["importo"], x["data_pub"], int(x.get("durata_prevista") or 0)).items():
            q_att[y] += v
        for y, v in M.quote(x["importo"], x["d0"].isoformat(), min(x["durata_eff"], 3650)).items():
            q_eff[y] += v
    out["b3_durate"] = {"cig_con_date_dal_2020": len(cop), "copertura_dal_2020": round(len(cop) / len(ict), 3),
                        "cig_con_date_dal_2024": sum(1 for x in dal24.values() if "durata_eff" in x),
                        "fine_da_ultimazione": sum(1 for x in cop if x.get("d1_fine")),
                        "rapporto_durata_eff_su_prevista": {"n": len(rapp), "p25": _q(rapp, .25), "mediana": _q(rapp, .5), "p75": _q(rapp, .75)},
                        "quota_annua_stessi_cig": {str(y): {"regola_attuale": round(q_att[y] / 1e6, 1), "date_effettive": round(q_eff[y] / 1e6, 1)} for y in ANNI_QUOTA}}
    # B4
    def tab(it):
        t = collections.defaultdict(list)
        for x in it:
            t[("flag" if flag_si(x.get("flag_pnrr")) else "-") + "/" + ("indicatori" if x.get("ind_pnrr") else "-") + "/" + ("cup" if x.get("cup") else "-")].append(x)
        return {k: {"cig": len(v), "importo": E(v)} for k, v in sorted(t.items())}
    out["b4_pnrr"] = {"valori_flag": collections.Counter(x.get("flag_pnrr", "assente") for x in dal24.values()).most_common(10),
                      "flag_indicatori_cup_tutti_ict": tab(dal24.values()), "flag_indicatori_cup_cloud": tab(x for x in dal24.values() if cloud(x)),
                      "catena_v3_dal_2024": {m: {"cig": len(v), "flag": sum(flag_si(x.get("flag_pnrr")) for x in v), "indicatori": sum(bool(x.get("ind_pnrr")) for x in v)}
                                             for m, v in sorted(_per(dal24, "v3", None, "v3").items())}}
    out["ingressi"] = ingressi
    return out


def _per(d, campo, valore, chiave):
    g = collections.defaultdict(list)
    for x in d.values():
        if (valore is None and x.get(campo)) or (valore is not None and x.get(campo) == valore):
            g[x[chiave]].append(x)
    return g


def _q(v, p):
    return round(v[int(p * (len(v) - 1))], 2) if v else None


def scrivi(ict, out):
    os.makedirs(OUT, exist_ok=True)
    campi = ["cig", "anno", "strato", "sottoclasse", "importo", "da_verificare", "b1", "qe_evento", "qe_quota_lavori", "b2", "b2_cf", "b2_ipa",
             "data_pub", "durata_prevista", "d0", "d1", "durata_eff", "flag_pnrr", "ind_pnrr", "cup", "v3", "ente", "aggiudicatari"]
    with gzip.open(OUT / "segnali.csv.gz", "wt", newline="", encoding="utf-8") as fh:  # 19/11: 51 MB non compresso, oltre il limite consigliato da GitHub
        w = csv.writer(fh)
        w.writerow(campi)
        for c in sorted(ict):
            x = ict[c]
            if not any(k in x for k in ("qe_quota_lavori", "b2", "durata_eff", "ind_pnrr", "cup", "v3")) and not flag_si(x.get("flag_pnrr")):
                continue
            w.writerow([c] + [round(x[k], 3) if isinstance(x.get(k), float) else x.get(k, "") for k in campi[1:]])
    # semi: 7419 campione di sviluppo B1, 20261119 campioni di misura 0.1, 202611192 campione di misura B1 0.2
    visti = {r["cig"] for p in VISTI_B1 if (R / p).exists() for r in csv.DictReader(open(R / p, encoding="utf-8"))}
    for nome, sel, seme in (("campione-b1-esce-lavori", lambda x: x.get("b1") == "esce-lavori", 202611192),
                            ("campione-b2-non-sa", lambda x: x.get("b2") == "non-sa", 20261119)):
        rnd = random.Random(seme)
        el = sorted(c for c, x in ict.items() if x["anno"] >= 2024 and sel(x) and not (nome.startswith("campione-b1") and c in visti))
        with open(OUT / f"{nome}.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["cig", "strato", "sottoclasse", "importo", "qe_quota_lavori", "b2_cf", "ente", "aggiudicatari", "testo", "giudizio"])
            for c in sorted(rnd.sample(el, min(40, len(el)))):
                x = ict[c]
                w.writerow([c, x["strato"], x["sottoclasse"], round(x["importo"]), round(x.get("qe_quota_lavori", 0), 2), x.get("b2_cf", ""),
                            x["ente"], x["aggiudicatari"], x["testo"], ""])
    json.dump(out, open(OUT / "riepilogo.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=str)


def main():
    ict = carica_ict()
    print(datetime.datetime.now().isoformat(timespec="seconds"), "ICT", len(ict), flush=True)
    for passo in (b1_quadro, b2_inhouse, b3_durate, b4_pnrr, cig_anac):
        passo(ict)
        print(datetime.datetime.now().isoformat(timespec="seconds"), passo.__name__, flush=True)
    out = riepilogo(ict)
    scrivi(ict, out)
    print(json.dumps({k: v for k, v in out.items() if k != "ingressi"}, indent=1, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
