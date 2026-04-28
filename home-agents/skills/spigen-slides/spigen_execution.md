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

### 3-1.a 테마 확인

```bash
THEME=${THEME:-dark}   # dark | light
echo "theme=$THEME"
```

> **테마 선택 원칙:**
> - **KPI / 성과 / 실적 보고서 → light 고정 (dark 사용 불가)**
> - 상세 세부 보고서 (수치·근거 중심, KPI 제외) → light 우선
> - 제안서, 발표자료, 임원 보고 등 임팩트 중심 → dark

---

### 3-1.b KPI 보고서 양식 고정 규칙

KPI 내용이 포함된 보고서는 아래 두 슬라이드 포맷을 **반드시 세트로** 사용한다. (양식 고정)

| 슬라이드 용도 | 함수 | 출처 |
|-------------|------|------|
| KPI 진행 현황 수치 (목표·실적·달성률 요약) | `mk_kpi_status_light()` | `guide_kpi_status_light` |
| 핵심과제 상세 (연관 KPI·핵심과제·실행 계획·나의 역할) | `mk_kpi_dense_table()` | `light_dense_table_01` |

적용 조건:
- KPI 수치 요약이 필요한 경우 → `mk_kpi_status_light()` 필수
- KPI 항목별 핵심과제·실행 계획·나의 역할이 포함된 경우 → `mk_kpi_dense_table()` 필수
- **두 함수는 세트** — 한쪽만 단독 사용 불가
- 이 함수들 사용 시 **light 테마 고정** (`lib.set_theme('light')`)
- 커스텀 카드/그리드로 대체 불가 — 임의 대체 금지

### 3-2. 템플릿 복사

템플릿 ID (테마별):

| 테마 | 템플릿 ID |
|------|-----------|
| dark | `1R_z4ZKSbRSe5uQ-uWT6dnmBDTJ7M4yOjbGW_1UfxnEk` |
| light | `1gPAlxb421I_IaVIG0y9xGTV0qLxiF3PIgLVFODq30tc` |

