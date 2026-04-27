---
name: spigen-slides
description: "PPT 만들어줘 / 피피티 만들어줘 / 장표 만들어줘 / 슬라이드 만들어줘 / 발표자료 만들어줘 / 프레젠테이션 만들어줘 / 보고서 슬라이드 만들어줘 / 덱 만들어줘" 등 슬라이드 생성 요청 시 발동. Spigen 내부용 Google Slides 자동 생성 스킬 — 브랜드 디자인 규칙을 적용하여 발표 시간을 줄이고 디자인 일관성을 유지하기 위해 사용. Spigen 슬라이드에서 섹션 구분자·도표·TOC·카드 등 특정 컴포넌트가 필요할 때도 참조. 전체 PPT 제작 기획 → spigen_planning.md | Google Slides 실행 → spigen_execution.md | 디자인 사양 → spigen_design_spec.md | 렌더링 규칙 → spigen_render_rules.md | 컴포넌트 코드 → spigen_lib.py
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

### 신규 기본 원칙 (중요)

이제 `HTML -> Slides 변환`을 source of truth로 사용하지 않는다.

```txt
source of truth = SlideSpec + ComponentSpec
preview = spigen_preview.py
final delivery = spigen_lib.py / Google Slides API
```

즉 HTML은 미리보기 렌더러이고, Google Slides와 **같은 spec**을 소비해야 한다.

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

슬라이드 생성 직후, 완료 보고 전에 **Step A → Step B → 기획자·디자이너·대상 병렬 동시 spawn** 순서로 실행한다.

```
1. 슬라이드 생성
2. Step A: spigen_verify.py 수치 검증
   ├─ FAIL / MISS → spigen_lib.py 수정 → 재생성 → 2번으로
   └─ 전원 PASS → Step B로
3. Step B: getThumbnail 이미지 검수 (시각적 오버플로·겹침·오렌지 과다 확인)
   ├─ 문제 발견 → 수정 → 재생성 → 2번으로
   └─ 이상 없음 → 서브에이전트 spawn으로
4. Agent 도구로 기획자·디자이너·대상 3개를 **하나의 메시지에서 동시에** spawn
5. 세 에이전트 결과 수집 후 종합 판정 — 하나라도 ❌이면 Step A부터 재실행
```

### Step A: 수치 검증 (spigen_verify.py)

```bash
python3 /Users/harugury/.agents/skills/spigen-slides/spigen_verify.py <PRESENTATION_ID>
```

### Step B: 이미지 검수 (getThumbnail)

전체 슬라이드 썸네일 URL을 일괄 조회하고, Claude가 각 이미지를 직접 확인한다.

```bash
python3 << 'EOF'
import subprocess, json
NEW_ID = "<PRESENTATION_ID>"
result = subprocess.run(["gws", "slides", "presentations", "get",
    "--params", f'{{"presentationId":"{NEW_ID}"}}'], capture_output=True, text=True)
slides = json.loads(result.stdout)["slides"]
for i, slide in enumerate(slides):
    thumb = subprocess.run(["gws", "slides", "presentations", "pages", "getThumbnail",
        "--params", json.dumps({"presentationId": NEW_ID, "pageObjectId": slide["objectId"]})],
        capture_output=True, text=True)
    url = json.loads(thumb.stdout).get("contentUrl", "")
    print(f"슬라이드 {i+1}: {url}")
EOF
```

확인 항목: 텍스트 오버플로 / 요소 겹침 / 오렌지 강조 슬라이드당 3개 이하 / 전체 레이아웃 균형
썸네일 URL은 발급 후 **1시간** 유효 — 검수 즉시 진행.

### 기획자: 내용 검수 (룰 준수 체크)

메인 에이전트가 `spigen_execution.md`의 **기획자 서브에이전트 프롬프트 템플릿**으로 서브에이전트를 spawn한다.  
서브에이전트는 **슬라이드 ID + COMPONENT_BRIEF**를 받고, 생성 컨텍스트(기획 과정·사용자 지시·대화 내용)는 전달하지 않는다.  
서브에이전트가 슬라이드를 처음 보는 상태에서 규칙과 대조하도록 하여 생성 편향을 차단한다.

**제약 (반드시 준수)**:
- 의도나 지시가 아니라 결과물이 규칙을 준수하는지만 판단한다.
- "만들려고 했다"는 이유로 PASS 주지 않는다.

**검수 항목**:

1. **컴포넌트 선택 적합성**: 기획 단계 COMPONENT_BRIEF와 실제 사용된 컴포넌트가 일치하는가? (`spigen_render_rules.md` 섹션 8 결정 테이블 기준)
   - COMPONENT_BRIEF가 `mk_split_cards()`를 명시했는데 `mk_3col_cards()`를 쓰지 않았는가?
   - 여러 항목의 동일 속성 비교 → 표가 맞는데 카드를 쓰지 않았는가?
   - 상태(완료/진행중/대기)가 핵심 → 상태 구분된 형식인가?
   - 독립적이지 않은 항목에 카드를 쓰지 않았는가?

