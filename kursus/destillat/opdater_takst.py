#!/usr/bin/env python3
"""Destillat af modul 10 (modul 14): opdaterer takster for en zone uden en model.

Samme opgave som skillen /takstopdatering, skrevet ned til det mindst mulige:
1. Taler med takstserveren over stdio (samme MCP-protokol, ingen agent imellem).
2. Skriver zonens takster ind i data/takster.json for praecis de transportformer, serveren tilbyder.
3. Koerer testene og rapporterer.

Brug: python3 kursus/destillat/opdater_takst.py 5
Ingen afhaengigheder. Ingen modelkald. Deterministisk.
"""
import json
import os
import subprocess
import sys

ROD = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERVER = os.path.join(ROD, "kursus", "mcp", "takstserver.py")
TAKSTER = os.path.join(ROD, "data", "takster.json")
TRANSPORTFORMER = ("fly", "vej", "soe")


def mcp_kald(beskeder):
    """Sender JSON-RPC-beskeder til takstserveren og returnerer svarene per id."""
    linjer = "\n".join(json.dumps(b, ensure_ascii=False) for b in beskeder) + "\n"
    p = subprocess.run([sys.executable, SERVER], input=linjer, capture_output=True, text=True, check=True)
    svar = {}
    for l in p.stdout.splitlines():
        if l.strip():
            o = json.loads(l)
            if "id" in o:
                svar[o["id"]] = o
    return svar


def hent_takster(zone):
    beskeder = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "opdater_takst", "version": "1.0"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
    ]
    for i, tf in enumerate(TRANSPORTFORMER, start=10):
        beskeder.append({"jsonrpc": "2.0", "id": i, "method": "tools/call", "params": {"name": "hent_takst", "arguments": {"zone": zone, "transportform": tf}}})
    svar = mcp_kald(beskeder)
    fundet = {}
    for i, tf in enumerate(TRANSPORTFORMER, start=10):
        r = svar.get(i, {}).get("result", {})
        if r and not r.get("isError"):
            tekst = r["content"][0]["text"]            # fx "zone 5 (Oversoeisk), fly: 128.00 DKK per kg"
            tal = tekst.split(":")[-1].split("DKK")[0].strip()
            fundet[tf] = float(tal)
    return fundet


def skriv(zone, takster):
    with open(TAKSTER, encoding="utf-8") as f:
        data = json.load(f)
    for tf, kr in takster.items():
        data["kr_per_kg"][tf][zone] = kr
    with open(TAKSTER, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main(argv):
    if len(argv) != 2 or not argv[1].isdigit():
        print("brug: opdater_takst.py <zone>", file=sys.stderr)
        return 2
    zone = argv[1]
    takster = hent_takster(zone)
    if not takster:
        print("zone %s findes ikke i takstsystemet" % zone, file=sys.stderr)
        return 1
    skriv(zone, takster)
    print("zone %s: %s" % (zone, ", ".join("%s %.2f" % (tf, kr) for tf, kr in takster.items())))
    t = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"], cwd=ROD, capture_output=True, text=True)
    print(t.stdout.strip().splitlines()[-1] if t.stdout.strip() else t.stderr.strip()[-200:])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
