#!/usr/bin/env python3
"""Copia report/metodo/bdncp-e-l190-inventario.md (#74) nella pagina del sito sito/content/rendiconti/bdncp-l190.md:
tiene il front matter e la riga di provenienza della pagina, sostituisce il resto con il rendiconto senza il titolo.
Da rilanciare a ogni nuova versione del rendiconto, poi build Hugo."""
from pathlib import Path

R = Path(__file__).resolve().parents[1]
P = R / "sito/content/rendiconti/bdncp-l190.md"
pag = P.read_text(encoding="utf-8")
testa = pag[:pag.index("\n", pag.index("ticket [#74]")) + 1]
src = (R / "report/metodo/bdncp-e-l190-inventario.md").read_text(encoding="utf-8").split("\n")
P.write_text(testa + "\n" + "\n".join(src[1:]).lstrip("\n"), encoding="utf-8")
print("scritto", P)
