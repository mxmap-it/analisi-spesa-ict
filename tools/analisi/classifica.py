"""Classificatore del cloud provider: funzione pura, senza accesso ai dati ANAC, riusabile su qualunque fonte di appalti
(OCDS, TED, registri regionali). Metodo: sito/content/progetto/metodo-cloud-provider.md. Test: tests/test_classifica.py.

    from classifica import Classificatore
    c = Classificatore()                      # legge config/lotti_cloud.yaml e config/marchi_cloud.yaml
    c.classifica("Licenze Microsoft 365", aggiudicatari=["TIM S.P.A."])
    -> {"via": "3-marchio", "provider": "Microsoft", "giurisdizione": "EXTRA-UE", "servizio": "cloud",
        "canale": "rivenditore", "regola": "microsoft\\s*365"}

Regole v3 (28/10/2026), ultima revisione v4.5 (9/11/2026, #40/#72: classi d'errore del sesto campione a cieco). Vie: 1 lotto di AQ/convenzione, 2 lotto dichiarato nel testo, 3 marchio, 5 fornitore = provider,
7 indeterminato. Le vie 4 (PSN voce per voce) e 6 (modello linguistico) non sono ancora implementate."""
import re
from pathlib import Path
import yaml

RADICE = Path(__file__).resolve().parents[2]
VERSIONE = "v3.1"
CPV_ICT = re.compile(r"^(48|72|302|3223|3224|3225|3226|50312|50320|51611|64216|64222)")  # 79342 marketing tolto il 7/11/2026 (#44, review in report/cpv/review-79342-3224/)
# via 2: solo riferimenti espliciti alla seconda edizione: "Public Cloud IaaS e PaaS" (ID 2213) ha lotti diversi
# #41/#40 9/11/2026: "2746" solo come numero a sé (prima colpiva "GARA ANAC 9127462", "ACTC227464") e solo con contesto cloud/Consip
RX_AQ2746 = re.compile(r"(?<!\d)2746(?!\d)|iaas\s*(e|/|-)?\s*paas\s*(2|ed\.?\s*2|edizione\s*2)\b", re.I)
RX_CONTESTO_AQ = re.compile(r"\b(iaas|paas|cloud|consip|accordo\s+quadro|aq)\b", re.I)
RX_MULTILOTTO = re.compile(r"\blott[oi]\s*(n\.?\s*)?\d.{0,400}?\blott[oi]\s*(n\.?\s*)?\d", re.I)
RX_LOTTO = re.compile(r"\blott?o\s*n?\.?\s*(\d)\b", re.I)
RX_CLOUD = re.compile(r"\bcloud\b|\bsaas\b|\biaas\b|\bpaas\b|\bhosting\b|data\s*cent(er|re)|\bhousing\b", re.I)
# "servizi applicativi in ottica cloud" (AQ Consip) è sviluppo applicativo, non servizio cloud
RX_NON_CLOUD = re.compile(r"in\s+ottica\s+cloud|cloud\s+native\s+development|cloud\s+enabling|servizi\s+applicativi\s+cloud", re.I)
# servizi professionali su una piattaforma: il prodotto è giusto ma non è spesa in abbonamento.
# v3: "ambienti di sviluppo" e "sandbox" sono abbonamento; i contratti misti (licenze + servizi) restano abbonamento
RX_SERVIZI = re.compile(r"sviluppo\s+(evolutiv|applicativ|software|di\s+nuov)|sviluppo\s*,?\s*e?\s*(manutenzione|assistenza)|manutenzione\s+(evolutiva|correttiva|applicativa|di\s+base|base)|manutenzione\s+e\s+supporto|\bams\b|"
                        r"implementazion|integrazion|change\s+request|personalizzazion|migrazion|assistenza\s+(specialistica|sistemistica)|supporto\s+(specialistico|all.adoption)|"
                        r"servizi\s+(professionali|specialistici)|affiancamento|conduzione\s+sistemistica|attivit\w+\s+sistemistic|consulenz|\bbasis\b|unified\s+support|"
                        # v4.4 #40 cieco 5: supporto tecnico, application maintenance, evolutive, servizi applicativi (AQ 2610), assistenza e supporto/manutenzione
                        r"supporto\s+tecnico|application\s+maintenance|\bevolutiv[ea]\s+su\b|servizi\s+applicativi|assistenza\s*(,|e)\s*(manutenzione|supporto)|manutenzione\s+e\s+assistenza", re.I)
