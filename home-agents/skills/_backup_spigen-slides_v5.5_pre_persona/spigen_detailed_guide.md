# spigen_detailed_guide.md — 보고용 상세 시스템 가이드 원문

> 목적: 발표용 요약 가이드가 아니라, **보고/구현/검수용 상세 시스템 가이드**를 정의한다.
> 기준: 기존 발표용 가이드의 **폰트 규칙 / spacing 규칙 / 카드 규칙 / 컴포넌트 규칙은 그대로 유지**한다.
> 확장: HTML 가이드 수준으로 **세부 설명·표·예외·검수 기준**을 추가한다.

---

## 0. 문서 성격

이 가이드는 아래 3가지 용도를 동시에 만족해야 한다.

1. **디자인 시스템 보고서**
   - 시스템을 이해관계자에게 설명할 수 있어야 한다.
2. **구현 명세서**
   - 개발자/에이전트가 그대로 구현할 수 있어야 한다.
3. **검수 기준서**
   - 결과물을 확인할 때 체크 포인트가 명확해야 한다.

즉 이 문서는 “예쁜 설명용 덱”이 아니라 아래 형식을 갖는 **명세 덱**이다.

```txt
원칙
→ 토큰
→ 규칙
→ 컴포넌트 anatomy
→ 선택 조건
→ 금지 조건
→ 예외
→ validator
→ appendix
```

---

## 1. 고정 기준

### 1.1 유지되는 규칙

아래는 기존 발표용 가이드와 **동일하게 유지**된다.

- 캔버스: `720 × 405pt`
- 색상 시스템: `BG / SURFACE / SURFACE_HI / TEXT / TEXT_DIM / TEXT_FAINT / ACCENT / ACCENT_DIM`
- 폰트 규칙:
  - 한글 포함 → `Noto Sans`
  - 그 외 → `Proxima Nova`
- 최소 폰트 크기: `7pt`
- type scale remap 규칙
- slide margin > block gap > body gap
- outer padding > inner gap
- small card no bullets
- structure = diagram only
- flow = one-row 우선
- mapping = card 내부 divider만 허용
- 강조 row/card는 항상 최상단

### 1.2 이 문서에서만 추가되는 것

- 규칙을 텍스트로 설명하는 **상세 표 페이지**
- 컴포넌트 anatomy의 **세부 항목 설명**
- 예외/실패 사례
- validator 기준 표
- appendix

---

## 2. 권장 페이지 구조

이 보고용 상세 가이드는 **24장 내외**를 기본으로 한다.

### Part A. Overview / Foundations
1. Cover
2. 문서 목적 / 적용 범위
3. 시스템 개요
4. 핵심 원칙
5. 캔버스 / 안전영역 / 콘텐츠 영역
6. 색상 시스템
7. 타이포그래피
8. spacing / grid / density
9. shape / divider / emphasis

### Part B. Components
10. page anatomy
11. rule grid / summary card anatomy
12. flow component anatomy
13. structure component anatomy
14. mapping component anatomy
15. chart / KPI anatomy
16. callout / conclusion anatomy

### Part C. Rules / Decision
17. layout selection matrix
18. typography remap table
19. spacing / padding decision table
20. connector / divider policy
21. emphasis / z-order policy
22. validator / review checklist

### Part D. Appendix
23. do / don’t 사례
24. known issue / fallback / exceptions

---

## 3. 페이지별 상세 명세

아래는 각 페이지에 반드시 포함할 내용이다.

### Page 1. Cover

**목적**
- 문서 제목과 버전을 명확히 제시한다.

**구성**
- 제목
- 부제
- 문서 성격: `보고용 상세 시스템 가이드`
- 버전 / 날짜

**주의**
- 발표용 표지와 동일 톤 유지
- 표지는 기존 가이드 시트 스타일을 유지해도 됨

---

### Page 2. 문서 목적 / 적용 범위

**목적**
- 이 문서가 무엇을 위한 것인지 명확히 한다.

