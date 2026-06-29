---
name: obsidian-cli
description: Interact with Obsidian vaults using the Obsidian CLI to read, create, search, and manage notes, tasks, properties, and more. Also supports plugin and theme development with commands to reload plugins, run JavaScript, capture errors, take screenshots, and inspect the DOM. Use when the user asks to interact with their Obsidian vault, manage notes, search vault content, perform vault operations from the command line, or develop and debug Obsidian plugins and themes.
---

# Obsidian CLI

Use the `obsidian` CLI to interact with a running Obsidian instance. Requires Obsidian to be open.

## 3-Tier Fallback Pattern

Always try tiers in order. Move to the next tier only when the current tier fails.

**Tier 1 — Obsidian CLI (primary)**
```bash
/opt/homebrew/bin/obsidian <command>
```

**Tier 2 — MCP server**
Use the Obsidian MCP server tools if available and CLI fails.

**Tier 3 — Direct file access**
Use Write/Read/Grep tools directly on vault files as last resort.

## Environment Setup

### Install (macOS)

```bash
# Homebrew (recommended)
brew install obsidian-cli

# Verify installation
which obsidian          # → /opt/homebrew/bin/obsidian
obsidian --version
```

### Vault Path Setup

Find vault root path from Obsidian: Settings → General → "Vault path"

```bash
# Test vault access
obsidian vault="Second Brain" search query="test" limit=1
```

**Path normalization rules:**
- Use vault-relative paths only: `Library/Books/my-book.md`
- Never use vault-root-prefixed paths: `Second_Brain/Library/...` (wrong)
- No leading slash: `Library/Books/note.md` (correct)
- Wikilink-style name resolution via `file=`: no path, no `.md` extension needed

## Command Reference

Run `obsidian help` to see all available commands. Full docs: https://help.obsidian.md/cli

## Syntax

**Parameters** take a value with `=`. Quote values with spaces:

```bash
obsidian create name="My Note" content="Hello world"
```

**Flags** are boolean switches with no value:

```bash
obsidian create name="My Note" silent overwrite
```

For multiline content use `\n` for newline and `\t` for tab.

## File Targeting

Many commands accept `file` or `path` to target a file. Without either, the active file is used.

- `file=<name>` — resolves like a wikilink (name only, no path or extension needed)
- `path=<path>` — exact path from vault root, e.g. `folder/note.md`

## Vault Targeting

Commands target the most recently focused vault by default. Use `vault=<name>` as the first parameter to target a specific vault:

```bash
obsidian vault="My Vault" search query="test"
```

## Common Patterns

```bash
obsidian read file="My Note"
obsidian create name="New Note" content="# Hello" template="Template" silent
obsidian append file="My Note" content="New line"
obsidian search query="search term" limit=10
obsidian daily:read
obsidian daily:append content="- [ ] New task"
obsidian property:set name="status" value="done" file="My Note"
obsidian tasks daily todo
obsidian tags sort=count counts
obsidian backlinks file="My Note"
```

Use `--copy` on any command to copy output to clipboard. Use `silent` to prevent files from opening. Use `total` on list commands to get a count.

## Obsidian URI Scheme

Use `obsidian://` URIs to open notes directly in the app:

```bash
# Open a note (URL-encode spaces as %20, slashes as %2F)
obsidian "obsidian://open?vault=Second%20Brain&file=Library%2FBooks%2Fmy-book"

# Open daily note
obsidian "obsidian://daily"
```

URL encoding quick reference:
- Space → `%20`
- `/` → `%2F`
- `#` → `%23`

```bash
# Encode a path with python3
python3 -c "import urllib.parse; print(urllib.parse.quote('Library/Books/My Note'))"
```

## Known Bugs + Workarounds

### Bug 1: `search:context` exits with code 255

**Symptom:** `obsidian search:context query="..."` returns exit code 255 with no output.

**Workaround:** Use plain `search` instead:
```bash
# Wrong
obsidian search:context query="keyword"

# Correct
obsidian search query="keyword"
```

### Bug 2: `deadends --format=json` not supported

**Symptom:** `obsidian deadends --format=json` fails or outputs non-JSON.

**Workaround:** Capture stdout and parse with python3:
```bash
obsidian deadends | python3 -c "
import sys
lines = sys.stdin.read().strip().splitlines()
import json; print(json.dumps(lines))
"
```

### Bug 3: Mac GraphRAG index not deployed

**Symptom:** Semantic search / connection detection commands return no results or error on macOS.

**Cause:** GraphRAG index is not deployed for Mac builds (as of 2026-06).

**Workaround:** Use 4th-tier fallback — combine Obsidian CLI keyword search with Grep:
```bash
# Keyword search via CLI
obsidian search query="keyword" limit=20

# Then grep vault files for additional matches
grep -r "keyword" /path/to/vault --include="*.md" -l
```

Semantic connection detection (`similar`, `related`) is not available on Mac. Do not attempt; use explicit link traversal via `backlinks` and `outgoing` commands instead.

## Self-Verification (5 Steps)

Run these checks when CLI behaves unexpectedly:

```bash
# Step 1: Binary exists
ls -la /opt/homebrew/bin/obsidian

# Step 2: Vault path accessible
obsidian vault="<VaultName>" search query="." limit=1

# Step 3: Search working
obsidian search query="test" limit=3

# Step 4: URI scheme functional
obsidian "obsidian://open?vault=<VaultName>&file=<NoteName>"
# (Obsidian should open/focus the note)

# Step 5: MCP fallback available
# Verify MCP server is running if Tier 1 fails
```

If Step 1 fails → install via `brew install obsidian-cli`
If Step 2 fails → check vault name spelling and that Obsidian is open
If Step 3 fails → check if Obsidian is in focus (run `open -a Obsidian` first)
If Step 4 fails → check URL encoding
If Step 5 needed → switch to Tier 2 (MCP) or Tier 3 (file tools)

## Plugin Development

### Develop/Test Cycle

After making code changes to a plugin or theme, follow this workflow:

1. **Reload** the plugin to pick up changes:
   ```bash
   obsidian plugin:reload id=my-plugin
   ```
2. **Check for errors** — if errors appear, fix and repeat from step 1:
   ```bash
   obsidian dev:errors
   ```
3. **Verify visually** with a screenshot or DOM inspection:
   ```bash
   obsidian dev:screenshot path=screenshot.png
   obsidian dev:dom selector=".workspace-leaf" text
   ```
4. **Check console output** for warnings or unexpected logs:
   ```bash
   obsidian dev:console level=error
   ```

### Additional Developer Commands

Run JavaScript in the app context:

```bash
obsidian eval code="app.vault.getFiles().length"
```

Inspect CSS values:

```bash
obsidian dev:css selector=".workspace-leaf" prop=background-color
```

Toggle mobile emulation:

```bash
obsidian dev:mobile on
```

Run `obsidian help` to see additional developer commands including CDP and debugger controls.
