---
name: spigen-slides
description: "PPT 만들어줘 / 피피티 만들어줘 / 장표 만들어줘 / 슬라이드 만들어줘 / 발표자료 만들어줘 / 프레젠테이션 만들어줘 / 보고서 슬라이드 만들어줘 / 덱 만들어줘 등 슬라이드 생성 요청 시 발동. Spigen 내부용 Google Slides 자동 생성 스킬."
license: MIT
metadata:
  category: productivity
  locale: ko-KR
  phase: v6.1.1
---

# spigen-slides

> 컬러 토큰 출처: `~/Downloads/Spigen Dark|Light Design System/colors_and_type.css`
> 빌더가 디자인 룰을 자동 강제. 페르소나 검수는 빌드 후 필수 자동 호출.

## 핵심 원칙

- **AI는 내용을 창작하지 않는다.** 사용자가 준 내용을 정리할 뿐이다.
- **내용이 먼저다.** 컴포넌트가 내용을 강요하면 안 된다.
- **자유도가 먼저다.** 형식 때문에 내용이 잘리면 형식을 버리고 내용을 살린다.
- 디자인 시스템은 **안전장치**다. 폰트/간격/겹침/강조 남발만 막고 내용 표현은 최대한 열어둔다.
- 기본 생성 모드는 **운영용 = 디테일용 = 보고서형** 하나다.
- 각 슬라이드는 **한 페이지 자기완결 설명**을 우선한다. 발표용 희소 카피보다 읽고 바로 실행 가능한 설명을 우선한다.
- **표지는 직접 그리지 않는다.** light / dark 모두 지정 템플릿 cover를 복사하고 텍스트만 교체한다.

---

## 고정값

- 담당자: `한원진 담당`
- 부서: `디자인부문ㅣ패키지디자인팀`
- 오렌지: `#FF6B1A`
- dark 배경: `#1C1C1E` / 텍스트: `#FFFFFF`
- light 배경: `#FFFFFF` / 텍스트: `#1C1C1E`
- 빌더: `~/.agents/skills/spigen-slides/spigen_build.py`

---

## 진행 흐름

```
Step 1. 내용 수집
Step 2. 슬라이드 구성 제안 → 사용자 승인
Step 3. 생성 + 링크 공유
```

---

## Step 1. 내용 수집

### 경로 A — 원본 데이터 있음

문서, 노트, 보드 데이터, 채팅 기록 등 원본이 있으면:
1. 원본을 읽는다
2. 핵심 내용만 추출한다
3. 추출 결과를 사용자에게 확인받는다

원칙: 원본에 없는 내용을 추가하지 않는다. 수치·고유명사는 원본 그대로 사용한다.

### 경로 B — 직접 제공

아래 4가지만 묻는다:

```
Q1. 이 PPT의 목적은?
    보고 / 교육·안내 / 제안 / 홍보 중 선택 또는 직접 설명

Q2. 청중은 누구인가요?
    (예: 경영진, 팀 내부, 외부 고객)

Q3. 전달할 핵심 내용을 적어주세요.
    형식 무관 — 글머리, 메모, 키워드 나열 모두 가능

Q4. 테마: 생략 가능 (기본 = light, 필요 시 dark)
```

테마를 따로 지정하지 않으면 **light를 기본값**으로 사용한다.

### 기본 생성 모드

사용자가 따로 요약형/발표형을 요구하지 않으면 아래 **단일 기본값**을 적용한다.

```txt
default_mode = operational_detail_report
```

즉 기본 출력은:
- 운영 전달용
- 한 장 자기완결형
- 5~6줄 설명 허용
- "왜"보다 "누가 / 언제 / 무엇을 / 어디서 확인" 우선

내부 파라미터 기본값:

```txt
detail_level = 8
layout_variance = 3
content_preservation_priority = max
execution_clarity_priority = max
```

의미:
- `detail_level`: 설명 밀도
- `layout_variance`: 레이아웃 변주 강도
- `content_preservation_priority`: 형식보다 내용 보존 우선 여부
- `execution_clarity_priority`: 실무 실행 가능성 우선 여부

---

## Step 1.5. 콘텐츠 분석 (내부 — 출력 안 함)

Step 2 진입 전 아래를 내부적으로 수행한다. 사용자에게 출력하지 않는다.

