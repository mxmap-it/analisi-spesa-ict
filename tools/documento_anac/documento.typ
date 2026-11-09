// Documento per ANAC (#34). Dati da dati.json, generato da genera.py a partire da report/anac/problemi.yaml.
#let d = json("dati.json")
#let blu = rgb("#1f3a5f")
#let grigio = rgb("#5b6470")
#let chiaro = rgb("#eef2f7")
#let sans = "New Computer Modern Sans"
#let colgrav = (alta: rgb("#b3261e"), media: rgb("#b26a00"), bassa: rgb("#2e6b3a"), da_valutare: grigio)
#let etgrav = (alta: "alta", media: "media", bassa: "bassa", da_valutare: "da valutare")

#set document(title: "I dati aperti di ANAC: problemi e rimedi", author: "Osservatorio Nazionale Sovranità Digitale")
#set text(font: "Libertinus Serif", size: 10.5pt, lang: "it", hyphenate: true)
#set par(justify: true, leading: 0.62em, spacing: 0.9em)
#show heading.where(level: 1): it => { pagebreak(weak: true); block(below: 1em, text(font: sans, size: 18pt, fill: blu, weight: "bold", it.body)) }
#show heading.where(level: 2): it => block(above: 1.3em, below: 0.6em, text(font: sans, size: 12.5pt, fill: blu, weight: "bold", it.body))
#show raw: set text(font: "DejaVu Sans Mono", size: 7.8pt)
#show link: set text(fill: blu)

#let badge(g) = box(fill: colgrav.at(g, default: grigio), inset: (x: 5pt, y: 2pt), radius: 2pt,
  text(font: sans, fill: white, size: 7pt, weight: "bold", upper(etgrav.at(g, default: g))))
#let etich(t) = text(font: sans, size: 7.5pt, fill: grigio, weight: "bold", upper(t))

