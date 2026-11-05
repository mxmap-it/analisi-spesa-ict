"""#62, passo 1: censimento delle iniziative ICT principali (accordi quadro, convenzioni, PSN, soggetti aggregatori).

Fonti (tutte versionate o archiviate con sha256):
  - report/metodo/conoscenza/padri-ict.csv       CIG padre richiamati da attuativi ICT 2020-2026 (tools/analisi/padri_ict.py)
  - report/convenzioni/database/padri-ict-2024-2025.csv  stessi conteggi per i soli attuativi 2024-2025 (se presente)
  - config/iniziative_ict.yaml                    base di conoscenza (nome, categoria, dossier, documenti)
  - report/metodo/llm/conoscenza-iniziative.yaml  iniziative note anche senza attuativi nei dati (es. IaaS/PaaS 2)

Criterio (documentato in report/convenzioni/database/README.md):
  1. un'iniziativa = ID Sigef Consip ricavato dall'oggetto del CIG padre o dalla base di conoscenza; senza ID, il CIG padre;
  2. valore = somma degli importi dei CIG derivati ICT 2024-2025 (se il file c'è) altrimenti 2020-2026;
  3. non vecchie = con CIG derivati ICT 2024-2025, o nuove (PRINCO 2928, IaaS/PaaS 2 ID 2746); tipo di soggetto da config/tipi_soggetto.yaml;
  4. fuori Consip almeno 3 derivati ICT 2024-2025 e 1 M EUR;
  5. principali = le prime QUOTE[tipo] per valore in ciascun tipo + PSN + nuove; le iniziative della base di conoscenza senza
     derivati 2024-2025 ma con >= 100 M EUR dal 2020 restano come «storiche» (segnalate a parte).
Deterministico: stesso input, stessa uscita. Uscita: report/convenzioni/database/censimento.csv
Uso: python tools/convenzioni/censimento.py"""
import csv, os, re, sys, collections
from pathlib import Path
import yaml

R = Path(__file__).resolve().parent.parent.parent
DB = R / "report/convenzioni/database"
RE_ID = re.compile(r"\bID\s*(?:SIGEF\s*)?(?:N\.?\s*)?(\d{4})\b", re.I)
RE_ID_KB = re.compile(r"\b(?:ID|SIGEF)(?:\s*Sigef)?\s*(\d{4})\b", re.I)
# quante iniziative per tipo di soggetto (le prime per valore ICT 2024-2025)
QUOTE = {"consip": 40, "aggregatore-regionale": 25, "consorzio-unione": 15, "altro": 10}
SOGLIA_STORICO = 100_000_000
# fuori Consip un CIG padre e' un'iniziativa di acquisto aggregato solo se ha piu' derivati: soglie minime
MIN_DERIVATI, MIN_EURO = 3, 1_000_000
FORZATE = {"psn": "9066973ECE", "consip-2928": "BAFCF54A81"}


def leggi_padri(p):
    if not p.exists():
        return {}
    with open(p, encoding="utf-8") as f:
        return {r["cig_padre"]: r for r in csv.DictReader(f)}


