#!/usr/bin/env python3
"""#52 #71 Verifica per CIG della classe «in-house» dell'imbuto dal 2024 (versione 0.1, 19/11/2026).

Ingressi: lavoro/imbuto/ict.csv (imbuto 0.3.4), esiti/*/imbuto/bdncp/segnali.csv (livello B2: aggiudicatario contro
Indice PA), esiti/*/imbuto/tetti-cig-v2.csv, config/inhouse_verifica.yaml (decisioni per CIG con fonti sha256).

Che cosa fa:
1. applica le decisioni per CIG verificate sugli atti (config `cig`);
2. sposta le adesioni al Sistema Cloud Toscana da «in-house» a «cloud certo IT» (decisione di Fabio del 29/10/2026);
   sopra la soglia, per enti diversi da Regione Toscana, Comune di Firenze ed ESTAR, l'importo dell'adesione si conta 0 finché l'atto non dà il valore (probabile massimale copiato);
3. divide il resto della classe in: affidamenti a società in-house pubbliche (B2 «ipa»), acquisti fatti DALLE in-house
   (stazione appaltante = società in-house: infrastruttura propria), altro (aggiudicatario privato o senza aggiudicatario).

Uscite in esiti/<data>/imbuto/inhouse-verifica/:
  spostamenti-inhouse.csv  (cig, livello, da, a, giurisdizione, importo, motivo, fonte), letto da imbuto_spostamenti.py come MAN;
  riepilogo.json           (prima/dopo in M€, lordo e netto dei tetti).
Uso: python3 tools/verifiche/inhouse_verifica.py [AAAA-MM-GG]
"""
import collections, csv, glob, json, os, re, sys
from datetime import date

import yaml

VERSIONE = "0.1"
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GIORNO = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
OUT = os.path.join(R, "esiti", GIORNO, "imbuto", "inhouse-verifica")
csv.field_size_limit(10**9)
INHOUSE_SA = re.compile(r"LEPIDA|CINECA|CONSORZIO PER IL SISTEMA INFOR|CSI[\s-]+PIEMONTE|LIGURIA DIGITALE|\bINVA\b|"
                        r"TRENTINO DIGITALE|INSIEL|SOGEI|AZIENDA REGIONALE PER L.?INNOVA|\bARIA\b|PASUBIO TECNOLOGIA|"
                        r"LAZIOCREA|SORESA|INNOVAPUGLIA|SARDEGNA IT|ACI INFORMATICA|SILFI")
SCT_RTI = re.compile(r"TIM|TELECOM|ENTERPRISE SERVICES|KYNDRYL|IBM|LUTECH|DEDALUS|T\.A\.I\.|ENGINEERING|NET7|ELITE")


def ultimo(pat):
    f = sorted(glob.glob(os.path.join(R, pat)))
    return f[-1] if f else None


