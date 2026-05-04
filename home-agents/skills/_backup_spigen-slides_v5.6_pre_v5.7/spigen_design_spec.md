# spigen_design_spec.md — Spigen Slide Design System v2

> 기준 템플릿: `1rh_2NNwM2CeZxFaZFfgoK3s1RAU2SyzZd794480hrVo`
> 시스템 가이드 시트: `https://docs.google.com/presentation/d/1HJbTWXPCr38gXDQuarglSLrkheDQXAojlrYUKcfVgAc/edit`
> 캔버스: **720 × 405pt** · Google Slides 16:9
> 방향: **Theme-aware (dark / light) + Orange accent + Native editable shapes**

---

## 1. 설계 원칙

네 가지 원칙이 모든 생성 결정의 기준이다.

**① 템플릿 우선** — 완성형 1~6번 슬라이드를 복사 후 텍스트만 교체한다. 새로 그리기는 마지막 수단이다.

**①-a 테마 규칙** — KPI / 실적 / 상세 수치 보고서는 `light`, 제안서 / 임팩트 중심 발표는 `dark`를 기본값으로 한다.

**② 페이지당 메시지 하나** — 한 슬라이드에 경쟁하는 강조점이 2개 이상 있으면 분리하거나 하나를 제거한다.

**③ 절제된 오렌지** — `ACCENT #FF6B1A`는 한 슬라이드에 3개 이하 요소에만 사용한다. 결론·핵심 수치·상호작용 포인트 이외에는 `ACCENT_DIM` 또는 오렌지 선으로 처리한다.

**④ 의미가 형태를 결정한다** — 같은 의미 역할은 같은 형태로, 다른 의미 역할은 다른 형태로. 장식 목적의 색상·형태 변형은 금지한다.

### 1.1 Cover source of truth

표지는 임의 커스텀 커버가 아니라 아래 기준을 사용한다.

```txt
template ID 1R_z4ZKSbRSe5uQ-uWT6dnmBDTJ7M4yOjbGW_1UfxnEk 의 1페이지
```

즉 기본 cover 는 새 세부 가이드 표지와 동일한 구조를 사용한다.

cover 구조:

- 메인 제목 (필요 시 2줄)
- 하단 좌측: 부서 / 담당자
- 하단 우측: 날짜 / 버전

---

## 2. 색상 시스템

### 2.1 토큰

| 토큰 | 값 | 역할 |
|-----|----|------|
| `BG` | `#000000` | 슬라이드 배경 |
| `SURFACE` | `#0E0E0E` | 카드·표·플로우 박스 (기본) |
| `SURFACE_HI` | `#161616` | 강조 카드 (대비 필요 시) |
| `BORDER` | `#202020` | 일반 테두리 |
| `BORDER_HI` | `#303030` | 강조 테두리·구분선 |
| `TEXT` | `#F0F0F0` | 제목·주요 본문 |
| `TEXT_DIM` | `#AAAAAA` | 설명·보조 텍스트 |
| `TEXT_FAINT` | `#6E6E6E` | 푸터·페이지 번호·라벨 |
| `ACCENT` | `#FF6B1A` | 핵심 강조 (번호·화살표·결론) |
| `ACCENT_DIM` | `#3D1A05` | 오렌지 틴트 카드 배경 |
| `GOOD` | `#9CE37D` | 긍정 지표 |
| `BAD` | `#FF7A7A` | 부정·삭제·위험 |

> Google Slides API는 alpha 채널 미지원. 반투명 오렌지는 `ACCENT_DIM` 솔리드로 근사한다.

### 2.1.a Theme variants

시스템은 **하나의 레이아웃 규칙 + 두 개의 테마 토큰 집합**으로 운영한다.

#### Dark

- `BG`: `#000000`
- `SURFACE`: `#0E0E0E`
- `TEXT`: `#F0F0F0`
- `TEXT_DIM`: `#AAAAAA`
- `TEXT_FAINT`: `#6E6E6E`
- `ACCENT`: `#FF6B1A`
- `ACCENT_DIM`: `#3D1A05`

#### Light

