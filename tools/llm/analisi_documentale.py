#!/usr/bin/env python3
"""Runner neutro rispetto al fornitore per il prompt portabile di analisi documentale (#55 #66, richiesta di Fabio 7/11/2026).

Ingresso: CIG + testi dei documenti (con sha256). Uscita: JSON validato contro schemi/analisi-documentale.schema.json,
con le citazioni ricontrollate alla lettera nel testo. Solo libreria standard (jsonschema usato se già installato).

  analisi_documentale.py pacchetto [--n 50]       # SUL SERVER: pacchetto di riproduzione da report/metodo/llm/imbuto-g1g3
        -> report/metodo/llm/riproduzione/v1/ingressi/<CIG>.json + SHA256SUMS + manifest.json
  analisi_documentale.py esegui --fornitore stampa|claude-cli|openai --modello NOME [--url URL --chiave-env VAR] [--cig CIG...]
        stampa      scrive il prompt completo di ogni CIG in prompt/<CIG>.txt (da incollare in qualunque LLM, a mano)
        claude-cli  `claude -p` in abbonamento, senza strumenti (passa da tools/llm/claude_tetto.py)
        openai      qualunque endpoint compatibile /v1/chat/completions (vLLM, llama.cpp server, Ollama, OpenRouter, DeepSeek,
                    Qwen/DashScope, Mistral…): --url https://host/v1 --chiave-env NOME_VARIABILE (la chiave non passa mai da riga di comando)
        ollama      modello open-weight locale (es. qwen3-vl:8b), API nativa con num_ctx (NUM_CTX, default 32768)
        -> report/metodo/llm/riproduzione/v1/esiti-<modello>/<CIG>.json
  analisi_documentale.py importa --modello NOME FILE...   # risposte ottenute a mano (incollate): le valida e le registra
Confronto: tools/verifiche/concordanza_llm.py esiti-A esiti-B
"""
import argparse, hashlib, json, os, re, subprocess, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

R = Path(__file__).resolve().parents[2]
PROMPT = R / "report/metodo/llm/prompt-analisi-documentale-v1.md"
SCHEMA = R / "schemi/analisi-documentale.schema.json"
RIP = R / "report/metodo/llm/riproduzione/v1"
MAX_DOC, MAX_TOT = int(os.environ.get("MAX_DOC", 25000)), int(os.environ.get("MAX_TOT", 60000))  # caratteri; ridurre per modelli locali piccoli


def sha_b(b): return hashlib.sha256(b).hexdigest()


def istruzioni():
    t = PROMPT.read_text(encoding="utf-8")
    return t.split("## ISTRUZIONI PER IL MODELLO", 1)[1].split("## INGRESSO (compilato dal runner)", 1)[0].strip("-\n ")


