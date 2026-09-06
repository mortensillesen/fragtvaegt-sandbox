# fragtvaegt-sandbox

Python 3.9-pakke, der beregner fragtpligtig vægt (chargeable weight) og pris for en forsendelse. Ingen eksterne afhængigheder ud over pytest.

## Kommandoer

* Tests: `python3 -m pytest -q`
* CLI: `python3 -m fragtvaegt <fly|vej|soe> <zone> <LxBxH:VAEGT[xANTAL]> [...] [--tillaeg NAVN]`
* Brug altid `python3 -m ...`, ikke `pytest` eller `python`. De er ikke på PATH.

## Struktur

* `fragtvaegt/modeller.py`: `Kolli` (cm, kg, antal) og `Forsendelse` (kolli, transportform, zone, tillæg). Validerer input.
* `fragtvaegt/beregner.py`: `volumenvaegt`, `afrund_vaegt`, `fragtpligtig_vaegt`.
* `fragtvaegt/pris.py`: `beregn_pris` returnerer en dict med vægt, vægtpris, gebyr, tillæg, total.
* `fragtvaegt/takster.py`: læser `data/takster.json` og cacher.
* `fragtvaegt/cli.py`: argparse. `parse_kolli` tolker `LxBxH:VAEGT[xANTAL]`.
* `tests/`: pytest. Dækningen er ufuldstændig: ingen tests for soe, faste tillæg, flere kolli eller CLI.

## Forretningsregler

Reglerne står i README.md under "Regler i denne applikation". README er facit. Afviger koden fra README, er det koden, der er forkert.

## Arbejdsregler

* Kør tests før og efter hver ændring. Rapportér antal bestået og fejlet.
* Ændr ikke `data/takster.json` uden at sige hvilke felter der ændres og hvorfor.
* Ændr ikke afrundingsregler uden at pege på den linje i README, der begrunder det.
* Små commits med dansk besked i bydeform, fx "Ret afrunding for fly".
* Ingen nye afhængigheder.
