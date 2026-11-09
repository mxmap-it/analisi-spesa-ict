"""Il registro delle raccomandazioni deve avere tutti i campi obbligatori (tools/raccomandazioni_pagina.py)."""
import importlib.util
from pathlib import Path

_P = Path(__file__).resolve().parent.parent / "tools/raccomandazioni_pagina.py"
_spec = importlib.util.spec_from_file_location("raccomandazioni_pagina", _P)
rp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rp)


def test_registro_completo():
    errori, _ = rp.controlla(rp.carica())
    assert errori == [], "\n".join(errori)


def test_voce_incompleta_fallisce():
    errori, _ = rp.controlla([{"id": "R01", "destinatario": "ANAC", "stato": "verificato"}])
    assert any("evidenza" in e for e in errori)
    assert any("titolo" in e for e in errori) and True


def test_id_duplicato_fallisce():
    v = {"id": "R01", "destinatario": "ANAC", "tipo": "difetto", "stato": "proposta", "titolo": "t",
         "richiesta": "r", "rif": ["#1"], "prova": "tools/x.py"}
    errori, _ = rp.controlla([v, dict(v)])
    assert any("duplicato" in e for e in errori)
