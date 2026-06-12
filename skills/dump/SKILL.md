---
name: dump
description: Obsidian에 자유 발화를 분류·기록할 때 사용한다. "dump", "기록해줘", "저장해줘"에 반응한다. 또한 cokacdir 스케줄 회고 세션, "회고 대화", "오늘 하루 회고", "회고를 시작해줘" 문맥에서는 사용자의 모든 발화를 자동으로 dump 처리해 Daily 회고, 업무 노트, Brag Doc, Index, 사람/팀 맥락에 정리한다.
---

# Dump

자유 발화, 회고 답변, 업무 진행 내용, 결정, 이슈, 성과, 사람/팀 맥락을 Obsidian에 분류해 기록하는 스킬이다. 특히 스케줄로 시작된 Obsidian 회고 세션에서는 사용자의 모든 메시지를 별도 `/dump` 명령 없이 이 스킬의 입력으로 취급한다.

## 기준 경로

Obsidian Vault:

```text
/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Obsidian Vault/
```

Daily 회고:

```text
/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Obsidian Vault/회고일기/Daily/
```

업무 PDF 조회 기준:

```text
/Users/user/Library/Mobile Documents/com~apple~CloudDocs/0.work
```

## 자동 적용 조건

다음 중 하나에 해당하면 dump 모드로 처리한다.

- 사용자가 `dump`, `기록해줘`, `저장해줘`라고 말함
- 스케줄 프롬프트에 `회고 대화`, `오늘 하루 회고`, `회고를 시작해줘`, `dump 자동 적용`이 있음
- 저녁 회고 세션에서 사용자가 하루 업무, 감정, 결정, 완료/미완료, PDF 진행 내용을 답함

자동 모드에서는 사용자의 모든 발화를 다음 기준으로 분류하고 기록한다.

## 분류 기준

- `decision`: 결정, 합의, 방향 확정
- `project_update`: 프로젝트 진행 상황
- `task_update`: 할 일 완료/미완료/진행 중
- `incident`: 문제, 트러블, 재발 방지 필요 사항
- `win`: 성과, 칭찬, 기여, Brag 후보
- `people_context`: 사람/팀 관계, 협업 맥락
- `meeting`: 회의, 1:1, 논의 내용
- `learning`: 배운 것, 주의점, 패턴
- `pdf_work`: 오늘 업데이트한 PDF 파일별 진행 내용
- `general_note`: 그 외 업무 메모

## Workflow

### 1. 먼저 기존 노트 검색

새 노트를 만들기 전에 관련 기존 노트가 있는지 확인한다.

- 프로젝트 관련: `work/Project/`
- 사건/문제: `work/incidents/`
- 사람/팀: `org/`
- 성과: `perf/`
- 회고: `회고일기/Daily/`
- 패턴/주의점: `brain/`

기존 노트가 있으면 새 파일보다 append를 우선한다.

### 2. Daily 회고에 우선 기록

회고 세션의 기본 기록 대상은 오늘 Daily 파일이다.

파일명:

```text
회고일기/Daily/YYYY.MM.DD.md
```

발화 내용은 적절한 섹션에 넣는다.

- 완료한 일 → `### 완료`
- 진행 중 → `### 진행 중`
- 배운 점 → `## 배운 것 / 주의점`
- 사람/팀 맥락 → `## 사람 & 팀`
- 성과 → `## 성과 & 승리`
- 회의 → `## 회의 / 1:1`
- 문제 → `## 문제 / 트러블`
- 고민 → `## 고민`
- 나중에 볼 것 → `## 💡 나중에 검토할 것`
- 대기 → `## ⏳ 대기 (피드백/결과 대기)`
- 내일 할 일 → `## ✅ 다음에 할 일 > ### 내일`

### 3. PDF 작업 내용 기록

스케줄이 `/Users/user/Library/Mobile Documents/com~apple~CloudDocs/0.work`에서 오늘 수정/생성된 PDF를 리스팅한 경우, 사용자의 답변을 아래 섹션에 남긴다.

```markdown
## 오늘 업데이트한 PDF 파일
- `파일명.pdf` — 진행한 일: 사용자가 말한 작업 요약
  - 경로: `/absolute/path/to/file.pdf`
```

주의:

- `.pdf`만 대상이다.
- 같은 파일명으로 `.ai`, `.jpg`, `.png`가 있어도 기록 기준은 PDF의 수정 여부다.
- PDF 내용을 임의로 추정하지 말고, 사용자가 말한 진행 내용을 기준으로 기록한다.

### 4. 보조 노트 업데이트

필요한 경우에만 업데이트한다.

- `work/Index.md`: 프로젝트 상태나 새 프로젝트
- `perf/Brag Doc.md`: 명확한 성과, 기여, 칭찬
- `org/People & Context.md`: 사람/팀 맥락 변화
- `brain/Patterns.md`: 반복 가능한 업무 패턴
- `brain/Gotchas.md`: 재발 방지해야 할 실수/주의점
- `brain/Memories.md`: 다음 세션에 이어갈 중요한 맥락

### 5. 출력

처리 후 간결히 보고한다.

- 기록한 내용 요약
- 업데이트한 파일 경로
- 새로 만든 노트 경로
- 불확실해서 사용자 확인이 필요한 항목

## 중요 규칙

- iCloud 경로의 파일 읽기/쓰기는 bash/Python 기반 접근을 우선한다.
- 사용자가 말하지 않은 내용을 확정해서 쓰지 않는다.
- 회고 세션에서는 기록 누락을 줄이는 것이 우선이다.
- `정리해줘`가 나오면 dump를 마무리하고 `wrap-up` 스킬로 넘긴다.