**포함 항목**
- 적용 대상
  - 보고용 슬라이드
  - 시스템 가이드
  - 내부 구현 기준
- 제외 대상
  - 외부 홍보용 디자인 변주
  - 임의 스타일 실험
- 문서 역할
  - 설명
  - 구현
  - 검수

**권장 형태**
- 2열 또는 3열 grid card
- 카드형이지만 정보 밀도는 높아도 됨

---

### Page 3. 시스템 개요

**목적**
- 전체 시스템을 한 장에서 요약한다.

**포함 항목**
- design tokens
- component family
- selection rules
- validation layer

**권장 형태**
- flow + grouped blocks
- 커넥터 과다 사용 금지
- 그룹 배치로 읽히게 구성

---

### Page 4. 핵심 원칙

**포함 항목**
- 템플릿 우선
- 페이지당 메시지 하나
- 절제된 오렌지
- 의미가 형태를 결정
- off-canvas 금지
- small card no bullets

**권장 형태**
- 규칙 카드 grid
- 카드 내부는 plain text stack

---

### Page 5. 캔버스 / 안전영역 / 콘텐츠 영역

**목적**
- 720pt 기준 공간 구조를 정의한다.

**필수 항목**
- canvas size
- left/right margin
- header start
- content top
- content bottom
- safe area

**표 항목**
- 항목명
- 값
- 의미
- 금지 예시

---

### Page 6. 색상 시스템

**필수 표**
- token
- hex
- 역할
- 사용 위치
- 금지 위치

**추가 설명**
- accent는 1~3개 요소 이내
- accentDim은 카드 배경, 텍스트 색 금지

---

### Page 7. 타이포그래피

**필수 내용**
- font family rule
- size tier
- caption/body/title hierarchy
- 7pt minimum
- type scale remap table

**꼭 들어갈 표**
- 입력 크기
- 실제 적용 크기
- 사용 레벨

---

### Page 8. spacing / grid / density

**필수 내용**
- slide margin
- block gap
- title-body gap
- body-body gap
- outer padding
- inner gap
- density level

**핵심 문장**
- `slide margin > block gap > body gap`
- `outer padding > inner gap`

---

### Page 9. shape / divider / emphasis

**포함 항목**
- 직각 shape
- rounded 최소
- border weight
- divider는 thin rect
- 강조 카드 사용 조건
- 100% orange 금지 규칙

**권장 표 열**
- 요소
- 허용
- 금지
- 비고

---

### Page 10. page anatomy

**목적**
- 한 페이지 안의 헤더/본문/블록 구조를 정의한다.

**세부 항목**
- eyebrow
- title
- lead block
- body blocks
- summary block

**규칙**
- 바깥 여백보다 내부 블록 간격이 커지지 않음

---

### Page 11. rule grid / summary card anatomy

**포함 항목**
- small card
- summary card
- balanced card
- top-weighted card

**설명해야 할 것**
- 언제 balanced 인가
- 언제 top-weighted 인가
- 내부 라벨/타이틀/본문의 간격 구조

---

### Page 12. flow component anatomy

**필수 내용**
- one-row 우선
- step label
- title
- service
- arrow
- multiline 대응

**표 항목**
- 필드
- 의미
- 줄 수 규칙
- overflow 대응

---

### Page 13. structure component anatomy

**필수 내용**
- structure는 diagram only
- 카드 나열 fallback 금지
- connector 최소화 가능
- 배치로 구조를 읽히게 할 것

**포함 항목**
- input
- orchestrator / main node
- reference settings group
- output

---

### Page 14. mapping component anatomy

**필수 내용**
- left lane / middle relation / right lane
- divider는 카드 내부만
- gutter 요소 금지
- nested box 금지

**표 열**
- lane
- 역할
- 허용 요소
- 금지 요소

---

### Page 15. chart / KPI anatomy

**포함 항목**
- KPI card
- metric label
- value
- caption
- bar / axis / highlight

**규칙**
- 강조값 1개만
- 차트는 정보 우선
- 장식형 그라데이션 금지

