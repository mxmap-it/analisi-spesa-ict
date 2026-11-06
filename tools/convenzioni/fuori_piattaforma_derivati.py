"""#62 fuori piattaforma, passo 1: CIG derivati (cig_accordo_quadro) dei CIG padre delle iniziative con righe di criticità 3
in documenti-mancanti.csv, uniti al link «documenti di gara» della PVL (lavoro/pvl/cig_link.csv).
Uscita: lavoro/convenzioni/fuori-piattaforma/derivati.csv (iniziativa,padre,cig,anno,ente,cf_ente,importo,oggetto,link,dominio).
Input copiati in lavoro/convenzioni/fuori-piattaforma/input/ (il clone del server non è allineato). Ripartibile: se l'uscita esiste non rifà nulla. Uso (server): nice python tools/convenzioni/fuori_piattaforma_derivati.py"""
import csv, glob, os, sys
from pathlib import Path

R = Path(__file__).resolve().parent.parent.parent
L = R / "lavoro/convenzioni/fuori-piattaforma"
csv.field_size_limit(10**9)


def main():
    L.mkdir(parents=True, exist_ok=True)
    out = L / "derivati.csv"
    if out.exists():
        print("già fatto", out); return
    inz = {r["iniziativa"] for r in csv.DictReader(open(L / "input/documenti-mancanti.csv", encoding="utf-8")) if r["criticita"] == "3"}
    padri = {}
    for r in csv.DictReader(open(L / "input/lotti.csv", encoding="utf-8")):
        if r["iniziativa"] in inz:
            padri[r["cig_padre"]] = r["iniziativa"]
    for i in inz:
        if i.startswith("cig-"):
            padri.setdefault(i[4:], i)
    print(len(inz), "iniziative,", len(padri), "padri", flush=True)
    der = {}
    for f in sorted(glob.glob(str(R / "lavoro/cig_completo/*.csv"))):
        b = os.path.basename(f)
        if not (b.startswith("2026") or any(f"_{a}_" in b for a in ("2022", "2023", "2024", "2025", "2026"))):
            continue
        with open(f, encoding="utf-8", errors="replace") as fh:
            for r in csv.DictReader(fh, delimiter=";"):
                aq = (r.get("cig_accordo_quadro") or "").strip()
                if aq in padri and r["cig"] not in der:
                    der[r["cig"]] = {"iniziativa": padri[aq], "padre": aq, "cig": r["cig"], "anno": r.get("anno_pubblicazione", ""),
                                     "ente": r.get("denominazione_amministrazione_appaltante", ""), "cf_ente": r.get("cf_amministrazione_appaltante", ""),
                                     "importo": r.get("importo_lotto", ""), "oggetto": (r.get("oggetto_lotto") or r.get("oggetto_gara") or "")[:200]}
        print(b, len(der), flush=True)
    link = {}
    with open(R / "lavoro/pvl/cig_link.csv", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["cig"] in der and r["link"]:
                link[r["cig"]] = (r["link"], r["dominio"])
    campi = ["iniziativa", "padre", "cig", "anno", "ente", "cf_ente", "importo", "oggetto", "link", "dominio"]
    with open(str(out) + ".part", "w", newline="", encoding="utf-8") as fo:
        w = csv.DictWriter(fo, fieldnames=campi); w.writeheader()
        for c, d in der.items():
            d["link"], d["dominio"] = link.get(c, ("", ""))
            w.writerow(d)
    os.replace(str(out) + ".part", out)
    print("derivati", len(der), "con link", len(link))


if __name__ == "__main__":
    main()
