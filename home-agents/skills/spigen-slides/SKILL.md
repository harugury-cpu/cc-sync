---
name: spigen-slides
description: Spigen 슬라이드에서 섹션 구분자·도표·TOC·카드 등 특정 컴포넌트가 필요할 때 참조. 전체 PPT 제작 기획 → spigen_planning.md | Google Slides 실행 → spigen_execution.md | 디자인 사양 → spigen_design_spec.md | 렌더링 규칙 → spigen_render_rules.md | 컴포넌트 코드 → spigen_lib.py
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


## 생성 후 검증 (필수)

슬라이드 생성 직후, 완료 보고 전에 반드시 실행한다.

```bash
python3 /Users/harugury/.agents/skills/spigen-slides/spigen_verify.py <PRESENTATION_ID>
```

검증 루프:

```
1. 슬라이드 생성
2. spigen_verify.py 실행
3. 결과 확인
   ├─ 모든 체크 PASS → "완료" 보고 가능
   └─ FAIL / MISS 존재 → spigen_lib.py 수정 → 재생성 → 2번으로
```

`FAIL/MISS`가 하나라도 있으면 **"완료"라고 말하지 않는다.**


---

## 레퍼런스 파일

| 파일 | 내용 | 호출 시점 |
|-----|-----|---------|
| `spigen_render_rules.md` | 색상·타이포·강조·컴포넌트 선택 hard rule | 슬라이드 생성 시 참조 |
| `spigen_lib.py` | 컴포넌트 Python 코드 | 슬라이드 생성 시 `cp` 후 import |
| `template_spec.json` | 컴포넌트별 위치·크기·폰트 기준값 | 검증 기준 참조 |
| `spigen_verify.py` | 생성된 슬라이드 자동 검증 스크립트 | 슬라이드 생성 직후 실행 |
| `spigen_planning.md` | Step 1~2 기획·구성 계획 | 전체 PPT 제작 시작 시 |
| `spigen_execution.md` | Step 3 API 실행 코드 | 실제 Google Slides 생성 시 |
| `spigen_design_spec.md` | 슬라이드 유형별 시각 규격 | HTML 디자인 생성 시 |
