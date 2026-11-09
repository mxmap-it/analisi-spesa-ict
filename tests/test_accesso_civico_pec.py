"""Test dell'adattatore PEC (#58), SOLO in modalità secca: nessuna connessione, messaggi .eml costruiti a mano in
tests/dati/pec/ (ricevute secondo le regole tecniche DM 2/11/2005 allegate al DPR 68/2005).
Eseguire: .venv/bin/python -m unittest tests/test_accesso_civico_pec.py"""
import email
import os
import email.policy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / "tools/accesso_civico"))
import pec  # noqa: E402
import stati  # noqa: E402

EML = R / "tests/dati/pec"
RID1, RID2 = "ac-prova-12345678901-1", "ac-prova-98765432109-1"
MID1 = "<ac-prova-12345678901-1.20261112101500@pec.richiedente.invalid>"
MID2 = "<ac-prova-98765432109-1.20261112101700@pec.richiedente.invalid>"


def base():  # cartella di lavoro sotto lavoro/ (mai /tmp)
    (R / "lavoro").mkdir(exist_ok=True)
    return tempfile.TemporaryDirectory(dir=R / "lavoro", prefix="test-pec-")


def scrivi(registro, eventi):
    for e in eventi:
        stati.aggiungi(registro, dict({"chi": "test"}, **e))


def inviata(rid, mid):
    return [{"id_richiesta": rid, "tipo": "creazione", "data": "2026-11-01"},
            {"id_richiesta": rid, "tipo": "approvazione", "data": "2026-11-02"},
            {"id_richiesta": rid, "tipo": "invio", "data": "2026-11-12", "documento": {"message_id": mid}}]


class FintoSMTP:
    def __init__(self):
        self.inviati = []

    def send_message(self, m):
        self.inviati.append(m)


class Riconoscimento(unittest.TestCase):
    def leggi(self, nome):
        return email.message_from_bytes((EML / nome).read_bytes(), policy=email.policy.default)

    def test_ricevute(self):
        for nome, tipo in (("01-accettazione.eml", "accettazione"), ("02-avvenuta-consegna.eml", "avvenuta-consegna"),
                           ("04-errore-consegna.eml", "errore-consegna")):
            classe, d = pec.classifica(self.leggi(nome))
            self.assertEqual((classe, d["tipo"], d["coerente"]), ("ricevuta", tipo, True), nome)
        _, d = pec.classifica(self.leggi("02-avvenuta-consegna.eml"))
        self.assertEqual(d["riferimento"], MID1)
        self.assertEqual((d["daticert"]["giorno"], d["daticert"]["msgid"]), ("12/11/2026", MID1))
        _, d = pec.classifica(self.leggi("04-errore-consegna.eml"))
        self.assertEqual(d["daticert"]["errore"], "no-dest")

    def test_incoerente(self):
        _, d = pec.classifica(self.leggi("05-daticert-incoerente.eml"))
        self.assertFalse(d["coerente"])

    def test_busta_e_ordinario(self):
        classe, d = pec.classifica(self.leggi("03-busta-risposta-ente.eml"))
        self.assertEqual((classe, d["tipo"]), ("busta", "posta-certificata"))
        self.assertEqual(d["interno"]["In-Reply-To"], MID1)
        self.assertEqual(pec.classifica(self.leggi("07-ordinario-estraneo.eml"))[0], "messaggio")


class Lettura(unittest.TestCase):
    def test_cartella_completa(self):
        with base() as t:
            t = Path(t)
            reg = t / "eventi.jsonl"
            scrivi(reg, inviata(RID1, MID1) + inviata(RID2, MID2))
            arch = pec.Archivio(t / "pec")
            righe = {r["percorso"].split("/")[-1]: r for r in pec.leggi_cartella(EML, reg, arch)}
            self.assertEqual(len(righe), 7)
            per = stati.leggi(reg)
            s1, s2 = stati.ricostruisci(per[RID1]), stati.ricostruisci(per[RID2])
            self.assertEqual((s1["stato"], str(s1["presentazione"]), str(s1["scadenza"])),
                             ("consegnata", "2026-11-12", "2026-12-12"))
            self.assertEqual(s2["stato"], "approvata")                  # mancata consegna -> si può ritentare
            g = [json.loads(x) for x in (t / "pec/giornale.jsonl").read_text(encoding="utf-8").splitlines()]
            per_tipo = {(r["tipo"], r.get("id_richiesta")): r for r in g}
            self.assertEqual(per_tipo[("accettazione", RID1)]["esito"], "solo giornale")
            self.assertTrue(per_tipo[("avvenuta-consegna", RID1)]["esito"].startswith("evento consegna del 2026-11-12"))
            self.assertTrue(per_tipo[("errore-consegna", RID2)]["esito"].startswith("evento mancata-consegna"))
            risp = [r for r in g if r["classe"] == "busta"]
            self.assertEqual({(r["id_richiesta"], r["abbinamento"]) for r in risp},
                             {(RID1, "message-id (In-Reply-To)"), (RID2, "codice nell'oggetto/testo")})
            self.assertTrue(all(r["esito"].startswith("da-esaminare") for r in risp))
            self.assertTrue(any(r.get("esito", "").startswith("anomalia") for r in g))
            estr = [r for r in g if r["classe"] == "messaggio"][0]
            self.assertEqual((estr["id_richiesta"], estr["esito"]), (None, "da-esaminare: non abbinato"))
            # ogni messaggio archiviato con il suo sha256
            for r in g:
                self.assertEqual(pec.sha((R / r["percorso"]).read_bytes()), r["sha256"])
            # idempotenza: una seconda lettura non aggiunge eventi
            n = sum(len(v) for v in stati.leggi(reg).values())
            seconda = pec.leggi_cartella(EML, reg, arch)
            self.assertTrue(all(r["esito"] == "già elaborato" for r in seconda))
            self.assertEqual(sum(len(v) for v in stati.leggi(reg).values()), n)

    def test_consegna_senza_invio_non_registra(self):
        with base() as t:
            t = Path(t)
            reg = t / "eventi.jsonl"
            scrivi(reg, inviata(RID1, MID1)[:2])                        # approvata, mai inviata
            arch = pec.Archivio(t / "pec")
            r = pec.elabora((EML / "02-avvenuta-consegna.eml").read_bytes(), reg, arch)
            self.assertIn("nessun evento", r["esito"])                 # abbinata per codice, ma mai inviata
            self.assertEqual(stati.ricostruisci(stati.leggi(reg)[RID1])["stato"], "approvata")


