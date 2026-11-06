"""#43 PNRR cloud: quanta parte dei contratti collegati alle Misure 1.1 e 1.2 va a prodotti delle big tech USA.
Ingresso: report/metodo/pnrr-contratti-v3.csv (catena PA Digitale 2026 candidature_finanziate_11/12 -> CUP ->
dataset ANAC cup -> CIG -> attribuzione v3 per prodotto). Padri di AQ e importi da verificare esclusi dal totale
(contati a parte). Big tech USA = stessa lista di tools/analisi/rivenditori.py + VMware (Broadcom).
Avvertenza: importo_lotto dei CIG collegati al CUP, non l'importo PNRR finanziato (un CUP può avere CIG anche
fuori dal finanziamento, e una parte dei CUP non ha CIG): è la spesa contrattuale collegata, non la quota del fondo.

Uso: python tools/verifiche/pnrr_bigtech.py -> esiti/<oggi>/pnrr/pnrr-bigtech.json"""
import csv, json, os, datetime, collections
from pathlib import Path

R = Path(__file__).resolve().parents[2]
BIGTECH = {"Microsoft", "Amazon Web Services", "Google", "Oracle", "IBM", "Salesforce", "ServiceNow", "Adobe", "Zoom",
           "Cisco Webex", "Cloudera", "VMware"}


def main():
    csv.field_size_limit(10 ** 7)
    m = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for r in csv.DictReader(open(R / "report/metodo/pnrr-contratti-v3.csv", encoding="utf-8")):
        imp = float(r["importo_lotto"] or 0)
        x = m[r["misura"]]
        if r["e_padre"] == "1" or r["importo_da_verificare"]:
            x["esclusi"]["n"] += 1; x["esclusi"]["eur"] += imp; continue
        g = "bigtech_usa" if r["provider"] in BIGTECH else (r["giurisdizione"] or "senza_provider")
        x[g]["n"] += 1; x[g]["eur"] += imp
        x["tot"]["n"] += 1; x["tot"]["eur"] += imp
        if r["provider"] in BIGTECH: x["bt_provider"][r["provider"]] += imp; x["bt_canale"][r["canale"]] += imp
    out = {}
    for mis, x in sorted(m.items()):
        tot = x["tot"]["eur"]
        att = tot - x["senza_provider"]["eur"]
        out[mis] = {"cig": x["tot"]["n"], "importo": round(tot),
                    **{g: {"cig": x[g]["n"], "importo": round(x[g]["eur"])} for g in ("bigtech_usa", "EXTRA-UE", "UE", "IT", "senza_provider")},
                    "quota_bigtech_sul_totale": round(x["bigtech_usa"]["eur"] / tot, 4) if tot else None,
                    "quota_bigtech_sul_attribuito": round(x["bigtech_usa"]["eur"] / att, 4) if att else None,
                    "bigtech_per_provider": {k: round(v) for k, v in x["bt_provider"].most_common()},
                    "bigtech_per_canale": {k: round(v) for k, v in x["bt_canale"].items()},
                    "esclusi_padri_o_da_verificare": {"cig": x["esclusi"]["n"], "importo": round(x["esclusi"]["eur"])}}
    o = R / f"esiti/{datetime.date.today().isoformat()}/pnrr"; os.makedirs(o, exist_ok=True)
    json.dump({"ingresso": "report/metodo/pnrr-contratti-v3.csv", "misure": out}, open(o / "pnrr-bigtech.json", "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
