// Presentazione esecutiva per ANAC, dal registro report/anac/problemi.yaml (gravità, stato, id).
// Testi brevi per un pubblico dirigente qui sotto, uno per problema: i dettagli tecnici restano nelle schede.
const fs = require("fs");
const path = require("path");
const yaml = require("js-yaml");
const pptxgen = require("pptxgenjs");

const REPO = path.resolve(__dirname, "../..");
const OUT = process.argv[2] || path.join(REPO, "report/anac/presentazione-anac-2026-10.pptx");
const reg = yaml.load(fs.readFileSync(path.join(REPO, "report/anac/problemi.yaml"), "utf8"));
const byId = Object.fromEntries(reg.map((p) => [p.id, p]));

const BREVE = {
  P01: { t: "Mesi OCDS duplicati", cosa: "24 mesi su 96 sono la copia di un altro mese: cambia solo l'indirizzo scritto dentro il file.", cons: "Le serie storiche sono falsate e nulla lo segnala: chi analizza quegli anni conta due volte gli stessi appalti.", rim: "Rigenerare i mesi dal contenuto reale e impedire che un mese identico a un altro venga pubblicato.", ver: "Ogni giorno: nessuna coppia di mesi identici." },
  P02: { t: "OCDS fermo a marzo 2026", cosa: "Del 2026 è pubblicato solo marzo. Da aprile lo standard internazionale non riceve dati.", cons: "Per chi usa lo standard internazionale, in Europa e nel mondo, gli appalti italiani si fermano a marzo.", rim: "Pubblicare i mesi mancanti, o dichiarare sulla pagina la sospensione e la data di ripresa.", ver: "Ogni mese, dopo il giorno 2: il mese precedente è pubblicato." },
  P03: { t: "Il vincitore manca negli appalti 2026", cosa: "Nel 2026 il fornitore manca in 4 aggiudicazioni su 5. Negli anni precedenti c'era nel 99% dei casi.", cons: "Nello standard internazionale non si sa chi vince gli appalti dell'anno in corso.", rim: "Ripristinare l'esportazione del fornitore, che ANAC già possiede, e rigenerare il 2026.", ver: "Ogni mese: quota di aggiudicazioni con fornitore." },
  P08: { t: "Aggiornamenti mensili cancellati", cosa: "Gennaio, febbraio e marzo 2026 non sono più scaricabili, e non esiste un file completo dell'anno.", cons: "Per chi non li ha archiviati in tempo, quei tre mesi di contratti sono persi.", rim: "Conservare gli aggiornamenti fino al file annuale e dichiarare la regola di conservazione.", ver: "Ogni giorno: nessun file sparisce prima del file completo successivo." },
  P04: { t: "Date non leggibili dagli strumenti", cosa: "Dal 2022 le date sono in un formato non standard; nel 2026 il 13% non ha data.", cons: "Gli strumenti standard non riescono a collocare gli appalti nel tempo senza correzioni manuali.", rim: "Date nel formato standard internazionale (ISO 8601), sempre valorizzate.", ver: "100% di date valide in ogni file." },
  P05: { t: "Aggiudicazioni assenti dall'OCDS", cosa: "Fra il 22% e il 33% delle aggiudicazioni presenti nella banca dati non arriva nell'OCDS.", cons: "Chi usa solo lo standard internazionale sottostima appalti e spesa.", rim: "Includere tutte le aggiudicazioni, o dichiarare il criterio di esclusione.", ver: "Ogni mese: rapporto fra OCDS e dati tabellari." },
  P06: { t: "Interfaccia per programmi non funzionante", cosa: "L'interfaccia per l'accesso ai dati in tempo reale, descritta sul portale, risponde «non trovato».", cons: "Chi segue la documentazione ufficiale non ottiene nulla.", rim: "Ripristinare l'interfaccia, o toglierla dalla documentazione.", ver: "Ogni giorno: prova degli indirizzi documentati." },
  P09: { t: "Affidamenti sotto soglia mancanti", cosa: "Mancano giugno e luglio 2026 degli affidamenti sotto soglia; il formato JSON si è fermato a maggio.", cons: "Mancano proprio gli affidamenti diretti, quelli a più alto rischio.", rim: "Pubblicare i mesi mancanti; riprendere il JSON o dichiararne la fine.", ver: "Ogni giorno: continuità di ogni serie mensile." },
  P10: { t: "Il catalogo promette file che non esistono", cosa: "Quattro file elencati nel catalogo rispondono «non trovato».", cons: "Gli scarichi automatici falliscono senza spiegazione.", rim: "Allineare il catalogo ai file realmente pubblicati.", ver: "Ogni giorno: ogni file elencato esiste." },
  P12: { t: "Informazioni false ai programmi", cosa: "A una richiesta automatica il server risponde «tutto bene» ma con una pagina web al posto dei dati del file.", cons: "I controlli automatici vengono ingannati senza alcun errore: aggiornamenti non rilevati.", rim: "Stessa risposta a browser e programmi, oppure un errore esplicito.", ver: "Ogni giorno: confronto fra browser e programma." },
  P14: { t: "Contratti scollegati dai progetti finanziati", cosa: "1,95 milioni di righe riportano «ND» al posto del codice del progetto (CUP).", cons: "Non si segue il denaro pubblico, PNRR compreso, dal finanziamento al contratto.", rim: "Lasciare il campo vuoto quando il codice manca, e documentare la convenzione.", ver: "Numero di righe con «ND»." },
  P16: { t: "File 2026 non conformi allo standard", cosa: "Da quest'anno alcune righe usano virgolette fuori standard; fino al 2025 no.", cons: "Gli strumenti standard scartano o leggono male quelle righe.", rim: "Esportare secondo lo standard CSV, come negli anni precedenti.", ver: "Zero righe rifiutate in ogni nuovo file." },
  P07: { t: "Due licenze diverse per gli stessi dati", rim: "Una sola licenza in catalogo, pagina e file." },
  P11: { t: "Dimensioni dichiarate 4 volte quelle reali", rim: "Dichiarare la dimensione del file servito." },
  P13: { t: "Nessuna impronta per sapere se un file è cambiato", rim: "Esporre l'ETag, per scaricare solo ciò che cambia." },
};
for (const id of Object.keys(BREVE)) if (!byId[id] || !byId[id].pronto_per_anac) throw new Error(`${id} non è pronto nel registro`);

