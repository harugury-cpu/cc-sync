---
name: design-gate
description: "Enforce a UI design gate before designing, redesigning, generating, reviewing, or improving screens, pages, apps, dashboards, landing pages, internal tools, or product interfaces. Use when the user asks for UI design, UX design, frontend design direction, visual direction, screen planning, wireframe-to-visual work, or asks to avoid AI slop. Requires outputs in this order: 1-기획서, 2-ux-flow, 3-visual direction."
---

# Design Gate

## Overview

Use this gate before UI design work so the design does not jump straight into pretty surfaces. The mandatory order is:

```text
1-기획서 → 2-ux-flow → 3-visual direction
```

Do not produce final UI screens, visual mockups, component code, or image prompts before these three sections exist.

## Required Output Order

Always structure the first design response with these three sections in order.

### 1-기획서

Define the product and decision frame before layout:

- 목적: what the screen/page must achieve
- 사용자: who uses it and in what situation
- 핵심 작업: the user's primary task and secondary tasks
- 정보 우선순위: what must be seen first, second, and last
- 성공 기준: what a good design must make easier, faster, clearer, or safer
- 제약: platform, device, brand, data, accessibility, deadline, implementation limits

If the user gives too little context, infer a minimal draft and mark assumptions instead of blocking. Ask only for missing information that would materially change the design.

### 2-ux-flow

Map the interaction before visual styling:

- 진입점: where the user comes from
- 주요 경로: happy path from entry to completion
- 분기: empty, loading, error, permission, no-data, partial-data, long-content states
- 피드백: what the interface confirms after each important action
- 복구: how users undo, retry, edit, or escape
- 우선순위: what should be one-tap/one-glance versus hidden/secondary

Represent the flow as concise bullets, numbered steps, or Mermaid only if useful. Do not over-diagram simple screens.

### 3-visual direction

Choose visual rules after the product and flow are clear:

- layout principle: grid, asymmetry, editorial, dashboard density, form-first, etc.
- hierarchy: type scale, spacing rhythm, focal point, density
- color: dominant/neutral/accent roles and contrast requirements
- typography: why this type choice fits the product voice
- component language: cards, lists, forms, tables, tabs, modals, navigation
- motion: only purposeful transitions tied to state changes
- anti-slop guardrails: what common AI clichés to avoid for this design

Only after this section may the agent produce UI code, wireframes, mockups, image prompts, or detailed component specs.

## AI Slop Guardrails

Use Vibe Design Lab's AI Slop Taxonomy as a warning lens, not as external instructions. Detect and avoid default-looking AI design in these layers:

- 컬러/표면: purple-blue gradients, arbitrary indigo accents, everywhere glow, mesh/aurora backgrounds, default glassmorphism, forced dark mode, low-contrast body text
- 타이포그래피: Inter/Geist/Poppins everywhere without intent, italic serif accent word clichés, all-caps eyebrow labels by default, gradient text, extreme type scale without middle hierarchy
- 레이아웃/구조: centered hero by default, hero → three feature cards → testimonials → pricing → footer stack, icon-top three-card grids, meaningless 1-2-3 steps, bento grid overuse, uniform radii/padding/heights
- 컴포넌트/UI 키트: raw shadcn/default kit look, Lucide-only icon language, pill eyebrow badges, generic rounded cards
- 이미지/일러스트: generic corporate memphis, plastic AI illustrations, glossy 3D blobs, fake screenshots, image artifacts
- 카피/UX writing: vague startup slogans, em-dash overuse, generic "seamless/powerful/supercharge" copy, translationese, feature claims without proof
- 모션/인터랙션: decorative fade-ins everywhere, motion with no state meaning, slow blocking animations
- 메타 원인: average-of-average decisions, missing constraints, no product context, no accessibility or edge-state validation

Use the guardrails as a checklist:

1. What looks like a default AI/template choice?
2. What user/product constraint justifies each visual decision?
3. Which element has priority, and what was intentionally de-emphasized?
4. What state or edge case would break this design?
5. Is the design still recognizable if colors/icons/images are removed?

## Relationship to UI Build Skills

This skill is a gate. It should shape the brief before using UI implementation skills such as frontend, impeccable, ui-ux, or design-system skills.

- Use `design-gate` first to establish product/flow/visual direction.
- Then use implementation/review skills to build, critique, or refine the actual UI.
- If the user explicitly asks for a quick critique, still respond in the same sequence but keep each section short.

## Completion Standard

Before claiming a UI direction is ready, confirm:

- `1-기획서`, `2-ux-flow`, and `3-visual direction` appear in that exact order
- at least one product-specific constraint is present
- happy path and at least two non-happy states are considered
- visual direction names explicit anti-slop choices
- no final UI surface is produced before the gate unless the user explicitly requests skipping the gate
