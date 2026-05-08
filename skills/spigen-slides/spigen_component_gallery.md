# spigen_component_gallery.md — 전체 컴포넌트 인벤토리
> 기획 단계(Step 1-4 아웃라인 작성 전)에 반드시 이 파일을 스캔하고, 각 슬라이드에 가장 적합한 후보를 2개 이상 비교한 뒤 선택한다.

---

## 구조 선택 전 필수 질문

슬라이드마다 아래 3가지를 먼저 답한다:

```
Q. 청중이 이 슬라이드에서 무엇을 해야 하는가?
   understand → 아래 결정 테이블로
   decide     → mk_decision_tree() 우선
   execute    → mk_flow_focus() 또는 mk_split_cards() 우선

Q. 항목들이 서로 독립적인가, 아니면 순서/관계가 있는가?
   독립       → 카드 계열 (3col-cards, rule-grid, feature-grid)
   순서/흐름  → 플로우 계열 (flow, flow-focus)
   관계       → 다이어그램 계열 (arch-layers, arch-orchestrator, swimlane, decision-tree)
   비교       → compare-rows, split

Q. 항목이 몇 개인가?
   2개 비교   → compare-rows, split
   3개        → 3col, 3col-cards
   4~6개      → flow, flow-focus, rule-grid
   7개 이상   → report-table, swimlane-mapping
```

---

## 카드 계열 — 독립 항목 나열

### `mk_3col_cards()` ★자주 씀★
- 언제: 독립적인 항목 3개를 동등하게 보여줄 때
- 예: 3가지 핵심 원칙 / 3가지 기능 / 3가지 이점
- 주의: 항목 간 순서나 관계가 있으면 쓰지 말 것

### `mk_3col()` ★자주 씀★
- 언제: 3열 텍스트 중심 내용 (카드보다 가벼운 버전)
- 예: 3개 섹션 요약 / 팀별 역할 간략 정리
- 3col_cards보다 텍스트 비중이 높을 때

### `mk_rule_grid()`
- 언제: 같은 비율의 규칙/가이드 카드 여러 개 (2열 그리드)
- 예: 디자인 규칙 목록 / 체크리스트 / 금지사항 나열
- 주의: 카드 혼합 패턴 안 됨 — 모든 카드가 동일 비율이어야 함

### `mk_feature_grid()`
- 언제: 기능/특징을 격자로 나열
- 예: 제품 기능 소개 / 서비스 구성 요소
- rule_grid와 비슷하나 더 feature 중심

### `mk_split_cards()` ★팀 액션 설명에 좋음★
- 언제: 왼쪽에 텍스트 설명 + 오른쪽에 관련 카드 4개
- 예: "해야 할 것" 설명 + 각 단계 카드 / 규칙 설명 + 항목 카드
- 텍스트 블록과 카드를 한 슬라이드에 같이 쓸 때

---

## 플로우 계열 — 순서/프로세스

### `mk_flow()` ★자주 씀★
- 언제: 프로세스 단계가 흐름으로 이어질 때 (비용/시간 정보 포함 가능)
- 예: 6단계 업무 프로세스 / 제품 출시 플로우
- mk_flow_focus()보다 카드가 작고 밀도 높음

### `mk_flow_focus()` ★프로세스가 메인일 때★
- 언제: 프로세스 자체가 슬라이드의 핵심 메시지일 때
- 예: "우리 팀이 해야 할 3단계" / 신규 워크플로 온보딩
- mk_flow()보다 카드가 크고 타이틀/본문 강조
- 최대 6단계, 단일 행 가로 배치

---

## 비교 계열 — Before/After, 좌우 대비

### `mk_compare_rows()` ★비교 슬라이드 전용★
- 언제: 현재 상태 vs 도입 후 상태 비교
- 예: 기존 프로세스 vs 새 프로세스 / 문제 vs 해결
- 좌측 카드(어두움) + 화살표 + 우측 카드(오렌지 틴트)
- callout 문구 추가 가능 (핵심 메시지 한 줄)

