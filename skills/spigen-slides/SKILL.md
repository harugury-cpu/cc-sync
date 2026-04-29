---
name: spigen-slides
description: "PPT 만들어줘 / 피피티 만들어줘 / 장표 만들어줘 / 슬라이드 만들어줘 / 발표자료 만들어줘 / 프레젠테이션 만들어줘 / 보고서 슬라이드 만들어줘 / 덱 만들어줘 등 슬라이드 생성 요청 시 발동. Spigen 내부용 Google Slides 자동 생성 스킬."
license: MIT
metadata:
  category: productivity
  locale: ko-KR
  phase: v4
---

# spigen-slides v4

## 핵심 원칙

**AI의 역할**: 내용 구조화 + Spigen 디자인 적용  
**AI의 역할이 아닌 것**: 내용 창작  
**사용자의 역할**: 내용 제공 + 최종 승인

내용을 모르는 채로 슬라이드를 만들지 않는다.  
사용자가 내용을 주면 AI가 구조화하고 디자인을 입힌다.

---

## 고정값

- 담당자: `한원진 담당`
- 부서: `디자인부문ㅣ패키지디자인팀`
- 템플릿 ID: `1R_z4ZKSbRSe5uQ-uWT6dnmBDTJ7M4yOjbGW_1UfxnEk`
- 콘텐츠 템플릿 ID: `1rh_2NNwM2CeZxFaZFfgoK3s1RAU2SyzZd794480hrVo`
- 라이브러리: `~/.agents/skills/spigen-slides/spigen_lib.py`

---

## 5단계 실행 흐름

```
Step 1. 내용 수집
Step 2. 슬라이드 아웃라인 제안 → 사용자 승인
Step 3. 생성
Step 4. 썸네일 시각 확인
Step 5. 완료
```

승인 없이 Step 3으로 넘어가지 않는다.  
썸네일 확인 없이 완료를 선언하지 않는다.

---

### Step 1. 내용 수집

**경로 A — 원본 데이터 있음** (문서, 보드 데이터, 채팅, 메모 등)  
→ 원본에서 핵심 내용을 추출한다. AI가 내용을 창작하지 않는다.

**경로 B — 사용자가 직접 제공**  
→ 아래 4가지만 묻는다:

```
1. 이 PPT의 목적 (보고 / 교육 / 제안 / 안내)
2. 청중
3. 전달할 핵심 내용 (글머리, 메모, 흐름 설명 무엇이든)
4. 테마: dark / light
```

질문 4개 이상 하지 않는다. 내용이 충분하면 바로 Step 2로.

---

### Step 2. 슬라이드 아웃라인 제안

아래 형식으로 작성하고 **사용자 승인 후** Step 3으로 넘어간다.

```
[슬라이드 N] 제목
  내용 요약 (1~2줄)
  → 컴포넌트: mk_xxx()
  → 이유: 왜 이 컴포넌트인지 1줄
```

**컴포넌트 자동 선택 기준 (내용 구조에서 결정):**

| 내용 구조 | 컴포넌트 |
|-----------|---------|
| 순서 있는 단계 3~6개 | `mk_flow_focus()` |
| Yes/No 분기 판단 | `mk_decision_tree()` |
| Before / After 비교 | `mk_split_cards()` |
| 독립 항목 나열 | `mk_3col_cards()` |
| 섹션 구분 | `mk_section_divider()` |
| 표지 | `mk_cover()` |
| KPI / 수치 표 | `mk_kpi_status_detail()` |

컴포넌트를 먼저 정하지 않는다. 내용을 파악한 뒤 자동 선택한다.

---

### Step 3. 생성

승인된 아웃라인대로 Python 빌드 스크립트를 작성하고 실행한다.

```bash
# 라이브러리 복사
for f in spigen_lib.py spigen_layout.py spigen_models.py; do
  cp ~/.agents/skills/spigen-slides/$f /tmp/$f
done

# 빌드 실행
python3 /tmp/build_<name>.py
```

생성 직후 수치 검증:
```bash
python3 ~/.agents/skills/spigen-slides/spigen_verify.py <PRESENTATION_ID>
```

FAIL 항목 → 수정 후 재생성. 전원 PASS → Step 4.

---

### Step 4. 썸네일 시각 확인

전체 썸네일을 조회하고 직접 확인한다.

```python
import subprocess, json
NEW_ID = "<PRESENTATION_ID>"
prs = json.loads(subprocess.run(["gws","slides","presentations","get",
    "--params",f'{{"presentationId":"{NEW_ID}"}}'],
    capture_output=True,text=True).stdout)
for i,slide in enumerate(prs["slides"]):
    thumb = json.loads(subprocess.run(["gws","slides","presentations","pages","getThumbnail",
        "--params",json.dumps({"presentationId":NEW_ID,"pageObjectId":slide["objectId"]})],
        capture_output=True,text=True).stdout)
    print(f"슬라이드 {i+1}: {thumb.get('contentUrl','')}")
```

확인 항목: 텍스트 오버플로 / 요소 겹침 / 캔버스 이탈 / 오렌지 과다  
문제 발견 → 수정 후 재생성. 이상 없음 → Step 5.

---

### Step 5. 완료

```
완료: https://docs.google.com/presentation/d/<ID>/edit
```

---

## 디자인 규칙 (불변)

- 캔버스: 720 × 405pt — 이탈 요소 = hard fail, 납품 금지
- 오렌지 강조(`#FF6B1A`): 슬라이드당 핵심 1개, 전체 최대 3개
- 테마: `lib.set_theme('dark')` 또는 `lib.set_theme('light')`
- 표지: `mk_cover()` 또는 템플릿 1페이지 복사 후 텍스트 교체
- 폰트: Noto Sans KR(한글) / Proxima Nova(영문)

세부 규칙 → `spigen_render_rules.md`

---

## 레퍼런스

| 파일 | 용도 |
|------|------|
| `spigen_lib.py` | 컴포넌트 Python 코드 |
| `spigen_layout.py` | 레이아웃 헬퍼 |
| `spigen_models.py` | 데이터 모델 |
| `spigen_render_rules.md` | 색상·타이포·강조 hard rule |
| `spigen_verify.py` | 수치 검증 스크립트 |
| `spigen_design_spec.md` | 슬라이드 유형별 시각 규격 |
| `template_spec.json` | 컴포넌트별 위치·크기 기준값 |
| `spigen_inplace_update.py` | 기존 덱 수정 반영 |
