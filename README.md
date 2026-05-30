# cc-sync

Back up and sync your Claude Code settings (`~/.claude/`) plus shared Agents/Codex config via Git. Restore instantly on any device.

![Why You Need This](docs/images/01-problem.png)

![How It Works](docs/images/02-architecture.png)

![What Gets Synced](docs/images/03-sync-targets.png)

![Usage](docs/images/04-usage.png)

![Multi-Device Sync](docs/images/05-multi-device.png)

![Automation Pipeline](docs/images/06-automation.png)

## The Problem

- `~/.claude/` only exists locally -- OS reinstall or disk failure = everything gone
- Multiple devices = skills, hooks, rules evolving separately on each machine
- Manual sync is error-prone -- miss one file and things break

## How It Works

```
~/.claude/                    cc-sync (Git repo)              Other Device
~/.agents/    ──sync.sh──→     skills/      ──apply.sh──→     ~/.claude/
~/.codex/                      hooks/                           ~/.agents/
  skills/                      rules/                           ~/.codex/
  rules/                       home-agents/
  memories/                    codex/
  automations/                 memory-bank-sync/   ←── import-sync.sh
```

## Quick Start

### 1. Clone this repo

```bash
git clone https://github.com/YOUR_USERNAME/cc-sync.git ~/Project/cc-sync
cd ~/Project/cc-sync
```

### 2. First sync (export your settings)

```bash
./sync.sh
# Follow prompts to commit and push
```

### 3. On another device (import)

```bash
git clone https://github.com/YOUR_USERNAME/cc-sync.git ~/Project/cc-sync
cd ~/Project/cc-sync
./apply.sh
claude restart
```

## Slash Commands (Optional)

Copy the example command files to enable `/cc-sync` and `/cc-apply` in Claude Code:

```bash
cp examples/commands/cc-sync.md ~/.claude/commands/
cp examples/commands/cc-apply.md ~/.claude/commands/
```

Then in Claude Code:
```
/cc-sync     # Export: ~/.claude/ → Git
/cc-apply    # Import: Git → ~/.claude/
```

## What Gets Synced

| Directory | Description |
|-----------|-------------|
| `agents/` | Custom agent definitions |
| `skills/` | Skill files (SKILL.md) |
| `hooks/` | Hook scripts (auto-validate, notifications, etc.) |
| `rules/` | Rule files (coding patterns, review rules) |
| `plugins/` | Installed plugins |
| `commands/` | Slash command definitions |
| `scripts/` | Utility scripts |
| `memory/` | Memory files |
| `teams/` | Team definitions |
| `settings.json` | Global settings |
| `CLAUDE.md` | Global instructions |
| `home-agents/` | Shared `~/.agents/` skills and setup |
| `codex/` | Safe Codex config: skills, rules, memories, automations, non-cache plugin metadata |
| `memory-bank-sync/` | Cross-device memory-bank facts |

### What is intentionally not synced

- `~/.cokacdir/`
- Codex auth/session/runtime state: `auth.json`, `sessions/`, `history.jsonl`, sqlite DBs, logs, cache, tmp, generated images, Computer Use app bundle
- Claude/Codex credentials that should be re-authenticated per device

## Automation

### Daily auto-sync (within a Claude Code session)

```
/loop 1d /cc-sync
```

### Memory-Bank cross-device sync

Cross-device memory sync requires the [memory-bank](https://github.com/jung-wan-kim/memory-bank) plugin:

```bash
# Install memory-bank plugin (one-time)
/plugin marketplace add https://github.com/jung-wan-kim/memory-bank
/plugin install memory-bank
```

Then on each device:

```bash
# On Device B after git pull:
./import-sync.sh
```

This copies memory-bank facts so the next session automatically imports them.

## Security

**Before pushing to a remote repo, check for sensitive data:**

- Telegram Bot tokens / Chat IDs
- Supabase keys (especially `service_role`)
- API keys, passwords
- Personal file paths

**Recommended `.gitignore` entries** (already included):

```
settings.local.json
claude_desktop_config.json
memory/
memory-bank-sync/
plugins/cache/
```

**Use environment variables** instead of hardcoding secrets:

```bash
# In your shell profile (~/.zshrc or ~/.bashrc)
export TELEGRAM_BOT_TOKEN="your-token"
export TELEGRAM_CHAT_ID="your-chat-id"
```

Then reference in scripts:
```bash
BOT_TOKEN="${TELEGRAM_BOT_TOKEN}"
```

## Project Structure

```
cc-sync/
├── sync.sh              # Export: ~/.claude/ → Git
├── apply.sh             # Import: Git → ~/.claude/
├── import-sync.sh       # Import memory-bank sync data
├── .gitignore           # Excludes sensitive/large files
├── examples/
│   ├── CLAUDE.md.example
│   ├── settings.json.example
│   └── commands/
│       ├── cc-sync.md
│       └── cc-apply.md
├── agents/              # (created after first sync)
├── skills/
├── hooks/
├── rules/
├── commands/
├── scripts/
├── plugins/
├── settings.json
└── CLAUDE.md
```

## License

MIT
