"""Etichette del settimo campione a cieco (annotatore Claude, 19/11/2026, criterio «prodotto comprato», regole v4.5 congelate).
Lette solo dal file mescolato campione-cieco.csv (senza strato né uscita della lente). Vuoto = nessun prodotto del dizionario
comprato (servizio, hardware, software di altri); «altro:x» = prodotto fuori dal dizionario.
Uso: python tools/verifiche/lente_cieco7_etichette.py report/metodo/lente-cieco-7/campione-cieco.csv report/metodo/lente-cieco-7/etichette.csv"""
import csv, sys
csv.field_size_limit(10**8)
MS, AWS, G, O, SF, AD, VM, SAP, PSN = "Microsoft", "Amazon Web Services", "Google", "Oracle", "Salesforce", "Adobe", "VMware", "SAP", "Polo Strategico Nazionale"
IH = "In-house pubblico"
SERV = lambda x: ("", x + ": servizio")
E = {
1: "altro:deda-next", 2: "altro:apkappa", 3: SERV("migrazione Windows Server di terzi"), 4: SERV("manutenzione applicativi SAP S/4HANA di terzi"),
5: SERV("integrazione cyber con Azure"), 6: MS, 7: "altro:moodys", 8: (G, "licenze Google Workspace in convenzione con TIM"), 9: "altro:avaya",
10: MS, 11: AD, 12: (O, "manutenzione sistemi Exadata via rivenditore: supporto del produttore (ambiguo)"),
13: ("altro:recube", "licenze ReVA «powered» AWS: AWS dentro il prodotto di un terzo (confine #70)"), 14: "", 15: O,
16: SERV("supporto al passaggio di DocsPA su PSN"), 17: SF, 18: "", 19: SERV("assistenza sistemistica VMware/NetApp/Veeam di terzi"),
20: MS, 21: MS, 22: "altro:nivi", 23: (VM, "manutenzione vSphere: supporto del produttore"), 24: SAP, 25: "", 26: PSN,
27: (MS, "VDI di un terzo con licenze MS VDA e Office 365 comprate (ambiguo)"), 28: MS, 29: SERV("manutenzione evolutiva S/4HANA di terzi"),
30: (IH, "hosting presso server farm CINECA"), 31: MS, 32: "altro:canto", 33: "altro:softinventive", 34: (IH, "risorse nel DC Lepida"),
35: "", 36: SERV("assistenza e supporto tecnico sulle licenze Oracle da un partner (ambiguo)"), 37: O, 38: MS, 39: "", 40: "altro:halley",
41: VM, 42: PSN, 43: MS, 44: "ServiceNow", 45: (MS, "sottoscrizioni M365 con migrazione e backup"), 46: O,
47: SERV("manutenzione Salesforce di Deloitte"), 48: (VM, "Workspace ONE (AirWatch) col marchio VMware"), 49: "",
50: (AD, "«supporto per l'acquisto di licenze Adobe»: letto come acquisto (ambiguo)"), 51: MS, 52: "altro:artec", 53: MS,
54: "altro:lifesize", 55: AD, 56: SF, 57: "altro:gruppo-marche-informatica", 58: MS, 59: MS, 60: SERV("migrazione Proxysign su PSN"),
61: "altro:apkappa", 62: MS, 63: MS, 64: SERV("supporto Salesforce MuleSoft"), 65: (VM, "«servizi software virtualizzazione VMware» (ambiguo)"),
66: SF, 67: SERV("assistenza sistemistica SQL Server"), 68: (IH, "private cloud INVA"), 69: "", 70: (VM, "supporto e manutenzione vSphere"),
71: AD, 72: SERV("assistenza e manutenzione suite Office 365 e Azure (ambiguo)"), 73: MS, 74: AD, 75: "", 76: MS, 77: G, 78: MS, 79: MS,
80: SERV("formazione Power BI"), 81: "altro:puntozero", 82: (PSN, "adesione alla convenzione PSN"), 83: ("", "notebook con Windows 11: hardware"),
84: AD, 85: SERV("configurazione e manutenzione di licenze Salesforce"), 86: "", 87: ("altro:trentino-digitale", "assistenza e gestione Google Workspace dell'in-house"),
88: (IH, "migrazione e gestione su CSI Nivola"), 89: "", 90: (SAP, "manutenzione licenze SAP"), 91: "altro:pa-digitale",
92: SERV("servizi professionali SharePoint Online"), 93: ("altro:idrostudi", "SaaS di un terzo su AWS (confine #70)"),
94: (O, "basket di attività con Oracle PaaS (ambiguo)"), 95: O, 96: "", 97: SERV("assistenza specialistica Office 365"), 98: MS, 99: "",
100: SF, 101: (O, "servizi professionali e servizi cloud Oracle"), 102: MS, 103: SERV("assessment SQL Server"),
104: (AWS, "infrastruttura del SIL Sardegna su AWS"), 105: "", 106: SERV("consulenza Salesforce"), 107: "Cisco Webex", 108: MS, 109: MS,
110: G, 111: SERV("aggiornamento Windows Server di terzi"), 112: "", 113: AD, 114: "", 115: MS, 116: MS, 117: SERV("supporto app su Salesforce"),
118: "", 119: MS, 120: (O, "canone manutenzione Oracle embedded"), 121: "", 122: (IH, "servizi e hosting virtuale dell'in-house Trentino Digitale"),
123: "", 124: MS, 125: MS, 126: SF, 127: "altro:pa33", 128: MS, 129: "", 130: ("", "manutenzione di terzi su libreria Oracle StorageTek: hardware"),
131: "", 132: "altro:ddmanagement", 133: O, 134: MS, 135: AD, 136: (IH, "servizi di data center Lepida"), 137: O, 138: "", 139: "altro:red-hat",
140: "",
141: MS, 142: ("", "workstation con Windows 11: hardware"), 143: (O, "crediti cloud Oracle e servizi professionali"), 144: AD, 145: "", 146: G,
147: AD, 148: (MS, "licenze Libraesva e Microsoft 365"), 149: MS, 150: "altro:datagraph", 151: (VM, "rinnovo manutenzioni VMware e Veeam con storage (ambiguo)"),
152: "Nextcloud", 153: "altro:ptc", 154: "", 155: ("", "VM con Windows Server e migrazione da un fornitore locale (ambiguo)"), 156: "", 157: AD,
158: (VM, "licenze VMware e Veeam"), 159: "", 160: MS, 161: SERV("supporto e assistenza su Google Workspace"), 162: MS, 163: "", 164: (MS, "licenze M365 con migrazione"),
165: MS, 166: MS, 167: "altro:tuttogare", 168: "", 169: G, 170: VM, 171: O, 172: MS, 173: AWS, 174: (SAP, "manutenzione licenze SAP"), 175: SF,
176: "", 177: "altro:halley", 178: "", 179: MS, 180: ("altro:palitalsoft", "manutenzione moduli e server Aruba Cloud dentro il servizio (ambiguo)"),
181: "altro:bip", 182: (VM, "rinnovo del supporto VMware (ambiguo)"), 183: "altro:anthesi", 184: MS, 185: (MS, "licenze Office 365 e migrazione"),
186: MS, 187: (MS, "posta in bundle Microsoft 365 Business Basic"), 188: ("altro:jpsoft", "private cloud su Aruba dentro il servizio"),
189: (VM, "manutenzione HW Dell e SW VMware"), 190: SAP, 191: "", 192: SERV("migrazione a Exchange Online"), 193: MS,
194: (G, "licenze Google Workspace rivendute dall'in-house con servizi"), 195: SERV("supporto e configurazione Salesforce"), 196: MS, 197: "",
198: O, 199: "altro:fortinet", 200: SAP, 201: "", 202: "altro:graphisoft", 203: SERV("evolutive CRM fatte da Salesforce"), 204: "altro:halley",
205: (SF, "licenze Salesforce e Amazon Connect: prevale Salesforce"), 206: "", 207: "altro:halley", 208: "", 209: "altro:stoelting", 210: MS,
}
GIUR = {MS: "EXTRA-UE", AWS: "EXTRA-UE", G: "EXTRA-UE", O: "EXTRA-UE", SF: "EXTRA-UE", AD: "EXTRA-UE", VM: "EXTRA-UE", "Zoom": "EXTRA-UE",
        "Cisco Webex": "EXTRA-UE", "ServiceNow": "EXTRA-UE", "Cloudera": "EXTRA-UE", SAP: "UE", "Nextcloud": "UE", PSN: "IT", IH: "IT"}
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
assert len(rows) == 210 and set(E) == set(range(1, 211))
with open(sys.argv[2], "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n"); w.writerow(["cig", "etichetta_prodotto", "giurisdizione", "fonte", "nota"])
    for r in rows:
        v = E[int(r["n"])]
        lab, nota = v if isinstance(v, tuple) else (v, "")
        w.writerow([r["cig"], lab, GIUR.get(lab, ""), "oggetto ANAC (nessun atto archiviato per questi CIG)", nota])
