"""Confronta gli esiti di una riesecuzione con quelli pubblicati nel rendiconto ANAC.

Uso: python tools/verifiche/confronta.py esiti/AAAA-MM-GG [prefisso]   (prefisso "cloud/" = solo la misura cloud)
Per ogni numero pubblicato stampa UGUALE o DIVERSO; esce con codice 1 se c'è almeno una differenza.
Le differenze attese quando ANAC ha cambiato i file dopo il 27/10/2026 si riconoscono con
`verifica_anac.sh snapshot`: se gli sha256 coincidono, i numeri devono coincidere."""
import json
import sys
from pathlib import Path

PUBBLICATI = {
    "verifica_ocds_mesi_duplicati.json": "report/anac/verifica-ocds-mesi-duplicati-2026-10-27.json",
    "verifica_38_42.json": "report/anac/verifica-38-42-2026-10-27.json",
    "verifica_cig_accordo_quadro.json": "report/anac/verifica-cig-accordo-quadro-2026-10-27.json",
    "integrita-completo.json": "report/anac/integrita-completo-2026-10-27.json",
    "seconde_vie.json": "report/anac/seconde-vie-2026-10-27.json",
    # misura cloud (tools/misura_cloud.sh)
    "cloud/attribuzione-riepilogo.json": "report/metodo/attribuzione-riepilogo-v3.json",
    "cloud/rivenditori.json": "report/metodo/rivenditori-v3.json",
    "cloud/pnrr-cloud.json": "report/metodo/pnrr-cloud-v3.json",
}
IGNORA = {"generato", "esempi", "nota", "regole"}  # data di esecuzione ed esempi illustrativi non sono numeri del rendiconto


def numeri(x, via=""):
    """Appiattisce un JSON in coppie (percorso, valore) per i soli numeri e stringhe brevi."""
    if isinstance(x, dict):
        if "id" in x and "dataset" in x:  # controllo di integrità: chiave stabile
            via = f"{via}/{x['dataset']}:{x['id']}"
            x = {k: v for k, v in x.items() if k not in ("id", "dataset")}
        for k, v in x.items():
            if k not in IGNORA:
                yield from numeri(v, f"{via}/{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from numeri(v, f"{via}[{i}]")
    elif isinstance(x, (int, float)) and not isinstance(x, bool):
        yield via, x


def main() -> int:
    esiti = Path(sys.argv[1])
    diverse = uguali = 0
    prefisso = sys.argv[2] if len(sys.argv) > 2 else ""
    for nome, pubblicato in PUBBLICATI.items():
        if not nome.startswith(prefisso): continue
        nuovo = esiti / nome
        if not nuovo.exists():
            print(f"MANCA     {nome}: verifica non eseguita")
            diverse += 1
            continue
        a = dict(numeri(json.loads(Path(pubblicato).read_text(encoding="utf-8"))))
        b = dict(numeri(json.loads(nuovo.read_text(encoding="utf-8"))))
        for k in sorted(set(a) | set(b)):
            if a.get(k) == b.get(k):
                uguali += 1
            else:
                diverse += 1
                print(f"DIVERSO   {nome}{k}: pubblicato {a.get(k)}  ora {b.get(k)}")
        print(f"verificato {nome}")
    print(f"\n{uguali} numeri uguali, {diverse} diversi")
    return 1 if diverse else 0


if __name__ == "__main__":
    raise SystemExit(main())
