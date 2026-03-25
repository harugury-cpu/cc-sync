---
description: Project to User Scope (~/.claude/) sync
---

# cc-apply

**Direction: Git project -> ~/.claude/**

Applies settings from this repository to your local Claude Code.

## Usage

Run the apply script in the project root:

```bash
./apply.sh
```

## What it applies

1. agents, hooks, skills, memory, plugins, commands, scripts, rules, teams
2. settings.json, CLAUDE.md
3. Optional: keybindings.json, claude_desktop_config.json
4. Sets executable permissions on hooks and scripts
5. memory-bank sync data import
