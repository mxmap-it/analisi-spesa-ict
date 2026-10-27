# Prima annotazione (annotatore: Claude, non cieca: per eccezione rispetto all'esito automatico),
# righe 0-436 del campione di misura. Indici = posizione nel CSV.
import csv, json, collections
LETTE = range(0, 437)
PROVIDER_ERRATO = {3,39,77,81,111,128,156,179,215,223,261,268,271,291,367,412,422}   # falso positivo o provider sbagliato
SERVIZIO_ERRATO = {22,37,40,47,55,69,85,132,153,189,193,199,205,211,221,225,282,290,316,319,322,354,405,415,424}
MANCATI = {16:"SAP cloud",116:"SAP cloud",154:"SAP cloud",248:"SAP cloud",89:"SAP licenza",400:"SAP licenza",
           63:"Oracle licenza",198:"Oracle licenza",425:"Oracle licenza",72:"Microsoft cloud",434:"Microsoft cloud",
           220:"Nextcloud (UE)",79:"TIM cloud (IT)",250:"Fastweb hosting (IT)",381:"Fastweb community cloud (IT)",
           394:"SPC Cloud lotto 1 (IT)",38:"in-house pubblico (IT)",152:"in-house pubblico (IT)",392:"in-house pubblico (IT)",
           413:"in-house pubblico (IT)",435:"in-house pubblico (IT)"}
rows = list(csv.DictReader(open("lavoro/attribuzione/campione-misura.csv", encoding="utf-8")))
pos = collections.Counter(); err_p = collections.Counter(); err_s = collections.Counter(); neg = collections.Counter(); miss = collections.Counter()
for i in LETTE:
    v = rows[i]["via"][:1]
    if v in "1235":
        pos[v] += 1
        if i in PROVIDER_ERRATO: err_p[v] += 1
        elif i in SERVIZIO_ERRATO: err_s[v] += 1
    else:
        neg[v] += 1
        if i in MANCATI: miss[v] += 1
out = {"righe_lette": len(LETTE), "attribuite": dict(pos), "provider_errato": dict(err_p), "solo_servizio_errato": dict(err_s),
       "non_attribuite": dict(neg), "mancati": dict(miss), "mancati_dettaglio": MANCATI}
tp = sum(pos.values()); fp = sum(err_p.values()); fs = sum(err_s.values())
out["precisione_provider"] = round((tp - fp) / tp * 100, 1)
out["precisione_provider_e_servizio"] = round((tp - fp - fs) / tp * 100, 1)
out["quota_mancati_fra_non_attribuite"] = round(sum(miss.values()) / sum(neg.values()) * 100, 1)
for k in list(out)[:]:
    pass
print(json.dumps(out, indent=1, ensure_ascii=False))
json.dump(out, open("lavoro/attribuzione/annotazione-claude-v2.json", "w"), indent=1, ensure_ascii=False)