2. **페이지별 주제 명확성**: 각 슬라이드에서 주제가 하나인가?
   - 제목(eyebrow + title)만 봐도 이 슬라이드가 무엇에 대한 것인지 알 수 있는가?
   - 경쟁하는 주제가 한 슬라이드 안에 들어가지 않았는가?

3. **슬라이드 의도 (무엇을 보여주려는가)**:
   - 각 슬라이드가 청중에게 무엇을 전달하려는지 명확한가?
   - "이 슬라이드를 보고 나서 청중이 무엇을 알아야 하는가?"가 한 문장으로 표현 가능한가?
   - 정보 나열 / 판단 유도 / 현황 보고 — 의도가 선택한 컴포넌트 형식과 일치하는가?

4. **카드 역할 구분**: mk_split_cards 카드에 완료/대기/Next가 섞이면 `✅`/`⏳`/`primary`로 구분됐는가?

5. **핵심 메시지**: 발표자 설명 없이 슬라이드만 봐도 핵심이 파악되는가?

6. **디테일용 기준** (Q2-1 디테일용 선택 시): 5~6줄 허용·수치 생략 없음·자기완결 기준을 지켰는가?

**판정**: 결과를 종합 판정 단계로 전달한다. ❌ 항목이 있으면 명시.

피드백 출력 형식:
```
[내용 검수]

슬라이드별 분석:
- 슬라이드 N: [주제 한 줄] / [의도 한 줄] / [컴포넌트 선택 적합 여부]

확인한 항목:
- [컴포넌트 선택] ✅ / ❌ (이유)
- [페이지별 주제] ✅ / ❌ (이유)
- [슬라이드 의도] ✅ / ❌ (이유)
- [카드 역할 구분] ✅ / ❌ (이유)
- [핵심 메시지] ✅ / ❌ (이유)
- [디테일 기준] ✅ / ❌ / N/A (이유)

판정: ✅ 통과 / ❌ 불통과
불통과 시: 어떤 슬라이드의 어떤 요소가 문제인지 구체적으로 명시
```

---

### 디자이너: 시뮬레이션

메인 에이전트가 `spigen_execution.md`의 **디자이너 서브에이전트 프롬프트 템플릿**으로 서브에이전트를 spawn한다.  
서브에이전트는 슬라이드 ID를 받고, 생성 컨텍스트는 전달하지 않는다.  
서브에이전트는 `spigen_design_spec.md`를 숙지한 Spigen 디자이너 페르소나로 슬라이드를 검수한다.

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

**판정**: 결과를 종합 판정 단계로 전달한다. ❌ 항목이 있으면 명시.

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

### 대상: 청중 시뮬레이션 피드백

메인 에이전트가 `spigen_execution.md`의 **대상 서브에이전트 프롬프트 템플릿**으로 서브에이전트를 spawn한다.  
기획 시 결정한 `{{Q2}}`(청중)와 `{{Q4}}`(목적)를 템플릿 변수에 주입한다.  
서브에이전트는 슬라이드 ID + Q2/Q4 값만 받고, 그 외 생성 컨텍스트는 전달하지 않는다.

**제약 (반드시 준수)**:
- 입력은 Google Slides API로 읽은 슬라이드 텍스트·구조만 사용한다.
- 기획 과정, 사용자 지시, 대화 맥락은 일절 참조하지 않는다.
- 이 슬라이드를 처음 보는 사람의 눈으로만 판단한다.

**평가 항목**:
1. 이 자료만 보고 무슨 말을 하려는지 파악할 수 있는가?
2. Q4 목적(동기부여 / 사용법 전수 / 조직 설득 / 홍보·소개)이 달성됐는가?
3. 청중 입장에서 불명확하거나 빠진 것이 있는가?

**판정**: 결과를 종합 판정 단계로 전달한다. ❌ 항목이 있으면 명시.

피드백 출력 형식:
```
[청중: 경영진 / 목적: 조직 설득]

이 자료만 보고 느낀 점:
- (구체적 반응)

목적 달성 여부: ✅ 충족 / ❌ 미충족

미충족 시 이유:
- (무엇이 불명확한가, 무엇이 빠졌는가)
```

### 종합 판정 (병렬 결과 수집 후)

기획자·디자이너·대상 3개 에이전트 결과를 모두 수집한 후 아래 형식으로 종합 보고한다:

```
[검증 결과 요약]

기획자:   ✅ 통과 / ❌ 불통과 — {한 줄 판정}
디자이너: ✅ 통과 / ❌ 불통과 — {한 줄 판정}
대상:     ✅ 통과 / ❌ 불통과 — {한 줄 판정}
```

**전원 ✅** → "완료" 보고 및 Google Slides 링크 공유.  
**하나라도 ❌** → FAIL 항목 명시 → 수정 → Step A부터 전체 재실행.

---

**Step A + Step B + 기획자 + 디자이너 + 대상 목적 충족 판정 전까지 절대 "완료"라고 말하지 않는다.**


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
| `spigen_subagent_prompts.md` | 기획자·디자이너·대상 서브에이전트 프롬프트 원문 | 검수 서브에이전트 spawn 시 |
