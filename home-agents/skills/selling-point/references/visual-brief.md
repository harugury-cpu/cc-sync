# 비주얼 브리프 8필드 작성 규칙

각 TOP 카드마다 ChatGPT 웹 이미지 생성 등 외부 이미지 생성 환경에 복사해 사용할 수 있는 영문 비주얼 브리프를 작성한다. 한국어 라벨로 출력하지 말고 영문 1줄씩 8필드를 작성한다.

로컬 Codex CLI 데몬 환경에서는 AI 이미지 자동 생성을 수행하지 않는다. 이 브리프는 실제 생성용 결과물이 아니라, 사용자가 ChatGPT 웹 이미지 생성 등 별도 환경에 복사해 사용할 핸드오프 산출물이다.

## 8필드

- Subject — 메인 피사체. 제품 색·재질·형태·장착된 Apple 디바이스를 명시.
  - 예: "MagFit Pro hard-shell phone case in matte black, mounted on an iPhone 15 Pro"

- Action — 프레임 안에서 무엇이 일어나는지.
  - 예: "MagSafe charger snaps onto the back of the case with a visible alignment ring"

- Setting — 배경 또는 환경.
  - product_hero 예: "Pure white seamless studio background"
  - lifestyle 예: "Modern minimalist cafe table by a window, soft morning sunlight"

- Camera — 렌즈, 거리, 각도, 시점.
  - 예: "100mm macro lens, 30cm distance, 3/4 hero angle, slight elevation"

- Lighting — 광원 종류, 방향, 분위기.
  - 예: "Soft studio softbox from upper left, even illumination, controlled minimal shadow"

- Composition — 프레이밍, 피사체 배치, 깊이.
  - 예: "Subject centered, occupies 60% of frame, generous negative space, shallow depth of field on background"

- Must show — 셀링포인트를 증명하는 필수 가시 요소.
  - 예: "Visible MagSafe alignment ring, magnet snap moment, slim profile under 1mm"

- Framing — 화면비, 피사체 크기, 여백 규모.
  - 예: "Square 1:1, product occupies 50% of frame, balanced negative space"

## 작성 규칙

- 모든 필드 영문 1줄. 두 줄 금지.
- baseline은 product_hero 또는 lifestyle 중 하나를 선택한 후 visualBrief 위에 prefix로 둔다.
- "best quality", "8k resolution", "ultra detailed" 같은 클리셰 키워드 금지. baseline에 이미 충분한 품질 키워드가 포함되어 있다.
- 텍스트 오버레이, 워터마크, 한국어 텍스트 등장 금지. 이미지 생성 모델이 텍스트를 합성하면 결과가 망가진다.
- "Spigen", "Apple", "MagSafe" 등 공식 브랜드 표기는 케이스에 장착된 Apple 디바이스 또는 액세서리 컨텍스트에 한해 자연스럽게 사용. 별도 로고 합성 지시는 하지 않는다.
- 같은 셀링포인트에 product_hero와 lifestyle을 동시에 출력하지 않는다. 1개만 선택.

## 최종 출력 형식 (외부 이미지 생성 환경에 복사 가능한 형태)

```text
{baseline 텍스트 9~10줄}

Subject: {1줄}
Action: {1줄}
Setting: {1줄}
Camera: {1줄}
Lighting: {1줄}
Composition: {1줄}
Must show: {1줄}
Framing: {1줄}

Selling point: {셀링포인트 한 줄 요약}
Product: {제품명}.
```

## scoreReasons 객관성 규칙

reason은 다음 두 요소를 모두 포함한다.

- 점수 체크리스트(`scoring.md`)의 어느 조건에 해당해서 그 점수인지 1문장 매핑.
- 분석 메모(`output-format.md`의 analysis 섹션)에 등장한 데이터 인용. 예: "competitorMessageMap에서 경쟁사 4개 중 3개", "uniqueFeatures의 X 기능".

좋은 reason 예시:

> "competitorMessageMap에서 경쟁사 A, C가 'MagSafe 호환'만 언급하고 자력 강도를 명시한 곳이 없어 5점 조건(우리만의 기능 단어 2개 이상 + 경쟁사 0건)에 해당."

나쁜 reason 예시:

> "구매로 직접 연결되는 핵심 기능이다."
> (이유: 모든 셀링포인트에 통용되는 일반론, 데이터 인용 없음, 체크리스트 매핑 없음)

reason에 일반론을 적었다면 결과를 다시 작성한다.