# v4.4 #40 cieco 5: formazione, POC e supporto a una gara non comprano il prodotto (vale anche per i marchi di licenza: Cloudera)
RX_SUPPORTO_NON_PRODOTTO = re.compile(r"\bpoc\b|proof\s+of\s+concept|supporto\s+(\w+\s+){0,2}gara|\bformazion|\bcors[oi]\b|docenz", re.I)
# v4.4 #40 cieco 5: consulenza sulle licenze (assessment, licensing advisory) è un servizio anche se il testo dice «licenze»
RX_CONSULENZA_LICENZE = re.compile(r"(consulenz|assessment|advisory)\w*\s+(\w+\s+){0,3}licenz|licensing\s+advisory|ottimizzazione\s+(del\s+)?contratt|"
                                   r"(formazion|cors[oi])[^|]{0,30}(utilizzo|uso)\W+(\w+\W+){0,2}licenz", re.I)  # v4.5 cieco 6: corso «per l'utilizzo di licenze» Power BI
# v4.5 #40 cieco 6: «assistenza/supporto/migrazione» DAVANTI al marchio (nella stessa parte del testo, entro 150 caratteri) =
# servizio sulla piattaforma, salvo che il testo compri licenze, sottoscrizioni, crediti, servizi cloud o un canone annuale.
# Marchi cloud e PSN: basta «assistenza/supporto/migrazione/configurazione/affiancamento/backlog/manutenzione ed aggiornamenti».
# Marchi di licenza e VMware: il «supporto tecnico per il prodotto Oracle», «assistenza e manutenzione database Oracle»,
# «rinnovo supporto VMware» sono il supporto del produttore, cioe acquisto del prodotto (ciechi 4-6): conta solo il lavoro
# sistemistico di un terzo (assistenza sistemistica/su/ai sistemi, supporto specialistico, servizi professionali, giornate,
# migrazione, configurazione, system architect/administrator) e mai se il testo parla di prodotti, rinnovo o fornitura.
RX_SERV_PRIMA_CLOUD = re.compile(r"assistenz|supporto|migrazion|servizi\s+professional|configurazion|affiancamento|backlog|manutenzione\s+ed?\s+aggiornament", re.I)
RX_SERV_PRIMA_LICENZA = re.compile(r"assistenza\s+(sistemistic|su\b|tecnica\s+ed?\s+informatica)|assistenza\s+e\s+supporto\s+ai\s+sistemi|supporto\s+specialistic|"
                                   r"servizi?\s+professional|giornate|migrazion|configurazion|system\s+(architect|administrator)", re.I)
RX_ACQUISTO = re.compile(r"licenz|sottoscrizion|crediti|subscription|abbonament|canone\s+annual|servizi\s+(cloud|iaas|paas|saas)\b|fornitura\s+(\w+\s+){0,2}prodott", re.I)
RX_ACQUISTO_LICENZA = re.compile(r"prodott|rinnov|fornitura|\bcanone\s+di\s+manutenzione", re.I)
RX_CANONE_ASSISTENZA = re.compile(r"canone\s+(di\s+)?assistenz", re.I)  # «canone assistenza» di un partner (Fastweb su AWS)
# un contratto misto (abbonamento + servizi) resta abbonamento: è la voce di costo principale e la dipendenza da misurare
RX_ABBONAMENTO = re.compile(r"licenz|crediti|sottoscrizion|abbonament|subscription|canone|servizi\s+(cloud|iaas|paas|saas)\b|(acquisizione|fornitura)\s+di\s+prodotti|"
                            r"adesion\w*\s+(\w+\s+){0,3}(polo\s+strategico|psn)|contratto\s+di\s+utenza|infrastruttura\s+cloud\s+in\s+adesione", re.I)
# v3.1 (29/10/2026, indicazione di Fabio): telefonia VoIP e centralino in cloud (UCaaS) hanno un tipo a sé, "telefonia".
# Vale solo se la telefonia è l'oggetto: con il provider da via 5 (telco, hosting) o ignoto (via 7), o con un marchio di sola
# comunicazione (Webex). Se c'è un'altra piattaforma (Microsoft 365, Salesforce) o altro cloud (IaaS, data center, backup) vince quella.
RX_TELEFONIA = re.compile(r"voip|voice\s+over\s+ip|centralin|pbx\b|\bucaas\b|unified\s+communication|comunicazione\s+unificata|sip\s+trunk|telefonia\s+(ip|cloud|virtuale)", re.I)
# centralino ospitato dal fornitore: è cloud anche se il testo non dice "cloud"
RX_TELEFONIA_CLOUD = re.compile(r"centralin\w*\s+(telefonic\w+\s+)?(virtual|in\s+cloud|cloud|hosted|ospitat)|virtual\s*(ip\s*)?pbx|(cloud|hosted)\s*pbx|pbx\s+(virtual|hosted|in\s+cloud)|\bucaas\b|voip\s+in\s+cloud", re.I)
RX_ALTRO_CLOUD = re.compile(r"\b(iaas|paas|saas)\b|data\s*cent|server\s+virtual|macchine\s+virtual|backup|storage|cloud\s+computing|hosting\s+(web|sito|siti)", re.I)
# v4.4 #40 cieco 5: un collegamento (fibra, IP transit, MPLS) verso un data center non è acquisto di cloud: niente via 5
# per la telco (Fastweb, TIM) salvo che il testo compri anche hosting/IaaS/servizi cloud
RX_CONNETTIVITA = re.compile(r"fibra\s+ottica|ip\s+transit|connettivit|\bmpls\b|collegament", re.I)
RX_ANCHE_CLOUD = re.compile(r"\b(iaas|paas|saas)\b|hosting|housing|servizi\s+cloud|server\s+virtual|macchine\s+virtual", re.I)
MARCHI_COMUNICAZIONE = {"Cisco Webex", "Zoom"}
NOME_CANONICO = {"AWS": "Amazon Web Services", "Google Cloud": "Google", "Microsoft Azure": "Microsoft", "Oracle Cloud": "Oracle", "IBM Cloud": "IBM"}


