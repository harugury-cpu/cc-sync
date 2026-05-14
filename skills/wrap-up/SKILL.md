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

## Vault Structure (Actual)

```
work/
  Project/
    leading/          # Active projects (leading role)
    participating/    # Active projects (participating role)
  archive/
    leading/          # Completed/archived leading projects
    participating/    # Completed/archived participating projects
  incidents/          # Incident logs
  Index.md            # Project index

회고일기/
  Daily/              # Daily retrospective notes (YYYY.MM.DD.md)
  2026.04 N주차/      # Weekly folders containing daily notes
  2026.05 N주차/
  대화회고/           # Conversation retrospectives

brain/
  Patterns.md
  Gotchas.md
  Memories.md
  Key Decisions.md
  Skills.md
  North Star.md

org/
  People & Context.md
  people/
  teams/

perf/
  evidence/
    Brag Doc.md
    2026 H1 KPI.md
    Portfolio.md
  competencies/
  brag/

Apps/
  Trace.md            # Personal desktop app PRD

Dashboard.md          # Project dashboard (Dataview-based)
Home.md
CLAUDE.md
```

## Project Frontmatter Standard

All project notes under `work/Project/leading/`, `work/Project/participating/`, `work/archive/leading/`, `work/archive/participating/` follow this schema:

```yaml
---
date: YYYY-MM-DD            # Project start date
description: "..."          # Short summary
tags: [work-note, ...]
status: active | done | completed | paused | archived
quarter: Q1-2026 | Q2-2026 | ...
role: leading | participating
current_stage: "..."        # Current stage description
last_updated: YYYY-MM-DD    # Last meaningful update
project_folder: "..."       # Absolute path to working folder (if exists)
related_repo: "..."         # GitHub repo (e.g. "harugury-cpu/box-engine-")

# Optional KPI fields (only for H1/H2 KPI projects)
is_kpi: true
kpi_label: "H1-A" | "H1-B" | "H1-C"
stage_number: 2
total_stages: 5
---
```

## Usage

```
/wrap-up
```

Triggered when the user says "wrap up", "let's wrap", "wrapping up", "랩업", "마무리", "정리해줘", or similar. Claude should invoke this automatically.

## Workflow

### 1. Review What Was Done

Scan the conversation for:
- Notes created or modified (list with absolute paths)
- People notes created or updated (`org/People & Context.md`, `org/people/`, `org/teams/`)
- Indexes updated (`work/Index.md`, `Home.md`, `Dashboard.md`)
- Brag doc entries added (`perf/evidence/Brag Doc.md`, `perf/brag/Q?.md`)
- Brain notes updated (`brain/Patterns.md`, `brain/Gotchas.md`, `brain/Key Decisions.md`, `brain/Memories.md`, `brain/Skills.md`)
- Daily retrospective updates (`회고일기/Daily/YYYY.MM.DD.md` or weekly folders)

### 2. Verify Note Quality

For each project note created or modified:

**Required frontmatter** (check all 7 base fields):
- `date` — project start date present?
- `description` — present, ~150 chars?
- `tags` — at least one tag?
- `status` — one of: active / done / completed / paused / archived
- `quarter` — Q?-YYYY format?
- `role` — leading or participating?

**Standard fields added per project standard** (check all 4):
- `current_stage` — non-empty descriptive text?
- `last_updated` — YYYY-MM-DD format, plausible (not future)?
- `project_folder` — absolute path or empty string?
- `related_repo` — GitHub repo or empty string?

**KPI fields** (only if `is_kpi: true`):
- `kpi_label` — H1-A / H1-B / H1-C / etc.?
- `stage_number` ≤ `total_stages`?
- `total_stages` ≥ 1?

**Other checks**:
- At least one wikilink to another note?
- Correct folder?
  - Active leading → `work/Project/leading/`
  - Active participating → `work/Project/participating/`
  - Completed/archived → `work/archive/leading/` or `work/archive/participating/`
  - Incident → `work/incidents/`

### 3. Check Index Consistency

- `work/Index.md` — new project notes linked?
- `Dashboard.md` — "지금 봐야 할 프로젝트" curation still current? Manual pins outdated?
- `brain/Memories.md` — Recent Context updated?
- `org/People & Context.md` — new people captured? new people notes under `org/people/` indexed?
- `perf/evidence/Brag Doc.md` — wins added?
- `perf/brag/Q?-YYYY.md` — quarterly wins added?
- `Home.md` — Bases still valid?

### 4. Check for Orphans

- New notes not linked from anywhere?
- New people not in `org/People & Context.md`?
- Thinking notes (`thinking/`) to promote or delete?
- Daily retrospective wikilinks pointing to non-existent notes?

### 5. Archive Check

- `work/Project/leading/` notes that should move to `work/archive/leading/`?
- `work/Project/participating/` notes that should move to `work/archive/participating/`?
- `status: active` fields that should be `done` or `completed`?
- When moving: also update wikilinks in any daily notes (`회고일기/`) that reference the old path.

### 6. Daily/Weekly Retrospective Consistency

- Today's daily note (`회고일기/Daily/YYYY.MM.DD.md` or current week folder) exists?
- Today's daily mentions all projects worked on (via `[[...]]` wikilinks)?
- Weekly folder (`회고일기/YYYY.MM N주차/`) contains all daily notes for that week?
- For each project mentioned today, was `last_updated` field on the project note bumped?

### 7. Ways of Working Review

- New pattern → `brain/Patterns.md`?
- New gotcha → `brain/Gotchas.md`?
- Workflow improvement → `brain/Skills.md`?
- Important decision → `brain/Key Decisions.md`?
- Long-term context → `brain/Memories.md`?
- North Star drift → `brain/North Star.md`?
- CLAUDE.md update needed?
- New slash command or hook?

### 8. Suggest Improvements

- Friction points in the workflow?
- Manual steps to automate?
- Repeated patterns that should become a skill?
- New Bases needed?
- Trace app (`Apps/Trace.md`) — opportunities for new data sources or views?

### 9. Report

- **Done**: what was captured this session
- **Fixed**: issues found and resolved
- **Flagged**: things needing user input (especially: status changes, archive moves)
- **Suggested**: improvements for next time

## Important

- READ + VERIFY pass only — fix small issues, flag large changes for user approval.
  - **Small (auto-fix)**: missing `date`, missing `description`, malformed frontmatter, typos.
  - **Large (flag only)**: `status` changes, archive moves, `current_stage` rewrites, `stage_number` increments. These require the user's judgment about the project state.
- Be honest about what's missing.
- Always use the absolute vault path when reading files.
- If North Star goals shifted during the session, suggest updating it.
- When in doubt about file location, prefer `work/Project/leading/` for new leading projects and check `Dashboard.md`'s scan paths to confirm.