const THEME = {
  name: "Osservatorio",
  headFontFace: "Calibri",
  bodyFontFace: "Calibri",
  colors: { dk1: "1B2631", lt1: "FFFFFF", dk2: "17324D", lt2: "EEF3F8", accent1: "0066CC", accent2: "A61919", accent3: "A66300", accent4: "5C6F82", accent5: "008758", accent6: "CFE0F3", hlink: "0066CC", folHlink: "17324D" },
};
const HEX = { navy: "17324D", blu: "0066CC", rosso: "A61919", ambra: "A66300", ardesia: "5C6F82", tenue: "EEF3F8", bianco: "FFFFFF", testo: "1B2631" };
const GRAV = { alta: { c: HEX.rosso, l: "Gravità alta" }, media: { c: HEX.ambra, l: "Gravità media" }, bassa: { c: HEX.ardesia, l: "Gravità bassa" } };

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "I dati aperti di ANAC: problemi e rimedi";
pres.author = "Osservatorio Nazionale Sovranità Digitale";
const C = pres.SchemeColor;
const W = 13.333;

pres.defineSlideMaster({
  title: "COPERTINA",
  background: { color: HEX.navy },
  objects: [{ placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.0, w: 11.7, h: 1.8, fontSize: 40, bold: true, color: HEX.bianco, valign: "bottom", align: "left" }, text: "" } },
            { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 3.9, w: 11.7, h: 1.6, fontSize: 20, color: "CFE0F3", valign: "top" }, text: "" } }],
});
pres.defineSlideMaster({
  title: "CONTENUTO",
  background: { color: HEX.bianco },
  margin: [0.5, 0.6, 0.6, 0.6],
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 12.1, h: 0.9, fontSize: 30, bold: true, color: HEX.navy, valign: "middle" }, text: "" } },
    { text: { text: "Osservatorio Nazionale Sovranità Digitale · I dati aperti di ANAC: problemi e rimedi · ottobre 2026", options: { x: 0.6, y: 7.0, w: 10, h: 0.3, fontSize: 10, color: HEX.ardesia } } },
  ],
  slideNumber: { x: 12.2, y: 7.0, w: 0.5, h: 0.3, fontSize: 10, color: HEX.ardesia },
});

