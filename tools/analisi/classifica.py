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
VERSIONE = "v3"
CPV_ICT = re.compile(r"^(48|72|302|3223|3224|3225|3226|50312|50320|51611|64216|64222|79342)")
# via 2: solo riferimenti espliciti alla seconda edizione: "Public Cloud IaaS e PaaS" (ID 2213) ha lotti diversi
RX_AQ2746 = re.compile(r"2746|iaas\s*(e|/|-)?\s*paas\s*(2|ed\.?\s*2|edizione\s*2)\b", re.I)
RX_LOTTO = re.compile(r"\blott?o\s*n?\.?\s*(\d)\b", re.I)
RX_CLOUD = re.compile(r"\bcloud\b|\bsaas\b|\biaas\b|\bpaas\b|\bhosting\b|data\s*cent(er|re)|\bhousing\b", re.I)
# "servizi applicativi in ottica cloud" (AQ Consip) è sviluppo applicativo, non servizio cloud
RX_NON_CLOUD = re.compile(r"in\s+ottica\s+cloud|cloud\s+native\s+development|cloud\s+enabling|servizi\s+applicativi\s+cloud", re.I)
# servizi professionali su una piattaforma: il prodotto è giusto ma non è spesa in abbonamento.
# v3: "ambienti di sviluppo" e "sandbox" sono abbonamento; i contratti misti (licenze + servizi) restano abbonamento
RX_SERVIZI = re.compile(r"sviluppo\s+(evolutiv|applicativ|software|di\s+nuov)|manutenzione\s+(evolutiva|correttiva|applicativa|di\s+base|base)|manutenzione\s+e\s+supporto|\bams\b|"
                        r"change\s+request|personalizzazion|migrazion|assistenza\s+specialistica|servizi\s+(professionali|specialistici)|conduzione\s+sistemistica|attivit\w+\s+sistemistic|consulenz", re.I)
RX_ABBONAMENTO = re.compile(r"licenz|crediti|sottoscrizion|abbonament|subscription|rinnovo|canone", re.I)
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
        # chi è il provider stesso (per distinguere vendita diretta da rivendita)
        self.propri = {}
        for m in self.marchi:
            self.propri.setdefault(m["provider"], []).extend(m["fx"])

    def marchio(self, testo):
        """Primo marchio del dizionario che compare nel testo e non è escluso; restituisce (voce, regola)."""
        for m in self.marchi:
            for r in m["rx"]:
                if r.search(testo) and not any(e.search(testo) for e in m["ex"]):
                    return m, r.pattern
        return None, ""

    def _servizio(self, serv, testo):
        if serv in ("cloud", "psn") and RX_SERVIZI.search(testo) and not RX_ABBONAMENTO.search(testo):
            return "servizi-professionali"
        return serv

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
                via, prov, serv = "3-marchio", m["provider"], self._servizio(m["servizio"], testo)
            elif RX_CLOUD.search(testo):
                for m in self.marchi:
                    if m["servizio"] != "licenza" and (f := next((f for f in m["fx"] for n in aggiudicatari if f.search(n)), None)):
                        via, prov, serv, regola = "5-fornitore", m["provider"], self._servizio(m["servizio"], testo), f.pattern
                        break
        if not via:
            if cpv and not CPV_ICT.match(cpv): return None
            via = "7-indeterminato-cloud" if RX_CLOUD.search(testo) and not RX_NON_CLOUD.search(testo) else "0-ict-non-cloud"
        prov = NOME_CANONICO.get(prov, prov)
        return {"via": via, "provider": prov, "giurisdizione": self.giur.get(prov, ""), "servizio": serv,
                "canale": self.canale(prov, aggiudicatari) if prov else "", "regola": regola}
