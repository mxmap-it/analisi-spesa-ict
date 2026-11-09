"""Etichette del sesto campione a cieco (annotatore Claude, criterio «prodotto comprato», v4.4). Uso: python et6.py <campione-cieco.csv> <etichette.csv>"""
import csv, sys
csv.field_size_limit(10**8)
MS, AWS, G, O, SF, AD, VM, SAP, PSN = "Microsoft", "Amazon Web Services", "Google", "Oracle", "Salesforce", "Adobe", "VMware", "SAP", "Polo Strategico Nazionale"
E = {
1: MS, 2: "altro:zucchetti", 3: ("altro:point-gedi", ""), 5: SAP, 6: O,
7: ("", "affiancamento/assistenza su M365: servizio, nessuna licenza"), 8: AWS,
9: ("", "migrazione su Azure: servizi su piattaforma"), 10: MS, 11: MS, 12: "altro:halley", 13: "altro:dasein",
14: (("ServiceNow"), "solo «SERVICE NOW», probabile sottoscrizione via rivenditore"), 15: "Zoom", 16: MS, 17: MS, 18: MS, 19: AD,
20: (PSN, "servizi di migrazione comprati dentro la convenzione PSN (venditore PSN): caso di confine"),
21: ("altro:dev4side", "WAF e supporto Azure/O365: servizio"), 22: ("", "assistenza su VMware: servizio"), 23: MS, 24: MS, 25: SF,
27: "altro:namirial", 28: O, 30: SAP, 31: AD, 32: "altro:maggioli", 33: MS,
34: ("altro:laser-romae", "IaaS gestita «(VMware)» di un provider locale: non prodotto VMware"), 35: MS, 36: AD, 37: O, 38: MS, 39: MS,
40: "altro:infor", 41: MS, 42: (AWS, "servizi cloud AWS in managed service: si compra anche il consumo AWS (ambiguo)"),
43: ("", "supporto su Azure: servizio"), 45: (MS, "canone annuale del cloud Office 365 e Halley: ambiguo, letto come sottoscrizione"),
47: G, 48: G, 50: ("", "supporto al RUP della concessione PSN"), 51: VM, 52: ("altro:greenext", "aggiornamento modulo WMS su AWS: servizio"),
53: SAP, 54: "altro:processframe", 55: SAP, 56: "", 57: "altro:advenias", 58: ("", "migrazione a M365: servizio"),
59: (AWS, "AQ per AWS cloud e servizi di manutenzione"), 60: AD, 61: "altro:fortinet", 62: MS, 63: "Cisco Webex", 66: MS, 67: AD,
68: ("altro:alfabitomega", "migrazione in cloud, Nextcloud come software: servizio"), 69: (MS, "licenze Office Professional Plus con PC"),
71: "altro:mys", 72: "altro:siscom", 73: ("altro:log80", "migrazione su DC Lepida"), 74: AD, 75: "altro:halley",
76: ("", "servizi professionali su VMware/Microsoft"), 78: ("altro:ads", "migrazione su PSN da terzi: servizio"), 79: MS,
82: ("", "supporto e conduzione Azure/M365: servizio"), 84: ("altro:3cime", "backup nel DC Lepida"), 85: (MS, "hardware, servizi e licenze M365"),
88: O, 89: ("", "supporto per Nextcloud open source: servizio, non sottoscrizione detta"), 93: "altro:csi-piemonte", 95: MS, 96: SF,
97: ("altro:iconsulting", "migrazione da Azure Data Factory a Databricks"), 99: "altro:sharegate", 100: G,
102: ("altro:ciditech", "migrazione su PSN da terzi: servizio"), 104: MS, 105: "altro:qstar", 106: "altro:infocamere",
107: ("altro:ricca-it", "gestionale su SAP S/4HANA con hosting, servizi: licenza SAP non detta"), 109: MS, 110: AD, 111: SF,
112: "altro:project", 113: AD, 114: G, 115: "altro:picieffe", 117: ("", "corso Power BI: formazione"), 118: PSN,
120: ("altro:apple", "hardware"), 121: ("", "migrazione posta a Office 365: servizio"), 122: SF,
123: (SF, "consumi Service Cloud Voice venduti da Salesforce"), 124: ("altro:qintesi", "configurazione e migrazione SAP: servizio"), 125: VM,
126: MS, 127: O, 128: ("altro:valyrian", "backlog attività Salesforce: servizi"), 129: "altro:infocert", 130: "altro:municipia",
131: ("altro:palitalsoft", "migrazione su DC Lepida"), 132: MS, 133: G, 134: ("", "testo non dice il prodotto"), 135: AD,
137: (MS, "licenze Exchange Online e migrazione"), 139: MS, 140: MS, 141: MS, 142: O, 143: AWS, 144: "altro:trentino-digitale",
145: O, 146: SAP, 147: ("altro:cpl-concordia", "manutenzione add-on DINETWORK su Dynamics BC: servizio"),
148: ("", "assistenza informatica su più prodotti"), 149: ("", "GCP = Good Clinical Practice, omonimia"),
150: (G, "fornitura e attivazione Google Workspace"), 151: ("altro:berenice", "manutenzione applicativo con hosting su Azure incluso"),
153: (MS, "sviluppi su Dynamics 365 BC e licenze Microsoft"), 154: MS, 156: "Cloudera", 157: VM, 158: G, 161: AWS,
162: "altro:meteda", 163: ("altro:mvc", "manutenzione sito con spostamento in Azure dell'ente"), 164: MS, 165: ("altro:apple", "hardware"),
166: O, 167: PSN, 168: ("altro:flagmii", "assistenza procedura ex SPC Cloud lotto 1: non SPC Cloud"),
169: ("", "canone di assistenza Fastweb per abilitazione al cloud AWS: servizio (ambiguo)"),
170: ("", "migrazione a OneDrive: servizio"), 171: (O, "ampliamento Exadata: prodotto Oracle on-premises"), 172: O,
173: "altro:nemea", 174: "altro:consorzio-comuni-trentini", 175: O, 176: ("", "assistenza tecnica su Azure: servizio"), 179: O, 180: AD,
181: SF, 182: (SAP, "SAP Analytics Cloud"), 183: (O, "manutenzione HW Exadata da Oracle"), 184: AD, 185: MS, 186: "altro:csi-piemonte",
187: O, 189: "altro:inaz", 192: MS, 193: "altro:maggioli", 194: (VM, "assistenza, fornitura e componenti VMware"), 195: MS, 196: G, 197: MS,
198: "altro:maggioli", 199: (G, "attivazione Google Workspace con formazione e spazio cloud (ambiguo)"),
200: ("altro:winning", "sviluppo su IBM FileNet: servizio"), 201: ("altro:deda-next", "«Next Cloud» di Deda, omonimia con Nextcloud"),
202: MS, 203: PSN, 204: AD, 205: G, 206: MS, 207: "altro:lepida", 208: "altro:tai", 209: (MS, "licenze Microsoft, Veeam, VMware: prevale Microsoft"),
211: ("", "assistenza Nextcloud/Wazuh: servizio"), 214: MS, 216: "altro:halley", 217: AD, 218: AD, 219: MS, 220: "altro:maggioli", 221: AD,
222: AD, 223: AD, 224: VM, 225: MS, 226: O, 228: O, 229: MS, 230: O, 231: AD, 232: MS, 233: "altro:exetesis", 234: G, 235: SF,
236: O, 237: MS, 238: "altro:csi-piemonte", 239: O, 240: ("altro:deda-digital", "manutenzione sito con hosting in AWS incluso"),
241: ("altro:afi", "backup di terzi per G Suite"), 242: G, 243: SAP, 245: ("", "assistenza sistemistica SQL Server: servizio"),
246: (MS, "licenze M365 e migrazione"), 249: G,
}
GIUR = {MS: "EXTRA-UE", AWS: "EXTRA-UE", G: "EXTRA-UE", O: "EXTRA-UE", SF: "EXTRA-UE", AD: "EXTRA-UE", VM: "EXTRA-UE", "Zoom": "EXTRA-UE",
        "Cisco Webex": "EXTRA-UE", "ServiceNow": "EXTRA-UE", "Cloudera": "EXTRA-UE", SAP: "UE", PSN: "IT"}
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
assert len(rows) == 250
with open(sys.argv[2], "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n"); w.writerow(["cig", "etichetta_prodotto", "giurisdizione", "fonte", "nota"])
    for r in rows:
        v = E.get(int(r["n"]), "")
        lab, nota = v if isinstance(v, tuple) else (v, "")
        w.writerow([r["cig"], lab, GIUR.get(lab, ""), "oggetto ANAC (nessun atto archiviato per questi CIG)", nota])