def main():
    tutti = leggi_padri(R / "report/metodo/conoscenza/padri-ict.csv")
    recenti = leggi_padri(DB / "padri-ict-2024-2025.csv")
    kb = yaml.safe_load(open(R / "config/iniziative_ict.yaml", encoding="utf-8")) or []
    kb_cig = {str(v["cig"]): v for v in kb if isinstance(v, dict) and v.get("cig")}
    con = yaml.safe_load(open(R / "report/metodo/llm/conoscenza-iniziative.yaml", encoding="utf-8")) or {}
    lotti_con = {}
    for it in con.get("iniziative", []) or []:
        for l in it.get("lotti", []) or []:
            if l.get("cig_aq"):
                lotti_con[str(l["cig_aq"])] = (it.get("id"), it.get("nome"), str(l.get("lotto", "")))

    def id_iniziativa(cig, ogg):
        if cig == FORZATE["psn"]:
            return "psn"
        if cig in lotti_con and lotti_con[cig][0]:
            return lotti_con[cig][0]
        k = kb_cig.get(cig, {})
        m = RE_ID_KB.search(k.get("iniziativa", "") or "") or RE_ID.search(ogg or "")
        if m:
            return f"consip-{m.group(1)}"
        d = re.match(r"(\d{4})-", os.path.basename(k.get("dossier", "") or ""))
        if d:
            return f"consip-{d.group(1)}"
        # senza ID: i lotti della stessa gara (stesso testo prima di " | ") sono una sola iniziativa
        return "gara:" + (ogg.split(" | ")[0].strip() or cig)

    righe = []
    for cig in sorted(set(tutti) | set(recenti) | set(kb_cig) | set(lotti_con) | set(FORZATE.values())):
        t, r2 = tutti.get(cig, {}), recenti.get(cig, {})
        ogg = t.get("oggetto_padre") or r2.get("oggetto_padre") or ""
        righe.append({
            "iniziativa": "consip-2928" if cig == FORZATE["consip-2928"] else id_iniziativa(cig, ogg),
            "cig_padre": cig,
            "stazione_appaltante": t.get("stazione_appaltante_padre") or r2.get("stazione_appaltante_padre") or "",
            "anno_padre": t.get("anno_padre") or r2.get("anno_padre") or "",
            "oggetto": ogg[:300] or (kb_cig.get(cig, {}).get("iniziativa") or (lotti_con.get(cig, ("", "", ""))[1]) or ""),
            "derivati_ict_2020_2026": int(t.get("attuativi_ict") or 0),
            "euro_ict_2020_2026": int(float(t.get("euro_attuativi") or 0)),
            "derivati_ict_2024_2025": int(r2.get("attuativi_ict") or 0),
            "euro_ict_2024_2025": int(float(r2.get("euro_attuativi") or 0)),
            "in_base_conoscenza": "si" if cig in kb_cig or cig in lotti_con else "no",
        })
    # le gare senza ID prendono come identificativo il CIG padre piu' basso
    gare = collections.defaultdict(list)
    for r in righe:
        if r["iniziativa"].startswith("gara:"):
            gare[r["iniziativa"]].append(r["cig_padre"])
    for r in righe:
        if r["iniziativa"].startswith("gara:"):
            r["iniziativa"] = "cig-" + min(gare[r["iniziativa"]])
    regole = [(x["tipo"], re.compile(x["rx"])) for x in yaml.safe_load(open(R / "config/tipi_soggetto.yaml", encoding="utf-8"))["regole"]]
    def tipo_sogg(r):
        if r["iniziativa"] == "psn":
            return "psn"
        sa = (r["stazione_appaltante"] or ("CONSIP" if r["iniziativa"].startswith("consip-") else "")).upper()
        return next(t for t, rx in regole if rx.search(sa or "?"))
    for r in righe:
        r["tipo_soggetto"] = tipo_sogg(r)
    campo = "euro_ict_2024_2025" if recenti else "euro_ict_2020_2026"
    val, val_storico, tipo_ini = collections.Counter(), collections.Counter(), {}
    for r in righe:
        val[r["iniziativa"]] += r[campo]; val_storico[r["iniziativa"]] += r["euro_ict_2020_2026"]
        tipo_ini.setdefault(r["iniziativa"], r["tipo_soggetto"])
    nder = collections.Counter()
    for r in righe:
        nder[r["iniziativa"]] += r["derivati_ict_2024_2025"]
    ordine = sorted(val.items(), key=lambda x: (-x[1], x[0]))
    rango = {i: k + 1 for k, (i, _) in enumerate(ordine)}
    # criterio «non vecchie»: CIG derivati ICT 2024-2025 (val > 0) oppure iniziativa nuova nota (PRINCO, IaaS/PaaS 2)
    NUOVE = {"consip-2928", "consip-2746"}
    scelte, stato = set(), {}
    for t, n in QUOTE.items():
        for i in [i for i, v in ordine if tipo_ini[i] == t and v > 0 and (t == "consip" or (v >= MIN_EURO and nder[i] >= MIN_DERIVATI))][:n]:
            scelte.add(i); stato[i] = "attiva"
    for i in NUOVE | {"psn"}:
        scelte.add(i); stato[i] = "attiva"
    # base di conoscenza senza derivati recenti: «storica», segnalata a parte se pesa ancora (>= SOGLIA_STORICO dal 2020)
    for r in righe:
        i = r["iniziativa"]
        if r["in_base_conoscenza"] == "si" and i not in scelte and val_storico[i] >= SOGLIA_STORICO:
            scelte.add(i); stato[i] = "storica"
    out = [dict(r, rango_iniziativa=rango.get(r["iniziativa"], ""), valore_iniziativa=val[r["iniziativa"]],
                valore_iniziativa_2020_2026=val_storico[r["iniziativa"]], criterio_valore=campo, stato_iniziativa=stato[r["iniziativa"]])
           for r in righe if r["iniziativa"] in scelte]
    out.sort(key=lambda r: (-r["valore_iniziativa"], r["iniziativa"], -r[campo], r["cig_padre"]))
    DB.mkdir(parents=True, exist_ok=True)
    with open(DB / "censimento.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader(); w.writerows(out)
    print(collections.Counter(tipo_ini[i] for i in scelte), collections.Counter(stato.values()))
    print(f"{len(scelte)} iniziative, {len(out)} lotti (CIG padre); valore = {campo}; padri ICT nei dati: {len(tutti)}")


if __name__ == "__main__":
    main()