// ---------- copertina
#page(paper: "a4", margin: (x: 2.4cm, y: 2.6cm), numbering: none)[
  #v(1fr)
  #text(font: sans, size: 9pt, fill: grigio, tracking: 1pt)[OSSERVATORIO NAZIONALE SOVRANITÀ DIGITALE · ANALISI-SPESA-ICT]
  #v(0.5cm)
  #line(length: 100%, stroke: 2pt + blu)
  #v(0.4cm)
  #text(font: sans, size: 28pt, weight: "bold", fill: blu)[I dati aperti di ANAC:\ problemi e rimedi]
  #v(0.3cm)
  #text(size: 14pt, fill: grigio)[Sintesi e schede tecniche per la correzione della Banca Dati Nazionale dei Contratti Pubblici]
  #v(1.2cm)
  #grid(columns: (1fr, 1fr, 1fr), gutter: 10pt,
    ..((str(d.pronti.len()), "problemi documentati"), (str(d.gravita.alta), "di gravità alta"), ("1.797", "risorse del portale verificate")).map(((n, t)) =>
      block(fill: chiaro, inset: 10pt, radius: 3pt, width: 100%)[#text(size: 22pt, weight: "bold", fill: blu, n)\ #text(size: 9pt, fill: grigio, t)]))
  #v(1fr)
  #text(size: 9pt, fill: grigio)[Rilevazione di ottobre-novembre 2026 · versione #d.versione del #d.data · *bozza, non inviata* \
  Registro dei problemi: `report/anac/problemi.yaml`, sha256 #raw(d.registro_sha256.slice(0, 16))… \
  Ogni numero è riproducibile: #link("https://github.com/mxmap-it/analisi-spesa-ict")[github.com/mxmap-it/analisi-spesa-ict]]
]

#set page(paper: "a4", margin: (x: 2.2cm, top: 2.4cm, bottom: 2.2cm),
  header: [#set text(size: 8pt, fill: grigio, font: sans); I dati aperti di ANAC: problemi e rimedi #h(1fr) versione #d.versione · bozza del #d.data],
  footer: context [#set text(size: 8pt, fill: grigio); #h(1fr) #counter(page).display("1") #h(1fr)])

= Perché questo documento
ANAC pubblica sul portale `dati.anticorruzione.it` uno dei patrimoni di dati sugli appalti pubblici più ampi d'Europa: oltre dodici milioni di contratti dal 2007, in tre formati e nello standard internazionale OCDS. Per misurare la spesa pubblica in servizi cloud abbiamo scaricato e verificato tutto il portale: 1.797 risorse, 77 GB di file usati per le verifiche.

Abbiamo trovato problemi che impediscono di usare quei dati in modo affidabile. Questo documento li elenca *con un solo scopo: che vengano corretti.* Per ognuno indica la conseguenza per chi usa i dati, il rimedio che chiediamo e il controllo automatico con cui verificheremo nel tempo che il problema sia risolto e non si ripresenti.

Diversi problemi sono noti anche ad AgID, che li ha documentati in modo indipendente da noi nel codice pubblico di Cruscotto Italia (ottobre 2026).

== La regola di ammissione
Un problema entra in questo documento solo se ha tutti e quattro i requisiti:
+ una *prova riproducibile*, con lo script, l'esito e l'impronta sha256 dei file;
+ una *conferma per una seconda via indipendente* (altro formato, altro strumento o altro soggetto);
+ un'*azione correttiva* concreta;
+ una *metrica di non ricorrenza*, eseguita ogni giorno dalla nostra sonda.
Ciò che non regge resta interno: in appendice, con il motivo (#d.interni.len() su #d.totale).

== Come riprodurre tutto
#block(fill: chiaro, inset: 8pt, radius: 3pt, width: 100%)[
```bash
git clone https://github.com/mxmap-it/analisi-spesa-ict.git && cd analisi-spesa-ict
tools/verifica_anac.sh ambiente    # versioni bloccate
tools/verifica_anac.sh dal-vivo    # stato attuale del server ANAC
tools/verifica_anac.sh scarica     # i file usati, ~77 GB
tools/verifica_anac.sh snapshot    # stessi file del 27/10/2026? (sha256)
tools/verifica_anac.sh verifiche   # tutte le verifiche
tools/verifica_anac.sh confronta   # ogni numero contro quelli pubblicati
```]

= Sintesi
#table(columns: (auto, 1.3fr, 1fr), stroke: none, inset: (x: 5pt, y: 6pt),
  fill: (_, y) => if y == 0 { blu } else if calc.odd(y) { chiaro } else { none },
  table.header(..("", "Problema e conseguenza", "Rimedio atteso").map(t => text(font: sans, fill: white, weight: "bold", size: 9pt, t))),
  ..d.pronti.map(p => (
    [#text(font: sans, weight: "bold", fill: blu, p.id)\ #badge(p.gravita)],
    [#set text(size: 9pt, hyphenate: false); #set par(justify: false); *#p.titolo* \ #p.conseguenza],
    [#set text(size: 9pt); #set par(justify: false); #p.azione_correttiva])).flatten())

= Schede tecniche
#for p in d.pronti [
  #block(breakable: true, above: 1.4em, below: 1.4em, width: 100%, stroke: (left: 3pt + colgrav.at(p.gravita, default: grigio)), inset: (left: 10pt, y: 4pt))[
    #text(font: sans, size: 11.5pt, weight: "bold", fill: blu)[#p.id · #p.titolo] #h(4pt) #badge(p.gravita)
    #if p.rif != "" [#text(size: 8pt, fill: grigio)[ · rif. #p.rif]]

    #etich("Conseguenza") \ #p.conseguenza

    #etich("Cosa abbiamo misurato") \ #p.prova.at("sintesi", default: "") \
    #text(size: 8.5pt, fill: grigio)[Script #raw(p.prova.at("script", default: "")) · esito #raw(p.prova.at("esito", default: "")) · verificato il #p.prova.at("verificato_il", default: "")]

    #for m in p.at("altre_misure", default: ()) [
      #etich(m.etichetta) \ #text(size: 9.5pt, m.testo)

    ]
    #etich("Conferma indipendente") \ #p.controvalidazione

    #etich("Rimedio atteso") \ #p.azione_correttiva

    #etich("Metrica di non ricorrenza") \ #p.metrica
    #if p.at("storia", default: none) != none [

      #etich("Correzioni") \ #text(size: 9pt, fill: grigio, p.storia)]
  ]
]

= Appendice: problemi che restano interni
#if d.interni.len() == 0 [Nessuno: in questa versione tutti i #d.totale problemi del registro hanno i quattro requisiti.]
#for p in d.interni [
  == #p.id · #p.titolo
  #p.at("motivo_interno", default: "Manca: " + p.at("manca", default: ""))
]

== Il nostro impegno
Se un nostro numero è sbagliato lo correggiamo e lo registriamo, come abbiamo già fatto più volte nel registro delle revisioni del rendiconto tecnico (#link("https://analisi-spesa-ict.mxmap.it/rendiconti/anac-2026-10/")[analisi-spesa-ict.mxmap.it/rendiconti/anac-2026-10]). Le segnalazioni si aprono su GitHub.

== Registro delle revisioni
#table(columns: (auto, auto, 1fr), stroke: none, inset: (x: 5pt, y: 5pt),
  fill: (_, y) => if y == 0 { blu } else if calc.odd(y) { chiaro } else { none },
  table.header(..("Versione", "Data", "Modifiche").map(t => text(font: sans, fill: white, weight: "bold", size: 9pt, t))),
  ..d.revisioni.map(r => (text(size: 9pt, r.versione), text(size: 9pt, r.data), [#set text(size: 9pt); #set par(justify: false); #r.nota])).flatten())
