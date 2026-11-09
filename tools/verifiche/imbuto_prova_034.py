"""Prova a secco della rigenerazione dell imbuto (#71, #66): perimetro CPV 0.3.3 + R53 (imbuto 0.3.4, DEDUP_CPV)
+ regole della lente v4.3, SENZA toccare lavoro/imbuto/ict.csv.

Quattro varianti, per separare l effetto di ogni cambiamento:
  A  imbuto 0.3.4 completo: DEDUP_CPV, perimetro 0.3.3 (79342 fuori, RX_ICT con sw e connettività), classifica v4.3
  B  come A senza DEDUP_CPV (prima riga per CIG, 0.3.2)                    -> effetto R53 = A - B
  C  come B col perimetro di prima (79342 dentro, RX_ICT del 3/11)         -> effetto perimetro = B - C
  D  come C con classifica.py e config/ del 3/11 (commit 4820e09d)         -> effetto lente = C - D

INCIDENTE 9/11 (AGENTS.md §4): la prima versione lanciava A/B/C in parallelo, ~7 GB ciascuno (aggiudicatari e delta
interi in dizionari Python), e ha reso il server irraggiungibile. Ora:
  - «prepara» mette aggiudicatari, delta (ultima versione per CIG) e padri AQ in lavoro/imbuto-prova-0.3.4/base.duckdb
    (duckdb memory_limit 4GB, threads 2, temp su disco in lavoro/); le varianti leggono gli aggiudicatari a blocchi
    di 50.000 CIG e il delta a blocchi, senza dizionari interi;
  - «tutto» lancia UNA variante alla volta, in sequenza, con nice 19 + ionice -c3 e limite di memoria virtuale 8 GB;
    prima di ogni lancio servono >= 12 GB disponibili e carico < 60; durante il lancio, carico (5 min) > 60 -> SIGSTOP
    finché scende, RAM disponibile < 6 GB -> la variante si ferma (si riprende rilanciando: è idempotente, salta le
    varianti con riepilogo.json).
Uscite (git-ignored): lavoro/imbuto-prova-0.3.4/<V>/{ict.csv,riepilogo.json}, log/. Confronto: imbuto_prova_034_confronto.py.
Uso (sul server, dalla radice): .venv/bin/python tools/verifiche/imbuto_prova_034.py tutto   (oppure prepara | A | B | C | D)
"""
import csv, glob, importlib.util, io, os, re, resource, signal, subprocess, sys, time, zipfile

RADICE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
PROVA = "lavoro/imbuto-prova-0.3.4"
BASE = os.path.join(PROVA, "base.duckdb")
VECCHIO = os.path.join(PROVA, "vecchio")
COMMIT_VECCHIO = "4820e09d"
BLOCCO = 50000
LIMITE_V = 8 * 1024 ** 3


def disponibile_gb():
    for l in open("/proc/meminfo"):
        if l.startswith("MemAvailable:"): return int(l.split()[1]) / 1024 ** 2


def carico():
    return [float(x) for x in open("/proc/loadavg").read().split()[:3]]


def connetti(sola_lettura=False):
    import duckdb
    os.makedirs(os.path.join(PROVA, "tmp"), exist_ok=True)
    c = duckdb.connect(BASE, read_only=sola_lettura)
    c.execute(f"SET memory_limit='4GB'; SET threads=2; SET temp_directory='{PROVA}/tmp'; SET preserve_insertion_order=false")
    return c


