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


## 컴포넌트 선택

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


## 제작 원칙

### 카피 작성 원칙 (slides-grab 기준)

- **슬라이드당 하나의 메시지**: 경쟁하는 블록 금지
- **3~5초 스캔 가능하게**: 본문 글머리는 3줄 이내
- **제목은 주장형 문장**: "성능 비교" → "성능이 30% 향상됐다"
- **섹션 구분 슬라이드**: 번호 + 짧은 제목만, 설명 없음
- **여백 우선**: 공간을 채우려 하지 말 것


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

## 레퍼런스 파일

| 파일 | 내용 | 호출 시점 |
|-----|-----|---------|
| `spigen_lib.py` | 컴포넌트 A~L Python 코드 | 슬라이드 생성 시 `cp` 후 import |
| `spigen_planning.md` | Step 1~2 기획·구성 계획 | 전체 PPT 제작 시작 시 |
| `spigen_execution.md` | Step 3 API 실행 코드 | 실제 Google Slides 생성 시 |
| `spigen_design_spec.md` | 슬라이드 유형별 시각 규격 | HTML 디자인 생성 시 |
