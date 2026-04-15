# spigen_design_spec.md — 슬라이드 디자인 사양
> 각 슬라이드 유형의 시각 규격. slides-grab-design이 HTML 생성 시 참조.

## 슬라이드 디자인 사양 (slides-grab × Spigen)

**표지(slide-01.html)만 Spigen 브랜드 커버로 교체한다. 나머지 슬라이드는 slides-grab-design이 HTML로 생성한다.**

### 공통 디자인 토큰

| 토큰 | 값 | 용도 |
|-----|---|-----|
| accent | `#FF6900` | 강조선·번호·포인트 |
| 영문 폰트 | `Proxima Nova` (fallback `sans-serif`) | heading, display |
| 한글 폰트 | `Noto Sans KR`, `Noto Sans` | 한글 포함 모든 요소 |
| 섹션 배경 | `#1A1A1A` | section-divider 배경 |
| 섹션 텍스트 | `#FFFFFF` | section-divider 제목 |

### 슬라이드 유형별 디자인 사양 (slides-grab-design 가이드)

**표지 (Spigen 브랜드 커버) — 다크 테마**
- `#000000` 배경 / 상단 `#FF6900` 가로 바 (3pt)
- 대형 제목 (Proxima Nova/Noto Sans, 17pt, `#F9FAFB`, bold)
- 하단: 부서·담당자 (왼쪽) / 날짜·버전 (오른쪽)

**섹션 구분 (section-divider) — 다크 테마**
- `#000000` 풀블리드 배경 / 상단 `#FF6900` 가로 바
- 대형 번호 (Proxima Nova, 120pt, `#FF6900`, 좌측)
- 섹션 제목 (36pt, `#F9FAFB`, 번호 하단)
- 나머지 비움 — 텍스트 최소화

**일반 내용 (content) — 라이트 테마**
- `#FFFFFF` 배경 / 상단 `#FF6900` 가로 바 (3pt)
- 제목 (Proxima Nova/Noto Sans, 17pt, `#1A1A1A`, bold)
- 본문 (Noto Sans, 8.5pt, `#4A4A4A`, 줄간격 1.6)

**3열 항목 (statistics) — 라이트 테마**
- `#FFFFFF` 배경 / 상단 제목 (content와 동일)
- 카드 배경 `#F5F5F5`, 테두리 `#E5E5E5`
- 3개 균등 컬럼: `#FF6900` 번호 블록 + 소제목(bold) + 설명

---