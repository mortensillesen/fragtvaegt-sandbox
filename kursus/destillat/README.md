# Destillat (modul 14)

`opdater_takst.py` løser samme opgave som systemet i modul 10, uden model: den taler direkte med takstserveren over stdio, skriver taksterne ind og kører testene. Én fil, cirka 70 linjer, deterministisk.

```bash
python3 kursus/destillat/opdater_takst.py 5
```

Det, der er tilbage til en agent, er dømmekraften: subagenten `takst-tester` fra modul 10 kan stadig bruges til at regne efter og rapportere.
