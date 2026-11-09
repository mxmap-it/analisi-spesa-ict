"""Test della macchina a stati e delle scadenze dell'accesso civico (#58). Eseguire: .venv/bin/python -m unittest tests/test_accesso_civico_stati.py"""
import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / "tools/accesso_civico"))
import stati  # noqa: E402

D = dt.date


def ev(tipo, data, **dati):
    return {"id_richiesta": "t", "tipo": tipo, "data": data, "dati": dati}


BASE = [ev("creazione", "2026-11-09"), ev("approvazione", "2026-11-10"), ev("invio", "2026-11-12"),
        ev("consegna", "2026-11-12")]


class Termini(unittest.TestCase):
    def test_pasqua(self):
        self.assertEqual(stati.pasqua(2026), D(2026, 4, 5))
        self.assertEqual(stati.pasqua(2027), D(2027, 3, 28))

    def test_festivi(self):
        self.assertTrue(stati.festivo(D(2026, 12, 8)))
        self.assertTrue(stati.festivo(D(2026, 4, 6)))       # lunedì dell'Angelo
        self.assertTrue(stati.festivo(D(2026, 11, 15)))      # domenica
        self.assertFalse(stati.festivo(D(2026, 11, 14)))     # sabato
        self.assertTrue(stati.festivo(D(2026, 11, 14), sabato=True))

    def test_trenta_giorni_esatto(self):
        self.assertEqual(stati.termine(D(2026, 11, 12), 30, proroga=False), D(2026, 12, 12))
        self.assertEqual(stati.termine(D(2026, 11, 12), 30), D(2026, 12, 12))
        self.assertEqual(stati.termine(D(2026, 11, 13), 30), D(2026, 12, 14))  # 13/12 domenica -> lunedì
        self.assertEqual(stati.termine(D(2026, 11, 25), 30), D(2026, 12, 28))  # 25/12 + slitta oltre 26 e 27 (domenica)


class FontiVerificate(unittest.TestCase):
    """Punti verificati su Normattiva/GU il 9/11/2026 (report/metodo/prove-normativa/)."""

    def test_quattro_ottobre_dal_2026(self):           # L. 151/2025, in vigore 1/1/2026
        self.assertFalse(stati.festivo(D(2025, 10, 4)))  # sabato 2025, legge non ancora in vigore
        self.assertTrue(stati.festivo(D(2027, 10, 4)))  # lunedì
        self.assertEqual(stati.termine(D(2027, 9, 4), 30), D(2027, 10, 5))
        self.assertEqual(stati.termine(D(2025, 9, 3), 30), D(2025, 10, 3))

    def test_due_giugno_e_ognissanti(self):           # L. 260/1949 artt. 1-2
        self.assertTrue(stati.festivo(D(2027, 6, 2)))
        self.assertTrue(stati.festivo(D(2027, 11, 1)))
        self.assertFalse(stati.festivo(D(2027, 11, 4)))  # soppresso dal 1977

    def test_ricorso_tar_116_cpa(self):               # 30 gg, sabato prorogato (art. 52 c. 5 c.p.a.)
        self.assertEqual(stati.TERMINI["ricorso_tar"], 30)
        self.assertEqual(stati.termine_tar(D(2026, 11, 2)), D(2026, 12, 2))
        self.assertEqual(stati.termine_tar(D(2026, 11, 12)), D(2026, 12, 14))  # 12/12 sabato -> lunedì 14
        s = stati.ricostruisci(BASE + [ev("risposta", "2026-12-01", esito="diniego"), ev("riesame", "2026-12-03"),
                                       ev("risposta", "2026-12-20", esito="diniego")])
        self.assertIn("TAR entro il 2027-01-19", stati.alla_data(s, "2026-12-21")["prossima_azione"])