### `mk_split()`
- 언제: 좌우 두 영역에 다른 내용 (비교보다는 병렬 설명)
- 예: 임시영상 설명 + 공식영상 설명
- compare_rows보다 구분이 덜 강조됨

---

## 다이어그램 계열 — 관계/구조 설명

### `mk_swimlane_mapping()` ★팀 역할 분담에★
- 언제: 여러 행(팀/역할)이 각 열(단계/항목)에 매핑될 때
- 예: 팀별 업무 분담표 / 모듈 ↔ 데이터 매핑
- 최대 3행, 3열 구조
- **일반 표 대신 역할 시각화가 필요할 때 우선 고려**

### `mk_decision_tree()`
- 언제: 하나의 판단 기준에서 두 갈래로 분기할 때
- 예: "전작과 동일한가?" → Yes: 전작 영상 / No: 새 영상 제작
- 청중이 직접 판단/선택해야 하는 슬라이드에 사용

### `mk_arch_layers()`
- 언제: 입력→처리→출력 레이어 구조를 설명할 때
- 예: 시스템 아키텍처 / 데이터 파이프라인
- 최대 4개 레이어

### `mk_arch_orchestrator()`
- 언제: 모듈 간 호출/소유 관계를 설명할 때
- 예: main → engine → output 구조
- 화살표로 관계를 명시해야 할 때

---

## 텍스트/숫자 계열

### `mk_text_block()`
- 언제: 설명이 길고 구조화하기 어려울 때 텍스트 블록으로
- 예: 배경 설명 / 정책 본문 / 주의사항 나열

### `mk_callout_message()`
- 언제: 강조 메시지 하나를 크게 보여줄 때
- 예: "출하 전 게시 완료" 같은 단일 강조 룰

### `mk_kpi_dashboard()`
- 언제: KPI 수치 3~4개를 대시보드처럼 보여줄 때

### `chart_hbar` — 가로 막대 차트 ★
- 언제: 연도별·항목별 비율/수치를 막대 길이로 비교 (3~6개 항목)
- 예: 선호도 추이 / 카테고리별 점유율 / 항목별 달성률

```python
# ── 가로 막대 차트 ──────────────────────────────────────
data = [("2022", 35), ("2023", 42), ("2024", 38), ("2025", 51)]
BAR_X    = 100   # 막대 시작 x (항목 라벨 뒤)
BAR_MAX_W = 500  # 100%일 때 최대 너비 (pt)  ← 조정 포인트
BAR_H    = 20    # 막대 높이
ROW_H    = 34    # 행 높이 (막대 + 간격)
CHART_Y  = 160   # 차트 시작 y

for i, (label, val) in enumerate(data):
    ry = CHART_Y + i * ROW_H

    # 항목 라벨 (왼쪽, 오른쪽 정렬)
    yl = _uid()
    b._shape(pid, yl, 48, ry + 2, 46, BAR_H - 4, valign="MIDDLE")
    b._text(yl, label)
    b._style(yl, 7.5, color=b.c["dim"], align="END")

    # 배경 바 (전체 기준선)
    b._rect(pid, BAR_X, ry, BAR_MAX_W, BAR_H, b.c["surface"], b.c["surface"])

    # 전경 바 (비율만큼)
    bar_w = max(4, int(BAR_MAX_W * val / 100))
    b._rect(pid, BAR_X, ry, bar_w, BAR_H, b.c["accent"], b.c["accent"])

    # 수치 라벨 (막대 끝 오른쪽)
    pl = _uid()
    b._shape(pid, pl, BAR_X + bar_w + 6, ry + 2, 40, BAR_H - 4, valign="MIDDLE")
    b._text(pl, f"{val}%")
    b._style(pl, 8, bold=True, color=b.c["fg"])
```

---

### `chart_vbar` — 세로 막대 차트
- 언제: 기간별 수치 증감을 막대 높이로 비교 (2~6개 항목)
- 예: 분기별 매출 / 연도별 성장률 / 월별 출하량

