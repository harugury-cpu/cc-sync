---
name: ckm:slides
description: Create strategic HTML presentations with Chart.js, design tokens, responsive layouts, copywriting formulas, and contextual slide strategies.
argument-hint: "[topic] [slide-count]"
metadata:
  author: claudekit
  version: "1.0.0"
---

# Slides

Strategic HTML presentation design with data visualization.

<args>$ARGUMENTS</args>

## When to Use

- Marketing presentations and pitch decks
- Data-driven slides with Chart.js
- Strategic slide design with layout patterns
- Copywriting-optimized presentation content

## NOT For (use spigen-slides instead)

- Spigen 내부 팀 발표 자료 (파트원 교육, 온보딩, 보고서, 가이드)
- Google Slides 출력이 필요한 모든 경우
- 한국어로 PPT/슬라이드/장표/발표자료/덱 요청이 들어온 경우
→ 위 경우는 반드시 `spigen-slides` 스킬을 먼저 로드한다. `ckm-slides`는 `spigen-slides`의 planning 단계에서 레이아웃 패턴 추천기로만 사용한다.

## Subcommands

| Subcommand | Description | Reference |
|------------|-------------|-----------|
| `create` | Create strategic presentation slides | `references/create.md` |

## References (Knowledge Base)

| Topic | File |
|-------|------|
| Layout Patterns | `references/layout-patterns.md` |
| HTML Template | `references/html-template.md` |
| Copywriting Formulas | `references/copywriting-formulas.md` |
| Slide Strategies | `references/slide-strategies.md` |

## Routing

1. Parse subcommand from `$ARGUMENTS` (first word)
2. Load corresponding `references/{subcommand}.md`
3. Execute with remaining arguments
