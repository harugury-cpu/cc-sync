---
name: wrap-up
description: Full session review before ending. Scans the Obsidian vault for notes created or modified, verifies quality, checks index consistency, and suggests improvements. Triggered by "wrap up", "랩업", "정리해줘", "마무리" and similar phrases.
---

# Wrap Up

Full session review before ending. Review context, ways of working, files modified, consistency, and suggest improvements.

## Vault Path

The Obsidian vault is located at:

```
/Users/harugury/Library/Mobile Documents/com~apple~CloudDocs/Obsidian Vault/
```

All relative paths below resolve from this root.

## Usage

```
/wrap-up
```

Triggered when the user says "wrap up", "let's wrap", "wrapping up", "랩업", "마무리", "정리해줘", or similar. Claude should invoke this automatically.

## Workflow

### 1. Review What Was Done

Scan the conversation for:
- Notes created or modified (list with absolute paths)
- People notes created or updated
- Indexes updated
- Brag doc entries added
- Brain notes updated (Patterns, Gotchas, Key Decisions, Memories)

### 2. Verify Note Quality

For each note created or modified:
- Frontmatter complete? (`date`, `quarter`, `description`, `tags`, type-specific fields)
- At least one wikilink to another note?
- Correct folder? (`work/active/` vs `work/archive/` vs `work/incidents/`)
- Description ~150 chars?
- Status field correct?

### 3. Check Index Consistency

- `work/Index.md` — new notes linked?
- `brain/Memories.md` — Recent Context updated?
- `org/People & Context.md` — new people captured?
- `perf/Brag Doc.md` — wins added?
- `Home.md` — Bases still valid?

### 4. Check for Orphans

- New notes not linked from anywhere?
- New people not in People & Context?
- Thinking notes to promote or delete?

### 5. Archive Check

- `work/active/` notes that should move to `work/archive/YYYY/`?
- Status fields still `active` that should be `completed`?

### 6. Ways of Working Review

- New pattern → `brain/Patterns.md`?
- New gotcha → `brain/Gotchas.md`?
- Workflow improvement → `brain/Skills.md`?
- CLAUDE.md update needed?
- New slash command or hook?

### 7. Suggest Improvements

- Friction points in the workflow?
- Manual steps to automate?
- Repeated patterns that should become a skill?
- New Bases needed?

### 8. Report

- **Done**: what was captured this session
- **Fixed**: issues found and resolved
- **Flagged**: things needing user input
- **Suggested**: improvements for next time

## Important

- READ + VERIFY pass only — fix small issues, flag large changes for user approval.
- Be honest about what's missing.
- Always use the absolute vault path when reading files.
- If North Star goals shifted during the session, suggest updating it.
