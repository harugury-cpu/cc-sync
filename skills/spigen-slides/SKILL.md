---
name: spigen-slides
description: Spigen 브랜드 PPT 템플릿으로 내용이 채워진 Google Slides를 생성한다. 주제·내용을 받아 템플릿 레이아웃을 선택하고 내용을 자동 입력한다. "PPT 만들어줘", "프레젠테이션 만들어", "슬라이드 만들어줘" 등의 요청에 사용한다.
license: MIT
metadata:
  category: productivity
  locale: ko-KR
  phase: v2
---

# spigen-slides

## 고정값

- 담당자: `한원진 담당`
- 부서: `디자인부문ㅣ패키지디자인팀`
- 템플릿 ID: `16yCUv6G8QwiqZdRaxktCQROwUD9p-WO2v88BppsUs5M`

## 사용 가능한 슬라이드 레이아웃 (인덱스 기준, 0-based)

| 인덱스 | 용도 | 텍스트 박스 |
|-------|-----|-----------|
| 0 | 제목 슬라이드 | [0]: 제목\n부제목, [1]: 부서\n담당자, [2]: 날짜\nV버전 |
| 3 | 목차 (Contents) | [0]: "Contents", [1]: 01번호, [2]: 섹션1제목, [3]: 섹션1서브, [4]: 02, [5]: 섹션2제목, [6]: 섹션2서브, [7]: 03, [8]: 섹션3제목, [9]: 섹션3서브 |
| 4 | 섹션 구분 | [0]: 번호(01/02/03), [1]: 섹션 제목, [2]: 서브 항목 목록 |
| 5 | 기본 텍스트 | [0]: 섹션.슬라이드제목, [1]: 본문 제목 |
| 6 | 3열 도형+텍스트 | [0]: 섹션.슬라이드제목, [1]: 전체설명, [2]: 타이틀1, [3]: 설명1, [4]: 타이틀2, [5]: 설명2, [6]: 타이틀3, [7]: 설명3, [8]: 슬라이드소제목 |
| 15 | 제목+설명 (넓은) | [0]: 제목, [1]: 설명 |
| 16 | 제목+설명 (넓은2) | [0]: 제목, [1]: 설명 |
| 17 | 변경이력 | [0]: 변경 내용 |
| 18 | 마지막 슬라이드 | (빈 슬라이드) |

**삭제할 슬라이드:** 인덱스 1(영문제목), 2(안내), 7(이미지3열-좌), 8(이미지3열-중), 9(이미지4열), 10(전체이미지1), 11(전체이미지2), 12(전체이미지3), 13(이미지+제목-소), 14(이미지+제목-대)

---

## Step 1: 콘텐츠 수집

텍스트로 다음을 순서대로 질문한다:

1. **주제**: "어떤 내용의 프레젠테이션인가요?"
2. **핵심 내용**: "전달할 주요 내용이나 섹션을 알려주세요. (섹션명, 핵심 포인트 등 자유롭게)"
3. **날짜** (언급 없으면 오늘 날짜 자동 사용, 묻지 않음)
4. **버전** (언급 없으면 V1.0, 묻지 않음)

---

## Step 2: 슬라이드 구성 계획 생성

수집한 내용을 바탕으로 아래 구조로 슬라이드 구성을 생성한다.

### 구성 규칙

- **항상 포함**: 인덱스 0 (제목), 인덱스 18 (마지막)
- **섹션 2개 이상**: 인덱스 3 (목차) 추가
- **섹션마다**: 인덱스 4 (섹션 구분) 추가
- **3개 항목 나열**: 인덱스 6 (3열 도형) 사용
- **일반 설명**: 인덱스 15 또는 16 사용
- **변경이력 있음**: 인덱스 17 추가 (마지막 직전)

### 구성 예시 출력 형식

```
[제안 구성]
슬라이드 1 (제목): 패키지 디자인 가이드라인 2026
슬라이드 2 (목차): 3개 섹션
슬라이드 3 (섹션01): 디자인 원칙
슬라이드 4 (3열도형): 색상 / 타이포 / 레이아웃
슬라이드 5 (섹션02): 소재 사용 규정
슬라이드 6 (제목+설명): 승인 소재 목록
슬라이드 7 (섹션03): 적용 사례
슬라이드 8 (제목+설명): 제품별 적용 예시
슬라이드 9 (마지막)
```

구성을 사용자에게 보여주고 확인받는다. "수정 사항이 있으면 말씀해 주세요. 없으면 생성하겠습니다."

---

## Step 3: 기술 실행

### 3-1. 오늘 날짜 확인

```bash
TODAY=$(date +%Y.%m.%d)
echo $TODAY
```

### 3-2. 템플릿 복사

```bash
COPY_RESULT=$(gws drive files copy \
  --params '{"fileId":"16yCUv6G8QwiqZdRaxktCQROwUD9p-WO2v88BppsUs5M"}' \
  --json "{\"name\":\"$TITLE\"}" 2>/dev/null)
NEW_ID=$(echo "$COPY_RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")
echo "복사된 ID: $NEW_ID"
```

