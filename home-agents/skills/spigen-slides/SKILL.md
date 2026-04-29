---
name: spigen-slides
description: "PPT 만들어줘 / 피피티 만들어줘 / 장표 만들어줘 / 슬라이드 만들어줘 / 발표자료 만들어줘 / 프레젠테이션 만들어줘 / 보고서 슬라이드 만들어줘 / 덱 만들어줘 등 슬라이드 생성 요청 시 발동. Spigen 내부용 Google Slides 자동 생성 스킬 - 브랜드 디자인 규칙을 적용하여 발표 시간을 줄이고 디자인 일관성을 유지하기 위해 사용. Spigen 슬라이드에서 섹션 구분자·도표·TOC·카드 등 특정 컴포넌트가 필요할 때도 참조. 전체 PPT 제작 기획 -> spigen_planning.md | Google Slides 실행 -> spigen_execution.md | 디자인 사양 -> spigen_design_spec.md | 렌더링 규칙 -> spigen_render_rules.md | 컴포넌트 코드 -> spigen_lib.py"
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
- cover source of truth: `1R_z4ZKSbRSe5uQ-uWT6dnmBDTJ7M4yOjbGW_1UfxnEk` 의 1페이지 (새 세부 가이드 표지와 동일 기준)
- 시스템 가이드 시트: `https://docs.google.com/presentation/d/1HJbTWXPCr38gXDQuarglSLrkheDQXAojlrYUKcfVgAc/edit`
- 로컬 디자인 레퍼런스: `/Users/harugury/Downloads/구글챗봇 ppt`


## Google Slides 생성 정책

### 외부 디자인 스킬 통합 원칙

설치된 외부 디자인 스킬은 `spigen-slides`를 대체하지 않는다.  
역할은 아래처럼 **보조 엔진**으로만 제한한다.

```txt
ckm-slides     = 레이아웃 패턴 추천기
ui-ux-pro-max = 디자인 규칙 / 안티패턴 사전
impeccable    = 결과물 critique / polish 검수 엔진
```

금지:

```txt
ckm-slides가 만든 HTML을 최종 결과물로 채택
ui-ux-pro-max를 슬라이드 직접 생성기로 사용
impeccable을 컴포넌트 선택기로 사용
```

원칙:

```txt
최종 생성은 항상 spigen_preview.py + spigen_lib.py
외부 스킬은 planning / rules / review 단계에만 개입
```

### 신규 기본 원칙 (중요)

이제 `HTML -> Slides 변환`을 source of truth로 사용하지 않는다.

```txt
source of truth = SlideSpec + ComponentSpec
preview = spigen_preview.py
final delivery = spigen_lib.py / Google Slides API
```

즉 HTML은 미리보기 렌더러이고, Google Slides와 **같은 spec**을 소비해야 한다.

### huashu-design 이식 원칙

`huashu-design`에서 가져온 것은 아래 3개만 사용한다.

```txt
1. preview stage shell
2. preview playwright verify
3. export / verify / review 분리 사고방식
```

가져오지 않는 것:

```txt
1. HTML을 최종 truth로 두는 철학
2. HTML -> PPTX를 메인 납품 경로로 두는 방식
3. 문서 규칙만으로 품질을 통제하는 방식
```

### 기본 선택

제안서·시안·CrossCheck Bot·Google Chat Bot류 자료는 **콘텐츠 템플릿 방식**을 우선 사용한다.

```
콘텐츠 템플릿 복사 → 필요한 완성형 슬라이드 유지/복제 → 텍스트 교체 → 부족한 페이지만 ccbot_lib/spigen_lib로 추가
```

완성형 템플릿은 이미 디자인이 잡힌 Google Slides이므로, 새로 그리기보다 **복사 후 텍스트만 교체**하는 것이 1순위다.
동적 생성이 필요할 때만 `ccbot_lib.py` 또는 `spigen_lib.py`를 사용한다.

### 표지 규칙

표지는 별도 실험 버전이나 커스텀 cover를 쓰지 않고, 아래 기준으로 고정한다.

```txt
cover source = 템플릿 ID 1R_z4ZKSbRSe5uQ-uWT6dnmBDTJ7M4yOjbGW_1UfxnEk 의 1페이지
```

즉 `/spigen-slides`로 생성하는 모든 덱은 기본적으로 **새 세부 가이드와 동일한 표지 구조**를 사용해야 한다.

표지 텍스트 계층:

- 제목: 메인 제목 / 필요 시 2줄
- 하단 좌측: 부서 / 담당자
- 하단 우측: 날짜 / 버전

표지 생성 시 커스텀 표지를 새로 그리기보다, 위 템플릿 표지를 복사한 뒤 텍스트만 교체하는 것을 우선한다.
preview / sample deck 처럼 템플릿 cover 를 직접 복사하지 않는 경우에는 반드시 `mk_cover()` helper 를 사용한다.

### 테마 선택 규칙

