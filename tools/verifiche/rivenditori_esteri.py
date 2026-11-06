"""#41 Quota della spesa in prodotti cloud esteri intermediata da rivenditori.
Ingresso: la mappa pubblicata report/metodo/rivenditori-v3.{json,csv} (tools/analisi/rivenditori.py, regole v3,
contratti attuativi 2022-2026, padri di AQ e importi da verificare esclusi). Giurisdizione = quella del PRODOTTO
(config/marchi_cloud.yaml). Canale: diretto (incassa il produttore), rivenditore, ignoto (senza aggiudicatari).
Ricalcola: per giurisdizione, importo per canale; quota rivenditori sul noto; primi rivenditori dei prodotti EXTRA-UE.
Limite: la nazionalità del rivenditore non è nel file (manca il CF): si riporta la quota dei primi 20 per nome,
la giurisdizione del rivenditore resta da verificare sui CF ANAC.

Uso: python tools/verifiche/rivenditori_esteri.py -> esiti/<oggi>/rivenditori/rivenditori-esteri.json"""
import csv, json, os, sys, datetime, collections
from pathlib import Path
import yaml

R = Path(__file__).resolve().parents[2]
NOME = {"AWS": "Amazon Web Services", "Google Cloud": "Google", "Microsoft Azure": "Microsoft", "Oracle Cloud": "Oracle", "IBM Cloud": "IBM"}


def main():
    giur = {NOME.get(m["provider"], m["provider"]): m["giurisdizione"]
            for m in yaml.safe_load(open(R / "config/marchi_cloud.yaml", encoding="utf-8"))}
    giur.setdefault("VMware", "EXTRA-UE")
    d = json.load(open(R / "report/metodo/rivenditori-v3.json", encoding="utf-8"))
    t = collections.defaultdict(collections.Counter)
    for r in d["per_provider_e_canale"]:
        t[giur.get(r["provider"], "?")][r["canale"]] += r["importo"]
    per_giur = {}
    for g, c in sorted(t.items()):
        noto = c["diretto"] + c["rivenditore"]
        per_giur[g] = {**{k: round(v) for k, v in c.items()}, "totale": round(sum(c.values())),
                       "quota_rivenditore_sul_noto": round(c["rivenditore"] / noto, 3) if noto else None}
    # rivenditori dei prodotti EXTRA-UE, dal csv (provider_rivenduti = "P=importo ; ...")
    riv = []
    for r in csv.DictReader(open(R / "report/metodo/rivenditori-v3.csv", encoding="utf-8")):
        est = 0.0; prod = []
        for p in filter(None, (x.strip() for x in r["provider_rivenduti"].split(";"))):
            n, _, v = p.rpartition("=")
            if giur.get(n.strip()) == "EXTRA-UE": est += float(v); prod.append(n.strip())
        if est: riv.append({"rivenditore": r["rivenditore"], "estero_eur": round(est), "prodotti": prod, "contratti": int(r["contratti"])})
    riv.sort(key=lambda x: -x["estero_eur"])
    tot_riv = sum(x["estero_eur"] for x in riv)
    out = {"ingresso": ["report/metodo/rivenditori-v3.json", "report/metodo/rivenditori-v3.csv", "config/marchi_cloud.yaml"],
           "per_giurisdizione_prodotto": per_giur,
           "rivenditori_di_prodotti_extra_ue": len(riv), "importo_extra_ue_via_rivenditori_csv": round(tot_riv),
           "quota_primi_5": round(sum(x["estero_eur"] for x in riv[:5]) / tot_riv, 3) if tot_riv else None,
           "primi_15": riv[:15],
           "esclusi_importi_da_verificare": d["esclusi_importi_da_verificare"],
           "nota": "verificato: ricalcolo dalla mappa v3; la nazionalità dei rivenditori non è misurata (manca il CF)"}
    o = R / f"esiti/{datetime.date.today().isoformat()}/rivenditori"; os.makedirs(o, exist_ok=True)
    json.dump(out, open(o / "rivenditori-esteri.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({k: out[k] for k in ("per_giurisdizione_prodotto", "rivenditori_di_prodotti_extra_ue",
                                           "importo_extra_ue_via_rivenditori_csv", "quota_primi_5")}, indent=1, ensure_ascii=False))
    for x in riv[:10]: print(x["rivenditore"], x["estero_eur"], x["prodotti"][:4])


if __name__ == "__main__":
    main()
