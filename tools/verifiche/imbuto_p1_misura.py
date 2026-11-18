#!/usr/bin/env python3
"""#71 Misura della proposta P1 su TUTTO il residuo S6 dell'imbuto 0.3.4 (NON applicata all'imbuto ufficiale).

P1 (vedi imbuto_g1_segnali_deboli.py, dove è stata misurata sui soli 59 G1 nuovi): un CIG che entra nell'imbuto per il
solo testo (CPV non ICT, sottoclasse «cpv-non-ict-testo-ict») resta fuori se i segnali RX_ICT trovati nel testo sono
tutti «deboli» (connettività, sw) e il CPV è di una divisione non ICT di beni o lavori (33, 38, 41-45, 73).

Variante P1r (18/11, dal giudizio del campione): solo CPV 33, 38, 73 (le divisioni 41-45 contengono anche
installazioni telefoniche e lavori di rete dati, che sono ICT). Si misura accanto a P1.
I giudizi a mano del campione (colonne `giudizio` = non-ict / ict / dubbio e `nota`) sono in GIUDIZI qui sotto,
non nel csv: il csv si rigenera con i giudizi e la precisione per variante si calcola da lì.

Uscite (esiti/<data>/imbuto/): p1-misura.json (totali per periodo e gruppo, segnali, CPV) e p1-campione.csv
(40 CIG che P1 toglierebbe, dal 2024, estratti con sha256(cig + seme): da giudicare a mano, colonna `giudizio`).
Lettura in streaming di lavoro/imbuto/ict.csv (una riga per CIG nella 0.3.4): poca memoria.
Uso (sul server): nice .venv/bin/python tools/verifiche/imbuto_p1_misura.py [AAAA-MM-GG]
"""
import collections, csv, hashlib, json, re, sys
from datetime import date
from pathlib import Path

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools" / "analisi"))
from imbuto import RX_ICT  # noqa: E402

ICT = R / "lavoro/imbuto/ict.csv"
CPV_NON_ICT = ("33", "38", "41", "42", "43", "44", "45", "73")
CPV_P1R = ("33", "38", "73")
# giudizio a mano (Claude, 18/11/2026, sul testo ANAC): non-ict = P1 fa bene a togliere; ict = acquisto ICT perso; dubbio
GIUDIZI = {
    "B60F0DD7A5": ("non-ict", "ASI, payload iperspettrale PRISMA (hardware spaziale)"),
    "B3EBDBE34D": ("dubbio", "Areti, sistemi TLC delle cabine elettriche (telecontrollo della rete, OT)"),
    "B3EBDBF420": ("dubbio", "Areti, sistemi TLC delle cabine elettriche, lotto 2"),
    "B427784774": ("non-ict", "isola ecologica e cassonetti intelligenti"),
    "BBF43D9075": ("non-ict", "contatori smart NB-IoT"),
    "B9BF1E9BDE": ("non-ict", "ASI, missione picosatelliti"),
    "BB910FDBE4": ("non-ict", "lavori su area pubblica, «connettività» non informatica"),
    "B363479BE0": ("non-ict", "colonna endoscopica (apparecchio medico)"),
    "B6A63FCA0B": ("non-ict", "smart meter"),
    "B798436071": ("dubbio", "Areti, connettività degli apparati di media/bassa tensione (telecontrollo)"),
    "B70F8DC12E": ("non-ict", "software di una TAC (apparecchio medico)"),
    "B43277152A": ("ict", "moduli software Terranova (gestionale utility)"),
    "B00E8B4A02": ("non-ict", "noleggio apparecchiature di laboratorio con software"),
    "BC9AEEB016": ("non-ict", "connettività della rete ecologica"),
    "BB170FA20A": ("ict", "Comune, acquisto HW e SW (bando Risorse in comune)"),
    "B5EA30EDEC": ("ict", "adesione AQ Regione Toscana-TIM, connettività della rete telematica regionale"),
    "B950D618BC": ("non-ict", "moduli software di un mammografo"),
    "B436742EDF": ("non-ict", "software di TAC"),
    "B3771C100E": ("non-ict", "controllore di processo di un depuratore (OT)"),
    "B526149F5F": ("non-ict", "software di TAC"),
    "B3F3EB60F8": ("non-ict", "aggiornamento di un ecografo"),
    "B4DE142088": ("non-ict", "microscopio"),
    "B4659CFBAD": ("non-ict", "software e telecamera di un microscopio"),
    "B788C14C6A": ("non-ict", "sistemi di misura della dose"),
    "B936C7283A": ("ict", "moduli software Terranova (gestionale utility)"),
    "BB01F6090A": ("ict", "Comune, fornitura HW e SW (bando Risorse in comune)"),
    "B4588299CB": ("non-ict", "software di strumenti di laboratorio"),
    "B724431DAB": ("non-ict", "software di un sistema di pneumologia"),
    "B542D93713": ("ict", "servizio Smarticloud di telefonia e connettività"),
    "BCBBFEFECA": ("non-ict", "comunicatore per CAA (ausilio)"),
    "B4A1A76D0E": ("non-ict", "titolatore di laboratorio"),
    "B44341A9BC": ("non-ict", "sistema di acquisizione per microscopio"),
    "BA5E655217": ("non-ict", "comunicatore per CAA (ausilio)"),
    "B53989C913": ("non-ict", "comunicatore per CAA (ausilio)"),
    "B3021BA783": ("non-ict", "software di contornamento per radioterapia (dispositivo medico)"),
    "B5DE355702": ("non-ict", "contatori d'acqua NB-IoT"),
    "B3FA679173": ("ict", "centralino VoIP con connettività"),
    "BC6F5EC22A": ("non-ict", "contenitori di quarzo"),
    "B5C7381C69": ("non-ict", "comunicatore per CAA (ausilio)"),
    "B5B9A4DE89": ("ict", "linee telefoniche e connettività dati di una scuola"),
}
SEME = "p1-20261118"
N_CAMPIONE = 40
csv.field_size_limit(1 << 30)


