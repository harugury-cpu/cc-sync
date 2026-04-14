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
- 템플릿 ID: `16yCUv6G8QwiqZdRaxktCQROwUD9p-WO2v88BppsUs5M`

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

| 토큰 | 다크 테마 (Black 배경) | 라이트 테마 (White 배경) | 용도 |
|-----|---------------------|----------------------|-----|
| `SLIDE_BG` | `#000000` | `#FFFFFF` | 슬라이드 배경 |
| `TITLE_COLOR` | `#F9FAFB` | `#1A1A1A` | 제목 텍스트 |
| `BODY_COLOR` | `#6B7280` | `#4A4A4A` | 본문·카드 텍스트 |
| `CARD_BG` | `#0A0A0A` | `#F5F5F5` | 카드·아이템 배경 |
| `CARD_BORDER` | `#141414` | `#E5E5E5` | 카드 테두리 |
| `ACCENT` | `#FF6900` | `#FF6900` | 강조·바·화살표 (테마 불문 동일) |

**슬라이드 유형별 기본 테마:**

| 유형 | 기본 테마 | 이유 |
|-----|---------|-----|
| cover | 다크 | Spigen 브랜드 커버 |
| section-divider | 다크 | 포스터 스타일 |
| content | 라이트 | 가독성 우선 |
| statistics / 3-col | 라이트 | 데이터 가독성 |
| closing | 다크 | 브랜드 마감 |

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

구성을 사용자에게 보여주고 확인받는다. "수정 사항이 있으면 말씀해 주세요. 없으면 생성하겠습니다."

---

## Step 3: 기술 실행 (Google Slides API 직접 구현)

### 핵심 전략

| 슬라이드 | 방식 |
|---------|------|
| 표지 (slide 1) | Spigen 템플릿 인덱스 0 복사 → 텍스트 삽입 |
| 마지막 슬라이드 | Spigen 템플릿 인덱스 18 복사 (빈 슬라이드) |
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
  --params '{"fileId":"16yCUv6G8QwiqZdRaxktCQROwUD9p-WO2v88BppsUs5M"}' \
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

### 3-4. 표지·마지막(인덱스 0, 18)만 남기고 전부 삭제

```python
# /tmp/delete_for_cover.py
import json

with open('/tmp/spigen_map.json') as f:
    m = json.load(f)

keep = {0, 18}
reqs = [{"deleteObject": {"objectId": m[str(i)]['slide_id']}}
        for i in range(len(m)) if i not in keep]
import sys
print(json.dumps({"requests": reqs}))
print(f"삭제: {len(reqs)}개", file=sys.stderr)
```

```bash
python3 /tmp/delete_for_cover.py 2>/dev/null > /tmp/del_req.json
gws slides presentations batchUpdate \
  --params "{\"presentationId\":\"$NEW_ID\"}" \
  --json "$(cat /tmp/del_req.json)" 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print('삭제 완료')"
```

### 3-5. 표지 텍스트 삽입

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

### 3-6. 내용 슬라이드 생성 — 디자인 컴포넌트 라이브러리

내용 슬라이드마다 아래 Python 헬퍼로 구성한다.
모든 요청을 하나의 `batchUpdate`로 묶어 한 번에 실행한다.

#### 공통 헬퍼