### 3-3. 복사본 구조 조회 (objectId 추출)

```bash
gws slides presentations get \
  --params "{\"presentationId\":\"$NEW_ID\"}" 2>/dev/null > /tmp/spigen_prs.json
```

Python으로 슬라이드별 objectId 매핑 추출:

```python
import json

with open('/tmp/spigen_prs.json') as f:
    prs = json.load(f)

slides = prs['slides']
slide_map = {}  # { index: { slide_id, text_boxes: [{ oid, text }] } }

for i, slide in enumerate(slides):
    boxes = []
    for el in slide.get('pageElements', []):
        shape = el.get('shape', {})
        text_els = shape.get('text', {}).get('textElements', [])
        content = ''.join(t.get('textRun', {}).get('content', '') for t in text_els).strip()
        if content:
            boxes.append({'oid': el['objectId'], 'text': content})
    slide_map[i] = {'slide_id': slide['objectId'], 'boxes': boxes}

# 저장
with open('/tmp/spigen_map.json', 'w') as f:
    json.dump(slide_map, f, ensure_ascii=False, indent=2)

print(json.dumps(slide_map, ensure_ascii=False, indent=2))
```

```bash
python3 /tmp/parse_slides.py
```

### 3-4. 불필요한 슬라이드 삭제

Step 2 계획에서 **사용하지 않을 슬라이드 인덱스**를 결정하고, 해당 objectId로 `deleteObject` 요청을 생성한다.

```python
import json

with open('/tmp/spigen_map.json') as f:
    slide_map = json.load(f)

# Step 2 계획에서 결정한 사용할 인덱스 목록 (예시)
keep_indices = {0, 3, 4, 6, 15, 18}  # 실제 계획에 따라 변경

requests = []
for idx_str, info in slide_map.items():
    idx = int(idx_str)
    if idx not in keep_indices:
        requests.append({"deleteObject": {"objectId": info['slide_id']}})

print(json.dumps({"requests": requests}, ensure_ascii=False))
```

```bash
python3 /tmp/delete_slides.py > /tmp/delete_req.json
gws slides presentations batchUpdate \
  --params "{\"presentationId\":\"$NEW_ID\"}" \
  --json "$(cat /tmp/delete_req.json)" 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print('삭제 완료')"
```

### 3-5. 콘텐츠 삽입

각 남은 슬라이드의 텍스트 박스에 내용을 삽입한다.
`deleteText` (기존 텍스트 삭제) → `insertText` (새 내용 삽입) 순서로 요청을 구성한다.

```python
import json

with open('/tmp/spigen_map.json') as f:
    slide_map = json.load(f)

# 슬라이드별 입력 내용 (Step 2에서 생성한 콘텐츠)
content_map = {
    0: {  # 제목 슬라이드
        0: "패키지 디자인 가이드라인 2026\n",   # box[0]: 제목
        1: "디자인부문ㅣ패키지디자인팀\n한원진 담당",  # box[1]: 부서\n담당자
        2: "2026.04.13\nV1.0",               # box[2]: 날짜\n버전
    },
    # ... (각 슬라이드 인덱스별 내용)
}

requests = []
for slide_idx, box_contents in content_map.items():
    info = slide_map[str(slide_idx)]
    for box_pos, new_text in box_contents.items():
        if box_pos < len(info['boxes']):
            oid = info['boxes'][box_pos]['oid']
            requests.append({"deleteText": {"objectId": oid, "textRange": {"type": "ALL"}}})
            requests.append({"insertText": {"objectId": oid, "insertionIndex": 0, "text": new_text}})

print(json.dumps({"requests": requests}, ensure_ascii=False))
```

```bash
python3 /tmp/fill_content.py > /tmp/fill_req.json
gws slides presentations batchUpdate \
  --params "{\"presentationId\":\"$NEW_ID\"}" \
  --json "$(cat /tmp/fill_req.json)" 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print('내용 입력 완료:', len(d.get('replies',[])), '항목')"
```

### 3-6. 결과 출력

```
프레젠테이션 생성 완료
제목: $TITLE
날짜: $TODAY / 버전: $VERSION
슬라이드 수: N장
URL: https://docs.google.com/presentation/d/$NEW_ID/edit
```

---

## 오류 처리

- copy 실패 → "템플릿 복사 실패. `gws auth status`를 확인하세요." 출력 후 중단
- batchUpdate 실패 → 복사된 파일 ID와 오류 메시지 함께 출력
- `/tmp` 파일 권한 오류 → `$TMPDIR` 또는 `/var/tmp`로 대체

## Done when

- 새 프레젠테이션 URL이 출력됐다.
- 제목/부서/담당자/날짜/버전이 올바르게 채워졌다.
- Step 2에서 계획한 모든 슬라이드에 내용이 입력됐다.
- 불필요한 슬라이드(이미지 예시, 안내 슬라이드 등)가 삭제됐다.
