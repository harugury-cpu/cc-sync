---
name: spigen-slides
description: Spigen 브랜드 PPT 템플릿으로 내용이 채워진 Google Slides를 생성한다. 주제·내용을 받아 템플릿 레이아웃을 선택하고 내용을 자동 입력한다. "PPT 만들어줘", "프레젠테이션 만들어", "슬라이드 만들어줘" 등의 요청에 사용한다.
license: MIT
metadata:
  category: productivity
  locale: ko-KR
  phase: v2
---

# spigen-slides

## 고정값

- 담당자: `한원진 담당`
- 부서: `디자인부문ㅣ패키지디자인팀`
- 템플릿 ID: `1R_z4ZKSbRSe5uQ-uWT6dnmBDTJ7M4yOjbGW_1UfxnEk`

## 디자인 시스템

| 항목 | 값 |
|-----|---|
| 포인트 컬러 | `#FF6900` (RGB: 1.0 / 0.412 / 0.0) |
| 영어 폰트 | `Proxima Nova` |
| 한글 폰트 | `Noto Sans` |

**폰트 적용 규칙**:
- 한글이 포함된 텍스트 → `Noto Sans`
- 영문/숫자 전용 텍스트 → `Proxima Nova`
- 혼합 콘텐츠 → `Noto Sans` (한글 우선)

### 테마별 색상 토큰

슬라이드 배경이 **검정(다크)**이냐 **흰색(라이트)**이냐에 따라 텍스트·카드 색상이 달라진다.

| 토큰 | 다크 테마 (Black 배경) | 라이트 테마 (White 배경) | 웜 테마 (Beige 배경) | 용도 |
|-----|---------------------|----------------------|--------------------|-----|
| `SLIDE_BG` | `#000000` | `#FFFFFF` | `#F5F0E8` | 슬라이드 배경 |
| `TITLE_COLOR` | `#F9FAFB` | `#1A1A1A` | `#1A1A1A` | 제목 텍스트 |
| `BODY_COLOR` | `#6B7280` | `#4A4A4A` | `#4A4A4A` | 본문·카드 텍스트 |
| `CARD_BG` | `#0A0A0A` | `#F5F5F5` | `#FFFFFF` | 카드·아이템 배경 |
| `CARD_BORDER` | `#141414` | `#E5E5E5` | `#E5E5E5` | 카드 테두리 |
| `ACCENT` | `#FF6900` | `#FF6900` | `#FF6900` | 강조·바·화살표 (테마 불문 동일) |

**슬라이드 유형별 기본 테마:**

| 유형 | 기본 테마 | 이유 |
|-----|---------|-----|
| cover | 다크 | Spigen 브랜드 커버 |
| section-divider | 다크 | 포스터 스타일 |
| content | 라이트 | 가독성 우선 |
| statistics / 3-col | 라이트 | 데이터 가독성 |
| 3col-cards | 라이트 | 카드별 색상 변형 (light·dark·accent) |
| toc | 웜 | 베이지 배경 + 메타 라벨 |
| split-cards | 라이트 | 좌측 텍스트 + 우측 카드 스택 |
| closing | 다크 | 브랜드 마감 |

### 색상 비율 원칙 (60-30-10)

| 비율 | 역할 | 적용 토큰 |
|-----|-----|---------|
| 60% | 슬라이드 배경 | 다크: `#000000` / 라이트: `#FFFFFF` / 웜: `#F5F0E8` |
| 30% | 중립 텍스트·카드 | `TITLE_COLOR`, `BODY_COLOR`, `CARD_BG` |
| 10% | 강조 포인트 | `#FF6900` — 상단 바, 번호, 화살표, 배지 |

> `#FF6900`은 한 슬라이드당 **3개 이하** 요소에 사용한다. 과용하면 브랜드 강조 효과가 희석된다.

### 테마 교차 원칙

동일 테마가 3장 이상 연속되면 시각적 단조로움이 생긴다. 다크↔라이트를 교차 배치한다.

```
cover(dark) → contents(dark) → section-divider(dark) → content(light) → statistics(light) → section-divider(dark) → ...
```

## 슬라이드 디자인 사양 (slides-grab × Spigen)

**표지(slide-01.html)만 Spigen 브랜드 커버로 교체한다. 나머지 슬라이드는 slides-grab-design이 HTML로 생성한다.**

### 공통 디자인 토큰

