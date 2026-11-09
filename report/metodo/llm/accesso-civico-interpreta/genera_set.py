"""Genera il set sintetico v1 (eseguito una volta; il file prodotto è quello versionato)."""
import json, sys

V2 = [{"id": "v1", "cig": "Z1A2B3C4D5", "oggetto": "Servizio di hosting in cloud del portale istituzionale 2024-2026", "documento_atteso": "contratto e capitolato tecnico"},
      {"id": "v2", "cig": "9A8B7C6D5E", "oggetto": "Licenze Microsoft 365 per 120 postazioni", "documento_atteso": "ordine di acquisto e determina di affidamento"}]
V1 = V2[:1]
V3 = V2 + [{"id": "v3", "cig": "B12C34D56E", "oggetto": "Migrazione dei servizi al Polo Strategico Nazionale", "documento_atteso": "piano dei fabbisogni e contratto di utenza"}]
INT = "Oggetto: Istanza di accesso civico generalizzato ai sensi dell'art. 5, comma 2, del d.lgs. 33/2013 - codice ac-0-00000000001-1.\n"
FIRMA = "\n\nDistinti saluti\nIl Responsabile del Servizio\n[firma oscurata]"

C = []
def c(i, esito, voci, allegati, testo, motivi=(), descr="", varianti=""):
    C.append({"id": f"s{i:02d}", "descrizione": descr, "richiesta": {"id": f"ac-sint-{i:02d}", "voci": voci},
              "allegati": allegati, "testo": INT + testo + FIRMA,
              "atteso": {"esito": esito, "motivi": sorted(motivi)}})

c(1, "accolta", V2, ["contratto_hosting_2024.pdf", "capitolato_tecnico.pdf", "determina_123_2024.pdf", "ordine_MEPA_456789.pdf"],
  "In riscontro alla Sua istanza, pervenuta in data 12/11/2026 prot. n. 34567, si trasmettono in allegato i documenti richiesti relativi ai CIG Z1A2B3C4D5 e 9A8B7C6D5E.",
  descr="accoglimento pieno, allegati per ogni voce")
c(2, "accolta", V1, ["Contratto rep. 88-2024.pdf.p7m"],
  "Con riferimento alla richiesta in oggetto, si comunica che la stessa è accolta. Si allega copia del contratto repertorio n. 88/2024 comprensivo del capitolato tecnico.",
  descr="accolta con file firmato digitalmente")
c(3, "parziale", V2, ["contratto_hosting_2024.pdf"],
  "Si trasmette in allegato il contratto relativo al CIG Z1A2B3C4D5. Per quanto riguarda il CIG 9A8B7C6D5E, si comunica che l'ordine di acquisto non è detenuto da questo Ente in quanto l'acquisto è stato effettuato dalla centrale di committenza regionale.",
  motivi=["inesistente"], descr="parziale: una voce non detenuta")
c(4, "parziale", V2, ["contratto_oscurato.pdf", "determina_45.pdf"],
  "Si accoglie parzialmente la richiesta. Il capitolato tecnico relativo al CIG Z1A2B3C4D5 viene trasmesso con l'oscuramento delle parti contenenti l'architettura di sicurezza dei sistemi, ai sensi dell'art. 5-bis, comma 1, lett. a) del d.lgs. 33/2013, la cui divulgazione potrebbe arrecare pregiudizio alla sicurezza pubblica. Si trasmette integralmente la determina di affidamento.",
  motivi=["5bis-c1-a"], descr="parziale con oscuramento per sicurezza")
c(5, "diniego", V2, [],
  "Con la presente si comunica il diniego all'istanza in oggetto ai sensi dell'art. 5-bis, comma 2, lett. c), del d.lgs. n. 33/2013, in quanto i documenti richiesti contengono informazioni tecniche e commerciali dell'operatore economico la cui divulgazione arrecherebbe un pregiudizio concreto agli interessi economici e commerciali dello stesso, inclusi i segreti commerciali.",
  motivi=["5bis-c2-c"], descr="diniego segreti commerciali")