```bash
# THEME 변수에 따라 자동 선택
if [ "$THEME" = "light" ]; then
  TMPL_ID="1gPAlxb421I_IaVIG0y9xGTV0qLxiF3PIgLVFODq30tc"
else
  TMPL_ID="1R_z4ZKSbRSe5uQ-uWT6dnmBDTJ7M4yOjbGW_1UfxnEk"
fi

COPY_RESULT=$(gws drive files copy \
  --params "{\"fileId\":\"$TMPL_ID\"}" \
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

> **표지 source of truth**: 테마별 템플릿 1페이지  
> 새 세부 가이드 표지와 동일한 구조를 기본 cover 로 사용한다.

표지 박스 인덱스 (슬라이드 인덱스 0 기준) — **테마마다 다름**:

**dark 템플릿** (`1R_z4ZKSbRSe5uQ-uWT6dnmBDTJ7M4yOjbGW_1UfxnEk`):

| box | 위치 | 내용 |
|-----|------|------|
| box[0] | 제목 | `제목\n부제목` |
| box[1] | 부서·담당자 | `디자인부문ㅣ패키지디자인팀\n한원진 담당` |
| box[3] | 날짜·버전 | `YYYY.MM.DD\nV1.0` |

> **주의**: box[2]는 빈 박스 — 건너뜀.

**light 템플릿** (`1gPAlxb421I_IaVIG0y9xGTV0qLxiF3PIgLVFODq30tc`):

| box | 위치 | 내용 |
|-----|------|------|
| box[0] | 제목 | `제목\n부제목` |
| box[1] | 부서·담당자 | `디자인부문ㅣ패키지디자인팀\n한원진 담당` |
| box[2] | 날짜·버전 | `YYYY.MM.DD\nV1.0` |

> `existing_text`가 있는 박스만 `deleteText` 실행.

표지 생성 원칙:

```txt
1. 커스텀 cover를 새로 그리지 않는다.
2. 기본은 템플릿 cover 복사 + 텍스트 교체다.
3. 제목 / 부서·담당자 / 날짜·버전의 3영역 구조를 유지한다.
4. 다른 덱에서 임시로 만든 커버를 source 로 삼지 않는다.
```

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

> **코드 라이브러리**: `~/.agents/skills/spigen-slides/spigen_lib.py`
> 스크립트 작성 시 이 파일을 `/tmp/spigen_lib.py`로 복사 후 import 한다.

```bash
cp ~/.agents/skills/spigen-slides/spigen_lib.py /tmp/spigen_lib.py
```

테마 선택이 필요한 경우:

```python
import spigen_lib as lib
lib.set_theme(THEME)   # 'dark' | 'light'
```

원칙:

- theme 값은 deck 생성 시작 전에 한 번만 정한다.
- 생성 중간에 dark / light 를 섞지 않는다.
- 테마를 바꿔도 레이아웃/spacing/validator 규칙은 유지된다.

preview / 샘플 덱 / 실험 덱의 첫 슬라이드는 임시 텍스트박스로 직접 그리지 않고 아래 helper 를 사용한다.

```python
lib.mk_cover(
    'slide_cover',
    title='메인 제목',
    subtitle='부제목',
    department='디자인부문ㅣ패키지디자인팀',
    owner='한원진 담당',
    date_text='2026.04.25',
    version='V1.0',
    insert_index=0,
    reqs=reqs,
)
```

#### 공통 헬퍼 (spigen_lib.py)

| 함수 | 역할 |
|-----|-----|
| `pt(v)` | pt → EMU 변환 (v × 12700) |
| `c255(r, g, b)` | RGB 0-255 → 0.0-1.0 변환 |
| `shape(oid, page, stype, x, y, w, h)` | 도형 생성 요청 |
| `line(oid, page, x1, y1, x2, y2, category)` | native line / connector 생성 |
| `fill(oid, fg, bg, wt)` | 도형 채우기·테두리 |
| `linestyle(oid, color, weight, start_arrow, end_arrow)` | line 색·두께·화살표 |
| `connector(reqs, sid, oid, x1, y1, x2, y2, ...)` | 의미 있는 흐름/관계선 생성 |
| `_divider(reqs, sid, oid, x, y, w, h, color)` | 정적 divider를 thin rectangle으로 생성 |
| `txtstyle(oid, color, size, bold)` | 텍스트 스타일 |
| `txt(oid, text)` | 텍스트 삽입 |

**상수**: `BG`, `SURFACE`, `BORDER`, `ORANGE` (#FF6B1A), `TEXT`, `TEXT_DIM`, `TEXT_FAINT`

폰트 최소값:

```txt
모든 생성 텍스트는 7pt 이상으로 clamp 한다.
```

선 사용 원칙:

```txt
connector / 화살표 / 분기선 → line() / connector()
표 구분선 / 카드 separator / 장식 바 → _divider() 또는 thin rectangle
```

overflow / bounds 검증 원칙:

```txt
모든 요소는 720 × 405pt 캔버스 안에 있어야 한다.
내용 컴포넌트는 가급적 y≈128 ~ 381 영역 안에서 끝나야 한다.
```

검증 식:

```txt
x >= 0
y >= 0
x + width <= 720
y + height <= 405
```

실패 시 대응 (내용이 레이아웃을 초과할 때):

```txt
원칙: 내용을 잘라 레이아웃에 맞추지 않는다. 레이아웃을 교체하거나 페이지를 분리한다.

텍스트가 카드 안에서 잘리거나 "…"이 생기는 상황 → 레이아웃 선택 실패 신호
→ 더 큰 컴포넌트(text-block, split-layout 등)로 교체

카드 내용이 넘침 (항목당 줄 수 초과)
→ 카드 수를 줄이고 레이아웃을 넓히거나, 페이지 분리

슬라이드 한 장에 담기지 않음
→ 페이지 분리. 억지로 한 장에 압축하지 않는다

항목 3개 각각 내용이 많음
→ mk_3col_cards() 대신 mk_split() 또는 mk_text_block()으로 교체