class Macchina(unittest.TestCase):
    def test_flusso_base_e_scadenza(self):
        s = stati.ricostruisci(BASE)
        self.assertEqual(s["stato"], "consegnata")
        self.assertEqual(s["scadenza"], D(2026, 12, 12))
        self.assertEqual(stati.alla_data(s, "2026-12-12")["stato"], "consegnata")
        r = stati.alla_data(s, "2026-12-13")
        self.assertEqual(r["stato"], "silenzio")
        self.assertEqual(r["prossima_azione"], "sollecito")

    def test_sospensione_controinteressati(self):
        s = stati.ricostruisci(BASE + [ev("comunicazione-controinteressati", "2026-11-20"),
                                       ev("fine-sospensione", "2026-12-01", opposizione=False)])
        self.assertEqual(s["sospensione_giorni"], 11)
        self.assertEqual(s["scadenza"], stati.termine(D(2026, 11, 12), 41))
        self.assertEqual(s["stato"], "consegnata")

    def test_sospesa_derivato_oltre_dieci(self):
        s = stati.ricostruisci(BASE + [ev("comunicazione-controinteressati", "2026-11-20")])
        self.assertIn("oltre i 10", stati.alla_data(s, "2026-12-05")["derivato"])

    def test_chiarimento_non_riavvia(self):
        s = stati.ricostruisci(BASE + [ev("richiesta-chiarimento", "2026-11-20"), ev("invio-chiarimento", "2026-11-22")])
        self.assertEqual(s["scadenza"], D(2026, 12, 12))

    def test_diniego_riesame_venti(self):
        s = stati.ricostruisci(BASE + [ev("risposta", "2026-12-01", esito="diniego")])
        self.assertEqual(s["termine_riesame"], D(2026, 12, 31))
        self.assertTrue(stati.alla_data(s, "2026-12-02")["prossima_azione"].startswith("riesame-diniego"))
        s = stati.ricostruisci(BASE + [ev("risposta", "2026-12-01", esito="diniego"), ev("riesame", "2026-12-03")])
        self.assertEqual((s["stato"], s["fase"], s["scadenza"]), ("riesame", "riesame", D(2026, 12, 23)))
        self.assertEqual(stati.alla_data(s, "2026-12-24")["stato"], "silenzio")

    def test_garante_proroga_riesame(self):
        s = stati.ricostruisci(BASE + [ev("risposta", "2026-12-01", esito="parziale"), ev("riesame", "2026-12-03"),
                                       ev("richiesta-garante", "2026-12-05")])
        self.assertEqual(s["scadenza"], D(2027, 1, 2))

    def test_silenzio_registrato_e_riesame(self):
        s = stati.ricostruisci(BASE + [ev("sollecito", "2026-12-14"), ev("silenzio", "2026-12-14"),
                                       ev("riesame", "2026-12-20")])
        self.assertEqual(s["solleciti"], 1)
        self.assertEqual(s["scadenza"], D(2027, 1, 9))  # 20/12 + 20 = 9/1, sabato non festivo per default

    def test_silenzio_prematuro_rifiutato(self):
        with self.assertRaises(stati.ErroreTransizione):
            stati.ricostruisci(BASE + [ev("silenzio", "2026-12-10")])

    def test_difensore_illegittimo_poi_accesso_consentito(self):
        evs = BASE + [ev("risposta", "2026-12-01", esito="diniego"), ev("difensore", "2026-12-10"),
                      ev("pronuncia-difensore", "2027-01-05", esito="illegittimo")]
        s = stati.ricostruisci(evs)
        self.assertEqual(s["stato"], "difensore-conferma")
        self.assertEqual(s["scadenza"], D(2027, 2, 4))
        self.assertEqual(stati.alla_data(s, "2027-02-05")["stato"], "accolta")
        s2 = stati.ricostruisci(evs + [ev("conferma-diniego", "2027-01-20")])
        self.assertEqual(s2["stato"], "diniego")

    def test_difensore_trenta(self):
        s = stati.ricostruisci(BASE + [ev("risposta", "2026-12-01", esito="diniego"), ev("difensore", "2026-12-10")])
        self.assertEqual(s["scadenza"], D(2027, 1, 9))

    def test_transizioni_vietate(self):
        for extra in ([ev("riesame", "2026-11-20")],                                   # riesame senza esito
                      [ev("risposta", "2026-11-20", esito="boh")],                      # esito non valido
                      [ev("risposta", "2026-11-20", esito="diniego"), ev("riesame", "2026-11-21"),
                       ev("risposta", "2026-11-25", esito="diniego"), ev("riesame", "2026-11-26")],  # doppio riesame
                      [ev("consegna", "2026-11-13")]):                                  # consegna due volte
            with self.assertRaises(stati.ErroreTransizione):
                stati.ricostruisci(BASE + extra)
        with self.assertRaises(stati.ErroreTransizione):
            stati.ricostruisci([ev("creazione", "2026-11-09"), ev("invio", "2026-11-10")])  # invio senza approvazione
        with self.assertRaises(stati.ErroreTransizione):
            stati.ricostruisci(BASE + [ev("sollecito", "2026-11-01")])                 # data all'indietro

    def test_registro_append_only(self):
        with tempfile.TemporaryDirectory(dir=R / "lavoro") as d:
            p = Path(d) / "eventi.jsonl"
            for e in BASE:
                stati.aggiungi(p, e)
            with self.assertRaises(stati.ErroreTransizione):
                stati.aggiungi(p, ev("approvazione", "2026-11-13"))
            righe = [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(righe), 4)
            self.assertTrue(all(x["formato"] == stati.FORMATO for x in righe))


class Modelli(unittest.TestCase):
    def test_tutti_i_modelli_si_rendono(self):
        import re
        import bozze
        for f in sorted(bozze.MODELLI.glob("*.md")):
            testo = f.read_text(encoding="utf-8")
            self.assertIn("norme citate", testo)
            var = set(re.findall(r"\{\{\s*(\w+)\s*\}\}", testo))
            out = bozze.rendi(f.stem, {k: "X" for k in var})
            self.assertNotIn("{{", out)
            self.assertNotIn("{#", out)
            with self.assertRaises(KeyError):
                bozze.rendi(f.stem, {})


if __name__ == "__main__":
    unittest.main()
