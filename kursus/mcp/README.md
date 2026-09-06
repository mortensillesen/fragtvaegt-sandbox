# Takstserver (modul 05)

`takstserver.py` er en MCP-server skrevet i ren Python uden afhængigheder. Den simulerer et eksternt takstsystem. Zone 5 findes kun her.

Som udgangspunkt er `.mcp.json` i repoets rod tom. Aktivér serveren ved at kopiere den forberedte konfiguration ind:

```bash
cp kursus/mcp/mcp.aktiv.json .mcp.json
```

Slå den fra igen:

```bash
git checkout -- .mcp.json
```

Prøv serveren uden Claude, direkte fra terminalen:

```bash
printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"test","version":"0"}}}' '{"jsonrpc":"2.0","method":"notifications/initialized"}' '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"hent_takst","arguments":{"zone":"5","transportform":"fly"}}}' | python3 kursus/mcp/takstserver.py
```

Kilder: MCP-specifikationen 2025-06-18, siderne basic/lifecycle, basic/transports og server/tools.
