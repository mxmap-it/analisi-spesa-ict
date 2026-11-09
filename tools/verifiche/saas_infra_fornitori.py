"""#43 estensione del pilota DNS/AS (saas_infra_pilota.py) ai fornitori SaaS S2 della Misura 1.2.

Per ogni dominio di config/saas_host.yaml: fino a 5 host per ente presi dall'archivio (archivio/mirror), CNAME (per
riconoscere i CDN), record A, AS di origine (Team Cymru), whois .it dell'intestatario. Riusa dig/asn/whois_it del pilota.
Attendibilità B per «dove risponde il servizio pubblico», NON per dove stanno i dati (back-office, DB, backup).
Un CDN (Cloudflare, Akamai, Fastly) è marcato: nasconde l'origine.
Uso: nice .venv/bin/python tools/verifiche/saas_infra_fornitori.py --data 2026-11-09
   -> esiti/<data>/infrastruttura-sottostante/saas-infra-dns.json"""
import collections, json, os, re, sys, time
from pathlib import Path
import yaml
R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import saas_infra_pilota as P  # noqa: E402

AS_IT = {208761: "Maggioli (rete propria, IT)", 200760: "Dinova (IT)", 12637: "Seeweb (IT)", 31034: "Aruba (IT)",
         205985: "Halley (rete propria, IT)", 3302: "Retelit (IT)", 20746: "TIM (IT)", 12874: "Fastweb (IT, controllo CH)",
         44920: "Si.TEK (IT)", 24940: "Hetzner (DE, UE)", 51167: "Contabo (DE, UE)", 16276: "OVH (FR, UE)"}


def classe(a):
    if a in P.AS_CLASSE: return P.AS_CLASSE[a]
    return AS_IT.get(a, "altro (da verificare)")


def main():
    data = sys.argv[sys.argv.index("--data") + 1]
    conf = yaml.safe_load(open(R / "config/saas_host.yaml", encoding="utf-8"))
    hosts = sorted({h.split(":")[0] for h in os.listdir(R / "archivio/mirror") if not h.endswith((".link", "__allegati"))})
    out = []
    for c in conf:
        d = c["dominio"]; hs = [h for h in hosts if h == d or h.endswith("." + d)][:5] or [d, "www." + d]
        prove = []
        for h in hs:
            cname = P.dig(h, "CNAME")
            ips = [x for x in P.dig(h) if re.match(r"^\d+\.\d+\.\d+\.\d+$", x)]
            if not ips: continue
            a, n = P.asn(ips[0])
            prove.append({"host": h, "cname": cname, "ip": ips[0], "as": a, "as_nome": n, "classe": classe(a),
                          "cdn": bool(re.search(r"CDN", classe(a)))})
            time.sleep(0.5)
        cl = collections.Counter(p["classe"] for p in prove)
        out.append({**c, "intestatario_whois": P.whois_it(d) if d.endswith(".it") else None, "host_provati": len(prove),
                    "classi": dict(cl), "prove": prove})
        print(d, c["fornitore"], dict(cl), out[-1]["intestatario_whois"]); time.sleep(1)
    o = R / f"esiti/{data}/infrastruttura-sottostante"; o.mkdir(parents=True, exist_ok=True)
    json.dump({"data": data, "metodo": __doc__, "domini": out}, open(o / "saas-infra-dns.json", "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
