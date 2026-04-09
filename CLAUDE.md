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

<!-- User customizations (migrated from previous CLAUDE.md) -->
# Global Rules

- 모든 대화 응답은 한국어로 작성한다.
- 터미널 출력(print문, 에러 메시지, 로그)은 파일 경로·변수명·코드 키워드를 제외하고 한국어로 작성.
- 커밋 메시지는 한글로 작성.
- 파일 읽기/쓰기 시 반드시 UTF-8 인코딩 사용.

## 코딩 필수 워크플로우

코드를 작성하거나 수정할 때 **반드시** 아래 순서를 따른다.

1. **플랜 수립** — 작업 시작 전 반드시 계획을 먼저 작성한다.
   ```
   목표:
   수정할 파일:
   검증 방법:
   ```
2. **Read** — 대상 파일을 읽는다. 기존 구조·패턴·의존성을 확인한다.
3. **Edit** — 변경 범위를 최소화하여 수정한다.
4. **코드 작성** — 계획한 내용을 구현한다.
5. **/codex 검증** — 코드 작성 완료 후 `/codex`로 반드시 검증한다.

이 순서를 절대 건너뛰지 않는다.

---

## Superpowers + OMC 조율 워크플로우

작업 규모에 따라 아래 순서를 따른다.

### 소규모 (버그 수정, 간단한 수정)
```
Superpowers: systematic-debugging  →  직접 수정  →  verification-before-completion
```

### 중규모 (새 기능 추가)
```
Superpowers: brainstorming          →  요구사항 명확화
Superpowers: writing-plans          →  계획 수립
OMC: executor 에이전트              →  구현
Superpowers: verification-before-completion  →  완료 확인
```

### 대규모 (멀티파일, 아키텍처 변경)
```
Superpowers: brainstorming          →  아이디어 탐색
OMC: /oh-my-claudecode:ralplan      →  깊은 계획 수립
OMC: /oh-my-claudecode:ultrawork    →  병렬 구현
Superpowers: requesting-code-review →  리뷰
```

### 핵심 원칙
- **Superpowers 먼저** — 무엇을 할지 결정 (규율)
- **OMC는 실행 단계에서** — 복잡한 작업만 에이전트 위임
- **단순 작업에 OMC 남용 금지** — 에이전트 오버헤드가 더 클 수 있음
- **완료 주장 전 항상** `verification-before-completion` 실행

---

## Bash 명령어 승인 안내

Claude가 터미널 명령어(Bash)를 실행하기 전에 승인을 요청할 수 있다. 승인 창에 표시되는 명령어의 의미를 아래에서 확인한다.

### 자주 나오는 명령어 유형

| 명령어 예시 | 하는 일 | 승인 여부 |
|---|---|---|
| `ls`, `pwd`, `cat` | 파일/폴더 목록 조회, 내용 읽기 | 안전 — 승인 가능 |
| `python 파일.py` | 파이썬 파일 실행 | 안전 — 승인 가능 |
| `pip install 패키지` | 파이썬 패키지 설치 | 확인 후 승인 |
| `npm install` | Node.js 패키지 설치 | 확인 후 승인 |
| `git add`, `git commit` | 변경사항 저장 (커밋) | 내용 확인 후 승인 |
| `git push` | 원격 저장소에 업로드 | 반드시 확인 후 승인 |
| `rm 파일`, `rm -rf 폴더` | 파일/폴더 **영구 삭제** | **신중하게 확인** |
| `mv 파일 경로` | 파일 이동/이름 변경 | 경로 확인 후 승인 |
| `cp 파일 경로` | 파일 복사 | 안전 — 승인 가능 |
| `curl`, `wget` | 인터넷에서 파일 다운로드 | URL 확인 후 승인 |
| `docker run` | 도커 컨테이너 실행 | 내용 확인 후 승인 |

### 승인 판단 기준

- **되돌릴 수 없는 작업** (삭제, 원격 push 등) → 명령어를 꼼꼼히 읽고 승인
- **파일을 읽거나 조회만** 하는 작업 → 바로 승인해도 무방
- **모르는 명령어** → 승인 전에 Claude에게 "이 명령어가 무엇을 하는지 설명해줘"라고 먼저 물어본다

---

## 컨텍스트 윈도우 관리

### 80% 도달 시 — 작업 중단 전 저장
컨텍스트 윈도우 사용량이 80% 이상이 되면:
1. 현재 작업 중인 폴더에 `WORK_MEMORY.md` 파일을 UTF-8로 생성한다.
2. 다음 내용을 저장한다:
   - 현재 작업 목표 (Goal)
   - 완료된 작업 목록
   - 남은 작업 목록 (다음에 이어서 할 것)
   - 수정한 파일 목록
   - 주의사항 및 미결 사항
3. 사용자에게 "컨텍스트 한도에 근접하여 `WORK_MEMORY.md`에 작업 상태를 저장했습니다. 새 세션에서 이어서 진행해 주세요." 라고 알린다.

### 새 작업 시작 시 — memory 파일 확인
새로운 지시를 받으면, 작업을 시작하기 전에:
1. 현재 작업 폴더에 `WORK_MEMORY.md` 파일이 있는지 확인한다.
2. 파일이 있으면:
   - 내용을 읽고, 이전 작업 맥락을 파악한다.
   - 사용자에게 "이전 작업 기록(`WORK_MEMORY.md`)을 발견했습니다. 내용을 불러와 이어서 진행합니다." 라고 알린다.
   - 파일을 삭제한다.
3. 파일이 없으면 새 작업으로 정상 시작한다.
