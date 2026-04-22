---
name: dump
description: Freeform capture mode. Dump anything — conversations, decisions, incidents, wins, thoughts — and routes it all to the right Obsidian vault notes with proper templates, frontmatter, and wikilinks. Triggered by "dump", "기록해줘", "저장해줘", or freeform information the user wants filed. ALSO: automatically activates for ALL user responses throughout any session whose initial prompt contains "회고를 시작해줘", "회고 대화", "오늘 하루 회고" or similar 회고 schedule openers. In such sessions, every user message is treated as content to process through dump — no explicit /dump command needed.
---

# Dump

Freeform capture mode. Dump anything — conversations, decisions, incidents, wins, thoughts — and I'll route it all to the right notes with proper templates, frontmatter, and wikilinks.

## Vault Path

The Obsidian vault is located at:

```
/Users/harugury/Library/Mobile Documents/com~apple~CloudDocs/Obsidian Vault/
```

All relative paths below resolve from this root.

## Usage

```
/dump <content>
```

## 회고 세션 자동 모드

세션의 초기 프롬프트(스케줄로 시작된 경우)에 다음 중 하나가 포함되어 있으면 즉시 dump 모드로 전환한다:

- "오늘 하루 회고를 시작해줘"
- "회고 대화"
- "회고를 시작해줘"

이 경우, 사용자가 보내는 **모든 메시지**를 별도의 `/dump` 호출 없이 자동으로 dump 워크플로우로 처리한다. 세션이 끝나면 wrap-up 스킬로 마무리한다.

## Workflow

For each distinct piece of information in the dump:

1. **Classify** it: decision, incident, 1-on-1 content, win/achievement, architecture, project update, person context, or general work note.

2. **Search first**: Check if a related note already exists. Prefer appending to existing notes over creating new ones for small updates.

3. **Create or update** the appropriate note following vault conventions:
   - Correct folder placement (`work/active/`, `work/incidents/`, `work/1-1/`, `org/people/`, `회고일기/`, etc.)
   - Full YAML frontmatter with `date`, `description`, `tags`, and type-specific fields
   - All relevant `[[wikilinks]]` to people, projects, teams, competencies

4. **Update indexes** as needed:
   - `work/Index.md`
   - `perf/Brag Doc.md`
   - `org/People & Context.md`

5. **Cross-link**: Ensure every new note links to at least one existing note and is linked FROM at least one existing note.

## Output

After processing, provide a summary:
- What was captured and where each piece was filed
- Any new notes created (with absolute paths)
- Any existing notes updated
- Any items you weren't sure how to classify (ask the user)

## Important

- Always use the absolute vault path when reading or writing files.
- Prefer updating existing notes over creating new ones for small additions.
- When in doubt about classification, file it and flag it rather than skipping.
