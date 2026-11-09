#!/usr/bin/env python3
"""Revisione indipendente delle proposte della via 6 (G1/G3) prima che entrino nei totali (#55 #66, AGENTS § 3 controvalidazione).

Oggetto: le proposte di passaggio a «certo» di report/metodo/llm/imbuto-g1g3/verificati.jsonl, S1 escluso:
  S5  = asse A «escluso-certo» con ict != n (ICT non cloud);
  CC  = asse A «incluso-certo» (cloud certo; con asse B «incluso-certo» la giurisdizione è proposta).
Criteri deterministici (tutti necessari):
  C1 fonte primaria: almeno un atto archiviato (dati/atti/atti-server.jsonl, sha256, esito ok, pertinenza cig-citato)
     con il testo estratto presente in dati/atti/testi/ (ricontrollato qui, non preso dall'esito);
  C2 coerenza con le regole R/A/B: rieseguendo tools/llm/verifica_imbuto.verifica() sull'esito grezzo si ottengono
     gli stessi stati e la stessa confidenza; inoltre S5 -> e_cloud = n e ict = s; CC -> e_cloud = s;
  C3 (solo CC) prodotto identificato -> giurisdizione del prodotto: provider non vuoto, giurisdizione IT/UE/EXTRA-UE e,
     se il provider è nel dizionario config/marchi_cloud.yaml, giurisdizione uguale a quella del dizionario;
  C4 seconda lettura indipendente concorde (sotto).
Seconda lettura (C4): `claude -p --model opus` (modello diverso da Sonnet della via 6), istruzioni diverse
(report/metodo/llm/imbuto-revisione/istruzioni-revisione.md), CIECA (non vede la proposta), niente web: legge solo
gli estratti deterministici degli atti archiviati (finestre attorno al CIG). Ordine: importo decrescente.
Consumo in stato/claude-consumi.jsonl, etichetta «imbuto-revisione», attraverso tools/llm/claude_tetto.py (tetto
condiviso: codice 75 = tetto raggiunto -> ci si ferma, si riprende rilanciando `leggi`).
Concordanza: «concorde» se la lettura è certa (alta) e dice lo stesso stato (S5: non cloud e ICT; CC: cloud e, se
proposta, stessa giurisdizione); «non-confermato» se la lettura non è certa; «discorde» se dice il contrario
(in coda per Fabio con motivazione breve).
Entra nei totali solo C1 ∧ C2 ∧ C3 ∧ C4. Ogni passaggio si aggiunge al registro spesaict.classificazione/1
(dati/classificazioni/imbuto-revisione.jsonl: copia dei record di imbuto-g1g3.jsonl + passaggi di revisione).

Uso:
  python tools/verifiche/imbuto_via6_revisione.py prepara          # pacchetti ciechi + estratti (idempotente)
  python tools/verifiche/imbuto_via6_revisione.py leggi [N]        # seconda lettura, ripartibile (salta i fatti)
  python tools/verifiche/imbuto_via6_revisione.py esito AAAA-MM-GG # criteri, concordanza, numeri, coda, sezione per #66
"""
import collections
import csv
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

import yaml

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/llm"))
from verifica_imbuto import verifica  # noqa: E402

B = R / "report/metodo/llm/imbuto-g1g3"
RV = R / "report/metodo/llm/imbuto-revisione"
LAV = R / "lavoro/imbuto-revisione"
ISTR = RV / "istruzioni-revisione.md"
PACCO = 6
MAX_ESTRATTO = 12000


def jl(p):
    fs = sorted(p.glob("*.jsonl")) if p.is_dir() else ([p] if p.exists() else [])
    out = []
    for f in fs:
        for l in f.read_text(encoding="utf-8").splitlines():
            if l.strip():
                try:
                    out.append(json.loads(l))
                except json.JSONDecodeError:
                    pass
    return out


def strato(v):
    a = v["asse_a"]
    if a["stato"] == "escluso-certo":
        return "S1" if a.get("ict") == "n" else "S5"
    if a["stato"] == "incluso-certo":
        return "CC"
    return "S6"