- `BG`: `#F7F7F5`
- `SURFACE`: `#FFFFFF`
- `SURFACE_HI`: `#F1F1ED`
- `BORDER`: `#D9D9D2`
- `BORDER_HI`: `#BFC0B8`
- `TEXT`: `#171717`
- `TEXT_DIM`: `#5F615B`
- `TEXT_FAINT`: `#8A8D84`
- `ACCENT`: `#FF6B1A`
- `ACCENT_DIM`: `#FFE6D6`

원칙:

```txt
dark / light 에서 바뀌는 것은 token 값뿐이다.
폰트 규칙, 간격 규칙, 컴포넌트 선택 규칙은 그대로 유지한다.
```

### 2.2 색상 비율 원칙 (60-30-10)

| 비율 | 역할 | 토큰 |
|-----|-----|------|
| 60% | 슬라이드 배경 | `BG #000000` |
| 30% | 중립 텍스트·카드 | `SURFACE`, `TEXT`, `TEXT_DIM` |
| 10% | 강조 포인트 | `ACCENT #FF6B1A` |

### 2.3 의미별 색상 역할

| 색상 | 의미 역할 |
|-----|---------|
| `SURFACE` | 분석·근거·일반 정보 |
| `ACCENT_DIM` | 보조 강조, 결론 전 단계 중요 정보 |
| `ACCENT` | 결론·최우선 카드·현재 지점·핵심 액션 |
| `TEXT_FAINT` | 라벨·보조 정보 |

### 2.4 Avoid — 색상

- `BG #000000`과 동일한 fill·선·테두리 생성 금지
- 검정 배경 위에 `ACCENT_DIM` 텍스트 사용 금지
- 검정 배경 위에 저채도·저명도 화색(어두운 오렌지/갈색) 텍스트 사용 금지
- 긴 본문·보조 설명을 오렌지 계열로 표기 금지
- 한 슬라이드에 100% 오렌지 카드(`ACCENT` fill) 2개 이상 금지
- 모든 페이지에 습관적으로 100% 오렌지 카드 추가 금지

---

## 3. 타이포그래피

### 3.1 크기 스케일

| 레벨 | 크기 (pt) | 굵기 | 용도 |
|-----|---------|------|------|
| `DISPLAY` | 80~100 | Bold | 섹션 번호·대형 수치 |
| `TITLE` | 22~28 | Bold | 슬라이드 제목 |
| `CARD_TITLE` | 12~14 | Bold | 카드 제목 |
| `BODY` | 7~10 | Regular | 본문·설명 |
| `CAPTION` | 4~7 | Regular/Bold | 단계 번호·푸터·라벨 |

실행 규칙:

```txt
생성 시 실제 적용 font size는 7pt 미만으로 내려가지 않는다.
```

### 3.2 폰트 패밀리

| 폰트 | 용도 |
|-----|------|
| `Noto Sans` | 한글이 포함된 모든 텍스트 |
| `Proxima Nova` | 한글이 없는 영문·숫자·레이블 |

폰트 선택 규칙: 한글 포함 → `Noto Sans` / 그 외 전부 → `Proxima Nova`

### 3.3 Avoid — 타이포그래피

- 위 3종 외 폰트 사용 금지
- 검정 배경 위 긴 문장을 오렌지 계열로 표기 금지
- 보조 설명을 `ACCENT` 색상으로 표기 금지
- `ACCENT_DIM`을 텍스트 색으로 사용 금지

### 3.4 최신 타입 스케일 규칙

현재 스킬은 단순 minimum floor 가 아니라 **type scale remap** 을 사용한다.

| 입력 크기 | 출력 크기 |
|----------|----------|
| 5.5 | 7 |
| 6.0 | 7.5 |
| 6.5 | 8 |
| 7.0 | 7.5 |
| 8.0 | 9.5 |
| 8.5 | 10 |
| 9.0 | 10.5 |
| 11.0 | 12.5 |
| 13.0 | 14.5 |

원칙:

```txt
최소값만 강제로 올려서 계층 비율을 깨지 않는다.
작은 / 중간 텍스트 계층을 같이 재매핑한다.
큰 디스플레이 타이틀은 과도하게 키우지 않는다.
```

---

## 4. 레이아웃 & 공간

### 4.1 캔버스 규격

