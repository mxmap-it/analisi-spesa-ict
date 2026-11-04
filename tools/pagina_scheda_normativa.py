"""Pubblica la scheda normativa del #63 come pagina del sito: unica fonte report/metodo/accessibilita-documenti-normativa.md."""
import re
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
SORGENTE = RADICE / "report/metodo/accessibilita-documenti-normativa.md"
DESTINAZIONE = RADICE / "sito/content/progetto/normativa-documenti-gara.md"
GITHUB = "https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/metodo/"

testo = SORGENTE.read_text(encoding="utf-8")
righe = testo.split("\n")
titolo = righe[0].lstrip("# ").strip()
corpo = "\n".join(righe[1:]).lstrip("\n")
# i collegamenti relativi del repo puntano ai file su GitHub
corpo = re.sub(r"\]\((?!https?://|#|/)([^)]+)\)", lambda m: f"]({GITHUB}{m.group(1)})", corpo)
DESTINAZIONE.write_text(
    "---\n"
    f'title: "{titolo}"\n'
    "date: 2026-11-04\n"
    'description: "Norme violate quando il link ai documenti di gara manca o non porta ai documenti, chi ne risponde, chi vigila, giurisprudenza e rimedi."\n'
    "weight: 20\n"
    "---\n\n"
    "<!-- Generata da tools/pagina_scheda_normativa.py: si modifica la sorgente, non questa pagina. -->\n\n"
    + corpo,
    encoding="utf-8",
)
