"""Test dell'interpretazione delle risposte (#58). Eseguire: .venv/bin/python -m unittest tests/test_accesso_civico_interpreta.py
Nessuna chiamata a Claude: l'LLM è sostituito da risposte finte."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / "tools/accesso_civico"))
import interpreta as I  # noqa: E402

SET = R / "report/metodo/llm/accesso-civico-interpreta/set-sintetico-v1.jsonl"
CASI = [json.loads(l) for l in SET.read_text(encoding="utf-8").splitlines() if l.strip()]
PER_ID = {c["id"]: c for c in CASI}


class Regole(unittest.TestCase):
    def test_set_dimensione_e_vocabolario(self):
        self.assertTrue(20 <= len(CASI) <= 30)
        for c in CASI:
            self.assertIn(c["atteso"]["esito"], I.ESITI, c["id"])
            for m in c["atteso"]["motivi"]:
                self.assertIn(m, I.MOTIVI, c["id"])
        self.assertEqual({c["atteso"]["esito"] for c in CASI}, set(I.ESITI))  # ogni esito ha almeno un caso

    def test_regole_mai_sbagliate(self):
        """Le regole possono astenersi, ma quando rispondono devono dare l'esito atteso (precisione 100 % sul set)."""
        for c in CASI:
            r, tr = I.regole(c)
            if r:
                self.assertEqual(r["esito"], c["atteso"]["esito"], (c["id"], tr))

    def test_copertura_minima(self):
        coperti = sum(1 for c in CASI if I.regole(c)[0])
        self.assertGreaterEqual(coperti, len(CASI) // 2)

    def test_motivi_regole(self):
        for c in CASI:
            r, _ = I.regole(c)
            if r and r["esito"] in I.CON_MOTIVO:
                self.assertEqual(r["motivi"], c["atteso"]["motivi"], c["id"])

    def test_astensione_casi_ambigui(self):
        for i in ("s24", "s25", "s03", "s04"):  # parziale/controinteressati misti, altro procedimento, parziali
            self.assertIsNone(I.regole(PER_ID[i])[0], i)

    def test_accolta_senza_allegati_ne_link_si_astiene(self):
        c = dict(PER_ID["s02"], allegati=[])
        self.assertIsNone(I.regole(c)[0])

    def test_citazioni_letterali(self):
        for c in CASI:
            r, _ = I.regole(c)
            if r:
                self.assertTrue(r["citazioni"], c["id"])
                for q in r["citazioni"]:
                    self.assertIn(q, c["testo"])

    def test_motivi_da_testo(self):
        self.assertEqual(I.motivi_da_testo("ai sensi dell'art. 5-bis, comma 2, lett. a)"), ["5bis-c2-a"])
        self.assertEqual(I.motivi_da_testo("art. 5 bis c. 3"), ["5bis-c3"])
        self.assertEqual(I.motivi_da_testo("richiesta massiva"), ["massiva"])


class LLM(unittest.TestCase):
    def test_uscita_valida(self):
        c = PER_ID["s24"]
        g = json.dumps({"esito": "parziale", "motivi": ["5bis-c2-c", "inventato"], "voci_fornite": [{"voce": "v2", "documenti": ["d"]}],
                        "voci_non_fornite": [{"voce": "v1", "motivo": "altro"}, {"voce": "vX"}], "confidenza": "alta",
                        "citazioni": ["Si trasmette la determina relativa al CIG 9A8B7C6D5E."]})
        o, err = I.analizza_uscita("testo prima " + g + " dopo", c)
        self.assertEqual(err, [])
        self.assertEqual(o["motivi"], ["5bis-c2-c"])
        self.assertEqual([x["voce"] for x in o["voci_non_fornite"]], ["v1"])
        self.assertEqual(o["confidenza"], "alta")

    def test_citazione_inventata_abbassa_confidenza(self):
        g = json.dumps({"esito": "diniego", "confidenza": "alta", "citazioni": ["frase che non c'è"]})
        o, err = I.analizza_uscita(g, PER_ID["s25"])
        self.assertEqual(o["confidenza"], "bassa")
        self.assertTrue(err)

    def test_non_json(self):
        self.assertEqual(I.analizza_uscita("non so", PER_ID["s25"]), (None, ["uscita non JSON"]))

    def test_interpreta_usa_llm_solo_se_regole_astengono(self):
        chiamate = []
        finto = lambda t, m: chiamate.append(m) or json.dumps({"esito": "non-pertinente", "confidenza": "alta",
                                                                "citazioni": ["la pratica è in lavorazione"]})
        r1 = I.interpreta(PER_ID["s01"], llm=finto, blob=False)
        self.assertEqual((r1["fonte"], chiamate), ("regole", []))
        r2 = I.interpreta(PER_ID["s25"], llm=finto, blob=False)
        self.assertEqual((r2["fonte"], r2["interpretazione"]["esito"], len(chiamate)), ("modello", "non-pertinente", 1))
        self.assertEqual([p["tipo"] for p in r2["passaggi"]], ["regola", "modello"])
        self.assertEqual(r2["passaggi"][1]["versione"], "istruzioni-v1")


class Proposte(unittest.TestCase):
    def test_evento_e_coda(self):
        casi = {"accolta": ("risposta", "esame-risposta"), "diniego": ("risposta", "seguito"),
                "chiarimento": ("richiesta-chiarimento", "chiarimento"),
                "controinteressati": ("comunicazione-controinteressati", "controinteressati"),
                "rinvio-altro-ufficio": (None, "abbinamento"), "non-pertinente": (None, "abbinamento"),
                "differimento": ("risposta", "seguito"), "già-pubblicato": ("risposta", "esame-risposta")}
        for e, (tipo, coda) in casi.items():
            ev, c = I.evento_proposto({"esito": e, "motivi": []}, "ac-x", "2026-12-01")
            self.assertEqual((ev and ev["tipo"], c), (tipo, coda), e)
        ev, _ = I.evento_proposto({"esito": "differimento", "motivi": ["5bis-c1-g"]}, "ac-x", "2026-12-01")
        self.assertEqual(ev["dati"]["esito"], "diniego")

    def test_evento_proposto_valido_per_stati(self):
        import stati
        base = [{"id_richiesta": "t", "tipo": t, "data": d, "dati": {}} for t, d in
                [("creazione", "2026-11-09"), ("approvazione", "2026-11-10"), ("invio", "2026-11-12"), ("consegna", "2026-11-12")]]
        for c in CASI:
            r, _ = I.regole(c)
            if not r:
                continue
            ev, _ = I.evento_proposto(r, "t", "2026-11-20")
            if ev:
                s = stati.ricostruisci(base + [ev])
                self.assertIn(s["stato"], stati.STATI, c["id"])

    def test_revisione_al_100_per_cento_salvo_accolte_alte(self):
        for e in I.ESITI:
            obb, _ = I.revisione({"esito": e, "confidenza": "alta"})
            self.assertEqual(obb, e != "accolta", e)
        self.assertTrue(I.revisione({"esito": "accolta", "confidenza": "media"})[0])
        self.assertTrue(I.revisione({"esito": "accolta", "confidenza": "alta"}, disaccordo=True)[0])

    def test_campione_almeno_10_per_cento_e_deterministico(self):
        ids = [f"ac-0-{i}" for i in range(37)]
        s = I.campione(ids)
        self.assertEqual(len(s), 4)
        self.assertEqual(s, I.campione(list(reversed(ids))))
        self.assertEqual(len(I.campione(["a"])), 1)
        self.assertEqual(I.campione([]), set())

    def test_accoda_idempotente_e_mai_applicata(self):
        base = R / "lavoro/test-interpreta"  # mai /tmp (AGENTS.md § 4)
        base.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=base) as d:
            coda = Path(d) / "coda.jsonl"
            ris = I.interpreta(PER_ID["s01"], blob=False)
            p1 = I.accoda(PER_ID["s01"], ris, coda, data="2026-11-20")
            I.accoda(PER_ID["s01"], ris, coda, data="2026-11-20")
            righe = coda.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(righe), 1)
            self.assertEqual(p1["stato"], "da-rivedere")
            self.assertEqual(p1["revisione"], "da-campionare")
            self.assertIn("non applicato", p1["evento_proposto"]["note"])
            ps = I.assegna_campione([p1])
            self.assertEqual(ps[0]["revisione"], "campione-controllo")  # 1 su 1: ceil(10 %) = 1

    def test_accordo(self):
        a = I.accordo([("accolta", "accolta"), ("diniego", "diniego"), ("accolta", "parziale"), ("chiarimento", "chiarimento")])
        self.assertEqual(a["n"], 4)
        self.assertEqual(a["accordo"], 0.75)
        self.assertGreater(a["kappa"], 0.6)
        j = I.accordo([({"esito": "diniego", "motivi": ["a", "b"]}, {"esito": "diniego", "motivi": ["a"]})])
        self.assertEqual(j["jaccard_motivi"], 0.5)


class Registro(unittest.TestCase):
    def test_record_classificazione(self):
        ris = I.interpreta(PER_ID["s01"], blob=False)
        recs = I.record_classificazione(PER_ID["s01"], ris, quando="2026-11-09T00:00:00+00:00")
        self.assertEqual([r["cig"] for r in recs], ["Z1A2B3C4D5", "9A8B7C6D5E"])
        ac = recs[0]["esito"]["accesso_civico"]
        self.assertEqual((ac["esito"], ac["esito_voce"], ac["prompt_versione"]), ("accolta", "fornita", "v1"))
        self.assertEqual(len(ac["input_sha256"]), 64)
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema non installato")
        schema = json.loads((R / "schemi/classificazione.schema.json").read_text(encoding="utf-8"))
        for r in recs:
            jsonschema.validate(r, schema)


if __name__ == "__main__":
    unittest.main()
