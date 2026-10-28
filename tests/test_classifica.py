"""Test del classificatore sui casi di riferimento (tests/casi_classifica.yaml).
Uso: python tests/test_classifica.py   (oppure pytest)"""
import sys
from pathlib import Path
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools/analisi"))
from classifica import Classificatore  # noqa: E402

CASI = yaml.safe_load(open(Path(__file__).with_name("casi_classifica.yaml"), encoding="utf-8"))
C = Classificatore()


def esito(caso):
    e = C.classifica(caso["testo"], caso.get("cig_accordo_quadro", ""), caso.get("aggiudicatari", []), caso.get("cpv", "")) or {"provider": "", "via": "fuori-ict"}
    errori = [f"{k}: atteso {caso[k]!r}, ottenuto {e.get(k)!r}" for k in ("provider", "servizio", "giurisdizione", "canale", "via") if k in caso and e.get(k) != caso[k]]
    return e, errori


def test_casi():
    falliti = [(c["fonte"], err) for c in CASI if (err := esito(c)[1])]
    assert not falliti, falliti


if __name__ == "__main__":
    n = 0
    for c in CASI:
        e, err = esito(c)
        if err:
            n += 1
            print(f"FALLITO {c['fonte']}: {'; '.join(err)}  [regola {e.get('regola')!r}]")
    print(f"{len(CASI) - n}/{len(CASI)} casi superati")
    sys.exit(1 if n else 0)
