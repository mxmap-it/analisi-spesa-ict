"""Test di tools/acquisizione/at_cig.py (#73, 9/11/2026): fogli di stile, script, font e immagini non sono documenti."""
import sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / "tools/acquisizione"))
import at_cig as A  # noqa: E402


def test_estensioni_scartate():
    for u in ["https://x.it/a/stile.css", "https://x.it/b.min.js?v=3", "https://x.it/f.woff2", "https://x.it/logo.PNG",
              "https://x.it/i.svg", "https://x.it/favicon.ico", "https://x.it/a%20b.jpg"]:
        assert A.non_documento(u), u


def test_documenti_tenuti():
    for u in ["https://x.it/det.pdf", "https://x.it/x.p7m", "https://x.it/getfile?id=3", "https://x.it/allegato.docx",
              "https://x.it/download/123"]:
        assert not A.non_documento(u), u


def test_mime_e_contenuto():
    assert A.non_documento("https://x.it/download?id=1", "text/css; charset=utf-8")
    assert A.non_documento("https://x.it/download?id=1", "image/png")
    assert A.non_documento("https://x.it/download?id=1", "", b"\x89PNG\r\n\x1a\n")
    assert A.non_documento("https://x.it/download?id=1", "", b'@charset "UTF-8"; body{}')
    assert A.non_documento("https://x.it/download?id=1", "", b"!function(e){}")
    assert not A.non_documento("https://x.it/download?id=1", "application/pdf", b"%PDF-1.7")
    assert not A.non_documento("https://x.it/download?id=1", "", b"PK\x03\x04")


def test_filtra():
    orig = A.testa_blob; A.testa_blob = lambda sha: b""
    try:
        t, n = A.filtra_documenti([{"url": "https://x.it/a.pdf", "sha256": "0" * 64}, {"url": "https://x.it/s.css", "sha256": "1" * 64}])
    finally:
        A.testa_blob = orig
    assert n == 1 and [d["url"] for d in t] == ["https://x.it/a.pdf"]


if __name__ == "__main__":  # uso: python tests/test_at_cig_documenti.py (senza pytest)
    for n, f in sorted(globals().items()):
        if n.startswith("test_"):
            f(); print("ok", n)
