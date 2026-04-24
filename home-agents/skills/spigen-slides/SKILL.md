---
name: spigen-slides
description: Spigen 슬라이드에서 섹션 구분자·도표·TOC·카드 등 특정 컴포넌트가 필요할 때 참조. 전체 PPT 제작 기획 → spigen_planning.md | Google Slides 실행 → spigen_execution.md | 디자인 사양 → spigen_design_spec.md | 컴포넌트 코드 → spigen_lib.py
license: MIT
metadata:
  category: productivity
  locale: ko-KR
  phase: v3
---

# spigen-slides

## 고정값

- 담당자: `한원진 담당`
- 부서: `디자인부문ㅣ패키지디자인팀`
- 템플릿 ID: `1R_z4ZKSbRSe5uQ-uWT6dnmBDTJ7M4yOjbGW_1UfxnEk`
- 콘텐츠 템플릿 ID: `1rh_2NNwM2CeZxFaZFfgoK3s1RAU2SyzZd794480hrVo`
- 로컬 디자인 레퍼런스: `/Users/harugury/Downloads/구글챗봇 ppt`


## Google Slides 생성 정책

### 기본 선택

제안서·시안·CrossCheck Bot·Google Chat Bot류 자료는 **콘텐츠 템플릿 방식**을 우선 사용한다.

```
콘텐츠 템플릿 복사 → 필요한 완성형 슬라이드 유지/복제 → 텍스트 교체 → 부족한 페이지만 ccbot_lib/spigen_lib로 추가
```

완성형 템플릿은 이미 디자인이 잡힌 Google Slides이므로, 새로 그리기보다 **복사 후 텍스트만 교체**하는 것이 1순위다.  
동적 생성이 필요할 때만 `ccbot_lib.py` 또는 `spigen_lib.py`를 사용한다.

### 콘텐츠 템플릿 1~6번 인벤토리

Google Slides `1rh_2NNwM2CeZxFaZFfgoK3s1RAU2SyzZd794480hrVo` 기준:

| 번호 | objectId 예시 | 용도 | 사용 기준 |
|-----|---------------|------|----------|
| 1 | `g9001df85b1_0_0` | 표지 | 제목·부제·담당자·날짜 교체 |
| 2 | `sl_sec01` | 섹션 구분 | 섹션 번호·섹션명 교체 |
| 3 | `g3e018b790e1_0_0` | 현행 vs 도입 후 비교 | Before/After 비교 제안 |
| 4 | `g3e018b790e1_0_197` | 일정·목표·확장 계획 | Roadmap / KPI / Next steps |
| 5 | `g3e018b790e1_0_73` | 프로세스 & 비용 | Flow + 비용 상세 + Summary |
| 6 | `sl_qte1` | Quote / closing callout | 핵심 한 문장 / 비전 문구 |

### CrossCheck Bot류 덱 권장 순서

기본 6장 구성:

```
1. Cover
2. Section Divider
3. 현행 vs 도입 후 비교
4. 일정 · 목표 · 확장 계획
5. 프로세스 & 비용
6. Quote / Closing
```

3장 압축 보고서가 필요하면:

```
1. 현행 vs 도입 후 비교
2. 프로세스 & 비용
3. 일정 · 목표 · 확장 계획
```

이때는 `ccbot_lib.py`의 `ccbot_compare()`, `ccbot_flow()`, `ccbot_roadmap()`을 사용한다.


## 디자인 시스템

| 항목 | 값 |
|-----|---|
| 포인트 컬러 | `#FF6B1A` (RGB: 1.0 / 0.420 / 0.102) |
| 영어 폰트 | `Proxima Nova` |
| 한글 폰트 | `Noto Sans` |

**폰트 적용 규칙**:
- 한글이 포함된 텍스트 → `Noto Sans`
- 영문/숫자 전용 텍스트 → `Proxima Nova`
- 혼합 콘텐츠 → `Noto Sans` (한글 우선)

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