class Invio(unittest.TestCase):
    def prepara(self, t, n):
        ids = []
        for i in range(n):
            rid = f"ac-prova-0000000000{i}-1"
            md = (f"**Da:** Richiedente — richiedente@pec.richiedente.invalid\n**A:** Ente {i} — p{i}@pec.ente.invalid\n"
                  f"**Oggetto:** Istanza di accesso civico generalizzato — rif. {rid}\n\nSpett.le Ente {i},\ntesto.\n")
            (t / f"{rid}.md").write_text(md, encoding="utf-8")
            (t / f"{rid}.json").write_text(json.dumps({"id": rid, "destinatario": {"pec": f"p{i}@pec.ente.invalid"}}),
                                           encoding="utf-8")
            (t / f"{rid}.pdf.p7m").write_bytes(b"%PDF-1.4 finto firmato " + rid.encode())
            scrivi(t / "eventi.jsonl", inviata(rid, None)[:2])
            ids.append(rid)
        return ids

    def test_tetto_ritmo_ed_eventi(self):
        with base() as t:
            t = Path(t)
            ids = self.prepara(t, 4)
            (t / f"{ids[3]}.pdf.p7m").unlink()                         # senza allegato firmato: saltata
            smtp, pause = FintoSMTP(), []
            esito = dict(pec.invia(t, t / "eventi.jsonl", pec.Archivio(t / "pec"), "richiedente@pec.richiedente.invalid",
                                   smtp=smtp, tetto_giorno=2, intervallo=90, oggi="2026-11-12", dormi=pause.append))
            self.assertEqual([esito[i] for i in ids], ["inviata", "inviata", "rinviata: tetto giornaliero raggiunto",
                                                       "rinviata: tetto giornaliero raggiunto"])
            self.assertEqual(pause, [90])                              # una pausa fra due invii
            m = smtp.inviati[0]
            self.assertIn(ids[0], m["Subject"])
            self.assertIn(ids[0], m["Message-ID"])
            self.assertEqual(m["To"], "p0@pec.ente.invalid")
            self.assertEqual([p.get_filename() for p in m.iter_attachments()], [f"{ids[0]}.pdf.p7m"])
            per = stati.leggi(t / "eventi.jsonl")
            ev = per[ids[0]][-1]
            self.assertEqual((ev["tipo"], ev["documento"]["message_id"]), ("invio", m["Message-ID"]))
            self.assertEqual(stati.ricostruisci(per[ids[0]])["stato"], "inviata")
            blob = R / ev["documento"]["percorso"]
            self.assertEqual(pec.sha(blob.read_bytes()), ev["documento"]["sha256"])
            # il giorno dopo il tetto riparte; la richiesta senza allegato resta ferma
            esito = dict(pec.invia(t, t / "eventi.jsonl", pec.Archivio(t / "pec"), "r@pec.invalid", smtp=smtp,
                                   tetto_giorno=2, oggi="2026-11-13", dormi=pause.append))
            self.assertEqual(esito, {ids[2]: "inviata", ids[3]: "saltata: manca l'allegato firmato (<id>.pdf.p7m o <id>.pdf)"})

    def test_secca_e_reale_negato(self):
        with base() as t:
            t = Path(t)
            ids = self.prepara(t, 1)
            vero = (t / "eventi.jsonl").read_bytes()
            pec.main(["invia", str(t), "--archivio", str(t / "pec")])
            self.assertEqual((t / "eventi.jsonl").read_bytes(), vero)  # il registro vero non si tocca
            sec = stati.leggi(t / "eventi-secca.jsonl")[ids[0]]
            self.assertEqual((sec[-1]["tipo"], sec[-1]["note"]), ("invio", "SECCA: nessun invio"))
            os.environ.pop("PEC_REALE", None)
            self.assertFalse(pec.reale_ammesso(True))
            with self.assertRaises(SystemExit):
                pec.main(["invia", str(t), "--reale", "--archivio", str(t / "pec")])

    def test_oggetto_senza_codice(self):
        with base() as t:
            p = Path(t) / "a.pdf"
            p.write_bytes(b"%PDF")
            with self.assertRaises(pec.ErrorePec):
                pec.componi("ac-x-1", "**Oggetto:** senza codice\n\ntesto", p, "a@b.invalid", "c@d.invalid")


if __name__ == "__main__":
    unittest.main()
