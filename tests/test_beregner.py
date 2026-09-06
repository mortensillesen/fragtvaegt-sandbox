from fragtvaegt import Forsendelse, Kolli, fragtpligtig_vaegt, volumenvaegt


def test_volumenvaegt_fly():
    # 60 x 40 x 50 cm = 120000 cm3, divisor 6000 -> 20 kg
    assert volumenvaegt(Kolli(60, 40, 50, 12), "fly") == 20.0


def test_fragtpligtig_er_volumenvaegt_naar_den_er_stoerst():
    f = Forsendelse([Kolli(60, 40, 50, 12)], "fly", 2)
    assert fragtpligtig_vaegt(f) == 20.0


def test_fragtpligtig_er_faktisk_vaegt_naar_den_er_stoerst():
    # 30 x 20 x 10 = 6000 cm3 -> 1 kg volumen, men 12 kg faktisk
    f = Forsendelse([Kolli(30, 20, 10, 12)], "fly", 1)
    assert fragtpligtig_vaegt(f) == 12.0


def test_fly_afrundes_op_til_naermeste_halve_kilo():
    # 40 x 30 x 20 = 24000 cm3 -> 4,0 kg volumen, faktisk 4,2 kg -> faktureres som 4,5 kg
    f = Forsendelse([Kolli(40, 30, 20, 4.2)], "fly", 1)
    assert fragtpligtig_vaegt(f) == 4.5


def test_vej_afrundes_op_til_hele_kilo():
    # 100 x 60 x 50 = 300000 cm3 / 3000 = 100 kg volumen, faktisk 100,3 -> 101 kg
    f = Forsendelse([Kolli(100, 60, 50, 100.3)], "vej", 1)
    assert fragtpligtig_vaegt(f) == 101.0


def test_vej_under_minimum_faktureres_som_minimum():
    f = Forsendelse([Kolli(10, 10, 10, 1)], "vej", 1)
    assert fragtpligtig_vaegt(f) == 30.0


def test_ugyldigt_kolli_afvises():
    import pytest
    with pytest.raises(ValueError):
        Kolli(0, 10, 10, 1)