**① 사실 추출 — delta 고정값**

수치·고유명사·시스템명·날짜는 원본과 동일하게 고정한다. 이 값은 슬라이드 본문에서 변경 불가.
동사·조사·연결어는 슬라이드 형식에 맞게 최소 조정 허용. 새로운 사실 추가는 절대 금지.

**② 콘텐츠 타입 분류 → 컴포넌트 결정**

대원칙:
- 컴포넌트는 내용을 **번역**할 뿐 내용을 **재단**하면 안 된다.
- 내용 손실이 우려되면 더 단순한 텍스트형 / 설명형 컴포넌트를 선택한다.
- 운영용(=디테일용=보고서형)에서는 sparse pitch deck 스타일을 사용하지 않는다.

**강제 규칙 — 모든 덱에 예외 없이 적용:**
- **첫 슬라이드**: 반드시 `cover()` — 사용자가 생략을 요청해도 포함한다.
- **클로징 없음**: 마지막은 콘텐츠 슬라이드로 끝낸다.
- **기본 테마: dark** — `theme="dark"` 가 default. light는 사용자가 "라이트로", "light theme" 같이 명시 요청 시에만 사용.
- **표지 제목 2줄 이내**: `cover(title=...)` 의 `\n` 개수 1개 이하. 3줄 이상 시 자동 트림 + 경고.
- **테마 선택**: `theme="light"` 또는 `theme="dark"` — 각각 별도 지정 템플릿 cover 사용.
- **light cover 기준**: KPI 라이트 템플릿 `1BBG9PR6ZBsEABbJLhbUUfRMkgGYQtNMOWAmLQgPhr70`
- **dark cover 기준**: 다크 가이드 템플릿 `1HJbTWXPCr38gXDQuarglSLrkheDQXAojlrYUKcfVgAc`
- **KPI 덱**: `template="kpi"` — 라이트 모드 전용. `kpi_status()` + `kpi_tasks()` 사용.

중간 슬라이드 컴포넌트 결정 (위에서 아래로 순서대로 확인, 첫 번째 일치 항목 사용).

**선택 원칙 (시트는 결과 레퍼런스, 입력 슬롯이 아니다):**
- 콘텐츠가 mk_* 컴포넌트의 슬롯(항목 수·키 형식)에 **정확히 일치하지 않으면** 자유 레이아웃 우선.
- mk_*는 슬롯이 명백히 일치할 때만 — 강제 매핑(끼워맞추기)은 절대 금지.
- 디자인 토큰(색·간격·타이포)은 자유 레이아웃에서도 시트와 동일하게 적용된다.

| 타입 | 판단 기준 | 사용 방식 |
|-----|---------|------------|
| 단순 서술/나열 | 구조화 어려운 설명·주의사항·요약 본문 | `slide()` |
| 단일 강조 메시지 | 한 슬라이드 = 한 문장 강조 | `callout()` |
| 완료·미완료 체크리스트 | 항목별 완료 여부 목록 | `checklist()` |
| 자유 카드 조합 | 항목 수가 4개+ 또는 시트 슬롯과 다른 카드 그룹 | `start_slide()` + `card()` 반복 |
| 자유 플로우 조합 | 단계 7개+ 또는 자유 형태 단계 | `start_slide()` + `flow_step()` 반복 |
| 자유 비교 조합 | 비교 6행+ 또는 비교 + 결론을 한 슬라이드에 | `start_slide()` + `compare_pair()` 반복 |
| **시트 슬롯 정확 일치 — Before/After** | 항목별 before→after, 정확히 1~5행 | `mk_compare_rows` |
| **시트 슬롯 정확 일치 — 프로세스 강조** | 정확히 3~6단계, 동일 형태 | `mk_flow_focus` |
| **시트 슬롯 정확 일치 — 프로세스 밀도** | 6단계 이상, 비용/시간 포함 | `mk_flow` |
| **시트 슬롯 정확 일치 — 팀 매핑** | 팀(행) × 항목(열), **정확히 3행 이하** | `mk_swimlane_mapping` |
| **시트 슬롯 정확 일치 — 3카드** | 정확히 3개 동등 항목 | `mk_3col_cards` |
| **시트 슬롯 정확 일치 — 분기** | YES/NO 두 갈래 결정 | `mk_decision_tree` |
| **시트 슬롯 정확 일치 — 레이어** | 입력→처리→출력 레이어 | `mk_arch_layers` |
| KPI 진행 현황 | KPI / 목표 / 실적 / 달성률 | `kpi_status()` ★ template="kpi" |
| KPI 핵심과제 | 연관KPI / 핵심과제 / 실행계획 | `kpi_tasks()` ★ template="kpi" |
| **결론 페이지 (선택)** — 대부분 사용 안 함 | 좌 큰 메트릭 + 우 디테일 4개 (시트 mk_conclusion_detail 양식) | `conclusion(metric, caption, details=[...])` |

