# spigen_render_rules.md — 렌더링·디자인 규칙 레퍼런스
> 슬라이드를 실제로 생성·편집할 때 참조하는 hard rule 모음.
> 기획·구성 → `spigen_planning.md` | API 실행 → `spigen_execution.md`

---

## 1. 색상 시스템

### 현재 템플릿 색상 토큰

이 스킬은 기존 라이트/웜 혼합 디자인을 사용하지 않는다.
모든 신규 생성 슬라이드는 사용자가 만든 Google Slides 템플릿과 같은 **다크 기반**으로 생성한다.

| 토큰 | 값 | 용도 |
|-----|----|------|
| `BG` | `#000000` | 슬라이드 배경 |
| `SURFACE` | `#0E0E0E` | 카드·표·단계 박스 |
| `SURFACE_HI` | `#161616` | 강조 카드 |
| `BORDER` | `#202020` | 카드 테두리 |
| `TEXT` | `#F0F0F0` | 제목·주요 본문 |
| `TEXT_DIM` | `#AAAAAA` | 보조 설명 |
| `TEXT_FAINT` | `#6E6E6E` | 페이지 번호·푸터·라벨 |
| `ACCENT` | `#FF6B1A` | 강조선·번호·도입 후·화살표 |
| `ACCENT_DIM` | `#3D1A05` | 오렌지 틴트 카드 |

**출력 원칙:**

| 유형 | 기본 스타일 |
|-----|------------|
| cover | 템플릿 복사 후 텍스트 교체 |
| section-divider | 다크 배경 + 대형 오렌지 번호 |
| compare | 좌측 어두운 카드 / 중앙 화살표 / 우측 오렌지 틴트 카드 |
| flow | 6단계 카드. 기본형에서는 하단 오렌지 강조 박스 없음 |
| roadmap | 3단계 Phase 카드 + KPI |
| quote | 다크 배경 + 큰 인용문 |
| 추가 content | `spigen_lib.py` 다크 컴포넌트 사용 |

### 색상 비율 원칙 (60-30-10)

| 비율 | 역할 | 적용 토큰 |
|-----|-----|---------|
| 60% | 슬라이드 배경 | `BG #000000` |
| 30% | 중립 텍스트·카드 | `SURFACE`, `TEXT`, `TEXT_DIM` |
| 10% | 강조 포인트 | `ACCENT #FF6B1A` — 번호, 화살표, 현재 지점, 개선 영역 |

> `#FF6B1A`은 한 슬라이드당 **3개 이하** 요소에 사용한다. 과용하면 브랜드 강조 효과가 희석된다.

### 테마 원칙

현재 템플릿은 다크 테마 하나로 통일한다. 단조로움은 배경색 교차가 아니라 아래 요소로 해결한다.

- 카드 밀도 조절
- 오렌지 틴트 카드 수 제한
- 섹션 구분 / 비교 / 플로우 / 로드맵 / Quote 레이아웃 교차
- 푸터와 페이지 라벨 일관 유지

---

## 2. 가시성 & 대비 규칙

### 가시성 안전 규칙

배경색(`BG #000000`)과 같은 색의 선, 박스, 카드가 생성되면 안 된다.

금지:

```txt
검정 배경 위 검정 박스
검정 배경 위 검정 선
배경과 구분되지 않는 테두리
```

원칙:

```txt
중립 박스 → SURFACE / BORDER
중립 선 → BORDER_HI 또는 ORANGE
강조 박스 → ACCENT_DIM / ORANGE
```

라이브러리에서 배경색과 동일한 fill/outline 조합이 들어오면 자동으로 visible token으로 보정한다.

### 텍스트 대비 규칙

검정 배경 위에는 **진한 화색(어두운 오렌지/갈색 계열) 텍스트를 사용하지 않는다.**

원칙:

```txt
긴 문장 / 보조 설명 / 라벨
→ TEXT_DIM 또는 TEXT_FAINT

강조 키워드 / 번호 / 짧은 포인트
→ ACCENT

금지
→ ACCENT_DIM 텍스트
→ 검정 배경 위 저채도/저명도 화색 텍스트
```

---

## 3. 타이포그래피 규칙

### 폰트 패밀리

