# Modello di analisi di un'infrastruttura cloud con dubbi di giurisdizione

Versione 1, 29/10/2026 (#55). Si usa quando un servizio non è attribuibile con le regole: cloud regionali, consorzi, raggruppamenti misti italiani/esteri, offerte "sovrane" su tecnologia di terzi. Esempio svolto: [cloud-toscana.md](cloud-toscana.md).

Il criterio deciso (DECISIONI.md, 29/10/2026): la giurisdizione è quella del **controllo giuridico di chi eroga e opera il servizio**. Data center in Italia/UE + operatore UE a controllo UE, non soggetto a leggi extraterritoriali (CLOUD Act, FISA 702) = **cloud sovrano**, anche con software extra-UE, che si registra come dipendenza tecnologica.

## Le domande, in ordine

Per ognuna: risposta, livello (**verificato** su fonte primaria letta, con pagina; **riferito**; **dedotto**), fonte.

1. **Dove stanno i dati.** Data center, città, proprietario dell'edificio e degli apparati. Copie, backup e DR: anche loro.
2. **Chi opera il servizio.** Il soggetto giuridico che gestisce l'infrastruttura (sistemisti, rete, backup, sicurezza): personale e accessi amministrativi (root, console, chiavi).
3. **Catena di controllo di ogni soggetto con accesso.** Per ogni società del raggruppamento, i subappaltatori e il fornitore della tecnologia: sede, capogruppo fino al vertice, paese. Una controllata italiana di una capogruppo USA è nella catena USA.
4. **Ruolo di ciascun soggetto.** Per ogni soggetto, una tra:
   - (a) proprietà o gestione dell'infrastruttura con accesso ai dati;
   - (b) servizi gestiti con accesso amministrativo;
   - (c) consulenza o sviluppo senza accesso stabile ai dati di produzione;
   - (d) sola fornitura di software o licenze;
   - (e) hardware.

   Contano (a) e (b). La quota percentuale di esecuzione da sola non basta: una quota piccola con accesso root pesa più di una quota grande di consulenza.
5. **Esposizione a leggi extraterritoriali.** Il CLOUD Act (18 U.S.C. § 2713) obbliga il fornitore di servizi di comunicazione o di calcolo remoto a consegnare i dati in suo "possesso, custodia o controllo", ovunque si trovino. Quindi la domanda è se un soggetto della catena USA ha possesso, custodia o controllo dei dati (ruoli a e b). Un fornitore di sole licenze (ruolo d) non lo è, per i dati. Resta però il rischio di dipendenza: aggiornamenti, licenze che si collegano al produttore, telemetria, interruzione della fornitura.
6. **Dipendenze tecnologiche.** Elenca hypervisor, sistemi operativi, database, storage e sicurezza, con produttore e giurisdizione. Indica se esiste un'alternativa aperta già prevista (es. OpenStack accanto a VMware).
7. **Qualifiche e garanzie contrattuali.** Considera:
   - la qualifica ACN e il suo livello;
   - ISO 27001, 27017 e 27018;
   - l'equivalenza con SecNumCloud o EUCS;
   - le clausole contrattuali contro l'accesso di autorità estere: art. 48 GDPR, obbligo di notifica, divieto di trasferimento.
8. **Esito.** Indica:
   - la giurisdizione: IT, UE, EXTRA-UE o ignota;
   - se è cloud sovrano: sì, no o condizionato;
   - le dipendenze tecnologiche;
   - la confidenza;
   - i punti aperti, ciascuno con il documento che li chiuderebbe;
   - le raccomandazioni di policy che ne derivano, con un riferimento a `richieste-e-raccomandazioni.yaml`.

## Come si registra

- Una scheda markdown per infrastruttura in questa cartella, con un registro delle revisioni in fondo.
- Una voce nella base di conoscenza `report/metodo/llm/conoscenza-iniziative.yaml`, con i campi `classificazione_decisa`, `sovranita`, `dipendenze` e `fonti`.
- I CIG che vi aderiscono ereditano l'esito nel registro di classificazione (`dati/classificazioni/`), tramite un passaggio `tabella` che cita la scheda.
- I documenti letti vanno nell'archivio con sha256 e nel dataset CIG → atti (`dati/atti/`).
