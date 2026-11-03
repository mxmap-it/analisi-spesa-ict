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




# --- catalogo delle problematiche (README §Catalogo): un test per voce ---
import diagnosi  # noqa: E402


def test_cat_waf_cloudflare():
    r = diagnosi.riconosci_blocco(403, {"Server": "cloudflare", "cf-mitigated": "challenge", "cf-ray": "x"}, "<title>Just a moment...</title>", [])
    assert "Cloudflare challenge" in r["vendor_blocco"] and "Cloudflare" in r["cdn"] and r["challenge_js"]


def test_cat_waf_akamai():
    corpo = "<HTML><HEAD><TITLE>Access Denied</TITLE></HEAD><BODY>You don't have permission ... Reference&#32;#18.abc"
    r = diagnosi.riconosci_blocco(403, {"Server": "AkamaiGHost"}, corpo, [])
    assert "Akamai" in r["vendor_blocco"] and "Akamai" in r["cdn"]


def test_cat_waf_imperva_f5_azure_aws():
    assert "Imperva/Incapsula" in diagnosi.riconosci_blocco(200, {"X-Iinfo": "1"}, "", [])["vendor_blocco"]
    assert "F5 BIG-IP ASM" in diagnosi.riconosci_blocco(200, {}, "The requested URL was rejected. Please consult with your administrator.", [])["vendor_blocco"]
    assert "Azure Application Gateway/Front Door" in diagnosi.riconosci_blocco(403, {}, "<center>Microsoft-Azure-Application-Gateway/v2</center>", [])["vendor_blocco"]
    assert "AWS WAF" in diagnosi.riconosci_blocco(405, {}, "<script>window.awsWafCookieDomainList=[];aws-waf-token</script>", [])["vendor_blocco"]


def test_cat_captcha():
    r = diagnosi.riconosci_blocco(403, {}, '<div class="g-recaptcha" data-sitekey="x"></div>', [])
    assert r["captcha"]


def test_cat_cdn_da_dns():
    assert "Akamai" in diagnosi.riconosci_blocco(200, {}, "", ["www.ente.it.edgekey.net"])["cdn"]


def test_cat_tls():
    assert diagnosi.tipo_errore_tls("verifica: unable to get local issuer certificate (20)") == "catena incompleta o CA sconosciuta"
    assert diagnosi.tipo_errore_tls("verifica: certificate has expired (10)") == "certificato scaduto"
    assert diagnosi.tipo_errore_tls("verifica: Hostname mismatch, certificate is not valid for 'x' (62)") == "nome non corrispondente"
    assert diagnosi.tipo_errore_tls("verifica: self-signed certificate (18)") == "certificato autofirmato"


def test_cat_robots_intero_sito():
    g = robots.analizza("User-agent: *\nDisallow: /\n")
    assert not robots.consentito(g, "Googlebot", "/amministrazione-trasparente/")[0]


def test_cat_ricercabilita():
    assert diagnosi.classifica_ricerca({}, {}) == "ricerca assente"
    assert diagnosi.classifica_ricerca({"trovato": True}, {"trovato": True}) == "trovato"
    assert diagnosi.classifica_ricerca({"trovato": False}, {"trovato": True}) == "non trovato"
    assert diagnosi.classifica_ricerca({"trovato": False}, {"trovato": False}) == "ricerca non funzionante"


def test_cat_sezione_non_individuata_e_url_anac_rotto():
    assert sonda.link_at('<a href="/news">Notizie</a>', "https://x.it/") == ""
    assert deriva_at("  https://www.ente.it/doc/dataset.xml  ") == ("", "")
    assert deriva_at("ftp://x") == ("", "")


import tassonomia  # noqa: E402


def _t(identita, status, giro=1, ts="2026-11-03T20:00:00Z", origine="server", **k):
    return {"identita": identita, "status": status, "giro_conferma": giro, "ts": ts, "origine": origine, "errore": k.get("errore", ""),
            "vendor_blocco": k.get("vendor", []), "challenge_js": k.get("js", False), "captcha": k.get("captcha", False),
            "transitorio": k.get("transitorio", False)}


def test_cat_waf_per_user_agent_confermato():
    srv = [_t("bot-progetto", 403), _t("python-requests", 403), _t("browser-reale", 200),
           _t("bot-progetto", 403, 2, "2026-11-03T22:00:00Z"), _t("browser-reale", 200, 2, "2026-11-03T22:00:00Z")]
    x = tassonomia.classifica(srv, [], [])
    assert "WAF per User-Agent/identità" in x["meccanismi"] and x["conferma"] == "confermato"


def test_cat_waf_per_ip_datacenter():
    srv = [_t("bot-progetto", 403), _t("browser-reale", 403)]
    dsk = [_t("bot-progetto", 200, origine="desktop"), _t("browser-reale", 200, origine="desktop")]
    assert "WAF per IP/ASN (datacenter)" in tassonomia.classifica(srv, dsk, [])["meccanismi"]


def test_cat_blocco_non_riprodotto_e_transitorio():
    srv = [_t("bot-progetto", 403), _t("bot-progetto", 200, 2, "2026-11-03T22:00:00Z")]
    assert tassonomia.classifica(srv, [], [])["conferma"] == "non riprodotto"
    srv = [_t("bot-progetto", None, errore="ReadTimeout: timed out", transitorio=True)]
    assert "errore transitorio" in tassonomia.classifica(srv, [], [])["meccanismi"]


def test_cat_robots_per_identita():
    neg = tassonomia.robots_negati("User-agent: GPTBot\nDisallow: /\n\nUser-agent: *\nAllow: /\n", "/amministrazione-trasparente/")
    assert neg == ["GPTBot"]
    assert "robots.txt (solo crawler AI o altri client)" in tassonomia.classifica([], [], neg)["meccanismi"]
    neg = tassonomia.robots_negati("User-agent: *\nDisallow: /\n", "/x")
    assert "Googlebot" in neg and "robots.txt (motori di ricerca)" in tassonomia.classifica([], [], neg)["meccanismi"]



def test_cat_accesso_negato_a_tutti_e_interferenza():
    srv = [_t("bot-progetto", 403), _t("browser-reale", 403)]
    dsk = [_t("bot-progetto", 403, origine="desktop"), _t("browser-reale", 403, origine="desktop")]
    assert "nessun client accettato (blocco totale o sito guasto)" in tassonomia.classifica(srv, dsk, [])["meccanismi"]
    assert diagnosi.riconosci_blocco(200, {}, "<title>Web Protection by Bitdefender</title>", [])["interferenza_locale"]
    dsk = [dict(_t("browser-reale", 200, origine="desktop"), interferenza_locale=True)]
    assert "WAF per IP/ASN (datacenter)" not in tassonomia.classifica(srv, dsk, [])["meccanismi"]


if __name__ == "__main__":
    for k, f in list(globals().items()):
        if k.startswith("test_"):
            f()
            print("ok", k)
