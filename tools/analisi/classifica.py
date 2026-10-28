"""Classificatore del cloud provider: funzione pura, senza accesso ai dati ANAC, riusabile su qualunque fonte di appalti
(OCDS, TED, registri regionali). Metodo: sito/content/progetto/metodo-cloud-provider.md. Test: tests/test_classifica.py.

    from classifica import Classificatore
    c = Classificatore()                      # legge config/lotti_cloud.yaml e config/marchi_cloud.yaml
    c.classifica("Licenze Microsoft 365", aggiudicatari=["TIM S.P.A."])
    -> {"via": "3-marchio", "provider": "Microsoft", "giurisdizione": "EXTRA-UE", "servizio": "cloud",
        "canale": "rivenditore", "regola": "microsoft\\s*365"}

Regole v3 (28/10/2026). Vie: 1 lotto di AQ/convenzione, 2 lotto dichiarato nel testo, 3 marchio, 5 fornitore = provider,
7 indeterminato. Le vie 4 (PSN voce per voce) e 6 (modello linguistico) non sono ancora implementate."""
import re
from pathlib import Path
import yaml

RADICE = Path(__file__).resolve().parents[2]
VERSIONE = "v3.1"
CPV_ICT = re.compile(r"^(48|72|302|3223|3224|3225|3226|50312|50320|51611|64216|64222|79342)")
# via 2: solo riferimenti espliciti alla seconda edizione: "Public Cloud IaaS e PaaS" (ID 2213) ha lotti diversi
RX_AQ2746 = re.compile(r"2746|iaas\s*(e|/|-)?\s*paas\s*(2|ed\.?\s*2|edizione\s*2)\b", re.I)
RX_LOTTO = re.compile(r"\blott?o\s*n?\.?\s*(\d)\b", re.I)
RX_CLOUD = re.compile(r"\bcloud\b|\bsaas\b|\biaas\b|\bpaas\b|\bhosting\b|data\s*cent(er|re)|\bhousing\b", re.I)
# "servizi applicativi in ottica cloud" (AQ Consip) è sviluppo applicativo, non servizio cloud
RX_NON_CLOUD = re.compile(r"in\s+ottica\s+cloud|cloud\s+native\s+development|cloud\s+enabling|servizi\s+applicativi\s+cloud", re.I)
# servizi professionali su una piattaforma: il prodotto è giusto ma non è spesa in abbonamento.
# v3: "ambienti di sviluppo" e "sandbox" sono abbonamento; i contratti misti (licenze + servizi) restano abbonamento
RX_SERVIZI = re.compile(r"sviluppo\s+(evolutiv|applicativ|software|di\s+nuov)|sviluppo\s*,?\s*e?\s*(manutenzione|assistenza)|manutenzione\s+(evolutiva|correttiva|applicativa|di\s+base|base)|manutenzione\s+e\s+supporto|\bams\b|"
                        r"implementazion|integrazion|change\s+request|personalizzazion|migrazion|assistenza\s+(specialistica|sistemistica)|supporto\s+(specialistico|all.adoption)|"
                        r"servizi\s+(professionali|specialistici)|conduzione\s+sistemistica|attivit\w+\s+sistemistic|consulenz|\bbasis\b|unified\s+support", re.I)
# un contratto misto (abbonamento + servizi) resta abbonamento: è la voce di costo principale e la dipendenza da misurare
RX_ABBONAMENTO = re.compile(r"licenz|crediti|sottoscrizion|abbonament|subscription|canone|servizi\s+(cloud|iaas|paas|saas)\b|(acquisizione|fornitura)\s+di\s+prodotti|"
                            r"adesion\w*\s+(\w+\s+){0,3}(polo\s+strategico|psn)|contratto\s+di\s+utenza|infrastruttura\s+cloud\s+in\s+adesione", re.I)
# v3.1 (29/10/2026, indicazione di Fabio): telefonia VoIP e centralino in cloud (UCaaS) hanno un tipo a sé, "telefonia".
# Vale solo se la telefonia è l'oggetto: con il provider da via 5 (telco, hosting) o ignoto (via 7), o con un marchio di sola
# comunicazione (Webex). Se c'è un'altra piattaforma (Microsoft 365, Salesforce) o altro cloud (IaaS, data center, backup) vince quella.
RX_TELEFONIA = re.compile(r"voip|voice\s+over\s+ip|centralin|\bpbx\b|\bucaas\b|unified\s+communication|comunicazione\s+unificata|sip\s+trunk|telefonia\s+(ip|cloud|virtuale)", re.I)
# centralino ospitato dal fornitore: è cloud anche se il testo non dice "cloud"
RX_TELEFONIA_CLOUD = re.compile(r"centralin\w*\s+(telefonic\w+\s+)?(virtual|in\s+cloud|cloud|hosted|ospitat)|virtual\s*(ip\s*)?pbx|(cloud|hosted)\s*pbx|pbx\s+(virtual|hosted|in\s+cloud)|\bucaas\b|voip\s+in\s+cloud", re.I)
RX_ALTRO_CLOUD = re.compile(r"\b(iaas|paas|saas)\b|data\s*cent|server\s+virtual|macchine\s+virtual|backup|storage|cloud\s+computing|hosting\s+(web|sito|siti)", re.I)
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
        for m in self.marchi:
            for r in m["rx"]:
                if r.search(testo) and not any(e.search(testo) for e in m["ex"]):
                    return m, r.pattern
        return None, ""

    def marchi_presenti(self, testo):
        """Tutti i provider nominati nel testo (non solo il primo): serve alla mappa dei rivenditori, es. PSN + Azure."""
        return sorted({NOME_CANONICO.get(m["provider"], m["provider"]) for m in self.marchi
                       if any(r.search(testo) for r in m["rx"]) and not any(e.search(testo) for e in m["ex"])})

    def _servizio(self, serv, testo, provider=""):
        if serv in ("cloud", "psn", "") and RX_TELEFONIA.search(testo) and not RX_ALTRO_CLOUD.search(testo) \
                and (provider in MARCHI_COMUNICAZIONE or provider not in self.piattaforme):
            return "telefonia"
        if serv in ("cloud", "psn") and RX_SERVIZI.search(testo) and not RX_ABBONAMENTO.search(testo):
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
        elif RX_AQ2746.search(testo) and (mm := RX_LOTTO.search(testo)) and mm.group(1) in self.lotto_n:
            via, prov, serv, regola = "2-lotto-nel-testo", self.lotto_n[mm.group(1)]["provider"], "cloud", f"AQ 2746 lotto {mm.group(1)}"
        else:
            m, regola = self.marchio(testo)
            if m:
                via, prov, serv = "3-marchio", m["provider"], self._servizio(m["servizio"], testo, m["provider"])
            elif self._e_cloud(testo) and not RX_NON_CLOUD.search(testo):
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
        return {"via": via, "provider": prov, "giurisdizione": self.giur.get(prov, ""), "servizio": serv,
                "canale": self.canale(prov, aggiudicatari) if prov else "", "regola": regola}
