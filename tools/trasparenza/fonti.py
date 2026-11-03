"""Fonte degli URL: registro ANAC L. 190/2012 art. 1 c. 32 + IndicePA + anagrafica ANAC.

1. ANAC, «Registro comunicazioni Art.1 comma 32 L.190/2012» (dati.anticorruzione.it/#/l190,
   API rest/legge190/ricerca). Ogni ente comunica via PEC l'URL del file XML dei contratti,
   pubblicato nella sezione «Amministrazione trasparente» > Bandi di gara e contratti.
   ANAC registra anche l'esito del suo ultimo tentativo di accesso a quell'URL.
2. IndicePA (CKAN JSON, risorsa «enti»): codice IPA, sito istituzionale, categoria, PEC, comune ISTAT.
3. Anagrafica ANAC stazioni appaltanti (mirror locale): natura giuridica e comune per chi non è in IPA.

Chiave: codice fiscale dell'ente. Ogni pagina scaricata è archiviata con sha256.
"""
from __future__ import annotations

import csv
import io
import json
import re
import time
import zipfile
from urllib.parse import urlsplit, urlunsplit

import requests

from comune import ARCHIVIO, LAVORO, UA_ANAC, adesso, connetti, jdump, salva_blob

L190 = "https://dati.anticorruzione.it/rest/legge190"
IPA = "https://indicepa.gov.it/ipa-dati/api/3/action/datastore_search"
IPA_ENTI = "d09adf99-dc10-4349-8c53-27b1e5aa97b6"
IPA_CATEGORIE = "84ebb2e7-0e61-427b-a1dd-ab8bb2a84f07"  # datastore JSON della risorsa categorie
SA_ZIP = ARCHIVIO / "mirror/dati.anticorruzione.it/opendata/download/dataset/stazioni-appaltanti/filesystem/stazioni-appaltanti_csv.zip"

# Codice ISTAT della provincia (prime 3 cifre del comune) -> regione.
_REG = {
    "Piemonte": [1, 2, 3, 4, 5, 6, 96, 103], "Valle d'Aosta": [7], "Liguria": [8, 9, 10, 11],
    "Lombardia": [12, 13, 14, 15, 16, 17, 18, 19, 20, 97, 98, 108],
    "Trentino-Alto Adige": [21, 22], "Veneto": [23, 24, 25, 26, 27, 28, 29],
    "Friuli-Venezia Giulia": [30, 31, 32, 93], "Emilia-Romagna": [33, 34, 35, 36, 37, 38, 39, 40, 99],
    "Marche": [41, 42, 43, 44, 109], "Toscana": [45, 46, 47, 48, 49, 50, 51, 52, 53, 100],
    "Umbria": [54, 55], "Lazio": [56, 57, 58, 59, 60], "Campania": [61, 62, 63, 64, 65],
    "Abruzzo": [66, 67, 68, 69], "Molise": [70, 94], "Puglia": [71, 72, 73, 74, 75, 110],
    "Basilicata": [76, 77], "Calabria": [78, 79, 80, 101, 102],
    "Sicilia": [81, 82, 83, 84, 85, 86, 87, 88, 89],
    "Sardegna": [90, 91, 92, 95, 104, 105, 106, 107, 111],
}
PROV_REGIONE = {p: r for r, ps in _REG.items() for p in ps}


def regione_da_istat(cod: str | None) -> str:
    if not cod or not str(cod).strip().isdigit():
        return ""
    c = str(cod).strip().zfill(6)
    return PROV_REGIONE.get(int(c[-6:-3]), "")


def deriva_at(url: str | None) -> tuple[str, str]:
    """URL della sezione AT dal file XML L.190: prefisso fino al segmento che contiene «trasparen».

    Restituisce (url, regola). Se nessun segmento lo contiene, ("", "") e si passa alla scoperta
    dalla home page.
    """
    if not url:
        return "", ""
    u = url.strip()
    if not re.match(r"^https?://", u, re.I):
        return "", ""
    p = urlsplit(u)
    segs = p.path.split("/")
    for i, s in enumerate(segs):
        if re.search(r"trasparen", s, re.I) and not re.search(r"\.(xml|php|aspx?|jsp)$", s, re.I):
            return urlunsplit((p.scheme.lower(), p.netloc.lower(), "/".join(segs[: i + 1]) + "/", "", "")), "anac-l190-prefisso"
    m = re.match(r"^(.*?/zf/index.php/)", p.path)
    if m:  # schema di URL dei portali con «/zf/index.php/» (Halley): la sezione è trasparenza/index/index
        return urlunsplit((p.scheme.lower(), p.netloc.lower(), m.group(1) + "trasparenza/index/index", "", "")), "anac-l190-regola-zf"
    if re.search(r"trasparen", p.netloc, re.I):  # host dedicato (trasparenza.ente.it, *.portaletrasparenza.net)
        return urlunsplit((p.scheme.lower(), p.netloc.lower(), "/", "", "")), "anac-l190-host-trasparenza"
    return "", ""


