# fragtvaegt-sandbox

Lille Python-applikation, der beregner fragtpligtig vægt (chargeable weight) og pris for en forsendelse. Bruges som øvelsesrepo i agentkurset. Koden må gerne gå i stykker, det er meningen.

## Kør

Kræver Python 3.9 eller nyere og pytest.

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m pytest -q
python3 -m fragtvaegt fly 2 60x40x50:12
python3 -m fragtvaegt vej 1 120x80x100:180x2 --tillaeg brandstof
```

Et kolli skrives som `LxBxH:VAEGT[xANTAL]` i cm og kg.

## Regler i denne applikation

Konventionerne her er dem, applikationen følger. De er valgt, så tallene er lette at regne efter i hovedet.

| | fly | vej | soe |
|---|---|---|---|
| Volumenvægt | L x B x H (cm) / 6000 | / 3000 | / 1000 |
| Afrunding | op til nærmeste 0,5 kg | op til hele kg | op til hele kg |
| Minimum | 1 kg | 30 kg | 100 kg |
| Gebyr per forsendelse | 250 kr | 95 kr | 400 kr |

* Fragtpligtig vægt beregnes for hele forsendelsen: den største af samlet faktisk vægt og samlet volumenvægt, derefter afrundet, derefter løftet til minimum.
* Pris = fragtpligtig vægt x kr/kg for zonen + gebyr. Procent-tillæg beregnes af den sum. Faste tillæg lægges til bagefter.
* Totalen afrundes til hele kroner. Halve kroner rundes op.
* Zoner 1 til 4 og takster står i `data/takster.json`.

## Struktur

```
fragtvaegt/        pakken: modeller, beregner, pris, takster, cli
tests/             pytest
data/takster.json  zoner, takster, gebyrer, tillæg
site/              lille statisk side, deployes af workflowen i modul 09
kursus/            komponenter til kurset, alle slået fra som udgangspunkt
```

## Til kurset

Hvert modul har en startbranch `start/modul-NN`. Kursussiden viser den kommando, der stiller repoet om til modulets startpunkt. Komponenterne i `kursus/` aktiveres kun, når et modul beder om det.
