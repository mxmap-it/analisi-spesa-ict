// Costruisce la pagina di revisione (tools/revisione/pagina.html + dati pubblicati in report/metodo) -> lavoro/revisione/index.html
// Uso: node tools/revisione/costruisci.js   La copia cieca NON contiene l'esito del classificatore: la pagina resta alla cieca.
const fs = require("fs"), path = require("path");
const R = p => fs.readFileSync(p, "utf8");
function csv(t) {
  const rows = []; let row = [], f = "", q = false;
  for (let i = 0; i < t.length; i++) {
    const c = t[i];
    if (q) { if (c === '"') { if (t[i + 1] === '"') { f += '"'; i++ } else q = false } else f += c }
    else if (c === '"') q = true; else if (c === ",") { row.push(f); f = "" }
    else if (c === "\n") { row.push(f); rows.push(row); row = []; f = "" } else if (c !== "\r") f += c;
  }
  if (f || row.length) { row.push(f); rows.push(row) }
  const h = rows.shift();
  return rows.filter(r => r.length > 1).map(r => Object.fromEntries(h.map((k, i) => [k, r[i] ?? ""])));
}
const tieni = (o, ks) => Object.fromEntries(ks.map(k => [k, o[k]]));
const campione = csv(R("report/metodo/campione-misura-v3-cieco.csv"))
  .map(r => tieni(r, ["cig", "cod_cpv", "importo_lotto", "stazione_appaltante", "aggiudicatari", "testo"]));
const imp = csv(R("report/metodo/importi-da-verificare-v3.csv"));
const perImporto = {};
imp.forEach(r => (perImporto[r.importo_lotto] ||= []).push(r));
const importi = imp.map(r => {
  const altri = perImporto[r.importo_lotto].filter(x => x.cig !== r.cig);
  const ipotesi = r.e_padre === "1" ? "padre AQ: già escluso dai totali"
    : altri.some(x => x.stazione_appaltante !== r.stazione_appaltante) ? "probabile massimale: stesso importo presso altri enti"
    : "grande importo: serve il documento";
  return { ...tieni(r, ["anno", "cig", "importo_lotto", "motivo", "stazione_appaltante", "aggiudicatari", "provider", "servizio", "e_padre", "testo"]),
    ipotesi, gemelli: altri.map(x => `${x.cig} (${x.stazione_appaltante})`).join("; ") };
}).sort((a, b) => b.importo_lotto - a.importo_lotto);
const richieste = [];
for (const blocco of R("report/metodo/richieste-e-raccomandazioni.yaml").split(/^- id: /m).slice(1)) {
  const g = k => ((blocco.match(new RegExp("^  " + k + ": (.*)$", "m")) || [])[1] || "").replace(/^["']|["']$/g, "");
  richieste.push({ id: blocco.split("\n")[0].trim(), destinatario: g("destinatario"), stato: g("stato"), titolo: g("titolo") });
}
const gap = JSON.parse(R("tools/revisione/lacune.json"));
const html = R("tools/revisione/pagina.html").replace("/*DATA*/null", JSON.stringify({ campione, importi, richieste, gap }).replace(/</g, "\u003c"));
fs.mkdirSync("lavoro/revisione", { recursive: true });
fs.writeFileSync("lavoro/revisione/index.html", html);
console.log(`campione ${campione.length}, importi ${importi.length}, richieste ${richieste.length}, lacune ${gap.length}, ${html.length} byte`);
