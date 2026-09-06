"""fragtvaegt: beregner fragtpligtig vaegt og pris for en forsendelse.

Kolli maales i cm og kg. Transportformer: fly, vej, soe. Zoner: 1 til 4.
Reglerne staar i README.md.
"""
from .modeller import Kolli, Forsendelse
from .beregner import volumenvaegt, fragtpligtig_vaegt, afrund_vaegt
from .pris import beregn_pris

__all__ = ["Kolli", "Forsendelse", "volumenvaegt", "fragtpligtig_vaegt", "afrund_vaegt", "beregn_pris"]
