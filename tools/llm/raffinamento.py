#!/usr/bin/env python3
"""Raffinamento a livelli sopra l'imbuto (decisione di Fabio del 18/11/2026, #71): l'imbuto resta LARGO (nessuna
esclusione a regola dei CIG che entrano per «sw» o «connettività»); sopra si aggiungono passaggi di esclusione
sempre più costosi, ciascuno registrato, che NON modificano lavoro/imbuto/ict.csv ma producono una tabella di
spostamenti per CIG (esiti/<data>/imbuto/raffinamento-*.csv) da applicare come strato.

Livelli (sul residuo S6 dal 2024 dell'imbuto 0.3.4):
  L2  regole (deciso da Fabio il 18/11): stampanti, multifunzione, fotocopiatrici, toner e consumabili, cablaggio di
      rete -> fuori dalla misura cloud (asse A escluso-certo, resta ICT non cloud), salvo che il testo nomini un servizio
      cloud (RX_CLOUD). Campione di 40 a seme fisso da giudicare a mano (precisione della regola).
  L3  lettura con un modello più potente (Claude Opus, `claude -p`, nessuno strumento, solo il testo ANAC: oggetto,
      CPV, ente, aggiudicatari, importo) dei CIG entrati per soli segnali deboli («sw», «connettività»), esclusi quelli
      già presi da L2 e quelli della via 6. Un CIG esce solo con certezza alta; gli altri restano incerti e passano al
      livello successivo (L4: via 6 con ricerca degli atti, modello con web).
Consumo in stato/claude-consumi.jsonl (etichetta «raffinamento-l3») attraverso tools/llm/claude_tetto.py (tetto condiviso:
codice 75 -> ci si ferma, si riprende rilanciando).

Uso (sul server, nice):
  python tools/llm/raffinamento.py l2 [AAAA-MM-GG]          # tabella L2 + campione
  python tools/llm/raffinamento.py prepara-l3 [G3|G4|tutti]  # pacchetti ciechi, idempotente (salta i CIG già impacchettati)
  python tools/llm/raffinamento.py leggi-l3 [N]              # lettura Opus, ripartibile
  python tools/llm/raffinamento.py esito [AAAA-MM-GG]        # tabella L3, riepilogo dei livelli
  python tools/llm/raffinamento.py prepara-l4 AAAA-MM-GG      # lotti L4 (formato via 6) in report/metodo/llm/raffinamento-l4/lotti
  L4: GIRO_DIR=report/metodo/llm/raffinamento-l4 GIRO_LOG=log/raffinamento-l4 MODELLO=opus PAR=2 tools/llm/giro_imbuto.sh
      (via 6 con ricerca e archiviazione degli atti, modello più potente). Ingressi: i casi discordi della revisione C1-C4
      non risolti da L2 (arbitro) e i CIG che L3 lascia incerti o dice cloud.
"""
import collections, csv, hashlib, json, os, re, subprocess, sys
from datetime import date
from pathlib import Path

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools" / "analisi"))
from imbuto import RX_ICT  # noqa: E402

ICT = R / "lavoro/imbuto/ict.csv"
LAV = R / "lavoro/raffinamento"
RV = R / "report/metodo/llm/raffinamento"
ISTR = RV / "istruzioni-l3.md"
VIA6 = R / "report/metodo/llm/imbuto-g1g3/lotti"
PACCO = 10
SEME = "raffinamento-l2-20261118"
csv.field_size_limit(1 << 30)

RX_PERIF = re.compile(r"stampant|multifunzion|fotocopiat|\btoner|cartucc|consumabil|materiale\s+di\s+consumo|cablaggi|"
                      r"rete\s+dati\s+e\s+fonia|plotter", re.I)
RX_CLOUD = re.compile(r"cloud|saas|iaas|paas|hosting|data\s*cent|datacent|piattaforma\s+(?:web|online)|in\s+remoto|\bpsn\b", re.I)


def norm(s):
    return re.sub(r"\W", "", s.lower().replace("à", "a"))


def debole(s):
    return s == "sw" or s.startswith("connettivit")


def s6_dal_2024():
    for r in csv.DictReader(open(ICT, encoding="utf-8")):
        if r["strato"] == "S6-residuo" and int(r["anno"]) >= 2024:
            yield r


def l2_regola(r):
    return bool(RX_PERIF.search(r["testo"])) and not RX_CLOUD.search(r["testo"])


def solo_deboli(r):
    segn = {norm(m.group(0)) for m in RX_ICT.finditer(r["testo"])}
    return r["sottoclasse"] == "cpv-non-ict-testo-ict" and bool(segn) and all(debole(s) for s in segn)


