# Sistema Cloud Toscana — scheda di analisi (esempio del [modello](MODELLO.md))

Stato: **bozza in corso**, 29/10/2026 (#55). L'approfondimento sui ruoli dei partner è in [cloud-toscana-ruoli.md](cloud-toscana-ruoli.md). Fonti lette in `lavoro/ricerca_cloud/`, da archiviare con sha256.

**Esito provvisorio.** Cloud sovrano IT, con dipendenze tecnologiche extra-UE: VMware/Broadcom, Microsoft, SAS. È **condizionato** alla verifica del punto 4 (che cosa fanno DXC, IBM e Kyndryl). Confidenza: media.

| # | domanda | risposta | livello | fonte |
|---|---|---|---|---|
| 1 | Dove stanno i dati | Nodo primario TIX, il data center regionale a Firenze. Nodi secondari nei DC TIM di Acilia (DR) e Firenze Bruni (continuità). Che TIX sia della Regione è dedotto dal contratto, che prevede lavori sui suoi impianti. | verificato (contratto quadro, progetti dei fabbisogni); proprietà di TIX dedotta | cq.txt; pf_dsu.txt |
| 2 | Chi opera | Il raggruppamento a mandataria TIM, nel suo insieme. Il contratto **non** dice quale società gestisce quale servizio: rinvia alle domande di partecipazione e all'atto costitutivo del raggruppamento (art. 1, c. 3), che non sono pubblici. | verificato che il riparto non è nel contratto | cq.txt r. 182-191 |
| 3 | Catena di controllo | TIM, Lutech e Dedalus: italiane (Lutech e Dedalus hanno azionisti di fondi esteri, da verificare). Enterprise Services Italia: DXC Technology, USA. IBM Italia: IBM, USA. Kyndryl Italia: Kyndryl, USA; è nata nel 2021 dallo scorporo dei servizi infrastrutturali di IBM e compare negli atti dal 2024. | verificato per i nomi; controllo dei fondi da verificare | dd8446.txt r. 99-120; pf_fi.txt r. 106-128 |
| 4 | Ruolo di ciascuno | **Aperto.** Quote di esecuzione 2019: TIM 41,27%, Lutech 20,48%, DXC 16,53%, Dedalus 11,71%, IBM 9,65%; queste quote possono cambiare in corso di contratto. Kyndryl di mestiere fa *gestione di infrastrutture*, cioè il ruolo (b), e quindi è il punto più delicato. | quote verificate; ruoli da verificare | cq.txt r. 185-197 |
| 5 | Esposizione al CLOUD Act | Se DXC, IBM o Kyndryl gestiscono sistemi con accesso amministrativo ai dati degli enti (ruoli a e b), la loro capogruppo USA ne avrebbe il "controllo": il servizio non sarebbe immune, anche con una quota di minoranza. Se forniscono solo software o consulenza (ruoli c e d), non lo sono. È il criterio indicato da Fabio, da verificare con fonti. | dedotto (analisi giuridica da validare) | 18 U.S.C. § 2713 |
| 6 | Dipendenze tecnologiche | L'ente sceglie tra hypervisor OpenStack (open source) e VMware (a pagamento, "VMM commerciale"). I sistemi operativi Windows Server sono a canone. Tra i SaaS c'è SAS (USA). | verificato (progetto dei fabbisogni TIM per DSU) | pf_dsu.txt |
| 7 | Qualifiche | Catalogo/Marketplace AgID; ISO 27001, 27017 e 27018 (dal sito). La qualifica ACN non è stata trovata: certificazione in corso secondo il BURT di luglio 2026 (riferito). Clausole contro l'accesso di autorità estere: da cercare nel capitolato. | sito verificato; ACN riferito | cloud.toscana.it |
| 8 | Esito | Vedi in testa. Punti aperti: ruoli dei partner (domanda 4), qualifica ACN, clausole contrattuali. Per la quota extra-UE servono i progetti dei fabbisogni dei singoli contratti (quanta parte OpenStack e quanta VMware). | — | — |

**Raccomandazione di policy** emersa (da aggiungere come R19): nei contratti cloud della PA, pubblicare per ogni membro del raggruppamento e per ogni subappaltatore il **ruolo e il livello di accesso ai dati**, con la catena di controllo societario. Oggi il riparto delle prestazioni sta in un atto costitutivo non pubblico.

## Registro delle revisioni

| data | modifica |
|---|---|
| 2026-10-29 | prima stesura dai documenti letti (contratto quadro, progetti dei fabbisogni, DD Firenze 8446/2025) |
