#!/usr/bin/env python3
"""Generatore di bozze delle istanze di accesso civico per ondata (#58, versione 0.1, 9/11/2026). NESSUN INVIO.

Dall'elenco unico (esiti/<data>/accesso-civico/elenco-mancanti.csv) produce, per gli enti dell'ondata, una richiesta
per ente con al massimo `tetto` voci (priorità decrescente), indirizzata alla PEC istituzionale IndicePA
(DECISIONI.md 2026-11-09) e, nel testo, all'ufficio che detiene i dati (art. 5 c. 3 lett. a d.lgs. 33/2013).

Uscite:
- lavoro/accesso-civico/<ondata>-bozze/<id>.md (testo) e <id>.json (spesaict.accesso-civico-richiesta/1):
  NON in git (possono contenere i dati del richiedente);
- lavoro/accesso-civico/<ondata>-bozze/eventi.jsonl: evento «creazione» (stato bozza), append-only, idempotente;
- esiti/<data>/accesso-civico/<ondata>/riepilogo.{csv,json,md}: riepilogo committato (solo dati pubblici degli enti).

Uso:
  bozze.py <data> --ondata ondata-0 [--tetto 20] [--proponi 30 | --enti cf1,cf2,...]
Parametri di default in config/accesso-civico/parametri.yaml (proposte, non decisioni).
"""
import argparse
import collections
import csv
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import stati  # noqa: E402

csv.field_size_limit(10**9)
VERSIONE = "0.1"
IPA = R / ("archivio/mirror/indicepa.gov.it/ipa-dati/dataset/502ff370-1b2c-4310-94c7-f39ceb7500e3/resource/"
           "3ed63523-ff9c-41f6-a6fe-980f3d9e501f/download/amministrazioni.txt")
MODELLI = R / "config/accesso-civico/modelli"
# tipologie ISTAT/IPA per cui il difensore civico è competente (art. 5 c. 8: regioni ed enti locali)
LOCALI = ("Comuni", "Province", "Citta' Metropolitane", "Regioni", "Unioni di Comuni", "Comunita' Montane",
          "Consorzi tra Amministrazioni Locali", "Altri Enti Locali")


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode("utf-8")).hexdigest()


def rendi(nome, valori):
    """Sottoinsieme compatibile con Jinja: {# commento #} e {{ variabile }}. Variabile mancante = errore."""
    testo = (MODELLI / f"{nome}.md").read_text(encoding="utf-8")
    testo = re.sub(r"\{#.*?#\}\n?", "", testo, flags=re.S)

    def sost(m):
        k = m.group(1)
        if k not in valori:
            raise KeyError(f"modello {nome}: manca la variabile {k}")
        return str(valori[k])
    return re.sub(r"\{\{\s*(\w+)\s*\}\}", sost, testo)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")


def pulisci_oggetto(s, n=280):
    parti = []
    for p in re.split(r"\s*\|\s*", s or ""):
        if p and not any(p.upper() in q.upper() for q in parti):
            parti.append(p.strip())
    s = " | ".join(parti)
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + "…"


def euro(x):
    try:
        return f"{float(x):,.0f} €".replace(",", ".")
    except (TypeError, ValueError):
        return ""


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def indicepa():
    per_cf = {}
    for r in csv.DictReader(open(IPA, encoding="utf-8-sig"), delimiter="\t"):
        cf = (r.get("cf") or "").strip()
        if cf and cf not in per_cf:
            per_cf[cf] = {"tipologia_istat": r.get("tipologia_istat", ""), "tipologia_amm": r.get("tipologia_amm", ""),
                          "regione": r.get("Regione", "")}
    return per_cf


# note di lavoro dell elenco unico che non vanno nel testo all ente
NOTE_INTERNE = re.compile(r";\s*(la pagina pubblica cita il CIG ma non contiene l.atto|i documenti pubblicati trovati non citano il CIG)")


