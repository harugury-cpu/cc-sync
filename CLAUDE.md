# Global Claude Code Guidelines

# 코드 완료 검증 (절대 원칙)
코드를 작성하거나 수정한 후 완료를 주장하기 전에:
1. 반드시 테스트 또는 빌드를 실행한다
2. 실행 명령과 결과(통과/실패 수, 에러)를 응답에 포함한다
3. 테스트가 없는 프로젝트라면 빌드 성공 또는 수동 검증 결과를 명시한다
4. 이 단계 없이 "완료", "수정했습니다", "구현했습니다" 등의 표현 사용 금지

- 문제 해결을 위한 패치, 보안 금지. 근본적인 설계문제의 해결에 집중

# 직접 실행 원칙
도구로 직접 실행 가능한 작업(앱 재시작, 파일 복사, 명령 실행, 설치 등)은 사용자에게 지시하지 않고 바로 실행한다.
"~해줘요", "~켜줘요", "~확인해줘요" 등 사용자에게 액션을 요청하는 표현 금지.

# 코드 작성 위임 (codex)
- Claude는 **기획·설계·지시**를 담당하고, **코드 작성·수정·리뷰는 codex에 위임**한다 (토큰 절약). 모든 프로젝트에 적용.
- 위임 단위는 작게 쪼갠다 — codex에는 파일 수정만 시키고, **빌드·테스트 실행은 Claude가 직접** 한 줄 명령으로 (직접 실행 원칙 유지). codex에 빌드까지 한꺼번에 시켜 백그라운드로 늘어지게 하지 않는다.
- 마크다운 문서(기획안·브리프·메모리·SKILL.md 등 비코드 텍스트)는 Claude가 직접 작성해도 된다.
- codex 리뷰는 유지한다 — 없애면 버그를 놓쳐 빌드 실패·재시도로 오히려 느려진다. 단 리뷰 호출은 수정분만 저비용(effort low)으로 가볍게.

# 언어 설정
- **모든 응답은 한국어로 작성한다.**
- 코드, 파일 경로, 변수명, 명령어는 영어 그대로 유지한다.
- 에러 메시지, 설명, 주석, 커밋 메시지는 한국어로 작성한다.

# File Safety
- 파일/디렉토리 삭제 시 rm, rmdir 대신 항상 trash 명령을 사용합니다.
- trash를 먼저 시도하고, rm을 폴백으로 사용하지 않습니다.
- mv 사용 시 항상 -n 플래그를 사용합니다.
- 대상이 이미 존재하면 덮어쓰지 않고 멈춘 뒤 사용자에게 확인합니다.

# 인증/자격증명 보호 (데이터 손실 방지)
- gws 인증 문제를 디버깅할 때 keyring/file backend를 번갈아 가며 API smoke test하지 않는다. 잘못된 backend로 encrypted credentials를 읽으면 gws가 undecryptable로 판단해 `credentials.enc`를 삭제할 수 있다. 먼저 사용할 backend(`GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND`)를 하나로 고정하고, 그 backend로만 auth status와 API 호출을 확인한다.

# 수정 요청 시 완료 조건 사전 확인
수정(fix, 버그 수정, 기능 변경, 코드 수정) 요청을 받으면:
1. 실행 전에 완료 조건을 명시하고 사용자 승인을 받는다
2. 예: "완료 조건: [A, B, C]. 진행할까요?"
3. 생성·읽기·설명 요청은 이 단계를 생략한다
# graphify
- **graphify** (`~/.claude/skills/graphify/SKILL.md`) - any input to knowledge graph. Trigger: `/graphify`
When the user types `/graphify`, invoke the Skill tool with `skill: "graphify"` before doing anything else.

<!-- FABLIZE:BEGIN — run Opus like Fable (always-on router). Verified procedures only. Install/update: fablize setup.sh -->
## Operating mode (always on — auto-route by task signal)

Apply what the task signals; with no signal, baseline only. Read each pack only when needed. Routing: smallest matching discipline only, overlap only when genuinely multi-category, mimic observable behavior only.

- **[always]** Lead with the outcome · stay within the requested scope (no incidental refactors) · ground completion claims in this session's tool results · confirm before destructive or hard-to-reverse actions.
- **[2+ sequential stories]** Run `python3 /Users/user/.claude/plugins/fablize/scripts/goals.py`: create → next → checkpoint (with evidence) → final verification gate (no completion without `--verify-cmd` and `--verify-evidence`). Run from the repo root; state in `./.fablize/` (resume with `status`). Skip for single-step tasks.
- **[debugging / test failure / unknown cause / review]** Follow `/Users/user/.claude/plugins/fablize/packs/investigation-protocol.txt`: reproduce first → 3+ competing hypotheses → evidence per hypothesis → full causal chain → verify before/after → report rejected hypotheses.
- **[render/executable artifact: HTML, SVG, game, UI, chart]** Follow `/Users/user/.claude/plugins/fablize/packs/verification-grounding-pack.txt` grounding loop: run it in the real renderer → observe the output → fix what you see → re-run. A static check is not observation.
- **[hard or ambiguous task]** Adaptive thinking scales with difficulty automatically. To go higher, recommend `/effort xhigh` to the user. Depth (capability) cannot be raised: if stuck 2+ times or out-of-spec discovery is needed, report the limit honestly and escalate.
<!-- FABLIZE:END -->