라이브러리는 이제 **분리된 테마 토큰**을 가진다.

```txt
lib.set_theme('dark')
lib.set_theme('light')
```

원칙:

- 레이아웃 규칙은 dark / light 에서 동일하게 유지한다.
- 바뀌는 것은 색상 토큰뿐이다.
- 폰트 규칙, spacing 규칙, validator 규칙은 테마와 무관하게 동일하다.
- planning 단계에서 theme를 묻고, execution 단계에서 `lib.set_theme(theme)`로 주입한다.

### 화면 밖 요소 금지

모든 shape / text box / card / chart / diagram node는 720 × 405pt 캔버스 안에 있어야 한다.

실행 규칙:

```txt
1. 먼저 콘텐츠 영역 높이를 계산한다.
2. 현재 페이지에 안 들어가면 컴포넌트 높이/간격을 줄인다.
3. 그래도 안 들어가면 더 가벼운 레이아웃으로 바꾸거나 페이지를 분리한다.
4. 화면 밖으로 나간 상태를 그대로 납품하지 않는다.
```

우선순위: 폰트 축소보다 → 카드 높이 재조정 → 간격 재분배 → 행 수 축소 → 페이지 분리

이 규칙은 이제 hard fail validator 대상이다.

```txt
off-canvas 요소 발견
→ 생성 성공 처리 금지
→ 수정 후 재생성
```

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

### 추가 appendix 컴포넌트

보고용 시스템 가이드나 부록 장표에서 표 중심 dense page가 필요하면 아래 helper를 사용한다.

- `mk_kpi_status_detail()`
  - 용도: KPI 현황표 + 정의/측정식 표가 함께 들어가는 appendix/report page
  - 특징: dark/light theme 공용, dense table 2단 구성, 720pt 규칙 준수
  - 기본 구조:
    - 상단 = 목표 / KPI / 가중치 + 상반기 목표·실적 + 연간 목표·실적
    - 하단 = KPI / 정의 / 측정산식 / 증빙
  - 일반화 입력:
    - `summary_title`
    - `summary_groups`
    - `summary_headers`
    - `summary_rows`
    - `detail_title`
    - `detail_headers`
    - `detail_rows`

KPI 관련 내용이 들어오면 아래 컴포넌트를 우선 사용한다.

```txt
KPI / 목표 / 실적 / 달성률 / 가중치 / 측정산식 / 증빙
→ mk_kpi_status_detail() 강제
```


## 생성 후 검증 (필수)

검증 흐름·품질 우선 원칙·서브에이전트 상세: **`spigen_execution.md`** 품질 우선 원칙·생성 후 검증 흐름 섹션 참조.  
서브에이전트 프롬프트 원문: **`spigen_subagent_prompts.md`** 참조.

**Step A + preview verify + Step B + 서브에이전트 3종 판정 전까지 절대 "완료"라고 말하지 않는다.**

---

## 레퍼런스 파일

| 파일 | 내용 | 호출 시점 |
|-----|-----|---------|
| `spigen_render_rules.md` | 색상·타이포·강조·컴포넌트 선택 hard rule | 슬라이드 생성 시 참조 |
| `spigen_lib.py` | 컴포넌트 Python 코드 | 슬라이드 생성 시 `cp` 후 import |
| `template_spec.json` | 컴포넌트별 위치·크기·폰트 기준값 | 검증 기준 참조 |
| `spigen_verify.py` | 생성된 슬라이드 자동 검증 스크립트 | 슬라이드 생성 직후 실행 |
| `spigen_preview_verify.py` | preview HTML Playwright 검증 + 슬라이드별 screenshot | preview 생성 직후 실행 |
| `spigen_inplace_update.py` | 같은 presentation ID에 슬라이드 수정 반영 | 검수 FAIL 후 새 덱 대신 기존 덱 갱신 |
| `spigen_postgen_hook.py` | verify + thumbnail + review manifest 강제 훅 | Step B 직후, 서브에이전트 spawn 전 |
| `spigen_review_checklist.md` | 완료 전 수동/자동 검수 체크리스트 | `spigen_verify.py` PASS 후 검수 |
| `skill-status.md` | 현재 스킬화 완료 규칙 요약 | 스킬 상태 확인 시 |
| `spigen_detailed_guide.md` | 디테일용 슬라이드 상세 기준 가이드 | Q2-1 디테일용 선택 시 참조 |
| `spigen_planning.md` | Step 1~2 기획·구성 계획 | 전체 PPT 제작 시작 시 |
| `spigen_execution.md` | Step 3 API 실행 코드 | 실제 Google Slides 생성 시 |
| `spigen_design_spec.md` | 슬라이드 유형별 시각 규격 | HTML 디자인 생성 시 |
| `spigen_subagent_prompts.md` | 기획자·디자이너·대상(피드백용) 서브에이전트 프롬프트 원문 | 검수 서브에이전트 spawn 시 |
