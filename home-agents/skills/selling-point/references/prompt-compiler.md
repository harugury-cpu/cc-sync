# 이미지 프롬프트 컴파일 규칙

이 파일은 `gongnyang-prompt-kit`에서 이미지 품질에 직접 영향을 주는 규칙만 가져온 후처리 규칙이다. 셀링포인트 판단, 점수화, 경쟁사 분석, TOP 선정 로직은 바꾸지 않는다.

## 적용 위치

`visual-brief.md`의 8필드 작성 후, 이미지 생성용 최종 프롬프트를 출력하기 직전에 적용한다.

```text
분석 → TOP 카드 → 비주얼 브리프 → prompt compile → 최종 이미지 프롬프트
```

추가 LLM 호출을 만들지 말고, 작성 규칙으로만 반영한다. 시간 증가를 만들지 않는 것이 목적이다.

## 품질 규칙

### 1. 네거티브 문장 금지

이미지 프롬프트에 `no`, `without`, `do not`, `avoid`, `금지`, `없음`처럼 모델이 원치 않는 대상을 다시 떠올리게 하는 표현을 쓰지 않는다. 빼고 싶은 것은 원하는 상태를 긍정형으로 쓴다.

예시:

- `No text` → `clean blank copy area reserved for later layout`
- `No logo overlays` → `brand-free clean surface treatment`
- `No props` → `minimal product-only studio setup`
- `No people` → `environment-only composition focused on the cased device`
- `Do not invent specs` → `show only visually grounded product details from the provided reference`
- `Avoid clutter` → `clean composition with one clear hero subject and controlled spacing`

### 2. SD식 품질 태그 금지

다음 표현은 쓰지 않는다.

```text
masterpiece
best quality
8k
4k
uhd
ultra detailed
highly detailed
sharp focus
trending on artstation
```

품질은 결과 조건으로 쓴다.

예시:

- `ultra high resolution, razor-sharp focus` → `crisp product edges, true material rendering, precise contact shadows`
- `premium quality` → `Apple-style commercial product photography with controlled lighting and clear material separation`

### 3. 장비 스펙보다 결과 묘사

카메라 장비명과 과한 EXIF 나열보다 결과를 쓴다.

예시:

- `Canon R5, f/1.4` → `shallow depth of field with softly falling background`
- `100mm macro lens`는 제품 디테일 목적일 때만 쓰고, 가능하면 `macro product detail view with crisp edges`처럼 결과를 함께 쓴다.

### 4. 수치와 화면 조건은 명확히

가능하면 다음을 명시한다.

- 화면비: `AR 1:1`, `AR 4:5`, `AR 3:4`, `AR 16:9`, `AR 9:16`
- 제품 점유율: `product occupies 30-50% of frame`
- 팔레트: HEX 3~5개
- 조명: 방향, soft/hard, shadow 성격
- 재질: matte, glossy, transparent, textured, rubberized, hard-shell 등 실제 제품 재질

### 5. 1프롬프트 = 1이미지 컷

한 프롬프트에서 여러 이미지를 한 캔버스에 동시에 요구하지 않는다. 비교/인포그래픽이 필요하면 한 장 안에서 읽기 순서와 역할을 명확히 제한한다.

좋음:

```text
single product hero composition with one small proof crop area
```

나쁨:

```text
four separate panels showing every feature
```

### 6. 상세페이지 컷 라우팅

상세페이지 셀링포인트 이미지는 아래 중 하나로 라우팅한다.

- 제품 구조/재질/핏/호환성 증명: `product catalog / product diagram`
- 사용 순서/기능 원리/결과 증명: `clean infographic / action proof`
- 카드뉴스형 설명: `editorial card`
- 실제 사용 신뢰: `lifestyle product proof`

제품 케이스/액세서리는 우선 `product catalog`, `action proof`, `clean infographic` 중에서 고른다.

## 최종 프롬프트 필수 형태

최종 이미지 프롬프트에는 최소한 아래 요소가 들어가야 한다.

```text
Scene:
Camera / View:
Lighting:
Color palette:
Material / Texture:
Composition:
Must show:
AR x:y
```

단, 사용자에게 보여주는 출력은 자연어 문단이어도 된다. 내부적으로 위 요소가 누락되지 않게 작성한다.

## 자체 점검

최종 프롬프트 작성 후 확인한다.

- 네거티브 문장, `no`, `without`, `do not`, `avoid`가 남아 있지 않은가?
- SD식 품질 태그가 남아 있지 않은가?
- AR 토큰이 끝에 있는가?
- 셀링포인트를 증명하는 구체 가시 요소가 있는가?
- 경쟁사 이미지를 복제하는 레이아웃/브랜드/소품을 요구하지 않는가?
- 제품 레퍼런스와 다른 제품을 만들도록 유도하지 않는가?