def carica():
    lotti = {c["cig"]: c for c in jl(B / "lotti")}
    ver = {v["cig"]: v for v in jl(B / "verificati.jsonl")}
    grezzi = {e["cig"]: e for e in jl(B / "esiti") if e.get("cig") in lotti}
    atti = collections.defaultdict(list)
    for a in jl(R / "dati/atti/atti-server.jsonl"):
        if a.get("cig") in lotti:
            atti[a["cig"]].append(a)
    cand = sorted((v for v in ver.values() if strato(v) in ("S5", "CC")), key=lambda v: -lotti[v["cig"]]["importo"])
    return lotti, ver, grezzi, atti, cand


def docs_ok(lst):
    visti, out = set(), []
    for a in lst:
        if a.get("sha256") and a.get("esito_recupero") == "ok" and a["sha256"] not in visti:
            f = R / "dati/atti/testi" / f"{a['sha256']}.txt"
            if f.exists():
                visti.add(a["sha256"]); out.append((a, f))
    return out


def estratto(cig, docs):
    """Estratto deterministico: per ogni documento (prima i cig-citato) finestre di ±1.500 caratteri attorno al CIG,
    altrimenti l inizio del testo; tetto complessivo MAX_ESTRATTO caratteri."""
    parti, tot = [], 0
    for a, f in sorted(docs, key=lambda x: (x[0].get("pertinenza") != "cig-citato", x[0]["sha256"])):
        t = re.sub(r"\s+", " ", f.read_text(encoding="utf-8", errors="replace"))
        pos = [m.start() for m in re.finditer(re.escape(cig), t, re.I)][:3]
        fin = [(max(0, p - 1500), p + 1500) for p in pos] or [(0, 3000)]
        pezzi, fine = [], -1
        for s, e in fin:
            s = max(s, fine)
            if s < e:
                pezzi.append(t[s:e]); fine = e
        txt = " […] ".join(pezzi)
        spazio = MAX_ESTRATTO - tot
        if spazio <= 200:
            break
        txt = txt[:spazio]; tot += len(txt)
        parti.append({"sha256": a["sha256"], "url": a["url"], "pertinenza": a.get("pertinenza"), "testo": txt})
    return parti


def prepara():
    lotti, ver, grezzi, atti, cand = carica()
    (LAV / "pacchetti").mkdir(parents=True, exist_ok=True)
    righe = []
    for v in cand:
        c = lotti[v["cig"]]
        righe.append({"cig": c["cig"], "oggetto": c["testo"], "cpv": c["cpv"], "importo": c["importo"], "ente": c["ente"],
                      "aggiudicatari": c.get("aggiudicatari") or "", "estratti_atti": estratto(c["cig"], docs_ok(atti[c["cig"]]))})
    for i in range(0, len(righe), PACCO):
        (LAV / "pacchetti" / f"r{i // PACCO + 1:03d}.jsonl").write_text(
            "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in righe[i:i + PACCO]), encoding="utf-8")
    print(f"{len(righe)} candidati (S5 {sum(strato(v) == 'S5' for v in cand)}, CC {sum(strato(v) == 'CC' for v in cand)}) "
          f"in {-(-len(righe) // PACCO)} pacchetti ciechi -> {LAV / 'pacchetti'}")


def leggi(massimo=None):
    (RV / "esiti").mkdir(parents=True, exist_ok=True)
    (LAV / "log").mkdir(parents=True, exist_ok=True)
    istr = ISTR.read_text(encoding="utf-8")
    fatti = 0
    for p in sorted((LAV / "pacchetti").glob("r*.jsonl")):
        out = RV / "esiti" / p.name
        attesi = {json.loads(l)["cig"] for l in p.read_text(encoding="utf-8").splitlines() if l.strip()}
        if out.exists() and attesi <= {e.get("cig") for e in jl(out)}:
            continue
        tent = LAV / "log" / f"{p.stem}.tentativi"
        nt = int(tent.read_text()) if tent.exists() else 0
        if nt >= 2:
            continue  # due tentativi incompleti: i CIG mancanti restano «da-leggere» (STATO.md)
        if massimo is not None and fatti >= massimo:
            break
        prompt = istr + "\n\n## Contratti (JSONL)\n\n" + p.read_text(encoding="utf-8")
        env = dict(os.environ, TETTO_ETICHETTA="imbuto-revisione")
        env.pop("CLAUDE_CODE_OAUTH_TOKEN", None)
        r = subprocess.run(["nice", "-n", "15", str(R / ".venv/bin/python"), str(R / "tools/llm/claude_tetto.py"), "--progetto", "analisi-spesa-ict",
                            "--", "claude", "-p", "--model", "opus", "--disallowedTools", "Bash,WebSearch,WebFetch,Write,Edit,Read,Glob,Grep,Task"],
                           input=prompt, capture_output=True, text=True, env=env, cwd=R, timeout=3600)
        (LAV / "log" / f"{p.stem}.log").write_text(r.stdout + "\n--- stderr\n" + r.stderr, encoding="utf-8")
        if r.returncode == 75:
            print(f"TETTO RAGGIUNTO prima di {p.name}: riprendere con `leggi` più tardi"); return 75
        tent.write_text(str(nt + 1))
        righe = []
        for l in r.stdout.splitlines():
            l = l.strip().strip("`")
            if l.startswith("{") and '"cig"' in l:
                try:
                    e = json.loads(l)
                except json.JSONDecodeError:
                    continue
                if e.get("cig") in attesi:
                    e.update(modello="claude-opus", istruzioni="revisione-1", data=date.today().isoformat())
                    righe.append(e)
        out.write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in righe), encoding="utf-8")
        fatti += 1
        print(f"{p.name}: {len(righe)}/{len(attesi)} letture (codice {r.returncode})", flush=True)
    return 0