function t(slide, text, o) { slide.addText(text, Object.assign({ isTextBox: true, margin: 0, fontFace: "Calibri", color: HEX.testo, valign: "top" }, o)); }
function badge(slide, x, y, id, colore, d = 0.62) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: colore }, line: { color: colore } });
  t(slide, id, { x, y, w: d, h: d, align: "center", valign: "middle", fontSize: d > 0.6 ? 16 : 12, bold: true, color: HEX.bianco });
}

// 1. Copertina
pres.addSection({ title: "Apertura" });
let s = pres.addSlide({ masterName: "COPERTINA", sectionTitle: "Apertura" });
s.addText("I dati aperti di ANAC: quindici problemi, quindici rimedi", { placeholder: "title" });
s.addText("Rilevazione di ottobre 2026 sulla Banca Dati Nazionale dei Contratti Pubblici\nOsservatorio Nazionale Sovranità Digitale", { placeholder: "body" });
s.addNotes("Obiettivo dell'incontro: concordare con ANAC le correzioni e il modo di verificarle. Non è una valutazione del lavoro di ANAC: il patrimonio di dati è tra i più ampi d'Europa.");

// 2. Il messaggio
const pronti = reg.filter((p) => p.pronto_per_anac);
const conta = (g) => pronti.filter((p) => p.gravita === g).length;
s = pres.addSlide({ masterName: "CONTENUTO", sectionTitle: "Apertura" });
s.addText("Un patrimonio prezioso, che oggi non si può usare in modo affidabile", { placeholder: "title" });
const stats = [["12 milioni", "codici di gara (CIG) dal 2007 nella banca dati"], [String(pronti.length), "problemi confermati due volte"], [String(conta("alta")), "di gravità alta"], ["100%", "riproducibile da chiunque, con pochi comandi"]];
stats.forEach(([n, l], i) => {
  const x = 0.6 + i * 3.08;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.6, w: 2.8, h: 2.3, rectRadius: 0.12, fill: { color: HEX.tenue }, line: { color: HEX.tenue } });
  t(s, n, { x: x + 0.2, y: 1.85, w: 2.4, h: 1.0, fontSize: 40, bold: true, color: i === 2 ? HEX.rosso : HEX.blu });
  t(s, l, { x: x + 0.2, y: 2.9, w: 2.4, h: 0.8, fontSize: 15, color: HEX.testo });
});
t(s, [
  { text: "Tutti i problemi sono correggibili, e ciascuno ha un controllo automatico che ci dirà, giorno per giorno, quando è risolto.", options: { breakLine: true } },
  { text: "AgID ha documentato in modo indipendente diversi degli stessi problemi nel codice pubblico di Cruscotto Italia.", options: {} },
], { x: 0.6, y: 4.4, w: 12.1, h: 1.4, fontSize: 18, paraSpaceAfter: 10 });
s.addNotes("Messaggio chiave: i dati ci sono e sono preziosi; i difetti sono nella pubblicazione e si correggono. Ogni numero è riproducibile da chiunque.");

// 3. Sintesi: griglia dei 15 problemi per gravità
s = pres.addSlide({ masterName: "CONTENUTO", sectionTitle: "Apertura" });
s.addText("Sintesi: quindici problemi, in ordine di gravità", { placeholder: "title" });
const ordine = ["alta", "media", "bassa"];
const elenco = ordine.flatMap((g) => pronti.filter((p) => p.gravita === g));
elenco.forEach((p, i) => {
  const col = i % 3, row = Math.floor(i / 3);
  const x = 0.6 + col * 4.1, y = 1.35 + row * 1.02;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 3.9, h: 0.92, rectRadius: 0.08, fill: { color: HEX.tenue }, line: { color: HEX.tenue } });
  badge(s, x + 0.15, y + 0.17, p.id, GRAV[p.gravita].c, 0.58);
  t(s, BREVE[p.id].t, { x: x + 0.9, y: y + 0.12, w: 2.85, h: 0.7, fontSize: 14, bold: true, valign: "middle", color: HEX.navy });
});
t(s, [{ text: "● ", options: { color: HEX.rosso } }, { text: "alta   " }, { text: "● ", options: { color: HEX.ambra } }, { text: "media   " }, { text: "● ", options: { color: HEX.ardesia } }, { text: "bassa" }], { x: 0.6, y: 6.5, w: 6, h: 0.3, fontSize: 12, color: HEX.ardesia });

