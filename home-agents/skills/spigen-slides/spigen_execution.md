# spigen-slides Execution Guide (v5)

## Step 3. 생성

승인된 구성을 그대로 Python 빌드 스크립트로 변환하고 실행한다.

---

## 빌드 스크립트 템플릿

```python
import subprocess, json, sys, shutil

# 빌더 복사
shutil.copy2("/Users/harugury/.agents/skills/spigen-slides/spigen_build.py",
             "/tmp/spigen_build.py")
sys.path.insert(0, "/tmp")
from spigen_build import SpigenBuilder

THEME = "light"  # 또는 "dark"
TITLE = "(PPT 제목)"

# 1. 새 프레젠테이션 생성
r = subprocess.run(
    ["gws", "slides", "presentations", "create",
     "--params", json.dumps({"title": TITLE})],
    capture_output=True, text=True)
prs = json.loads(r.stdout)
PID = prs["presentationId"]
first_slide = prs["slides"][0]["objectId"]
print(f"ID: {PID}")

b = SpigenBuilder(PID, THEME)

# 2. 기본 슬라이드 삭제
b.reqs.append({"deleteObject": {"objectId": first_slide}})

# 3. 슬라이드 추가 (승인된 구성대로)
b.cover("sl001", 0,
    title="(제목)",
    subtitle="(부제)",
    date="2026. 04.")

b.slide("sl002", 1,
    heading="(슬라이드 제목)",
    body="(본문 내용\n• bullet\n• bullet)")

b.two_col("sl003", 2,
    heading="(슬라이드 제목)",
    left_title="(왼쪽 제목)",
    left_body="(왼쪽 내용)",
    right_title="(오른쪽 제목)",
    right_body="(오른쪽 내용)")

# 4. 실행
ok = b.flush()
if ok:
    print(f"완료: https://docs.google.com/presentation/d/{PID}/edit")
else:
    print("생성 실패")
```

---

## 슬라이드 함수 레퍼런스

### `cover(oid, idx, title, subtitle, dept, name, date)`

| 파라미터 | 설명 | 기본값 |
|---------|------|--------|
| `oid` | 슬라이드 object ID (예: "sl001") | 필수 |
| `idx` | 삽입 위치 (0부터 시작) | 필수 |
| `title` | 메인 제목 | 필수 |
| `subtitle` | 부제 (생략 가능) | `""` |
| `dept` | 부서명 | `"디자인부문ㅣ패키지디자인팀"` |
| `name` | 담당자명 | `"한원진 담당"` |
| `date` | 날짜 | `"2026. 04."` |

### `slide(oid, idx, heading, body, body_size)`

| 파라미터 | 설명 | 기본값 |
|---------|------|--------|
| `oid` | 슬라이드 object ID | 필수 |
| `idx` | 삽입 위치 | 필수 |
| `heading` | 헤더 텍스트 | 필수 |
| `body` | 본문 텍스트 (`\n` 줄바꿈, `• ` bullet) | 필수 |
| `body_size` | 본문 폰트 크기 (pt) | `14` |

### `two_col(oid, idx, heading, left_title, left_body, right_title, right_body)`

| 파라미터 | 설명 |
|---------|------|
| `oid`, `idx` | 슬라이드 위치 |
| `heading` | 전체 헤더 |
| `left_title` | 왼쪽 패널 제목 (오렌지) |
| `left_body` | 왼쪽 본문 |
| `right_title` | 오른쪽 패널 제목 (오렌지) |
| `right_body` | 오른쪽 본문 |

---

## 실행 명령

```bash
python3 /tmp/build_<name>.py
```

FAIL 시: 오류 메시지 확인 → 해당 슬라이드 수정 → 재실행.

---

## 완료 보고

```
완료: https://docs.google.com/presentation/d/<ID>/edit
```