def elenco_documenti(voci):
    righe = []
    for i, v in enumerate(voci, 1):
        testa = f"CIG {v['cig']}" if v["cig"] else "Iniziativa/convenzione"
        extra = ", ".join(x for x in (v["anno"], euro(v["importo"]) and f"importo {euro(v['importo'])}") if x)
        righe.append(f"{i}. **{testa}** — {pulisci_oggetto(v['oggetto'])}" + (f" ({extra})" if extra else "")
                     + f"  \n   *Documento richiesto:* {NOTE_INTERNE.sub('', v['documento_atteso'])}")
    return "\n".join(righe)


def proponi(enti, ipa, bozze_esistenti, p, n):
    """Selezione proposta dell'ondata 0: quota di enti con convenzioni (A) + mix di tipologie dal residuo (B)."""
    o = p["ondata_0"]
    ok = []
    for cf, e in enti.items():
        info = ipa.get(cf, {})
        if not e["pec"] or info.get("tipologia_amm") != o["tipologia_amm"]:
            continue
        if any(b.startswith(slug(e["ente"])[:40]) or slug(e["ente"]).startswith(b[:40]) for b in bozze_esistenti):
            continue
        ok.append(cf)
    scelti, per_tip = [], collections.Counter()

    def prendi(cf, motivo):
        tip = ipa[cf]["tipologia_istat"]
        if cf in [c for c, _ in scelti] or per_tip[tip] >= o["max_per_tipologia"]:
            return False
        scelti.append((cf, motivo))
        per_tip[tip] += 1
        return True
    for cf in sorted((c for c in ok if enti[c]["voci_A"]), key=lambda c: -enti[c]["priorita"]):
        if sum(1 for _, m in scelti if m.startswith("A")) >= o["quota_convenzioni"]:
            break
        prendi(cf, "A: convenzioni, priorità più alta senza bozza già pronta")
    # B: per tipologia, a turno: il più prioritario grande (>5 voci) e il più prioritario piccolo (1-5 voci)
    per_tipologia = collections.defaultdict(list)
    for cf in ok:
        if not enti[cf]["voci_A"]:
            per_tipologia[ipa[cf]["tipologia_istat"]].append(cf)
    ordine = sorted(per_tipologia, key=lambda t: -sum(enti[c]["priorita"] for c in per_tipologia[t]))
    giro = 0
    while len(scelti) < n and giro < 10:
        for t in ordine:
            if len(scelti) >= n:
                break
            grandi = sorted((c for c in per_tipologia[t] if len(enti[c]["voci"]) > 5), key=lambda c: -enti[c]["priorita"])
            piccoli = sorted((c for c in per_tipologia[t] if len(enti[c]["voci"]) <= 5), key=lambda c: -enti[c]["priorita"])
            lista = (grandi if giro % 2 == 0 else piccoli) or piccoli or grandi
            for c in lista:
                if prendi(c, f"B: residuo imbuto, tipologia «{t}», {'>5' if len(enti[c]['voci']) > 5 else '1-5'} voci"):
                    break
        giro += 1
    return scelti


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data")
    ap.add_argument("--ondata", default="ondata-0")
    ap.add_argument("--tetto", type=int)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--proponi", type=int, default=30)
    g.add_argument("--enti", help="codici fiscali separati da virgola")
    a = ap.parse_args()
    p = yaml.safe_load(open(R / "config/accesso-civico/parametri.yaml", encoding="utf-8"))
    tetto = a.tetto or p["tetto_voci_per_richiesta"]
    d_es = R / "esiti" / a.data / "accesso-civico"
    f_elenco = d_es / "elenco-mancanti.csv"
    enti = {}
    for r in csv.DictReader(open(f_elenco, encoding="utf-8")):
        e = enti.setdefault(r["cf"], {"ente": r["ente"].strip(), "codice_ipa": r["codice_ipa"], "pec": r["pec"],
                                      "pec_fonte": r["pec_fonte"], "voci": [], "voci_A": 0, "priorita": 0.0})
        e["voci"].append(r)
        e["voci_A"] += r["fonte"].startswith("A")
        e["priorita"] += num(r["priorita"])
    enti.pop("", None)
    # PEC mancante in IndicePA: ripiego su destinatari.csv (giro rpct_destinatari.py), con attendibilità
    dest = {}
    f_dest = d_es / "destinatari.csv"
    if f_dest.exists():
        for r in csv.DictReader(open(f_dest, encoding="utf-8")):
            dest[r["cf"]] = r
    for cf, e in enti.items():
        e["pec_att"] = "A" if e["pec"] else ""
        if not e["pec"] and dest.get(cf, {}).get("dest_pec"):
            e.update(pec=dest[cf]["dest_pec"], pec_fonte=f"destinatari.csv ({dest[cf].get('dest_fonte', '')})",
                     pec_att=dest[cf].get("dest_att") or "C")
    ipa = indicepa()
    bozze_esistenti = sorted({f.stem[len("mancanti-"):] for f in (R / p["ondata_0"]["escludi_bozze_esistenti"]).glob("mancanti-*")})
    if a.enti:
        scelti = [(cf.strip(), "indicato a mano") for cf in a.enti.split(",") if cf.strip()]
    else:
        scelti = proponi(enti, ipa, bozze_esistenti, p, a.proponi)

    out = R / "lavoro/accesso-civico" / f"{a.ondata}-bozze"
    out.mkdir(parents=True, exist_ok=True)
    f_ev = out / "eventi.jsonl"
    gia = stati.leggi(f_ev) if f_ev.exists() else {}
    h_elenco = sha(f_elenco.read_bytes())
    h_modello = sha((MODELLI / "istanza.md").read_bytes())
    ora = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rich = p["richiedente"]
    riepilogo = []
    for cf, motivo in scelti:
        e = enti[cf]
        info = ipa.get(cf, {})
        voci = sorted(e["voci"], key=lambda v: (-num(v["priorita"]), -num(v["importo"])))
        prime, resto = voci[:tetto], len(voci) - tetto
        rid = f"ac-{slug(a.ondata)}-{cf.lower()}-1"
        testo = rendi("istanza", {
            "richiedente_nome": rich["nome"], "richiedente_pec": rich["pec"], "richiedente_firma": rich.get("firma", ""),
            "ente": e["ente"], "pec_destinatario": e["pec"] or "[PEC MANCANTE]", "n_documenti": len(prime),
            "id_richiesta": rid, "elenco_documenti": elenco_documenti(prime),
            "luogo_data": f"{rich['luogo']}, [DATA DI INVIO]"})
        locale = any(info.get("tipologia_istat", "").startswith(x) for x in LOCALI)
        rec = {"formato": "spesaict.accesso-civico-richiesta/1", "id": rid, "ondata": a.ondata,
               "ente": {"cf": cf, "nome": e["ente"], "codice_ipa": e["codice_ipa"],
                        "tipologia_istat": info.get("tipologia_istat", ""), "regione": info.get("regione", ""),
                        "difensore_civico_competente": locale},
               "destinatario": {"pec": e["pec"], "fonte": e["pec_fonte"], "attendibilita": e["pec_att"] or "C",
                                "ufficio": "ufficio che detiene i dati (art. 5 c. 3 lett. a), per il tramite del protocollo/URP"},
               "voci": [{"id": v["id"], "fonte": v["fonte"], "cig": v["cig"], "oggetto": v["oggetto"],
                         "documento_atteso": v["documento_atteso"], "importo": num(v["importo"]) or None,
                         "anno": v["anno"] or None, "priorita": num(v["priorita"])} for v in prime],
               "voci_rinviate": max(resto, 0), "tetto": tetto, "modello": f"istanza.md {VERSIONE}",
               "modello_sha256": h_modello, "testo_sha256": sha(testo), "elenco_sha256": h_elenco,
               "generata": ora, "approvazione": None, "selezione": motivo}
        (out / f"{rid}.md").write_text(testo, encoding="utf-8")
        (out / f"{rid}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        if rid not in gia:
            stati.aggiungi(f_ev, {"id_richiesta": rid, "tipo": "creazione", "data": ora[:10], "chi": "bozze.py",
                                  "note": f"bozza generata, testo sha256 {sha(testo)}"})
        riepilogo.append({"id": rid, "ente": e["ente"], "cf": cf, "codice_ipa": e["codice_ipa"],
                          "tipologia_istat": info.get("tipologia_istat", ""), "regione": info.get("regione", ""),
                          "pec": e["pec"], "pec_attendibilita": e["pec_att"] or "C",
                          "voci_totali": len(voci), "voci_richiesta": len(prime), "voci_A": sum(v["fonte"].startswith("A") for v in prime),
                          "voci_rinviate": max(resto, 0), "euro_richiesta": round(sum(num(v["importo"]) for v in prime)),
                          "difensore_civico": "sì" if locale else "no (TAR)", "selezione": motivo,
                          "testo_sha256": sha(testo)})
    d_out = d_es / a.ondata
    d_out.mkdir(parents=True, exist_ok=True)
    with open(d_out / "riepilogo.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(riepilogo[0]))
        w.writeheader()
        w.writerows(riepilogo)
    sintesi = {"data": a.data, "ondata": a.ondata, "generato": ora, "versione": VERSIONE, "tetto": tetto,
               "enti": len(riepilogo), "voci": sum(r["voci_richiesta"] for r in riepilogo),
               "voci_A": sum(r["voci_A"] for r in riepilogo),
               "voci_rinviate": sum(r["voci_rinviate"] for r in riepilogo),
               "euro": sum(r["euro_richiesta"] for r in riepilogo),
               "tipologie": dict(collections.Counter(r["tipologia_istat"] for r in riepilogo).most_common()),
               "regioni": len({r["regione"] for r in riepilogo}),
               "difensore_civico_competente": sum(r["difensore_civico"] == "sì" for r in riepilogo),
               "enti_esclusi_bozza_esistente": bozze_esistenti, "elenco_sha256": h_elenco,
               "modello_sha256": h_modello, "invii": 0}
    (d_out / "riepilogo.json").write_text(json.dumps(sintesi, ensure_ascii=False, indent=1), encoding="utf-8")
    md = [f"# Ondata {a.ondata}: riepilogo delle bozze (proposta, NESSUN INVIO)", "",
          f"Generato il {ora} da `tools/accesso_civico/bozze.py {a.data} --ondata {a.ondata}` (versione {VERSIONE}), "
          f"tetto {tetto} voci per richiesta. Elenco sha256 `{h_elenco[:16]}…`, modello `istanza.md` sha256 `{h_modello[:16]}…`.",
          f"Testi in `lavoro/accesso-civico/{a.ondata}-bozze/` (sul server, non in git).", "",
          f"**{sintesi['enti']} enti, {sintesi['voci']} voci** ({sintesi['voci_A']} convenzioni), "
          f"{euro(sintesi['euro'])}; {sintesi['voci_rinviate']} voci oltre il tetto restano per le ondate successive. "
          f"Difensore civico competente per {sintesi['difensore_civico_competente']} enti.", "",
          "| # | Ente | Tipologia | Regione | Voci (rinviate) | Importo | Selezione |", "|---|---|---|---|---|---|---|"]
    for i, r in enumerate(riepilogo, 1):
        md.append(f"| {i} | {r['ente']} | {r['tipologia_istat']} | {r['regione']} | {r['voci_richiesta']} ({r['voci_rinviate']}) "
                  f"| {euro(r['euro_richiesta'])} | {r['selezione']} |")
    (d_out / "riepilogo.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in sintesi.items() if k != "enti_esclusi_bozza_esistente"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