// 4. Una slide per problema (alta e media)
function problema(id) {
  const p = byId[id], b = BREVE[id], g = GRAV[p.gravita];
  const sl = pres.addSlide({ masterName: "CONTENUTO", sectionTitle: p.gravita === "alta" ? "Problemi gravi" : "Problemi di gravità media" });
  sl.addText(b.t, { placeholder: "title" });
  badge(sl, 0.6, 1.4, id, g.c, 0.75);
  t(sl, g.l, { x: 1.55, y: 1.57, w: 3, h: 0.4, fontSize: 14, bold: true, color: g.c, valign: "middle" });
  const card = (x, titolo, testo, sfondo, colTit, colTesto) => {
    sl.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 2.4, w: 3.85, h: 2.9, rectRadius: 0.12, fill: { color: sfondo }, line: { color: sfondo } });
    t(sl, titolo, { x: x + 0.3, y: 2.65, w: 3.25, h: 0.45, fontSize: 16, bold: true, color: colTit });
    t(sl, testo, { x: x + 0.3, y: 3.2, w: 3.25, h: 1.95, fontSize: 17, color: colTesto });
  };
  card(0.6, "Cosa non va", b.cosa, HEX.tenue, HEX.navy, HEX.testo);
  card(4.74, "Conseguenza", b.cons, HEX.tenue, g.c, HEX.testo);
  card(8.88, "Rimedio atteso da ANAC", b.rim, HEX.navy, "CFE0F3", HEX.bianco);
  t(sl, [{ text: "Come verificheremo che non si ripresenti: ", options: { bold: true, color: HEX.navy } }, { text: b.ver }], { x: 0.6, y: 5.65, w: 12.1, h: 0.45, fontSize: 16 });
  sl.addNotes(`${p.titolo}\n\nMisura: ${(p.prova || {}).sintesi || ""}\n\nConferma indipendente: ${p.controvalidazione}\n\nScheda tecnica ${id} nel documento per ANAC.`);
}
pres.addSection({ title: "Problemi gravi" });
["P01", "P02", "P03", "P08"].forEach(problema);
pres.addSection({ title: "Problemi di gravità media" });
["P04", "P05", "P06", "P09", "P10", "P12", "P14", "P16"].forEach(problema);

// 5. Le correzioni semplici (gravità bassa)
pres.addSection({ title: "Correzioni semplici" });
s = pres.addSlide({ masterName: "CONTENUTO", sectionTitle: "Correzioni semplici" });
s.addText("Tre correzioni semplici, di gravità bassa", { placeholder: "title" });
["P07", "P11", "P13"].forEach((id, i) => {
  const y = 1.6 + i * 1.55;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y, w: 12.1, h: 1.3, rectRadius: 0.1, fill: { color: HEX.tenue }, line: { color: HEX.tenue } });
  badge(s, 0.85, y + 0.33, id, HEX.ardesia, 0.64);
  t(s, BREVE[id].t, { x: 1.75, y: y + 0.22, w: 5.0, h: 0.9, fontSize: 18, bold: true, color: HEX.navy, valign: "middle" });
  t(s, [{ text: "Rimedio: ", options: { bold: true } }, { text: BREVE[id].rim }], { x: 6.9, y: y + 0.22, w: 5.6, h: 0.9, fontSize: 16, valign: "middle" });
});
s.addNotes("Correzioni di configurazione e di metadati: poco lavoro, beneficio immediato per chi riusa i dati.");

// 6. Come lo sappiamo
pres.addSection({ title: "Metodo" });
s = pres.addSlide({ masterName: "CONTENUTO", sectionTitle: "Metodo" });
s.addText("Ogni problema è confermato per due vie indipendenti", { placeholder: "title" });
[["Misurato", "Abbiamo scaricato l'intero portale: 1.797 risorse, 12 milioni di codici di gara (CIG), file conservati con impronta digitale (sha256)."],
 ["Confermato", "Ogni problema è rifatto con codice diverso, su un altro mese o da un'altra rete. Ciò che non regge è stato tolto o corretto."],
 ["Riscontrato da AgID", "Diversi problemi sono documentati, indipendentemente da noi, nel codice pubblico di Cruscotto Italia."]].forEach(([h, d], i) => {
  const x = 0.6 + i * 4.14;
  badge(s, x, 1.6, String(i + 1), HEX.blu, 0.7);
  t(s, h, { x, y: 2.5, w: 3.8, h: 0.5, fontSize: 20, bold: true, color: HEX.navy });
  t(s, d, { x, y: 3.1, w: 3.8, h: 2.4, fontSize: 16 });
});
t(s, "Quando un nostro numero si è rivelato sbagliato lo abbiamo corretto e registrato pubblicamente nel registro delle revisioni del rendiconto tecnico.", { x: 0.6, y: 5.8, w: 12.1, h: 0.7, fontSize: 15, italic: true, color: HEX.ardesia });

