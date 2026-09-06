#!/usr/bin/env python3
"""Takstserver: en lille MCP-server uden afhaengigheder (modul 05).

Simulerer et eksternt takstsystem, som agenten kun kan naa gennem en forbindelse.
Zone 5 findes kun her, ikke i data/takster.json.

Protokol: JSON-RPC 2.0 over stdio, en besked per linje, efter MCP-specifikationen
2025-06-18 (basic/lifecycle, basic/transports, server/tools). Logning gaar til stderr.
"""
import json
import sys

PROTOKOLVERSION = "2025-06-18"

# Den "eksterne" prisliste. Bemaerk zone 5, som repoet ikke kender.
PRISLISTE = {
    "valuta": "DKK",
    "zoner": {
        "1": {"navn": "Danmark", "kr_per_kg": {"fly": 42.0, "vej": 3.2, "soe": 0.9}},
        "2": {"navn": "Norden", "kr_per_kg": {"fly": 55.0, "vej": 4.6, "soe": 1.3}},
        "3": {"navn": "Europa", "kr_per_kg": {"fly": 71.0, "vej": 6.1, "soe": 1.8}},
        "4": {"navn": "Europa, fjern", "kr_per_kg": {"fly": 96.0, "vej": 8.4, "soe": 2.4}},
        "5": {"navn": "Oversoeisk", "kr_per_kg": {"fly": 128.0, "soe": 3.1}},
    },
}

VAERKTOEJER = [
    {
        "name": "liste_zoner",
        "description": "Returnerer alle zoner i det eksterne takstsystem med navn og hvilke transportformer der tilbydes.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "hent_takst",
        "description": "Henter kr per kg for en zone og en transportform (fly, vej eller soe) fra det eksterne takstsystem.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "zone": {"type": "string", "description": "Zonenummer som tekst, fx \"5\""},
                "transportform": {"type": "string", "enum": ["fly", "vej", "soe"]},
            },
            "required": ["zone", "transportform"],
        },
    },
]


def log(besked):
    sys.stderr.write("takstserver: %s\n" % besked)
    sys.stderr.flush()


def send(obj):
    sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def svar(id_, result):
    send({"jsonrpc": "2.0", "id": id_, "result": result})


def fejl(id_, code, message):
    send({"jsonrpc": "2.0", "id": id_, "error": {"code": code, "message": message}})


def tekst(t, is_error=False):
    return {"content": [{"type": "text", "text": t}], "isError": is_error}


def kald(navn, args):
    if navn == "liste_zoner":
        linjer = []
        for nr, z in PRISLISTE["zoner"].items():
            linjer.append("zone %s: %s (%s)" % (nr, z["navn"], ", ".join(sorted(z["kr_per_kg"]))))
        return tekst("\n".join(linjer))
    if navn == "hent_takst":
        zone = str(args.get("zone", ""))
        tf = args.get("transportform", "")
        z = PRISLISTE["zoner"].get(zone)
        if z is None:
            return tekst("ukendt zone: %s" % zone, True)
        if tf not in z["kr_per_kg"]:
            return tekst("zone %s tilbyder ikke %s" % (zone, tf), True)
        return tekst("zone %s (%s), %s: %.2f %s per kg" % (zone, z["navn"], tf, z["kr_per_kg"][tf], PRISLISTE["valuta"]))
    return None


def haandter(besked):
    metode = besked.get("method")
    id_ = besked.get("id")
    params = besked.get("params") or {}
    if metode == "initialize":
        log("initialize fra %s" % (params.get("clientInfo") or {}).get("name", "ukendt klient"))
        svar(id_, {
            "protocolVersion": PROTOKOLVERSION,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "takstserver", "version": "1.0.0"},
        })
    elif metode == "notifications/initialized":
        log("klar")
    elif metode == "ping":
        svar(id_, {})
    elif metode == "tools/list":
        svar(id_, {"tools": VAERKTOEJER})
    elif metode == "tools/call":
        navn = params.get("name")
        log("tools/call %s %s" % (navn, json.dumps(params.get("arguments") or {}, ensure_ascii=False)))
        r = kald(navn, params.get("arguments") or {})
        if r is None:
            fejl(id_, -32602, "Unknown tool: %s" % navn)
        else:
            svar(id_, r)
    elif id_ is not None:
        fejl(id_, -32601, "Method not found: %s" % metode)


def main():
    for linje in sys.stdin:
        linje = linje.strip()
        if not linje:
            continue
        try:
            besked = json.loads(linje)
        except ValueError:
            fejl(None, -32700, "Parse error")
            continue
        try:
            haandter(besked)
        except Exception as e:  # noqa: BLE001
            log("fejl: %s" % e)
            if besked.get("id") is not None:
                fejl(besked.get("id"), -32603, "Internal error")


if __name__ == "__main__":
    main()
