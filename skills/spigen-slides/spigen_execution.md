# spigen_execution.md — Google Slides API 실행 코드
> Step 3 (기술 실행). 템플릿 복사, 표지 삽입, batchUpdate 실행.

## 방식 선택

| 브랜치 | 유형 | 실행 방식 |
|-------|-----|---------|
| **lib 방식** | 보고서·분석·회의자료·기타 | 브랜드 템플릿(표지·마감) + spigen_lib 내용 생성 |
| **템플릿 방식** | 제안서·시안 | 콘텐츠 템플릿 복사 → 슬라이드 선택 → 텍스트 교체 → (선택) lib 추가 |

lib 방식 → 아래 3-1~3-7 진행  
템플릿 방식 → 파일 하단 "템플릿 방식" 섹션으로 이동

---

## lib 방식

## Step 3: 기술 실행 (Google Slides API 직접 구현)

### 핵심 전략

| 슬라이드 | 방식 |
|---------|------|
| 표지 (slide 1) | Spigen 템플릿 인덱스 0 복사 → 텍스트 삽입 |
| 마지막 슬라이드 | Spigen 템플릿 인덱스 1, 2 (마지막 2페이지) |
| 내용 슬라이드 | `createSlide` (BLANK) → slides-grab-design 스타일 도형 직접 구현 |

**PPTX 변환 없음** — 텍스트·도형 모두 수정 가능한 네이티브 구글 슬라이드.

---

### 3-1. 날짜 확인

```bash
TODAY=$(date +%Y.%m.%d)
echo $TODAY
```

### 3-2. 템플릿 복사

```bash
COPY_RESULT=$(gws drive files copy \
  --params '{"fileId":"1R_z4ZKSbRSe5uQ-uWT6dnmBDTJ7M4yOjbGW_1UfxnEk"}' \
  --json "{\"name\":\"$TITLE\"}" 2>/dev/null)
NEW_ID=$(echo "$COPY_RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")
echo "복사된 ID: $NEW_ID"
```

### 3-3. 슬라이드 구조 조회 + slide_map 생성

```bash
gws slides presentations get \
  --params "{\"presentationId\":\"$NEW_ID\"}" 2>/dev/null > /tmp/spigen_prs.json
```

```python
# /tmp/parse_slides.py
import json

with open('/tmp/spigen_prs.json') as f:
    prs = json.load(f)

slide_map = {}
for i, slide in enumerate(prs['slides']):
    boxes = []
    for el in slide.get('pageElements', []):
        shape = el.get('shape', {})
        text_els = shape.get('text', {}).get('textElements', [])
        content = ''.join(t.get('textRun', {}).get('content', '') for t in text_els).strip()
        boxes.append({'oid': el['objectId'], 'text': content})
    slide_map[i] = {'slide_id': slide['objectId'], 'boxes': boxes}

with open('/tmp/spigen_map.json', 'w') as f:
    json.dump(slide_map, f, ensure_ascii=False, indent=2)

print(f'총 슬라이드 수: {len(prs["slides"])}')
```

```bash
python3 /tmp/parse_slides.py
```

### 3-4. 표지 텍스트 삽입

표지 박스 인덱스 (Spigen 템플릿 인덱스 0 기준):

| box | 위치 | 내용 |
|-----|------|------|
| box[0] | 제목 | `제목\n부제목` |
| box[1] | 부서·담당자 | `디자인부문ㅣ패키지디자인팀\n한원진 담당` |
| box[3] | 날짜·버전 | `YYYY.MM.DD\nV1.0` |

> **주의**: box[2]는 빈 박스 — 건너뜀. `existing_text`가 있는 박스만 `deleteText` 실행.

```python
# /tmp/fill_cover.py
import json

with open('/tmp/spigen_map.json') as f:
    m = json.load(f)

content = {
    0: {0: "제목\n부제목", 1: "디자인부문ㅣ패키지디자인팀\n한원진 담당", 3: "YYYY.MM.DD\nV1.0"}
}

reqs = []
for slide_idx, boxes_content in content.items():
    info = m[str(slide_idx)]
    for box_pos, text in boxes_content.items():
        if box_pos < len(info['boxes']):
            oid = info['boxes'][box_pos]['oid']
            existing = info['boxes'][box_pos].get('text', '')
            if existing:
                reqs.append({"deleteText": {"objectId": oid, "textRange": {"type": "ALL"}}})
            if text:
                reqs.append({"insertText": {"objectId": oid, "insertionIndex": 0, "text": text}})

print(json.dumps({"requests": reqs}))
```

```bash
gws slides presentations batchUpdate \
  --params "{\"presentationId\":\"$NEW_ID\"}" \
  --json "$(python3 /tmp/fill_cover.py 2>/dev/null)" 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print('표지 완료')"
```

---