```python
def pt(v): return int(v * 12700)
def c255(r, g, b): return {"red": r/255, "green": g/255, "blue": b/255}

ORANGE = c255(255, 105,   0)   # #FF6900 (테마 불문 고정)

# 테마별 색상 토큰 — 배경이 검정(dark)이면 텍스트·카드가 밝게, 흰(light)이면 어둡게
THEMES = {
    'dark': {
        'SLIDE_BG':    {"red": 0,        "green": 0,        "blue": 0},        # #000000
        'TITLE_COLOR': c255(249, 250, 251),   # #F9FAFB
        'BODY_COLOR':  c255(107, 114, 128),   # #6B7280
        'CARD_BG':     c255( 10,  10,  10),   # #0A0A0A
        'CARD_BORDER': c255( 20,  20,  20),   # #141414
    },
    'light': {
        'SLIDE_BG':    {"red": 1,        "green": 1,        "blue": 1},        # #FFFFFF
        'TITLE_COLOR': c255( 26,  26,  26),   # #1A1A1A
        'BODY_COLOR':  c255( 74,  74,  74),   # #4A4A4A
        'CARD_BG':     c255(245, 245, 245),   # #F5F5F5
        'CARD_BORDER': c255(229, 229, 229),   # #E5E5E5
    },
}

def shape(oid, page, stype, x, y, w, h):
    return {"createShape": {"objectId": oid, "shapeType": stype,
        "elementProperties": {"pageObjectId": page,
            "size": {"width":  {"magnitude": pt(w), "unit": "EMU"},
                     "height": {"magnitude": pt(h), "unit": "EMU"}},
            "transform": {"scaleX":1,"scaleY":1,
                "translateX": pt(x),"translateY": pt(y),"unit":"EMU"}}}}

def fill(oid, fg, bg=None, wt=0.6):
    bg = bg or fg
    return {"updateShapeProperties": {"objectId": oid,
        "fields": "shapeBackgroundFill,outline",
        "shapeProperties": {
            "shapeBackgroundFill": {"solidFill": {"color": {"rgbColor": fg}}},
            "outline": {"outlineFill": {"solidFill": {"color": {"rgbColor": bg}}},
                        "weight": {"magnitude": pt(wt), "unit": "EMU"}}}}}

def txtstyle(oid, color, size, bold=False):
    return {"updateTextStyle": {"objectId": oid,
        "textRange": {"type": "ALL"},
        "style": {"foregroundColor": {"opaqueColor": {"rgbColor": color}},
                  "fontSize": {"magnitude": size, "unit": "PT"},
                  "fontFamily": "Noto Sans", "bold": bold},
        "fields": "foregroundColor,fontSize,fontFamily,bold"}}

def txt(oid, text):
    return {"insertText": {"objectId": oid, "insertionIndex": 0, "text": text}}
```

#### 컴포넌트 A: 슬라이드 기본 레이아웃 (배경 + 오렌지 상단 바 + 제목)

`theme='dark'` → 검정 배경 + 밝은 제목 / `theme='light'` → 흰 배경 + 어두운 제목

```python
def slide_base(slide_oid, title_text, insert_index, reqs, theme='dark'):
    T = THEMES[theme]
    reqs.append({"createSlide": {"objectId": slide_oid,
        "insertionIndex": insert_index,
        "slideLayoutReference": {"predefinedLayout": "BLANK"}}})
    # 배경색 (테마에 따라 결정)
    reqs.append({"updatePageProperties": {"objectId": slide_oid,
        "fields": "pageBackgroundFill",
        "pageProperties": {"pageBackgroundFill": {
            "solidFill": {"color": {"rgbColor": T['SLIDE_BG']}}}}}})
    # 상단 오렌지 바 (테마 불문 고정)
    bar = f"{slide_oid}_bar"
    reqs += [shape(bar, slide_oid, "RECTANGLE", 0, 0, 720, 3), fill(bar, ORANGE)]
    # 제목 (테마에 따라 글자색 결정)
    ttl = f"{slide_oid}_ttl"
    reqs += [shape(ttl, slide_oid, "TEXT_BOX", 56, 44, 500, 22),
             txt(ttl, title_text), txtstyle(ttl, T['TITLE_COLOR'], 17, bold=True)]
```

#### 컴포넌트 B: 3열 레이아웃 (현황·비교형)

```
열 구조: 1fr(189pt) 20pt 1fr 20pt 1fr  (padding 56pt)
col-label 6.5pt bold → 왼쪽 컬러 바(2pt) + ROUND_RECTANGLE 카드(24pt)
```