```python
# ── 세로 막대 차트 ──────────────────────────────────────
data = [("Q1", 35), ("Q2", 52), ("Q3", 44), ("Q4", 61)]
COL_W        = 60    # 막대 너비  ← 조정 포인트
COL_GAP      = 20    # 막대 간격
BAR_MAX_H    = 150   # 최대값일 때 막대 높이 (pt)
MAX_VAL      = max(v for _, v in data)
CHART_X      = 120   # 차트 시작 x
CHART_BOTTOM = 320   # 바닥 기준선 y

for i, (label, val) in enumerate(data):
    cx    = CHART_X + i * (COL_W + COL_GAP)
    bar_h = max(4, int(BAR_MAX_H * val / MAX_VAL))
    bar_y = CHART_BOTTOM - bar_h

    # 배경 바 (전체 기준선)
    b._rect(pid, cx, CHART_BOTTOM - BAR_MAX_H, COL_W, BAR_MAX_H, b.c["surface"], b.c["surface"])

    # 전경 바
    b._rect(pid, cx, bar_y, COL_W, bar_h, b.c["accent"], b.c["accent"])

    # 수치 라벨 (막대 위)
    vl = _uid()
    b._shape(pid, vl, cx, bar_y - 16, COL_W, 14, valign="MIDDLE")
    b._text(vl, str(val))
    b._style(vl, 8, bold=True, color=b.c["fg"], align="CENTER")

    # 기간 라벨 (바닥 아래)
    ll = _uid()
    b._shape(pid, ll, cx, CHART_BOTTOM + 4, COL_W, 14, valign="MIDDLE")
    b._text(ll, label)
    b._style(ll, 7.5, color=b.c["dim"], align="CENTER")
```

---

### `chart_progress` — 단일 진척도 바
- 언제: 목표 대비 달성률 1개를 강조할 때
- 예: 출하 달성률 / 프로젝트 진행률

```python
# ── 단일 진척도 바 ──────────────────────────────────────
ratio    = 0.73   # 달성률 (0.0 ~ 1.0)
BAR_X, BAR_Y = 48, 200
BAR_W, BAR_H = 550, 28

b._rect(pid, BAR_X, BAR_Y, BAR_W, BAR_H, b.c["surface"], b.c["surface"])
fill_w = max(4, int(BAR_W * ratio))
b._rect(pid, BAR_X, BAR_Y, fill_w, BAR_H, b.c["accent"], b.c["accent"])

pct = _uid()
b._shape(pid, pct, BAR_X + fill_w + 8, BAR_Y + 2, 50, BAR_H - 4, valign="MIDDLE")
b._text(pct, f"{int(ratio * 100)}%")
b._style(pct, 10, bold=True, color=b.c["fg"])
```

### `mk_report_table()`
- 언제: 행이 많은 데이터 표 (7개 이상 항목)

---

## 고정 양식 계열 (내용 무관하게 구조 고정)

| 컴포넌트 | 용도 | 변경 가능 여부 |
|---------|-----|-------------|
| `mk_cover()` | 표지 | 텍스트만 교체 |
| `mk_section_divider()` | 섹션 구분 | 번호+제목만 |
| `mk_quote()` | 인용/강조 한 문장 | 텍스트만 교체 |
| `mk_contents()` / `mk_toc()` | 목차 | 섹션명만 교체 |

| `mk_kpi_status_detail()` | KPI 보고 전용 | 강제 지정 |
| `mk_kpi_dense_table()` | KPI 밀도 표 | 강제 지정 |

---

## 빠른 선택 가이드

```
"왜 바꾸는가" 슬라이드    → mk_compare_rows()
"어떻게 돌아가는가"       → mk_flow() 또는 mk_flow_focus()
"누가 무엇을 하는가"      → mk_swimlane_mapping()
"팀이 해야 할 것"         → mk_flow_focus() 또는 mk_split_cards()
"선택/판단 기준"          → mk_decision_tree()
"3가지 원칙/특징"         → mk_3col_cards()
"꼭 지켜야 할 규칙"       → mk_callout_message() 또는 mk_rule_grid()
"시스템 구조"             → mk_arch_layers() 또는 mk_arch_orchestrator()
"핵심 한 문장"            → mk_quote()
```
