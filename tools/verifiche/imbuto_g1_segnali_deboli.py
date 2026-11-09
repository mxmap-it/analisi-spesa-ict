"""#71/#44 Revisione dei CIG G1 nuovi del perimetro 0.3.3 (RX_ICT con «sw» e «connettività») e misura di una correzione
proposta (NON applicata all'imbuto ufficiale).

Proposta P1: un CIG entra in S6 per il solo testo se RX_ICT trova almeno un segnale forte; se i soli segnali sono
«deboli» (connettività, sw) e il CPV è di una divisione non ICT di beni/lavori (33 apparecchi medici, 38 strumenti e
contatori, 41-45 lavori, 73 ricerca e sviluppo) il CIG resta fuori. I CPV di telecomunicazione (64) e ICT (30, 32, 48,
50.3, 72) non sono toccati, quindi la connettività vera (SPC, Infratel, E-Distribuzione) resta dentro.

Uso (anche in locale, legge solo un csv piccolo):
  python tools/verifiche/imbuto_g1_segnali_deboli.py [esiti/2026-11-09/imbuto-prova]
-> <cartella>/g1-revisione.csv, g1-revisione.json
"""
import csv, json, re, sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools" / "analisi"))
from imbuto import RX_ICT  # noqa: E402

D = R / (sys.argv[1] if len(sys.argv) > 1 else "esiti/2026-11-09/imbuto-prova")
DEBOLI = {"sw", "connettivita", "connettività"}
CPV_NON_ICT = ("33", "38", "41", "42", "43", "44", "45", "73")

# revisione a mano (9/11/2026) degli 11 CIG delle multiutility: True = acquisto ICT, False = falso positivo
MANO = {
    "BA88CF13AB": (True, "E-Distribuzione: connettività IP per telecontrollo impianti (servizio TLC, Wind)"),
    "B8DF534749": (True, "E-Distribuzione: gara connettività lotto 1 (servizio TLC)"),
    "B9168D69AE": (True, "E-Distribuzione: gara connettività lotto 1 (servizio TLC; doppione di B8DF534749?)"),
    "B9168D9C27": (True, "E-Distribuzione: gara connettività lotto 4 (servizio TLC)"),
    "B8DF5379C2": (True, "E-Distribuzione: gara connettività lotto 4 (servizio TLC; doppione di B9168D9C27?)"),
    "BA31D50B15": (True, "E-Distribuzione: connettività M2M (SIM dati, Wind)"),
    "B711AF0074": (True, "A2A Smart City: apparati di rete Cisco (hardware di rete)"),
    "B007E8276A": (False, "Padania Acque: contatori acqua smart meter NB-IoT, fornitura e posa"),
    "B009C6D7D2": (False, "Padania Acque: contatori acqua smart meter NB-IoT, fornitura e posa"),
    "B0A6E2176C": (False, "Sorical: lavori di riduzione perdite rete idrica (PNRR M2C4), CPV 41110000"),
    "BBCCABCA46": (False, "Sorical: fornitura e installazione contatori intelligenti con connettività"),
}


def norm(s):
    return s.lower().replace("à", "a")


def main():
    righe = list(csv.DictReader(open(D / "g1-nuovi.csv", encoding="utf-8")))
    out, tot = [], {}
    for r in righe:
        segn = {norm(m.group(0)) for m in RX_ICT.finditer(r["testo"])}
        solo_deboli = bool(segn) and all(re.sub(r"\W", "", s) in {"sw", "connettivita"} or s.startswith("connettivit") for s in segn)
        cpv = r["cod_cpv"][:2]
        esce = solo_deboli and cpv.startswith(CPV_NON_ICT)
        mano = MANO.get(r["cig"])
        o = dict(anno=r["anno"], cig=r["cig"], importo=r["importo"], cod_cpv=r["cod_cpv"], ente=r["stazione_appaltante"],
                 segnali="|".join(sorted(segn)), solo_deboli=int(solo_deboli), p1_esce=int(esce),
                 mano_ict="" if mano is None else int(mano[0]), mano_nota="" if mano is None else mano[1])
        out.append(o)
        for k in ("tutti", "dal_2024") if int(r["anno"]) >= 2024 else ("tutti",):
            t = tot.setdefault(k, dict(cig=0, euro=0.0, p1_esce_cig=0, p1_esce_euro=0.0))
            t["cig"] += 1; t["euro"] += float(r["importo"])
            if esce: t["p1_esce_cig"] += 1; t["p1_esce_euro"] += float(r["importo"])
    rev = [o for o in out if o["mano_ict"] != ""]
    conf = dict(
        rivisti=len(rev),
        falsi_mano=sum(1 for o in rev if o["mano_ict"] == 0),
        falsi_mano_euro=sum(float(o["importo"]) for o in rev if o["mano_ict"] == 0),
        p1_falsi_tolti=sum(1 for o in rev if o["mano_ict"] == 0 and o["p1_esce"]),
        p1_veri_persi=sum(1 for o in rev if o["mano_ict"] == 1 and o["p1_esce"]),
    )
    with open(D / "g1-revisione.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
    ris = dict(totali=tot, revisione_multiutility=conf,
               p1_esce=[(o["cig"], o["anno"], o["cod_cpv"], o["ente"], float(o["importo"])) for o in out if o["p1_esce"]])
    json.dump(ris, open(D / "g1-revisione.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(ris, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