```python
# 열 색상 설정 — 테마별로 구분 (라벨 색·왼쪽 바 색)
COL_STYLES = {
    'dark': {
        "현재":             {"lbl": c255(107,114,128), "bar": c255( 20, 20, 20)},
        "문제점":           {"lbl": c255(239, 68, 68), "bar": c255(127, 29, 29)},
        "도입 시 기대효과": {"lbl": c255( 52,211,153), "bar": c255(  6, 78, 59)},
    },
    'light': {
        "현재":             {"lbl": c255(107,114,128), "bar": c255(229,231,235)},
        "문제점":           {"lbl": c255(220, 38, 38), "bar": c255(254,226,226)},
        "도입 시 기대효과": {"lbl": c255(  5,150,105), "bar": c255(209,250,229)},
    },
}
PAD, COL_W, ARW_W = 56, 189, 20
COL_Y, LBL_H, ITEM_H, ITEM_GAP = 83, 11, 24, 5

def mk_3col(sid, cols, reqs, theme='light'):
    """cols = [{"label":"현재", "items":["항목1","항목2",...]}, ...]
    theme: 'dark' (검정 배경) | 'light' (흰 배경, 기본값)
    """
    T = THEMES[theme]
    sty_map = COL_STYLES[theme]
    CX = [PAD, PAD+COL_W+ARW_W, PAD+COL_W*2+ARW_W*2]
    AX = [PAD+COL_W, PAD+COL_W*2+ARW_W]

    for ci, col in enumerate(cols):
        cx  = CX[ci]
        sty = sty_map.get(col["label"], {"lbl": T['BODY_COLOR'], "bar": T['CARD_BORDER']})
        IY0 = COL_Y + LBL_H + 8

        lid = f"{sid}_lbl{ci}"
        reqs += [shape(lid, sid, "TEXT_BOX", cx, COL_Y, COL_W, LBL_H),
                 txt(lid, col["label"].upper()),
                 txtstyle(lid, sty["lbl"], 6.5, bold=True)]

        for ii, item in enumerate(col["items"]):
            iy = IY0 + ii*(ITEM_H+ITEM_GAP)
            bid, cid = f"{sid}_b{ci}{ii}", f"{sid}_c{ci}{ii}"
            reqs += [
                shape(bid, sid, "RECTANGLE", cx, iy, 2, ITEM_H),
                fill(bid, sty["bar"]),
                shape(cid, sid, "ROUND_RECTANGLE", cx+2, iy, COL_W-2, ITEM_H),
                fill(cid, T['CARD_BG'], T['CARD_BORDER']),
                txt(cid, item),
                txtstyle(cid, T['BODY_COLOR'], 7.5),
            ]

    for ai, ax in enumerate(AX):
        aid = f"{sid}_arw{ai}"
        reqs += [shape(aid, sid, "TEXT_BOX", ax, COL_Y+26, ARW_W, 18),
                 txt(aid, "›"), txtstyle(aid, ORANGE, 13, bold=True),
                 {"updateParagraphStyle": {"objectId": aid,
                   "textRange":{"type":"ALL"},
                   "style":{"alignment":"CENTER"},"fields":"alignment"}}]
```

#### 컴포넌트 C: 플로우 다이어그램 (동작흐름·프로세스형)

```
5단계 스텝 박스(ROUND_RECTANGLE) + OPEN_ARROW 라인 + 과금 스텝 아래 비용 박스
```

