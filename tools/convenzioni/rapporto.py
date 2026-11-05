"""#62: rapporto sullo stato della trasparenza nelle convenzioni ICT (rendiconto web, iterativo).

Si rigenera dalla base dati (report/convenzioni/database/iniziative.json, carenze.yaml, accesso-civico/registro.csv).
Ogni esecuzione con una VERSIONE nuova aggiunge una riga a report/convenzioni/rapporto/versioni.jsonl con le metriche e calcola
cosa è cambiato rispetto alla versione precedente (documenti trovati, carenze risolte, istanze inviate o con risposta).
Le metriche sono calcolate da metriche() e ricontrollate per seconda via da tools/verifiche/convenzioni_rapporto.py.

Indice di visibilità (nessun peso, solo conteggi):
  per ogni iniziativa e per ciascun tipo di dato atteso dell'inventario (13, 14 per PSN e SPC Cloud), una sola classe:
    pubblico  = archiviato o pubblicato dalla fonte ufficiale;
    altrove   = non pubblico, ma reperito da fonte non ufficiale (atti di enti aderenti, ecc.);
    assente   = non pubblicato, assenza constatata sulla pagina ufficiale (verificato);
    ignoto    = da verificare.
  indice = pubblici / attesi.
  «Ben visibile» = tutti e quattro i dati di spesa e sovranità sono pubblici: offerta tecnica, offerta economica,
  transato e monitoraggio, ordinativi. Il valore «non ben visibile» è la somma dei derivati ICT 2024-2025 delle iniziative
  che non lo sono (ordine di grandezza: include i massimali dichiarati negli attuativi).
Uso: python tools/convenzioni/rapporto.py VERSIONE DATA "nota della revisione" """
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

R = Path(__file__).resolve().parent.parent.parent
DB = R / "report/convenzioni/database"
RAP = R / "report/convenzioni/rapporto"
OUT = R / "sito/content/rendiconti/convenzioni-trasparenza.md"
CHIAVE = ("offerta_tecnica", "offerta_economica", "transato_monitoraggio", "ordinativi")
TIPI = {"consip": "Consip", "psn": "PSN", "aggregatore-regionale": "Aggregatori regionali", "consorzio-unione": "Consorzi e unioni", "altro": "Altri"}


# iniziative che il filtro CPV ICT lascia passare ma non sono ICT (vedi § Metodo e limiti)
FUORI_PERIMETRO = {"consip-2638"}


DATI_AL = "2026-11-05"  # consultazione più recente delle fonti (pagine Consip, open data, enti campione, ricerca web)
DT = "05/11/2026"


def enti_campione():
    import csv as _csv
    p = R / "report/convenzioni/enti-campione/enti-campione-2026-11-05.csv"
    if not p.exists():
        return {}
    rr = [r for r in _csv.DictReader(open(p, encoding="utf-8")) if "controllo" not in (r["note"] or "").lower()]
    c = Counter(r["esito"] for r in rr)
    return {"righe": len(rr), "enti": len({r["ente"] for r in rr}), "iniziative": len({r["iniziativa"] for r in rr}),
            "in_at": c.get("trovato-in-AT", 0), "fuori_at": c.get("trovato-fuori-AT", 0), "non_trovato": c.get("non-trovato", 0),
            "at_irraggiungibile": c.get("AT-irraggiungibile", 0), "archiviati": sum(1 for r in rr if r["sha256"]),
            "at_da_home_no": sum(1 for r in rr if r["at_raggiungibile_da_home"] == "no")}


def fonti_web():
    import csv as _csv
    p = R / "report/convenzioni/fonti-non-ufficiali/fonti-2026-11-05.csv"
    if not p.exists():
        return {}
    rr = list(_csv.DictReader(open(p, encoding="utf-8")))
    return {"righe": len(rr), "url": len({r["url"] for r in rr}), "archiviati": len({r["url"] for r in rr if r["sha256"]})}