def main():
    cfg = yaml.safe_load(open(os.path.join(R, "config/inhouse_verifica.yaml"), encoding="utf-8"))
    f_seg, f_tet = ultimo("esiti/*/imbuto/bdncp/segnali.csv"), ultimo("esiti/*/imbuto/tetti-cig-v2.csv")
    seg = {r["cig"]: r for r in csv.DictReader(open(f_seg, encoding="utf-8")) if r["sottoclasse"] == "in-house"}
    tet = {r["cig"]: float(r["euro_netti"]) for r in csv.DictReader(open(f_tet, encoding="utf-8"))}
    rows = {}
    for x in csv.DictReader(open(os.path.join(R, "lavoro/imbuto/ict.csv"), encoding="utf-8")):
        if x["anno"] >= "2024" and x["sottoclasse"] == "in-house":
            rows[x["cig"]] = x
    rx_sct = re.compile(cfg["sct"]["regex"])
    soglia = cfg["sct"]["soglia_importo_da_verificare"]
    fonte_sct = "; ".join(f"{f['url']} sha256 {f.get('sha256', '')[:12]}" for f in cfg["sct"]["fonti"])
    sp, classi = [], collections.defaultdict(lambda: [0, 0.0, 0.0])
    for cig, x in sorted(rows.items()):
        imp = float(x["importo"] or 0)
        netto = tet.get(cig, imp)
        b2 = seg.get(cig, {}).get("b2", "")
        da = f"{x['strato']}/in-house (inhouse-certo)"
        if cig in cfg["cig"]:
            d = cfg["cig"][cig]
            nuovo = imp if d.get("importo") in ("", None) else float(d["importo"])
            fonti = "; ".join(f"{f['url']} sha256 {f.get('sha256', '')[:12]}" for f in d["fonti"])
            sp.append([cig, "MAN", da, d["a"], d.get("giurisdizione", ""), nuovo, " ".join(d["motivo"].split())[:400], fonti])
            k = "verificato-" + d["a"]
        elif rx_sct.search(x["testo"]) and b2 != "ipa":
            agg = x["aggiudicatari"].upper()
            incoerente = bool(agg) and not SCT_RTI.search(agg)
            grande = x["stazione_appaltante"].upper() in ("REGIONE TOSCANA", "COMUNE DI FIRENZE", "ESTAR")
            if imp >= soglia and not grande:
                nuovo = 0.0
                mot = (f"Adesione al Sistema Cloud Toscana: cloud sovrano IT (decisione 29/10/2026), non in-house. Importo "
                       f"{imp/1e6:.2f} M€ da verificare (probabile massimale del contratto quadro, 40 M€ di adesioni in tutto)"
                       + ("; aggiudicatario ANAC non del RTI SCT" if incoerente else "") + ": contato 0 finché l'atto non dà il valore")
                k = "sct-importo-da-verificare"
            else:
                nuovo = imp
                mot = "Adesione al Sistema Cloud Toscana: cloud sovrano IT (decisione di Fabio 29/10/2026), non in-house"
                k = "sct-cloud-it"
            sp.append([cig, "MAN", da, "cloud-certo", "IT", nuovo, mot, fonte_sct])
        elif b2 == "ipa":
            k, nuovo = "affidamento-a-inhouse-ipa", imp
        elif INHOUSE_SA.search(x["stazione_appaltante"].upper()):
            k, nuovo = "acquisto-della-inhouse-infrastruttura-propria", imp
        else:
            k, nuovo = "altro-" + (b2 or "senza-b2"), imp
        c = classi[k]
        c[0] += 1; c[1] += imp; c[2] += nuovo if cig in cfg["cig"] or k.startswith("sct") else netto
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "spostamenti-inhouse.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["cig", "livello", "da", "a", "giurisdizione", "importo", "motivo", "fonte"])
        for s in sp:
            w.writerow(s[:5] + [f"{s[5]:.2f}"] + s[6:])
    tot = [len(rows), sum(float(x["importo"] or 0) for x in rows.values()), sum(tet.get(c, float(x["importo"] or 0)) for c, x in rows.items())]
    out = {"versione": VERSIONE, "data": GIORNO, "nota": "M€; lordo = importo del lotto; corretto = importo dopo la verifica (netto dei tetti v2 per le classi non toccate)",
           "ingressi": {"ict": "lavoro/imbuto/ict.csv", "segnali": os.path.relpath(f_seg, R), "tetti": os.path.relpath(f_tet, R),
                        "config": "config/inhouse_verifica.yaml"},
           "classe_inhouse_dal_2024": {"cig": tot[0], "lordo": round(tot[1] / 1e6, 1), "netto_tetti": round(tot[2] / 1e6, 1)},
           "classi": {k: {"cig": v[0], "lordo": round(v[1] / 1e6, 1), "corretto": round(v[2] / 1e6, 1)} for k, v in sorted(classi.items(), key=lambda a: -a[1][1])},
           "spostamenti": len(sp)}
    json.dump(out, open(os.path.join(OUT, "riepilogo.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
