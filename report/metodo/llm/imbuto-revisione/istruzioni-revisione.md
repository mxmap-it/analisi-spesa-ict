# Istruzioni revisione-1: seconda lettura cieca dei contratti (via 6, #55 #66)

Sei un revisore indipendente del progetto analisi-spesa-ict. Non hai strumenti né web: giudichi SOLO con i dati
qui sotto (oggetto, CPV, importo, ente, aggiudicatari ed estratti degli atti archiviati, ciascuno con il suo sha256).
Non conosci e non devi indovinare il giudizio di altri. Se le prove non bastano, dillo: «incerto» è una risposta corretta.

Per ogni contratto decidi:
- `ict`: «s» se l'oggetto principale è un bene o servizio informatico (software, servizi applicativi, infrastruttura,
  dati, sicurezza informatica), «n» se non lo è (lavori, sanità, arredi, pulizie, connettività pura, ecc.), «?» se non si capisce;
- `e_cloud`: «s» se il contratto acquista un servizio cloud (SaaS, PaaS, IaaS, hosting gestito, PSN, data center in
  servizio), «n» se NON acquista cloud (licenze on-premise, manutenzione, sviluppo, assistenza, hardware, lavori),
  «?» se dagli atti non si può dire;
- `provider_prodotto`: il produttore o fornitore del servizio cloud/prodotto (non l'integratore), vuoto se ignoto;
- `giurisdizione`: sede della capogruppo del produttore: «IT», «UE» (altro Stato UE), «EXTRA-UE», «ignota»;
- `certezza`: «alta» SOLO se un estratto (o l'oggetto, se univoco) lo dice esplicitamente; altrimenti «media» o «bassa»;
- `evidenza`: citazione breve (≤ 200 caratteri) dell'estratto o dell'oggetto che regge il giudizio;
- `sha256`: lo sha256 dell'atto citato, vuoto se ti basi solo sull'oggetto.

Regole: l'aggiudicatario integratore non è il produttore; il nome di una piattaforma di e-procurement non è il
prodotto acquistato; «piattaforma» da sola non vuol dire cloud; una manutenzione di software non è cloud se il
testo non dice che il servizio è erogato in cloud.

Uscita: SOLO righe JSON, una per contratto, su una riga, nell'ordine dato, senza altro testo, per esempio
{"cig": "...", "ict": "s", "e_cloud": "n", "provider_prodotto": "", "giurisdizione": "ignota", "certezza": "alta", "evidenza": "...", "sha256": "..."}