즉, 검정 배경에서 약한 주황/갈색 글자로 분위기만 내지 말고,  
템플릿의 회색 글자 컬러(`TEXT_DIM`, `TEXT_FAINT`)를 보조 텍스트 기준으로 사용한다.

### 의미 구조별 형태 차별화 원칙

구성요소의 **내용 역할이 같으면** 같은 형태와 비율을 반복해도 된다.

예:

```txt
KPI 4개 → 같은 크기의 KPI 카드
월별 수치 6개 → 같은 폭의 bar
Phase 3개 → 같은 Phase 카드
비교 row 5개 → 같은 표 row
```

하지만 구성요소의 **의미 역할이 다르면** 같은 카드 형태를 반복하지 않는다.

예:

```txt
분석 → 결론
문제 → 해결
근거 → 액션
현황 → 제안
수치 → 해석
```

이런 경우에는 아래처럼 형태를 분리한다.

| 의미 역할 | 권장 형태 | 색상/비율 |
|----------|----------|----------|
| 분석·근거 | 표, 그래프, 어두운 surface 카드 | `SURFACE` 중심 |
| 핵심 수치 | 큰 숫자 카드, metric panel | 숫자만 크게, 오렌지 강조 |
| 결론·판단 | 독립 callout, 필요 시 100% 오렌지 카드 | `ACCENT #FF6B1A` |
| 액션·다음 단계 | 단계 카드, roadmap 카드 | 기본은 surface, 필요 시 보조 강조 |
| 보조 설명 | 작은 캡션 또는 생략 | 과도한 보조문구 금지 |

**금지:** 분석 카드와 결론 카드를 같은 크기·같은 색·같은 밀도로 나란히 배치하지 않는다.  
**권장:** 분석은 차분하게, 결론은 명확하게 다르게 보이게 한다.

### 100% 오렌지 카드 사용 제한

`ACCENT #FF6B1A`로 꽉 찬 카드는 **모든 페이지에 넣지 않는다.**

이 카드는 "페이지의 결론/요약 카드"가 명확할 때만 사용한다.  
단순히 `hot`, `accent`, `paid`인 항목은 100% 오렌지가 아니라 보조 강조로 처리한다.

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

두 번째로 중요한 요소는 `ACCENT_DIM`, 오렌지 라인, 오렌지 텍스트만 사용한다.

### 페이지별 의미 강조 원칙

한 페이지 안에는 보는 사람이 바로 잡아야 할 **의미 강조점 1개**가 있어야 한다.  
단, 이 강조점이 항상 100% 오렌지 카드일 필요는 없다.

강조 기준은 발표자가 아니라 **PPT를 확인하는 사람 기준**으로 잡는다.

강조점은 키워드가 아니라 **그 페이지가 존재하는 이유**에서 고른다.  
`입력`, `출력`, `금액`, `모듈명` 같은 단어가 있다고 자동으로 강조하지 않는다.

강조 선택 전 반드시 아래 질문에 답한다:

```txt
이 페이지에서 보는 사람이 가장 먼저 이해해야 하는 한 가지는 무엇인가?
이 항목을 강조하지 않으면 페이지 의도가 흐려지는가?
왜 이 항목이 다른 항목보다 중요한가?
```

