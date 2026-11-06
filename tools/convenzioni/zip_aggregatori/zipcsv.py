import json,csv,re
I=json.load(open("zip_indice.json",encoding="utf-8"))
C={
"fcd3c6f47d87b796":("schema_aq_convenzione","Convenzione SIL 3 (assistenza tecnica SILER), Intercent-ER; fornitore RTI Engineering Ingegneria Informatica (mandataria) + Azioninnova + SCS; importo massimo 20.600.000 € IVA esclusa"),
"444c94e511e10d00":("schema_aq_convenzione","Convenzione Business Analytics e Data Management 2 (CIG 9923894067), Intercent-ER, SDA appalto specifico; fornitore Iconsulting S.p.A.; importo massimo 23.662.400 € IVA esclusa"),
"5d19ab46b0fa2d51":("capitolato","Capitolato BA&DM 2 (all. 4): stack di riferimento con marchi (Microsoft Power BI/SQL Server/Azure Data Lake, SAP BW/4HANA e BusinessObjects, Oracle, Tableau, Amazon S3/MinIO, Kafka); nessun prezzo"),
"5cc930d5ced5c6a1":("capitolato","Allegato 4A al capitolato BA&DM 2: profili e attività; nessun prezzo"),
"f54f8579312ba126":("schema_aq_convenzione","Convenzione Sanzioni Polizia Locale 4 lotto 1 (CIG 9580558E8E); fornitore RTI Municipia S.p.A. + I.C.A. S.r.l.; importo massimo 18.834.886,40 €; 48 mesi"),
"cf9df8989fed8001":("schema_aq_convenzione","Convenzione Sanzioni Polizia Locale 4 lotto 2 (CIG 9580560039); fornitore Safety21 S.p.A.; importo massimo 5.748.618,62 €; 48 mesi"),
"d642ad1a9c5ffd01":("listini","Listino lotto 1 aggiornato 3/2/2026 (Municipia): prezzi unitari offerti con adeguamento, es. notifica postale 1,82 -> 1,86 €, PEC 1,30 -> 1,33 €, ora extra 20 -> 20,44 €, canone device 5 -> 5,11 €; nessun marchio"),
"8ad39c6ed1d55b55":("listini","Listino lotto 1 originario (Municipia): prezzi offerti, notifica postale 1,82 €, PEC 1,30 €, ora extra 20 €, canone device 5 €"),
"24906be4e7fdc8a0":("listini","Listino lotto 2 (Safety21): aggio offerto 13,75% per notifiche all'estero"),
"e62446e61067f5a3":("capitolato","Capitolato tecnico lotto 1 sanzioni PL 4: servizi di gestione verbali/notifiche; cita genericamente cloud, nessun prezzo"),
"346464452573b969":("capitolato","Capitolato tecnico lotto 2 sanzioni PL 4 (notifiche all'estero); nessun prezzo"),
"1718eb14ff2b6aa1":("schema_aq_convenzione","Convenzione telefonia lotti 1 (CIG 9016294130, reti fisse) e 2 (CIG 9016295203, reti mobili); fornitore Telecom Italia/TIM S.p.A.; importo massimo 31 M€ (L1) e 37 M€ (L2) IVA esclusa"),
"54007c1c276f9679":("schema_aq_convenzione","Convenzione lotto 3 (CIG 90162962D6) gestione e manutenzione apparati di telefonia; fornitore Fastweb S.p.A.; 48 mesi"),
"327bca9d11538a2f":("listini","Listino adeguamenti apparati lotto 3 (Fastweb): migliaia di apparati con marchio, codice e prezzo (Avaya, Unify, Alcatel, Poly, Panasonic, Siemens, Cisco, Mitel; es. Alcatel Temporis 10 PRO 11,97 €)"),
"e601b899ae65321f":("listini","Listino codificato lotto 3 Fastweb (conv. 00004188, RSPIC.2022.138): manutenzione quadriennale per derivato per livelli di qualità, presidio on site; prezzi unitari"),
"475904a624b8585f":("listini","Listino espansione rete passiva lotto 3 (Fastweb): punti rete RJ45 cat. 6a 275-312,5 €, fibra OM4 13-31 €/m, cassetti ottici 300-562,5 €"),
"d8a04bc54755bb16":("listini","Listino servizi aggiuntivi lotto 1 rev. 2024 (TIM): coefficienti per durata, router+SIM (es. 150 € una tantum + 23 €/mese), servizi di collaborazione (Microsoft Teams, Zoom citati)"),
"7a26edd603045dbf":("listini","Listino servizi aggiuntivi lotto 2 (TIM): router LTE con modello e prezzo (Lipari 5100 20,28 € + 7,81 €/mese; Imola 5262 ...), cita Aruba e Motorola"),
"84a0cb1041d607a4":("listini","Listino prezzi lotto 1 (TIM): canoni mensili per linea/accesso, es. RTG 4,00 €, VoIP 1,10 €, TDA 2 7,90 €, TDAG 200 24,00 €"),
"dd54b4e952ad830c":("listini","Listino prezzi lotto 2 (TIM): traffico dati a plafond 0,75-4,00 €/mese, noleggio terminali Android 1,00-4,20 €, iOS top 10,00 €/mese, tablet"),
"de9a454305ae4400":("altro","Schede descrittive servizi aggiuntivi lotto 2 (TIM), descrizione servizi senza prezzi"),
"e5c56548dff70219":("altro","Schede descrittive servizi aggiuntivi lotto 1 (TIM) rev. 02, descrizione servizi senza prezzi"),
"d64469bc6ca6249a":("progetti_fabbisogni","Modello vuoto «Dettaglio fabbisogni» lotto 3 (da compilare dall'ente)"),
"efedbcb657499b13":("progetti_fabbisogni","Modello A6B piano dei fabbisogni fonia (vuoto, da compilare)"),
"ecdf6461830c5a13":("progetti_fabbisogni","Modello A6C piano dei fabbisogni servizi dati (vuoto)"),
"2944f39d5991c8df":("progetti_fabbisogni","Modello A6D piano fabbisogni servizi aggiuntivi (vuoto)"),
"5c67c620407e3c73":("altro","A8 schede tecniche terminali VoIP (TIM)"),
"6090e5a774abd535":("altro","A8 elenco terminali VoIP (TIM), solo immagini, testo non estraibile"),
"0b05b4e3dd649034":("listini","Allegato SIM e terminali radiomobili rev17 04/2026 (TIM): schede dei terminali in noleggio con marchio (Samsung, Apple, Motorola, ZTE, Oppo, Nokia); prezzi nel listino lotto 2"),
"89dea8d579410530":("offerta_economica","Modello vuoto C.2 scheda di dettaglio dell'offerta economica (conservazione a norma ESTAR, 72 mesi, costo a GB): NON è l'offerta dell'aggiudicatario"),
"b36b06055e36dab1":("capitolato","Allegato CS-1 canali e modelli di conservazione esistenti per azienda sanitaria toscana; nessun prezzo"),
"fc9179209dd4f2fd":("bando","Bando GA24_006 CSI Piemonte (AQ servizi per Fondi SIE): valore 44 M€, lotti 1 e 2 17 M€ ciascuno, lotto 3 10 M€"),
"0972c647994438f4":("disciplinare","Disciplinare GA24_006 (CSI Piemonte, AQ servizi informatici Fondi SIE, 3 lotti)"),
"60729a8eb58465c2":("schema_aq_convenzione","Schema di accordo quadro GA24_006 (CSI Piemonte), senza fornitore né prezzi"),
"341ff096a27b66aa":("disciplinare","Disciplinare GA23_006 (CSI Piemonte, AQ piattaforme middleware abilitanti, 6 lotti)"),
"a76a952fd70a2ec9":("schema_aq_convenzione","Schema di accordo quadro GA23_006 (CSI Piemonte), senza fornitore né prezzi"),
"b8066e54de09bb04":("chiarimenti","Errata corrige GA23_006 (p7m): sostituisce i profili professionali del lotto 6"),
"d6c855a65e22325f":("disciplinare","Disciplinare GA23_011 (CSI Piemonte, AQ servizi ad alta specializzazione, 3 lotti; lotto 1 piattaforma pagamenti elettronici)"),
"a5ec7fcad2e81c9a":("schema_aq_convenzione","Schema di accordo quadro GA23_011 (CSI Piemonte), senza fornitore né prezzi"),
"86d0f9721dab0ea2":("capitolato","Allegato A contesto tecnologico CSI Piemonte (GA23_006 e GA23_011, stesso file): infrastruttura su cloud Nivola (CSP qualificato AgID, 252 citazioni), WSO2, Oracle, PostgreSQL, Red Hat, SAP, Microsoft"),
"67b8e3109c36ce0d":("capitolato","Allegato A contesto tecnologico GA24_006: cloud Nivola (CSI), SAP, Microsoft, Kubernetes"),
}
def regola(n):
  b=n.split("/")[-1]
  if "ACbis" in b:
    m=re.search(r"LOTTO_(\d)",b); return ("offerta_economica",f"Modello vuoto di listino prezzi unitari lotto {m.group(1)} (tariffe GG/PP e FP a base di gara, colonne sconto/offerta da compilare): NON è l'offerta dell'aggiudicatario")
  if "Requisiti_tecnici" in b: return ("capitolato","Requisiti tecnici del "+re.search(r"LOTTO ?\d",b).group(0).lower()+" (servizi a GG/PP, nessun prezzo né marchio di prodotto venduto)")
  if "Scheda" in b and "A." in b: return ("capitolato","Scheda tecnica del contesto informatico di un ambito ("+b.split("_")[-1][:-4]+")"+("; cita Oracle" if "Agricoltura" in b else ""))
  return None