def prepara():
    """Aggiudicatari, delta e padri AQ in duckdb su disco. Idempotente (salta se base.duckdb è completa)."""
    os.chdir(RADICE)
    sys.path.insert(0, os.path.join(RADICE, "tools/analisi"))
    from attribuisci_provider import D
    if os.path.exists(BASE + ".ok"): return
    if os.path.exists(BASE): os.remove(BASE)
    tmp = os.path.join(PROVA, "tmp"); os.makedirs(tmp, exist_ok=True)
    # aggiudicatari: cig;denominazione (stessa decodifica di attribuisci_provider.aggiudicatari)
    fa = os.path.join(tmp, "agg.csv")
    with open(fa, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["cig", "den"])
        for z in sorted(glob.glob(D + "aggiudicatari/filesystem/*_csv.zip")):
            zf = zipfile.ZipFile(z); m = next(i for i in zf.namelist() if i.endswith(".csv"))
            for r in csv.DictReader(io.TextIOWrapper(zf.open(m), encoding="utf-8-sig", errors="replace"), delimiter=";"):
                w.writerow([r["cig"], (r["denominazione"] or "").strip()])
    print(time.strftime("%H:%M"), "aggiudicatari estratti", flush=True)
    # delta: tutte le colonne, con file e riga per tenere l ultima versione di ogni CIG (come righe_cig("delta"))
    fd = []
    for i, z in enumerate(sorted(glob.glob(D + "cig/filesystem/*-cig_csv.zip"))):
        zf = zipfile.ZipFile(z); m = next(x for x in zf.namelist() if x.endswith(".csv"))
        p = os.path.join(tmp, f"delta_{i:03d}.csv"); fd.append(p)
        with open(p, "w", newline="", encoding="utf-8") as f:
            w = None
            for n, r in enumerate(csv.DictReader(io.TextIOWrapper(zf.open(m), encoding="utf-8-sig", errors="replace"), delimiter=";")):
                if w is None:
                    w = csv.DictWriter(f, fieldnames=list(r) + ["_f", "_rn"], extrasaction="ignore"); w.writeheader()
                r["_f"] = i; r["_rn"] = n; w.writerow(r)
    print(time.strftime("%H:%M"), "delta estratto", flush=True)
    # padri AQ dai file annuali (tutti gli anni, come imbuto.basi): solo la colonna, in streaming
    fp = os.path.join(tmp, "padri.csv")
    with open(fp, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["cig"])
        for d in sorted(glob.glob(D + "cig-20*")):
            for z in sorted(glob.glob(d + "/filesystem/cig_csv_*.zip")):
                zf = zipfile.ZipFile(z)
                for r in csv.DictReader(io.TextIOWrapper(zf.open(zf.namelist()[0]), encoding="utf-8-sig", errors="replace"), delimiter=";"):
                    if r["cig_accordo_quadro"]: w.writerow([r["cig_accordo_quadro"]])
    print(time.strftime("%H:%M"), "padri estratti", flush=True)
    c = connetti()
    c.execute(f"""CREATE TABLE agg AS SELECT cig, list(DISTINCT coalesce(den, '')) nomi
                  FROM read_csv('{fa}', all_varchar=true, header=true, delim=',', quote='"', escape='"', strict_mode=true) GROUP BY cig""")
    lista = "[" + ",".join(f"'{p}'" for p in fd) + "]"
    c.execute(f"""CREATE TABLE delta AS SELECT * EXCLUDE (_f, _rn) FROM read_csv({lista}, all_varchar=true, header=true, delim=',', quote='"', escape='"', strict_mode=true, union_by_name=true)
                  QUALIFY row_number() OVER (PARTITION BY cig ORDER BY _f::INT DESC, _rn::BIGINT DESC) = 1""")
    c.execute(f"""CREATE TABLE padri AS SELECT DISTINCT cig FROM (SELECT cig FROM read_csv('{fp}', all_varchar=true, header=true, delim=',', quote='"', escape='"', strict_mode=true)
                  UNION ALL SELECT cig_accordo_quadro FROM delta WHERE coalesce(cig_accordo_quadro, '') <> '')""")
    print({t: c.execute(f"SELECT count(*) FROM {t}").fetchone()[0] for t in ("agg", "delta", "padri")}, flush=True)
    c.close()
    for p in [fa, fp] + fd: os.remove(p)
    open(BASE + ".ok", "w").write(time.strftime("%Y-%m-%d %H:%M:%S\n"))


class Aggiudicatari:
    """Al posto del dizionario intero: i nomi del blocco di CIG in lettura (riempito da righe_a_blocchi)."""
    def __init__(self, c): self.c, self.cur = c.cursor(), {}  # cursore proprio: non interrompe la lettura a blocchi del delta

    def carica(self, cigs):
        self.cur = dict(self.c.execute("SELECT cig, nomi FROM agg WHERE cig IN (SELECT unnest($1::VARCHAR[]))",
                                       [list(set(cigs))]).fetchall())

    def get(self, k, d=None): return self.cur.get(k, d)


