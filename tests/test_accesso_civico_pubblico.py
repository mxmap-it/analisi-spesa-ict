"""Test di campagna, redazione e generatore pubblico dell'accesso civico (#58).
Eseguire: .venv/bin/python -m unittest tests/test_accesso_civico_pubblico.py"""
import csv
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / "tools/accesso_civico"))
import campagna as cmp  # noqa: E402
import pubblica  # noqa: E402
import redazione as red  # noqa: E402
import stati  # noqa: E402

OGGI = "2026-11-09"
RICH = {"nome": "Richiedente Di Prova", "pec": "rich.prova@pec.esempio.invalid", "firma": "FIRMA-XYZ",
        "codice_fiscale": "RSSMRA80A01H501U"}


class Campagna(unittest.TestCase):
    def setUp(self):
        self.c = cmp.carica("cmp-spesa-ict-2026")

    def test_carica_e_stato_proposta(self):
        self.assertEqual(self.c["formato"], cmp.FORMATO)
        self.assertEqual(self.c["stato"], "proposta")
        self.assertIsNone(self.c["approvata"])

    def test_sha_modelli_allineati(self):
        self.assertEqual(cmp.verifica_modelli(self.c), [])

    def test_sha_modello_cambiato(self):
        c = json.loads(json.dumps(self.c))
        c["modelli"]["istanza"]["sha256"] = "f" * 64
        self.assertEqual(len(cmp.verifica_modelli(c)), 1)

    def test_campi_obbligatori(self):
        c = dict(self.c)
        del c["scopo"]
        with self.assertRaises(cmp.ErroreCampagna):
            cmp.valida(c)

    def test_stato_senza_decisione_respinto(self):
        with self.assertRaises(cmp.ErroreCampagna):
            cmp.valida(dict(self.c, stato="attiva"))
        with self.assertRaises(cmp.ErroreCampagna):
            cmp.cambia_stato(self.c, "approvata")
        with self.assertRaises(cmp.ErroreCampagna):
            cmp.cambia_stato(self.c, "attiva", "DECISIONI.md x")
        c = cmp.cambia_stato(self.c, "approvata", "DECISIONI.md 2026-11-xx")
        self.assertEqual(c["stato"], "approvata")
        with self.assertRaises(cmp.ErroreCampagna):
            cmp.aggiorna_sha_modelli(c)

    def test_parametri_sovrapposti(self):
        p = cmp.parametri(dict(self.c, parametri={"tetto_voci": 7, "tetto_pec_giorno": 3}),
                          {"tetto_voci_per_richiesta": 20, "pec": {"tetto_giorno": 20, "intervallo_secondi": 120}})
        self.assertEqual(p["tetto_voci_per_richiesta"], 7)
        self.assertEqual(p["pec"], {"tetto_giorno": 3, "intervallo_secondi": 120})
        self.assertEqual(p["campagna"], "cmp-spesa-ict-2026")

    def test_schema_campagna_coerente(self):
        s = json.loads((R / "schemi/accesso-civico-campagna.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(s["$id"], cmp.FORMATO)
        self.assertEqual(sorted(s["required"]), sorted(cmp.OBBLIGATORI))
        self.assertEqual(s["properties"]["stato"]["enum"], cmp.STATI)

    def test_schemi_richiesta_evento_campo_campagna(self):
        for n in ("richiesta", "evento"):
            s = json.loads((R / f"schemi/accesso-civico-{n}.schema.json").read_text(encoding="utf-8"))
            self.assertIn("campagna", s["properties"])
            self.assertNotIn("campagna", s["required"])  # retrocompatibile
        e = json.loads((R / "schemi/accesso-civico-evento.schema.json").read_text(encoding="utf-8"))
        for k in ("blob_sha256", "pubblico", "motivo_non_pubblico"):
            self.assertIn(k, e["properties"])


class Redazione(unittest.TestCase):
    def test_dati_personali_rimossi(self):
        t = ("Referente Mario Bianchi, CF BNCMRA75C12H501Z, tel. 06 1234 5678, cell. +39 333 1234567, "
             "mail mario.bianchi@gmail.com, IBAN IT60 X054 2811 1010 0000 0123 456. Scrivere a protocollo@pec.ente.it.")
        out, n = red.redigi_testo(t, ["protocollo@pec.ente.it"])
        self.assertEqual(red.residui(out, ["protocollo@pec.ente.it"]), [])
        for x in ("BNCMRA75C12H501Z", "1234 5678", "333 1234567", "gmail", "IT60"):
            self.assertNotIn(x, out)
        self.assertIn("protocollo@pec.ente.it", out)
        self.assertEqual(n, {"cf": 1, "iban": 1, "email": 1, "telefono": 2})

    def test_non_tocca_cig_importi_cf_ente_date(self):
        t = "CIG 9A1B2C3D4E, ente CF 80012345678, CF 00317740371, P.IVA 06363391001, AIC 049123456, euro,324571809,1, importo 3.456.789 €, del 2026-11-09, 345.678 euro, n. 12/2024"
        out, n = red.redigi_testo(t)
        self.assertEqual(out, t)
        self.assertEqual(n, {})

    def test_iban_non_valido_resta(self):
        self.assertEqual(red.redigi_testo("IT00X0000000000000000000000")[1], {})

    def test_richiedente(self):
        t = f"Da {RICH['nome']} — {RICH['pec']}, C.F. {RICH['codice_fiscale']}\nAllegato: documento d'identità\n{RICH['firma']}"
        out, _ = red.redigi_istanza(t, {"destinatario": {"pec": "x@pec.ente.it"}}, RICH)
        self.assertEqual(red.residui(out, [], RICH), [])
        self.assertIn(RICH["nome"], out)  # in pubblico solo il nome
        self.assertIn(red.SEGNAPOSTO["firma"], out)
        self.assertIn(red.SEGNAPOSTO["documento"], out)
        self.assertIn(red.SEGNAPOSTO["pec_richiedente"], out)

    def test_pec_richiedente_pubblica_per_decisione(self):
        out, _ = red.redigi_testo(f"scrivere a {RICH['pec']}", [], RICH, pec_pubblica=True)
        self.assertIn(RICH["pec"], out)
        self.assertEqual(red.residui(out, [], RICH, pec_pubblica=True), [])

    def test_residui_trova(self):
        r = red.residui("a mario@libero.it, RSSMRA80A01H501U, 3331234567", [])
        self.assertEqual(len(r), 3)

    def test_evento(self):
        ev = {"id_richiesta": "x", "tipo": "risposta", "data": OGGI, "chi": "Operatore Rossi",
              "documento": {"sha256": "a" * 64, "percorso": "registro-privato/x.eml"}, "note": "tel 06 12345678"}
        p = red.redigi_evento(ev)
        self.assertNotIn("percorso", p["documento"])
        self.assertNotIn("Rossi", p["chi"])
        self.assertNotIn("12345678", p["note"])
        self.assertIn("percorso", ev["documento"])  # l'originale non si tocca
        self.assertIsNone(red.redigi_evento(dict(ev, pubblico=False)))
        c = red.redigi_evento({"tipo": "comunicazione-controinteressati", "data": OGGI, "note": "Luigi Verdi",
                               "documento": {"sha256": "b" * 64, "message_id": "m"}})
        self.assertNotIn("note", c)
        self.assertEqual(c["documento"], {"sha256": "b" * 64})

    def test_richiesta(self):
        r = {"id": "ac-x", "destinatario": {"pec": "p@pec.ente.it"}, "richiedente": RICH, "testo": "x",
             "voci": [{"id": "v", "oggetto": "servizio, referente a.b@gmail.com", "documento_atteso": "contratto"}]}
        p = red.redigi_richiesta(r)
        self.assertNotIn("richiedente", p)
        self.assertNotIn("testo", p)
        self.assertNotIn("gmail", p["voci"][0]["oggetto"])


class Pubblico(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(dir=R / "lavoro" if (R / "lavoro").exists() else None)
        cls.out = Path(cls.tmp.name) / "anteprima"
        camp, rich, ev, testi, richiedente = pubblica.sintetici(OGGI)
        cls.camp, cls.rich, cls.ev = camp, rich, ev
        cls.ris = pubblica.genera([cmp.carica("cmp-spesa-ict-2026")] + camp, rich, ev, OGGI, cls.out, testi,
                                  richiedente, sintetico=True)
        cls.static = cls.out / "sito/static/accesso-civico"
        cls.content = cls.out / "sito/content/accesso-civico"

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_sintetici_validi_per_la_macchina_a_stati(self):
        per = {}
        for e in self.ev:
            per.setdefault(e["id_richiesta"], []).append(e)
        for evs in per.values():
            stati.ricostruisci(evs)

    def test_pagine(self):
        self.assertTrue((self.content / "_index.md").exists())
        self.assertTrue((self.content / "campagne/cmp-prova-sintetica.md").exists())
        self.assertTrue((self.content / "campagne/cmp-spesa-ict-2026.md").exists())
        self.assertEqual(len(list((self.content / "richieste").glob("ac-*.md"))), 12)
        self.assertEqual(len(list((self.content / "enti").glob("9*.md"))), 12)
        self.assertIn("DATI SINTETICI", (self.content / "_index.md").read_text(encoding="utf-8"))

    def test_nessun_residuo_in_tutto_l_output(self):
        for p in self.out.rglob("*"):
            if p.is_file():
                t = p.read_text(encoding="utf-8")
                self.assertEqual(red.residui(t, [r["destinatario"]["pec"] for r in self.rich]), [], p)
                for x in ("FIRMA-PROVA-XYZ", "RSSMRA80A01H501U", "richiedente.prova@", "registro-privato", "Rossi",
                          "Verdi", "gmail"):
                    self.assertNotIn(x, t, p)

    def test_dashboard(self):
        d = json.loads((self.static / "dashboard.json").read_text(encoding="utf-8"))
        k = d["per_campagna"]["cmp-prova-sintetica"]
        self.assertEqual(k["richieste"], 12)
        self.assertEqual(k["inviate"], 10)
        self.assertEqual(k["consegnate"], 9)
        self.assertEqual(k["mancata_consegna"], 1)
        self.assertEqual(k["esiti_risposte"], {"accolta": 2, "diniego": 3, "parziale": 1})
        self.assertEqual(sum(k["dinieghi_per_motivo"].values()), 4)
        self.assertEqual(k["tempi_risposta_giorni"]["n"], 5)
        self.assertEqual(k["tempi_risposta_giorni"]["mediana"], 20)
        self.assertEqual(k["stati"].get("annullata"), 1)
        self.assertEqual(d["per_campagna"]["cmp-spesa-ict-2026"]["richieste"], 0)
        self.assertEqual(d["totale"]["richieste"], 12)

    def test_dataset_e_manifest(self):
        v = self.static / "dati/v" / OGGI
        m = json.loads((v / "manifest.json").read_text(encoding="utf-8"))
        nomi = {f["percorso"] for f in m["file"]}
        self.assertTrue({"richieste.csv", "eventi.jsonl", "enti-tempi.csv", "campagne.json", "dizionario.md",
                         "LICENZA.txt", "campagne/cmp-prova-sintetica/richieste.csv"} <= nomi)
        for f in m["file"]:
            self.assertEqual(hashlib.sha256((v / f["percorso"]).read_bytes()).hexdigest(), f["sha256"])
        self.assertIn("da decidere", m["licenza"])
        somme = (v / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(somme), len(m["file"]) + 1)
        righe = list(csv.DictReader(open(v / "richieste.csv", encoding="utf-8")))
        self.assertEqual(len(righe), 12)
        self.assertEqual((self.static / "dati/ultima/manifest.json").read_bytes(), (v / "manifest.json").read_bytes())
        for e in map(json.loads, (v / "eventi.jsonl").read_text(encoding="utf-8").splitlines()):
            self.assertNotIn("percorso", e.get("documento", {}))
            self.assertEqual(e["campagna"], "cmp-prova-sintetica")
        self.assertNotIn("richiedente_id", (v / "campagne.json").read_text(encoding="utf-8"))

    def test_residuo_blocca(self):
        rich = json.loads(json.dumps(self.rich[:1]))
        ev = [dict(e) for e in self.ev if e["id_richiesta"] == rich[0]["id"]]
        rich[0]["ente"]["nome"] = "Ente 333 1234567"  # telefono finito in un campo non redatto
        with self.assertRaises(SystemExit):
            pubblica.genera(self.camp, rich, ev, OGGI, Path(self.tmp.name) / "x")

    def test_uscita_vietata_in_docs(self):
        import subprocess
        p = subprocess.run([sys.executable, str(R / "tools/accesso_civico/pubblica.py"), "--sintetico", "--uscita",
                            str(R / "docs/accesso-civico")], capture_output=True, text=True)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("vietata", p.stderr)


if __name__ == "__main__":
    unittest.main()
