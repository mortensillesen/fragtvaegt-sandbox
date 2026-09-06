"""Kommandolinje: python3 -m fragtvaegt <transportform> <zone> <kolli> [<kolli> ...] [--tillaeg NAVN ...]

Et kolli skrives som LxBxH:VAEGT[xANTAL], fx 40x30x20:5 eller 120x80x100:180x2.
"""
import argparse
import sys

from .modeller import Forsendelse, Kolli
from .pris import beregn_pris


def parse_kolli(tekst: str) -> Kolli:
    try:
        maal, rest = tekst.split(":")
        l, b, h = (float(x) for x in maal.split("x"))
        dele = rest.split("x")
        vaegt = float(dele[0])
        antal = int(dele[1]) if len(dele) > 1 else 1
    except (ValueError, IndexError):
        raise argparse.ArgumentTypeError("kolli skal skrives som LxBxH:VAEGT[xANTAL], fik %r" % tekst)
    return Kolli(l, b, h, vaegt, antal)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="fragtvaegt", description="Beregner fragtpligtig vaegt og pris.")
    p.add_argument("transportform", choices=("fly", "vej", "soe"))
    p.add_argument("zone", type=int)
    p.add_argument("kolli", nargs="+", type=parse_kolli)
    p.add_argument("--tillaeg", action="append", default=[], help="fx brandstof, farligt-gods, oe-tillaeg")
    a = p.parse_args(argv)
    try:
        f = Forsendelse(a.kolli, a.transportform, a.zone, a.tillaeg)
        r = beregn_pris(f)
    except ValueError as e:
        print("fejl: %s" % e, file=sys.stderr)
        return 2
    print("Fragtpligtig vaegt: %.1f kg" % r["fragtpligtig_vaegt"])
    print("Vaegtpris:          %.2f %s" % (r["vaegtpris"], r["valuta"]))
    print("Gebyr:              %.2f %s" % (r["gebyr"], r["valuta"]))
    print("Tillaeg:            %.2f %s" % (r["tillaeg"], r["valuta"]))
    print("Total:              %d %s" % (r["total"], r["valuta"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