세 질문에 답하지 못하면 카드/row/step을 억지로 강조하지 않는다.  
그 경우 제목 문장, 요약 문장, 결론 문장을 더 명확하게 만드는 쪽을 우선한다.

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
중요해 보이는 단어만 보고 실제 핵심이 아닌 요소를 강조하는 것
동등한 모듈/항목 중 하나를 근거 없이 강조하는 것
```


## 컴포넌트 선택

### 컴포넌트 빠른 선택 가이드

| 상황 | 컴포넌트 | 함수 | 기본 테마 |
|-----|---------|-----|---------|
| 표지 / 섹션 구분 | slide-base + section-divider | `slide_base()` / `mk_section_divider()` | dark |
| 목차 (다크 스타일) | contents | `mk_contents()` | dark |
| 목차 | toc | `mk_toc()` | dark |
| 현재→문제→기대효과 3열 비교 | 3-col | `mk_3col()` | dark |
| 핵심 개념 3가지 카드 | 3col-cards | `mk_3col_cards()` | dark |
| 프로세스 / 흐름도 | flow | `mk_flow()` | dark |
| 마지막 요약 / 결론→근거 | conclusion-detail | `mk_conclusion_detail()` | dark |
| 레이어 구조도 | arch-layers | `mk_arch_layers()` | dark |
| 분기 / 폴백 구조 | decision-tree | `mk_decision_tree()` | dark |
| 모듈 ↔ 설정 매핑 | swimlane-mapping | `mk_swimlane_mapping()` | dark |
| 텍스트 중심 설명 | text-block | `mk_text_block()` | dark |
| 좌우 비교 / 병렬 | split-layout | `mk_split()` | dark |
| 텍스트 + 우측 카드 스택 | split-cards | `mk_split_cards()` | dark |
| 임팩트 한 줄 메시지 | quote | `mk_quote()` | dark |
| 오렌지+테마색 2색 제목 | title-accent | `mk_title_accent()` | dark |

### Flow / Process 페이지 선택 원칙

`mk_flow()`는 **생성 플로우, 실행 순서, 처리 단계**를 보여주는 기본 컴포넌트다.

기본 사용:

```txt
상단 제목
6단계 flow 카드
끝
```

기본 `mk_flow()` 페이지에는 하단 오렌지 강조 박스를 붙이지 않는다.  
생성 플로우와 동작흐름은 의미상 거의 같은 내용이므로, 단순 흐름 설명은 `mk_flow()` 하나로 처리한다.

하단 callout을 추가해도 되는 경우:

```txt
해당 페이지의 결론/요약 문장이 별도로 필요할 때
사용자가 명시적으로 결론 박스를 요청했을 때
```

하단 callout을 추가하면 안 되는 경우:

```txt
단순 생성 플로우
단순 실행 순서
프로세스 자체가 이미 핵심 내용인 페이지
```

### 프로세스 + 운영 금액 / 여러 표 조합 기준

동작흐름과 운영 금액처럼 **flow + 비용표 + summary**가 한 페이지에 같이 들어가야 할 때는  
`mk_flow()`만 새로 그리지 말고, 콘텐츠 템플릿 **5페이지 `프로세스 & 비용`**을 우선 참고한다.

사용 기준:

```txt
단순 흐름만 필요 → mk_flow()
흐름 + 비용표 + 운영 금액 + summary 필요 → 템플릿 5페이지 참고/복제
```

템플릿 5페이지를 사용할 때는 큰 제목과 구조는 유지하고, 세부 금액/서비스명/사용량만 교체한다.  
세부 내역을 제거하더라도 페이지 타이틀과 섹션 맥락은 삭제하지 않는다.

### 다이어그램 구성 참고 원칙 (`diagram-design` 우선)

다이어그램 템플릿의 **1차 레퍼런스는 `cathrynlavery/diagram-design`** 으로 잡는다.  
이 레포에서 차용하는 것은 결과물 자체가 아니라 **밀도, 강조 규칙, 레이아웃 타입**이다.

보조 레퍼런스로만 `mingrammer/diagrams`의 구조 문법을 참고할 수 있다.  
아이콘 스타일, 클라우드 provider 그래픽, Graphviz 출력물은 그대로 가져오지 않는다.

차용하는 것:

```txt
낮은 정보 밀도
accent 1~2개만 쓰는 규칙
짧은 라벨
넓은 여백
노드 배치 방식
허브-스포크 관계
입력 → 처리 → 출력 흐름
분기 / 폴백 구조
레이어 구조
모듈 ↔ 설정 / 데이터 매핑 구조
```

차용하지 않는 것:

```txt
AWS/GCP/Kubernetes 아이콘
Graphviz 결과 이미지를 슬라이드에 그대로 삽입
클라우드 아키텍처 전용 시각 언어
```

즉, diagrams는 **레이아웃 문법 참고용**이고 실제 출력은 항상 아래 기준으로 다시 그린다.

```txt
Google Slides native shape
dark background
surface card
orange accent
editable text
```

다이어그램용 기본 템플릿 함수:

```txt
mk_arch_layers()       → 입력/선택/렌더링/출력 같은 계층 구조
mk_decision_tree()     → YES/NO, 자동/수동, 분기/폴백
mk_swimlane_mapping()  → 모듈 ↔ 설정/데이터 관계
```

### 선 / 커넥터 / divider 사용 기준

다이어그램에서 선을 모두 얇은 면(rectangle)으로 처리하지 않는다.

원칙:

```txt
의미가 있는 연결선 / 흐름 화살표 / 분기선
→ Google Slides native line / connector 사용