def marchi():
    m = {}
    for x in yaml.safe_load((R / "config/marchi_cloud.yaml").read_text(encoding="utf-8")):
        m.setdefault(x["provider"].lower(), x.get("giurisdizione"))
    return m


def c3(v, tab):
    b = v["asse_b"]; prov = (b.get("provider_prodotto") or "").strip(); g = b.get("giurisdizione")
    if b["stato"] != "incluso-certo":
        return True, "giurisdizione non proposta (resta incerta): C3 non richiesto per l asse A"
    if not prov or g not in ("IT", "UE", "EXTRA-UE"):
        return False, "provider o giurisdizione mancanti"
    for k, gt in tab.items():
        if re.search(r"\b" + re.escape(k) + r"\b", prov, re.I):
            return (gt == g), f"dizionario marchi: {k} -> {gt}"
    return True, "provider fuori dal dizionario marchi: giurisdizione dalla sola proposta, decide C4"


def concordanza(v, s, l):
    if not l:
        return "da-leggere", "seconda lettura non ancora fatta"
    ec, ict, cert, g = l.get("e_cloud"), l.get("ict"), l.get("certezza"), l.get("giurisdizione")
    if s == "S5":
        if ec == "s":
            return "discorde", f"la seconda lettura dice cloud: {l.get('evidenza', '')[:160]}"
        if ec == "n" and ict == "n":
            return "discorde", f"seconda lettura: non ICT (S1, non S5): {l.get('evidenza', '')[:160]}"
        if ec == "n" and ict == "s" and cert == "alta":
            return "concorde", ""
        return "non-confermato", "seconda lettura non certa"
    if ec == "n":
        return "discorde", f"la seconda lettura dice non cloud: {l.get('evidenza', '')[:160]}"
    if ec != "s" or cert != "alta":
        return "non-confermato", "seconda lettura non certa"
    if v["asse_b"]["stato"] == "incluso-certo":
        gp = v["asse_b"].get("giurisdizione")
        if g in ("IT", "UE", "EXTRA-UE") and g != gp:
            return "discorde", f"giurisdizione {gp} proposta, {g} in seconda lettura ({l.get('provider_prodotto', '')})"
        if g != gp:
            return "non-confermato", "cloud confermato, giurisdizione non confermata"
    return "concorde", ""