| 항목 | 값 |
|-----|---|
| 캔버스 | 720 × 405pt (Google Slides 16:9) |
| 마진 | 36pt (좌·우) |
| 헤더 eyebrow | x=36, y=36 |
| 슬라이드 제목 | x=36, y≈54 |
| 짧은 오렌지 바 | x=36, y≈99, w=21, h=1.5 |
| 콘텐츠 시작 | y≈128 |
| 푸터 좌측 | x=36, y≈379 |
| 푸터 우측 연도 | x≈666, y≈379 |

### 4.2 Avoid — 레이아웃

- 배경과 동일한 fill·선·테두리 배치 금지
- 콘텐츠를 공간 채우기 목적으로 추가 금지
- 한 슬라이드에 같은 강도·크기·색으로 동등한 카드 5개 이상 배치 금지
- 720 × 405pt 캔버스 밖으로 shape / text box / chart / diagram node 가 나가는 상태 금지
- 콘텐츠 영역(`y≈128 ~ 381`)을 넘기는 상태 금지

### 4.3 화면 경계 / overflow 규칙

모든 생성 컴포넌트는 아래 bounds 를 만족해야 한다.

```txt
x >= 0
y >= 0
x + width <= 720
y + height <= 405
```

내용 영역 컴포넌트는 추가로:

```txt
y >= 128
y + height <= 381
```

overflow 해결 순서:

```txt
1. 블록 높이 재계산
2. 내부 간격 재분배
3. 행 수 / 카드 수 축소
4. 레이아웃 교체
5. 페이지 분리
```

### 4.4 선 / divider / connector 규칙

| 요소 | 구현 방식 | 용도 |
|-----|---------|------|
| 관계선 / 흐름 화살표 | native `Line` / connector | 방향, 분기, 관계 |
| 표 구분선 / 카드 separator | thin rectangle | 정적 분리 |
| 장식 바 | thin rectangle | 헤더·강조 포인트 |

원칙:

- 방향 의미가 있는 선은 `Line` 객체를 사용한다.
- 화살표가 필요한 경우 `startArrow` / `endArrow`를 설정한다.
- 표·카드·그리드 분리선은 `Line`이 아니라 thin rectangle을 사용한다.
- 대각선·분기선·모듈 연결선은 얇은 면으로 흉내내지 않는다.
- 강조를 위해 카드 내부에 작은 accent box를 하나 더 넣지 않는다.

### 4.5 카드 내부 세로 여백 규칙

카드 안의 제목/설명/보조문구는 하나의 text group 으로 계산한다.

규칙:

```txt
텍스트 그룹 높이 = x
상·하단 padding 이 각각 x보다 작은 tight 상태
→ 텍스트 그룹을 카드 세로 중앙 기준으로 재배치
```

### 4.6 Dense appendix table component

보고용 가이드 / appendix / KPI reference page 에서는 `mk_kpi_status_detail()` 컴포넌트를 사용한다.

구성:

- KPI 요약 group header row
- KPI 요약 column header row
- KPI 요약 body rows (목표 / KPI / 가중치 / 반기 / 연간)
- 하단 섹션 타이틀
- 정의 / 측정산식 / 증빙 상세 표

입력 데이터 구조:

```txt
summary_groups  = [(label, start_col, span), ...]
summary_headers = [col1, col2, ...]
summary_rows    = [
  {
    goal, goal_span?,
    kpi, weight,
    half_target, half_actual, half_rate,
    year_target, year_actual, year_rate
  },
  ...
]

detail_headers  = [col1, col2, col3, col4]
detail_rows     = [
  {kpi, definition, formula, evidence},
  ...
]
```

용도:

- KPI 진행 현황
- 평가 기준표
- 정의 / 선정배경 / 산식 appendix
- dense report형 시스템 가이드 부록

선택 규칙:

```txt
KPI / 목표 / 실적 / 달성률 / 가중치 / 측정산식 / 증빙 성격의 페이지
→ mk_kpi_status_detail() 우선
```

의도:

- 글자 크기를 억지로 줄이기 전에
- 박스 안에서 위아래 여백이 비슷하게 보이도록 만든다

적용 대상:

- flow card
- structure node
- mapping row
- KPI card
- callout card

### 4.6 불렛 정렬 규칙

불렛 리스트는 점/사각형과 텍스트를 별도 장식 요소로 보지 않는다.
하나의 텍스트 row 로 취급한다.

규칙:

```txt
bullet centerY = first-line text area centerY
```