표 구분선 / 카드 divider / 장식용 짧은 선
→ 얇은 rectangle 사용
```

즉, 아래는 **진짜 선**으로 만든다.

```txt
입력 → 처리 → 출력
YES / NO 분기
모듈 ↔ 설정 관계
사용자 상호작용 방향
```

아래는 **얇은 면(divider)** 으로 둔다.

```txt
표 행 구분선
카드 내부 separator
레이아웃 정리용 수평선
장식용 짧은 바
```

Google Slides API에서 connector는 `createLine` + `updateLineProperties(startArrow/endArrow)` 로 처리한다.  
즉, **커넥터는 line object**, **divider는 thin rectangle** 이 기본 규칙이다.

### 템플릿 텍스트 교체 안전 규칙

Google Slides 템플릿에서 텍스트를 교체할 때 `deleteText → insertText`만 쓰면 기존 스타일이 날아갈 수 있다.  
검정 배경에서 `themeColor: DARK1` 텍스트가 들어가면 내용이 있어도 보이지 않는다.

원칙:

```txt
1. 가능하면 replaceAllText 또는 기존 텍스트 범위 교체를 우선한다.
2. deleteText → insertText를 썼다면 반드시 updateTextStyle을 같이 실행한다.
3. 교체 후 주요 텍스트가 TEXT/TEXT_DIM/ORANGE 중 하나인지 검증한다.
4. 템플릿 3/4/5페이지는 타이틀·섹션명·큰 맥락은 유지하고 세부값만 교체한다.
```


## 제작 원칙

### ⚠️ 내지 장수 제한 (최우선 규칙)

**내지(본문) 슬라이드는 3~4장이 최대다.** cover·closing·toc·section-divider는 카운트에서 제외.

```
cover (1장) + 내지 3~4장 + closing (1장) = 총 5~6장
```

내용이 많아도 이 한도를 넘지 않는다. 넘으면 아래 압축 기술을 적용한다.

### 내용 압축 기술

내지를 줄일 때 아래 순서로 압축한다:

1. **합칠 수 있는 슬라이드 통합**: 유사한 포인트 2장 → 1장 (3col 또는 split으로)
2. **나열 → 카드**: 4개 이상 나열 항목 → `mk_3col()` 3개로 핵심만 추려서 표현
3. **프로세스 압축**: 단계가 많은 흐름 → `mk_flow()` 1장으로 처리
4. **문장 → 키워드**: 본문 설명을 완전한 문장이 아닌 명사구·동사구로 교체
5. **섹션 구분 제거**: 내지 3장 이하면 section-divider 불필요 → 생략

### 카피 작성 원칙 (slides-grab 기준)

- **슬라이드당 하나의 메시지**: 경쟁하는 블록 금지
- **3~5초 스캔 가능하게**: 본문 글머리는 3줄 이내
- **제목은 주장형 문장**: "성능 비교" → "성능이 30% 향상됐다"
- **섹션 구분 슬라이드**: 번호 + 짧은 제목만, 설명 없음
- **여백 우선**: 공간을 채우려 하지 말 것
- **AI 클리셰 금지**: 혁신적인·원활한·극대화·시너지·솔루션·최적화·스마트한·강력한·게임체인저 사용 금지 → 구체적 수치·사실로 대체


### 리뷰 기준 (slides-grab Review Litmus)

구성 확정 전 아래 항목을 점검한다:

- [ ] **내지가 3~4장 이내인가?** (cover·closing·toc·section-divider 제외한 본문 슬라이드 수)
- [ ] 각 슬라이드의 핵심 포인트를 3~5초 안에 파악할 수 있는가?
- [ ] 각 슬라이드에 경쟁하는 블록 없이 하나의 지배적인 메시지가 있는가?
- [ ] 제거해도 의미가 손상되지 않는 카피·배지·콜아웃이 없는가?
- [ ] 섹션 구분 슬라이드가 포스터처럼 간결한가?
- [ ] `#FF6B1A`이 한 슬라이드에 3개 이하 요소에만 사용됐는가?
- [ ] 폰트는 Proxima Nova(영문) / Noto Sans(한글) 두 가지만 사용됐는가?
- [ ] 모든 슬라이드가 현재 템플릿의 다크 배경·오렌지 강조 체계를 따르는가?
- [ ] 섹션 구분 / 비교 / 플로우 / 로드맵 / Quote 등 레이아웃 유형이 적절히 교차되는가?