**자유 레이아웃 빌딩 블록:**

```python
# 슬라이드 시작 — eyebrow는 모든 콘텐츠 슬라이드에 권장 (★ 표준)
b.start_slide(heading="슬라이드 제목", eyebrow="CATEGORY")

# 카드 — emphasis 옵션:
#   None / 미지정 : 일반 (surface + border)
#   "dim"         : 약한 강조 (accent_bg + accent border)
#   "full"        : 풀 ORANGE 배경 + 검정 텍스트 (★ 한 슬라이드 1개만 허용)
b.card(x=40, y=110, w=200, h=120, label="01", title="제목",
       body="본문 (**굵게** 마크업 자동)", emphasis=None)

# footer 섹션이 필요한 카드 (mk_conclusion_detail 스타일)
b.card(x=40, y=110, w=200, h=200, label="01", title="제목",
       body="본문",
       footer_label="현재 지점", footer_body="**핵심값** 보강 메시지")

# 플로우 단계 — 가로 자유 배치, primary=True로 강조 단계 1개 지정
b.flow_step(x=40, y=110, w=160, h=140, num="01", name="단계명",
            desc="설명 (**굵게**)", primary=False)

# 비교 행 — y만 지정 (가로 자동 배치), 여러 번 호출 가능
b.compare_pair(y=110, item="항목1", before="기존", after="개선")
b.compare_pair(y=144, item="항목2", before="기존", after="개선")

# 단일 강조 메시지 슬라이드
b.callout(text="핵심 메시지 한 줄", sub="부연 설명")

# 결론 페이지 (선택, 대부분 사용 안 함) — 시트 mk_conclusion_detail 양식
b.conclusion(metric="QR 1종", caption="**3대 부담 해소**",
             heading="결론", eyebrow="CONCLUSION",
             details=[{"label": "관리", "body": "..."},
                      {"label": "일정", "body": "..."}])

# 자유 텍스트 (큰 헤더, 라벨 등)
b.text(x=40, y=110, w=300, h=24, content="자유 위치 **굵게**", size=14, bold=True)

# 구분선
b.divider(x=40, y=240, w=640, orange=False)
```

> ★ **모든 콘텐츠 슬라이드에 eyebrow 권장**. 카테고리 라벨로 슬라이드 의미 명확화 (예: PROBLEM / COMPARE / ACTION PLAN / WORKFLOW / STATUS / CONCLUSION).
> 표지(cover)에는 eyebrow 사용 안 함.

토큰은 `import spigen_tokens as T`로 직접 사용 가능.
- `T.CANVAS["margin"]`, `T.SPACING["card_gap"]`, `T.TYPO["heading"]`, `T.color("ORANGE")` 등.

KPI 덱은 `SpigenBuilder(title, template="kpi")`로 생성한다. 표지·마지막 슬라이드는 KPI 전용 템플릿에서 복사.

**mk_* 컴포넌트 props 형식 레퍼런스 (시트 슬롯 정확 일치 시만):**