실무 규칙:

- 불렛은 텍스트 첫 줄과 같은 세로 리듬에 맞춘다
- 불렛과 텍스트 시작 간격은 컴포넌트별 고정값을 사용한다
- 줄 간격은 불렛 크기로 보정하지 않는다

금지:

- 불렛이 첫 줄보다 위에 떠 있는 상태
- 불렛이 텍스트 블록 중앙이 아니라 전체 박스 중앙 기준으로 배치되는 상태

적용 원칙:

- compact card / small rule card / 3-column card → 불렛 금지
- 카드 계열에서는 plain text stack 사용
- bullet semantics 가 꼭 필요한 넓은 본문 영역에서만 native paragraph bullets 사용

### 4.7 최신 spacing hierarchy

슬라이드 전체:

```txt
outer margin > block gap > card gap > body line gap
```

카드 내부:

```txt
outer padding > title/body gap > body/body gap
```

대형 카드(대표 카드 / 구조 다이어그램 메인 노드)는
균등 여백이 아니라 아래 기준을 우선 적용한다.

```txt
top-weighted:
top padding < bottom padding
```

반복형 작은 카드(rule grid / compact info card)는:

```txt
balanced:
top padding ≈ bottom padding
```

---

## 5. 컴포넌트 카탈로그

### 5.1 의미 강조 원칙

모든 내용 슬라이드는 **보는 사람이 확인해야 할 핵심 강조점 1개**를 가진다.

강조점 선택 전 질문:
- 이 페이지가 말하려는 한 문장은 무엇인가?
- 이 항목을 강조하지 않으면 페이지 의미가 흐려지는가?
- 왜 이 항목이 다른 항목보다 중요한가?

세 질문에 답하지 못하면 억지로 강조하지 않는다. 대신 제목·요약 문장을 더 명확하게 만든다.

강조 우선순위:
1. 결론 / 요약
2. 사용자 상호작용 포인트
3. 금액 / 비용 / 운영비
4. 입력값
5. 출력값
6. 판단 기준 / 상태 전환

표현 방식:
- 일반 강조 → `ACCENT_DIM` 카드, 오렌지 보더, 오렌지 번호, 오렌지 텍스트
- 결론/요약 강조 → 100% `ACCENT` 카드 (페이지 내 1개만)

의미 흐름별 형태 분리:

| 의미 흐름 | 시각 처리 |
|----------|----------|
| 분석 → 결론 | 분석은 표/그래프(`SURFACE`), 결론은 별도 callout 또는 100% 오렌지 카드 |
| 문제 → 해결 | 문제는 `SURFACE`, 해결은 `ACCENT_DIM` 또는 오렌지 강조 |
| 근거 → 액션 | 근거는 data/table, 액션은 roadmap/step card |
| 수치 → 해석 | 수치는 metric/chart, 해석은 짧은 callout |
| 현황 → 제안 | 현황은 muted card, 제안은 accent card |

### 5.2 최신 컴포넌트 규칙

#### Flow card

`mk_flow_focus()` 는 아래를 자동 계산해야 한다.

```txt
- step label 줄수 / 높이
- title 줄수 / 높이
- service 줄수 / 높이
- max group height
- card height
- 내부 상하 여백
```

금지:

```txt
폰트가 커졌는데 카드 높이와 내부 간격을 그대로 두는 것
step label 이 2줄로 접히는데 1줄 높이 박스를 유지하는 것
```

#### Structure diagram

구조 페이지는 diagram only 이지만, 관계선을 과도하게 남발하지 않는다.

```txt
배치 / 그룹핑 / 근접성으로 구조를 먼저 읽히게 한다.
선은 핵심 흐름만 제한적으로 사용한다.
```

Google Slides native connector 관련:

```txt
native BENT connector 는 정밀 제어가 약하므로 기본값으로 채택하지 않는다.
필요 시 manual orthogonal routing 또는 connector 최소화 전략을 사용한다.
```

#### Mapping page

mapping page 의 divider / bar / 기준선은:

```txt
카드 내부에만 존재해야 한다.
카드 밖 gutter 영역에 의미 있는 선 / 바를 두지 않는다.
```

#### Emphasis z-order

강조 row / 강조 card / 오렌지 보더가 있는 surface 는:

```txt
같은 페이지의 일반 카드보다 항상 위에 있어야 한다.
```

적용 이유:

```txt
accent border / accent line 이 다른 row 경계선에 가려지면 안 된다.
보더는 끊김 없이 보여야 한다.
```

### 5.2 완성형 슬라이드 유형 (1~6)

#### 1. Cover

**용도**: 표지
**Signature Elements**: Spigen 브랜드 레이아웃, 제목, 부제, 담당자·날짜·버전
**생성 방식**: 템플릿 복사 후 텍스트만 교체
**Avoid**: 새 도형 추가, 배경 색상 변경

---

#### 2. Section Divider

**용도**: 섹션 구분
**Signature Elements**: 다크 배경, 좌측 대형 오렌지 번호(100pt), 얇은 세로 구분선, 섹션 라벨 + 제목
**Avoid**: 설명 텍스트 추가, 카드·박스 삽입, 오렌지 외 배경색

---

#### 3. Compare — 현행 vs 도입 후

**용도**: Before/After 비교 제안
**Signature Elements**:
- 좌측: `SURFACE` 카드 (현재 상태)
- 중앙: `›` 오렌지 화살표
- 우측: `ACCENT_DIM` 또는 오렌지 강조 카드 (도입 후)
- 하단: 핵심 결론 1문장 callout

**Avoid**: 5행 초과, 좌우 동일한 색상, 결론 callout 생략

---

#### 4. Roadmap — 일정·목표·확장 계획

**용도**: 로드맵, KPI, 다음 단계
**Signature Elements**:
- 3개 Phase 카드
- 현재 Phase만 오렌지 틴트(`ACCENT_DIM`)
- KPI 또는 연말 리뷰 지표 박스

**Avoid**: Phase 2개 이상 동시 오렌지 강조, 카드당 bullet 4개 초과

---

#### 5. Flow & Cost — 프로세스 & 비용

**용도**: 동작 흐름 + 비용 상세 + summary가 한 페이지에 함께 필요할 때
**Signature Elements**:
- 상단 6단계 step 카드
- 유료/핵심 단계 오렌지 틴트
- 하단 좌측 비용 표
- 하단 우측 비용 summary callout

**Avoid**: 단순 생성 플로우에 이 전체 구조 적용 금지 — flow만 필요하면 `mk_flow()` 단독 사용

---

#### 6. Quote / Closing

**용도**: 비전 문구, 핵심 한 문장, 마감
**Signature Elements**: 다크 배경, 대형 인용부호 또는 오렌지 포인트, 핵심 문장 1개, 출처/비전 문구 1줄
**Avoid**: 메시지 2개 이상, 로고·배지 장식 추가

---

### 5.3 spigen_lib.py 컴포넌트 매핑

| 함수 | 역할 |
|-----|------|
| `slide_base()` | 헤더 포함 다크 콘텐츠 슬라이드 기반 |
| `mk_section_divider()` | 2번 유형 섹션 구분 |
| `mk_quote()` | 6번 유형 Quote / Closing |
| `mk_contents()` / `mk_toc()` | 다크 목차 |
| `mk_3col()` / `mk_3col_cards()` | 다크 3열 카드 |
| `mk_flow()` | 단순 프로세스 카드 (하단 callout 없음이 기본) |
| `mk_flow_focus()` | 동작흐름 메인 페이지용 한 줄 카드 flow |
| `mk_arch_layers()` | 레이어 구조 다이어그램 |
| `mk_arch_orchestrator()` | 모듈 관계 구조 다이어그램 |
| `mk_decision_tree()` | 판단 / 분기 / 폴백 다이어그램 |
| `mk_swimlane_mapping()` | 모듈 ↔ 설정/데이터 스윔레인 매핑 |
| `mk_text_block()` | 다크 본문 카드 |
| `mk_split()` | 좌우 비교 카드 |
| `mk_split_cards()` | 좌측 텍스트 + 우측 카드 스택 |
| `mk_title_accent()` | 오렌지 부분 강조 제목 |
| `mk_kpi_dashboard()` | KPI 수치 카드 그리드 |
| `mk_bar_chart()` | 막대 차트 |
| `mk_report_table()` | 비교 표 (도입 전/후) |
| `mk_callout_message()` | 대형 결론 callout 박스 |
| `mk_conclusion_detail()` | 결론 + 세부 근거 (좌/우 분리) |
| `mk_metric_bar_summary()` | 좌측 KPI 수치 + 우측 막대 차트 |