| 항목 | 값 |
|-----|---|
| 영어 폰트 | `Proxima Nova` |
| 한글 폰트 | `Noto Sans` |
폰트 적용 규칙:
- 한글이 포함된 텍스트 → `Noto Sans`
- 한글이 없는 모든 텍스트(영문/숫자/레이블) → `Proxima Nova`
- 모든 생성 텍스트는 `7pt` 미만으로 내리지 않는다

### 타입 스케일 (type scale remap)

이 스킬은 단순 `font >= 7pt` floor만 쓰지 않는다.
작은/중간 텍스트 계층 전체를 같이 올리는 **type scale remap**을 사용한다.

기본 매핑:

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

원칙:

```txt
최소값만 올려서 계층 비율을 깨지 않는다.
작은 글자가 커지면, 그 주변 보조 계층도 같이 비례 조정한다.
```

---

## 4. 레이아웃 & 공간 규칙

### 캔버스

```txt
720 × 405pt · 마진 36pt · Google Slides 16:9
```

### 박스 내부 여백 규칙

카드/박스 안에서 텍스트 그룹은 기본적으로 위쪽에 몰지 않는다.

원칙:

```txt
텍스트 영역 높이를 x라고 할 때
위/아래 여백 각각이 x보다 작아지는 tight 상태에서는
텍스트 그룹을 세로 중앙 기준으로 다시 배치한다.
```

간격 계층:

```txt
카드 안: outer padding > title/body gap > body/body gap
슬라이드 전체: slide outer margin > block gap > card inner gap
```

금지:

```txt
카드 안에서 제목이 위에 붙고 아래 여백만 과하게 남는 상태
카드 안에서 텍스트 묶음이 박스 경계에 치우친 상태
```

### 박스 안에 박스 금지

강조를 위해 카드 내부에 작은 박스를 하나 더 넣지 않는다.

금지:

```txt
lane 안에 accent box 삽입
card 안에 또 다른 강조 박스 삽입
관계 라벨을 작은 박스로 다시 감싸기
```

대신 아래 방식으로 강조한다:

```txt
보더 색 / 라벨 색 / 커넥터 색 / 텍스트 굵기·색
```

---

## 5. 컴포넌트 규칙

### 불렛 규칙

불렛 포인트는 점/사각형과 텍스트를 따로 눈대중 배치하지 않는다.

원칙:

```txt
불렛과 텍스트를 하나의 row로 계산한다.
불렛은 텍스트 첫 줄 영역의 세로 중심에 맞춘다.
```

카드 계열 적용:

```txt
small card = bullet 금지
compact info card = bullet 금지
wide text block only = native paragraph bullets 허용 가능
```

### Flow 카드 자동 재계산

`mk_flow_focus()`는 아래를 자동 계산해야 한다.

```txt
- STEP 라벨 줄수 / 높이
- title 줄수 / 높이
- service 줄수 / 높이
- 카드 높이
- 내부 상하 여백
- title ↔ service 간격
```

즉:

```txt
텍스트가 내려오면 카드 높이와 내부 간격이 같이 재계산되어야 한다.
폰트만 키우고 카드 크기를 그대로 두면 안 된다.
```

### Structure 페이지 규칙

structure page는 여전히 diagram family only이다.
Google Slides native connector는 정밀 제어가 약하므로:

```txt
native BENT connector를 기본값으로 쓰지 않는다.
필요하면 manual orthogonal routing 또는 커넥터 최소화 방향을 우선한다.
```

최근 기준:

```txt
구조 설명은 배치와 그룹핑으로 읽히게 한다.
모든 관계를 선으로 설명하려 하지 않는다.
선은 입력→main→engine→output 같은 핵심 흐름에만 제한적으로 사용한다.
```

### Mapping 페이지 규칙

```txt
모든 divider / bar / 의미 요소는 카드 내부에 있어야 한다.
카드 밖 gutter 영역에 의미 있는 선이나 바를 남기지 않는다.
```

### Dense appendix table 규칙

`mk_kpi_status_detail()`은 보고용 부록/상세 가이드에서 쓰는 dense table component다.

원칙:

```txt
상단 = KPI 요약 표
하단 = 정의 / 배경 / 측정식 표
두 표 모두 같은 페이지 안에서만 의미를 닫는다.
그룹 헤더 / 컬럼 헤더 / body row 계층을 분리한다.
```

일반화 입력:

```txt
summary_title
summary_groups
summary_headers
summary_rows
detail_title
detail_headers
detail_rows
```

강제 선택 규칙:

```txt
입력 내용에 KPI / 목표 / 실적 / 달성률 / 가중치 / 측정산식 / 증빙 성격이 있으면
rule grid / 일반 report table 로 풀지 말고
mk_kpi_status_detail()을 우선 사용한다.
```

생성 원칙:

```txt
실제 업무 디테일을 과도하게 복사하지 않는다.
형태와 컬럼 구조를 유지하고,
세부 문구는 그럴듯한 예시 수준으로 정리한다.
```

### 선 / 커넥터 / divider 사용 기준

```txt
의미가 있는 연결선 / 흐름 화살표 / 분기선
→ Google Slides native line / connector 사용

표 구분선 / 카드 divider / 장식용 짧은 선
→ 얇은 rectangle 사용
```

커넥터는 `createLine` + `updateLineProperties(startArrow/endArrow)`로 처리한다.
**커넥터는 line object, divider는 thin rectangle**이 기본 규칙이다.

### Cover 정책

```txt
표지는 고정 자산이다.
내지 교체/재생성은 가능하지만 cover는 기본적으로 유지한다.
```

---

## 6. 강조 규칙

### 페이지별 의미 강조 원칙

한 페이지 안에는 보는 사람이 바로 잡아야 할 **의미 강조점 1개**가 있어야 한다.
단, 이 강조점이 항상 100% 오렌지 카드일 필요는 없다.

강조 선택 전 반드시 아래 질문에 답한다:

```txt
이 페이지에서 보는 사람이 가장 먼저 이해해야 하는 한 가지는 무엇인가?
이 항목을 강조하지 않으면 페이지 의도가 흐려지는가?
왜 이 항목이 다른 항목보다 중요한가?
```

세 질문에 답하지 못하면 억지로 강조하지 않는다.

우선순위:

```txt
1. 결론 / 요약
2. 사용자가 상호작용해야 하는 지점
3. 금액 / 비용 / 운영비
4. 입력값
5. 출력값
6. 판단 기준 / 상태 전환 지점
```

표현 방식:

```txt
일반 강조 → ACCENT_DIM 카드, 오렌지 보더, 오렌지 라벨, 오렌지 숫자
결론/요약 강조 → 필요한 경우에만 100% 오렌지 카드
```

컴포넌트별 적용:

```txt
mk_3col / mk_3col_cards → 가장 중요한 카드 1개에 accent: true
mk_flow → 상호작용 포인트, 입력, 출력, 판단 단계 중 1개에 accent: true
mk_kpi_dashboard → 가장 중요한 KPI 1개에 accent: true
mk_report_table → 금액/결과/출력 row 1개에 accent: true
mk_conclusion_detail → 결론 문장 자체가 강조점
```

금지:

```txt
한 페이지에 아무 강조점도 없이 모든 카드가 같은 밀도로 보이는 상태
여러 요소를 동시에 같은 강도로 강조하는 상태
단순히 예뻐 보이게 하려고 임의로 강조하는 것
동등한 모듈/항목 중 하나를 근거 없이 강조하는 것
```

### 100% 오렌지 카드 사용 제한

`ACCENT #FF6B1A`로 꽉 찬 카드는 **모든 페이지에 넣지 않는다.**

사용 대상:

```txt
그 페이지에서 가장 중요한 결론
그 페이지를 요약하는 한 문장
여러 카드 중 사용자가 명시한 최우선 카드
```

사용 금지:

```txt
모든 페이지마다 습관적으로 100% 오렌지 카드를 넣기
한 페이지에서 KPI 카드 2개 이상을 100% 오렌지로 칠하기
여러 step을 동시에 100% 오렌지로 칠하기
단순 유료/중요/강조 항목을 자동으로 100% 오렌지로 칠하기
분석 카드와 결론 카드를 둘 다 100% 오렌지로 칠하기
```

### 강조 카드 z-order

오렌지 보더 또는 오렌지 라인이 있는 강조 row/card는:

```txt
항상 같은 페이지의 다른 일반 카드보다 위(z-order front)에 있어야 한다.
주황 보더가 인접 row/card의 경계선에 가려지면 안 된다.
```

---

## 7. 의미 구조별 형태 차별화

