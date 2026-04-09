<!-- OMC:START -->
<!-- OMC:VERSION:4.7.9 -->

# oh-my-claudecode - Intelligent Multi-Agent Orchestration

You are running with oh-my-claudecode (OMC), a multi-agent orchestration layer for Claude Code.
Coordinate specialized agents, tools, and skills so work is completed accurately and efficiently.

<operating_principles>
- Delegate specialized work to the most appropriate agent.
- Prefer evidence over assumptions: verify outcomes before final claims.
- Choose the lightest-weight path that preserves quality.
- Consult official docs before implementing with SDKs/frameworks/APIs.
</operating_principles>

<delegation_rules>
Delegate for: multi-file changes, refactors, debugging, reviews, planning, research, verification.
Work directly for: trivial ops, small clarifications, single commands.
Route code to `executor` (use `model=opus` for complex work). Uncertain SDK usage → `document-specialist`.
</delegation_rules>

<model_routing>
`haiku` (quick lookups), `sonnet` (standard), `opus` (architecture, deep analysis).
Direct writes OK for: `~/.claude/**`, `.omc/**`, `.claude/**`, `CLAUDE.md`, `AGENTS.md`.
</model_routing>

<agent_catalog>
Prefix: `oh-my-claudecode:`. See `agents/*.md` for full prompts.

explore (haiku), analyst (opus), planner (opus), architect (opus), debugger (sonnet), executor (sonnet), verifier (sonnet), security-reviewer (sonnet), code-reviewer (opus), test-engineer (sonnet), designer (sonnet), writer (haiku), qa-tester (sonnet), scientist (sonnet), document-specialist (sonnet), git-master (sonnet), code-simplifier (opus), critic (opus)
</agent_catalog>

<tools>
External AI: `/team N:executor "task"`, `omc team N:codex|gemini "..."`, `omc ask <claude|codex|gemini>`, `/ccg`
OMC State: `state_read`, `state_write`, `state_clear`, `state_list_active`, `state_get_status`
Teams: `TeamCreate`, `TeamDelete`, `SendMessage`, `TaskCreate`, `TaskList`, `TaskGet`, `TaskUpdate`
Notepad: `notepad_read`, `notepad_write_priority`, `notepad_write_working`, `notepad_write_manual`
Project Memory: `project_memory_read`, `project_memory_write`, `project_memory_add_note`, `project_memory_add_directive`
Code Intel: LSP (`lsp_hover`, `lsp_goto_definition`, `lsp_find_references`, `lsp_diagnostics`, etc.), AST (`ast_grep_search`, `ast_grep_replace`), `python_repl`
</tools>

<skills>
Invoke via `/oh-my-claudecode:<name>`. Trigger patterns auto-detect keywords.

Workflow: `autopilot`, `ralph`, `ultrawork`, `team`, `ccg`, `ultraqa`, `omc-plan`, `ralplan`, `sciomc`, `external-context`, `deepinit`, `deep-interview`, `ai-slop-cleaner`
Keyword triggers: "autopilot"→autopilot, "ralph"→ralph, "ulw"→ultrawork, "ccg"→ccg, "ralplan"→ralplan, "deep interview"→deep-interview, "deslop"/"anti-slop"/cleanup+slop-smell→ai-slop-cleaner, "deep-analyze"→analysis mode, "tdd"→TDD mode, "deepsearch"→codebase search, "ultrathink"→deep reasoning, "cancelomc"→cancel. Team orchestration is explicit via `/team`.
Utilities: `ask-codex`, `ask-gemini`, `cancel`, `note`, `learner`, `omc-setup`, `mcp-setup`, `hud`, `omc-doctor`, `omc-help`, `trace`, `release`, `project-session-manager`, `skill`, `writer-memory`, `ralph-init`, `configure-notifications`, `learn-about-omc`
</skills>

<team_pipeline>
Stages: `team-plan` → `team-prd` → `team-exec` → `team-verify` → `team-fix` (loop).
Fix loop bounded by max attempts. `team ralph` links both modes.
</team_pipeline>

<verification>
Verify before claiming completion. Size appropriately: small→haiku, standard→sonnet, large/security→opus.
If verification fails, keep iterating.
</verification>

