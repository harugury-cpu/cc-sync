---
name: anti-ai-design
description: Use when creating any UI, slides, visual design, layout, or any design-related task. Prevents generic AI design patterns and enforces premium, human-quality visual decisions. Trigger keywords: design, UI, layout, slide, 디자인, 슬라이드, 레이아웃, 화면, 인터페이스, 카드, 스타일, 시각.
---

# Anti-AI Design Protocol

AI가 기본적으로 생성하는 디자인 패턴을 차단하고, 사람이 만든 것처럼 보이는 시각적 결정을 강제한다.

## 1. 절대 금지 (BANNED)

### 폰트
- Inter, Roboto, Arial, Open Sans, Helvetica → AI 기본값. 사용 금지
- 대체: Geist, Outfit, Cabinet Grotesk, Satoshi, Plus Jakarta Sans, Switzer

### 색상 패턴
- 보라/파란 글로우, 네온 그라디언트 → "AI Purple" 패턴. 사용 금지
- 강조색은 최대 1개. 채도 80% 이하
- 배경 전체에 원색(파란색, 초록색, 빨간색) 사용 금지
- 절대 검정(#000000) 텍스트 금지 → 오프블랙(#111111, #1A1A1A) 사용

### 레이아웃
- 완전 중앙 정렬 Hero 섹션 → 레이아웃 변화가 없으면 금지
- 균일한 3열 Bootstrap 그리드 → 비대칭 구성으로 대체
- 카드 남용 → elevation이 계층을 표현할 때만 카드 사용

### 아이콘
- 굵은 선 Lucide, FontAwesome, Material Icons → 사용 금지
- 대체: Phosphor Light, Radix Icons (ultra-light, precise lines)

### 카피라이팅
- "Elevate", "Seamless", "Unleash", "Next-Gen", "Game-changer", "Delve" → AI 클리셰. 사용 금지
- 구체적이고 평이한 언어 사용

### 모션
- `linear`, `ease-in-out` → AI 기본 easing. 사용 금지
- 대체: Spring physics (`stiffness: 100, damping: 20`) 또는 `cubic-bezier(0.32, 0.72, 0, 1)`

### 기타
- 이모지를 코드, 마크업, 제목에 사용 금지 → 아이콘 또는 SVG로 대체
- "Lorem Ipsum", "John Doe", "Acme Corp" → 실제처럼 보이는 컨텍스트 기반 콘텐츠로 대체
- 일반적인 drop shadow (`shadow-md`, `rgba(0,0,0,0.3)`) → 배경색 틴트를 섞은 diffuse shadow

## 2. 타이포그래피 원칙

- 헤드라인: `tracking-tighter`, `leading-none` (tight tracking이 프리미엄감)
- 본문: `max-w-[65ch]`, `leading-relaxed` (가독성 라인 길이 제한)
- 텍스트 색상은 절대 검정 금지 → `#111111` 또는 `#1A1A1A`
- 보조 텍스트: `#6B7280` 또는 `#787774` (너무 연하면 저렴해 보임)

## 3. 레이아웃 원칙

- 여백을 2배로. 섹션 패딩은 `py-24` ~ `py-40`
- 비대칭 분할 (50/50 Split, 좌측 텍스트/우측 이미지, 비대칭 화이트스페이스)
- 복잡한 flexbox % 계산 금지 → CSS Grid 사용
- 전체 너비: `max-w-[1400px] mx-auto` 또는 `max-w-7xl`

## 4. 컴포넌트 원칙

### 카드
- 카드 테두리: 1px solid, 낮은 투명도 (`border border-black/5` 또는 `#EAEAEA`)
- 그림자: 극도로 diffuse하고 낮은 투명도 (opacity < 0.05)
- 카드 radius: `8px` ~ `12px` (pill 형태의 큰 카드 금지)

### 버튼
- Primary: 단색 배경 + hover시 `scale(0.98)` 또는 미세 색상 변화
- 아이콘이 있는 버튼: 아이콘을 별도 원형 wrapper 안에 넣기 (naked 배치 금지)

### 색상 비율 (60-30-10 규칙)
- 60%: 배경색
- 30%: 텍스트, 카드, 중립 요소
- 10%: 강조색 (한 화면에 3개 이하 요소에만)

## 5. 실행 체크리스트

디자인 생성 전 묵시적으로 확인:
- [ ] 금지된 폰트를 사용하지 않는가?
- [ ] 강조색이 1개이고 채도 80% 이하인가?
- [ ] 레이아웃이 중앙 정렬 일변도가 아닌가?
- [ ] 카드가 남용되지 않는가?
- [ ] 여백이 충분한가? (답답하면 2배)
- [ ] AI 카피라이팅 클리셰가 없는가?
- [ ] 이모지가 없는가?
- [ ] 그림자가 과하지 않은가?
