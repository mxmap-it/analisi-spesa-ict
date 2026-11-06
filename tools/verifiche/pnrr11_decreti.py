"""Verifica «PNRR 1.1 per ente» (#66): spoglio dei decreti di finanziamento dell'Investimento 1.1 «Infrastrutture
digitali» (migrazione al PSN) pubblicati da DTD (presidenza.governo.it, Amministrazione trasparente > Sovvenzioni >
Criteri e modalità; tre decreti PAC pilota solo su assets.innovazione.gov.it). Ogni PDF è nell'archivio con sha256.

Per ogni decreto: righe dell'elenco ammessi (CUP, ente, importo 1.1), somma delle righe e confronto con gli importi
«complessivi» scritti nel decreto stesso (controvalidazione interna); poi totale contro i ~700 M€ assegnati su 900
dichiarati da PSN nel bilancio 2025 [R]. I decreti di rinuncia e revoca NON sono sottratti (lordo assegnato).

Uso:
  python tools/verifiche/pnrr11_decreti.py             # da un clone: legge esiti/2026-11-06/pnrr11/finanziati.csv
  python tools/verifiche/pnrr11_decreti.py --rigenera  # SUL SERVER: rilegge i PDF archiviati (pdftotext -layout)
"""
import csv, collections, hashlib, json, os, re, subprocess, sys, urllib.parse

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.normpath(os.path.join(QUI, "..", ".."))
ESITI = os.path.join(RADICE, "esiti/2026-11-06/pnrr11")
URLS = os.path.join(ESITI, "decreti-urls.txt")
OUT = os.path.join(ESITI, "finanziati.csv")
DEC = os.path.join(ESITI, "decreti.json")
CUP = re.compile(r"\b([A-Z][0-9]{2}[A-Z][0-9]{9,11})\b")  # pdftotext a volte tronca il CUP a 13-14 caratteri
EUR = re.compile(r"(?:€\s*)?([0-9]{1,3}(?:\.[0-9]{3})*,[0-9]{2})\s*€?")
MISURE_ESCLUSE = ("Avviso12", "Avviso131")   # decreti delle misure 1.2 e 1.3.1, finiti nelle stesse cartelle


def num(s): return float(s.replace(".", "").replace(",", "."))


def modo_b(t, nome, h):
    L = t.splitlines(); i0 = max((i for i, l in enumerate(L) if re.search(r"ALLEGATO\s*\d?\s*-?\s*ELENCO|ELENCO (DOMANDE|ISTANZE)", l, re.I)), default=0)
    out = []
    for i in range(i0, len(L)):
        m = re.search(r"([0-9]{1,3}(?:\.[0-9]{3})*,[0-9]{2})\s*€\s*$", L[i])
        if not m or re.search(r"totale", L[i], re.I): continue   # la riga del totale non è un ente
        vic = [(abs(j - i), CUP.search(L[j]).group(1)) for j in range(max(i0, i - 3), min(len(L), i + 3)) if CUP.search(L[j])]
        cup = min(vic)[1] if vic else ""
        ente = re.sub(r"^\s*\d{1,3}\s+|" + CUP.pattern, "", L[i][:m.start()]).strip()
        out.append([nome, h, cup, ente, num(m.group(1))])
    return out


def rigenera():
    righe, decreti = [], []
    for u in open(URLS, encoding="utf-8").read().split():
        nome = os.path.basename(urllib.parse.unquote(u))
        if any(m in nome for m in MISURE_ESCLUSE): continue
        p = os.path.join(RADICE, "archivio/mirror", urllib.parse.unquote(u.split("://", 1)[1]))
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        t = subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True).stdout
        multi = "multimisura" in nome.lower()
        cur = None; n = s = 0
        for ln in t.splitlines():
            m = CUP.search(ln)
            if m:
                imp = EUR.findall(ln[m.end():])
                if not imp: cur = None; continue
                e = num(imp[0])          # nei multimisura la prima colonna è l'Investimento 1.1
                ente = EUR.sub("", ln[m.end():]).strip(" €")
                cur = [nome, h, m.group(1), ente, e]; righe.append(cur); n += 1; s += e
            elif cur and ln.strip() and not EUR.search(ln) and len(ln.strip()) < 80 and not re.match(r"\s*(N\.|Pag|Elenco|ALLEGATO)", ln, re.I):
                cur[3] = (cur[3] + " " + ln.strip())[:160]
            elif not ln.strip(): cur = None
        compl = sorted({num(x) for x in EUR.findall(t)})
        if s <= 0 or not any(abs(c - s) < 1 for c in compl):   # modo B: righe che finiscono con «importo €» dopo l'allegato, CUP vicino
            rb = modo_b(t, nome, h)
            if rb and any(abs(c - sum(r[4] for r in rb)) < 1 for c in compl):
                righe = [r for r in righe if r[0] != nome] + rb; n = len(rb); s = sum(r[4] for r in rb)
        compl_c = sorted({num(x) for x in re.findall(r"complessiv\w*[^0-9€]{0,60}€?\s*([0-9]{1,3}(?:\.[0-9]{3})+,[0-9]{2})", t, re.I | re.S)})
        decreti.append({"decreto": nome, "url": u, "sha256": h, "righe": n, "somma_righe": round(s, 2),
                        "importi_complessivi_nel_testo": compl_c, "somma_coincide_con_un_importo_del_testo": s > 0 and any(abs(c - s) < 1 for c in compl), "multimisura": multi})
    os.makedirs(ESITI, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["decreto", "sha256", "cup", "ente", "importo_1_1"])
        for r in righe: w.writerow(r[:4] + [round(r[4], 2)])
    json.dump(decreti, open(DEC, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("scritti", len(righe), "righe da", len(decreti), "decreti")


def main():
    if "--rigenera" in sys.argv: return rigenera()
    R = list(csv.DictReader(open(OUT, encoding="utf-8"))); D = json.load(open(DEC, encoding="utf-8"))
    cup = {}
    for r in R: cup[r["cup"]] = r          # un CUP ammesso in più finestre si conta una volta (l'ultima)
    tot = sum(float(r["importo_1_1"]) for r in cup.values())
    pos = {c: r for c, r in cup.items() if float(r["importo_1_1"]) > 0}
    for d in D: print(f'{d["decreto"][:70]:70} {d["righe"]:4} {d["somma_righe"]:16,.2f} coincide={d["somma_coincide_con_un_importo_del_testo"]}')
    T = {"decreti": len(D), "decreti_con_somma_coincidente": sum(d["somma_coincide_con_un_importo_del_testo"] for d in D), "righe": len(R),
         "cup_distinti_con_importo": len(pos), "enti_distinti": len({r["ente"] for r in pos.values()}),
         "totale_lordo_euro": round(tot), "riferimento_bilancio_psn_R": {"assegnati": 700e6, "dotazione": 900e6},
         "quota_del_riferimento": round(tot / 700e6, 3)}
    print(json.dumps(T, ensure_ascii=False, indent=1))
    if "--json" in sys.argv: json.dump(T, open(sys.argv[sys.argv.index("--json") + 1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
