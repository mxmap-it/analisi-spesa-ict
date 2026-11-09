"""#43 pilota: su quale infrastruttura girano i SaaS dei fornitori PA (strato sotto S2/S3 della Misura 1.2).

Metodo (ripetibile, poche richieste, nessun aggiramento):
1. domini di secondo livello delle piattaforme SaaS già nell'archivio (archivio/mirror/<host>), con almeno MIN_HOST host
   (= una piattaforma multi-ente: ogni ente ha il suo sottodominio sul SaaS del fornitore);
2. per ogni dominio, fino a 3 host: record A (dig) e AS di origine dell'IP (DNS TXT origin.asn.cymru.com, Team Cymru);
3. intestatario del dominio .it dal whois del Registro .it (whois.nic.it, porta 43, una richiesta per dominio);
4. classe dell'AS: hyperscaler extra-UE (Amazon, Microsoft, Google, Oracle, Cloudflare, Akamai, Fastly = CDN), altro.
Limite: si vede dove risponde il servizio pubblico (front-end o CDN), non dove stanno i dati; un CDN nasconde l'origine.
Uso: python tools/verifiche/saas_infra_pilota.py [--data AAAA-MM-GG] -> esiti/<data>/pnrr12/saas-infra-pilota.json"""
import collections, datetime, json, os, re, socket, subprocess, sys, time
from pathlib import Path

R = Path(__file__).resolve().parents[2]
MIN_HOST = 15
AS_CLASSE = {16509: "Amazon (EXTRA-UE)", 14618: "Amazon (EXTRA-UE)", 8075: "Microsoft (EXTRA-UE)", 8068: "Microsoft (EXTRA-UE)",
             15169: "Google (EXTRA-UE)", 396982: "Google (EXTRA-UE)", 31898: "Oracle (EXTRA-UE)", 13335: "Cloudflare CDN (EXTRA-UE)",
             20940: "Akamai CDN (EXTRA-UE)", 16625: "Akamai CDN (EXTRA-UE)", 54113: "Fastly CDN (EXTRA-UE)"}


def dig(name, typ="A"):
    try:
        return [x.strip().strip('"') for x in subprocess.run(["dig", "+short", typ, name], capture_output=True, text=True, timeout=15).stdout.split("\n") if x.strip()]
    except Exception: return []


def asn(ip):
    t = dig(".".join(reversed(ip.split("."))) + ".origin.asn.cymru.com", "TXT")
    if not t: return None, None
    a = t[0].split("|")[0].strip().split()[0]
    nome = dig(f"AS{a}.asn.cymru.com", "TXT")
    return int(a), (nome[0].split("|")[-1].strip() if nome else "")


def whois_it(dom):
    try:
        s = socket.create_connection(("whois.nic.it", 43), timeout=15); s.sendall((dom + "\r\n").encode())
        b = b""
        while (c := s.recv(4096)): b += c
        s.close(); t = b.decode("utf-8", "replace")
        m = re.search(r"Registrant\s*\n\s*Organization:\s*(.+)", t)
        return m.group(1).strip() if m else ("(nessun intestatario pubblico)" if "Status" in t else None)
    except Exception as e: return f"errore: {e.__class__.__name__}"


def main():
    data = sys.argv[sys.argv.index("--data") + 1] if "--data" in sys.argv else datetime.date.today().isoformat()
    host = collections.defaultdict(list)
    for h in os.listdir(R / "archivio/mirror"):
        h = h.split(":")[0]
        if h.endswith(".link") or not re.match(r"^[a-z0-9.-]+\.[a-z]+$", h): continue
        p = h.split(".")
        if len(p) >= 3 and p[-1] in ("it", "com", "net", "cloud", "eu"): host[".".join(p[-2:])].append(h)
    domini = {d: sorted(set(hs)) for d, hs in host.items() if len(set(hs)) >= MIN_HOST and not re.search(r"(gov|edu|comune|provincia|regione)\.", d)
              and d.split(".")[0] not in ("gov", "edu") and len(d.split(".")[0]) > 2}
    out = []
    for d, hs in sorted(domini.items(), key=lambda x: -len(x[1])):
        prove = []
        for h in hs[:3]:
            for ip in [x for x in dig(h) if re.match(r"^\d+\.\d+\.\d+\.\d+$", x)][:1]:
                a, n = asn(ip); prove.append({"host": h, "ip": ip, "as": a, "as_nome": n, "classe": AS_CLASSE.get(a, "altro (verificare: IT/UE?)")})
            time.sleep(0.5)
        out.append({"dominio": d, "host_in_archivio": len(hs), "intestatario_whois": whois_it(d) if d.endswith(".it") else None, "prove": prove})
        time.sleep(1)
    o = R / f"esiti/{data}/pnrr12"; os.makedirs(o, exist_ok=True)
    riep = collections.Counter(p["classe"] for x in out for p in x["prove"][:1])
    json.dump({"data": data, "metodo": __doc__, "riepilogo_per_dominio": dict(riep), "domini": out}, open(o / "saas-infra-pilota.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    for x in out: print(x["dominio"], x["host_in_archivio"], x["intestatario_whois"], [(p["as"], p["as_nome"][:30]) for p in x["prove"]])
    print(riep)


if __name__ == "__main__":
    main()