```python
def mk_flow(sid, steps, cost_map, reqs, theme='dark'):
    """
    steps    = [("STEP 01","이름","서비스", is_paid), ...]
    cost_map = {step_index: "₩X,XXX~X,XXX"}
    theme: 'dark' (기본값) | 'light'
    """
    T = THEMES[theme]
    N = len(steps)
    BW, FH, AW = 108, 55, 14
    FY = 50
    SX = (720 - N*BW - (N-1)*AW) // 2

    for i, (step, name, svc, paid) in enumerate(steps):
        bx  = SX + i*(BW+AW)
        bid = f"{sid}_s{i}"
        # 유료 스텝: 오렌지 테두리 강조 / 일반 스텝: 테마 카드색
        fc  = c255(13,7,0) if paid else T['CARD_BG']
        bc  = ORANGE       if paid else T['CARD_BORDER']
        reqs += [shape(bid, sid, "ROUND_RECTANGLE", bx, FY, BW, FH),
                 fill(bid, fc, bc, 0.8),
                 txt(bid, f"{step}\n{name}\n{svc}"),
                 txtstyle(bid, T['BODY_COLOR'], 6.5)]

        if i < N-1:
            lid = f"{sid}_l{i}"
            reqs += [
                {"createLine": {"objectId": lid, "lineCategory": "STRAIGHT",
                    "elementProperties": {"pageObjectId": sid,
                        "size": {"width":{"magnitude":pt(AW),"unit":"EMU"},
                                 "height":{"magnitude":pt(1),"unit":"EMU"}},
                        "transform":{"scaleX":1,"scaleY":1,
                            "translateX":pt(bx+BW),"translateY":pt(FY+FH//2),
                            "unit":"EMU"}}}},
                {"updateLineProperties": {"objectId": lid,
                    "fields": "lineFill,weight,endArrow",
                    "lineProperties": {
                        "lineFill": {"solidFill": {"color": {"rgbColor": ORANGE}}},
                        "weight": {"magnitude": pt(1), "unit": "EMU"},
                        "endArrow": "OPEN_ARROW"}}},
            ]

        if i in cost_map:
            cid = f"{sid}_cost{i}"
            bx2 = SX + i*(BW+AW)
            reqs += [shape(cid, sid, "ROUND_RECTANGLE", bx2, FY+FH+18, BW, 40),
                     fill(cid, c255(13,7,0), ORANGE, 0.8),
                     txt(cid, f"월 예상\n{cost_map[i]}"),
                     txtstyle(cid, ORANGE, 7.5, bold=True)]
```

#### 컴포넌트 D: 텍스트 블록 (제목 + 본문)

```python
def mk_text_block(sid, body_text, reqs, y_start=83, font_size=8.5, theme='light'):
    """theme: 'light' (흰 배경, 기본값) | 'dark' (검정 배경)"""
    T = THEMES[theme]
    bid = f"{sid}_body"
    reqs += [shape(bid, sid, "TEXT_BOX", 56, y_start, 608, 280),
             txt(bid, body_text),
             txtstyle(bid, T['BODY_COLOR'], font_size)]
```

---

### 3-7. batchUpdate 실행

모든 컴포넌트 요청을 하나의 리스트에 모아 실행:

```bash
gws slides presentations batchUpdate \
  --params "{\"presentationId\":\"$NEW_ID\"}" \
  --json "$(cat /tmp/content_req.json)" 2>/dev/null | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print('완료:', len(d.get('replies',[])), '항목')"
```

### 3-8. 결과 출력

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
- `createShape` 실패 → objectId 중복 확인 (슬라이드마다 고유 prefix 사용)
- Google Drive 인증 오류 → `gws auth status` 확인 후 재인증

## Done when

- 새 프레젠테이션 URL이 출력됐다.
- 표지는 Spigen 템플릿 그대로 (제목/부서/담당자/날짜/버전 정확히 입력됨).
- 내용 슬라이드는 유형별 테마가 올바르게 적용됐다: cover/section-divider → 검정 배경(`dark`), content/statistics → 흰 배경(`light`), 오렌지 상단 바는 테마 불문 공통.
- 마지막 슬라이드는 Spigen 템플릿 인덱스 18 (빈 슬라이드).
- 모든 텍스트·도형이 구글 슬라이드에서 직접 수정 가능하다.
- Step 2에서 계획한 모든 슬라이드에 내용이 입력됐다.
