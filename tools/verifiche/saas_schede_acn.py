#!/usr/bin/env python3
"""#70 (M9) Infrastruttura dichiarata nelle schede ACN dei SaaS dei fornitori S2 della Misura 1.2. Versione 0.1 (19/11/2026).

Per ogni fornitore S2 (esiti/<ingressi>/pnrr12/pnrr12-dettaglio.csv) prende le sue schede nel CSV ACN dei servizi
qualificati (sha256 8559a074…) e legge le pagine delle schede già archiviate (archivio/mirror/www.acn.gov.it/portale/en/w/
<id>, scaricate con tools/archivia.py --lista: nessuna rete qui). Dal testo della scheda (nome, «Descrizione Generale» …
«Card ID», escluse le «Reti di accesso» che citano i browser) riconosce:
  hyperscaler = AWS/Amazon, Azure, Google Cloud/GCP, Oracle Cloud/OCI, IBM Cloud;
  IT/UE       = IaaS o DC italiani o europei nominati (Aruba, TIM, Fastweb, Retelit, DATA4, Lepida, Nivola/CSI, PSN, Seeweb,
                WIIT, Irideos, Engineering, Dinova, OVH, IaaS qualificata «IA-…»/«IN-…», data center proprietario/di proprietà);
  ignoto      = nessuna delle due.
Attendibilità B (dichiarazione del fornitore ad ACN per la variante qualificata, non per il singolo contratto).
Quota per fornitore = schede su hyperscaler / schede con infrastruttura nota (come le «varianti» di Maggioli in
config/saas_infrastruttura.yaml).
Uso: python3 tools/verifiche/saas_schede_acn.py --ingressi 2026-11-09 --data 2026-11-19 [--primi 45]
Uscite: esiti/<data>/infrastruttura-sottostante/schede-acn.csv, schede-acn.json
"""
import argparse, collections, csv, json, re
from pathlib import Path

R = Path(__file__).resolve().parents[2]
ACN = R / "archivio/blobs/sha256/85/59/8559a074c7484f85608701adec0248841b99370d2fb2db0ab3ffdb5586127c96"
PAG = R / "archivio/mirror/www.acn.gov.it/portale/en/w"
RX_HS = re.compile(r"\baws\b|amazon|azure|google\s+cloud|\bgcp\b|oracle\s+cloud|\boci\b|ibm\s+cloud|microsoft\s+cloud", re.I)
RX_IT = re.compile(r"\baruba\b|\btim\b|telecom\s+italia|fastweb|retelit|data4|lepida|nivola|csi[\s-]+piemonte|polo\s+strategico|\bpsn\b|"
                   r"seeweb|\bwiit\b|irideos|engineering|dinova|\bovh|\b(?:ia|in)-\d+\b|data\s*center\s+(?:proprietari|di\s+propriet|propri)|"
                   r"infrastruttura\s+(?:proprietaria|propria|qualificata)|cloud\s+toscana|liguria\s+digitale|\binsiel\b|trentino\s+digitale", re.I)


def testo(p):
    t = p.read_text(encoding="utf-8", errors="ignore")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    tit = re.search(r"<title>(.*?)</title>", t, re.S)
    t = re.sub(r"<[^>]+>", "\n", t)
    a, b = t.find("Descrizione Generale"), t.find("Card ID")
    corpo = t[a:b] if a >= 0 and b > a else ""
    corpo = re.sub(r"Reti di accesso.*?Servizio di prossimit", " ", corpo, flags=re.S)
    return ((tit.group(1) if tit else "") + "\n" + corpo), bool(corpo)


def main():
    a = argparse.ArgumentParser(); a.add_argument("--ingressi", required=True); a.add_argument("--data", required=True)
    a.add_argument("--primi", type=int, default=45); o = a.parse_args()
    s2 = collections.Counter()
    for r in csv.DictReader(open(R / f"esiti/{o.ingressi}/pnrr12/pnrr12-dettaglio.csv", encoding="utf-8")):
        parts = r["strati"].split(" | "); w = float(r["importo_lotto"] or 0) / len(parts) / 1e6
        for p in parts:
            st, giu, forn = (p.split(":") + ["", ""])[:3]
            if st[:2] == "S2": s2[forn] += w
    acn = collections.defaultdict(list)
    for r in csv.DictReader(open(ACN, encoding="utf-8-sig"), delimiter=";"):
        acn[r["Nome Fornitore"]].append(r)
    righe, per = [], {}
    for forn, meur in s2.most_common(o.primi):
        c = collections.Counter()
        for sc in acn.get(forn, []):
            if sc["Tipologia"] != "SaaS": continue
            p = PAG / sc["Id Scheda"].lower()
            if not p.exists():
                cl, hs, it = "non-archiviata", "", ""
            else:
                t, ok = testo(p)
                hs = "|".join(sorted({" ".join(m.lower().split()) for m in RX_HS.findall(t)})); it = "|".join(sorted({" ".join(m.lower().split()) for m in RX_IT.findall(t)}))
                cl = "hyperscaler" if hs and not it else "misto" if hs and it else "it-ue" if it else ("ignoto" if ok else "pagina-vuota")
            c[cl] += 1
            righe.append({"fornitore": forn, "scheda": sc["Id Scheda"], "nome": sc["Nome"], "classe": cl, "hyperscaler": hs, "it_ue": it})
        noti = c["hyperscaler"] + c["misto"] + c["it-ue"]
        tot = sum(c.values()); hs = c["hyperscaler"] + 0.5 * c["misto"]; ign = tot - noti
        # quota per i fornitori con almeno una scheda che dichiara l'infrastruttura: basso = hs/tutte, alto = (hs+ignote)/tutte,
        # centrale = media dei due (le schede che tacciono possono stare ovunque)
        q = [round(hs / tot, 3), round((2 * hs + ign) / (2 * tot), 3), round((hs + ign) / tot, 3)] if noti else None
        per[forn] = {"meur_s2": round(meur, 2), "schede_saas": tot, **dict(c), "schede_con_infrastruttura": noti, "quota_hyperscaler": q}
    out = R / f"esiti/{o.data}/infrastruttura-sottostante"; out.mkdir(parents=True, exist_ok=True)
    with open(out / "schede-acn.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(righe[0])); w.writeheader(); w.writerows(righe)
    lette = [r for r in righe if r["classe"] not in ("non-archiviata", "pagina-vuota")]
    sintesi = {"schede_saas": len(righe), "lette": len(lette),
               "con_infrastruttura_dichiarata": sum(r["classe"] != "ignoto" for r in lette),
               "su_hyperscaler": sum(r["classe"] in ("hyperscaler", "misto") for r in lette),
               "meur_fornitori_con_prova": round(sum(v["meur_s2"] for v in per.values() if v["quota_hyperscaler"]), 2)}
    json.dump({"versione": "0.1", "ingressi": o.ingressi, "acn_csv_sha256": ACN.name, "sintesi": sintesi, "per_fornitore": per},
              open(out / "schede-acn.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(sintesi)
    for f, v in per.items(): print(f, v)


if __name__ == "__main__":
    main()