out=open("zip-letti-2026-11-07.csv","w",encoding="utf-8",newline="")
w=csv.writer(out,lineterminator="\n"); w.writerow("iniziativa,zip,sha256_zip,file_interno,sha256_file,tipo_documento,contenuto,livello".split(","))
nr=0
for i in I:
  if not i["rilevante"]: continue
  s=i["sha256_file"][:16]; n=i["file_interno"]; b=n.split("/")[-1]
  if s in C: t,c=C[s]
  elif b.startswith("Listino ") and "Convenzioni_2023" in n:
    L=open("../t62_testi/"+s+".txt",encoding="utf-8").read().splitlines(); rows=[l.split(" | ") for l in L[2:] if re.match(r"\d+ \| ",l)]
    cig=sorted({r[3] for r in rows}); pr=[]
    for r in rows:
      for x in r[9:14]:
        try: pr.append(float(x)); break
        except: pass
    prod=sorted({(r[6] if r[5][:1].isdigit() else r[5]).split(" - ")[0].strip()[:40] for r in rows})[:4]
    fo=b[8:-5].strip(); match=" (CIG dell'iniziativa)" if i["iniziativa"][4:] in cig else ""
    t,c="listini",f"Listino dell'aggiudicatario {fo}, AQ manutenzione software sanitario Intercent-ER, CIG lotto {','.join(cig)}{match}: {len(rows)} voci, prezzi {min(pr):g}-{max(pr):g} € IVA escl.; prodotti: {'; '.join(prod)}"
  else:
    r=regola(n)
    if not r: print("MANCA",s,n); continue
    t,c=r
  w.writerow([i["iniziativa"],i["zip"],i["sha256_zip"],n,i["sha256_file"],t,c,"V"]); nr+=1
print(nr)