```python
# mk_compare_rows — 행별 before/after 비교
lib.mk_compare_rows(oid, rows=[
    {"item": "항목명", "before": "기존 상태", "after": "변화/문제"},
], reqs=b.reqs, left_label="기존", right_label="제안",
   is_bilateral=True,   # 대립 구도가 아닌 대등한 분기일 때
   callout="핵심 메시지 한 줄")

# mk_flow_focus — 단계 강조 흐름 (최대 6단계)
lib.mk_flow_focus(oid, steps=[
    {"num": "01", "name": "단계명", "service": "카테고리", "desc": "설명\n두 줄 가능", "primary": True},
], reqs=b.reqs)

# mk_swimlane_mapping — 팀 역할 분담 (최대 3행)
lib.mk_swimlane_mapping(oid, rows=[
    {"left": "팀명", "middle": "액션", "right": "결과/산출물"},
], reqs=b.reqs)

# mk_3col_cards — 독립 항목 3개
lib.mk_3col_cards(oid, cards=[
    {"label": "레이블", "title": "카드 제목", "items": ["항목1", "항목2"], "hot": True},
], reqs=b.reqs, theme="light")

# mk_decision_tree — YES/NO 분기
lib.mk_decision_tree(oid, nodes={
    "input": "입력",
    "decision": "판단 질문?",
    "yes": "YES 결과", "yes_label": "예",
    "no": "NO 결과",  "no_label": "아니오",
    "output": "최종 결과",
}, reqs=b.reqs)
```

**③ Voice Fingerprint 확인 (생성 전 내부 체크)**

헤더·본문 작성 전 아래를 머릿속으로 확인한다:
- 헤더: 명사형 또는 주장형 문장, 10자 이내 권장 ("패키지 리뉴얼 방향" O / "패키지 리뉴얼 방향에 대한 검토" X)
- bullet: 1줄 이내, 슬라이드당 3줄 이하
- 수치가 있으면 수치 먼저, 설명은 다음
- AI 클리셰 없음: 혁신적인·원활한·극대화·시너지·솔루션·최적화 → 구체 수치·사실로 대체
- 원본에 없는 내용 추가 없음

---

## Step 2. 슬라이드 구성 제안

수집한 내용을 바탕으로 슬라이드 구성을 제안한다.

출력 형식:
```
=== 슬라이드 구성 ===

[1] 표지 — (제목)
[2] (슬라이드 제목) — (핵심 내용 1줄)
[3] ...

승인하시면 생성을 시작합니다.
```

슬라이드 수 기준:

| 목적 | 권장 장수 |
|------|----------|
| 빠른 보고 | 4~6장 |
| 교육·안내 | 6~10장 |
| 제안서 | 5~8장 |

슬라이드 유형 선택:

| 상황 | 유형 |
|------|------|
| 일반 내용 | `slide()` — 헤더 + 텍스트박스 |
| Before/After 또는 두 항목 비교 | `two_col()` — 2단 분리 |
| 첫 슬라이드 | `cover()` — 표지 |

컴포넌트를 먼저 정하지 않는다. 내용을 파악한 뒤 유형을 결정한다.

승인 없이 Step 3으로 넘어가지 않는다.

---

## Step 3. 생성

승인된 구성대로 Python 빌드 스크립트를 작성하고 실행한다.

### 기본 빌드 패턴

```python
import sys, shutil

# 필수 파일 복사
for f in ["spigen_build.py", "spigen_lib.py", "spigen_models.py",
          "spigen_layout.py", "spigen_tokens.py"]:
    shutil.copy2(f"/Users/harugury/.agents/skills/spigen-slides/{f}", f"/tmp/{f}")
sys.path.insert(0, "/tmp")

from spigen_build import SpigenBuilder, load_pid, save_pid
import spigen_lib as lib

BUILD_NAME = "my_deck"  # ← in-place 빌드용 PID 캐시 키 (덱마다 고유)

def build(theme):
    lib.set_theme(theme)
    pid = load_pid(BUILD_NAME, theme)
    b = SpigenBuilder("(PPT 제목)", theme=theme, presentation_id=pid)
    if pid is None:
        save_pid(BUILD_NAME, theme, b.pid)

    # [1] 표지 — subtitle 사용 안 함 (V6: 표지 제목 2줄 이내)
    b.cover(title="(제목 1줄)\n(제목 2줄)", date="2026. 05.")

    # [2] 콘텐츠 슬라이드 — eyebrow 항상 명시 (★ 권장)
    b.start_slide(heading="슬라이드 제목", eyebrow="CATEGORY")
    b.card(x=40, y=110, w=200, h=180, label="01", title="...", body="...")
    # ... 추가 빌딩 블록 자유 호출

    # [3] 체크리스트 — eyebrow 권장
    b.checklist(heading="진행 현황", eyebrow="STATUS",
                items=[("항목", True), ...])

    # [4] 결론 (선택, 대부분 안 씀)
    b.conclusion(metric="...", caption="...", heading="결론",
                 eyebrow="CONCLUSION", details=[...])

    ok = b.flush()
    if ok:
        print(f"[{theme}] {'NEW' if pid is None else 'UPDATE'} "
              f"https://docs.google.com/presentation/d/{b.pid}/edit")

build("dark")  # ← default 테마. light는 사용자 명시 시에만.
```

