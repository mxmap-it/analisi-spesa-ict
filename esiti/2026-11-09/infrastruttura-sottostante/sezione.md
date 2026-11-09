### Misura 1.2: su quale infrastruttura girano i «prodotti italiani» (v0.1, 9/11/2026, #43 #45)

Verifica `nice .venv/bin/python tools/verifiche/infrastruttura_sottostante.py --data 2026-11-09` → `esiti/2026-11-09/infrastruttura-sottostante/infrastruttura.json` (nessuna rete). Tabella dei fornitori: `config/saas_infrastruttura.yaml`.

**Terzo asse.** Accanto a prodotto e fornitore, la giurisdizione di **chi gestisce l'infrastruttura** su cui il servizio gira (DC proprio in Italia, provider IT-UE, hyperscaler extra-UE).

**1. PSN (389,2 M€ della 1.2).** Fonte nuova [V, A]: *Libro PSN 2025* (bilancio integrato, sha256 b8fe9ec1…; p. 71-72 e 106).
- Ricavi 2025 454,3 M€: migrazione e servizi professionali 360,7 M€ (79 %); **Secure Public Cloud (Azure, Google, AWS) 19,9 M€ + Public Cloud PSN Managed (Oracle Alloy) 4,5 M€ = 5,4 % dei ricavi, 27,3 % dei ricavi infrastrutturali** (2024: 2,6 % e 16,8 %).
- Contratti dall'inizio (3.853 M€): 60 % servizi professionali, 40 % canoni. Canoni: SPC 15 % (PA centrali 24 %, **PA locali 6 %, ASL/AO 7 %**); «Soluzioni Oracle PSN» 14 % (PAL 20 %, ASL 24 %), che mescolano Oracle su Industry Standard e PSN Managed; Hybrid dentro «altri» (< 5 %).
- Per la 1.2 (enti locali e ASL) quota hyperscaler sui canoni: **6,5 % basso (solo SPC), 14,4 % centrale (SPC + Managed stimato al 36 % di Oracle PSN dai ricavi), 33,5 % alto (tutto Oracle PSN + 5 % Hybrid)**.
- Due letture: *stretta* (la migrazione è servizio PSN, IT): 5,1 / 22,4 / 78,2 M€; *destinazione* (la migrazione segue l'infrastruttura, R-S1): **25,3 / 56,1 / 130,4 M€** su 389,2.
- PSN in generale (#45): sui contratti ~6 % SPC (15 % × 40 %) + ~2 % Managed ≈ **8 % del valore ordinato (~0,3 mld su 3,85)**, 5,4 % dei ricavi 2025, ~27 % dell'infrastruttura venduta nel 2025, in crescita. Incertezza: il Libro è del concessionario (fonte unica), la base del 60/40 non è dichiarata, i Contratti di Utenza per ente restano non pubblici (R50).

**2. SaaS dei primi 20 fornitori S2 (130,4 dei 150,2 M€).** Ricerca su siti, DPA, schede, atti (nessun contatto).
- **Nessun hyperscaler accertato.** Infrastruttura IT nota per 56,8 M€ [B]: Maggioli 37,9 (DC proprio Cornaredo + Retelit Bologna, pagina di gruppo), Halley 6,6, Fastweb 4,5, TIM 4,4, Informatica Alto Adige 1,7, Engineering D.HUB 1,6 (IaaS qualificato ACN proprio: inferenza, non dichiarazione per SaaS).
- **Ignota per 93,4 M€ di S2** (Datamanagement 15,1, svic 8,6, APKappa 7,1, Deda Next, Almaviva, Siscom, We-Com, PA Digitale, Kibernetes…), più S3-S4 55,7 M€. Indizi C (Aruba per Kibernetes e Deda; AWS MSP Almaviva) non archiviabili.
- Nessuna classe A: nessun fornitore pubblica l'elenco dei sub-responsabili o l'IaaS sotto ciascun SaaS; la scheda ACN che lo direbbe non è specchiabile (R55). Nuova **R78**.

**3. Misura 1.2 con il terzo asse** (818,9 M€):

| Scenario | big tech prodotto | PSN su hyperscaler | SaaS/S3-S4 ignoti | S5 | S6 | **Totale infra extra-UE** |
|---|---|---|---|---|---|---|
| basso (accertato) | 13,6 | 25,3 | 0 | 0 | 0 | **38,9 M€ (4,7 %)** |
| centrale | 13,6 | 56,1 | 37,3 (25 %, ipotesi) | 28,5 | 33,5 | **169,0 M€ (20,6 %)** |
| alto | 13,6 | 130,4 | 149,1 | 28,5 | 162,3 | **483,9 M€ (59,1 %)** |

- Rispetto alla lente prodotto (1,7 %) la soglia accertata sale a **4,7 %** per il solo PSN su hyperscaler [V, lettura destinazione]. La stima centrale (~21 %) **dipende da un'ipotesi non misurata** (25 % dei SaaS ignoti su hyperscaler) e dal residuo S6: è un ordine di grandezza, non un fatto. L'intervallo 4,7-59 % misura quanto poco si sa.
- L'infrastruttura italiana dei SaaS noti è [B], non [A].