c(6, "diniego", V3, [],
  "Esaminata l'istanza, si rappresenta che la stessa, per il numero di documenti richiesti e per l'arco temporale interessato, si configura come richiesta massiva e manifestamente irragionevole, tale da comportare un carico di lavoro in grado di interferire con il buon funzionamento dell'amministrazione (cfr. Linee guida ANAC n. 1309/2016, § 4.2). Pertanto la richiesta non può essere accolta.",
  motivi=["massiva"], descr="diniego per richiesta massiva")
c(7, "diniego", V1, [],
  "La richiesta non può essere accolta in quanto la S.V. non ha indicato l'interesse diretto, concreto e attuale sotteso all'istanza, come previsto dalla legge n. 241/1990.",
  motivi=["interesse"], descr="diniego illegittimo: pretende l'interesse (confusione con accesso documentale)")
c(8, "diniego", V2, [],
  "Si comunica che l'istanza è rigettata.",
  motivi=["non-motivato"], descr="diniego senza motivazione")
c(9, "differimento", V1, [],
  "Si comunica che l'accesso al contratto relativo al CIG Z1A2B3C4D5 è differito, ai sensi dell'art. 5-bis, comma 5, del d.lgs. 33/2013, fino alla conclusione della verifica di conformità prevista per il 31/03/2027, in quanto la divulgazione anticipata potrebbe pregiudicare il regolare svolgimento delle attività ispettive in corso.",
  motivi=["5bis-c1-g"], descr="differimento per attività ispettive")
c(10, "chiarimento", V2, [],
  "Al fine di poter dare riscontro alla Sua richiesta, si chiede di voler precisare meglio i documenti di interesse, indicando il periodo di riferimento e gli estremi degli atti, entro 10 giorni dal ricevimento della presente. In mancanza, l'istanza sarà archiviata.",
  descr="chiarimento con termine di 10 giorni")
c(11, "chiarimento", V1, [],
  "Si chiede cortesemente di trasmettere copia di un documento di identità in corso di validità del richiedente, necessario per l'istruttoria dell'istanza.",
  descr="chiarimento: chiede documento d'identità")
c(12, "controinteressati", V2, [],
  "Si comunica che, ai sensi dell'art. 5, comma 5, del d.lgs. 33/2013, è stata data comunicazione della Sua istanza ai soggetti controinteressati, i quali possono presentare motivata opposizione entro dieci giorni dalla ricezione. Il termine di conclusione del procedimento è sospeso fino all'eventuale opposizione dei controinteressati.",
  descr="comunicazione ai controinteressati")
c(13, "rinvio-altro-ufficio", V1, [],
  "Si comunica che la Sua istanza è stata inoltrata, per competenza, al Settore Sistemi Informativi, che provvederà a fornire riscontro direttamente alla S.V.",
  descr="rinvio a ufficio interno")
c(14, "rinvio-altro-ufficio", V2, [],
  "Questa Amministrazione non è competente in merito ai contratti richiesti, stipulati dall'Unione dei Comuni. Si invita pertanto a rivolgere l'istanza all'Unione dei Comuni della Valle, PEC [EMAIL OSCURATA].",
  descr="non competente, rinvio ad altro ente")
c(15, "già-pubblicato", V1, [],
  "Si comunica che i documenti richiesti sono già pubblicati nella sezione Amministrazione Trasparente del sito istituzionale, sottosezione Bandi di gara e contratti, al seguente link: https://www.comune.esempio.it/amministrazione-trasparente/bandi-di-gara-e-contratti/cig-Z1A2B3C4D5 .",
  descr="rinvio a pubblicazione")
c(16, "accolta", V2, ["contratto_hosting_2024.pdf"],
  "Si trasmette il contratto relativo al CIG Z1A2B3C4D5. La determina di affidamento e l'ordine relativi al CIG 9A8B7C6D5E sono consultabili all'albo pretorio online al link https://albo.esempio.it/atti/2024/det-512 , dove sono pubblicati integralmente.",
  descr="accolta: allegato + link che copre l'altra voce")
c(17, "non-pertinente", V1, [],
  "Si comunica che la Sua comunicazione è stata protocollata in data 13/11/2026 con il numero 0045678 ed assegnata all'ufficio competente.",
  descr="avviso automatico di protocollazione")