def _get(sess, url):
    for t in range(4):
        try:
            r = sess.get(url, timeout=120)
            if r.status_code == 200:
                return r
        except requests.RequestException:
            pass
        time.sleep(10 * (t + 1))
    raise RuntimeError(f"fonte non raggiungibile: {url}")


def _registra(c, url, dati: bytes, nota: str):
    sha = salva_blob(dati)
    c.execute("INSERT INTO fonti_scaricate VALUES(?,?,?,?,?)", (url, adesso(), sha, len(dati), nota))
    return sha


def scarica_l190(c, sess) -> dict[str, dict]:
    cache = LAVORO / f"l190-{adesso()[:10]}.json"  # stesso giorno: non si riscarica
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    anni = sess.get(f"{L190}/anni", timeout=60).json()
    _registra(c, f"{L190}/anni", jdump(anni).encode(), "anni disponibili")
    per_cf: dict[str, dict] = {}
    for anno in sorted(anni, key=int):  # l'anno più recente sovrascrive i precedenti
        start, tot = 0, None
        while tot is None or start < tot:
            url = f"{L190}/ricerca?start={start}&max=1000"
            r = sess.post(url, json={"anno": str(anno)}, timeout=180)
            r.raise_for_status()
            _registra(c, f"{url}#anno={anno}", r.content, f"registro L190 anno {anno}")
            d = r.json()
            tot = d["paging"]["itemsCount"]
            for x in d["result"]:
                cf = (x.get("codiceFiscale") or "").strip().upper()
                if not cf:
                    continue
                prec = per_cf.get(cf)
                # Si tiene l'URL più recente; a parità di anno si preferisce un esito «successo».
                if prec and prec["anno"] == anno and prec["esito"] == "successo" and x.get("esitoUltimoTentativoAccessoUrl") != "successo":
                    continue
                per_cf[cf] = {"url": (x.get("url") or "").strip(), "anno": anno,
                              "esito": x.get("esitoUltimoTentativoAccessoUrl") or "",
                              "denominazione": x.get("ragioneSociale") or ""}
            start += 1000
            time.sleep(2)
        c.commit()
    cache.write_text(jdump(per_cf), encoding="utf-8")
    return per_cf


def scarica_ipa(c, sess) -> tuple[list[dict], dict]:
    cat = {}
    r = _get(sess, f"{IPA}?resource_id={IPA_CATEGORIE}&limit=1000")
    _registra(c, r.url, r.content, "IndicePA categorie")
    for x in r.json()["result"]["records"]:
        cat[x.get("Codice_categoria") or x.get("Codice_Categoria")] = x.get("Nome_categoria") or x.get("Descrizione_categoria") or ""
    enti, off = [], 0
    while True:
        r = _get(sess, f"{IPA}?resource_id={IPA_ENTI}&limit=5000&offset={off}")
        _registra(c, r.url, r.content, "IndicePA enti")
        rec = r.json()["result"]["records"]
        enti += rec
        if len(rec) < 5000:
            break
        off += 5000
    return enti, cat


def anagrafica_anac() -> dict[str, dict]:
    out = {}
    if not SA_ZIP.exists():
        return out
    with zipfile.ZipFile(SA_ZIP) as z, z.open(z.namelist()[0]) as fh:
        for row in csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"), delimiter=";"):
            if row.get("stato") != "ATTIVO":
                continue
            out[row["codice_fiscale"].strip().upper()] = {
                "natura": row.get("natura_giuridica_descrizione", ""),
                "regione": regione_da_istat(row.get("citta_codice"))}
    return out


def normalizza_sito(s: str | None) -> str:
    s = (s or "").strip()
    if not s:
        return ""
    if not re.match(r"^https?://", s, re.I):
        s = "https://" + s
    return s


