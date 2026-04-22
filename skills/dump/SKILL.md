---
name: dump
description: Freeform capture mode. Dump anything — conversations, decisions, incidents, wins, thoughts — and routes it all to the right Obsidian vault notes with proper templates, frontmatter, and wikilinks. Triggered by "dump", "기록해줘", "저장해줘", or freeform information the user wants filed. ALSO: automatically activates for ALL user-provided content during a 회고 session. When the user says "회고 시작", "회고하자", "회고 세션", "회고 할게" or similar, treat every subsequent message as content to process through dump — no explicit /dump command needed. Continue in 회고 mode until the user says "마무리", "끝", or triggers wrap-up.
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

Triggered when the user wants to capture freeform information — meeting notes, decisions, wins, incidents, thoughts, etc.

## 회고 세션 모드

사용자가 "회고 시작", "회고하자", "회고 세션", "회고 할게" 등을 말하면:

1. 회고 세션이 시작된 것으로 간주한다.
2. 이후 사용자가 보내는 **모든 메시지**를 dump 워크플로우로 자동 처리한다.
3. 명시적인 `/dump` 커맨드 없이도 사용자가 입력하는 내용을 그대로 vault에 분류·저장한다.
4. 사용자가 "마무리", "끝", "wrap up" 등을 말할 때까지 이 모드를 유지한다.
5. 회고 세션 종료 시 wrap-up 스킬을 자동으로 실행한다.

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