| 토큰 | 값 | 용도 |
|-----|---|-----|
| accent | `#FF6900` | 강조선·번호·포인트 |
| 영문 폰트 | `Proxima Nova` (fallback `sans-serif`) | heading, display |
| 한글 폰트 | `Noto Sans KR`, `Noto Sans` | 한글 포함 모든 요소 |
| 섹션 배경 | `#1A1A1A` | section-divider 배경 |
| 섹션 텍스트 | `#FFFFFF` | section-divider 제목 |

### 슬라이드 유형별 디자인 사양 (slides-grab-design 가이드)

**표지 (Spigen 브랜드 커버) — 다크 테마**
- `#000000` 배경 / 상단 `#FF6900` 가로 바 (3pt)
- 대형 제목 (Proxima Nova/Noto Sans, 17pt, `#F9FAFB`, bold)
- 하단: 부서·담당자 (왼쪽) / 날짜·버전 (오른쪽)

**섹션 구분 (section-divider) — 다크 테마**
- `#000000` 풀블리드 배경 / 상단 `#FF6900` 가로 바
- 대형 번호 (Proxima Nova, 120pt, `#FF6900`, 좌측)
- 섹션 제목 (36pt, `#F9FAFB`, 번호 하단)
- 나머지 비움 — 텍스트 최소화

**일반 내용 (content) — 라이트 테마**
- `#FFFFFF` 배경 / 상단 `#FF6900` 가로 바 (3pt)
- 제목 (Proxima Nova/Noto Sans, 17pt, `#1A1A1A`, bold)
- 본문 (Noto Sans, 8.5pt, `#4A4A4A`, 줄간격 1.6)

**3열 항목 (statistics) — 라이트 테마**
- `#FFFFFF` 배경 / 상단 제목 (content와 동일)
- 카드 배경 `#F5F5F5`, 테두리 `#E5E5E5`
- 3개 균등 컬럼: `#FF6900` 번호 블록 + 소제목(bold) + 설명

---

## Step 1: 기획 (slides-grab 방식)

### 1-1. 목적·청중·톤 파악

순서대로 질문한다 (한 번에 모아서 묻지 않는다):

1. **주제**: "어떤 내용의 프레젠테이션인가요?"
2. **청중**: "누가 보는 자료인가요? (내부 팀 / 경영진 / 외부 고객 등)"
3. **톤**: "어떤 분위기로 전달하고 싶으신가요? (예: 신뢰감 있는 / 데이터 중심 / 설득적인)"
4. **날짜** (언급 없으면 오늘 날짜 자동 사용, 묻지 않음)
5. **버전** (언급 없으면 V1.0, 묻지 않음)

### 1-2. 비주얼 테제 작성

수집한 정보를 바탕으로 **한 문장**으로 무드·방향·에너지를 정의한다.

예시: _"제품의 신뢰성을 데이터로 증명하는, 간결하고 자신감 있는 톤의 덱"_

### 1-3. 내러티브 구조 설계

slides-grab의 내러티브 시퀀스를 따른다:

| 단계 | 역할 | slides-grab 슬라이드 유형 |
|-----|-----|----------------------|
| **Opener** | 전제·약속·정체성 제시 | cover (Spigen 브랜드 커버) |
| **Support / Proof** | 핵심 근거·맥락·구체적 가치 | statistics / 3-col |
| **Detail / Story** | 메커니즘·프로세스·심층 설명 | content / split-layout |
| **Close / CTA** | 결론·권고·다음 액션 | closing |

섹션 구분(section-divider)은 시각적 템포를 리셋하는 **포스터**로 취급한다. 텍스트는 최소화.

### 1-4. 아웃라인 초안 제시

각 슬라이드의 역할과 핵심 메시지를 아래 포맷으로 제시한다:

```
[아웃라인]
슬라이드 1 (cover)          — 제목 + 한 줄 부제목
슬라이드 2 (contents)       — 섹션 목록
슬라이드 3 (section-divider)— 01: [섹션명]
슬라이드 4 (content)        — 핵심 메시지: "___는 ___하다"
...
슬라이드 N (closing)        — 다음 액션 또는 결론 한 줄
```

사용자에게 아웃라인을 보여주고 승인받는다. **승인 전 Step 2로 넘어가지 않는다.**

---

## Step 2: 슬라이드 구성 계획 (디자인 원칙 적용)

승인된 아웃라인을 slides-grab 레이아웃에 매핑하고 각 슬라이드의 카피를 확정한다.

### 레이아웃 선택 규칙

