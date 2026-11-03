# Controllo dei falsi positivi — monitor «Amministrazione trasparente», giro 2026-11 (#61)

**Data:** 3/11/2026, 21:47-22:01 UTC. **Esecutore:** Claude (agente) su richiesta di Fabio Pietrosanti.
**Requisito:** è la condizione per pubblicare i nomi degli enti (decisione di Fabio, 3/11/2026).

## Executive summary
- **Campione:** 53 enti classificati come bloccati dalla prima prova sul server (giro 2026-11, metodo 1.0.0). Estrazione casuale con seme fisso 20261104 dentro ogni esito: 30 «WAF/anti-bot», 15 «robots.txt», 8 «noindex». File: `lavoro/trasparenza/campione-fp-2026-11.json`.
- **Seconda osservazione:** dal portatile di Fabio, IP residenziale 212.66.116.2 (AS20912), con il Chrome installato e la finestra visibile. Le identità usate sono cinque: bot del progetto, python-requests, curl, UA da browser, Chrome reale. Per robots.txt e noindex c'è anche una rilettura indipendente: curl e requests, con la regola letta riga per riga.
- **robots.txt: 15 su 15 confermati.** Una sfumatura: su trasparenza-pa.net e sui siti Halley (`/amministrazione/trasparenza/...`) la regola `User-agent: *` / `Disallow: /` vieta tutto a Bingbot e a tutti gli altri client, mentre a Googlebot è concesso un gruppo proprio. La violazione resta: Bing è un motore di ricerca. La dashboard mostra le identità escluse ente per ente.
- **noindex: 8 su 8 confermati.** Il `<meta name="robots" content="noindex, nofollow">` è presente, letto di nuovo con un client indipendente.
- **WAF/anti-bot: 13 su 30 confermati, 16 non lo sono, 1 non valutabile.** Il metodo 1.0.0 sovrastimava i blocchi per i bot. Le regole sono state corrette nella versione 1.1.0-beta (vedi sotto). Con le nuove regole nessuno di questi 16 casi verrebbe più classificato come blocco dei bot.

## Dettaglio dei 30 «WAF/anti-bot»

| gruppo | enti | prima prova (server) | portatile (residenziale) | giudizio |
|---|---|---|---|---|
| web.spaggiari.eu (scuole) | 11 | 403 a bot e browser-UA | 403 a bot, python, curl e browser-UA; **Chrome reale 200** («Amministrazione Trasparente») | **vero positivo**: blocco dei client non-browser (Akamai), anche da IP residenziale |
| studiok.it | 2 | 403/403 | 200 a tutte le identità | **vero positivo, ma di altro tipo**: blocco dell'IP del datacenter, non dell'identità |
| albo.comune.it (6), dgegovpa.it (4), difesa.it (3), halleyweb.com/c059003 (1) | 14 | 403/403 senza firma | 403 anche a Chrome reale («403 - Accesso negato», «403 Forbidden») | **falso positivo come «blocco dei bot»**: l'accesso è negato a tutti. Nuovo esito «accesso negato a tutti i client», che non conta come violazione dell'art. 9 ma resta un'anomalia da segnalare |
| egov.halleysardegna.com/ottana, comune.padenghesulgarda.bs.it | 2 | errore di connessione o TLS solo sul bot | 200 a tutte le identità | **falso positivo**: errore transitorio. Ora ci sono i ritentativi con backoff e la conferma in due giri |
| ctrgsr.camcom.gov.it | 1 | errore TLS sul bot | la pagina è di **Bitdefender** (l'antivirus del portatile intercetta il traffico) | **non valutabile** dal portatile. Il tentativo ora è marcato «interferenza locale» ed escluso |

## Correzioni introdotte (metodo 1.1.0-beta)
1. Se nessuna identità è accettata, nemmeno il browser reale, e non c'è una firma di WAF, l'esito è «accesso negato a tutti i client», non «bloccato da WAF/anti-bot» (`esporta.arricchisci`; test `test_cat_accesso_negato_a_tutti_e_interferenza`).
2. Gli errori di rete si ritentano con backoff (10 s, 30 s). Un blocco è «confermato» solo se si ripete in due giri distanti almeno 60 minuti. Se l'ultimo giro non lo riproduce, l'esito torna «accessibile».
3. Si confrontano le origini: datacenter contro residenziale («WAF per IP/ASN»).
4. Le pagine di antivirus locali (Bitdefender, Kaspersky, ESET, Avast) sono escluse come interferenza dell'osservatore.

## Limiti
- Il portatile ha un antivirus che intercetta HTTPS (Bitdefender): per la beta va tenuto presente. Per un'origine residenziale pulita serve escludere i siti dalla scansione oppure usare una macchina senza intercettazione.
- 53 enti su circa 1.300 bloccati sondati al momento del controllo. Le stime di precisione per esito valgono per questo campione.

## Prove
- Tentativi dal portatile: `lavoro/trasparenza-fp/pacchetto-fp/` (`tentativi.jsonl` e log grezzi con sha256), importati nel database del server con origine «desktop».
- robots.txt riletti con curl dal portatile; regole riportate nel registro di questa sessione.
