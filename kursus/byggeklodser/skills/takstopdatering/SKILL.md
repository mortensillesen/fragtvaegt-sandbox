---
name: takstopdatering
description: Opdaterer data/takster.json med takster fra takstserveren for en given zone og verificerer med tests. Brug ved "/takstopdatering <zone>".
disable-model-invocation: true
argument-hint: <zone>
---

Opdatér takster for zone $ARGUMENTS i denne rækkefølge, og spring ikke trin over:

1. Kald værktøjet `liste_zoner` på takstserveren og bekræft, at zonen findes. Findes den ikke, stop og sig det.
2. Kald `hent_takst` for hver transportform, zonen tilbyder.
3. Skriv taksterne ind i `data/takster.json` under `kr_per_kg`. Rør ikke andre felter.
4. Kør `python3 -m pytest -q`. Fejler noget, ret det ikke selv. Rapportér.
5. Bed subagenten `takst-tester` om at køre CLI-tjekket for zonen.
6. Afslut med en oversigt: zone, takster per transportform, testresultat, CLI-resultat.
