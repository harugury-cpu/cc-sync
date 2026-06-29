---
name: GAS-vault
description: Use when user says "먼데이 자동화 정리해줘", "gas 정리해줘", "GAS 문서화해줘", or requests documenting a Monday.com Google Apps Script automation in the Obsidian vault.
---

# GAS-vault

## 목적
GAS(Google Apps Script) 파일을 분석해 Obsidian `monday-automation.md`에 섹션과 Mermaid 흐름도 토글을 자동 삽입한다.

## 트리거
- "먼데이 자동화 정리해줘"
- "gas 정리해줘"
- "GAS 문서화해줘"
- "자동화 노트 추가해줘"

---

## ⚠️ 핵심 제약사항

**iCloud 경로 파일은 Read/Write 도구 사용 금지 — 반드시 Bash만 사용**

| 방법 | 가능 여부 |
|---|---|
| `cat "파일경로"` (Bash) | ✅ |
| Python heredoc `python3 << 'PYEOF'` | ✅ |
| Read 도구 | ❌ 무한 대기 발생 |
| Write 도구 | ❌ 무한 대기 발생 |

---

## 대상 파일

```
/Users/harugury/Library/Mobile Documents/com~apple~CloudDocs/Obsidian Vault/work/Project/leading/monday-automation.md
```

---

## 실행 순서

### STEP 1: GAS 파일 경로 확인
사용자가 경로를 제공하지 않은 경우 요청:
> "정리할 GAS 파일 경로를 알려주세요. (예: ~/Desktop/my_script.gs)"

### STEP 2: GAS 파일 읽기 (Bash)
```bash
cat "<GAS_FILE_PATH>"
```

### STEP 3: 코드 분석 → Mermaid 다이어그램 생성

분석 항목:
- 자동화 목적 (무엇을 하는가)
- 주요 함수 호출 흐름
- 입력/출력 데이터
- 외부 연동 (Monday API, Slack, Google Sheets 등)
- 조건 분기 및 오류 처리

**Mermaid 작성 규칙:**
- `flowchart TD` 사용
- 노드 레이블은 **한국어 평어** (함수명·영문 금지)
  - ✅ `A[Monday 웹훅 수신]`
  - ❌ `A[handleWebhook()]`
- 분기·조건·오류 처리를 명확히 표현
- 이모지 포함 가능 (노드 설명에)

### STEP 4: monday-automation.md 현재 상태 파악
```bash
cat "/Users/harugury/Library/Mobile Documents/com~apple~CloudDocs/Obsidian Vault/work/Project/leading/monday-automation.md"
```

확인 항목:
- 마지막 섹션 번호 (`1-7.` → 다음은 `1-8.`)
- 어떤 그룹(1, 2, 3...)에 속하는지 판단
- 삽입 위치: `## 📅 Daily 언급 기록` 헤더 바로 앞

### STEP 5: 새 섹션 삽입 (Python heredoc)

**섹션 형식:**
```
### {번호}. {파일명}

**목적**: {한 줄 설명}
**트리거**: {실행 조건 — 예: Monday 웹훅, 시간 트리거, 수동 실행}
**주요 기능**:
- {기능1}
- {기능2}

> [!abstract]- {이모지} {한국어 제목} 흐름도
> ```mermaid
> flowchart TD
>     A[...] --> B[...]
> ```

---
```

**삽입 스크립트 (Python heredoc):**
```bash
python3 << 'PYEOF'
FILE = "/Users/harugury/Library/Mobile Documents/com~apple~CloudDocs/Obsidian Vault/work/Project/leading/monday-automation.md"

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

new_section = """\
### {번호}. {파일명}

**목적**: ...
**트리거**: ...
**주요 기능**:
- ...

> [!abstract]- {이모지} {제목} 흐름도
> ```mermaid
> flowchart TD
>     A[...] --> B[...]
> ```

---"""

# ## 📅 Daily 언급 기록 앞에 삽입
ANCHOR = "## 📅 Daily 언급 기록"
if ANCHOR in content:
    content = content.replace(ANCHOR, new_section + "\n\n" + ANCHOR, 1)
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"삽입 완료: {len(new_section)}자")
else:
    print("앵커 없음 — 파일 끝에 추가")
    with open(FILE, 'a', encoding='utf-8') as f:
        f.write("\n\n" + new_section)
PYEOF
```

### STEP 6: 검증
```bash
grep -n "abstract" "/Users/harugury/Library/Mobile Documents/com~apple~CloudDocs/Obsidian Vault/work/Project/leading/monday-automation.md" | tail -5
```
새 토글이 정상적으로 추가되었는지 확인.

---

## 완료 보고 형식

```
✅ GAS-vault 완료
- 섹션: {번호}. {파일명}
- 삽입 위치: {줄 번호}번째 줄
- 다이어그램 노드: {N}개
```

생성된 Mermaid 다이어그램 미리보기 포함.