최후 수단으로 카드/블록 높이 재계산 및 내부 여백 재분배를 시도하되,
그래도 담기지 않으면 반드시 레이아웃 교체 또는 페이지 분리로 해결한다.
```

카드 내부 여백 원칙:

```txt
텍스트 그룹 높이보다 상·하 padding 이 더 작아지는 tight 상태에서는
텍스트 묶음을 카드 중앙 기준으로 다시 배치한다.
```

불렛 검증 원칙:

```txt
불렛은 첫 줄 텍스트와 같은 세로 행에 정렬되어야 한다.
불렛과 텍스트가 어긋난 상태로 납품하지 않는다.
```

선택 원칙:

```txt
card component = bullet 제거
bullet 필요 = wide text block 에서만 native paragraph bullets 우선
```

최신 실행 원칙:

```txt
단순 font floor 적용으로 끝내지 않는다.
작은 / 중간 텍스트 계층은 type scale remap 으로 같이 조정한다.
```

현재 기준:

```txt
5.5 → 7
6.0 → 7.5
6.5 → 8
7.0 → 7.5
8.0 → 9.5
8.5 → 10
9.0 → 10.5
11.0 → 12.5
13.0 → 14.5
```

flow 카드 실행 규칙:

```txt
step label / title / service 가 multiline 이 되면
카드 높이와 내부 간격을 같이 다시 계산한다.
텍스트만 커지고 카드 높이가 그대로인 상태로 납품하지 않는다.
```

structure 페이지 실행 규칙:

```txt
native BENT connector 를 기본값으로 쓰지 않는다.
필요 시 manual orthogonal routing 또는 connector 최소화 방향을 사용한다.
모든 관계를 선으로 설명하려 하지 않는다.
```

mapping 페이지 실행 규칙:

```txt
divider / 기준선 / bar 는 카드 내부에만 존재해야 한다.
카드 밖 gutter 영역에 남아 있으면 FAIL 이다.
```

레이아웃 제한 원칙 (강제):

```txt
[불필요한 선 금지]
- 카드 밖에 구분선 / 데코 bar / separator line 삽입 금지
- 텍스트 블록 사이에 장식용 선 추가 금지
- connector 는 흐름·관계가 명확히 존재할 때만 사용 — 단순 배치 목적 사용 금지
- _divider() / thin rectangle 은 카드 내부에서만 호출

[불필요한 여백 금지]
- 공간을 채우기 위한 빈 rect / 투명 shape 삽입 금지
- top / bottom 여백을 도형으로 추가하는 것 금지
- 내용이 적으면 레이아웃을 단순화한다 — 빈 공간을 도형으로 채우지 않는다
- 슬라이드 내 요소 수는 내용이 요구하는 최솟값으로 유지한다
```

강조 row / 강조 card 실행 규칙:

```txt
오렌지 보더 / 오렌지 라인이 있는 강조 요소는
반드시 BRING_TO_FRONT 로 일반 요소보다 위에 와야 한다.
```

> 현재 `spigen_lib.py`는 사용자가 만든 콘텐츠 템플릿 기준으로 교체됐다.  
> `theme` 인자는 구버전 스니펫 호환용으로만 남아 있으며, 신규 출력은 모두 다크 템플릿 스타일이다.

#### 컴포넌트 참조

| 컴포넌트 | 함수 시그니처 | 기본 테마 |
|---------|------------|---------|
| A: slide-base | `slide_base(slide_oid, title_text, insert_index, reqs, theme='dark')` | dark |
| B: 3-col | `mk_3col(sid, cols, reqs, theme='dark')` | dark |
| C: flow | `mk_flow(sid, steps, cost_map, reqs, theme='dark')` | dark |
| C-2: flow-focus | `mk_flow_focus(sid, steps, reqs, x=54, y=136, w=612, cols=3)` | dark |
| D: text-block | `mk_text_block(sid, body_text, reqs, y_start=128, font_size=10, theme='dark')` | dark |
| E: section-divider | `mk_section_divider(slide_oid, num, title, insert_index, reqs)` | dark 고정 |
| F: contents | `mk_contents(slide_oid, sections, insert_index, reqs)` | dark 고정 |
| G: quote | `mk_quote(slide_oid, quote_text, insert_index, reqs, attribution="")` | dark 고정 |
| H: split-layout | `mk_split(sid, left, right, reqs, theme='dark')` | dark |
| I: title-accent | `mk_title_accent(sid, accent_part, rest_part, reqs, theme='dark', subtitle="", y=54, font_size=22)` | dark |
| J: 3col-cards | `mk_3col_cards(sid, cards, reqs, theme='dark')` | dark |
| K: toc | `mk_toc(slide_oid, items, insert_index, reqs, category="", year="", title_accent="Table Of", title_rest=" Content", description="")` | dark |
| L: split-cards | `mk_split_cards(sid, text_lines, cards, reqs, theme='dark')` | dark |
| M: arch-layers | `mk_arch_layers(sid, layers, reqs, eyebrow="", title="")` | dark |
| N: decision-tree | `mk_decision_tree(sid, nodes, reqs, eyebrow="", title="")` | dark |
| O: swimlane-mapping | `mk_swimlane_mapping(sid, rows, reqs, eyebrow="", title="")` | dark |
| P: arch-orchestrator | `mk_arch_orchestrator(sid, nodes, reqs, eyebrow="", title="", x=54, y=146)` | dark |
| Q: conclusion-detail | `mk_conclusion_detail(sid, conclusion, details, reqs, eyebrow="SUMMARY", title="요약")` | dark |
| R: rule-grid | `mk_rule_grid(sid, cards, reqs, x=M, y=CONTENT_TOP, w=None, cols=2, gap_x=12, gap_y=12, card_h=96)` | dark |
| S: kpi-dashboard | `mk_kpi_dashboard(sid, kpis, reqs, y=128)` | dark |
| T: bar-chart | `mk_bar_chart(sid, bars, reqs, x=M, y=144, w=420, h=150)` | dark |
| U: report-table | `mk_report_table(sid, rows, reqs, x=M, y=138, w=648)` | dark |
| V: callout-message | `mk_callout_message(sid, message, reqs, sub="", x=84, y=148, w=552, h=126)` | dark |
| W: metric-bar-summary | `mk_metric_bar_summary(sid, metric, bars, reqs)` | dark |
| X: kpi-status-light | `mk_kpi_status_light(sid, reqs, year="24", period="상반기", kpi_rows=[], def_rows=[], y=99)` | **light 전용·KPI 고정 양식 (슬라이드 6)** |
| Y: kpi-dense-table | `mk_kpi_dense_table(sid, rows, reqs, y=96)` · rows 키: `kpi/task/plan/role` | **light 전용·KPI 고정 양식 (슬라이드 7)** |

#### 사용 패턴

```python
from spigen_lib import *

