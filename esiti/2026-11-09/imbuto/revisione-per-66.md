### 4.3.2 Revisione delle proposte della via 6 (2026-11-09)

Revisione indipendente (AGENTS § 3) delle 178 proposte di passaggio a «certo» della via 6, S1 escluso (verso S5 e cloud certo), con `tools/verifiche/imbuto_via6_revisione.py`. Una proposta entra nei totali solo se: C1 ha una fonte primaria (atto archiviato con sha256 il cui testo cita il CIG); C2 le regole R/A/B di `verifica_imbuto.py` rieseguite danno lo stesso esito e i campi sono coerenti con lo stato; C3 per il cloud, il prodotto identificato porta alla giurisdizione del dizionario dei marchi (`config/marchi_cloud.yaml`); C4 una seconda lettura cieca (Claude Opus, istruzioni diverse, solo gli estratti degli atti archiviati, niente web) dice la stessa cosa con certezza alta. Esito `esiti/2026-11-09/imbuto/revisione-via6.json`, coda `revisione-coda-discordi.csv` [V].

**Seconda lettura:** 175 su 178 candidati letti; esiti {'concorde': 62, 'non-confermato': 76, 'discorde': 37, 'da-leggere': 3}. **PARZIALE**: i non letti restano fuori dai totali.

| gruppo e strato proposto | proposti | C1 fonte primaria | C1+C2+C3 | entra nei totali (C1-C4) |
|---|---:|---:|---:|---:|
| CTL cloud certo, IT | 2 CIG, 0,4 M€ | 2 CIG, 0,4 M€ | 2 CIG, 0,4 M€ | 2 CIG, 0,4 M€ |
| CTL verso S5 (ICT non cloud) | 2 CIG, 0,4 M€ | 2 CIG, 0,4 M€ | 2 CIG, 0,4 M€ | 1 CIG, 0,3 M€ |
| G1 cloud certo, extra-UE | 2 CIG, 53,8 M€ | 0 | 0 | 0 |
| G1 cloud certo, IT | 2 CIG, 14,9 M€ | 1 CIG, 8,0 M€ | 1 CIG, 8,0 M€ | 0 |
| G1 cloud certo, UE | 1 CIG, 14,4 M€ | 1 CIG, 14,4 M€ | 1 CIG, 14,4 M€ | 1 CIG, 14,4 M€ |
| G1 verso S5 (ICT non cloud) | 65 CIG, 1,77 mld | 23 CIG, 596,0 M€ | 22 CIG, 532,1 M€ | 9 CIG, 387,0 M€ |
| G3 cloud certo, extra-UE | 1 CIG, 1,7 M€ | 1 CIG, 1,7 M€ | 1 CIG, 1,7 M€ | 0 |
| G3 cloud certo, IT | 4 CIG, 10,9 M€ | 1 CIG, 2,4 M€ | 1 CIG, 2,4 M€ | 0 |
| G3 cloud certo, UE | 3 CIG, 9,8 M€ | 3 CIG, 9,8 M€ | 3 CIG, 9,8 M€ | 3 CIG, 9,8 M€ |
| G3 verso S5 (ICT non cloud) | 96 CIG, 208,4 M€ | 14 CIG, 34,0 M€ | 13 CIG, 30,8 M€ | 5 CIG, 10,0 M€ |
| tutti cloud certo, extra-UE | 3 CIG, 55,5 M€ | 1 CIG, 1,7 M€ | 1 CIG, 1,7 M€ | 0 |
| tutti cloud certo, IT | 8 CIG, 26,2 M€ | 4 CIG, 10,8 M€ | 4 CIG, 10,8 M€ | 2 CIG, 0,4 M€ |
| tutti cloud certo, UE | 4 CIG, 24,2 M€ | 4 CIG, 24,2 M€ | 4 CIG, 24,2 M€ | 4 CIG, 24,2 M€ |
| tutti verso S5 (ICT non cloud) | 163 CIG, 1,98 mld | 39 CIG, 630,4 M€ | 37 CIG, 563,3 M€ | 15 CIG, 397,4 M€ |

- **Casi discordi in coda per Fabio:** 37 (`revisione-coda-discordi.csv`, con motivazione breve).
- **Cosa resta fuori:** le proposte senza fonte primaria (C1) restano proposte da rivedere anche se la seconda lettura concorda: senza un atto che cita il CIG la classificazione si regge su ricerche e deduzioni.
- Il gruppo CTL è di controllo e non si somma a G1 e G3; la riga «tutti» li comprende.