구성요소의 **내용 역할이 같으면** 같은 형태와 비율을 반복해도 된다.

예:

```txt
KPI 4개 → 같은 크기의 KPI 카드
월별 수치 6개 → 같은 폭의 bar
Phase 3개 → 같은 Phase 카드
```

하지만 구성요소의 **의미 역할이 다르면** 같은 카드 형태를 반복하지 않는다.

| 의미 역할 | 권장 형태 | 색상/비율 |
|----------|----------|----------|
| 분석·근거 | 표, 그래프, 어두운 surface 카드 | `SURFACE` 중심 |
| 핵심 수치 | 큰 숫자 카드, metric panel | 숫자만 크게, 오렌지 강조 |
| 결론·판단 | 독립 callout, 필요 시 100% 오렌지 카드 | `ACCENT #FF6B1A` |
| 액션·다음 단계 | 단계 카드, roadmap 카드 | 기본은 surface, 필요 시 보조 강조 |
| 보조 설명 | 작은 캡션 또는 생략 | 과도한 보조문구 금지 |

**금지:** 분석 카드와 결론 카드를 같은 크기·같은 색·같은 밀도로 나란히 배치하지 않는다.

---

## 8. 컴포넌트 선택 가이드

### 컴포넌트 결정 테이블

서술형 해석 없이 입력 데이터 특성으로 결정론적으로 선택한다.
기획 단계(1-4 아웃라인)에서 이 테이블 기준으로 컴포넌트를 **먼저 확정**하고 이유를 기록한다.
`select_component()` (spigen_lib.py)가 이 결정을 자동으로 수행한다.

| 우선순위 | 조건 | 컴포넌트 | 함수 |
|--------|-----|---------|-----|
| 1 | KPI·실적·달성률·가중치 포함 | kpi-status-detail | `mk_kpi_status_detail()` |
| 2 | 양방향 비교 (현재 vs 이후, Before/After) | compare-rows | `mk_compare_rows()` |
| 3 | 단방향 프로세스 ≤4단계 | flow-focus | `mk_flow_focus()` |
| 4 | 단방향 프로세스 5단계+ | flow | `mk_flow()` |
| 5 | 동일 속성 비교 (속성이 행/열로 정렬 가능) | compare-rows | `mk_compare_rows()` |
| 6 | 상태(완료/진행중/대기) 구분 필요 | split-cards | `mk_split_cards()` |
| 7 | 독립 항목 정확히 3개 | 3col-cards | `mk_3col_cards()` |
| 8 | 독립 항목 1~2개 | split-layout | `mk_split()` |
| 9 | 서술형·순차 설명 (기본값) | text-block | `mk_text_block()` |

우선순위 순서대로 조건을 확인한다. 첫 번째로 일치하는 행의 컴포넌트를 사용한다.

판단 원칙:

```
카드      — 항목이 독립적·동등하고, 비교보다 존재감이 중요할 때 (우선순위 7)
표/분할   — 동일 속성 비교, 상태 파악, 양방향 대조 (우선순위 2·5·6)
텍스트 블록 — 순차적 단계·완료 내역·서술형 설명 (기본값)
```

**mk_split_cards 카드 역할 구분 규칙**

오른쪽 카드 목록에 완료/대기/Next가 섞이는 경우 반드시 구분한다:

```
완료:      라벨 앞 ✅ 접두사
진행중/대기: 라벨 앞 ⏳ 접두사
다음 액션:  primary: True + "→ [동사형]" 형식
```

같은 스타일로 나열하면 안 된다.

---

### 빠른 선택 가이드