def costruisci() -> int:
    c = connetti()
    sess = requests.Session()
    sess.headers["User-Agent"] = UA_ANAC
    l190 = scarica_l190(c, sess)
    ipa, cat = scarica_ipa(c, sess)
    ana = anagrafica_anac()
    righe: dict[str, dict] = {}
    for e in ipa:
        cf = (e.get("Codice_fiscale_ente") or "").strip().upper()
        if not cf:
            continue
        righe[cf] = {"cf": cf, "ipa": e.get("Codice_IPA"), "denominazione": e.get("Denominazione_ente"),
                     "tipologia": e.get("Tipologia") or "", "categoria": cat.get(e.get("Codice_Categoria"), e.get("Codice_Categoria") or ""),
                     "regione": regione_da_istat(e.get("Codice_comune_ISTAT")),
                     "sito_ipa": normalizza_sito(e.get("Sito_istituzionale")),
                     "pec_ipa": e.get("Mail1") if (e.get("Tipo_Mail1") or "").lower() == "pec" else "",
                     "fonti": ["indicepa"]}
    for cf, x in l190.items():
        r = righe.setdefault(cf, {"cf": cf, "ipa": "", "denominazione": x["denominazione"], "tipologia": "non in IndicePA",
                                  "categoria": ana.get(cf, {}).get("natura", ""), "regione": ana.get(cf, {}).get("regione", ""),
                                  "sito_ipa": "", "pec_ipa": "", "fonti": []})
        r.update(url_l190=x["url"], anno_l190=x["anno"], esito_anac=x["esito"])
        r["fonti"].append("anac-l190")
    for r in righe.values():
        at, prov = deriva_at(r.get("url_l190"))
        if not r["regione"]:
            r["regione"] = ana.get(r["cf"], {}).get("regione", "")
        c.execute("""INSERT INTO enti VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
          ON CONFLICT(cf) DO UPDATE SET ipa=excluded.ipa, denominazione=excluded.denominazione,
          tipologia=excluded.tipologia, categoria=excluded.categoria, regione=excluded.regione,
          sito_ipa=excluded.sito_ipa, pec_ipa=excluded.pec_ipa, url_l190=excluded.url_l190,
          anno_l190=excluded.anno_l190, esito_anac=excluded.esito_anac, at_url=excluded.at_url,
          at_provenienza=excluded.at_provenienza, fonti=excluded.fonti""",
                  (r["cf"], r["ipa"], r["denominazione"], r["tipologia"], r["categoria"], r["regione"],
                   r["sito_ipa"], r["pec_ipa"], r.get("url_l190", ""), r.get("anno_l190", ""), r.get("esito_anac", ""),
                   at, prov, ",".join(r["fonti"])))
    c.commit()
    n = c.execute("SELECT count(*), sum(url_l190<>''), sum(at_url<>''), sum(sito_ipa<>'') FROM enti").fetchone()
    print(json.dumps({"enti": n[0], "con_url_l190": n[1], "at_da_l190": n[2], "con_sito_ipa": n[3]}))
    return 0


CIG_DIR = ARCHIVIO / "mirror/dati.anticorruzione.it/opendata/download/dataset"


def indice_cig(anni=("2024", "2025"), soglia=40000.0) -> int:
    """Un CIG di test per ente, dai file CIG ANAC archiviati: il più recente con importo del lotto >= soglia
    (atto atteso in AT > Bandi di gara e contratti), altrimenti il più recente. Lettura in streaming."""
    c = connetti()
    cfs = {r[0] for r in c.execute("SELECT cf FROM enti")}
    migliore: dict[str, tuple] = {}
    for anno in anni:
        for z in sorted((CIG_DIR / f"cig-{anno}" / "filesystem").glob("cig_csv_*.zip")):
            with zipfile.ZipFile(z) as zz, zz.open(zz.namelist()[0]) as fh:
                for row in csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"), delimiter=";"):
                    cf = (row.get("cf_amministrazione_appaltante") or "").strip().upper()
                    if cf not in cfs or row.get("COD_MOTIVO_CANCELLAZIONE"):
                        continue
                    try:
                        imp = float((row.get("importo_lotto") or "0").replace(",", "."))
                    except ValueError:
                        imp = 0.0
                    chiave = (imp >= soglia, row.get("data_pubblicazione") or "")
                    if cf not in migliore or chiave > migliore[cf][0]:
                        migliore[cf] = (chiave, row["cig"], row.get("data_pubblicazione"), (row.get("oggetto_lotto") or row.get("oggetto_gara") or "")[:200], imp)
    c.executemany("INSERT OR REPLACE INTO cig_test VALUES(?,?,?,?,?)", [(cf, v[1], v[2], v[3], v[4]) for cf, v in migliore.items()])
    c.commit()
    print(json.dumps({"enti_con_cig_test": len(migliore)}))
    return len(migliore)