# giudizi a mano del campione L2 (cig -> (giudizio, nota)); giudizio: «giusto» = né cloud né da misurare come cloud,
# «sbagliato» = il contratto compra (anche) un servizio cloud; si compila dopo la prima estrazione
# 18/11/2026, Claude sul testo ANAC: 40 su 40 non comprano cloud; 6 non sono nemmeno ICT
GIUDIZI_L2 = {
    "B9FE956095": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B02FBF3FED": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B29FD20709": ("giusto", "carta per fotocopie (non ICT)"),
    "BC9F29DD3D": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B10331AD88": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B621BDA348": ("giusto", "stampante 3D di laboratorio (non ICT)"),
    "BBFC92A498": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B16FD66A74": ("giusto", "cancelleria (non ICT)"),
    "B73D4E488B": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B3257B5759": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B5FB7048DA": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B7D720CB33": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B067F18F4C": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B065573194": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B8F1F22349": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B9FA5303AF": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B8F66AFEF0": ("giusto", "apparecchi e consumabili medici (non ICT)"),
    "B78E4A41F4": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B2B9E3BBD9": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "BC603B82D8": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B0B1C2626D": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B7C4DC8BC8": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B0AA9D080D": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B5EDAA1A6B": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B985D28463": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B8560FC6C3": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "BCD63D40D6": ("giusto", "carta (non ICT)"),
    "B1A9DF9316": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B692746E5B": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B77ED6AD61": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "BB148FAFB5": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B839368EBC": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B139E1E37E": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "BC1563D1A8": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "BAD259631A": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "BB8EA94972": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B261109D22": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B8D009BE18": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "B43D660145": ("giusto", "stampanti, consumabili o noleggio: ICT non cloud"),
    "BBDFA74D40": ("giusto", "carta (non ICT)"),
}


