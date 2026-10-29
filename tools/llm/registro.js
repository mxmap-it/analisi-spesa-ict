// Costruisce gli artefatti intermedi riusabili (schemi in schemi/):
//   dati/classificazioni/campione-v3.jsonl  registro di classificazione per CIG, con tutti i passaggi (spesaict.classificazione/1)
//   dati/atti/atti.jsonl                    collegamenti CIG -> documenti aperti dagli agenti (spesaict.atto/1)
// Ingressi: lotti della via 6 (dati BDNCP del campione), proposta regole v3.1, esiti giro 1 (p1) e giro 2 (p2).
// Idempotente: rigenera i due file da ciò che è in git. Metodo: sito/content/progetto/formato-classificazione.md
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const R = path.resolve(__dirname, "../.."), L = p => path.join(R, p);
const jsonl = d => fs.existsSync(L(d)) ? fs.readdirSync(L(d)).filter(f => f.endsWith(".jsonl")).sort()
  .flatMap(f => fs.readFileSync(L(d + "/" + f), "utf8").split("\n").filter(s => s.trim()).map(s => JSON.parse(s))) : [];
const sha = f => crypto.createHash("sha256").update(fs.readFileSync(L(f))).digest("hex");
const prop = {};
for (const r of fs.readFileSync(L("report/metodo/campione-misura-v3-proposta.csv"), "utf8").split("\n").slice(1).filter(Boolean)) {
  const [cig, versione, via, provider, giurisdizione, servizio, ...regola] = r.split(",");
  prop[cig] = { versione, via, provider, giurisdizione, servizio, regola: regola.join(",").replace(/^"|"$/g, "") };
}
const g1 = Object.fromEntries(jsonl("report/metodo/llm/esiti").map(x => [x.cig, x]));
const g2 = Object.fromEntries(jsonl("report/metodo/llm/giro2/esiti").map(x => [x.cig, x]));
const fonteCampione = { dataset: "BDNCP/ANAC cig + aggiudicatari, campione v3 (611)", file: "report/metodo/campione-misura-v3-cieco.csv", sha256: sha("report/metodo/campione-misura-v3-cieco.csv") };
const esito = x => ({ e_cloud: x.e_cloud, servizio: x.servizio, provider_prodotto: x.provider_prodotto || "", giurisdizione: x.giurisdizione || "ignota",
  confidenza: x.confidenza, fonte_primaria: !!x.fonte_primaria, motivazione: x.motivazione || "" });
const out = [], atti = [];
for (const c of jsonl("report/metodo/llm/lotti")) {
  const p = prop[c.cig], a = g1[c.cig], b = g2[c.cig], passi = [];
  if (p) passi.push({ n: passi.length + 1, tipo: "regola", strumento: "tools/analisi/classifica.py", versione: p.versione,
    parametri: { via: p.via, regola: p.regola }, risultato: { provider: p.provider, giurisdizione: p.giurisdizione, servizio: p.servizio }, data: "2026-10-28" });
  if (a) passi.push({ n: passi.length + 1, tipo: "modello", strumento: a.modello || "claude-opus-5-5", versione: "istruzioni " + (a.versione_istruzioni || "p1"),
    parametri: { istruzioni: "tools/llm/istruzioni.md" }, risultato: { ...esito(a), accordo_regole: a.accordo_regole, fonti: a.fonti || [] }, data: a.data,
    nota: "giro 1: classificazione quasi solo dal testo (ricerca web minima)" });
  if (b) passi.push({ n: passi.length + 1, tipo: "modello", strumento: b.modello || "claude-haiku-5-5", versione: "istruzioni " + (b.versione_istruzioni || "p2"),
    parametri: { istruzioni: "tools/llm/istruzioni-p2.md", ricerche: b.ricerche }, risultato: { ...esito(b), atto_ente: b.atto_ente || "", fonti: b.fonti || [] }, data: b.data,
    nota: "giro 2: verifica sulle fonti (ricerca web + apertura pagine obbligatorie)" });
  const fin = b || a;
  const fonti = [...new Set([...(a?.fonti || []), ...(b?.fonti || [])].map(f => typeof f === "string" ? f : f.url).filter(Boolean))]
    .map(url => ({ url, tipo: url === b?.atto_ente ? "atto-ente" : "altro", sha256: "", aperta: !!b }));
  for (const f of fonti) atti.push({ schema: "spesaict.atto/1", cig: c.cig, url: f.url, trovato_con: { metodo: "agente " + (b ? "giro 2" : "giro 1") },
    recuperato_il: (fin?.data || "2026-10-29") + "T00:00:00Z", tipo_atto: f.tipo === "atto-ente" ? "determina" : "altro", ente: c.ente,
    esito_recupero: "ok", nota: "aperto dall'agente, non ancora archiviato con sha256 (strumento tools/llm/atti.py da fare)" });
  out.push({ schema: "spesaict.classificazione/1", cig: c.cig, versione_metodo: "v3.1+via6-" + (b ? "p2" : "p1"), generato_il: (fin?.data || "2026-10-28") + "T00:00:00Z",
    ingresso: { fonte: fonteCampione, oggetto: c.testo, cpv: c.cpv, importo: c.importo, stazione_appaltante: c.ente,
      aggiudicatari: (c.aggiudicatari || "").split(/\s*;\s*/).filter(Boolean) },
    esito: fin ? { ...esito(fin), via: "6-modello", cloud_sovrano: null, dipendenze_tecnologiche: [] }
               : { e_cloud: "", servizio: p?.servizio || "", provider_prodotto: p?.provider || "", giurisdizione: p?.giurisdizione || "ignota", via: p?.via, confidenza: "bassa", fonte_primaria: false },
    passaggi: passi, fonti, revisione: { stato: !fin || fin.confidenza !== "alta" || fin.accordo_regole === "n" ? "da-rivedere" : "campione-controllo" } });
}
fs.mkdirSync(L("dati/classificazioni"), { recursive: true }); fs.mkdirSync(L("dati/atti"), { recursive: true });
fs.writeFileSync(L("dati/classificazioni/campione-v3.jsonl"), out.map(x => JSON.stringify(x)).join("\n") + "\n");
fs.writeFileSync(L("dati/atti/atti.jsonl"), atti.map(x => JSON.stringify(x)).join("\n") + (atti.length ? "\n" : ""));
console.log(out.length, "classificazioni;", atti.length, "collegamenti CIG->documento");
