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
         "istanze_preparate": sum(1 for r in reg if r["stato"] == "preparata"), "istanze_inviate": sum(1 for r in reg if r["stato"] != "preparata"),
         "istanze_con_risposta": sum(1 for r in reg if r.get("risposta")),
         "flusso_dati": sum(1 for v in voci if v.get("evidenze_dato_esistente")),
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
    for k in ("istanze_inviate", "istanze_con_risposta"):
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
         f"date: {data}",
         'description: "Stato della trasparenza delle principali convenzioni e accordi quadro ICT (Consip, PSN, soggetti aggregatori): documenti pubblici, dati assenti, valore non verificabile, rimedi."',
         "---", "",
         "<!-- Generato da tools/convenzioni/rapporto.py dalla base dati: non modificare a mano. -->", "",
         f"**Versione {versione} del {data}** · [registro delle revisioni](#registro-delle-revisioni) · **bozza da presentare a Fabio Pietrosanti prima di ogni diffusione esterna**", "",
         "Ogni numero viene dalla base dati `report/convenzioni/database/` e si rifà con `python tools/verifiche/convenzioni_rapporto.py`.", "",
         "## 1. Sintesi", "",
         f"- **Perimetro.** {g['iniziative']} iniziative ICT ({g['attive']} attive): Consip, PSN, soggetti aggregatori regionali, consorzi e altre "
         f"stazioni appaltanti con più contratti derivati. Criterio nel [README della base dati](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/database/README.md).",
         f"- **Valore.** I contratti derivati con CPV ICT pubblicati nel 2024-2025 dichiarano in BDNCP circa **{meur(g['valore_2024_2025'])} M€**. "
         "È un ordine di grandezza, non la spesa: alcuni attuativi riportano il massimale dell'accordo quadro invece del valore del contratto.",
         f"- **Visibilità.** Dei {tot_celle} dati attesi (iniziativa × tipo di documento o dato), sono pubblici dalla fonte ufficiale "
         f"{g['celle'].get('pubblico', 0)} ({pct(g['celle'].get('pubblico', 0), tot_celle)}); reperibili solo altrove {g['celle'].get('altrove', 0)}; "
         f"assenti (verificato) {g['celle'].get('assente', 0)} ({pct(g['celle'].get('assente', 0), tot_celle)}); ancora da verificare "
         f"{g['celle'].get('ignoto', 0)} ({pct(g['celle'].get('ignoto', 0), tot_celle)}). Indice di visibilità medio: **{round(100 * g['indice_medio'])} %**.",
         f"- **Valore non ben visibile.** {g['iniziative_ben_visibili']} iniziative su {g['iniziative']} pubblicano tutti e quattro i dati che servono a "
         f"controllare spesa e sovranità (offerte tecnica ed economica, transato, ordinativi) nella fonte ufficiale dell'iniziativa. Il valore delle altre è circa "
         f"**{meur(g['valore_non_ben_visibile'])} M€**, cioè {pct(g['valore_non_ben_visibile'], g['valore_2024_2025'])} del totale; per {g['celle'].get('ignoto', 0)} dati "
         "la verifica non è ancora fatta, quindi è un limite superiore provvisorio.",
         f"- **Concentrazione.** La prima iniziativa per valore ({nomi[top][:80]}) pesa {meur(pi[top]['valore'])} M€, "
         f"{pct(pi[top]['valore'], g['valore_2024_2025'])} del totale: il dato è dominato da pochi accordi quadro e da importi che sono massimali.",
         "- **Carenze principali.** Offerte dei vincitori, listini offerti, transato per lotto e marchio, elenco degli ordinativi: non pubblicati "
         "dalla centrale su nessuna delle pagine Consip consultate (gli ordinativi si trovano, in parte, negli atti dei singoli enti aderenti). Region e data center: dichiarati in gara (verificato per IaaS/PaaS 2 e PRINCO), non pubblicati.",
         f"- **Il dato esiste.** Per {g['flusso_dati']} iniziative la documentazione di gara prevede che il fornitore trasmetta a Consip i flussi "
         "del fatturato (d.m. MEF 23/11/2012, commissioni): il transato è quindi presso Consip, ma non è pubblicato per lotto né per marchio.",
         f"- **Rimedi.** {g['istanze_preparate']} bozze di accesso civico generalizzato preparate e **non inviate**; proposte di policy R08 e R37-R42 "
         "perché questi dati diventino pubblici senza bisogno di chiederli.", "",
         "## 2. Due misure del valore", "",
         f"Per {g['od_iniziative']} iniziative Consip il valore si può misurare anche con gli **open data Consip** degli ordini diretti "
         f"(dati.consip.it, 2024 e 2025, file archiviati con sha256): **{meur(g['od_ordinato'])} M€** ordinati, contro **{meur(g['od_bdncp'])} M€** "
         "dichiarati in BDNCP per i loro CIG derivati ICT 2024-2025. Le due misure non sono la stessa grandezza: gli open data contano solo "
         "gli ordini diretti (non gli appalti specifici con rilancio competitivo) e l'anno dell'ordine, BDNCP l'importo dichiarato all'acquisizione "
         "del CIG (spesso il massimale). La distanza conferma che la somma BDNCP va letta come ordine di grandezza; per l'ID 2483 il rapporto è "
         "di circa 13 a 1. Gli open data non riportano listino, marchio né ente: la carenza C3 resta.", "",
         "| Iniziativa | M€ BDNCP 2024-25 | M€ ordinati 2024+2025 (open data Consip) | Abbinamento |", "|---|---|---|---|"]
    for v in sorted([v for v in voci if v.get("ordinato_consip")], key=lambda v: -(v["valore_ict_2024_2025"] or 0)):
        o = v["ordinato_consip"]
        L.append(f"| [{v['nome'][:60]}](/convenzioni/{v['id'].lower()}/) | {meur(v['valore_ict_2024_2025'] or 0)} | {meur(o['2024'] + o['2025'])} | "
                 f"{'; '.join(n.split(' [')[1].rstrip(']')[:40] for n in o['nomi'])} |")
    L += ["", "## 3. Matrice", "",
         "La [griglia di tutte le iniziative](/convenzioni/griglia/) mostra cella per cella cosa è pubblico, cosa è reperito altrove, "
         "cosa manca e cosa è stato richiesto, con i riepiloghi in alto. L'[indice delle convenzioni](/convenzioni/) riporta il riquadro "
         "delle carenze di trasparenza.", "",
         "| Classe | Celle | Quota |", "|---|---|---|"]
    for k, n in (("pubblico", "pubblico (fonte ufficiale)"), ("altrove", "solo da fonte non ufficiale"), ("assente", "assente (verificato)"), ("ignoto", "da verificare")):
        L.append(f"| {n} | {g['celle'].get(k, 0)} | {pct(g['celle'].get(k, 0), tot_celle)} |")
    L += ["", "## 4. Convenzione per convenzione", "",
          "Le iniziative principali (attive, per valore). Indice = dati pubblici / dati attesi; «ben visibile» = offerte, transato e ordinativi tutti pubblici.", "",
          "| Iniziativa | Soggetto | M€ 2024-25 | Pubblici | Altrove | Assenti | Da verificare | Indice | Ben visibile | Carenze verificate |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    princ = sorted([k for k, p in pi.items() if p["stato"] == "attiva"], key=lambda k: -pi[k]["valore"])[:30]
    for k in princ:
        p = pi[k]
        L.append(f"| [{nomi[k][:70]}](/convenzioni/{k.lower()}/) | {TIPI[p['tipo']]} | {meur(p['valore'])} | {p['pubblico']} | {p['altrove']} | {p['assente']} | "
                 f"{p['ignoto']} | {round(100 * p['indice'])} % | {'sì' if p['ben_visibile'] else 'no'} | {', '.join(p['carenze_verificate']) or '–'} |")
    L += ["", f"Le altre {len(pi) - len(princ)} iniziative sono nell'[indice](/convenzioni/) e nella [griglia](/convenzioni/griglia/).", "",
          "## 5. Per tipo di soggetto", "",
          "| Soggetto | Iniziative | M€ 2024-25 | Indice medio | Ben visibili | Dati assenti | Dati da verificare |", "|---|---|---|---|---|---|---|"]
    for t, x in pt.items():
        L.append(f"| {TIPI[t]} | {x['iniziative']} | {meur(x['valore'])} | {round(100 * x['indice_medio'])} % | {x['ben_visibili']} | {x['assenti']} | {x['ignoti']} |")
    L += ["", "Per aggregatori regionali e consorzi quasi tutti i dati sono «da verificare»: le loro piattaforme (Sintel, Intercent-ER, EmPULIA, START…) "
          "non sono ancora state visitate, i CIG padre non hanno link ai documenti in PVL (verificato: nessuno dei 295 CIG padre) e su TED "
          "l'abbinamento riesce solo per testo. **Un indice basso qui misura il nostro lavoro ancora da fare, non la loro trasparenza.**", "",
          "## 6. Metodo e limiti", "",
          "- **Fonti.** BDNCP ANAC (nostro mirror, sha256 nel manifest) per i CIG padre e derivati; pagine dei bandi su consip.it, consultate il 5/11/2026; "
          "TED; open data Consip degli ordini (dati.consip.it, file 2024-2025 archiviati il 5/11/2026); atti di enti aderenti trovati con ricerca online (fonte non ufficiale, archiviati con sha256).",
          "- **Verificato e riferito.** «Assente» vuol dire che abbiamo consultato la pagina ufficiale dell'iniziativa e il documento non c'è; il tipo di "
          "documento si deduce dal nome del file (controllo a mano solo per PRINCO). Le norme e i dati che non abbiamo letto sulla fonte sono marcati [R] "
          "nelle schede ([carenze.yaml](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/database/carenze.yaml)).",
          "- **Valori.** Somme di importi dichiarati in BDNCP: ordine di grandezza, non spesa né transato (confronto con gli open data Consip al § 2).",
         "- **Rumore nel censimento.** Il filtro per CPV ICT sui derivati lascia passare iniziative non ICT (es. ID 2638 Energia elettrica 21, 30 M€): "
         "restano in elenco finché il filtro non viene corretto, con peso trascurabile sul totale.",
         "- **Lettura dei documenti.** Letti per intero solo gli atti di PRINCO (ID 2928) e alcune determine di enti; per le altre iniziative "
         "le schede mostrano estratti automatici per parole chiave, marcati «da leggere».",
          "- **Aggregatori.** Ancora da verificare (sopra). Il tipo di soggetto si assegna con regole sul nome della stazione appaltante, da controvalidare "
          "con l'elenco ANAC dei soggetti aggregatori.",
          "- **Cosa non diciamo.** Che un dato assente sia nascosto di proposito; che un dato reperito presso un ente valga per tutta la convenzione.", "",
          "## 7. Rimedi", "",
          f"- **Accesso civico generalizzato** (art. 5 c. 2 d.lgs. 33/2013), come rimedio di breve periodo: {g['istanze_preparate']} bozze preparate, "
          f"{g['istanze_inviate']} inviate. [Registro](/convenzioni/accesso-civico/) e "
          "[analisi dei dinieghi](https://github.com/mxmap-it/analisi-spesa-ict/blob/main/report/convenzioni/accesso-civico/analisi-dinieghi.md).",
          "- **Proposte di policy** (stato «proposta», nessuna inviata):"]
    for c in car:
        L.append(f"  - {c['id']} {c['titolo']} → {c['raccomandazione']}")
    L += ["", "## Registro delle revisioni", "", "| Versione | Data | Nota | Cosa è cambiato |", "|---|---|---|---|"]
    for s in reversed(storia):
        L.append(f"| {s['versione']} | {s['data']} | {s['nota']} | {'; '.join(s['cambiamenti'])[:600]} |")
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("rapporto", versione, "scritto;", "; ".join(diff)[:300])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
