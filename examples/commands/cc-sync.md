---
description: User Scope (~/.claude/) to project sync
---

# cc-sync

**Direction: ~/.claude/ -> Git project**

Syncs your local Claude Code settings to this git repository.

## Usage

Run the sync script in the project root:

```bash
./sync.sh          # Interactive (asks for commit message)
./sync.sh --auto   # Auto commit + push
```

## What it syncs

1. agents, hooks, skills, memory, plugins, commands, scripts, rules, teams
2. settings.json, CLAUDE.md
3. Optional: keybindings.json, claude_desktop_config.json
4. memory-bank sync data (for multi-device)
