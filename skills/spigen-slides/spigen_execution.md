# spigen-slides Execution Guide (v4)

## Step 3. 생성

승인된 아웃라인을 그대로 Python 빌드 스크립트로 변환하고 실행한다.

### 라이브러리 준비

```bash
SKILL_DIR="$HOME/.agents/skills/spigen-slides"
for f in spigen_lib.py spigen_layout.py spigen_models.py; do
  cp "$SKILL_DIR/$f" /tmp/$f
done
```

### 빌드 스크립트 기본 구조

```python
import sys, subprocess, json, shutil, os

SKILL_DIR = os.path.expanduser("~/.agents/skills/spigen-slides")
for fname in ("spigen_lib.py", "spigen_layout.py", "spigen_models.py"):
    shutil.copy2(os.path.join(SKILL_DIR, fname), f"/tmp/{fname}")
sys.path.insert(0, "/tmp")
import spigen_lib as lib

TMPL_ID = "1R_z4ZKSbRSe5uQ-uWT6dnmBDTJ7M4yOjbGW_1UfxnEk"
TITLE   = "<PPT 제목>"

# 1. 템플릿 복사
copy_r = subprocess.run(
    ["gws", "drive", "files", "copy",
     "--params", json.dumps({"fileId": TMPL_ID}),
     "--json",   json.dumps({"name": TITLE})],
    capture_output=True, text=True)
NEW_ID = json.loads(copy_r.stdout)["id"]

# 2. 기존 슬라이드 ID 수집
prs_data = json.loads(subprocess.run(
    ["gws", "slides", "presentations", "get",
     "--params", json.dumps({"presentationId": NEW_ID})],
    capture_output=True, text=True).stdout)
existing_ids = [s["objectId"] for s in prs_data["slides"]]

# 3. 슬라이드 생성 요청 누적
reqs = []
lib.set_theme("dark")  # 또는 "light"

# 승인된 아웃라인 그대로 구현
lib.mk_cover("cover", "<제목>", 0, reqs, subtitle="<부제>",
             date_text="<날짜>", version="V1.0")
# ... 나머지 슬라이드

# 4. 기존 슬라이드 삭제
for oid in existing_ids:
    reqs.append({"deleteObject": {"objectId": oid}})

# 5. batchUpdate (50개씩 청크)
for i in range(0, len(reqs), 50):
    chunk = reqs[i:i+50]
    result = subprocess.run(
        ["gws", "slides", "presentations", "batchUpdate",
         "--params", json.dumps({"presentationId": NEW_ID}),
         "--json",   json.dumps({"requests": chunk})],
        capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[오류] 청크 {i//50+1}: {result.stderr[:400]}")
        sys.exit(1)
    print(f"청크 {i//50+1} ({len(chunk)}건) 완료")

print(f"\n완료: https://docs.google.com/presentation/d/{NEW_ID}/edit")
```

---

## Step 4. 수치 검증

```bash
python3 ~/.agents/skills/spigen-slides/spigen_verify.py <PRESENTATION_ID>
```

**PASS 기준**: 전원 PASS  
**FAIL 시**: 해당 항목만 수정 후 재생성. 전체 재빌드하지 않아도 되면 `spigen_inplace_update.py` 사용.

---

## Step 5. 썸네일 시각 확인

```python
import subprocess, json
NEW_ID = "<PRESENTATION_ID>"
prs = json.loads(subprocess.run(
    ["gws","slides","presentations","get",
     "--params", f'{{"presentationId":"{NEW_ID}"}}'],
    capture_output=True, text=True).stdout)
for i, slide in enumerate(prs["slides"]):
    thumb = json.loads(subprocess.run(
        ["gws","slides","presentations","pages","getThumbnail",
         "--params", json.dumps({"presentationId": NEW_ID,
                                 "pageObjectId": slide["objectId"]})],
        capture_output=True, text=True).stdout)
    print(f"슬라이드 {i+1}: {thumb.get('contentUrl','')}")
```

**확인 항목:**
- 텍스트 오버플로 (박스 밖으로 잘린 텍스트)
- 요소 겹침
- 캔버스 이탈 (720×405pt 밖)
- 오렌지 강조 슬라이드당 3개 이하

문제 발견 → 해당 슬라이드만 `spigen_inplace_update.py`로 수정.  
전원 이상 없음 → 완료 링크 공유.

---

## 슬라이드 부분 수정

기존 덱에서 특정 슬라이드만 고칠 때:

```bash
python3 ~/.agents/skills/spigen-slides/spigen_inplace_update.py \
  <PRESENTATION_ID> <SLIDE_OBJECT_ID>
```

전체 재빌드보다 이 방식을 먼저 시도한다.

---

## 컴포넌트 주요 함수 시그니처

```python
lib.mk_cover(obj_id, title, slide_idx, reqs,
             subtitle="", date_text="", version="")

lib.mk_section_divider(obj_id, number, title, slide_idx, reqs)

lib.mk_flow_focus(slide_obj_id, steps, reqs)
# steps: [{"num":"01","name":"...","service":"...","style":"auto"|"primary"}]

lib.mk_decision_tree(slide_obj_id, config, reqs)
# config: {"input":"...","decision":"...","yes":"...","no":"...",
#           "output":"...","yes_label":"...","no_label":"..."}

lib.mk_split_cards(slide_obj_id, left, right, reqs)
# left/right: {"label":"...","items":[...]}

lib.mk_3col_cards(slide_obj_id, cards, reqs)
# cards: [{"title":"...","body":"..."}]

lib.mk_kpi_status_detail(slide_obj_id, reqs,
    summary_title, summary_groups, summary_headers, summary_rows,
    detail_title, detail_headers, detail_rows)

lib.slide_base(obj_id, title, slide_idx, reqs,
               page_label="", page_no=1, total=1)
```

`slide_base()`는 콘텐츠 슬라이드마다 먼저 호출하고, 이후 컴포넌트 함수를 호출한다.

---

## 디자인 규칙 (불변)

- 캔버스 720×405pt — 이탈 요소 = 수정 후 재생성, 납품 금지
- 오렌지(`#FF6B1A`): 슬라이드당 핵심 1개, 전체 최대 3개
- `lib.set_theme('dark')` 또는 `lib.set_theme('light')` — Step 2 승인 시 결정
- 표지: `mk_cover()` 또는 템플릿 1페이지 복사 후 텍스트 교체

세부 규칙: `spigen_render_rules.md`