def migliaia(riga):
    """Separatore delle migliaia anche per i numeri di 4 cifre (1.120), salvo anni, ID e codici (regola del sito)."""
    if riga.startswith("---") or riga.startswith(("title:", "date:", "lastmod:", "datiAl:", "subtitle:", "description:")):
        return riga

    def f(m):
        n = int(m.group(0))
        return m.group(0) if 1990 <= n <= 2035 else f"{n:,}".replace(",", ".")
    return re.sub(r"(?<![\w./#=:-])(?<!ID )(?<!Sigef )\d{4,}(?![\w.,/%-])", f, riga)


def meur2(v):
    if not v:
        return "0"
    if v < 50_000:
        return "<0,1"
    return f"{v / 1e6:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")


def pct1(a, b):
    return f"{100 * a / b:.1f} %".replace(".", ",") if b else "–"


def classe(i):
    if i["stato"] in ("archiviato", "pubblicato-non-archiviato"):
        return "pubblico"
    if i.get("reperiti_altrove"):
        return "altrove"
    return "assente" if i["stato"] == "non-pubblicato" else "ignoto"


def metriche(voci, reg):
    per = {}
    for v in voci:
        c = Counter(classe(i) for i in v["inventario"])
        chiave = {i["tipo"]: classe(i) for i in v["inventario"] if i["tipo"] in CHIAVE}
        per[v["id"]] = {"attesi": len(v["inventario"]), **{k: c.get(k, 0) for k in ("pubblico", "altrove", "assente", "ignoto")},
                        "indice": round(c.get("pubblico", 0) / len(v["inventario"]), 3),
                        "ben_visibile": all(x == "pubblico" for x in chiave.values()) and len(chiave) == 4,
                        "valore": v["valore_ict_2024_2025"] or 0, "tipo": v["tipo_soggetto"], "stato": v["stato_iniziativa"],
                        "carenze_verificate": sorted(k["id"] for k in v["carenze"] if k["stato"] == "verificato"),
                        "carenze_da_verificare": sorted(k["id"] for k in v["carenze"] if k["stato"] != "verificato"),
                        "documenti": sum(len(i["documenti"]) for i in v["inventario"]),
                        "altrove_doc": sum(len(i.get("reperiti_altrove", [])) for i in v["inventario"])}
    tot = sum(p["valore"] for p in per.values())
    nbv = sum(p["valore"] for p in per.values() if not p["ben_visibile"])
    g = {"iniziative": len(per), "attive": sum(1 for p in per.values() if p["stato"] == "attiva"),
         "valore_2024_2025": tot, "valore_non_ben_visibile": nbv, "iniziative_ben_visibili": sum(1 for p in per.values() if p["ben_visibile"]),
         "indice_medio": round(sum(p["indice"] for p in per.values()) / len(per), 3),
         "celle": dict(Counter(classe(i) for v in voci for i in v["inventario"])),
         "documenti_ufficiali": sum(p["documenti"] for p in per.values()), "documenti_altrove": sum(p["altrove_doc"] for p in per.values()),
         "istanze_preparate": sum(1 for r in reg if r["stato"] == "preparata"), "istanze_inviate": sum(1 for r in reg if r["stato"] not in ("preparata", "ritirata")),
         "istanze_con_risposta": sum(1 for r in reg if r.get("risposta")),
         "flusso_dati": sum(1 for v in voci if v.get("evidenze_dato_esistente")),
         "flusso_letti": sum(1 for v in voci for e in v.get("evidenze_dato_esistente", []) if e["livello"].startswith("V")),
         "istanze_ritirate": sum(1 for r in reg if r["stato"] == "ritirata"),
         "aretepa_vetrina": len(json.loads((R / "report/convenzioni/aretepa/vetrina-sintesi.json").read_text(encoding="utf-8"))) if (R / "report/convenzioni/aretepa/vetrina-sintesi.json").exists() else 0,
         "aretepa_schede": sum(1 for v in voci if v.get("aretepa")),
         "aretepa_documenti": sum((v.get("aretepa") or {}).get("documenti", 0) for v in voci),
         "enti_campione": enti_campione(), "fonti_web": fonti_web(),
         "od_iniziative": sum(1 for v in voci if v.get("ordinato_consip")),
         "od_bdncp": sum(v["valore_ict_2024_2025"] or 0 for v in voci if v.get("ordinato_consip")),
         "od_ordinato": sum(v["ordinato_consip"]["2024"] + v["ordinato_consip"]["2025"] for v in voci if v.get("ordinato_consip"))}
    pt = {}
    for t in TIPI:
        x = [p for p in per.values() if p["tipo"] == t]
        if x:
            pt[t] = {"iniziative": len(x), "valore": sum(p["valore"] for p in x), "indice_medio": round(sum(p["indice"] for p in x) / len(x), 3),
                     "ben_visibili": sum(1 for p in x if p["ben_visibile"]), "ignoti": sum(p["ignoto"] for p in x), "assenti": sum(p["assente"] for p in x)}
    return {"globali": g, "per_tipo": pt, "per_iniziativa": per}


