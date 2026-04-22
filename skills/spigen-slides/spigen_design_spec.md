# spigen_design_spec.md — 디자인 시스템
> 캔버스: **1920 × 1080 pt** · 단위: pt (1pt = 12700 EMU)

---

## 색상 토큰

| 토큰 | 값 | 역할 |
|-----|---|-----|
| `Accent` | `#FF6B1A` | Primary · CTA · 강조선 · 번호 · 포인트 |
| `Accent Dim` | `rgba(255,107,26,0.24)` | Fill · Hover (다크 배경 위) |
| `Accent Line` | `rgba(255,107,26,0.55)` | 강조 Border |
| `Good` | `#9CE37D` | Positive · 긍정 상태 |
| `Bad` | `#FF7A7A` | Negative · 부정 상태 |
| `BG` | `#000000` | Base · 다크 슬라이드 배경 |
| `Surface` | `#0E0E0E` | Card 배경 (다크) |
| `Border` | `rgba(255,255,255,0.08)` | Divider · 카드 테두리 (다크) |

> Google Slides API는 alpha 미지원 → `Accent Dim` / `Accent Line` / `Border`는 솔리드 근사값으로 대체:
> - `Accent Dim` ≈ `#3D1A05`
> - `Border` ≈ `#141414`

---

## 타이포그래피 스케일

| 레벨 | 크기(pt) | 굵기 | 용도 |
|-----|--------|-----|-----|
| `DISPLAY` | 84 | 800 | 표지 제목 |
| `H1 · TITLE` | 64 | 700 | 페이지 제목 |
| `H2 · HERO` | 40 | 600 | 핵심 한 줄 · Lead copy |
| `BODY LG` | 22 | 500 | Intro · 불릿 리스트 |
| `BODY` | 18 | 400 | 본문 · 카드 텍스트 |
| `CAPTION · LABEL` | 14 | 600 | Eyebrow · 푸터 · 배지 |

---

## 폰트

| 종류 | 폰트 스택 | 적용 |
|-----|---------|-----|
| SANS | `Proxima Nova` / `Mona Sans` / `Noto Sans KR` | 제목·본문 전반 |
| MONO | `JetBrains Mono` | 코드 · 수치 · 기술값 |

**적용 규칙:**
- 한글 포함 텍스트 → `Noto Sans KR`
- 영문·숫자 전용 → `Proxima Nova` (없으면 `Mona Sans`)
- 코드·hex·수치 표기 → `JetBrains Mono`

---

## 스페이싱 스케일

| 스텝 | 값 |
|-----|----|
| xs  | 4  |
| sm  | 8  |
| md  | 12 |
| lg  | 16 |
| xl  | 24 |
| 2xl | 32 |
| 3xl | 48 |
| 4xl | 64 |
| 5xl | 96 |

---

## 테마별 색상 매핑

### Dark (표지 · 섹션 구분 · closing · flow · quote)

| 요소 | 값 |
|-----|---|
| 슬라이드 배경 | `#000000` |
| 상단 강조 바 | `#FF6B1A`, 3pt |
| 제목 | `#FFFFFF`, DISPLAY or H1 |
| 본문 | `#6B7280`, BODY |
| 카드 배경 | `#0E0E0E` (Surface) |
| 카드 테두리 | `#141414` (Border 근사) |
| 번호 · 포인트 | `#FF6B1A` |

### Light (content · statistics · text-block · split-layout · split-cards)

| 요소 | 값 |
|-----|---|
| 슬라이드 배경 | `#FFFFFF` |
| 상단 강조 바 | `#FF6B1A`, 3pt |
| 제목 | `#1A1A1A`, H1 |
| 본문 | `#4A4A4A`, BODY |
| 카드 배경 | `#F5F5F5` |
| 카드 테두리 | `#E5E5E5` |

### Warm (toc)

| 요소 | 값 |
|-----|---|
| 슬라이드 배경 | `#F5F0E8` |
| 제목 | `#1A1A1A`, H1 |
| 본문 | `#4A4A4A`, BODY |
| 카드 배경 | `#FFFFFF` |
| 카드 테두리 | `#C8C4BE` |

---

## 슬라이드 유형별 사양

**표지 (cover) — Dark**
- 배경 `#000000` / 상단 Accent 바 3pt
- 제목: DISPLAY 84pt/800, `#FFFFFF`, Proxima Nova
- 부제목: H2 40pt/600, `#6B7280`
- 하단 메타: CAPTION 14pt/600, 좌(부서·담당자) / 우(날짜·버전)

**섹션 구분 (section-divider) — Dark**
- 배경 `#000000` / 상단 Accent 바 3pt
- 대형 번호: 120pt, `#FF6B1A`, Proxima Nova, 좌측
- 섹션 제목: H1 64pt/700, `#FFFFFF`, 번호 하단
- 나머지 비움 — 포스터 스타일

**일반 내용 (content) — Light**
- 배경 `#FFFFFF` / 상단 Accent 바 3pt
- 제목: H1 64pt/700, `#1A1A1A`
- 본문: BODY 18pt/400, `#4A4A4A`, 줄간격 1.6
- 글머리 3줄 이내

**3열 항목 (statistics) — Light**
- 카드 배경 `#F5F5F5`, 테두리 `#E5E5E5`
- 3열 균등: Accent 번호 블록 + 소제목(BODY LG/bold) + 설명(BODY)

**closing — Dark**
- 표지와 동일 구조, CTA 또는 결론 한 줄 중앙 배치
