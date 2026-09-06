# Pre-commit hook (modul 06)

`pre-commit` kører testene og afviser committen, hvis de fejler. Den er slået fra, indtil git får at vide, at hooks ligger her.

Aktivér:

```bash
git config core.hooksPath kursus/hooks
```

Slå fra igen:

```bash
git config --unset core.hooksPath
```

Kilde: `git help config`, nøglen `core.hooksPath`.
