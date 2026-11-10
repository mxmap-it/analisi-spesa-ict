"""Test di tools/archivia.py: --url da solo e riconoscimento delle pagine di blocco (#43, 9/11/2026)."""
import subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / "tools"))
import archivia as A  # noqa: E402


def _f(tmp_path, testo):
    p = tmp_path / "x.part"; p.write_text(testo, encoding="utf-8"); return p


def test_file_atteso_html_resta_errore(tmp_path):
    p = _f(tmp_path, "<html><body>ok</body></html>")
    assert A.html_rifiutato("https://dati.anticorruzione.it/opendata/download/x.zip", 200, {}, p)
    assert A.html_rifiutato("https://example.it/a/b.csv", 200, {}, p)


def test_pagina_legittima_accettata(tmp_path):
    p = _f(tmp_path, "<html><head><title>Data center</title></head><body>" + "Cornaredo Retelit " * 2000 + "</body></html>")
    assert A.html_rifiutato("https://www.maggioli.com/en-us/cloud-solutions-pa-data-center", 200,
                            {"Content-Type": "text/html"}, p) is None


def test_pagina_di_blocco_rifiutata(tmp_path):
    p = _f(tmp_path, "<html><title>Just a moment...</title><script>window._cf_chl_opt={}</script>"
                     "Checking your browser before accessing. Attention Required! | Cloudflare</html>")
    m = A.html_rifiutato("https://example.it/pagina", 403, {"Server": "cloudflare", "cf-mitigated": "challenge"}, p)
    assert m and m.startswith("pagina di blocco")


def test_url_da_solo_non_da_errore():
    r = subprocess.run([sys.executable, str(R / "tools/archivia.py"), "--url", "x"], capture_output=True, text=True,
                       env={"ARCHIVIO_ROOT": "/nonexistent-archivio-test", "PATH": "/usr/bin"})
    assert "nessun URL" not in r.stderr


def _vista(tmp_path, url, testo):
    A.ROOT = tmp_path  # senza pytest: niente monkeypatch
    b = tmp_path / "blob" / testo; b.parent.mkdir(parents=True, exist_ok=True); b.write_text(testo)
    return A.collega_vista(b, A.percorso_mirror(url))


def test_prefisso_prima_il_corto(tmp_path):  # #12: c'è un file dove servirebbe una cartella
    a = _vista(tmp_path, "https://h.it/x/connect", "A")
    b = _vista(tmp_path, "https://h.it/x/connect/pagina", "B")
    assert a == tmp_path / "mirror/h.it/x/connect" and a.read_text() == "A"
    assert b == tmp_path / "mirror/h.it/x/connect__d/pagina" and b.read_text() == "B"
    assert _vista(tmp_path, "https://h.it/x/connect/pagina", "B2") == b  # deterministico


def test_prefisso_prima_il_lungo(tmp_path):  # #12: c'è una cartella dove servirebbe un file
    b = _vista(tmp_path, "https://h.it/x/connect/pagina", "B")
    a = _vista(tmp_path, "https://h.it/x/connect", "A")
    assert b == tmp_path / "mirror/h.it/x/connect/pagina" and b.read_text() == "B"
    assert a == tmp_path / "mirror/h.it/x/connect/__index__" and a.read_text() == "A"
    assert _vista(tmp_path, "https://h.it/x/connect/", "C") == a  # URL con «/» finale


def test_senza_collisione_percorso_naturale(tmp_path):  # retrocompatibilità
    assert _vista(tmp_path, "https://h.it/a/b.csv", "A") == tmp_path / "mirror/h.it/a/b.csv"


if __name__ == "__main__":  # uso: python tests/test_archivia.py (senza pytest)
    import tempfile
    for n, f in sorted(globals().items()):
        if n.startswith("test_"):
            f(*([Path(tempfile.mkdtemp(dir=R / "lavoro"))] if f.__code__.co_argcount else [])); print("ok", n)
