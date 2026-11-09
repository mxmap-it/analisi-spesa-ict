"""Misura 1.2: giurisdizione dell infrastruttura come terzo asse (#43, #45). Versione 0.1.

Uso: nice .venv/bin/python tools/verifiche/infrastruttura_sottostante.py --data 2026-11-09
Ingressi (nessuna rete, nessun LLM):
- esiti/<data>/pnrr12/pnrr12-dettaglio.csv (pnrr12_prodotto.py)
- config/saas_infrastruttura.yaml (classi infrastruttura dei SaaS S2)
- Libro PSN 2025 dall archivio (sha256 b8fe9ec1...), letto con pdftotext: ricavi 2025/2024 per servizio, mix canoni
Uscita: esiti/<data>/infrastruttura-sottostante/infrastruttura.json
"""
import argparse, collections, csv, json, pathlib, re, subprocess, yaml
R = pathlib.Path(__file__).resolve().parents[2]
LIBRO = "b8fe9ec1b4becdbf07cf837cac4f5ef26621bda85c7bfa1162773bf9a7ed64ed"

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
    assert "60% rispetto al 40% dei canoni" in t.replace("\n", " ") or re.search(r"60%\s+rispetto al 40%", t)
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
    # quota hyperscaler sui canoni PAL/ASL (Misura 1.2 = enti locali e ASL)
    spc = (mix["Secure Public Cloud"]["PAL"] + mix["Secure Public Cloud"]["ASL"]) / 2
    ora = (mix["Soluzioni Oracle PSN"]["PAL"] + mix["Soluzioni Oracle PSN"]["ASL"]) / 2
    canone = {"basso": spc, "centrale": spc + k * ora, "alto": spc + ora + 5}  # +5: Hybrid dentro Altri (<5 %)
    # due letture: stretta (migrazione = servizio PSN, IT) e destinazione (R-S1: la migrazione segue l infrastruttura)
    peso_canoni = {"basso": 0.2, "centrale": 0.4, "alto": 0.6}
    # dettaglio 1.2
    yml = yaml.safe_load(open(R / "config/saas_infrastruttura.yaml", encoding="utf-8"))
    noto_it = {f["nome"] for f in yml["fornitori"] if f["classe"] != "ignoto" and "hyperscaler" not in f["classe"]}
    s = collections.Counter()
    for r in csv.DictReader(open(R / f"esiti/{d}/pnrr12/pnrr12-dettaglio.csv", encoding="utf-8")):
        parts = r["strati"].split(" | "); w = float(r["importo_lotto"] or 0) / len(parts)
        for p in parts:
            st, giu, forn = (p.split(":") + ["", ""])[:3]; st = st[:2]
            if st == "S1": s["S1 PSN" if forn == "Polo Strategico Nazionale" else ("S1 big tech" if "EXTRA" in giu else "S1 IT altro")] += w
            elif st == "S2": s["S2 infra IT nota" if forn in noto_it else "S2 infra ignota"] += w
            else: s[st] += w
    s = {k2: v / 1e6 for k2, v in s.items()}; tot = sum(s.values())
    psn12 = s["S1 PSN"]
    ign = s["S2 infra ignota"] + s.get("S3", 0) + s.get("S4", 0)
    quota_ign = {"basso": 0, "centrale": 0.25, "alto": 1}  # ipotesi, nessun dato: nessun hyperscaler accertato fra i noti
    out = {}
    for sc in ("basso", "centrale", "alto"):
        psn_str = psn12 * peso_canoni[sc] * canone[sc] / 100
        psn_dest = psn12 * canone[sc] / 100
        s5 = {"basso": 0, "centrale": s["S5"], "alto": s["S5"]}[sc]
        base = s["S1 big tech"] + psn_dest + ign * quota_ign[sc] + s5
        attrib = tot - s["S6"]
        s6 = {"basso": 0, "centrale": s["S6"] * base / attrib, "alto": s["S6"]}[sc]
        out[sc] = {"psn_hyperscaler_pct_canoni": round(canone[sc], 1), "psn_lettura_stretta_meur": round(psn_str, 1),
                   "psn_lettura_destinazione_meur": round(psn_dest, 1), "saas_s3_s4_ignoti_meur": round(ign * quota_ign[sc], 1),
                   "s5_meur": round(s5, 1), "s6_meur": round(s6, 1), "totale_extraue_infra_meur": round(base + s6, 1),
                   "quota_pct": round(100 * (base + s6) / tot, 1)}
    res = {"data": d, "versione": "0.1", "psn_libro_2025": psn, "misura_12_strati_meur": {k2: round(v, 2) for k2, v in s.items()},
           "totale_meur": round(tot, 1), "saas_ignoti_meur": round(ign, 1), "scenari": out,
           "assunzioni": {"peso_canoni": peso_canoni, "quota_hyperscaler_saas_ignoti": quota_ign,
                          "canone_pal_asl": "media semplice PAL e ASL/AO del Libro PSN 2025; Managed = quota k di Oracle PSN da ricavi 2025",
                          "S5": "controllo extra-UE del fornitore = giurisdizione extra-UE sull infrastruttura che gestisce (centrale)",
                          "S6": "centrale: stessa quota dell attribuito; alto: tutto"}}
    o = R / f"esiti/{d}/infrastruttura-sottostante"; o.mkdir(parents=True, exist_ok=True)
    (o / "infrastruttura.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(res, indent=1, ensure_ascii=False))
main()
