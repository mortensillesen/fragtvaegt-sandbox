"""Pris = fragtpligtig vaegt x kr/kg for zonen + gebyr per forsendelse + tillaeg.

Procent-tillaeg beregnes af vaegtpris plus gebyr. Faste tillaeg laegges til bagefter.
Prisen afrundes til hele kroner, halve kroner rundes op.
"""
from .beregner import fragtpligtig_vaegt
from .modeller import Forsendelse
from .takster import hent_takster


def beregn_pris(forsendelse: Forsendelse, takster: dict = None) -> dict:
    takster = takster or hent_takster()
    tf = forsendelse.transportform
    zone = str(forsendelse.zone)
    if zone not in takster["kr_per_kg"][tf]:
        raise ValueError("ukendt zone %s for %s" % (zone, tf))

    vaegt = fragtpligtig_vaegt(forsendelse, takster)
    vaegtpris = vaegt * takster["kr_per_kg"][tf][zone]
    gebyr = takster["gebyr_per_forsendelse"][tf]
    grundlag = vaegtpris + gebyr

    procent_sum = 0.0
    fast_sum = 0.0
    for navn in forsendelse.tillaeg:
        if navn not in takster["tillaeg"]:
            raise ValueError("ukendt tillaeg: %s" % navn)
        t = takster["tillaeg"][navn]
        if t["type"] == "procent":
            procent_sum += grundlag * t["vaerdi"] / 100.0
        else:
            fast_sum += t["vaerdi"]

    total = grundlag + procent_sum + fast_sum
    return {
        "fragtpligtig_vaegt": vaegt,
        "vaegtpris": vaegtpris,
        "gebyr": gebyr,
        "tillaeg": procent_sum + fast_sum,
        "total": round(total),
        "valuta": takster["valuta"],
    }
