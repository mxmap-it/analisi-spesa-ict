// Divide il campione (611 contratti) in lotti da 20 per la classificazione assistita da modello linguistico + ricerca web.
// Ingresso: campione cieco + proposta v3.1. Uscita: report/metodo/llm/lotti/lotto-NN.jsonl
const fs = require("fs"), path = require("path");
const R = path.resolve(__dirname, "../..");
function csv(f) {
  const t = fs.readFileSync(path.join(R, f), "utf8"), rows = []; let row = [], cell = "", q = false;
  for (let i = 0; i < t.length; i++) {
    const c = t[i];
    if (q) { if (c === '"') { if (t[i + 1] === '"') { cell += '"'; i++; } else q = false; } else cell += c; }
    else if (c === '"') q = true; else if (c === ",") { row.push(cell); cell = ""; }
    else if (c === "\n") { row.push(cell.replace(/\r$/, "")); rows.push(row); row = []; cell = ""; } else cell += c;
  }
  if (cell || row.length) { row.push(cell); rows.push(row); }
  const h = rows.shift(); return rows.filter(r => r.length > 1).map(r => Object.fromEntries(h.map((k, i) => [k, r[i] || ""])));
}
const prop = Object.fromEntries(csv("report/metodo/campione-misura-v3-proposta.csv").map(r => [r.cig, r]));
const righe = csv("report/metodo/campione-misura-v3-cieco.csv").map(r => {
  const p = prop[r.cig] || {};
  return { cig: r.cig, cpv: r.cod_cpv, importo: Number(r.importo_lotto), ente: r.stazione_appaltante, aggiudicatari: r.aggiudicatari, testo: r.testo,
           regole_v31: { via: p.via, provider: p.provider, giurisdizione: p.giurisdizione, servizio: p.servizio } };
});
const N = 20;
for (let i = 0; i < righe.length; i += N)
  fs.writeFileSync(path.join(R, `report/metodo/llm/lotti/lotto-${String(i / N + 1).padStart(2, "0")}.jsonl`), righe.slice(i, i + N).map(x => JSON.stringify(x)).join("\n") + "\n");
console.log(righe.length, "contratti in", Math.ceil(righe.length / N), "lotti");