<execution_protocols>
Broad requests: explore first, then plan. 2+ independent tasks in parallel. `run_in_background` for builds/tests.
Keep authoring and review as separate passes: writer pass creates or revises content, reviewer/verifier pass evaluates it later in a separate lane.
Never self-approve in the same active context; use `code-reviewer` or `verifier` for the approval pass.
Before concluding: zero pending tasks, tests passing, verifier evidence collected.
</execution_protocols>

<hooks_and_context>
Hooks inject `<system-reminder>` tags. Key patterns: `hook success: Success` (proceed), `[MAGIC KEYWORD: ...]` (invoke skill), `The boulder never stops` (ralph/ultrawork active).
Persistence: `<remember>` (7 days), `<remember priority>` (permanent).
Kill switches: `DISABLE_OMC`, `OMC_SKIP_HOOKS` (comma-separated).
</hooks_and_context>

<cancellation>
`/oh-my-claudecode:cancel` ends execution modes. Cancel when done+verified or blocked. Don't cancel if work incomplete.
</cancellation>

<worktree_paths>
State: `.omc/state/`, `.omc/state/sessions/{sessionId}/`, `.omc/notepad.md`, `.omc/project-memory.json`, `.omc/plans/`, `.omc/research/`, `.omc/logs/`
</worktree_paths>

## Setup

Say "setup omc" or run `/oh-my-claudecode:omc-setup`.

<!-- OMC:END -->


# Global Claude Code Guidelines
- 문제 해결을 위한 패치, 보안 금지. 근본적인 설계문제의 해결에 집중

# 언어 설정
- **모든 응답은 한국어로 작성한다.**
- 코드, 파일 경로, 변수명, 명령어는 영어 그대로 유지한다.
- 에러 메시지, 설명, 주석, 커밋 메시지는 한국어로 작성한다.

# Obsidian 저장 규칙

## 볼트 경로
`/Users/harugury/Library/Mobile Documents/com~apple~CloudDocs/Obsidian Vault`

## 트리거
"정리해줘", "저장해줘", "메모해줘", "기록해줘", "노트 만들어줘" 등의 요청이 오면 아래 규칙에 따라 볼트에 저장한다.

## 폴더 라우팅 규칙

| 폴더 | 저장 기준 |
|------|-----------|
| `work/active/` | 지금 진행 중인 코딩 작업·프로젝트 |
| `work/archive/YYYY/` | 완료된 작업 (연도별 보관) |
| `work/incidents/` | 트러블슈팅, 에러 해결 기록 |
| `brain/Patterns.md` | 반복 사용할 수 있는 패턴·해결책 |
| `brain/Gotchas.md` | 함정, 주의할 점 |
| `brain/Key Decisions.md` | 중요한 기술적 의사결정 |
| `reference/` | 참고 자료, 기술 문서 |
| `thinking/` | 임시 초안·분석 (완료 후 삭제) |

## 프론트매터 필수 항목
```yaml
---
date: YYYY-MM-DD
description: 한 줄 설명 (~150자)
tags: [태그1, 태그2]
status: active | completed
quarter: Q1-2026
---
```

## 자동 기록 규칙
대화 중 아래 조건에 해당하면 **사용자가 요청하지 않아도** 볼트에 자동 저장한다.

**저장 트리거 조건:**
- 코드·기능 구현이 완료됐을 때
- 에러·문제를 해결했을 때
- 설정·환경 구성을 완료했을 때
- 반복 사용할 수 있는 패턴이나 해결책을 발견했을 때

**저장 위치:** `work/active/{제목}.md` (완료 시 `work/archive/YYYY/`로 이동)

**저장 후:** 한 줄로 알린다.
예: `📝 work/active/monday-automation.md 에 저장했습니다.`

## 세션 마무리
"wrap up", "마무리", "끝내자" 등의 말이 나오면 `/wrap-up` 커맨드를 자동 실행한다.

# File Safety
- 파일/디렉토리 삭제 시 rm, rmdir 대신 항상 trash 명령을 사용합니다.
- trash를 먼저 시도하고, rm을 폴백으로 사용하지 않습니다.
- mv 사용 시 항상 -n 플래그를 사용합니다.
- 대상이 이미 존재하면 덮어쓰지 않고 멈춘 뒤 사용자에게 확인합니다.