reqs = []

# 슬라이드 1: 섹션 구분
mk_section_divider("sec_01", "01", "디자인 원칙", 1, reqs)

# 슬라이드 2: 3열 비교
slide_base("cont_01", "현황 분석", 2, reqs, page_label="PAGE 01 · 현황 분석", page_no=1, total=3)
mk_3col("cont_01", [
    {"label": "현재", "title": "현재", "items": ["항목 A", "항목 B"]},
    {"label": "개선", "title": "도입 후", "items": ["효과 P", "효과 Q"], "hot": True},
    {"label": "기대효과", "title": "결과", "items": ["지표 개선", "비용 관리"]},
], reqs)

import json
with open('/tmp/content_req.json', 'w') as f:
    json.dump({"requests": reqs}, f)
```

#### 신규 권장 패턴: shared spec → preview / Slides 동시 생성

```python
from spigen_models import SlideSpec, ComponentSpec
import spigen_preview as prev
import spigen_lib as lib
import json

slides = [
    SlideSpec(
        slide_id="slide_decision",
        label="SLIDE 01 — DECISION",
        eyebrow="PROCESS",
        title="자동 선택 실패 시 수동 폴백",
        page_no=1,
        components=[
            ComponentSpec(
                type="decision-tree",
                props={
                    "nodes": {
                        "input": "CSV 입력",
                        "decision": "자동 선택 가능?",
                        "yes": "project.json 자동 선택",
                        "no": "리스트박스 수동 폴백",
                        "output": "PDF 출력",
                    }
                },
            )
        ],
    )
]

# 1) preview
prev.send_specs("/tmp/spigen_preview.html", slides)

# 2) Google Slides requests
reqs = []
for idx, slide in enumerate(slides):
    lib.slide_base(slide.slide_id, slide.title, idx, reqs, page_no=idx + 1, total=len(slides))
    for component in slide.components:
        lib.render_component_spec(slide.slide_id, component, reqs, eyebrow=slide.eyebrow, title=slide.title)

with open("/tmp/content_req.json", "w", encoding="utf-8") as f:
    json.dump({"requests": reqs}, f, ensure_ascii=False)
```

원칙:

```txt
HTML을 먼저 만들고 Slides로 변환하지 않는다.
SlideSpec / ComponentSpec을 먼저 만든다.
preview HTML과 Google Slides는 같은 spec을 각각 렌더한다.
```

### 3-6. batchUpdate 실행

모든 컴포넌트 요청을 하나의 리스트에 모아 실행:

```bash
gws slides presentations batchUpdate \
  --params "{\"presentationId\":\"$NEW_ID\"}" \
  --json "$(cat /tmp/content_req.json)" 2>/dev/null | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print('완료:', len(d.get('replies',[])), '항목')"
```


### 3-7. 템플릿 잔여 슬라이드 삭제

템플릿 복사 시 원본 슬라이드가 뒤에 남는다. batchUpdate 완료 직후 삭제한다.
`ex_` 또는 `slide_` 로 시작하지 않는 objectId가 잔여 슬라이드다.

```python
import subprocess, json

r = subprocess.run(
    ["gws", "slides", "presentations", "get",
     "--params", json.dumps({"presentationId": NEW_ID})],
    capture_output=True, text=True
)
slides = json.loads(r.stdout).get("slides", [])

