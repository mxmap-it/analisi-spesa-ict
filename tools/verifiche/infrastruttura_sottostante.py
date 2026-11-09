"""Misura 1.2: giurisdizione dell infrastruttura come terzo asse (#43, #45). Versione 0.2.

v0.2: ASL/AO con la quota misurata sui Progetti dei piani dei fabbisogni PSN (psn-ppdf.csv); SaaS con quota per fornitore
da config/saas_infrastruttura.yaml (atti, schede ACN, DNS/AS); i fornitori senza prove prendono la media in euro di quelli
con prove (non piu l ipotesi fissa del 25 % della v0.1).

Uso: nice .venv/bin/python tools/verifiche/infrastruttura_sottostante.py --data 2026-11-09
Ingressi (nessuna rete, nessun LLM):
- esiti/<data>/pnrr12/pnrr12-dettaglio.csv (pnrr12_prodotto.py)
- config/saas_infrastruttura.yaml (classe e quota hyperscaler per fornitore SaaS S2)
- esiti/<data>/infrastruttura-sottostante/psn-ppdf.csv (Riepilogo prezzi dei PPdF PSN letti)
- Libro PSN 2025 dall archivio (sha256 b8fe9ec1...), letto con pdftotext: ricavi 2025/2024 per servizio, mix canoni
Uscita: esiti/<data>/infrastruttura-sottostante/infrastruttura.json
"""
import argparse, collections, csv, json, pathlib, re, subprocess, yaml
R = pathlib.Path(__file__).resolve().parents[2]
LIBRO = "b8fe9ec1b4becdbf07cf837cac4f5ef26621bda85c7bfa1162773bf9a7ed64ed"
SCENARI = ("basso", "centrale", "alto")


def libro():
    blob = R / "archivio/blobs/sha256" / LIBRO[:2] / LIBRO[2:4] / LIBRO
    t = subprocess.run(["pdftotext", "-layout", str(blob), "-"], capture_output=True, text=True, check=True).stdout
    def ric(et):
        m = re.search(r"^\s*" + re.escape(et) + r"\s+([\d.]+)\s+([\d.]+)\s*$", t, re.M)
        return [int(x.replace(".", "")) for x in m.groups()]
    voci = ["IaaS", "Secure Public Cloud", "Housing", "Hosting", "Public Cloud on PSN Managed", "PaaS", "CaaS",
            "Data Protection, Security, Sistemi Operativi, Connettività", "Servizi di coordinamento progettuale"]
    r = {v: ric(v) for v in voci}
    m = re.search(r"Totale\s+(454\.328\.062)\s+(255\.534\.885)", t); assert m, "totale ricavi"
    r["Totale"] = [454328062, 255534885]
    r["Servizi migrazione"] = [r["Totale"][i] - sum(r[v][i] for v in voci) for i in (0, 1)]
    mix = {}
    for et in ["Soluzioni Oracle PSN", "Secure Public Cloud", "Housing & Hosting", "Servizi di Backup", "PaaS"]:
        m = re.search(r"^\s*" + re.escape(et) + r"\s+(\d+)%\s+(\d+)%\s+(\d+)%\s+(\d+)%", t, re.M)
        mix[et] = dict(zip(["PAC", "PAL", "ASL", "Tot"], map(int, m.groups())))
    assert re.search(r"60%\s+rispetto al 40%", t)
    return r, mix


