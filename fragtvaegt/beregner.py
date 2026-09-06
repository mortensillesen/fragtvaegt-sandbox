"""Volumenvaegt, fragtpligtig vaegt og afrunding.

Regler (se README.md):
* Volumenvaegt per kolli = laengde x bredde x hoejde (cm) / divisor for transportformen.
* Fragtpligtig vaegt for hele forsendelsen = den stoerste af samlet faktisk vaegt og samlet volumenvaegt.
* Afrunding: fly op til naermeste 0,5 kg, vej og soe op til naermeste hele kg.
* Under minimum for transportformen faktureres minimum.
"""
import math

from .modeller import Forsendelse, Kolli
from .takster import hent_takster


def volumenvaegt(kolli: Kolli, transportform: str, takster: dict = None) -> float:
    takster = takster or hent_takster()
    divisor = takster["divisor"][transportform]
    return kolli.volumen_cm3 / divisor * kolli.antal


def afrund_vaegt(vaegt: float, transportform: str) -> float:
    """Runder op til den enhed, transportformen fakturerer i."""
    if transportform == "fly":
        return math.floor(vaegt * 2) / 2.0
    return float(math.ceil(vaegt))


def fragtpligtig_vaegt(forsendelse: Forsendelse, takster: dict = None) -> float:
    takster = takster or hent_takster()
    tf = forsendelse.transportform
    samlet = 0.0
    for k in forsendelse.kolli:
        faktisk = k.vaegt_kg * k.antal
        volumen = volumenvaegt(k, tf, takster)
        samlet += max(faktisk, volumen)
    minimum = takster["minimum_kg"][tf]
    return max(afrund_vaegt(samlet, tf), minimum)