def esito(giorno):
    lotti, ver, grezzi, atti, cand = carica()
    tab = marchi()
    let = {e["cig"]: e for e in jl(RV / "esiti")}
    reg = {x["cig"]: x for x in jl(R / "dati/classificazioni/imbuto-g1g3.jsonl")}
    righe, coda, regout = [], [], []
    for v in cand:
        cig = v["cig"]; c = lotti[cig]; s = strato(v)
        dk = docs_ok(atti[cig]); citati = [a for a, _ in dk if a.get("pertinenza") == "cig-citato"]
        k1 = bool(citati)
        g = grezzi.get(cig)
        k2, n2 = False, "esito grezzo assente"
        if g:
            r2, _, _ = verifica(g, c, atti[cig])
            same = (r2["asse_a"]["stato"], r2["asse_b"]["stato"], r2["confidenza"]) == (v["asse_a"]["stato"], v["asse_b"]["stato"], v["confidenza"])
            coer = (v["asse_a"].get("e_cloud") == "n" and v["asse_a"].get("ict") == "s") if s == "S5" else v["asse_a"].get("e_cloud") == "s"
            k2, n2 = same and coer, ("ok" if same and coer else ("regole non idempotenti" if not same else "campi incoerenti con lo stato"))
        k3, n3 = c3(v, tab) if s == "CC" else (True, "non applicabile")
        k4, n4 = concordanza(v, s, let.get(cig))
        entra = k1 and k2 and k3 and k4 == "concorde"
        sotto = s if s == "S5" else ("CC-" + v["asse_b"].get("giurisdizione", "") if v["asse_b"]["stato"] == "incluso-certo" else "CC-giur-incerta")
        rr = {"cig": cig, "gruppo": c["gruppo"], "strato_proposto": sotto, "importo": c["importo"], "C1_fonte_primaria": k1, "C2_regole": k2, "C2_nota": n2,
              "C3_giurisdizione": k3, "C3_nota": n3, "C4_seconda_lettura": k4, "C4_nota": n4, "entra_nei_totali": entra,
              "provider_proposto": v["asse_b"].get("provider_prodotto", ""), "lettura": let.get(cig)}
        righe.append(rr)
        if k4 == "discorde" or (s == "CC" and not k3):
            coda.append(rr)
        x = reg.get(cig)
        if x:
            x = json.loads(json.dumps(x)); n = len(x["passaggi"])
            x["passaggi"].append({"n": n + 1, "tipo": "verifica", "strumento": "tools/verifiche/imbuto_via6_revisione.py", "versione": "revisione-1",
                                  "parametri": {"criteri": "C1 C2 C3"}, "risultato": {"C1": k1, "C2": k2, "C3": k3, "nota": n2 + "; " + n3}, "data": giorno})
            if let.get(cig):
                x["passaggi"].append({"n": n + 2, "tipo": "revisione", "strumento": "claude-opus (claude -p, abbonamento)", "versione": "istruzioni revisione-1 (cieca, solo atti archiviati)",
                                      "parametri": {"etichetta_consumi": "imbuto-revisione"}, "risultato": {k: let[cig].get(k) for k in ("e_cloud", "ict", "provider_prodotto", "giurisdizione", "certezza", "evidenza", "sha256")},
                                      "data": let[cig].get("data")})
            x["revisione"] = {"stato": "controvalidato" if entra else ("discorde" if k4 == "discorde" else "da-rivedere"),
                              "nota": f"revisione via 6 {giorno}: C1={k1} C2={k2} C3={k3} C4={k4}" + (f" ({n4})" if n4 else "")}
            regout.append(x)
    (R / "dati/classificazioni/imbuto-revisione.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in regout), encoding="utf-8")
    agg = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0.0]))
    for r in righe:
        for chiave in ("proposti", "C1", "C1+C2", "C1+C2+C3", "entra (C1-C4)"):
            ok = {"proposti": True, "C1": r["C1_fonte_primaria"], "C1+C2": r["C1_fonte_primaria"] and r["C2_regole"],
                  "C1+C2+C3": r["C1_fonte_primaria"] and r["C2_regole"] and r["C3_giurisdizione"], "entra (C1-C4)": r["entra_nei_totali"]}[chiave]
            if ok:
                for gg in (r["gruppo"], "tutti"):
                    agg[f"{gg} {r['strato_proposto']}"][chiave][0] += 1; agg[f"{gg} {r['strato_proposto']}"][chiave][1] += r["importo"]
    conc = collections.Counter(r["C4_seconda_lettura"] for r in righe)
    letti = [r for r in righe if r["C4_seconda_lettura"] != "da-leggere"]
    T = {"data": giorno, "strumento": "tools/verifiche/imbuto_via6_revisione.py", "candidati": len(righe),
         "letti": len(letti), "concordanza": dict(conc),
         "accordo_sui_letti_certi": {"concordi": conc["concorde"], "discordi": conc["discorde"]},
         "per_strato": {k: {kk: {"cig": vv[0], "euro": round(vv[1])} for kk, vv in d.items()} for k, d in sorted(agg.items())},
         "coda_discordi": len(coda), "righe": righe}
    o = R / "esiti" / giorno / "imbuto"; o.mkdir(parents=True, exist_ok=True)
    (o / "revisione-via6.json").write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(o / "revisione-coda-discordi.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["cig", "gruppo", "strato_proposto", "importo", "provider_proposto", "C1", "C3_nota", "seconda_lettura", "motivazione"])
        for r in sorted(coda, key=lambda r: -r["importo"]):
            l = r["lettura"] or {}
            w.writerow([r["cig"], r["gruppo"], r["strato_proposto"], round(r["importo"]), r["provider_proposto"], r["C1_fonte_primaria"], r["C3_nota"],
                        f"cloud={l.get('e_cloud')} ict={l.get('ict')} {l.get('provider_prodotto', '')} {l.get('giurisdizione', '')} ({l.get('certezza')})", r["C4_nota"] or r["C3_nota"]])
    sezione(T, o, agg, coda)
    fmt = lambda x: f"{x:,.0f}".replace(",", ".")
    print(f"candidati {len(righe)}, letti {len(letti)}, concordanza {dict(conc)}, coda {len(coda)}")
    for k, d in sorted(agg.items()):
        print(f"  {k}: " + "; ".join(f"{kk} {vv[0]} CIG {fmt(vv[1])} €" for kk, vv in d.items()))
    return T


def sezione(T, o, agg, coda):
    """Sezione pronta per il rendiconto imbuto (#66): non modifica il rendiconto."""
    eu = lambda x: (f"{x / 1e9:.2f} mld" if x >= 1e9 else f"{x / 1e6:.1f} M€").replace(".", ",")
    nomi = {"S5": "verso S5 (ICT non cloud)", "CC-IT": "cloud certo, IT", "CC-UE": "cloud certo, UE", "CC-EXTRA-UE": "cloud certo, extra-UE",
            "CC-giur-incerta": "cloud certo, giurisdizione incerta"}
    L = [f"### 4.3.2 Revisione delle proposte della via 6 ({T['data']})", "",
         f"Revisione indipendente (AGENTS § 3) delle {T['candidati']} proposte di passaggio a «certo» della via 6, S1 escluso "
         "(verso S5 e cloud certo), con `tools/verifiche/imbuto_via6_revisione.py`. Una proposta entra nei totali solo se: "
         "C1 ha una fonte primaria (atto archiviato con sha256 il cui testo cita il CIG); C2 le regole R/A/B di `verifica_imbuto.py` "
         "rieseguite danno lo stesso esito e i campi sono coerenti con lo stato; C3 per il cloud, il prodotto identificato porta alla "
         "giurisdizione del dizionario dei marchi (`config/marchi_cloud.yaml`); C4 una seconda lettura cieca (Claude Opus, istruzioni diverse, "
         "solo gli estratti degli atti archiviati, niente web) dice la stessa cosa con certezza alta. "
         f"Esito `esiti/{T['data']}/imbuto/revisione-via6.json`, coda `revisione-coda-discordi.csv` [V].", "",
         f"**Seconda lettura:** {T['letti']} su {T['candidati']} candidati letti; esiti {T['concordanza']}."
         + ("" if T["letti"] == T["candidati"] else " **PARZIALE**: i non letti restano fuori dai totali."), "",
         "| gruppo e strato proposto | proposti | C1 fonte primaria | C1+C2+C3 | entra nei totali (C1-C4) |", "|---|---:|---:|---:|---:|"]
    for k in sorted(agg):
        g, st = k.split(" ", 1)
        d = agg[k]
        f = lambda kk: f"{d[kk][0]} CIG, {eu(d[kk][1])}" if d[kk][0] else "0"
        L.append(f"| {g} {nomi.get(st, st)} | {f('proposti')} | {f('C1')} | {f('C1+C2+C3')} | {f('entra (C1-C4)')} |")
    L += ["", f"- **Casi discordi in coda per Fabio:** {len(coda)} (`revisione-coda-discordi.csv`, con motivazione breve).",
          "- **Cosa resta fuori:** le proposte senza fonte primaria (C1) restano proposte da rivedere anche se la seconda lettura concorda: "
          "senza un atto che cita il CIG la classificazione si regge su ricerche e deduzioni.",
          "- Il gruppo CTL è di controllo e non si somma a G1 e G3; la riga «tutti» li comprende.", ""]
    (o / "revisione-per-66.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "esito"
    if cmd == "prepara":
        prepara()
    elif cmd == "leggi":
        sys.exit(leggi(int(sys.argv[2]) if len(sys.argv) > 2 else None))
    else:
        esito(sys.argv[2] if len(sys.argv) > 2 else date.today().isoformat())