class Classificatore:
    def __init__(self, lotti=RADICE / "config/lotti_cloud.yaml", marchi=RADICE / "config/marchi_cloud.yaml"):
        self.marchi = yaml.safe_load(open(marchi, encoding="utf-8"))
        for m in self.marchi:
            m["rx"] = [re.compile(r, re.I) for r in m["regex"]]
            m["ex"] = [re.compile(r, re.I) for r in m.get("escludi", [])]
            m["fx"] = [re.compile(r, re.I) for r in m.get("fornitori", [])]
        self.lotti = {}
        for ini in yaml.safe_load(open(lotti, encoding="utf-8")):
            for l in ini["lotti"]:
                self.lotti[l["cig"]] = dict(l, iniziativa=ini["iniziativa"])
        self.lotto_n = {str(l.get("lotto")): l for l in self.lotti.values() if l.get("lotto")}
        self.giur = {m["provider"]: m["giurisdizione"] for m in self.marchi}
        # piattaforme di prodotto: se il testo ne nomina una, la telefonia è accessoria (es. Teams Phone dentro Microsoft 365)
        self.piattaforme = {"Microsoft", "Amazon Web Services", "Google", "Oracle", "IBM", "Salesforce", "ServiceNow", "SAP", "Adobe"}
        # chi è il provider stesso (per distinguere vendita diretta da rivendita)
        self.propri = {}
        for m in self.marchi:
            # rti: soci del concessionario (es. PSN: TIM, Leonardo, CDP, Sogei) che incassano come provider; contano solo per il canale
            self.propri.setdefault(m["provider"], []).extend(m["fx"] + [re.compile(r, re.I) for r in m.get("rti", [])])

    def marchio(self, testo):
        """Primo marchio del dizionario che compare nel testo e non è escluso; restituisce (voce, regola)."""
        # #40/#41 9/11/2026, «marchio di un altro lotto»: il testo è «oggetto del lotto | oggetto della gara». Se la gara
        # elenca più lotti e l'oggetto del lotto non nomina marchi del dizionario, il marchio nella gara è di un altro lotto.
        parti = testo.split(" | ", 1)
        if len(parti) == 2 and parti[0].strip() and RX_MULTILOTTO.search(parti[1]):
            m, r = self._marchio(parti[0])
            return (m, r) if m else (None, "")
        return self._marchio(testo)

    def _marchio(self, testo):
        for m in self.marchi:
            for r in m["rx"]:
                if r.search(testo) and not any(e.search(testo) for e in m["ex"]):
                    return m, r.pattern
        return None, ""

    def marchi_presenti(self, testo):
        """Tutti i provider nominati nel testo (non solo il primo): serve alla mappa dei rivenditori, es. PSN + Azure."""
        return sorted({NOME_CANONICO.get(m["provider"], m["provider"]) for m in self.marchi
                       if any(r.search(testo) for r in m["rx"]) and not any(e.search(testo) for e in m["ex"])})

    def _servizio_davanti(self, serv, testo, rx):
        """v4.5: servizio nominato davanti al marchio, senza acquisto di licenze/sottoscrizioni/crediti."""
        if serv not in ("cloud", "psn", "licenza", "software-infrastruttura") or not rx:
            return False
        if RX_CANONE_ASSISTENZA.search(testo):
            return True
        if RX_ACQUISTO.search(testo):
            return False
        if serv in ("licenza", "software-infrastruttura"):
            if RX_ACQUISTO_LICENZA.search(testo):
                return False
            rxp = RX_SERV_PRIMA_LICENZA
        else:
            rxp = RX_SERV_PRIMA_CLOUD
        for parte in testo.split(" | "):
            for r in rx:
                if (mm := r.search(parte)) and rxp.search(parte[max(0, mm.start() - 150):mm.start()]):
                    return True
        return False

    def _servizio(self, serv, testo, provider="", rx=None):
        if serv in ("cloud", "psn", "") and RX_TELEFONIA.search(testo) and not RX_ALTRO_CLOUD.search(testo) \
                and (provider in MARCHI_COMUNICAZIONE or provider not in self.piattaforme):
            return "telefonia"
        if self._servizio_davanti(serv, testo, rx):
            return "servizi-professionali"
        if serv in ("cloud", "psn", "licenza") and RX_CONSULENZA_LICENZE.search(testo):
            return "servizi-professionali"
        if serv in ("cloud", "psn") and RX_SERVIZI.search(testo) and not RX_ABBONAMENTO.search(testo):
            return "servizi-professionali"
        if serv in ("cloud", "psn", "licenza") and RX_SUPPORTO_NON_PRODOTTO.search(testo) and not RX_ABBONAMENTO.search(testo):
            return "servizi-professionali"
        return serv

    def _e_cloud(self, testo):
        return bool((RX_CLOUD.search(testo) or RX_TELEFONIA_CLOUD.search(testo)) and not RX_NON_CLOUD.search(testo))

    def canale(self, provider, aggiudicatari):
        """diretto se un aggiudicatario è il provider stesso, rivenditore se no, ignoto senza aggiudicatari."""
        if not aggiudicatari: return "ignoto"
        fx = self.propri.get(provider, [])
        return "diretto" if any(f.search(n) for f in fx for n in aggiudicatari) else "rivenditore"

    def classifica(self, testo, cig_accordo_quadro="", aggiudicatari=(), cpv=""):
        """Restituisce un dict con via, provider, giurisdizione, servizio, canale, regola; None se fuori perimetro ICT."""
        aggiudicatari = [a for a in aggiudicatari if a]
        via = prov = serv = regola = ""
        if cig_accordo_quadro in self.lotti:
            l = self.lotti[cig_accordo_quadro]
            via, prov, serv, regola = "1-lotto", l["provider"], "cloud", f"cig_accordo_quadro={cig_accordo_quadro}"
        elif RX_AQ2746.search(testo) and RX_CONTESTO_AQ.search(testo) and (mm := RX_LOTTO.search(testo)) and mm.group(1) in self.lotto_n:
            via, prov, serv, regola = "2-lotto-nel-testo", self.lotto_n[mm.group(1)]["provider"], "cloud", f"AQ 2746 lotto {mm.group(1)}"
        else:
            m, regola = self.marchio(testo)
            if m:
                via, prov, serv = "3-marchio", m["provider"], self._servizio(m["servizio"], testo, m["provider"], m["rx"])
            elif self._e_cloud(testo) and not RX_NON_CLOUD.search(testo) \
                    and not (RX_CONNETTIVITA.search(testo) and not RX_ANCHE_CLOUD.search(testo)):
                # via 5 solo se TUTTI gli aggiudicatari sono il provider: in un RTI la mandante (es. TIM con GPI) non dice il prodotto
                for m in self.marchi:
                    if m["servizio"] != "licenza" and m["fx"] and aggiudicatari and all(any(f.search(n) for f in m["fx"]) for n in aggiudicatari) \
                            and (f := next(f for f in m["fx"] if f.search(aggiudicatari[0]))):
                        via, prov, serv, regola = "5-fornitore", m["provider"], self._servizio(m["servizio"], testo, "via5"), f.pattern
                        break
        if not via:
            # i CPV di telefonia (642) entrano solo per il centralino ospitato: il resto della telefonia è fuori perimetro
            if cpv and not CPV_ICT.match(cpv) and not (cpv.startswith("642") and RX_TELEFONIA_CLOUD.search(testo)): return None
            via = "7-indeterminato-cloud" if self._e_cloud(testo) else "0-ict-non-cloud"
            if via[0] == "7": serv = self._servizio("", testo)
        prov = NOME_CANONICO.get(prov, prov)
        canale = self.canale(prov, aggiudicatari) if prov else ""
        # v4.5 #40 cieco 6: migrazione/sviluppo di un terzo (non l'in-house) verso il data center in-house = servizio del terzo
        if serv == "in-house" and canale == "rivenditore" and RX_SERVIZI.search(testo) and not RX_ABBONAMENTO.search(testo):
            serv = "servizi-professionali"
        return {"via": via, "provider": prov, "giurisdizione": self.giur.get(prov, ""), "servizio": serv,
                "canale": canale, "regola": regola}