구성을 사용자에게 보여주고 확인받는다. 


---

## 생성 후 검증 (필수 — 완료 선언 전 반드시 실행)

슬라이드를 생성한 직후, 사용자에게 "완료"를 보고하기 **전에** 반드시 아래 검증 루프를 실행한다.

### 검증 명령

```bash
python3 /Users/harugury/.agents/skills/spigen-slides/spigen_verify.py <PRESENTATION_ID>
```

특정 슬라이드만 검증할 경우:

```bash
python3 /Users/harugury/.agents/skills/spigen-slides/spigen_verify.py <PRESENTATION_ID> <slide_index>
```

### 검증 루프

```
1. 슬라이드 생성 (spigen_lib.py → gws API 실행)
2. spigen_verify.py 실행
3. 결과 확인
   ├─ 모든 체크 PASS → "완료" 보고 가능
   └─ FAIL / MISS 존재 → spigen_lib.py 수정 → 슬라이드 재생성 → 2번으로 돌아감
```

### 검증 기준 (template_spec.json)

- 위치(x, y): ±2.5pt 허용
- 크기(w, h): ±2.5pt 허용
- 폰트 크기: ±0.6pt 허용
- 폰트 패밀리: 정확히 일치
- 감지 컴포넌트: `section_divider`, `flow`, `3col`, `kpi_dashboard`, `quote`, `slide_base`

### 절대 규칙

- `spigen_verify.py` 실행 결과 FAIL/MISS가 하나라도 있으면 **"완료"라고 말하지 않는다.**
- 수정 후 반드시 재생성 + 재검증한다.
- SKIP은 데이터 부재로 건너뜀이므로 FAIL로 취급하지 않는다.


---

## 레퍼런스 파일

| 파일 | 내용 | 호출 시점 |
|-----|-----|---------|
| `spigen_lib.py` | 컴포넌트 A~L Python 코드 | 슬라이드 생성 시 `cp` 후 import |
| `template_spec.json` | 컴포넌트별 위치·크기·폰트 기준값 | 검증 기준 참조 |
| `spigen_verify.py` | 생성된 슬라이드 자동 검증 스크립트 | 슬라이드 생성 직후 실행 |
| `spigen_planning.md` | Step 1~2 기획·구성 계획 | 전체 PPT 제작 시작 시 |
| `spigen_execution.md` | Step 3 API 실행 코드 | 실제 Google Slides 생성 시 |
| `spigen_design_spec.md` | 슬라이드 유형별 시각 규격 | HTML 디자인 생성 시 |