# 우리가 만든 슬라이드 이외는 모두 삭제
OUR_PREFIXES = ("ex_", "slide_")
leftover = [s["objectId"] for s in slides
            if not any(s["objectId"].startswith(p) for p in OUR_PREFIXES)]

if leftover:
    reqs = [{"deleteObject": {"objectId": oid}} for oid in leftover]
    subprocess.run(
        ["gws", "slides", "presentations", "batchUpdate",
         "--params", json.dumps({"presentationId": NEW_ID}),
         "--json", json.dumps({"requests": reqs})],
        capture_output=True
    )
    print(f"템플릿 잔여 {len(leftover)}장 삭제 완료")
```

> objectId prefix 규칙: `render_slide_spec()` 호출 시 `slide_id`에 `ex_` 또는 `slide_` 로 시작하는 값을 사용한다.

---

### 3-8. 결과 출력

```
프레젠테이션 생성 완료
제목: $TITLE
날짜: $TODAY / 버전: $VERSION
슬라이드 수: N장
URL: https://docs.google.com/presentation/d/$NEW_ID/edit
```


---

### 3-9. 생성 후 이미지 검수 (getThumbnail)

슬라이드 생성 완료 후, 기획자·디자이너 서브에이전트 spawn 전에 실행한다.
API 텍스트 데이터만으로 잡을 수 없는 **시각적 문제(오버플로·겹침·오렌지 과다)를 이미지로 직접 확인**한다.

```bash
# 슬라이드 N번 썸네일 URL 조회 (1-indexed)
PAGE_IDX=1  # 0-indexed → 1번 슬라이드 = 0
gws slides presentations pages getThumbnail \
  --params "{"presentationId":"$NEW_ID", "pageObjectId":"$(gws slides presentations get \
    --params "{\"presentationId\":\"$NEW_ID\"}" 2>/dev/null | \
    python3 -c "import json,sys; slides=json.load(sys.stdin)['slides']; print(slides[$PAGE_IDX]['objectId'])")}" \
  2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin)['contentUrl'])"
```

실용적 사용 패턴 (전체 슬라이드 URL 일괄 조회):

```bash
python3 << 'EOF'
import subprocess, json

result = subprocess.run(
    ["gws", "slides", "presentations", "get",
     "--params", f'{{"presentationId":"{NEW_ID}"}}'],
    capture_output=True, text=True
)
slides = json.loads(result.stdout)["slides"]

for i, slide in enumerate(slides):
    thumb = subprocess.run(
        ["gws", "slides", "presentations", "pages", "getThumbnail",
         "--params", json.dumps({"presentationId": NEW_ID, "pageObjectId": slide["objectId"]})],
        capture_output=True, text=True
    )
    url = json.loads(thumb.stdout).get("contentUrl", "")
    print(f"슬라이드 {i+1}: {url}")
EOF
```

Claude가 각 URL을 읽어 시각적으로 확인하는 항목:
- 텍스트가 도형 밖으로 넘치지 않는가
- 요소 간 겹침이 없는가
- 오렌지 강조가 슬라이드당 3개 이하인가
- 전체 레이아웃이 균형 있는가

썸네일 URL은 발급 후 **1시간** 유효. 검수 즉시 진행한다.

---

### 3-10. 강제 postgen hook

이미지 검수 직후, 아래 훅을 **반드시** 실행한다.

```bash
python3 /Users/harugury/.agents/skills/spigen-slides/spigen_postgen_hook.py "$NEW_ID" \
  --audience "$Q2" \
  --purpose "$Q4" \
  --strict
