"""Test minimi (pytest o `python test_trasparenza.py`). Nessun accesso alla rete."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import piattaforme  # noqa: E402
import robots  # noqa: E402
import sonda  # noqa: E402
from censimento import campione_stratificato  # noqa: E402
from fonti import deriva_at, regione_da_istat  # noqa: E402

ROBOTS = """
User-agent: *
Disallow: /amministrazione-trasparente/
Allow: /amministrazione-trasparente/bandi
Disallow: /*.pdf$

User-agent: Googlebot
User-agent: Bingbot
Disallow:
"""


def test_robots_lunghezza_e_gruppi():
    g = robots.analizza(ROBOTS)
    assert robots.consentito(g, "*", "/amministrazione-trasparente/")[0] is False
    assert robots.consentito(g, "*", "/amministrazione-trasparente/bandi-di-gara")[0] is True
    assert robots.consentito(g, "*", "/a/b.pdf")[0] is False
    assert robots.consentito(g, "*", "/a/b.pdf?x")[0] is True
    assert robots.consentito(g, "Googlebot", "/amministrazione-trasparente/")[0] is True
    assert robots.consentito(g, "bingbot", "/amministrazione-trasparente/")[0] is True


def test_robots_vuoto():
    assert robots.consentito(robots.analizza(""), "*", "/x")[0] is True


def test_deriva_at():
    assert deriva_at("https://www.comuneweb.it/egov/Palagonia/ammTrasparente/Bandi_di_gara_e_contratti/anac.2021.xml") == \
        ("https://www.comuneweb.it/egov/Palagonia/ammTrasparente/", "anac-l190-prefisso")
    assert deriva_at("https://x.portaletrasparenza.net/l190.xml")[1] == "anac-l190-host-trasparenza"
    assert deriva_at("https://www.leserre.org/avcpweb/xmldir/avcp-2021.xml") == ("", "")
    assert deriva_at("  https://www.x.it/trasparenza.xml") == ("", "")
    assert deriva_at("non un url") == ("", "")
    assert deriva_at("http://www.halleyweb.com/c058083/zf/index.php/dataset/appalti-2020.xml") == (
        "http://www.halleyweb.com/c058083/zf/index.php/trasparenza/index/index", "anac-l190-regola-zf")


def test_regione():
    assert regione_da_istat("058091") == "Lazio"
    assert regione_da_istat("15146") == "Lombardia"
    assert regione_da_istat("") == ""


def test_piattaforme():
    assert piattaforme.riconosci("comune.portaletrasparenza.net", "", {})["piattaforma"].startswith("DigitalPA")
    assert piattaforme.riconosci("www.x.it", '<meta name="generator" content="WordPress 6.5">', {})["piattaforma"] == "WordPress"
    assert piattaforme.riconosci("www.x.it", "<html>nulla</html>", {})["piattaforma"] == "ignota"
    # un link a padigitale2026 non è una piattaforma
    assert piattaforme.riconosci("www.x.it", '<a href="https://padigitale2026.gov.it">', {})["piattaforma"] == "ignota"


def test_firme_e_noindex():
    assert "Cloudflare challenge" in sonda.firme(403, {"cf-mitigated": "challenge"}, "")
    assert "Imperva/Incapsula" in sonda.firme(200, {}, "<script src=/_Incapsula_Resource?x>")
    assert sonda.firme(200, {}, "<html>" + "x" * 50000 + "</html>") == []
    assert sonda.noindex({"X-Robots-Tag": "noindex"}, "")
    assert sonda.noindex({}, '<meta name="robots" content="noindex, nofollow">')
    assert not sonda.noindex({}, '<meta name="robots" content="index, follow">')


def test_link_at():
    html = '<a href="/menu">Menu</a><a href="/it/amministrazione-trasparente">Amministrazione Trasparente</a>'
    assert sonda.link_at(html, "https://www.x.it/") == "https://www.x.it/it/amministrazione-trasparente"


def test_campione_stratificato():
    righe = [{"cf": str(i), "categoria": "C" if i % 3 else "P", "tipologia": "", "regione": "R%d" % (i % 4)} for i in range(100)]
    s = campione_stratificato(righe, 10)
    assert len(s) == 10 and len({(r["categoria"], r["regione"]) for r in s}) == 8
    assert [r["cf"] for r in s] == [r["cf"] for r in campione_stratificato(righe, 10)]


if __name__ == "__main__":
    for k, f in list(globals().items()):
        if k.startswith("test_"):
            f()
            print("ok", k)
