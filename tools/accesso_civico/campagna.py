#!/usr/bin/env python3
"""Entità CAMPAGNA dell'accesso civico (#58, versione 0.1, 9/11/2026). NESSUN INVIO.

Una campagna (`spesaict.accesso-civico-campagna/1`, schemi/accesso-civico-campagna.schema.json) raccoglie scopo,
perimetro, criteri di selezione, parametri e modelli (con sha256) di un insieme di richieste. File in
config/accesso-civico/campagne/<id>.json. Stati: proposta -> approvata -> attiva -> in-pausa -> chiusa; ogni cambio
oltre «proposta» richiede una decisione di Fabio in DECISIONI.md (campo `approvata`).

Funzioni:
- carica(id_o_percorso) -> dict validato (controlli minimi senza dipendenze: campi, stato, sha256 dei modelli);
- parametri(c, base) -> parametri effettivi: quelli della campagna sovrascrivono parametri.yaml;
- verifica_modelli(c) -> elenco di discrepanze fra sha256 registrati e file attuali (vuoto = ok);
- aggiorna_sha_modelli(c) -> campagna con sha256 ricalcolati (solo per campagne in stato «proposta»).

Uso: campagna.py verifica <id> | campagna.py sha <id>  (sha riscrive gli sha256 dei modelli, solo se «proposta»)
"""
import hashlib
import json
import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]
DIR = R / "config/accesso-civico/campagne"
FORMATO = "spesaict.accesso-civico-campagna/1"
STATI = ["proposta", "approvata", "attiva", "in-pausa", "chiusa"]
TRANSIZIONI = {"proposta": {"approvata", "chiusa"}, "approvata": {"attiva", "chiusa"},
               "attiva": {"in-pausa", "chiusa"}, "in-pausa": {"attiva", "chiusa"}, "chiusa": set()}
OBBLIGATORI = ["formato", "id", "titolo", "scopo", "progetto", "responsabile", "perimetro", "selezione", "parametri",
               "modelli", "template", "licenza_dati", "stato", "creata"]
ID = re.compile(r"^cmp-[0-9a-z-]+$")


class ErroreCampagna(ValueError):
    pass


def sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def percorso(ident):
    p = Path(ident)
    if p.suffix == ".json" and p.exists():
        return p
    return DIR / f"{ident}.json"


def valida(c):
    manca = [k for k in OBBLIGATORI if k not in c]
    if manca:
        raise ErroreCampagna(f"campagna {c.get('id')}: mancano {manca}")
    if c["formato"] != FORMATO:
        raise ErroreCampagna(f"formato {c['formato']} diverso da {FORMATO}")
    if not ID.match(c["id"]):
        raise ErroreCampagna(f"id non valido: {c['id']}")
    if c["stato"] not in STATI:
        raise ErroreCampagna(f"stato non valido: {c['stato']}")
    if c["stato"] != "proposta" and not (c.get("approvata") or {}).get("decisione"):
        raise ErroreCampagna(f"{c['id']}: stato {c['stato']} senza riferimento alla decisione di Fabio (approvata.decisione)")
    if "istanza" not in c["modelli"]:
        raise ErroreCampagna(f"{c['id']}: manca il modello «istanza»")
    for nome, m in c["modelli"].items():
        if not {"path", "sha256", "versione"} <= set(m):
            raise ErroreCampagna(f"{c['id']}: modello {nome} senza path/sha256/versione")
    return c


def carica(ident):
    return valida(json.loads(percorso(ident).read_text(encoding="utf-8")))


def verifica_modelli(c, radice=R):
    err = []
    for nome, m in c["modelli"].items():
        f = radice / m["path"]
        if not f.exists():
            err.append(f"{nome}: file mancante {m['path']}")
        elif sha_file(f) != m["sha256"]:
            err.append(f"{nome}: sha256 cambiato ({m['path']})")
    return err


def aggiorna_sha_modelli(c, radice=R):
    if c["stato"] != "proposta":
        raise ErroreCampagna(f"{c['id']}: modelli bloccati (stato {c['stato']}); serve una nuova versione della campagna")
    for m in c["modelli"].values():
        m["sha256"] = sha_file(radice / m["path"])
    return c


def parametri(c, base=None):
    """Parametri effettivi: copia di parametri.yaml con le chiavi della campagna sovrapposte."""
    p = json.loads(json.dumps(base or {}))
    cp = c.get("parametri", {})
    if "tetto_voci" in cp:
        p["tetto_voci_per_richiesta"] = cp["tetto_voci"]
    pec = p.setdefault("pec", {})
    for k_c, k_p in (("tetto_pec_giorno", "tetto_giorno"), ("intervallo_secondi", "intervallo_secondi")):
        if k_c in cp:
            pec[k_p] = cp[k_c]
    if "sollecito_dopo" in cp:
        p.setdefault("termini", {})["sollecito_dopo"] = cp["sollecito_dopo"]
    p["campagna"] = c["id"]
    return p


def cambia_stato(c, nuovo, decisione=None):
    if nuovo not in TRANSIZIONI[c["stato"]]:
        raise ErroreCampagna(f"{c['id']}: {c['stato']} -> {nuovo} non ammesso")
    if nuovo != "chiusa" and not decisione:
        raise ErroreCampagna(f"{c['id']}: {nuovo} richiede il riferimento a una decisione di Fabio in DECISIONI.md")
    c = dict(c, stato=nuovo)
    if nuovo == "approvata":
        c["approvata"] = {"decisione": decisione}
    return valida(c)


def main():
    cmd, ident = sys.argv[1], sys.argv[2]
    c = carica(ident)
    if cmd == "verifica":
        err = verifica_modelli(c)
        print(json.dumps({"id": c["id"], "stato": c["stato"], "errori": err}, ensure_ascii=False))
        sys.exit(1 if err else 0)
    if cmd == "sha":
        c = aggiorna_sha_modelli(c)
        percorso(ident).write_text(json.dumps(c, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("sha256 dei modelli aggiornati")


if __name__ == "__main__":
    main()