def carica():
    voci = json.loads((DB / "iniziative.json").read_text(encoding="utf-8"))
    rp = R / "report/convenzioni/accesso-civico/registro.csv"
    reg = list(csv.DictReader(open(rp, encoding="utf-8"))) if rp.exists() else []
    return voci, reg


def meur(v):
    return f"{v / 1e6:,.0f}".replace(",", ".")


def pct(a, b):
    return f"{round(100 * a / b)} %" if b else "–"


def differenze(prima, ora):
    if not prima:
        return ["prima versione"]
    out = []
    pi, oi = prima["per_iniziativa"], ora["per_iniziativa"]
    for k, o in oi.items():
        p = pi.get(k)
        if not p:
            out.append(f"nuova iniziativa nel censimento: {k}")
            continue
        if o["documenti"] > p["documenti"]:
            out.append(f"{k}: documenti ufficiali da {p['documenti']} a {o['documenti']}")
        if o["altrove_doc"] > p["altrove_doc"]:
            out.append(f"{k}: documenti da fonte non ufficiale da {p['altrove_doc']} a {o['altrove_doc']}")
        risolte = set(p["carenze_verificate"] + p["carenze_da_verificare"]) - set(o["carenze_verificate"] + o["carenze_da_verificare"])
        if risolte:
            out.append(f"{k}: carenze non più presenti {sorted(risolte)}")
    for k in ("istanze_preparate", "istanze_inviate", "istanze_con_risposta"):
        if ora["globali"][k] != prima["globali"][k]:
            out.append(f"{k.replace('_', ' ')}: da {prima['globali'][k]} a {ora['globali'][k]}")
    return out or ["nessuna variazione nei dati"]