// 7. Riproducibilità
s = pres.addSlide({ masterName: "CONTENUTO", sectionTitle: "Metodo" });
s.addText("Chiunque può rifare tutto, con pochi comandi", { placeholder: "title" });
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 1.5, w: 7.6, h: 3.7, rectRadius: 0.1, fill: { color: "1B2631" }, line: { color: "1B2631" } });
t(s, ["git clone github.com/mxmap-it/analisi-spesa-ict", "tools/verifica_anac.sh ambiente", "tools/verifica_anac.sh dal-vivo", "tools/verifica_anac.sh scarica", "tools/verifica_anac.sh snapshot", "tools/verifica_anac.sh verifiche", "tools/verifica_anac.sh confronta"].join("\n"),
  { x: 0.9, y: 1.8, w: 7.1, h: 3.2, fontSize: 16, fontFace: "Courier New", color: "E8F0F8", paraSpaceAfter: 8 });
t(s, [{ text: "Dal vivo", options: { bold: true, color: HEX.navy, breakLine: true } }, { text: "Misura in pochi minuti lo stato attuale del portale: mostra quali problemi sono risolti.", options: { breakLine: true } },
       { text: " ", options: { breakLine: true } },
       { text: "Dallo snapshot", options: { bold: true, color: HEX.navy, breakLine: true } }, { text: "Rifà i numeri esatti del rapporto sugli stessi 349 file, verificati con la loro impronta digitale." }],
  { x: 8.6, y: 1.6, w: 4.1, h: 4.4, fontSize: 16 });
s.addNotes("Istruzioni complete in RIPRODURRE.md nel repository. Il controllo dal vivo gira ogni mattina sul nostro server.");

// 8. Proposta
pres.addSection({ title: "Proposta" });
s = pres.addSlide({ masterName: "CONTENUTO", sectionTitle: "Proposta" });
s.addText("La nostra proposta", { placeholder: "title" });
[["Un referente tecnico", "Un contatto in ANAC con cui verificare le schede tecniche e concordare i rimedi."],
 ["Prima le correzioni rapide", "Catalogo, licenza, dimensioni, impronte dei file, risposte ai programmi: lavoro di configurazione."],
 ["Poi le correzioni strutturali", "Rigenerazione dell'OCDS (mesi duplicati, 2026, fornitore, date) e conservazione degli aggiornamenti mensili."],
 ["Verifica pubblica e continua", "I nostri controlli girano ogni giorno: ogni correzione diventa visibile, e lo riconosceremo pubblicamente."]].forEach(([h, d], i) => {
  const col = i % 2, row = Math.floor(i / 2);
  const x = 0.6 + col * 6.15, y = 1.5 + row * 2.45;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 5.95, h: 2.2, rectRadius: 0.12, fill: { color: HEX.tenue }, line: { color: HEX.tenue } });
  badge(s, x + 0.3, y + 0.3, String(i + 1), HEX.blu, 0.62);
  t(s, h, { x: x + 1.15, y: y + 0.32, w: 4.5, h: 0.55, fontSize: 19, bold: true, color: HEX.navy, valign: "middle" });
  t(s, d, { x: x + 1.15, y: y + 0.95, w: 4.5, h: 1.1, fontSize: 15 });
});

// 9. Chiusura
s = pres.addSlide({ masterName: "COPERTINA", sectionTitle: "Proposta" });
s.addText("Grazie", { placeholder: "title" });
s.addText("Documento con le schede tecniche: analisi-spesa-ict.mxmap.it/rendiconti/anac-2026-10-problemi\nCodice e prove: github.com/mxmap-it/analisi-spesa-ict\nOsservatorio Nazionale Sovranità Digitale · osservatorio.mxmap.it", { placeholder: "body" });

(async () => {
  await pres.writeFile({ fileName: OUT });
  // facoltativo: scrive la palette nel tema del file (i colori delle slide sono comunque espliciti)
  if (process.env.APPLY_THEME) await require(process.env.APPLY_THEME).applyTheme(OUT, THEME);
  console.log("scritto", OUT);
})();
