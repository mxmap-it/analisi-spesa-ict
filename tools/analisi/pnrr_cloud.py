"""Collegamento fra i finanziamenti PNRR cloud (PA Digitale 2026, Misure 1.1 e 1.2) e i contratti ANAC attribuiti (#43).
Catena: candidatura finanziata (CUP) -> dataset ANAC `cup` (CIG-CUP) -> contratto in lavoro/attribuzione/<anno>.csv.
Fonti, tutte archiviate con sha256: config/pnrr-risorse.txt (PA Digitale 2026) e il dataset ANAC `cup`.
Uso: python tools/analisi/pnrr_cloud.py -> lavoro/attribuzione/pnrr-cloud.json e pnrr-contratti.csv

Cosa misura, per ogni misura:
1. copertura del collegamento: quanti CUP finanziati hanno almeno un CIG (difetto del dato se basso);
2. dove finisce la spesa dei contratti collegati: provider, giurisdizione, tipo, canale;
3. quanta parte dei contratti collegati il classificatore NON attribuisce: è cloud per definizione (migrazione
   finanziata), quindi è una stima indipendente del cloud che sfugge alle vie 1-5.
Un CIG collegato a più CUP si conta una volta sola; gli importi sono importo_lotto, padri e importi da verificare esclusi."""
import collections, csv, glob, io, json, zipfile

PAD = "archivio/mirror/raw.githubusercontent.com/teamdigitale/padigitale2026-opendata/main/data/"
CUP = "archivio/mirror/dati.anticorruzione.it/opendata/download/dataset/cup/filesystem/cup_csv.zip"
MISURE = {"1.1": PAD + "candidature_finanziate_11.csv", "1.2": PAD + "candidature_finanziate_12.csv"}

def main():
    cand = {}
    for misura, f in MISURE.items():
        for r in csv.DictReader(open(f, encoding="utf-8")):
            cup = (r["codice_cup"] or "").strip().upper()
            if cup: cand[cup] = {"misura": misura, "importo": float(r["importo_finanziamento"] or 0), "tipologia": r["tipologia_ente"], "avviso": r["avviso"], "ente": r["ente"]}
    cig_per_cup = collections.defaultdict(set)
    z = zipfile.ZipFile(CUP)
    for r in csv.DictReader(io.TextIOWrapper(z.open(z.namelist()[0]), encoding="utf-8-sig", errors="replace"), delimiter=";"):
        cup = (r["CUP"] or "").strip().upper()
        if cup in cand: cig_per_cup[cup].add(r["CIG"].strip())
    cup_per_cig = collections.defaultdict(set)
    for c, gs in cig_per_cup.items():
        for g in gs: cup_per_cig[g].add(c)
    attr = {}
    for f in sorted(glob.glob("lavoro/attribuzione/[0-9]*.csv")):
        for r in csv.DictReader(open(f, encoding="utf-8")):
            attr[r["cig"]] = dict(r, anno=f[-8:-4])
    out = {"fonti": {"pa_digitale_2026": list(MISURE.values()), "anac_cup": CUP}, "misure": {}}
    righe = []
    for misura in MISURE:
        cups = [c for c, v in cand.items() if v["misura"] == misura]
        collegati = [c for c in cups if cig_per_cup.get(c)]
        cigs = {g for c in collegati for g in cig_per_cup[c]}
        visti = [attr[g] for g in sorted(cigs) if g in attr]
        spesa = collections.Counter(); n = collections.Counter(); esclusi = collections.Counter()
        for r in visti:
            imp = float(r["importo_lotto"] or 0)
            k = (r["giurisdizione"] or "-", r["provider"] or "nessun provider (" + r["via"] + ")", r["servizio"] or "-")
            n[k] += 1
            if r["e_padre"] == "1": esclusi["padri"] += imp
            elif r.get("importo_da_verificare"): esclusi["importi_da_verificare"] += imp
            else: spesa[k] += imp
            righe.append([misura, r["cig"], r["anno"], " ; ".join(sorted(c for c in cup_per_cig[r["cig"]] if cand[c]["misura"] == misura)), r["stazione_appaltante"], r["aggiudicatari"], imp,
                          r["via"], r["provider"], r["giurisdizione"], r["servizio"], r.get("canale", ""), r["e_padre"], r.get("importo_da_verificare", ""), r["testo"][:300]])
        attribuiti = sum(v for k, v in spesa.items() if not k[1].startswith("nessun"))
        totale = sum(spesa.values())
        out["misure"][misura] = {
            "candidature_finanziate": len(cups),
            "importo_finanziato": round(sum(cand[c]["importo"] for c in cups)),
            "cup_con_almeno_un_cig": len(collegati),
            "copertura_collegamento_pct": round(100 * len(collegati) / len(cups), 1) if cups else None,
            "cig_collegati": len(cigs),
            "cig_nel_perimetro_attribuito": len(visti),
            "cig_fuori_perimetro": len(cigs) - len(visti),
            "importo_contratti_nel_perimetro": round(totale),
            "importo_con_provider_attribuito_pct": round(100 * attribuiti / totale, 1) if totale else None,
            "esclusi": {k: round(v) for k, v in esclusi.items()},
            "per_giurisdizione_provider_tipo": [{"giurisdizione": k[0], "provider": k[1], "servizio": k[2], "cig": n[k], "importo": round(v)} for k, v in spesa.most_common()],
        }
    with open("lavoro/attribuzione/pnrr-contratti.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["misura", "cig", "anno", "cup", "stazione_appaltante", "aggiudicatari", "importo_lotto", "via", "provider", "giurisdizione", "servizio", "canale", "e_padre", "importo_da_verificare", "testo"])
        w.writerows(righe)
    json.dump(out, open("lavoro/attribuzione/pnrr-cloud.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({m: {k: v for k, v in d.items() if k != "per_giurisdizione_provider_tipo"} | {"primi": d["per_giurisdizione_provider_tipo"][:12]} for m, d in out["misure"].items()}, indent=1, ensure_ascii=False))

if __name__ == "__main__":
    main()
