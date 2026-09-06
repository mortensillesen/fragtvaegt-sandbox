import pytest

from fragtvaegt import Forsendelse, Kolli, beregn_pris


def test_pris_fly_zone_2_uden_tillaeg():
    # 20 kg x 55 kr + 250 kr gebyr = 1350 kr
    f = Forsendelse([Kolli(60, 40, 50, 12)], "fly", 2)
    r = beregn_pris(f)
    assert r["fragtpligtig_vaegt"] == 20.0
    assert r["vaegtpris"] == 1100.0
    assert r["gebyr"] == 250
    assert r["total"] == 1350


def test_procent_tillaeg_beregnes_af_vaegtpris_plus_gebyr():
    # 1350 kr + 12 % brandstof = 1512 kr
    f = Forsendelse([Kolli(60, 40, 50, 12)], "fly", 2, ["brandstof"])
    assert beregn_pris(f)["total"] == 1512


def test_ukendt_zone_giver_fejl():
    with pytest.raises(ValueError):
        beregn_pris(Forsendelse([Kolli(60, 40, 50, 12)], "fly", 9))


def test_ukendt_tillaeg_giver_fejl():
    with pytest.raises(ValueError):
        beregn_pris(Forsendelse([Kolli(60, 40, 50, 12)], "fly", 1, ["rabat"]))
