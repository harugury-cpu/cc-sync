# spigen_execution.md — Google Slides API 실행 코드
> Step 3 (기술 실행). 템플릿 복사, 표지 삽입, batchUpdate 실행.

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

## 오류 처리

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