def pacchetto(n):
    B = R / "report/metodo/llm/imbuto-g1g3"
    lotti = {}
    for f in sorted((B / "lotti").glob("*.jsonl")):
        for l in f.read_text(encoding="utf-8").splitlines():
            if l.strip(): c = json.loads(l); lotti[c["cig"]] = c
    ver = [json.loads(l) for l in (B / "verificati.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    atti = {}
    for l in (R / "dati/atti/atti-server.jsonl").read_text(encoding="utf-8").splitlines():
        try: a = json.loads(l)
        except json.JSONDecodeError: continue
        if a.get("cig") in lotti and a.get("esito_recupero") == "ok" and a.get("sha256"): atti.setdefault(a["cig"], {})[a["sha256"]] = a
    # campione: prima i CIG di controllo (campione 611), poi alternanza fra gruppi e stati, con almeno un documento quando possibile
    ver.sort(key=lambda v: (not lotti[v["cig"]].get("controllo"), not atti.get(v["cig"]), v["cig"]))
    scelti = ver[:n]
    d = RIP / "ingressi"; d.mkdir(parents=True, exist_ok=True)
    somme = []
    for v in scelti:
        c = lotti[v["cig"]]; docs = []
        for s, a in atti.get(c["cig"], {}).items():
            f = R / "dati/atti/testi" / f"{s}.txt"
            if f.exists():
                t = f.read_text(encoding="utf-8", errors="replace")
                docs.append({"sha256": s, "testo_sha256": sha_b(t.encode()), "tipo": a.get("tipo_atto"), "url": a["url"],
                             "pertinenza": a.get("pertinenza"), "estrazione": (a.get("estrazione") or {}).get("strumento"), "testo": t})
        ing = {"cig": c["cig"], "gruppo": c["gruppo"], "controllo": c.get("controllo", False), "stazione_appaltante": c["ente"], "oggetto": c["testo"],
               "cpv": c["cpv"], "importo": c["importo"], "aggiudicatari": c["aggiudicatari"], "documenti": docs}
        b = json.dumps(ing, ensure_ascii=False, indent=1).encode()
        (d / f"{c['cig']}.json").write_bytes(b); somme.append(f"{sha_b(b)}  ingressi/{c['cig']}.json")
        # uscita di riferimento (Claude, via 6 con ricerca web), per il confronto
        e = RIP / "esiti-claude-via6"; e.mkdir(exist_ok=True)
        (e / f"{c['cig']}.json").write_text(json.dumps({k: v.get(k) for k in ("cig", "asse_a", "asse_b", "confidenza", "fonte_primaria", "motivazione", "modello")}, ensure_ascii=False, indent=1), encoding="utf-8")
    somme.append(f"{sha_b(PROMPT.read_bytes())}  ../../prompt-analisi-documentale-v1.md")
    (RIP / "SHA256SUMS").write_text("\n".join(somme) + "\n", encoding="utf-8")
    (RIP / "manifest.json").write_text(json.dumps({"creato_il": datetime.now(timezone.utc).isoformat(timespec="seconds"), "cig": len(scelti),
        "con_documenti": sum(bool(atti.get(v["cig"])) for v in scelti), "controllo": sum(bool(lotti[v["cig"]].get("controllo")) for v in scelti),
        "prompt_sha256": sha_b(PROMPT.read_bytes()), "riferimento": "esiti-claude-via6 = giro imbuto G1/G3 (Claude Sonnet + ricerca web, istruzioni p3, verificato)"}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(scelti), "ingressi in", d)


def testo_prompt(ing):
    righe = [f"CIG: {ing['cig']}", f"Stazione appaltante: {ing['stazione_appaltante']}", f"Oggetto (BDNCP): {ing['oggetto']}",
             f"CPV: {ing['cpv']}   Importo: {ing['importo']}   Aggiudicatari: {ing['aggiudicatari']}", "Documenti:" if ing["documenti"] else "Documenti: nessuno"]
    tot = 0
    for d in ing["documenti"]:
        t = d["testo"][:MAX_DOC]
        if tot + len(t) > MAX_TOT: t = t[:max(0, MAX_TOT - tot)]
        tot += len(t)
        righe += [f"=== documento sha256={d['sha256']} tipo={d['tipo']} url={d['url']}{' (troncato)' if len(t) < len(d['testo']) else ''} ===", t]
    return istruzioni() + "\n\n## INGRESSO\n\n" + "\n".join(righe)


def estrai_json(s):
    s = s.strip()
    m = re.search(r"\{.*\}", s, re.S)
    return json.loads(m.group(0) if m else s)


def valida(o, ing):
    err = []
    try:
        import jsonschema  # opzionale
        jsonschema.validate(o, json.loads(SCHEMA.read_text(encoding="utf-8")))
    except ImportError:
        S = json.loads(SCHEMA.read_text(encoding="utf-8"))
        for k in S["required"]:
            if k not in o: err.append(f"manca {k}")
        for asse in ("asse_a", "asse_b"):
            for k, spec in S["properties"][asse]["properties"].items():
                if "enum" in spec and k in (o.get(asse) or {}) and o[asse][k] not in spec["enum"]: err.append(f"{asse}.{k} fuori vocabolario")
        if o.get("confidenza") not in S["properties"]["confidenza"]["enum"]: err.append("confidenza fuori vocabolario")
    except Exception as x:  # jsonschema.ValidationError
        err.append(str(x).splitlines()[0])
    # citazioni alla lettera
    testi = {d["sha256"]: d["testo"] for d in ing["documenti"]}; testi["oggetto-bdncp"] = ing["oggetto"]
    norm = lambda s: re.sub(r"\s+", " ", s or "").strip().lower()
    prove_ok = []
    for p in o.get("prove") or []:
        prove_ok.append(bool(p.get("sha256") in testi and norm(p.get("citazione")) and norm(p.get("citazione")) in norm(testi[p["sha256"]])))
    return err, prove_ok


def chiama(fornitore, modello, testo, url=None, chiave_env=None):
    if fornitore == "claude-cli":
        p = subprocess.run([sys.executable, str(R / "tools/llm/claude_tetto.py"), "--progetto", "analisi-spesa-ict", "--",
                            "claude", "-p", "--model", modello, "--allowedTools", ""], input=testo, capture_output=True, text=True,
                           env=dict(os.environ, TETTO_ETICHETTA="riproduzione-v1"))
        if p.returncode == 75: raise SystemExit("tetto raggiunto: riprovare più tardi")
        return p.stdout
    if fornitore == "openai":
        req = urllib.request.Request(url.rstrip("/") + "/chat/completions", method="POST",
                                     data=json.dumps({"model": modello, "temperature": 0, "messages": [{"role": "user", "content": testo}]}).encode(),
                                     headers={"Content-Type": "application/json", "Authorization": "Bearer " + os.environ.get(chiave_env or "", "")})
        with urllib.request.urlopen(req, timeout=600) as r:
            return json.load(r)["choices"][0]["message"]["content"]
    if fornitore == "ollama":  # modelli open-weight locali già presenti (API nativa: serve per fissare num_ctx)
        req = urllib.request.Request((url or "http://localhost:11434").rstrip("/") + "/api/chat", method="POST",
                                     data=json.dumps({"model": modello, "stream": False, "format": "json", "think": False,
                                                      "options": {"temperature": 0, "num_ctx": int(os.environ.get("NUM_CTX", 32768))},
                                                      "messages": [{"role": "user", "content": testo}]}).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=3600) as r:
            return json.load(r)["message"]["content"]
    raise SystemExit("fornitore sconosciuto")


def registra(modello, ing, risposta, fornitore):
    out = RIP / f"esiti-{modello.replace(':', '_')}"; out.mkdir(parents=True, exist_ok=True)
    rec = {"cig": ing["cig"], "modello": modello, "fornitore": fornitore, "prompt_sha256": sha_b(PROMPT.read_bytes()),
           "ingresso_sha256": sha_b((RIP / "ingressi" / f"{ing['cig']}.json").read_bytes()), "quando": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    try:
        o = estrai_json(risposta); err, prove = valida(o, ing)
        rec.update(uscita=o, errori_schema=err, prove_letterali=prove, valida=not err)
    except (json.JSONDecodeError, ValueError) as x:
        rec.update(uscita=None, errori_schema=[f"JSON non valido: {x}"], risposta_grezza=risposta[:4000], valida=False)
    (out / f"{ing['cig']}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    return rec


def main():
    a = argparse.ArgumentParser(); sub = a.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pacchetto"); p.add_argument("--n", type=int, default=50)
    e = sub.add_parser("esegui"); e.add_argument("--fornitore", required=True, choices=["stampa", "claude-cli", "openai", "ollama"])
    e.add_argument("--modello", required=True); e.add_argument("--url"); e.add_argument("--chiave-env"); e.add_argument("--cig", nargs="*")
    i = sub.add_parser("importa"); i.add_argument("--modello", required=True); i.add_argument("file", nargs="+")
    x = a.parse_args()
    if x.cmd == "pacchetto": return pacchetto(x.n)
    if x.cmd == "importa":
        for f in x.file:
            t = Path(f).read_text(encoding="utf-8"); o = estrai_json(t)
            ing = json.loads((RIP / "ingressi" / f"{o['cig']}.json").read_text(encoding="utf-8"))
            print(o["cig"], registra(x.modello, ing, t, "a-mano")["valida"])
        return
    for f in sorted((RIP / "ingressi").glob("*.json")):
        ing = json.loads(f.read_text(encoding="utf-8"))
        if x.cig and ing["cig"] not in x.cig: continue
        if x.fornitore == "stampa":
            d = RIP / "prompt"; d.mkdir(exist_ok=True); (d / f"{ing['cig']}.txt").write_text(testo_prompt(ing), encoding="utf-8"); continue
        if (RIP / f"esiti-{x.modello.replace(':', '_')}" / f"{ing['cig']}.json").exists(): continue  # ripartibile
        rec = registra(x.modello, ing, chiama(x.fornitore, x.modello, testo_prompt(ing), x.url, x.chiave_env), x.fornitore)
        print(ing["cig"], "valida" if rec["valida"] else rec["errori_schema"], flush=True)


if __name__ == "__main__":
    main()
