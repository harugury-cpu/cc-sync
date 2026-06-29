# Tools Reference

사용자가 Telegram/Codex/Claude를 통해 업무 자동화, 기록, 스케줄, 파일 전달을 맡길 때 참고하는 로컬 도구 카탈로그다. secret 원문은 이 파일에 기록하지 않는다.

## Cokacdir Telegram

**용도**: Telegram 대화에서 파일 전달, 스케줄 등록/조회/삭제, 현재 서버 시간 확인.

**주의**
- 파일을 만들었으면 사용자에게 `/down`을 안내하지 말고 cokacdir 파일 전송 명령을 사용한다.
- 스케줄 프롬프트는 사용자의 언어로 작성한다.
- 현재 대화 맥락을 이어야 하는 스케줄에만 `--session`을 붙인다.
- secret key 원문은 응답이나 장기 메모리에 불필요하게 노출하지 않는다.

## Skills

**경로**

```text
/Users/harugury/.agents/skills
```

**검증**

```bash
python3 /Users/harugury/.agents/scripts/validate-agent-skills.py
```

**업무 자동화 유지보수 스킬**

- `automation-ops-triage`: 구두 제보, 이상징후, 오류를 티켓화
- `automation-code-review`: Apps Script, GWS, HTML Service, Illustrator/Adobe 스크립트, API 연동 코드 점검
- `automation-change-safety`: 수정 전 완료조건, 실패케이스, 백업, 롤백, 검증방법 고정
- `automation-regression-check`: 수정 후 정상/문제/예외/중복/파일 산출물 검증
- `automation-incident-log`: 장애, 수동 복구, 재발 방지, 수정 이력 기록

## Obsidian

**Vault**

```text
/Users/harugury/Library/Mobile Documents/com~apple~CloudDocs/Obsidian Vault
```

**주요 brain 노트**

```text
brain/Skills.md
brain/Patterns.md
brain/Gotchas.md
brain/Memories.md
brain/Automation Changelog.md
```

**기록 원칙**
- 새 노트보다 기존 노트 append를 우선한다.
- 확인되지 않은 원인은 확정하지 않는다.
- secret, API token, credential 원문은 기록하지 않는다.
- 장애 기록은 비난이 아니라 재발 방지 중심으로 쓴다.

## Monday 업무기록

**용도**: 사용자가 파닥몬에게 “나 지금 뭐 했어”, “나 오늘 뭐했어” 형태로 업무기록을 말하면 Monday 보드에 입력한다.

**구분**
- 업무기록 입력 요청은 Obsidian `dump`가 아니다.
- 자동화 장애/개선/수정 요청은 `automation-*` 유지보수 스킬로 처리한다.
- 작업구분 또는 소요시간이 없으면 추측하지 말고 먼저 물어본다.

## 업무 자동화 코드

**대상**
- Google Apps Script
- Google Workspace/GWS 자동화
- Sheets/Docs/Drive/Gmail 연동
- Apps Script HTML Service
- 내부 HTML 서비스
- Illustrator/Adobe 스크립트
- Monday/API/파일 처리 자동화

**수정 전 확인**
- 운영 데이터 또는 원본 파일에 직접 쓰는가?
- 테스트 사본이 있는가?
- 날짜/시간대, 컬럼명, 파일명, 레이어명, 템플릿 구조에 의존하는가?
- 중복 실행 시 안전한가?
- 실패 로그가 남는가?

## Graphify

**용도**: 업무 자동화 코드의 함수, 파일, 트리거, 시트, 보드, 레이어, 템플릿, 출력물 관계를 그래프/다이어그램/Obsidian 구조 노트로 정리한다.

**설치**

```text
CLI wrapper: /Users/harugury/.local/bin/graphify
venv: /Users/harugury/.agents/venvs/graphify
package: graphifyy
```

**사용 기준**
- 자동화 구조도, 관계도, 다이어그램, Obsidian 구조 정리를 원할 때 사용한다.
- 일반 버그 검토, 수정 전 위험 점검은 `automation-code-review`와 `automation-change-safety`를 우선한다.
- `graphify install`은 기본 Graphify skill을 덮어쓸 수 있으므로 사용자 동의 없이 실행하지 않는다.

**대표 명령**

```bash
graphify extract <path>
graphify query "질문" --graph <path>/graphify-out/graph.json
graphify tree --graph <path>/graphify-out/graph.json
```

## Google Drive / Sheets / Docs

**용도**: 연결된 Google Drive 플러그인을 통해 파일 검색, 문서/시트 읽기, 요약, 편집을 수행한다.

**주의**
- 실제 셀/문서 수정 전 대상 파일과 범위를 명확히 확인한다.
- 운영 데이터 변경은 테스트 사본 또는 샘플 검증을 우선한다.
- 사용자가 업로드하거나 명시한 파일이 있으면 웹 검색보다 연결된 Drive 컨텍스트를 우선한다.
