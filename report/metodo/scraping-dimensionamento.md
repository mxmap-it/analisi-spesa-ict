# Acquisizione degli atti su larga scala: studio di dimensionamento (avviato 3/11/2026, #55)

Stato: **in corso**. Le cifre arriveranno dalle misure sui campioni (contratti Microsoft, progetti PSN). Finché non ci sono, qui ci sono solo domande e metodo.

## Perché
L'imbuto lascia incerti contratti per circa 3 miliardi l'anno sul solo cloud. Per chiuderli serve l'atto dell'ente: determina, carrello, progetto PSN. Su scala nazionale sono **decine di migliaia di atti** da cercare.

Regola (Fabio, 3/11/2026): **l'accesso civico viene dopo lo scraping**. Si chiede solo ciò che lo scraping non ha trovato, e solo per un ente il cui portale è stato effettivamente consultato. La strategia di accesso civico e il suo strumento di automazione si disegnano più avanti, a partire da questo studio.

## Cosa misuriamo (per ente e per contratto)
File: `report/convenzioni/ea-campione/metriche-scraping.csv`, poi lo stesso formato per il PSN.

| misura | serve a |
|---|---|
| tipo di ente, dominio | stratificare i costi |
| piattaforma del portale di Amministrazione trasparente e dell'albo (se dichiarata; altrimenti «ignota») | capire se pochi adattatori coprono molti enti |
| robots.txt e crawl-delay | ritmo consentito, quindi tempo totale |
| albo con storico o solo pubblicazioni correnti | quanti atti sono ancora online dopo il periodo di pubblicazione |
| ricerca interna per oggetto o CIG | costo per atto |
| allegati scaricabili e formato (PDF testo, scansione, p7m) | costo di estrazione (OCR) |
| richieste HTTP, tempo, esito e motivo | resa e costo per atto trovato |

## Domande a cui rispondere
1. **Resa:** su 100 contratti cercati, quanti atti con il dato utile si trovano, per tipo di ente? Ricerca web finora: circa l'11 % (V, 62 contratti Microsoft).
2. **Concentrazione delle piattaforme:** quanti fornitori di portali coprono la maggior parte degli enti? È un'**ipotesi da misurare**, non un fatto. Se è vera, lo scraping si fa con un adattatore per piattaforma invece che ente per ente.
3. **Tempo:** richieste per atto × ritmo consentito dal robots.txt → giorni-macchina per 10.000 e per 50.000 contratti.
4. **Durata della pubblicazione:** gli albi tengono gli atti 15 giorni; l'Amministrazione trasparente in genere più a lungo. Quanta parte del 2024-2025 è ancora online?
5. **Estrazione:** quota di scansioni e di p7m, quindi costo di OCR (vedi `dimensionamento.md`).
6. **Confine per l'accesso civico:** criterio documentato di «portale consultato, atto assente», contratto per contratto.

## Output previsto
- Costo per atto trovato, per tipo di ente e per piattaforma.
- Dimensionamento: macchine, giorni, disco, OCR, da integrare in `dimensionamento.md`.
- Architettura: adattatori per piattaforma, coda ripartibile, archivio content-addressed, registro dei tentativi utilizzabile come prova nell'accesso civico.
- Lista dei contratti per i quali lo scraping ha fallito, con il motivo: è l'ingresso della futura strategia di accesso civico.

## Prime misure (3/11/2026, campione licenze Microsoft, V)
Fonte: `report/convenzioni/ea-campione/metriche-scraping.csv`, log delle richieste sul server in `lavoro/ea-campione/l4/richieste.jsonl`.

- **Ricerca web per CIG/oggetto:** 7 atti su 62 contratti cercati (~11 %).
- **Portali degli enti (L4), 38 enti, 93 richieste, ~10 minuti di rete:**

| esito | enti |
|---|---|
| carrello trovato | 2 |
| atto senza carrello | 8 |
| atto non trovato | 10 |
| portale non navigabile | 18 |

- **Cause del «non navigabile»** (nulla aggirato):
  - protezioni anti-bot o WAF: 6 enti;
  - robots.txt che vieta la ricerca: 4;
  - sito irraggiungibile o certificato non valido: 4;
  - pagine navigabili solo a click (postback ASP.NET): 1.
- **Albi a scadenza:** in un caso (ASL Pescara) l'atto è nell'indice ma il testo è stato tolto a fine affissione. È un limite strutturale per gli atti 2024-2025.
- **Piattaforme:**
  - **DigitalPA** (`portaletrasparenza.net`) ha ricerca per CIG, URL stabili e allegati scaricabili. Costa 2-4 richieste per contratto, con crawl-delay di 5 s. L'abbiamo incontrata su 9 enti, da cui vengono 2 carrelli su 2. È il primo candidato per un adattatore.
  - Piattaforme dichiarate incontrate: ISWEB, Netribe on.Cube, Maggioli JCityGov. Le altre sono «ignote».
- **Lettura:** anche quando l'atto c'è, il carrello in euro manca spesso. Nella maggior parte dei casi l'atto riporta solo l'importo, oppure prodotti senza prezzi. Lo scraping ente per ente ha resa bassa; conviene lavorare per piattaforma.

**Prossimo passo proposto:** censire quanti enti usano ciascuna piattaforma (dal dominio e dal footer dei siti di IndicePA), poi un adattatore DigitalPA e una misura della resa su un campione ampio.

## Censimento delle piattaforme e dell'accessibilità (3/11/2026, #61)
Il monitor `tools/trasparenza/` riconosce la piattaforma di ogni sezione «Amministrazione trasparente» (regole in `piattaforme.py`, «ignota» se non certa) e misura i blocchi (robots, noindex, WAF). È l'ingresso per scegliere gli adattatori: concentrazione per host dal registro ANAC L.190 (3/11/2026, 30.701 enti): avcp.trasparenza-pa.net 2.834 enti, halleyweb.com 1.454, servizipubblicaamministrazione.it 1.419, trasparenzascuole.it 1.185, nuvola.madisoft.it 740, spaggiari.eu 460, apkappa 302. Esiti per piattaforma in `sito/static/dati/trasparenza/ultimo/per-piattaforma.csv` a fine giro.