---

### Page 16. callout / conclusion anatomy

**포함 항목**
- 결론 카드
- summary message
- detail bullets 없는 요약 구조
- conclusion → detail 패턴

**규칙**
- 한 페이지에 필요한 경우에만 강한 강조
- 무조건 orange fill 금지

---

### Page 17. layout selection matrix

**필수 표**
- page intent
- recommended component
- allowed variant
- avoid

예:
- problem/solution → compare
- process → flow
- architecture → structure
- relation table → mapping
- performance → chart / KPI

---

### Page 18. typography remap table

**목적**
- 구현자가 타입 스케일을 숫자로 바로 참조 가능하게 한다.

**필수 표**
- raw size
- rendered size
- typical use

---

### Page 19. spacing / padding decision table

**목적**
- 카드 내부/슬라이드 레벨 간격 결정을 수치로 본다.

**필수 열**
- context
- top/bottom padding
- title/body gap
- line gap
- align mode

---

### Page 20. connector / divider policy

**필수 내용**
- divider vs connector 구분
- native bent connector 기본 금지
- structure는 connector 최소화
- mapping은 card internal divider only

**형식**
- 규칙 표 + 금지 예시

---

### Page 21. emphasis / z-order policy

**필수 내용**
- 강조 카드 1순위 규칙
- 강조 row/card bring to front
- orange border가 가려지지 않게 할 것
- 강조 요소 남발 금지

---

### Page 22. validator / review checklist

**필수 항목**
- off-canvas 검사
- 7pt 미만 검사
- overflow 검사
- 내부 여백 검사
- nested box 검사
- structure diagram 여부
- mapping gutter 요소 검사
- orange z-order 검사

**형식**
- 체크 항목
- 자동/수동
- PASS 기준
- FAIL 시 조치

---

### Page 23. do / don’t 사례

**포함 항목**
- 좋은 예
- 나쁜 예
- 왜 안 되는지
- 대체 방식

**권장 형식**
- 좌우 비교 또는 2행 비교

---

### Page 24. known issue / fallback / exceptions

**포함 항목**
- multiline overflow 대응
- flow 단계 수가 많을 때
- structure connector가 어색할 때
- mapping 정보가 많을 때
- 차트 수치가 과밀할 때

**표 항목**
- 상황
- 증상
- fallback
- 최종 선택

---

## 4. 페이지 유형별 톤

### 설명형 페이지
- 원칙을 짧고 강하게
- 문장 수 적음
- 카드형 가능

### 명세형 페이지
- 표 중심
- 열 구조 명확
- 세부값 포함

### appendix 페이지
- 정보 밀도 높음
- 읽기용
- 발표용보다 문서용 우선

---

## 5. 작성 원칙

### 5.1 문장 스타일
- 애매한 감성 표현 금지
- 규칙 문장 우선
- “해야 한다 / 금지한다 / 허용한다” 형태 사용

### 5.2 표 스타일
- 열 제목은 짧고 명확하게
- 셀 안 문장도 최대한 짧게
- 비고는 필요한 경우만

### 5.3 시각 밀도
- 강연용보다 높아도 됨
- 단, 표 안에서도 hierarchy는 유지

---

## 6. 최종 산출물 기준

이 가이드는 아래 기준을 만족해야 완료다.

- 발표용 요약 가이드와 충돌하지 않는다.
- 기존 규칙(폰트/spacing/component)을 그대로 유지한다.
- HTML 가이드 수준으로 세부 항목이 충분하다.
- 구현자가 페이지를 보고 바로 코드를 짤 수 있다.
- 검수자가 페이지를 보고 PASS/FAIL 기준을 판정할 수 있다.

---

## 7. 다음 단계

이 문서를 기준으로 실제 구글슬라이드 가이드를 생성할 때는 아래 순서를 따른다.

1. 페이지 목차 확정
2. 각 페이지별 component 선택
3. 표 페이지용 템플릿 추가
4. appendix 페이지 생성
5. validator 기준 재확인