def variante(v):
    os.chdir(RADICE)
    os.environ["IMBUTO_OUT"] = os.path.join(PROVA, v)
    os.environ["IMBUTO_DEDUP_CPV"] = "1" if v == "A" else "0"
    if v == "D":
        if not os.path.exists(os.path.join(VECCHIO, "tools/analisi/classifica.py")):
            os.makedirs(VECCHIO, exist_ok=True)
            subprocess.run(f"git archive {COMMIT_VECCHIO} tools/analisi config | tar -x -C {VECCHIO}", shell=True, check=True)
        spec = importlib.util.spec_from_file_location("classifica", os.path.join(VECCHIO, "tools/analisi/classifica.py"))
        m = importlib.util.module_from_spec(spec); sys.modules["classifica"] = m; spec.loader.exec_module(m)
    sys.path.insert(0, os.path.join(RADICE, "tools/analisi"))
    import imbuto
    c = connetti(sola_lettura=True)
    agg = Aggiudicatari(c)
    originale = imbuto.righe_cig

    def righe_a_blocchi(fonte):
        if fonte == "delta":
            q = c.cursor().execute("SELECT * FROM delta"); cols = [d[0] for d in q.description]
            sorgente = ({k: (x or "") for k, x in zip(cols, t)} for b in iter(lambda: q.fetchmany(BLOCCO), []) for t in b)
        else:
            sorgente = originale(fonte)
        buf = []
        for r in sorgente:
            buf.append(r)
            if len(buf) >= BLOCCO:
                agg.carica([x["cig"] for x in buf]); yield from buf; buf = []
        if buf:
            agg.carica([x["cig"] for x in buf]); yield from buf

    imbuto.righe_cig = righe_a_blocchi
    imbuto.basi = lambda: (agg, {r[0] for r in c.execute("SELECT cig FROM delta").fetchall()},
                           {r[0] for r in c.execute("SELECT cig FROM padri").fetchall()})
    if v in ("C", "D"):
        imbuto.CPV_ICT = re.compile(r"^(48|72|302|3223|3224|3225|3226|50312|50320|51611|64216|64222|79342)")
        sys.modules["classifica"].CPV_ICT = imbuto.CPV_ICT
        vecchio = subprocess.run(["git", "show", f"{COMMIT_VECCHIO}:tools/analisi/imbuto.py"], capture_output=True, text=True, check=True).stdout
        ns = {}
        exec(re.search(r"^RX_ICT = re\.compile\(.*?re\.I\)", vecchio, re.S | re.M).group(0), {"re": re}, ns)
        imbuto.RX_ICT = ns["RX_ICT"]
    imbuto.VERSIONE_IMBUTO += f" PROVA-{v}"
    print(time.strftime("%H:%M"), "inizio", imbuto.VERSIONE_IMBUTO, "DEDUP_CPV", imbuto.DEDUP_CPV, flush=True)
    imbuto.main(2020)
    print(time.strftime("%H:%M"), "fine", flush=True)


def lancia(args, log):
    """Un processo alla volta, sorvegliato. Ritorna il codice d uscita (None se fermato per la RAM)."""
    while True:
        gb, ld = disponibile_gb(), carico()
        if gb >= 12 and ld[1] < 60: break
        print(time.strftime("%H:%M"), f"attesa: disponibili {gb:.1f} GB, carico {ld}", flush=True); time.sleep(120)
    print(time.strftime("%H:%M"), f"lancio {args}: disponibili {gb:.1f} GB, carico {ld}", flush=True)

    def lim(): resource.setrlimit(resource.RLIMIT_AS, (LIMITE_V, LIMITE_V))
    p = subprocess.Popen(["nice", "-n", "19", "ionice", "-c3", sys.executable, os.path.abspath(__file__)] + args,
                         stdout=open(log, "a"), stderr=subprocess.STDOUT, preexec_fn=lim, cwd=RADICE)
    fermo = False
    while p.poll() is None:
        time.sleep(30)
        gb, ld = disponibile_gb(), carico()
        if gb < 6:
            print(time.strftime("%H:%M"), f"RAM disponibile {gb:.1f} GB < 6: fermo {args}", flush=True)
            p.kill(); p.wait(); return None
        if ld[1] > 60 and not fermo:
            print(time.strftime("%H:%M"), f"carico {ld} > 60: sospendo", flush=True); p.send_signal(signal.SIGSTOP); fermo = True
        elif ld[1] <= 60 and fermo:
            print(time.strftime("%H:%M"), f"carico {ld}: riprendo", flush=True); p.send_signal(signal.SIGCONT); fermo = False
    return p.returncode


def tutto():
    os.chdir(RADICE); os.makedirs(os.path.join(PROVA, "log"), exist_ok=True)
    if not os.path.exists(BASE + ".ok"):
        if lancia(["prepara"], os.path.join(PROVA, "log/prepara.log")) != 0: sys.exit("prepara non riuscita")
    for v in "ABCD":
        if os.path.exists(os.path.join(PROVA, v, "riepilogo.json")): continue
        t = time.time(); rc = lancia([v], os.path.join(PROVA, f"log/{v}.log"))
        print(time.strftime("%H:%M"), v, "codice", rc, f"{(time.time() - t) / 60:.0f} min", flush=True)
        if rc != 0: sys.exit(f"variante {v} non riuscita")


if __name__ == "__main__":
    a = sys.argv[1]
    {"tutto": tutto, "prepara": prepara}.get(a, lambda: variante(a))()