---

## 6. 카피 원칙

- **슬라이드당 하나의 메시지**: 경쟁하는 블록 금지
- **3~5초 스캔 가능하게**: 본문 글머리는 3줄 이내
- **제목은 주장형 문장**: "성능 비교" → "성능이 30% 향상됐다"
- **섹션 구분**: 번호 + 짧은 제목만, 설명 없음
- **여백 우선**: 공간 채우기 목적의 콘텐츠 추가 금지
- **숫자가 먼저**: 설명은 다음
- **AI 클리셰 금지**: 혁신적인·원활한·극대화·시너지·솔루션·최적화·스마트한·강력한·게임체인저 → 구체적 수치·사실로 대체

---

## 7. Avoid — 절대 금지

### 시각 충돌

- 검정 배경 위 검정 박스·선·테두리
- 검정 배경 위 `ACCENT_DIM` 텍스트
- 검정 배경 위 저명도 화색(어두운 갈색/오렌지) 텍스트
- `deleteText → insertText` 후 `updateTextStyle` 미적용으로 `DARK1` 텍스트 방치

### 오렌지 과용

- 한 슬라이드에 100% 오렌지 카드 2개 이상
- 모든 페이지마다 습관적으로 100% 오렌지 카드 삽입
- 동등한 step·항목 여러 개를 동시에 오렌지 강조
- 단순 유료/중요 태그를 자동으로 100% 오렌지 처리

### 강조 오남용

- 한 페이지에 강조점 2개 이상을 같은 강도로 표시
- 동등한 모듈·파일·항목 중 하나를 근거 없이 강조
- 보조 문구를 여러 줄 넣어 결론의 힘을 약하게 만드는 것

### 레이아웃 오류

- 단순 flow 페이지에 하단 오렌지 강조 박스 습관적 추가
- 분석 카드와 결론 카드를 같은 크기·색·밀도로 나열
- 수치 카드와 해석 문장을 같은 카드 안에 과하게 혼합

### 다이어그램

- AWS/GCP/Kubernetes 아이콘 직접 사용
- Graphviz 결과 이미지 슬라이드에 삽입
- 클라우드 아키텍처 전용 시각 언어 그대로 차용

---

## 8. 리뷰 체크리스트

### 시각 안전

- [ ] 모든 슬라이드가 `#000000` 배경을 따른다.
- [ ] 배경색과 동일한 fill·선·테두리가 없다.
- [ ] 검정 배경 위 `ACCENT_DIM` 텍스트가 없다.
- [ ] 텍스트 교체 후 검정 배경 위 검정 텍스트가 없다.

### 오렌지 절제

- [ ] `ACCENT #FF6B1A`이 한 슬라이드에 3개 이하 요소에만 사용됐다.
- [ ] 100% 오렌지 카드는 결론/요약 카드가 명확한 경우에만 1개 사용됐다.
- [ ] 단순 flow 페이지에 하단 오렌지 강조 박스를 습관적으로 추가하지 않았다.

### 메시지 집중

- [ ] 각 슬라이드에 보는 사람 기준의 의미 강조점이 1개 있다.
- [ ] 강조 기준이 결론·상호작용·금액·입력·출력·판단 기준 중 하나로 설명 가능하다.
- [ ] 강조 대상이 페이지의 핵심 주장과 직접 연결된다.
- [ ] 동등한 모듈/항목 중 하나가 근거 없이 강조되지 않았다.

### 가독성

- [ ] 표·플로우·로드맵의 텍스트는 3~5초 안에 읽힌다.
- [ ] 폰트는 Noto Sans / Proxima Nova 두 가지만 사용됐다.
- [ ] 모든 요소가 Google Slides에서 직접 수정 가능한 텍스트/도형이다.

### 구성

- [ ] 내지 슬라이드는 3~4장 이내다 (cover·toc·section-divider 제외).
- [ ] 섹션 구분 / 비교 / 플로우 / 로드맵 / Quote 등 레이아웃 유형이 적절히 교차됐다.
- [ ] flow + 비용표 + summary가 필요한 복합 페이지는 템플릿 5번 구조를 참고했다.