### 3-5. 내용 슬라이드 생성 — 디자인 컴포넌트 라이브러리

> **코드 라이브러리**: `~/.claude/skills/spigen-slides/spigen_lib.py`
> 스크립트 작성 시 이 파일을 `/tmp/spigen_lib.py`로 복사 후 import 한다.

```bash
cp ~/.claude/skills/spigen-slides/spigen_lib.py /tmp/spigen_lib.py
```

#### 공통 헬퍼 (spigen_lib.py)

| 함수 | 역할 |
|-----|-----|
| `pt(v)` | pt → EMU 변환 (v × 12700) |
| `c255(r, g, b)` | RGB 0-255 → 0.0-1.0 변환 |
| `shape(oid, page, stype, x, y, w, h)` | 도형 생성 요청 |
| `fill(oid, fg, bg, wt)` | 도형 채우기·테두리 |
| `txtstyle(oid, color, size, bold)` | 텍스트 스타일 |
| `txt(oid, text)` | 텍스트 삽입 |

**상수**: `ORANGE` (#FF6900), `WHITE`, `BLACK`, `THEMES` (dark/light/warm)

#### 컴포넌트 참조

| 컴포넌트 | 함수 시그니처 | 기본 테마 |
|---------|------------|---------|
| A: slide-base | `slide_base(slide_oid, title_text, insert_index, reqs, theme='dark')` | dark |
| B: 3-col | `mk_3col(sid, cols, reqs, theme='light')` | light |
| C: flow | `mk_flow(sid, steps, cost_map, reqs, theme='dark')` | dark |
| D: text-block | `mk_text_block(sid, body_text, reqs, y_start=83, font_size=8.5, theme='light')` | light |
| E: section-divider | `mk_section_divider(slide_oid, num, title, insert_index, reqs)` | dark 고정 |
| F: contents | `mk_contents(slide_oid, sections, insert_index, reqs)` | dark 고정 |
| G: quote | `mk_quote(slide_oid, quote_text, insert_index, reqs, attribution="")` | dark 고정 |
| H: split-layout | `mk_split(sid, left, right, reqs, theme='light')` | light |
| I: title-accent | `mk_title_accent(sid, accent_part, rest_part, reqs, theme='light', subtitle="", y=44, font_size=22)` | light |
| J: 3col-cards | `mk_3col_cards(sid, cards, reqs, theme='light')` | light |
| K: toc | `mk_toc(slide_oid, items, insert_index, reqs, category="", year="", title_accent="Table Of", title_rest=" Content", description="")` | warm 고정 |
| L: split-cards | `mk_split_cards(sid, text_lines, cards, reqs, theme='light')` | light |

#### 사용 패턴

```python
from spigen_lib import *

reqs = []

# 슬라이드 1: 섹션 구분
mk_section_divider("sec_01", "01", "디자인 원칙", 1, reqs)

# 슬라이드 2: 3열 비교
slide_base("cont_01", "현황 분석", 2, reqs, theme='light')
mk_3col("cont_01", [
    {"label": "현재",   "items": ["항목 A", "항목 B"]},
    {"label": "문제점", "items": ["문제 X", "문제 Y"]},
    {"label": "도입 시 기대효과", "items": ["효과 P", "효과 Q"]},
], reqs, theme='light')

import json
with open('/tmp/content_req.json', 'w') as f:
    json.dump({"requests": reqs}, f)
```

### 3-6. batchUpdate 실행

모든 컴포넌트 요청을 하나의 리스트에 모아 실행:

```bash
gws slides presentations batchUpdate \
  --params "{\"presentationId\":\"$NEW_ID\"}" \
  --json "$(cat /tmp/content_req.json)" 2>/dev/null | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print('완료:', len(d.get('replies',[])), '항목')"
```

### 3-7. 결과 출력

```
프레젠테이션 생성 완료
제목: $TITLE
날짜: $TODAY / 버전: $VERSION
슬라이드 수: N장
URL: https://docs.google.com/presentation/d/$NEW_ID/edit
```

---

---

## 템플릿 방식 (제안서·시안)

콘텐츠 템플릿 ID: `1rh_2NNwM2CeZxFaZFfgoK3s1RAU2SyzZd794480hrVo`

### B-1. 날짜 확인

```bash
TODAY=$(date +%Y.%m.%d)
echo $TODAY
```

### B-2. 콘텐츠 템플릿 복사

```bash
COPY_RESULT=$(gws drive files copy \
  --params '{"fileId":"1rh_2NNwM2CeZxFaZFfgoK3s1RAU2SyzZd794480hrVo"}' \
  --json "{\"name\":\"$TITLE\"}" 2>/dev/null)
NEW_ID=$(echo "$COPY_RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")
echo "복사된 ID: $NEW_ID"
```

### B-3. 슬라이드 구조 조회

lib 방식 3-3과 동일: `parse_slides.py` 실행 → `/tmp/spigen_map.json` 생성.

### B-4. 슬라이드 선택 + 불필요 슬라이드 삭제

`slide_map`을 보고 유지할 슬라이드 인덱스를 결정 후 나머지 삭제:

```python
# /tmp/delete_slides.py
import json

with open('/tmp/spigen_map.json') as f:
    m = json.load(f)

KEEP = {0, 2, 5}  # 유지할 슬라이드 인덱스 — AI가 slide_map 보고 결정

reqs = []
for idx in sorted(m.keys(), key=int, reverse=True):
    if int(idx) not in KEEP:
        reqs.append({"deleteObject": {"objectId": m[idx]['slide_id']}})

with open('/tmp/delete_req.json', 'w') as f:
    json.dump({"requests": reqs}, f)
print(f"삭제 대상: {len(reqs)}장")
```

```bash
python3 /tmp/delete_slides.py
gws slides presentations batchUpdate \
  --params "{\"presentationId\":\"$NEW_ID\"}" \
  --json "$(cat /tmp/delete_req.json)" 2>/dev/null | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print('슬라이드 삭제 완료')"
```

### B-5. 텍스트 교체

남은 슬라이드의 placeholder를 실제 내용으로 교체:

```python
# /tmp/fill_template.py
import json

with open('/tmp/spigen_map.json') as f:
    m = json.load(f)

# {슬라이드_인덱스: {박스_위치: "교체할 텍스트"}} — AI가 구성
FILL = {
    0: {0: "제안서 제목", 1: "디자인부문ㅣ패키지디자인팀\n한원진 담당", 3: "2026.04.15\nV1.0"},
}

reqs = []
for slide_idx, boxes in FILL.items():
    info = m.get(str(slide_idx))
    if not info:
        continue
    for box_pos, text in boxes.items():
        if box_pos < len(info['boxes']):
            oid = info['boxes'][box_pos]['oid']
            existing = info['boxes'][box_pos].get('text', '')
            if existing:
                reqs.append({"deleteText": {"objectId": oid, "textRange": {"type": "ALL"}}})
            if text:
                reqs.append({"insertText": {"objectId": oid, "insertionIndex": 0, "text": text}})

with open('/tmp/fill_req.json', 'w') as f:
    json.dump({"requests": reqs}, f)
print(f"교체 요청: {len(reqs)}개")
```

```bash
python3 /tmp/fill_template.py
gws slides presentations batchUpdate \
  --params "{\"presentationId\":\"$NEW_ID\"}" \
  --json "$(cat /tmp/fill_req.json)" 2>/dev/null | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print('텍스트 교체 완료')"
```

### B-6. 추가 슬라이드 생성 (선택)

동적 슬라이드가 필요하면 lib 방식 3-5~3-6과 동일하게 spigen_lib 적용.

### B-7. 결과 출력

lib 방식 3-7과 동일.

## 오류 처리 (공통)


- 템플릿 복사 실패 → `gws auth status` 확인
- `deleteText` 400 오류 → 빈 박스에 deleteText 적용 금지. `existing_text`가 있는 박스에만 실행
- `createShape` 실패 → objectId 중복 확인 (슬라이드마다 고유 prefix 사용). **objectId는 최소 5자 이상** 필요 (예: `slide_01`, `sec_01` — `s01` 같은 4자 이하는 API 거부)
- Google Drive 인증 오류 → `gws auth status` 확인 후 재인증

## Done when

- 새 프레젠테이션 URL이 출력됐다.
- 표지는 Spigen 템플릿 그대로 (제목/부서/담당자/날짜/버전 정확히 입력됨).
- 내용 슬라이드는 유형별 테마가 올바르게 적용됐다: cover/section-divider → 검정 배경(`dark`), content/statistics → 흰 배경(`light`), 오렌지 상단 바는 테마 불문 공통.
- 마지막 슬라이드는 Spigen 템플릿 인덱스 1, 2 (마지막 2페이지).
- 모든 텍스트·도형이 구글 슬라이드에서 직접 수정 가능하다.
- Step 2에서 계획한 모든 슬라이드에 내용이 입력됐다.

---

## ccbot 방식 (CrossCheck Bot 전용)

> 캔버스: **1440 × 810pt** (Full HD 16:9)  
> 참조 템플릿: `1aVvlg0jQyZkcp-jbRqxQ1tQE4Zp0Pn6HsIcvfOY0hpk`  
> 색상: BG `#000000` / DARK `#0E0E0E` / ORNG `#FF6B1A` / WHT `#FFFFFF`

CrossCheck Bot 보고서 전용. 항상 다크 배경 + 오렌지 강조, 3슬라이드 고정 구성.

### C-1. 라이브러리 준비

```bash
cp ~/.claude/skills/spigen-slides/ccbot_lib.py /tmp/ccbot_lib.py
cp ~/.claude/skills/spigen-slides/spigen_lib.py /tmp/spigen_lib.py
```

### C-2. 함수 시그니처

| 컴포넌트 | 함수 | 설명 |
|---------|------|------|
| 현황 비교 | `ccbot_compare(sid, rows, callout, insert_index, reqs)` | 현행 vs 도입 후 비교표 (좌=취소선, 우=오렌지) |
| 프로세스 & 비용 | `ccbot_flow(sid, steps, table_rows, summary, insert_index, reqs)` | STEP 카드 + 비용 테이블 + callout 박스 |
| 로드맵 | `ccbot_roadmap(sid, phases, schedule, kpi, insert_index, reqs)` | Phase 카드 + SCHEDULE + KPI 박스 |

#### 데이터 형식

```python
# ccbot_compare
rows = [
    {"item": "인력 투입", "before": "크로스체크 2인", "after": "봇 자동 대조"},
    ...  # 최대 5행 권장 (ROW_Y0=230, ROW_H=80, ROW_GAP=9)
]
callout = "기존 2인 육안 대조를 1인 + 봇으로 전환, 건당 약 45초"

# ccbot_flow
steps = [
    {"num": "01", "name": "이미지 업로드", "service": "Google Chat API",
     "desc": "라벨 이미지 업로드", "cost": "무료", "paid": False},
    ...  # 6단계 고정 (CW=206, 6×(206+12)=1296, 마진 포함 1440 내)
]
table_rows = [("인프라", "과금 기준", "사용량", "월 비용"), ...]  # 첫 행=헤더
summary = {
    "label":    "장당 발생 비용",
    "price":    "≈ ₩133",
    "subtitle": "월 75장 기준 · 월 ₩10,000 이하",
    "note":     "배포시에만 발생 비용 별도",
}

# ccbot_roadmap
phases = [
    {"label":     "Phase 1 · 개발",
     "period":    "~ 2026. 08",
     "title":     "봇 개발 완료",
     "bullets":   ["9개 항목 자동 대조 로직 개발", ...],  # 최대 4개
     "current":   True,
     "note":      "← 현재 지점",
     "note_body": "개발 기간 동안 월 최대 5만 원 발생 가능"},
    ...  # 3 phases 권장 (PW=245, 3×(245+12)=771, 마진 포함 915 내)
]
schedule = [{"num": "1", "title": "봇 개발 완료", "when": "~ 8월"}, ...]  # 4행 권장
kpi = {
    "label": "파일럿 목표 · 연말 리뷰 지표",
    "text":  "OCR 정확도 95% 이상 · 월 실사용 비용 정확 산출",
}
```

### C-3. 사용 패턴

```python
import sys, json, subprocess
sys.path.insert(0, '/tmp')
from spigen_lib import *
from ccbot_lib import *

TMPL_ID = "1aVvlg0jQyZkcp-jbRqxQ1tQE4Zp0Pn6HsIcvfOY0hpk"
TITLE   = "CrossCheck Bot 보고서"

raw = subprocess.run(
    ["gws", "drive", "files", "copy",
     "--params", f'{{"fileId":"{TMPL_ID}"}}',
     "--json", f'{{"name":"{TITLE}"}}'],
    capture_output=True, text=True
).stdout
NEW_ID = json.loads(raw)["id"]
print(f"복사된 ID: {NEW_ID}")

reqs = []
ccbot_compare("s01_cmp", rows, callout, 1, reqs)
ccbot_flow("s02_flow", steps, table_rows, summary, 2, reqs)
ccbot_roadmap("s03_road", phases, schedule, kpi, 3, reqs)

with open('/tmp/ccbot_req.json', 'w', encoding='utf-8') as f:
    json.dump({"requests": reqs}, f, ensure_ascii=False)
```

```bash
gws slides presentations batchUpdate \
  --params "{\"presentationId\":\"$NEW_ID\"}" \
  --json "$(cat /tmp/ccbot_req.json)" 2>/dev/null | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print('완료:', len(d.get('replies',[])), '항목')"
echo "URL: https://docs.google.com/presentation/d/$NEW_ID/edit"
```

### C-4. 설계 규칙

| 규칙 | 상세 |
|-----|------|
| 투명 배경 | `propertyState: "NOT_RENDERED"` — 알파 0이 아님 |
| 반투명 오렌지 테두리 | `alpha=0.549` (원·날짜 배지) |
| 10% 오렌지 틴트 카드 | `_fill(oid, ORNG, 0.1)` (유료 STEP, Phase current, callout) |
| 취소선 텍스트 | `_style(oid, WHT, 16.5, strike=True)` |
| `"›"` 화살표 | 별도 TEXT_BOX, `_ghost()` 적용 + `_center()` |