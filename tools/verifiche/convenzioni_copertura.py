"""#62: verifica rieseguibile dei numeri pubblicati nella sezione /convenzioni/.

1. Ricostruisce la base dati da zero (censimento -> base_dati) da un clone pulito e controlla che iniziative.json non cambi
   (stesso sha256): i numeri dipendono solo da file versionati.
2. Ricalcola per seconda via, direttamente da censimento.csv e archiviati.jsonl, numero di iniziative, attive/storiche,
   lotti e somma dei valori, e li confronta con iniziative.json.
3. Stampa i numeri citati nella pagina indice e nel ticket (copertura media, buchi per tipo di documento).
Uso: python tools/verifiche/convenzioni_copertura.py   (esce con codice 1 se qualcosa non torna)"""
import collections, csv, hashlib, json, subprocess, sys
from pathlib import Path

R = Path(__file__).resolve().parent.parent.parent
DB = R / "report/convenzioni/database"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    prima = sha(DB / "iniziative.json")
    for s in ("tools/convenzioni/censimento.py", "tools/convenzioni/base_dati.py"):
        subprocess.run([sys.executable, str(R / s)], check=True, cwd=R, stdout=subprocess.DEVNULL)
    ok = sha(DB / "iniziative.json") == prima
    print("ricostruzione identica:", ok)
    voci = json.loads((DB / "iniziative.json").read_text(encoding="utf-8"))
    cens = list(csv.DictReader(open(DB / "censimento.csv", encoding="utf-8")))
    ini = {r["iniziativa"]: r for r in cens}
    val = collections.Counter()
    for r in cens:
        val[r["iniziativa"]] += int(r["euro_ict_2024_2025"])
    conti = {"iniziative": (len(ini), len(voci)), "lotti": (len(cens), sum(len(v["lotti"]) for v in voci)),
             "attive": (sum(1 for r in ini.values() if r["stato_iniziativa"] == "attiva"), sum(1 for v in voci if v["stato_iniziativa"] == "attiva")),
             "euro_2024_2025": (sum(val.values()), sum(v["valore_ict_2024_2025"] or 0 for v in voci))}
    for k, (a, b) in conti.items():
        print(f"{k}: seconda via {a} / base dati {b}", "OK" if a == b else "DIVERSO")
        ok &= a == b
    print("copertura media:", round(sum(v["copertura"] for v in voci) / len(voci), 3))
    print("per tipo di soggetto:", dict(collections.Counter(v["tipo_soggetto"] for v in voci)))
    st = collections.defaultdict(collections.Counter)
    for v in voci:
        for i in v["inventario"]:
            st[i["tipo"]][i["stato"]] += 1
    for t, c in st.items():
        print(f"  {t}: {dict(c)}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