**빌드 표준**
- `theme="dark"` default — light는 사용자가 명시 요청 시에만
- `subtitle` 표지에 사용 안 함 (제목만 2줄 이내)
- 모든 콘텐츠 슬라이드에 `eyebrow` 권장 (카테고리 라벨)
- in-place 모드 (`load_pid` / `save_pid`) — 같은 덱은 같은 URL에 누적 수정
- 빌드 후 페르소나 검수 자동 호출 (default ON, 사용자가 "검수 생략" 명시 시 OFF)

```bash
python3 /tmp/build_<name>.py
```

완료 후:
```
완료: https://docs.google.com/presentation/d/<ID>/edit
```

---

## 슬라이드 구조 규칙

### 표지 (`cover`)
- 배경: 테마 색상
- 왼쪽: 오렌지 세로선 (4pt)
- 제목: 34pt Bold
- 부제: 17pt muted
- 하단: 부서 | 담당자 | 날짜 (11pt muted)

### 본문 (`slide`)
- 배경: 테마 색상
- 헤더: 좌상단 22pt Bold
- 오렌지 가로선: 헤더 아래 (2pt)
- 본문: 14pt, 텍스트박스 전체

### 2단 비교 (`two_col`)
- 헤더 + 오렌지 가로선
- 왼쪽 패널: 제목(오렌지) + 본문
- 세로 구분선 (muted, 1pt)
- 오른쪽 패널: 제목(오렌지) + 본문

---

## 디자인 금지 규칙

> 시각 일관성과 정보 전달력을 무너뜨리는 패턴들. 빌드 전 / 검토 시 반드시 점검.
> 자세한 사양: `spigen_render_rules.md` · `spigen_design_spec.md`

### 1. 색·대비
- ❌ 배경(BG)과 동일한 fill / 선 / 테두리 (검정 위 검정 박스 등)
- ❌ 검정 배경 위 `ACCENT_DIM` 텍스트
- ❌ 검정 배경 위 어두운 오렌지·갈색 톤 텍스트
- ❌ 긴 본문이나 보조 설명을 오렌지 계열 색으로 표기 — 오렌지는 강조 전용
- ❌ `ACCENT_DIM`을 텍스트 색으로 사용 (배경 fill 전용)

### 2. 강조 카드 사용 제한
- ❌ 한 슬라이드에 풀 ORANGE 강조 카드 (`emphasis="full"`) **2개 이상**
- ❌ 모든 슬라이드에 습관적으로 풀 강조 카드 추가
- ❌ 분석 카드와 결론 카드를 **같은 크기·색·밀도**로 나란히 배치 (위계 무너짐)
- ❌ 색만으로 의미 전달 (`color-only meaning`) — 형태/위치도 함께 차별화

### 3. 카드 구성
- ❌ 카드 안에 강조용 sub-box 삽입 (박스 안 박스) — `emphasis` 토큰으로 대체
- ❌ 비대칭 혼합 — 같은 슬라이드에 크기·비율 다른 카드 무근거 혼재
- ❌ 한 슬라이드에 카드 유형 3종 이상 (1~2종 권장)
- ❌ 동일 카드 5개 이상 단순 반복 (밀도만 채움, 위계 평평)

### 4. 레이아웃
- ❌ 720 × 405pt 캔버스 밖으로 shape / 텍스트박스 / chart 가 나가는 상태
- ❌ 콘텐츠 영역 (`y = 100 ~ 373`) 초과
  - 위 빈 여백 32pt (slide top → eyebrow 시작 y=32)
  - 아래 빈 여백 32pt (콘텐츠 끝 y=373 → slide bottom y=405) — **대칭 유지**
- ❌ 눈대중 위치 조정 — 토큰값(margin 36/40, gap 8/12 등) 사용
- ❌ 빈 도형·장식 구분선으로 공간 채우기 — 내용이 적으면 단순화
- ❌ 카드 안 제목 위에 붙고 아래 여백만 과하게 남는 상태