| 상황 | 컴포넌트 | 함수 | 기본 테마 |
|-----|---------|-----|---------|
| 표지 / 섹션 구분 | slide-base + section-divider | `slide_base()` / `mk_section_divider()` | dark |
| 목차 (다크 스타일) | contents | `mk_contents()` | dark |
| 목차 | toc | `mk_toc()` | dark |
| 현재→문제→기대효과 3열 비교 | 3-col | `mk_3col()` | dark |
| 핵심 개념 3가지 카드 | 3col-cards | `mk_3col_cards()` | dark |
| 프로세스 / 흐름도 | flow | `mk_flow()` | dark |
| 동작흐름 메인 페이지 | flow-focus | `mk_flow_focus()` | dark |
| 마지막 요약 / 결론→근거 | conclusion-detail | `mk_conclusion_detail()` | dark |
| 레이어 구조도 | arch-layers | `mk_arch_layers()` | dark |
| 모듈 관계 구조도 | arch-orchestrator | `mk_arch_orchestrator()` | dark |
| 분기 / 폴백 구조 | decision-tree | `mk_decision_tree()` | dark |
| 모듈 ↔ 설정 매핑 | swimlane-mapping | `mk_swimlane_mapping()` | dark |
| 텍스트 중심 설명 | text-block | `mk_text_block()` | dark |
| 행 기반 비교 / Before-After | compare-rows | `mk_compare_rows()` | dark |
| 좌우 병렬 일반 레이아웃 | split-layout | `mk_split()` | dark |
| 텍스트 + 우측 카드 스택 | split-cards | `mk_split_cards()` | dark |
| 임팩트 한 줄 메시지 | quote | `mk_quote()` | dark |
| 오렌지+테마색 2색 제목 | title-accent | `mk_title_accent()` | dark |

### Flow / Process 페이지 선택 원칙

```txt
압축형 / 보조 흐름 설명 → mk_flow()
동작흐름이 메인 메시지 → mk_flow_focus() (한 줄 카드)
flow + 비용표 + summary 복합형 → 템플릿 5페이지 참고
```

기본 `mk_flow()` 페이지에는 하단 오렌지 강조 박스를 붙이지 않는다.

하단 callout을 추가해도 되는 경우:

```txt
해당 페이지의 결론/요약 문장이 별도로 필요할 때
사용자가 명시적으로 결론 박스를 요청했을 때
```

### 다이어그램 구성 참고 원칙

1차 레퍼런스: `cathrynlavery/diagram-design` — 밀도, 강조 규칙, 레이아웃 타입만 차용.

차용하는 것:

```txt
낮은 정보 밀도 / accent 1~2개 규칙 / 짧은 라벨 / 넓은 여백
노드 배치 / 허브-스포크 / 입력→처리→출력 / 분기·폴백 / 레이어 / 매핑 구조
```

차용하지 않는 것:

```txt
AWS/GCP/Kubernetes 아이콘
Graphviz 결과 이미지를 슬라이드에 그대로 삽입
클라우드 아키텍처 전용 시각 언어
```

실제 출력은 항상: Google Slides native shape + dark background + surface card + orange accent + editable text

### 디자인 시스템 강제 범위

디자인 시스템 가이드는 **모든 슬라이드의 exact 모양을 강제하는 용도**가 아니다.  
대신 아래 3가지를 강제한다:

```txt
1. 토큰: 색 / 폰트 / 대비 / 여백 계층
2. 컴포넌트 패밀리: 비교 / 프로세스 / 구조도 / 매핑 / KPI / 텍스트 블록
3. 선택 규칙: 어떤 내용에서 어떤 패밀리를 써야 하는지
```

강제하지 않는 것:

```txt
모든 상황에서 동일 슬라이드 레이아웃 재사용
HTML 결과를 Slides에 그대로 변환하는 것
내용 구조가 다른데도 같은 템플릿에 억지로 끼워넣는 것
```

다이어그램용 기본 함수:

```txt
mk_arch_layers()       → 입력/선택/렌더링/출력 같은 계층 구조
mk_decision_tree()     → YES/NO, 자동/수동, 분기/폴백
mk_swimlane_mapping()  → 모듈 ↔ 설정/데이터 관계
```

---

## 9. 텍스트 교체 안전 규칙

Google Slides 템플릿에서 텍스트를 교체할 때 `deleteText → insertText`만 쓰면 기존 스타일이 날아갈 수 있다.
검정 배경에서 `themeColor: DARK1` 텍스트가 들어가면 내용이 있어도 보이지 않는다.

원칙:

```txt
1. 가능하면 replaceAllText 또는 기존 텍스트 범위 교체를 우선한다.
2. deleteText → insertText를 썼다면 반드시 updateTextStyle을 같이 실행한다.
3. 교체 후 주요 텍스트가 TEXT/TEXT_DIM/ORANGE 중 하나인지 검증한다.
4. 템플릿 3/4/5페이지는 타이틀·섹션명·큰 맥락은 유지하고 세부값만 교체한다.
```
