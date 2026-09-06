from dataclasses import dataclass, field
from typing import List

TRANSPORTFORMER = ("fly", "vej", "soe")


@dataclass(frozen=True)
class Kolli:
    """Et kolli: maal i cm, vaegt i kg, antal ens kolli."""
    laengde_cm: float
    bredde_cm: float
    hoejde_cm: float
    vaegt_kg: float
    antal: int = 1

    def __post_init__(self):
        for navn in ("laengde_cm", "bredde_cm", "hoejde_cm", "vaegt_kg"):
            if getattr(self, navn) <= 0:
                raise ValueError("%s skal vaere stoerre end 0" % navn)
        if self.antal < 1:
            raise ValueError("antal skal vaere mindst 1")

    @property
    def volumen_cm3(self) -> float:
        return self.laengde_cm * self.bredde_cm * self.hoejde_cm


@dataclass
class Forsendelse:
    kolli: List[Kolli]
    transportform: str
    zone: int
    tillaeg: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.transportform not in TRANSPORTFORMER:
            raise ValueError("ukendt transportform: %s" % self.transportform)
        if not self.kolli:
            raise ValueError("en forsendelse skal have mindst et kolli")

    @property
    def faktisk_vaegt(self) -> float:
        return sum(k.vaegt_kg * k.antal for k in self.kolli)