```

strict 결과 해석:

- `VERIFY_FAILED` → 생성 실패, 코드 수정 후 같은 presentation ID에 반영
- `SUBAGENT_REVIEWS_PENDING` → 정상, 이제 서브에이전트 3종 검수 진행

생성 완료로 인정되는 최소 산출물:

- `review_manifest.json`
- `verify.txt`
- `thumbnails/*.png`

위 3종이 없으면 **완료 보고 금지**.

---

### ⛔ 3-11. 검수 FAIL 시 인플레이스 수정 — 새 presentation 생성 절대 금지

검수 FAIL(기획자 / 디자이너 / 대상 어느 하나라도) 시 아래를 엄수한다.

**절대 금지 (예외 없음):**
- `gws drive files copy` 재실행으로 새 파일 생성
- 새 `presentationId` 로 URL 교체
- 이미 공유된 링크를 버리는 행위

**유일한 수정 경로: `spigen_inplace_update.py`**

```bash
python3 /Users/harugury/.agents/skills/spigen-slides/spigen_inplace_update.py \
  "$NEW_ID" \
  /path/to/updated_requests.json \
  --prefix slide_
```

수정 반영 후 반드시 Step A → Step B → 서브에이전트 검수 전 과정 재실행.

**3회 이상 FAIL 반복 시:**
- 새 파일을 만들지 않는다.
- 아웃라인(1-4) 기획 품질 게이트(1-4.a)로 돌아가 근본 원인을 확인한다.
- "데이터 없는 주장" / "컴포넌트 선택 근거 불명확" / "내러티브 단절" 중 무엇이 원인인지 먼저 진단한다.

---

---

## 템플릿 방식 (제안서·시안)

콘텐츠 템플릿 ID: `1rh_2NNwM2CeZxFaZFfgoK3s1RAU2SyzZd794480hrVo`

### 템플릿 우선 원칙

제안서·시안·CrossCheck Bot·Google Chat Bot류 자료는 이 콘텐츠 템플릿을 먼저 복사한다.  
템플릿 1~6번은 완성형 디자인이므로, 가능하면 **슬라이드 복사/유지 + 텍스트 교체**로 만든다.

| 템플릿 번호 | 용도 | 대표 objectId |
|------------|------|---------------|
| 1 | Cover | `g9001df85b1_0_0` |
| 2 | Section Divider | `sl_sec01` |
| 3 | 현행 vs 도입 후 비교 | `g3e018b790e1_0_0` |
| 4 | 일정 · 목표 · 확장 계획 | `g3e018b790e1_0_197` |
| 5 | 프로세스 & 비용 | `g3e018b790e1_0_73` |
| 6 | Quote / Closing | `sl_qte1` |

권장 구성:

```
Cover → Section Divider → 현행/도입 후 비교 → 일정/목표/확장 계획 → 프로세스/비용 → Quote
```

3장 압축 보고서가 필요하면 3~5번 유형만 사용한다.  
완전히 새로운 내용 슬라이드가 필요할 때만 `ccbot_lib.py` 또는 `spigen_lib.py`로 추가 생성한다.

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

> **권장**: box index(`0`, `1`, `3` 등)로 채우지 말고, `slide_map`에서 placeholder 텍스트 또는 objectId 역할을 먼저 식별해
> `{"cover_title": "...", "cover_team": "...", "cover_meta": "..."}` 같은 의미 키로 매핑한 뒤 교체한다.
> 템플릿 수정 시 box 순서는 쉽게 바뀌지만 의미 기반 object 매핑은 덜 깨진다.

> **중요**: `deleteText → insertText`만 실행하면 텍스트 스타일이 `themeColor: DARK1` 등으로 초기화되어
> 검정 배경에서 내용이 안 보일 수 있다. 텍스트 교체 후에는 반드시 `updateTextStyle`을 함께 실행하거나,
> 최종 검증에서 `foregroundColor`가 `TEXT`, `TEXT_DIM`, `ORANGE` 계열인지 확인한다.

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
                # 필요 시 바로 뒤에 updateTextStyle 추가:
                # reqs.append({
                #   "updateTextStyle": {
                #     "objectId": oid,
                #     "textRange": {"type": "ALL"},
                #     "style": {
                #       "foregroundColor": {"opaqueColor": {"rgbColor": {"red": 0.94, "green": 0.94, "blue": 0.94}}},
                #       "fontFamily": "Noto Sans"
                #     },
                #     "fields": "foregroundColor,fontFamily"
                #   }
                # })

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
- 텍스트가 사라진 것처럼 보임 → 내용은 있으나 색상이 `DARK1`로 초기화됐을 수 있음. `updateTextStyle`로 `TEXT/TEXT_DIM/ORANGE` 재적용
- `createShape` 실패 → objectId 중복 확인 (슬라이드마다 고유 prefix 사용). **objectId는 최소 5자 이상** 필요 (예: `slide_01`, `sec_01` — `s01` 같은 4자 이하는 API 거부)
- Google Drive 인증 오류 → `gws auth status` 확인 후 재인증

## 생성 후 검증 — Step A → Step B → 기획자 → 디자이너 → 대상

슬라이드 생성(`NEW_ID` 확보) 직후 아래 순서로 실행한다.  
하나라도 FAIL이면 수정 후 Step A부터 재실행한다.

---

### Step A: 수치 검증

```bash
python3 /Users/harugury/.agents/skills/spigen-slides/spigen_verify.py $NEW_ID
```

---

### Step B: 이미지 검수 (getThumbnail)

Step A 전원 PASS 이후, 서브에이전트 spawn 전에 반드시 실행한다.  
API 구조 데이터만으로 놓치기 쉬운 시각적 문제를 여기서 잡는다.

```bash
python3 << 'EOF'
import subprocess, json

result = subprocess.run(
    ["gws", "slides", "presentations", "get",
     "--params", f'{{"presentationId":"{NEW_ID}"}}'],
    capture_output=True, text=True
)
slides = json.loads(result.stdout)["slides"]

for i, slide in enumerate(slides):
    thumb = subprocess.run(
        ["gws", "slides", "presentations", "pages", "getThumbnail",
         "--params", json.dumps({"presentationId": NEW_ID, "pageObjectId": slide["objectId"]})],
        capture_output=True, text=True
    )
    print(f"슬라이드 {i+1}: {json.loads(thumb.stdout).get('contentUrl', '')}")
EOF
```

확인 항목:
- 텍스트 오버플로
- 요소 겹침
- 오렌지 강조 슬라이드당 3개 이하
- 강조점 1개 원칙 유지
- 전체 레이아웃 균형

문제 발견 시:

```txt
수정 → 재생성 → Step A부터 전체 재실행
```

---

### 기획자: 내용 검수 서브에이전트

메인 에이전트가 아래 프롬프트로 서브에이전트를 spawn한다.  
**서브에이전트는 생성 컨텍스트를 전달받지 않는다. 단, 슬라이드 ID + COMPONENT_BRIEF는 반드시 전달한다.**

기획자에게 넘기는 최소 입력:

```txt
- PRESENTATION_ID
- slide별 COMPONENT_BRIEF
  (select_component() 입력값 / function_name / rationale)
  (ui_position_dependent / evidence_mode / render_scope 포함)
```

→ 프롬프트 원문: `spigen_subagent_prompts.md` 참조

### 입력 자산 부족 예외 처리

planning 단계에서 아래 조건이면 생성 전에 범위를 낮춘다.

```txt
- ui_position_dependent = true
- evidence_mode = text_only
```

이 경우 허용:
- 개념 흐름 설명
- 역할 분담 설명
- 상태 전이 설명

이 경우 금지:
- 실제 보드 화면의 칼럼 위치/버튼 위치/패널 배치 단정
- 스크린샷을 본 것처럼 보이는 UI 상세 설명

즉, 이 경우 대상 검수 FAIL은 우선 **컴포넌트 선택 실패**가 아니라 **입력 자산 부족** 가능성을 먼저 확인한다.

---

### 디자이너: 시뮬레이션 서브에이전트

→ 프롬프트 원문: `spigen_subagent_prompts.md` 참조

---

### 대상: 청중 시뮬레이션 서브에이전트

메인 에이전트가 Q2(청중)와 Q4(목적)를 함께 전달한다.

→ 프롬프트 원문: `spigen_subagent_prompts.md` 참조

---

## Done when

- 새 프레젠테이션 URL이 출력됐다.
- `spigen_postgen_hook.py --strict` 가 실행됐다.
- `review_manifest.json`, `verify.txt`, `thumbnails/` 가 생성됐다.
- 기획자 / 디자이너 / 대상 서브에이전트 검수가 모두 수행됐다.
- 표지는 Spigen 템플릿 그대로 (제목/부서/담당자/날짜/버전 정확히 입력됨).
- 단순 생성 플로우 페이지에 하단 오렌지 강조 박스를 추가하지 않았다.
- 동작흐름 + 운영 금액 + 비용표처럼 복합 구조가 필요하면 콘텐츠 템플릿 5페이지 구조를 참고했다.
- 텍스트 교체 후 배경색과 같거나 유사한 색의 텍스트가 없는지 확인했다 (dark: 검정 배경 위 검정, light: 흰 배경 위 흰/연회색).
- 배경색과 동일한 선/박스/테두리가 생성되지 않았는지 확인했다.
- 긴 문장/보조 텍스트가 배경색과 구분되지 않는 색으로 들어가지 않았는지 확인했다 (dark: 진한 화색, light: 연회색·흰색).
- 각 내용 슬라이드에 보는 사람 기준의 의미 강조점이 1개 있다.
- 강조 기준이 결론, 상호작용 포인트, 금액, 입력, 출력, 판단 기준 중 하나로 설명 가능하다.
- 내용 슬라이드는 Q7에서 선택한 테마 + 오렌지 강조 + 해당 테마 카드 구조를 따른다.
- 마지막 슬라이드는 Spigen 템플릿 인덱스 1, 2 (마지막 2페이지).
- 모든 텍스트·도형이 구글 슬라이드에서 직접 수정 가능하다.
- Step 2에서 계획한 모든 슬라이드에 내용이 입력됐다.
- Step 1에서 확정한 `select_component()` 결과와 실제 렌더 함수가 일치한다.
- slide별 `COMPONENT_BRIEF`가 저장되고, 기획자 검수 입력에 함께 전달됐다.
- 슬라이드 텍스트에 함수명·파일명·변수명(`mk_flow()`, `spigen_lib.py` 등)이 그대로 노출되지 않았다.
- 슬라이드에 장식용 선·구분선이 없다. 카드 밖 gutter에 divider / bar가 없다.
- 여백을 채우기 위한 빈 rect / 투명 도형이 없다. 요소 수가 내용 기준 최솟값이다.
- 각 슬라이드의 핵심이 3~5초 안에 파악된다. 경쟁하는 메시지 블록이 없다.
- 카드·구분선·장식 요소가 구조나 이해에 실질적으로 기여하는가? 그렇지 않으면 삭제했다.

---

## ccbot 방식 (CrossCheck Bot 전용)

> 캔버스: **720 × 405pt** (Google Slides 16:9)  
> 참조 템플릿: `1rh_2NNwM2CeZxFaZFfgoK3s1RAU2SyzZd794480hrVo`  
> 색상: BG `#000000` / DARK `#0E0E0E` / ORNG `#FF6B1A` / WHT `#FFFFFF`

CrossCheck Bot 보고서 전용. 항상 다크 배경 + 오렌지 강조, 3슬라이드 압축 구성.

기본은 위 "템플릿 방식"으로 1~6번 완성형 슬라이드를 복사/수정한다.  
`ccbot 방식`은 아래 경우에만 사용한다:

- 3장짜리 압축 보고서가 필요할 때
- 템플릿 슬라이드 복제가 아니라 API로 네이티브 도형을 새로 생성해야 할 때
- 3~5번 완성형 디자인과 같은 톤으로 추가 슬라이드를 만들어야 할 때

### C-1. 라이브러리 준비

```bash
cp ~/.agents/skills/spigen-slides/ccbot_lib.py /tmp/ccbot_lib.py
cp ~/.agents/skills/spigen-slides/spigen_lib.py /tmp/spigen_lib.py
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

TMPL_ID = "1rh_2NNwM2CeZxFaZFfgoK3s1RAU2SyzZd794480hrVo"
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
| 투명 배경 | `alpha: 0.0` (solidFill, black base) — `NOT_RENDERED` 사용 금지 |
| 오렌지 3중 충돌 | eyebrow(항상 ORANGE) + flow hot step + sbox_bar 동시 사용 금지 — hot step 있는 슬라이드의 sbox_bar는 `ORANGE_DIM` 사용 |
| 반투명 오렌지 테두리 | `alpha=0.549` (원·날짜 배지) |
| 10% 오렌지 틴트 카드 | `_fill(oid, ORNG, 0.1)` (유료 STEP, Phase current, callout) |
| 취소선 텍스트 | `_style(oid, WHT, 16.5, strike=True)` |
| `"›"` 화살표 | 별도 TEXT_BOX, `_ghost()` 적용 + `_center()` |

### C-5. 커스텀 마스터 템플릿 사용 시 (중요)

기본 Google 테마가 아닌 커스텀 마스터(예: 참조 템플릿 `1rh_2NNwM2CeZxFaZFfgoK3s1RAU2SyzZd794480hrVo`)를 복사해 사용할 때는  
`predefinedLayout: "BLANK"`가 지원되지 않을 수 있다. 이 경우 기존 슬라이드의 `layoutObjectId`를 가져와  
`layout_id` 파라미터로 전달한다.

```python
prs = gws_get(NEW_ID)
slides = prs['slides']
layout_id = slides[1]['slideProperties'].get('layoutObjectId')  # 기존 콘텐츠 슬라이드에서 추출

ccbot_compare("s01_cmp", rows, callout, 1, reqs, page_no=1, total=2, layout_id=layout_id)
ccbot_flow("s02_flow", steps, table_rows, summary, 2, reqs, page_no=2, total=2, layout_id=layout_id)
```

> API 주의: 읽을 때는 `slideProperties.layoutObjectId`, 생성할 때는 `createSlide.slideLayoutReference.layoutId` (다른 필드명)