### 5. 타이포·콘텐츠
- ❌ Noto Sans / Pretendard / Proxima Nova 외 폰트
- ❌ AI 클리셰 — 혁신적인·원활한·극대화·시너지·솔루션·최적화·스마트한·강력한·게임체인저
- ❌ 함수명 / 파일명 / 변수명 직접 기재 (`mk_flow()`, `spigen_lib.py` 등)
- ❌ 사내 약어·코드명 슬라이드 표기 (외부 청중인 경우)
- ❌ Gradient text / 장식용 glassmorphism 기본 적용

### 6. 위계·리듬
- ❌ Hierarchy 평평한 구성 (모든 카드가 같은 강도)
- ❌ Spacing rhythm 없는 균일 패딩
- ❌ 같은 의미 역할인데 형태가 다름 / 다른 의미 역할인데 형태가 같음
- ❌ 장식 목적의 색상·형태 변형 (의미가 형태를 결정한다)

### 7. 불렛
- ❌ Compact card / small rule card / 3-column card 안에 native paragraph bullets
- ✅ 카드 계열은 텍스트 마커 (`■`, `▶`, `•`) 직접 입력
- ✅ 넓은 본문 영역에서만 `paragraph_bullets` 호출 허용
- ❌ 불렛이 첫 줄보다 위에 떠 있는 상태

### 8. 차트
- ❌ 그라디언트 fill / 3D / 과도한 애니메이션 차트
- ❌ 여러 KPI 수치를 동등하게 나열 — 핵심 1개를 큰 숫자로 분리

### 9. 슬라이드 메시지
- ❌ 한 슬라이드에 경쟁하는 주 메시지 2개 이상
- ❌ 공간 채우기 목적의 콘텐츠 추가 (여백 우선)
- ❌ 제목이 묘사형 (`성능 비교`) — 주장형 권장 (`성능이 30% 향상됐다`)

---

## 페르소나 검수 (필수 자동 호출)

> ★ **모든 빌드 후 즉시 자동 진행 — 사용자가 명시 거부하지 않은 모든 케이스에 강제 적용.**
> 빌드 완료 메시지 출력 후 다음 응답에서 곧바로 페르소나 검수 단계로 진입한다.
> "다음 작업 알려주세요" 같은 대기 응답으로 끝내지 않는다.

### 빌드 직후 강제 동작

```
[1] 빌드 결과 URL 출력
[2] 즉시 → 3종 페르소나 검수 자동 진행 (별도 사용자 요청 없이)
    - 검수 대상: 빌드 출력의 PPT URL
    - 검수 기준: 본 SKILL.md 페르소나 검수 섹션 + spigen_subagent_prompts.md 영역 매트릭스
    - 자동 강제 룰(컬러·좌표·폰트 위계·콘텐츠 영역·표지 2줄)은 빌더 코드가 처리 — 페르소나는 텍스트·메시지·청중 차원만 검수
[3] 의견 종합 + 충돌 시 사용자 1회 문의
[4] 1회 통합 수정 → 종료
```

### 검수 생략 트리거 (사용자 명시 시에만 OFF)

다음 표현이 사용자 메시지에 명시적으로 있어야만 OFF:
- "검수 생략", "검수 안 해도 돼", "skip review", "검수 빼고"

→ 위 표현이 없으면 **반드시 자동 검수 진행**. "잘 됐는지 보세요" 같은 모호한 표현으로 검수 생략하지 않는다.

### 4조건 운영 룰 (반드시 준수)

```
① 관찰만 — 수정안 강제 X
   페르소나는 "이 부분이 [관점]에서 어색하다" 형태로 관찰만 출력.
   "이렇게 바꿔라" 같은 강제 수정안 금지.

② 우선순위 명시 — 자동 룰 > 페르소나 의견 > 사용자 명시
   디자인 금지 규칙(spigen_render_rules)과 페르소나 의견 충돌 시
   자동 룰이 항상 우선. 페르소나 의견은 자동 룰을 위반하지 않는 범위 내에서만 채택.

③ 1회 호출 + 1회 통합 수정 + 종료
   페르소나 호출 → 의견 종합 → 1회 일괄 수정 → 종료.
   수정 후 페르소나 재호출 금지 (반복 루프 방지).

④ 충돌 항목은 사용자에게 1회 문의 (옵션)
   페르소나 의견이 서로 충돌하고 자동 룰로도 결정 못하면
   사용자에게 1회 문의 후 결정. 메인 에이전트 임의 결정 금지.
```