모든 슬라이드는 **slides-grab-design이 HTML로 생성**한다. 표지만 Step 3-4에서 Spigen 브랜드 커버로 교체한다.

| 슬라이드 유형 | slides-grab 레이아웃 | 비고 |
|------------|-------------------|-----|
| 표지 (Cover) | **Spigen 브랜드 HTML** (Step 3-4에서 교체) | 담당자/날짜/버전 포함 |
| 목차 (Contents) | `contents` | 섹션 2개 이상일 때 추가 |
| 섹션 구분 | `section-divider` | 포스터 스타일, 최소 텍스트 |
| 일반 내용 | `content` | 설명·근거·스토리 |
| 3열 항목 | `statistics` 또는 `split-layout` | 3개 병렬 항목 나열 시 |
| 인용·강조 | `quote` | 임팩트 있는 한 줄 메시지 |
| 변경이력 | `content` | 변경이력 있을 때만 추가 |
| 마지막 | `closing` | Spigen 분위기 마감 |

### 컴포넌트 빠른 선택 가이드

| 상황 | 컴포넌트 | 함수 | 기본 테마 |
|-----|---------|-----|---------|
| 표지 / 섹션 구분 | slide-base + section-divider | `slide_base()` / `mk_section_divider()` | dark |
| 목차 (다크 스타일) | contents | `mk_contents()` | dark |
| 목차 (베이지, 메타 라벨) | toc | `mk_toc()` | warm |
| 현재→문제→기대효과 3열 비교 | 3-col | `mk_3col()` | light |
| 핵심 개념 3가지 카드 | 3col-cards | `mk_3col_cards()` | light |
| 프로세스 / 흐름도 | flow | `mk_flow()` | dark |
| 텍스트 중심 설명 | text-block | `mk_text_block()` | light |
| 좌우 비교 / 병렬 | split-layout | `mk_split()` | light |
| 텍스트 + 우측 카드 스택 | split-cards | `mk_split_cards()` | light |
| 임팩트 한 줄 메시지 | quote | `mk_quote()` | dark |
| 오렌지+테마색 2색 제목 | title-accent | `mk_title_accent()` | light |

### 카피 작성 원칙 (slides-grab 기준)

- **슬라이드당 하나의 메시지**: 경쟁하는 블록 금지
- **3~5초 스캔 가능하게**: 본문 글머리는 3줄 이내
- **제목은 주장형 문장**: "성능 비교" → "성능이 30% 향상됐다"
- **섹션 구분 슬라이드**: 번호 + 짧은 제목만, 설명 없음
- **여백 우선**: 공간을 채우려 하지 말 것

### 구성 예시 출력 형식

```
[확정 구성]
슬라이드 1  (cover)          : 패키지 디자인 가이드라인 2026 / 부제목
슬라이드 2  (contents)       : 3개 섹션 목차
슬라이드 3  (section-divider): 01 — 디자인 원칙
슬라이드 4  (statistics)     : 색상 / 타이포 / 레이아웃
슬라이드 5  (section-divider): 02 — 소재 사용 규정
슬라이드 6  (content)        : 승인 소재 목록
슬라이드 7  (section-divider): 03 — 적용 사례
슬라이드 8  (content)        : 제품별 적용 예시
슬라이드 9  (closing)        :
```

### 리뷰 기준 (slides-grab Review Litmus)

구성 확정 전 아래 항목을 점검한다:

- [ ] 각 슬라이드의 핵심 포인트를 3~5초 안에 파악할 수 있는가?
- [ ] 각 슬라이드에 경쟁하는 블록 없이 하나의 지배적인 메시지가 있는가?
- [ ] 제거해도 의미가 손상되지 않는 카피·배지·콜아웃이 없는가?
- [ ] 섹션 구분 슬라이드가 포스터처럼 간결한가?
- [ ] `#FF6900`이 한 슬라이드에 3개 이하 요소에만 사용됐는가?
- [ ] 폰트는 Proxima Nova(영문) / Noto Sans(한글) 두 가지만 사용됐는가?
- [ ] 동일 테마가 3장 이상 연속 배치되지 않았는가? (다크↔라이트 교차 권장)
- [ ] 슬라이드 유형에 맞는 기본 테마가 적용됐는가? (cover·section-divider → dark, content·statistics → light)

구성을 사용자에게 보여주고 확인받는다. "수정 사항이 있으면 말씀해 주세요. 없으면 생성하겠습니다."

---

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
