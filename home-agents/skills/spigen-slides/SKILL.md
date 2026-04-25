---
name: spigen-slides
description: "PPT 만들어줘 / 피피티 만들어줘 / 장표 만들어줘 / 슬라이드 만들어줘" 등 슬라이드 생성 요청 시 발동. Spigen 슬라이드에서 섹션 구분자·도표·TOC·카드 등 특정 컴포넌트가 필요할 때도 참조. 전체 PPT 제작 기획 → spigen_planning.md | Google Slides 실행 → spigen_execution.md | 디자인 사양 → spigen_design_spec.md | 렌더링 규칙 → spigen_render_rules.md | 컴포넌트 코드 → spigen_lib.py
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

슬라이드 생성 직후, 완료 보고 전에 **Step A → Step B → Step C 순서로 반드시 실행**한다.  
셋 다 통과해야 "완료"라고 말할 수 있다.

### Step A: 수치 검증 (spigen_verify.py)

```bash
python3 /Users/harugury/.agents/skills/spigen-slides/spigen_verify.py <PRESENTATION_ID>
```

```
1. 슬라이드 생성
2. spigen_verify.py 실행
3. 결과 확인
   ├─ 모든 체크 PASS → Step B로
   └─ FAIL / MISS 존재 → spigen_lib.py 수정 → 재생성 → 2번으로
```

### Step B: 디자이너 시뮬레이션

Claude가 `spigen_design_spec.md`를 숙지한 Spigen 디자이너 페르소나를 취해 완성된 슬라이드를 검수한다.

**제약 (반드시 준수)**:
- 입력은 Google Slides API로 읽은 슬라이드 텍스트·구조·색상·폰트 데이터만 사용한다.
- 기획 과정, 사용자 지시, 대화 맥락은 일절 참조하지 않는다.
- `spigen_design_spec.md` 규칙만 기준으로 판단한다.

**검수 항목**:
1. 폰트·색상·캔버스 bounds가 스펙에 맞는가? (Step A 통과 기준 재확인)
2. 레이아웃이 디자인 원칙(60-30-10, 오렌지 절제, 캔버스 여백)에 맞는가?
3. 강조 구조가 올바른가? (슬라이드당 강조점 1개, 근거 있는 강조)
4. 의미 역할별 형태 차별화가 됐는가? (분석/결론/수치 카드가 구분되는가)
5. 화면 밖으로 나간 요소가 없는가?

**판정**:
```
전 항목 ✅ → Step C로
하나라도 ❌ → FAIL 항목 명시 → 수정 → Step A부터 재실행
```

피드백 출력 형식:
```
[디자이너 검수]

확인한 항목:
- [폰트] ✅ / ❌ (이유)
- [색상·오렌지] ✅ / ❌ (이유)
- [레이아웃] ✅ / ❌ (이유)
- [강조 구조] ✅ / ❌ (이유)
- [형태 차별화] ✅ / ❌ (이유)
- [캔버스 오버플로] ✅ / ❌ (이유)

판정: ✅ 통과 / ❌ 불통과
```

### Step C: 청중 시뮬레이션 피드백

기획 시 결정된 **Q2(청중)** 와 **Q4(목적)** 를 바탕으로 Claude가 해당 청중 페르소나를 취해 완성된 슬라이드를 평가한다.

**제약 (반드시 준수)**:
- 입력은 Google Slides API로 읽은 슬라이드 텍스트·구조만 사용한다.
- 기획 과정, 사용자 지시, 대화 맥락은 일절 참조하지 않는다.
- 이 슬라이드를 처음 보는 사람의 눈으로만 판단한다.

**평가 항목**:
1. 이 자료만 보고 무슨 말을 하려는지 파악할 수 있는가?
2. Q4 목적(동기부여 / 사용법 전수 / 조직 설득 / 홍보·소개)이 달성됐는가?
3. 청중 입장에서 불명확하거나 빠진 것이 있는가?

**판정**:
```
목적 충족 ✅ → "완료" 보고 및 링크 공유
목적 미충족 ❌ → 구체적 피드백 명시 → 수정 → Step A부터 재실행
```

피드백 출력 형식:
```
[청중: 경영진 / 목적: 조직 설득]

이 자료만 보고 느낀 점:
- (구체적 반응)

목적 달성 여부: ✅ 충족 / ❌ 미충족

미충족 시 이유:
- (무엇이 불명확한가, 무엇이 빠졌는가)
```

**Step A + Step B + Step C 목적 충족 판정 전까지 절대 "완료"라고 말하지 않는다.**


---

## 레퍼런스 파일

| 파일 | 내용 | 호출 시점 |
|-----|-----|---------|
| `spigen_render_rules.md` | 색상·타이포·강조·컴포넌트 선택 hard rule | 슬라이드 생성 시 참조 |
| `spigen_lib.py` | 컴포넌트 Python 코드 | 슬라이드 생성 시 `cp` 후 import |
| `template_spec.json` | 컴포넌트별 위치·크기·폰트 기준값 | 검증 기준 참조 |
| `spigen_verify.py` | 생성된 슬라이드 자동 검증 스크립트 | 슬라이드 생성 직후 실행 |
| `spigen_review_checklist.md` | 완료 전 수동/자동 검수 체크리스트 | `spigen_verify.py` PASS 후 검수 |
| `skill-status.md` | 현재 스킬화 완료 규칙 요약 | 스킬 상태 확인 시 |
| `spigen_detailed_guide.md` | 디테일용 슬라이드 상세 기준 가이드 | Q2-1 디테일용 선택 시 참조 |
| `spigen_planning.md` | Step 1~2 기획·구성 계획 | 전체 PPT 제작 시작 시 |
| `spigen_execution.md` | Step 3 API 실행 코드 | 실제 Google Slides 생성 시 |
| `spigen_design_spec.md` | 슬라이드 유형별 시각 규격 | HTML 디자인 생성 시 |