def main(versione, data, nota):
    voci, reg = carica()
    m = metriche(voci, reg)
    RAP.mkdir(parents=True, exist_ok=True)
    vf = RAP / "versioni.jsonl"
    storia = [json.loads(x) for x in open(vf, encoding="utf-8")] if vf.exists() else []
    storia = [s for s in storia if s["versione"] != versione]
    diff = differenze(storia[-1]["metriche"] if storia else None, m)
    storia.append({"versione": versione, "data": data, "nota": nota, "cambiamenti": diff, "metriche": m})
    with open(vf, "w", encoding="utf-8") as f:
        for s in storia:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    (RAP / "metriche-ultime.json").write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
    car = yaml.safe_load(open(DB / "carenze.yaml", encoding="utf-8"))["carenze"]
    g, pt, pi = m["globali"], m["per_tipo"], m["per_iniziativa"]
    nomi = {v["id"]: v["nome"] for v in voci}
    top = max(pi, key=lambda k: pi[k]["valore"])
    tot_celle = sum(g["celle"].values())
    L = ["---", 'title: "Trasparenza delle convenzioni ICT della PA"',
         'subtitle: "Rendiconto iterativo: cosa si può verificare delle convenzioni e degli accordi quadro ICT, e cosa no"',
         "date: 2026-11-05", f"lastmod: {data}", f"datiAl: {DATI_AL}",
         'description: "Stato della trasparenza delle principali convenzioni e accordi quadro ICT (Consip, PSN, soggetti aggregatori): documenti pubblici, dati assenti, valore non verificabile, rimedi."',
         "---", "",
         "<!-- Generato da tools/convenzioni/rapporto.py dalla base dati: non modificare a mano. -->", "",
         f"**Versione {versione} del {data}** · [registro delle revisioni](#registro-delle-revisioni) · **bozza da presentare a Fabio Pietrosanti prima di ogni diffusione esterna**", "",
         "Ogni numero viene dalla base dati `report/convenzioni/database/` e si rifà con `python tools/verifiche/convenzioni_rapporto.py`.", "",
         "## 1. Sintesi", "",
         "*Cosa non diciamo:* che un dato non individuato sia nascosto di proposito; che un dato reperito presso un ente valga per tutta la "
         "convenzione; che le somme BDNCP siano spesa. Molte carenze riguardano dati che oggi nessuna norma obbliga a pubblicare.", "",
         f"- **Perimetro.** {g['iniziative']} iniziative ICT ({g['attive']} attive): Consip, PSN, soggetti aggregatori regionali, consorzi e altre "
         f"stazioni appaltanti con più contratti derivati. Criterio nel [README della base dati](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/database/README.md).",
         f"- **Valore.** I contratti derivati con CPV ICT pubblicati nel 2024-2025 dichiarano in BDNCP circa **{meur(g['valore_2024_2025'])} M€**. "
         "È un ordine di grandezza, non la spesa: in molti casi l'importo dichiarato è il massimale o il valore pluriennale (§ 2).",
         f"- **Visibilità.** Dei {tot_celle} dati attesi (iniziativa × tipo di documento o dato): pubblici dalla fonte ufficiale "
         f"{g['celle'].get('pubblico', 0)} ({pct(g['celle'].get('pubblico', 0), tot_celle)}); reperiti solo presso enti aderenti {g['celle'].get('altrove', 0)} "
         f"({pct1(g['celle'].get('altrove', 0), tot_celle)}); non individuati sulla pagina del bando {g['celle'].get('assente', 0)} ({pct(g['celle'].get('assente', 0), tot_celle)}); "
         f"non ancora verificati {g['celle'].get('ignoto', 0)} ({pct(g['celle'].get('ignoto', 0), tot_celle)}). Indice di visibilità medio "
         f"**{round(100 * g['indice_medio'])} %**, da leggere come limite inferiore finché le celle non verificate restano così tante.",
         "- **Dati per controllare spesa e sovranità.** Nelle iniziative verificate non abbiamo individuato, pubblicati insieme, offerte dei vincitori, "
         "transato per marchio ed elenco degli ordinativi per ente: sono dati che oggi la norma non obbliga la centrale a pubblicare (carenze C1-C4, con la base di ciascuna).",
         "- **Carenze principali** (pagine dei bandi su consip.it, open data Consip, Amministrazione trasparente di Consip e campione di enti, "
         "consultati il 5/11/2026; acquistinretepa solo in parte): offerte tecniche dei vincitori, transato per listino e marchio, elenco degli ordinativi per ente non individuati. "
         "Gli ordinativi si trovano in parte negli atti dei singoli enti. Region e data center: per IaaS/PaaS 2 (ID 2746) e PRINCO (ID 2928) i "
         "documenti di gara prevedono che il fornitore li dichiari, ma la dichiarazione non è pubblicata.",
         "- **Il dato dovrebbe essere presso Consip.** Secondo l'allegato 4E della convenzione Microsoft EA8 (ID 2615, letto per intero), "
         "il fornitore deve trasmettere ogni mese a Consip il dettaglio delle fatture, con l'ID dell'ordine sulla piattaforma e l'imponibile, "
         "per il calcolo della commissione (d.m. MEF 23/11/2012). Se il flusso è rispettato, Consip dispone dei dati per ricostruire il transato "
         "per ordine e quindi per ente; non abbiamo verificato che il flusso avvenga né in che forma sia conservato. "
         f"Gli altri {g['flusso_dati'] - 1} allegati, analizzati per parole chiave (R), seguono in gran parte lo stesso schema; fa eccezione quello "
         "di System Management 3 (ID 2275), sui flussi di monitoraggio, dove compaiono campi per ente e prodotto.",
         f"- **Rimedi.** Dopo le fonti online del § 3 (acquistinretepa ancora parziale), {g['istanze_preparate']} bozze di accesso civico generalizzato, "
         f"tutte verso Consip, restano utili all'analisi; {g['istanze_ritirate']} sono ritirate, con il motivo di ciascuna nel registro; **nessuna inviata**; proposte di policy R08 e R37-R44 "
         "perché questi dati diventino pubblici senza bisogno di chiederli.", "",
         "## 2. Due misure del valore", "",
         f"Per {g['od_iniziative']} iniziative Consip esiste una seconda misura: gli **open data Consip** degli ordini diretti "
         f"(dati.consip.it, 2024 e 2025, file archiviati con sha256): **{meur(g['od_ordinato'])} M€** ordinati. Le stesse iniziative dichiarano "
         f"in BDNCP **{meur(g['od_bdncp'])} M€** di derivati ICT 2024-2025. **Le due grandezze non sono confrontabili** una a una: gli open data "
         "contano gli ordini diretti dell'anno (non gli appalti specifici degli accordi quadro con rilancio competitivo); BDNCP l'importo "
         "dichiarato all'acquisizione del CIG, spesso pluriennale o pari al massimale. La tabella serve a mostrare l'ordine di grandezza e i casi "
         "da spiegare (es. ID 2496, dove l'ordinato supera il dichiarato: cause possibili derivati con CPV non ICT, lotti non censiti o abbinamento da rivedere). "
         "Gli abbinamenti sono per coincidenza del nome («V-testo»): confermati con il titolo della pagina Consip trovata per ID Sigef, o per il 2483 con atti di enti che riportano ID e CIG; nessun open data riporta l'ID Sigef. Gli open data non riportano listino, marchio né "
         "ente: la carenza C3 resta.", "",
         f"Open data Consip scaricati il {DT}; BDNCP elaborato il {DT}.", "",
         "| Iniziativa | M€ BDNCP 2024-25 | M€ ordinati 2024+2025 (open data Consip) | Abbinamento |", "|---|---|---|---|"]
    for v in sorted([v for v in voci if v.get("ordinato_consip") and v["id"] not in FUORI_PERIMETRO], key=lambda v: -(v["valore_ict_2024_2025"] or 0)):
        o = v["ordinato_consip"]
        L.append(f"| [{v['nome'][:60]}](/convenzioni/{v['id'].lower()}/) | {meur(v['valore_ict_2024_2025'] or 0)} | {meur(o['2024'] + o['2025'])} | "
                 f"{'; '.join(n.split(' [')[1].rstrip(']')[:40] for n in o['nomi'])} |")
    L += ["", "### Consumato per convenzione, fonte per fonte", "",
          f"Consultazioni del {DT}. [V] = dato letto da noi sulla fonte archiviata; [R] = riferito. Nessuna fonte pubblica dà il consumato "
          "per listino, marchio o ente.", "",
          "Legenda: «–» = iniziativa non abbinata negli open data; «0» = abbinata con importo nullo; «<0,1» = importo positivo sotto 0,05 M€. Ordinato 2026: file open data Consip scaricato il 05/11/2026 (copertura dell'anno non dichiarata dal file). Separatore delle migliaia: punto; decimali: virgola.", "",
          "| Iniziativa | BDNCP derivati ICT 2024-25 (M€) [V] | Ordinato 2024 (M€) [V] | Ordinato 2025 (M€) [V] | Ordinato 2026, file del 05/11/2026 (M€) [V] | Massimale residuo su acquistinretepa | Corte dei conti [R] |",
          "|---|---|---|---|---|---|---|"]
    for v in sorted([v for v in voci if v["tipo_soggetto"] == "consip" and v["id"] not in FUORI_PERIMETRO and (v.get("ordinato_consip") or v.get("aretepa"))],
                    key=lambda v: -(v["valore_ict_2024_2025"] or 0)):
        o_ = v.get("ordinato_consip") or {}
        ar = v.get("aretepa")
        res = "sezione presente ma vuota alla consultazione («Nessun risultato»)" if ar and not ar["residuo_pubblico"] else ("dati presenti" if ar else "scheda non individuata da noi")
        L.append(f"| [{v['nome'][:60]}](/convenzioni/{v['id'].lower()}/) | {meur(v['valore_ict_2024_2025'] or 0)} | "
                 + (f"{meur2(o_.get('2024', 0))} | {meur2(o_.get('2025', 0))} | {meur2(o_.get('2026', 0))}" if o_ else "– | – | –")
                 + f" | {res} | solo aggregato degli AQ |")
    L += ["", "**Perché le fonti non coincidono.** BDNCP registra l'importo dichiarato quando l'ente acquisisce il CIG derivato (spesso pluriennale o "
          "pari al massimale) e solo per i derivati con CPV ICT; gli open data Consip contano gli ordini diretti dell'anno (non gli appalti specifici "
          "con rilancio competitivo) per convenzione o AQ; la Corte dei conti riporta l'erogato complessivo degli accordi quadro, non per iniziativa. "
          "Per alcune iniziative (es. ID 2648 e 2496) l'ordinato supera il dichiarato BDNCP (derivati senza CPV ICT o CIG fuori dal 2024-25): le due "
          "misure non vanno sommate né sottratte. Il massimale residuo, che darebbe l'erosione per lotto, ha una sezione nella scheda pubblica di "
          "acquistinretepa che il 05/11/2026 risultava vuota («Nessun risultato»); alcune parti della pagina mostravano date segnaposto, quindi la "
          "resa potrebbe essere stata incompleta: non abbiamo verificato se il dato compaia dopo l'accesso. È nell'[elenco dei blocchi](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/blocchi-accesso.csv) "
          "da provare a mano.", ""]
    ec, fw = g["enti_campione"], g["fonti_web"]
    L += ["", "## 3. Fonti online consultate prima dell'accesso civico", "",
          f"Tutte consultate il {DT}, senza login né CAPTCHA, a ritmo basso e con User-Agent dichiarato.", "",
          "| Fonte | Esito | Livello |", "|---|---|---|",
          "| Pagine dei bandi su consip.it | documentazione di gara di 44 iniziative; offerte, transato per marchio ed elenco degli ordinativi non individuati | V per la presenza dei file; R per il tipo dedotto dal nome |",
          "| Open data Consip (dati.consip.it) | ordinato per anno, convenzione o AQ e lotto (2024-2025); niente ente, listino, marchio | V |",
          f"| acquistinretepa (browser reale, Chrome headless) | vetrina: {g['aretepa_vetrina']} iniziative (servizio getIniziative, attive e archivio); schede pubbliche trovate per {g['aretepa_schede']} iniziative del censimento, con {g['aretepa_documenti']} documenti linkati; sezione «Massimale residuo» vuota alla consultazione (resa forse incompleta: date segnaposto); catalogo e acquisto dietro «Accedi»; chiamate JSON registrate con sha256 | V per ciò che è stato visto; da riverificare il residuo |",
          "| Amministrazione trasparente di Consip | le sottosezioni di «Bandi di gara e contratti» riguardano gli acquisti di Consip per sé; «Controlli e rilievi» rinvia alla Corte dei conti | V (indice delle sezioni) |",
          f"| Campione di enti aderenti | {ec.get('righe', 0)} righe valide (righe di controllo escluse), {ec.get('enti', 0)} enti, {ec.get('iniziative', 0)} iniziative: file nel percorso AT {ec.get('in_at', 0)}, URL esterno al percorso AT {ec.get('fuori_at', 0)} (collegamento dalla sezione AT non verificato), non trovato {ec.get('non_trovato', 0)}, AT non verificabile automaticamente il 5/11 {ec.get('at_irraggiungibile', 0)} (da ripetere); {ec.get('archiviati', 0)} archiviati | V per i documenti letti; R per la posizione rispetto all'AT |",
          f"| Ricerca web (Corte dei conti, stampa, atti di enti) | {fw.get('righe', 0)} dati da {fw.get('url', 0)} URL, {fw.get('archiviati', 0)} archiviati; erogato per iniziativa non trovato (nelle due relazioni della Corte dei conti consultate, gestioni 2021 e 2022, l'erogato degli AQ è aggregato) | R |",
          f"| Allegati «flussi dati del fatturato» | {g['flusso_dati']} allegati acquisiti e analizzati per parole chiave, letto per intero quello di EA8: invio mensile a Consip del dettaglio delle fatture (numero, data, ID dell'ordine, imponibile); in 35 non compaiono campi per ente, prodotto o marchio; in quello di System Management 3 (ID 2275, flussi di monitoraggio) compaiono campi per ente e prodotto (da leggere) | V per EA8; R per gli altri |", "",
          "Il dettaglio per iniziativa e per ente è nelle [schede](/convenzioni/) e nei file "
          "[enti-campione](https://github.com/mxmap-it/analisi-spesa-ict/tree/main/report/convenzioni/enti-campione) e "
          "[fonti-non-ufficiali](https://github.com/mxmap-it/analisi-spesa-ict/tree/main/report/convenzioni/fonti-non-ufficiali), "
          "in un formato riusabile dal monitor dell'Amministrazione trasparente.", ""]
    L += ["", "## 4. Matrice", "",
         "La [griglia di tutte le iniziative](/convenzioni/griglia/) mostra cella per cella cosa è pubblico, cosa è reperito altrove, "
         "cosa manca e cosa è stato richiesto, con i riepiloghi in alto. L'[indice delle convenzioni](/convenzioni/) riporta il riquadro "
         "delle carenze di trasparenza.", "",
         f"Celle al {DT} (documenti) e BDNCP elaborato il {DT}.", "",
         "| Classe | Celle | Quota |", "|---|---|---|"]
    for k, n in (("pubblico", "pubblico (fonte ufficiale)"), ("altrove", "solo da fonte non ufficiale"), ("assente", "non individuato sulla pagina del bando"), ("ignoto", "non ancora verificato")):
        L.append(f"| {n} | {g['celle'].get(k, 0)} | {pct1(g['celle'].get(k, 0), tot_celle)} |")
    L += ["", "## 5. Convenzione per convenzione", "",
          "Le iniziative principali (attive, per valore). Indice = dati pubblici / dati attesi (13; 14 per PSN e SPC Cloud, con i progetti dei fabbisogni). "
          "«Non individuati» = non trovati sulla pagina del bando, con tipo dedotto dal nome dei file. Il PSN non ha una pagina Consip: le sue celle "
          "sono quasi tutte «non verificate», il che non significa assenza di carenze.", "",
          f"Fonti consultate il {DT}; valori BDNCP elaborati il {DT}.", "",
          "| Iniziativa | Soggetto | M€ 2024-25 | Pubblici | Altrove | Non individuati | Non verificati | Indice | Carenze accertate |",
          "|---|---|---|---|---|---|---|---|---|"]
    princ = sorted([k for k, p in pi.items() if p["stato"] == "attiva" and k not in FUORI_PERIMETRO], key=lambda k: -pi[k]["valore"])[:30]
    for k in princ:
        p = pi[k]
        L.append(f"| [{nomi[k][:70]}](/convenzioni/{k.lower()}/) | {TIPI[p['tipo']]} | {meur(p['valore'])} | {p['pubblico']} | {p['altrove']} | {p['assente']} | "
                 f"{p['ignoto']} | {round(100 * p['indice'])} % | {', '.join(p['carenze_verificate']) or '–'} |")
    L += ["", f"Le altre {len(pi) - len(princ)} iniziative sono nell'[indice](/convenzioni/) e nella [griglia](/convenzioni/griglia/).", "",
          "## 6. Per tipo di soggetto", "",
          f"Fonti consultate il {DT}.", "",
          "| Soggetto | Iniziative | M€ 2024-25 | Indice medio | Non individuati | Non verificati |", "|---|---|---|---|---|---|"]
    for t, x in pt.items():
        ind = f"{round(100 * x['indice_medio'])} %" if t == "consip" else "n.d. (non ancora verificati)"
        L.append(f"| {TIPI[t]} | {x['iniziative']} | {meur(x['valore'])} | {ind} | {x['assenti']} | {x['ignoti']} |")
    L += ["", "Per aggregatori regionali e consorzi quasi tutti i dati sono «da verificare»: le loro piattaforme (Sintel, Intercent-ER, EmPULIA, START…) "
          "non sono ancora state visitate, i CIG padre non hanno link ai documenti in PVL (verificato: nessuno dei 295 CIG padre) e su TED "
          "l'abbinamento riesce solo per testo. **Un indice basso qui misura il nostro lavoro ancora da fare, non la loro trasparenza.**", "",
          "## 7. Metodo e limiti", "",
          "- **Fonti.** BDNCP ANAC (nostro mirror, sha256 nel manifest) per i CIG padre e derivati; pagine dei bandi su consip.it, consultate il 5/11/2026; "
          "TED; open data Consip degli ordini (dati.consip.it, file 2024-2025 archiviati il 5/11/2026); atti di enti aderenti trovati con ricerca online (fonte non ufficiale, archiviati con sha256).",
          "- **Verificato e riferito.** «Assente» vuol dire che abbiamo consultato la pagina ufficiale dell'iniziativa e il documento non c'è; il tipo di "
          "documento si deduce dal nome del file (controllo a mano solo per PRINCO). Le norme e i dati che non abbiamo letto sulla fonte sono marcati [R] "
          "nelle schede ([carenze.yaml](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/database/carenze.yaml)).",
          "- **Valori.** Somme di importi dichiarati in BDNCP: ordine di grandezza, non spesa né transato (seconda misura al § 2). La prima "
          f"iniziativa per valore pesa {meur(pi[top]['valore'])} M€ ({pct(pi[top]['valore'], g['valore_2024_2025'])} del totale).",
          f"- **Archivio.** {g['documenti_ufficiali']} documenti ufficiali collegati alle iniziative (compresi i file dentro gli zip), archiviati con sha256; "
          "una cella «pubblico» può contenerne molti.",
          "- **PVL.** Nessuno dei 295 CIG padre ha un link ai documenti di gara nei dati PVL scaricati il 3-4/11/2026 (verificato): è lo stato "
          "dei dati PVL, non un'assenza dei documenti, che gli aggregatori pubblicano sulle proprie piattaforme.",
         "- **Rumore nel censimento.** Il filtro per CPV ICT sui derivati lascia passare iniziative non ICT (es. ID 2638 Energia elettrica 21, 30 M€): "
         "restano in elenco finché il filtro non viene corretto, con peso trascurabile sul totale.",
         "- **Lettura dei documenti.** Letti per intero solo gli atti di PRINCO (ID 2928) e alcune determine di enti; per le altre iniziative "
         "le schede mostrano estratti automatici per parole chiave, marcati «da leggere».",
          "- **Aggregatori.** Ancora da verificare (sopra). Il tipo di soggetto si assegna con regole sul nome della stazione appaltante, da controvalidare "
          "con l'elenco ANAC dei soggetti aggregatori.",
          "- **Cosa non diciamo.** Che un dato assente sia nascosto di proposito; che un dato reperito presso un ente valga per tutta la convenzione.", "",
          "## 8. Rimedi", "",
          f"- **Accesso civico generalizzato** (art. 5 c. 2 d.lgs. 33/2013), come rimedio di breve periodo e solo dopo le fonti del § 3: "
          f"{g['istanze_preparate']} bozze necessarie (carenza accertata e dato utile all'imbuto: prodotti e marchi delle iniziative cloud e multibrand, "
          f"ordinativi delle più grandi, region e data center, erosione), {g['istanze_ritirate']} ritirate, {g['istanze_inviate']} inviate. [Registro](/convenzioni/accesso-civico/) e "
          "[analisi dei dinieghi](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/accesso-civico/analisi-dinieghi.md).",
          "- **Proposte di policy** (stato «proposta», nessuna inviata):"]
    for c in car:
        L.append(f"  - {c['id']} {c['titolo']} → {c['raccomandazione']}")
    L += ["", "## Registro delle revisioni", "", "| Versione | Data | Nota | Cosa è cambiato |", "|---|---|---|---|"]
    for s in reversed(storia):
        L.append(f"| {s['versione']} | {s['data']} | {s['nota']} | {'; '.join(s['cambiamenti'])[:600]} |")
    OUT.write_text("\n".join(migliaia(x) for x in L) + "\n", encoding="utf-8")
    print("rapporto", versione, "scritto;", "; ".join(diff)[:300])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