### 페르소나 종류 (`spigen_subagent_prompts.md` 참조)

- **기획자** — 메시지 구조·내용 일관성 검수
- **디자이너** — 시각 위계·여백·정렬 검수
- **대상(청중)** — 청중 관점 이해도·전달력 검수

### 영역 매트릭스 (영역 혼동 금지)

| 검수 항목 | 기획자 | 디자이너 | 청중 |
|---|:---:|:---:|:---:|
| 슬라이드별 핵심 메시지 | ★ | | |
| 메시지 일관성 / 카테고리 라벨링 | ★ | | |
| 정보 흐름 / 시간 순서 / 인과관계 | ★ | | |
| 콘텐츠 적합도 / 슬롯 매칭 | ★ | | |
| 시각 위계 (강조 카드, 폰트 크기) | | ★ | |
| 좌표 일관성 / 정렬 / 여백 | | ★ | |
| **카드 내부 정렬·시각 균형** (텍스트가 카드 가운데에 보이는가) | | ★ | |
| **페이지 간 폰트 위계 일관성** (한 페이지만 갑자기 폰트 큼/작음 검출) | | ★ | |
| **최소 변경 원칙** (작은 여백은 좌표만 미세 조정, 레이아웃 자체 바꾸지 말 것) | | ★ | |
| 색상 / 톤 / 디자인 시스템 적합성 | | ★ | |
| 타이포 / line spacing / 가독성 | | ★ | |
| 첫인상 / 즉시 이해 가능성 | | | ★ |
| 용어 적절성 / 전문 용어 부담 | | | ★ |
| 전달력 / 청중 입장 |  |  | ★ |

> 메인 에이전트는 검수 종합 시 위 매트릭스대로 의견을 분류한다.
> 영역 혼동(예: "헤더 좌표 일관성"을 기획자에게 묻기) 금지.

### 흐름 (기본 ON)

```
빌드 완료 (spigen_build.py 실행 후)
  ↓
[1] PPT 생성 확인 (완료 링크 추출)
[2] 3종 페르소나 동시 호출 (병렬, 관찰만)
[3] 메인 에이전트가 의견 종합 + 충돌 해결
    - 자동 룰 위반은 즉시 수정
    - 페르소나만의 의견은 자동 룰 위반 없으면 채택
    - 충돌 시 사용자 1회 문의
[4] 1회 통합 수정 (필요 시) → 종료
```

### 검수 생략하기 (사용자가 명시 거부할 때)

기본값은 **자동 검수 ON**입니다. 다음 표현으로 검수를 건너뜁니다:
- "검수 생략", "검수 안 해도 돼", "skip review", "검수 빼고"

---

## 레퍼런스

| 파일 | 용도 |
|------|------|
| `spigen_build.py` | 슬라이드 빌더 (cover / slide / two_col / start_slide / 빌딩 블록 / 자동 강제 룰) |
| `spigen_lib.py` | mk_* 컴포넌트 라이브러리 + THEME_TOKENS |
| `spigen_tokens.py` | 디자인 토큰 (HEADER / SHEET_GEOM / SPACING / TYPO / FONT_HIERARCHY / EMPHASIS) |
| `spigen_subagent_prompts.md` | 페르소나 검수 프롬프트 + 영역 매트릭스 |
| `spigen_review_checklist.md` | 빌드 후 점검 체크리스트 |
| `spigen_planning.md` | Step 1~2 기획 가이드 |
| `spigen_execution.md` | Step 3 실행 코드 템플릿 |
| `spigen_component_gallery.md` | 컴포넌트 인벤토리 |

> 디자인 룰은 빌더 코드(`spigen_build.py` / `spigen_lib.py` / `spigen_tokens.py`)가 자동 강제. 코드로 못 잡는 텍스트·메시지·청중 차원 룰만 `SKILL.md` 디자인 금지 9카테고리 + `spigen_subagent_prompts.md` 페르소나 영역 매트릭스에 명시.
