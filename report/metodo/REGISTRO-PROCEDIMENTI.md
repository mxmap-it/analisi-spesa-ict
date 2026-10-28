# Registro dei procedimenti: attribuzione della spesa cloud

Ogni tentativo è registrato con la stessa struttura: **ipotesi, approccio, risultato, errori, correzione,
commit**. Gli errori restano scritti anche dopo la correzione: servono a chi rivede il metodo per capire
perché una regola è fatta così. Ogni passo si rifà con il commit indicato
(`git checkout <commit>` e poi `tools/misura_cloud.sh`).

Livello del risultato: **misurato** (prodotto da uno script su dati archiviati con sha256), **stimato**
(dipende da un'ipotesi dichiarata), **da verificare** (osservato, non ancora controvalidato).

---

## 1. Pilota sul 2025 (27/10/2026)

- **Ipotesi.** Nei dati ANAC il provider si riconosce dal marchio nella descrizione e dal lotto
  dell'accordo quadro.
- **Approccio.** Vie 1 (lotto), 2 (lotto nel testo), 3 (marchio), 5 (fornitore = provider) su
  `cig-2025`.
- **Risultato.** La classe "cloud generico" era dominata dai massimali: i 10 contratti più grandi
  valevano l'85% dell'importo. *Misurato.*
- **Correzione.** Si escludono dalle somme i CIG padre degli accordi quadro.
- **Commit.** Precedenti a `4bf74cb`.

## 2. Campione di sviluppo, regole v2 (27/10/2026)

- **Approccio.** Campione stratificato di 745 contratti, letti 190, per correggere le regole.
- **Errori trovati.**
  - Sigle PSN omonime (Piano sanitario, PO).
  - AQ 2213 scambiato per il 2746.
  - "Ariba" che riconosceva "Garibaldi".
  - "Servizi applicativi in ottica cloud" contato come cloud.
  - Router Aruba e MPLS Retelit.
- **Correzione.** Esclusioni e marchi nuovi, in `config/marchi_cloud.yaml`.
- **Commit.** `4bf74cb`, `9db45cf`.

## 3. Misura v2 (27/10/2026)

- **Approccio.** Campione di misura di 717 contratti, distinto da quello di sviluppo. Annotate
  437 righe da Claude, **non alla cieca**.
- **Risultato.**
  - Provider corretto nel 94,6% dei casi; provider e tipo corretti nell'86,6%.
  - Fra i non attribuiti, 20 su 124 erano cloud.
  - *Misurato, ma l'annotazione non è indipendente.*
- **Errori trovati (classi).**
  - Omonimie PSN: piano PAC e sviluppo rurale; connettività e firewall "PSN".
  - "GCP" con il significato di Good Clinical Practice.
  - Switch HPE Aruba.
  - Ambienti di sviluppo classificati come servizi.
  - Contratti misti licenze + servizi.
  - Marchi mancanti: SAP S/4HANA e R/3, Exchange 365, "MO 365", Oracle ULA, Nextcloud.
  - Provider italiani mancanti: TIM cloud, Fastweb hosting, SPC Cloud lotto 1, in-house.
- **Commit.** `9442a34`, `dd32085`.

## 4. Regole v3 e classificatore come modulo testato (28/10/2026)

- **Approccio.**
  - Regole riscritte dalle classi di errore della misura v2.
  - Classificatore estratto in una funzione pura (`tools/analisi/classifica.py`).
  - Ogni errore diventa un caso in `tests/casi_classifica.yaml`.
  - Le 437 righe della misura v2 diventano **campione di sviluppo**: non valgono più come misura.
- **Errori introdotti e trovati dai test.**
  - Gli in-house rubavano i contratti VMware e Oracle a Lepida e Sogei. Correzione: in-house in
    fondo al dizionario, con contesto cloud obbligatorio.
  - "Servizi cloud Oracle" non era riconosciuto: mancava l'ordine inverso.
  - "Upgrade hardware" escludeva un contratto Oracle ULA.
  - La regola PSN con contesto obbligatorio perdeva "adesione PSN".
- **Commit.** Da `4c63769` a `2057103`.

## 5. VMware riclassificato (28/10/2026, indicazione di Fabio)

- **Decisione.** VMware è software per costruire cloud in casa, non un cloud provider. Diventa tipo
  `software-infrastruttura`, fuori dalla misura cloud, e viene usato per il punto aperto #52.
- **Commit.** `db5e82a`.

## 6. Primo calcolo completo v3 e controllo dei grandi importi (28/10/2026)

- **Errore 1, grave: doppio conteggio.**
  - Gli aggiornamenti mensili ANAC (delta) contengono CIG di **tutti** gli anni, dal 2007 al 2026,
    e venivano sommati ai file annuali.
  - Esempio: l'adesione PSN "wave 1-ter", da 118,2 milioni, contata due volte.
  - Lo stesso errore era nel riepilogo v2 pubblicato (`report/metodo/attribuzione-riepilogo-2026-10-27.json`).
  - **Correzione.** Per ogni CIG vale l'ultima versione pubblicata (il delta vince) e il contratto
    va all'anno di pubblicazione.
  - *Misurato:* distribuzione di `anno_pubblicazione` nel delta.
- **Errore 2: RTI.**
  - La via 5 attribuiva al provider un contratto vinto da un raggruppamento in cui il provider era
    solo mandante. Esempio: un RTI guidato da GPI, con TIM fra i membri, risultava "TIM cloud".
  - **Correzione.** La via 5 vale solo se *tutti* gli aggiudicatari sono il provider.
- **Errore 3.** La via 5 non applicava l'esclusione di "in ottica cloud" e "cloud enabling".
  Corretto.
- **Marchi mancanti.** "Servizi cloud Google", "Microsoft Enterprise Agreement", "SPC Cloud- lotto 1".
- **Commit.** `c25aa6f`.

## 7. Importi da verificare (28/10/2026)

- **Osservazione.** In molte adesioni l'importo del lotto sembra il massimale della convenzione,
  non la spesa dell'ente. *Da verificare.* Esempi:
  - 430,0 milioni identici per Banca d'Italia e, due volte, per Infocamere (Microsoft EA);
  - 607,4 milioni per ASL NA3 Sud;
  - 723,3 milioni per un museo (convenzione PSN del DTD).
- **Approccio: regola trasparente, non correzione.**
  - Si marcano i contratti di almeno 50 milioni e quelli con un importo identico (≥ 5 milioni)
    presso enti diversi.
  - Si pubblicano i totali con e senza questi contratti, insieme all'elenco
    (`importi-da-verificare`).
  - La verifica caso per caso si fa sui documenti di gara.
- **Altro osservato.** 789 contratti hanno come aggiudicatario "IMPRESA INESISTENTE"
  (registro R13). *Da classificare.*
- **Commit.** `06a48fa`, `9efedf3`.

## 8. Collegamento ai finanziamenti PNRR cloud (28/10/2026)

- **Ipotesi.** I contratti collegati, tramite CUP, a una candidatura finanziata dalla Misura 1.2
  ("Abilitazione e facilitazione migrazione al cloud") o 1.1 sono spesa cloud per definizione.
  Quindi:
  - la quota che il classificatore non attribuisce stima in modo **indipendente** il cloud che
    sfugge alle vie 1-5;
  - la spesa PNRR cloud si ripartisce per provider e giurisdizione (#43).
- **Fonti.**
  - Dati aperti PA Digitale 2026 (DTD), archiviati: `config/pnrr-risorse.txt`.
  - Dataset ANAC `cup` (CIG-CUP).
- **Conseguenza.** I finanziamenti partono dal 2022, quindi la misura è stata estesa al 2022-2026.
- **Commit.** `9dfb52a`, `8121f6e`, `7269a52`.
- **Risultato.** *(in calcolo)*