def main():
    a = argparse.ArgumentParser(); a.add_argument("--data", required=True); d = a.parse_args().data
    ric, mix = libro()
    hs = [ric["Secure Public Cloud"][i] + ric["Public Cloud on PSN Managed"][i] for i in (0, 1)]
    infra = [ric["Totale"][i] - ric["Servizi migrazione"][i] - ric["Servizi di coordinamento progettuale"][i] for i in (0, 1)]
    psn = {"ricavi_2025": ric["Totale"][0], "ricavi_2024": ric["Totale"][1],
           "hyperscaler_ricavi_2025_pct": round(100 * hs[0] / ric["Totale"][0], 1),
           "hyperscaler_su_infrastruttura_2025_pct": round(100 * hs[0] / infra[0], 1),
           "hyperscaler_ricavi_2024_pct": round(100 * hs[1] / ric["Totale"][1], 1),
           "hyperscaler_su_infrastruttura_2024_pct": round(100 * hs[1] / infra[1], 1),
           "managed_su_oracle_psn_stima": round(ric["Public Cloud on PSN Managed"][0] / infra[0] / (mix["Soluzioni Oracle PSN"]["Tot"] / 100), 2),
           "mix_canoni": mix}
    k = psn["managed_su_oracle_psn_stima"]
    # PSN, quota hyperscaler sui canoni per tipologia.
    # ASL/AO: centrale = misurata sui PPdF letti; basso = solo SPC ASL del Libro; alto = scheda PPdF piu alta.
    # Comuni e altri: Libro PAL (SPC; centrale + Managed = k x Oracle PSN; alto tutto Oracle + 5 di Hybrid).
    pp = list(csv.DictReader(open(R / f"esiti/{d}/infrastruttura-sottostante/psn-ppdf.csv", encoding="utf-8"), delimiter=";"))
    hs_pp = lambda r: float(r["spc"]) + float(r["managed_canone"]) + float(r["hybrid"])
    asl = [r for r in pp if r["ente"].startswith("ARES-")]  # schede del SSR sardo (ASL, AO, AREUS)
    asl_mis = 100 * sum(map(hs_pp, asl)) / sum(float(r["tot_canone"]) for r in asl)
    asl_max = max(100 * hs_pp(r) / float(r["tot_canone"]) for r in asl)
    pal, ora_pal = mix["Secure Public Cloud"]["PAL"], mix["Soluzioni Oracle PSN"]["PAL"]
    canone = {"ASL": dict(zip(SCENARI, (mix["Secure Public Cloud"]["ASL"], asl_mis, asl_max))),
              "altri": dict(zip(SCENARI, (pal, pal + k * ora_pal, pal + ora_pal + 5)))}
    peso_canoni = dict(zip(SCENARI, (0.2, 0.4, 0.6)))
    # Misura 1.2
    yml = yaml.safe_load(open(R / "config/saas_infrastruttura.yaml", encoding="utf-8"))
    qf = {f["nome"]: f.get("quota_hyperscaler") for f in yml["fornitori"]}
    s = collections.Counter(); psn_t = collections.Counter(); s2f = collections.Counter()
    for r in csv.DictReader(open(R / f"esiti/{d}/pnrr12/pnrr12-dettaglio.csv", encoding="utf-8")):
        parts = r["strati"].split(" | "); w = float(r["importo_lotto"] or 0) / len(parts) / 1e6
        for p in parts:
            st, giu, forn = (p.split(":") + ["", ""])[:3]; st = st[:2]
            if st == "S1" and forn == "Polo Strategico Nazionale":
                s["S1 PSN"] += w; psn_t["ASL" if r["tipologia_ente"] == "ASL" else "altri"] += w
            elif st == "S1": s["S1 big tech" if "EXTRA" in giu else "S1 IT altro"] += w
            elif st == "S2": s2f[forn] += w; s["S2"] += w
            else: s[st] += w
    tot = sum(s.values())
    noti = {f: v for f, v in s2f.items() if qf.get(f)}
    nota_eur = sum(noti.values())
    saas_q = {sc: sum(v * qf[f][i] for f, v in noti.items()) for i, sc in enumerate(SCENARI)}
    p_noti = saas_q["centrale"] / nota_eur
    s2_ign = s["S2"] - nota_eur
    ign = s2_ign + s.get("S3", 0) + s.get("S4", 0)
    quota_ign = dict(zip(SCENARI, (0, p_noti, 1)))
    out = {}
    for sc in SCENARI:
        psn_dest = sum(psn_t[t] * canone[t][sc] / 100 for t in psn_t)
        s5 = {"basso": 0, "centrale": s["S5"], "alto": s["S5"]}[sc]
        base = s["S1 big tech"] + psn_dest + saas_q[sc] + ign * quota_ign[sc] + s5
        s6 = {"basso": 0, "centrale": s["S6"] * base / (tot - s["S6"]), "alto": s["S6"]}[sc]
        out[sc] = {"psn_canone_hyperscaler_pct": {t: round(canone[t][sc], 1) for t in canone},
                   "psn_lettura_stretta_meur": round(psn_dest * peso_canoni[sc], 1),
                   "psn_lettura_destinazione_meur": round(psn_dest, 1),
                   "saas_con_prove_meur": round(saas_q[sc], 1), "saas_senza_prove_e_s3_s4_meur": round(ign * quota_ign[sc], 1),
                   "s5_meur": round(s5, 1), "s6_meur": round(s6, 1), "totale_extraue_infra_meur": round(base + s6, 1),
                   "quota_pct": round(100 * (base + s6) / tot, 1)}
    res = {"data": d, "versione": "0.2", "psn_libro_2025": psn,
           "psn_ppdf": {"schede": len(asl), "asl_canone_hyperscaler_misurato_pct": round(asl_mis, 1), "asl_max_pct": round(asl_max, 1)},
           "psn_12_per_tipologia_meur": {t: round(v, 1) for t, v in psn_t.items()},
           "misura_12_strati_meur": {k2: round(v, 2) for k2, v in s.items()}, "totale_meur": round(tot, 1),
           "saas_con_prove_meur": round(nota_eur, 1), "saas_con_prove_quota_centrale": round(p_noti, 3),
           "saas_s2_senza_prove_meur": round(s2_ign, 1), "saas_senza_prove_e_s3_s4_meur": round(ign, 1),
           "saas_per_fornitore": {f: {"meur": round(v, 2), "quota": qf[f]} for f, v in sorted(noti.items(), key=lambda x: -x[1])},
           "scenari": out,
           "assunzioni": {"peso_canoni_lettura_stretta": peso_canoni, "quota_saas_senza_prove": quota_ign,
                          "psn": "ASL: centrale misurata sui PPdF (ARES); altri: Libro PAL con Managed = k x Oracle PSN",
                          "saas": "quota per fornitore da config/saas_infrastruttura.yaml; senza prove = media in euro dei fornitori con prove",
                          "S5": "controllo extra-UE del fornitore = giurisdizione extra-UE sull infrastruttura che gestisce (centrale)",
                          "S6": "centrale: stessa quota dell attribuito; alto: tutto"}}
    o = R / f"esiti/{d}/infrastruttura-sottostante"; o.mkdir(parents=True, exist_ok=True)
    (o / "infrastruttura.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k2: v for k2, v in res.items() if k2 not in ("psn_libro_2025", "assunzioni")}, indent=1, ensure_ascii=False))


main()