def l2(data):
    out = R / f"esiti/{data}/imbuto"; out.mkdir(parents=True, exist_ok=True)
    righe, tot = [], collections.defaultdict(lambda: [0, 0.0])
    for r in s6_dal_2024():
        g = r["gruppo"][:2]; imp = float(r["importo"] or 0)
        tot[("S6", g)][0] += 1; tot[("S6", g)][1] += imp
        if l2_regola(r):
            tot[("L2", g)][0] += 1; tot[("L2", g)][1] += imp
            righe.append({"cig": r["cig"], "anno": r["anno"], "gruppo": r["gruppo"], "importo": imp, "cod_cpv": r["cod_cpv"],
                          "motivo": RX_PERIF.search(r["testo"]).group(0).lower(), "ente": r["stazione_appaltante"], "testo": r["testo"][:300]})
    with open(out / "raffinamento-l2.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(righe[0])); w.writeheader(); w.writerows(righe)
    cam = sorted(righe, key=lambda x: hashlib.sha256((x["cig"] + SEME).encode()).hexdigest())[:40]
    with open(out / "raffinamento-l2-campione.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(righe[0]) + ["giudizio", "nota"]); w.writeheader()
        for x in sorted(cam, key=lambda x: -x["importo"]):
            g, n = GIUDIZI_L2.get(x["cig"], ("", "")); w.writerow(dict(x, giudizio=g, nota=n))
    J = {"data": data, "imbuto": "0.3.4", "ict_csv_sha256": hashlib.sha256(open(ICT, "rb").read()).hexdigest(),
         "regola": "L2: RX_PERIF (stampanti, consumabili, cablaggio) e non RX_CLOUD -> fuori dalla misura cloud (decisione di Fabio 18/11)",
         "rx_perif": RX_PERIF.pattern, "rx_cloud": RX_CLOUD.pattern,
         "per_gruppo": [{"livello": k[0], "gruppo": k[1], "cig": v[0], "euro": round(v[1])} for k, v in sorted(tot.items())],
         "campione": {"n": len(cam), "giudizi": dict(collections.Counter(GIUDIZI_L2.get(x["cig"], ("non-giudicato",))[0] for x in cam))}}
    json.dump(J, open(out / "raffinamento-l2.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(J, ensure_ascii=False, indent=1))


def gia_impacchettati():
    s = set()
    for f in (LAV / "pacchetti").glob("d*.jsonl"):
        s |= {json.loads(l)["cig"] for l in f.read_text(encoding="utf-8").splitlines() if l.strip()}
    return s


def prepara_l3(quali):
    (LAV / "pacchetti").mkdir(parents=True, exist_ok=True)
    via6 = {json.loads(l)["cig"] for f in VIA6.glob("*.jsonl") for l in f.read_text(encoding="utf-8").splitlines() if l.strip()}
    gia = gia_impacchettati()
    gruppi = ("G3", "G4") if quali == "tutti" else (quali,)
    sel = [r for r in s6_dal_2024() if r["gruppo"][:2] in gruppi and solo_deboli(r) and not l2_regola(r)
           and r["cig"] not in via6 and r["cig"] not in gia]
    sel.sort(key=lambda r: -float(r["importo"] or 0))
    n0 = len(list((LAV / "pacchetti").glob("d*.jsonl")))
    for i in range(0, len(sel), PACCO):
        righe = [{"cig": r["cig"], "oggetto": r["testo"][:600], "cpv": r["cod_cpv"], "importo": float(r["importo"] or 0),
                  "ente": r["stazione_appaltante"], "aggiudicatari": r["aggiudicatari"][:200]} for r in sel[i:i + PACCO]]
        (LAV / "pacchetti" / f"d{n0 + i // PACCO + 1:04d}.jsonl").write_text(
            "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in righe), encoding="utf-8")
    print(len(sel), "CIG", round(sum(float(r["importo"] or 0) for r in sel) / 1e6, 1), "M€ in", -(-len(sel) // PACCO), "pacchetti da", f"d{n0 + 1:04d}")


def jl(p):
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


def leggi_l3(massimo=None):
    (RV / "esiti").mkdir(parents=True, exist_ok=True); (LAV / "log").mkdir(parents=True, exist_ok=True)
    istr = ISTR.read_text(encoding="utf-8"); fatti = 0
    for p in sorted((LAV / "pacchetti").glob("d*.jsonl")):
        out = RV / "esiti" / p.name
        attesi = {e["cig"] for e in jl(p)}
        if out.exists() and attesi <= {e.get("cig") for e in jl(out)}: continue
        tent = LAV / "log" / f"{p.stem}.tentativi"; nt = int(tent.read_text()) if tent.exists() else 0
        if nt >= 2: continue
        if massimo is not None and fatti >= massimo: break
        env = dict(os.environ, TETTO_ETICHETTA="raffinamento-l3"); env.pop("CLAUDE_CODE_OAUTH_TOKEN", None)
        r = subprocess.run(["nice", "-n", "15", str(R / ".venv/bin/python"), str(R / "tools/llm/claude_tetto.py"), "--progetto", "analisi-spesa-ict",
                            "--", "claude", "-p", "--model", "opus", "--disallowedTools", "Bash,WebSearch,WebFetch,Write,Edit,Read,Glob,Grep,Task"],
                           input=istr + "\n\n## Contratti (JSONL)\n\n" + p.read_text(encoding="utf-8"),
                           capture_output=True, text=True, env=env, cwd=R, timeout=3600)
        (LAV / "log" / f"{p.stem}.log").write_text(r.stdout + "\n--- stderr\n" + r.stderr, encoding="utf-8")
        if r.returncode == 75:
            print(f"TETTO RAGGIUNTO prima di {p.name}: riprendere più tardi"); return 75
        tent.write_text(str(nt + 1)); righe = []
        for l in r.stdout.splitlines():
            l = l.strip().strip("`")
            if l.startswith("{") and '"cig"' in l:
                try: e = json.loads(l)
                except json.JSONDecodeError: continue
                if e.get("cig") in attesi:
                    e.update(modello="claude-opus", istruzioni="raffinamento-l3-1", data=date.today().isoformat()); righe.append(e)
        out.write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in righe), encoding="utf-8")
        fatti += 1
        print(f"{p.name}: {len(righe)}/{len(attesi)} (codice {r.returncode})", flush=True)
    return 0


def esito(data):
    out = R / f"esiti/{data}/imbuto"; out.mkdir(parents=True, exist_ok=True)
    ing = {}
    for p in sorted((LAV / "pacchetti").glob("d*.jsonl")):
        for e in jl(p): ing[e["cig"]] = e
    let = {}
    for p in sorted((RV / "esiti").glob("d*.jsonl")):
        for e in jl(p): let[e["cig"]] = e
    agg = collections.defaultdict(lambda: [0, 0.0]); righe = []
    for c, x in ing.items():
        e = let.get(c)
        if e is None: k = "da-leggere"
        elif e.get("certezza") == "alta" and e.get("categoria") in ("non-ict", "ict-non-cloud"): k = "esce-" + e["categoria"]
        elif e.get("certezza") == "alta" and e.get("categoria") == "ict-cloud": k = "cloud-da-L4"
        else: k = "resta-incerto-L4"
        agg[k][0] += 1; agg[k][1] += x["importo"]
        righe.append({"cig": c, "importo": x["importo"], "esito_l3": k, "categoria": (e or {}).get("categoria", ""),
                      "certezza": (e or {}).get("certezza", ""), "evidenza": (e or {}).get("evidenza", ""), "oggetto": x["oggetto"][:200]})
    with open(out / "raffinamento-l3.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(righe[0]) if righe else ["cig"]); w.writeheader(); w.writerows(righe)
    J = {"data": data, "pacchetti": len(list((LAV / "pacchetti").glob("d*.jsonl"))), "cig": len(ing), "letti": len(let),
         "esiti": {k: {"cig": v[0], "euro": round(v[1])} for k, v in sorted(agg.items())}}
    json.dump(J, open(out / "raffinamento-l3.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(J, ensure_ascii=False, indent=1))


def prepara_l4(data):
    L4 = R / "report/metodo/llm/raffinamento-l4/lotti"; L4.mkdir(parents=True, exist_ok=True)
    gia = {json.loads(l)["cig"] for f in L4.glob("*.jsonl") for l in f.read_text(encoding="utf-8").splitlines() if l.strip()}
    l2 = {r["cig"] for r in csv.DictReader(open(R / f"esiti/{data}/imbuto/raffinamento-l2.csv", encoding="utf-8"))}
    voglio = {}
    disc = R / f"esiti/{data}/imbuto/revisione-coda-discordi.csv"
    if disc.exists():
        for r in csv.DictReader(open(disc, encoding="utf-8")):
            # all'arbitro solo i disaccordi sull'asse cloud: una delle due letture dice cloud. Se entrambe dicono «non cloud»
            # (es. connettività che la revisione chiama non ICT) il CIG è fuori dalla misura cloud comunque.
            cloud = r["strato_proposto"].startswith("CC") or "cloud=s" in r["seconda_lettura"]
            if cloud and r["cig"] not in l2 and not (RX_PERIF.search(r["motivazione"]) and not RX_CLOUD.search(r["motivazione"])):
                voglio[r["cig"]] = "arbitro-discorde-cloud"
    l3 = R / f"esiti/{data}/imbuto/raffinamento-l3.csv"
    if l3.exists():
        for r in csv.DictReader(open(l3, encoding="utf-8")):
            if r["esito_l3"] in ("resta-incerto-L4", "cloud-da-L4"): voglio.setdefault(r["cig"], r["esito_l3"])
    link = {}
    for r in csv.DictReader(open(R / "lavoro/pvl/cig_link.csv", encoding="utf-8")):
        if r.get("link") and r["cig"] in voglio: link.setdefault(r["cig"], r["link"])
    righe = {}
    for r in csv.DictReader(open(ICT, encoding="utf-8")):
        c = r["cig"]
        if c in voglio and c not in gia and c not in righe:
            righe[c] = {"cig": c, "gruppo": "L4", "motivo_l4": voglio[c], "anno": int(r["anno"]), "sottoclasse": r["sottoclasse"],
                        "cpv": r["cod_cpv"], "importo": float(r["importo"] or 0), "importo_da_verificare": r["importo_da_verificare"] in ("1", "True", "true"),
                        "ente": r["stazione_appaltante"], "aggiudicatari": r["aggiudicatari"], "testo": r["testo"],
                        "link_documenti": link.get(c, ""), "regole_v31": {"via": r["via"], "provider": r["provider"],
                        "giurisdizione": r["giurisdizione"], "servizio": r["servizio"]}, "controllo": False}
    sel = sorted(righe.values(), key=lambda x: -x["importo"])
    n0 = len(list(L4.glob("l4-*.jsonl")))
    for i in range(0, len(sel), 2):
        (L4 / f"l4-{n0 + i // 2 + 1:03d}.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in sel[i:i + 2]), encoding="utf-8")
    fuori = sorted(set(voglio) - set(righe) - gia)
    print(len(sel), "CIG in", -(-len(sel) // 2), "lotti L4;", collections.Counter(x["motivo_l4"] for x in sel), "; non in S3-S6 di ict.csv:", fuori)


if __name__ == "__main__":
    a = sys.argv[1:] or ["l2"]
    if a[0] == "l2": l2(a[1] if len(a) > 1 else date.today().isoformat())
    elif a[0] == "prepara-l3": prepara_l3(a[1] if len(a) > 1 else "G3")
    elif a[0] == "leggi-l3": sys.exit(leggi_l3(int(a[1]) if len(a) > 1 else None))
    elif a[0] == "esito": esito(a[1] if len(a) > 1 else date.today().isoformat())
    elif a[0] == "prepara-l4": prepara_l4(a[1])