def norm(s):
    return re.sub(r"\W", "", s.lower().replace("à", "a"))


def debole(s):
    return s == "sw" or s.startswith("connettivit")


def main():
    data = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
    out = R / f"esiti/{data}/imbuto"; out.mkdir(parents=True, exist_ok=True)
    tot = collections.defaultdict(lambda: [0, 0.0]); esce = collections.defaultdict(lambda: [0, 0.0])
    esce_r = collections.defaultdict(lambda: [0, 0.0])
    cpv_esce = collections.Counter(); segn_esce = collections.Counter(); cand = []
    for r in csv.DictReader(open(ICT, encoding="utf-8")):
        if r["strato"] != "S6-residuo": continue
        per = "dal-2024" if int(r["anno"]) >= 2024 else "2020-2023"
        g = (r["gruppo"] or "")[:2]; imp = float(r["importo"] or 0)
        for k in ((per, "tutti"), (per, g)):
            tot[k][0] += 1; tot[k][1] += imp
        if r["sottoclasse"] != "cpv-non-ict-testo-ict": continue
        segn = {norm(m.group(0)) for m in RX_ICT.finditer(r["testo"])}
        if not (segn and all(debole(s) for s in segn) and r["cod_cpv"][:2].startswith(CPV_NON_ICT)): continue
        for k in ((per, "tutti"), (per, g)):
            esce[k][0] += 1; esce[k][1] += imp
            if r["cod_cpv"][:2] in CPV_P1R: esce_r[k][0] += 1; esce_r[k][1] += imp
        if per == "dal-2024":
            cpv_esce[r["cod_cpv"][:2]] += 1; segn_esce["|".join(sorted(segn))] += 1
            cand.append({"cig": r["cig"], "anno": r["anno"], "gruppo": r["gruppo"], "importo": imp, "cod_cpv": r["cod_cpv"],
                         "segnali": "|".join(sorted(segn)), "ente": r["stazione_appaltante"], "testo": r["testo"][:300]})
    cam = sorted(cand, key=lambda x: hashlib.sha256((x["cig"] + SEME).encode()).hexdigest())[:N_CAMPIONE]
    with open(out / "p1-campione.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(cam[0]) + ["giudizio", "nota"] if cam else ["cig"]); w.writeheader()
        for x in sorted(cam, key=lambda x: -x["importo"]):
            g, n = GIUDIZI.get(x["cig"], ("", "")); w.writerow(dict(x, giudizio=g, nota=n))
    prec = {}
    for nome, sel in (("P1", lambda x: True), ("P1r", lambda x: x["cod_cpv"][:2] in CPV_P1R)):
        c = collections.Counter(GIUDIZI.get(x["cig"], ("non-giudicato",))[0] for x in cam if sel(x))
        prec[nome] = {"campione": sum(c.values()), "giudizi": dict(c),
                      "euro_ict_persi": round(sum(x["importo"] for x in cam if sel(x) and GIUDIZI.get(x["cig"], ("",))[0] == "ict"))}
    J = {"data": data, "imbuto": "0.3.4", "regola": "P1: solo segnali deboli (connettività, sw) e CPV 33/38/41-45/73 -> fuori",
         "ict_csv_sha256": hashlib.sha256(open(ICT, "rb").read()).hexdigest(),
         "s6": [{"periodo": k[0], "gruppo": k[1], "cig": v[0], "euro": round(v[1]), "p1_esce_cig": esce[k][0], "p1_esce_euro": round(esce[k][1]),
                "p1r_esce_cig": esce_r[k][0], "p1r_esce_euro": round(esce_r[k][1])}
                for k, v in sorted(tot.items())],
         "dal_2024_cpv_divisione": dict(cpv_esce.most_common()), "dal_2024_segnali": dict(segn_esce.most_common(10)),
         "campione": {"seme": SEME, "n": len(cam), "file": f"esiti/{data}/imbuto/p1-campione.csv", "precisione": prec}}
    json.dump(J, open(out / "p1-misura.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(J, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
