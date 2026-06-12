---
name: wrap-up
description: Obsidian 회고 세션을 마무리할 때 사용한다. 사용자가 "정리해줘", "마무리", "랩업", "wrap up", "wrap-up"이라고 말하면 발동한다. 회고 세션에서 생성·수정된 Obsidian 노트, Daily 회고, Brag Doc, Index, 사람/프로젝트/업무 메모를 점검하고 누락된 기록과 개선점을 정리한다.
---

# Wrap Up

Obsidian 회고 세션을 끝낼 때 실행하는 마무리 점검 스킬이다. 특히 cokacdir 스케줄로 시작된 저녁 회고에서 사용자가 `정리해줘`라고 말하면 반드시 이 스킬을 적용한다.

## 기준 경로

Obsidian Vault:

```text
/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Obsidian Vault/
```

Daily 회고:

```text
/Users/user/Library/Mobile Documents/com~apple~CloudDocs/Obsidian Vault/회고일기/Daily/
```

## 중요 규칙

- iCloud 경로의 파일은 `Read`/`Write` 도구 대신 bash/Python 기반 파일 접근을 우선 사용한다.
- 사용자가 "정리해줘"라고 하면 단순 요약만 하지 말고, 이 스킬의 점검 절차를 실행한다.
- 같은 세션에서 `dump` 스킬로 처리된 사용자 발화, 결정, 진행 내용, PDF 작업 내역을 Daily 회고에 반영한다.
- 확정되지 않은 내용은 확정 표현으로 쓰지 말고, "확인 필요" 또는 "추정"으로 표시한다.

## Workflow

### 1. 세션에서 처리한 내용 확인

다음을 확인한다.

- 오늘 Daily 파일 생성/수정 여부
- 사용자의 회고 답변 중 기록해야 할 결정, 진행 상황, 이슈, 배운 점
- `dump` 스킬로 분류된 업무 메모
- 오늘 업데이트한 PDF 파일과 파일별 진행 내용
- 생성·수정된 Obsidian 노트 경로
- `perf/Brag Doc.md`에 남길 성과 후보

### 2. Daily 회고 품질 점검

오늘 Daily 파일에 아래 섹션이 있는지 확인하고, 누락 시 추가한다.

```markdown
## 오늘의 일
### 📋 할 일
### 완료
### 진행 중
## 배운 것 / 주의점
## 사람 & 팀
## 성과 & 승리
## 회의 / 1:1
## 문제 / 트러블
## 고민
## 오늘 업데이트한 PDF 파일
## 💡 나중에 검토할 것
## ⏳ 대기 (피드백/결과 대기)
## ✅ 다음에 할 일
### 내일
### ✔ 완료된 항목
## 📝 커밋 기록
```

### 3. 오늘 업데이트한 PDF 파일 정리

회고 스케줄이 제공한 PDF 목록과 사용자 답변을 바탕으로 다음 형식으로 남긴다.

```markdown
## 오늘 업데이트한 PDF 파일
- `파일명.pdf` — 진행한 일: 사용자가 말한 작업 요약
  - 경로: `/absolute/path/to/file.pdf`
```

주의:

- 기준 폴더는 `/Users/user/Library/Mobile Documents/com~apple~CloudDocs/0.work`다.
- `.pdf`만 기록한다.
- 같은 파일명으로 `.ai`, `.jpg`, `.png`가 있어도 PDF 업데이트만 기록한다.

### 4. Index / Brag / People 점검

필요할 때만 업데이트한다.

- `work/Index.md`: 새 프로젝트나 진행 상태 변경이 있으면 반영
- `perf/Brag Doc.md`: 성과나 칭찬, 명확한 기여가 있으면 후보로 추가
- `org/People & Context.md`: 사람/팀 맥락 변화가 있으면 추가
- `brain/Patterns.md`, `brain/Gotchas.md`, `brain/Memories.md`: 반복 패턴·주의점·맥락이 생기면 업데이트

### 5. 내일 파일 이관 확인

저녁 회고 스케줄에서는 "정리해줘" 이후 내일 Daily 파일을 만들거나 갱신한다.

- 오늘 미완료 `- [ ]` 항목
- `✅ 다음에 할 일`
- `⏳ 대기`

위 항목이 내일 Daily의 `📋 할 일` 또는 `⏳ 대기`로 이관됐는지 확인한다.

### 6. 최종 보고

간결하게 보고한다.

- 오늘 Daily 업데이트 여부
- 오늘 업데이트한 PDF 파일 기록 여부
- Brag/Index/People 등 추가 업데이트 여부
- 내일 파일 생성/갱신 여부
- 확인이 필요한 항목