c(18, "non-pertinente", V1, [],
  "Questo è un messaggio generato automaticamente. La casella di posta certificata è abilitata alla sola ricezione di messaggi PEC; non rispondere a questo messaggio.",
  descr="risposta automatica della casella")
c(19, "diniego", V1, [],
  "Si rigetta l'istanza ai sensi dell'art. 53 del d.lgs. 50/2016 e dell'art. 24, comma 1, della legge 241/1990, trattandosi di atti di gara sottratti all'accesso.",
  motivi=["5bis-c3"], descr="diniego per esclusione di legge sugli atti di gara")
c(20, "parziale", V3, ["contratto_hosting.pdf", "ordine_m365.pdf"],
  "In esito all'istanza si trasmettono i documenti relativi ai CIG Z1A2B3C4D5 e 9A8B7C6D5E. Per il CIG B12C34D56E il piano dei fabbisogni non può essere ostensibile ai sensi dell'art. 5-bis, comma 1, lett. b), trattandosi di informazioni attinenti alla sicurezza nazionale e alla cybersicurezza delle infrastrutture.",
  motivi=["5bis-c1-b"], descr="parziale: una voce per sicurezza nazionale")
c(21, "diniego", V1, [],
  "Si comunica che la documentazione richiesta contiene dati personali dei dipendenti dell'operatore economico; pertanto, a tutela della protezione dei dati personali ai sensi dell'art. 5-bis, comma 2, lett. a), del d.lgs. 33/2013, l'accesso non può essere consentito.",
  motivi=["5bis-c2-a"], descr="diniego per dati personali (sproporzionato: si poteva oscurare)")
c(22, "accolta", V2, ["Prot_45678_allegati.zip"],
  "Gentile richiedente, facendo seguito alla Sua istanza, Le inviamo in allegato quanto richiesto (contratto, capitolato, determina e ordine). Restiamo a disposizione per ogni ulteriore chiarimento.",
  descr="accolta con zip; «chiarimento» compare come cortesia")
c(23, "diniego", V2, [],
  "La richiesta risulta generica e non consente di individuare i documenti oggetto di accesso, configurandosi come richiesta esplorativa. Si dichiara pertanto inammissibile.",
  motivi=["generica"], descr="diniego per genericità")
c(24, "parziale", V2, ["determina_45.pdf"],
  "Si trasmette la determina relativa al CIG 9A8B7C6D5E. Relativamente al CIG Z1A2B3C4D5, il contratto contiene informazioni riservate dell'aggiudicatario: è stata avviata la comunicazione al controinteressato; la S.V. riceverà riscontro all'esito.",
  motivi=[], descr="parziale + controinteressati su una voce (caso ambiguo)")
c(25, "non-pertinente", V1, [],
  "In riferimento alla Sua richiesta di rimborso della TARI anno 2025, si comunica che la pratica è in lavorazione.",
  descr="messaggio di altro procedimento, abbinato per errore")
c(26, "diniego", V1, [],
  "Si comunica che il documento richiesto non è detenuto da questa Amministrazione e pertanto non è possibile dar corso alla richiesta.",
  motivi=["inesistente"], descr="diniego per inesistenza (tutte le voci)")
c(27, "accolta", V1, [],
  "Si comunica che la richiesta è accolta. I documenti sono scaricabili al seguente link temporaneo, valido 30 giorni: https://cloud.esempio.it/s/AbCdEf123 .",
  descr="accolta via link di scaricamento, senza allegati")
c(28, "chiarimento", V2, [],
  "Ai fini dell'evasione dell'istanza si chiede di confermare se la richiesta è riferita ai soli contratti in essere o anche a quelli cessati. Si precisa che il termine di cui all'art. 5, comma 6, decorrerà dalla ricezione del chiarimento.",
  descr="chiarimento con pretesa (infondata) di riavvio del termine")

with open(sys.argv[1], "w", encoding="utf-8") as f:
    for x in C:
        f.write(json.dumps(x, ensure_ascii=False) + "\n")
print(len(C))
