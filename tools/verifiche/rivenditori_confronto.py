"""#41 Confronto fra due versioni della mappa rivenditori (es. v4.3 -> v4.5): CIG ed euro per marchio, quote, enti.

Legge solo le uscite di rivenditori_mappa.py (cig-rivenditore-<v>.csv, mappa-<v>.json); leggero.
Uso: python tools/verifiche/rivenditori_confronto.py v4.3 v4.5 [esiti/2026-11-09/rivenditori] [v4.2 ...]
-> <cartella>/confronto-<a>-<b>.json
Enti = stazioni appaltanti con almeno un CIG di prodotto extra-UE comprato via rivenditore (definizione del dato
«2.182 enti» v4.2; la verifica lo riproduce per ogni versione passata).
"""
import csv, json, sys
from collections import defaultdict
from pathlib import Path

R = Path(__file__).resolve().parents[2]
A, B = sys.argv[1], sys.argv[2]
D = R / (sys.argv[3] if len(sys.argv) > 3 else "esiti/2026-11-09/rivenditori")
ALTRE = sys.argv[4:]


def carica(v):
    marchi = defaultdict(lambda: [set(), 0.0]); enti = defaultdict(float); cig = set()
    for r in csv.DictReader(open(D / f"cig-rivenditore-{v}.csv", encoding="utf-8")):
        cig.add(r["cig"])
        m = marchi[r["provider"]]; m[0].add(r["cig"]); m[1] += float(r["quota_eur"] or 0)
        if r["giurisdizione_prodotto"] == "EXTRA-UE":
            enti[r["ente"]] += float(r["quota_eur"] or 0)
    j = json.load(open(D / f"mappa-{v}.json", encoding="utf-8"))
    return dict(marchi=marchi, enti=enti, cig=cig, j=j)


def sintesi(v, d):
    e = d["j"]["extra_ue"]
    top = sorted(d["enti"].items(), key=lambda x: -x[1])[:10]
    return dict(cig_rivenditore=len(d["cig"]), rivenditori=d["j"].get("rivenditori"),
                rivenditori_con_prodotti_extra_ue=d["j"].get("rivenditori_con_prodotti_extra_ue"),
                extra_ue_totale=e["totale"], extra_ue_noto=e["noto"], via_rivenditore=e["via_rivenditore"],
                cf_it=e["via_rivenditore_cf_it"], quota_cf_it_totale=e["quota_cf_it_sul_totale"],
                quota_cf_it_noto=e["quota_cf_it_sul_noto"], quota_capogruppo_it=e["quota_cf_it_capogruppo_it_sul_totale"],
                capogruppo=e["per_naz_cf_e_capogruppo"],
                enti_extra_ue=len(d["enti"]), enti_top10=[(n, round(x)) for n, x in top])


def main():
    da, db = carica(A), carica(B)
    marchi = []
    for k in sorted(set(da["marchi"]) | set(db["marchi"])):
        ca, ea = da["marchi"].get(k, [set(), 0.0]); cb, eb = db["marchi"].get(k, [set(), 0.0])
        if ca == cb and abs(ea - eb) < 1: continue
        marchi.append(dict(marchio=k, cig_a=len(ca), cig_b=len(cb), entrano=len(cb - ca), escono=len(ca - cb),
                           eur_a=round(ea), eur_b=round(eb), delta_eur=round(eb - ea)))
    marchi.sort(key=lambda x: -abs(x["delta_eur"]))
    ris = dict(versioni=[A, B], A=sintesi(A, da), B=sintesi(B, db), marchi_cambiati=marchi,
               cig_entrano=len(db["cig"] - da["cig"]), cig_escono=len(da["cig"] - db["cig"]),
               enti_entrano=len(set(db["enti"]) - set(da["enti"])), enti_escono=len(set(da["enti"]) - set(db["enti"])),
               altre={v: dict(enti_extra_ue=len(carica(v)["enti"])) for v in ALTRE})
    json.dump(ris, open(D / f"confronto-{A}-{B}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(ris, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
