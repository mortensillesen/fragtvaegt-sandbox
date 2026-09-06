# Byggeklodser til modul 10

Tre færdige dele, alle slået fra. Modul 10 sætter dem sammen til ét system, der opdaterer takster for en ny zone.

| Del | Fil | Aktivering |
|---|---|---|
| Skill | `skills/takstopdatering/SKILL.md` | `mkdir -p .claude/skills && cp -r kursus/byggeklodser/skills/takstopdatering .claude/skills/` |
| Subagent | `agents/takst-tester.md` | `mkdir -p .claude/agents && cp kursus/byggeklodser/agents/takst-tester.md .claude/agents/` |
| Hook | `hooks/settings.json` og `hooks/test-efter-aendring.sh` | `mkdir -p .claude && cp kursus/byggeklodser/hooks/settings.json .claude/settings.json` |

Skillen forudsætter, at takstserveren fra modul 05 er aktiv (`cp kursus/mcp/mcp.aktiv.json .mcp.json`).

Kilder: code.claude.com/docs/skills, code.claude.com/docs/sub-agents, code.claude.com/docs/hooks. Hentet 2026-09-06.
